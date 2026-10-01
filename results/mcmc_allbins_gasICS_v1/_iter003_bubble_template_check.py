import sys
sys.path.insert(0, "code")
import numpy as np
import mcmc_fit_all_bins as mfa
import plot_skymap_all_subtracted as _sub

df_all = mfa.load_all_events()
pos, neg = _sub.build_fermi_bubble_templates_posneg(df_all)

bubble_region = (np.abs(_sub.L_GRID) < 22) & (np.abs(_sub.B_GRID) > 10) & (np.abs(_sub.B_GRID) < 55)
outside = ~bubble_region & (np.abs(_sub.B_GRID) >= 10)

print("=== outside bubble_region (|b|>=10) pixel stats ===")
print("n_pix_outside:", int(outside.sum()))
print("template_pos: n_nonzero=", int((pos[outside] > 0).sum()), "mean=", float(pos[outside].mean()), "max=", float(pos[outside].max()))
print("template_neg: n_nonzero=", int((neg[outside] > 0).sum()), "mean=", float(neg[outside].mean()), "max=", float(neg[outside].max()))
