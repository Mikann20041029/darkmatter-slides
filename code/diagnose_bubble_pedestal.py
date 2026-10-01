#!/usr/bin/env python3
"""バブルテンプレの「台座」を取り除けば等方成分が戻るかを直接試す。

これまでに確定していること (`results/audits/FINDINGS_iso_root_cause.md`):
    低E で gas/ICS/点源/Loop I は Totani と 20% 以内で一致するのに、
    バブル正が 1.3〜1.6 倍・バブル負が 1.6〜2.1 倍明るく、等方成分が 0 に潰れる。
    バブル正テンプレは ROI の 65% を覆い、総量の 42.5% がバブル矩形の外側にある。

本スクリプトの問い:
    **その「矩形の外側に広がった台座」を消せば、等方成分は戻るのか。**

試す変種 (いずれも診断であって、そのまま採用するとは限らない):
    A. baseline                — 現行 (何もしない)
    B. 矩形外をゼロ            — LAT team のバブル矩形 (|l|<22°, 10°<|b|<55°) の外を 0 にする
    C. 矩形外の中央値を差引    — 台座の高さだけ全体から引き、負はクリップ (形は保つ)
    D. 平滑化した台座を差引    — 矩形外を σ=10° で平滑化した「なだらかな床」を引く

判定:
    iso が Totani 値付近に戻り、かつ lnL が大きく悪化しないなら、台座が原因と確定し、
    その変種が対処の候補になる。
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
from scipy.ndimage import gaussian_filter

sys.path.insert(0, "code")
import mcmc_fit_all_bins as m          # noqa: E402
import plot_skymap_all_subtracted as _sub  # noqa: E402

BASE = Path(__file__).resolve().parent.parent
T_ISO = [2.64e-4, 1.59e-4, 1.91e-4, 1.82e-4, 1.60e-4, 1.24e-4, 7.56e-5, 9.83e-5, 1.91e-5]
TEST_BINS = [0, 1, 2, 5]


def variants(bpos, bneg, rect, roi):
    """バブル正負テンプレの 4 変種を返す。"""
    out = {"A_baseline": (bpos, bneg)}

    zp, zn = bpos.copy(), bneg.copy()
    zp[~rect] = 0.0
    zn[~rect] = 0.0
    out["B_矩形外ゼロ"] = (zp, zn)

    cp, cn = bpos.copy(), bneg.copy()
    out_reg = roi & ~rect
    for arr in (cp, cn):
        ped = float(np.median(arr[out_reg]))
        arr -= ped
        np.clip(arr, 0.0, None, out=arr)
    out["C_台座(中央値)差引"] = (cp, cn)

    dp, dn = bpos.copy(), bneg.copy()
    sig = 10.0 / _sub.PIXEL_DEG
    for arr in (dp, dn):
        # 矩形外だけを使って「なだらかな床」を作り、全体から引く
        w = (roi & ~rect).astype(float)
        num = gaussian_filter(np.where(roi & ~rect, arr, 0.0), sigma=sig)
        den = gaussian_filter(w, sigma=sig)
        floor = np.zeros_like(arr)
        ok = den > 1e-6
        floor[ok] = num[ok] / den[ok]
        arr -= floor
        np.clip(arr, 0.0, None, out=arr)
    out["D_台座(平滑床)差引"] = (dp, dn)
    return out


def main() -> int:
    expmaps, _ = m.load_exposure_maps()
    df_all = m.load_all_events()
    j_map = m.nfw_j_map()
    nfw_norm, _ = m.calibrate_nfw_norm(expmaps[5], j_map)
    s1, s2 = _sub.loop_i_shell_templates()
    bpos0, bneg0 = m.build_bubble_counts_template(m.load_events_with_disk())
    idx = {n: i for i, n in enumerate(m.PARAM_NAMES)}

    roi = (np.abs(m.BG) >= 10) & (np.abs(m.BG) <= 60)
    rect = (np.abs(m.LG) < 22) & (np.abs(m.BG) >= 10) & (np.abs(m.BG) < 55)
    vs = variants(bpos0, bneg0, rect, roi)
    for k, (p, n) in vs.items():
        inside = p[rect].sum() / max(p[roi].sum(), 1e-300)
        print(f"  変種 {k:<18} 正テンプレの矩形内割合 = {inside * 100:5.1f}% "
              f"(面積比 33.0%)", flush=True)

    rows = []
    for ib in TEST_BINS:
        lo, hi = m.BIN_EDGES[ib], m.BIN_EDGES[ib + 1]
        de_mev = (hi - lo) * 1000.0
        sel = df_all[(df_all.energy_GeV >= lo) & (df_all.energy_GeV < hi)]
        counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
        gas_i, ics_i = _sub._load_galprop_gas_ics_templates(lo, hi)
        valid = (~np.isnan(counts) & ~_sub.extended_source_mask()
                 & (np.abs(m.BG) >= 10) & (np.abs(m.BG) <= 60))
        denom = float(np.sum(expmaps[ib][valid] * m.PIX_SOLID_ANGLE_SR[valid] * de_mev))
        e2 = m.BIN_CENTERS[ib] ** 2 * 1e6
        unit_mean = float((expmaps[ib] * m.PIX_SOLID_ANGLE_SR * de_mev).mean())
        f_iso_totani = T_ISO[ib] * unit_mean / e2

        rec = {"bin": ib + 1, "e_center_gev": float(m.BIN_CENTERS[ib]), "cases": []}
        base_fun = None
        for label, (bp, bn) in vs.items():
            t = m.build_templates_for_bin(ib, counts, expmaps[ib], gas_i, ics_i,
                                          bubble_counts_bin3_pos=bp, bubble_counts_bin3_neg=bn,
                                          expmap_bubble_bin=expmaps[m.BUBBLE_BIN],
                                          j_map=j_map, nfw_norm=nfw_norm,
                                          loop_shell1=s1, loop_shell2=s2)
            t["valid"] = valid
            t["valid_pixel"] = valid
            c_ll, t_ll = (m.cellize_counts_and_templates(counts, t, valid)
                          if m.CELL_MODE else (counts, t))
            x0 = np.array([1e-4 * unit_mean / e2 if n == "f_iso" else
                           (1.0 if (n == "f_gas" or n.startswith("f_ics") or n == "f_ps") else 0.0)
                           for n in m.PARAM_NAMES])
            r = minimize(lambda p: m.neg_log_likelihood_and_grad(p, c_ll, t_ll),
                         x0=x0, jac=True, method="L-BFGS-B", bounds=m._bounds_with_halo(),
                         options={"maxiter": 5000, "ftol": 1e-14})
            if base_fun is None:
                base_fun = float(r.fun)
            iso_phys = e2 * float(np.sum(r.x[idx["f_iso"]] * t["iso_counts"][valid])) / denom
            rec["cases"].append({
                "label": label,
                "iso_ratio": iso_phys / T_ISO[ib],
                "delta_lnL_vs_baseline": float(base_fun - r.fun),
                "f_halo": float(r.x[-1]),
                "f_gas": float(r.x[idx["f_gas"]]), "f_ics": float(r.x[idx["f_ics"]]),
            })
            c = rec["cases"][-1]
            print(f"[bin{ib + 1:2d}] {label:<18} iso/Totani = {c['iso_ratio']:6.3f}  "
                  f"ΔlnL(基準比) = {c['delta_lnL_vs_baseline']:9.1f}  "
                  f"f_halo = {c['f_halo']:.4g}", flush=True)
        rows.append(rec)
        print(flush=True)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outdir = BASE / "results/audits" / f"bubble_pedestal_{stamp}"
    outdir.mkdir(parents=True, exist_ok=True)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=BASE, text=True).strip()
    (outdir / "pedestal.json").write_text(json.dumps({
        "purpose": "バブルテンプレの台座を除けば等方成分が戻るかの検定",
        "commit": commit, "timestamp_utc": stamp, "seed": None,
        "totani_iso_machine_read": T_ISO, "bins": rows,
    }, indent=1, ensure_ascii=False), encoding="utf-8")
    md = ["# バブルテンプレの台座除去による等方成分の回復検定", "",
          f"- commit: `{commit}` / 実行(UTC): {stamp}", ""]
    for rec in rows:
        md += [f"## Bin{rec['bin']} ({rec['e_center_gev']:.2f} GeV)", "",
               "| 変種 | iso/Totani | ΔlnL(基準比) | f_halo |", "| --- | ---:| ---:| ---:|"]
        for c in rec["cases"]:
            md.append(f"| {c['label']} | {c['iso_ratio']:.3f} | "
                      f"{c['delta_lnL_vs_baseline']:+.1f} | {c['f_halo']:.4g} |")
        md.append("")
    (outdir / "SUMMARY.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"[pedestal] 出力: {outdir.relative_to(BASE)}/SUMMARY.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
