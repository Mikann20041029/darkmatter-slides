"""
[系統誤差感度チェック・非headline] GALPROP webrun実出力(gas+ICS独立テンプレート)を
使った場合の全13ビンMCMC同時フィット — v2 (2026-07-13)。

背景: 2026-07-12に一度この検証(`mcmc_fit_all_bins_galprop_webrun_check.py`)を
試みたが、全13ビンで有意度が6.8-95.6σに跳ね上がり不採用と判定した。しかし、
その原因調査(下記)の結果、旧スクリプトは
  (a) 単一始点Nelder-Mead(多点始動なし) — 2026-07-12/13に本体パイプラインで
      発見・修正した「局所解にはまる」バグをそのまま抱えていた
  (b) 旧Loop I幾何(単一中心リング近似、2026-07-12に2シェルAckermannモデルへ
      修正済みだが本スクリプトには未反映)
  (c) 旧フェルミバブル(正のみ単一テンプレート、2026-07-13に正負2テンプレート化
      したが本スクリプトには未反映)
という3つの既知バグを全て抱えたままGALPROPだけをgas/ICS分離した状態だったため、
6.8-95.6σという壊れ方が「GALPROP webrunデータの較正不一致」由来なのか
「他の3バグ」由来なのか切り分けられていなかった。

本v2は、検証済みの現行headlineパイプライン(mcmc_fit_all_bins.py, 2026-07-13時点:
多点始動30回・Loop I 2シェル・バブル正負2テンプレート)からGALPROP部分だけを
gas/ICS分離版に差し替えることで、この切り分けを行う。

**なお、galdef_54_10000001自体に以下の確認済みの較正不一致がある**:
  - HI opacity補正スピン温度 Ts=125K (SLZ6R30T150C2の要求は150K、
    ファイル名`rbands_hi12_v2_qdeg_zmax1_Ts125.fits`で確認)
  - CR源分布 source_model=1(parameterized、汎用モデル) — Totaniが実際に
    使った分布(pulsars等)と一致するか未検証。galdefのTitleが
    "Untitled WebRun calculation"であり既定/例題ジョブの疑いが強い
  - gas/ICSテンプレートの絶対規格化がgll_iem_v07.fitsとピクセル平均で
    ~1e8倍異なる(原因未特定)
**そのためこの結果もTotaniの正式な再現値としては使えない**。あくまで
「GALPROPをgas/ICS分離するとheadline(単一テンプレート版)からどれだけ結果が
動くか」という感度チェックであり、旧チェック(2026-07-12)より高精度な
パイプラインで再検証した参考値として扱う。

モデル（各ビンiで独立にフィット、7自由パラメータ）:
  μ = ISO_i(固定, |b|≥50°平均)
    + f_gas × GAS_i + f_ics × ICS_i
    + f_loopI_a × LIa_i + f_loopI_b × LIb_i
    + f_fb × FB_i + f_fb_neg × FBneg_i
    + f_halo × HALO_i

出力:
  results/mcmc_allbins_webrun_check_v2/mcmc_bin<NN>.json
  results/mcmc_allbins_webrun_check_v2/halo_spectrum.png
  results/mcmc_allbins_webrun_check_v2/halo_spectrum.json
"""
import pathlib as _pathlib
import sys
sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))

import json
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import emcee
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"

import mcmc_fit_all_bins as mfa
import plot_skymap_all_subtracted as _sub

BASE = _pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = BASE / "results/mcmc_allbins_webrun_check_v2"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PARAM_NAMES = ["f_gas", "f_ics", "f_loopI_a", "f_loopI_b", "f_fb", "f_fb_neg", "f_halo"]
NDIM = len(PARAM_NAMES)


