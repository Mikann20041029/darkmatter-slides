"""[2026-07-31] 他天体 (矮小銀河 5 天体 + M31) のハロー有意度スペクトル (診断用)。

天の川の `halo_spectrum.png` に対応する図。ただし天の川版は上段 f_halo (振幅) /
下段 有意度 の 2 段だが、**本図は有意度だけにする**。理由は f_halo が天体ごとに
別の rho_s^2 で規格化されており、**天体間で数値を比べる意味が無い**ため
(`apply_v20_method_targets.py` の [ASSUMPTION] 4 を参照)。

形式は小多面 (天体ごとに 1 パネル、軸を共有)。1 系列なので凡例は不要。
事象数が 20 未満のビンは白抜きマーカーで区別する (落とさずに描いて理由を図中に書く。
2026-07-24 の教訓「表示条件でデータを黙って落とすと『無い』と誤読される」)。

配色は天の川の halo_spectrum.png に合わせた暗色テーマ (診断用の図であることが
一目で分かるようにする。発表用は significance_spectrum.png のほう)。

出力: results/mcmc_allbins_gasICS_v20_constructsplit/other_celestial_body/halo_spectrum.png
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
OUT = RES / "halo_spectrum.png"

BG = "#0d0d18"          # 天の川 halo_spectrum.png と同系の暗色背景
FG = "#e8e8e6"
LINE = "#2ee59d"        # 天の川版の有意度パネルと同じ緑
GUIDE = "#9a9aa0"
WARN = "#e05a5a"
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

    fig, axes = plt.subplots(3, 3, figsize=(12.6, 10.0), sharex=True, sharey=True,
                             facecolor=BG)
    for ax, name in zip(axes.ravel(), names):
        d = data[name]
        e = np.array(d["e_center_gev"])
        s = np.array(d["significance_sigma"])
        n_ev = np.array(d["n_events_bin"])
        ok = n_ev >= MIN_EVENTS

        ax.set_facecolor(BG)
        # グリッドの目盛が ±2 と重なるので、グリッドを必ず下に敷く
        # (これをしないと ±2σ の赤破線がパネルによって暗いグリッドに隠れる)
        ax.set_axisbelow(True)
        ax.axhline(0, color=GUIDE, lw=1.0, ls=":", zorder=2)
        for y in (-2, 2):
            ax.axhline(y, color=WARN, lw=1.4, ls="--", alpha=0.95, zorder=2)
        ax.axvline(20.76, color="gold", lw=1.0, ls=":", alpha=0.7, zorder=2)
        ax.plot(e, s, "-", color=LINE, lw=2.0, zorder=3)
        ax.plot(e[ok], s[ok], "o", ms=7, color=LINE, zorder=4)
        ax.plot(e[~ok], s[~ok], "o", ms=7, mfc=BG, mec=LINE, mew=1.8, zorder=4)

        m = d["meta"]
        ax.set_title(f"{DISPLAY[name]}  (D = {m['D_kpc']:.0f} kpc, "
                     r"$\theta_s$ = " + f"{m['theta_s_deg']:.2f}°)",
                     fontsize=11, color=FG)
        ax.set_xscale("log")
        ax.grid(True, axis="y", color="#23233a", lw=0.8, zorder=0)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(GUIDE)
        ax.tick_params(colors=FG, labelsize=9)

    axes[0, 0].set_ylim(-7.0, 4.0)
    axes[0, 0].set_xlim(1.0, 1200.0)
    for ax in axes[:, 0]:
        ax.set_ylabel("有意度 [σ] (符号 = f_halo の符号)", fontsize=10, color=FG)
    for ax in axes[-1, :]:
        ax.set_xlabel("Energy [GeV]", fontsize=11, color=FG)

    fig.suptitle("他天体: ハロー成分の有意度スペクトル (全13ビン)",
                 fontsize=15, color=FG, y=0.985)
    fig.text(0.5, 0.93,
             "赤破線 = ±2σ / 金の点線 = 20.76 GeV / "
             f"白抜き = ROI 内の事象数が {MIN_EVENTS} 未満のビン (統計的に意味が無い)",
             ha="center", fontsize=9.5, color=GUIDE)
    fig.text(0.5, 0.015,
             "振幅 f_halo は天体ごとに別の ρ_s² で規格化されており天体間で比較できないため、"
             "天の川の halo_spectrum.png と違い有意度のみを示す。",
             ha="center", fontsize=8.5, color=GUIDE)

    fig.tight_layout(rect=(0.0, 0.05, 1.0, 0.92))
    fig.savefig(OUT, dpi=150, facecolor=BG)
    print(f"→ {OUT}")


if __name__ == "__main__":
    main()
