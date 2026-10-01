import pathlib as _pathlib
#!/usr/bin/env python3
"""
矮小銀河 5天体 — ON/OFF 空間マップ可視化
各天体について:
  左: 全エネルギー (1.5-814 GeV) のスカイマップ + ON/OFF リング
  中: Bin6 (15.35-28.07 GeV) のスカイマップ + ON/OFF リング
  右: ON カウント vs BG推定値 スペクトル (13ビン)

出力: data/figure-dwarfs/<name>/<name>_skymap_on_off.png
      data/figure-dwarfs/all5_skymap_comparison.png
"""
import sys
sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))
import warnings
warnings.filterwarnings("ignore")

import zlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"

from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUT_DIR  = DATA_DIR / "figure-dwarfs"

# 解析パラメータ
ON_RAD  = 2.0
OFF_RAD = 5.0
ALPHA   = ON_RAD**2 / (OFF_RAD**2 - ON_RAD**2)  # ≈ 0.190

N_BINS = 13
BIN_CENTERS = np.logspace(np.log10(1.51), np.log10(814.0), N_BINS)
_r = (814.0 / 1.51) ** (1.0 / (N_BINS - 1))
BIN_EDGES = np.concatenate([[1.51/_r**0.5],
                             np.sqrt(BIN_CENTERS[:-1]*BIN_CENTERS[1:]),
                             [814.0*_r**0.5]])

EMIN_B6, EMAX_B6, ECEN_B6 = 15.35, 28.07, 20.76

TARGETS = [
    ("draco",     260.052,  57.915, "Draco dSph", -1.28),
    ("sculptor",   15.039, -33.709, "Sculptor dSph", +1.33),
    ("ursa_minor",227.285,  67.222, "Ursa Minor dSph", +1.68),
    ("segue1",    151.767,  16.082, "Segue 1", -0.38),
    ("coma_ber",  186.746,  23.904, "Coma Berenices", +4.54),
]

# ON/OFFリングを描画する関数
def draw_rings(ax, color_on="lime", color_off="orange", lw=1.5):
    theta = np.linspace(0, 2*np.pi, 300)
    ax.plot(ON_RAD*np.cos(theta), ON_RAD*np.sin(theta),
            color=color_on, lw=lw, ls="-", label=f"ON (<{ON_RAD:.0f}°)", alpha=0.9)
    ax.plot(OFF_RAD*np.cos(theta), OFF_RAD*np.sin(theta),
            color=color_off, lw=lw, ls="--", label=f"OFF (<{OFF_RAD:.0f}°)", alpha=0.9)
    ax.plot(0, 0, "w+", ms=10, mew=2, zorder=10)
    ax.set_aspect("equal")


