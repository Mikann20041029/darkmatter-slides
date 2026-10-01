"""[2026-07-18] 検証②: 尤度粒度(1°ピクセル vs Totani §2.2 の10°セル)が
有意度・成分割り振りに効くかを全13ビンで比較。point推定のみ(MCMCなし=OOM安全)。

v8はピクセル尤度(likelihood_cell_mode=False)。Totaniは10°セル。セル化すると
ピクセルスケールのモデル-データ不一致が尤度から除かれ、有意度・成分の割り振りが
Totaniに寄るはず、という仮説を検証する。

出力: results/mcmc_allbins_gasICS_v8_diskbubble/diag_cellmode_v8.{json,png}
"""
from __future__ import annotations
import os
os.environ.setdefault("MCMC_DISK_BUBBLE", "1")
os.environ.setdefault("MCMC_ICS_SPLIT", "0")
os.environ.setdefault("MCMC_CELL_LIKELIHOOD", "0")  # 手動で両方試すのでモジュール既定はOFF
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
TOT_DLNL = [101, 0, 22, 79, 93, 101, 51, 22, 7, 5, 1, 0, 0]
TOT_SIG = [float(np.sqrt(2 * d)) for d in TOT_DLNL]
# Totani Fig.6 ROI平均 E²dN/dE(overlay と同一, 20GeV=index5)
TOT_F6 = {"iso": 1.0e-4, "halo": 1.8e-4, "gas": 5.0e-4, "ics": 1.3e-4}

print("露出/イベント/J-map/バブル(disk込み)構築中...")
expmaps, _ = m.load_exposure_maps()
df_all = m.load_all_events()
j_map = m.nfw_j_map()
nfw_norm, _ = m.calibrate_nfw_norm(expmaps[5], j_map)
df_bubble = m.load_events_with_disk()
bpos, bneg = m.build_bubble_counts_template(df_bubble)
s1, s2 = _sub.loop_i_shell_templates()

PARAM_OF = {"gas": "f_gas", "ics": "f_ics", "iso_counts": "f_iso"}


def x0_for(t, counts, valid):
    c_mean = max(counts[valid].mean(), 1e-6)
    def _x(name):
        if name in ("f_fb", "f_halo"): return 0.5
        key = m.PARAM_TO_TEMPLATE_KEY[name]; tmean = float(t[key][valid].mean())
        if name == "f_fb_neg": return 0.3 * c_mean / tmean if tmean > 0 else 0.3
        coef = 0.5 if (name == "f_gas" or name.startswith("f_ics")) else 0.3
        return coef * c_mean / tmean if tmean > 0 else 0.3
    return [_x(n) for n in m.PARAM_NAMES]


def fit_full(counts_ll, t_ll, x0):
    """point推定で全パラメータとΔlnLを返す(counts_ll/t_llはピクセルorセル)。"""
    _nnh = m.NDIM - 1
    def f_nh(p):
        v, g = m.neg_log_likelihood_and_grad(list(p) + [0.0], counts_ll, t_ll); return v, g[:_nnh]
    rnh, _ = m._multistart_minimize(f_nh, x0[:_nnh], m._bounds_no_halo())
    def f(p): return m.neg_log_likelihood_and_grad(p, counts_ll, t_ll)
    r, _ = m._multistart_minimize(f, list(rnh.x) + [x0[_nnh]], m._bounds_with_halo())
    best = r.x if (-r.fun) >= (-rnh.fun) else np.array(list(rnh.x) + [0.0])
    dl = max((-r.fun) - (-rnh.fun), 0.0)
    return {n: float(v) for n, v in zip(m.PARAM_NAMES, best)}, float(np.sqrt(2 * dl)), dl


def comp_e2dnde(ib, t_pixel, params, valid_px):
    """成分ROI平均E²dN/dE(ピクセルテンプレ×fit振幅)。"""
    de_mev = (m.BIN_EDGES[ib + 1] - m.BIN_EDGES[ib]) * 1000.0
    denom = np.sum(expmaps[ib][valid_px] * m.PIX_SOLID_ANGLE_SR[valid_px] * de_mev)
    e2 = m.BIN_CENTERS[ib] ** 2 * 1e6
    out = {}
    for name, tk in [("iso", "iso_counts"), ("gas", "gas"), ("ics", "ics"), ("halo", "halo")]:
        f = params[PARAM_OF.get(tk, "f_" + name)] if name != "halo" else params["f_halo"]
        out[name] = e2 * np.sum(f * t_pixel[tk][valid_px]) / denom
    return out


