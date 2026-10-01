"""[2026-07-19] UltraClean版の780週イベント再取得(Totani §2.1 忠実化)。
既存の rebuild_filtered_events_week780.py と同一設計(DL並列12・パース並列3・
RLIMIT_AS 3GB・FITSは逐次削除)に、Totaniが採用する Pass8 UltraClean クラスの
イベント選別を追加する。

UltraClean選別: EVENT_CLASS は 32X(shape=(N,32) bool)。astropy col j = bit(31-j)。
P8R3 ULTRACLEAN=evclass 2^9 → col(31-9)=col22 が True。

ワンパスで |b|<=60 全域を取得し、|b|>=10 を halo探索用、|b|<10 を disk(バブル構築用)に
分割して2つのCSVに書き出す(既存の load_all_events/load_events_with_disk 構造に対応)。

出力(既存ファイルは温存):
  data/CSV/filtered_events_week780_ultraclean.csv   (|b|>=10, halo探索用)
  data/CSV/disk_bl10_week780_ultraclean.csv         (|b|<10,  disk/バブル構築用)

安全: 書き込み先 /tmp/fermi_rebuild_uc は /dev/sdd(907GB, C:とは別ディスク)。
C:ドライブは一切書き込まない。RLIMIT_AS 3GB で暴走時も個別プロセスが落ちるだけ。
"""
import os
import csv
import json
import time
import resource
import subprocess
import pathlib as _pathlib
from concurrent.futures import ThreadPoolExecutor, FIRST_COMPLETED, wait
import numpy as np
from astropy.io import fits

BASE = _pathlib.Path(__file__).resolve().parent.parent
TMP = _pathlib.Path("/tmp/fermi_rebuild_uc")
TMP.mkdir(parents=True, exist_ok=True)
OUT_HALO = BASE / "data/CSV/filtered_events_week780_ultraclean.csv"
OUT_DISK = BASE / "data/CSV/disk_bl10_week780_ultraclean.csv"
PROGRESS = BASE / "results/rebuild_ultraclean_progress.json"
PROGRESS.parent.mkdir(parents=True, exist_ok=True)
(BASE / "data/CSV").mkdir(parents=True, exist_ok=True)

WEEKS = list(range(9, 789))  # w009〜w788（780週）
_NCPU = len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else 4
# [2026-07-19 高速化] CPUがアイドル(DLはI/O律速・HEASARC1接続0.5MB/s)なので
# 環境変数で並列数を上げられるようにする。既定は従来12/3(後方互換)。
N_DOWNLOAD_WORKERS = int(os.environ.get("DL_WORKERS", max(4, _NCPU * 3)))  # 既定12
N_PARSE_WORKERS = int(os.environ.get("PARSE_WORKERS", max(2, _NCPU - 1)))  # 既定3
MEMORY_LIMIT_BYTES = 3 * 1024 ** 3      # 3 GiB 安全弁

E_MIN_GEV = 1.0
ZENITH_MAX = 100.0
L_MAX = 60.0
B_MAX = 60.0
UC_COL = 31 - 9   # UltraClean (evclass 2^9) の EVENT_CLASS 32X 列
COLUMNS = ["energy_GeV", "l_deg", "b_deg", "ra_deg", "dec_deg", "zenith_angle_deg", "time_met_s"]


def set_memory_guard():
    try:
        resource.setrlimit(resource.RLIMIT_AS, (MEMORY_LIMIT_BYTES, MEMORY_LIMIT_BYTES))
    except (ValueError, OSError) as e:
        print(f"警告: メモリ上限設定に失敗 ({e})。安全弁なしで続行。")


def load_progress():
    if PROGRESS.exists():
        with open(PROGRESS) as f:
            return json.load(f)
    return {"done": [], "n_halo": 0, "n_disk": 0}


def save_progress(prog):
    with open(PROGRESS, "w") as f:
        json.dump(prog, f)


def download_week(week: int):
    url = (f"https://heasarc.gsfc.nasa.gov/FTP/fermi/data/lat/weekly/photon/"
           f"lat_photon_weekly_w{week:03d}_p305_v001.fits")
    fname = TMP / f"w{week:03d}.fits"
    try:
        proc = subprocess.run(["wget", "-q", "--timeout=600", "-t", "2", url, "-O", str(fname)],
                              timeout=1200)
    except subprocess.TimeoutExpired:
        fname.unlink(missing_ok=True)
        return week, None
    if proc.returncode != 0 or not fname.exists() or fname.stat().st_size < 1e5:
        fname.unlink(missing_ok=True)
        return week, None
    return week, fname