def plot_dwarf(name, ra, dec, label, sigma_b6):
    csv_path = DATA_DIR / "CSV" / "dwarfs" / f"dwarf_{name}_780w.csv"
    if not csv_path.exists():
        print(f"  {name}: CSVなし スキップ"); return

    df = pd.read_csv(csv_path)
    ang = df["ang_dist_deg"].values
    ene = df["energy_GeV"].values

    # (dRA, dDec) 相対座標を角距離方向で近似
    # 実際のCSVにはang_dist_degしかないため、ランダム方位角でプロット（位置情報なし）
    # → 放射対称を仮定して ang_dist と方位角θで表示
    rng = np.random.default_rng(seed=42 + zlib.crc32(name.encode()) % 100)
    phi = rng.uniform(0, 2*np.pi, len(df))
    dx = ang * np.cos(phi)
    dy = ang * np.sin(phi)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.patch.set_facecolor("white")
    sigma_str = f"{sigma_b6:+.2f}σ"
    color_sig = "#cc0000" if sigma_b6 > 2 else ("#003399" if sigma_b6 < -2 else "#555555")
    fig.suptitle(
        f"{label}  (RA={ra:.2f}°, Dec={dec:.2f}°)  "
        f"Bin6 S/N = {sigma_str}",
        fontsize=13, fontweight="bold",
        color=color_sig if abs(sigma_b6) > 2 else "black"
    )

    # 色: エネルギーで着色
    log_e = np.log10(ene)
    norm_e = mcolors.Normalize(vmin=np.log10(1.5), vmax=np.log10(814))
    cmap_e = plt.cm.plasma

    # ── 左パネル: 全エネルギー ──
    ax0 = axes[0]
    ax0.set_facecolor("#05051a")
    sc = ax0.scatter(dx, dy, c=log_e, cmap=cmap_e, norm=norm_e,
                     s=2, alpha=0.5, rasterized=True)
    draw_rings(ax0)
    ax0.set_xlim(-6, 6); ax0.set_ylim(-6, 6)
    ax0.set_xlabel("ΔRA相当 [deg]", fontsize=9)
    ax0.set_ylabel("ΔDec相当 [deg]", fontsize=9)
    ax0.set_title(f"全エネルギー (1.5–814 GeV)\n{len(df)} photons total", fontsize=10)
    ax0.legend(fontsize=8, loc="upper right")
    ax0.tick_params(labelsize=8)
    plt.colorbar(sc, ax=ax0,
                 label=r"log$_{10}$ Energy [GeV]").ax.tick_params(labelsize=7)

    # ── 中パネル: Bin6のみ ──
    ax1 = axes[1]
    ax1.set_facecolor("#05051a")
    b6_mask = (ene >= EMIN_B6) & (ene < EMAX_B6)
    b6_on   = b6_mask & (ang < ON_RAD)
    b6_off  = b6_mask & (ang >= ON_RAD) & (ang < OFF_RAD)
    b6_n_on  = b6_on.sum()
    b6_n_off = b6_off.sum()
    b6_bg    = ALPHA * b6_n_off
    b6_exc   = b6_n_on - b6_bg
    b6_sig   = b6_exc / np.sqrt(b6_bg + ALPHA**2 * b6_n_off) if b6_bg > 0 else 0

    if b6_mask.sum() > 0:
        sc2 = ax1.scatter(dx[b6_mask], dy[b6_mask],
                          c="#ff6600", s=8, alpha=0.7, label=f"Bin6 photons ({b6_mask.sum()})")
    draw_rings(ax1)
    ax1.set_xlim(-6, 6); ax1.set_ylim(-6, 6)
    ax1.set_xlabel("ΔRA相当 [deg]", fontsize=9)
    ax1.set_ylabel("ΔDec相当 [deg]", fontsize=9)
    ax1.set_title(
        f"Bin6 ({ECEN_B6:.1f} GeV)\n"
        f"ON={b6_n_on}, BG={b6_bg:.1f}, S/N={b6_sig:+.2f}σ",
        fontsize=10
    )
    ax1.tick_params(labelsize=8)

    # ── 右パネル: スペクトル ──
    ax2 = axes[2]
    on_counts  = np.zeros(N_BINS)
    off_counts = np.zeros(N_BINS)
    for i in range(N_BINS):
        em = (ene >= BIN_EDGES[i]) & (ene < BIN_EDGES[i+1])
        on_counts[i]  = (ang < ON_RAD)[em].sum()
        off_counts[i] = ((ang >= ON_RAD) & (ang < OFF_RAD))[em].sum()
    bg_est = ALPHA * off_counts
    excess = on_counts - bg_est
    sigma_arr = np.where(bg_est > 0,
                         excess / np.sqrt(bg_est + ALPHA**2 * off_counts), 0)

    colors_spec = ["#cc3300" if s > 0 else "#0033cc" for s in sigma_arr]
    ax2.bar(range(N_BINS), sigma_arr, color=colors_spec, width=0.8, alpha=0.85)
    ax2.axhline(0, color="black", lw=1)
    ax2.axhline(2, color="red", lw=0.8, ls="--", alpha=0.5, label="2σ")
    ax2.axhline(-2, color="red", lw=0.8, ls="--", alpha=0.5)
    ax2.axvline(5, color="gold", lw=1.5, ls="-", alpha=0.8, label="Bin6 (20.76 GeV)")
    ax2.set_xticks(range(N_BINS))
    ax2.set_xticklabels([f"{c:.1f}" for c in BIN_CENTERS],
                        rotation=60, ha="right", fontsize=7)
    ax2.set_xlabel("Energy bin center [GeV]", fontsize=9)
    ax2.set_ylabel("S/N (σ)", fontsize=9)
    ax2.set_title(f"ON/OFF 有意性スペクトル\nα={ALPHA:.3f}", fontsize=10)
    ax2.legend(fontsize=8)
    ax2.tick_params(labelsize=8)

    plt.tight_layout()
    out_dir = OUT_DIR / name
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{name}_skymap_on_off.png"
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved: {out}")
    return out


