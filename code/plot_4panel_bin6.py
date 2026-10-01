"""
Bin 6（20.76 GeV）の 4枚組スカイマップを生成。

レイアウト（2行×2列）:
  [左列: 元の範囲 ROI |l|≤60°, |b|=10°-60°]  [右列: 全球 |l|≤180°, |b|≤90°]
  行1: 差し引き前（生データ）
  行2: 差し引き後（ROI=5成分逐次差引, 全球=等方背景のみ）

各パネルの軸:
  主軸: 銀緯 b [deg] / 銀経 l [deg]
  副軸(右): GC からの垂直距離 [kpc]  (h = 8 kpc × tan(|b|))
  副軸(上): GC からの水平距離 [kpc]  (d = 8 kpc × tan(|l|), b=0近似)
"""

import numpy as np
import pandas as pd
from pathlib import Path
from scipy.optimize import minimize_scalar
import warnings
warnings.filterwarnings("ignore")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
import matplotlib
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"
from astropy.io import fits as afits

# ── パス設定 ──────────────────────────────────────────────────────────────
BASE        = Path(__file__).resolve().parent.parent
ALLSKY_CSV  = Path("/root/grad-nakamura/data/CSV/allsky_events.csv")
ROI_CSV     = BASE / "data/CSV/filtered_events_week780.csv"
GALPROP     = BASE / "ref/gll_iem_v07.fits"
CAT_PATH    = BASE / "ref/gll_psc_v35_dr4.fit"  # 4FGL-DR4(14年分); 旧DR2(12年分)から2026-07-10更新
OUT_DIR     = BASE / "data/figure-roi-physics"
OUT_DIR.mkdir(exist_ok=True)

D_SUN = 8.0  # kpc

# ── Bin 6 設定 ─────────────────────────────────────────────────────────────
BIN6_ECENTER = 20.76   # GeV
BIN6_EMIN    = 15.35
BIN6_EMAX    = 28.07

# ── グリッド定義 ─────────────────────────────────────────────────────────
PIXEL = 1.0

# ROI グリッド
L_ROI = np.arange(-60, 60 + PIXEL, PIXEL)
B_ROI = np.arange(-60, 60 + PIXEL, PIXEL)
L_ROI_C = (L_ROI[:-1] + L_ROI[1:]) / 2
B_ROI_C = (B_ROI[:-1] + B_ROI[1:]) / 2
LG_ROI, BG_ROI = np.meshgrid(L_ROI_C, B_ROI_C, indexing="ij")

# 全球グリッド
L_ALL = np.arange(-180, 180 + PIXEL, PIXEL)
B_ALL = np.arange(-90, 90 + PIXEL, PIXEL)
L_ALL_C = (L_ALL[:-1] + L_ALL[1:]) / 2
B_ALL_C = (B_ALL[:-1] + B_ALL[1:]) / 2
LG_ALL, BG_ALL = np.meshgrid(L_ALL_C, B_ALL_C, indexing="ij")

# ────────────────────────────────────────────────────────────────────────
# 1. データ読み込み
# ────────────────────────────────────────────────────────────────────────
print("データ読み込み中...")
df_all = pd.read_csv(ALLSKY_CSV, comment="#",
                     usecols=["energy_GeV", "l_deg", "b_deg"])
df_all = df_all[(df_all.energy_GeV >= BIN6_EMIN) &
                (df_all.energy_GeV <  BIN6_EMAX)].copy()
print(f"  全球 Bin6: {len(df_all):,} イベント")

df_roi = pd.read_csv(ROI_CSV, usecols=["energy_GeV", "l_deg", "b_deg"])
df_roi = df_roi[(df_roi.energy_GeV >= BIN6_EMIN) &
                (df_roi.energy_GeV <  BIN6_EMAX)].copy()
print(f"  ROI Bin6: {len(df_roi):,} イベント")

# ────────────────────────────────────────────────────────────────────────
# 2. ビニング（生データ）
# ────────────────────────────────────────────────────────────────────────
raw_roi, _, _ = np.histogram2d(df_roi.l_deg, df_roi.b_deg, bins=[L_ROI, B_ROI])
raw_all, _, _ = np.histogram2d(df_all.l_deg, df_all.b_deg, bins=[L_ALL, B_ALL])

