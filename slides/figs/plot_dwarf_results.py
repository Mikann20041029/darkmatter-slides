# 矮小銀河・M31/M33 と、何も無い空 (対照) の有意度の分布を比べる図
# 実行: python slides/figs/plot_dwarf_results.py  (リポジトリの一番上で)
import glob
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = ["Noto Sans CJK JP", "DejaVu Sans"]

D = "cloud_reports/2026-10-02_v20r_targets/targets"  # 10/2 に今のコードで計算し直した結果
tgt, ctl = [], []
for f in sorted(glob.glob(D + "/*_spectrum.json")):
    j = json.load(open(f))
    m = j["meta"]
    if not m.get("usable", True):  # SMC・LMC は中心がマスクされ使えない
        continue
    s = np.array(j["significance_sigma"], dtype=float)
    s = s[np.isfinite(s)]
    (ctl if m["category"] == "control" else tgt).append(s)
n_tgt, n_ctl = len(tgt), len(ctl)
tgt, ctl = np.concatenate(tgt), np.concatenate(ctl)

bins = np.arange(-5, 5.5, 0.5)
x = np.linspace(-5, 5, 400)
fig, ax = plt.subplots(figsize=(8, 4.6), dpi=150)
ax.hist(ctl, bins=bins, density=True, histtype="step", color="0.5", lw=2,
        label=f"何も無い空 {n_ctl} か所（最大 {ctl.max():.2f}σ）")
ax.hist(tgt, bins=bins, density=True, histtype="step", color="k", lw=2,
        label=f"矮小銀河・M31・M33 {n_tgt} 天体（最大 {tgt.max():.2f}σ）")
ax.plot(x, np.exp(-x ** 2 / 2) / np.sqrt(2 * np.pi), "k:", lw=1.5, label="理論（平均 0、ばらつき 1）")
ax.set_xlabel("ハローの有意度 σ（全 13 エネルギービン）", fontsize=13)
ax.set_ylabel("割合", fontsize=13)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.legend(frameon=False, fontsize=11)
fig.tight_layout()
fig.savefig("slides/figs/fig_dwarf_results.png")
print(f"天体 {n_tgt} ({tgt.size} 個), 最大 {tgt.max():.2f}; 対照 {n_ctl} ({ctl.size} 個), 最大 {ctl.max():.2f}")
