"""[2026-07-22] 中間発表(7/31)用の図を生成する。

出力: results/figures_interim2026/
  fig1_nfw_density.png            スライド1: NFW密度(中心集中が一目で分かる)
  fig5_loopI_bubble_shapes.png    スライド5: Loop I / フェルミバブル テンプレートの形(目視検証用)
  fig9_component_overlay_vertical.png  スライド9: 成分スペクトル比較(縦並び・全f_n成分)

方針(feedback_plot_all_fitted_components): 倍率 f_n が掛かる成分は全て載せる
  = gas / ICS / iso / Loop I(a,b) / フェルミバブル正 fb / バブル負 fb_neg / halo
"""
from __future__ import annotations
import os, sys, json
os.environ.setdefault("MCMC_ULTRACLEAN", "1")
os.environ.setdefault("MCMC_PIXEL_DEG", "0.125")
os.environ.setdefault("MCMC_DISK_BUBBLE", "1")
os.environ.setdefault("MCMC_CELL_LIKELIHOOD", "1")
os.environ.setdefault("MCMC_SIGNFREE_HALO", "1")
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
plt.rcParams["font.family"] = "Noto Sans CJK JP"
sys.path.insert(0, "code")

from pathlib import Path
BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "results/figures_interim2026"
OUT.mkdir(parents=True, exist_ok=True)
RESDIR = BASE / "results/mcmc_allbins_gasICS_v15_specfaithful"

# ══════════════ fig1: NFW 密度(中心集中) ══════════════
RS, RHO_S, D_SUN = 21.0, 8.1e6, 8.0          # kpc, Msun/kpc^3, kpc (Via Lactea II)
n = 600
x = np.linspace(-30, 30, n); y = np.linspace(-30, 30, n)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)
xx = np.maximum(R, 0.05) / RS
rho = RHO_S / (xx * (1 + xx) ** 2)            # NFW: rho_s / (x (1+x)^2)

fig, ax = plt.subplots(figsize=(7.2, 6.2))
im = ax.imshow(rho, origin="lower", extent=(-30, 30, -30, 30),
               norm=LogNorm(vmin=np.percentile(rho, 5), vmax=rho.max()), cmap="inferno")
ax.plot(-D_SUN, 0, marker="*", ms=18, color="deepskyblue", mec="k", mew=0.8, zorder=5)
ax.annotate("太陽系\n(8 kpc)", xy=(-D_SUN, 0), xytext=(-25, 8), color="white", fontsize=11,
            arrowprops=dict(arrowstyle="->", color="white", lw=1.4))
ax.plot(0, 0, marker="+", ms=14, color="white", mew=2.0, zorder=5)
ax.annotate("銀河中心", xy=(0, 0), xytext=(4, -9), color="white", fontsize=11,
            arrowprops=dict(arrowstyle="->", color="white", lw=1.4))
ax.set_xlabel("銀河面内の距離 x [kpc]"); ax.set_ylabel("銀河面内の距離 y [kpc]")
ax.set_title("天の川のダークマター密度(NFWプロファイル)\n中心ほど密度が高い → 中心方向が最も信号を期待できる",
             fontsize=12)
cb = fig.colorbar(im, ax=ax, shrink=0.86)
cb.set_label(r"ダークマター密度 $\rho$ [$M_\odot$ kpc$^{-3}$]")
fig.tight_layout(); fig.savefig(OUT / "fig1_nfw_density.png", dpi=160); plt.close()
print("done fig1")

# ══════════════ fig9: 成分スペクトル(縦並び・全成分) ══════════════
S = json.load(open(RESDIR / "component_spectra.json"))
E = np.array(S["energies_gev"]); sp = S["e2dnde"]
ours = {
    "gas": np.array(sp["gas"]), "ics": np.array(sp["ics"]),
    "iso": np.array(sp["iso_counts"]),
    "loopI": np.array(sp["loopI_a"]) + np.array(sp["loopI_b"]),
    "ps": np.array(sp["ps"]), "fb": np.array(sp["fb"]), "fb_neg": np.abs(np.array(sp["fb_neg"])),
    "halo": np.array(sp["halo"]),
}
TOTANI = {  # Fig.6 目視読み取り(±30%)。fb/fb_neg は未デジタイズのため比較なし
    "gas":   [2.1e-3,1.6e-3,1.2e-3,9.5e-4,6.5e-4,5.0e-4,3.8e-4,2.8e-4,1.9e-4,1.0e-4,9e-5,9e-5,6e-5],
    "ics":   [9.0e-4,7.0e-4,5.5e-4,3.5e-4,2.0e-4,1.3e-4,1.0e-4,2.5e-5,3.5e-5,3.0e-5,1.5e-5,5e-6,6e-5],
    "iso":   [3.0e-4,2.3e-4,1.9e-4,1.6e-4,1.3e-4,1.0e-4,8.0e-5,8.0e-5,3.0e-5,np.nan,np.nan,np.nan,np.nan],
    "loopI": [4.5e-4,4.0e-4,3.5e-4,3.3e-4,2.0e-4,1.4e-4,1.3e-4,2.0e-5,np.nan,np.nan,np.nan,np.nan,np.nan],
    "halo":  [np.nan,5.0e-6,6.0e-5,1.3e-4,1.7e-4,1.8e-4,1.5e-4,1.05e-4,7.0e-5,6.0e-5,3.0e-5,1.8e-5,3.0e-5],
}
C = {"gas":"#1f77b4","ics":"#ff7f0e","iso":"#7f7f7f","loopI":"#9467bd",
     "fb":"#2ca02c","fb_neg":"#17becf","ps":"#8c564b","halo":"#d62728"}
