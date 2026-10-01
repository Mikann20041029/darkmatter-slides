"""
iter-004: 有意度超過(iter-002→iter-003)の機構分析。

iter-003で修正した「フェルミバブル正負テンプレートのROI制限バグ」だけを
分離するため、本スクリプト内でOLD(bubble_region矩形制限、iter-002以前の
バグ版)とNEW(ROI全域、iter-003修正後=現行本番)の2種類のバブルテンプレートを
構築し、それ以外は完全に同一の設定(N-1修正済みのneg_log_likelihood_and_grad、
同じgas/ICS/LoopI/NFWテンプレート、同じイベントデータ)で全13ビンのno-halo/
with-halo L-BFGS-B点推定(MCMCは行わない、lnL比較が目的のため)を行う。

これにより「lnLの変化が本当にバブルテンプレートのROI拡大だけに起因するか」を
このタスク単体で再現・定量化できる(iter-002の生データ/JSONバックアップは
本タスク開始前に削除済みで参照不可のため、再構築した比較用に注記する)。

出力: iter004_lnL_mechanism_analysis.json (このディレクトリに保存)
標準出力は要約1-2行のみ。
"""
import json
import pathlib as _pathlib
import sys
sys.path.insert(0, "code")
import warnings
warnings.filterwarnings("ignore")

import numpy as np
from scipy.ndimage import gaussian_filter

import mcmc_fit_all_bins as mfa
import plot_skymap_all_subtracted as _sub

BASE = _pathlib.Path(__file__).resolve().parent.parent.parent
OUT_PATH = _pathlib.Path(__file__).resolve().parent / "iter004_lnL_mechanism_analysis.json"


def build_bubble_templates(df_all, *, old_restricted: bool):
    """old_restricted=True: iter-002以前のバグ版(bubble_region矩形の外側を強制ゼロ化)。
    old_restricted=False: iter-003修正後(ROI全域|b|>=10)。現行 _sub.build_fermi_bubble_templates_posneg
    と数値的に同一になるはず(検証目的でここでも独立に計算する)。"""
    emin, emax = _sub.BIN_EDGES[_sub.BUBBLE_TEMPLATE_BIN], _sub.BIN_EDGES[_sub.BUBBLE_TEMPLATE_BIN + 1]
    sel = df_all[(df_all["energy_GeV"] >= emin) & (df_all["energy_GeV"] < emax)]
    counts, _, _ = np.histogram2d(sel["l_deg"], sel["b_deg"], bins=[_sub.L_BINS, _sub.B_BINS])
    counts = counts.astype(float)
    counts, _ = _sub.subtract_isotropic(counts)
    counts, _, _ = _sub.subtract_galactic_diffuse(counts, emin, emax)
    counts, _, _ = _sub.subtract_point_sources(counts, emin, emax)

    if old_restricted:
        region = (np.abs(_sub.L_GRID) < 22) & (np.abs(_sub.B_GRID) > 10) & (np.abs(_sub.B_GRID) < 55)
        valid_px = region & ~np.isnan(counts)
    else:
        valid_px = (np.abs(_sub.B_GRID) >= 10) & ~np.isnan(counts)

    resid = np.zeros_like(counts)
    resid[valid_px] = counts[valid_px]
    pos = gaussian_filter(np.maximum(resid, 0.0), sigma=1.0)
    neg = gaussian_filter(np.maximum(-resid, 0.0), sigma=1.0)
    return pos, neg


def point_estimate_fit(counts, templates, x0):
    """MCMCを省き、L-BFGS-B点推定のみでno-halo/with-halo lnLを得る
    (fit_one_bin()のうちMCMC以前の部分を再利用)。"""
    def neg_ll_nohalo(p6):
        val, grad7 = mfa.neg_log_likelihood_and_grad(list(p6) + [0.0], counts, templates)
        return val, grad7[:6]

    res_nh, diag_nh = mfa._multistart_minimize(neg_ll_nohalo, x0[:6], mfa._bounds_no_halo())
    lnL_noh = -res_nh.fun

    def neg_ll(p):
        return mfa.neg_log_likelihood_and_grad(p, counts, templates)

    x0_with_halo = list(res_nh.x) + [x0[6]]
    res, diag_wh = mfa._multistart_minimize(neg_ll, x0_with_halo, mfa._bounds_with_halo())
    lnL_with = -res.fun
    if lnL_with < lnL_noh:
        lnL_with = lnL_noh
        best = np.array(list(res_nh.x) + [0.0])
    else:
        best = res.x
    delta_lnL = lnL_with - lnL_noh
    sig = float(np.sqrt(2 * max(delta_lnL, 0)))
    return dict(lnL_no_halo=float(lnL_noh), lnL_with_halo=float(lnL_with),
                delta_lnL=float(delta_lnL), significance_sigma=sig,
                f_halo_pointest=float(best[6]),
                n_failed_starts_no_halo=diag_nh["n_failed_starts"],
                n_failed_starts_with_halo=diag_wh["n_failed_starts"])


