"""[2026-07-31] 他天体 (矮小銀河 5 天体 + M31) の成分スペクトル図。

天の川の `plot_component_overlay_vN.py` に対応する図だが、**Totani の値は載せない**。
Totani (2025) は天の川ハロー ROI しか扱っておらず、矮小銀河・M31 に対応する数値が
論文中に存在しないため (2026-06-15 に Fig.1-16 を全文検索して確認済み)。したがって
本図は「本研究の各成分」だけを描き、比パネルも持たない。

形式は小多面 (天体ごとに 1 パネル、軸を共有)。成分の色は**天の川の図と同一**にする
(同じ概念には同じ記号・色を使う。gas=青 / ICS=橙 / IGRB=灰 / 既知点源=茶 / halo=赤)。

halo は負になりうるので、正の区間は実線、負の区間は破線 + x 印で絶対値を描く
(2026-07-23 の教訓「log 軸は負値を黙って捨てる」に従う)。

出力: results/mcmc_allbins_gasICS_v20_constructsplit/other_celestial_body/component_overlay.png
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
OUT = RES / "component_overlay.png"

# 天の川の plot_component_overlay_vN.py と同一の配色
COLORS = {"gas": "#1f77b4", "ics": "#ff7f0e", "iso": "#7f7f7f",
          "ps": "#8c564b", "halo": "#d62728"}
LABELS = {"gas": "gas (GALPROP)", "ics": "ICS (GALPROP)", "iso": "IGRB (等方背景)",
          "ps": "既知点源 (4FGL-DR4)", "halo": r"halo (NFW-$\rho^2$)"}
ORDER = ["gas", "ics", "iso", "ps", "halo"]
DISPLAY = {t.key: t.display for t in tg.load_targets()}
# 図に出す注目天体。全 80 天体は 1 枚に入らないので、
# 元の 5 矮小銀河 + マゼラン雲 + 局所銀河群の 4 天体に絞る。
# 全天体の一覧は ensemble_significance.png と summary.json を見ること。
FEATURED = ["draco_1", "sculptor_1", "ursa_minor_1", "segue_1", "coma_berenices_1",
            "lmc", "smc", "m31", "m33"]


def featured_targets() -> list[tg.Target]:
    ts = {t.key: t for t in tg.load_targets()}
    return [ts[k] for k in FEATURED if k in ts]

MIN_EVENTS = 20


def main() -> None:
    names = [t.key for t in featured_targets()]
    data = {n: json.loads((RES / f"{n}_spectrum.json").read_text()) for n in names}

    y_lo, y_hi = 1e-9, 1e-2
    fig, axes = plt.subplots(3, 3, figsize=(13.2, 10.5), sharex=True, sharey=True)
    for ax, name in zip(axes.ravel(), names):
        d = data[name]
        E = np.array(d["e_center_gev"])
        enough = np.array(d["n_events_bin"]) >= MIN_EVENTS
        for key in ORDER:
            y = np.array(d["e2dnde"][key])
            # halo は事象数の少ないビンで f_halo が拘束されず値が数桁暴れるので、
            # 統計的に意味のあるビンだけ描く (キャプションに理由を明記する)
            if key == "halo":
                y = np.where(enough, y, np.nan)
            pos = np.where(y > 0, y, np.nan)
            neg = np.where(y < 0, -y, np.nan)
            ax.plot(E, pos, "-", color=COLORS[key], lw=2.0, label=LABELS[key])
            if np.isfinite(neg).any():
                ax.plot(E, neg, "--x", color=COLORS[key], lw=1.6, ms=7, mew=1.8)
            # 振幅が下限 0 に張り付いたビンは log 軸に描けないので枠の下端に印を出す
            zero = np.isfinite(y) & (y == 0.0)
            if zero.any():
                ax.plot(E[zero], np.full(zero.sum(), y_lo * 1.6), "v",
                        color=COLORS[key], ms=6, mfc="white", mew=1.4, clip_on=False)
        ax.axvline(20.76, color="gold", ls="--", alpha=0.6, zorder=0)
        m = d["meta"]
        ax.set_title(f"{DISPLAY[name]}  (D = {m['D_kpc']:.0f} kpc)", fontsize=11)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.grid(True, which="major", color="#ededeb", lw=0.7, zorder=0)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)

    axes[0, 0].set_xlim(1.0, 1200.0)
    axes[0, 0].set_ylim(y_lo, y_hi)
    for ax in axes[:, 0]:
        ax.set_ylabel(r"$E^2\,dN/dE$ [MeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]", fontsize=10)
    for ax in axes[-1, :]:
        ax.set_xlabel("エネルギー [GeV]", fontsize=11)

    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=5, fontsize=10,
               frameon=False, bbox_to_anchor=(0.5, 0.075))
    fig.suptitle("他天体の成分スペクトル (本研究のみ)", fontsize=15, y=0.985)
    fig.text(0.5, 0.935,
             "破線 + × は負の値の絶対値 / ▽ は振幅が下限 0 に張り付いたビン / "
             "縦の金線 = 20.76 GeV / "
             "Totani (2025) には矮小銀河・M31 に対応する数値が無いため比較は載せない",
             ha="center", fontsize=9.5, color="#6b6b68")
    fig.text(0.5, 0.012,
             "Fermi-LAT Pass 8 UltraClean 779 週。各成分は ROI (半径 10°) 平均。"
             "点源は立体角を掛けていないため実効強度 (天の川の図と同じ扱い)。\n"
             f"halo は ROI 内の事象数が {MIN_EVENTS} 未満のビンでは振幅が拘束されず"
             "数桁暴れるため描いていない (有意度は halo_spectrum.png を参照)。",
             ha="center", fontsize=8.5, color="#6b6b68")

    fig.tight_layout(rect=(0.0, 0.115, 1.0, 0.925))
    fig.savefig(OUT, dpi=150)
    print(f"→ {OUT}")


if __name__ == "__main__":
    main()
