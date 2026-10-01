"""
2026-07-16: 領域A(フェルミバブル内)/C(バブル外高緯度)でf_haloを共有した場合の
尤度比検定(LRT)を全13ビンに拡張して実行する。

背景: .dev/teams/galprop-gas-ics-separation/verdict.md の「次の一手」①
「領域C(バブル除外)単独での全13ビンhaloフィット、またはA/C共有f_haloのLRT検定」を
実行する。既存の code/diagnose_halo_degeneracy_gasics_roi.py はBin5・Bin6のみで
領域A/C独立フィットを実行済みで、両領域ともf_haloが正だが振幅が大きく異なる
(Bin5: A=+8.64 vs C=+3.43、Bin6: A=+3.27 vs C=+1.23)。この振幅差が統計的揺らぎの
範囲内か、有意な空間不整合(球対称ハロー仮説への反証)かを、全13ビンでLRTにより
定量検定する。詳細は .dev/teams/regionAC-lrt-halo-test/spec.md 参照。

物理的背景: 真の球対称NFWハローなら、視線積分J値の方向依存性はテンプレート
(j_map)に折り込み済みなので、同じ物理的ハローなら領域A・Cで独立にフィットしても
同じf_halo(規格化係数)が出るはず。gas/ICS/Loop I/フェルミバブルの寄与は領域ごとに
独立でよい(背景成分の実効規格化は空間的にムラがあってもおかしくない)。共有を
強制すべきはf_haloのみ。

モデル1(制約なし=独立フィット): 領域Aと領域Cをそれぞれ独立に7パラメータフィット
  (既存 diagnose_halo_degeneracy_gasics_roi.refit() のMCMCなし点推定版と同じロジック)。
  lnL_unconstrained = lnL_A(θ_A*, f_halo_A*) + lnL_C(θ_C*, f_halo_C*) (自由パラメータ14=7x2)

モデル2(制約あり=f_halo共有): 領域A・Cの6背景パラメータは独立のまま、f_haloだけ
  共有した13パラメータ同時フィット。
  lnL_shared = max_{θ_A,θ_C,f_halo共有} [ lnL_A(θ_A,f_halo) + lnL_C(θ_C,f_halo) ]
  (自由パラメータ13)
  領域Aと領域Cのピクセル集合は排他的(valid=valid&BUBBLE_REGION vs
  valid&highlat&~BUBBLE_REGION)なので対数尤度は加法分解でき、
  mfa.neg_log_likelihood_and_grad() を領域ごとに呼んで値・勾配を単純加算する
  薄いラッパー(_joint_neg_ll_and_grad)で13次元⇔7次元x2のパラメータ組み替えのみ行う
  (テンプレート構築・valid mask・尤度計算そのものは再実装しない)。

LRT統計量:
  delta_lnL_LRT = lnL_unconstrained - lnL_shared  (>=0のはず、モデル2はモデル1の
    部分集合=f_halo_A=f_halo_Cという等式制約を課した入れ子モデルなので、その
    最大尤度は理論上モデル1のそれを超えられない)
  test_statistic = 2 * delta_lnL_LRT  (Wilks' theorem, 自由度1のchi2に漸近)
  p_value = scipy.stats.chi2.sf(test_statistic, df=1)
  equivalent_sigma = scipy.stats.norm.isf(p_value / 2)

[ASSUMPTION] MCMC事後分布は取得しない(spec.md §5: 必須ではない)。全結果は
L-BFGS-B多点始動によるMLE点推定。理由: 13ビン×2モデル(独立2領域+共有)の
点推定のみで合格条件(delta_lnL_LRT>=0の検証・収束診断)を満たせ、実行時間を
数分〜十数分に抑えられるため。JSON出力中の f_halo_A/f_halo_C は
(MCMC事後中央値ではなく)L-BFGS-B点推定値である旨を明記する。

[ASSUMPTION] 解釈("ハローは本物か縮退か")はこのスクリプトでは出さない
(spec.md 合格条件5)。数値のみ報告する。

標準出力は1-2行/ビンのサマリのみ(output-discipline遵守)。詳細ログは
results/mcmc_allbins_gasICS_v1/regionAC_lrt_all_bins.log に保存する。
結果本体は results/mcmc_allbins_gasICS_v1/regionAC_lrt_all_bins.json に保存する。

再現性: mfa.SEED=42 を np.random.seed() で固定する(MCMCは使わないため
乱数依存は multistart の初期点スケール選択のみだが、既存スクリプト群との
慣行を踏襲し明示的に固定する)。
"""
import json
import logging
import pathlib as _pathlib
import sys
import time
sys.path.insert(0, "code")
import warnings
warnings.filterwarnings("ignore")

