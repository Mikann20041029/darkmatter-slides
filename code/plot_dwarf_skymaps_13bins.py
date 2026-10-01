"""
矮小銀河5天体 × 全13ビン スカイマップ（Totani Fig.11-13 相当）

各天体について：
  - 全13ビンの ON/OFF 領域スカイマップ
  - Totani Fig.11: 「ハローなし残差」= 生データ（差し引き前）スカイマップ
  - Totani Fig.12/13: 低エネルギー/高エネルギービン別スカイマップ

出力:
  data/figure-dwarfs/<name>/skymaps13_low_<name>.png   (Bin1-6, Totani Fig.12相当)
  data/figure-dwarfs/<name>/skymaps13_high_<name>.png  (Bin7-13, Totani Fig.13相当)
  data/figure-dwarfs/<name>/skymap_bin6_<name>.png     (Bin6のみ, Totani Fig.11相当)
"""
import pathlib as _pathlib

import sys
sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))
import numpy as np
import pandas as pd
from pathlib import Path
import warnings; warnings.filterwarnings("ignore")
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"
from astropy.coordinates import SkyCoord
import astropy.units as u

BASE     = _pathlib.Path(__file__).resolve().parent.parent
DATA_DIR = BASE / "data"
OUT_DIR  = DATA_DIR / "figure-dwarfs"

N_BINS = 13
_centers = np.logspace(np.log10(1.51), np.log10(814.0), N_BINS)
_ratio   = (_centers[-1] / _centers[0]) ** (1 / (N_BINS - 1))
_edges   = np.concatenate([[1.51/_ratio**0.5],
                           np.sqrt(_centers[:-1]*_centers[1:]),
                           [814.0*_ratio**0.5]])
BIN_CENTERS = _centers
BIN_EDGES   = _edges

TARGETS = {
    "draco":      {"l": 86.37,  "b": 34.72,  "label": "Draco",      "dist_kpc": 76},
    "sculptor":   {"l": 287.53, "b": -83.16, "label": "Sculptor",   "dist_kpc": 86},
    "ursa_minor": {"l": 104.97, "b": 44.80,  "label": "Ursa Minor", "dist_kpc": 76},
    "segue1":     {"l": 220.48, "b": 50.43,  "label": "Segue 1",    "dist_kpc": 23},
    "coma_ber":   {"l": 241.89, "b": 83.61,  "label": "Coma Ber.",  "dist_kpc": 44},
}

C_BG = "#05051A"
CMAP_DIV = LinearSegmentedColormap.from_list("totani_div", [
    (0.0, "#00FFFF"), (0.17, "#0000FF"), (0.33, "#000080"),
    (0.45, "#000020"), (0.50, "#000000"), (0.55, "#200000"),
    (0.67, "#800000"), (0.83, "#FF4400"), (0.92, "#FFCC00"),
    (1.0,  "#FFFF00"),
])
ON_RAD   = 2.0
PIXEL_DEG = 0.5
ROI_DEG  = 6.0


def make_skymap_grid(df, l_cen, b_cen, roi=ROI_DEG, pix=PIXEL_DEG):
    """天体中心周辺の RA/Dec → 銀経/銀緯 グリッドにビニング"""
    l_bins = np.arange(l_cen - roi, l_cen + roi + pix, pix)
    b_bins = np.arange(b_cen - roi, b_cen + roi + pix, pix)
    l_c = (l_bins[:-1] + l_bins[1:]) / 2
    b_c = (b_bins[:-1] + b_bins[1:]) / 2

    # RA/Dec → 銀経/銀緯 変換
    sky = SkyCoord(ra=df.ra_deg.values*u.deg, dec=df.dec_deg.values*u.deg, frame="icrs")
    gal = sky.galactic
    l_arr = gal.l.deg
    b_arr = gal.b.deg

    counts, _, _ = np.histogram2d(l_arr, b_arr, bins=[l_bins, b_bins])
    return l_c, b_c, counts.astype(float), l_bins, b_bins


