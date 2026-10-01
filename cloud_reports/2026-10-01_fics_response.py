"""[クラウド・2026-10-01] 「バブル矩形を外したときだけ f_ics が 1.025 に戻る」は何を意味するか。

調べること (Bin6、v20 と同じ設定):
  1. 各矩形 (除外なし / l0=0 / ±20 / ±30 / ±38) で最尤フィットをやり直し、w1-control-sweep の値を再現できるか
  2. 最尤点のフィッシャー行列から各 f の統計誤差と、f_ics と f_halo・f_gas の相関
  3. f_halo を固定して当て直す:
       除外なしで f_halo = 1.136 (バブル外の値) に固定 → f_ics はいくつになるか
       l0=0 で   f_halo = 1.479 (除外なしの値) に固定 → f_ics はいくつになるか
     f_ics が f_halo に引きずられて動くなら、「1.025 に戻る」は f_halo が下がったことの裏返し

実行 (リポジトリ直下):
  MCMC_ULTRACLEAN=1 MCMC_PIXEL_DEG=0.125 MCMC_DISK_BUBBLE=1 MCMC_CELL_LIKELIHOOD=1 MCMC_SIGNFREE_HALO=1 \\
    python3 cloud_reports/2026-10-01_fics_response.py
テンプレートは /tmp/fics_response_tmpl.npz にキャッシュする (2 回目以降は数十秒)。
"""
import json
import os
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "code"))
for k, v in dict(MCMC_ULTRACLEAN="1", MCMC_PIXEL_DEG="0.125", MCMC_DISK_BUBBLE="1",
                 MCMC_CELL_LIKELIHOOD="1", MCMC_SIGNFREE_HALO="1").items():
    if os.environ.get(k) != v:
        sys.exit(f"環境変数 {k}={v} を付けて実行してください")

import mcmc_fit_all_bins as M  # noqa: E402

_sub = M._sub
IB = 5
CACHE = Path("/tmp/fics_response_tmpl.npz")
KEYS = sorted(set(M.PARAM_TO_TEMPLATE_KEY.values()))

# --- テンプレート (v20 と同じ手順。cloud_reports/2026-10-01_fisher_geometry_check.py と同じ) ---
if CACHE.exists():
    z = np.load(CACHE)
    tmpl = {k: z[k] for k in KEYS}
    counts = z["counts"]
    extra = dict(gas_flux_raw=z["gas_flux_raw"], ics_flux_raw=z["ics_flux_raw"], iso_level=float(z["iso_level"]))