from typing import Optional

import numpy as np
from numpy.typing import NDArray
from scipy import stats as _stats

import mcmc_fit_all_bins as mfa
import plot_skymap_all_subtracted as _sub

BASE = _pathlib.Path(__file__).resolve().parent.parent

# [2026-07-17] 出力先をコマンドライン引数(第1引数)または環境変数
# REGIONAC_LRT_OUTDIR で上書き可能にした(既定は従来通り gasICS_v1、後方互換)。
# DPIX_SR cos(b) 修正版の再検証を既存 v1 結果を上書きせず別ディレクトリ
# (results/mcmc_allbins_gasICS_v2_cosb/)に保存するため。テンプレート・尤度は
# import した mfa.* が cos(b) 修正を自動反映するので、本スクリプト自体のロジックは不変。
def _resolve_out_dir() -> _pathlib.Path:
    import os
    if len(sys.argv) > 1:
        return _pathlib.Path(sys.argv[1])
    env = os.environ.get("REGIONAC_LRT_OUTDIR")
    if env:
        return _pathlib.Path(env)
    return BASE / "results/mcmc_allbins_gasICS_v1"


OUT_DIR = _resolve_out_dir()
OUT_JSON = OUT_DIR / "regionAC_lrt_all_bins.json"
OUT_LOG = OUT_DIR / "regionAC_lrt_all_bins.log"

# 領域定義: 既存 diagnose_halo_degeneracy_gasics_roi.py / spec.md §1 と同一。
BUBBLE_REGION = (np.abs(_sub.L_GRID) < 22) & (np.abs(_sub.B_GRID) > 10) & (np.abs(_sub.B_GRID) < 55)

logger = logging.getLogger("regionAC_lrt")


def _region_x0(counts: NDArray[np.float64], valid: NDArray[np.bool_],
                t: mfa.TemplateDict) -> list[float]:
    """既存 diagnose_halo_degeneracy_gasics_roi.refit() と同じデータ駆動x0ヒューリスティック。"""
    c_mean = max(counts[valid].mean(), 1e-6)
    x0_gas = 0.5 * c_mean / max(t["gas"][valid].mean(), 1e-30)
    x0_ics = 0.5 * c_mean / max(t["ics"][valid].mean(), 1e-30)
    x0_la = 0.3 * c_mean / max(t["loopI_a"][valid].mean(), 1e-30)
    x0_lb = 0.3 * c_mean / max(t["loopI_b"][valid].mean(), 1e-30)
    x0_fbneg = 0.3 * c_mean / max(t["fb_neg"][valid].mean(), 1e-30) if t["fb_neg"][valid].mean() > 0 else 0.3
    return [x0_gas, x0_ics, x0_la, x0_lb, 0.5, x0_fbneg, 0.5]


