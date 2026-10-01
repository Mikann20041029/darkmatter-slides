"""
Fermi-LAT 露出マップ（Exposure Map）— Totani 13 ビン全てに拡張

2026-07-11: code/compute_exposure_map.py (Bin6専用) を全13ビンに一般化した版。
FT2（スペースクラフト姿勢データ）は光子エネルギーに依存しないため、
780週分のFT2を1回走査するだけで13ビン全ての露出マップを同時に積算できる
（13回ダウンロードし直す必要はない）。

[ASSUMPTION] 有効面積のエネルギー依存性について:
  本解析には Fermi Science Tools の公式IRF (P8R3_SOURCE_V3等) が無いため、
  gtexposure 相当の厳密計算はできない。代わりに、Pass 8 SOURCE class の
  一般的な性能（Atwood+2009, Ackermann+2012 Pass 7/8 performance paper 群に
  記載される概形: ~1 GeV 未満で急減、数GeV〜数百GeVでほぼプラトー、
  それ以上でやや減少）を模した滑らかな対数補間モデルを用いる。
  角度依存性 A_eff(θ) の形状は既存の compute_exposure_map.py (Bin6用) と
  同一と仮定し、エネルギー依存性は on-axis 実効面積の比でスケールする
  （角度分布とエネルギー分布が分離可能という近似）。
  これは厳密な計算ではなく近似であることを明記する。

出力: data/fermi_exposure/expmap_allbins.npz
        - "expmaps": shape (13, 120, 120)  各ビンの露出マップ [cm²·s]
        - "bin_centers": shape (13,)  ビン中心エネルギー [GeV]
"""
import pathlib as _pathlib
import sys
sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))

import os
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor, FIRST_COMPLETED, wait

import numpy as np
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u

import plot_skymap_all_subtracted as _sub

BASE     = _pathlib.Path(__file__).resolve().parent.parent
OUT_DIR  = BASE / "data/fermi_exposure"
OUT_DIR.mkdir(exist_ok=True, parents=True)
TMP_DIR  = _pathlib.Path("/tmp/fermi_ft2_allbins")
TMP_DIR.mkdir(exist_ok=True, parents=True)
CKPT     = OUT_DIR / "expmap_allbins_checkpoint.npz"
PROGRESS = OUT_DIR / "expmap_allbins_progress.json"

WEEKS = list(range(9, 789))  # w009〜w788

_NCPU = len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else 4
N_DOWNLOAD_WORKERS = max(4, _NCPU * 3)
CHUNK_T = 2000  # 時間方向チャンクサイズ（ピークメモリ = CHUNK_T × N_pix × 8B × N_BINS 程度）

BIN_CENTERS = np.array([
    1.51, 2.55, 4.31, 7.28, 12.29, 20.76, 35.06,
    59.22, 100.02, 168.93, 285.33, 481.93, 814.00
])
N_BINS = len(BIN_CENTERS)

L_C = (_sub.L_BINS[:-1] + _sub.L_BINS[1:]) / 2
B_C = (_sub.B_BINS[:-1] + _sub.B_BINS[1:]) / 2
LG, BG = np.meshgrid(L_C, B_C, indexing="ij")


# ── [ASSUMPTION] on-axis 実効面積のエネルギー依存性（近似モデル） ──────────────
# アンカー点（log10(E[GeV]), Aeff[cm²]）。Pass 8 SOURCE class on-axisの一般的な
# 性能曲線の概形を模したもの。20 GeVでの値(7000 cm²)は既存のBin6専用スクリプト
# (compute_exposure_map.py) の値と一致させ、連続性を保つ。
_ANCHOR_LOGE = np.log10(np.array([0.3, 1.0, 3.0, 20.0, 100.0, 1000.0]))
_ANCHOR_AEFF = np.array([2500.0, 5500.0, 6800.0, 7000.0, 6800.0, 6200.0])


def aeff_onaxis(e_gev: float) -> float:
    """on-axis実効面積 [cm²] のエネルギー依存性（対数補間、[ASSUMPTION]）。"""
    loge = np.log10(e_gev)
    return float(np.interp(loge, _ANCHOR_LOGE, _ANCHOR_AEFF))


_AEFF_ONAXIS = np.array([aeff_onaxis(e) for e in BIN_CENTERS])  # 13ビン分を事前計算


def theta_shape_factor(theta_deg):
    """θ依存の形状因子（cosθの平方根則、65°でカット）。エネルギーに依存しないので
    チャンクごとに1回だけ計算し、各ビンでは on-axis 実効面積のスカラー倍だけ行う
    （13ビン分 cos**0.5 や where を再計算するのは無駄なため分離した）。"""
    t = np.asarray(theta_deg, dtype=np.float32)
    cos_t = np.maximum(np.cos(np.radians(t)), 0.0)
    shape = np.where(t < 65, cos_t ** 0.5, 0.0)
    return np.maximum(shape, 0.0)


def lb_to_xyz(l_deg, b_deg):
    l, b = np.radians(l_deg), np.radians(b_deg)
    return np.array([np.cos(b) * np.cos(l),
                      np.cos(b) * np.sin(l),
                      np.sin(b)], dtype=np.float32)


pixel_xyz = lb_to_xyz(LG.ravel(), BG.ravel()).T  # (N_pix, 3) float32
N_PIX = len(pixel_xyz)


