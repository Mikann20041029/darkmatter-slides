"""[2026-07-19] bin6 を同一UltraCleanデータで 1° と 0.125° でフィットし、
成分崩壊が解像度で起きるかを切り分ける。PIXEL_DEG を引数で受ける。
"""
from __future__ import annotations
import os, sys
PIXEL = sys.argv[1] if len(sys.argv) > 1 else "1.0"
os.environ["MCMC_ULTRACLEAN"] = "1"
os.environ["MCMC_PIXEL_DEG"] = PIXEL
os.environ["MCMC_DISK_BUBBLE"] = "1"
os.environ["MCMC_CELL_LIKELIHOOD"] = "1"
os.environ["MCMC_SIGNFREE_HALO"] = "1"
os.environ["MCMC_ICS_SPLIT"] = "0"

import json
import numpy as np
sys.path.insert(0, "code")
import mcmc_fit_all_bins as m
import plot_skymap_all_subtracted as _sub

IB = 5
print(f"=== PIXEL_DEG={PIXEL}, grid={len(m.L_C)}x{len(m.B_C)}, CELL_MODE={m.CELL_MODE} ===")
expmaps, _ = m.load_exposure_maps()
df_all = m.load_all_events()
j_map = m.nfw_j_map()
nfw_norm, _ = m.calibrate_nfw_norm(expmaps[5], j_map)
df_bubble = m.load_events_with_disk()
bpos, bneg = m.build_bubble_counts_template(df_bubble)
s1, s2 = _sub.loop_i_shell_templates()
valid = (np.abs(m.BG) >= 10) & (np.abs(m.BG) <= 60)

lo, hi = m.BIN_EDGES[IB], m.BIN_EDGES[IB + 1]
sel = df_all[(df_all.energy_GeV >= lo) & (df_all.energy_GeV < hi)]
counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
gas_i, ics_i = _sub._load_galprop_gas_ics_templates(lo, hi)
t_pix = m.build_templates_for_bin(IB, counts, expmaps[IB], gas_i, ics_i,
    bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
    expmap_bubble_bin=expmaps[m.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
    loop_shell1=s1, loop_shell2=s2)
counts_fit, t = m.cellize_counts_and_templates(counts, t_pix, valid) if m.CELL_MODE else (counts, t_pix)

_nnh = m.NDIM - 1
x0 = np.array([1.0, 1.0, 1.0, 1.0, 0.01, 0.5, -0.2, 1.0])
def nll_nh(p):
    v, g = m.neg_log_likelihood_and_grad(list(p) + [0.0], counts_fit, t); return v, g[:_nnh]
def nll_h(p): return m.neg_log_likelihood_and_grad(p, counts_fit, t)
res_nh, _ = m._multistart_minimize(nll_nh, x0[:_nnh], m._bounds_no_halo())
res_h, _ = m._multistart_minimize(nll_h, list(res_nh.x) + [x0[-1]], m._bounds_with_halo())
dlnL = -res_h.fun - (-res_nh.fun)
sig = np.sqrt(max(2 * dlnL, 0.0))
pd = dict(zip(m.PARAM_NAMES, res_h.x))

# 各成分の ROI平均 E2dNdE 比(vs Totani 20GeV 目視値)
TOT = {"gas": 5.0e-4, "ics": 1.3e-4, "iso": 1.0e-4, "loopI": 1.4e-4, "halo": 1.8e-4}
de_mev = (hi - lo) * 1000.0
denom = np.sum(expmaps[IB][valid] * m.PIX_SOLID_ANGLE_SR[valid] * de_mev)
e2 = m.BIN_CENTERS[IB] ** 2 * 1e6
def e2dnde(key, f):
    return e2 * np.sum(f * t_pix[key][valid]) / denom
comp = {
    "gas": e2dnde("gas", pd["f_gas"]),
    "ics": e2dnde("ics", pd["f_ics"]),
    "iso": e2dnde("iso_counts", pd["f_iso"]),
    "loopI": e2dnde("loopI_a", pd["f_loopI_a"]) + e2dnde("loopI_b", pd["f_loopI_b"]),
    "halo": e2dnde("halo", pd["f_halo"]),
}
print(f"\nσ(halo)={sig:.2f}  ΔlnL={dlnL:.1f}")
print("成分   f値      E2dNdE      Totani比")
for c in ["gas", "ics", "iso", "loopI", "halo"]:
    fk = {"gas":"f_gas","ics":"f_ics","iso":"f_iso","loopI":"f_loopI_a","halo":"f_halo"}[c]
    print(f"  {c:6s} {pd[fk]:8.4f} {comp[c]:.3e}  {comp[c]/TOT[c]:6.2f}")
json.dump({"pixel_deg": PIXEL, "sigma": float(sig), "params": {k: float(v) for k, v in pd.items()},
           "e2dnde": {k: float(v) for k, v in comp.items()},
           "ratio": {k: float(comp[k]/TOT[k]) for k in comp}},
          open(f"results/mcmc_allbins_gasICS_v12_bubblefix/diag_res_{PIXEL}.json", "w"), indent=2)
