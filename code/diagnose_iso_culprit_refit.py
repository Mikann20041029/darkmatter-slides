"""[2026-07-31] 等方成分が潰れる原因の**最終同定**。条件を変えて再フィットし、
そのたびに「緯度帯ごとの残差」を測る。

直前の測定 (`diagnose_iso_latitude_residual.py`) で分かったこと (Bin1):
  v20 の最良フィットの残差は **低銀緯で +5.7% (過小予測) / 高銀緯で -4.2% (過剰予測)**。
  つまり**モデルの緯度プロファイルが平坦すぎる**。等方成分は最も平坦なので、
  足すと高銀緯の過剰予測が悪化する (Totani 値を入れると 50-60° で -18%)。
  **だから fit は iso を 0 に潰す。iso が「奪われている」のではなく、
  「入れる余地が無い」。**

では**何がモデルを平坦にしているのか**。候補と、それぞれを潰したときの予測:
  - Loop I シェル1 が犯人なら: 外すと iso が回復し、緯度残差が平らになるはず
    (cv=0.287 と iso の 0.233 に次いで平坦。iso を回帰したときの寄与も 66% と最大)
  - ICS の規格化が犯人なら: f_ics を 1 に固定すると同じことが起きるはず
    (v20 は f_ics=2.35 と GALPROP を 2.35 倍にスケールしている。
     ICS の緯度**形**は Totani と 1% で一致すると確認済みなので、疑うなら絶対値)
  - どちらでもないなら: iso を Totani 値に固定して**他を全て自由に再フィット**しても
    緯度残差が消えない = より上流 (データか露出) の問題

**重要**: 直前の測定は iso を差し替えただけで再フィットしていない。ここでは必ず再フィットする。
他の成分が肩代わりできるなら iso 固定でも当てはまりは悪化しないはずで、
それが起きるかどうかが「縮退」と「余地が無い」を分ける。

出力: results/audits/iso_culprit_refit_<UTC>/refit.json
"""
from __future__ import annotations

import json
import os
import pathlib as _pathlib
import subprocess
import sys
import time
from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import minimize

os.environ.setdefault("MCMC_ULTRACLEAN", "1")
os.environ.setdefault("MCMC_PIXEL_DEG", "0.125")
os.environ.setdefault("MCMC_DISK_BUBBLE", "1")
os.environ.setdefault("MCMC_CELL_LIKELIHOOD", "1")
os.environ.setdefault("MCMC_SIGNFREE_HALO", "1")

BASE = _pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "code"))

import plot_skymap_all_subtracted as _sub   # noqa: E402
import mcmc_fit_all_bins as m               # noqa: E402

TEST_BINS = [0, 2, 5]                 # 1.51 / 4.31 (症状) + 20.76 GeV (対照)
BANDS = [(10, 20), (20, 30), (30, 40), (40, 50), (50, 60)]
TOTANI_ISO = [3.0e-4, 2.3e-4, 1.9e-4, 1.6e-4, 1.3e-4, 1.0e-4, 8.0e-5, 8.0e-5, 3.0e-5]


