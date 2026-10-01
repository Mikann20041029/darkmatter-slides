#!/usr/bin/env python3
"""
生のγ線カウントマップをプロット（何も差し引かない）

Totaniの解析領域: |l|<=60°, 10<=|b|<=60°
エネルギービン: 1-10 GeV, 10-100 GeV, 1-100 GeV（全体）
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
OUTPUT_DIR = DATA_DIR / "figure-week9-phase0"
CSV_PATH   = DATA_DIR / "CSV" / "filtered_events.csv"

# マップ解像度（Totaniは0.125°だが、10週のデータでは1°が見やすい）
PIXEL_DEG = 1.0
L_BINS = np.arange(-60, 60 + PIXEL_DEG, PIXEL_DEG)
B_BINS = np.arange(-60, 60 + PIXEL_DEG, PIXEL_DEG)

ENERGY_BANDS = [
    ("1-100GeV",  1.0,   100.0,  "All energies (1-100 GeV)"),
    ("1-10GeV",   1.0,    10.0,  "Low energy (1-10 GeV)"),
    ("10-100GeV", 10.0,  100.0,  "High energy (10-100 GeV)"),
]


def load_data() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH, comment="#")
    print(f"読み込み: {len(df):,} イベント")
    print(f"エネルギー範囲: {df['energy_GeV'].min():.2f} 〜 {df['energy_GeV'].max():.1f} GeV")
    return df


def plot_skymap(df: pd.DataFrame, emin: float, emax: float,
                label: str, tag: str) -> None:
    sel = df[(df["energy_GeV"] >= emin) & (df["energy_GeV"] < emax)]
    print(f"\n{label}: {len(sel):,} イベント")

    counts, _, _ = np.histogram2d(sel["l_deg"], sel["b_deg"],
                                   bins=[L_BINS, B_BINS])

    fig, ax = plt.subplots(figsize=(10, 8))

    ax.axhspan(-10, 10, color="gray", alpha=0.25, label="Galactic plane mask |b|<10 deg")

    im = ax.pcolormesh(L_BINS, B_BINS, counts.T,
                       norm=mcolors.LogNorm(vmin=max(counts.max()*0.01, 0.5)),
                       cmap="inferno")

    cbar = fig.colorbar(im, ax=ax, label="Photon count / pixel")
    ax.set_xlabel("Galactic longitude l [deg]", fontsize=13)
    ax.set_ylabel("Galactic latitude b [deg]", fontsize=13)
    ax.set_title(
        f"Fermi-LAT Raw Gamma-ray Count Map ({label})\n"
        f"w009-w018 (10 weeks), {len(sel):,} events, pixel={PIXEL_DEG} deg",
        fontsize=12
    )
    ax.set_xlim(-60, 60)
    ax.set_ylim(-60, 60)
    ax.invert_xaxis()   # 天文慣例: l は右が小さい
    ax.legend(loc="upper right", fontsize=9)

    ax.axhline(10,  color="white", lw=0.5, ls="--")
    ax.axhline(-10, color="white", lw=0.5, ls="--")

    out = OUTPUT_DIR / f"skymap_raw_{tag}.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  保存: {out}")


def main():
    df = load_data()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for tag, emin, emax, label in ENERGY_BANDS:
        plot_skymap(df, emin, emax, label, tag)

    print("\n全プロット完了。data/ フォルダの PNG を確認してください。")


if __name__ == "__main__":
    main()
