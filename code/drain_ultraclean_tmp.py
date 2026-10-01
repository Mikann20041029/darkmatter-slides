"""[2026-07-19] 40並列DLがパースを溢れさせTMPに堆積したFITSを直接パースして
CSVに書き込む(ダウンロード無しなのでI/O競合ゼロで高速)。rebuild_ultraclean の
parse_and_filter / CSV / progress をそのまま再利用。処理済みは削除・progress更新。
"""
import sys, csv, glob, re
import pathlib as _pathlib
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.insert(0, "code")
import rebuild_ultraclean_week780 as R

R.set_memory_guard()
prog = R.load_progress()
done = set(prog["done"])

fits_files = sorted(glob.glob(str(R.TMP / "w*.fits")))
print(f"TMP堆積FITS: {len(fits_files)}個, 既存done: {len(done)}週")

hh = "a" if R.OUT_HALO.exists() else "w"
dd = "a" if R.OUT_DISK.exists() else "w"

def week_of(p):
    m = re.search(r"w(\d+)\.fits", p)
    return int(m.group(1)) if m else None

n_done = n_skip = n_fail = 0
with open(R.OUT_HALO, hh, newline="", encoding="utf-8") as fh, \
     open(R.OUT_DISK, dd, newline="", encoding="utf-8") as fd:
    wh, wd = csv.writer(fh), csv.writer(fd)
    # 4ワーカーでパース(DL無しなのでメモリ・I/Oに余裕)
    with ThreadPoolExecutor(max_workers=4) as ex:
        fut_week = {}
        for p in fits_files:
            wk = week_of(p)
            if wk is None or wk in done:
                _pathlib.Path(p).unlink(missing_ok=True); n_skip += 1; continue
            fut_week[ex.submit(R.parse_and_filter, _pathlib.Path(p))] = wk
        for fut in as_completed(fut_week):
            wk = fut_week[fut]
            res = fut.result()
            if res is None:
                n_fail += 1; print(f"  w{wk:03d} パース失敗"); continue
            halo_rows, disk_rows = res
            for r in halo_rows: wh.writerow(r)
            for r in disk_rows: wd.writerow(r)
            fh.flush(); fd.flush()
            prog["done"].append(wk)
            prog["n_halo"] += len(halo_rows); prog["n_disk"] += len(disk_rows)
            R.save_progress(prog)
            n_done += 1
            if n_done % 25 == 0:
                print(f"  {n_done}週 drain完了 (halo={prog['n_halo']} disk={prog['n_disk']})", flush=True)

print(f"\ndrain完了: {n_done}週処理, {n_skip}スキップ, {n_fail}失敗")
print(f"  progress: {len(prog['done'])}/779週 done, 残り{779-len(prog['done'])}週")
