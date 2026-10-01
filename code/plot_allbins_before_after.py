#!/usr/bin/env python3
"""
data/figure-allbins-steps/ の文字化け(□)図14枚(13bin + グリッド)を再生成する。

【背景】
旧図はフォント設定(Noto Sans CJK JP)前のmatplotlibで生成されたため
日本語ラベルが文字化けしていた。生成元スクリプトは未コミットで紛失している
(commit 1eba76d のメッセージ参照)。フォント修正(commit 69b353a)は他の
16スクリプトのみ対象で、この図には適用されなかった。

本スクリプトは plot_skymap_all_subtracted.py の差し引きパイプライン
(Step0=生データ 〜 Step5=最終残差)を再利用し、各ビンの「差引前 vs 差引後」
2パネル比較図13枚 + 全13ビン差引後グリッド1枚(Bin6強調)を生成する。

【表示用マスク半径について】
本解析(all_bins_nfw_fit.py 等)のコア点源マスクは mask_point_sources()
(1ピクセルのみNaN化)を使用している。4FGL J1555.7+1111 (l=21.91°,
b=43.96°) のようにピクセル境界(b=44°)付近0.04°にある点源では、
PSF裾が隣接ピクセル(l=21.5°,b=44.5°)に漏れ"明るい正方形"アーチファクト
として残る(Bin4で残差256.5、Bin6で97.3 counts/pixel。詳細は
.dev/TODO.md の CRITICAL 項目参照)。
本スクリプトは表示用に限り mask_point_sources_wide(radius=1) で
3×3ピクセルマスクを適用しこのアーチファクトを視覚的に除去する。
コア解析側のマスク半径は変更していない。

出力: data/figure-allbins-steps/
  binNN_X.XXGeV_before_after.png  (13枚)
  all13bins_after_grid.png        (1枚)
"""
import sys
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import plot_skymap_all_subtracted as _sub

BASE     = Path(__file__).resolve().parent.parent
OUT_DIR  = BASE / "data/figure-allbins-steps"
CSV_PATH = BASE / "data/CSV/filtered_events_week780.csv"
C_BG     = "#05051A"

L_BINS, B_BINS = _sub.L_BINS, _sub.B_BINS
L_CENTERS, B_CENTERS = _sub.L_CENTERS, _sub.B_CENTERS
N_BINS, BIN_CENTERS, BIN_EDGES = _sub.N_BINS, _sub.BIN_CENTERS, _sub.BIN_EDGES

# Bin6 (20.76 GeV) のベースライン全ROI S/N (all_bins_nfw_fit.py 結果, slide53表より)
BIN6_SN = "+0.24σ"
HIGHLIGHT_BIN = 6  # 1-indexed


def mask_point_sources_wide(counts, radius=1):
    """表示用: 各4FGLカタログ点源の周囲 (2*radius+1)^2 ピクセルをNaN化する。

    コア解析の mask_point_sources() (半径0=1ピクセルのみ) とは異なる。
    """
    result = counts.copy()
    nl, nb = len(L_CENTERS), len(B_CENTERS)
    n_masked = 0
    for lc, bc in zip(_sub._CAT_L, _sub._CAT_B):
        il = int((lc - L_BINS[0]) / _sub.PIXEL_DEG)
        ib = int((bc - B_BINS[0]) / _sub.PIXEL_DEG)
        for di in range(-radius, radius + 1):
            for dj in range(-radius, radius + 1):
                ii, jj = il + di, ib + dj
                if 0 <= ii < nl and 0 <= jj < nb:
                    if not np.isnan(result[ii, jj]):
                        result[ii, jj] = np.nan
                        n_masked += 1
    return result, n_masked