# ────────────────────────────────────────────────────────────────────────
# 3. 差し引き処理
# ────────────────────────────────────────────────────────────────────────

def subtract_iso(counts, lg, bg, b_thresh=50.0):
    """等方背景: |b| > b_thresh の平均値"""
    mask_iso = (np.abs(bg) > b_thresh) & (counts > 0)
    level = counts[mask_iso].mean() if mask_iso.sum() > 5 else 0.0
    return counts - level, level


# --- ROI 差し引き（5成分） ---
print("ROI 5成分差し引き中...")

# Step 1: 等方背景
sub_roi = raw_roi.copy().astype(float)
sub_roi, iso_lv = subtract_iso(sub_roi, LG_ROI, BG_ROI)
print(f"  Step1 等方BG 差引: level = {iso_lv:.3f}")

# Step 2: GALPROP（指数関数近似 exp(-|b|/b0) を各 l でフィット）
roi_mask = (np.abs(BG_ROI) >= 10) & (np.abs(BG_ROI) <= 60)
galprop_model = np.zeros_like(sub_roi)
for il, lval in enumerate(L_ROI_C):
    col = sub_roi[il, :].copy()
    b_abs = np.abs(B_ROI_C)
    valid = (b_abs >= 10) & (b_abs <= 60) & np.isfinite(col) & (col > 0)
    if valid.sum() < 5:
        continue
    try:
        log_c = np.log(col[valid])
        b_v   = b_abs[valid]
        slope, intercept = np.polyfit(b_v, log_c, 1)
        b0 = -1.0 / slope if slope < 0 else 20.0
        A  = np.exp(intercept)
        galprop_model[il, :] = A * np.exp(-b_abs / b0)
    except Exception:
        pass
sub_roi -= galprop_model
print("  Step2 GALPROP 差引済み")

# Step 3: 点源マスク（4FGL-DR2 を NaN化）
if CAT_PATH.exists():
    with afits.open(CAT_PATH) as hdul:
        cat = hdul[1].data
        l_cat_raw = cat["GLON"].astype(float)
        b_cat     = cat["GLAT"].astype(float)
        l_cat = np.where(l_cat_raw > 180, l_cat_raw - 360, l_cat_raw)
        roi_src = (np.abs(l_cat) <= 60) & (np.abs(b_cat) >= 10) & (np.abs(b_cat) <= 60)
        l_src, b_src = l_cat[roi_src], b_cat[roi_src]
    il_idx = np.searchsorted(L_ROI, l_src, side="right") - 1
    ib_idx = np.searchsorted(B_ROI, b_src, side="right") - 1
    n_masked = 0
    for il_i, ib_i in zip(il_idx, ib_idx):
        if 0 <= il_i < len(L_ROI_C) and 0 <= ib_i < len(B_ROI_C):
            sub_roi[il_i, ib_i] = np.nan
            n_masked += 1
    print(f"  Step3 点源マスク: {n_masked}ピクセル")

# Step 4: フェルミバブル（Bin3残差テンプレート）
# 全CSVから Bin3 を抽出してテンプレート構築
df_allcol = pd.read_csv(ROI_CSV, usecols=["energy_GeV", "l_deg", "b_deg"])
bin3_e = df_allcol[(df_allcol.energy_GeV >= 3.17) & (df_allcol.energy_GeV < 5.49)]
counts_b3, _, _ = np.histogram2d(bin3_e.l_deg, bin3_e.b_deg, bins=[L_ROI, B_ROI])
counts_b3 = counts_b3.astype(float)
counts_b3, _ = subtract_iso(counts_b3, LG_ROI, BG_ROI)

bubble_region = (
    (np.abs(LG_ROI) < 22) &
    (np.abs(BG_ROI) >= 15) & (np.abs(BG_ROI) <= 50)
)
bubble_tmpl = np.zeros_like(counts_b3)
bubble_tmpl[bubble_region & ~np.isnan(counts_b3)] = \
    counts_b3[bubble_region & ~np.isnan(counts_b3)]
