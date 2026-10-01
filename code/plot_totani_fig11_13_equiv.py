"""
plot_totani_fig11_13_equiv.py
Totani (2025) Fig 11-13 相当: NFW-rho^2 ハローモデル・残差マップを生成する。

2026-07-13 改訂: 旧版(OLS + GALPROP指数関数近似 + 単一中心LoopIリング)は
現行パイプライン(code/mcmc_fit_all_bins.py: 直接GALPROPフィット, Ackermann
2シェルLoop I幾何モデル, Poisson尤度MCMC同時フィット, 多点始動Nelder-Mead)
と整合しなくなったため、mcmc_fit_all_bins.py の関数・保存済みベストフィット値
(results/mcmc_allbins/mcmc_bin<NN>.json)を再利用して全面的に再生成する。

各ビンについて、no-halo(4パラメータ)フィットと with-halo(5パラメータ)フィットの
背景パラメータは別々に最適化されている(mcmc_fit_all_bins.fit_one_bin参照)ため、
本図の①と②は旧版と異なり同一ではない:
  [0,0] ①ハロー無しフィット残差 = data - mu_nohalo(no-halo最適化パラメータ)
  [0,1] ②ハロー込みフィット残差 = data - mu_nohalo(with-halo最適化パラメータ、
        f_halo項を除く) ― これから③を差し引くと④になる「信号」
  [1,0] ③ハローモデル = f_halo(MCMC中央値) × halo_tmpl
  [1,1] ④フィット後残差 = ② − ③ = data − full_model(MCMC中央値)

no-halo最適化パラメータは mcmc_bin<NN>.json に保存されていないため、
_multistart_minimize() を用いてその場で再計算する(MCMCは行わない、点推定のみ)。
with-halo側は mcmc_bin<NN>.json の MCMC事後中央値をそのまま使う。

出力:
  data/figure-all-bins/fig11_equiv_bin6_maps.png
  data/figure-all-bins/fig12_equiv_lowE_maps.png
  data/figure-all-bins/fig13_equiv_highE_maps.png
  data/figure-all-bins/fig11_13_equiv_summary.txt
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

DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results" / "mcmc_allbins"
OUT_DIR = DATA_DIR / "figure-all-bins"
OUT_DIR.mkdir(parents=True, exist_ok=True)

L_MAX = 60.0
B_MIN = 10.0
B_MAX = 60.0

FIG12_BINS = [0, 1, 2, 4]   # 0-indexed -> Bin1,2,3,5 = 1.51/2.55/4.31/12.29 GeV
FIG13_BINS = [6, 7, 8, 9]   # 0-indexed -> Bin7,8,9,10 = 35.06/59.22/100.02/168.93 GeV


def load_bin_fit(ib):
    with open(RESULTS_DIR / f"mcmc_bin{ib+1:02d}.json") as f:
        return json.load(f)


def compute_bin_maps(ib, df_all, expmaps, j_map, nfw_norm, bubble_counts_bin3,
                      expmap_bubble_bin, loop_shell1, loop_shell2):
    """mcmc_fit_all_bins.fit_one_bin() と同じテンプレート・マスク定義を用いて、
    保存済みベストフィット値(with-halo=MCMC中央値, no-halo=その場で多点始動再最適化)
    から4種類のマップ(no-halo残差, with-halo残差, ハローモデル, フィット後残差)を作る。"""
    emin, emax = mfa.BIN_EDGES[ib], mfa.BIN_EDGES[ib + 1]
    sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
    counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])

    masked_counts, n_masked = _sub.mask_point_sources(counts.copy())
    valid = ~np.isnan(masked_counts)
    valid &= (np.abs(mfa.BG) >= B_MIN) & (np.abs(mfa.BG) <= B_MAX)

    galprop_flux_i = _sub._load_galprop_template(emin, emax)
    t = mfa.build_templates_for_bin(
        ib, counts, expmaps[ib], galprop_flux_i,
        bubble_counts_bin3, expmap_bubble_bin, j_map, nfw_norm,
        loop_shell1, loop_shell2,
    )
    t["valid"] = valid

    fit = load_bin_fit(ib)
    p = fit["params"]
    with_halo = [p["f_gal"]["median"], p["f_loopI_a"]["median"], p["f_loopI_b"]["median"],
                 p["f_fb"]["median"], p["f_halo"]["median"]]

    # no-halo(4パラメータ)側は json に保存されていないためその場で再最適化する
    c_mean = max(counts[valid].mean(), 1e-6)
    x0_la = 0.3 * c_mean / max(t["loopI_a"][valid].mean(), 1e-30)
    x0_lb = 0.3 * c_mean / max(t["loopI_b"][valid].mean(), 1e-30)
    x0_nohalo = [1.0, x0_la, x0_lb, 0.5]

    def neg_ll_nohalo(p4):
        if any(x < 0 for x in p4):
            return 1e10
        return -mfa.log_likelihood(list(p4) + [0.0], counts, t)

    res_nh = mfa._multistart_minimize(neg_ll_nohalo, x0_nohalo)
    no_halo = list(res_nh.x) + [0.0]

    mu_nohalo_bg = mfa.make_mu(no_halo, t)          # no-halo最適化パラメータでの背景モデル
    mu_withhalo_bg = mfa.make_mu(with_halo[:4] + [0.0], t)  # with-halo最適化パラメータ、ハロー項抜き
    halo_model = with_halo[4] * t["halo"]

    resid_nohalo = counts - mu_nohalo_bg
    resid_withhalo = counts - mu_withhalo_bg
    resid_after = resid_withhalo - halo_model

    for arr in (resid_nohalo, resid_withhalo, halo_model, resid_after):
        arr[~valid] = np.nan

    return dict(
        resid_nohalo=resid_nohalo, resid_withhalo=resid_withhalo,
        halo_model=halo_model, resid_after=resid_after,
        f_halo=with_halo[4], sig=fit["significance_sigma"] * np.sign(with_halo[4]),
        n_masked=n_masked,
    )


def robust_vlim(data, pct=98.0):
    finite = data[np.isfinite(data)]
    if finite.size == 0:
        return 1.0
    v = np.nanpercentile(np.abs(finite), pct)
    return v if v > 0 else 1.0


def plot_map(ax, data, title, vlim, cbar_label="counts/pixel"):
    im = ax.pcolormesh(_sub.L_BINS, _sub.B_BINS, data.T, cmap="RdBu_r",
                        vmin=-vlim, vmax=vlim, shading="flat")
    ax.set_xlim(L_MAX, -L_MAX)
    ax.set_ylim(-B_MAX, B_MAX)
    ax.axhspan(-B_MIN, B_MIN, color="gray", alpha=0.35, zorder=3)
    ax.set_xlabel("銀経 l [deg]", fontsize=9)
    ax.set_ylabel("銀緯 b [deg]", fontsize=9)
    ax.set_title(title, fontsize=10, fontweight="bold")
    ax.tick_params(labelsize=8)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="4%", pad=0.06)
    cb = ax.figure.colorbar(im, cax=cax)
    cb.set_label(cbar_label, fontsize=8)
    cb.ax.tick_params(labelsize=7)


def main():
    print("実測露出マップ読み込み中...")
    expmaps, exp_bin_centers = mfa.load_exposure_maps()
    print("イベントデータ読み込み中...")
    df_all = mfa.load_all_events()
    print("NFW J-factorマップ計算中(数十秒)...")
    j_map = mfa.nfw_j_map()
    nfw_norm, calib_info = mfa.calibrate_nfw_norm(expmaps[5], j_map)
    print("バブルテンプレート構築中(Bin3基準)...")
    bubble_counts_bin3 = mfa.build_bubble_counts_template(df_all)
    expmap_bubble_bin = expmaps[mfa.BUBBLE_BIN]
    print("Loop I幾何シェルテンプレート計算中...")
    loop_shell1, loop_shell2 = _sub.loop_i_shell_templates()

    summary_lines = [
        "# Totani (2025) Fig11-13 相当 マップ生成 サマリ (2026-07-13, MCMCベース再生成)",
        "# Bin  E_center[GeV]  f_halo(中央値)  有意度[σ](符号=f_halo符号)  point_source_masked",
    ]

    def do_bin(ib):
        r = compute_bin_maps(ib, df_all, expmaps, j_map, nfw_norm,
                              bubble_counts_bin3, expmap_bubble_bin,
                              loop_shell1, loop_shell2)
        summary_lines.append(
            f"  {ib+1:2d}  {mfa.BIN_CENTERS[ib]:9.2f}  {r['f_halo']:+.4e}  {r['sig']:+.3f}  {r['n_masked']}"
        )
        print(f"  Bin{ib+1}: f_halo={r['f_halo']:+.3e}  有意度={r['sig']:+.3f}σ")
        return r

    # ---- Fig11相当: Bin6 (20.76 GeV) 2x2 ----
    print("Bin6 (20.76 GeV) 計算中...")
    r6 = do_bin(5)
    vlim6 = robust_vlim(r6["resid_withhalo"])
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 10.5))
    plot_map(axes[0, 0], r6["resid_nohalo"],
             "① ハロー無しフィット残差\n(no-halo 4パラメータ最適化)", vlim6)
    plot_map(axes[0, 1], r6["resid_withhalo"],
             "② ハロー込みフィット残差\n(with-halo最適化, ハロー項抜き)", vlim6)
    plot_map(axes[1, 0], r6["halo_model"],
             f"③ ハローモデル (NFW-ρ²)\n(f_halo={r6['f_halo']:+.3f}, MCMC中央値)", vlim6)
    plot_map(axes[1, 1], r6["resid_after"],
             "④ フィット後残差\n(= ② − ③)", vlim6)
    fig.suptitle(
        "Totani (2025) Fig.11 相当: Bin6 (20.76 GeV) ハローモデル・残差マップ (MCMC同時フィット)\n"
        f"f_halo={r6['f_halo']:+.3f} (中央値), 有意度={r6['sig']:+.2f}σ",
        fontsize=11,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    out11 = OUT_DIR / "fig11_equiv_bin6_maps.png"
    fig.savefig(out11, dpi=150)
    plt.close(fig)
    print(f"Fig11相当マップを保存: {out11}")

    # ---- Fig12/13相当 ----
    for fig_no, bins_idx, fname, label_jp in (
        (12, FIG12_BINS, "fig12_equiv_lowE_maps.png", "21 GeV より低い4ビン"),
        (13, FIG13_BINS, "fig13_equiv_highE_maps.png", "21 GeV より高い4ビン"),
    ):
        print(f"Fig{fig_no}相当 ({label_jp}) 計算中...")
        fig, axes = plt.subplots(2, 2, figsize=(11.5, 10.5))
        for ax, ibin in zip(axes.flat, bins_idx):
            rb = do_bin(ibin)
            vlim_b = robust_vlim(rb["resid_withhalo"])
            plot_map(
                ax, rb["resid_withhalo"],
                f"Bin{ibin+1} ({mfa.BIN_CENTERS[ibin]:.2f} GeV)\n"
                f"ハロー込み残差 (f_halo={rb['f_halo']:+.2e}, {rb['sig']:+.2f}σ)",
                vlim_b,
            )
        fig.suptitle(
            f"Totani (2025) Fig.{fig_no} 相当: {label_jp}のハロー込み残差マップ (MCMC同時フィット)\n"
            "(各パネル独立のカラースケール、1deg×1degピクセル)",
            fontsize=11,
        )
        fig.tight_layout(rect=[0, 0, 1, 0.92])
        out_fig = OUT_DIR / fname
        fig.savefig(out_fig, dpi=150)
        plt.close(fig)
        print(f"Fig{fig_no}相当マップを保存: {out_fig}")

    out_summary = OUT_DIR / "fig11_13_equiv_summary.txt"
    with open(out_summary, "w") as f:
        f.write("\n".join(summary_lines) + "\n")
    print(f"サマリを保存: {out_summary}")


if __name__ == "__main__":
    main()
