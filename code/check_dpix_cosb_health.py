"""DPIX_SR cos(b) 修正の数値健全性チェック。
1. 物理: PIX_SOLID_ANGLE_SR の b=0 極限一致 / b->-b 対称 / b=60 比 / ROI総立体角の次元整合
2. 数値: Bin6 の解析勾配 vs 有限差分一致(no-halo/with-halo 点で)、fun_spread
出力: results/mcmc_allbins_gasICS_v2_cosb/health_check.json
"""
import json
import pathlib
import sys

import numpy as np
from scipy.optimize import approx_fprime

sys.path.insert(0, "code")
import mcmc_fit_all_bins as mfa
import plot_skymap_all_subtracted as _sub

BASE = pathlib.Path(__file__).resolve()
OUT = mfa.BASE / "results/mcmc_allbins_gasICS_v2_cosb"
OUT.mkdir(parents=True, exist_ok=True)

np.random.seed(mfa.SEED)
report: dict[str, object] = {"seed": mfa.SEED, "environment": mfa.env_stamp()}

# ---- 1. 物理チェック -------------------------------------------------------
psa = mfa.PIX_SOLID_ANGLE_SR
BG = mfa.BG
scalar_old = (np.pi / 180.0) ** 2
# b=0 に最も近い緯度セルでの一致度
j0 = np.argmin(np.abs(mfa.B_C))
b0 = float(mfa.B_C[j0])
ratio_b0 = float(psa[0, j0] / scalar_old)
# b->-b 対称性: cos は偶関数。B_C が対称グリッドか確認しつつ、|b| が等しいセルで一致
sym_err = 0.0
for jb in range(len(mfa.B_C)):
    b = mfa.B_C[jb]
    jmatch = np.argmin(np.abs(mfa.B_C + b))
    sym_err = max(sym_err, abs(psa[0, jb] - psa[0, jmatch]))
# b=60 での比(cos60=0.5)
j60 = np.argmin(np.abs(np.abs(mfa.B_C) - 60.0))
ratio_b60 = float(psa[0, j60] / scalar_old)
# 次元整合: ROI(|b| in [10,60])の総立体角。解析値 = ∫dl ∫cos b db
#   l:[-60,60]=120°=2.094 rad, b:±[10,60] => 2*∫_10^60 cos b db = 2*(sin60-sin10)
valid = (np.abs(BG) >= 10) & (np.abs(BG) <= 60)
sum_psa = float(np.sum(psa[valid]))
dl_rad = np.radians(120.0)
analytic = dl_rad * 2.0 * (np.sin(np.radians(60.0)) - np.sin(np.radians(10.0)))
report["physics"] = dict(
    b_nearest_zero_deg=b0,
    ratio_at_b0_over_scalar=ratio_b0,          # ~cos(0.5°)~0.99996
    symmetry_max_abs_err=float(sym_err),        # ~0 (偶関数)
    ratio_at_b60_over_scalar=ratio_b60,         # ~0.5
    roi_total_solid_angle_sr_numeric=sum_psa,
    roi_total_solid_angle_sr_analytic=float(analytic),
    roi_rel_err=float(abs(sum_psa - analytic) / analytic),
    old_scalar_roi_total_sr=float(np.sum(np.full(valid.sum(), scalar_old))),
)
print(f"[physics] b0比={ratio_b0:.5f} b60比={ratio_b60:.5f} 対称誤差={sym_err:.2e} "
      f"ROI相対誤差={report['physics']['roi_rel_err']:.4f}")

# ---- 2. Bin6 の勾配一致 + fun_spread ---------------------------------------
IB6 = 5
expmaps, exp_bc = mfa.load_exposure_maps()
df_all = mfa.load_all_events()
j_map = mfa.nfw_j_map()
nfw_norm, calib = mfa.calibrate_nfw_norm(expmaps[IB6], j_map)
bpos, bneg = mfa.build_bubble_counts_template(df_all)
loop1, loop2 = _sub.loop_i_shell_templates()

emin, emax = mfa.BIN_EDGES[IB6], mfa.BIN_EDGES[IB6 + 1]
sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
masked, n_masked = _sub.mask_point_sources(counts.copy())
valid6 = ~np.isnan(masked)
valid6 &= (np.abs(BG) >= 10) & (np.abs(BG) <= 60)

gas_flux, ics_flux = _sub._load_galprop_gas_ics_templates(emin, emax)
t = mfa.build_templates_for_bin(
    IB6, counts, expmaps[IB6], gas_flux, ics_flux,
    bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
    expmap_bubble_bin=expmaps[mfa.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
    loop_shell1=loop1, loop_shell2=loop2)
t["valid"] = valid6

c_mean = max(counts[valid6].mean(), 1e-6)
x0 = [0.5 * c_mean / max(t["gas"][valid6].mean(), 1e-30),
      0.5 * c_mean / max(t["ics"][valid6].mean(), 1e-30),
      0.3 * c_mean / max(t["loopI_a"][valid6].mean(), 1e-30),
      0.3 * c_mean / max(t["loopI_b"][valid6].mean(), 1e-30),
      0.5,
      0.3 * c_mean / max(t["fb_neg"][valid6].mean(), 1e-30) if t["fb_neg"][valid6].mean() > 0 else 0.3,
      0.5]

r = mfa.fit_one_bin(IB6, counts, t, x0)
best = np.array([r["params"][n]["median"] for n in mfa.PARAM_NAMES])

# 解析勾配 vs 有限差分(fit点と x0 の2点)
def val_only(p):
    return mfa.neg_log_likelihood_and_grad(p, counts, t)[0]

grad_checks = []
for label, p in [("x0", np.array(x0, float)), ("best", best)]:
    _, ga = mfa.neg_log_likelihood_and_grad(p, counts, t)
    eps = np.sqrt(np.finfo(float).eps) * np.maximum(np.abs(p), 1.0)
    gf = approx_fprime(p, val_only, eps)
    denom = np.maximum(np.abs(ga), 1.0)
    max_rel = float(np.max(np.abs(ga - gf) / denom))
    grad_checks.append(dict(point=label, max_abs_err=float(np.max(np.abs(ga - gf))),
                            max_rel_err=max_rel,
                            analytic=ga.tolist(), finite_diff=gf.tolist()))
    print(f"[grad] {label}: max_abs_err={np.max(np.abs(ga-gf)):.2e} max_rel_err={max_rel:.2e}")

spreads = [r["convexity_check"]["no_halo"]["fun_spread_successful_only"],
           r["convexity_check"]["with_halo"]["fun_spread_successful_only"]]
report["bin6"] = dict(
    f_halo_median=r["params"]["f_halo"]["median"],
    f_halo_lo16=r["params"]["f_halo"]["lo16"],
    f_halo_hi84=r["params"]["f_halo"]["hi84"],
    delta_lnL=r["delta_lnL"], significance_sigma=r["significance_sigma"],
    fun_spread_no_halo=spreads[0], fun_spread_with_halo=spreads[1],
    n_masked_point_sources=int(n_masked),
    gradient_checks=grad_checks,
)
print(f"[bin6] f_halo={report['bin6']['f_halo_median']:.4g} "
      f"sig={report['bin6']['significance_sigma']:.2f}sigma "
      f"fun_spread(nohalo/withhalo)={spreads[0]:.2e}/{spreads[1]:.2e}")

with open(OUT / "health_check.json", "w") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)
print(f"-> {OUT}/health_check.json")
