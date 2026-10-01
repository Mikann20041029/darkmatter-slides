"""
Fermi-LAT 露出マップ（Exposure Map）の計算

スペースクラフトファイル（FT2、30秒間隔の衛星姿勢データ）から
各ピクセルへの積算露出量 [cm²·s] を計算する。

手法:
  各30秒インターバルで、衛星の視野（FOV、半頂角100°）内にある
  ピクセルについて、有効面積 A_eff(E, θ) × LIVETIME を積算する。

2026-07-11 の設計変更（メモリ安全化）:
  旧版は1週分(時刻サンプル数 N_t ≈ 20,160 × ピクセル数 N_pix = 14,400)の
  (N_t, N_pix) 行列を一括生成しており、float64で約2.3GB/週。cos_theta・
  theta_deg・aeff の3枚が同時に存在しうるため、ピーク時 ~7GB に達する
  可能性があり、本機のRAM総量5.8GBを超えてクラッシュしうる設計だった
  （code/rebuild_filtered_events_week780.py の事故と同種のリスク）。
  対策:
    (1) 時間方向をチャンク分割(CHUNK_T=2000)して逐次加算し、ピークメモリを
        チャンクサイズ分に限定する
    (2) ダウンロード(軽量・並列可)と計算(重量・逐次)を分離し、
        ダウンロードのみ複数並列にする(本機CPU数に応じて自動決定)
    (3) 部分結果(expmap配列 + 完了週リスト)を定期的にディスクへチェックポイント
        保存し、途中終了しても再開できるようにする

出力: data/fermi_exposure/expmap_bin6.npy, expmap_bin6.png
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
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

import plot_skymap_all_subtracted as _sub

BASE     = _pathlib.Path(__file__).resolve().parent.parent
OUT_DIR  = BASE / "data/fermi_exposure"
OUT_DIR.mkdir(exist_ok=True, parents=True)
TMP_DIR  = _pathlib.Path("/tmp/fermi_ft2")
TMP_DIR.mkdir(exist_ok=True, parents=True)
CKPT     = OUT_DIR / "expmap_checkpoint.npz"
PROGRESS = OUT_DIR / "expmap_progress.json"

WEEKS = list(range(9, 789))  # w009〜w788

_NCPU = len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else 4
N_DOWNLOAD_WORKERS = max(4, _NCPU * 3)  # ダウンロードは軽量なので並列可
CHUNK_T = 2000  # 時間方向のチャンクサイズ（ピークメモリ = CHUNK_T × N_pix × 8B 程度）

L_C = (_sub.L_BINS[:-1] + _sub.L_BINS[1:]) / 2
B_C = (_sub.B_BINS[:-1] + _sub.B_BINS[1:]) / 2
LG, BG = np.meshgrid(L_C, B_C, indexing="ij")


def aeff_p8_20gev(theta_deg):
    """Pass 8 SOURCE, ~20 GeV での有効面積 [cm²]
    出典: Fermi-LAT Performance (Ackermann+2013)
    0-65° で約7000 cm²、65-70° で急減、70° 以上で 0"""
    t = np.asarray(theta_deg, dtype=np.float32)
    # cos(t)は t>90°で負値になり**0.5(平方根)がNaN+RuntimeWarningを出すため、
    # 0以上にクリップしてから計算する(t>=65は元よりnp.whereで0にするため結果に影響なし)
    cos_t = np.maximum(np.cos(np.radians(t)), 0.0)
    aeff = np.where(t < 65, 7000.0 * cos_t ** 0.5, 0.0)
    return np.maximum(aeff, 0.0)


def lb_to_xyz(l_deg, b_deg):
    l, b = np.radians(l_deg), np.radians(b_deg)
    return np.array([np.cos(b) * np.cos(l),
                      np.cos(b) * np.sin(l),
                      np.sin(b)], dtype=np.float32)


pixel_xyz = lb_to_xyz(LG.ravel(), BG.ravel()).T  # (N_pix, 3) float32
N_PIX = len(pixel_xyz)


def download_week(week: int):
    """1週分のFT2ファイルをダウンロードするだけ。失敗時は (week, None)。"""
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


def accumulate_week(fname: _pathlib.Path, expmap: np.ndarray) -> bool:
    """ダウンロード済みFT2を読み、チャンク分割しながら expmap に加算する（in-place）。"""
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
    flat_exp = expmap.reshape(-1)
    for start in range(0, n_t, CHUNK_T):
        end = min(start + CHUNK_T, n_t)
        sc_xyz = lb_to_xyz(l_sc[start:end], b_sc[start:end]).T  # (chunk, 3)
        cos_theta = np.clip(sc_xyz @ pixel_xyz.T, -1, 1)         # (chunk, N_pix)
        theta_deg = np.degrees(np.arccos(cos_theta))
        aeff = aeff_p8_20gev(theta_deg)
        contrib = (aeff * live[start:end, np.newaxis]).sum(axis=0)  # (N_pix,)
        flat_exp += contrib
        del sc_xyz, cos_theta, theta_deg, aeff, contrib
    return True


def load_checkpoint():
    if CKPT.exists() and PROGRESS.exists():
        expmap = np.load(CKPT)["expmap"]
        prog = json.loads(PROGRESS.read_text())
        return expmap, prog
    return np.zeros((len(L_C), len(B_C)), dtype=np.float64), {"done": [], "n_ok": 0}


def save_checkpoint(expmap, prog):
    np.savez(CKPT, expmap=expmap)
    PROGRESS.write_text(json.dumps(prog))


def main():
    expmap, prog = load_checkpoint()
    done = set(prog["done"])
    remaining = [w for w in WEEKS if w not in done]
    print(f"露出マップ計算: {len(WEEKS)}週中 {len(remaining)}週が未処理 "
          f"(DL並列={N_DOWNLOAD_WORKERS}, チャンクサイズ={CHUNK_T}, ROI: {N_PIX}ピクセル)")

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
                ok = accumulate_week(fname, expmap)
                if not ok:
                    n_fail += 1
                    continue
                prog["done"].append(week)
                prog["n_ok"] += 1
                n_done += 1
                if n_done % 20 == 0:
                    save_checkpoint(expmap, prog)
                    print(f"  {n_done}/{len(remaining)}週完了 (失敗{n_fail}), "
                          f"最大露出量: {expmap.max():.3e} cm²·s")

    save_checkpoint(expmap, prog)
    print(f"\n完了: {prog['n_ok']}週処理 (総対象{len(WEEKS)}週)")
    print("露出マップ統計:")
    print(f"  平均: {expmap.mean():.3e} cm²·s")
    print(f"  最大: {expmap.max():.3e} cm²·s")
    nz = expmap[expmap > 0]
    if len(nz):
        print(f"  最小（ROI内）: {nz.min():.3e} cm²·s")
        print(f"  Mrk501較正値との比: {expmap.mean() / 1.24e11:.2f}")

    out = OUT_DIR / "expmap_bin6.npy"
    np.save(out, expmap)
    print(f"\n→ {out}")

    fig, ax = plt.subplots(figsize=(12, 5), facecolor="#05051A")
    ax.set_facecolor("#05051A")
    if len(nz):
        im = ax.pcolormesh(L_C, B_C, expmap.T,
                            norm=LogNorm(vmin=nz.min(), vmax=expmap.max()),
                            cmap="hot", shading="auto")
        plt.colorbar(im, ax=ax, label="露出量 [cm²·s]")
    ax.set_xlim(60, -60); ax.set_ylim(-60, 60)
    ax.set_xlabel("銀経 l [deg]", color="white")
    ax.set_ylabel("銀緯 b [deg]", color="white")
    ax.set_title("Fermi-LAT 780週 積算露出マップ（Bin6: 20.76 GeV）", color="white")
    ax.tick_params(colors="white")
    for sp in ax.spines.values():
        sp.set_color("white")
    plt.savefig(OUT_DIR / "expmap_bin6.png", dpi=130, bbox_inches="tight", facecolor="#05051A")
    plt.close()
    print(f"→ {OUT_DIR}/expmap_bin6.png")

    failed_weeks = [w for w in WEEKS if w not in set(prog["done"])]
    if failed_weeks:
        print(f"\n未取得の週 ({len(failed_weeks)}): {failed_weeks}")
        print("再度このスクリプトを実行すれば失敗週のみリトライされる。")


if __name__ == "__main__":
    main()
