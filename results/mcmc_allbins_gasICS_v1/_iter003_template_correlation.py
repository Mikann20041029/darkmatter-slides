"""iter-003 物理レビュー: バグ修正(fb_neg全ROI化)後のテンプレート間空間相関を診断。
halo有意度上昇が真の検出改善か fb_neg<->halo 新縮退の産物かを切り分ける。
結果は iter003_template_correlation.json に保存。"""
import json, pathlib, sys, warnings
sys.path.insert(0, "code")
warnings.filterwarnings("ignore")
import numpy as np
import mcmc_fit_all_bins as mfa
import plot_skymap_all_subtracted as _sub

BASE = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = BASE / "results/mcmc_allbins_gasICS_v1/iter003_template_correlation.json"
BUBBLE_REGION = (np.abs(_sub.L_GRID) < 22) & (np.abs(_sub.B_GRID) > 10) & (np.abs(_sub.B_GRID) < 55)

np.random.seed(mfa.SEED)
expmaps, _ = mfa.load_exposure_maps()
df_all = mfa.load_all_events()
j_map = mfa.nfw_j_map()
nfw_norm, _ = mfa.calibrate_nfw_norm(expmaps[5], j_map)
bpos, bneg = mfa.build_bubble_counts_template(df_all)
loop1, loop2 = _sub.loop_i_shell_templates()

comp_names = ["gas", "ics", "loopI_a", "loopI_b", "fb", "fb_neg", "halo"]

def corr_report(ib):
    emin, emax = mfa.BIN_EDGES[ib], mfa.BIN_EDGES[ib + 1]
    sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
    counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
    masked, _ = _sub.mask_point_sources(counts.copy())
    valid = ~np.isnan(masked) & (np.abs(mfa.BG) >= 10) & (np.abs(mfa.BG) <= 60)
    gas_flux, ics_flux = _sub._load_galprop_gas_ics_templates(emin, emax)
    t = mfa.build_templates_for_bin(ib, counts, expmaps[ib], gas_flux, ics_flux,
        bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
        expmap_bubble_bin=expmaps[mfa.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
        loop_shell1=loop1, loop_shell2=loop2)
    highlat = np.abs(mfa.BG) >= 30
    regions = {"full_roi": valid,
               "A_bubble": valid & BUBBLE_REGION,
               "C_highlat_ex_bubble": valid & highlat & ~BUBBLE_REGION}
    out = {}
    for rname, mask in regions.items():
        M = np.vstack([t[c][mask].ravel() for c in comp_names])  # (7, npix)
        # Pearson correlation matrix
        C = np.corrcoef(M)
        # halo vs each
        halo_corr = {comp_names[i]: float(C[6, i]) for i in range(6)}
        # regress halo on other 6 (standardized), R^2
        X = M[:6].T  # (npix, 6)
        y = M[6]     # halo
        Xc = X - X.mean(0); yc = y - y.mean()
        # least squares
        beta, *_ = np.linalg.lstsq(Xc, yc, rcond=None)
        yhat = Xc @ beta
        ss_res = np.sum((yc - yhat) ** 2); ss_tot = np.sum(yc ** 2)
        r2_all = float(1 - ss_res / ss_tot)
        # regress halo on {gas, ics} only (indices 0,1)
        Xg = M[[0, 1]].T; Xgc = Xg - Xg.mean(0)
        bg, *_ = np.linalg.lstsq(Xgc, yc, rcond=None)
        r2_gasics = float(1 - np.sum((yc - Xgc @ bg) ** 2) / ss_tot)
        # regress halo on fb_neg only
        Xn = M[[5]].T; Xnc = Xn - Xn.mean(0)
        bn, *_ = np.linalg.lstsq(Xnc, yc, rcond=None)
        r2_fbneg = float(1 - np.sum((yc - Xnc @ bn) ** 2) / ss_tot)
        # condition number of the standardized 7-template design
        Ms = (M - M.mean(1, keepdims=True))
        norms = np.linalg.norm(Ms, axis=1, keepdims=True); norms[norms == 0] = 1
        Msn = Ms / norms
        sv = np.linalg.svd(Msn, compute_uv=False)
        cond = float(sv[0] / sv[-1])
        out[rname] = dict(npix=int(mask.sum()),
                          halo_corr_with=halo_corr,
                          R2_halo_on_all6=r2_all,
                          R2_halo_on_gas_ics=r2_gasics,
                          R2_halo_on_fbneg_only=r2_fbneg,
                          cond_number_7template=cond)
    return out

result = {f"bin{ib+1}_{mfa.BIN_CENTERS[ib]:.2f}GeV": corr_report(ib) for ib in (2, 4, 5)}
OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False))
# short stdout summary
for k, v in result.items():
    for rn, d in v.items():
        print(f"{k} {rn}: corr(halo,fbneg)={d['halo_corr_with']['fb_neg']:+.3f} "
              f"corr(halo,ics)={d['halo_corr_with']['ics']:+.3f} "
              f"R2(halo|all6)={d['R2_halo_on_all6']:.3f} "
              f"R2(halo|fbneg)={d['R2_halo_on_fbneg_only']:.3f} cond={d['cond_number_7template']:.1f}")
print(f"-> {OUT}")