def parse_and_filter(fname: _pathlib.Path):
    """UltraCleanのみ選別し、(halo_rows |b|>=10, disk_rows |b|<10) を返す。"""
    try:
        with fits.open(str(fname)) as hdul:
            ev = hdul["EVENTS"].data
            energy_gev = ev["ENERGY"].astype(np.float32) / 1000.0
            l_raw = ev["L"].astype(np.float32)
            l = np.where(l_raw > 180, l_raw - 360, l_raw)
            b = ev["B"].astype(np.float32)
            ra = ev["RA"].astype(np.float32)
            dec = ev["DEC"].astype(np.float32)
            zenith = ev["ZENITH_ANGLE"].astype(np.float32)
            time_met = ev["TIME"].astype(np.float64)
            uc = np.asarray(ev["EVENT_CLASS"])[:, UC_COL]   # UltraClean bit (bool)
    except Exception:
        return None
    finally:
        fname.unlink(missing_ok=True)

    base = (
        (energy_gev >= E_MIN_GEV) & (zenith < ZENITH_MAX) &
        (np.abs(l) <= L_MAX) & (np.abs(b) <= B_MAX) & uc
    )
    absb = np.abs(b)
    halo_idx = np.where(base & (absb >= 10.0))[0]
    disk_idx = np.where(base & (absb < 10.0))[0]

    def fmt(idx):
        return [(f"{energy_gev[i]:.5f}", f"{l[i]:.5f}", f"{b[i]:.5f}",
                 f"{ra[i]:.5f}", f"{dec[i]:.5f}", f"{zenith[i]:.3f}", f"{time_met[i]:.2f}")
                for i in idx]
    return fmt(halo_idx), fmt(disk_idx)


def main():
    set_memory_guard()
    prog = load_progress()
    done = set(prog["done"])
    remaining = [w for w in WEEKS if w not in done]

    hh = "a" if OUT_HALO.exists() else "w"
    dd = "a" if OUT_DISK.exists() else "w"
    write_h_header = not OUT_HALO.exists()
    write_d_header = not OUT_DISK.exists()

    print(f"UltraClean再取得: {len(WEEKS)}週中 {len(remaining)}週 未処理 "
          f"(DL並列={N_DOWNLOAD_WORKERS}, パース並列={N_PARSE_WORKERS}, "
          f"メモリ上限={MEMORY_LIMIT_BYTES/1e9:.1f}GB, 保存先=/dev/sdd)")
    t0 = time.time()

    with open(OUT_HALO, hh, newline="", encoding="utf-8") as fh, \
         open(OUT_DISK, dd, newline="", encoding="utf-8") as fd:
        wh, wd = csv.writer(fh), csv.writer(fd)
        if write_h_header:
            fh.write("# " + " | ".join(COLUMNS) + "\n"); wh.writerow(COLUMNS)
        if write_d_header:
            fd.write("# " + " | ".join(COLUMNS) + "\n"); wd.writerow(COLUMNS)

        n_done = n_fail = 0
        with ThreadPoolExecutor(max_workers=N_DOWNLOAD_WORKERS) as dl_ex, \
             ThreadPoolExecutor(max_workers=N_PARSE_WORKERS) as parse_ex:
            dl_week_of = {dl_ex.submit(download_week, w): w for w in remaining}
            parse_week_of = {}
            pending = set(dl_week_of)
            while pending:
                finished, pending = wait(pending, return_when=FIRST_COMPLETED)
                for fut in finished:
                    if fut in dl_week_of:
                        week = dl_week_of.pop(fut)
                        _, fname = fut.result()
                        if fname is None:
                            n_fail += 1; print(f"  w{week:03d}: DL失敗")
                            continue
                        pfut = parse_ex.submit(parse_and_filter, fname)
                        parse_week_of[pfut] = week; pending.add(pfut)
                    else:
                        week = parse_week_of.pop(fut)
                        res = fut.result()
                        if res is None:
                            n_fail += 1; print(f"  w{week:03d}: パース失敗")
                            continue
                        halo_rows, disk_rows = res
                        for r in halo_rows: wh.writerow(r)
                        for r in disk_rows: wd.writerow(r)
                        fh.flush(); fd.flush()
                        prog["done"].append(week)
                        prog["n_halo"] += len(halo_rows); prog["n_disk"] += len(disk_rows)
                        save_progress(prog)
                        n_done += 1
                        del halo_rows, disk_rows
                        if n_done % 20 == 0:
                            el = time.time() - t0
                            rate = n_done / el * 60 if el > 0 else 0
                            eta = (len(remaining) - n_done) / max(rate, 1e-9)
                            print(f"  {n_done}/{len(remaining)}週 完了 "
                                  f"({rate:.1f}週/分, ETA {eta:.0f}分, "
                                  f"halo={prog['n_halo']} disk={prog['n_disk']})", flush=True)

    dt = time.time() - t0
    print(f"\n完了: {n_done}週処理, {n_fail}週失敗, {dt/60:.1f}分")
    print(f"  halo(|b|>=10): {prog['n_halo']} 事象 → {OUT_HALO}")
    print(f"  disk(|b|<10):  {prog['n_disk']} 事象 → {OUT_DISK}")


if __name__ == "__main__":
    main()