def plot_skymaps_for_target(name, cfg, df_all, out_dir, mode="low"):
    """low: Bin1-6（Totani Fig.12相当）, high: Bin7-13（Totani Fig.13相当）"""
    if mode == "low":
        bin_indices = range(0, 6)
        title_suffix = "低エネルギー (Bin1-6, 1.5–28 GeV)"
        fname = f"skymaps13_low_{name}.png"
    elif mode == "high":
        bin_indices = range(6, N_BINS)
        title_suffix = "高エネルギー (Bin7-13, 35–814 GeV)"
        fname = f"skymaps13_high_{name}.png"
    else:  # bin6 only
        bin_indices = [5]
        title_suffix = "Bin6 (20.76 GeV) — Totani Fig.11 相当"
        fname = f"skymap_bin6_{name}.png"

    n_plots = len(list(bin_indices))
    ncols = 3
    nrows = (n_plots + ncols - 1) // ncols

    fig, axes = plt.subplots(nrows, ncols,
                             figsize=(ncols*5, nrows*4.5),
                             facecolor=C_BG)
    if nrows == 1 and ncols > 1:
        axes = axes.reshape(1, -1)
    elif nrows > 1:
        pass
    axes_flat = axes.flatten() if hasattr(axes, 'flatten') else [axes]

    fig.suptitle(f"{cfg['label']}  {title_suffix}",
                 color="white", fontsize=13)

    l_cen = cfg["l"]
    b_cen = cfg["b"]

    for plot_idx, bin_idx in enumerate(bin_indices):
        ax = axes_flat[plot_idx]
        e_lo = BIN_EDGES[bin_idx]
        e_hi = BIN_EDGES[bin_idx + 1]
        e_cen = BIN_CENTERS[bin_idx]

        sel = df_all[(df_all.energy_GeV >= e_lo) & (df_all.energy_GeV < e_hi)]
        l_c, b_c, counts, l_bins, b_bins = make_skymap_grid(
            sel, l_cen, b_cen)

        ax.set_facecolor(C_BG)
        fin = counts[np.isfinite(counts)]
        vmax = float(np.nanpercentile(fin, 99)) if len(fin) else 5.0
        vmax = max(vmax, 1.0)

        im = ax.pcolormesh(l_c, b_c, counts.T,
                           norm=mcolors.Normalize(vmin=-vmax, vmax=vmax),
                           cmap=CMAP_DIV, shading="auto")
        # ON/OFF 領域の円
        theta = np.linspace(0, 2*np.pi, 100)
        ax.plot(l_cen + ON_RAD*np.cos(theta),
                b_cen + ON_RAD*np.sin(theta),
                "w-", lw=1.2, alpha=0.8)
        ax.plot(l_cen + 5.0*np.cos(theta),
                b_cen + 5.0*np.sin(theta),
                "w--", lw=0.8, alpha=0.5)
        ax.plot(l_cen, b_cen, "w+", ms=8, mew=1.5)

        plt.colorbar(im, ax=ax).ax.yaxis.set_tick_params(color="white", labelsize=7)
        ax.set_xlim(l_cen - ROI_DEG, l_cen + ROI_DEG)
        ax.set_ylim(b_cen - ROI_DEG, b_cen + ROI_DEG)
        ax.set_title(f"Bin{bin_idx+1}: {e_cen:.1f} GeV",
                     color="white", fontsize=9)
        ax.tick_params(colors="white", labelsize=7)
        for sp in ax.spines.values(): sp.set_color("white")

    # 余ったサブプロットを非表示
    for ax in axes_flat[n_plots:]:
        ax.set_visible(False)

    plt.tight_layout(pad=1.5)
    out = out_dir / name / fname
    (out_dir / name).mkdir(exist_ok=True)
    plt.savefig(out, dpi=120, bbox_inches="tight", facecolor=C_BG)
    plt.close()
    print(f"  → {out}")


def main():
    print("矮小銀河5天体 スカイマップ生成中...\n")

    for name, cfg in TARGETS.items():
        print(f"--- {cfg['label']} ---")
        csv_path = DATA_DIR / "CSV" / "dwarfs" / f"dwarf_{name}_780w.csv"
        if not csv_path.exists():
            print(f"  CSVなし → スキップ")
            continue

        # 列名確認
        df_all = pd.read_csv(csv_path, comment="#", low_memory=False)
        print(f"  列名: {list(df_all.columns[:8])}")

        # ra_deg/dec_deg列がない場合は l_deg/b_deg から変換
        if "ra_deg" not in df_all.columns:
            if "l_deg" in df_all.columns and "b_deg" in df_all.columns:
                gal = SkyCoord(l=df_all.l_deg.values*u.deg,
                               b=df_all.b_deg.values*u.deg, frame="galactic")
                icrs = gal.icrs
                df_all["ra_deg"]  = icrs.ra.deg
                df_all["dec_deg"] = icrs.dec.deg
            else:
                print(f"  座標列なし → スキップ")
                continue

        plot_skymaps_for_target(name, cfg, df_all, OUT_DIR, mode="low")
        plot_skymaps_for_target(name, cfg, df_all, OUT_DIR, mode="high")
        plot_skymaps_for_target(name, cfg, df_all, OUT_DIR, mode="bin6")
        print()

    print("完了。")


if __name__ == "__main__":
    main()
