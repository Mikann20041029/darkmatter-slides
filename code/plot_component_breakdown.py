"""
MCMC_VERIFICATION.md 向けの補助図: Bin6(20.76GeV)で、各成分(ISO・GAL・LoopI×2・
FB・FBneg・HALO)が実際にどれだけの「明るさ」(1ピクセルあたりの平均カウント数)を
担っているかを積み上げ棒グラフにする。「なぜf_◯という倍率が必要なのか」を
具体的な数字で見せるための図。

出力: mcmc_verification_images/component_breakdown_bin6.png
"""
import sys
import warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, "code")

import numpy as np
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"

import mcmc_fit_all_bins as mfa
import plot_skymap_all_subtracted as _sub

print("読み込み中...")
expmaps, _ = mfa.load_exposure_maps()
df_all = mfa.load_all_events()
j_map = mfa.nfw_j_map()
nfw_norm, calib = mfa.calibrate_nfw_norm(expmaps[5], j_map)
bpos, bneg = mfa.build_bubble_counts_template(df_all)
loop1, loop2 = _sub.loop_i_shell_templates()

ib = 5  # Bin6
emin, emax = mfa.BIN_EDGES[ib], mfa.BIN_EDGES[ib + 1]
sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
masked, _ = _sub.mask_point_sources(counts.copy())
valid = ~np.isnan(masked)
valid &= (np.abs(mfa.BG) >= 10) & (np.abs(mfa.BG) <= 60)
galflux = _sub._load_galprop_template(emin, emax)
t = mfa.build_templates_for_bin(ib, counts, expmaps[ib], galflux, bpos, bneg,
                                 expmaps[mfa.BUBBLE_BIN], j_map, nfw_norm, loop1, loop2)

fit = json.load(open("results/mcmc_allbins/mcmc_bin06.json"))
p = fit["params"]
f_gal = p["f_gal"]["median"]
f_la = p["f_loopI_a"]["median"]
f_lb = p["f_loopI_b"]["median"]
f_fb = p["f_fb"]["median"]
f_fbneg = p["f_fb_neg"]["median"]
f_halo = p["f_halo"]["median"]

iso_mean = t["iso_counts"][valid].mean()
gal_mean = (f_gal * t["gal"])[valid].mean()
la_mean = (f_la * t["loopI_a"])[valid].mean()
lb_mean = (f_lb * t["loopI_b"])[valid].mean()
fb_mean = (f_fb * t["fb"])[valid].mean()
fbneg_mean = (f_fbneg * t["fb_neg"])[valid].mean()
halo_mean = (f_halo * t["halo"])[valid].mean()
data_mean = counts[valid].mean()

labels = ["①等方背景\n(ISO)", "②銀河の光\n(f_gal×GAL)", "③ループIa\n(f_a×LIa)",
          "④ループIb\n(f_b×LIb)", "⑤バブル正\n(f_fb×FB)", "⑥バブル負\n(f_neg×FBneg)",
          "⑦ハロー\n(f_halo×HALO)"]
values = [iso_mean, gal_mean, la_mean, lb_mean, fb_mean, fbneg_mean, halo_mean]
colors = ["#888888", "#ffcc00", "#44ff88", "#22cc66", "#ff8844", "#cc4444", "#00ffff"]

fig, ax = plt.subplots(figsize=(10, 6), facecolor="#05051A")
ax.set_facecolor("#05051A")
bottom = 0
for lab, val, col in zip(labels, values, colors):
    ax.bar(["予測の内訳"], [val], bottom=bottom, color=col, label=f"{lab}: {val:+.3f}", width=0.5)
    bottom += val
ax.axhline(data_mean, color="white", ls="--", lw=1.5)
ax.text(0.42, data_mean, f" 実測平均 = {data_mean:.3f}", color="white", va="center", fontsize=10)
ax.bar(["実測(参考)"], [data_mean], color="none", edgecolor="white", lw=2, width=0.5)

ax.set_ylabel("1ピクセルあたりの平均カウント数", color="white", fontsize=11)
ax.set_title("Bin6(20.76GeV)の予測内訳(積み上げ) vs 実測平均\n"
             "(有効ピクセル約1万個の平均値、点源マスク・|b|<10°除外後)", color="white", fontsize=12)
ax.tick_params(colors="white", labelsize=11)
for sp in ax.spines.values():
    sp.set_color("#666")
ax.legend(fontsize=9, loc="center left", bbox_to_anchor=(1.02, 0.5),
          facecolor="#0d0d2a", labelcolor="white", framealpha=0.95)
fig.tight_layout()
out = "mcmc_verification_images/component_breakdown_bin6.png"
fig.savefig(out, dpi=140, facecolor="#05051A", bbox_inches="tight")
print("saved:", out)
print(f"\n実測平均={data_mean:.4f}  予測合計={sum(values):.4f}")
for lab, val in zip(labels, values):
    print(f"  {lab.splitlines()[0]}: {val:+.4f}  ({val/data_mean*100:+.1f}%)")
