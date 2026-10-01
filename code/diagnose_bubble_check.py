"""
2026-07-13 ユーザー指摘への対応: 「フェルミバブルは正規の方法でやっているのに、
なぜバブル領域内でNFWハローが正の振幅を要求するのか」を検証する。

diagnose_halo_degeneracy_2.py はf_haloの値しか記録していなかった。本スクリプトは
Bin6についてバブル領域(region A)・全ROI・高緯度非バブル領域(region C)の3通りで
再フィットし、f_gal/f_loopI_a/f_loopI_b/f_fb/f_haloの全パラメータを比較する。

もしバブル領域内でf_fbが全ROIと同程度の「妥当な」値に収まっているなら、
バブルテンプレートの規格化不足が原因ではなく、テンプレートの空間形状自体が
実データの残差と合っていない(規格化を自由にしても吸収しきれない)ことを示唆する。
逆にf_fbが極端な値(境界に張り付く等)ならバブル振幅の自由度不足が主因の可能性が高まる。

[2026-07-13 追記・結果] 実行の結果f_fbは0.40-0.46と妥当な範囲に収まっており、
「バブル規格化不足」は主因ではないと判明。この結果を受けてTotani (2025) §3.1の
正負2テンプレート方式(f_fb_negの追加)を実装したところ、バブル領域内の見かけの
超過は7.78σ→1.60σまで縮小した(diagnose_halo_degeneracy_3_posneg.py参照)。
つまり主因は「バブル振幅の自由度不足」ではなく「バブルテンプレートの空間形状
そのものの不完全性(負の残差成分の欠落)」だったと最終的に判明した。
旧5パラメータモデル前提のため本スクリプト自体は再実行不可。
"""
import pathlib as _pathlib
import sys
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import emcee

SCRIPT_DIR = _pathlib.Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

import mcmc_fit_all_bins as mfa  # noqa: E402
import plot_skymap_all_subtracted as _sub  # noqa: E402

BUBBLE_REGION = (np.abs(_sub.L_GRID) < 22) & (np.abs(_sub.B_GRID) > 10) & (np.abs(_sub.B_GRID) < 55)


def refit_full(counts, valid, t, seed=0):
    t = dict(t)
    t["valid"] = valid
    c_mean = max(counts[valid].mean(), 1e-6)
    x0_la = 0.3 * c_mean / max(t["loopI_a"][valid].mean(), 1e-30)
    x0_lb = 0.3 * c_mean / max(t["loopI_b"][valid].mean(), 1e-30)
    x0 = [1.0, x0_la, x0_lb, 0.5, 0.5]

    def neg_ll_nohalo(p4):
        if any(x < 0 for x in p4):
            return 1e10
        return -mfa.log_likelihood(list(p4) + [0.0], counts, t)

    res_nh = mfa._multistart_minimize(neg_ll_nohalo, x0[:4], seed=seed)
    lnL_noh = -res_nh.fun

    def neg_ll(p):
        if any(x < 0 for x in [p[0], p[1], p[2], p[3]]):
            return 1e10
        return -mfa.log_likelihood(p, counts, t)

    x0_with = list(res_nh.x) + [x0[4]]
    res = mfa._multistart_minimize(neg_ll, x0_with, seed=seed)
    best = res.x
    lnL_with = -res.fun
    if lnL_with < lnL_noh:
        best = np.array(list(res_nh.x) + [0.0])
        lnL_with = lnL_noh
    delta_lnL = lnL_with - lnL_noh
    sig = float(np.sqrt(2 * max(delta_lnL, 0)))

    n_walkers, n_steps, n_burn = 32, 1200, 400
    rng = np.random.default_rng(seed)
    pos = best + 1e-3 * np.abs(best).clip(min=1e-6) * rng.standard_normal((n_walkers, mfa.NDIM))
    pos[:, :4] = np.abs(pos[:, :4])
    sampler = emcee.EnsembleSampler(n_walkers, mfa.NDIM, mfa.log_probability, args=(counts, t))
    sampler.run_mcmc(pos, n_steps, progress=False)
    flat = sampler.get_chain(discard=n_burn, thin=5, flat=True)
    med = np.median(flat, axis=0)
    lo, hi = np.percentile(flat, [16, 84], axis=0)
    return dict(delta_lnL=float(delta_lnL), sig=sig,
                params={n: (float(m), float(l), float(h)) for n, m, l, h in zip(mfa.PARAM_NAMES, med, lo, hi)},
                n_valid_pixels=int(valid.sum()), n_events=float(counts[valid].sum()))


def main():
    print("実測露出マップ読み込み中...")
    expmaps, _ = mfa.load_exposure_maps()
    df_all = mfa.load_all_events()
    print("NFW J-factorマップ計算中...")
    j_map = mfa.nfw_j_map()
    nfw_norm, calib = mfa.calibrate_nfw_norm(expmaps[5], j_map)
    bubble3 = mfa.build_bubble_counts_template(df_all)
    expmap_bubble = expmaps[mfa.BUBBLE_BIN]
    loop1, loop2 = _sub.loop_i_shell_templates()

    ib = 5  # Bin6
    emin, emax = mfa.BIN_EDGES[ib], mfa.BIN_EDGES[ib + 1]
    sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
    counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
    masked, _ = _sub.mask_point_sources(counts.copy())
    valid = ~np.isnan(masked)
    valid &= (np.abs(mfa.BG) >= 10) & (np.abs(mfa.BG) <= 60)
    galflux = _sub._load_galprop_template(emin, emax)
    t = mfa.build_templates_for_bin(ib, counts, expmaps[ib], galflux, bubble3,
                                     expmap_bubble, j_map, nfw_norm, loop1, loop2)

    highlat = np.abs(mfa.BG) >= 30
    region_A = valid & BUBBLE_REGION
    region_C = valid & highlat & ~BUBBLE_REGION

    print("\n=== Bin6 (20.76 GeV): 領域別 全パラメータ比較 ===")
    for name, mask in (("全ROI", valid), ("A:バブル領域", region_A), ("C:高緯度・バブル外", region_C)):
        r = refit_full(counts, mask, t)
        p = r["params"]
        print(f"\n[{name}] n_pix={r['n_valid_pixels']} n_evt={r['n_events']:.0f} sig={r['sig']:.2f}sigma")
        for pname in mfa.PARAM_NAMES:
            m, lo, hi = p[pname]
            print(f"    {pname:10s} = {m:+10.4g}  (16-84%: {lo:+.4g} .. {hi:+.4g})")


if __name__ == "__main__":
    main()