def build_templates_for_bin(ib, counts, expmap_i, gas_flux_i, ics_flux_i,
                             bubble_pos_bin3, bubble_neg_bin3, expmap_bubble_bin,
                             j_map, nfw_norm, loop_shell1, loop_shell2):
    emin, emax = mfa.BIN_EDGES[ib], mfa.BIN_EDGES[ib + 1]
    de_mev = (emax - emin) * 1000.0

    hi_b = np.abs(mfa.BG) >= 50
    iso_level = float(counts[hi_b].mean()) if hi_b.sum() > 0 else 0.0
    iso_counts = np.full_like(counts, iso_level)

    # [2026-07-17] mfa.DPIX_SR(スカラー)→ mfa.PIX_SOLID_ANGLE_SR(緯度依存配列
    # (π/180)^2·cos(b))に追従。mfa.BG(=このファイルのグリッド)と同形状 (120,120) で
    # expmap_i・gas_flux_i と要素ごとに掛かる。
    gas_tmpl = gas_flux_i * expmap_i * mfa.PIX_SOLID_ANGLE_SR * de_mev
    ics_tmpl = ics_flux_i * expmap_i * mfa.PIX_SOLID_ANGLE_SR * de_mev

    e3 = mfa.BIN_CENTERS[mfa.BUBBLE_BIN]
    ei = mfa.BIN_CENTERS[ib]
    de3_mev = (mfa.BIN_EDGES[mfa.BUBBLE_BIN + 1] - mfa.BIN_EDGES[mfa.BUBBLE_BIN]) * 1000.0
    exp_ratio = np.divide(expmap_i, expmap_bubble_bin,
                          out=np.zeros_like(expmap_i), where=expmap_bubble_bin > 0)
    spec_scale = exp_ratio * (de_mev / de3_mev) * (e3 / ei) ** 2
    fb_tmpl = bubble_pos_bin3 * spec_scale
    fb_neg_tmpl = bubble_neg_bin3 * spec_scale

    halo_tmpl = j_map * nfw_norm * expmap_i * mfa.PIX_SOLID_ANGLE_SR * de_mev

    return {
        "iso_counts": iso_counts, "gas": gas_tmpl, "ics": ics_tmpl,
        "loopI_a": loop_shell1, "loopI_b": loop_shell2,
        "fb": fb_tmpl, "fb_neg": fb_neg_tmpl, "halo": halo_tmpl,
        "iso_level": iso_level,
    }


def make_mu(params, t):
    f_gas, f_ics, f_la, f_lb, f_fb, f_fb_neg, f_halo = params
    mu = (t["iso_counts"] + f_gas * t["gas"] + f_ics * t["ics"] +
          f_la * t["loopI_a"] + f_lb * t["loopI_b"] +
          f_fb * t["fb"] + f_fb_neg * t["fb_neg"] + f_halo * t["halo"])
    return np.maximum(mu, 1e-10)


def log_prior(params):
    f_gas, f_ics, f_la, f_lb, f_fb, f_fb_neg, f_halo = params
    if any(p < 0 for p in [f_gas, f_ics, f_la, f_lb, f_fb]):
        return -np.inf
    if any(abs(p) > 1e6 for p in params):
        return -np.inf
    return 0.0


def log_likelihood(params, counts, t):
    mu = make_mu(params, t)
    valid = t["valid"]
    return float(np.sum(counts[valid] * np.log(mu[valid]) - mu[valid]))


def log_probability(params, counts, t):
    lp = log_prior(params)
    if not np.isfinite(lp):
        return -np.inf
    ll = log_likelihood(params, counts, t)
    return lp + ll if np.isfinite(ll) else -np.inf