# ── 全5天体を個別に生成 ──
print("矮小銀河 ON/OFF スカイマップ生成中...")
saved = {}
for name, ra, dec, label, sig in TARGETS:
    f = plot_dwarf(name, ra, dec, label, sig)
    if f:
        saved[name] = f


# ── 5天体まとめ図 ──
print("\n5天体まとめ図 (Bin6 S/N) 生成中...")
fig_all, axes_all = plt.subplots(1, 5, figsize=(25, 5.5))
fig_all.patch.set_facecolor("white")
fig_all.suptitle(
    "矮小銀河 5天体 — Bin6 (20.76 GeV) ON/OFF スカイマップ比較\n"
    f"ON:<{ON_RAD:.0f}°, OFF:{ON_RAD:.0f}°–{OFF_RAD:.0f}°, α={ALPHA:.3f}",
    fontsize=12, fontweight="bold"
)

for ax, (name, ra, dec, label, sig) in zip(axes_all, TARGETS):
    csv_path = DATA_DIR / "CSV" / "dwarfs" / f"dwarf_{name}_780w.csv"
    if not csv_path.exists():
        ax.text(0.5, 0.5, "データなし", ha="center", va="center",
                transform=ax.transAxes)
        continue

    df = pd.read_csv(csv_path)
    ang = df["ang_dist_deg"].values
    ene = df["energy_GeV"].values

    rng = np.random.default_rng(seed=42 + zlib.crc32(name.encode()) % 100)
    phi = rng.uniform(0, 2*np.pi, len(df))
    dx = ang * np.cos(phi)
    dy = ang * np.sin(phi)

    b6_mask = (ene >= EMIN_B6) & (ene < EMAX_B6)
    b6_on   = (ang < ON_RAD) & b6_mask

    ax.set_facecolor("#05051a")
    if b6_mask.sum() > 0:
        ax.scatter(dx[b6_mask], dy[b6_mask],
                   c="#ff6600", s=6, alpha=0.7, label=f"Bin6 ({b6_mask.sum()})")
    # 他エネルギーを薄く表示
    other = ~b6_mask
    if other.sum() > 0:
        ax.scatter(dx[other], dy[other], c="gray", s=1, alpha=0.15)

    theta = np.linspace(0, 2*np.pi, 200)
    ax.plot(ON_RAD*np.cos(theta), ON_RAD*np.sin(theta),
            color="lime", lw=1.5, ls="-")
    ax.plot(OFF_RAD*np.cos(theta), OFF_RAD*np.sin(theta),
            color="orange", lw=1.5, ls="--")
    ax.plot(0, 0, "w+", ms=10, mew=2, zorder=10)

    sigma_c = "#cc0000" if sig > 2 else ("#003399" if sig < -2 else "white")
    ax.set_title(f"{label}\nS/N = {sig:+.2f}σ",
                 fontsize=9, color=sigma_c, fontweight="bold")
    ax.set_xlim(-6, 6); ax.set_ylim(-6, 6)
    ax.set_xlabel("Δ [deg]", fontsize=7)
    ax.set_ylabel("Δ [deg]", fontsize=7)
    ax.tick_params(labelsize=6)
    ax.set_aspect("equal")

plt.tight_layout()
out_all = OUT_DIR / "all5_skymap_bin6.png"
fig_all.savefig(out_all, dpi=150, bbox_inches="tight", facecolor="white")
plt.close(fig_all)
print(f"  Saved: {out_all}")
print(f"\n完了 → {OUT_DIR}")
