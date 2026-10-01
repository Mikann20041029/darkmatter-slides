"""[2026-07-19] バブルテンプレート検証(halo過大の最有力容疑 P2)。
「halo無し残差=翼を引きすぎ・中心取り残し」がバブル形状のズレか、を空間で見る。
UltraClean・1°。バブル正/負テンプレ、f_fbスケール後のバブル、halo無し残差、haloテンプレを
スカイマップで並べ、バブル領域の翼(|l|>15)と中心(|l|<15)での引き残しを定量。
出力: results/mcmc_allbins_gasICS_v11_ultraclean_hires/diag_bubble_shape.{png,txt}
"""
from __future__ import annotations
import os
os.environ.setdefault("MCMC_ULTRACLEAN", "1"); os.environ.setdefault("MCMC_PIXEL_DEG", "1.0")
os.environ.setdefault("MCMC_DISK_BUBBLE", "1"); os.environ.setdefault("MCMC_SIGNFREE_HALO", "1")
os.environ.setdefault("MCMC_CELL_LIKELIHOOD", "0")
import sys
import numpy as np
from scipy.optimize import minimize
from scipy.ndimage import gaussian_filter
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
plt.rcParams["font.family"] = "Noto Sans CJK JP"
sys.path.insert(0, "code")
import mcmc_fit_all_bins as m
import plot_skymap_all_subtracted as _sub

OUT = "results/mcmc_allbins_gasICS_v11_ultraclean_hires"
BG, LG = m.BG, m.LG
expmaps, _ = m.load_exposure_maps(); df = m.load_all_events()
j_map = m.nfw_j_map(); nfw_norm, _ = m.calibrate_nfw_norm(expmaps[5], j_map)
dfb = m.load_events_with_disk(); bpos, bneg = m.build_bubble_counts_template(dfb)
s1, s2 = _sub.loop_i_shell_templates()
ib = 5; lo, hi = m.BIN_EDGES[ib], m.BIN_EDGES[ib + 1]
sel = df[(df.energy_GeV >= lo) & (df.energy_GeV < hi)]
counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
gas_i, ics_i = _sub._load_galprop_gas_ics_templates(lo, hi)
t = m.build_templates_for_bin(ib, counts, expmaps[ib], gas_i, ics_i,
    bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
    expmap_bubble_bin=expmaps[m.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
    loop_shell1=s1, loop_shell2=s2)
masked, _ = _sub.mask_point_sources(counts.copy())
roi = (~np.isnan(masked)) & (np.abs(BG) >= 10) & (np.abs(BG) <= 60)

# halo無しフル + fb_neg(符号自由)を含めて点推定
keys = ["iso_counts", "gas", "ics", "loopI_a", "loopI_b", "fb", "fb_neg"]
A = np.array([t[k][roi] for k in keys]); c = counts[roi]
signs = [0, 0, 0, 0, 0, 0, 1]  # fb_negのみ符号自由
def nll(f):
    mu = np.maximum(f @ A, 1e-10); return -np.sum(c * np.log(mu) - mu)
bounds = [(None, None) if s else (0, None) for s in signs]
r = minimize(nll, np.full(len(keys), 0.3), method="L-BFGS-B", bounds=bounds)
f = dict(zip(keys, r.x))
model = np.zeros_like(counts)
for k in keys: model += f[k] * t[k]
resid = counts - model
fb_scaled = f["fb"] * t["fb"]

# バブル領域 翼 vs 中心 の残差
bub = roi & (np.abs(LG) < 22) & (np.abs(BG) >= 10) & (np.abs(BG) < 55)
wing = bub & (np.abs(LG) >= 15)
cen = bub & (np.abs(LG) < 15) & (np.abs(BG) < 25)
lines = []
lines.append("halo無しフィット振幅: " + " ".join(f"{k}={v:.3f}" for k, v in f.items()))
lines.append(f"バブル領域 翼(|l|15-22): 残差={resid[wing].sum():+.0f} counts (平均{resid[wing].mean():+.3f})")
lines.append(f"バブル領域 中心(|l|<15,|b|<25): 残差={resid[cen].sum():+.0f} counts (平均{resid[cen].mean():+.3f})")
lines.append(f"バブル正テンプレ 翼合計={t['fb'][wing].sum()*f['fb']:.0f} 中心合計={t['fb'][cen].sum()*f['fb']:.0f}")
lines.append("→ 中心残差>0 かつ 翼残差<0 なら『バブルが翼を引きすぎ・中心取り残し』=形状ズレ確定")
txt = "\n".join(lines); print(txt); open(f"{OUT}/diag_bubble_shape.txt", "w").write(txt)

def sky(ax, arr, title, div=True):
    a = arr.astype(float).copy(); a[~roi] = np.nan
    sm = a.copy(); sm[np.isnan(sm)] = 0; sm = gaussian_filter(sm, 1.0); sm[~roi] = np.nan
    if div:
        lim = np.nanpercentile(np.abs(a[roi]), 98) or 1
        im = ax.pcolormesh(_sub.L_BINS, _sub.B_BINS, sm.T, cmap="RdBu_r", norm=mcolors.TwoSlopeNorm(0, -lim, lim))
    else:
        im = ax.pcolormesh(_sub.L_BINS, _sub.B_BINS, sm.T, cmap="inferno")
    # バブル矩形
    for sgn in (1, -1):
        ax.plot([-22, 22, 22, -22, -22], [sgn*10, sgn*10, sgn*55, sgn*55, sgn*10], "g-", lw=1, alpha=0.7)
    ax.axhspan(-10, 10, color="gray", alpha=0.4); ax.set_xlim(-60, 60); ax.set_ylim(-60, 60)
    ax.set_title(title, fontsize=9); plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

fig, axs = plt.subplots(1, 4, figsize=(22, 5))
sky(axs[0], resid, "halo無し残差(緑=バブル矩形)")
sky(axs[1], fb_scaled, "バブル正×f_fb", div=False)
sky(axs[2], f["fb_neg"] * t["fb"] if False else t["fb_neg"] * f["fb_neg"], "バブル負×f_fb_neg")
sky(axs[3], f.get("_halo", 1) * t["halo"], "NFW haloテンプレ", div=False)
fig.suptitle("バブル形状検証(20GeV, UltraClean): 残差が『翼引きすぎ+中心取り残し』か", fontsize=13)
fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig(f"{OUT}/diag_bubble_shape.png", dpi=115)
print(f"\n完成: {OUT}/diag_bubble_shape.{{png,txt}}")
