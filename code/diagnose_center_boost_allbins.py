"""[2026-07-18] 中心ブースト実験の全13ビン版 + gas単独/ICS単独の切り分け。
diagnose_center_boost_scan.py の判定(a*=0.3で20GeVがTotani帯入り)を受けて、
(1) a=0(現状)と a=0.3(中心30%増光)の全13ビン有意度を並べる、
(2) Bin6で「gas単独ブースト / ICS単独ブースト / 両方」を比較しどちらが効くか切り分ける。
point推定ΔlnLのみ(MCMCなし=OOM安全)。a=0はv8 MCMC値と一致確認済み。

出力: results/mcmc_allbins_gasICS_v8_diskbubble/diag_center_boost_allbins.{json,png}
"""
from __future__ import annotations
import os
os.environ.setdefault("MCMC_DISK_BUBBLE", "1")
os.environ.setdefault("MCMC_ICS_SPLIT", "0")
os.environ.setdefault("MCMC_CELL_LIKELIHOOD", "0")
os.environ.setdefault("MCMC_SIGNFREE_HALO", "1")

import sys, json, subprocess
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
WIN = np.exp(-(LG / 15.0) ** 2)      # 中心経度窓
A = 0.30
# Totani Fig.9 ΔlnL(目視)→ σ=sqrt(2ΔlnL)
TOT_DLNL = [101, 0, 22, 79, 93, 101, 51, 22, 7, 5, 1, 0, 0]
TOT_SIG = [float(np.sqrt(2 * d)) for d in TOT_DLNL]

print("露出/イベント/J-map/バブル(disk込み)構築中...")
expmaps, _ = m.load_exposure_maps()
df_all = m.load_all_events()
j_map = m.nfw_j_map()
nfw_norm, _ = m.calibrate_nfw_norm(expmaps[5], j_map)
df_bubble = m.load_events_with_disk()
bpos, bneg = m.build_bubble_counts_template(df_bubble)
s1, s2 = _sub.loop_i_shell_templates()


def point_sig(counts, t, x0):
    _nnh = m.NDIM - 1
    def f_nh(p):
        v, g = m.neg_log_likelihood_and_grad(list(p) + [0.0], counts, t); return v, g[:_nnh]
    rnh, _ = m._multistart_minimize(f_nh, x0[:_nnh], m._bounds_no_halo())
    def f(p): return m.neg_log_likelihood_and_grad(p, counts, t)
    r, _ = m._multistart_minimize(f, list(rnh.x) + [x0[_nnh]], m._bounds_with_halo())
    dl = max((-r.fun) - (-rnh.fun), 0.0)
    return float(np.sqrt(2 * dl)), float(r.x[-1])


