import pathlib as _pathlib
#!/usr/bin/env python3
"""
Totani (2025) Figure 14 相当: 各モデルテンプレートのスカイマップ
  Fig.14: GALPROP gas, Loop I-A, Loop I-B, GALPROP ICS (optical/IR/CMB)

本解析での対応:
  - GALPROP ICS テンプレート (gll_iem_v07)
  - Loop I 幾何モデル (2シェル)
  - フェルミバブルテンプレート (4.3 GeV残差)
  - 点源カタログ位置

出力: data/figure-5component/totani_fig14_equiv.png
"""
import sys
sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"

from pathlib import Path
import plot_skymap_all_subtracted as _sub

BASE    = _pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = BASE / "data/figure-5component"
OUT_DIR.mkdir(parents=True, exist_ok=True)

L_BINS, B_BINS   = _sub.L_BINS, _sub.B_BINS
L_CENTERS        = _sub.L_CENTERS
B_CENTERS        = _sub.B_CENTERS
L_GRID, B_GRID   = _sub.L_GRID, _sub.B_GRID

# Bin6 (20.76 GeV)
EMIN, EMAX, ECEN = 15.35, 28.07, 20.76

# ── GALPROP テンプレートを取得 ──
print("GALPROP テンプレート取得中...")
galprop_template = _sub._load_galprop_template(EMIN, EMAX)

# ── Loop I テンプレート構築 ──
# 2026-07-12更新: 旧・単一中心角度リング近似(Berkhuijsen 1971)から、
# Totaniが実際に使うAckermann+2014/2017の2シェル3次元幾何モデル
# (Wolleben 2007電波偏光サーベイ由来)に置き換え済み。
print("Loop I テンプレート構築中(2シェル3次元幾何モデル)...")
loopi_A, loopi_B = _sub.loop_i_shell_templates()

# ── バブルテンプレート ──
print("バブルテンプレート構築中...")
CSV_PATH = BASE / "data/CSV/filtered_events_week780.csv"
df_all = pd.read_csv(CSV_PATH, comment="#", low_memory=False)
bubble_template = _sub.build_fermi_bubble_template(df_all)

# ── 点源カタログ位置 ──
cat_l, cat_b = _sub._CAT_L, _sub._CAT_B

# ── 図の描画 ──
def plot_map(ax, data, title, cmap="hot", log=True, vmin=None, vmax=None,
             cbar_label="flux [arb.]", show_disk=True, overlay_circles=False):
    d = data.T
    if log and np.any(d > 0):
        d_plot = np.where(d > 0, d, np.nan)
        norm = mcolors.LogNorm(vmin=vmin or float(np.nanpercentile(d_plot[d_plot > 0], 1)),
                               vmax=vmax or float(np.nanpercentile(d_plot[d_plot > 0], 99.5)))
    else:
        d_plot = d
        norm = mcolors.Normalize(vmin=vmin or 0, vmax=vmax or float(np.nanmax(np.abs(d))))

    im = ax.pcolormesh(L_BINS, B_BINS, d_plot, norm=norm, cmap=cmap, shading="flat")
    ax.set_xlim(60, -60)
    ax.set_ylim(-60, 60)
    ax.set_xlabel("銀経 l [deg]", fontsize=8)
    ax.set_ylabel("銀緯 b [deg]", fontsize=8)
    ax.set_title(title, fontsize=9, fontweight="bold", pad=3)
    ax.tick_params(labelsize=7)
    if show_disk:
        ax.axhspan(-10, 10, color="gray", alpha=0.35, zorder=3)
    return im

def add_cbar(fig, im, ax, label, fontsize=7):
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="4%", pad=0.05)
    cb = fig.colorbar(im, cax=cax)
    cb.set_label(label, fontsize=fontsize)
    cb.ax.tick_params(labelsize=6)

# ── 6パネル: Totani Fig.14 対応 ──
fig, axes = plt.subplots(2, 3, figsize=(18, 11))
fig.patch.set_facecolor("white")
fig.suptitle(
    f"Totani (2025) Fig.14 対応: モデルテンプレートのスカイマップ (Bin6 = {ECEN:.1f} GeV)\n"
    "上段: GALPROP gas, Loop I-A (内側シェル), Loop I-B (外側シェル)\n"
    "下段: バブルテンプレート, 点源カタログ位置, GALPROP×フィット係数",
    fontsize=11, fontweight="bold", y=0.98
)

