#!/usr/bin/env python3
"""中間発表用: Bin6 の「差引前 / 差引後」2 パネル図を Totani の色・単位で作る。

ユーザ指示 (2026-07-24): Totani Fig.11 の**配色と単位だけ**合わせて、
「左 = 差引前 (観測)、右 = 差引後 (残差)」の正方形 2 枚を横に並べた図にする。
4 パネル版 (`plot_bin6_totani_fig11_v20.py`) はそのまま残す。

- 左「差引前」: 点源(拡張源)マスク後の**観測フラックス** (背景モデル未差引)。
  観測は正値のみなので Totani カラーマップの**正の半分** (黒→赤→黄) を使う
- 右「差引後」: 観測 − v20 最良フィットの全モデル = **残差フラックス**。
  Totani の発散カラーマップ (シアン→黒→黄) を 0 中心で使う

単位・平滑化・灰色域・計算パイプラインは `plot_bin6_totani_fig11_v20` と同一
(その `build` / `_smooth_flux` / カラーマップ / 定数をそのまま再利用する)。

出力: results/figures_interim2026/fig_bin6_before_after_totani_style_v20.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize, TwoSlopeNorm

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "code"))

# 計算・配色・単位変換を 4 パネル版からそのまま流用する
import plot_bin6_totani_fig11_v20 as f11  # noqa: E402
import mcmc_fit_all_bins as mfb  # noqa: E402
import plot_skymap_all_subtracted as _sub  # noqa: E402

OUT = BASE / "results/figures_interim2026/fig_bin6_before_after_totani_style_v20.png"

# 観測 (正値のみ) 用: Totani カラーマップの正の半分 (黒 → 赤 → 橙 → 黄)
_POS_HALF = LinearSegmentedColormap.from_list(
    "totani_pos", f11._TOTANI_CMAP(np.linspace(0.5, 1.0, 256)))
_POS_HALF.set_bad("0.6")


def _colorbar(ax, m, ticks, labels):
    cb = ax.figure.colorbar(m, ax=ax, orientation="horizontal", location="top",
                            fraction=0.05, pad=0.02, ticks=ticks)
    cb.ax.set_xticklabels(labels, fontsize=8)
    cb.set_label(r"flux [cm$^{-2}$s$^{-1}$sr$^{-1}$MeV$^{-1}$]", fontsize=8.5)
    return cb


def main():
    d = f11.build()
    counts, tmpl, unit = d["counts"], d["tmpl"], d["unit"]
    valid, grey = d["valid"], d["grey"]

    mu_full = mfb._raw_mu(d["p_full"], tmpl)

    # 左: 差引前 = 観測フラックス / 右: 差引後 = 残差フラックス (どちらも σ=1° 平滑化)
    obs = f11._smooth_flux(counts, unit, valid, grey)
    resid = f11._smooth_flux(counts - mu_full, unit, valid, grey)

    edges = _sub.L_BINS
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(14.0, 7.2))

    # --- 左: 差引前 (観測) --- 正値なので正の半分カラーマップ + 0..vmax ---------
    vmax = float(np.nanpercentile(obs, 99.5))
    mL = axL.pcolormesh(edges, edges, obs.T, cmap=_POS_HALF,
                        norm=Normalize(0.0, vmax), shading="flat",
                        rasterized=True)
    axL.text(0.03, 0.955, "21 GeV, before subtraction (observed)",
             transform=axL.transAxes, fontsize=10.5, color="white",
             family="monospace", weight="bold")
    _colorbar(axL, mL, [0, vmax / 2, vmax],
              ["0", f"{vmax/2:.0e}", f"{vmax:.0e}"])

    # --- 右: 差引後 (残差) --- 発散カラーマップ + 0 中心 -------------------------
    vlim = f11.VLIM
    mR = axR.pcolormesh(edges, edges, resid.T, cmap=f11._TOTANI_CMAP,
                        norm=TwoSlopeNorm(vmin=-vlim, vcenter=0.0, vmax=vlim), shading="flat",
                        rasterized=True)
    axR.text(0.03, 0.955, "21 GeV, after full subtraction (residual)",
             transform=axR.transAxes, fontsize=10.5, color="white",
             family="monospace", weight="bold")
    _colorbar(axR, mR, [-2e-12, 0, 2e-12],
              [r"$-2\times10^{-12}$", "0", r"$2\times10^{-12}$"])

    for ax in (axL, axR):
        ax.set_xlabel("longitude $l$ [deg]", fontsize=9.5)
        ax.set_ylabel("latitude $b$ [deg]", fontsize=9.5)
        ax.set_xlim(60, -60)
        ax.set_ylim(-60, 60)
        ax.set_aspect("equal")

    fig.suptitle("Bin6 (20.76 GeV): 差引前 → 差引後  【本研究 v20・Totani 配色/単位】",
                 fontsize=13.5, y=0.99)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150)
    plt.close()

    rf = ((counts - mu_full) / unit)[valid]
    print(f"\n完成: {OUT}")
    print(f"  観測フラックス表示レンジ: 0 〜 {vmax:.3e}")
    print(f"  残差フラックス: 平均 {rf.mean():.3e} / rms {np.sqrt((rf**2).mean()):.3e}")


if __name__ == "__main__":
    main()