def fit_region_independent(
    counts: NDArray[np.float64],
    valid: NDArray[np.bool_],
    t: mfa.TemplateDict,
) -> Optional[dict[str, object]]:
    """領域単独の7パラメータ独立フィット(点推定のみ、MCMCなし)。
    diagnose_halo_degeneracy_gasics_roi.refit()のMCMC呼び出し部分を省いたもの
    (spec.md §5: MCMCは必須ではない)。目的関数・勾配は
    mfa.neg_log_likelihood_and_grad() を再利用し、最適化は mfa._multistart_minimize()
    (L-BFGS-B多点始動)を再利用する(重複実装を避ける、spec.md 合格条件4)。

    戻り値: best(7次元パラメータ, PARAM_NAMES順), lnL(with-halo/no-haloの大きい方,
    with-haloがno-haloを下回った場合はno-halo解にf_halo=0を足したものにフォールバック
    することでΔlnL>=0を保証, mfa.fit_one_bin()と同じ安全策), 収束診断。
    """
    t_r = dict(t)
    t_r["valid"] = valid
    if valid.sum() < 20:
        return None
    x0 = _region_x0(counts, valid, t_r)

    def neg_ll_nohalo(p6):
        val, grad7 = mfa.neg_log_likelihood_and_grad(list(p6) + [0.0], counts, t_r)
        return val, grad7[:6]

    res_nh, diag_nh = mfa._multistart_minimize(neg_ll_nohalo, x0[:6], mfa._bounds_no_halo())
    lnL_noh = -res_nh.fun

    def neg_ll(p):
        return mfa.neg_log_likelihood_and_grad(p, counts, t_r)

    x0_with = list(res_nh.x) + [x0[6]]
    res, diag_wh = mfa._multistart_minimize(neg_ll, x0_with, mfa._bounds_with_halo())
    best = np.asarray(res.x, dtype=float)
    lnL_with = -res.fun
    if lnL_with < lnL_noh:
        best = np.array(list(res_nh.x) + [0.0])
        lnL_with = lnL_noh

    return dict(
        best_params=best, lnL=float(lnL_with), lnL_no_halo=float(lnL_noh),
        f_halo_pointest=float(best[6]),
        n_valid_pixels=int(valid.sum()), n_events=float(counts[valid].sum()),
        convexity_check=dict(no_halo=diag_nh, with_halo=diag_wh),
    )


def _joint_neg_ll_and_grad(
    p13: NDArray[np.float64],
    counts: NDArray[np.float64],
    t_a: mfa.TemplateDict,
    t_c: mfa.TemplateDict,
) -> tuple[float, NDArray[np.float64]]:
    """モデル2(f_halo共有13パラメータ)の目的関数・勾配。

    p13 = [gas_A,ics_A,loopIa_A,loopIb_A,fb_A,fbneg_A,
           gas_C,ics_C,loopIa_C,loopIb_C,fb_C,fbneg_C, halo_shared]
    (spec.md タスク節で指定された順序)。

    領域Aと領域C(t_a["valid"]/t_c["valid"])のピクセル集合は排他的
    (region_A = valid&BUBBLE_REGION, region_C = valid&highlat&~BUBBLE_REGION)なので、
    対数尤度は加法分解できる: lnL_shared = lnL_A(θ_A,halo) + lnL_C(θ_C,halo)。
    既存の mfa.neg_log_likelihood_and_grad() を7次元領域別ベクトルに組み替えて
    領域ごとに呼び出し、値は単純加算、共有パラメータhaloの勾配は両領域からの
    寄与の和に再分配する(chain ruleの帰結: dNLL/dhalo = dNLL_A/dhalo + dNLL_C/dhalo)。
    """
    p_a = np.concatenate([p13[0:6], p13[12:13]])
    p_c = np.concatenate([p13[6:12], p13[12:13]])
    val_a, grad_a = mfa.neg_log_likelihood_and_grad(p_a, counts, t_a)
    val_c, grad_c = mfa.neg_log_likelihood_and_grad(p_c, counts, t_c)
    val = val_a + val_c
    grad13 = np.zeros(13)
    grad13[0:6] = grad_a[0:6]
    grad13[6:12] = grad_c[0:6]
    grad13[12] = grad_a[6] + grad_c[6]
    return val, grad13


