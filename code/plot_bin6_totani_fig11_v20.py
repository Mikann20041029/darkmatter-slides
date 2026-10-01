#!/usr/bin/env python3
"""中間発表用: Totani (2025) Fig.11 を v20 で再現する (21 GeV = Bin6)。

Totani Fig.11 は NFW-ρ² フィットの 4 パネルマップ (すべて 21 GeV ビン):

  - 左上「no-halo fit residual」  : halo 無しフィットの残差 (= halo 信号 + 雑音)
  - 右上「NFW-ρ² model+residual」: 観測 − (halo 以外の全モデル) (= halo モデル + 残差)
  - 左下「NFW-ρ² model」          : halo モデルそのもの (= 滑らかな球対称)
  - 右下「NFW-ρ² fit residual」   : halo 込みフィットの残差 (= 雑音)

**Totani に合わせたもの (ユーザ指示 2026-07-24)**:
  - 単位: **flux [cm⁻²s⁻¹sr⁻¹MeV⁻¹]** (counts ではない)。
    flux = counts / (exposure × dΩ × dE)。mcmc の `unit` 係数の逆数
  - 配色: シアン→青→黒(0)→赤→橙→黄 の発散カラーマップ
  - カラーバー: 各パネル上部・水平・目盛 ±2×10⁻¹² と 0
  - 平滑化: **Gaussian σ = 1°** (0.125° 画素で 8 px)。銀河面のギャップが
    にじまないよう normalized convolution (valid で重み付け)
  - 灰色域: 銀河面 |b| < 10° と拡張源マスク (Totani の grey circular regions)

**計算は v20 と完全に同一のパイプライン** (`mcmc_fit_all_bins` を v20 の
環境変数つきで import)。最良フィット値 (halo 込み・halo 無しの両方) は
`results/mcmc_allbins_gasICS_v20_constructsplit/mcmc_bin06.json` から読む。

出力: results/figures_interim2026/fig_bin6_totani_fig11_v20.png
"""
from __future__ import annotations

import os

os.environ.setdefault("MCMC_ULTRACLEAN", "1")
os.environ.setdefault("MCMC_PIXEL_DEG", "0.125")
os.environ.setdefault("MCMC_DISK_BUBBLE", "1")
os.environ.setdefault("MCMC_CELL_LIKELIHOOD", "1")
os.environ.setdefault("MCMC_SIGNFREE_HALO", "1")
os.environ.setdefault("MCMC_CONSTRUCT_SPLIT", "1")

import json
import sys
from pathlib import Path

import numpy as np
from scipy.ndimage import gaussian_filter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib import font_manager as _fm

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "code"))

_FONT = Path.home() / ".local/share/fonts/NotoSansCJKjp-Regular.otf"
if _FONT.exists():
    _fm.fontManager.addfont(str(_FONT))
    plt.rcParams["font.family"] = _fm.FontProperties(fname=str(_FONT)).get_name()

import mcmc_fit_all_bins as mfb  # noqa: E402
import plot_skymap_all_subtracted as _sub  # noqa: E402

RESDIR = BASE / "results/mcmc_allbins_gasICS_v20_constructsplit"
BIN6 = 5
SIGMA_PX = 8.0                        # 1° / 0.125°
VLIM = 2.6e-12                        # カラーバー範囲 (Totani と同じ ±~2.6e-12)
OUT = BASE / "results/figures_interim2026/fig_bin6_totani_fig11_v20.png"

# Totani Fig.11 の配色 (シアン→青→黒→赤→橙→黄)
_TOTANI_CMAP = LinearSegmentedColormap.from_list("totani_flux", [
    (0.00, (0.0, 1.0, 1.0)),   # cyan (最も負)
    (0.12, (0.0, 0.35, 1.0)),  # blue
    (0.30, (0.0, 0.0, 0.45)),  # dark blue
    (0.50, (0.0, 0.0, 0.0)),   # black (0)
    (0.68, (0.42, 0.0, 0.0)),  # dark red
    (0.82, (1.0, 0.12, 0.0)),  # red
    (0.92, (1.0, 0.55, 0.0)),  # orange
    (1.00, (1.0, 1.0, 0.0)),   # yellow (最も正)
])
_TOTANI_CMAP.set_bad("0.6")            # 灰色域


