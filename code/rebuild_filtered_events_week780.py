#!/usr/bin/env python3
"""
data/CSV/filtered_events_week780.csv の再構築（780週分、並列ダウンロード＋逐次パース）

背景:
  2026-05〜06 の解析で生成された filtered_events_week780.csv は、生成スクリプトが
  一度も commit されないまま Ubuntu 環境の消失とともに失われた（.dev/CHANGELOG.md
  参照）。本スクリプトはその再現手順を明文化し、再実行可能にする。

2026-07-11 の事故と設計変更:
  初版はダウンロードとFITSパース（numpy配列への変換）を同じ80並列ワーカーで
  行っていたため、1プロセスが anon-rss 5.2GB まで肥大し、OS の OOM killer に
  よって強制終了された（本機のRAM総量は約5.8GBしかない）。カーネルログ
  (`journalctl -b -1`) に直接記録が残っている:
    "Out of memory: Killed process ... (python3) total-vm:23059652kB,
     anon-rss:5489592kB"
  対策として、(1) ダウンロード（軽量・並列可、30並列）とFITSパース（重量・
  要低並列化、4並列に制限）を別プールに分離し、(2) プロセス全体に
  resource.RLIMIT_AS で仮想メモリ上限(3GB)を設定して、万一の暴走時も個別
  プロセスの MemoryError で止まるようにし、OSごとクラッシュすることを防ぐ。

フィルタ条件（Totani 2025 Section 2.1、code/make_filtered_csv.py と同一）:
  - エネルギー  : E >= 1 GeV
  - 天頂角     : zenith_angle < 100°
  - ROI 銀経   : |l| <= 60°
  - ROI 銀緯   : 10° <= |b| <= 60°

出力列は make_filtered_csv.py と同一スキーマ（energy_GeV, l_deg, b_deg, ra_deg,
dec_deg, zenith_angle_deg, time_met_s）にし、下流の全スクリプトが無改造で読める
ようにする。

対象週: w009〜w788（780週）
再開可能: results/rebuild_filtered_events_progress.json に完了週を保存
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
OUT_CSV = BASE / "data/CSV/filtered_events_week780.csv"
PROGRESS = BASE / "results/rebuild_filtered_events_progress.json"
TMP = _pathlib.Path("/tmp/fermi_rebuild")
TMP.mkdir(parents=True, exist_ok=True)
PROGRESS.parent.mkdir(parents=True, exist_ok=True)
(BASE / "data/CSV").mkdir(parents=True, exist_ok=True)

WEEKS = list(range(9, 789))  # w009〜w788（780週）

# ダウンロード（軽量・I/Oバウンド）は並列度を高くしてよい。
# パース（numpy配列生成・メモリ重量）は少数の別プールに制限する
# (完全逐次だとパース側が律速してダウンロード帯域を使い切れないため、
#  安全マージンを保てる範囲で少数だけ並列化する)。
_NCPU = len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else 4
# 2026-07-11 の追加事故: 本機はCPU 4コアのみ。80並列DLにしたところ
# load average が 28〜38 まで跳ね上がり、パース側スレッドがCPUを取れず
# 完全に停止した（ダウンロードは進むがCSV書き込みが0件/30秒という状態）。
# wgetはI/Oバウンドとはいえプロセス数そのものがスケジューラ・ディスクI/Oを
# 圧迫するため、コア数に対して常識的な範囲に抑える。
N_DOWNLOAD_WORKERS = max(4, _NCPU * 3)  # 4コア環境なら12
N_PARSE_WORKERS = max(2, _NCPU - 1)     # 4コア環境なら3（メインスレッド分を残す）

# 本機のRAM総量(~5.8GB)に対する安全マージン。単一プロセスがこれを超えて
# 確保しようとすると MemoryError で落ちる（=OSごとクラッシュさせない安全弁）。
MEMORY_LIMIT_BYTES = 3 * 1024 ** 3  # 3 GiB（仮想アドレス空間。Python/numpy/astropyの
                                     # 通常オーバーヘッドを避けつつ、本機のRAM総量
                                     # 5.8GBには収まる余裕を残す値として設定）

E_MIN_GEV = 1.0
ZENITH_MAX = 100.0
L_MAX = 60.0
B_MIN = 10.0
B_MAX = 60.0

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
    """ダウンロード済みFITSを読み、ROIフィルタ後の行リストを返す。
    float32で保持しメモリを抑える（有効数字5桁の出力要件に対し十分）。
    """
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
            time_met = ev["TIME"].astype(np.float64)  # MET秒は精度確保のため64bit維持
    except Exception:
        return None
    finally:
        fname.unlink(missing_ok=True)

    mask = (
        (energy_gev >= E_MIN_GEV) &
        (zenith < ZENITH_MAX) &
        (np.abs(l) <= L_MAX) &
        (np.abs(b) >= B_MIN) &
        (np.abs(b) <= B_MAX)
    )
    idx = np.where(mask)[0]
    rows = [
        (f"{energy_gev[i]:.5f}", f"{l[i]:.5f}", f"{b[i]:.5f}",
         f"{ra[i]:.5f}", f"{dec[i]:.5f}", f"{zenith[i]:.3f}", f"{time_met[i]:.2f}")
        for i in idx
    ]
    return rows


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
            pending = set(dl_week_of)  # ダウンロード未完了 + パース未完了 のfutureの合併集合

            while pending:
                finished, pending = wait(pending, return_when=FIRST_COMPLETED)

                for fut in finished:
                    if fut in dl_week_of:
                        # ダウンロードが完了 → パースプールに投入し、pendingに合流させる
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
                        # パースが完了 → CSVに書き出し
                        week = parse_week_of.pop(fut)
                        rows = fut.result()
                        if rows is None:
                            n_fail += 1
                            print(f"  w{week:03d}: パース失敗")
                            continue

                        for row in rows:
                            writer.writerow(row)
                        f.flush()
                        n_rows = len(rows)
                        del rows
                        prog["done"].append(week)
                        prog["n_events_total"] += n_rows
                        save_progress(prog)  # クラッシュ時の重複書き込みを防ぐため毎回保存
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