def run_pipeline(df, emin, emax, bubble_template):
    """Step0(生データ)〜Step5(最終残差)を計算して返す"""
    sel = df[(df.energy_GeV >= emin) & (df.energy_GeV < emax)]
    s0, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[L_BINS, B_BINS])
    s0 = s0.astype(float)
    n_events = len(sel)

    s1, iso_lv = _sub.subtract_isotropic(s0.copy())
    s2, _, gal_label = _sub.subtract_galactic_diffuse(s1.copy(), emin, emax)
    s3, n_ps = mask_point_sources_wide(s2.copy(), radius=1)
    s4, bbl_A, _ = _sub.subtract_fermi_bubbles(s3.copy(), bubble_template)
    s5, li_in, li_out = _sub.subtract_loop_i(s4.copy())

    info = (f"iso={iso_lv:.3f} | {gal_label} | PS(3x3)={n_ps}px | "
            f"bubble_A={bbl_A:.3f} | loopI in={li_in:.3f} out={li_out:.3f}")
    return s0, s5, n_events, info


def panel_raw(ax, data, title):
    """Step0: 生データ (対数スケール inferno)"""
    ax.set_facecolor(C_BG)
    ax.axhspan(-10, 10, alpha=0.2, color="gray")
    d_pos = np.where(np.isfinite(data) & (data > 0), data, np.nan)
    vmax = np.nanpercentile(d_pos, 99.5)
    if not np.isfinite(vmax) or vmax <= 0:
        vmax = 1.0
    im = ax.pcolormesh(L_CENTERS, B_CENTERS, d_pos.T,
                        norm=mcolors.LogNorm(vmin=0.3, vmax=vmax),
                        cmap="inferno", shading="auto")
    cbar = plt.colorbar(im, ax=ax, extend="max")
    cbar.set_label("カウント / pixel（対数スケール）", color="white", fontsize=11)
    cbar.ax.yaxis.set_tick_params(color="white", labelsize=10)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color="white", fontsize=10)

    ax.set_xlim(60, -60)
    ax.set_ylim(-60, 60)
    ax.set_aspect("equal")
    ax.set_xlabel("銀経 l [deg]", color="white", fontsize=11)
    ax.set_ylabel("銀緯 b [deg]", color="white", fontsize=11)
    ax.tick_params(colors="white", labelsize=10)
    for sp in ax.spines.values():
        sp.set_color("white")
    ax.set_title(title, color="white", fontsize=12, pad=6)
    return cbar


def panel_residual(ax, data, title, fontsize_title=12, show_colorbar=True,
                    show_labels=True, highlight=False):
    """Step5: 最終残差 (正値=対数inferno、負値/NaN=灰点)"""
    ax.set_facecolor(C_BG)
    ax.axhspan(-10, 10, alpha=0.2, color="gray")
    d_pos = np.where(np.isfinite(data) & (data > 0), data, np.nan)
    vmax = np.nanpercentile(d_pos, 99.5) if np.any(np.isfinite(d_pos)) else 1.0
    if not np.isfinite(vmax) or vmax <= 0:
        vmax = 1.0
    vmin = 0.3
    im = ax.pcolormesh(L_CENTERS, B_CENTERS, d_pos.T,
                        norm=mcolors.LogNorm(vmin=vmin, vmax=max(vmax, vmin * 2)),
                        cmap="inferno", shading="auto")
    neg_mask = (~np.isfinite(data)) | (data <= 0)
    if neg_mask.any():
        ax.pcolormesh(L_CENTERS, B_CENTERS, np.where(neg_mask, 1.0, np.nan).T,
                       cmap="Greys_r", vmin=0, vmax=2, alpha=0.6, shading="auto")
    if show_colorbar:
        cbar = plt.colorbar(im, ax=ax, extend="max")
        cbar.set_label("残差カウント / pixel（対数スケール）", color="white", fontsize=11)
        cbar.ax.yaxis.set_tick_params(color="white", labelsize=10)
        plt.setp(cbar.ax.yaxis.get_ticklabels(), color="white", fontsize=10)

    ax.set_xlim(60, -60)
    ax.set_ylim(-60, 60)
    ax.set_aspect("equal")
    if show_labels:
        ax.set_xlabel("銀経 l [deg]", color="white", fontsize=11)
        ax.set_ylabel("銀緯 b [deg]", color="white", fontsize=11)
    ax.tick_params(colors="white", labelsize=9)
    edge_color = "#FFCC00" if highlight else "white"
    edge_width = 2.5 if highlight else 1.0
    for sp in ax.spines.values():
        sp.set_color(edge_color)
        sp.set_linewidth(edge_width)
    ax.set_title(title, color=edge_color if highlight else "white",
                  fontsize=fontsize_title, pad=4)


