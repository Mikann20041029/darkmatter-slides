"""[2026-07-18] component_overlay_totani を (1)v8正式版 と (2)中心30%増光版 の2つ作る。
従来 plot_mw_component_spectra.py はバブルを disk抜きで再構築し図ラベルも"v6"のままで
厳密なv8ではなかった。本スクリプトは disk込みバブル(v8構成)で成分スペクトルを
point推定(MCMCなし=OOM安全)で再計算し、Totani Fig.6 に重ねる。

出力(results/mcmc_allbins_gasICS_v8_diskbubble/):
  component_spectra_v8.json / component_overlay_totani_v8.png              (a=0)
  component_spectra_centerboost30.json / component_overlay_totani_centerboost30.png (a=0.3)

a=0 の point推定成分は v8 MCMC中央値とほぼ一致する(f_halo等で確認済み)。
30%増光版は gas+ICS を中心経度窓 ×(1+0.3·exp(-(l/15°)²)) で明るくした再フィット。
"""
from __future__ import annotations
import os
os.environ.setdefault("MCMC_DISK_BUBBLE", "1")
os.environ.setdefault("MCMC_ICS_SPLIT", "0")
os.environ.setdefault("MCMC_CELL_LIKELIHOOD", "0")
os.environ.setdefault("MCMC_SIGNFREE_HALO", "1")

import sys, json
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
plt.rcParams["font.family"] = "Noto Sans CJK JP"

sys.path.insert(0, "code")
import mcmc_fit_all_bins as m
import plot_skymap_all_subtracted as _sub

OUT = Path("results/mcmc_allbins_gasICS_v8_diskbubble")
BG, LG = m.BG, m.LG
WIN = np.exp(-(LG / 15.0) ** 2)

# Totani Fig.6 目視読み取り(|l|<=60°,10°<=|b|<=60° ROI平均、±30%)。plot_component_overlay_totani.py と同一
TOTANI = {
    "gas":   [2.1e-3, 1.6e-3, 1.2e-3, 9.5e-4, 6.5e-4, 5.0e-4, 3.8e-4, 2.8e-4, 1.9e-4, 1.0e-4, 9e-5, 9e-5, 6e-5],
    "ics":   [9.0e-4, 7.0e-4, 5.5e-4, 3.5e-4, 2.0e-4, 1.3e-4, 1.0e-4, 2.5e-5, 3.5e-5, 3.0e-5, 1.5e-5, 5e-6, 6e-5],
    "iso":   [3.0e-4, 2.3e-4, 1.9e-4, 1.6e-4, 1.3e-4, 1.0e-4, 8.0e-5, 8.0e-5, 3.0e-5, np.nan, np.nan, np.nan, np.nan],
    "loopI": [4.5e-4, 4.0e-4, 3.5e-4, 3.3e-4, 2.0e-4, 1.4e-4, 1.3e-4, 2.0e-5, np.nan, np.nan, np.nan, np.nan, np.nan],
    "halo":  [np.nan, 5.0e-6, 6.0e-5, 1.3e-4, 1.7e-4, 1.8e-4, 1.5e-4, 1.05e-4, 7.0e-5, 6.0e-5, 3.0e-5, 1.8e-5, 3.0e-5],
}
COLORS = {"gas": "#1f77b4", "ics": "#ff7f0e", "iso": "#7f7f7f", "loopI": "#9467bd", "halo": "#d62728"}
LABELS = {"gas": "gas", "ics": "ICS", "iso": "等方(iso)", "loopI": "Loop I", "halo": "halo (NFW-ρ²)"}

print("露出/イベント/J-map/バブル(disk込み)構築中...")
expmaps, _ = m.load_exposure_maps()
df_all = m.load_all_events()
j_map = m.nfw_j_map()
nfw_norm, _ = m.calibrate_nfw_norm(expmaps[5], j_map)
df_bubble = m.load_events_with_disk()
bpos, bneg = m.build_bubble_counts_template(df_bubble)
s1, s2 = _sub.loop_i_shell_templates()

COMPS = ["gas", "ics", "iso_counts", "loopI_a", "loopI_b", "fb", "fb_neg", "halo"]
PARAM_OF = {"gas": "f_gas", "ics": "f_ics", "iso_counts": "f_iso",
            "loopI_a": "f_loopI_a", "loopI_b": "f_loopI_b",
            "fb": "f_fb", "fb_neg": "f_fb_neg", "halo": "f_halo"}


def x0_for(t, counts, valid):
    c_mean = max(counts[valid].mean(), 1e-6)
    def _x(name):
        if name in ("f_fb", "f_halo"): return 0.5
        key = m.PARAM_TO_TEMPLATE_KEY[name]; tmean = float(t[key][valid].mean())
        if name == "f_fb_neg": return 0.3 * c_mean / tmean if tmean > 0 else 0.3
        coef = 0.5 if (name == "f_gas" or name.startswith("f_ics")) else 0.3
        return coef * c_mean / tmean if tmean > 0 else 0.3
    return [_x(n) for n in m.PARAM_NAMES]


def fit_point(counts, t, x0):
    """with-halo 点推定の全パラメータ辞書を返す(MCMCなし)。"""
    _nnh = m.NDIM - 1
    def f_nh(p):
        v, g = m.neg_log_likelihood_and_grad(list(p) + [0.0], counts, t); return v, g[:_nnh]
    rnh, _ = m._multistart_minimize(f_nh, x0[:_nnh], m._bounds_no_halo())
    def f(p): return m.neg_log_likelihood_and_grad(p, counts, t)
    r, _ = m._multistart_minimize(f, list(rnh.x) + [x0[_nnh]], m._bounds_with_halo())
    best = r.x if (-r.fun) >= (-rnh.fun) else np.array(list(rnh.x) + [0.0])
    return {n: float(v) for n, v in zip(m.PARAM_NAMES, best)}