bubble_tmpl = np.maximum(bubble_tmpl, 0)

b_valid = (np.abs(BG_ROI) >= 10) & ~np.isnan(sub_roi) & (bubble_tmpl > 0)
if b_valid.sum() > 10:
    T = bubble_tmpl[b_valid]
    N = sub_roi[b_valid]
    A_bbl = max(np.dot(N, T) / (np.dot(T, T) + 1e-12), 0.0)
    sub_roi -= bubble_tmpl * A_bbl
    print(f"  Step4 フェルミバブル 差引: A={A_bbl:.4f}")

# Step 5: ループ I（2成分幾何近似）
loop_center_l = np.radians(-31.0)
loop_center_b = np.radians(+18.0)
cos_ang = (np.sin(np.radians(BG_ROI)) * np.sin(loop_center_b) +
           np.cos(np.radians(BG_ROI)) * np.cos(loop_center_b) *
           np.cos(np.radians(LG_ROI) - loop_center_l))
ang_deg = np.degrees(np.arccos(np.clip(cos_ang, -1, 1)))
for inner, outer in [(40, 55), (55, 70)]:
    mask_li = (ang_deg >= inner) & (ang_deg < outer) & ~np.isnan(sub_roi)
    if mask_li.sum() > 0:
        lv_li = np.nanmedian(sub_roi[mask_li])
        sub_roi[mask_li] -= lv_li
print("  Step5 ループI 差引済み")

# --- 全球 差し引き（等方背景のみ） ---
print("全球: 等方背景差し引き中...")
sub_all = raw_all.copy().astype(float)
sub_all, iso_all = subtract_iso(sub_all, LG_ALL, BG_ALL, b_thresh=70.0)
print(f"  全球等方BG: level = {iso_all:.3f}")

# ────────────────────────────────────────────────────────────────────────
# 4. 軸変換ヘルパー
# ────────────────────────────────────────────────────────────────────────

def deg_to_kpc(b_deg_array):
    return D_SUN * np.tan(np.radians(b_deg_array))


def make_kpc_ticks_b(b_range_deg, n_max=8):
    """b軸の kpc ティック（b の範囲に合わせて kpc_vals を選ぶ）"""
    b_min, b_max = min(b_range_deg), max(b_range_deg)
    kpc_candidates = [1, 2, 5, 10, 15, 20, 30, 50, 80]
    kpc_neg = [-k for k in kpc_candidates]
    kpc_all = sorted(kpc_neg + kpc_candidates)
    kpc_in_range = [k for k in kpc_all
                    if b_min < np.degrees(np.arctan(k / D_SUN)) < b_max]
    return kpc_in_range


def make_kpc_ticks_l(l_range_deg, n_max=6):
    """l軸の kpc ティック（b=0 での近似: d = D_SUN * tan(|l|)）"""
    l_min, l_max = min(l_range_deg), max(l_range_deg)
    kpc_cand = [0, 5, 10, 20, 50, 100, 200]
    ticks_l, ticks_kpc = [], []
    for k in kpc_cand:
        l_pos = np.degrees(np.arctan(k / D_SUN))
        if l_min <= -l_pos or l_max >= l_pos:
            if -l_pos >= l_min:
                ticks_l.append(-l_pos)
                ticks_kpc.append(-k)
            if l_pos <= l_max and k > 0:
                ticks_l.append(l_pos)
                ticks_kpc.append(k)
    return ticks_l, ticks_kpc


# ────────────────────────────────────────────────────────────────────────
# 5. 4パネル図の作成
# ────────────────────────────────────────────────────────────────────────

C_BG = "#05051A"
fig, axes = plt.subplots(2, 2, figsize=(18, 12), facecolor=C_BG)
fig.subplots_adjust(hspace=0.38, wspace=0.35)

