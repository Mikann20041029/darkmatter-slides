"""
矮小銀河5天体 — テンプレートスカイマップ（Totani Fig.14 相当）

各天体の周辺 ±6° で：
  (a) 等方背景テンプレート（一定値）
  (b) GALPROP 銀河拡散放射テンプレート（gll_iem_v07.fits）
  (c) 既知点源テンプレート（4FGL-DR2, PSF 畳み込み近似）

出力: data/figure-dwarfs/<name>/templates_fig14_<name>.png
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
from astropy.io import fits as afits
from astropy.wcs import WCS
from scipy.ndimage import map_coordinates, gaussian_filter
from astropy.coordinates import SkyCoord
import astropy.units as u

BASE     = _pathlib.Path(__file__).resolve().parent.parent
DATA_DIR = BASE / "data"
REF_DIR  = BASE / "ref"
OUT_DIR  = DATA_DIR / "figure-dwarfs"

GALPROP_PATH = REF_DIR / "gll_iem_v07.fits"
CATALOG_PATH = REF_DIR / "gll_psc_v35_dr4.fit"  # 4FGL-DR4(14年分); 旧DR2(12年分)から2026-07-10更新

EMIN, EMAX, ECEN = 15.35, 28.07, 20.76  # Bin6 [GeV]
PIXEL_DEG = 0.5
ROI_DEG   = 6.0

TARGETS = {
    "draco":      {"l": 86.37,  "b": 34.72,  "label": "Draco"},
    "sculptor":   {"l": 287.53, "b": -83.16, "label": "Sculptor"},
    "ursa_minor": {"l": 104.97, "b": 44.80,  "label": "Ursa Minor"},
    "segue1":     {"l": 220.48, "b": 50.43,  "label": "Segue 1"},
    "coma_ber":   {"l": 241.89, "b": 83.61,  "label": "Coma Ber."},
}

C_BG = "#05051A"
CMAP_HOT = "hot"
CMAP_DIV = LinearSegmentedColormap.from_list("totani_div", [
    (0.0, "#00FFFF"), (0.17, "#0000FF"), (0.33, "#000080"),
    (0.45, "#000020"), (0.50, "#000000"), (0.55, "#200000"),
    (0.67, "#800000"), (0.83, "#FF4400"), (0.92, "#FFCC00"),
    (1.0,  "#FFFF00"),
])


def load_galprop_patch(l_cen, b_cen, roi=ROI_DEG, pix=PIXEL_DEG):
    """GALPROP テンプレートから天体周辺パッチを抽出"""
    with afits.open(GALPROP_PATH) as hdul:
        hdr  = hdul[0].header
        data = hdul[0].data   # (28, 1440, 2880)
        try:
            energies_mev = hdul[1].data["Energy"].flatten()
        except Exception:
            n_e   = hdr["NAXIS3"]
            e_ref = hdr.get("CRVAL3", 100.0)
            e_dlt = hdr.get("CDELT3", 0.0)
            energies_mev = e_ref * (10 ** (e_dlt * np.arange(n_e)))

        emid_mev = (EMIN + EMAX) / 2 * 1000.0
        e_idx    = int(np.argmin(np.abs(energies_mev - emid_mev)))
        slice2d  = data[e_idx]   # (1440, 2880) = (b, l)

        wcs = WCS(hdr, naxis=2)
        l_arr = np.arange(l_cen - roi, l_cen + roi + pix, pix)
        b_arr = np.arange(b_cen - roi, b_cen + roi + pix, pix)
        l_c   = (l_arr[:-1] + l_arr[1:]) / 2
        b_c   = (b_arr[:-1] + b_arr[1:]) / 2
        LG, BG = np.meshgrid(l_c, b_c, indexing="ij")

        # WCS でピクセル座標に変換
        px, py = wcs.all_world2pix(LG.ravel(), BG.ravel(), 0)
        vals = map_coordinates(slice2d, [py, px], order=1, mode="nearest")
        patch = vals.reshape(LG.shape)
        return l_c, b_c, patch


def load_point_sources(l_cen, b_cen, roi=ROI_DEG, pix=PIXEL_DEG):
    """4FGL-DR2 点源の位置マップ（PSF 畳み込み近似）"""
    with afits.open(CATALOG_PATH) as hdul:
        cat = hdul[1].data
        l_src = cat["GLON"].astype(float)
        b_src = cat["GLAT"].astype(float)

    mask = ((np.abs(l_src - l_cen) < roi + 1) &
            (np.abs(b_src - b_cen) < roi + 1))
    l_sel = l_src[mask]
    b_sel = b_src[mask]

    l_arr = np.arange(l_cen - roi, l_cen + roi + pix, pix)
    b_arr = np.arange(b_cen - roi, b_cen + roi + pix, pix)
    l_c   = (l_arr[:-1] + l_arr[1:]) / 2
    b_c   = (b_arr[:-1] + b_arr[1:]) / 2

    patch = np.zeros((len(l_c), len(b_c)))
    for ls, bs in zip(l_sel, b_sel):
        il = np.argmin(np.abs(l_c - ls))
        ib = np.argmin(np.abs(b_c - bs))
        if 0 <= il < len(l_c) and 0 <= ib < len(b_c):
            patch[il, ib] += 1.0

    # PSF 近似: 20 GeV の PSF ≈ 0.2° → σ = 0.2°/pix
    psf_sigma = 0.2 / pix
    patch = gaussian_filter(patch, sigma=psf_sigma)
    return l_c, b_c, patch


def plot_templates_fig14(name, cfg):
    l_cen = cfg["l"]
    b_cen = cfg["b"]

    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5), facecolor=C_BG)
    fig.suptitle(f"{cfg['label']} — テンプレートスカイマップ（Totani Fig.14 相当）\n"
                 f"Bin6 (20.76 GeV) | 0.5°/pix | 白丸=ON領域(2°), 十字=天体中心",
                 color="white", fontsize=13)

    panels = []

    # (a) 等方背景テンプレート（一定値マップ）
    l_arr = np.arange(l_cen - ROI_DEG, l_cen + ROI_DEG + PIXEL_DEG, PIXEL_DEG)
    b_arr = np.arange(b_cen - ROI_DEG, b_cen + ROI_DEG + PIXEL_DEG, PIXEL_DEG)
    l_c = (l_arr[:-1] + l_arr[1:]) / 2
    b_c = (b_arr[:-1] + b_arr[1:]) / 2
    iso_patch = np.ones((len(l_c), len(b_c))) * 2.443   # 等方背景レベル
    panels.append(("(a) 等方背景テンプレート\n（一定値 = 2.443 cnt/pix）",
                   l_c, b_c, iso_patch, CMAP_HOT, False))

    # (b) GALPROP テンプレート
    try:
        l_c2, b_c2, gal_patch = load_galprop_patch(l_cen, b_cen)
        panels.append(("(b) GALPROP 銀河拡散放射\n（gll_iem_v07.fits, Bin6）",
                       l_c2, b_c2, gal_patch, CMAP_HOT, False))
    except Exception as e:
        print(f"  GALPROP エラー: {e}")
        panels.append(("(b) GALPROP [エラー]", l_c, b_c,
                       np.zeros_like(iso_patch), CMAP_HOT, False))

    # (c) 既知点源テンプレート
    try:
        l_c3, b_c3, ps_patch = load_point_sources(l_cen, b_cen)
        panels.append(("(c) 既知点源テンプレート\n（4FGL-DR2, PSF畳み込み近似）",
                       l_c3, b_c3, ps_patch, CMAP_HOT, False))
    except Exception as e:
        print(f"  点源エラー: {e}")
        panels.append(("(c) 点源 [エラー]", l_c, b_c,
                       np.zeros_like(iso_patch), CMAP_HOT, False))

    theta = np.linspace(0, 2*np.pi, 100)
    for ax, (title, lc, bc, patch, cmap, div) in zip(axes, panels):
        ax.set_facecolor(C_BG)
        fin = patch[np.isfinite(patch) & (patch > 0)]
        vmax = float(np.nanpercentile(fin, 99)) if len(fin) > 0 else 1.0
        vmax = max(vmax, 1e-20)

        if div:
            norm = mcolors.Normalize(vmin=-vmax, vmax=vmax)
        else:
            norm = mcolors.Normalize(vmin=0, vmax=vmax)

        im = ax.pcolormesh(lc, bc, patch.T, norm=norm, cmap=cmap, shading="auto")
        ax.plot(l_cen + 2.0*np.cos(theta), b_cen + 2.0*np.sin(theta),
                "w-", lw=1.2, alpha=0.8)
        ax.plot(l_cen, b_cen, "w+", ms=10, mew=2)
        cbar = plt.colorbar(im, ax=ax)
        cbar.ax.yaxis.set_tick_params(color="white", labelsize=8)
        plt.setp(cbar.ax.yaxis.get_ticklabels(), color="white", fontsize=8)
        ax.set_xlim(l_cen - ROI_DEG, l_cen + ROI_DEG)
        ax.set_ylim(b_cen - ROI_DEG, b_cen + ROI_DEG)
        ax.set_title(title, color="white", fontsize=11)
        ax.set_xlabel("銀経 l [deg]", color="white", fontsize=9)
        ax.set_ylabel("銀緯 b [deg]", color="white", fontsize=9)
        ax.tick_params(colors="white", labelsize=8)
        for sp in ax.spines.values(): sp.set_color("white")

    plt.tight_layout(pad=1.5)
    out_path = OUT_DIR / name / f"templates_fig14_{name}.png"
    (OUT_DIR / name).mkdir(exist_ok=True)
    plt.savefig(out_path, dpi=120, bbox_inches="tight", facecolor=C_BG)
    plt.close()
    print(f"  → {out_path}")


def main():
    print("テンプレートマップ（Totani Fig.14 相当）生成中...\n")
    for name, cfg in TARGETS.items():
        print(f"--- {cfg['label']} ---")
        plot_templates_fig14(name, cfg)
        print()
    print("完了。")


if __name__ == "__main__":
    main()
