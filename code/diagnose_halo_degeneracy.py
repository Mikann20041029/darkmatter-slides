"""
2026-07-13 天の川銀河ハロー解析の頑健性診断(ユーザー指摘への対応)。

問題意識: Bin6のヘッドライン有意度8.73σは、Poisson尤度のみに基づくため系統誤差
(GALPROP単一テンプレートのgas/ICS分離なし、フェルミバブルの平坦スペクトル外挿)
を含んでいない。低エネルギー側の明らかに疑わしい有意度(-22.7σ等)も同程度の
%レベルの全体カウントミスマッチで説明できてしまうため、ヘッドラインの「検出」が
NFW空間形状に由来する本物の信号か、それともGALPROP/バブルテンプレートの形状不完全性
がNFW形状に部分的に吸収されているだけかを、テンプレート形状の違いを使って切り分ける。

診断1: Bin6のピクセル別 log-likelihood 寄与差 (with-halo − no-halo) をマップ化し、
       改善が銀河面近傍・バブル領域に集中しているか、NFW形状(高銀緯まで滑らかに広がる)
       と整合する分布かを目視確認する。
診断2: |b|>=30°(GALPROP/バブルテンプレートの値が銀河面近傍よりずっと小さい高銀緯域)
       に限定して同じ5パラメータ最適化+MCMCを再実行し、f_halo の有意度が残るか検証する。
       比較対照として、既知に疑わしいBin1(1.51GeV)でも同じ高銀緯限定テストを行う。

出力:
  data/figure-halo-diagnostics/bin6_loglik_map.png
  data/figure-halo-diagnostics/highlat_refit_summary.txt

[2026-07-13 追記・注意] 本スクリプトはバブルテンプレートが正のみの旧5パラメータ
モデル(mcmc_fit_all_bins.pyの旧版)を前提に書かれており、その後の修正
(バブル正負2テンプレート化・多点始動30回化)後のmcmc_fit_all_bins.pyとは
関数シグネチャが変わったため、再実行するとエラーになる(build_bubble_counts_templateが
tupleを返す・build_templates_for_binの引数が変わった等)。ここで得られた「符号反転」
という定性的発見自体は正しく、後続のdiagnose_halo_degeneracy_2.py・
diagnose_bubble_check.py・diagnose_halo_degeneracy_3_posneg.pyで追試・発展させている。
数値そのもの(f_halo, 有意度)は6パラメータ修正版の値(diagnose_halo_degeneracy_3_posneg.py
の出力、または.dev/CHANGELOG.md参照)で置き換わっている。
"""
import json
import pathlib as _pathlib
import sys
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm
from mpl_toolkits.axes_grid1 import make_axes_locatable
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"

SCRIPT_DIR = _pathlib.Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

import mcmc_fit_all_bins as mfa  # noqa: E402
import plot_skymap_all_subtracted as _sub  # noqa: E402
import emcee  # noqa: E402

OUT_DIR = ROOT / "data" / "figure-halo-diagnostics"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def build_bin_data(ib, df_all, expmaps, j_map, nfw_norm, bubble3, expmap_bubble, loop1, loop2):
    emin, emax = mfa.BIN_EDGES[ib], mfa.BIN_EDGES[ib + 1]
    sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
    counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
    masked, n_masked = _sub.mask_point_sources(counts.copy())
    valid = ~np.isnan(masked)
    valid &= (np.abs(mfa.BG) >= 10) & (np.abs(mfa.BG) <= 60)
    galflux = _sub._load_galprop_template(emin, emax)
    t = mfa.build_templates_for_bin(ib, counts, expmaps[ib], galflux, bubble3,
                                     expmap_bubble, j_map, nfw_norm, loop1, loop2)
    return counts, valid, t


