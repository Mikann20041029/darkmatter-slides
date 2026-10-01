#!/usr/bin/env python3
"""
矮小銀河のエネルギースペクトル解析
各天体周辺5°以内の光子を13ビンに分け、
オン領域（天体周辺2°）とオフ領域（2°-5°）でカウントを比較し
20 GeV付近に過剰があるか検証する。

出力: data/figure-dwarfs/
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
import matplotlib
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUT_DIR  = DATA_DIR / "figure-dwarfs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Totani 13ビン
N_BINS      = 13
BIN_CENTERS = np.logspace(np.log10(1.51), np.log10(814.0), N_BINS)
_r          = (814.0 / 1.51) ** (1.0 / (N_BINS - 1))
BIN_EDGES   = np.concatenate([[1.51/_r**0.5],
                               np.sqrt(BIN_CENTERS[:-1]*BIN_CENTERS[1:]),
                               [814.0*_r**0.5]])

TARGETS = [
    ("draco",     260.052,  57.915, "Draco dSph — DM支配的、最有力ターゲット"),
    ("sculptor",   15.039, -33.709, "Sculptor dSph — 光子数多く統計有利"),
    ("ursa_minor",227.285,  67.222, "Ursa Minor dSph — J-factor高"),
    ("segue1",    151.767,  16.082, "Segue 1 — 最高J-factor候補"),
    ("coma_ber",  186.746,  23.904, "Coma Berenices — Fermi公式解析採用"),
]

ON_RAD  = 2.0   # オン領域半径 [deg]
OFF_RAD = 5.0   # オフ領域外径 [deg]
# オン面積 / オフ面積 の比（バックグラウンド規格化用）
ALPHA = ON_RAD**2 / (OFF_RAD**2 - ON_RAD**2)


def analyze_target(name, ra, dec, label):
    csv_path = DATA_DIR / "CSV" / "dwarfs" / f"dwarf_{name}_780w.csv"
    if not csv_path.exists():
        print(f"  {name}: CSVなし スキップ"); return None

    df = pd.read_csv(csv_path)
    d  = df["ang_dist_deg"].values
    e  = df["energy_GeV"].values

    on_mask  = d < ON_RAD
    off_mask = (d >= ON_RAD) & (d < OFF_RAD)

    on_counts  = np.zeros(N_BINS)
    off_counts = np.zeros(N_BINS)

    for i in range(N_BINS):
        e_mask = (e >= BIN_EDGES[i]) & (e < BIN_EDGES[i+1])
        on_counts[i]  = (on_mask  & e_mask).sum()
        off_counts[i] = (off_mask & e_mask).sum()

    # 超過光子数：On - α×Off
    bg_est  = ALPHA * off_counts
    excess  = on_counts - bg_est
    # 有意性：Li & Ma (1983) 近似
    sigma = np.where(bg_est > 0, excess / np.sqrt(bg_est + ALPHA**2 * off_counts), 0)

    return {
        "name":       name,
        "label":      label,
        "on":         on_counts,
        "off":        off_counts,
        "bg":         bg_est,
        "excess":     excess,
        "sigma":      sigma,
        "total_on":   on_counts.sum(),
        "total_off":  off_counts.sum(),
    }


def plot_target(res):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.patch.set_facecolor("#05051a")
    fig.suptitle(f"{res['name'].upper()} — {res['label']}",
                 color="white", fontsize=13, fontweight="bold")

    # 左：カウントスペクトル
    ax = axes[0]
    ax.set_facecolor("#0d0d2a")
    ax.bar(range(N_BINS), res["on"],  color="#4488ff", alpha=0.8, label=f"On (<{ON_RAD}°)")
    ax.step(range(N_BINS), res["bg"], color="orange",  where="mid", lw=2,  label=f"BG estimate (α×Off)")
    ax.set_xticks(range(N_BINS))
    ax.set_xticklabels([f"{c:.1f}" for c in BIN_CENTERS], rotation=45, fontsize=8, color="white")
    ax.set_xlabel("Energy bin center [GeV]", color="white")
    ax.set_ylabel("Photon counts", color="white")
    ax.set_title("Count spectrum (On vs Background)", color="white")
    ax.tick_params(colors="white"); ax.legend(fontsize=9)
    ax.axvline(5, color="gold", ls="--", lw=1.5, label="Bin6 (20.76 GeV)")
    for sp in ax.spines.values(): sp.set_edgecolor("#444")
    ax.grid(alpha=0.2)

    # 右：有意性スペクトル
    ax = axes[1]
    ax.set_facecolor("#0d0d2a")
    colors = ["#ff4444" if abs(s) > 2 else "#4488ff" for s in res["sigma"]]
    ax.bar(range(N_BINS), res["sigma"], color=colors, alpha=0.85)
    ax.axhline(0,  color="white", lw=0.8)
    ax.axhline(2,  color="gold",  lw=1, ls="--", label="2σ")
    ax.axhline(-2, color="gold",  lw=1, ls="--")
    ax.axvline(5,  color="gold",  lw=2, label="Bin6 (20.76 GeV)")
    ax.set_xticks(range(N_BINS))
    ax.set_xticklabels([f"{c:.1f}" for c in BIN_CENTERS], rotation=45, fontsize=8, color="white")
    ax.set_xlabel("Energy bin center [GeV]", color="white")
    ax.set_ylabel("Significance σ", color="white")
    ax.set_title("Excess significance per bin", color="white")
    ax.tick_params(colors="white"); ax.legend(fontsize=9)
    for sp in ax.spines.values(): sp.set_edgecolor("#444")
    ax.grid(alpha=0.2)

    plt.tight_layout()
    out = OUT_DIR / f"dwarf_{res['name']}_spectrum.png"
    fig.savefig(out, dpi=130, bbox_inches="tight", facecolor="#05051a")
    plt.close(fig)
    return out


def plot_summary(results):
    """全天体のBin6有意性をまとめたバーチャート"""
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#05051a")
    ax.set_facecolor("#0d0d2a")

    names  = [r["name"].replace("_"," ").title() for r in results]
    sigmas = [r["sigma"][5] for r in results]   # Bin6 = index5
    colors = ["#ff4444" if s > 2 else "#4488ff" for s in sigmas]

    bars = ax.bar(names, sigmas, color=colors, alpha=0.85, width=0.5)
    ax.axhline(0, color="white", lw=0.8)
    ax.axhline(2, color="gold", lw=1.5, ls="--", label="2σ 目安")
    ax.axhline(-2, color="gold", lw=1.5, ls="--")

    for bar, s in zip(bars, sigmas):
        ax.text(bar.get_x()+bar.get_width()/2, s+0.05 if s>=0 else s-0.15,
                f"{s:.2f}σ", ha="center", va="bottom" if s>=0 else "top",
                color="white", fontsize=11, fontweight="bold")

    ax.set_ylabel("Bin6（20.76 GeV）有意性 σ", color="white", fontsize=12)
    ax.set_title("矮小銀河5天体 — 20.76 GeV 過剰の有意性 [780週]",
                 color="white", fontsize=13, fontweight="bold")
    ax.tick_params(colors="white")
    for sp in ax.spines.values(): sp.set_edgecolor("#444")
    ax.legend(fontsize=10); ax.grid(axis="y", alpha=0.2)

    plt.tight_layout()
    out = OUT_DIR / "dwarf_summary_bin6.png"
    fig.savefig(out, dpi=130, bbox_inches="tight", facecolor="#05051a")
    plt.close(fig)
    print(f"サマリー図: {out.name}")


def main():
    print("矮小銀河解析開始\n")
    results = []
    for name, ra, dec, label in TARGETS:
        print(f">>> {name}")
        res = analyze_target(name, ra, dec, label)
        if res is None: continue
        out = plot_target(res)
        b6 = res["sigma"][5]
        print(f"    Bin6(20.76GeV): On={res['on'][5]:.0f}  BG={res['bg'][5]:.1f}  "
              f"Excess={res['excess'][5]:.1f}  sigma={b6:.2f}σ")
        print(f"    → {out.name}")
        results.append(res)

    if results:
        plot_summary(results)
        print("\n=== Bin6（20.76 GeV）有意性まとめ ===")
        for r in results:
            flag = "★" if abs(r["sigma"][5]) > 2 else "  "
            print(f"  {flag} {r['name']:12s}: {r['sigma'][5]:+.2f}σ")
    print(f"\n完了 → {OUT_DIR}")

if __name__ == "__main__":
    main()
