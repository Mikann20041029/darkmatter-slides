"""[2026-07-18] 銀河面(|b|<10°)Fermiデータ取得——Totani §3.1のバブル/GCE構築を
disk込みで再現するため。既存の |b|>=10 データ(filtered_events_week780.csv)を補完する。

週次全天FITS(116MB/週)をw009-w788の780週分ダウンロードし、Totani ROIの銀河面
(|l|<=60°, |b|<10°, 1<=E<=1000 GeV)のみ抽出してCSV化する。各FITSは解析後即削除
(90GBを溜めない)。並列ダウンロード(I/O律速、メモリ安全)。resumable。

出力: data/CSV/disk_bl10_week780.csv (既存CSVと同一スキーマ)
検証列: 各週の高緯度(10<=|b|<=60)件数も集計し既存CSVと整合を確認可能にする。
"""
from pathlib import Path
import subprocess, json, os, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
import pandas as pd
from astropy.io import fits

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "data/CSV/disk_bl10_week780.csv"
PROG = BASE / "results/download_disk_progress.json"
TMP = Path("/tmp/fermi_disk_dl"); TMP.mkdir(exist_ok=True)
PROG.parent.mkdir(exist_ok=True)

WEEKS = list(range(9, 789))           # w009-w788 (780週、既存と同一)
EMIN_MEV, EMAX_MEV = 1000.0, 1_000_000.0
L_MAX, B_DISK = 60.0, 10.0
N_WORKERS = 4               # [2026-07-18 C:安全] 瞬間最大4×116MB=464MBに抑える
C_FREE_MIN_MB = 500         # C:空きがこれ未満ならDL停止(vhdx膨張→C:満杯を防ぐ)


def c_free_mb():
    """Windows C: の空きMB(WSL vhdxはC:上、膨張でC:を圧迫するため監視)。"""
    try:
        import shutil
        return shutil.disk_usage("/mnt/c").free / 1e6
    except Exception:
        return 1e9
COLUMNS = ["energy_GeV", "l_deg", "b_deg", "ra_deg", "dec_deg", "zenith_angle_deg", "time_met_s"]


def load_prog():
    if PROG.exists():
        return json.load(open(PROG))
    return {"done": [], "n_disk": 0}


def fetch_week(week: int):
    """1週分をDLし銀河面イベントを返す。(week, DataFrame or None, n_hi_lat, err)"""
    # [2026-07-18 C:安全ガード] C:空きが閾値未満ならDLせず中断(vhdx膨張防止)
    if c_free_mb() < C_FREE_MIN_MB:
        return week, None, 0, f"C:空き不足({c_free_mb():.0f}MB<{C_FREE_MIN_MB})→中断"
    url = (f"https://heasarc.gsfc.nasa.gov/FTP/fermi/data/lat/weekly/photon/"
           f"lat_photon_weekly_w{week:03d}_p305_v001.fits")
    fn = TMP / f"w{week:03d}.fits"
    try:
        r = subprocess.run(["wget", "-q", "--timeout=600", "-t", "3", url, "-O", str(fn)],
                           capture_output=True)
        if r.returncode != 0 or not fn.exists() or fn.stat().st_size < 1000:
            return week, None, 0, f"wget rc={r.returncode}"
        with fits.open(fn) as h:
            d = h["EVENTS"].data
            e = np.asarray(d["ENERGY"], float); l = np.asarray(d["L"], float)
            b = np.asarray(d["B"], float)
            emask = (e >= EMIN_MEV) & (e <= EMAX_MEV)
            disk = emask & (np.abs(l) <= L_MAX) & (np.abs(b) < B_DISK)
            hi = int((emask & (np.abs(l) <= L_MAX) & (np.abs(b) >= B_DISK) & (np.abs(b) <= 60)).sum())
            df = pd.DataFrame({
                "energy_GeV": e[disk] / 1000.0, "l_deg": l[disk], "b_deg": b[disk],
                "ra_deg": np.asarray(d["RA"], float)[disk], "dec_deg": np.asarray(d["DEC"], float)[disk],
                "zenith_angle_deg": np.asarray(d["ZENITH_ANGLE"], float)[disk],
                "time_met_s": np.asarray(d["TIME"], float)[disk],
            })[COLUMNS]
        return week, df, hi, None
    finally:
        if fn.exists():
            fn.unlink()   # 即削除(90GBを溜めない)


def main():
    prog = load_prog()
    done = set(prog["done"])
    todo = [w for w in WEEKS if w not in done]
    print(f"残り {len(todo)}/{len(WEEKS)} 週。並列={N_WORKERS}", flush=True)
    if not todo:
        print("全週完了済み。", flush=True); return
    write_header = not OUT.exists()
    t0 = time.time(); n_ok = 0; n_disk_events = 0
    with ThreadPoolExecutor(max_workers=N_WORKERS) as ex:
        futs = {ex.submit(fetch_week, w): w for w in todo}
        for i, fut in enumerate(as_completed(futs), 1):
            week, df, hi, err = fut.result()
            if err is not None:
                print(f"  w{week:03d} 失敗: {err}", flush=True); continue
            df.to_csv(OUT, mode="a", header=write_header, index=False)
            write_header = False
            done.add(week); n_ok += 1; n_disk_events += len(df)
            prog["done"] = sorted(done); prog["n_disk"] = prog.get("n_disk", 0) + len(df)
            json.dump(prog, open(PROG, "w"))
            if i <= 8 or i % 50 == 0:
                rate = i / (time.time() - t0)  # 週/秒
                eta_min = (len(todo) - i) / rate / 60 if rate > 0 else -1
                print(f"  [{i}/{len(todo)}] w{week:03d} disk={len(df)} hi={hi} "
                      f"速度={rate*60:.1f}週/分 ETA={eta_min:.0f}分", flush=True)
    print(f"\n完了: {n_ok}週追加, 銀河面イベント計{n_disk_events} → {OUT}", flush=True)


if __name__ == "__main__":
    main()
