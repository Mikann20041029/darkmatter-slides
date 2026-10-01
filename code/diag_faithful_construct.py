"""[2026-07-19] バブル構築フィットを Totani §3.1 忠実版(全成分同時)にすると
A_ics が回復するかを検証。現行(gas+ICS+GCE+flat+offset)vs 忠実(+iso+Loop I)を比較。
構築ビン=1.5(bin1)と4.3(bin3)GeV、whole ROI(disk込み)、セル束ね(10°)で比較。
"""
from __future__ import annotations
import os, sys
os.environ["MCMC_ULTRACLEAN"] = "1"
os.environ["MCMC_PIXEL_DEG"] = "0.125"
os.environ["MCMC_DISK_BUBBLE"] = "1"
os.environ["MCMC_CELL_LIKELIHOOD"] = "1"
os.environ["MCMC_SIGNFREE_HALO"] = "1"
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0, "code")
import mcmc_fit_all_bins as m
import plot_skymap_all_subtracted as _sub

df_bubble = m.load_events_with_disk()
j_map = m.nfw_j_map()
s1, s2 = _sub.loop_i_shell_templates()
expmaps, _ = m.load_exposure_maps()

# セル集約(10°)。whole ROI(|b|>=0..60)で構築する(Totani §3.1: disk込み)。
CELL = 10.0
LG, BG = m.LG, m.BG
il = np.clip(((LG + 60) / CELL).astype(int), 0, 11)
ib = np.clip(((BG + 60) / CELL).astype(int), 0, 11)
cid = (il * 12 + ib).ravel()
def agg(a): return np.bincount(cid, weights=a.ravel(), minlength=144)

def build_and_fit(bin_idx):
    lo, hi = m.BIN_EDGES[bin_idx], m.BIN_EDGES[bin_idx + 1]
    de_mev = (hi - lo) * 1000.0
    sel = df_bubble[(df_bubble.energy_GeV >= lo) & (df_bubble.energy_GeV < hi)]
    counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
    gas_f, ics_f = _sub._load_galprop_gas_ics_templates(lo, hi)
    gce_f = _sub.gce_nfw_rho25_map()
    if gce_f.max() > 0: gce_f = gce_f / gce_f.max() * gas_f.max()
    unit = expmaps[bin_idx] * m.PIX_SOLID_ANGLE_SR * de_mev
    gas_c, ics_c, gce_c = gas_f * unit, ics_f * unit, gce_f * unit
    flat = ((np.abs(LG) < 22) & (np.abs(BG) >= 10) & (np.abs(BG) < 55)).astype(float)
    iso_c = unit / max(float((unit).mean()), 1e-300)
    li_a = s1 * unit; li_a /= max(li_a.mean(), 1e-300)
    li_b = s2 * unit; li_b /= max(li_b.mean(), 1e-300)
    # whole ROI(disk込み) セル集約
    roi = (np.abs(BG) <= 60) & ((gas_c > 0) | (ics_c > 0))
    N = agg(np.where(roi, counts, 0.0))
    T = {k: agg(np.where(roi, v, 0.0)) for k, v in
         dict(gas=gas_c, ics=ics_c, gce=gce_c, flat=flat, iso=iso_c, li_a=li_a, li_b=li_b).items()}
    cell_valid = agg(roi.astype(float)) > 0

    def make_fit(comps):
        Ts = [T[c] for c in comps]
        def nll(p):
            mu = p[-1] + sum(pi * Ti for pi, Ti in zip(p[:-1], Ts))
            mu = np.maximum(mu[cell_valid], 1e-10)
            return float(np.sum(mu - N[cell_valid] * np.log(mu)))
        x0 = [1.0] * len(comps) + [0.0]
        bnds = [(0, None) if c != "flat" else (0, None) for c in comps] + [(None, None)]
        r = minimize(nll, x0, bounds=bnds, method="L-BFGS-B", options={"maxiter": 2000, "ftol": 1e-13})
        return dict(zip(comps + ["off"], r.x))

    cur = make_fit(["gas", "ics", "gce", "flat"])                     # 現行(iso別処理・Loop I無し)
    faith = make_fit(["gas", "ics", "gce", "flat", "iso", "li_a", "li_b"])  # 忠実(全成分同時)
    return lo, cur, faith

for bidx in (0, 2):  # 1.5 GeV, 4.3 GeV
    lo, cur, faith = build_and_fit(bidx)
    print(f"\n===== 構築ビン {m.BIN_CENTERS[bidx]:.2f} GeV =====")
    print(f"  現行(gas/ICS/GCE/flat): A_gas={cur['gas']:.3g} A_ics={cur['ics']:.3g} "
          f"A_gce={cur['gce']:.3g} A_flat={cur['flat']:.3g}")
    print(f"  忠実(+iso+Loop I)     : A_gas={faith['gas']:.3g} A_ics={faith['ics']:.3g} "
          f"A_gce={faith['gce']:.3g} A_flat={faith['flat']:.3g} A_iso={faith['iso']:.3g} "
          f"A_liA={faith['li_a']:.3g} A_liB={faith['li_b']:.3g}")
