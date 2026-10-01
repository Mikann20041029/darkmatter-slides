"""[2026-07-27] 全天 UltraClean イベントの取得 (矮小銀河5天体・M31 への v20 手法適用用)。

背景:
  既存の UltraClean CSV 2 本 (filtered_events_week780_ultraclean.csv /
  disk_bl10_week780_ultraclean.csv) は実測で l∈[-60,60], b∈[-60,60] に限定されており、
  対象 6 天体 (Draco l=86.4 / Sculptor b=-83.2 / Ursa Minor l=105.0 / Segue 1 l=-139.5 /
  Coma Berenices b=+83.6 / M31 l=121.2) は **全て範囲外**。
  一方 data/CSV/allsky_events.csv は全天だが、rebuild_allsky_events.py に EVENT_CLASS 選別が
  無く UltraClean 選別が入っていない (= weekly photon file の既定クラスのまま)。
  よって v20 と同じ選別で他天体を解析するには全天 UltraClean を取り直す必要がある。

  今回は **空間カットを一切かけずに** 全天分を保存し、以後どの天体を追加しても
  再ダウンロードが不要になるようにする (l・b とも無制限、E>=1 GeV と zenith<100° のみ)。

UltraClean 選別: EVENT_CLASS は 32X (shape=(N,32) bool)。astropy col j = bit(31-j)。
P8R3 ULTRACLEAN = evclass 2^9 → col(31-9) = col22 が True。
(rebuild_ultraclean_week780.py と同一の選別。差は空間カットの有無のみ)

出力 (既存ファイルは一切変更しない):
  data/CSV/allsky_events_ultraclean.csv   (全天, E>=1 GeV, zenith<100°, UltraClean)

安全設計 (rebuild_ultraclean_week780.py を踏襲):
  - ⚠️ **[2026-07-28 訂正] WSL の / (/dev/sdd) は C: 上の仮想ディスクである**。
    実体は C:\\Users\\arsei\\AppData\\Local\\wsl\\{760fa712-...}\\ext4.vhdx (実測 87.9 GB)。
    既存スクリプト (rebuild_ultraclean_week780.py) の「/dev/sdd は C: とは別ディスク」
    という記述は誤りで、**/tmp や /home への書き込みは C: を消費する**。
    しかも vhdx はファイル削除では縮まないため、消費は恒久的に残る。
    → 大容量の一時ファイルを扱う前に必ず `df -h /mnt/c` で C: の空きを確認すること
  - DL 並列 12 / パース並列 3 / RLIMIT_AS 3 GB / FITS はパース後すぐ削除
  - 未処理の週を MAX_INFLIGHT 件までに絞る背圧制御を追加し、TMP のピーク使用量を
    約 190 MB x MAX_INFLIGHT に抑える (元スクリプトは 780 週を一括投入するため、
    DL がパースを追い越すと TMP に数十 GB 溜まりうる)。既定 8 週 = ピーク約 1.5 GB
  - 中断しても results/rebuild_ultraclean_allsky_progress.json から再開できる

規模: weekly photon file は 1 本 190 MB、780 週で計 148 GB を転送する (逐次削除するので
残るのは出力 CSV のみ)。
"""
from __future__ import annotations

import csv
import json
import os
import pathlib as _pathlib
import resource
import subprocess
import time
from concurrent.futures import Future, ThreadPoolExecutor, FIRST_COMPLETED, wait

import numpy as np
from astropy.io import fits

BASE = _pathlib.Path(__file__).resolve().parent.parent
TMP = _pathlib.Path("/tmp/fermi_rebuild_uc_allsky")
TMP.mkdir(parents=True, exist_ok=True)
OUT_ALLSKY = BASE / "data/CSV/allsky_events_ultraclean.csv"
PROGRESS = BASE / "results/rebuild_ultraclean_allsky_progress.json"
PROGRESS.parent.mkdir(parents=True, exist_ok=True)
(BASE / "data/CSV").mkdir(parents=True, exist_ok=True)

WEEKS: list[int] = list(range(9, 789))  # w009〜w788 (780 週)
_NCPU = len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else 4
N_DOWNLOAD_WORKERS = int(os.environ.get("DL_WORKERS", max(4, _NCPU * 3)))   # 既定 12
N_PARSE_WORKERS = int(os.environ.get("PARSE_WORKERS", max(2, _NCPU - 1)))   # 既定 3
# [2026-07-28] /tmp は C: 上の vhdx を消費するので既定を 24→8 週に下げた (ピーク ~1.5 GB)。
# C: に十分な空きがあるなら MAX_INFLIGHT=24 で少し速くなる。
MAX_INFLIGHT = int(os.environ.get("MAX_INFLIGHT", 8))   # TMP ピーク ~1.5 GB
MEMORY_LIMIT_BYTES = 3 * 1024 ** 3      # 3 GiB 安全弁

E_MIN_GEV = 1.0
ZENITH_MAX = 100.0
UC_COL = 31 - 9   # UltraClean (evclass 2^9) の EVENT_CLASS 32X 列
COLUMNS = ["energy_GeV", "l_deg", "b_deg", "ra_deg", "dec_deg", "zenith_angle_deg", "time_met_s"]

Row = tuple[str, str, str, str, str, str, str]


def set_memory_guard() -> None:
    try:
        resource.setrlimit(resource.RLIMIT_AS, (MEMORY_LIMIT_BYTES, MEMORY_LIMIT_BYTES))
    except (ValueError, OSError) as e:
        print(f"警告: メモリ上限設定に失敗 ({e})。安全弁なしで続行。")


