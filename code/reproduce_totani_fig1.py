"""
reproduce_totani_fig1.py
Totani (2025) Fig 1 相当 — 1.5 GeV と 4.3 GeV のスカイマップ（フェルミバブル可視化）

出力:
  data/figure-totani-fig1/fermi_bubbles_1p5_4p3_GeV.png
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LogNorm
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
import matplotlib
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"

# ---- パス設定 ----------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(ROOT, "data")
OUT_DIR = os.path.join(DATA_DIR, "figure-totani-fig1")
os.makedirs(OUT_DIR, exist_ok=True)

CSV_PATH = os.path.join(DATA_DIR, "CSV", "filtered_events_week780.csv")

# ---- Totani 13 ビン ----------------------------------------------------------
BIN_CENTERS = np.array([
    1.51, 2.55, 4.31, 7.28, 12.29, 20.76, 35.06,
    59.22, 100.02, 168.93, 285.33, 481.93, 814.00
])
BIN_EDGES = np.zeros(len(BIN_CENTERS) + 1)
BIN_EDGES[1:-1] = np.sqrt(BIN_CENTERS[:-1] * BIN_CENTERS[1:])
BIN_EDGES[0] = BIN_CENTERS[0] ** 2 / BIN_EDGES[1]
BIN_EDGES[-1] = BIN_CENTERS[-1] ** 2 / BIN_EDGES[-2]

# ---- グリッド定義 (|l|≤60°, |b|≤60°, 1°ピクセル) ----------------------------
PIX = 1.0
L_MAX = 60.0
B_MAX = 60.0
B_GP = 10.0   # 銀河面: |b| < 10°

l_edges = np.arange(-L_MAX, L_MAX + PIX, PIX)   # 121点 → 120セル
b_edges = np.arange(-B_MAX, B_MAX + PIX, PIX)   # 121点 → 120セル
l_centers = 0.5 * (l_edges[:-1] + l_edges[1:])
b_centers = 0.5 * (b_edges[:-1] + b_edges[1:])

# ---- CSV 読み込み ------------------------------------------------------------
print("CSV データ読み込み中...")
df = pd.read_csv(CSV_PATH)
df["l_norm"] = ((df["l_deg"] + 180.0) % 360.0) - 180.0

# ---- ビニング関数 ------------------------------------------------------------
def make_count_map(df_sel):
    """イベント DataFrame を 1°ピクセルにビニングし 2D count map を返す"""
    # 範囲外を除外
    valid = (
        (df_sel["l_norm"] >= -L_MAX) & (df_sel["l_norm"] < L_MAX) &
        (df_sel["b_deg"] >= -B_MAX) & (df_sel["b_deg"] < B_MAX)
    )
    df_v = df_sel[valid]
    count, _, _ = np.histogram2d(
        df_v["b_deg"].values,
        df_v["l_norm"].values,
        bins=[b_edges, l_edges]
    )
    return count  # shape: (n_b, n_l)

# ---- Bin 1 (1.51 GeV) -------------------------------------------------------
sel1 = (df["energy_GeV"] >= BIN_EDGES[0]) & (df["energy_GeV"] < BIN_EDGES[1])
map1 = make_count_map(df[sel1])

# ---- Bin 3 (4.31 GeV) -------------------------------------------------------
sel3 = (df["energy_GeV"] >= BIN_EDGES[2]) & (df["energy_GeV"] < BIN_EDGES[3])
map3 = make_count_map(df[sel3])

# ---- プロット ----------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
fig.suptitle("Fermi-LAT スカイマップ (Totani 2025 Fig 1 相当)", fontsize=13)

def draw_skymap(ax, count_map, title, bin_idx):
    """スカイマップを描画するヘルパー"""
    # 表示用の count_map (コピーして銀河面を NaN にしない — 表示はするが解析除外)
    display_map = count_map.copy().astype(float)

    # LogNorm のために 0 を小さい値に置換
    vmin = max(1e-1, np.percentile(display_map[display_map > 0], 5)) if (display_map > 0).any() else 1.0
    vmax = np.percentile(display_map[display_map > 0], 99) if (display_map > 0).any() else 10.0

    im = ax.pcolormesh(
        l_edges, b_edges, display_map,
        cmap="RdBu_r",
        norm=LogNorm(vmin=vmin, vmax=vmax),
        shading="flat"
    )
    plt.colorbar(im, ax=ax, label="counts / pixel")

    # 銀河面 |b| < 10° を半透明グレーで overlay
    gp_rect = plt.Rectangle(
        (-L_MAX, -B_GP), 2 * L_MAX, 2 * B_GP,
        facecolor="gray", alpha=0.4, edgecolor="none"
    )
    ax.add_patch(gp_rect)

    # フェルミバブル境界 (幾何テンプレート): |l|<22°, 15°<|b|<50°
    # 矩形アウトライン (北バブル)
    for sign in [1, -1]:
        ax.plot(
            [-22, -22, 22, 22, -22],
            [sign * 15, sign * 50, sign * 50, sign * 15, sign * 15],
            color="white", lw=1.5, ls="-", alpha=0.85
        )

    ax.set_xlim(L_MAX, -L_MAX)   # l は右→左の向き
    ax.set_ylim(-B_MAX, B_MAX)
    ax.set_xlabel("Galactic longitude l (deg)", fontsize=11)
    ax.set_ylabel("Galactic latitude b (deg)", fontsize=11)
    ax.set_title(title, fontsize=11)
    ax.axhline(B_GP, color="gray", lw=0.8, ls="--", alpha=0.6)
    ax.axhline(-B_GP, color="gray", lw=0.8, ls="--", alpha=0.6)
    ax.set_xticks(np.arange(-60, 61, 20))
    ax.set_yticks(np.arange(-60, 61, 20))
    ax.grid(True, ls=":", alpha=0.3, color="white")

    # 凡例パッチ
    patches = [
        mpatches.Patch(color="gray", alpha=0.4, label="|b| < 10° (銀河面)"),
        mpatches.Patch(color="white", alpha=0.85, label="フェルミバブル境界")
    ]
    ax.legend(handles=patches, fontsize=8, loc="lower right",
              framealpha=0.6, facecolor="k", labelcolor="w")

draw_skymap(axes[0], map1, f"Bin 1: {BIN_CENTERS[0]:.2f} GeV", 0)
draw_skymap(axes[1], map3, f"Bin 3: {BIN_CENTERS[2]:.2f} GeV", 2)

fig.tight_layout()
out_path = os.path.join(OUT_DIR, "fermi_bubbles_1p5_4p3_GeV.png")
fig.savefig(out_path, dpi=150)
plt.close(fig)
print(f"スカイマップを保存: {out_path}")
