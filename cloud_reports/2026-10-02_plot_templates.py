"""[クラウド・2026-10-02] 当てはめに使う 9 枚の型紙 (テンプレート) を、20.8 GeV で 1 枚ずつ地図にする。
型紙の「形」を見せるための図で、倍率 (係数) は掛けていない (それぞれ自分の明るさの範囲で色を付ける)。
使い方 (データ復元済みのチェックアウトで): python <この.py> <出力フォルダ>
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path.cwd() / "code"))
import plot_bin6_totani_fig11_v20 as f11  # noqa: E402  (v20 と同じ設定で型紙を作る)
import plot_skymap_all_subtracted as _sub  # noqa: E402

plt.rcParams["font.family"] = ["Noto Sans CJK JP", "DejaVu Sans"]
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

d = f11.build()
T = d["tmpl"]
edges = _sub.L_BINS
names = {"iso_counts": "等方背景", "gas": "ガス (π⁰ 崩壊＋制動放射)", "ics": "ICS (逆コンプトン散乱)",
         "ps": "点源 (4FGL カタログ)", "loopI_a": "Loop I (殻 1)", "loopI_b": "Loop I (殻 2)",
         "fb": "フェルミバブル (正)", "fb_neg": "フェルミバブル (負)", "halo": "ハロー (NFW, 密度の 2 乗)"}
for k, title in names.items():
    m = f11._smooth_flux(T[k], d["unit"], d["valid"], d["grey"])
    fig, ax = plt.subplots(figsize=(5.2, 5.4), dpi=150)
    v = np.nanpercentile(np.abs(m), 99.5)
    # バブル (負) の型紙は「負の残差の大きさ」(正の値) で、当てはめでは符号自由の倍率を掛ける
    im = ax.pcolormesh(edges, edges, m.T, cmap="inferno", vmin=0, vmax=v, shading="flat", rasterized=True)
    ax.set_xlim(60, -60)
    ax.set_ylim(-60, 60)
    ax.set_aspect("equal")
    ax.set_xlabel("銀経 l [deg]", fontsize=11)
    ax.set_ylabel("銀緯 b [deg]", fontsize=11)
    ax.set_title(f"{title}　20.8 GeV の型紙", fontsize=11)
    cb = fig.colorbar(im, ax=ax, orientation="horizontal", fraction=0.05, pad=0.12)
    cb.set_label("明るさ (相対値)", fontsize=9)
    cb.set_ticks([])
    fig.tight_layout()
    fig.savefig(OUT / f"template_{k}.png")
    plt.close(fig)
    print("saved", k)
