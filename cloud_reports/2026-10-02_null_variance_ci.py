"""[クラウド・2026-10-02] 「何も無い空での σ のばらつき」(帰無分布の標準偏差 s) に信頼区間を付け、
19.0σ を較正し直す。

着想: Kimura (2019, JJSDS; arXiv:1710.06683) は、推定量の信頼区間を作るために
「漸近分散の推定量」を 2 種類作り、シミュレーションで比べた。ここでも s の不確かさを 2 通りで見積もる:
  (A) 素朴: 299 個の有意度を全部独立とみなす  SE(s) ≈ s / sqrt(2n)
  (B) 場所ごとのブートストラップ: 同じ対照フィールドの 13 ビンは同じ空・同じ背景モデルを
      共有するので互いに相関しうる。フィールド (23 個) を単位に復元抽出する
そして、場所の中で相関がある仮想データで「95% 区間が本当に 95% で当たるか」(カバレッジ) を比べる。

較正の仮定 (assumption): 名目の有意度 z は、背景モデルの誤りで分散が s² 倍に膨らむ
(quasi-likelihood の過分散)。すると較正後の有意度は z / s。

入力: results/mcmc_allbins_gasICS_v20_constructsplit/other_celestial_body/control_*_spectrum.json
出力: 画面と cloud_reports/2026-10-02_null_variance_ci_result.json
"""
import glob
import json
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent.parent
D = BASE / "results/mcmc_allbins_gasICS_v20_constructsplit/other_celestial_body"
fs = sorted(glob.glob(str(D / "control_*_spectrum.json")))
J = [json.load(open(f)) for f in fs]
E = np.array(J[0]["e_center_gev"])
S = np.array([j["significance_sigma"] for j in J], dtype=float)  # (23 フィールド, 13 ビン)
NEV = np.array([j["n_events_bin"] for j in J], dtype=float)
Z_MAIN = 19.00  # v20r Bin6 (本人 PC)
B = 20000
rng = np.random.default_rng(20261002)


def sd(x):
    return float(np.sqrt(np.mean(x ** 2)))  # 帰無の平均は 0 と仮定 (実測平均 -0.07)


def ci_naive(x):
    s = sd(x)
    se = s / np.sqrt(2 * x.size)
    return s, s - 1.96 * se, s + 1.96 * se


def ci_cluster(X):
    # X: (フィールド, ビン)。フィールドを単位に復元抽出 (percentile 法)
    nf = X.shape[0]
    idx = rng.integers(0, nf, size=(B, nf))
    bs = np.sqrt(np.mean(X[idx] ** 2, axis=(1, 2)))
    return sd(X), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def ci_cluster_quick(X, rng_, nb=400):
    nf = X.shape[0]
    idx = rng_.integers(0, nf, size=(nb, nf))
    bs = np.sqrt(np.mean(X[idx] ** 2, axis=(1, 2)))
    return np.percentile(bs, 2.5), np.percentile(bs, 97.5)


out = dict(input=str(D.relative_to(BASE)), n_fields=len(fs), energies_gev=E.tolist())

# 1. エネルギーごとの s (光子が少ないビンは漸近理論の前提が崩れる)
print("ビン  E[GeV]  平均光子数  s(23 フィールド)")
per_bin = []
for k in range(13):
    x = S[:, k]
    per_bin.append(dict(e_gev=float(E[k]), mean_events=float(NEV[:, k].mean()), s=sd(x)))
    print(f"{k+1:>3} {E[k]:>7.1f} {NEV[:, k].mean():>10.0f}  {sd(x):.3f}")
out["per_bin"] = per_bin

