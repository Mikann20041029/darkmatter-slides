"""[2026-07-18] 検証①: うちのイベントサンプルにTotaniのUltraClean(P8R3)未適用の
背景がどれだけ混じっているかを、生の週次photon FITS 1週分のEVENT_CLASSで定量する。

重要: 週次photon FITS の EVENT_CLASS は `32X`(32ビットのbool配列)。astropyは
shape=(N,32) で返し、col j は bit(31-j)。Pass8 P8R3 クラスは evclass=2^b:
  TRANSIENT010=2^6, SOURCE=2^7, CLEAN=2^8, ULTRACLEAN=2^9, ULTRACLEANVETO=2^10。
UltraClean選別 = col(31-9)=col22 が True。うちのパイプラインはこのカットをしていない
(=SOURCE級の広いクラスを全採用)。うちのROI選別を適用した上でUltraClean率を出す。
100%未満なら差分がTotaniにない余分な背景(iso過大の候補)。

引数: FITSパス。出力: 標準出力 + JSON。
"""
import sys, json
from pathlib import Path
import numpy as np
from astropy.io import fits

fpath = sys.argv[1] if len(sys.argv) > 1 else None
assert fpath and Path(fpath).exists(), f"FITS not found: {fpath}"

BIN = [1.51, 2.55, 4.31, 7.28, 12.29, 20.76, 35.06, 59.22, 100.02, 168.93, 285.33, 481.93, 814.0]
c = np.array(BIN)
edges = np.zeros(14)
edges[1:-1] = np.sqrt(c[:-1] * c[1:]); edges[0] = c[0] ** 2 / edges[1]; edges[-1] = c[-1] ** 2 / edges[-2]

with fits.open(fpath, memmap=True) as h:
    d = h["EVENTS"].data
    ec = np.asarray(d["EVENT_CLASS"])          # (N,32) bool
    en = np.asarray(d["ENERGY"], float)        # MeV
    zn = np.asarray(d["ZENITH_ANGLE"], float)
    l = np.asarray(d["L"], float); b = np.asarray(d["B"], float)

# 本研究ROI選別に完全一致
sel = (en >= 1000.0) & (zn < 100.0) & (np.abs(l) <= 60) & (np.abs(b) >= 10) & (np.abs(b) <= 60)
CLASS_COL = {"SOURCE": 31 - 7, "CLEAN": 31 - 8, "ULTRACLEAN": 31 - 9, "ULTRACLEANVETO": 31 - 10}

n_sel = int(sel.sum())
frac_class = {name: float(ec[sel, col].mean()) for name, col in CLASS_COL.items()}
uc = ec[:, CLASS_COL["ULTRACLEAN"]]

print(f"FITS: {fpath}")
print(f"ROI選別(E>1GeV,zenith<100,|l|<=60,10<=|b|<=60)後: {n_sel} 事象")
print("\nクラス階層 通過率(nested=単調減少):")
for name in ["SOURCE", "CLEAN", "ULTRACLEAN", "ULTRACLEANVETO"]:
    print(f"  {name:16s}: {frac_class[name]*100:6.2f}%")
print(f"\n★ UltraClean率={frac_class['ULTRACLEAN']*100:.2f}%  "
      f"→ 非UltraClean混入={100*(1-frac_class['ULTRACLEAN']):.2f}%(Totaniは除外, うちは採用)")

per_bin = []
print("\nbin  E[GeV]     n   UltraClean%  非UC混入%")
for i in range(13):
    mm = sel & (en >= edges[i] * 1000) & (en < edges[i + 1] * 1000)
    n = int(mm.sum())
    fr = float(uc[mm].mean()) if n else float("nan")
    per_bin.append(dict(bin=i + 1, e=BIN[i], n=n, ultraclean_frac=fr))
    if n:
        print(f"{i+1:2d} {BIN[i]:7.1f}  {n:5d}    {fr*100:6.2f}%   {(1-fr)*100:5.2f}%")

out = dict(fits=str(Path(fpath).name), note="1週分(w300)。780週全体の代表値。",
           n_selected_roi=n_sel, frac_class_in_roi=frac_class,
           ultraclean_frac_overall=frac_class["ULTRACLEAN"],
           non_ultraclean_frac_overall=float(1 - frac_class["ULTRACLEAN"]),
           per_bin=per_bin)
outp = Path("results/mcmc_allbins_gasICS_v8_diskbubble/diag_eventclass_check.json")
json.dump(out, open(outp, "w"), ensure_ascii=False, indent=2)
print(f"\n完成: {outp}")