def fit_shared_halo(
    counts: NDArray[np.float64],
    region_a: NDArray[np.bool_],
    region_c: NDArray[np.bool_],
    t: mfa.TemplateDict,
    fit_a: dict[str, object],
    fit_c: dict[str, object],
) -> dict[str, object]:
    """モデル2(13パラメータ、f_halo共有)の同時フィット。

    x0は領域独立フィット(fit_a/fit_c)の6背景パラメータ点推定をそのまま使い、
    共有halo初期値だけ2通り試す(領域A独立推定値、領域C独立推定値)。これは
    L-BFGS-Bが凸問題でも数値的に初期点依存の早期停止をしうるため、
    delta_lnL_LRT>=0(理論的制約、spec.md合格条件2)を安定して満たすための
    追加の頑健化(既存mfa._multistart_minimizeの5スケールmultistartに、
    共有haloパラメータのみ2通りの独立候補を追加した二重multistart)。
    """
    t_a = dict(t)
    t_a["valid"] = region_a
    t_c = dict(t)
    t_c["valid"] = region_c

    bounds13 = mfa._bounds_no_halo() + mfa._bounds_no_halo() + [(0.0, None)]

    best_a = np.asarray(fit_a["best_params"], dtype=float)
    best_c = np.asarray(fit_c["best_params"], dtype=float)
    halo_candidates = sorted({round(float(best_a[6]), 12), round(float(best_c[6]), 12), 0.5})

    all_results = []
    all_diags = []
    for halo0 in halo_candidates:
        x0_13 = np.concatenate([best_a[:6], best_c[:6], [halo0]])

        def neg_ll(p, _t_a=t_a, _t_c=t_c):
            return _joint_neg_ll_and_grad(p, counts, _t_a, _t_c)

        res13, diag13 = mfa._multistart_minimize(neg_ll, x0_13, bounds13)
        all_results.append(res13)
        all_diags.append(diag13)

    best_res = min(all_results, key=lambda r: r.fun)
    lnL_shared = -best_res.fun

    # 複数halo候補にわたるfun_spread(収束の頑健性診断、既存_multistart_minimizeの
    # fun_spread_successful_only と同じ思想で候補間のばらつきも記録する)。
    fun_values_all = [float(r.fun) for r in all_results]
    success_all = [bool(r.success) for r in all_results]
    successful_fun = [f for f, s in zip(fun_values_all, success_all) if s]
    fun_spread_across_halo0 = (float(max(successful_fun) - min(successful_fun))
                                if successful_fun else None)

    return dict(
        best_params_13=best_res.x.tolist(), lnL_shared=float(lnL_shared),
        f_halo_shared_pointest=float(best_res.x[12]),
        halo0_candidates=halo_candidates,
        convexity_check_per_halo0=all_diags,
        fun_spread_across_halo0_candidates=fun_spread_across_halo0,
    )


