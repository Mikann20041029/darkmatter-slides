"""[2026-07-31] 他天体 (矮小銀河 5 天体 + M31) の有意度スペクトル (発表用)。

天の川の `significance_spectrum.png` に対応する図。ただし**Totani (2025) との比較は載せない**
(Totani は天の川ハロー ROI しか扱っておらず、矮小銀河・M31 に対応する数値が論文中に無い)。
したがって比パネルも持たない。

発表用なので天の川版と同じ体裁にする: 明色・タイトル無し・軸ラベル特大・線主体。
6 天体を 1 つの軸に重ねる (すべて ±2σ 帯に収まるので重ねても読め、
「どれも検出されていない」ことが一目で分かる)。

診断用の小多面版は `halo_spectrum.png` (こちらは天体ごとにパネルを分ける)。

出力: results/mcmc_allbins_gasICS_v20_constructsplit/other_celestial_body/
      significance_spectrum.png と同 significance_table.txt (図に頼らず読める表)
"""
from __future__ import annotations

import json
import pathlib as _pathlib
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))
from jp_font import setup_jp_font
import target_geometry as tg

setup_jp_font()

BASE = _pathlib.Path(__file__).resolve().parent.parent
RES = BASE / "results/mcmc_allbins_gasICS_v20_constructsplit/other_celestial_body"
OUT = RES / "significance_spectrum.png"
OUT_TXT = RES / "significance_table.txt"

# categorical slot 1..6 (light) — 固定順で割り当てる (循環させない)
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300",
          "#4a3aa7", "#e34948", "#7f7f7f"]
INK = "#1a1a19"
MUTED = "#6b6b68"
MIN_EVENTS = 20
DISPLAY = {t.key: t.display for t in tg.load_targets()}
# 図に出す注目天体。全 80 天体は 1 枚に入らないので、
# 元の 5 矮小銀河 + マゼラン雲 + 局所銀河群の 4 天体に絞る。
# 全天体の一覧は ensemble_significance.png と summary.json を見ること。
FEATURED = ["draco_1", "sculptor_1", "ursa_minor_1", "segue_1", "coma_berenices_1",
            "lmc", "smc", "m31", "m33"]


def featured_targets() -> list[tg.Target]:
    ts = {t.key: t for t in tg.load_targets()}
    return [ts[k] for k in FEATURED if k in ts]



def main() -> None:
    names = [t.key for t in featured_targets()]
    data = {n: json.loads((RES / f"{n}_spectrum.json").read_text()) for n in names}

    fig, ax = plt.subplots(figsize=(12.4, 6.6))
    ax.axhspan(-2, 2, color="#eeeeec", zorder=0)
    ax.axhline(0, color=MUTED, lw=1.2, zorder=1)
    ax.axvline(20.76, color=MUTED, lw=1.2, ls=":", zorder=1)

    for color, name in zip(SERIES, names):
        d = data[name]
        e = np.array(d["e_center_gev"])
        s = np.array(d["significance_sigma"])
        ok = np.array(d["n_events_bin"]) >= MIN_EVENTS
        ax.plot(e, s, "-", color=color, lw=2.4, label=DISPLAY[name], zorder=3)
        ax.plot(e[ok], s[ok], "o", ms=8, color=color, zorder=4)
        ax.plot(e[~ok], s[~ok], "o", ms=8, mfc="white", mec=color, mew=2.0, zorder=4)

    ax.set_xscale("log")
    ax.set_xlim(1.0, 1200.0)
    ax.set_ylim(-7.0, 4.0)
    ax.set_xlabel("光子エネルギー [GeV]", fontsize=22, color=INK)
    ax.set_ylabel("halo 成分の有意度 σ", fontsize=22, color=INK)
    ax.tick_params(labelsize=15, colors=MUTED)
    ax.grid(True, axis="y", color="#ededeb", lw=0.9, zorder=0)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)

    ax.text(1.15, 2.25, "±2σ", fontsize=13, color=MUTED, va="bottom")
    ax.text(21.6, -6.7, "20.76 GeV", fontsize=13, color=MUTED, rotation=90, va="bottom")
    ax.legend(fontsize=14, loc="center left", bbox_to_anchor=(1.005, 0.5),
              frameon=False)

    fig.text(0.012, 0.015,
             f"白抜き = ROI 内の事象数が {MIN_EVENTS} 未満のビン (統計的に意味が無い)。"
             "M31 の低エネルギー側の負値は M31 自身の 4FGL 天体を点源として置いたことによる系統誤差。",
             fontsize=10.5, color=MUTED)

    fig.tight_layout(rect=(0.0, 0.05, 0.84, 1.0))
    fig.savefig(OUT, dpi=150)
    print(f"→ {OUT}")

    # 図に頼らず読める表も出す (低コントラストの系列があるため)
    lines = [f"{'エネルギー[GeV]':>14}" + "".join(f"{DISPLAY[n][:12]:>14}" for n in names)]
    e = np.array(data[names[0]]["e_center_gev"])
    for i in range(len(e)):
        row = f"{e[i]:14.2f}"
        for n in names:
            d = data[n]
            mark = "" if d["n_events_bin"][i] >= MIN_EVENTS else "*"
            row += f"{d['significance_sigma'][i]:+13.2f}{mark:1s}"
        lines.append(row)
    lines.append(f"* = ROI 内の事象数が {MIN_EVENTS} 未満 (統計的に意味が無い)")
    OUT_TXT.write_text("\n".join(lines) + "\n")
    print(f"→ {OUT_TXT}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
