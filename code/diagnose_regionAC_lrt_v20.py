"""2026-09-28: 領域A(フェルミバブル内)/C(バブル外高緯度)でf_haloを共有した場合の
尤度比検定(LRT)を **v20 仕様** で全13ビンに対して実行する。

目的: v20 の halo 検出 (Bin6 19.1σ) が真の球対称 NFW ハローか、フェルミバブル/
GALPROP 拡散残差との空間縮退アーティファクトかを切り分ける。真の球対称ハローなら
視線積分 J の方向依存は j_map に折り込み済みなので、領域 A・C で独立にフィットしても
同じ f_halo が出るはず。有意に違えば球対称仮説への反証になる。

既存 code/diagnose_regionAC_lrt_all_bins.py (2026-07-16) を v20 仕様に作り直したもの。
旧版は当時の 7 パラメータ・1°ピクセル・点源 NaN マスク版に固定されており、v20 の
環境変数を与えても動かない(パラメータ数 7 vs 9、bounds 長不一致で L-BFGS-B が失敗)。
旧版は当時の結果の再現性記録として残し、本ファイルを新規に置く。

v20 からの継承(すべて mfa 経由で自動反映):
  - 9 パラメータ [f_iso, f_gas, f_ics, f_ps, f_loopI_a, f_loopI_b, f_fb, f_fb_neg, f_halo]
  - 点源は NaN マスクではなく f_ps 自由成分、除外は拡張源のみ (TOTANI_SPEC §3.1/§3.2)
  - f_halo 符号自由 (MCMC_SIGNFREE_HALO=1)
  - 10°セル束ね Poisson 尤度 (MCMC_CELL_LIKELIHOOD=1, Totani §2.2)
  - 0.125° ピクセル / UltraClean / disk 込みバブル構築

[ASSUMPTION] CELL_MODE では領域分割を**セル単位**で行う(ピクセル単位ではない)。
理由: v20 の尤度は 10°×10° セル単位であり、1 セルが領域 A と C にまたがると対数尤度の
加法分解 lnL = lnL_A + lnL_C が厳密に成り立たなくなる(同じセルが両モデルで二重計上
される)。セル中心が矩形 |l|<22°, 10°<|b|<55° の内側にあるセルを領域 A とする。
結果として実効的な領域 A は |l|<20°, 10°<|b|<50° (4列×8行=32セル) となり、名目の矩形
とわずかに異なる。領域 C は |b_center|>=30° かつ A でないセル (56セル)。この近似は
JSON の region_definition に明記する。

[ASSUMPTION] MCMC 事後分布は取得しない。全て L-BFGS-B 多点始動による MLE 点推定
(旧版 spec.md §5 と同じ判断。LRT の合格条件は点推定で満たせ、実行時間を抑えられる)。

LRT:
  delta_lnL = lnL_unconstrained - lnL_shared  (>=0 のはず。共有モデルは入れ子)
  test_statistic = 2*delta_lnL ~ chi2(df=1) (Wilks)
  equivalent_sigma = norm.isf(p/2)

実行 (v20 環境変数必須、単一プロセスで順次実行すること):
  MCMC_ULTRACLEAN=1 MCMC_PIXEL_DEG=0.125 MCMC_DISK_BUBBLE=1 \
  MCMC_CELL_LIKELIHOOD=1 MCMC_SIGNFREE_HALO=1 \
  REGIONAC_V20_OUTDIR=results/regionAC_lrt_v20 python code/diagnose_regionAC_lrt_v20.py
"""
import gc
import json
import logging
import os
import pathlib as _pathlib
import sys
import time
import warnings

warnings.filterwarnings("ignore")
sys.path.insert(0, "code")

from typing import Optional

import numpy as np
import pandas as pd
from numpy.typing import NDArray
from scipy import stats as _stats

import mcmc_fit_all_bins as mfa
import plot_skymap_all_subtracted as _sub

