# 何も無い空 (対照フィールド 23 か所) での「σ のばらつき」をエネルギーごとに描く
# 実行: python slides/figs/plot_null_variance.py  (リポジトリの一番上で)
import glob
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = ["Noto Sans CJK JP", "DejaVu Sans"]

# 対照フィールドの有意度を読む: S[フィールド, エネルギービン]
D = "cloud_reports/2026-10-02_v20r_targets/targets"  # 10/2 に今のコードで計算し直した結果
J = [json.load(open(f)) for f in sorted(glob.glob(D + "/control_*_spectrum.json"))]
E = np.array(J[0]["e_center_gev"])
S = np.array([j["significance_sigma"] for j in J], dtype=float)

rng = np.random.default_rng(20261002)


def rms(x):
    # ばらつき = 0 からのずれの2乗平均の平方根 (何も無ければ平均は 0 のはず)
    return np.sqrt(np.mean(x ** 2))


def boot_ci(X, nb=20000):
    # フィールドを単位に復元抽出して 95% 区間 (同じ場所のビン同士は相関するため)
    idx = rng.integers(0, X.shape[0], size=(nb, X.shape[0]))
    b = np.sqrt(np.mean(X[idx] ** 2, axis=tuple(range(1, X.ndim + 1))))
    return np.percentile(b, [2.5, 97.5])


s = np.array([rms(S[:, k]) for k in range(13)])
ci = np.array([boot_ci(S[:, k]) for k in range(13)])
use = np.zeros(13, bool)
use[1:10] = True  # 光子が十分あるビン 2–10 だけで全体の値を出す
s_all = rms(S[:, use])
lo, hi = boot_ci(S[:, use])

fig, ax = plt.subplots(figsize=(8, 4.6), dpi=150)
ax.axhspan(lo, hi, color="0.85", lw=0)  # 全体の値の 95% 区間 (灰色の帯)
ax.axhline(s_all, color="0.4", lw=1)
ax.axhline(1.0, color="k", ls="--", lw=1)  # 理論どおりなら 1
for k in range(13):
    c = "k" if use[k] else "0.6"
    ax.errorbar(E[k], s[k], yerr=[[s[k] - ci[k, 0]], [ci[k, 1] - s[k]]], fmt="o", color=c, ms=6, capsize=3)
ax.axvline(E[5], color="k", lw=0.6, ls=":")
ax.text(E[5] * 1.08, 2.55, "20 GeV", fontsize=11)
ax.text(1.2, 1.0 - 0.17, "理論どおりなら 1", fontsize=11)
ax.text(230, 1.55, f"全体 {s_all:.2f}\n(95%: {lo:.2f}–{hi:.2f})", fontsize=11, color="0.3")
ax.set_xscale("log")
ax.set_ylim(0, 3.0)
ax.set_xlabel("エネルギー [GeV]", fontsize=13)
ax.set_ylabel("何も無い空での σ のばらつき", fontsize=13)
ax.set_title("灰色の点: 光子が少ない / 低エネルギーの外れ (全体の値に使わない)", fontsize=10, color="0.4")
fig.tight_layout()
fig.savefig("slides/figs/fig_null_variance.png")
print(f"ビン2–10: {s_all:.3f} (95%: {lo:.3f}–{hi:.3f}), 20 GeV: {s[5]:.3f} ({ci[5,0]:.3f}–{ci[5,1]:.3f})")
