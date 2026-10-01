#!/usr/bin/env python3
"""
data/CSV/allsky_events.csv の再構築（780週分、全天版、並列ダウンロード＋逐次パース）

背景:
  矮小銀河5天体解析(code/extract_dwarf_csv.py)が必要とする全天球イベントCSVが、
  2026-07-11のUbuntuアカウント消失からの復旧時に再取得されていなかった(発覚:
  2026-07-12、issue-1のPPT精査中)。復旧時に再取得したのはROI限定版
  (data/CSV/filtered_events_week780.csv、|l|<=60°かつ10°<=|b|<=60°)のみで、
  矮小銀河は銀河座標のl方向を問わないため、この限定版だけでは足りない。

安全設計: code/rebuild_filtered_events_week780.py(2026-07-11のOOMクラッシュ事故を
受けて確立した設計)をそのまま踏襲する。ダウンロード(軽量・並列可、12並列)と
FITSパース(重量・低並列、3並列)を別プールに分離し、resource.RLIMIT_ASで
仮想メモリ上限(3GB)を設定する。本機のRAM総量は約5.8GBしかない。

フィルタ条件（extract_dwarf_csv.py・code/download_780w_allsky.pyと同一の全天版）:
  - エネルギー  : E >= 1 GeV
  - 天頂角     : zenith_angle < 100°
  - 銀緯       : |b| >= 10°（銀河面除外のみ、経度lは制限しない）

出力列は filtered_events_week780.csv と同一スキーマ（energy_GeV, l_deg, b_deg,
ra_deg, dec_deg, zenith_angle_deg, time_met_s）にする。

対象週: w009〜w788（780週）
再開可能: results/rebuild_allsky_progress.json に完了週を保存
"""

import pathlib as _pathlib
import subprocess
import resource
import json
import csv
import os
import time
from concurrent.futures import ThreadPoolExecutor, FIRST_COMPLETED, wait

import numpy as np
from astropy.io import fits

BASE = _pathlib.Path(__file__).resolve().parent.parent
OUT_CSV = BASE / "data/CSV/allsky_events.csv"
PROGRESS = BASE / "results/rebuild_allsky_progress.json"
TMP = _pathlib.Path("/tmp/fermi_allsky_rebuild")
TMP.mkdir(parents=True, exist_ok=True)
PROGRESS.parent.mkdir(parents=True, exist_ok=True)
(BASE / "data/CSV").mkdir(parents=True, exist_ok=True)

WEEKS = list(range(9, 789))  # w009〜w788（780週）

_NCPU = len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else 4
# 2026-07-12: 1.5時間の締め切りに対し12並列DLでは間に合わない(実測3.2MB/s、780週
# ≈30GBで2時間超)と判明。DLはI/Oバウンド(ネットワーク待ちが大半でメモリはほぼ
# 使わない)なのでワーカー数を大幅に増やす。パース側(FITS→numpy変換、メモリ重量)
# は据え置き、OOM再発を防ぐ。
N_DOWNLOAD_WORKERS = 20
N_PARSE_WORKERS = max(2, _NCPU - 1)     # 4コア環境なら3（メインスレッド分を残す）

MEMORY_LIMIT_BYTES = 3 * 1024 ** 3  # 3 GiB（rebuild_filtered_events_week780.pyと同一値）

E_MIN_GEV = 1.0
ZENITH_MAX = 100.0
B_MIN = 10.0  # 銀河面除外のみ。経度lは全天とも通す(矮小銀河がl方向を問わないため)

COLUMNS = ["energy_GeV", "l_deg", "b_deg", "ra_deg", "dec_deg",
           "zenith_angle_deg", "time_met_s"]


def set_memory_guard():
    try:
        resource.setrlimit(resource.RLIMIT_AS, (MEMORY_LIMIT_BYTES, MEMORY_LIMIT_BYTES))
    except (ValueError, OSError) as e:
        print(f"警告: メモリ上限の設定に失敗 ({e})。安全弁なしで続行します。")


def load_progress():
    if PROGRESS.exists():
        with open(PROGRESS) as f:
            return json.load(f)
    return {"done": [], "n_events_total": 0}


def save_progress(prog):
    with open(PROGRESS, "w") as f:
        json.dump(prog, f)


