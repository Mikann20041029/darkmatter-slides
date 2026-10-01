"""[クラウド・2026-10-02] 矮小銀河の J ファクターに誤差 (Δlog10 J = 0.5, Bertólez-Martínez+ 2026) を入れると、
「天の川の超過が暗黒物質なら矮小銀河で見えたはず」という検定はどう変わるか。

入力: results/dwarf_consistency/dwarf_consistency.json (code/dwarf_consistency_check.py の出力、45 天体、20 GeV)
  各天体 i について pred_i = 「DM なら何σで見えたはずか」(J は Pace & Strigari 2019 の推定値そのまま)
                    meas_i = 実測の有意度

検定統計量 (最適な重み付き和):
  T = Σ_i w_i · meas_i / sqrt(Σ_i w_i^2),   w_i = pred_i (J の推定値で決まる重み)
  - DM が無ければ T ~ N(0, s^2)            (s = 1、または空の領域で測った 1.362)
  - DM があり、本当の J が J_i·10^{δ_i} なら、本当の期待値は pred_i·10^{δ_i}·k
      (k = 天の川側の密度の仮定による係数。予測は局所密度 ρ☉ の -2 乗に比例: k = (0.42/ρ☉)^2)
    T の期待値 = Σ w_i·pred_i·10^{δ_i}·k / sqrt(Σ w_i^2)
  - 「DM ありで、実測の T 以下になる確率」p = Φ((T_obs − E[T]) / s) を、δ_i ~ N(0, σ_J^2) で平均する
    (σ_J = 0 なら J の誤差なし。0.5 なら論文の推奨)

出力: 画面の表と cloud_reports/2026-10-02_dwarf_J_uncertainty_result.json
"""
import json
from math import erf, sqrt
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent.parent
d = json.load(open(BASE / "results/dwarf_consistency/dwarf_consistency.json"))
ib = d["bin_index_20gev"]
keys = [t["key"] for t in d["targets"]]
pred = np.array([t["predicted_detection_sigma"][ib] for t in d["targets"]], dtype=float)
meas = np.array([t["measured_sigma"][ib] for t in d["targets"]], dtype=float)
ok = np.isfinite(pred) & np.isfinite(meas)
print(f"使える天体 {ok.sum()} / {len(keys)}")


def phi(x):
    return 0.5 * (1 + erf(x / sqrt(2)))


def z_of_p(p):
    # 片側 p 値を「何σの緊張か」に直す (p が小さいほど大きい)
    from scipy.stats import norm
    return float(norm.isf(p))


def analyse(mask, rho_local, sigma_J, s_null, n_mc=200_000, seed=0):
    w = pred[mask]
    m = meas[mask]
    norm_w = np.sqrt(np.sum(w ** 2))
    T_obs = float(np.sum(w * m) / norm_w)
    k = (0.42 / rho_local) ** 2
    if sigma_J == 0:
        ET = np.array([np.sum(w * w) * k / norm_w])
    else:
        rng = np.random.default_rng(seed)
        delta = rng.normal(0.0, sigma_J, size=(n_mc, w.size))
        ET = (np.sum(w * w * 10 ** delta, axis=1) * k) / norm_w
    p = float(np.mean([phi((T_obs - e) / s_null) for e in ET[:20000]])) if ET.size > 1 else phi((T_obs - ET[0]) / s_null)
    return dict(T_obs=T_obs, ET_median=float(np.median(ET)), ET_16=float(np.percentile(ET, 16)),
                ET_84=float(np.percentile(ET, 84)), p_value=p, tension_sigma=z_of_p(p))


# 他天体の解析で「使用不可」(標的の中心が拡張源マスクで消え、ハローの形が数%しか残らない) と判定された天体を除く。
# dwarf_consistency_check.py はこの判定を見ておらず、SMC・LMC が混ざっていた
D = BASE / "results/mcmc_allbins_gasICS_v20_constructsplit/other_celestial_body"
usable = np.array([json.load(open(D / f"{k}_spectrum.json"))["meta"].get("usable", True) for k in keys])
print("使用不可で除く天体:", [k for k, u in zip(keys, usable) if not u])
cases = []
print(f"\n{'天体':<10}{'ρ☉':>5}{'J誤差':>6}{'σ較正':>6} | {'実測T':>6} {'DMの期待値 (16–84%)':>22} | {'p値':>8} {'緊張':>6}")
for label, mask in (("使える43", ok & usable), ("45(誤り)", ok)):
    for rho in (0.3, 0.42, 0.6):
        for sJ in (0.0, 0.5):
            for s in (1.0, 1.362):
                r = analyse(mask, rho, sJ, s)
                cases.append(dict(targets=label, rho_local=rho, sigma_logJ=sJ, null_std=s, **r))
                print(f"{label:<10}{rho:>5.2f}{sJ:>6.1f}{s:>6.3f} | {r['T_obs']:>6.2f} "
                      f"{r['ET_median']:>8.2f} ({r['ET_16']:.2f}–{r['ET_84']:.2f}) | {r['p_value']:>8.4f} {r['tension_sigma']:>6.2f}")

dst = BASE / "cloud_reports/2026-10-02_dwarf_J_uncertainty_result.json"
json.dump(dict(input="results/dwarf_consistency/dwarf_consistency.json", bin_gev=d["energies_gev"][ib],
               n_targets_all=int(ok.sum()), n_targets_usable=int((ok & usable).sum()),
               excluded_unusable=[k for k, u in zip(keys, usable) if not u], cases=cases), open(dst, "w"), ensure_ascii=False, indent=2)
print(f"\nsaved {dst.relative_to(BASE)}")
