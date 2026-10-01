"""
allsky_events.csv（全天球データ）を使って Bin 6（20.76 GeV）の全球スカイマップを作成。

図1: 全球スカイマップ（Bin 6）
   - ROI 境界（緑破線）
   - 銀河面除外領域（赤帯）
   - GC からの物理スケール円（10 / 21 / 50 kpc に対応する b 角度）

図2: ROI 内と ROI 外の比較スカイマップ（横並び）
"""
import pathlib as _pathlib

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
import os

# ── 設定 ─────────────────────────────────────────────────────────────────
ALLSKY_CSV = "/root/grad-nakamura/data/CSV/allsky_events.csv"
OUT_DIR    = str(_pathlib.Path(__file__).resolve().parent.parent / "data/figure-roi-physics")
os.makedirs(OUT_DIR, exist_ok=True)

# Bin 6: 20.76 GeV（前後のビン境界）
E_MIN, E_MAX = 15.35, 28.07   # GeV（13ビン対数等間隔のBin6範囲）
D_SUN = 8.0  # kpc

# ── データ読み込み ────────────────────────────────────────────────────────
print("allsky_events.csv を読み込み中（3950万行）...")
df = pd.read_csv(ALLSKY_CSV, comment="#",
                 usecols=["energy_GeV", "l_deg", "b_deg"])
print(f"  読み込み完了: {len(df):,} イベント")

# Bin 6 のみ抽出
bin6 = df[(df.energy_GeV >= E_MIN) & (df.energy_GeV < E_MAX)].copy()
print(f"  Bin 6 ({E_MIN}–{E_MAX} GeV): {len(bin6):,} イベント")

# ── グリッド作成（1° × 1°）────────────────────────────────────────────────
print("グリッドにビニング中...")
L_EDGES = np.arange(-180, 181, 1)
B_EDGES = np.arange(-90,   91, 1)

counts, _, _ = np.histogram2d(bin6.l_deg, bin6.b_deg,
                               bins=[L_EDGES, B_EDGES])
L_CENTERS = (L_EDGES[:-1] + L_EDGES[1:]) / 2
B_CENTERS = (B_EDGES[:-1] + B_EDGES[1:]) / 2
L_GRID, B_GRID = np.meshgrid(L_CENTERS, B_CENTERS, indexing="ij")

# 物理スケール（GC からの高さ = D_SUN × tan(b)）に対応する銀緯
def b_for_kpc(d_kpc):
    return np.degrees(np.arctan(d_kpc / D_SUN))

b10  = b_for_kpc(10)   # ≈ 51.3°
b21  = b_for_kpc(21)   # ≈ 69.1°  (rs = 21 kpc)
b50  = b_for_kpc(50)   # ≈ 80.9°

print(f"物理スケール対応角度: 10 kpc → b={b10:.1f}°, rs=21 kpc → b={b21:.1f}°, 50 kpc → b={b50:.1f}°")

# ────────────────────────────────────────────────────────────────────────
# 図1: 全球スカイマップ（カウント数）
# ────────────────────────────────────────────────────────────────────────
print("図1 全球スカイマップ 作成中...")

C_BG = "#05051A"
fig, ax = plt.subplots(figsize=(14, 7), facecolor=C_BG)
ax.set_facecolor(C_BG)

# カウントマップ（0 を 0.1 に置換して対数スケール可能に）
c_plot = np.where(counts > 0, counts, 0.1)
im = ax.pcolormesh(L_GRID, B_GRID, c_plot,
                   norm=mcolors.LogNorm(vmin=0.5, vmax=c_plot.max()),
                   cmap="plasma", shading="auto")
cbar = fig.colorbar(im, ax=ax, pad=0.01)
cbar.set_label("Photon counts / pixel (1°×1°)", color="white", fontsize=11)
cbar.ax.yaxis.set_tick_params(color="white")
plt.setp(cbar.ax.yaxis.get_ticklabels(), color="white")

# ROI 境界（緑破線）
roi_color = "#44FF88"
lw = 2.0
# 上下の水平線
for b_line in [10, 60, -10, -60]:
    xmin = (180 - 60) / 360
    xmax = (180 + 60) / 360
    ax.axhline(b_line, xmin=xmin, xmax=xmax,
               color=roi_color, lw=lw, ls="--")
# 左右の垂直線
for l_line in [60, -60]:
    ymin = (90 - 60) / 180
    ymax = (90 + 60) / 180
    ax.axvline(l_line, ymin=ymin, ymax=ymax,
               color=roi_color, lw=lw, ls="--")

# 銀河面除外帯（|b|<10°）
ax.axhspan(-10, 10, alpha=0.25, color="#FF4444", label="銀河面除外 |b|<10°")

# 物理スケール線
for d_kpc, b_ang, col, lbl in [
    (10, b10, "#FFCC00", "10 kpc"),
    (21, b21, "#44CCFF", "rs=21 kpc"),
    (50, b50, "#FF88AA", "50 kpc"),
]:
    ax.axhline( b_ang, color=col, lw=1.3, ls=":", alpha=0.85)
    ax.axhline(-b_ang, color=col, lw=1.3, ls=":", alpha=0.85)
    ax.text(-178, b_ang + 1.5, lbl, color=col, fontsize=9, va="bottom")

# ROI ラベル
ax.text(0, 35, "ROI\n(本研究・Totani共通)", color=roi_color, fontsize=10,
        ha="center", va="center",
        bbox=dict(boxstyle="round,pad=0.3", fc="#111130", ec=roi_color, alpha=0.7))