else:
    expmaps, _ = M.load_exposure_maps()
    df_all = M.load_all_events()
    j_map = M.nfw_j_map()
    nfw_norm, _ = M.calibrate_nfw_norm(expmaps[5], j_map)
    df_bubble = M.load_events_with_disk() if M.DISK_BUBBLE else df_all
    fb_pos, fb_neg = M.build_bubble_counts_template(df_bubble)
    shell1, shell2 = _sub.loop_i_shell_templates()
    emin, emax = M.BIN_EDGES[IB], M.BIN_EDGES[IB + 1]
    sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
    counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
    gas_flux, ics_flux = _sub._load_galprop_gas_ics_templates(emin, emax)
    t = M.build_templates_for_bin(
        IB, counts, expmaps[IB], gas_flux, ics_flux,
        bubble_counts_bin3_pos=fb_pos, bubble_counts_bin3_neg=fb_neg,
        expmap_bubble_bin=expmaps[M.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
        loop_shell1=shell1, loop_shell2=shell2, ics_components=None)
    tmpl = {k: t[k] for k in KEYS}
    extra = dict(gas_flux_raw=t["gas_flux_raw"], ics_flux_raw=t["ics_flux_raw"], iso_level=float(t["iso_level"]))
    np.savez(CACHE, counts=counts, **tmpl, **extra)

base_valid = (~_sub.extended_source_mask() & (np.abs(M.BG) >= M.B_MIN_DEG) & (np.abs(M.BG) <= 60))
NAMES = list(M.PARAM_NAMES)
I_ICS, I_HALO, I_GAS = NAMES.index("f_ics"), NAMES.index("f_halo"), NAMES.index("f_gas")


def rect(l0):
    return (np.abs(M.LG - l0) < 22) & (np.abs(M.BG) > 10) & (np.abs(M.BG) < 55)


def cells(valid):
    t = dict(tmpl, **extra, valid=valid, valid_pixel=valid)
    return M.cellize_counts_and_templates(counts, t, valid)


def fit(cc, tc, x0, fix=None):
    """最尤フィット。fix={index: 値} のパラメータは固定する"""
    bounds = M._bounds_with_halo()
    if fix:
        bounds = [(fix[i], fix[i]) if i in fix else b for i, b in enumerate(bounds)]
        x0 = [fix.get(i, x) for i, x in enumerate(x0)]
    f = lambda p: M.neg_log_likelihood_and_grad(p, cc, tc)
    res, diag = M._multistart_minimize(f, x0, bounds)
    return res.x, -res.fun, diag["fun_spread_successful_only"]


def covariance(p, tc):
    ok = tc["valid"]
    mu = M.make_mu(p, tc)[ok]
    X = np.stack([tc[M.PARAM_TO_TEMPLATE_KEY[n]][ok] for n in NAMES], axis=1)
    F = (X / mu[:, None]).T @ X
    return np.linalg.inv(F)


sweep = {}
for tag in ("none", "0", "20", "-20", "30", "-30", "38", "-38"):
    d = json.load(open(BASE / f"results/w1_control_sweep/l0_{tag}_mcmc_bin06.json"))
    sweep[tag] = [d["params"][n]["median"] for n in NAMES]

out = {"names": NAMES, "regions": {}}
print(f"{'領域':>6} | {'f_ics 再現':>10} {'(sweep)':>8} {'±stat':>6} | {'f_halo':>7} {'±stat':>6} | {'r(ics,halo)':>11} {'r(ics,gas)':>10}")
for tag in ("none", "0", "20", "-20", "30", "-30", "38", "-38"):
    valid = base_valid if tag == "none" else base_valid & ~rect(float(tag))
    cc, tc = cells(valid)
    p, lnL, spread = fit(cc, tc, sweep[tag])
    C = covariance(p, tc)
    err = np.sqrt(np.diag(C))
    r_ih = C[I_ICS, I_HALO] / (err[I_ICS] * err[I_HALO])
    r_ig = C[I_ICS, I_GAS] / (err[I_ICS] * err[I_GAS])
    print(f"{tag:>6} | {p[I_ICS]:10.3f} {sweep[tag][I_ICS]:8.3f} {err[I_ICS]:6.3f} | {p[I_HALO]:7.3f} {err[I_HALO]:6.3f} | {r_ih:11.2f} {r_ig:10.2f}")
    out["regions"][tag] = dict(params=p.tolist(), lnL=lnL, fun_spread=spread, stat_err=err.tolist(),
                               corr_ics_halo=float(r_ih), corr_ics_gas=float(r_ig),
                               sweep_params=sweep[tag])

# --- f_halo を固定した当て直し ---
print()
for tag, fh in (("none", 1.136), ("none", 0.0), ("0", 1.479), ("0", 0.0)):
    valid = base_valid if tag == "none" else base_valid & ~rect(0.0)
    cc, tc = cells(valid)
    p, lnL, _ = fit(cc, tc, sweep[tag], fix={I_HALO: fh})
    dlnl = out["regions"][tag]["lnL"] - lnL
    print(f"領域 {tag:>4} で f_halo={fh:.3f} に固定 → f_ics={p[I_ICS]:.3f}, f_gas={p[I_GAS]:.3f} (最尤からの ΔlnL={dlnl:.2f})")
    out.setdefault("fixed_halo", []).append(dict(region=tag, f_halo=fh, params=p.tolist(), delta_lnL_from_best=dlnl))

dst = BASE / "cloud_reports/2026-10-01_fics_response_result.json"
json.dump(out, open(dst, "w"), ensure_ascii=False, indent=2)
print(f"saved {dst.relative_to(BASE)}")