def build():
    """v20 の設定で bin6 の counts / templates / unit / 両フィット値を返す。"""
    np.random.seed(mfb.SEED)
    print("露出マップ...")
    expmaps, ec = mfb.load_exposure_maps()
    assert np.allclose(ec, mfb.BIN_CENTERS)
    print("イベント...")
    df_all = mfb.load_all_events()
    print("NFW J-map (数分)...")
    j_map = mfb.nfw_j_map()
    nfw_norm, _ = mfb.calibrate_nfw_norm(expmaps[BIN6], j_map)
    print("バブル構築...")
    df_bubble = mfb.load_events_with_disk() if mfb.DISK_BUBBLE else df_all
    b_pos, b_neg = mfb.build_bubble_counts_template(df_bubble)
    print("Loop I...")
    ls1, ls2 = _sub.loop_i_shell_templates()

    emin, emax = mfb.BIN_EDGES[BIN6], mfb.BIN_EDGES[BIN6 + 1]
    sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
    counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg,
                                  bins=[_sub.L_BINS, _sub.B_BINS])
    gas_i, ics_i = _sub._load_galprop_gas_ics_templates(emin, emax)
    ics_comp = _sub._load_healpix_ics_components(emin, emax) if mfb.ICS_SPLIT else None
    tmpl = mfb.build_templates_for_bin(
        BIN6, counts, expmaps[BIN6], gas_i, ics_i,
        bubble_counts_bin3_pos=b_pos, bubble_counts_bin3_neg=b_neg,
        expmap_bubble_bin=expmaps[mfb.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
        loop_shell1=ls1, loop_shell2=ls2, ics_components=ics_comp,
    )
    # counts → flux の変換係数 (mcmc の unit と厳密に同一)
    de_mev = (emax - emin) * 1000.0
    unit = expmaps[BIN6] * mfb.PIX_SOLID_ANGLE_SR * de_mev

    jd = json.loads((RESDIR / "mcmc_bin06.json").read_text())
    p_full = [jd["params"][n]["median"] for n in mfb.PARAM_NAMES]
    p_noh = [jd["params_no_halo_pointest"][n] for n in mfb.PARAM_NAMES[:-1]]

    BG = _sub.B_GRID
    valid = (~np.isnan(counts) & ~_sub.extended_source_mask()
             & (np.abs(BG) >= 10) & (np.abs(BG) <= 60))
    grey = (np.abs(BG) < 10) | _sub.extended_source_mask()
    return dict(counts=counts, tmpl=tmpl, unit=unit, p_full=p_full,
                p_noh=p_noh, valid=valid, grey=grey)


def _smooth_flux(counts_map, unit, valid, grey):
    """counts → flux → σ=1° 平滑化 (normalized convolution) → 灰色域を NaN。"""
    flux = counts_map / unit
    w = valid.astype(float)
    num = gaussian_filter(flux * w, SIGMA_PX, mode="nearest")
    den = gaussian_filter(w, SIGMA_PX, mode="nearest")
    sm = np.where(den > 1e-6, num / den, 0.0)
    return np.where(grey, np.nan, sm)


def _panel(ax, field, title, edges):
    norm = TwoSlopeNorm(vmin=-VLIM, vcenter=0.0, vmax=VLIM)
    m = ax.pcolormesh(edges, edges, field.T, cmap=_TOTANI_CMAP, norm=norm,
                      shading="flat", rasterized=True)
    ax.text(0.03, 0.93, title, transform=ax.transAxes, fontsize=10.5,
            color="white", family="monospace", weight="bold")
    ax.set_xlabel("longitude $l$ [deg]", fontsize=9)
    ax.set_ylabel("latitude $b$ [deg]", fontsize=9)
    ax.set_xlim(60, -60)
    ax.set_ylim(-60, 60)
    ax.set_aspect("equal")
    cb = ax.figure.colorbar(m, ax=ax, orientation="horizontal",
                            location="top", fraction=0.055, pad=0.02,
                            ticks=[-2e-12, 0, 2e-12])
    cb.ax.set_xticklabels([r"$-2\times10^{-12}$", "0", r"$2\times10^{-12}$"],
                          fontsize=8)
    cb.set_label(r"flux [cm$^{-2}$s$^{-1}$sr$^{-1}$MeV$^{-1}$]", fontsize=8.5)
    return m


def main():
    d = build()
    counts, tmpl, unit = d["counts"], d["tmpl"], d["unit"]
    valid, grey = d["valid"], d["grey"]

    mu_full = mfb._raw_mu(d["p_full"], tmpl)
    mu_noh = mfb._raw_mu(d["p_noh"], tmpl)               # halo 項なし
    f_halo = d["p_full"][mfb.PARAM_NAMES.index("f_halo")]
    halo_counts = f_halo * tmpl["halo"]

    # 4 パネルの counts マップ
    resid_noh = counts - mu_noh                 # 左上: no-halo fit residual
    halo_plus_resid = (counts - mu_full) + halo_counts  # 右上: halo model + residual
    halo_model = halo_counts                    # 左下: halo model
    resid_full = counts - mu_full               # 右下: with-halo fit residual

    panels = [
        (resid_noh,        "21 GeV, no-halo fit residual"),
        (halo_plus_resid,  "21 GeV, NFW-ρ² model+residual"),
        (halo_model,       "21 GeV, NFW-ρ² model"),
        (resid_full,       "21 GeV, NFW-ρ² fit residual"),
    ]

    edges = _sub.L_BINS
    fig, axes = plt.subplots(2, 2, figsize=(13.0, 11.5))
    for ax, (cmap_counts, title) in zip(axes.ravel(), panels):
        field = _smooth_flux(cmap_counts, unit, valid, grey)
        _panel(ax, field, title, edges)

    fig.suptitle("Totani Fig.11 相当 — NFW-ρ² フィットの 21 GeV マップ 【本研究 v20】",
                 fontsize=13, y=0.995)
    fig.tight_layout(rect=(0, 0, 1, 0.98))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150)
    plt.close()

    # 数値サマリ
    rf = (resid_full / unit)[valid]
    print(f"\n完成: {OUT}")
    print(f"  halo 込み残差 flux: 平均 {rf.mean():.3e} / rms {np.sqrt((rf**2).mean()):.3e}")
    hm = (halo_model / unit)[valid]
    print(f"  halo モデル flux: 最大 {hm.max():.3e} (GC 方向で最大のはず)")


if __name__ == "__main__":
    main()
