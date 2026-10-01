#!/usr/bin/env python3
"""中間発表用: Bin6 の「差引前 / halo 以外を引いた図」2 パネル (Totani 配色・単位)。

ユーザ指示 (2026-07-24): 左=差引前(観測)、右=**halo 以外を全部引いた図**
(= 背景を消して 20 GeV の過剰=halo 信号を浮かび上がらせる) の正方形 2 枚。
配色・単位・平滑化は Totani に合わせる (`plot_bin6_totani_fig11_v20` を再利用)。

- 左「差引前」    : 点源マスク後の**観測フラックス**。Totani カラーマップの
  正の半分 (黒→赤→黄)、0..vmax
- 右「halo 以外を差引」: 観測 − (halo 以外の全モデル) = halo モデル + 残差。
  Totani Fig.11 右上と同じ量で、**中心に集中した過剰が見える**。
  発散カラーマップ (シアン→黒→黄)、±2×10⁻¹²

**旧版 (counts 単位の差引前/完全差引後) はこのファイルで置き換えた。**

出力: results/figures_interim2026/fig_bin6_before_after_v20.png
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

import plot_bin6_totani_fig11_v20 as f11  # noqa: E402
import mcmc_fit_all_bins as mfb  # noqa: E402
import plot_skymap_all_subtracted as _sub  # noqa: E402

OUT = BASE / "results/figures_interim2026/fig_bin6_before_after_v20.png"

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
    f_halo = d["p_full"][mfb.PARAM_NAMES.index("f_halo")]
    halo_counts = f_halo * tmpl["halo"]

    # 左: 差引前 = 観測 / 右: halo 以外を引いた図 = 観測 − (全モデル − halo)
    obs = f11._smooth_flux(counts, unit, valid, grey)
    halo_plus_resid = f11._smooth_flux((counts - mu_full) + halo_counts,
                                       unit, valid, grey)

    edges = _sub.L_BINS
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(14.5, 7.6))

    # --- 左: 差引前 (観測) --- 観測は正値なので正の半分カラーマップ + 0..vmax ---
    vmax = float(np.nanpercentile(obs, 99.5))
    mL = axL.pcolormesh(edges, edges, obs.T, cmap=_POS_HALF,
                        norm=Normalize(0.0, vmax), shading="flat",
                        rasterized=True)
    axL.text(0.03, 0.955, "21 GeV, before subtraction (observed)",
             transform=axL.transAxes, fontsize=10.5, color="white",
             family="monospace", weight="bold")
    _colorbar(axL, mL, [0, vmax / 2, vmax],
              ["0", f"{vmax/2:.0e}", f"{vmax:.0e}"])

    # --- 右: halo 以外を全部引いた図 (= 過剰) --- 発散カラーマップ ±2e-12 ------
    vlim = f11.VLIM
    mR = axR.pcolormesh(edges, edges, halo_plus_resid.T, cmap=f11._TOTANI_CMAP,
                        norm=TwoSlopeNorm(vmin=-vlim, vcenter=0.0, vmax=vlim),
                        shading="flat", rasterized=True)
    axR.text(0.03, 0.955, "21 GeV, all except halo subtracted (excess)",
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

    fig.suptitle("Bin6 (20.76 GeV): 差引前 → halo 以外を差引  【本研究 v20・Totani 配色/単位】",
                 fontsize=13.5, y=0.99)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150)
    plt.close()

    hp = ((counts - mu_full + halo_counts) / unit)[valid]
    print(f"\n完成: {OUT}")
    print(f"  観測フラックス表示レンジ: 0 〜 {vmax:.3e}")
    print(f"  右パネル(過剰)の最大: {np.nanpercentile(hp, 99.9):.3e} "
          f"(GC 方向に集中しているはず)")


if __name__ == "__main__":
    main()
