"""
galprop_comparison.py
GALPROP gll_iem_v07 と我々の指数関数近似を比較し、スペクトル図と偏差表を出力する。

出力:
  data/figure-galprop/galprop_comparison_spectra.png
  data/figure-galprop/deviation_table.txt
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
import matplotlib
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"
from astropy.io import fits
from scipy.optimize import curve_fit

# ---- パス設定 ----------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(ROOT, "data")
REF_DIR = os.path.join(ROOT, "ref")
OUT_DIR = os.path.join(DATA_DIR, "figure-galprop")
os.makedirs(OUT_DIR, exist_ok=True)

CSV_PATH = os.path.join(DATA_DIR, "CSV", "filtered_events_week780.csv")
FITS_PATH = os.path.join(REF_DIR, "gll_iem_v07.fits")

# ---- Totani 13ビン (GeV) -----------------------------------------------------
BIN_CENTERS = np.array([
    1.51, 2.55, 4.31, 7.28, 12.29, 20.76, 35.06,
    59.22, 100.02, 168.93, 285.33, 481.93, 814.00
])
# ビン境界: 対数中点を境界とする
BIN_EDGES = np.zeros(len(BIN_CENTERS) + 1)
BIN_EDGES[1:-1] = np.sqrt(BIN_CENTERS[:-1] * BIN_CENTERS[1:])
BIN_EDGES[0] = BIN_CENTERS[0] ** 2 / BIN_EDGES[1]
BIN_EDGES[-1] = BIN_CENTERS[-1] ** 2 / BIN_EDGES[-2]

# ---- ROI 定義 ----------------------------------------------------------------
L_MAX = 60.0   # deg
B_MIN = 10.0   # deg
B_MAX = 60.0   # deg
PIX = 1.0      # deg (我々の解析ピクセルサイズ)

# ---- GALPROP 読み込み --------------------------------------------------------
print("GALPROP FITS を読み込み中 (887 MB, 数十秒かかります)...")
hdul = fits.open(FITS_PATH, memmap=True)
gal_data = hdul[0].data          # shape: (28, 1440, 2880), 単位: cm⁻²s⁻¹sr⁻¹MeV⁻¹
gal_header = hdul[0].header
gal_energies_mev = hdul["ENERGIES"].data["energy"]  # MeV, shape: (28,)

# FITS 座標系: CRPIX1=1440.5, CRVAL1=0, CDELT1=0.125 → lon=0 が画像中央
# lon が [-180, 180) の範囲でインデックスを計算する関数
CDELT1 = gal_header["CDELT1"]   # 0.125 deg/pixel
CRPIX1 = gal_header["CRPIX1"]   # 1440.5
CDELT2 = gal_header["CDELT2"]   # 0.125 deg/pixel
CRPIX2 = gal_header["CRPIX2"]   # 721.0

def lon_to_xpix(lon_deg):
    """galactic longitude → FITS x pixel index (0-based, wrap-around 込み)"""
    # lon を [-180, 180) に正規化
    lon_norm = (lon_deg + 180.0) % 360.0 - 180.0
    xpix = (lon_norm / CDELT1 + CRPIX1 - 1).astype(int)
    xpix = xpix % gal_data.shape[2]
    return xpix

def lat_to_ypix(lat_deg):
    """galactic latitude → FITS y pixel index (0-based)"""
    ypix = (lat_deg / CDELT2 + CRPIX2 - 1).astype(int)
    ypix = np.clip(ypix, 0, gal_data.shape[1] - 1)
    return ypix

# ---- 我々の 13 ビンに対応する GALPROP フラックスを抽出 -----------------------
# ROI ピクセル格子を作成 (1° グリッド)
l_centers = np.arange(-59.5, 60.5, PIX)   # |l| <= 60
b_centers = np.concatenate([
    np.arange(-59.5, -9.5, PIX),           # -60 < b < -10
    np.arange(10.5, 60.5, PIX)             # 10 < b < 60
])
LL, BB = np.meshgrid(l_centers, b_centers)
LL_flat = LL.ravel()
BB_flat = BB.ravel()

# ROI マスク
roi_mask = (np.abs(LL_flat) <= L_MAX) & (np.abs(BB_flat) >= B_MIN) & (np.abs(BB_flat) <= B_MAX)
l_roi = LL_flat[roi_mask]
b_roi = BB_flat[roi_mask]

xpix = lon_to_xpix(l_roi)
ypix = lat_to_ypix(b_roi)

print("GALPROP ピクセル抽出中...")
# shape: (28, n_roi)
gal_roi = np.array([gal_data[ie, ypix, xpix] for ie in range(28)])  # cm⁻²s⁻¹sr⁻¹MeV⁻¹

# 13 ビン中心エネルギー (MeV) にログ補間
bin_centers_mev = BIN_CENTERS * 1e3  # GeV → MeV
log_gal_e = np.log(gal_energies_mev)
log_bin_e = np.log(bin_centers_mev)

# shape: (13, n_roi)
gal_roi_interp = np.zeros((13, gal_roi.shape[1]))
for i in range(gal_roi.shape[1]):
    log_flux = np.log(np.maximum(gal_roi[:, i], 1e-50))
    gal_roi_interp[:, i] = np.exp(np.interp(log_bin_e, log_gal_e, log_flux))

# ROI 平均フラックス (cm⁻²s⁻¹sr⁻¹MeV⁻¹)
galprop_mean = gal_roi_interp.mean(axis=1)

# ---- CSV データ読み込みと ROI ビニング ----------------------------------------
print("CSV データ読み込み中...")
df = pd.read_csv(CSV_PATH)

# 銀経を [-180, 180) に正規化
df["l_norm"] = ((df["l_deg"] + 180.0) % 360.0) - 180.0

# ROI フィルタ
roi = (
    (np.abs(df["l_norm"]) <= L_MAX) &
    (np.abs(df["b_deg"]) >= B_MIN) &
    (np.abs(df["b_deg"]) <= B_MAX)
)
df_roi = df[roi].copy()

# ---- 指数関数近似の計算 -------------------------------------------------------
# 各エネルギービンで:
#   1. |b| > 50° の平均を等方背景として差引
#   2. 残差を exp(-|b|/b0) でフィット
# ※ ここでは ROI 内ピクセルごとのカウント密度 (counts/sr) ではなく、
#   まず等方成分を推定し、GALPROP 比較用の近似スペクトルを導出する

# ピクセルソリッドアングル [sr]
pix_sr = (np.deg2rad(PIX)) ** 2

# 等方背景差引後の GALPROP 近似
# 高銀緯 (|b|>50°) のGALPROP平均を等方成分として推定
iso_mask = np.abs(b_roi) > 50.0
galprop_approx = np.zeros(13)
b0_vals = np.zeros(13)

for ibin in range(13):
    flux_roi = gal_roi_interp[ibin, :]
    flux_iso = flux_roi[iso_mask].mean()
    flux_residual = flux_roi - flux_iso

    # exp(-|b|/b0) フィット (flux_residual >= 0 のピクセルのみ)
    valid = flux_residual > 0
    if valid.sum() > 10:
        def exp_model(b_abs, A, b0):
            return A * np.exp(-b_abs / b0)
        try:
            popt, _ = curve_fit(
                exp_model,
                np.abs(b_roi[valid]),
                flux_residual[valid],
                p0=[flux_residual[valid].max(), 20.0],
                maxfev=5000
            )
            b0_vals[ibin] = popt[1]
            # ROI 平均近似値
            approx_vals = exp_model(np.abs(b_roi), *popt) + flux_iso
            galprop_approx[ibin] = approx_vals.mean()
        except RuntimeError:
            galprop_approx[ibin] = flux_roi.mean()
            b0_vals[ibin] = np.nan
    else:
        galprop_approx[ibin] = flux_roi.mean()
        b0_vals[ibin] = np.nan

hdul.close()

# ---- CSV カウント密度の計算 ---------------------------------------------------
# 1°ピクセルでビニングし、ROI内のカウント密度 (counts/pixel/sr) を計算
# ここでは単純にビン内イベント数を ROI ピクセル数×solid_angle で割る
n_roi_pixels = l_roi.size

csv_counts_per_sr = np.zeros(13)
for ibin in range(13):
    e_lo = BIN_EDGES[ibin]
    e_hi = BIN_EDGES[ibin + 1]
    n = ((df_roi["energy_GeV"] >= e_lo) & (df_roi["energy_GeV"] < e_hi)).sum()
    roi_area_sr = n_roi_pixels * pix_sr
    csv_counts_per_sr[ibin] = n / roi_area_sr if roi_area_sr > 0 else 0.0

# ---- 偏差計算 ----------------------------------------------------------------
deviation_pct = (galprop_approx - galprop_mean) / galprop_mean * 100.0

# ---- 偏差表の出力 ------------------------------------------------------------
table_path = os.path.join(OUT_DIR, "deviation_table.txt")
with open(table_path, "w") as f:
    f.write("# GALPROP vs 指数関数近似の偏差\n")
    f.write("# E_center[GeV]  GALPROP_mean[cm-2s-1sr-1MeV-1]  Approx_mean[cm-2s-1sr-1MeV-1]  Deviation[%]  b0[deg]\n")
    for i in range(13):
        f.write(
            f"{BIN_CENTERS[i]:8.2f}  {galprop_mean[i]:.4e}  {galprop_approx[i]:.4e}  "
            f"{deviation_pct[i]:+7.2f}  {b0_vals[i]:.2f}\n"
        )
print(f"偏差表を保存: {table_path}")

# ---- スペクトル比較図の出力 --------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))

# E² × flux に変換 [MeV cm⁻²s⁻¹sr⁻¹]
e2_galprop = bin_centers_mev ** 2 * galprop_mean
e2_approx = bin_centers_mev ** 2 * galprop_approx

ax.plot(BIN_CENTERS, e2_galprop, "b-o", ms=5, label="GALPROP (gll_iem_v07)", lw=1.5)
ax.plot(BIN_CENTERS, e2_approx, "r--s", ms=5, label=r"指数関数近似 ($e^{-|b|/b_0}$)", lw=1.5)

# CSV データはカウント/sr なので次元が異なる → 別軸に描画
ax2 = ax.twinx()
ax2.plot(BIN_CENTERS, csv_counts_per_sr, "g:^", ms=5, label="CSV カウント密度 (counts/sr)", lw=1.2)
ax2.set_ylabel("カウント密度 (counts sr$^{-1}$)", color="g", fontsize=10)
ax2.tick_params(axis="y", labelcolor="g")
ax2.set_yscale("log")

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Energy (GeV)", fontsize=12)
ax.set_ylabel(r"$E^2 \, dN/dE$ (MeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$)", fontsize=11)
ax.set_title("GALPROP vs 指数関数近似 (ROI: |l|≤60°, 10°≤|b|≤60°)", fontsize=11)

# 凡例を統合
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, fontsize=9, loc="lower left")

ax.grid(True, which="both", ls=":", alpha=0.5)
fig.tight_layout()
out_path = os.path.join(OUT_DIR, "galprop_comparison_spectra.png")
fig.savefig(out_path, dpi=150)
plt.close(fig)
print(f"スペクトル比較図を保存: {out_path}")
