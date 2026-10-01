"""
2026-07-13: diagnose_halo_degeneracy_2.py の6パラメータ版(最終版)。

バブルテンプレートを正負2成分化(Totani (2025) §3.1準拠、diagnose_bubble_check.py
の結果を受けた修正)し、かつ多点始動の再始動回数不足バグ(n_restarts=8→30、
diagnose_restart_stability.py参照)を修正した後のmcmc_fit_all_bins.pyで、
diagnose_halo_degeneracy_2.py と同じROI3分割(バブル領域/10-30度バブル外/
30-60度バブル外)再フィットを実行する。

結果(修正版、n_restarts=30):
  Bin6: 全ROI +0.664(4.83σ) | バブル領域 +0.295(1.60σ) | 高緯度バブル外 -4.05(8.89σ)
  Bin5: 全ROI +0.608(1.90σ) | バブル領域 -1.82(2.97σ)  | 高緯度バブル外 -18.4(15.5σ)

バブル領域内の見かけの超過はほぼ解消(Bin6: 7.78σ→1.60σ)したが、高緯度側の
強い負の有意度はバブル修正の影響を受けず不変(バブルテンプレートは元々その領域で
ゼロのため当然)。GALPROP単一テンプレートの空間形状不一致が引き続き未解決の主因。
"""
import sys
sys.path.insert(0, "code")
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import emcee
import mcmc_fit_all_bins as mfa
import plot_skymap_all_subtracted as _sub

BUBBLE_REGION = (np.abs(_sub.L_GRID) < 22) & (np.abs(_sub.B_GRID) > 10) & (np.abs(_sub.B_GRID) < 55)


def refit(counts, valid, t, seed=0):
    t = dict(t)
    t["valid"] = valid
    if valid.sum() < 20:
        return None
    c_mean = max(counts[valid].mean(), 1e-6)
    x0_la = 0.3 * c_mean / max(t["loopI_a"][valid].mean(), 1e-30)
    x0_lb = 0.3 * c_mean / max(t["loopI_b"][valid].mean(), 1e-30)
    x0_fbneg = 0.3 * c_mean / max(t["fb_neg"][valid].mean(), 1e-30) if t["fb_neg"][valid].mean() > 0 else 0.3
    x0 = [1.0, x0_la, x0_lb, 0.5, x0_fbneg, 0.5]

    def neg_ll_nohalo(p5):
        if any(x < 0 for x in p5[:4]):
            return 1e10
        return -mfa.log_likelihood(list(p5) + [0.0], counts, t)

    res_nh = mfa._multistart_minimize(neg_ll_nohalo, x0[:5], seed=seed)
    lnL_noh = -res_nh.fun

    def neg_ll(p):
        if any(x < 0 for x in p[:4]):
            return 1e10
        return -mfa.log_likelihood(p, counts, t)

    x0_with = list(res_nh.x) + [x0[5]]
    res = mfa._multistart_minimize(neg_ll, x0_with, seed=seed)
    best = res.x
    lnL_with = -res.fun
    if lnL_with < lnL_noh:
        best = np.array(list(res_nh.x) + [0.0])
        lnL_with = lnL_noh
    delta_lnL = lnL_with - lnL_noh
    sig = float(np.sqrt(2 * max(delta_lnL, 0)))

    n_walkers, n_steps, n_burn = 32, 1000, 300
    rng = np.random.default_rng(seed)
    pos = best + 1e-3 * np.abs(best).clip(min=1e-6) * rng.standard_normal((n_walkers, mfa.NDIM))
    pos[:, :4] = np.abs(pos[:, :4])
    sampler = emcee.EnsembleSampler(n_walkers, mfa.NDIM, mfa.log_probability, args=(counts, t))
    sampler.run_mcmc(pos, n_steps, progress=False)
    flat = sampler.get_chain(discard=n_burn, thin=5, flat=True)
    f_halo_med = float(np.median(flat[:, 5]))
    return dict(sig=sig, f_halo_median=f_halo_med, n_valid_pixels=int(valid.sum()),
                n_events=float(counts[valid].sum()))


def main():
    print("露出マップ...")
    expmaps, _ = mfa.load_exposure_maps()
    df_all = mfa.load_all_events()
    print("NFW J-map...")
    j_map = mfa.nfw_j_map()
    nfw_norm, calib = mfa.calibrate_nfw_norm(expmaps[5], j_map)
    bpos, bneg = mfa.build_bubble_counts_template(df_all)
    loop1, loop2 = _sub.loop_i_shell_templates()

    for ib in (4, 5):  # Bin5, Bin6
        emin, emax = mfa.BIN_EDGES[ib], mfa.BIN_EDGES[ib + 1]
        sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
        counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
        masked, _ = _sub.mask_point_sources(counts.copy())
        valid = ~np.isnan(masked)
        valid &= (np.abs(mfa.BG) >= 10) & (np.abs(mfa.BG) <= 60)
        galflux = _sub._load_galprop_template(emin, emax)
        t = mfa.build_templates_for_bin(ib, counts, expmaps[ib], galflux, bpos, bneg,
                                         expmaps[mfa.BUBBLE_BIN], j_map, nfw_norm, loop1, loop2)

        highlat = np.abs(mfa.BG) >= 30
        region_full = valid
        region_A = valid & BUBBLE_REGION
        region_C = valid & highlat & ~BUBBLE_REGION

        print(f"\n=== Bin{ib+1} ({mfa.BIN_CENTERS[ib]:.2f} GeV), バブル正負2成分版 ===")
        for name, mask in (("全ROI", region_full), ("A:バブル領域", region_A), ("C:高緯度・バブル外", region_C)):
            r = refit(counts, mask, t)
            print(f"  [{name:20s}] n_pix={r['n_valid_pixels']:5d} n_evt={r['n_events']:8.0f}  "
                  f"f_halo={r['f_halo_median']:+.4g}  sig={r['sig']:.2f}sigma")


if __name__ == "__main__":
    main()
