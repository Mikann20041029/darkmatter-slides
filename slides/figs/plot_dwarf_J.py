# 矮小銀河: 「暗黒物質なら何σ見えたはずか」の予測の幅 (J の誤差あり) と、実測を比べる図
# 実行: python slides/figs/plot_dwarf_J.py  (リポジトリの一番上で)
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = ["Noto Sans CJK JP", "DejaVu Sans"]

# 各天体の「予測」と「実測」を読む (20 GeV のビン)
d = json.load(open("cloud_reports/2026-10-02_v20r_targets/dwarf_consistency.json"))  # 天の川は v20r
ib = d["bin_index_20gev"]
D = Path("cloud_reports/2026-10-02_v20r_targets/targets")
pred, meas = [], []
for t in d["targets"]:
    usable = json.load(open(D / f"{t['key']}_spectrum.json"))["meta"].get("usable", True)
    p, m = t["predicted_detection_sigma"][ib], t["measured_sigma"][ib]
    if usable and np.isfinite(p) and np.isfinite(m):  # 使えない天体 (SMC・LMC) は除く
        pred.append(p)
        meas.append(m)
pred, meas = np.array(pred), np.array(meas)

# 天体をまとめる: 予測の大きい天体ほど重く数える重み付き和
w = pred
norm = np.sqrt(np.sum(w ** 2))
T_obs = np.sum(w * meas) / norm      # 実測をまとめた値
T_noJ = np.sum(w * pred) / norm      # J の誤差なしの予測

# J の誤差: 各天体の J を 10^δ 倍にずらす (δ は平均 0、幅 0.5 の正規分布 = 約 3 倍)。これを 20 万回
rng = np.random.default_rng(0)
delta = rng.normal(0.0, 0.5, size=(200_000, w.size))
T_J = np.sum(w * pred * 10 ** delta, axis=1) / norm

S_NULL = 1.26  # 実測の揺れ: 何も無い空で測った σ のばらつき

fig, ax = plt.subplots(figsize=(8, 4.8), dpi=150)
ax.hist(T_J, bins=np.linspace(-1, 10, 111), density=True, color="0.75", label="予測（J の誤差 約3倍あり）")
ax.axvline(T_noJ, color="k", ls="--", lw=2, label=f"予測（J の誤差なし、{T_noJ:.1f}σ）")
ytop = ax.get_ylim()[1]
y = ytop * 0.55
ax.errorbar(T_obs, y, xerr=S_NULL, fmt="o", color="k", ms=8, capsize=6, lw=2,
            label=f"実測 {T_obs:.1f}σ（横棒 = 測定の揺れ ±{S_NULL}）")
ax.set_xlim(-1.5, 10)
ax.set_yticks([])
ax.set_xlabel("暗黒物質なら見えたはずの信号 [σ]", fontsize=13)
ax.set_ylabel("確率", fontsize=13)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.legend(frameon=False, fontsize=11)
fig.tight_layout()
fig.savefig("slides/figs/fig_dwarf_J_uncertainty.png")
print(f"天体 {w.size}、実測 {T_obs:.2f}、予測 {T_noJ:.2f}、J あり中央値 {np.median(T_J):.2f}"
      f" (68%: {np.percentile(T_J,16):.2f}–{np.percentile(T_J,84):.2f})")
