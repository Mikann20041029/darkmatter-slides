"""[2026-07-17] 天の川halo解析の各モデル成分スペクトル(Totani 2025 Fig.2/4/6 相当)。
v2_cosb(cos(b)補正版)のフィット結果から、各成分(gas, ICS, iso, Loop I, バブル正負, halo)の
ROI平均フラックス E²dN/dE を全13ビンで再構成してプロットする。

目的: ICSスペクトルが「不自然なV字/急落」を示すか(Totani §4.1が警告するICS-halo縮退の兆候)、
各成分がTotaniのFig.6とどう違うかを可視化し、有意度過大の原因を診断する。
"""
from pathlib import Path
import json
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
plt.rcParams["font.family"] = "Noto Sans CJK JP"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mcmc_fit_all_bins as m
import plot_skymap_all_subtracted as _sub

BASE = Path(__file__).resolve().parent.parent
RES = json.load(open(BASE / "results/mcmc_allbins_gasICS_v8_diskbubble/halo_spectrum.json"))

expmaps, _ = m.load_exposure_maps()
df = m.load_all_events()
j_map = m.nfw_j_map()
bpos, bneg = m.build_bubble_counts_template(df)
nfw_norm, _ = m.calibrate_nfw_norm(expmaps[5], j_map)
s1, s2 = _sub.loop_i_shell_templates()
valid = (np.abs(m.BG) >= 10) & (np.abs(m.BG) <= 60)

COMPS = ["gas", "ics", "iso_counts", "loopI_a", "loopI_b", "fb", "fb_neg", "halo"]
PARAM_OF = {"gas": "f_gas", "ics": "f_ics", "loopI_a": "f_loopI_a", "loopI_b": "f_loopI_b",
            "fb": "f_fb", "fb_neg": "f_fb_neg", "halo": "f_halo", "iso_counts": "f_iso"}

spec = {c: [] for c in COMPS}
energies = []
for ib in range(m.N_BINS):
    lo, hi = m.BIN_EDGES[ib], m.BIN_EDGES[ib + 1]
    de_mev = (hi - lo) * 1000.0
    sel = df[(df.energy_GeV >= lo) & (df.energy_GeV < hi)]
    counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
    gas_i, ics_i = _sub._load_galprop_gas_ics_templates(lo, hi)
    t = m.build_templates_for_bin(ib, counts, expmaps[ib], gas_i, ics_i,
        bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
        expmap_bubble_bin=expmaps[m.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
        loop_shell1=s1, loop_shell2=s2)
    params = RES["bins"][ib]["params"]
    # ROI平均フラックス = Σ(f_k · template_counts_k[valid]) / Σ(exposure·dΩ·dE)[valid]
    denom = np.sum(expmaps[ib][valid] * m.PIX_SOLID_ANGLE_SR[valid] * de_mev)
    e2 = m.BIN_CENTERS[ib] ** 2 * 1e6  # GeV² → MeV² (E²dN/dE を MeV cm⁻²s⁻¹sr⁻¹ で出す)
    for c in COMPS:
        pk = PARAM_OF[c]
        f = 1.0 if pk is None else params[pk]["median"]
        comp_counts = np.sum(f * t[c][valid])
        flux_mean = comp_counts / denom            # ph cm⁻²s⁻¹sr⁻¹MeV⁻¹
        spec[c].append(e2 * flux_mean)             # E²dN/dE [MeV cm⁻²s⁻¹sr⁻¹]
    energies.append(m.BIN_CENTERS[ib])
    print(f"Bin{ib+1} ({m.BIN_CENTERS[ib]:.1f}GeV) 完了", flush=True)

# プロット(Totani Fig.6風、E²dN/dE vs E、両対数だが符号のため線形も併記)
LABELS = {"gas": "GALPROP gas", "ics": "GALPROP ICS", "iso_counts": "等方背景",
          "loopI_a": "Loop I (shell A)", "loopI_b": "Loop I (shell B)",
          "fb": "フェルミバブル(正)", "fb_neg": "フェルミバブル(負)×(-1)", "halo": "NFW halo (ρ²)"}
COLORS = {"gas": "#1f77b4", "ics": "#ff7f0e", "iso_counts": "#7f7f7f",
          "loopI_a": "#2ca02c", "loopI_b": "#98df8a", "fb": "#d62728",
          "fb_neg": "#9467bd", "halo": "#000000"}

fig, ax = plt.subplots(figsize=(10, 7))
for c in COMPS:
    y = np.array(spec[c])
    if c == "fb_neg":
        y = -y  # 負のバブル成分を -1 倍して正に反転(log軸で表示するため)
    lw = 3 if c in ("halo", "ics") else 1.6
    ax.plot(energies, y, "o-", color=COLORS[c], lw=lw, ms=5,
            label=LABELS[c], alpha=0.9 if c in ("halo", "ics") else 0.7)
ax.axvline(20.76, color="gold", ls="--", alpha=0.5, label="20 GeV")
ax.set_xscale("log")
ax.set_yscale("log")  # 縦軸を対数に(全成分を正にしたので log 表示可能)
ax.set_xlabel("Energy [GeV]")
ax.set_ylabel(r"$E^2 dN/dE$ [MeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]")
ax.set_title("天の川halo解析: 各モデル成分のスペクトル(cos(b)補正版, Totani Fig.6相当)\n"
             "ICS(橙)とhalo(黒)の形を要確認: ICSがV字/急落ならTotani§4.1のICS-halo縮退の兆候")
ax.legend(fontsize=9, ncol=2)
fig.tight_layout()
out = BASE / "results/mcmc_allbins_gasICS_v8_diskbubble/component_spectra.png"
fig.savefig(out, dpi=130)
plt.close()
print(f"\n完成: {out}")

# 数値も保存
json.dump({"energies_gev": energies, "e2dnde": {c: spec[c] for c in COMPS}},
          open(BASE / "results/mcmc_allbins_gasICS_v8_diskbubble/component_spectra.json", "w"), indent=2)
