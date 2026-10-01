"""
2026-07-13: バブル正負2テンプレート化(f_fb_neg追加)後の全13ビン初回実行で、
Bin3(4.31GeV)・Bin4(7.28GeV)・Bin7(35.06GeV)が旧5パラメータモデル時より
大幅に高い有意度(それぞれ25.3σ, 27.2σ, 8.0σ)を示した。これがLoop I幾何モデル
導入時(2026-07-12)と同種の「多点始動Nelder-Meadが局所解にはまる」バグの再発
(f_fb_neg追加で探索空間が4→5次元(no-halo)に拡張され、n_restarts=8では
不足になった)かどうかをn_restarts=8/30/60で比較検証する。

結果:
  Bin3: n_restarts=8→29.4σ, 30→20.6σ, 60→4.68σ (収束せず、8回は明らかに不足)
  Bin4: 8/30/60とも4.244σで不変(このseedでは8回でも安定していた)
  Bin7: n_restarts=8→27.9σ, 30/60とも3.51σで安定 (8回は不足、30回で収束)
判定: 局所解バグの再発と確認。mcmc_fit_all_bins.py の _multistart_minimize()
デフォルトを n_restarts=8→30 に修正し、全13ビンを再計算した
(結果: Bin6ヘッドライン 8.73σ→4.83σ、詳細は.dev/CHANGELOG.md参照)。
"""
import sys
sys.path.insert(0, "code")
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import mcmc_fit_all_bins as mfa
import plot_skymap_all_subtracted as _sub

print("露出マップ...")
expmaps, _ = mfa.load_exposure_maps()
df_all = mfa.load_all_events()
print("NFW J-map...")
j_map = mfa.nfw_j_map()
nfw_norm, calib = mfa.calibrate_nfw_norm(expmaps[5], j_map)
bpos, bneg = mfa.build_bubble_counts_template(df_all)
loop1, loop2 = _sub.loop_i_shell_templates()

for ib in (2, 3, 6):  # Bin3, Bin4, Bin7 (0-indexed)
    emin, emax = mfa.BIN_EDGES[ib], mfa.BIN_EDGES[ib + 1]
    sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
    counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
    masked, _ = _sub.mask_point_sources(counts.copy())
    valid = ~np.isnan(masked)
    valid &= (np.abs(mfa.BG) >= 10) & (np.abs(mfa.BG) <= 60)
    galflux = _sub._load_galprop_template(emin, emax)
    t = mfa.build_templates_for_bin(ib, counts, expmaps[ib], galflux, bpos, bneg,
                                     expmaps[mfa.BUBBLE_BIN], j_map, nfw_norm, loop1, loop2)
    t["valid"] = valid

    c_mean = max(counts[valid].mean(), 1e-6)
    x0_la = 0.3 * c_mean / max(t["loopI_a"][valid].mean(), 1e-30)
    x0_lb = 0.3 * c_mean / max(t["loopI_b"][valid].mean(), 1e-30)
    x0_fbneg = 0.3 * c_mean / max(t["fb_neg"][valid].mean(), 1e-30) if t["fb_neg"][valid].mean() > 0 else 0.3
    x0 = [1.0, x0_la, x0_lb, 0.5, x0_fbneg, 0.5]

    print(f"\n=== Bin{ib+1} ({mfa.BIN_CENTERS[ib]:.2f} GeV) ===")
    for n_restarts in (8, 30, 60):
        def neg_ll_nohalo(p5):
            if any(x < 0 for x in p5[:4]):
                return 1e10
            return -mfa.log_likelihood(list(p5) + [0.0], counts, t)
        res_nh = mfa._multistart_minimize(neg_ll_nohalo, x0[:5], n_restarts=n_restarts, seed=1)
        lnL_noh = -res_nh.fun

        def neg_ll(p):
            if any(x < 0 for x in p[:4]):
                return 1e10
            return -mfa.log_likelihood(p, counts, t)
        x0_with = list(res_nh.x) + [x0[5]]
        res = mfa._multistart_minimize(neg_ll, x0_with, n_restarts=n_restarts, seed=1)
        lnL_with = -res.fun
        if lnL_with < lnL_noh:
            lnL_with = lnL_noh
        delta_lnL = lnL_with - lnL_noh
        sig = float(np.sqrt(2 * max(delta_lnL, 0)))
        print(f"  n_restarts={n_restarts:3d}: lnL_noh={lnL_noh:12.3f}  lnL_with={lnL_with:12.3f}  "
              f"delta_lnL={delta_lnL:8.3f}  sig={sig:.3f}sigma  f_halo_pt={res.x[5]:+.4g}")
