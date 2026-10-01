"""
2026-07-15: GALPROP gas/ICS独立テンプレート化(galdef SLZ6R30T150C2, 7パラメータ)後の
ROI分割再検証。code/diagnose_halo_degeneracy_3_posneg.py(旧f_gal単一テンプレート、
6パラメータ版)と同じ3分割ロジック(全ROI / バブル領域内 / 高緯度バブル外)を、
更新後のmcmc_fit_all_bins.py(f_gas/f_ics/f_loopI_a/f_loopI_b/f_fb/f_fb_neg/f_halo、
NDIM=7)で再実行する。

旧版(単一f_gal, 2026-07-13時点)の結果(.dev/HANDOFF.md記載):
  Bin6: 全ROI +0.664(4.83σ) | バブル領域 +0.295(1.60σ) | 高緯度バブル外 -4.05(8.89σ)
  Bin5: 全ROI +0.608(1.90σ) | バブル領域 -1.82(2.97σ)  | 高緯度バブル外 -18.4(15.5σ)

[2026-07-15 iter-2] mcmc_fit_all_bins.py iter-2の修正(L-BFGS-B有界凸最適化への
切り替え、f_halo非負制約追加、np.random.seed固定)をこのROI分割スクリプトにも
反映する。最適化・emcee実行ロジックはmfa._multistart_minimize()/
mfa.run_mcmc_with_autocorr_check()を再利用し、重複実装を避ける
(詳細はconsolidated-feedback.md CRITICAL-1,2,4)。

本スクリプトの結果は results/mcmc_allbins_gasICS_v1/roi_partition_gasics.json に保存する
(標準出力は1-2行サマリのみ)。符号反転が解消したか否かは解釈せず数値のみ報告する
(.dev/teams/galprop-gas-ics-separation/spec.md 合格条件: 解消を前提にしない)。
"""
import json
import pathlib as _pathlib
import sys
sys.path.insert(0, "code")
import warnings
warnings.filterwarnings("ignore")

from typing import Optional

import numpy as np
from numpy.typing import NDArray
import mcmc_fit_all_bins as mfa
import plot_skymap_all_subtracted as _sub

BASE = _pathlib.Path(__file__).resolve().parent.parent
OUT_PATH = BASE / "results/mcmc_allbins_gasICS_v1/roi_partition_gasics.json"

BUBBLE_REGION = (np.abs(_sub.L_GRID) < 22) & (np.abs(_sub.B_GRID) > 10) & (np.abs(_sub.B_GRID) < 55)


def refit(
    counts: NDArray[np.float64],
    valid: NDArray[np.bool_],
    t: mfa.TemplateDict,
) -> Optional[dict[str, object]]:
    t = dict(t)
    t["valid"] = valid
    if valid.sum() < 20:
        return None
    c_mean = max(counts[valid].mean(), 1e-6)
    x0_gas = 0.5 * c_mean / max(t["gas"][valid].mean(), 1e-30)
    x0_ics = 0.5 * c_mean / max(t["ics"][valid].mean(), 1e-30)
    x0_la = 0.3 * c_mean / max(t["loopI_a"][valid].mean(), 1e-30)
    x0_lb = 0.3 * c_mean / max(t["loopI_b"][valid].mean(), 1e-30)
    x0_fbneg = 0.3 * c_mean / max(t["fb_neg"][valid].mean(), 1e-30) if t["fb_neg"][valid].mean() > 0 else 0.3
    x0 = [x0_gas, x0_ics, x0_la, x0_lb, 0.5, x0_fbneg, 0.5]

    # [2026-07-16 iter-2引き継ぎ修正] mfa._multistart_minimize()はscipy.optimize.minimize(...,
    # jac=True)を使う(consolidated-feedback.md CRITICAL-1でNelder-Mead→L-BFGS-Bに刷新済み)。
    # jac=Trueは目的関数が(値, 勾配)のタプルを返すことを要求するため、旧来の
    # -mfa.log_likelihood(...)(スカラーのみ返す)をそのまま渡すとscipyが
    # `fg[1]`でTypeErrorを起こす。fit_one_bin()と同様にneg_log_likelihood_and_grad()
    # (解析的勾配)を使う関数に置き換える。
    def neg_ll_nohalo(p6):
        val, grad7 = mfa.neg_log_likelihood_and_grad(list(p6) + [0.0], counts, t)
        return val, grad7[:6]

    res_nh, diag_nh = mfa._multistart_minimize(neg_ll_nohalo, x0[:6], mfa._bounds_no_halo())
    lnL_noh = -res_nh.fun

    def neg_ll(p):
        return mfa.neg_log_likelihood_and_grad(p, counts, t)

    x0_with = list(res_nh.x) + [x0[6]]
    res, diag_wh = mfa._multistart_minimize(neg_ll, x0_with, mfa._bounds_with_halo())
    best = res.x
    lnL_with = -res.fun
    if lnL_with < lnL_noh:
        best = np.array(list(res_nh.x) + [0.0])
        lnL_with = lnL_noh
    delta_lnL = lnL_with - lnL_noh
    sig = float(np.sqrt(2 * max(delta_lnL, 0)))

    flat, autocorr_diag = mfa.run_mcmc_with_autocorr_check(
        best, counts, t, n_walkers=32, n_steps_init=1000, n_burn=300
    )
    f_gas_med = float(np.median(flat[:, 0]))
    f_ics_med = float(np.median(flat[:, 1]))
    f_halo_med = float(np.median(flat[:, 6]))
    return dict(sig=sig, f_halo_median=f_halo_med, f_gas_median=f_gas_med, f_ics_median=f_ics_med,
                n_valid_pixels=int(valid.sum()), n_events=float(counts[valid].sum()),
                convexity_check=dict(no_halo=diag_nh, with_halo=diag_wh),
                autocorr_check=autocorr_diag)