def refit(counts, valid, t, seed=0):
    """mcmc_fit_all_bins.fit_one_bin() と同じ手順(多点始動 no-halo/with-halo + MCMC)を
    任意の valid マスクで実行する。"""
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

    n_walkers, n_steps, n_burn = 32, 1000, 300
    rng = np.random.default_rng(seed)
    pos = best + 1e-3 * np.abs(best).clip(min=1e-6) * rng.standard_normal((n_walkers, mfa.NDIM))
    pos[:, :4] = np.abs(pos[:, :4])
    sampler = emcee.EnsembleSampler(n_walkers, mfa.NDIM, mfa.log_probability, args=(counts, t))
    sampler.run_mcmc(pos, n_steps, progress=False)
    flat = sampler.get_chain(discard=n_burn, thin=5, flat=True)
    f_halo_med = float(np.median(flat[:, 4]))
    return dict(delta_lnL=float(delta_lnL), sig=sig, f_halo_median=f_halo_med,
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

    # ---- 診断1: Bin6 ピクセル別 log-likelihood 寄与差マップ ----
    print("\n[診断1] Bin6 ピクセル別 log-likelihood 寄与マップ")
    ib = 5
    counts, valid, t = build_bin_data(ib, df_all, expmaps, j_map, nfw_norm, bubble3, expmap_bubble, loop1, loop2)
    fit = json.load(open(ROOT / "results/mcmc_allbins/mcmc_bin06.json"))
    p = fit["params"]
    with_halo = [p["f_gal"]["median"], p["f_loopI_a"]["median"], p["f_loopI_b"]["median"],
                 p["f_fb"]["median"], p["f_halo"]["median"]]
    mu_noh = mfa.make_mu(with_halo[:4] + [0.0], t)
    mu_full = mfa.make_mu(with_halo, t)
    ll_noh = counts * np.log(mu_noh) - mu_noh
    ll_full = counts * np.log(mu_full) - mu_full
    dll = ll_full - ll_noh
    dll_masked = np.where(valid, dll, np.nan)

    fig, ax = plt.subplots(figsize=(8, 7))
    vlim = np.nanpercentile(np.abs(dll_masked), 98)
    im = ax.pcolormesh(_sub.L_BINS, _sub.B_BINS, dll_masked.T, cmap="RdBu_r",
                        vmin=-vlim, vmax=vlim, shading="flat")
    ax.set_xlim(60, -60); ax.set_ylim(-60, 60)
    ax.axhspan(-10, 10, color="gray", alpha=0.35, zorder=3)
    ax.axhline(30, color="lime", ls="--", lw=1); ax.axhline(-30, color="lime", ls="--", lw=1)
    ax.set_xlabel("銀経 l [deg]"); ax.set_ylabel("銀緯 b [deg]")
    ax.set_title(f"Bin6(20.76GeV): ピクセル別 log-likelihood 寄与差 (with-halo − no-halo)\n"
                 f"合計ΔlnL={dll_masked[valid].sum():.2f} (緑線: |b|=30°, 高緯度限定テストの境界)")
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="4%", pad=0.06)
    fig.colorbar(im, cax=cax, label="Δ(pixel log-likelihood)")
    fig.tight_layout()
    out1 = OUT_DIR / "bin6_loglik_map.png"
    fig.savefig(out1, dpi=150)
    plt.close(fig)
    print(f"  -> {out1}")

    frac_highlat = dll_masked[valid & (np.abs(mfa.BG) >= 30)].sum() / dll_masked[valid].sum()
    frac_lowlat = 1 - frac_highlat
    print(f"  ΔlnL全体={dll_masked[valid].sum():.2f}, うち|b|>=30度分={frac_highlat*100:.1f}%, "
          f"|b|<30度分={frac_lowlat*100:.1f}%")

    # ---- 診断2: 高緯度限定(|b|>=30度)再フィット ----
    print("\n[診断2] |b|>=30度限定での再フィット (Bin6, Bin5, 対照Bin1)")
    summary = [f"ΔlnL空間分布(Bin6): |b|>=30度分={frac_highlat*100:.1f}%, |b|<30度分={frac_lowlat*100:.1f}%", ""]
    for ib in (0, 4, 5):
        counts, valid, t = build_bin_data(ib, df_all, expmaps, j_map, nfw_norm, bubble3, expmap_bubble, loop1, loop2)
        valid_hl = valid & (np.abs(mfa.BG) >= 30)
        r_full = refit(counts, valid, t)
        r_hl = refit(counts, valid_hl, t)
        line = (f"Bin{ib+1:2d} E={mfa.BIN_CENTERS[ib]:7.2f}GeV  "
                f"[全ROI] f_halo={r_full['f_halo_median']:+.4g} sig={r_full['sig']:.2f}σ n={r_full['n_events']:.0f}  "
                f"[|b|>=30度] f_halo={r_hl['f_halo_median']:+.4g} sig={r_hl['sig']:.2f}σ n={r_hl['n_events']:.0f}")
        print("  " + line)
        summary.append(line)

    out2 = OUT_DIR / "highlat_refit_summary.txt"
    with open(out2, "w") as f:
        f.write("\n".join(summary) + "\n")
    print(f"\n-> {out2}")


if __name__ == "__main__":
    main()