def process_bin(
    ib: int,
    df_all,
    expmaps: NDArray[np.float64],
    j_map: NDArray[np.float64],
    nfw_norm: float,
    bpos: NDArray[np.float64],
    bneg: NDArray[np.float64],
    loop1: NDArray[np.float64],
    loop2: NDArray[np.float64],
) -> dict[str, object]:
    t0 = time.time()
    emin, emax = mfa.BIN_EDGES[ib], mfa.BIN_EDGES[ib + 1]
    sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
    counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
    masked, n_masked = _sub.mask_point_sources(counts.copy())
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
    region_a = valid & BUBBLE_REGION
    region_c = valid & highlat & ~BUBBLE_REGION

    fit_a = fit_region_independent(counts, region_a, t)
    fit_c = fit_region_independent(counts, region_c, t)
    if fit_a is None or fit_c is None:
        return dict(bin=ib + 1, e_center_gev=float(mfa.BIN_CENTERS[ib]),
                     error="領域A/Cいずれかの有効ピクセル数が20未満(valid.sum()<20)",
                     n_valid_pixels_A=(int(region_a.sum())),
                     n_valid_pixels_C=(int(region_c.sum())))

    lnL_unconstrained = fit_a["lnL"] + fit_c["lnL"]

    shared = fit_shared_halo(counts, region_a, region_c, t, fit_a, fit_c)
    lnL_shared = shared["lnL_shared"]

    delta_lnL_lrt = lnL_unconstrained - lnL_shared
    test_statistic = 2.0 * delta_lnL_lrt
    p_value = float(_stats.chi2.sf(max(test_statistic, 0.0), df=1))
    equivalent_sigma = float(_stats.norm.isf(p_value / 2.0)) if p_value > 0 else float("inf")

    # 収束診断: 各領域independent fit(with-halo段階)のfun_spread + 共有フィットの
    # 複数halo候補間fun_spreadのうち最大値を「このビンの収束の質」として報告する。
    spreads = [
        fit_a["convexity_check"]["with_halo"]["fun_spread_successful_only"],
        fit_c["convexity_check"]["with_halo"]["fun_spread_successful_only"],
    ]
    for d in shared["convexity_check_per_halo0"]:
        spreads.append(d["fun_spread_successful_only"])
    spreads_valid = [s for s in spreads if s is not None]
    fun_spread_max = float(max(spreads_valid)) if spreads_valid else None

    elapsed = time.time() - t0
    result = dict(
        bin=ib + 1, e_center_gev=float(mfa.BIN_CENTERS[ib]),
        n_masked_point_sources=int(n_masked),
        n_valid_pixels_A=fit_a["n_valid_pixels"], n_valid_pixels_C=fit_c["n_valid_pixels"],
        n_events_A=fit_a["n_events"], n_events_C=fit_c["n_events"],
        f_halo_A_pointest=fit_a["f_halo_pointest"], f_halo_C_pointest=fit_c["f_halo_pointest"],
        f_halo_shared_pointest=shared["f_halo_shared_pointest"],
        lnL_A_independent=fit_a["lnL"], lnL_C_independent=fit_c["lnL"],
        lnL_unconstrained=float(lnL_unconstrained), lnL_shared=float(lnL_shared),
        delta_lnL_LRT=float(delta_lnL_lrt), test_statistic=float(test_statistic),
        p_value=p_value, equivalent_sigma=equivalent_sigma,
        fun_spread_max=fun_spread_max,
        convergence_flag_ok=bool(fun_spread_max is not None and fun_spread_max < 1e-6),
        delta_lnL_nonneg_ok=bool(delta_lnL_lrt >= 0),
        region_A_fit_detail=dict(
            best_params=fit_a["best_params"].tolist(), lnL_no_halo=fit_a["lnL_no_halo"],
            convexity_check=fit_a["convexity_check"],
        ),
        region_C_fit_detail=dict(
            best_params=fit_c["best_params"].tolist(), lnL_no_halo=fit_c["lnL_no_halo"],
            convexity_check=fit_c["convexity_check"],
        ),
        model2_shared_fit_detail=shared,
        elapsed_sec=float(elapsed),
    )
    return result


