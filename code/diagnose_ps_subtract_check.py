"""
2026-07-16深夜: 点源処理を「NaNマスク」(mask_point_sources, 現行headline)から
「Totani式スペクトルモデル差し引き」(subtract_point_sources)に切り替えた場合、
結果がどう変わるかを検証する。

背景: subtract_point_sources()は2026-06-20に実装済みだったが、後発の
mcmc_fit_all_bins.py(gas/ICS分離7パラメータ版)には引き継がれておらず、
現行headlineはmask_point_sources()(NaN)のままだった。さらに
subtract_point_sources()自体も、2026-07-11に修正された実測露出マップ
(5.80e11 cm²·s平均、旧Mrk501較正1.24e11の4.68倍)を反映しておらず、
古い_PS_EXPOSURE定数のままだった。本スクリプトはこの2つの問題を修正した
「補正版」点源差し引きで、Bin6を含む複数ビンを現行headlineパイプラインと
比較する。

**これはheadlineの置き換えではなく検証。** results/mcmc_allbins_gasICS_v1/
配下の既存ファイルは一切上書きしない。出力は
results/mcmc_allbins_gasICS_v1/ps_subtract_check.json に保存する。
"""
import json
import pathlib as _pathlib
import sys
import warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, "code")

import numpy as np

import mcmc_fit_all_bins as mfa
import plot_skymap_all_subtracted as _sub

BASE = _pathlib.Path(__file__).resolve().parent.parent
OUT_PATH = BASE / "results/mcmc_allbins_gasICS_v1/ps_subtract_check.json"


def subtract_point_sources_corrected(counts, emin_gev, emax_gev, expmap):
    """subtract_point_sources()の補正版。定数_PS_EXPOSURE(旧Mrk501較正,
    1.24e11 cm²·s)の代わりに、実測済みの per-pixel 露出マップ(expmap,
    ビンごとに異なる、平均5.80e11 cm²·s)を使う。ロジックはオリジナルと同一、
    露出の取得元だけを差し替えた。

    [2026-07-16深夜、緊急数値レビューCRITICAL-1対応] LogParabola/PLSuperExpCutoff
    モデルをpivotエネルギーから遠いビンへ外挿すると期待カウントが実測カウントを
    上回り、差引後に負のカウント(物理的にありえない)が生じることがある
    (レビューで実測: Bin6で127/12000ピクセル、最悪-114.8)。Poisson尤度は
    負のデータを扱えない(勾配 dNLL/dmu = 1-c/mu が常に正になり最適化を歪める)。
    レビュー推奨の「最小限の修正」(np.maximum(0)でクリップ)を適用し、
    クリップ量を診断値として返す。"""
    emin_mev = emin_gev * 1000.0
    emax_mev = emax_gev * 1000.0
    E_grid = np.logspace(np.log10(emin_mev), np.log10(emax_mev), 30)

    result = counts.copy().astype(np.float64)
    n_sub_total = 0

    for i in range(len(_sub._CAT_L)):
        lc, bc = _sub._CAT_L[i], _sub._CAT_B[i]
        il = int((lc - _sub.L_BINS[0]) / _sub.PIXEL_DEG)
        ib = int((bc - _sub.B_BINS[0]) / _sub.PIXEL_DEG)
        if not (0 <= il < len(_sub.L_CENTERS) and 0 <= ib < len(_sub.B_CENTERS)):
            continue

        E0 = _sub._CAT_PIV[i]
        st = _sub._CAT_STYPE[i]

        if "LogParabola" in st:
            N0, alpha, beta = _sub._CAT_LPN0[i], _sub._CAT_LPA[i], _sub._CAT_LPB[i]
            log_ratio = np.log(E_grid / E0)
            flux_vals = N0 * (E_grid / E0) ** (-(alpha + beta * log_ratio))
        elif "PLSuperExpCutoff" in st or "PLEC" in st:
            e_peak = _sub._CAT_PLEC_EPEAK[i]
            if e_peak < 5000:
                continue
            N0, Gamma = _sub._CAT_PLN0[i], _sub._CAT_PLIDX[i]
            flux_vals = N0 * (E_grid / E0) ** (-Gamma)
        else:
            N0, Gamma = _sub._CAT_PLN0[i], _sub._CAT_PLIDX[i]
            flux_vals = N0 * (E_grid / E0) ** (-Gamma)

        if N0 <= 0 or not np.isfinite(N0):
            continue

        flux_bin = float(np.trapezoid(flux_vals, E_grid))
        if not np.isfinite(flux_bin) or flux_bin <= 0:
            continue

        exp_here = expmap[il, ib]  # 【修正点】定数ではなくピクセルごとの実測露出
        if exp_here <= 0:
            continue
        n_expect = flux_bin * exp_here
        result[il, ib] -= n_expect
        n_sub_total += 1

    # 【CRITICAL修正】負カウントをクリップし、量を記録する
    negative_mask = result < 0
    n_negative_pixels = int(negative_mask.sum())
    total_negative_deficit = float(-result[negative_mask].sum()) if n_negative_pixels else 0.0
    result = np.maximum(result, 0.0)

    return result, n_sub_total, n_negative_pixels, total_negative_deficit


