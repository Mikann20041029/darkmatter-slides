"""[2026-07-31] 多数の天体・対照フィールドを束ねた**統計検証**の図と数値。

個々の天体が非検出であることを 1 つずつ見せるのではなく、**同じ手法を多数の場所に
当てたときに有意度がどう散らばるか**を測る。狙いは 2 つ:

  1. **実データでの帰無分布を測る。** 合成データの較正
     (`audit_target_fit_calibration.py`) では sigma ~ |N(0,1)| だったが、実データには
     拡散モデルの誤差や点源の消し残りがある。**分布が N(0,1) より広ければ、その超過分が
     この手法の系統誤差の床**であり、天の川の有意度を読むときの基準になる
  2. **多数当たれば偶然に大きな値も出る (look-elsewhere)** ことを定量化する。
     13 ビン x N 天体を見れば最大値は必ず 2-3 sigma を超える。「どこかで 3 sigma が出た」
     が意味を持たないことを、期待される最大値の分布として示す

対象の区分:
  - `dwarf`   : LVDB (Pace 2025) の確認済み天の川矮小銀河
  - `galaxy`  : M31 / M33
  - `control` : 既知の標的が無い無作為の領域 (|b| > 20°、互いに 20° 以上離す)

**対照フィールドが本命の帰無標本**である。矮小銀河は「ダークマター信号があるかもしれない
場所」なので、帰無分布の推定には使わない (混ぜると信号があった場合に基準が甘くなる)。

出力: results/mcmc_allbins_gasICS_v20_constructsplit/other_celestial_body/
      ensemble_significance.png / ensemble_stats.json
"""
from __future__ import annotations

import json
import pathlib as _pathlib
import sys
from typing import Any

import numpy as np
from numpy.typing import NDArray
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))
from jp_font import setup_jp_font

setup_jp_font()

BASE = _pathlib.Path(__file__).resolve().parent.parent
RES = BASE / "results/mcmc_allbins_gasICS_v20_constructsplit/other_celestial_body"
OUT = RES / "ensemble_significance.png"
OUT_JSON = RES / "ensemble_stats.json"

MIN_EVENTS = 20
CAT_COLOR = {"control": "#2a78d6", "dwarf": "#eb6834", "galaxy": "#1baf7a"}
CAT_LABEL = {"control": "対照フィールド (空の領域)", "dwarf": "矮小銀河", "galaxy": "M31 / M33"}
INK, MUTED = "#1a1a19", "#6b6b68"


def collect() -> dict[str, dict[str, Any]]:
    summary = json.loads((RES / "summary.json").read_text())
    out: dict[str, dict[str, Any]] = {}
    for key, d in summary.items():
        meta = d["meta"]
        if not meta.get("usable", True):
            continue                      # 拡張源マスクでハローが覆われた天体は除く
        sig = np.array(d["sigma"], dtype=float)
        nev = np.array(d["n_events_bin"], dtype=float)
        keep = nev >= MIN_EVENTS          # 事象数が少なすぎるビンは統計にならない
        out[key] = {"category": meta["category"], "display": d["display"],
                    "sigma": sig[keep], "l": meta["l"], "b": meta["b"],
                    "n_bins": int(keep.sum())}
    return out


