"""Region C (highlat, bubble除外) のf_haloを非負制約なしで再最適化し、
iter-002レビュアが行った検証(制約を外すと真に負に落ちるか)を、
iter-003修正後のテンプレートで再現する。"""
import sys
sys.path.insert(0, "code")
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import mcmc_fit_all_bins as mfa
import plot_skymap_all_subtracted as _sub

np.random.seed(mfa.SEED)
BUBBLE_REGION = (np.abs(_sub.L_GRID) < 22) & (np.abs(_sub.B_GRID) > 10) & (np.abs(_sub.B_GRID) < 55)

expmaps, _ = mfa.load_exposure_maps()
df_all = mfa.load_all_events()
j_map = mfa.nfw_j_map()
nfw_norm, calib = mfa.calibrate_nfw_norm(expmaps[5], j_map)
bpos, bneg = mfa.build_bubble_counts_template(df_all)
loop1, loop2 = _sub.loop_i_shell_templates()

# _bounds_with_halo()と同じ(f_gas,f_ics,f_loopI_a,f_loopI_b,f_fbは非負、f_fb_negは符号自由)
# だがf_halo(index6)だけ非負制約を外す(=NONNEG_IDXからindex6を除いたもの)
bounds_unconstrained_halo = [(0.0, None)] * 5 + [(None, None), (None, None)]

for ib in (4, 5):
    emin, emax = mfa.BIN_EDGES[ib], mfa.BIN_EDGES[ib + 1]
    sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
    counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
    masked, _ = _sub.mask_point_sources(counts.copy())
    valid = ~np.isnan(masked)
    valid &= (np.abs(mfa.BG) >= 10) & (np.abs(mfa.BG) <= 60)
    highlat = np.abs(mfa.BG) >= 30
    region_C = valid & highlat & ~BUBBLE_REGION

    gas_flux, ics_flux = _sub._load_galprop_gas_ics_templates(emin, emax)
    t = mfa.build_templates_for_bin(
        ib, counts, expmaps[ib], gas_flux, ics_flux,
        bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
        expmap_bubble_bin=expmaps[mfa.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
        loop_shell1=loop1, loop_shell2=loop2,
    )
    t = dict(t)
    t["valid"] = region_C

    c_mean = max(counts[region_C].mean(), 1e-6)
    x0_gas = 0.5 * c_mean / max(t["gas"][region_C].mean(), 1e-30)
    x0_ics = 0.5 * c_mean / max(t["ics"][region_C].mean(), 1e-30)
    x0_la = 0.3 * c_mean / max(t["loopI_a"][region_C].mean(), 1e-30)
    x0_lb = 0.3 * c_mean / max(t["loopI_b"][region_C].mean(), 1e-30)
    x0_fbneg = 0.3

    def neg_ll(p):
        return mfa.neg_log_likelihood_and_grad(p, counts, t)

    for f_halo_sign, label in ((+0.5, "positive-start"), (-0.5, "negative-start")):
        x0 = [x0_gas, x0_ics, x0_la, x0_lb, 0.5, x0_fbneg, f_halo_sign]
        res, diag = mfa._multistart_minimize(neg_ll, x0, bounds_unconstrained_halo)
        print(f"Bin{ib+1} region_C unconstrained f_halo, init={label}: "
              f"f_halo_MLE={res.x[6]:+.6g}  fun={res.fun:.6f}  fun_spread={diag.get('fun_spread')}")
