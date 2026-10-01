#!/usr/bin/env python3
"""
等方背景放射（Isotropic background）を差し引いた13ビン天球マップを生成する

推定方法:
  銀緯 50°<=|b|<=60° の領域（銀河から最も遠い帯）の
  平均カウント/ピクセルを等方フロアとして各ピクセルから引く。

出力: data/figure-week9-isotropic/
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
import matplotlib
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"

DATA_DIR   = Path(__file__).resolve().parent.parent / "data"
CSV_PATH   = DATA_DIR / "CSV" / "filtered_events.csv"
OUTPUT_DIR = DATA_DIR / "figure-week9-isotropic"

PIXEL_DEG = 1.0
L_BINS = np.arange(-60, 60 + PIXEL_DEG, PIXEL_DEG)
B_BINS = np.arange(-60, 60 + PIXEL_DEG, PIXEL_DEG)
B_CENTERS = (B_BINS[:-1] + B_BINS[1:]) / 2

# 等方フロア推定に使う帯（銀河から最も遠い）
ISO_B_MIN = 50.0
ISO_B_MAX = 60.0

# Totani 13ビン
N_BINS = 13
centers = np.logspace(np.log10(1.51), np.log10(814.0), N_BINS)
ratio_step = (814.0 / 1.51) ** (1.0 / (N_BINS - 1))
e_low  = 1.51 / ratio_step**0.5
e_high = 814.0 * ratio_step**0.5
edges  = np.concatenate([[e_low],
                         np.sqrt(centers[:-1] * centers[1:]),
                         [e_high]])


def plot_bin(df, bin_idx, emin, emax, center):
    sel = df[(df["energy_GeV"] >= emin) & (df["energy_GeV"] < emax)]

    counts, _, _ = np.histogram2d(sel["l_deg"], sel["b_deg"],
                                   bins=[L_BINS, B_BINS])

    # 等方フロア = 高銀緯帯（50<=|b|<=60）の平均カウント/ピクセル
    iso_mask = (np.abs(B_CENTERS) >= ISO_B_MIN) & (np.abs(B_CENTERS) <= ISO_B_MAX)
    iso_level = counts[:, iso_mask].mean()

    counts_sub = counts - iso_level   # 全ピクセルから定数を引く

    n_pos = (counts_sub > 0).sum()
    print(f"  Bin{bin_idx:02d} ({center:6.2f} GeV): "
          f"iso_level={iso_level:.3f} cnt/pix  |  {len(sel):,} events  |  "
          f"正ピクセル数 {n_pos}/{counts_sub.size}")

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.axhspan(-10, 10, color="gray", alpha=0.25,
               label="Galactic plane mask |b|<10 deg")

    pos = counts_sub.copy()
    pos[pos <= 0] = np.nan   # 0以下はグレー表示

    vmin = max(np.nanmax(pos) * 0.01, 0.1) if np.any(~np.isnan(pos)) else 0.1
    im = ax.pcolormesh(L_BINS, B_BINS, pos.T,
                       norm=mcolors.LogNorm(vmin=vmin),
                       cmap="inferno")

    # 等方以下（差し引き後<=0）のピクセルをグレーで重ね描き
    neg = counts_sub.copy()
    neg[neg > 0] = np.nan
    ax.pcolormesh(L_BINS, B_BINS, neg.T * 0 + 1,
                  cmap="Greys", alpha=0.4, vmin=0, vmax=2)

    fig.colorbar(im, ax=ax, label="(Counts - Isotropic floor) / pixel")
    ax.set_xlabel("Galactic longitude l [deg]", fontsize=13)
    ax.set_ylabel("Galactic latitude b [deg]", fontsize=13)
    ax.set_title(
        f"Fermi-LAT  [Raw − Isotropic background]  |  "
        f"Bin {bin_idx:02d}/13  |  Center: {center:.2f} GeV "
        f"({emin:.3f}–{emax:.3f} GeV)\n"
        f"Isotropic floor = {iso_level:.3f} cnt/pix "
        f"(mean of 50≤|b|≤60 deg)  |  {len(sel):,} events",
        fontsize=10
    )
    ax.set_xlim(-60, 60)
    ax.set_ylim(-60, 60)
    ax.invert_xaxis()
    ax.legend(loc="upper right", fontsize=9)
    ax.axhline( 10, color="white", lw=0.5, ls="--")
    ax.axhline(-10, color="white", lw=0.5, ls="--")

    out = OUTPUT_DIR / f"skymap_bin{bin_idx:02d}_{center:.2f}GeV_minus_iso.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main():
    df = pd.read_csv(CSV_PATH, comment="#")
    print(f"読み込み: {len(df):,} イベント\n")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for i in range(N_BINS):
        plot_bin(df, i + 1, edges[i], edges[i + 1], centers[i])

    print(f"\n全{N_BINS}枚完了 → {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