def main() -> None:
    expmaps, _ = m.load_exposure_maps()
    df_all = m.load_all_events()
    j_map = m.nfw_j_map()
    nfw_norm, _ = m.calibrate_nfw_norm(expmaps[5], j_map)
    s1, s2 = _sub.loop_i_shell_templates()
    bpos, bneg = m.build_bubble_counts_template(m.load_events_with_disk())
    idx = {n: i for i, n in enumerate(m.PARAM_NAMES)}

    out: dict[str, Any] = {"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                           "bands_deg": BANDS, "bins": {}}
    try:
        out["commit"] = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=BASE,
                                       capture_output=True, text=True).stdout.strip()
    except Exception:
        out["commit"] = "unknown"

    for ib in TEST_BINS:
        lo, hi = m.BIN_EDGES[ib], m.BIN_EDGES[ib + 1]
        sel = df_all[(df_all.energy_GeV >= lo) & (df_all.energy_GeV < hi)]
        counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
        gas_i, ics_i = _sub._load_galprop_gas_ics_templates(lo, hi)
        t_pix = m.build_templates_for_bin(
            ib, counts, expmaps[ib], gas_i, ics_i,
            bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
            expmap_bubble_bin=expmaps[m.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
            loop_shell1=s1, loop_shell2=s2)
        valid = (~np.isnan(counts) & ~_sub.extended_source_mask()
                 & (np.abs(m.BG) >= 10) & (np.abs(m.BG) <= 60))
        t_pix["valid"] = valid
        t_pix["valid_pixel"] = valid
        counts_ll, t_ll = m.cellize_counts_and_templates(counts, t_pix, valid)

        unit_mean = float((expmaps[ib] * m.PIX_SOLID_ANGLE_SR * (hi - lo) * 1000.0).mean())
        e2 = m.BIN_CENTERS[ib] ** 2 * 1e6
        f_iso_tot = TOTANI_ISO[ib] * unit_mean / e2

        conds: dict[str, dict[str, float]] = {
            "v20 (自由)": {},
            "Loop I シェル1 を外す": {"f_loopI_a": 0.0},
            "f_ics を 1 に固定": {"f_ics": 1.0},
            "iso を Totani 値に固定": {"f_iso": f_iso_tot},
            "iso 固定 + LoopI-1 外す": {"f_iso": f_iso_tot, "f_loopI_a": 0.0},
        }

        x0 = np.array([1e-4 * unit_mean / e2 if n == "f_iso" else
                       (1.0 if (n == "f_gas" or n.startswith("f_ics") or n == "f_ps") else 0.0)
                       for n in m.PARAM_NAMES])

        rec: dict[str, Any] = {"e_center_gev": float(m.BIN_CENTERS[ib]),
                               "f_iso_totani_equiv": f_iso_tot, "cases": []}
        print(f"\n=== Bin{ib+1} ({m.BIN_CENTERS[ib]:.2f} GeV) "
              f"Totani 相当の f_iso = {f_iso_tot:.5f} ===")
        print(f"  {'条件':24s} {'f_iso':>9} {'iso/Totani':>11} {'f_ics':>7} {'f_LoopI1':>9} "
              f"{'ΔlnL':>9}   残差 % (|b| 10-20 / 20-30 / 30-40 / 40-50 / 50-60)")
        base_nll = None
        for label, fixes in conds.items():
            b = list(m._bounds_with_halo())
            xs = np.array(x0, dtype=float)
            for name, val in fixes.items():
                b[idx[name]] = (val, val)
                xs[idx[name]] = val
            r = minimize(lambda q: m.neg_log_likelihood_and_grad(q, counts_ll, t_ll)[0],
                         xs, jac=lambda q: m.neg_log_likelihood_and_grad(q, counts_ll, t_ll)[1],
                         method="L-BFGS-B", bounds=b, options={"maxiter": 8000, "ftol": 1e-14})
            pp = {n: float(v) for n, v in zip(m.PARAM_NAMES, r.x)}
            if base_nll is None:
                base_nll = float(r.fun)
            mu = np.zeros_like(counts)
            for name, key in m.PARAM_TO_TEMPLATE_KEY.items():
                if name in pp:
                    mu = mu + pp[name] * t_pix[key]
            res = []
            for b0, b1 in BANDS:
                mb = valid & (np.abs(m.BG) >= b0) & (np.abs(m.BG) < b1)
                o = float(counts[mb].sum()); e_ = float(mu[mb].sum())
                res.append(100.0 * (o - e_) / max(o, 1e-300))
            rec["cases"].append({"label": label, "params": pp,
                                 "nll": float(r.fun), "delta_lnL": float(r.fun) - base_nll,
                                 "resid_percent_by_band": res})
            print(f"  {label:24s} {pp['f_iso']:9.5f} {pp['f_iso']/f_iso_tot:11.3f} "
                  f"{pp['f_ics']:7.3f} {pp['f_loopI_a']:9.4f} {float(r.fun)-base_nll:9.1f}   "
                  + " / ".join(f"{v:+6.2f}" for v in res))
        out["bins"][str(ib + 1)] = rec

    d = BASE / f"results/audits/iso_culprit_refit_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    d.mkdir(parents=True, exist_ok=True)
    (d / "refit.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\n→ {d}/refit.json")


if __name__ == "__main__":
    main()