# 本スクリプトで使う列だけ読む。mfa.load_all_events()/load_events_with_disk() は
# CSV の全7列を読むが、本スクリプトが使うのは 3 列だけで、本機 (RAM 5.9 GB) では
# 全列読みが OOM で落ちる (halo CSV 312 MB を2回 + disk CSV 671 MB を同時保持するため。
# 2026-09-28 に実測でプロセスが無言で kill されることを確認)。列を絞っても値は同一。
_EVENT_COLS = ["energy_GeV", "l_deg", "b_deg"]

BASE = _pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = _pathlib.Path(
    sys.argv[1] if len(sys.argv) > 1
    else os.environ.get("REGIONAC_V20_OUTDIR", str(BASE / "results/regionAC_lrt_v20"))
)
OUT_JSON = OUT_DIR / "regionAC_lrt_v20.json"
OUT_LOG = OUT_DIR / "regionAC_lrt_v20.log"

# 背景パラメータ数 (f_halo を除く)。ICS_SPLIT 等で次元が変わっても追従する。
NB = mfa.NDIM - 1

# 名目のバブル矩形 (Totani §3.1 の平坦テンプレ境界と同一)。
BUBBLE_L_MAX, BUBBLE_B_MIN, BUBBLE_B_MAX = 22.0, 10.0, 55.0

# 領域 C (バブル外) の銀緯下限。既定 30° は 2026-07-16 の旧検定と同じ定義。
# REGIONAC_C_BMIN=10 にすると「バブル以外の有効 ROI 全部」になり、A ∪ C が v20 本体の
# ROI と一致する。背景共有 LRT ではこちらが本命 (背景が v20 と同じデータで拘束され、
# 帰無仮説 = halo 共通が v20 主結果の点推定そのものになる)。
REGION_C_B_MIN = float(os.environ.get("REGIONAC_C_BMIN", "30"))

logger = logging.getLogger("regionAC_v20")


def _read_events(csv_name: str, skip_bad: bool = False) -> pd.DataFrame:
    return pd.read_csv(
        mfa.BASE / "data/CSV" / csv_name, comment="#", usecols=_EVENT_COLS,
        **({"on_bad_lines": "skip"} if skip_bad else {}),
    )


def load_all_events_lean() -> pd.DataFrame:
    """mfa.load_all_events() と同一の選別 (|b| in [10,60], |l|<=60) を 3 列だけで行う。"""
    df = _read_events(mfa._HALO_CSV)
    return df[(df.b_deg.abs() >= 10) & (df.b_deg.abs() <= 60) & (df.l_deg.abs() <= 60)]


def load_events_with_disk_lean() -> pd.DataFrame:
    """mfa.load_events_with_disk() と同一の選別 (|b|<=60, |l|<=60) を 3 列だけで行う。"""
    hi = _read_events(mfa._HALO_CSV)
    disk = _read_events(mfa._DISK_CSV, skip_bad=True)
    both = pd.concat([hi, disk], ignore_index=True)
    del hi, disk
    return both[(both.b_deg.abs() <= 60) & (both.l_deg.abs() <= 60)]


def _cell_centers() -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """セル ID (= il*12 + ib) ごとの中心 (l, b) [deg]。mfa.build_cell_index() と同じ規約。"""
    ids = np.arange(mfa.N_CELLS)
    il = ids // mfa.N_CELLS_1D
    ib = ids % mfa.N_CELLS_1D
    l_c = -60.0 + mfa.CELL_DEG * il + mfa.CELL_DEG / 2.0
    b_c = -60.0 + mfa.CELL_DEG * ib + mfa.CELL_DEG / 2.0
    return l_c, b_c


def region_masks(valid_ll: NDArray[np.bool_]) -> tuple[NDArray[np.bool_], NDArray[np.bool_]]:
    """尤度グリッド(CELL_MODE ならセル、でなければピクセル)上の領域 A/C マスク。

    A = バブル矩形の内側、C = |b|>=30° かつ A の外側。両者は排他的なので
    lnL = lnL_A + lnL_C が厳密に成り立つ。
    """
    if mfa.CELL_MODE:
        l_c, b_c = _cell_centers()
    else:
        l_c, b_c = mfa.LG, mfa.BG
    in_bubble = (
        (np.abs(l_c) < BUBBLE_L_MAX)
        & (np.abs(b_c) > BUBBLE_B_MIN)
        & (np.abs(b_c) < BUBBLE_B_MAX)
    )
    region_a = valid_ll & in_bubble
    region_c = valid_ll & (np.abs(b_c) >= REGION_C_B_MIN) & ~in_bubble
    return region_a, region_c