# 2. 解析に使う範囲: 光子が十分あるビン 2–10 (2.6–169 GeV、1 フィールドあたり平均 94 個以上)。
#    ビン 1 は s=2.25 で外れ (低エネルギーで PSF が広く、背景モデルの誤りが大きい)、ビン 11–13 は光子が数個〜数十個
sel = slice(1, 10)
X = S[:, sel]
x = X.ravel()
# 同じフィールドの中で、ビン同士がどれだけ相関しているか (潜在的な共通成分 = その場所の背景モデルの誤り)
C = np.corrcoef(X.T)
off = C[~np.eye(C.shape[0], dtype=bool)]
adj = np.array([C[i, i + 1] for i in range(C.shape[0] - 1)])
# 級内相関 (ICC): 分散のうち「フィールド共通」の割合 (一元配置の分散成分推定)
nf, nb = X.shape
msb = nb * np.var(X.mean(1), ddof=1)
msw = np.sum((X - X.mean(1, keepdims=True)) ** 2) / (nf * (nb - 1))
icc = float((msb - msw) / (msb + (nb - 1) * msw))
print(f"\nビン 2–10: n={x.size}, 平均 {x.mean():+.3f}, s={sd(x):.3f}, 最大 {x.max():.2f}")
print(f"同じ場所のビン同士の相関: 隣どうし平均 {adj.mean():+.2f}, 全ペア平均 {off.mean():+.2f}, 級内相関 ICC={icc:+.2f}")

sA = ci_naive(x)
sB = ci_cluster(X)
s6 = ci_cluster(S[:, 5:6])
print(f"(A) 素朴       s={sA[0]:.3f}  95%区間 {sA[1]:.3f}–{sA[2]:.3f}")
print(f"(B) 場所ごと   s={sB[0]:.3f}  95%区間 {sB[1]:.3f}–{sB[2]:.3f}")
print(f"Bin6 だけ (23 個、場所ごと) s={s6[0]:.3f}  95%区間 {s6[1]:.3f}–{s6[2]:.3f}")

# 3. 仮想データでカバレッジを比べる (Kimura 2019 の §シミュレーションと同じ発想)
#    真の s = 1.3、場所共通の成分の割合 rho (0, 実測 ICC, 0.3, 0.5) で 23×9 の正規乱数を作る
cov = {}
for rho in sorted({0.0, max(icc, 0.0), 0.3, 0.5}):
    hitA = hitB = 0
    ntrial = 2000
    s_true = 1.3
    for t in range(ntrial):
        g = rng.normal(size=(nf, 1)) * np.sqrt(rho)
        e = rng.normal(size=(nf, nb)) * np.sqrt(1 - rho)
        Y = s_true * (g + e)
        _, lo, hi = ci_naive(Y.ravel())
        hitA += lo <= s_true <= hi
        lo, hi = ci_cluster_quick(Y, rng)
        hitB += lo <= s_true <= hi
    cov[f"{rho:.2f}"] = dict(naive=hitA / ntrial, cluster=hitB / ntrial)
    print(f"共通成分 {rho:.2f}: 95% 区間が当たる割合  素朴 {hitA/ntrial:.3f} / 場所ごと {hitB/ntrial:.3f}")

# 4. 19.0σ の較正
def cal(s):
    return Z_MAIN / s
res = dict(
    bins_2_10=dict(n=int(x.size), mean=float(x.mean()), s=sA[0], max=float(x.max()),
                   corr_adjacent=float(adj.mean()), corr_allpairs=float(off.mean()), icc=icc,
                   ci_naive=[sA[1], sA[2]], ci_cluster=[sB[1], sB[2]]),
    bin6_only=dict(s=s6[0], ci_cluster=[s6[1], s6[2]]),
    all_299=dict(n=int(np.isfinite(S).sum()), s=sd(S.ravel()), max=float(np.nanmax(S))),
    coverage_sim=cov,
    calibrated_bin6=dict(
        nominal=Z_MAIN,
        using_bins_2_10=[cal(sB[0]), cal(sB[2]), cal(sB[1])],
        using_bin6_only=[cal(s6[0]), cal(s6[2]), cal(s6[1])],
        using_record_1362=cal(1.362)),
)
print(f"\n19.0σ の較正: ビン2–10 の s → {cal(sB[0]):.1f}σ (95%: {cal(sB[2]):.1f}–{cal(sB[1]):.1f}σ)")
print(f"               Bin6 だけの s → {cal(s6[0]):.1f}σ (95%: {cal(s6[2]):.1f}–{cal(s6[1]):.1f}σ)")
print(f"               記録の 1.362 → {cal(1.362):.1f}σ")
out.update(res)
dst = BASE / "cloud_reports/2026-10-02_null_variance_ci_result.json"
json.dump(out, open(dst, "w"), ensure_ascii=False, indent=2)
print("saved", dst.relative_to(BASE))
