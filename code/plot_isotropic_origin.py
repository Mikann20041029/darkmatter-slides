"""
スライド21用: 等方背景レベル 2.443 cnt/pix の根拠図（3パネル）

左: Bin6スカイマップ（|b|≥50° のシアン帯を強調）
中: 銀緯ごとの平均カウント（b プロファイル）
右: |b|≥50° ピクセルのカウント数分布（ヒストグラム、x=0-20 にズーム）

出力: data/figure-rinko/fig_isotropic_origin.png
"""
import pathlib as _pathlib

import sys
sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))

import numpy as np
import pandas as pd
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"

import plot_skymap_all_subtracted as _sub

BASE    = _pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = BASE / "data/figure-rinko"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BIN6_EMIN, BIN6_EMAX = 15.35, 28.07

C_BG = "#05051A"

CMAP_DIV = LinearSegmentedColormap.from_list("totani_div", [
    (0.000, "#00FFFF"), (0.170, "#0000FF"), (0.330, "#000080"),
    (0.450, "#000020"), (0.500, "#000000"), (0.550, "#200000"),
    (0.670, "#800000"), (0.830, "#FF4400"), (0.920, "#FFCC00"),
    (1.000, "#FFFF00"),
])

def main():
    print("データ読み込み中...")
    df = pd.read_csv(BASE / "data/CSV/filtered_events_week780.csv",
                     comment="#", low_memory=False)
    df = df[(df.b_deg.abs() >= 10) & (df.b_deg.abs() <= 60) &
            (df.l_deg.abs() <= 60)]

    sel = df[(df.energy_GeV >= BIN6_EMIN) & (df.energy_GeV < BIN6_EMAX)]
    raw, _, _ = np.histogram2d(sel.l_deg, sel.b_deg,
                                bins=[_sub.L_BINS, _sub.B_BINS])
    raw = raw.astype(float)

    L_C = ((_sub.L_BINS[:-1] + _sub.L_BINS[1:]) / 2)
    B_C = ((_sub.B_BINS[:-1] + _sub.B_BINS[1:]) / 2)
    B_ABS = np.abs(B_C)
    iso_mask = B_ABS >= 50

    iso_level = raw[:, iso_mask].mean()
    iso_pixels = raw[:, iso_mask].ravel()
    print(f"  iso_level = {iso_level:.4f} cnt/pix")
    print(f"  N_iso_pix = {len(iso_pixels)},  sigma={iso_pixels.std():.3f}")

    # ─── 図作成 ─────────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(18, 6), facecolor=C_BG)
    fig.suptitle(
        f"① 等方背景レベル {iso_level:.3f} cnt/pix の根拠 "
        f"— |b|≥50° の平均カウント数\n"
        f"Bin 6（20.76 GeV）| 780週 Fermi-LAT | ROI: |l|≤60°, |b|=10°–60°",
        color="white", fontsize=14, y=1.01
    )
    ax1, ax2, ax3 = fig.subplots(1, 3, gridspec_kw={"width_ratios": [3, 2, 2]})

    # ─── パネル1: スカイマップ（Totani diverging cmap）──────────────────────
    ax1.set_facecolor(C_BG)
    fin = raw[np.isfinite(raw)]
    vmax = float(np.nanpercentile(np.abs(fin), 99.5))
    ax1.pcolormesh(L_C, B_C, raw.T,
                   norm=mcolors.LogNorm(vmin=max(fin[fin>0].min(),0.1), vmax=vmax),
                   cmap="hot", shading="auto")

    # |b|≥50° 帯をシアンで強調
    ax1.axhspan( 50,  60, color="#00FFFF", alpha=0.25, label="|b|≥50°（等方背景推定域）")
    ax1.axhspan(-60, -50, color="#00FFFF", alpha=0.25)

    ax1.set_xlim(60, -60)
    ax1.set_ylim(-60, 60)
    ax1.set_xlabel("銀経 l [deg]", color="white", fontsize=11)
    ax1.set_ylabel("銀緯 b [deg]", color="white", fontsize=11)
    ax1.tick_params(colors="white")
    for sp in ax1.spines.values(): sp.set_color("white")
    ax1.set_title(f"生データ（Bin6: 20.76 GeV）\nシアン帯: |b|≥50°（等方背景推定域）",
                  color="white", fontsize=11)
    ax1.axhline( 50, color="#00FFFF", lw=1.5, ls="--")
    ax1.axhline(-50, color="#00FFFF", lw=1.5, ls="--")
    leg1 = ax1.legend(loc="lower right", fontsize=9, framealpha=0.3)
    for text in leg1.get_texts(): text.set_color("white")

    # ─── パネル2: bプロファイル（銀緯ごとの平均カウント）──────────────────
    ax2.set_facecolor(C_BG)
    b_mean = raw.mean(axis=0)  # l方向平均
    ax2.plot(b_mean, B_C, color="#FFCC00", lw=1.5)
    ax2.axhline( 50, color="#00FFFF", lw=1.2, ls="--", alpha=0.8)
    ax2.axhline(-50, color="#00FFFF", lw=1.2, ls="--", alpha=0.8)
    ax2.axvline(iso_level, color="#FF4400", lw=1.5, ls="-",
                label=f"等方背景レベル = {iso_level:.3f} cnt/pix")
    ax2.axvspan(0, iso_level, color="#FF4400", alpha=0.1)

    ax2.set_xlabel("銀緯方向の平均カウント数 / pixel", color="white", fontsize=10)
    ax2.set_ylabel("銀緯 b [deg]", color="white", fontsize=10)
    ax2.tick_params(colors="white")
    for sp in ax2.spines.values(): sp.set_color("white")
    ax2.set_ylim(-60, 60)
    ax2.set_title("銀緯ごとの平均カウント数\n（l 方向に平均）", color="white", fontsize=11)
    leg2 = ax2.legend(loc="upper right", fontsize=9, framealpha=0.3)
    for text in leg2.get_texts(): text.set_color("white")
    ax2.text(iso_level * 1.05, 52,
             f"|b|≥50°\n平均 = {iso_level:.3f}", color="#FF4400", fontsize=9)
    ax2.text(iso_level * 0.1, -58,
             "コード: level = counts[:, B_ABS>=50].mean()\n"
             "[Bin6のデータから直接計算 — フィッティングではない]",
             color="#AAAAAA", fontsize=7.5, va="bottom")

    # ─── パネル3: ヒストグラム（x軸 0-20 にズーム）────────────────────────
    ax3.set_facecolor(C_BG)

    N_pix = len(iso_pixels)
    sigma = iso_pixels.std()

    # x軸は0-20にズーム（外れ値を別途アノテート）
    XMAX = 20
    zoom_pix = iso_pixels[iso_pixels <= XMAX]
    outliers  = iso_pixels[iso_pixels > XMAX]

    counts_h, edges_h = np.histogram(iso_pixels, bins=np.arange(0, XMAX+2, 1))
    ax3.bar(edges_h[:-1], counts_h, width=1, align="edge",
            color="#FF8800", alpha=0.8, edgecolor="#FFCC00", lw=0.5)

    ax3.axvline(iso_level, color="#FF4400", lw=2, ls="-",
                label=f"平均 = {iso_level:.3f}")
    ax3.axvline(iso_level - sigma, color="#FFCC00", lw=1.2, ls="--", alpha=0.7)
    ax3.axvline(iso_level + sigma, color="#FFCC00", lw=1.2, ls="--", alpha=0.7,
                label=f"±1σ = ±{sigma:.3f}")

    ax3.set_xlabel("カウント数 / pixel", color="white", fontsize=10)
    ax3.set_ylabel("ピクセル数", color="white", fontsize=10)
    ax3.tick_params(colors="white")
    for sp in ax3.spines.values(): sp.set_color("white")
    ax3.set_xlim(0, XMAX)
    ax3.set_title(
        f"|b|≥50° のカウント数分布\n"
        f"（N={N_pix} pix, 平均={iso_level:.3f}, σ={sigma:.3f}）",
        color="white", fontsize=11
    )
    leg3 = ax3.legend(loc="upper right", fontsize=9, framealpha=0.3)
    for text in leg3.get_texts(): text.set_color("white")

    # 外れ値注記
    if len(outliers) > 0:
        ax3.text(XMAX * 0.95, ax3.get_ylim()[1] * 0.85,
                 f"※ {len(outliers)} pix が表示範囲外\n"
                 f"（max={int(outliers.max())} cnt: 点源）",
                 color="#00FFFF", fontsize=8, ha="right", va="top")
        # 縦矢印で外れ値を示す
        ax3.annotate("→ 点源ピクセル\nを除外してx軸縮小",
                     xy=(XMAX, counts_h[-1]+5), xytext=(XMAX*0.7, counts_h[0]*0.6),
                     color="#00FFFF", fontsize=7, arrowprops={"arrowstyle":"->","color":"#00FFFF"})

    fig.tight_layout(pad=1.5)
    out = OUT_DIR / "fig_isotropic_origin.png"
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=C_BG)
    plt.close()
    print(f"  → {out}")
    return str(out)

if __name__ == "__main__":
    main()
