"""[2026-07-31] 全天の露出マップ (HEALPix) を FT2 から計算する。

`compute_exposure_map_targets.py` は 6 天体の ROI だけを対象にしていたが、
統計検証のために解析対象が 80 天体規模になったため、**一度だけ全天で作って
以後どの天体でも使い回す**方式に変える。天体を追加するたびに FT2 を
再ダウンロードして数時間待つ、という無駄が無くなる。

**有効面積のモデルは天の川用 (`compute_exposure_map_allbins`) を import して共有する。**
ここで別のモデルを書くと結果が比較できなくなるため。したがって [ASSUMPTION] も同一:
  - 公式 IRF が無いため Pass 8 の on-axis 実効面積の概形を対数補間で模す
  - 角度依存は cos(theta)^0.5、theta >= 65° はカット
  - エネルギー依存と角度依存が分離できると仮定する

解像度: NSIDE = 32 (12,288 画素、画素幅 1.8°)。露出は掃天観測の首振りで決まるため
天球上で滑らかで (天の川 ROI の実測で 120° あたり 63% p-p ≒ 0.5%/deg)、
1.8° 刻みからの内挿誤差は無視できる。実際に既存の 6 天体の 1° 接平面マップと
突き合わせて検証する (`audit_exposure_allsky_vs_targets.py`)。

出力: data/fermi_exposure/expmap_allsky_healpix.npz
  expmaps (13, 12288) [cm^2 s] / nside / bin_centers / n_weeks_ok
"""
from __future__ import annotations

import json
import os
import pathlib as _pathlib
import subprocess
import sys
import time
from concurrent.futures import Future, ThreadPoolExecutor, FIRST_COMPLETED, wait

import numpy as np
from numpy.typing import NDArray
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u
import healpy as hp

sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))
import compute_exposure_map_allbins as _mw   # 有効面積モデルを共有する

BASE = _pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = BASE / "data/fermi_exposure"
OUT_DIR.mkdir(parents=True, exist_ok=True)
TMP_DIR = _pathlib.Path("/tmp/fermi_ft2_allsky")
TMP_DIR.mkdir(parents=True, exist_ok=True)
OUT_NPZ = OUT_DIR / "expmap_allsky_healpix.npz"
CKPT = OUT_DIR / "expmap_allsky_checkpoint.npz"
PROGRESS = OUT_DIR / "expmap_allsky_progress.json"

NSIDE = int(os.environ.get("EXPMAP_NSIDE", 32))
WEEKS: list[int] = list(range(9, 789))
BIN_CENTERS = _mw.BIN_CENTERS
N_BINS = _mw.N_BINS
N_DOWNLOAD_WORKERS = int(os.environ.get("FT2_DL_WORKERS", 8))
CHUNK_T = 500          # 画素数が多いので時間チャンクを小さくしてメモリを抑える

_AEFF = np.array([_mw.aeff_onaxis(e) for e in BIN_CENTERS])
N_PIX = hp.nside2npix(NSIDE)
_lon, _lat = hp.pix2ang(NSIDE, np.arange(N_PIX), lonlat=True)
PIXEL_XYZ = _mw.lb_to_xyz(_lon, _lat).T          # (N_PIX, 3) float32


def download_week(week: int) -> tuple[int, _pathlib.Path | None]:
    url = (f"https://heasarc.gsfc.nasa.gov/FTP/fermi/data/lat/weekly/spacecraft/"
           f"lat_spacecraft_weekly_w{week:03d}_p310_v001.fits")
    fname = TMP_DIR / f"ft2_w{week:03d}.fits"
    try:
        proc = subprocess.run(["wget", "-q", "--timeout=300", "-t", "2", url, "-O", str(fname)],
                              timeout=600)
    except subprocess.TimeoutExpired:
        fname.unlink(missing_ok=True)
        return week, None
    if proc.returncode != 0 or not fname.exists() or fname.stat().st_size < 1e4:
        fname.unlink(missing_ok=True)
        return week, None
    return week, fname