rows = []
for ib in range(13):
    lo, hi = m.BIN_EDGES[ib], m.BIN_EDGES[ib + 1]
    sel = df_all[(df_all.energy_GeV >= lo) & (df_all.energy_GeV < hi)]
    counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
    gas_i, ics_i = _sub._load_galprop_gas_ics_templates(lo, hi)
    t = m.build_templates_for_bin(ib, counts, expmaps[ib], gas_i, ics_i,
        bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
        expmap_bubble_bin=expmaps[m.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
        loop_shell1=s1, loop_shell2=s2)
    masked, _ = _sub.mask_point_sources(counts.copy())
    valid = (~np.isnan(masked)) & (np.abs(BG) >= 10) & (np.abs(BG) <= 60)
    t["valid"] = valid; t["valid_pixel"] = valid
    x0 = x0_for(t, counts, valid)

    # ピクセル尤度
    p_px, sig_px, dl_px = fit_full(counts, t, x0)
    # セル尤度
    cc, ct = m.cellize_counts_and_templates(counts, t, valid)
    p_cl, sig_cl, dl_cl = fit_full(cc, ct, x0)

    c_px = comp_e2dnde(ib, t, p_px, valid)
    c_cl = comp_e2dnde(ib, t, p_cl, valid)
    rows.append(dict(bin=ib + 1, e=m.BIN_CENTERS[ib], sig_pixel=sig_px, sig_cell=sig_cl,
                     totani_sig=TOT_SIG[ib], f_halo_px=p_px["f_halo"], f_halo_cl=p_cl["f_halo"],
                     comp_pixel=c_px, comp_cell=c_cl))
    print(f"Bin{ib+1:2d} {m.BIN_CENTERS[ib]:6.1f}GeV: ピクセル={sig_px:5.1f}σ セル={sig_cl:5.1f}σ "
          f"Totani={TOT_SIG[ib]:5.1f}σ | f_halo px={p_px['f_halo']:+.3f} cell={p_cl['f_halo']:+.3f}")

# 20GeV(Bin6)の成分比まとめ
b6 = rows[5]
print("\n=== Bin6(20GeV) 成分 本研究/Totani 比 ===")
for name in ["gas", "ics", "iso", "halo"]:
    rp = b6["comp_pixel"][name] / TOT_F6[name]; rc = b6["comp_cell"][name] / TOT_F6[name]
    print(f"  {name:5s}: ピクセル={rp:.2f}  セル={rc:.2f}  (1.0=Totani一致)")

# 図
E = [r["e"] for r in rows]
fig, ax = plt.subplots(figsize=(11, 6))
ax.plot(E, [r["sig_pixel"] for r in rows], "o-", color="#d62728", lw=2.2, ms=6, label="ピクセル尤度(v8現状)")
ax.plot(E, [r["sig_cell"] for r in rows], "s-", color="#2ca02c", lw=2.2, ms=6, label="10°セル尤度(Totani §2.2)")
ax.plot(E, [r["totani_sig"] for r in rows], "^--", color="navy", lw=1.8, ms=7, mfc="none", label="Totani Fig.9")
ax.axhspan(13, 19, color="navy", alpha=0.10, label="Totani報告帯")
ax.axvline(20.76, color="gold", ls="--", alpha=0.5)
ax.set_xscale("log"); ax.set_xlabel("Energy [GeV]"); ax.set_ylabel("halo有意度 [σ]")
ax.set_title("検証②: 尤度粒度(1°ピクセル vs 10°セル)で有意度スペクトルは変わるか")
ax.legend(fontsize=9); ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(OUT / "diag_cellmode_v8.png", dpi=130); plt.close()

try:
    gh = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
except Exception:
    gh = "unknown"
json.dump(dict(generated="2026-07-18", git_hash=gh, totani_fig9_dlnL=TOT_DLNL,
               totani_fig6_20gev=TOT_F6, rows=rows),
          open(OUT / "diag_cellmode_v8.json", "w"), ensure_ascii=False, indent=2)
print("\n完成: diag_cellmode_v8.{json,png}")
