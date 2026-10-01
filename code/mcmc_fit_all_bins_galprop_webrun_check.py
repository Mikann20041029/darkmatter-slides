"""
[系統誤差チェック・非headline] GALPROP webrun実出力(gas+ICS独立テンプレート)を
使った場合の全13ビンMCMC同時フィット — mcmc_fit_all_bins.py(検証済み・headline)
の派生版。

2026-07-12の位置づけ:
  Totani (2025) §3.4.4-3.4.5の精読で、ベースライン解析は`gll_iem_v07.fits`ではなく
  GALPROP ver.54をgaldef `SLZ6R30T150C2`で自ら実行しgas/ICSを独立テンプレート化
  していると判明した。ユーザーが以前取得していたGALPROP webrun出力
  (`ref/galprop_webrun_10000001/`, galdef_54_10000001)でgas([pion_decay+bremss])と
  ICS(isotropic合算)を独立パラメータ化しmcmc_fit_all_bins.pyを拡張して試したところ、
  **全13ビンで有意度が6.8σ〜95.6σに跳ね上がった**(旧gll_iem_v07版は0.24σ〜11.78σ)。

  これは新しい検出ではなく、2026-07-11に発見・修正した「テンプレート不一致が
  ハロー成分に吸収され非物理的に有意度が水増しされる」バグと同じ壊れ方のパターン
  である。原因として以下の[ASSUMPTION]付き既知の不一致が濃厚:
    - galdef_54_10000001のHI opacity補正スピン温度Ts=125K(SLZ6R30T150C2の要求は150K)
    - CR源分布パラメータ(source_model=1, alpha=0.5/beta=1.0)がLorimer pulsarフィット
      値と一致するか未検証(webrun実行時にTitleが"Untitled WebRun calculation"であり
      デフォルト/例題ジョブの可能性が高い)
    - gas/ICSテンプレートの絶対規格化がgll_iem_v07.fitsとピクセル平均で~1e8倍異なる
      (CR源正規化パラメータ自体は現実的な値だが、粗いグリッド(dr=1,dz=0.2)や
      未較正の絶対規格化が影響している可能性、根本原因は未特定)

  **この派生スクリプトの結果はheadlineとして使用しない**。あくまで「GALPROPの
  較正がSLZ6R30T150C2と厳密に一致しないと結果が大きく動く」という系統誤差の
  存在を定量的に示す予備チェックとして`results/mcmc_allbins_webrun_check/`に
  隔離保存する。galprop.stanford.eduのwebrun復旧後、正しいgaldefで再計算し
  mcmc_fit_all_bins.py本体をgas+ICS構成に置き換えるのが今後の課題。

モデル（各ビンiで独立にフィット、6自由パラメータ）:
  μ = ISO_i(固定, |b|≥50°平均)
    + f_gas   × GAS_i   (= GALPROP gas[pion_decay+bremss]フラックス × exposure_i × ΔΩ × ΔE_i)
    + f_ics   × ICS_i   (= GALPROP ICS[isotropic合算]フラックス × exposure_i × ΔΩ × ΔE_i)
    + f_loopI_a × LIa_i
    + f_loopI_b × LIb_i
    + f_fb    × FB_i
    + f_halo  × HALO_i

出力:
  results/mcmc_allbins_webrun_check/mcmc_bin<NN>.json
  results/mcmc_allbins_webrun_check/halo_spectrum.png
  results/mcmc_allbins_webrun_check/halo_spectrum.json
"""
import pathlib as _pathlib
import sys
sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))

import json
import warnings
warnings.filterwarnings("ignore")

import numpy as np
from numpy.typing import NDArray
import pandas as pd
import emcee
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"

import plot_skymap_all_subtracted as _sub

BASE     = _pathlib.Path(__file__).resolve().parent.parent
OUT_DIR  = BASE / "results/mcmc_allbins_webrun_check"
OUT_DIR.mkdir(parents=True, exist_ok=True)
EXPMAP_PATH = BASE / "data/fermi_exposure/expmap_allbins.npz"