def _x0_v20(ib: int, expmap_i: NDArray[np.float64], emin: float, emax: float) -> list[float]:
    """v20 (mfa.main) と同一の初期値。Totani §2.3 末尾の初期値規定。

    点源・GALPROP(gas/ICS) は元の規格化 = 1、等方は E²dN/dE = 1e-4 MeV cm⁻² s⁻¹ sr⁻¹
    相当、その他 (Loop I・バブル正負・halo) は 0。
    """
    de_mev = (emax - emin) * 1000.0
    unit_mean = float((expmap_i * mfa.PIX_SOLID_ANGLE_SR * de_mev).mean())
    f_iso0 = 1e-4 * unit_mean / (mfa.BIN_CENTERS[ib] ** 2 * 1e6)

    def one(name: str) -> float:
        if name == "f_iso":
            return f_iso0
        if name == "f_gas" or name.startswith("f_ics") or name == "f_ps":
            return 1.0
        return 0.0

    return [one(n) for n in mfa.PARAM_NAMES]


def fit_region_independent(
    counts_ll: NDArray[np.float64],
    region: NDArray[np.bool_],
    t_ll: mfa.TemplateDict,
    x0: list[float],
) -> Optional[dict[str, object]]:
    """モデル1の片側: 領域単独の NDIM パラメータ独立フィット(点推定のみ)。

    mfa.fit_one_bin() と同じ二段構え(no-halo で温めてから with-halo)。with-halo が
    no-halo を下回った場合は no-halo 解 + f_halo=0 にフォールバックし ΔlnL>=0 を保証する。
    """
    if region.sum() < 5:
        return None
    t_r = dict(t_ll)
    t_r["valid"] = region

    def neg_ll_nohalo(p_bg):
        val, grad = mfa.neg_log_likelihood_and_grad(list(p_bg) + [0.0], counts_ll, t_r)
        return val, grad[:NB]

    res_nh, diag_nh = mfa._multistart_minimize(neg_ll_nohalo, x0[:NB], mfa._bounds_no_halo())
    lnL_noh = -res_nh.fun

    def neg_ll(p):
        return mfa.neg_log_likelihood_and_grad(p, counts_ll, t_r)

    x0_with = list(res_nh.x) + [x0[NB]]
    res, diag_wh = mfa._multistart_minimize(neg_ll, x0_with, mfa._bounds_with_halo())
    best = np.asarray(res.x, dtype=float)
    lnL_with = -res.fun
    if lnL_with < lnL_noh:
        best = np.array(list(res_nh.x) + [0.0])
        lnL_with = lnL_noh

    return dict(
        best_params=best,
        lnL=float(lnL_with),
        lnL_no_halo=float(lnL_noh),
        f_halo_pointest=float(best[NB]),
        delta_lnL_halo=float(lnL_with - lnL_noh),
        n_valid_units=int(region.sum()),
        n_events=float(counts_ll[region].sum()),
        convexity_check=dict(no_halo=diag_nh, with_halo=diag_wh),
    )


def _joint_neg_ll_and_grad(
    p_joint: NDArray[np.float64],
    counts_ll: NDArray[np.float64],
    t_a: mfa.TemplateDict,
    t_c: mfa.TemplateDict,
) -> tuple[float, NDArray[np.float64]]:
    """モデル2 (f_halo 共有、次元 2*NB+1) の目的関数・勾配。

    p_joint = [bg_A (NB個), bg_C (NB個), f_halo_shared]
    領域 A と C は排他的なので lnL = lnL_A + lnL_C。共有 halo の勾配は両領域の和
    (chain rule: dNLL/dhalo = dNLL_A/dhalo + dNLL_C/dhalo)。
    """
    p_a = np.concatenate([p_joint[0:NB], p_joint[2 * NB:2 * NB + 1]])
    p_c = np.concatenate([p_joint[NB:2 * NB], p_joint[2 * NB:2 * NB + 1]])
    val_a, grad_a = mfa.neg_log_likelihood_and_grad(p_a, counts_ll, t_a)
    val_c, grad_c = mfa.neg_log_likelihood_and_grad(p_c, counts_ll, t_c)
    grad = np.zeros(2 * NB + 1)
    grad[0:NB] = grad_a[:NB]
    grad[NB:2 * NB] = grad_c[:NB]
    grad[2 * NB] = grad_a[NB] + grad_c[NB]
    return val_a + val_c, grad