# [0,0]: GALPROP ICS (全体)
im = plot_map(axes[0, 0], galprop_template,
              f"GALPROP テンプレート (gll_iem_v07)\n{ECEN:.1f} GeV スライス [counts/pix/sr]",
              cmap="hot", log=True, cbar_label="GALPROP counts/pix")
add_cbar(fig, im, axes[0, 0], "counts/pix")

# Totani Fig.14 (上段中): Loop I shell1 (Ackermann+2014/2017 2シェルモデル)
im = plot_map(axes[0, 1], loopi_A,
              "Loop I shell1 テンプレート\n視線積分経路長 [kpc] (l=341°,b=3°,d=78pc,r=62-81pc)",
              cmap="hot", log=False, vmin=0, vmax=float(np.nanmax(loopi_A)), cbar_label="経路長 [kpc]")
add_cbar(fig, im, axes[0, 1], "経路長 [kpc]")

# Totani Fig.14 (上段右): Loop I shell2
im = plot_map(axes[0, 2], loopi_B,
              "Loop I shell2 テンプレート\n視線積分経路長 [kpc] (l=332°,b=37°,d=95pc,r=58-82pc)",
              cmap="hot", log=False, vmin=0, vmax=float(np.nanmax(loopi_B)), cbar_label="経路長 [kpc]")
add_cbar(fig, im, axes[0, 2], "経路長 [kpc]")

# [1,0]: バブルテンプレート (Totani では residual(+) map)
im = plot_map(axes[1, 0], bubble_template,
              "フェルミバブルテンプレート\n(Bin3 = 4.31 GeV 残差マップ正値)\nTotani Fig.1 対応",
              cmap="hot", log=False, vmin=0, vmax=float(np.nanmax(bubble_template)) * 0.8,
              cbar_label="counts/pixel")
add_cbar(fig, im, axes[1, 0], "counts/pixel")

# [1,1]: 点源位置 (4FGL-DR2)
ps_map = np.zeros_like(galprop_template)
for lc, bc in zip(cat_l, cat_b):
    il = int((lc - L_BINS[0]) / 1.0)
    ib = int((bc - B_BINS[0]) / 1.0)
    if 0 <= il < len(L_CENTERS) and 0 <= ib < len(B_CENTERS):
        ps_map[il, ib] += 1

im = plot_map(axes[1, 1], ps_map,
              f"点源カタログ位置 (4FGL-DR4)\n{int(cat_l.shape[0])} sources in ROI",
              cmap="Reds", log=False, vmin=0, vmax=1.2, cbar_label="点源数/ピクセル")
add_cbar(fig, im, axes[1, 1], "点源数/ピクセル")

# [1,2]: GALPROP × フィット係数 (本解析の差引き量)
print("GALPROP フィット係数計算中...")
CSV_PATH = BASE / "data/CSV/filtered_events_week780.csv"
df = pd.read_csv(CSV_PATH, comment="#", low_memory=False)
sel = df[(df["energy_GeV"] >= EMIN) & (df["energy_GeV"] < EMAX)]
raw, _, _ = np.histogram2d(sel["l_deg"], sel["b_deg"], bins=[L_BINS, B_BINS])
raw = raw.astype(float)
_, iso_lv = _sub.subtract_isotropic(raw.copy())
step1 = raw - iso_lv
_, galprop_sub, lbl = _sub.subtract_galactic_diffuse(step1.copy(), EMIN, EMAX)

im = plot_map(axes[1, 2], galprop_sub,
              "本解析 GALPROP 差引き量\n" r"(A×exp(-|b|/b$_0$) フィット結果)" f"\n{lbl[:40]}...",
              cmap="hot", log=True, cbar_label="counts/pixel")
add_cbar(fig, im, axes[1, 2], "counts/pixel")

# 全体参考ライン
for ax in axes.flat:
    ax.axhline(10, color="white", lw=0.5, ls="--", alpha=0.5)
    ax.axhline(-10, color="white", lw=0.5, ls="--", alpha=0.5)

plt.tight_layout(rect=[0, 0, 1, 0.93])
out = OUT_DIR / "totani_fig14_equiv.png"
fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"Saved: {out}")
