#!/usr/bin/env python3
"""
550週分データ（w009-w549）の全解析を一括実行する。
出力先: data/figure550-*/

実行方法:
  python3 code/run_all_550.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
sys.path.insert(0, str(ROOT / "code"))


def run(label, mod_name, out_dir):
    print(f"\n{'='*50}")
    print(f"  {label}  →  {out_dir.name}")
    print(f"{'='*50}")
    import importlib
    mod = importlib.import_module(mod_name)
    mod.OUTPUT_DIR = out_dir
    mod.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    mod.main()


# ── Phase 0: 生マップ ──────────────────────────
run("生マップ (3エネルギー帯)",
    "plot_raw_skymap",
    DATA / "figure550-phase0")

run("エネルギースペクトル",
    "plot_energy_spectrum",
    DATA / "figure550-phase0")

run("13ビン個別マップ",
    "plot_skymap_13bins",
    DATA / "figure550-phase0")

# グリッド画像
import make_grid_image  # noqa: F401 (side-effect import)
import importlib, make_grid_image as mg
mg.TARGET_DIR = DATA / "figure550-phase0"
files = sorted(mg.TARGET_DIR.glob("skymap_bin*.png"))
if files:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    fig, axes = plt.subplots(3, 5, figsize=(13.33, 7.5))
    fig.patch.set_facecolor("black")
    fig.suptitle("Fermi-LAT Count Maps — 13 Energy Bins [figure550-phase0]",
                 color="white", fontsize=13, y=0.995)
    for idx, ax in enumerate(axes.flat):
        ax.set_facecolor("black")
        if idx < len(files):
            ax.imshow(mpimg.imread(str(files[idx])))
        ax.axis("off")
    plt.tight_layout(pad=0.15, rect=[0, 0, 1, 0.97])
    out = mg.TARGET_DIR / "skymap_all13bins_grid.png"
    fig.savefig(out, dpi=150, bbox_inches=None, facecolor="black")
    plt.close(fig)
    print(f"グリッド保存: {out.name}")

# ── Phase 1: 等方背景差し引き ──────────────────
run("等方背景差し引き",
    "plot_skymap_minus_isotropic",
    DATA / "figure550-isotropic")

import subprocess
subprocess.run(["python3", "code/make_grid_image.py", "figure550-isotropic"],
               cwd=str(ROOT))

# ── Phase 2: 全成分差し引き ────────────────────
run("全5成分差し引き",
    "plot_skymap_all_subtracted",
    DATA / "figure550-all-subtracted")

subprocess.run(["python3", "code/make_grid_image.py", "figure550-all-subtracted"],
               cwd=str(ROOT))

# ── Phase 3: NFWフィット ───────────────────────
run("NFWハローフィット",
    "plot_nfw_halo_fit",
    DATA / "figure550-nfw-fit")

print("\n" + "="*50)
print("  全処理完了")
print("="*50)
print(f"  figure550-phase0/")
print(f"  figure550-isotropic/")
print(f"  figure550-all-subtracted/")
print(f"  figure550-nfw-fit/")