def fit_shared_halo(
    counts_ll: NDArray[np.float64],
    region_a: NDArray[np.bool_],
    region_c: NDArray[np.bool_],
    t_ll: mfa.TemplateDict,
    fit_a: dict[str, object],
    fit_c: dict[str, object],
) -> dict[str, object]:
    """モデル2 の同時フィット。共有 halo の初期値を 3 通り試す二重 multistart。"""
    t_a = dict(t_ll)
    t_a["valid"] = region_a
    t_c = dict(t_ll)
    t_c["valid"] = region_c

    halo_bound = mfa._bounds_with_halo()[-1]
    bounds = mfa._bounds_no_halo() + mfa._bounds_no_halo() + [halo_bound]

    best_a = np.asarray(fit_a["best_params"], dtype=float)
    best_c = np.asarray(fit_c["best_params"], dtype=float)
    halo0_candidates = sorted({
        round(float(best_a[NB]), 12),
        round(float(best_c[NB]), 12),
        0.0,
    })

    results, diags = [], []
    for halo0 in halo0_candidates:
        x0_joint = np.concatenate([best_a[:NB], best_c[:NB], [halo0]])

        def neg_ll(p, _ta=t_a, _tc=t_c):
            return _joint_neg_ll_and_grad(p, counts_ll, _ta, _tc)

        res, diag = mfa._multistart_minimize(neg_ll, x0_joint, bounds)
        results.append(res)
        diags.append(diag)

    best_res = min(results, key=lambda r: r.fun)
    successful = [float(r.fun) for r in results if r.success]
    spread = float(max(successful) - min(successful)) if successful else None

    return dict(
        best_params_joint=best_res.x.tolist(),
        lnL_shared=float(-best_res.fun),
        f_halo_shared_pointest=float(best_res.x[2 * NB]),
        halo0_candidates=halo0_candidates,
        convexity_check_per_halo0=diags,
        fun_spread_across_halo0_candidates=spread,
    )


def _shared_bg_neg_ll_and_grad(
    p: NDArray[np.float64],
    counts_ll: NDArray[np.float64],
    t_a: mfa.TemplateDict,
    t_c: mfa.TemplateDict,
    split_halo: bool,
) -> tuple[float, NDArray[np.float64]]:
    """背景共有モデルの目的関数・勾配。

    split_halo=True  (対立仮説): p = [bg (NB個), halo_A, halo_C]  → 次元 NB+2
    split_halo=False (帰無仮説): p = [bg (NB個), halo]            → 次元 NB+1

    背景 NB 個 (f_iso/f_gas/f_ics/f_ps/Loop I/バブル正負) は領域 A・C で共有する。
    これらは全 ROI 共通の規格化補正であり、Totani baseline も ROI 全体で 1 つの値を
    フィットするため、領域ごとに自由化するのは baseline から乖離する。かつ領域 C
    (|b|>=30、バブル外) 単独では ICS と NFW halo の緯度形状がほぼ同形で分離できず、
    背景を領域ごと自由にすると f_ics が 0 に潰れて halo がその分を肩代わりする
    (2026-09-28 実測: Bin5-7 の領域 C で f_ics=0、f_halo が領域 A の約3倍)。
    背景を共有すると f_ics は領域 A に含まれる低緯度データで拘束され縮退が破れる。
    """
    halo_a = p[NB]
    halo_c = p[NB + 1] if split_halo else p[NB]
    p_a = np.concatenate([p[:NB], [halo_a]])
    p_c = np.concatenate([p[:NB], [halo_c]])
    val_a, grad_a = mfa.neg_log_likelihood_and_grad(p_a, counts_ll, t_a)
    val_c, grad_c = mfa.neg_log_likelihood_and_grad(p_c, counts_ll, t_c)
    grad = np.zeros(NB + 2 if split_halo else NB + 1)
    grad[:NB] = grad_a[:NB] + grad_c[:NB]
    if split_halo:
        grad[NB] = grad_a[NB]
        grad[NB + 1] = grad_c[NB]
    else:
        grad[NB] = grad_a[NB] + grad_c[NB]
    return val_a + val_c, grad


