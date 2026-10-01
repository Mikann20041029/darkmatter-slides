#!/usr/bin/env python3
"""
Totani (2025) の13エネルギービンごとに天球マップを出力する

ビン設定: 対数等間隔13ビン、中心 1.51〜814 GeV
出力: data/figure-week9-phase0/skymap_bin01_1.51GeV.png 〜 skymap_bin13_814GeV.png
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
OUTPUT_DIR = DATA_DIR / "figure-week9-phase0"

PIXEL_DEG = 1.0
L_BINS = np.arange(-60, 60 + PIXEL_DEG, PIXEL_DEG)
B_BINS = np.arange(-60, 60 + PIXEL_DEG, PIXEL_DEG)

# --- Totani 13ビン ---
N_BINS = 13
centers = np.logspace(np.log10(1.51), np.log10(814.0), N_BINS)
ratio_step = (814.0 / 1.51) ** (1.0 / (N_BINS - 1))
e_low  = 1.51 / ratio_step**0.5
e_high = 814.0 * ratio_step**0.5
edges = np.concatenate([[e_low],
                        np.sqrt(centers[:-1] * centers[1:]),
                        [e_high]])


def plot_skymap_bin(df, bin_idx, emin, emax, center):
    sel = df[(df["energy_GeV"] >= emin) & (df["energy_GeV"] < emax)]
    n = len(sel)

    counts, _, _ = np.histogram2d(sel["l_deg"], sel["b_deg"],
                                   bins=[L_BINS, B_BINS])

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.axhspan(-10, 10, color="gray", alpha=0.25, label="Galactic plane mask |b|<10 deg")

    vmin = max(counts.max() * 0.01, 0.5) if counts.max() > 0 else 0.5
    im = ax.pcolormesh(L_BINS, B_BINS, counts.T,
                       norm=mcolors.LogNorm(vmin=vmin),
                       cmap="inferno")

    fig.colorbar(im, ax=ax, label="Photon count / pixel")
    ax.set_xlabel("Galactic longitude l [deg]", fontsize=13)
    ax.set_ylabel("Galactic latitude b [deg]", fontsize=13)
    ax.set_title(
        f"Fermi-LAT Raw Count Map  |  Bin {bin_idx:02d}/13  |  "
        f"Center: {center:.2f} GeV  ({emin:.3f}–{emax:.3f} GeV)\n"
        f"w009-w018 (10 weeks)  |  {n:,} events  |  pixel={PIXEL_DEG} deg",
        fontsize=11
    )
    ax.set_xlim(-60, 60)
    ax.set_ylim(-60, 60)
    ax.invert_xaxis()
    ax.legend(loc="upper right", fontsize=9)
    ax.axhline( 10, color="white", lw=0.5, ls="--")
    ax.axhline(-10, color="white", lw=0.5, ls="--")

    out = OUTPUT_DIR / f"skymap_bin{bin_idx:02d}_{center:.2f}GeV.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Bin{bin_idx:02d} ({center:6.2f} GeV): {n:5,} events → {out.name}")


def main():
    df = pd.read_csv(CSV_PATH, comment="#")
    print(f"読み込み: {len(df):,} イベント\n")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for i in range(N_BINS):
        plot_skymap_bin(df, i + 1, edges[i], edges[i + 1], centers[i])

    print(f"\n全{N_BINS}枚完了。{OUTPUT_DIR} を確認してください。")


if __name__ == "__main__":
    main()