def main():
    np.random.seed(mfa.SEED)
    expmaps, _ = mfa.load_exposure_maps()
    df_all = mfa.load_all_events()
    j_map = mfa.nfw_j_map()
    nfw_norm, calib = mfa.calibrate_nfw_norm(expmaps[5], j_map)
    loop1, loop2 = _sub.loop_i_shell_templates()

    print("OLD(bubble_region矩形制限, iter-002以前のバグ)バブルテンプレート構築中...")
    bpos_old, bneg_old = build_bubble_templates(df_all, old_restricted=True)
    print("NEW(ROI全域, iter-003修正後=現行本番)バブルテンプレート構築中...")
    bpos_new, bneg_new = build_bubble_templates(df_all, old_restricted=False)

    # 現行本番の _sub.build_fermi_bubble_templates_posneg と数値的に一致するか確認
    bpos_prod, bneg_prod = _sub.build_fermi_bubble_templates_posneg(df_all)
    match_pos = bool(np.allclose(bpos_new, bpos_prod))
    match_neg = bool(np.allclose(bneg_new, bneg_prod))
    print(f"NEW再構築 vs 本番関数一致: pos={match_pos} neg={match_neg}")

    results = {}
    for ib in range(mfa.N_BINS):
        emin, emax = mfa.BIN_EDGES[ib], mfa.BIN_EDGES[ib + 1]
        sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
        counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
        masked_counts, n_masked = _sub.mask_point_sources(counts.copy())
        valid = ~np.isnan(masked_counts)
        valid &= (np.abs(mfa.BG) >= 10) & (np.abs(mfa.BG) <= 60)

        gas_flux_i, ics_flux_i = _sub._load_galprop_gas_ics_templates(emin, emax)

        bin_result = {}
        for tag, bpos, bneg in (("OLD_restricted", bpos_old, bneg_old),
                                 ("NEW_roiwide", bpos_new, bneg_new)):
            templates = mfa.build_templates_for_bin(
                ib, counts, expmaps[ib], gas_flux_i, ics_flux_i,
                bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
                expmap_bubble_bin=expmaps[mfa.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
                loop_shell1=loop1, loop_shell2=loop2,
            )
            templates["valid"] = valid
            c_mean = max(counts[valid].mean(), 1e-6)
            x0_gas = 0.5 * c_mean / max(templates["gas"][valid].mean(), 1e-30)
            x0_ics = 0.5 * c_mean / max(templates["ics"][valid].mean(), 1e-30)
            x0_la = 0.3 * c_mean / max(templates["loopI_a"][valid].mean(), 1e-30)
            x0_lb = 0.3 * c_mean / max(templates["loopI_b"][valid].mean(), 1e-30)
            x0_fb_neg = 0.3 * c_mean / max(templates["fb_neg"][valid].mean(), 1e-30) \
                if templates["fb_neg"][valid].mean() > 0 else 0.3
            x0 = [x0_gas, x0_ics, x0_la, x0_lb, 0.5, x0_fb_neg, 0.5]
            try:
                r = point_estimate_fit(counts, templates, x0)
            except Exception as e:
                r = dict(error=str(e))
            bin_result[tag] = r

        results[f"bin{ib+1:02d}"] = dict(e_center_gev=float(mfa.BIN_CENTERS[ib]), **bin_result)
        old_r, new_r = bin_result["OLD_restricted"], bin_result["NEW_roiwide"]
        if "error" not in old_r and "error" not in new_r:
            print(f"Bin{ib+1:02d} ({mfa.BIN_CENTERS[ib]:6.2f} GeV): "
                  f"lnL_noh OLD={old_r['lnL_no_halo']:.2f} NEW={new_r['lnL_no_halo']:.2f} "
                  f"ΔlnL_noh={new_r['lnL_no_halo']-old_r['lnL_no_halo']:+.2f} | "
                  f"lnL_wh OLD={old_r['lnL_with_halo']:.2f} NEW={new_r['lnL_with_halo']:.2f} "
                  f"ΔlnL_wh={new_r['lnL_with_halo']-old_r['lnL_with_halo']:+.2f} | "
                  f"sig OLD={old_r['significance_sigma']:.2f} NEW={new_r['significance_sigma']:.2f}")

    with open(OUT_PATH, "w") as f:
        json.dump(dict(
            description="OLD(bubble_region矩形制限, iter-002以前のバグ再現)とNEW(ROI全域, "
                         "iter-003修正後=現行本番)のバブルテンプレートのみを差し替え、他は完全に"
                         "同一設定(N-1修正済みgrad、同一イベントデータ、同一gas/ICS/LoopI/NFWテンプレート)"
                         "でno-halo/with-halo点推定(L-BFGS-B、MCMCなし)を行った結果。",
            production_match=dict(pos=match_pos, neg=match_neg),
            reproducibility=dict(seed=mfa.SEED, commit_note="iter-004時点の未コミット差分含む"),
            results=results,
        ), f, indent=2, ensure_ascii=False)
    print(f"\n→ {OUT_PATH}")


if __name__ == "__main__":
    main()