def component_spectra(a: float):
    """中心ブースト a で全13ビンをpoint推定フィットし、各成分のROI平均E²dN/dEを返す。"""
    boost = 1.0 + a * WIN
    valid_roi = (np.abs(BG) >= 10) & (np.abs(BG) <= 60)
    spec = {c: [] for c in COMPS}
    energies = []
    for ib in range(m.N_BINS):
        lo, hi = m.BIN_EDGES[ib], m.BIN_EDGES[ib + 1]
        de_mev = (hi - lo) * 1000.0
        sel = df_all[(df_all.energy_GeV >= lo) & (df_all.energy_GeV < hi)]
        counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
        gas_i, ics_i = _sub._load_galprop_gas_ics_templates(lo, hi)
        t = m.build_templates_for_bin(ib, counts, expmaps[ib], gas_i * boost, ics_i * boost,
            bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
            expmap_bubble_bin=expmaps[m.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
            loop_shell1=s1, loop_shell2=s2)
        masked, _ = _sub.mask_point_sources(counts.copy())
        valid = valid_roi & (~np.isnan(masked))
        t["valid"] = valid; t["valid_pixel"] = valid
        params = fit_point(counts, t, x0_for(t, counts, valid))
        denom = np.sum(expmaps[ib][valid] * m.PIX_SOLID_ANGLE_SR[valid] * de_mev)
        e2 = m.BIN_CENTERS[ib] ** 2 * 1e6
        for c in COMPS:
            f = params[PARAM_OF[c]]
            comp_counts = np.sum(f * t[c][valid])
            spec[c].append(e2 * comp_counts / denom)
        energies.append(m.BIN_CENTERS[ib])
        print(f"  a={a} Bin{ib+1} 完了", flush=True)
    return energies, spec, params


def overlay_figure(energies, spec, tag, title):
    E = np.array(energies)
    ours = {"gas": np.array(spec["gas"]), "ics": np.array(spec["ics"]),
            "iso": np.array(spec["iso_counts"]),
            "loopI": np.array(spec["loopI_a"]) + np.array(spec["loopI_b"]),
            "halo": np.array(spec["halo"])}
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(15, 6.5))
    for c in ["gas", "ics", "iso", "loopI", "halo"]:
        axL.plot(E, ours[c], "-", color=COLORS[c], lw=2.2, label=f"{LABELS[c]}(本研究)")
        axL.plot(E, TOTANI[c], "o", color=COLORS[c], mfc="none", ms=8, mew=1.8,
                 ls=":", lw=1.0, label=f"{LABELS[c]}(Totani)")
    axL.axvline(20.76, color="gold", ls="--", alpha=0.5)
    axL.set_xscale("log"); axL.set_yscale("log"); axL.set_ylim(3e-6, 3e-3)
    axL.set_xlabel("Energy [GeV]"); axL.set_ylabel(r"$E^2 dN/dE$ [MeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]")
    axL.set_title("全成分: 本研究(実線) vs Totani Fig.6(○, 目視±30%)")
    axL.legend(fontsize=7.5, ncol=2, loc="lower left")
    for c in ["gas", "ics", "iso", "loopI", "halo"]:
        axR.plot(E, ours[c] / np.array(TOTANI[c]), "o-", color=COLORS[c], lw=2, ms=6, label=LABELS[c])
    axR.axhline(1.0, color="k", lw=1.0); axR.axhspan(0.7, 1.4, color="green", alpha=0.10)
    axR.axvline(20.76, color="gold", ls="--", alpha=0.5)
    axR.set_xscale("log"); axR.set_yscale("log"); axR.set_ylim(0.1, 10)
    axR.set_xlabel("Energy [GeV]"); axR.set_ylabel("本研究 / Totani")
    axR.set_title("成分ごとの比(1.0=一致, 緑帯=±40%)")
    axR.legend(fontsize=9, ncol=2)
    fig.suptitle(title, fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    out = OUT / f"component_overlay_totani_{tag}.png"
    fig.savefig(out, dpi=130); plt.close()
    json.dump({"energies_gev": energies, "e2dnde": {c: spec[c] for c in COMPS}},
              open(OUT / f"component_spectra_{tag}.json", "w"), indent=2)
    print(f"完成: {out}")
    return {c: float(np.nanmedian(ours[c] / np.array(TOTANI[c]))) for c in ["gas", "ics", "iso", "loopI", "halo"]}


print("\n=== (1) v8正式版 (a=0, disk込みバブル) ===")
E0, s0, _ = component_spectra(0.0)
r0 = overlay_figure(E0, s0, "v8",
    "成分スペクトル比較【v8正式版】(disk込みバブル, GALPROP baseline)")
print("  本研究/Totani 中央値:", {k: round(v, 2) for k, v in r0.items()})

print("\n=== (2) 中心30%増光版 (a=0.3) ===")
E3, s3, _ = component_spectra(0.3)
r3 = overlay_figure(E3, s3, "centerboost30",
    "成分スペクトル比較【中心30%増光版】(GALPROP gas+ICS の中心を+30%)")
print("  本研究/Totani 中央値:", {k: round(v, 2) for k, v in r3.items()})
print("\n完成: component_overlay_totani_{v8,centerboost30}.png と対応json")