panels = [
    # (row, col, data,    lg,     bg,     l_bins, b_bins,  title, subtitle, is_roi)
    (0, 0, raw_roi, LG_ROI, BG_ROI, L_ROI, B_ROI,
     "ROI  差し引き前（生データ）",
     f"|l|≤60°, |b|=10°-60°  /  Bin6 ({BIN6_ECENTER:.1f} GeV)  生カウント", True),

    (0, 1, raw_all, LG_ALL, BG_ALL, L_ALL, B_ALL,
     "全球  差し引き前（生データ）",
     f"全天 |l|≤180°, |b|≤90°  /  Bin6 ({BIN6_ECENTER:.1f} GeV)  生カウント", False),

    (1, 0, sub_roi, LG_ROI, BG_ROI, L_ROI, B_ROI,
     "ROI  差し引き後（5成分逐次差引）",
     "等方BG + GALPROP + 点源 + FB + LoopI 差引済み  ← NFW フィット対象", True),

    (1, 1, sub_all, LG_ALL, BG_ALL, L_ALL, B_ALL,
     "全球  差し引き後（等方背景のみ差引）",
     "等方BG（|b|>70° 平均）を差引。ROI 外は GALPROP 等の系統誤差が大きい", False),
]

for row, col, data, lg, bg, l_bins, b_bins, title, subtitle, is_roi in panels:
    ax = axes[row, col]
    ax.set_facecolor(C_BG)

    l_c = (l_bins[:-1] + l_bins[1:]) / 2
    b_c = (b_bins[:-1] + b_bins[1:]) / 2
    LGp, BGp = np.meshgrid(l_c, b_c, indexing="ij")

    # カラースケール
    valid = data[np.isfinite(data) & (data > 0)]
    if len(valid) == 0:
        valid = np.array([0.1])
    vmin = np.percentile(valid, 5)
    vmax = np.percentile(valid, 99.5)
    # 差し引き後は対称スケール（正負両方）
    if row == 1:
        vabs = max(abs(np.nanpercentile(data, 1)),
                   abs(np.nanpercentile(data, 99)))
        im = ax.pcolormesh(LGp, BGp, data,
                           vmin=-vabs, vmax=vabs,
                           cmap="RdBu_r", shading="auto")
    else:
        vmin = max(vmin, 0.5)
        d_plot = np.where(data > 0, data, 0.1)
        im = ax.pcolormesh(LGp, BGp, d_plot,
                           norm=mcolors.LogNorm(vmin=vmin, vmax=vmax),
                           cmap="plasma", shading="auto")
    cbar = fig.colorbar(im, ax=ax, pad=0.02, shrink=0.92)
    cbar.set_label("counts/pixel" if row == 0 else "residual counts",
                   color="white", fontsize=9)
    cbar.ax.yaxis.set_tick_params(color="white", labelsize=8)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color="white")

    # ROI 境界（緑破線）
    roi_col = "#44FF88"
    if not is_roi:
        for b_line in [10, 60, -10, -60]:
            xmin_f = (max(l_c) - 60) / (max(l_c) - min(l_c))
            xmax_f = (max(l_c) + 60) / (max(l_c) - min(l_c))
            xf = np.clip([xmin_f, xmax_f], 0, 1)
            ax.axhline(b_line, xmin=xf[0], xmax=xf[1],
                       color=roi_col, lw=1.5, ls="--", alpha=0.9)
        for l_line in [60, -60]:
            yf_min = (10 - min(b_c))  / (max(b_c) - min(b_c))
            yf_max = (60 - min(b_c))  / (max(b_c) - min(b_c))
            yf2_min = (-60 - min(b_c)) / (max(b_c) - min(b_c))
            yf2_max = (-10 - min(b_c)) / (max(b_c) - min(b_c))
            ax.axvline(l_line, ymin=yf_min, ymax=yf_max,
                       color=roi_col, lw=1.5, ls="--", alpha=0.9)
            ax.axvline(l_line, ymin=yf2_min, ymax=yf2_max,
                       color=roi_col, lw=1.5, ls="--", alpha=0.9)
        ax.text(0, 35, "ROI", color=roi_col, fontsize=9,
                ha="center", va="center",
                bbox=dict(boxstyle="round", fc="#111130", ec=roi_col, alpha=0.7))
        # 銀河面（赤帯）
        ax.axhspan(-10, 10, alpha=0.2, color="#FF4444")

    # 物理スケール線（kpc）
    scale_specs = [(10, "#FFCC00", "10"), (21, "#44CCFF", "rs=21"), (50, "#FF88AA", "50")]
    for d_kpc, col_s, lbl in scale_specs:
        b_ang = np.degrees(np.arctan(d_kpc / D_SUN))
        if b_ang <= max(b_c):
            ax.axhline( b_ang, color=col_s, lw=1.0, ls=":", alpha=0.75)
            ax.axhline(-b_ang, color=col_s, lw=1.0, ls=":", alpha=0.75)
            ax.text(min(l_c) + 2, b_ang + 1, f"{lbl}kpc",
                    color=col_s, fontsize=7, va="bottom")

    # 主軸ラベル
    ax.set_xlim(max(l_c), min(l_c))  # l は右から左
    ax.set_ylim(min(b_c), max(b_c))
    ax.set_xlabel("銀経 l [deg]", color="white", fontsize=10)
    ax.set_ylabel("銀緯 b [deg]", color="white", fontsize=10)
    ax.tick_params(colors="white", labelsize=9)
    for sp in ax.spines.values():
        sp.set_color("white")

    # ── 副軸（右）: b [deg] → h [kpc] ──────────────────────────
    ax2 = ax.twinx()
    ax2.set_ylim(min(b_c), max(b_c))
    # kpc ティック候補
    kpc_list = make_kpc_ticks_b([min(b_c), max(b_c)])
    tick_b_pos = [np.degrees(np.arctan(k / D_SUN)) for k in kpc_list]
    ax2.set_yticks(tick_b_pos)
    ax2.set_yticklabels([f"{k:+d}" for k in kpc_list], fontsize=7, color="#AAAAAA")
    ax2.set_ylabel("GC からの高さ h [kpc]\n(l=0方向, h=8×tan|b|)", color="#AAAAAA", fontsize=8)
    ax2.tick_params(colors="#AAAAAA", labelsize=7)
    for sp in ax2.spines.values():
        sp.set_color("white")

    # ── 副軸（上）: l [deg] → d [kpc] ──────────────────────────
    ax3 = ax.twiny()
    ax3.set_xlim(max(l_c), min(l_c))
    ticks_l, ticks_kpc = make_kpc_ticks_l([min(l_c), max(l_c)])
    ax3.set_xticks(ticks_l)
    ax3.set_xticklabels([f"{k:+d}" for k in ticks_kpc], fontsize=7, color="#AAAAAA")
    ax3.set_xlabel("GC からの水平距離 d [kpc]  (b≈0°近似, d=8×tan|l|)",
                   color="#AAAAAA", fontsize=8, labelpad=4)
    ax3.tick_params(colors="#AAAAAA", labelsize=7)
    for sp in ax3.spines.values():
        sp.set_color("white")

    # タイトル
    row_lbl = "差し引き前" if row == 0 else "差し引き後"
    col_lbl = "ROI" if is_roi else "全球"
    ax.set_title(f"【{col_lbl} / {row_lbl}】 {title}\n{subtitle}",
                 color="white" if is_roi else "#44CCFF",
                 fontsize=10, pad=20)

# 図全体タイトル
fig.suptitle(
    f"Bin 6 ({BIN6_ECENTER:.1f} GeV)  4パネル比較  |  780週分 Fermi-LAT データ\n"
    f"左列: ROI（|l|≤60°, |b|=10°–60°）/ 右列: 全球  |  上行: 生データ / 下行: 差し引き後\n"
    f"点線: GC からの物理スケール  10 kpc(黄) | rs=21 kpc(青) | 50 kpc(ピンク)",
    color="white", fontsize=12, y=1.01
)

plt.tight_layout()
out = OUT_DIR / "bin6_4panel_before_after.png"
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=C_BG)
plt.close()
print(f"\n完了 → {out}")
