"""
Fermi-LAT 780週分 全天 photon データダウンロード＆CSV保存

対象: 週 w009〜w788（780週分）
フィルタ: |b|≥10° かつ 1≤E≤1000 GeV
出力: data/CSV/allsky_780w.csv（全天高銀緯イベント）
      data/CSV/m31_cluster/m31_780w.csv
      data/CSV/m31_cluster/perseus_780w.csv
      data/CSV/m31_cluster/coma_780w.csv

再開可能: progress.json に進捗を保存
"""
import pathlib as _pathlib

import subprocess, os, json, sys
from pathlib import Path
import numpy as np
import pandas as pd
from astropy.io import fits

BASE = _pathlib.Path(__file__).resolve().parent.parent
OUT_MAIN = BASE / "data/CSV/allsky_780w.csv"
OUT_DIR  = BASE / "data/CSV/m31_cluster"
OUT_DIR.mkdir(exist_ok=True)
TMP = Path("/tmp/fermi_dl"); TMP.mkdir(exist_ok=True)
PROGRESS = BASE / "results/download_progress.json"
PROGRESS.parent.mkdir(exist_ok=True)

# ターゲット天体（全天CSVとは別に個別CSVも保存）
TARGETS = {
    "m31":     (121.17, -21.57, 5.0),
    "perseus": (150.6,  -13.3,  3.0),
    "coma":    ( 58.1,   87.7,  3.0),
}

# フィルタ
EMIN_MEV = 1000.0     # 1 GeV
EMAX_MEV = 1_000_000.0  # 1000 GeV
B_ABS_MIN = 10.0      # |b|≥10°

# 週リスト（Fermiは週9から開始）
WEEKS = list(range(9, 789))

def load_progress():
    if PROGRESS.exists():
        with open(PROGRESS) as f:
            return json.load(f)
    return {"done": [], "n_events_total": 0}

def save_progress(prog):
    with open(PROGRESS, "w") as f:
        json.dump(prog, f)