BIN_CENTERS = np.array([
    1.51, 2.55, 4.31, 7.28, 12.29, 20.76, 35.06,
    59.22, 100.02, 168.93, 285.33, 481.93, 814.00
])
BIN_EDGES = np.zeros(len(BIN_CENTERS) + 1)
BIN_EDGES[1:-1] = np.sqrt(BIN_CENTERS[:-1] * BIN_CENTERS[1:])
BIN_EDGES[0]  = BIN_CENTERS[0] ** 2 / BIN_EDGES[1]
BIN_EDGES[-1] = BIN_CENTERS[-1] ** 2 / BIN_EDGES[-2]
N_BINS = len(BIN_CENTERS)
BUBBLE_BIN = 2

PARAM_NAMES = ["f_gas", "f_ics", "f_loopI_a", "f_loopI_b", "f_fb", "f_halo"]
NDIM = len(PARAM_NAMES)

D_SUN, RS = 8.0, 21.0

L_C = (_sub.L_BINS[:-1] + _sub.L_BINS[1:]) / 2
B_C = (_sub.B_BINS[:-1] + _sub.B_BINS[1:]) / 2
LG, BG = np.meshgrid(L_C, B_C, indexing="ij")

# [2026-07-17 DPIX_SR cos(b) 修正] (l,b)グリッド1ピクセルの真の立体角 ΔΩ(b)=Δl·Δb·cos(b)
# [sr]。旧スカラー (π/180)^2 は b=0 でのみ正しく |b|=60°で最大2倍過大評価。BG と同形状の
# 配列に変更(headline mcmc_fit_all_bins.py と同期。この却下済み比較スクリプトも系統誤差
# チェックの整合のため同じ立体角定義に揃える)。
PIX_SOLID_ANGLE_SR: NDArray[np.float64] = (np.pi / 180.0) ** 2 * np.cos(np.radians(BG))


def load_exposure_maps():
    d = np.load(EXPMAP_PATH)
    return d["expmaps"], d["bin_centers"]


def load_all_events():
    df = pd.read_csv(BASE / "data/CSV/filtered_events_week780.csv",
                      comment="#", low_memory=False)
    df = df[(df.b_deg.abs() >= 10) & (df.b_deg.abs() <= 60) &
            (df.l_deg.abs() <= 60)]
    return df


def nfw_j_map():
    H = np.zeros((len(L_C), len(B_C)))
    s = np.linspace(0.01, 60.0, 150)
    ds = s[1] - s[0]
    for i, l in enumerate(L_C):
        for j, b in enumerate(B_C):
            if abs(b) < 10:
                continue
            l_r, b_r = np.radians(l), np.radians(b)
            r2 = D_SUN**2 + s**2 - 2*D_SUN*s*np.cos(b_r)*np.cos(l_r)
            r  = np.sqrt(np.maximum(r2, 0.01))
            x  = r / RS
            rho = 1.0 / (x * (1 + x)**2)
            H[i, j] = np.sum(rho**2 * ds)
    return H


def build_bubble_counts_template(df_all):
    return _sub.build_fermi_bubble_template(df_all)


def calibrate_nfw_norm(expmap_bin6, j_map):
    e_mev = 21000.0
    e2dnde = 3e-5
    flux = e2dnde / e_mev ** 2

    ib_ref = np.argmin(np.abs(L_C - 0.0))
    jb_ref = np.argmax(np.abs(B_C))
    exp_ref = expmap_bin6[ib_ref, jb_ref]
    j_ref = j_map[ib_ref, jb_ref]
    dpix_ref = float(PIX_SOLID_ANGLE_SR[ib_ref, jb_ref])

    de6_mev = (28.07 - 15.35) * 1000.0
    counts_ref = flux * exp_ref * dpix_ref * de6_mev
    norm = counts_ref / (j_ref * exp_ref * dpix_ref * de6_mev)
    return float(norm), dict(flux=flux, exp_ref=float(exp_ref), j_ref=float(j_ref),
                              b_ref=float(B_C[jb_ref]))


