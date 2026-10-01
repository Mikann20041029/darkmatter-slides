"""[2026-07-28] 他天体 (矮小銀河 5 天体 + M31) の ROI 露出マップを FT2 から計算する。

天の川用の `compute_exposure_map_allbins.py` は |l|,|b| <= 60° の 120x120 グリッド専用で、
対象 6 天体は全て範囲外 (Draco l=86.4 / Sculptor l=-72.5 / Ursa Minor l=105.0 /
Segue 1 l=-139.5 / Coma Ber l=-118.1 / M31 l=121.2)。そこで各天体の接平面 ROI 上で
同じ手順の露出を計算する。

**有効面積のモデルは天の川用と同一のものを import して使う** (`aeff_onaxis` /
`theta_shape_factor`)。ここで別のモデルを書くと、天の川と他天体の結果が
比較できなくなるため。したがって [ASSUMPTION] も同一:
  - 公式 IRF が無いため Pass 8 の on-axis 実効面積の概形を対数補間で模す
  - 角度依存は cos(theta)^0.5、theta >= 65° はカット
  - エネルギー依存と角度依存が分離できると仮定する

グリッド: `target_geometry.make_grid` の接平面 (gnomonic) 投影。
半幅 12° / 刻み 1° = 24x24 = 576 px を 6 天体分 (計 3,456 px) 同時に積算する
(天の川の 14,400 px より小さいので前回より軽い)。
フィットは半幅 10° / 0.125° で行い、この 1° マップを双線形補間して使う
(天の川と同じ近似。補間誤差は `audit_exposure_interp.py` で最大 0.15% と定量済み)。

FT2 は 1 週 2.8 MB (光子ファイルの 1/68) と軽い。780 週で計 2.2 GB。

出力: data/fermi_exposure/expmap_targets.npz
  expmaps   (n_target, 13, 24, 24) [cm^2 s]
  l_grid / b_grid / domega  (n_target, 24, 24)  [deg, deg, sr]
  names, bin_centers, half_deg, step_deg, n_weeks_ok
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

sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))
import target_geometry as tg
# 天の川と同一の有効面積モデルを使う (別実装にしない)
import compute_exposure_map_allbins as _mw

BASE = _pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = BASE / "data/fermi_exposure"
OUT_DIR.mkdir(parents=True, exist_ok=True)
TMP_DIR = _pathlib.Path("/tmp/fermi_ft2_targets")
TMP_DIR.mkdir(parents=True, exist_ok=True)
OUT_NPZ = OUT_DIR / "expmap_targets.npz"
CKPT = OUT_DIR / "expmap_targets_checkpoint.npz"
PROGRESS = OUT_DIR / "expmap_targets_progress.json"

WEEKS: list[int] = list(range(9, 789))
BIN_CENTERS = _mw.BIN_CENTERS
N_BINS = _mw.N_BINS
# [2026-07-28] 光子ファイルの取得と同時に走らせても本機 (4 コア / RAM 5.8 GB) が
# 詰まらないよう、既定の DL 並列を 4 に抑える。単独で走らせるなら 12 でよい。
N_DOWNLOAD_WORKERS = int(os.environ.get("FT2_DL_WORKERS", 4))
CHUNK_T = 2000

_ANCHOR_AEFF = np.array([_mw.aeff_onaxis(e) for e in BIN_CENTERS])  # (13,)

# ── 6 天体の ROI グリッドを作る ─────────────────────────────────────────────
NAMES: list[str] = [t[0] for t in tg.TARGETS]
_grids = []
for _name in NAMES:
    _l0, _b0 = tg.target_lb(_name)
    _xi, _eta, _lg, _bg, _dom = tg.make_grid(_l0, _b0, tg.ROI_HALF_DEG_EXP, tg.EXP_STEP_DEG)
    _grids.append((_lg, _bg, _dom))
L_GRIDS = np.stack([g[0] for g in _grids])      # (n_t, n, n)
B_GRIDS = np.stack([g[1] for g in _grids])
DOMEGAS = np.stack([g[2] for g in _grids])
N_TARGET, NG, _ = L_GRIDS.shape
N_PIX = N_TARGET * NG * NG

PIXEL_XYZ = _mw.lb_to_xyz(L_GRIDS.ravel(), B_GRIDS.ravel()).T   # (N_PIX, 3) float32


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
    """expmaps: shape (N_BINS, N_PIX) に in-place 加算する。"""
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

    n_t = len(l_sc)
    for start in range(0, n_t, CHUNK_T):
        end = min(start + CHUNK_T, n_t)
        sc_xyz = _mw.lb_to_xyz(l_sc[start:end], b_sc[start:end]).T   # (chunk, 3)
        cos_theta = np.clip(sc_xyz @ PIXEL_XYZ.T, -1.0, 1.0)          # (chunk, N_PIX)
        theta_deg = np.degrees(np.arccos(cos_theta))
        shape = _mw.theta_shape_factor(theta_deg)
        base = (shape * live[start:end, np.newaxis]).sum(axis=0)      # (N_PIX,)
        for ib, a0 in enumerate(_ANCHOR_AEFF):
            expmaps[ib] += a0 * base
        del sc_xyz, cos_theta, theta_deg, shape, base
    return True


def load_checkpoint() -> tuple[NDArray[np.float64], dict[str, object]]:
    if CKPT.exists() and PROGRESS.exists():
        return np.load(CKPT)["expmaps"], json.loads(PROGRESS.read_text())
    return np.zeros((N_BINS, N_PIX), dtype=np.float64), {"done": [], "n_ok": 0}


def save_checkpoint(expmaps: NDArray[np.float64], prog: dict[str, object]) -> None:
    np.savez(CKPT, expmaps=expmaps)
    PROGRESS.write_text(json.dumps(prog))


def main() -> None:
    expmaps, prog = load_checkpoint()
    done = set(prog["done"])            # type: ignore[arg-type]
    remaining = [w for w in WEEKS if w not in done]
    print(f"他天体 露出マップ: {len(WEEKS)}週中 {len(remaining)}週 未処理 "
          f"({N_TARGET}天体 x {NG}x{NG} = {N_PIX}px, {N_BINS}ビン同時, "
          f"DL並列={N_DOWNLOAD_WORKERS})", flush=True)
    t0 = time.time()

    with ThreadPoolExecutor(max_workers=N_DOWNLOAD_WORKERS) as dl_ex:
        n_done = n_fail = 0
        queue = list(remaining)
        dl_week_of: dict[Future, int] = {}
        pending: set[Future] = set()

        def refill() -> None:
            # FT2 は 1 本 2.8 MB と軽いが、溜め込む理由も無いので同時 16 本までにする
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
                if fname is None:
                    n_fail += 1
                    continue
                if not accumulate_week(fname, expmaps):
                    n_fail += 1
                    continue
                prog["done"].append(week)                   # type: ignore[union-attr]
                prog["n_ok"] = int(prog["n_ok"]) + 1        # type: ignore[arg-type]
                n_done += 1
                if n_done % 20 == 0:
                    save_checkpoint(expmaps, prog)
                    el = (time.time() - t0) / 60.0
                    rate = n_done / max(el, 1e-9)
                    print(f"  {n_done}/{len(remaining)}週 完了 (失敗{n_fail}, "
                          f"{rate:.1f}週/分, ETA {(len(remaining)-n_done)/max(rate,1e-9):.0f}分)",
                          flush=True)
            refill()

    save_checkpoint(expmaps, prog)
    maps = expmaps.reshape(N_BINS, N_TARGET, NG, NG).transpose(1, 0, 2, 3)
    np.savez(OUT_NPZ, expmaps=maps, l_grid=L_GRIDS, b_grid=B_GRIDS, domega=DOMEGAS,
             names=np.array(NAMES), bin_centers=BIN_CENTERS,
             half_deg=tg.ROI_HALF_DEG_EXP, step_deg=tg.EXP_STEP_DEG,
             n_weeks_ok=int(prog["n_ok"]))                  # type: ignore[arg-type]
    print(f"\n完了: {n_done}週処理, {n_fail}週失敗, {(time.time()-t0)/60:.1f}分")
    for it, name in enumerate(NAMES):
        m = maps[it, 5]     # Bin6 (20.76 GeV)
        print(f"  {name:12s} Bin6 露出 平均={m.mean():.3e} 最小={m.min():.3e} "
              f"最大={m.max():.3e} cm^2 s (振れ幅 {100*(m.max()-m.min())/m.mean():.1f}%)")
    print(f"→ {OUT_NPZ}")


if __name__ == "__main__":
    main()