def download_and_extract(week: int):
    """1週分をダウンロードして高銀緯イベントを返す。失敗時は None。"""
    url = (f"https://heasarc.gsfc.nasa.gov/FTP/fermi/data/lat/weekly/photon/"
           f"lat_photon_weekly_w{week:03d}_p305_v001.fits")
    fname = TMP / f"w{week:03d}.fits"

    try:
        proc = subprocess.Popen(
            ["wget", "-q", "--timeout=300", "-t", "1", url, "-O", str(fname)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        try:
            proc.wait(timeout=360)  # 6分。57MB÷450KB/s=127秒なので余裕を持つ
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
            fname.unlink(missing_ok=True)
            return None
        ret_code = proc.returncode
    except Exception:
        fname.unlink(missing_ok=True)
        return None

    if ret_code != 0 or not fname.exists():
        fname.unlink(missing_ok=True)
        return None
    fsize = fname.stat().st_size
    if fsize < 1e6 or fsize > 80_000_000:  # 1MB〜80MB の範囲外は異常
        fname.unlink(missing_ok=True)
        return None

    try:
        with fits.open(str(fname)) as hdul:
            d = hdul[1].data
            e   = d['ENERGY'].astype(float)
            l   = d['L'].astype(float)
            b   = d['B'].astype(float)
            t   = d['TIME'].astype(float)
    except Exception:
        fname.unlink(missing_ok=True)
        return None

    fname.unlink()

    # フィルタ: エネルギー + 高銀緯
    mask = (e >= EMIN_MEV) & (e <= EMAX_MEV) & (np.abs(b) >= B_ABS_MIN)
    if mask.sum() == 0:
        return {}

    result = {"main": pd.DataFrame({
        "energy_GeV": e[mask] / 1000,
        "l_deg":      l[mask],
        "b_deg":      b[mask],
        "time_met_s": t[mask],
        "week":       week,
    })}

    # ターゲット天体別
    for name, (l0, b0, rad) in TARGETS.items():
        dist = np.sqrt((l[mask]-l0)**2 + (b[mask]-b0)**2)
        tmask = dist < rad
        if tmask.sum() > 0:
            result[name] = result["main"][tmask].copy()
            result[name]["ang_dist_deg"] = dist[tmask]

    return result

def main():
    prog = load_progress()
    done = set(prog["done"])
    remaining = [w for w in WEEKS if w not in done]

    print(f"=== Fermi-LAT 780週分 全天ダウンロード ===")
    print(f"完了: {len(done)}/{len(WEEKS)} 週")
    print(f"残り: {len(remaining)} 週")
    print(f"出力: {OUT_MAIN}")
    print()

    main_buf, target_bufs = [], {k: [] for k in TARGETS}
    FLUSH_EVERY = 10

    for i, week in enumerate(remaining):
        print(f"[{len(done)+i+1}/{len(WEEKS)}] w{week:03d} ...", end=" ", flush=True)

        try:
            result = download_and_extract(week)
        except Exception as ex:
            print(f"エラー: {ex}")
            continue

        if result is None:
            print("スキップ")
            continue

        if "main" in result:
            main_buf.append(result["main"])
            n = len(result["main"])
        else:
            n = 0

        for name in TARGETS:
            if name in result:
                target_bufs[name].append(result[name])

        done.add(week)
        prog["done"] = list(done)
        prog["n_events_total"] = prog.get("n_events_total", 0) + n
        save_progress(prog)

        # Bin6のカウント
        if "main" in result:
            df_w = result["main"]
            n6 = ((df_w.energy_GeV>=15.35)&(df_w.energy_GeV<28.07)).sum()
            m31_n = len(result.get("m31", pd.DataFrame()))
            print(f"OK | {n} ev, Bin6={n6}, M31区域={m31_n}")
        else:
            print("OK (0 events)")

        # まとめて書き出し（バッファが貯まったら）
        if len(main_buf) >= FLUSH_EVERY:
            mode = "a" if OUT_MAIN.exists() else "w"
            hdr  = not OUT_MAIN.exists()
            pd.concat(main_buf, ignore_index=True).to_csv(
                OUT_MAIN, mode=mode, header=hdr, index=False)
            main_buf.clear()

            for name, buf in target_bufs.items():
                if buf:
                    out = OUT_DIR / f"{name}_780w.csv"
                    mode2 = "a" if out.exists() else "w"
                    hdr2  = not out.exists()
                    pd.concat(buf, ignore_index=True).to_csv(
                        out, mode=mode2, header=hdr2, index=False)
                    target_bufs[name].clear()

    # 残りのバッファを書き出し
    if main_buf:
        mode = "a" if OUT_MAIN.exists() else "w"
        pd.concat(main_buf, ignore_index=True).to_csv(
            OUT_MAIN, mode=mode, header=not OUT_MAIN.exists(), index=False)
    for name, buf in target_bufs.items():
        if buf:
            out = OUT_DIR / f"{name}_780w.csv"
            mode2 = "a" if out.exists() else "w"
            pd.concat(buf, ignore_index=True).to_csv(
                out, mode=mode2, header=not out.exists(), index=False)

    print(f"\n=== 完了 ===")
    print(f"総イベント数: {prog.get('n_events_total',0):,}")
    if OUT_MAIN.exists():
        print(f"全天CSV: {OUT_MAIN}  ({OUT_MAIN.stat().st_size//1024//1024} MB)")
    for name in TARGETS:
        out = OUT_DIR / f"{name}_780w.csv"
        if out.exists():
            df = pd.read_csv(out)
            n6 = ((df.energy_GeV>=15.35)&(df.energy_GeV<28.07)).sum()
            print(f"{name}: {len(df):,} events, Bin6={n6}")

if __name__ == "__main__":
    main()