def build(ib, counts, gas_i, ics_i, valid):
    t = m.build_templates_for_bin(ib, counts, expmaps[ib], gas_i, ics_i,
        bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
        expmap_bubble_bin=expmaps[m.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
        loop_shell1=s1, loop_shell2=s2)
    t["valid"] = valid; t["valid_pixel"] = valid
    return t


def x0_for(t, counts, valid):
    c_mean = max(counts[valid].mean(), 1e-6)
    def _x(name):
        if name in ("f_fb", "f_halo"): return 0.5
        key = m.PARAM_TO_TEMPLATE_KEY[name]; tmean = float(t[key][valid].mean())
        if name == "f_fb_neg": return 0.3 * c_mean / tmean if tmean > 0 else 0.3
        coef = 0.5 if (name == "f_gas" or name.startswith("f_ics")) else 0.3
        return coef * c_mean / tmean if tmean > 0 else 0.3
    return [_x(n) for n in m.PARAM_NAMES]


def prep(ib):
    emin, emax = m.BIN_EDGES[ib], m.BIN_EDGES[ib + 1]
    sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
    counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
    gas_i, ics_i = _sub._load_galprop_gas_ics_templates(emin, emax)
    masked, _ = _sub.mask_point_sources(counts.copy())
    valid = (~np.isnan(masked)) & (np.abs(BG) >= 10) & (np.abs(BG) <= 60)
    return counts, gas_i, ics_i, valid


# (1) 全13ビン: a=0 と a=0.3(gas+ICS両方ブースト)
print("\n=== 全13ビン 中心30%増光の効果 ===")
print("bin  E[GeV]   a=0     a=30%   Totani(σ)")
allbins = []
boost = 1.0 + A * WIN
for ib in range(13):
    counts, gas_i, ics_i, valid = prep(ib)
    t0 = build(ib, counts, gas_i, ics_i, valid)
    s0, h0 = point_sig(counts, t0, x0_for(t0, counts, valid))
    t3 = build(ib, counts, gas_i * boost, ics_i * boost, valid)
    s3, h3 = point_sig(counts, t3, x0_for(t3, counts, valid))
    allbins.append(dict(bin=ib + 1, e=m.BIN_CENTERS[ib], sig_a0=s0, sig_a30=s3,
                        f_halo_a0=h0, f_halo_a30=h3, totani_sig=TOT_SIG[ib]))
    print(f"{ib+1:2d}  {m.BIN_CENTERS[ib]:7.2f}  {s0:5.1f}σ  {s3:5.1f}σ  {TOT_SIG[ib]:5.1f}σ")

# (2) Bin6: gas単独 vs ICS単独 vs 両方(a=0.3)
print("\n=== Bin6 どの成分が中心で弱いか(a=0.3) ===")
ib = 5
counts, gas_i, ics_i, valid = prep(ib)
variants = {
    "現状(a=0)":       (gas_i, ics_i),
    "gas単独+30%":     (gas_i * boost, ics_i),
    "ICS単独+30%":     (gas_i, ics_i * boost),
    "gas+ICS両方+30%": (gas_i * boost, ics_i * boost),
}
bin6_split = {}
for name, (g, ic) in variants.items():
    t = build(ib, counts, g, ic, valid)
    s, h = point_sig(counts, t, x0_for(t, counts, valid))
    bin6_split[name] = dict(sig=s, f_halo=h)
    print(f"  {name:16s}: sig={s:5.1f}σ  f_halo={h:+.3f}")

# --- 図 ---
E = [r["e"] for r in allbins]
fig, ax = plt.subplots(figsize=(11, 6))
ax.plot(E, [r["sig_a0"] for r in allbins], "o-", color="#d62728", lw=2.2, ms=6, label="本研究 a=0(現状)")
ax.plot(E, [r["sig_a30"] for r in allbins], "s-", color="#2ca02c", lw=2.2, ms=6, label="本研究 a=30%(中心増光)")
ax.plot(E, [r["totani_sig"] for r in allbins], "^--", color="navy", lw=1.8, ms=7, mfc="none", label="Totani Fig.9 (σ=√2ΔlnL)")
ax.axhspan(13, 19, color="navy", alpha=0.10, label="Totani報告帯 13-19σ")
ax.axvline(20.76, color="gold", ls="--", alpha=0.5)
ax.set_xscale("log"); ax.set_xlabel("Energy [GeV]"); ax.set_ylabel("halo有意度 [σ]")
ax.set_title("全13ビン: 中心30%増光で有意度スペクトルはTotaniに寄るか")
ax.legend(fontsize=9); ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(OUT / "diag_center_boost_allbins.png", dpi=130)
plt.close()

try:
    gh = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
except Exception:
    gh = "unknown"
json.dump(dict(generated="2026-07-18", git_hash=gh, boost_a=A,
               boost_window="1+a*exp(-(l/15deg)^2)", allbins=allbins,
               bin6_component_split=bin6_split, totani_fig9_dlnL=TOT_DLNL),
          open(OUT / "diag_center_boost_allbins.json", "w"), ensure_ascii=False, indent=2)
print("\n完成: diag_center_boost_allbins.{json,png}")