def build_templates_for_bin(ib, counts, expmap_i, gas_flux_i, ics_flux_i,
                             bubble_counts_bin3, expmap_bubble_bin,
                             j_map, nfw_norm):
    emin, emax = BIN_EDGES[ib], BIN_EDGES[ib + 1]
    de_mev = (emax - emin) * 1000.0

    hi_b = np.abs(BG) >= 50
    iso_level = float(counts[hi_b].mean()) if hi_b.sum() > 0 else 0.0
    iso_counts = np.full_like(counts, iso_level)

    gas_tmpl = gas_flux_i * expmap_i * PIX_SOLID_ANGLE_SR * de_mev
    ics_tmpl = ics_flux_i * expmap_i * PIX_SOLID_ANGLE_SR * de_mev

    li_l, li_b = -31.0, 18.0
    cos_ang = (np.sin(np.radians(BG)) * np.sin(np.radians(li_b)) +
               np.cos(np.radians(BG)) * np.cos(np.radians(li_b)) *
               np.cos(np.radians(LG - li_l)))
    ang = np.degrees(np.arccos(np.clip(cos_ang, -1, 1)))
    li_a = ((ang >= 40) & (ang <= 55)).astype(float)
    li_b_tmpl = ((ang >= 55) & (ang <= 70)).astype(float)

    e3 = BIN_CENTERS[BUBBLE_BIN]
    ei = BIN_CENTERS[ib]
    de3_mev = (BIN_EDGES[BUBBLE_BIN + 1] - BIN_EDGES[BUBBLE_BIN]) * 1000.0
    exp_ratio = np.divide(expmap_i, expmap_bubble_bin,
                          out=np.zeros_like(expmap_i), where=expmap_bubble_bin > 0)
    fb_tmpl = bubble_counts_bin3 * exp_ratio * (de_mev / de3_mev) * (e3 / ei) ** 2

    halo_tmpl = j_map * nfw_norm * expmap_i * PIX_SOLID_ANGLE_SR * de_mev

    return {
        "iso_counts": iso_counts, "gas": gas_tmpl, "ics": ics_tmpl,
        "loopI_a": li_a, "loopI_b": li_b_tmpl,
        "fb": fb_tmpl, "halo": halo_tmpl,
        "iso_level": iso_level,
    }


def make_mu(params, t):
    f_gas, f_ics, f_la, f_lb, f_fb, f_halo = params
    mu = (t["iso_counts"] + f_gas * t["gas"] + f_ics * t["ics"] +
          f_la * t["loopI_a"] + f_lb * t["loopI_b"] +
          f_fb * t["fb"] + f_halo * t["halo"])
    return np.maximum(mu, 1e-10)


def log_prior(params):
    f_gas, f_ics, f_la, f_lb, f_fb, f_halo = params
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
    from scipy.optimize import minimize

    def neg_ll_nohalo(p5):
        if any(x < 0 for x in p5):
            return 1e10
        return -log_likelihood(list(p5) + [0.0], counts, templates)

    res_nh = minimize(neg_ll_nohalo, x0[:5], method="Nelder-Mead",
                       options={"maxiter": 8000, "fatol": 1e-6, "xatol": 1e-6})
    lnL_noh = -res_nh.fun

    def neg_ll(p):
        if any(x < 0 for x in p[:5]):
            return 1e10
        return -log_likelihood(p, counts, templates)

    x0_with_halo = list(res_nh.x) + [x0[5]]
    res = minimize(neg_ll, x0_with_halo, method="Nelder-Mead",
                    options={"maxiter": 8000, "fatol": 1e-6, "xatol": 1e-6})
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
        bin=ib + 1, e_center_gev=float(BIN_CENTERS[ib]),
        iso_level_fixed=templates["iso_level"],
        params={n: {"median": float(m), "lo16": float(l), "hi84": float(h)}
                for n, m, l, h in zip(PARAM_NAMES, medians, lo, hi)},
        delta_lnL=float(delta_lnL), significance_sigma=significance,
        n_events=int(counts.sum()),
    )


