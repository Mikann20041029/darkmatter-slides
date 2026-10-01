"""
Fermi-LAT 780週 並列ダウンロード（30並列）
目標: 1時間以内に完了
"""
import pathlib as _pathlib

import subprocess, json, sys, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from astropy.io import fits
import numpy as np
import pandas as pd

BASE = _pathlib.Path(__file__).resolve().parent.parent
OUT_MAIN = BASE / "data/CSV/allsky_780w.csv"
OUT_DIR  = BASE / "data/CSV/m31_cluster"
OUT_DIR.mkdir(exist_ok=True)
TMP = Path("/tmp/fermi_dl"); TMP.mkdir(exist_ok=True)
PROGRESS = BASE / "results/download_progress.json"

TARGETS = {
    "m31":     (121.17, -21.57, 5.0),
    "perseus": (150.6,  -13.3,  3.0),
    "coma":    ( 58.1,   87.7,  3.0),
}

EMIN_MEV = 1000.0
B_ABS_MIN = 10.0
N_WORKERS = 30

N = 13
centers = np.logspace(np.log10(1.51), np.log10(814.0), N)
ratio_v = (814.0/1.51)**(1/(N-1))
edges = np.concatenate([[1.51/ratio_v**0.5], np.sqrt(centers[:-1]*centers[1:]), [814.0*ratio_v**0.5]])

def load_progress():
    if PROGRESS.exists():
        with open(PROGRESS) as f: return json.load(f)
    return {"done": [], "n_events_total": 0}

def save_progress(d):
    with open(PROGRESS, "w") as f: json.dump(d, f)

def download_one(week):
    """1週ダウンロード → 抽出 → DataFrameを返す。失敗はNone。"""
    url = (f"https://heasarc.gsfc.nasa.gov/FTP/fermi/data/lat/weekly/photon/"
           f"lat_photon_weekly_w{week:03d}_p305_v001.fits")
    fname = TMP / f"w{week:03d}.fits"

    try:
        proc = subprocess.Popen(
            ["wget", "-q", "--timeout=300", "-t", "1", url, "-O", str(fname)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        proc.wait(timeout=360)
        if proc.returncode != 0: raise RuntimeError("wget failed")
        fsize = fname.stat().st_size if fname.exists() else 0
        if fsize < 1e6 or fsize > 80_000_000:
            fname.unlink(missing_ok=True)
            return week, None
    except Exception:
        if fname.exists(): fname.unlink(missing_ok=True)
        return week, None

    try:
        with fits.open(str(fname)) as hdul:
            d = hdul[1].data
            e = d['ENERGY'].astype(float)
            l = d['L'].astype(float)
            b = d['B'].astype(float)
            t = d['TIME'].astype(float)
        fname.unlink()
    except Exception:
        fname.unlink(missing_ok=True)
        return week, None

    mask = (e >= EMIN_MEV) & (np.abs(b) >= B_ABS_MIN)
    if mask.sum() == 0:
        return week, {}

    result = {"main": pd.DataFrame({
        "energy_GeV": e[mask]/1000, "l_deg": l[mask],
        "b_deg": b[mask], "time_met_s": t[mask], "week": week,
    })}
    for name, (l0, b0, rad) in TARGETS.items():
        dist = np.sqrt((l[mask]-l0)**2 + (b[mask]-b0)**2)
        tm = dist < rad
        if tm.sum() > 0:
            df = result["main"][tm].copy()
            df["ang_dist_deg"] = dist[tm]
            result[name] = df
    return week, result


def main():
    prog = load_progress()
    done = set(prog["done"])
    remaining = [w for w in range(9, 789) if w not in done]
    total = 780

    print(f"=== 並列ダウンロード開始 ({N_WORKERS}並列) ===")
    print(f"完了: {len(done)}/{total}週, 残り: {len(remaining)}週")
    t0 = time.time()

    main_buf = []
    target_bufs = {k: [] for k in TARGETS}
    n_events = prog.get("n_events_total", 0)
    n_done_new = 0

    with ThreadPoolExecutor(max_workers=N_WORKERS) as ex:
        futures = {ex.submit(download_one, w): w for w in remaining}
        for i, fut in enumerate(as_completed(futures)):
            week, result = fut.result()
            done.add(week)
            n_done_new += 1

            if result and "main" in result:
                main_buf.append(result["main"])
                n_events += len(result["main"])
                for name in TARGETS:
                    if name in result:
                        target_bufs[name].append(result[name])
                n6 = ((result["main"].energy_GeV>=15.35)&(result["main"].energy_GeV<28.07)).sum()
                elapsed = time.time()-t0
                rate = n_done_new / elapsed * 60
                eta = (len(remaining)-n_done_new) / (n_done_new/elapsed) / 60
                print(f"  w{week:03d} OK | {len(result['main']):,}ev Bin6={n6} "
                      f"| {n_done_new}/{len(remaining)} 完了 "
                      f"| {rate:.1f}週/分 ETA:{eta:.0f}分", flush=True)
            else:
                print(f"  w{week:03d} スキップ | {n_done_new}/{len(remaining)}", flush=True)

            # 50週ごとに書き出し
            if len(main_buf) >= 50:
                mode = "a" if OUT_MAIN.exists() else "w"
                pd.concat(main_buf, ignore_index=True).to_csv(
                    OUT_MAIN, mode=mode, header=not OUT_MAIN.exists(), index=False)
                main_buf.clear()
                for name, buf in target_bufs.items():
                    if buf:
                        out = OUT_DIR/f"{name}_780w.csv"
                        mode2 = "a" if out.exists() else "w"
                        pd.concat(buf, ignore_index=True).to_csv(
                            out, mode=mode2, header=not out.exists(), index=False)
                        target_bufs[name].clear()
                prog["done"] = list(done)
                prog["n_events_total"] = n_events
                save_progress(prog)

    # 残りを書き出し
    if main_buf:
        mode = "a" if OUT_MAIN.exists() else "w"
        pd.concat(main_buf, ignore_index=True).to_csv(
            OUT_MAIN, mode=mode, header=not OUT_MAIN.exists(), index=False)
    for name, buf in target_bufs.items():
        if buf:
            out = OUT_DIR/f"{name}_780w.csv"
            mode2 = "a" if out.exists() else "w"
            pd.concat(buf, ignore_index=True).to_csv(
                out, mode=mode2, header=not out.exists(), index=False)

    prog["done"] = list(done)
    prog["n_events_total"] = n_events
    save_progress(prog)

    elapsed = (time.time()-t0)/60
    print(f"\n=== 完了 ({elapsed:.1f}分) ===")
    print(f"総イベント: {n_events:,}")
    if OUT_MAIN.exists():
        mb = OUT_MAIN.stat().st_size//1024//1024
        print(f"全天CSV: {mb}MB")
    for name in TARGETS:
        out = OUT_DIR/f"{name}_780w.csv"
        if out.exists():
            df = pd.read_csv(out)
            n6 = ((df.energy_GeV>=15.35)&(df.energy_GeV<28.07)).sum()
            print(f"{name}: {len(df):,}ev, Bin6={n6}")

if __name__=="__main__":
    main()
