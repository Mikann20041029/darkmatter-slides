"""[2026-07-18] 低E偽haloの正体診断: halo無し残差をフェルミバブル領域内外に分割。
残差はバブル領域内で正・外で負、haloの57%がバブル領域に重なりその残差を吸う。
低Eほどバブルが明るく残差が大きい→低EでΔlnL爆発(=偽halo)。バブルテンプレートが
バブル光を吸いきれず余りをhaloが拾う機序を定量化。regionAC所見と整合。"""
"""低E(Bin2=2.5GeV)と20GeV(Bin6)の残差マップを並べ、偽haloが吸う残差の形を見る。"""
from pathlib import Path
import json, sys
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.ndimage import gaussian_filter
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
plt.rcParams["font.family"] = "Noto Sans CJK JP"
sys.path.insert(0, "code")
import mcmc_fit_all_bins as m
import plot_skymap_all_subtracted as _sub

BASE = Path(".")
RES = json.load(open("results/mcmc_allbins_gasICS_v6_isofree/halo_spectrum.json"))
expmaps, _ = m.load_exposure_maps(); df = m.load_all_events()
j_map = m.nfw_j_map(); bpos, bneg = m.build_bubble_counts_template(df)
nfw_norm, _ = m.calibrate_nfw_norm(expmaps[5], j_map); s1, s2 = _sub.loop_i_shell_templates()

def analyze(IB):
    lo, hi = m.BIN_EDGES[IB], m.BIN_EDGES[IB+1]
    sel = df[(df.energy_GeV >= lo) & (df.energy_GeV < hi)]
    counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
    gas_i, ics_i = _sub._load_galprop_gas_ics_templates(lo, hi)
    t = m.build_templates_for_bin(IB, counts, expmaps[IB], gas_i, ics_i,
        bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
        expmap_bubble_bin=expmaps[m.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
        loop_shell1=s1, loop_shell2=s2)
    masked, _ = _sub.mask_point_sources(counts.copy())
    roi = (np.abs(m.BG) >= 10) & (np.abs(m.BG) <= 60) & ~np.isnan(masked)
    pnh = RES["bins"][IB]["params_no_halo_pointest"]
    order = ["f_iso","f_gas","f_ics","f_loopI_a","f_loopI_b","f_fb","f_fb_neg"]
    keys = ["iso_counts","gas","ics","loopI_a","loopI_b","fb","fb_neg"]
    mnh = np.zeros_like(counts)
    for pk, tk in zip(order, keys): mnh += pnh[pk]*t[tk]
    resid = counts - mnh
    p = RES["bins"][IB]["params"]; halo = p["f_halo"]["median"]*t["halo"]
    # 残差 vs 各テンプレートの空間相関(何を吸っているか)
    corr = {}
    for tk in ["halo","gas","ics","loopI_a","fb"]:
        corr[tk] = float(np.corrcoef(resid[roi], t[tk][roi])[0,1])
    return dict(counts=counts, roi=roi, resid=resid, halo=halo, t=t, corr=corr,
                e=m.BIN_CENTERS[IB], fhalo=p["f_halo"]["median"], sig=RES["bins"][IB]["significance_sigma"])

def smooth(a, roi):
    out = a.copy(); out[~roi] = 0.0; return gaussian_filter(out, 1.0)

def sky(ax, a, roi, title, div=True):
    aa = a.copy().astype(float); aa[~roi]=np.nan
    if div:
        lim = np.nanpercentile(np.abs(a[roi]), 98)
        im = ax.pcolormesh(_sub.L_BINS,_sub.B_BINS,aa.T,cmap="RdBu_r",norm=mcolors.TwoSlopeNorm(0,-lim,lim))
    else:
        im = ax.pcolormesh(_sub.L_BINS,_sub.B_BINS,aa.T,cmap="inferno")
    ax.axhspan(-10,10,color="gray",alpha=0.5); ax.set_xlim(-60,60); ax.set_ylim(-60,60)
    ax.set_title(title,fontsize=9); ax.set_xlabel("l",fontsize=8); ax.set_ylabel("b",fontsize=8)
    plt.colorbar(im,ax=ax,fraction=0.046,pad=0.04)

fig, axs = plt.subplots(2, 3, figsize=(17, 10))
for row, IB in enumerate([1, 5]):  # Bin2=2.5GeV, Bin6=20.76GeV
    r = analyze(IB)
    sky(axs[row,0], smooth(r["resid"],r["roi"]), r["roi"], f"{r['e']:.1f}GeV halo無し残差 (σ={r['sig']:.0f})")
    sky(axs[row,1], smooth(r["halo"],r["roi"]), r["roi"], f"{r['e']:.1f}GeV haloテンプレ×f_halo", div=False)
    sky(axs[row,2], smooth(r["t"]["gas"],r["roi"]), r["roi"], f"{r['e']:.1f}GeV gasテンプレ", div=False)
    print(f"Bin{IB+1} {r['e']:.2f}GeV σ={r['sig']:.1f} f_halo={r['fhalo']:.3g}")
    print(f"  残差との空間相関: " + "  ".join(f"{k}={v:+.3f}" for k,v in r["corr"].items()))
fig.suptitle("低E(上,2.5GeV) vs 20GeV(下): halo無し残差の形と、halo/gasテンプレの形",fontsize=13)
fig.tight_layout(rect=(0,0,1,0.96))
fig.savefig("results/mcmc_allbins_gasICS_v6_isofree/repro_lowE_vs_20GeV_residual.png",dpi=110)
print("完成: results/mcmc_allbins_gasICS_v6_isofree/repro_lowE_vs_20GeV_residual.png")

# バブル領域(|l|<22, 10<|b|<55)内外で残差・haloを分ける
print("\n=== バブル領域 内 vs 外 の残差/halo(counts合計) ===")
for IB in [1,5]:
    r=analyze(IB); roi=r["roi"]
    bub=(np.abs(m.LG)<22)&(np.abs(m.BG)>=10)&(np.abs(m.BG)<55)&roi
    out=roi&~bub
    print("Bin%d %.1fGeV: 残差[バブル内=%+.0f 外=%+.0f]  halo[内=%.0f 外=%.0f]  (内割合 halo=%.0f%%)"%(
        IB+1,r["e"],r["resid"][bub].sum(),r["resid"][out].sum(),
        r["halo"][bub].sum(),r["halo"][out].sum(),
        100*r["halo"][bub].sum()/max(r["halo"][roi].sum(),1)))
    print("   バブル内 有効画素=%d / ROI全体=%d (面積割合=%.0f%%)"%(bub.sum(),roi.sum(),100*bub.sum()/roi.sum()))
