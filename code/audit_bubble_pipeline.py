"""[2026-07-23] バブルテンプレート構築を1工程ずつ追跡し、どこでバブルが消えるかを特定する。

各工程後に「バブル矩形(|l|<22, 10<|b|<55)内 vs 外」のカウント密度を測る。
本物のバブルがあれば in/out 比 > 1 で、工程を経ても保たれるはず。
"""
from __future__ import annotations
import os, sys
os.environ.setdefault("MCMC_ULTRACLEAN", "1")
os.environ.setdefault("MCMC_PIXEL_DEG", "0.125")
os.environ.setdefault("MCMC_DISK_BUBBLE", "1")
import numpy as np
sys.path.insert(0, "code")
import mcmc_fit_all_bins as m
import plot_skymap_all_subtracted as _sub

LG, BG = _sub.L_GRID, _sub.B_GRID
roi = (np.abs(BG) >= 10) & (np.abs(BG) <= 60)          # 解析で実際に使う領域
box = (np.abs(LG) < 22) & (np.abs(BG) >= 10) & (np.abs(BG) < 55)   # バブル矩形
out = roi & ~box

def report(tag, a):
    """バブル矩形の内外でカウント密度を比較。in/out>1 ならバブルが残っている。"""
    a = np.asarray(a, dtype=float)
    i, o = a[box].mean(), a[out].mean()
    tot = a[roi].sum()
    frac = a[box].sum() / tot if tot != 0 else np.nan
    print(f"  {tag:34s} in={i:+10.5f}  out={o:+10.5f}  in-out={i-o:+10.5f}  "
          f"in/out={(i/o if o != 0 else np.nan):8.3f}  矩形内割合={100*frac:5.1f}%")

ib = _sub.BUBBLE_TEMPLATE_BIN
emin, emax = _sub.BIN_EDGES[ib], _sub.BIN_EDGES[ib + 1]
print(f"=== バブル構築ビン Bin{ib+1} ({_sub.BIN_CENTERS[ib]:.2f} GeV) / 矩形の面積比={100*box[roi].mean():.1f}% ===")

df = m.load_events_with_disk()
sel = df[(df.energy_GeV >= emin) & (df.energy_GeV < emax)]
counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
counts = counts.astype(float)
report("0. 生カウント", counts)

# [2026-07-23] 等方背景の事前減算は廃止済み(iso は構築フィットに同時投入)。
# 実際の build_fermi_bubble_templates_posneg と同じ経路を測るため、ここでも行わない。
c1, _, _ = _sub.subtract_point_sources(counts, emin, emax)
report("1. 点源を先に引いた後", c1)

c2, subtracted, lab = _sub.subtract_galactic_diffuse_with_gce(c1, emin, emax)
print(f"     [{lab}]")
report("2. GALPROP+GCE を引いた後", c2)
report("   (参考) 引いた量 subtracted", subtracted)

c3 = c2
report("3. (点源はGALPROP前に減算済み)", c3)

_sigpx = 1.0 / _sub.PIXEL_DEG
from scipy.ndimage import gaussian_filter
c3s = gaussian_filter(c3, _sigpx)
pos_s = np.maximum(c3s, 0.0); neg_s = np.maximum(-c3s, 0.0)


report("4a. 正テンプレート(平滑後)", pos_s)
report("4b. 負テンプレート(平滑後)", neg_s)

# 補足: 等方背景の引きすぎ確認(|b|>50 はバブル上端 55° と重なる)
hi = (np.abs(BG) > 50) & (np.abs(BG) <= 60)
hib = hi & (np.abs(LG) < 22)
print(f"\n[確認] subtract_isotropic の基準域 |b|>50 のうち、バブル矩形と重なる画素の割合 = "
      f"{100*hib.sum()/hi.sum():.1f}%  → 基準域にバブルが混入していれば引きすぎになる")