def fit_shared_background_lrt(
    counts_ll: NDArray[np.float64],
    region_a: NDArray[np.bool_],
    region_c: NDArray[np.bool_],
    t_ll: mfa.TemplateDict,
    x0: list[float],
) -> dict[str, object]:
    """背景共有 LRT: 「背景が共通なら halo も領域 A・C で共通か」を検定する。

    帰無 (halo 共通、次元 NB+1) vs 対立 (halo を領域別、次元 NB+2)、df=1。
    本スクリプト本来の問い「真の球対称 NFW ハローなら領域間で f_halo は一致するはず」に
    対する、ICS-halo 縮退に汚染されにくい版。
    """
    t_a = dict(t_ll)
    t_a["valid"] = region_a
    t_c = dict(t_ll)
    t_c["valid"] = region_c
    halo_bound = mfa._bounds_with_halo()[-1]
    bg_bounds = mfa._bounds_no_halo()

    def _run(split_halo: bool, x0_vec):
        def f(p):
            return _shared_bg_neg_ll_and_grad(p, counts_ll, t_a, t_c, split_halo)
        bounds = bg_bounds + ([halo_bound, halo_bound] if split_halo else [halo_bound])
        return mfa._multistart_minimize(f, x0_vec, bounds)

    res_null, diag_null = _run(False, list(x0[:NB]) + [x0[NB]])
    x0_alt = list(res_null.x[:NB]) + [float(res_null.x[NB])] * 2
    res_alt, diag_alt = _run(True, x0_alt)

    # 各領域の halo を 0 に固定した入れ子モデル。「その領域単独で halo が有意か」を測る
    # (背景は共有のまま = 全 ROI で拘束されるので ICS-halo 縮退に汚染されにくい)。
    # L-BFGS-B は下限=上限の bounds を固定値として扱う。
    def _run_fixed_zero(which: str):
        def f(p):
            return _shared_bg_neg_ll_and_grad(p, counts_ll, t_a, t_c, True)
        b = bg_bounds + ([(0.0, 0.0), halo_bound] if which == "A"
                         else [halo_bound, (0.0, 0.0)])
        x = list(res_alt.x)
        x[NB if which == "A" else NB + 1] = 0.0
        return mfa._multistart_minimize(f, x, b)

    def _sig_from(lnL_free: float, lnL_fixed: float) -> tuple[float, float]:
        ts_ = 2.0 * max(lnL_free - lnL_fixed, 0.0)
        p_ = float(_stats.chi2.sf(ts_, df=1))
        return ts_, (float(_stats.norm.isf(p_ / 2.0)) if p_ > 0 else float("inf"))

    res_a0, diag_a0 = _run_fixed_zero("A")
    res_c0, diag_c0 = _run_fixed_zero("C")
    ts_a, sig_a = _sig_from(-res_alt.fun, -res_a0.fun)
    ts_c, sig_c = _sig_from(-res_alt.fun, -res_c0.fun)

    lnL_null, lnL_alt = -res_null.fun, -res_alt.fun
    if lnL_alt < lnL_null:  # 入れ子モデルなので理論上ありえない。数値的保険。
        lnL_alt = lnL_null
    delta = lnL_alt - lnL_null
    ts = 2.0 * delta
    p_value = float(_stats.chi2.sf(max(ts, 0.0), df=1))
    equiv = float(_stats.norm.isf(p_value / 2.0)) if p_value > 0 else float("inf")
    spreads = [d["fun_spread_successful_only"] for d in (diag_null, diag_alt)
               if d["fun_spread_successful_only"] is not None]

    return dict(
        f_halo_A=float(res_alt.x[NB]), f_halo_C=float(res_alt.x[NB + 1]),
        f_halo_common=float(res_null.x[NB]),
        shared_background_null={n: float(v) for n, v in zip(mfa.PARAM_NAMES[:NB], res_null.x[:NB])},
        shared_background_alt={n: float(v) for n, v in zip(mfa.PARAM_NAMES[:NB], res_alt.x[:NB])},
        lnL_null=float(lnL_null), lnL_alt=float(lnL_alt),
        delta_lnL_LRT=float(delta), test_statistic=float(ts),
        p_value=p_value, equivalent_sigma=equiv,
        halo_detection=dict(
            sigma_halo_A=sig_a, sigma_halo_C=sig_c,
            test_statistic_A=ts_a, test_statistic_C=ts_c,
            fun_spread_A0=diag_a0["fun_spread_successful_only"],
            fun_spread_C0=diag_c0["fun_spread_successful_only"],
        ),
        fun_spread_max=float(max(spreads)) if spreads else None,
        convexity_check=dict(null=diag_null, alt=diag_alt),
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

    # v20 と同一の valid: 点源はマスクせず f_ps でフィット、拡張源のみ除外。
    valid = ~np.isnan(counts) & ~_sub.extended_source_mask()
    valid &= (np.abs(mfa.BG) >= mfa.B_MIN_DEG) & (np.abs(mfa.BG) <= 60)

    gas_flux, ics_flux = _sub._load_galprop_gas_ics_templates(emin, emax)
    ics_comp = _sub._load_healpix_ics_components(emin, emax) if mfa.ICS_SPLIT else None
    t = mfa.build_templates_for_bin(
        ib, counts, expmaps[ib], gas_flux, ics_flux,
        bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
        expmap_bubble_bin=expmaps[mfa.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
        loop_shell1=loop1, loop_shell2=loop2, ics_components=ics_comp,
    )
    t["valid"] = valid
    t["valid_pixel"] = valid
    t["counts_total"] = int(counts.sum())

    if mfa.CELL_MODE:
        counts_ll, t_ll = mfa.cellize_counts_and_templates(counts, t, valid)
    else:
        counts_ll, t_ll = counts, t

    region_a, region_c = region_masks(np.asarray(t_ll["valid"], dtype=bool))
    x0 = _x0_v20(ib, expmaps[ib], emin, emax)

    fit_a = fit_region_independent(counts_ll, region_a, t_ll, x0)
    fit_c = fit_region_independent(counts_ll, region_c, t_ll, x0)
    if fit_a is None or fit_c is None:
        return dict(
            bin=ib + 1, e_center_gev=float(mfa.BIN_CENTERS[ib]),
            error="領域A/Cいずれかの有効単位数が5未満",
            n_units_A=int(region_a.sum()), n_units_C=int(region_c.sum()),
        )

    lnL_unconstrained = fit_a["lnL"] + fit_c["lnL"]
    shared = fit_shared_halo(counts_ll, region_a, region_c, t_ll, fit_a, fit_c)
    shared_bg = fit_shared_background_lrt(counts_ll, region_a, region_c, t_ll, x0)
    delta_lnL = lnL_unconstrained - shared["lnL_shared"]
    test_statistic = 2.0 * delta_lnL
    p_value = float(_stats.chi2.sf(max(test_statistic, 0.0), df=1))
    equiv_sigma = float(_stats.norm.isf(p_value / 2.0)) if p_value > 0 else float("inf")

    spreads = [
        fit_a["convexity_check"]["with_halo"]["fun_spread_successful_only"],
        fit_c["convexity_check"]["with_halo"]["fun_spread_successful_only"],
    ]
    spreads += [d["fun_spread_successful_only"] for d in shared["convexity_check_per_halo0"]]
    spreads = [s for s in spreads if s is not None]
    fun_spread_max = float(max(spreads)) if spreads else None

    return dict(
        bin=ib + 1, e_center_gev=float(mfa.BIN_CENTERS[ib]),
        n_units_A=fit_a["n_valid_units"], n_units_C=fit_c["n_valid_units"],
        n_events_A=fit_a["n_events"], n_events_C=fit_c["n_events"],
        f_halo_A_pointest=fit_a["f_halo_pointest"],
        f_halo_C_pointest=fit_c["f_halo_pointest"],
        f_halo_shared_pointest=shared["f_halo_shared_pointest"],
        delta_lnL_halo_A=fit_a["delta_lnL_halo"], delta_lnL_halo_C=fit_c["delta_lnL_halo"],
        lnL_A_independent=fit_a["lnL"], lnL_C_independent=fit_c["lnL"],
        lnL_unconstrained=float(lnL_unconstrained), lnL_shared=shared["lnL_shared"],
        delta_lnL_LRT=float(delta_lnL), test_statistic=float(test_statistic),
        p_value=p_value, equivalent_sigma=equiv_sigma,
        fun_spread_max=fun_spread_max,
        convergence_flag_ok=bool(fun_spread_max is not None and fun_spread_max < 1e-6),
        delta_lnL_nonneg_ok=bool(delta_lnL >= 0),
        region_A_fit_detail=dict(
            best_params={n: float(v) for n, v in zip(mfa.PARAM_NAMES, fit_a["best_params"])},
            lnL_no_halo=fit_a["lnL_no_halo"], convexity_check=fit_a["convexity_check"],
        ),
        region_C_fit_detail=dict(
            best_params={n: float(v) for n, v in zip(mfa.PARAM_NAMES, fit_c["best_params"])},
            lnL_no_halo=fit_c["lnL_no_halo"], convexity_check=fit_c["convexity_check"],
        ),
        model2_shared_fit_detail=shared,
        shared_background_lrt=shared_bg,
        elapsed_sec=float(time.time() - t0),
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(message)s",
        handlers=[logging.FileHandler(OUT_LOG, mode="w"), logging.StreamHandler(sys.stdout)],
    )
    np.random.seed(mfa.SEED)
    logger.info(
        f"v20設定: PIXEL_DEG={_sub.PIXEL_DEG} CELL_MODE={mfa.CELL_MODE} "
        f"SIGNFREE_HALO={mfa.SIGNFREE_HALO} ULTRACLEAN={mfa.ULTRACLEAN} "
        f"DISK_BUBBLE={mfa.DISK_BUBBLE} NDIM={mfa.NDIM} 出力先={OUT_DIR}"
    )
    logger.info("露出マップ読み込み中...")
    expmaps, exp_centers = mfa.load_exposure_maps()
    assert np.allclose(exp_centers, mfa.BIN_CENTERS), "ビン定義が露出マップと不一致"

    logger.info("NFW J-map計算中...")
    j_map = mfa.nfw_j_map()
    nfw_norm, calib = mfa.calibrate_nfw_norm(expmaps[5], j_map)

    # メモリ節約のため、バブル構築用の大きな DataFrame を先に使い切って解放してから
    # halo 探索用の df_all を読む (本機 RAM 5.9 GB では両方同時保持で OOM する)。
    logger.info("バブル・Loop Iテンプレート構築中...")
    df_bubble = load_events_with_disk_lean() if mfa.DISK_BUBBLE else load_all_events_lean()
    logger.info(f"  構築用イベント数={len(df_bubble)}")
    bpos, bneg = mfa.build_bubble_counts_template(df_bubble)
    del df_bubble
    gc.collect()
    loop1, loop2 = _sub.loop_i_shell_templates()

    logger.info("halo探索用イベント読み込み中...")
    df_all = load_all_events_lean()
    logger.info(f"  halo探索用イベント数={len(df_all)}")

    bins_out = []
    for ib in range(mfa.N_BINS):
        r = process_bin(ib, df_all, expmaps, j_map, nfw_norm, bpos, bneg, loop1, loop2)
        bins_out.append(r)
        if "error" in r:
            logger.info(f"Bin{r['bin']}: SKIPPED ({r['error']})")
            continue
        logger.info(
            f"Bin{r['bin']:2d} ({r['e_center_gev']:7.2f} GeV): "
            f"f_halo A={r['f_halo_A_pointest']:+.4g} C={r['f_halo_C_pointest']:+.4g} "
            f"shared={r['f_halo_shared_pointest']:+.4g} | "
            f"LRT={r['test_statistic']:.3g} p={r['p_value']:.3e} "
            f"equiv={r['equivalent_sigma']:.2f}σ | "
            f"spread={r['fun_spread_max']:.1e} ok={r['delta_lnL_nonneg_ok']} "
            f"({r['elapsed_sec']:.0f}s)"
        )
        sb = r["shared_background_lrt"]
        logger.info(
            f"        [背景共有] halo A={sb['f_halo_A']:+.4g} C={sb['f_halo_C']:+.4g} "
            f"共通={sb['f_halo_common']:+.4g} | f_ics={sb['shared_background_alt']['f_ics']:.4g} "
            f"| LRT={sb['test_statistic']:.3g} equiv={sb['equivalent_sigma']:.2f}σ "
            f"spread={sb['fun_spread_max']:.1e} "
            f"| halo検出 A={sb['halo_detection']['sigma_halo_A']:.2f}σ "
            f"C={sb['halo_detection']['sigma_halo_C']:.2f}σ"
        )

    n_fit = sum(1 for r in bins_out if "error" not in r)
    n_nonneg = sum(1 for r in bins_out if r.get("delta_lnL_nonneg_ok") is True)
    n_conv = sum(1 for r in bins_out if r.get("convergence_flag_ok") is True)

    summary = dict(
        description=(
            "領域A(フェルミバブル内)/C(バブル外高緯度)で f_halo を共有した場合の尤度比検定"
            "(LRT)、全13ビン、v20仕様。モデル1=領域A/C独立フィット、モデル2=背景"
            f"{NB}パラメータは領域独立・f_halo のみ共有。MCMC 事後分布は取得しておらず、"
            "全て L-BFGS-B 多点始動による MLE 点推定である。解釈はこのスクリプトでは"
            "行わず数値のみ報告する。"
        ),
        region_definition=dict(
            nominal_bubble_rect=f"|l|<{BUBBLE_L_MAX} & {BUBBLE_B_MIN}<|b|<{BUBBLE_B_MAX}",
            split_granularity="cell" if mfa.CELL_MODE else "pixel",
            note=(
                "CELL_MODE では 10°セル中心が矩形内かで A/C を分ける(セルが両領域に"
                "またがると lnL の加法分解が壊れるため)。実効的な A は |l|<20°, "
                "10°<|b|<50°。C は |b_center|>=30° かつ A の外側。"
            ),
            region_C_b_min=REGION_C_B_MIN,
        ),
        param_names=list(mfa.PARAM_NAMES),
        reproducibility_seed=mfa.SEED,
        environment=mfa.env_stamp(),
        v20_settings=dict(
            pixel_deg=_sub.PIXEL_DEG, cell_mode=mfa.CELL_MODE,
            signfree_halo=mfa.SIGNFREE_HALO, ultraclean=mfa.ULTRACLEAN,
            disk_bubble=mfa.DISK_BUBBLE, b_min_deg=mfa.B_MIN_DEG,
        ),
        mcmc_omitted=True,
        n_bins_total=mfa.N_BINS, n_bins_fit=n_fit,
        n_bins_delta_lnL_LRT_nonneg=n_nonneg,
        n_bins_convergence_ok_fun_spread_below_1em6=n_conv,
        nfw_calibration=calib,
        bins=bins_out,
    )
    with open(OUT_JSON, "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    logger.info(f"→ {OUT_JSON}")
    logger.info(
        f"完了: {n_fit}/{mfa.N_BINS}ビンでフィット成功、ΔlnL>=0 が {n_nonneg}/{n_fit}、"
        f"fun_spread<1e-6 が {n_conv}/{n_fit}。"
    )


if __name__ == "__main__":
    main()