ax.set_xlim(180, -180)
ax.set_ylim(-90, 90)
ax.set_xlabel("銀経 l [deg]", color="white", fontsize=12)
ax.set_ylabel("銀緯 b [deg]", color="white", fontsize=12)
ax.tick_params(colors="white")
for sp in ax.spines.values():
    sp.set_color("white")

ax.set_title(
    f"全球 γ 線スカイマップ — Bin 6 ({E_MIN:.0f}–{E_MAX:.0f} GeV, 約 20.76 GeV)  780 週分\n"
    f"緑破線: ROI 境界  赤帯: 銀河面除外  点線: GC からの物理スケール\n"
    f"物理スケール:  10 kpc → b={b10:.0f}°  |  rs=21 kpc → b={b21:.0f}°  |  50 kpc → b={b50:.0f}°",
    color="white", fontsize=11, pad=8
)
ax.legend(loc="lower right", facecolor="#111130", edgecolor="white",
          labelcolor="white", fontsize=9)

plt.tight_layout()
out1 = os.path.join(OUT_DIR, "allsky_bin6_fullmap.png")
plt.savefig(out1, dpi=150, bbox_inches="tight", facecolor=C_BG)
plt.close()
print(f"  → {out1}")

# ────────────────────────────────────────────────────────────────────────
# 図2: ROI 内 / 銀河面 / 高銀緯 の 3 領域比較（横並び）
# ────────────────────────────────────────────────────────────────────────
print("図2 領域比較マップ 作成中...")

fig, axes = plt.subplots(1, 3, figsize=(16, 5), facecolor=C_BG)

regions = [
    ("銀河面\n|b|<10°\n（解析から除外）",
     lambda l, b: (np.abs(b) < 10) & (np.abs(l) <= 60),
     "#FF4444"),
    ("ROI\n10°≤|b|≤60°, |l|≤60°\n（解析対象）",
     lambda l, b: (np.abs(b) >= 10) & (np.abs(b) <= 60) & (np.abs(l) <= 60),
     "#44FF88"),
    (f"高銀緯\n|b|>60°\n（GCから >{b21:.0f}kpc）",
     lambda l, b: np.abs(b) > 60,
     "#FFCC00"),
]

for ax, (title, mask_fn, col) in zip(axes, regions):
    ax.set_facecolor(C_BG)
    masked = np.where(mask_fn(L_GRID, B_GRID), c_plot, np.nan)
    vmin_r = np.nanpercentile(masked, 5)
    vmax_r = np.nanpercentile(masked, 99)
    vmin_r = max(vmin_r, 0.5)

    im = ax.pcolormesh(L_GRID, B_GRID, masked,
                       norm=mcolors.LogNorm(vmin=vmin_r, vmax=vmax_r),
                       cmap="plasma", shading="auto")
    fig.colorbar(im, ax=ax, label="counts", shrink=0.7)
    im.get_cmap().set_bad(C_BG)  # NaN を背景色に

    # 物理スケール線（全パネル共通）
    for b_ang, c_l in [(b10, "#FFCC00"), (b21, "#44CCFF"), (b50, "#FF88AA")]:
        ax.axhline( b_ang, color=c_l, lw=1, ls=":", alpha=0.7)
        ax.axhline(-b_ang, color=c_l, lw=1, ls=":", alpha=0.7)

    ax.set_xlim(180, -180)
    ax.set_ylim(-90, 90)
    ax.set_xlabel("l [deg]", color="white", fontsize=10)
    ax.set_ylabel("b [deg]", color="white", fontsize=10)
    ax.tick_params(colors="white")
    for sp in ax.spines.values():
        sp.set_color(col)
        sp.set_linewidth(2)
    ax.set_title(title, color=col, fontsize=11)

    # イベント数を表示
    n_events = int(np.nansum(np.where(mask_fn(L_GRID, B_GRID), counts, 0)))
    ax.text(0, -82, f"Bin6 光子数: {n_events:,}", color=col,
            fontsize=10, ha="center",
            bbox=dict(boxstyle="round", fc="#111130", ec=col, alpha=0.8))

fig.suptitle(
    f"Bin 6 ({E_MIN:.0f}–{E_MAX:.0f} GeV) 各解析領域の比較\n"
    f"点線: 10 kpc（黄）/ rs=21 kpc（青）/ 50 kpc（ピンク）",
    color="white", fontsize=12
)
plt.tight_layout()
out2 = os.path.join(OUT_DIR, "allsky_bin6_region_compare.png")
plt.savefig(out2, dpi=150, bbox_inches="tight", facecolor=C_BG)
plt.close()
print(f"  → {out2}")

# ── テキスト集計 ──────────────────────────────────────────────────────────
mask_disk = (bin6.b_deg.abs() < 10) & (bin6.l_deg.abs() <= 60)
mask_roi  = (bin6.b_deg.abs() >= 10) & (bin6.b_deg.abs() <= 60) & (bin6.l_deg.abs() <= 60)
mask_high = bin6.b_deg.abs() > 60

n_disk = mask_disk.sum()
n_roi  = mask_roi.sum()
n_high = mask_high.sum()
n_total= len(bin6)

print(f"\n=== Bin 6 光子数集計 ===")
print(f"全天: {n_total:,}")
print(f"銀河面 |b|<10°, |l|≤60°: {n_disk:,}  ({100*n_disk/n_roi:.1f}% of ROI)")
print(f"ROI 10°≤|b|≤60°, |l|≤60°: {n_roi:,}  (基準)")
print(f"|b|>60°: {n_high:,}  ({100*n_high/n_roi:.1f}% of ROI)")
print(f"\n全図完了: {out1}")
print(f"         {out2}")