def main() -> None:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(message)s",
        handlers=[logging.FileHandler(OUT_LOG, mode="w"), logging.StreamHandler(sys.stdout)],
    )

    np.random.seed(mfa.SEED)
    logger.info(f"再現性シード固定: np.random.seed({mfa.SEED})")
    logger.info("露出マップ・イベント読み込み中...")
    expmaps, _ = mfa.load_exposure_maps()
    df_all = mfa.load_all_events()
    logger.info("NFW J-map計算中...")
    j_map = mfa.nfw_j_map()
    nfw_norm, calib = mfa.calibrate_nfw_norm(expmaps[5], j_map)
    logger.info("バブル・Loop Iテンプレート構築中...")
    bpos, bneg = mfa.build_bubble_counts_template(df_all)
    loop1, loop2 = _sub.loop_i_shell_templates()

    bins_out = []
    for ib in range(mfa.N_BINS):
        r = process_bin(ib, df_all, expmaps, j_map, nfw_norm, bpos, bneg, loop1, loop2)
        bins_out.append(r)
        if "error" in r:
            logger.info(f"Bin{r['bin']} ({mfa.BIN_CENTERS[ib]:.2f} GeV): SKIPPED ({r['error']})")
            continue
        logger.info(
            f"Bin{r['bin']} ({r['e_center_gev']:.2f} GeV): "
            f"f_halo_A={r['f_halo_A_pointest']:+.4g} f_halo_C={r['f_halo_C_pointest']:+.4g} "
            f"f_halo_shared={r['f_halo_shared_pointest']:+.4g} "
            f"LRT={r['test_statistic']:.4g} p={r['p_value']:.3e} "
            f"equiv_sigma={r['equivalent_sigma']:.2f} "
            f"fun_spread_max={r['fun_spread_max']:.2e} "
            f"delta_lnL_ok={r['delta_lnL_nonneg_ok']} ({r['elapsed_sec']:.1f}s)"
        )

    n_bins_ok = sum(1 for r in bins_out if r.get("delta_lnL_nonneg_ok") is True)
    n_bins_converged = sum(1 for r in bins_out if r.get("convergence_flag_ok") is True)
    n_bins_fit = sum(1 for r in bins_out if "error" not in r)

    summary = dict(
        description=(
            "領域A(フェルミバブル内)/C(バブル外高緯度)でf_haloを共有した場合の"
            "尤度比検定(LRT)、全13ビン。モデル1=領域A/C独立7パラメータフィット、"
            "モデル2=6背景パラメータは領域独立・f_haloのみ共有した13パラメータ同時フィット。"
            "MCMC事後分布は取得していない(L-BFGS-B多点始動によるMLE点推定のみ、"
            "spec.md §5により必須ではないため省略)。f_halo_A/f_halo_C/f_halo_sharedは"
            "MCMC事後中央値ではなくL-BFGS-B点推定値である。解釈("
            "球対称ハロー仮説と整合的か否か)はこのスクリプトでは行わず、数値のみ報告する。"
        ),
        region_definition=dict(
            BUBBLE_REGION="(|L_GRID|<22) & (10<|B_GRID|<55)",
            region_A="valid & BUBBLE_REGION",
            region_C="valid & (|BG|>=30) & ~BUBBLE_REGION",
        ),
        reproducibility_seed=mfa.SEED,
        environment=mfa.env_stamp(),
        pixel_solid_angle_note=(
            "[2026-07-17] テンプレートは mfa.build_templates_for_bin 経由で "
            "cos(b) 込みのピクセル立体角 PIX_SOLID_ANGLE_SR を使用(DPIX_SR cos(b) 修正版)。"
        ),
        mcmc_omitted=True,
        n_bins_total=mfa.N_BINS,
        n_bins_fit=n_bins_fit,
        n_bins_delta_lnL_LRT_nonneg=n_bins_ok,
        n_bins_convergence_ok_fun_spread_below_1em6=n_bins_converged,
        nfw_calibration=calib,
        bins=bins_out,
    )
    with open(OUT_JSON, "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    logger.info(f"→ {OUT_JSON}")
    logger.info(
        f"完了: {n_bins_fit}/{mfa.N_BINS}ビンでフィット成功、"
        f"delta_lnL_LRT>=0が{n_bins_ok}/{n_bins_fit}ビンで成立、"
        f"fun_spread<1e-6が{n_bins_converged}/{n_bins_fit}ビンで成立。"
    )


if __name__ == "__main__":
    main()
