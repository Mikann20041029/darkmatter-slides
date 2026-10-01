#!/usr/bin/env python3
"""
指定フォルダの skymap_bin*.png を 5列×3行グリッドにまとめる
PowerPoint 16:9 (1999×1125 px) サイズ

使い方:
  python3 code/make_grid_image.py [フォルダ名]
  フォルダ名省略時は figure-week9-phase0
"""

import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
import matplotlib
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

folder = sys.argv[1] if len(sys.argv) > 1 else "figure-week9-phase0"
TARGET_DIR = DATA_DIR / folder

COLS, ROWS = 5, 3
PPT_W, PPT_H = 13.33, 7.5

files = sorted(TARGET_DIR.glob("skymap_bin*.png"))
if not files:
    raise FileNotFoundError(f"skymap_bin*.png が見つかりません: {TARGET_DIR}")

fig, axes = plt.subplots(ROWS, COLS, figsize=(PPT_W, PPT_H))
fig.patch.set_facecolor("black")
fig.suptitle(
    f"Fermi-LAT Count Maps — Totani 13 Energy Bins  [{folder}]",
    color="white", fontsize=13, y=0.995
)

for idx, ax in enumerate(axes.flat):
    ax.set_facecolor("black")
    if idx < len(files):
        img = mpimg.imread(str(files[idx]))
        ax.imshow(img)
        ax.axis("off")
    else:
        ax.axis("off")

plt.tight_layout(pad=0.15, rect=[0, 0, 1, 0.97])

out = TARGET_DIR / "skymap_all13bins_grid.png"
fig.savefig(out, dpi=150, bbox_inches=None, facecolor="black")
plt.close(fig)
print(f"保存: {out}")