def load_progress() -> dict[str, object]:
    if PROGRESS.exists():
        with open(PROGRESS) as f:
            return json.load(f)
    return {"done": [], "failed": [], "n_events": 0}


def save_progress(prog: dict[str, object]) -> None:
    with open(PROGRESS, "w") as f:
        json.dump(prog, f)


def download_week(week: int) -> tuple[int, _pathlib.Path | None]:
    url = (f"https://heasarc.gsfc.nasa.gov/FTP/fermi/data/lat/weekly/photon/"
           f"lat_photon_weekly_w{week:03d}_p305_v001.fits")
    fname = TMP / f"w{week:03d}.fits"
    try:
        proc = subprocess.run(["wget", "-q", "--timeout=600", "-t", "2", url, "-O", str(fname)],
                              timeout=1800)
    except subprocess.TimeoutExpired:
        fname.unlink(missing_ok=True)
        return week, None
    if proc.returncode != 0 or not fname.exists() or fname.stat().st_size < 1e5:
        fname.unlink(missing_ok=True)
        return week, None
    return week, fname


def parse_and_filter(fname: _pathlib.Path) -> list[Row] | None:
    """UltraClean のみ選別して全天の行を返す (空間カットなし)。"""
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

    idx = np.where((energy_gev >= E_MIN_GEV) & (zenith < ZENITH_MAX) & uc)[0]
    return [(f"{energy_gev[i]:.5f}", f"{l[i]:.5f}", f"{b[i]:.5f}",
             f"{ra[i]:.5f}", f"{dec[i]:.5f}", f"{zenith[i]:.3f}", f"{time_met[i]:.2f}")
            for i in idx]


def main() -> None:
    set_memory_guard()
    prog = load_progress()
    done = set(prog["done"])                    # type: ignore[arg-type]
    remaining = [w for w in WEEKS if w not in done]

    mode = "a" if OUT_ALLSKY.exists() else "w"
    write_header = not OUT_ALLSKY.exists()

    print(f"全天 UltraClean 取得: {len(WEEKS)}週中 {len(remaining)}週 未処理 "
          f"(DL並列={N_DOWNLOAD_WORKERS}, パース並列={N_PARSE_WORKERS}, "
          f"同時保持={MAX_INFLIGHT}週, メモリ上限={MEMORY_LIMIT_BYTES/1e9:.1f}GB, "
          f"保存先=/dev/sdd)", flush=True)
    t0 = time.time()

    with open(OUT_ALLSKY, mode, newline="", encoding="utf-8") as fh:
        w_out = csv.writer(fh)
        if write_header:
            fh.write("# " + " | ".join(COLUMNS) + "\n")
            w_out.writerow(COLUMNS)

        n_done = n_fail = 0
        queue = list(remaining)
        with ThreadPoolExecutor(max_workers=N_DOWNLOAD_WORKERS) as dl_ex, \
             ThreadPoolExecutor(max_workers=N_PARSE_WORKERS) as parse_ex:
            dl_week_of: dict[Future, int] = {}
            parse_week_of: dict[Future, int] = {}
            pending: set[Future] = set()

            def refill() -> None:
                """未完了 (DL 中 + パース待ち + パース中) を MAX_INFLIGHT 件までに保つ。"""
                while queue and len(pending) < MAX_INFLIGHT:
                    wk = queue.pop(0)
                    fut = dl_ex.submit(download_week, wk)
                    dl_week_of[fut] = wk
                    pending.add(fut)

            refill()
            while pending:
                finished, pending = wait(pending, return_when=FIRST_COMPLETED)
                for fut in finished:
                    if fut in dl_week_of:
                        week = dl_week_of.pop(fut)
                        _, fname = fut.result()
                        if fname is None:
                            n_fail += 1
                            prog["failed"].append(week)  # type: ignore[union-attr]
                            print(f"  w{week:03d}: DL失敗", flush=True)
                            continue
                        pfut = parse_ex.submit(parse_and_filter, fname)
                        parse_week_of[pfut] = week
                        pending.add(pfut)
                    else:
                        week = parse_week_of.pop(fut)
                        rows = fut.result()
                        if rows is None:
                            n_fail += 1
                            prog["failed"].append(week)  # type: ignore[union-attr]
                            print(f"  w{week:03d}: パース失敗", flush=True)
                            continue
                        for r in rows:
                            w_out.writerow(r)
                        fh.flush()
                        prog["done"].append(week)        # type: ignore[union-attr]
                        prog["n_events"] = int(prog["n_events"]) + len(rows)  # type: ignore[arg-type]
                        save_progress(prog)
                        n_done += 1
                        del rows
                        if n_done % 20 == 0:
                            el = time.time() - t0
                            rate = n_done / el * 60 if el > 0 else 0.0
                            eta = (len(remaining) - n_done) / max(rate, 1e-9)
                            print(f"  {n_done}/{len(remaining)}週 完了 "
                                  f"({rate:.2f}週/分, ETA {eta:.0f}分, "
                                  f"events={prog['n_events']})", flush=True)
                refill()

    dt = time.time() - t0
    print(f"\n完了: {n_done}週処理, {n_fail}週失敗, {dt/60:.1f}分")
    print(f"  全天 UltraClean: {prog['n_events']} 事象 → {OUT_ALLSKY}")


if __name__ == "__main__":
    main()
