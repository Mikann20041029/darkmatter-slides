"""[クラウド・2026-10-02] Totani と同じやり方 (MCMC で最尤値を求める) で Bin6 の有意度を出し、
本研究のやり方 (勾配法 L-BFGS-B で最尤値、MCMC は誤差だけ) と比べる。

Totani (2025) §2.2: "the best-fit values and statistical errors of the fitting parameters f_l are obtained
by maximizing the likelihood function using the Markov chain Monte Carlo (MCMC) method"
§2.3: MCMC の初期値は 点源・GALPROP = 1、等方 = E²dN/dE 1e-4、他 = 0。

やること (同じ型紙・同じ 10° セル尤度・同じ制約で):
  A. 本研究: L-BFGS-B で ln L の最大値 (ハローあり / なし) → σ = sqrt(2 Δln L)
  B. Totani 流: Totani の初期値から emcee を走らせ、チェーン中の ln L の最大値 (ハローあり / なし) → σ
環境: クラウド (x86_64)。本人 PC の 19.00σ とは環境の差 (19.46σ) があるので、A と B を同じ環境で比べる。
使い方 (データ復元済みのチェックアウトで): python <この.py>
"""
import sys
from pathlib import Path

import numpy as np
import emcee
from scipy.optimize import minimize

sys.path.insert(0, str(Path.cwd() / "code"))
import plot_bin6_totani_fig11_v20 as f11  # noqa: E402  (MCMC_* の設定を v20 と同じにしてから読み込む)
import mcmc_fit_all_bins as mfb  # noqa: E402

d = f11.build()
tm = dict(d["tmpl"])
tm["valid"] = d["valid"]
cc, ct = mfb.cellize_counts_and_templates(d["counts"], tm, d["valid"])
names = list(mfb.PARAM_NAMES)
ih = names.index("f_halo")
E = float(mfb.BIN_CENTERS[5])
f_iso0 = 1e-4 * float(d["unit"].mean()) / (E ** 2 * 1e6)
x0 = np.array([f_iso0 if n == "f_iso" else (1.0 if n in ("f_gas", "f_ics", "f_ps") else 0.0) for n in names])


def lnL_full(p):
    return -mfb.neg_log_likelihood_and_grad(list(p), cc, ct)[0]


# ---- A. 勾配法 (本研究) ----
def mle(nohalo):
    b = mfb._bounds_with_halo()
    if nohalo:
        f = lambda q: tuple(v if i == 0 else v[:ih] for i, v in enumerate(mfb.neg_log_likelihood_and_grad(list(q) + [0.0], cc, ct)))
        starts = [x0[:ih], np.asarray(d["p_full"])[:ih]]
        bb = b[:ih]
    else:
        f = lambda q: mfb.neg_log_likelihood_and_grad(list(q), cc, ct)
        starts = [x0, np.asarray(d["p_full"])]
        bb = b
    best = None
    for s0 in starts:
        r = minimize(f, s0, jac=True, method="L-BFGS-B", bounds=bb)
        if best is None or r.fun < best.fun:
            best = r
    return -best.fun, best.x


lA1, pA1 = mle(False)
lA0, _ = mle(True)
sA = np.sqrt(2 * max(lA1 - lA0, 0))


# ---- B. Totani 流 (MCMC のチェーン中の最大 ln L) ----
def run_chain(nohalo, n_walkers=32, n_steps=6000, seed=42):
    rng = np.random.default_rng(seed)
    dim = ih if nohalo else len(names)
    start = x0[:dim]
    pos = start + 1e-3 * np.maximum(np.abs(start), 1e-3) * np.abs(rng.normal(size=(n_walkers, dim)))
    if nohalo:
        lp = lambda q: mfb.log_probability(list(q) + [0.0], cc, ct)
    else:
        lp = lambda q: mfb.log_probability(list(q), cc, ct)
    np.random.seed(seed)
    s = emcee.EnsembleSampler(n_walkers, dim, lp)
    s.run_mcmc(pos, n_steps, progress=False)
    lpc = s.get_log_prob()
    i = np.unravel_index(np.argmax(lpc), lpc.shape)
    return float(lpc[i]), s.get_chain()[i], s


lB1, pB1, s1 = run_chain(False)
lB0, _, _ = run_chain(True)
sB = np.sqrt(2 * max(lB1 - lB0, 0))
med = np.median(s1.get_chain(discard=400, thin=5, flat=True), axis=0)

print("== Bin6 (20.8 GeV)、クラウド環境 (x86_64) ==")
print(f"A 本研究 (勾配法):        ln L あり {lA1:.4f} / なし {lA0:.4f}  →  {sA:.3f}σ")
print(f"B Totani 流 (MCMC 最大): ln L あり {lB1:.4f} / なし {lB0:.4f}  →  {sB:.3f}σ")
print(f"  ln L の差 (A − B): あり {lA1 - lB1:+.4f} / なし {lA0 - lB0:+.4f}")
print("倍率の比較 (A 勾配法の頂上 / B チェーン中の最大点 / B チェーンの中央値):")
for k, n in enumerate(names):
    print(f"  {n:10s} {pA1[k]:9.4f} {pB1[k]:9.4f} {med[k]:9.4f}")
