"""[2026-07-18] Totani (2025) Fig.11(21 GeV残差マップ)とFig.14(テンプレート形)を
今の仕様(v6 iso自由化フィット)で再現する診断図。

目的(教授指示): Totaniが作っている図を今のパイプラインで再現し、値や形がTotaniと
大きく違う箇所から有意度過大の原因の手がかりを探す。
- Fig.11相当: halo無しフィットの残差マップ。「うちの20 GeV超過は、空の上でTotaniの
  ような球対称haloの形をしているか?」を直接見る。artifactなら形が崩れるはず。
- Fig.14相当: gas / Loop I(2シェル)/ ICS の各テンプレートの天球形状。
"""
from pathlib import Path
import json
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.ndimage import gaussian_filter
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
plt.rcParams["font.family"] = "Noto Sans CJK JP"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mcmc_fit_all_bins as m
import plot_skymap_all_subtracted as _sub

BASE = Path(__file__).resolve().parent.parent
RUN = "mcmc_allbins_gasICS_v6_isofree"
RES = json.load(open(BASE / f"results/{RUN}/halo_spectrum.json"))
IB = 5  # Bin6 = 20.76 GeV (Totaniの"21 GeV bin"に対応)

# --- Bin6 のテンプレート再構築(v6と同一手順) ---
expmaps, _ = m.load_exposure_maps()
df = m.load_all_events()
j_map = m.nfw_j_map()
bpos, bneg = m.build_bubble_counts_template(df)
nfw_norm, _ = m.calibrate_nfw_norm(expmaps[5], j_map)
s1, s2 = _sub.loop_i_shell_templates()

lo, hi = m.BIN_EDGES[IB], m.BIN_EDGES[IB + 1]
sel = df[(df.energy_GeV >= lo) & (df.energy_GeV < hi)]
counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
gas_i, ics_i = _sub._load_galprop_gas_ics_templates(lo, hi)
t = m.build_templates_for_bin(IB, counts, expmaps[IB], gas_i, ics_i,
    bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
    expmap_bubble_bin=expmaps[m.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
    loop_shell1=s1, loop_shell2=s2)

# 点源マスク + ROI (|b|>=10)
masked, _ = _sub.mask_point_sources(counts.copy())
roi = (np.abs(m.BG) >= 10) & (np.abs(m.BG) <= 60) & ~np.isnan(masked)

# no-haloモデル(v6の点推定パラメータ)で残差を作る
pnh = RES["bins"][IB]["params_no_halo_pointest"]  # f_iso..f_fb_neg
order = ["f_iso", "f_gas", "f_ics", "f_loopI_a", "f_loopI_b", "f_fb", "f_fb_neg"]
keys = ["iso_counts", "gas", "ics", "loopI_a", "loopI_b", "fb", "fb_neg"]
model_nohalo = np.zeros_like(counts)
for pk, tk in zip(order, keys):
    model_nohalo += pnh[pk] * t[tk]
residual = counts - model_nohalo   # Fig.11 top-left 相当

# halo テンプレート(参照: 残差がこの形に一致するか)
p = RES["bins"][IB]["params"]
halo_scaled = p["f_halo"]["median"] * t["halo"]

def sky(ax, arr, title, cmap, norm=None, mask_roi=True, vmin=None, vmax=None):
    a = arr.copy().astype(float)
    if mask_roi:
        a[~roi] = np.nan
    if norm is None:
        im = ax.pcolormesh(_sub.L_BINS, _sub.B_BINS, a.T, cmap=cmap, vmin=vmin, vmax=vmax)
    else:
        im = ax.pcolormesh(_sub.L_BINS, _sub.B_BINS, a.T, cmap=cmap, norm=norm)
    ax.axhspan(-10, 10, color="gray", alpha=0.5)
    ax.set_xlim(-60, 60); ax.set_ylim(-60, 60)
    ax.set_xlabel("l [deg]", fontsize=9); ax.set_ylabel("b [deg]", fontsize=9)
    ax.set_title(title, fontsize=10)
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

# σ=1°(=1px)ガウス平滑(Totaniと同じ)
def smooth(a):
    out = a.copy(); out[~roi] = 0.0
    return gaussian_filter(out, sigma=1.0)

# ===== Fig.11 相当 =====
fig1, axs = plt.subplots(1, 3, figsize=(18, 5))
rlim = np.nanpercentile(np.abs(residual[roi]), 98)
sky(axs[0], smooth(residual), "① halo無しフィットの残差\n(Totani Fig.11左上相当: 球対称haloに見えるか?)",
    "RdBu_r", norm=mcolors.TwoSlopeNorm(vcenter=0, vmin=-rlim, vmax=rlim))
sky(axs[1], smooth(halo_scaled), "② NFW-ρ² haloテンプレート×f_halo\n(残差がこの形なら本物のhalo)",
    "inferno")
data_disp = counts.copy().astype(float); data_disp[~roi] = np.nan
sky(axs[2], data_disp, "③ 観測データ(点源マスク済)", "viridis")
fig1.suptitle(f"Totani Fig.11 再現 (本研究 v6, Bin6=20.76 GeV): 20 GeV超過の空間分布", fontsize=13)
fig1.tight_layout(rect=(0, 0, 1, 0.95))
out1 = BASE / f"results/{RUN}/repro_fig11_residual_map.png"
fig1.savefig(out1, dpi=120); plt.close()
print(f"完成: {out1}")

# ===== Fig.14 相当(テンプレート形) =====
fig2, axs = plt.subplots(2, 2, figsize=(13, 10))
sky(axs[0, 0], t["gas"], "gas (GALPROP π⁰+bremss)", "inferno")
sky(axs[0, 1], t["loopI_a"], "Loop I shell A", "inferno")
sky(axs[1, 0], t["loopI_b"], "Loop I shell B", "inferno")
sky(axs[1, 1], t["ics"], "ICS (GALPROP)", "inferno")
fig2.suptitle("Totani Fig.14 再現 (本研究 v6, Bin6): 各テンプレートの天球形状", fontsize=13)
fig2.tight_layout(rect=(0, 0, 1, 0.96))
out2 = BASE / f"results/{RUN}/repro_fig14_templates.png"
fig2.savefig(out2, dpi=120); plt.close()
print(f"完成: {out2}")

# 残差とhaloテンプレートの空間相関(本物のhaloなら高い相関)
rf = residual[roi]; hf = halo_scaled[roi]
corr = float(np.corrcoef(rf, hf)[0, 1])
print(f"\n残差 vs haloテンプレート 空間相関係数 = {corr:.3f}")
print(f"  (1に近い=残差が球対称haloの形。低い/負=別の構造)")
print(f"残差のROI内合計 = {residual[roi].sum():.1f} counts, halo成分合計 = {halo_scaled[roi].sum():.1f} counts")
