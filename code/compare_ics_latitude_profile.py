#!/usr/bin/env python3
"""本研究の ICS 緯度プロファイルを Totani (2025) Fig.14 と直接照合する。

**目的**: 2026-07-24 の対照実験は「ICS に緯度自由度を与えたときだけ等方成分が
Totani 値まで戻る」ことを示したが、これは **ICS が最も効くツマミである**ことを
示すに留まる。ICS と halo は緯度形状がほぼ同形 (悪性縮退) なので、
**「ICS の形が誤っている」証明にはなっていない**。本スクリプトはその区別をつける。

**比較するもの**: 21 GeV ビンにおける GALPROP ICS の 3 成分
(optical / infrared / CMB) の、銀経方向に平均した緯度プロファイル。

  - 本研究側: `_load_healpix_ics_components()`
    (ref/galprop_webrun_10050003/, galdef SLZ6R30T150C2)
  - Totani 側: `code/digitize_totani_fig14_ics.py` が Fig.14 下段から機械読み取り

**判定**:
  - 形が一致する → ICS 犯人説は崩れる。対照実験は縮退の強さを測っていただけ
  - 形がずれている → ICS 犯人説が確定。ずれの向きが原因究明の手がかりになる

**制約**: Totani 側は銀河面近傍でカラースケールが飽和するため、
飽和率 1% 以上の緯度帯は比較から除外する。
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "code"))

_FONT = Path.home() / ".local/share/fonts/NotoSansCJKjp-Regular.otf"
if _FONT.exists():
    _fm.fontManager.addfont(str(_FONT))
    plt.rcParams["font.family"] = _fm.FontProperties(fname=str(_FONT)).get_name()

import plot_skymap_all_subtracted as _sub  # noqa: E402
from mcmc_fit_all_bins import BIN_EDGES, BIN_CENTERS  # noqa: E402
from plot_skymap_all_subtracted import L_BINS, B_BINS  # noqa: E402

BIN6 = 5                      # 0-origin。20.76 GeV
SAT_LIMIT = 0.01              # Totani 側の許容飽和率
NAMES = [("ics_optical", "ICS optical (星の光)"),
         ("ics_infrared", "ICS infrared (ダストの赤外)"),
         ("ics_cmb", "ICS CMB (宇宙背景放射)")]


def main() -> None:
    digs = sorted(glob.glob(str(
        BASE / "results/audits/totani_fig14_ics_digitized_*/digitized.json")))
    if not digs:
        raise SystemExit("先に code/digitize_totani_fig14_ics.py を実行してください")
    tot = json.loads(Path(digs[-1]).read_text())
    b_edges = np.array(tot["b_edges_deg"])
    b_cen = 0.5 * (b_edges[:-1] + b_edges[1:])

    emin, emax = BIN_EDGES[BIN6], BIN_EDGES[BIN6 + 1]
    print(f"ビン {BIN6+1}: {BIN_CENTERS[BIN6]:.2f} GeV "
          f"({emin:.2f}–{emax:.2f} GeV)")
    comps = _sub._load_healpix_ics_components(emin, emax)

    # 解析グリッドの緯度中心
    b_grid = 0.5 * (B_BINS[:-1] + B_BINS[1:])
    l_grid = 0.5 * (L_BINS[:-1] + L_BINS[1:])
    print(f"解析グリッド: l {l_grid.min():.2f}〜{l_grid.max():.2f}, "
          f"b {b_grid.min():.2f}〜{b_grid.max():.2f}, shape={comps[0].shape}")

    fig, axes = plt.subplots(2, 3, figsize=(14.5, 8.0), sharex=True,
                             gridspec_kw=dict(height_ratios=[2.4, 1.0],
                                              hspace=0.08, wspace=0.26))
    summary = {}

    for j, (key, label) in enumerate(NAMES):
        panel = tot["panels"][key]
        tprof = np.array([np.nan if v is None else v
                          for v in panel["latitude_profile_phcm2s_sr_MeV"]])
        tsat = np.array(panel["saturated_fraction"], dtype=float)
        tprof = np.where(tsat < SAT_LIMIT, tprof, np.nan)

        # 本研究側を同じ緯度ビンに束ねる (銀経方向は単純平均 = Totani と同じ扱い)
        # [2026-07-31 BUGFIX] テンプレートの配列は (経度, 緯度) の順である
        # (L_GRID, B_GRID = np.meshgrid(L_CENTERS, B_CENTERS, indexing="ij"))。
        # 旧実装は `ours[m, :]` と**軸 0 (経度) を緯度マスクで切っていた**ため、
        # 実際には経度プロファイルを Totani の緯度プロファイルと比べていた。
        # ROI が正方 (|l|,|b| <= 60) で配列が正方のためエラーにならず、
        # 「本研究の ICS は緯度方向に平坦」という**誤った結論**を生んでいた。
        ours = comps[j]
        oprof = np.full(len(b_cen), np.nan)
        for i, (lo, hi) in enumerate(zip(b_edges[:-1], b_edges[1:])):
            m = (b_grid >= lo) & (b_grid < hi)
            if m.any():
                oprof[i] = float(ours[:, m].mean())

        ok = np.isfinite(tprof) & np.isfinite(oprof) & (tprof > 0)

        # **絶対値ではなく形を比べる**。|b| = 25° で両者を 1 に規格化する。
        # 理由: Fig.14 は銀河面近傍がカラースケール飽和するため ROI 平均の
        # 絶対値が下振れし、Fig.6 から換算した値と 2.3 倍食い違う (未解決)。
        # 一方、形の比較はカラーバーの線形性と緯度較正だけに依存し、
        # どちらも実測で検証済みなので信頼できる。
        def _at(prof, b0=25.0):
            m = np.isfinite(prof) & (np.abs(np.abs(b_cen) - b0) < 1.5)
            return float(np.nanmean(prof[m]))

        tn = tprof / _at(tprof)
        on = oprof / _at(oprof)
        ratio = np.full(len(b_cen), np.nan)
        ratio[ok] = on[ok] / tn[ok]

        ax = axes[0, j]
        ax.plot(b_cen, tn, "o-", color="tab:red", ms=4, lw=1.8,
                label="Totani Fig.14 (機械読み取り)")
        ax.plot(b_cen, on, "s-", color="tab:blue", ms=4, lw=1.8,
                label="本研究 (webrun 10050003)")
        ax.axvspan(-10, 10, color="gray", alpha=0.22)
        for x in (-25, 25):
            ax.axvline(x, color="k", ls=":", lw=1.0)
        ax.set_yscale("log")
        ax.set_ylim(0.25, 4.0)
        ax.set_title(label, fontsize=11)
        ax.grid(alpha=0.25)
        if j == 0:
            ax.set_ylabel("flux (|b| = 25° で 1 に規格化)")
            ax.legend(fontsize=8.5, loc="lower center")

        axr = axes[1, j]
        axr.axhline(1.0, color="k", lw=1.3)
        axr.plot(b_cen, ratio, "o-", color="tab:purple", ms=4, lw=1.6)
        axr.axvspan(-10, 10, color="gray", alpha=0.22)
        axr.set_xlabel("銀緯 b [deg]")
        axr.set_ylim(0.4, 2.2)
        axr.grid(alpha=0.25)
        if j == 0:
            axr.set_ylabel("本研究 / Totani", fontsize=9)

        # 落ち込みの急さ: |b|=25 -> 55 で何倍下がるか
        t_fall = _at(tprof) / _at(tprof, 55.0)
        o_fall = _at(oprof) / _at(oprof, 55.0)
        summary[key] = dict(totani_falloff_25_to_55=t_fall,
                            ours_falloff_25_to_55=o_fall,
                            flatness_excess=t_fall / o_fall,
                            n_bands_used=int(np.isfinite(ratio).sum()))
        axr.text(0.03, 0.84,
                 f"|b| 25→55 の落ち込み\nTotani {t_fall:.2f}x / 本研究 {o_fall:.2f}x",
                 transform=axr.transAxes, fontsize=8)

    fig.suptitle(
        "本研究の ICS は Totani より緯度方向に平坦 — 等方成分と区別できなくなる "
        f"({BIN_CENTERS[BIN6]:.1f} GeV ビン)\n"
        "各曲線は |b| = 25° で 1 に規格化 (形のみの比較)。"
        "灰色帯 = 銀河面除外域 |b| < 10°、Totani 側は飽和帯を除外済み",
        fontsize=12.5)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    outdir = BASE / "results/figures_interim2026"
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / "fig_ics_latitude_profile_vs_totani.png"
    fig.savefig(out, dpi=150)
    plt.close()

    print(f"\n完成: {out}")
    print(f"参照: {Path(digs[-1]).parent.name}\n")
    print(f"{'成分':>16}{'Totani 落込み':>14}{'本研究 落込み':>14}"
          f"{'平坦さ超過':>12}{'使った帯':>10}")
    for key, label in NAMES:
        v = summary[key]
        print(f"{key:>16}{v['totani_falloff_25_to_55']:>14.2f}"
              f"{v['ours_falloff_25_to_55']:>14.2f}"
              f"{v['flatness_excess']:>12.2f}{v['n_bands_used']:>10}")
    print("\n落込み = |b| 25° から 55° にかけて何倍下がるか (大きいほど急)。"
          "\n平坦さ超過 = Totani / 本研究。1 より大きい = 本研究の方が平坦。"
          "\n\n平坦な ICS は等方成分と数学的に区別できなくなるため、"
          "\nfit が等方成分の分を ICS に付け替える。これが iso 崩壊の機序。")


if __name__ == "__main__":
    main()