def make_before_after(idx, center, emin, emax, s0, s5, n_events, info, info_iso=None):
    fig, axes = plt.subplots(1, 2, figsize=(14, 7), facecolor=C_BG)
    fig.subplots_adjust(wspace=0.45)

    panel_raw(axes[0], s0,
              f"Step 0: 差引前（生データ）\n対数スケール")
    panel_residual(axes[1], s5,
                    f"Step 5: 差引後（最終残差）\n対数スケール、表示用に点源マスク半径3×3px")

    fig.suptitle(
        f"Bin {idx:02d}（{center:.2f} GeV, {emin:.3f}–{emax:.3f} GeV）  "
        f"差引前 vs 差引後  |  {n_events:,} events\n"
        f"ROI: |l|≤60°, |b|=10°–60°  |  {info}",
        color="white", fontsize=11, y=1.03,
    )
    out = OUT_DIR / f"bin{idx:02d}_{center:.2f}GeV_before_after.png"
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=C_BG)
    plt.close(fig)
    print(f"  -> {out.name}")


def make_grid(results):
    """全13ビンの Step5 最終残差を 4x4 グリッドで表示 (Bin6 強調)"""
    ncols, nrows = 4, 4
    fig, axes = plt.subplots(nrows, ncols, figsize=(13, 14.5), facecolor=C_BG)
    axes_flat = axes.ravel()

    for i, (idx, center, emin, emax, s0, s5, n_events, info) in enumerate(results):
        ax = axes_flat[i]
        is_hl = (idx == HIGHLIGHT_BIN)
        title = f"Bin {idx:02d} ({center:.2f} GeV)\n{n_events:,} events"
        if is_hl:
            title = f"★ Bin {idx:02d} ({center:.2f} GeV) ★\nNFW S/N = {BIN6_SN} (baseline)"
        panel_residual(ax, s5, title, fontsize_title=10,
                        show_colorbar=False, show_labels=False,
                        highlight=is_hl)

    for j in range(len(results), nrows * ncols):
        axes_flat[j].axis("off")
        axes_flat[j].set_facecolor(C_BG)

    fig.suptitle(
        "全13ビン: 5成分差し引き後の最終残差マップ (Step 5, 対数スケール)\n"
        f"★ Bin {HIGHLIGHT_BIN} (20.76 GeV) は全ROI NFWフィットで S/N = {BIN6_SN}（最大値）  |  "
        "表示用に点源マスク半径3×3px（コア解析は1px、詳細は.dev/TODO.md参照）",
        color="white", fontsize=12, y=0.998,
    )
    fig.subplots_adjust(hspace=0.55, wspace=0.25, top=0.93)
    out = OUT_DIR / "all13bins_after_grid.png"
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=C_BG)
    plt.close(fig)
    print(f"  -> {out.name}")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"CSV: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH, comment="#", low_memory=False)
    df = df[(df.b_deg.abs() >= 10) & (df.b_deg.abs() <= 60) & (df.l_deg.abs() <= 60)]
    print(f"  ROI events: {len(df):,}")

    print("Fermi Bubble テンプレート構築中...")
    bubble_template = _sub.build_fermi_bubble_template(df)

    results = []
    print("各ビン処理中...")
    for i in range(N_BINS):
        emin, emax, center = BIN_EDGES[i], BIN_EDGES[i + 1], BIN_CENTERS[i]
        s0, s5, n_events, info = run_pipeline(df, emin, emax, bubble_template)
        print(f"  Bin{i+1:02d} ({center:6.2f} GeV): {n_events:6,} events | {info}")
        results.append((i + 1, center, emin, emax, s0, s5, n_events, info))

    print("\n2パネル比較図13枚を生成中...")
    for (idx, center, emin, emax, s0, s5, n_events, info) in results:
        make_before_after(idx, center, emin, emax, s0, s5, n_events, info)

    print("\nグリッド図を生成中...")
    make_grid(results)

    print(f"\n完了: {OUT_DIR}")


if __name__ == "__main__":
    main()