def fit_one_bin(ib, counts, templates, x0):
    """mcmc_fit_all_bins.fit_one_bin()と同じ手順(多点始動30回+MCMC)。
    パラメータ数が7(先頭6が非負制約f_gas,f_ics,f_loopI_a,f_loopI_b,f_fb、
    f_fb_negとf_haloは符号自由)である点のみ異なる。"""
    def neg_ll_nohalo(p6):
        if any(x < 0 for x in p6[:5]):
            return 1e10
        return -log_likelihood(list(p6) + [0.0], counts, templates)

    res_nh = mfa._multistart_minimize(neg_ll_nohalo, x0[:6])
    lnL_noh = -res_nh.fun

    def neg_ll(p):
        if any(x < 0 for x in p[:5]):
            return 1e10
        return -log_likelihood(p, counts, templates)

    x0_with_halo = list(res_nh.x) + [x0[6]]
    res = mfa._multistart_minimize(neg_ll, x0_with_halo)
    best = res.x
    lnL_with = -res.fun
    if lnL_with < lnL_noh:
        best = np.array(list(res_nh.x) + [0.0])
        lnL_with = lnL_noh

    delta_lnL = lnL_with - lnL_noh
    significance = float(np.sqrt(2 * max(delta_lnL, 0)))

    n_walkers, n_steps, n_burn = 32, 1500, 400
    pos = best + 1e-3 * np.abs(best).clip(min=1e-6) * np.random.randn(n_walkers, NDIM)
    pos[:, :5] = np.abs(pos[:, :5])
    sampler = emcee.EnsembleSampler(n_walkers, NDIM, log_probability, args=(counts, templates))
    sampler.run_mcmc(pos, n_steps, progress=False)
    flat = sampler.get_chain(discard=n_burn, thin=5, flat=True)

    medians = np.median(flat, axis=0)
    lo, hi = np.percentile(flat, [16, 84], axis=0)
    return dict(
        bin=ib + 1, e_center_gev=float(mfa.BIN_CENTERS[ib]),
        iso_level_fixed=templates["iso_level"],
        params={n: {"median": float(m), "lo16": float(l), "hi84": float(h)}
                for n, m, l, h in zip(PARAM_NAMES, medians, lo, hi)},
        delta_lnL=float(delta_lnL), significance_sigma=significance,
        n_events=int(counts.sum()),
    )