def main():
    print("[系統誤差チェック用・非headline] GALPROP webrun実出力での全13ビンフィット")
    print("実測露出マップ読み込み中...")
    expmaps, exp_bin_centers = load_exposure_maps()
    assert np.allclose(exp_bin_centers, BIN_CENTERS), "ビン定義が露出マップと不一致"

    print("イベントデータ読み込み中...")
    df_all = load_all_events()

    print("NFW J-factorマップ計算中(数分)...")
    j_map = nfw_j_map()

    nfw_norm, calib_info = calibrate_nfw_norm(expmaps[5], j_map)
    print(f"  NFW校正: norm={nfw_norm:.4e}")

    print("バブルテンプレート構築中(Bin3基準)...")
    bubble_counts_bin3 = build_bubble_counts_template(df_all)
    expmap_bubble_bin = expmaps[BUBBLE_BIN]

    results = []
    for ib in range(N_BINS):
        emin, emax = BIN_EDGES[ib], BIN_EDGES[ib + 1]
        print(f"\n--- Bin{ib+1:02d} ({BIN_CENTERS[ib]:.2f} GeV) ---")
        sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
        counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
        print(f"  イベント数: {int(counts.sum())}")

        masked_counts, n_masked = _sub.mask_point_sources(counts.copy())
        valid = ~np.isnan(masked_counts)
        valid &= (np.abs(BG) >= 10) & (np.abs(BG) <= 60)
        print(f"  点源マスク: {n_masked}ピクセル除外 / |b|<10除外込みで有効ピクセル数={valid.sum()}")

        # 2026-07-15: _load_galprop_gas_ics_templates()は正しいgaldef SLZ6R30T150C2
        # (HEALPixベース)を指すよう更新されたため、この却下済みチェック(webrun_10000001,
        # Ts=125K不一致)の意図を保つため明示的にlegacy版を呼ぶ
        gas_flux_i, ics_flux_i = _sub._load_galprop_gas_ics_templates_legacy_webrun10000001(emin, emax)
        templates = build_templates_for_bin(
            ib, counts, expmaps[ib], gas_flux_i, ics_flux_i,
            bubble_counts_bin3, expmap_bubble_bin, j_map, nfw_norm,
        )
        templates["valid"] = valid

        c_mean = max(counts[valid].mean(), 1e-6)
        x0_gas = 0.5 * c_mean / max(templates["gas"][valid].mean(), 1e-30)
        x0_ics = 0.5 * c_mean / max(templates["ics"][valid].mean(), 1e-30)
        x0 = [x0_gas, x0_ics, 0.3, 0.3, 0.5, 0.5]
        try:
            r = fit_one_bin(ib, counts, templates, x0)
        except Exception as e:
            print(f"  フィット失敗: {e}")
            r = dict(bin=ib + 1, e_center_gev=float(BIN_CENTERS[ib]), error=str(e))
        results.append(r)
        if "significance_sigma" in r:
            print(f"  f_gas={r['params']['f_gas']['median']:.4g}  "
                  f"f_ics={r['params']['f_ics']['median']:.4g}  "
                  f"f_halo={r['params']['f_halo']['median']:.4g}  "
                  f"ΔlnL={r['delta_lnL']:.2f}  有意度={r['significance_sigma']:.2f}σ")

        with open(OUT_DIR / f"mcmc_bin{ib+1:02d}.json", "w") as f:
            json.dump(r, f, indent=2, ensure_ascii=False)

    summary = dict(
        method="[系統誤差チェック・非headline] MCMC (emcee, Poisson log-likelihood, 6 free params: f_gas/f_ics/f_loopI_a/f_loopI_b/f_fb/f_halo)",
        galprop_source="ref/galprop_webrun_10000001 (galdef_54_10000001, gas=pion_decay+bremss, ics=isotropic; [ASSUMPTION] Ts=125K not Totani's 150K, source dist. not verified as Lorimer, absolute norm ~1e8x gll_iem_v07 - 未解明)",
        caveat="全13ビンで有意度6.8-95.6σと非物理的に高い。gll_iem_v07版(headline, results/mcmc_allbins/)と比較すると2026-07-11に修正した縮退バグと同じ壊れ方のパターンであり、この結果を信頼してはいけない。SLZ6R30T150C2での再計算が必要。",
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
        axes[0].set_title("[系統誤差チェック・非headline] GALPROP webrun版 全13ビンスペクトル",
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
    print("\n完了。この結果はheadlineとして使わないこと(caveat参照)。")


if __name__ == "__main__":
    main()
