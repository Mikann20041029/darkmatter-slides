"""[クラウド・2026-10-02] MCMC の設定 (歩く人数・歩数・捨てる歩数・乱数の種) を変えても、
20.8 GeV の結果 (最良値・有意度・誤差) が変わらないかを確かめる。Totani 方式 (最良値 = 踏んだ点で尤度最大)。
型紙は 1 回だけ作り、歩かせ方だけを変える。
使い方 (データ復元済みのチェックアウトで): python <この.py> <出力 json>
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import emcee

sys.path.insert(0, str(Path.cwd() / "code"))
import plot_bin6_totani_fig11_v20 as f11  # noqa: E402
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
signfree = list(mfb.SIGNFREE_IDX)


def chain(with_halo, n_walkers, n_steps, seed):
    rng = np.random.default_rng(seed)
    dim = len(names) if with_halo else ih
    start = x0[:dim]
    pos = start + 1e-3 * np.maximum(np.abs(start), 1e-3) * np.abs(rng.normal(size=(n_walkers, dim)))
    sf = [i for i in signfree if i < dim]
    pos[:, sf] = start[sf] + 1e-3 * rng.normal(size=(n_walkers, len(sf)))
    lp = (lambda q: mfb.log_probability(list(q), cc, ct)) if with_halo else \
         (lambda q: mfb.log_probability(list(q) + [0.0], cc, ct))
    np.random.seed(seed)
    s = emcee.EnsembleSampler(n_walkers, dim, lp)
    s.run_mcmc(pos, n_steps, progress=False)
    return s


out = []
configs = [(32, 6000, 42), (20, 6000, 42), (64, 6000, 42), (32, 6000, 1), (32, 6000, 2), (32, 20000, 42)]
for nw, ns, seed in configs:
    t0 = time.time()
    s1 = chain(True, nw, ns, seed)
    s0 = chain(False, nw, ns, seed)
    lp1, lp0 = s1.get_log_prob(), s0.get_log_prob()
    k = np.unravel_index(int(np.argmax(lp1)), lp1.shape)
    best = s1.get_chain()[k]
    sig = float(np.sqrt(2 * max(lp1.max() - lp0.max(), 0)))
    try:
        tau = float(np.max(s1.get_autocorr_time(quiet=True)))
    except Exception:
        tau = float("nan")
    for burn in sorted({400, 2000, 5000} & set(range(0, ns - 500))):
        flat = s1.get_chain(discard=burn, thin=5, flat=True)[:, ih]
        lo, med, hi = np.percentile(flat, [16, 50, 84])
        row = dict(n_walkers=nw, n_steps=ns, seed=seed, burn=burn, significance=sig,
                   f_halo_best=float(best[ih]), f_halo_median=float(med), f_halo_lo16=float(lo), f_halo_hi84=float(hi),
                   tau_max=tau, acceptance=float(np.mean(s1.acceptance_fraction)), sec=round(time.time() - t0))
        out.append(row)
        print(json.dumps(row, ensure_ascii=False), flush=True)
json.dump(out, open(sys.argv[1], "w"), indent=2, ensure_ascii=False)
print("saved", sys.argv[1])