def download_week(week: int):
    url = (f"https://heasarc.gsfc.nasa.gov/FTP/fermi/data/lat/weekly/spacecraft/"
           f"lat_spacecraft_weekly_w{week:03d}_p310_v001.fits")
    fname = TMP_DIR / f"ft2_w{week:03d}.fits"
    try:
        proc = subprocess.run(
            ["wget", "-q", "--timeout=300", "-t", "2", url, "-O", str(fname)],
            timeout=450,
        )
    except subprocess.TimeoutExpired:
        fname.unlink(missing_ok=True)
        return week, None
    if proc.returncode != 0 or not fname.exists() or fname.stat().st_size < 1e4:
        fname.unlink(missing_ok=True)
        return week, None
    return week, fname


def accumulate_week(fname: _pathlib.Path, expmaps: np.ndarray) -> bool:
    """expmaps: shape (N_BINS, n_l, n_b)。in-placeで加算する。"""
    try:
        with fits.open(str(fname)) as hdul:
            sc = hdul[1].data
            ra_z  = sc["RA_SCZ"].astype(np.float32)
            dec_z = sc["DEC_SCZ"].astype(np.float32)
            live  = sc["LIVETIME"].astype(np.float32)
            coord = SkyCoord(ra=ra_z * u.deg, dec=dec_z * u.deg, frame="icrs")
            gal = coord.galactic
            l_sc = gal.l.deg.astype(np.float32)
            b_sc = gal.b.deg.astype(np.float32)
    except Exception:
        return False
    finally:
        fname.unlink(missing_ok=True)

    n_t = len(l_sc)
    for start in range(0, n_t, CHUNK_T):
        end = min(start + CHUNK_T, n_t)
        sc_xyz = lb_to_xyz(l_sc[start:end], b_sc[start:end]).T  # (chunk, 3)
        cos_theta = np.clip(sc_xyz @ pixel_xyz.T, -1, 1)         # (chunk, N_pix)
        theta_deg = np.degrees(np.arccos(cos_theta))
        # θ形状因子はエネルギーに依存しないためチャンクごとに1回だけ計算する
        shape = theta_shape_factor(theta_deg)                      # (chunk, N_pix)
        base_contrib = (shape * live[start:end, np.newaxis]).sum(axis=0)  # (N_pix,)
        # 各ビンは on-axis 実効面積のスカラー倍を足すだけ（安価）
        for ib, a0 in enumerate(_AEFF_ONAXIS):
            expmaps[ib] += a0 * base_contrib
        del sc_xyz, cos_theta, theta_deg, shape, base_contrib
    return True


def load_checkpoint():
    if CKPT.exists() and PROGRESS.exists():
        expmaps = np.load(CKPT)["expmaps"]
        prog = json.loads(PROGRESS.read_text())
        return expmaps, prog
    return np.zeros((N_BINS, N_PIX), dtype=np.float64), {"done": [], "n_ok": 0}


def save_checkpoint(expmaps, prog):
    np.savez(CKPT, expmaps=expmaps)
    PROGRESS.write_text(json.dumps(prog))


def main():
    expmaps, prog = load_checkpoint()
    done = set(prog["done"])
    remaining = [w for w in WEEKS if w not in done]
    print(f"全13ビン露出マップ計算: {len(WEEKS)}週中 {len(remaining)}週が未処理 "
          f"(DL並列={N_DOWNLOAD_WORKERS}, チャンク={CHUNK_T}, ROI:{N_PIX}px, {N_BINS}ビン同時計算)")

    with ThreadPoolExecutor(max_workers=N_DOWNLOAD_WORKERS) as dl_ex:
        dl_week_of = {dl_ex.submit(download_week, w): w for w in remaining}
        pending = set(dl_week_of)
        n_done = 0
        n_fail = 0

        while pending:
            finished, pending = wait(pending, return_when=FIRST_COMPLETED)
            for fut in finished:
                week = dl_week_of.pop(fut)
                _, fname = fut.result()
                if fname is None:
                    n_fail += 1
                    continue
                ok = accumulate_week(fname, expmaps)
                if not ok:
                    n_fail += 1
                    continue
                prog["done"].append(week)
                prog["n_ok"] += 1
                n_done += 1
                if n_done % 20 == 0:
                    save_checkpoint(expmaps, prog)
                    print(f"  {n_done}/{len(remaining)}週完了 (失敗{n_fail}), "
                          f"Bin6最大露出量: {expmaps[5].max():.3e} cm²·s")

    save_checkpoint(expmaps, prog)
    expmaps_2d = expmaps.reshape(N_BINS, len(L_C), len(B_C))

    print(f"\n完了: {prog['n_ok']}週処理 (総対象{len(WEEKS)}週)")
    for ib, e_gev in enumerate(BIN_CENTERS):
        m = expmaps_2d[ib]
        print(f"  Bin{ib+1:02d} ({e_gev:7.2f} GeV): 平均={m.mean():.3e} cm²·s, "
              f"最大={m.max():.3e} cm²·s")

    out = OUT_DIR / "expmap_allbins.npz"
    np.savez(out, expmaps=expmaps_2d, bin_centers=BIN_CENTERS)
    print(f"\n→ {out}")

    failed_weeks = [w for w in WEEKS if w not in set(prog["done"])]
    if failed_weeks:
        print(f"\n未取得の週 ({len(failed_weeks)}): {failed_weeks}")


if __name__ == "__main__":
    main()
