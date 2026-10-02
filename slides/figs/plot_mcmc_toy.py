# MCMC (メトロポリス法) の説明用のおもちゃの例。実データではない。
# 1 つのパラメータ (ハローの倍率 f) の事後分布が、平均 1.48・幅 0.075 の山だと仮定し、
# 「少しずらす → 比 r で移るか決める」を 3000 回くり返して、歩いた跡と、そのヒストグラムを描く。
# 実行: python slides/figs/plot_mcmc_toy.py  (リポジトリの一番上で)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = ["Noto Sans CJK JP", "DejaVu Sans"]
rng = np.random.default_rng(1)

MU, SD = 1.48, 0.075           # 仮の事後分布 (山の中心と幅)


def log_post(f):
    # 事後分布の対数 (定数は不要。比しか使わないため)
    return -0.5 * ((f - MU) / SD) ** 2


n, step = 3000, 0.05
f = np.empty(n)
f[0] = 1.2                      # わざと山から離れた所から出発
acc = 0
for t in range(1, n):
    cand = f[t - 1] + step * rng.normal()                 # 1. 少しずらした候補
    r = np.exp(log_post(cand) - log_post(f[t - 1]))       # 2. 比 r
    if rng.random() < r:                                  # 3. r >= 1 なら必ず、r < 1 なら確率 r で移る
        f[t] = cand
        acc += 1
    else:
        f[t] = f[t - 1]                                   #    移らなければ同じ場所にもう一度記録

burn = 200
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.6), dpi=150, gridspec_kw=dict(width_ratios=[2, 1]))
a1.plot(f, color="k", lw=0.6)
a1.axvspan(0, burn, color="0.85")
a1.text(burn / 2, 1.22, "捨てる", ha="center", fontsize=11)
a1.set_xlabel("歩数", fontsize=12)
a1.set_ylabel("倍率 f", fontsize=12)
a1.set_title("歩いた跡", fontsize=12)
a2.hist(f[burn:], bins=40, orientation="horizontal", color="0.6", density=True)
y = np.linspace(1.15, 1.8, 300)
a2.plot(np.exp(log_post(y)) / (SD * np.sqrt(2 * np.pi)), y, "k--", lw=1.2)
a2.set_title("跡のヒストグラム\n（点線 = 本当の事後分布）", fontsize=11)
a2.set_xticks([])
for a in (a1, a2):
    a.set_ylim(1.15, 1.8)
    for s in ("top", "right"):
        a.spines[s].set_visible(False)
fig.suptitle("説明用の例（実データではない）", fontsize=10, color="0.4", x=0.98, ha="right")
fig.tight_layout()
fig.savefig("slides/figs/fig_mcmc_toy.png")
print(f"受理率 {acc / (n - 1):.2f}, 平均 {f[burn:].mean():.3f}, 幅 {f[burn:].std():.3f}")