def main():
    print("[系統誤差感度チェック・非headline v2] GALPROP webrun実出力での全13ビンフィット")
    print("実測露出マップ読み込み中...")
    expmaps, exp_bin_centers = mfa.load_exposure_maps()
    print("イベントデータ読み込み中...")
    df_all = mfa.load_all_events()
    print("NFW J-factorマップ計算中...")
    j_map = mfa.nfw_j_map()
    nfw_norm, calib_info = mfa.calibrate_nfw_norm(expmaps[5], j_map)
    print("バブルテンプレート構築中(正負2成分)...")
    bubble_pos, bubble_neg = mfa.build_bubble_counts_template(df_all)
    expmap_bubble_bin = expmaps[mfa.BUBBLE_BIN]
    print("Loop I幾何シェルテンプレート計算中...")
    loop_shell1, loop_shell2 = _sub.loop_i_shell_templates()

    results = []
    for ib in range(mfa.N_BINS):
        emin, emax = mfa.BIN_EDGES[ib], mfa.BIN_EDGES[ib + 1]
        print(f"\n--- Bin{ib+1:02d} ({mfa.BIN_CENTERS[ib]:.2f} GeV) ---")
        sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
        counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
        print(f"  イベント数: {int(counts.sum())}")

        masked_counts, n_masked = _sub.mask_point_sources(counts.copy())
        valid = ~np.isnan(masked_counts)
        valid &= (np.abs(mfa.BG) >= 10) & (np.abs(mfa.BG) <= 60)
        print(f"  点源マスク: {n_masked}ピクセル除外 / 有効ピクセル数={valid.sum()}")

        # 2026-07-15: _load_galprop_gas_ics_templates()は正しいgaldef SLZ6R30T150C2
        # (HEALPixベース)を指すよう更新されたため、この却下済みチェック(webrun_10000001,
        # Ts=125K不一致)の意図を保つため明示的にlegacy版を呼ぶ
        gas_flux_i, ics_flux_i = _sub._load_galprop_gas_ics_templates_legacy_webrun10000001(emin, emax)
        templates = build_templates_for_bin(
            ib, counts, expmaps[ib], gas_flux_i, ics_flux_i,
            bubble_pos, bubble_neg, expmap_bubble_bin, j_map, nfw_norm,
            loop_shell1, loop_shell2,
        )
        templates["valid"] = valid

        c_mean = max(counts[valid].mean(), 1e-6)
        x0_gas = 0.5 * c_mean / max(templates["gas"][valid].mean(), 1e-30)
        x0_ics = 0.5 * c_mean / max(templates["ics"][valid].mean(), 1e-30)
        x0_la = 0.3 * c_mean / max(templates["loopI_a"][valid].mean(), 1e-30)
        x0_lb = 0.3 * c_mean / max(templates["loopI_b"][valid].mean(), 1e-30)
        x0_fbneg = 0.3 * c_mean / max(templates["fb_neg"][valid].mean(), 1e-30) \
            if templates["fb_neg"][valid].mean() > 0 else 0.3
        x0 = [x0_gas, x0_ics, x0_la, x0_lb, 0.5, x0_fbneg, 0.5]
        try:
            r = fit_one_bin(ib, counts, templates, x0)
        except Exception as e:
            print(f"  フィット失敗: {e}")
            r = dict(bin=ib + 1, e_center_gev=float(mfa.BIN_CENTERS[ib]), error=str(e))
        results.append(r)
        if "significance_sigma" in r:
            print(f"  f_gas={r['params']['f_gas']['median']:.4g}  "
                  f"f_ics={r['params']['f_ics']['median']:.4g}  "
                  f"f_halo={r['params']['f_halo']['median']:.4g}  "
                  f"ΔlnL={r['delta_lnL']:.2f}  有意度={r['significance_sigma']:.2f}σ")

        with open(OUT_DIR / f"mcmc_bin{ib+1:02d}.json", "w") as f:
            json.dump(r, f, indent=2, ensure_ascii=False)

    summary = dict(
        method="[系統誤差感度チェック・非headline v2] MCMC (emcee, Poisson尤度, 7自由パラメータ: "
               "f_gas/f_ics/f_loopI_a/f_loopI_b/f_fb/f_fb_neg/f_halo)。"
               "多点始動30回・Loop I 2シェル幾何・バブル正負2テンプレートは現行headlineと同一",
        galprop_source="ref/galprop_webrun_10000001 (galdef_54_10000001)。既知の較正不一致: "
                       "Ts=125K(要求150K)、source_model=1(汎用、Lorimer pulsarsと一致するか未検証、"
                       "Title='Untitled WebRun calculation')、絶対規格化がgll_iem_v07.fitsと大きく相違。"
                       "Totaniの正式な再現値ではなく感度チェック",
        nfw_calibration=calib_info,
        bins=results,
    )
    with open(OUT_DIR / "halo_spectrum.json", "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    valid_r = [r for r in results if "significance_sigma" in r]
    if valid_r:
        e = [r["e_center_gev"] for r in valid_r]
        f_halo = [r["params"]["f_halo"]["median"] for r in valid_r]
        f_halo_lo = [r["params"]["f_halo"]["lo16"] for r in valid_r]
        f_halo_hi = [r["params"]["f_halo"]["hi84"] for r in valid_r]
        sig = [r["significance_sigma"] * np.sign(r["params"]["f_halo"]["median"]) for r in valid_r]

        fig, axes = plt.subplots(2, 1, figsize=(9, 8), sharex=True, facecolor="#05051A")
        for ax in axes:
            ax.set_facecolor("#05051A")
            ax.set_xscale("log")
            ax.tick_params(colors="white")
            for sp in ax.spines.values():
                sp.set_color("white")
        axes[0].errorbar(e, f_halo,
                          yerr=[np.array(f_halo) - np.array(f_halo_lo),
                                np.array(f_halo_hi) - np.array(f_halo)],
                          fmt="o-", color="#FFCC00", ecolor="#FFCC00", capsize=3)
        axes[0].axhline(0, color="gray", ls=":")
        axes[0].set_ylabel("f_halo (振幅)", color="white")
        axes[0].set_title("[系統誤差感度チェック・非headline v2] GALPROP webrun版 全13ビンスペクトル",
                           color="white")
        axes[1].plot(e, sig, "o-", color="#44ff88")
        axes[1].axhline(0, color="gray", ls=":")
        axes[1].axhline(2, color="red", ls="--", alpha=0.5)
        axes[1].axhline(-2, color="red", ls="--", alpha=0.5)
        axes[1].set_ylabel("有意度 [σ]", color="white")
        axes[1].set_xlabel("Energy [GeV]", color="white")
        fig.tight_layout()
        fig.savefig(OUT_DIR / "halo_spectrum.png", dpi=130, facecolor="#05051A")
        plt.close()
        print(f"\n→ {OUT_DIR}/halo_spectrum.png")

    print(f"\n→ {OUT_DIR}/halo_spectrum.json")
    print("\n完了。galdefの較正不一致(Ts/source_model/絶対規格化)が既知のため、感度チェックとして扱うこと。")


if __name__ == "__main__":
    main()