def accumulate_week(fname: _pathlib.Path, expmaps: NDArray[np.float64]) -> bool:
    try:
        with fits.open(str(fname)) as hdul:
            sc = hdul[1].data
            ra_z = sc["RA_SCZ"].astype(np.float32)
            dec_z = sc["DEC_SCZ"].astype(np.float32)
            live = sc["LIVETIME"].astype(np.float32)
            gal = SkyCoord(ra=ra_z * u.deg, dec=dec_z * u.deg, frame="icrs").galactic
            l_sc = gal.l.deg.astype(np.float32)
            b_sc = gal.b.deg.astype(np.float32)
    except Exception:
        return False
    finally:
        fname.unlink(missing_ok=True)

    for start in range(0, len(l_sc), CHUNK_T):
        end = min(start + CHUNK_T, len(l_sc))
        sc_xyz = _mw.lb_to_xyz(l_sc[start:end], b_sc[start:end]).T
        cos_theta = np.clip(sc_xyz @ PIXEL_XYZ.T, -1.0, 1.0)
        shape = _mw.theta_shape_factor(np.degrees(np.arccos(cos_theta)))
        base = (shape * live[start:end, np.newaxis]).sum(axis=0)
        for ib, a0 in enumerate(_AEFF):
            expmaps[ib] += a0 * base
        del sc_xyz, cos_theta, shape, base
    return True


def load_checkpoint() -> tuple[NDArray[np.float64], dict[str, object]]:
    if CKPT.exists() and PROGRESS.exists():
        return np.load(CKPT)["expmaps"], json.loads(PROGRESS.read_text())
    return np.zeros((N_BINS, N_PIX), dtype=np.float64), {"done": [], "n_ok": 0}


def main() -> None:
    expmaps, prog = load_checkpoint()
    done = set(prog["done"])                    # type: ignore[arg-type]
    remaining = [w for w in WEEKS if w not in done]
    print(f"全天露出マップ: NSIDE={NSIDE} ({N_PIX}px), {len(WEEKS)}週中 {len(remaining)}週 未処理 "
          f"(DL並列={N_DOWNLOAD_WORKERS})", flush=True)
    t0 = time.time()

    with ThreadPoolExecutor(max_workers=N_DOWNLOAD_WORKERS) as dl_ex:
        n_done = n_fail = 0
        queue = list(remaining)
        dl_week_of: dict[Future, int] = {}
        pending: set[Future] = set()

        def refill() -> None:
            while queue and len(pending) < 16:
                wk = queue.pop(0)
                fut = dl_ex.submit(download_week, wk)
                dl_week_of[fut] = wk
                pending.add(fut)

        refill()
        while pending:
            finished, pending = wait(pending, return_when=FIRST_COMPLETED)
            for fut in finished:
                week = dl_week_of.pop(fut)
                _, fname = fut.result()
                if fname is None or not accumulate_week(fname, expmaps):
                    n_fail += 1
                    continue
                prog["done"].append(week)                   # type: ignore[union-attr]
                prog["n_ok"] = int(prog["n_ok"]) + 1        # type: ignore[arg-type]
                n_done += 1
                if n_done % 20 == 0:
                    np.savez(CKPT, expmaps=expmaps)
                    PROGRESS.write_text(json.dumps(prog))
                    el = (time.time() - t0) / 60.0
                    rate = n_done / max(el, 1e-9)
                    print(f"  {n_done}/{len(remaining)}週 (失敗{n_fail}, {rate:.2f}週/分, "
                          f"ETA {(len(remaining)-n_done)/max(rate,1e-9):.0f}分)", flush=True)
            refill()

    np.savez(CKPT, expmaps=expmaps)
    PROGRESS.write_text(json.dumps(prog))
    np.savez(OUT_NPZ, expmaps=expmaps, nside=NSIDE, bin_centers=BIN_CENTERS,
             n_weeks_ok=int(prog["n_ok"]))                  # type: ignore[arg-type]
    print(f"\n完了: {n_done}週処理, {n_fail}週失敗, {(time.time()-t0)/60:.1f}分")
    m = expmaps[5]
    print(f"  Bin6 露出: 平均={m.mean():.3e} 最小={m.min():.3e} 最大={m.max():.3e} cm^2 s")
    print(f"→ {OUT_NPZ}")


if __name__ == "__main__":
    main()