def refit_bin(ib, counts, valid, t):
    """既存mfa.fit_one_bin()相当のロジックをvalidマスク差し替え可能な形で再利用。

    [2026-07-16深夜、緊急数値レビューIMPORTANT対応] 呼び出し直前に必ず
    np.random.seed(mfa.SEED)を入れ直し、(A)(B)が同一walker初期化列を
    共有するようにする(RNGストリーム順序の交絡を排除するため)。"""
    np.random.seed(mfa.SEED)
    t = dict(t)
    t["valid"] = valid
    c_mean = max(counts[valid].mean(), 1e-6)
    x0 = [
        0.5 * c_mean / max(t["gas"][valid].mean(), 1e-30),
        0.5 * c_mean / max(t["ics"][valid].mean(), 1e-30),
        0.3 * c_mean / max(t["loopI_a"][valid].mean(), 1e-30),
        0.3 * c_mean / max(t["loopI_b"][valid].mean(), 1e-30),
        0.5,
        0.3 * c_mean / max(t["fb_neg"][valid].mean(), 1e-30) if t["fb_neg"][valid].mean() > 0 else 0.3,
        0.5,
    ]
    result = mfa.fit_one_bin(ib, counts, t, x0)
    return result


def run_for_bin(ib, df_all, expmaps, j_map, nfw_norm, bpos, bneg, loop1, loop2):
    emin, emax = mfa.BIN_EDGES[ib], mfa.BIN_EDGES[ib + 1]
    sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
    counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])

    gas_flux, ics_flux = _sub._load_galprop_gas_ics_templates(emin, emax)
    t = mfa.build_templates_for_bin(
        ib, counts, expmaps[ib], gas_flux, ics_flux,
        bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
        expmap_bubble_bin=expmaps[mfa.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
        loop_shell1=loop1, loop_shell2=loop2,
    )

    # --- (A) 現行headline: NaNマスク ---
    masked, _ = _sub.mask_point_sources(counts.copy())
    valid_a = ~np.isnan(masked)
    valid_a &= (np.abs(mfa.BG) >= 10) & (np.abs(mfa.BG) <= 60)
    res_a = refit_bin(ib, counts, valid_a, t)

    # --- (B) 補正版: スペクトルモデル差し引き(実測露出) + 負カウントクリップ ---
    counts_sub, n_sub, n_neg_pix, neg_deficit = subtract_point_sources_corrected(
        counts, emin, emax, expmaps[ib])
    valid_b = (np.abs(mfa.BG) >= 10) & (np.abs(mfa.BG) <= 60)  # NaNが無いので|b|カットのみ
    res_b = refit_bin(ib, counts_sub, valid_b, t)

    def diag(res):
        return dict(
            fun_spread_no_halo=res["convexity_check"]["no_halo"]["fun_spread_successful_only"],
            fun_spread_with_halo=res["convexity_check"]["with_halo"]["fun_spread_successful_only"],
            tau_max=res["autocorr_check"].get("tau_max"),
            meets_50tau_recommendation=res["autocorr_check"].get("meets_50tau_recommendation"),
        )

    return dict(
        bin=ib + 1, e_center_gev=float(mfa.BIN_CENTERS[ib]),
        n_point_sources_subtracted=n_sub,
        n_negative_pixels_clipped=n_neg_pix,
        total_negative_deficit_clipped=neg_deficit,
        A_nan_mask=dict(
            f_gas=res_a["params"]["f_gas"]["median"], f_ics=res_a["params"]["f_ics"]["median"],
            f_halo=res_a["params"]["f_halo"]["median"], sig=res_a["significance_sigma"],
            n_valid_pixels=int(valid_a.sum()), convergence=diag(res_a),
        ),
        B_spectral_subtract_corrected=dict(
            f_gas=res_b["params"]["f_gas"]["median"], f_ics=res_b["params"]["f_ics"]["median"],
            f_halo=res_b["params"]["f_halo"]["median"], sig=res_b["significance_sigma"],
            n_valid_pixels=int(valid_b.sum()), convergence=diag(res_b),
        ),
    )


def main():
    np.random.seed(mfa.SEED)
    print("読み込み中...")
    expmaps, _ = mfa.load_exposure_maps()
    df_all = mfa.load_all_events()
    j_map = mfa.nfw_j_map()
    nfw_norm, _ = mfa.calibrate_nfw_norm(expmaps[5], j_map)
    bpos, bneg = mfa.build_bubble_counts_template(df_all)
    loop1, loop2 = _sub.loop_i_shell_templates()

    # 時間の制約上、まずBin6のみ。動作確認後に他ビンへ拡張可能。
    target_bins = [5]  # Bin6 (0-indexed)

    results = []
    for ib in target_bins:
        print(f"\n=== Bin{ib+1} ({mfa.BIN_CENTERS[ib]:.2f} GeV) ===")
        r = run_for_bin(ib, df_all, expmaps, j_map, nfw_norm, bpos, bneg, loop1, loop2)
        results.append(r)
        a, b = r["A_nan_mask"], r["B_spectral_subtract_corrected"]
        print(f"  点源{r['n_point_sources_subtracted']}個差し引き / "
              f"負カウントクリップ: {r['n_negative_pixels_clipped']}ピクセル "
              f"(合計{r['total_negative_deficit_clipped']:.1f}カウント分)")
        # [数値レビュー推奨] 収束不足(50tau未達)を踏まえ有効数字2-3桁に丸めて報告
        print(f"  (A)NaNマスク    : f_gas={a['f_gas']:.3g} f_ics={a['f_ics']:.3g} "
              f"f_halo={a['f_halo']:.3g} sig={a['sig']:.2f}sigma (n_pix={a['n_valid_pixels']}) "
              f"[50tau達成={a['convergence']['meets_50tau_recommendation']}]")
        print(f"  (B)スペクトル差引: f_gas={b['f_gas']:.3g} f_ics={b['f_ics']:.3g} "
              f"f_halo={b['f_halo']:.3g} sig={b['sig']:.2f}sigma (n_pix={b['n_valid_pixels']}) "
              f"[50tau達成={b['convergence']['meets_50tau_recommendation']}]")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(dict(
            description="点源処理: 現行headline(NaNマスク) vs 補正版(Totani式スペクトル"
                         "差し引き、実測露出反映)の比較。headlineファイルは上書きしていない。",
            results=results,
        ), f, indent=2, ensure_ascii=False)
    print(f"\n→ {OUT_PATH}")


if __name__ == "__main__":
    main()
