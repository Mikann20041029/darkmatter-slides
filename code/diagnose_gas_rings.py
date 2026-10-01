#!/usr/bin/env python3
"""Totani §3.4.4 の GALPROP 分割 (gas 5 リング + ICS 3 成分) で等方成分が戻るかを検定する。

なぜこれをやるか (Totani §3.4.4 原文):
    "relatively large changes are observed when the cosmic-ray source distribution is
     changed to SNR. In this case, the halo component is positively fitted at all energy
     bins and is nearly zero at the lowest energy bin. This suggests that **one reason for
     the negative halo fits at the lowest energies in the baseline analysis may be the
     uncertainty of the gas component of GALPROP.**"

    すなわち **低エネルギーで halo が負になる原因は GALPROP のガス成分の不確かさ**だと
    Totani 自身が書いている。そして同じ §3.4.4 で、LAT team [7] と同じく
    **ガスを銀河中心距離 5 領域、ICS を 3 成分 (光学/赤外/CMB) に分けて独立フィット**する
    系統チェックを行っている。これはまさにガス形状の不確かさに自由度を与える手当てであり、
    **論文に書かれた正規の手法**なので、再現の枠内で実施できる。

検定する構成:
    A. baseline          — gas 1 枚 + ICS 1 枚 (現行)
    B. ICS 3 分割        — gas 1 枚 + ICS 3 枚
    C. **gas 5 + ICS 3** — Totani §3.4.4 の分割そのもの

判定: 等方成分が Totani 値に戻り、かつ lnL が改善するか。
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

os.environ.setdefault("MCMC_ULTRACLEAN", "1")
os.environ.setdefault("MCMC_PIXEL_DEG", "0.125")
os.environ.setdefault("MCMC_DISK_BUBBLE", "1")
os.environ.setdefault("MCMC_CELL_LIKELIHOOD", "1")
os.environ.setdefault("MCMC_SIGNFREE_HALO", "1")

import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, "code")
import mcmc_fit_all_bins as m          # noqa: E402
import plot_skymap_all_subtracted as _sub  # noqa: E402

BASE = Path(__file__).resolve().parent.parent
T_ISO = [2.64e-4, 1.59e-4, 1.91e-4, 1.82e-4, 1.60e-4, 1.24e-4, 7.56e-5, 9.83e-5, 1.91e-5]
TEST_BINS = [0, 1, 2, 5]


def cell_agg(arr, cid, rv, n_cells=144):
    return np.bincount(cid, weights=np.where(rv, arr.ravel(), 0.0), minlength=n_cells)


def main() -> int:
    expmaps, _ = m.load_exposure_maps()
    df_all = m.load_all_events()
    j_map = m.nfw_j_map()
    nfw_norm, _ = m.calibrate_nfw_norm(expmaps[5], j_map)
    s1, s2 = _sub.loop_i_shell_templates()
    bpos, bneg = m.build_bubble_counts_template(m.load_events_with_disk())

    rows = []
    for ib in TEST_BINS:
        lo, hi = m.BIN_EDGES[ib], m.BIN_EDGES[ib + 1]
        de_mev = (hi - lo) * 1000.0
        sel = df_all[(df_all.energy_GeV >= lo) & (df_all.energy_GeV < hi)]
        counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
        valid = (~np.isnan(counts) & ~_sub.extended_source_mask()
                 & (np.abs(m.BG) >= 10) & (np.abs(m.BG) <= 60))

        unit = expmaps[ib] * m.PIX_SOLID_ANGLE_SR * de_mev
        gas_f, ics_f = _sub._load_galprop_gas_ics_templates(lo, hi)
        gas_rings = _sub._load_healpix_gas_ring_groups(lo, hi)
        ics_c = _sub._load_healpix_ics_components(lo, hi)

        iso_t = unit / max(float(unit.mean()), 1e-300)
        li_a = s1 * unit; li_a /= max(float(li_a.mean()), 1e-300)
        li_b = s2 * unit; li_b /= max(float(li_b.mean()), 1e-300)
        ps_t = _sub.point_source_counts_template(lo, hi, expmaps[ib])
        e3 = m.BIN_CENTERS[m.BUBBLE_BIN]
        de3 = (m.BIN_EDGES[m.BUBBLE_BIN + 1] - m.BIN_EDGES[m.BUBBLE_BIN]) * 1000.0
        ratio = np.divide(expmaps[ib], expmaps[m.BUBBLE_BIN],
                          out=np.zeros_like(expmaps[ib]), where=expmaps[m.BUBBLE_BIN] > 0)
        spec = ratio * (de_mev / de3) * (e3 / m.BIN_CENTERS[ib]) ** 2
        fb_t, fbn_t = bpos * spec, bneg * spec
        halo_t = j_map * nfw_norm * unit

        cid = (np.clip(((m.LG + 60) / 10.0).astype(int), 0, 11) * 12
               + np.clip(((m.BG + 60) / 10.0).astype(int), 0, 11)).ravel()
        rv = valid.ravel()
        ok = np.bincount(cid, weights=rv.astype(float), minlength=144) > 0
        N = cell_agg(counts, cid, rv)[ok]

        denom = float(np.sum(unit[valid]))
        e2 = m.BIN_CENTERS[ib] ** 2 * 1e6

        configs = {
            "A_baseline (gas1+ICS1)": ([gas_f * unit], [ics_f * unit]),
            "B_ICS 3 分割":            ([gas_f * unit], [c * unit for c in ics_c]),
            "C_gas5+ICS3 (§3.4.4)":    ([g * unit for g in gas_rings], [c * unit for c in ics_c]),
        }
        rec = {"bin": ib + 1, "e_center_gev": float(m.BIN_CENTERS[ib]), "cases": []}
        base_fun = None
        for label, (gas_list, ics_list) in configs.items():
            pix_t = [iso_t] + gas_list + ics_list + [ps_t, li_a, li_b, fb_t, fbn_t, halo_t]
            T = [cell_agg(a, cid, rv)[ok] for a in pix_t]
            n = len(T)
            # 符号自由は fb_neg (末尾から2番目) と halo (末尾) のみ
            bnds = [(0.0, None)] * n
            bnds[-1] = (None, None)
            bnds[-2] = (None, None)
            x0 = np.zeros(n)
            x0[0] = 1e-4 * float(unit.mean()) / e2
            for k in range(1, 1 + len(gas_list) + len(ics_list)):
                x0[k] = 1.0
            x0[1 + len(gas_list) + len(ics_list)] = 1.0     # 点源

            def nll(p):
                mu = np.maximum(sum(pi * t for pi, t in zip(p, T)), 1e-10)
                val = float(np.sum(mu - N * np.log(mu)))
                grad = np.array([np.sum((1.0 - N / mu) * t) for t in T])
                return val, grad

            r = minimize(nll, x0=x0, jac=True, method="L-BFGS-B", bounds=bnds,
                         options={"maxiter": 8000, "ftol": 1e-14})
            if base_fun is None:
                base_fun = float(r.fun)
            iso_phys = e2 * float(np.sum(r.x[0] * iso_t[valid])) / denom
            rec["cases"].append({
                "label": label, "n_params": n,
                "iso_ratio": iso_phys / T_ISO[ib],
                "delta_lnL_vs_baseline": float(base_fun - r.fun),
                "f_halo": float(r.x[-1]),
                "f_gas": [float(v) for v in r.x[1:1 + len(gas_list)]],
                "f_ics": [float(v) for v in r.x[1 + len(gas_list):1 + len(gas_list) + len(ics_list)]],
            })
            c = rec["cases"][-1]
            print(f"[bin{ib + 1:2d}] {label:<24} (par={n:2d})  iso/Totani = {c['iso_ratio']:6.3f}  "
                  f"ΔlnL = {c['delta_lnL_vs_baseline']:+9.1f}  f_halo = {c['f_halo']:.4g}", flush=True)
        rows.append(rec)
        print(flush=True)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outdir = BASE / "results/audits" / f"gas_rings_{stamp}"
    outdir.mkdir(parents=True, exist_ok=True)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=BASE, text=True).strip()
    (outdir / "gas_rings.json").write_text(json.dumps({
        "purpose": "Totani §3.4.4 の GALPROP 分割で等方成分が戻るかの検定",
        "commit": commit, "timestamp_utc": stamp, "seed": None,
        "gas_ring_group_edges_kpc": _sub.GAS_RING_GROUP_EDGES_KPC,
        "totani_iso_machine_read": T_ISO, "bins": rows,
    }, indent=1, ensure_ascii=False), encoding="utf-8")
    md = ["# Totani §3.4.4 の GALPROP 分割による等方成分の回復検定", "",
          f"- commit: `{commit}` / 実行(UTC): {stamp}",
          f"- ガス 5 領域の境界 [kpc]: {_sub.GAS_RING_GROUP_EDGES_KPC}", ""]
    for rec in rows:
        md += [f"## Bin{rec['bin']} ({rec['e_center_gev']:.2f} GeV)", "",
               "| 構成 | パラメータ数 | iso/Totani | ΔlnL(基準比) | f_halo |",
               "| --- | ---:| ---:| ---:| ---:|"]
        for c in rec["cases"]:
            md.append(f"| {c['label']} | {c['n_params']} | {c['iso_ratio']:.3f} | "
                      f"{c['delta_lnL_vs_baseline']:+.1f} | {c['f_halo']:.4g} |")
        md.append("")
    (outdir / "SUMMARY.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"[gas-rings] 出力: {outdir.relative_to(BASE)}/SUMMARY.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
