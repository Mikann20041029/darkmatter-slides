#!/usr/bin/env python3
"""
Totani (2025) Section 2.1 に合わせた13エネルギービンのスペクトルプロット

ビン設定:
  - 13ビン、対数等間隔
  - ビン中心: 1.51 GeV (最小) 〜 814 GeV (最大)
  - ビン端: sqrt(ratio) を使って中心から計算
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
import matplotlib
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"

DATA_DIR   = Path(__file__).resolve().parent.parent / "data"
CSV_PATH   = DATA_DIR / "CSV" / "filtered_events.csv"
OUTPUT_DIR = DATA_DIR / "figure-week9-phase0"

# --- Totani の13ビン設定 ---
N_BINS   = 13
E_CENTER_MIN = 1.51    # GeV
E_CENTER_MAX = 814.0   # GeV

centers = np.logspace(np.log10(E_CENTER_MIN), np.log10(E_CENTER_MAX), N_BINS)

# ビン端: 隣り合うビン中心の幾何平均 + 両外側
ratio_step = (E_CENTER_MAX / E_CENTER_MIN) ** (1.0 / (N_BINS - 1))
e_low  = E_CENTER_MIN / ratio_step**0.5
e_high = E_CENTER_MAX * ratio_step**0.5
edges = np.concatenate([[e_low],
                        np.sqrt(centers[:-1] * centers[1:]),
                        [e_high]])

widths = np.diff(edges)   # 各ビンのエネルギー幅 [GeV]


def main():
    df = pd.read_csv(CSV_PATH, comment="#")
    print(f"読み込み: {len(df):,} イベント")

    counts, _ = np.histogram(df["energy_GeV"], bins=edges)

    # dN/dE: 光子数 / エネルギー幅
    dNdE = counts / widths

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # --- プロット ---
    fig, ax = plt.subplots(figsize=(9, 6))

    ax.step(edges[:-1], dNdE, where="post", color="steelblue", lw=1.5)
    ax.errorbar(centers, dNdE,
                xerr=[centers - edges[:-1], edges[1:] - centers],
                yerr=np.sqrt(counts) / widths,
                fmt="o", color="steelblue", ms=4, lw=1.2,
                label="Fermi-LAT (w009-w018, 10 weeks)")

    ax.axvline(20, color="red", ls="--", lw=1.2, label="20 GeV (Totani excess)")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Energy [GeV]", fontsize=13)
    ax.set_ylabel("dN/dE  [counts / GeV]", fontsize=13)
    ax.set_title(
        "Fermi-LAT Raw Energy Spectrum (Totani 13 log-bins)\n"
        f"ROI: |l|<=60 deg, 10<=|b|<=60 deg  |  {len(df):,} events",
        fontsize=12
    )
    ax.legend(fontsize=10)
    ax.grid(True, which="both", ls=":", alpha=0.5)

    out = OUTPUT_DIR / "energy_spectrum_13bins.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"保存: {out}")

    # --- ビン情報を表示 ---
    print(f"\n{'Bin':>4} {'Center[GeV]':>12} {'Edge_low':>10} {'Edge_high':>10} {'Counts':>8} {'dN/dE':>12}")
    for i in range(N_BINS):
        print(f"{i+1:>4} {centers[i]:>12.2f} {edges[i]:>10.3f} {edges[i+1]:>10.3f} {counts[i]:>8d} {dNdE[i]:>12.2f}")


if __name__ == "__main__":
    main()