L = {"gas":"gas","ics":"ICS","iso":"等方(iso)","loopI":"Loop I",
     "fb":"フェルミバブル(正)","fb_neg":"バブル(負)|絶対値|","ps":"既知点源","halo":"halo (NFW-ρ²)"}

fig, (axT, axB) = plt.subplots(2, 1, figsize=(8.6, 11.0), sharex=True)
for c in ["gas","ics","iso","ps","loopI","fb","fb_neg","halo"]:
    ls = "--" if c == "fb_neg" else "-"
    axT.plot(E, ours[c], ls, color=C[c], lw=2.3, label=f"{L[c]}(本研究)")
    if c in TOTANI:
        axT.plot(E, TOTANI[c], "o", color=C[c], mfc="none", ms=7, mew=1.6, ls=":", lw=0.9,
                 label=f"{L[c]}(Totani)")
axT.axvline(20.76, color="gold", ls="--", alpha=0.6)
axT.set_xscale("log"); axT.set_yscale("log"); axT.set_ylim(3e-6, 3e-3)
axT.set_ylabel(r"$E^2 dN/dE$ [MeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]")
axT.set_title("成分スペクトル: 本研究(線) vs Totani Fig.6(○, 目視±30%)\n"
              "※倍率 $f_n$ が掛かる全成分を表示(バブル正負を含む)", fontsize=12)
axT.legend(fontsize=8, ncol=2, loc="lower left")
axT.grid(alpha=0.25)

for c in ["gas","ics","iso","loopI","halo"]:
    axB.plot(E, ours[c] / np.array(TOTANI[c]), "o-", color=C[c], lw=2, ms=6, label=L[c])
axB.axhline(1.0, color="k", lw=1.2)
axB.axhspan(0.7, 1.4, color="green", alpha=0.10)
axB.axvline(20.76, color="gold", ls="--", alpha=0.6)
axB.set_xscale("log"); axB.set_yscale("log"); axB.set_ylim(0.05, 12)
axB.set_xlabel("エネルギー [GeV]"); axB.set_ylabel("本研究 / Totani")
axB.set_title("Totani との比(1.0=一致、緑帯=±40%)\nバブル正負はTotani値未デジタイズのため比は省略", fontsize=12)
axB.legend(fontsize=9, ncol=3); axB.grid(alpha=0.25)
fig.tight_layout(); fig.savefig(OUT / "fig9_component_overlay_vertical.png", dpi=160); plt.close()
print("done fig9")

# ══════════════ fig5: Loop I / バブル テンプレートの形 ══════════════
import mcmc_fit_all_bins as m, plot_skymap_all_subtracted as _sub
s1, s2 = _sub.loop_i_shell_templates()
B_GRID_ = _sub.B_GRID
dfb = m.load_events_with_disk()
bpos, bneg = m.build_bubble_counts_template(dfb)
ext = (60, -60, -60, 60)   # l は左右反転(銀経の慣習)
panels = [("Loop I shell1 (l=341°, b=3°)", s1), ("Loop I shell2 (l=332°, b=37°)", s2),
          ("フェルミバブル 正テンプレート", bpos), ("フェルミバブル 負テンプレート", bneg)]
fig, axs = plt.subplots(2, 2, figsize=(13.0, 9.4))
for ax, (title, arr) in zip(axs.ravel(), panels):
    a = np.asarray(arr).astype(float).copy()
    a[np.abs(B_GRID_) < 10] = np.nan     # 解析で使わない |b|<10 は非表示
    v = a[np.isfinite(a) & (a > 0)]
    vmax = np.percentile(v, 99) if v.size else 1.0
    a = a.T
    im = ax.imshow(a, origin="lower", extent=ext, aspect="auto", cmap="inferno", vmin=0, vmax=vmax)
    ax.plot([22,22,-22,-22,22], [10,55,55,10,10], color="lime", lw=1.3)   # バブル矩形(北)
    ax.plot([22,22,-22,-22,22], [-10,-55,-55,-10,-10], color="lime", lw=1.3)
    ax.set_title(title, fontsize=11); ax.set_xlabel("銀経 l [deg]"); ax.set_ylabel("銀緯 b [deg]")
    fig.colorbar(im, ax=ax, shrink=0.85)
fig.suptitle("Loop I とフェルミバブルのテンプレート形状(目視検証用)\n"
             "解析域 |b|≥10° のみ表示。緑枠=バブル矩形 |l|<22°, 10°<|b|<55°(バブル本体がこの枠内に見えるべき)", fontsize=13)
fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig(OUT / "fig5_loopI_bubble_shapes.png", dpi=150); plt.close()
print("done fig5")
print(f"出力先: {OUT}")
