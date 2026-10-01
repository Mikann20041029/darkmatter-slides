import sys
sys.path.insert(0, "code")
import numpy as np
from scipy.ndimage import gaussian_filter
import mcmc_fit_all_bins as mfa
import plot_skymap_all_subtracted as _sub

df_all = mfa.load_all_events()

emin, emax = _sub.BIN_EDGES[_sub.BUBBLE_TEMPLATE_BIN], _sub.BIN_EDGES[_sub.BUBBLE_TEMPLATE_BIN + 1]
sel = df_all[(df_all["energy_GeV"] >= emin) & (df_all["energy_GeV"] < emax)]
counts, _, _ = np.histogram2d(sel["l_deg"], sel["b_deg"], bins=[_sub.L_BINS, _sub.B_BINS])
counts = counts.astype(float)
counts, _ = _sub.subtract_isotropic(counts)
counts, _, _ = _sub.subtract_galactic_diffuse(counts, emin, emax)
counts, _, _ = _sub.subtract_point_sources(counts, emin, emax)

bubble_region_OLD = (np.abs(_sub.L_GRID) < 22) & (np.abs(_sub.B_GRID) > 10) & (np.abs(_sub.B_GRID) < 55)
valid_OLD = bubble_region_OLD & ~np.isnan(counts)
resid_OLD = np.zeros_like(counts)
resid_OLD[valid_OLD] = counts[valid_OLD]
pos_OLD = gaussian_filter(np.maximum(resid_OLD, 0.0), sigma=1.0)
neg_OLD = gaussian_filter(np.maximum(-resid_OLD, 0.0), sigma=1.0)

valid_NEW = (np.abs(_sub.B_GRID) >= 10) & ~np.isnan(counts)
resid_NEW = np.zeros_like(counts)
resid_NEW[valid_NEW] = counts[valid_NEW]
pos_NEW = gaussian_filter(np.maximum(resid_NEW, 0.0), sigma=1.0)
neg_NEW = gaussian_filter(np.maximum(-resid_NEW, 0.0), sigma=1.0)

outside = ~bubble_region_OLD & (np.abs(_sub.B_GRID) >= 10)
print("n_pix_outside_bubble_region:", int(outside.sum()))
print("--- OLD (bug: zeroed outside bubble_region before smoothing) ---")
print("pos: n_nonzero=", int((pos_OLD[outside] > 0).sum()), "mean=", float(pos_OLD[outside].mean()), "max=", float(pos_OLD[outside].max()))
print("neg: n_nonzero=", int((neg_OLD[outside] > 0).sum()), "mean=", float(neg_OLD[outside].mean()), "max=", float(neg_OLD[outside].max()))
print("--- NEW (fixed: ROI全域|b|>=10) ---")
print("pos: n_nonzero=", int((pos_NEW[outside] > 0).sum()), "mean=", float(pos_NEW[outside].mean()), "max=", float(pos_NEW[outside].max()))
print("neg: n_nonzero=", int((neg_NEW[outside] > 0).sum()), "mean=", float(neg_NEW[outside].mean()), "max=", float(neg_NEW[outside].max()))