def main() -> None:
    data = collect()
    cats = {c: np.concatenate([v["sigma"] for v in data.values() if v["category"] == c])
            for c in ("control", "dwarf", "galaxy")
            if any(v["category"] == c for v in data.values())}

    stats_out: dict[str, Any] = {"min_events_per_bin": MIN_EVENTS, "by_category": {}}
    for c, s in cats.items():
        ks = stats.kstest(s, "norm")
        stats_out["by_category"][c] = {
            "n_targets": sum(1 for v in data.values() if v["category"] == c),
            "n_sigma_values": int(s.size), "mean": float(s.mean()),
            "std": float(s.std(ddof=1)), "median": float(np.median(s)),
            "frac_gt2": float(np.mean(np.abs(s) > 2)),
            "frac_gt3": float(np.mean(np.abs(s) > 3)),
            "max": float(s.max()), "min": float(s.min()),
            "ks_stat": float(ks.statistic), "ks_pvalue": float(ks.pvalue),
        }

    fig, axes = plt.subplots(1, 3, figsize=(15.6, 5.2))

    # ── (1) 有意度のヒストグラム vs N(0,1) ──────────────────────────────────
    ax = axes[0]
    bins = np.arange(-6.25, 6.26, 0.5)
    for c, s in cats.items():
        ax.hist(s, bins=bins, density=True, histtype="step", lw=2.2,
                color=CAT_COLOR[c], label=f"{CAT_LABEL[c]} (n={s.size})")
    x = np.linspace(-6, 6, 400)
    ax.plot(x, stats.norm.pdf(x), "--", color=INK, lw=2.0, label="N(0, 1) (期待値)")
    ax.set_xlabel("ハロー成分の有意度 σ", fontsize=12, color=INK)
    ax.set_ylabel("確率密度", fontsize=12, color=INK)
    ax.set_title("① 有意度の分布は N(0,1) に一致するか", fontsize=12.5, color=INK)
    ax.legend(fontsize=9.5, frameon=False)

    # ── (2) 天体ごとの最大 σ vs look-elsewhere の期待分布 ────────────────────
    ax = axes[1]
    ctrl = [v for v in data.values() if v["category"] == "control"]
    n_bins_typ = int(np.median([v["n_bins"] for v in data.values()])) if data else 13
    maxima = {c: np.array([v["sigma"].max() for v in data.values() if v["category"] == c])
              for c in cats}
    # 13 回の独立な N(0,1) から得られる最大値の分布 (解析解)
    xx = np.linspace(-1.0, 5.0, 400)
    pdf_max = n_bins_typ * stats.norm.pdf(xx) * stats.norm.cdf(xx) ** (n_bins_typ - 1)
    ax.plot(xx, pdf_max, "--", color=INK, lw=2.0,
            label=f"独立な {n_bins_typ} ビンの最大値の期待分布")
    for c, m in maxima.items():
        if m.size < 5:
            # 天体数が少なすぎる区分は分布として意味を成さない (棒 1 本で密度 1.0 になる)。
            # 代わりに個々の値を縦線で示す
            for v in m:
                ax.axvline(v, color=CAT_COLOR[c], lw=1.6, ls=":", alpha=0.9)
            ax.plot([], [], ls=":", color=CAT_COLOR[c], lw=1.6,
                    label=f"{CAT_LABEL[c]} (n={m.size} 天体、個別に表示)")
            continue
        ax.hist(m, bins=np.arange(-1.0, 5.01, 0.5), density=True, histtype="step",
                lw=2.2, color=CAT_COLOR[c], label=f"{CAT_LABEL[c]} (n={m.size} 天体)")
    ax.set_xlabel("その天体で得られた最大の σ", fontsize=12, color=INK)
    ax.set_ylabel("確率密度", fontsize=12, color=INK)
    ax.set_title("② 「どこかで大きな σ」は偶然でどこまで出るか", fontsize=12.5, color=INK)
    ax.legend(fontsize=9.5, frameon=False)
    stats_out["max_sigma"] = {c: {"mean": float(m.mean()), "max": float(m.max())}
                              for c, m in maxima.items()}
    stats_out["expected_max_of_n_bins"] = {
        "n_bins": n_bins_typ,
        "mean": float(np.trapezoid(xx * pdf_max, xx)),
    }

    # ── (3) 全天のどこを見たか (銀河座標) ──────────────────────────────────
    ax = axes[2]
    for c in cats:
        vs = [v for v in data.values() if v["category"] == c]
        l = np.array([v["l"] for v in vs])
        b = np.array([v["b"] for v in vs])
        sz = 18 + 26 * np.clip([v["sigma"].max() for v in vs], 0, 4)
        ax.scatter(l, b, s=sz, facecolor="none", edgecolor=CAT_COLOR[c], lw=1.8,
                   label=CAT_LABEL[c])
    ax.axhspan(-20, 20, color="#eeeeec", zorder=0)
    ax.text(-175, 0, "|b| < 20° (対照フィールドを置かない帯)", fontsize=8.5, color=MUTED,
            va="center")
    ax.set_xlim(180, -180)
    ax.set_ylim(-90, 90)
    ax.set_xlabel("銀経 l [deg]", fontsize=12, color=INK)
    ax.set_ylabel("銀緯 b [deg]", fontsize=12, color=INK)
    ax.set_title("③ 解析した位置 (印の大きさ = 最大 σ)", fontsize=12.5, color=INK)
    ax.legend(fontsize=9.5, frameon=False, loc="lower right")

    for ax in axes:
        ax.tick_params(labelsize=10, colors=MUTED)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(MUTED)

    n_t = sum(len([v for v in data.values() if v["category"] == c]) for c in cats)
    n_s = sum(s.size for s in cats.values())
    ctrl_s = cats.get("control")
    line2 = ""
    if ctrl_s is not None:
        line2 = (f"対照フィールドの実測: 平均 {ctrl_s.mean():+.3f} / 標準偏差 "
                 f"{ctrl_s.std(ddof=1):.3f} (期待は 0 と 1)。"
                 f"|σ|>2 が {100*np.mean(np.abs(ctrl_s)>2):.1f}% (期待 4.6%)、"
                 f"|σ|>3 が {100*np.mean(np.abs(ctrl_s)>3):.1f}% (期待 0.27%)。")
    fig.suptitle(f"同じ手法を {n_t} 箇所に当てた統計検証 ({n_s} 個の有意度)",
                 fontsize=15, color=INK, y=0.985)
    fig.text(0.5, 0.012,
             line2 + f"  各ビンは ROI 内の事象数 {MIN_EVENTS} 以上のもののみ。",
             ha="center", fontsize=9.5, color=MUTED)

    fig.tight_layout(rect=(0.0, 0.045, 1.0, 0.94))
    fig.savefig(OUT, dpi=150)
    OUT_JSON.write_text(json.dumps(stats_out, indent=2))
    print(f"→ {OUT}\n→ {OUT_JSON}")
    for c, v in stats_out["by_category"].items():
        print(f"  {CAT_LABEL[c]:22s} 天体 {v['n_targets']:3d} / σ値 {v['n_sigma_values']:4d}  "
              f"平均 {v['mean']:+.3f}  標準偏差 {v['std']:.3f}  "
              f"|σ|>2 {100*v['frac_gt2']:5.1f}%  |σ|>3 {100*v['frac_gt3']:4.1f}%  "
              f"最大 {v['max']:+.2f}")


if __name__ == "__main__":
    main()