def download_week(week: int):
    """1週分をダウンロードするだけ。パースはしない。失敗時は (week, None)。"""
    url = (f"https://heasarc.gsfc.nasa.gov/FTP/fermi/data/lat/weekly/photon/"
           f"lat_photon_weekly_w{week:03d}_p305_v001.fits")
    fname = TMP / f"w{week:03d}.fits"

    try:
        proc = subprocess.run(
            ["wget", "-q", "--timeout=600", "-t", "2", url, "-O", str(fname)],
            timeout=900,
        )
    except subprocess.TimeoutExpired:
        fname.unlink(missing_ok=True)
        return week, None

    if proc.returncode != 0 or not fname.exists() or fname.stat().st_size < 1e5:
        fname.unlink(missing_ok=True)
        return week, None

    return week, fname


def parse_and_filter(fname: _pathlib.Path):
    """ダウンロード済みFITSを読み、全天フィルタ後の行リストを返す。"""
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
    except Exception:
        return None
    finally:
        fname.unlink(missing_ok=True)

    mask = (
        (energy_gev >= E_MIN_GEV) &
        (zenith < ZENITH_MAX) &
        (np.abs(b) >= B_MIN)
    )
    # [PERFORMANCE FIX 2026-07-13] 旧実装はPythonのリスト内包表記で1行ずつ
    # f-string整形しており、大きい週(200-400MB、数百万イベント)でパースが
    # DL(20並列)に追いつかず未処理ファイルが溜まり続けるボトルネックになっていた
    # (実測: 一時ディレクトリに140ファイル・28GB滞留、CPU使用率は逆に79%アイドル
    # =Pythonループ律速でCPUを使い切れていなかったことの証拠)。
    # numpy.savetxtによる一括ベクトル化整形に置き換え、桁違いに高速化する。
    import io
    arr = np.column_stack([
        energy_gev[mask], l[mask], b[mask], ra[mask], dec[mask],
        zenith[mask], time_met[mask],
    ])
    buf = io.StringIO()
    np.savetxt(buf, arr, delimiter=",",
               fmt=["%.5f", "%.5f", "%.5f", "%.5f", "%.5f", "%.3f", "%.2f"])
    return buf.getvalue(), int(mask.sum())


def main():
    set_memory_guard()

    prog = load_progress()
    done = set(prog["done"])
    remaining = [w for w in WEEKS if w not in done]

    write_header = not OUT_CSV.exists()
    mode = "a" if OUT_CSV.exists() else "w"

    print(f"対象週: {len(WEEKS)} 週中 {len(remaining)} 週が未処理 "
          f"(DL並列={N_DOWNLOAD_WORKERS}, パース並列={N_PARSE_WORKERS}, "
          f"メモリ上限={MEMORY_LIMIT_BYTES/1e9:.1f}GB)")
    t0 = time.time()

    with open(OUT_CSV, mode, newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            f.write("# " + " | ".join(COLUMNS) + "\n")
            writer.writerow(COLUMNS)

        n_done = 0
        n_fail = 0

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
                            n_fail += 1
                            print(f"  w{week:03d}: ダウンロード失敗")
                            continue
                        pfut = parse_ex.submit(parse_and_filter, fname)
                        parse_week_of[pfut] = week
                        pending.add(pfut)
                    else:
                        week = parse_week_of.pop(fut)
                        result = fut.result()
                        if result is None:
                            n_fail += 1
                            print(f"  w{week:03d}: パース失敗")
                            continue

                        csv_text, n_rows = result
                        f.write(csv_text)
                        f.flush()
                        del csv_text
                        prog["done"].append(week)
                        prog["n_events_total"] += n_rows
                        save_progress(prog)
                        n_done += 1
                        if n_done % 20 == 0:
                            elapsed = time.time() - t0
                            rate = n_done / elapsed * 60 if elapsed > 0 else 0
                            print(f"  {n_done}/{len(remaining)} 週完了 "
                                  f"(失敗 {n_fail}), 累計イベント数={prog['n_events_total']:,}, "
                                  f"経過={elapsed:.0f}s, {rate:.1f}週/分")

    save_progress(prog)
    print(f"\n完了: {len(prog['done'])}/{len(WEEKS)} 週処理済み, "
          f"総イベント数={prog['n_events_total']:,}")
    print(f"→ {OUT_CSV}")

    failed_weeks = [w for w in WEEKS if w not in set(prog["done"])]
    if failed_weeks:
        print(f"\n未取得の週 ({len(failed_weeks)}): {failed_weeks}")
        print("再度このスクリプトを実行すれば失敗週のみリトライされる。")


if __name__ == "__main__":
    main()