def main():
    # [2026-07-15 iter-2, consolidated-feedback.md CRITICAL-4] mcmc_fit_all_bins.SEEDと
    # 同じ固定シードで再現性を確保する(理由はmfa.run_mcmc_with_autocorr_check()docstring参照)。
    np.random.seed(mfa.SEED)
    print(f"再現性シード固定: np.random.seed({mfa.SEED})")
    print("露出マップ...")
    expmaps, _ = mfa.load_exposure_maps()
    df_all = mfa.load_all_events()
    print("NFW J-map...")
    j_map = mfa.nfw_j_map()
    nfw_norm, calib = mfa.calibrate_nfw_norm(expmaps[5], j_map)
    bpos, bneg = mfa.build_bubble_counts_template(df_all)
    loop1, loop2 = _sub.loop_i_shell_templates()

    all_results = {}
    for ib in (4, 5):  # Bin5, Bin6
        emin, emax = mfa.BIN_EDGES[ib], mfa.BIN_EDGES[ib + 1]
        sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
        counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
        masked, _ = _sub.mask_point_sources(counts.copy())
        valid = ~np.isnan(masked)
        valid &= (np.abs(mfa.BG) >= 10) & (np.abs(mfa.BG) <= 60)
        gas_flux, ics_flux = _sub._load_galprop_gas_ics_templates(emin, emax)
        t = mfa.build_templates_for_bin(
            ib, counts, expmaps[ib], gas_flux, ics_flux,
            bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
            expmap_bubble_bin=expmaps[mfa.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
            loop_shell1=loop1, loop_shell2=loop2,
        )

        highlat = np.abs(mfa.BG) >= 30
        region_full = valid
        region_A = valid & BUBBLE_REGION
        region_C = valid & highlat & ~BUBBLE_REGION

        bin_result = {}
        print(f"\n=== Bin{ib+1} ({mfa.BIN_CENTERS[ib]:.2f} GeV), gas/ICS分離7パラメータ版 ===")
        for name, mask in (("full_roi", region_full), ("A_bubble_region", region_A),
                            ("C_highlat_ex_bubble", region_C)):
            r = refit(counts, mask, t)
            bin_result[name] = r
            print(f"  [{name:20s}] n_pix={r['n_valid_pixels']:5d} n_evt={r['n_events']:8.0f}  "
                  f"f_gas={r['f_gas_median']:+.4g} f_ics={r['f_ics_median']:+.4g} "
                  f"f_halo={r['f_halo_median']:+.4g}  sig={r['sig']:.2f}sigma")
        all_results[f"bin{ib+1}"] = bin_result

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(dict(
            description="gas/ICS分離7パラメータ版でのROI3分割再フィット(Bin5,Bin6)。"
                         "旧f_gal単一テンプレート版(6パラメータ)の参考値は"
                         ".dev/HANDOFF.mdおよびcode/diagnose_halo_degeneracy_3_posneg.py参照",
            legacy_reference=dict(
                bin6="全ROI +0.664(4.83sigma) | バブル領域 +0.295(1.60sigma) | 高緯度バブル外 -4.05(8.89sigma)",
                bin5="全ROI +0.608(1.90sigma) | バブル領域 -1.82(2.97sigma) | 高緯度バブル外 -18.4(15.5sigma)",
            ),
            results=all_results,
        ), f, indent=2, ensure_ascii=False)
    print(f"\n→ {OUT_PATH}")


if __name__ == "__main__":
    main()
