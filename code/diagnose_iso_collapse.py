#!/usr/bin/env python3
"""低エネルギー側で等方成分 (iso) が桁で潰れる原因を切り分ける。

背景 (2026-07-23、`results/mcmc_allbins_gasICS_v17_nfwcal/FINDINGS_v17.md`):
    等方成分の本研究/Totani 比が、Bin1 0.005 / Bin2 0.005 / Bin3 0.039 と
    **低E 3 ビンだけ桁で潰れる**。同じビンで f_ics が 1.93 / 1.71 / 1.54 と
    論文の想定 (元の規格化 = 1) の約 2 倍に膨らみ、halo が負になる。

問う仮説:
    H1 (縮退): ICS は高緯度でなだらかに広がるので等方成分と形が似ており、
        「ICS を上げて iso を 0 にする」解と「iso を正しく入れる」解が
        尤度でほとんど区別できない (縮退の谷が平ら)。→ iso の潰れは
        パラメータの取り合いであって、上流のミスではない。
    H2 (上流のミス): データがそもそも等方成分を必要としない。
        iso を Totani の値に固定すると尤度が有意に悪化する。

検定:
    f_iso を Totani Fig.6 の値に**固定**して (L-BFGS-B の bounds を上下同値にする)
    残りを再フィットし、自由フィットとの Δln L を測る。
      - Δln L が小さい (数程度) → **H1**。縮退であり、データは両方を区別できない
      - Δln L が大きい (数十以上) → **H2**。データが本当に iso を拒否している

出力: results/audits/iso_collapse_<timestamp>/ に JSON と Markdown。
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

# Totani Fig.6 の等方成分 (目視読み取り、plot_component_overlay_vN.py と同一の値)
TOTANI_ISO = [3.0e-4, 2.3e-4, 1.9e-4, 1.6e-4, 1.3e-4, 1.0e-4, 8.0e-5, 8.0e-5, 3.0e-5]

# 低E 3 ビン (症状が出ている) + Bin6 (対照: 20.76 GeV, 主結果のビン)
TEST_BINS = [0, 1, 2, 5]


def fit(counts, templates, bounds, x0):
    """L-BFGS-B で点推定。bounds の上下を同値にしたパラメータは固定される。"""
    res = minimize(lambda p: m.neg_log_likelihood_and_grad(p, counts, templates),
                   x0=x0, jac=True, method="L-BFGS-B", bounds=bounds,
                   options={"maxiter": 5000, "ftol": 1e-14})
    return res


def main() -> int:
    expmaps, _ = m.load_exposure_maps()
    df_all = m.load_all_events()
    j_map = m.nfw_j_map()
    nfw_norm, _ = m.calibrate_nfw_norm(expmaps[5], j_map)
    s1, s2 = _sub.loop_i_shell_templates()
    df_bubble = m.load_events_with_disk()
    bpos, bneg = m.build_bubble_counts_template(df_bubble)

    rows = []
    for ib in TEST_BINS:
        lo, hi = m.BIN_EDGES[ib], m.BIN_EDGES[ib + 1]
        sel = df_all[(df_all.energy_GeV >= lo) & (df_all.energy_GeV < hi)]
        counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg,
                                      bins=[_sub.L_BINS, _sub.B_BINS])
        gas_i, ics_i = _sub._load_galprop_gas_ics_templates(lo, hi)
        t = m.build_templates_for_bin(ib, counts, expmaps[ib], gas_i, ics_i,
                                      bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
                                      expmap_bubble_bin=expmaps[m.BUBBLE_BIN],
                                      j_map=j_map, nfw_norm=nfw_norm,
                                      loop_shell1=s1, loop_shell2=s2)
        # 本番 (mcmc_fit_all_bins.main) と同一の有効マスク・セル束ね
        valid = (~np.isnan(counts) & ~_sub.extended_source_mask()
                 & (np.abs(m.BG) >= 10) & (np.abs(m.BG) <= 60))
        t["valid"] = valid
        t["valid_pixel"] = valid
        counts_f, t = (m.cellize_counts_and_templates(counts, t, valid)
                       if m.CELL_MODE else (counts, t))

        # f_iso ↔ 物理フラックスの換算 (plot_component_overlay_vN.py と同じ式)
        de_mev = (hi - lo) * 1000.0
        unit = expmaps[ib] * m.PIX_SOLID_ANGLE_SR * de_mev
        e2 = m.BIN_CENTERS[ib] ** 2 * 1e6
        f_iso_totani = TOTANI_ISO[ib] * float(unit.mean()) / e2

        # 本番と同じ初期値 (§3.11: 点源・GALPROP=1、等方=1e-4 相当、その他=0)
        f_iso0 = 1e-4 * float(unit.mean()) / e2
        x0 = np.array([f_iso0 if n == "f_iso" else
                       (1.0 if (n == "f_gas" or n.startswith("f_ics") or n == "f_ps") else 0.0)
                       for n in m.PARAM_NAMES])
        free_b = m._bounds_with_halo()

        res_free = fit(counts_f, t, free_b, x0)
        fixed_b = list(free_b)
        fixed_b[0] = (f_iso_totani, f_iso_totani)     # f_iso は PARAM_NAMES の先頭
        x0_fixed = np.array(res_free.x, dtype=float)
        x0_fixed[0] = f_iso_totani
        res_fix = fit(counts_f, t, fixed_b, x0_fixed)

        d_lnl = float(res_fix.fun - res_free.fun)     # NLL なので正なら固定側が悪い
        row = {
            "bin": ib + 1, "e_center_gev": float(m.BIN_CENTERS[ib]),
            "f_iso_free": float(res_free.x[0]), "f_iso_totani": float(f_iso_totani),
            "iso_ratio_free": float(res_free.x[0] / f_iso_totani),
            "delta_lnL": d_lnl,
            "sigma_equiv": float(np.sqrt(2 * max(d_lnl, 0.0))),
            "free": {n: float(v) for n, v in zip(m.PARAM_NAMES, res_free.x)},
            "iso_fixed": {n: float(v) for n, v in zip(m.PARAM_NAMES, res_fix.x)},
        }
        rows.append(row)
        print(f"[bin{ib + 1:2d}] ΔlnL(iso固定 − 自由) = {d_lnl:10.2f}  "
              f"({row['sigma_equiv']:.1f}σ 相当) | "
              f"f_ics {res_free.x[2]:.3f} → {res_fix.x[2]:.3f} | "
              f"f_halo {res_free.x[-1]:.4g} → {res_fix.x[-1]:.4g}", flush=True)

    # --- 補助測定: 各テンプレートの |b| 依存 ------------------------------------
    # 「fit は iso と ICS を区別できているのか」を直接見る。区別できないなら
    # iso の潰れは単なる縮退だが、区別できているなら fit は本当に「等方成分は不要」
    # と言っていることになる。
    bands = [(10, 20), (20, 30), (30, 40), (40, 50), (50, 60)]
    valid_all = (np.abs(m.BG) >= 10) & (np.abs(m.BG) <= 60)

    def lat_profile(tmpl):
        mean_all = float(tmpl[valid_all].mean())
        return [float(tmpl[(np.abs(m.BG) >= a) & (np.abs(m.BG) < b)].mean() / mean_all)
                for a, b in bands]

    profiles = {}
    for ib in (0, 5):
        lo, hi = m.BIN_EDGES[ib], m.BIN_EDGES[ib + 1]
        unit = expmaps[ib] * m.PIX_SOLID_ANGLE_SR * (hi - lo) * 1000.0
        gas_i, ics_i = _sub._load_galprop_gas_ics_templates(lo, hi)
        profiles[f"bin{ib + 1}"] = {
            "ICS": lat_profile(ics_i * unit),
            "gas": lat_profile(gas_i * unit),
            "iso": lat_profile(unit),
            "halo": lat_profile(j_map * nfw_norm * unit),
        }

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outdir = BASE / "results/audits" / f"iso_collapse_{stamp}"
    outdir.mkdir(parents=True, exist_ok=True)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=BASE, text=True).strip()
    payload = {
        "purpose": "低E で iso が桁で潰れる原因の切り分け (縮退 H1 か、上流のミス H2 か)",
        "commit": commit, "timestamp_utc": stamp, "seed": None,
        "env": {k: os.environ.get(k) for k in
                ("MCMC_ULTRACLEAN", "MCMC_PIXEL_DEG", "MCMC_DISK_BUBBLE",
                 "MCMC_CELL_LIKELIHOOD", "MCMC_SIGNFREE_HALO")},
        "totani_iso_e2dnde": TOTANI_ISO,
        "bins": rows,
        "latitude_bands_deg": bands,
        "latitude_profiles_normalized_to_own_mean": profiles,
    }
    (outdir / "iso_collapse.json").write_text(
        json.dumps(payload, indent=1, ensure_ascii=False), encoding="utf-8")

    md = ["# iso 崩壊の原因切り分け", "",
          f"- commit: `{commit}` / 実行(UTC): {stamp}",
          "- 検定: f_iso を Totani Fig.6 の値に固定して再フィットし、自由フィットとの ΔlnL を測る",
          "- **ΔlnL が小さければ縮退 (H1)、大きければデータが iso を拒否 (H2)**", "",
          "| bin | E [GeV] | 自由 f_iso / Totani | ΔlnL(固定−自由) | σ 相当 | f_ics 自由→固定 | f_halo 自由→固定 |",
          "| ---:| ---:| ---:| ---:| ---:| ---:| ---:|"]
    for r in rows:
        md.append(f"| {r['bin']} | {r['e_center_gev']:.2f} | {r['iso_ratio_free']:.4f} | "
                  f"{r['delta_lnL']:.2f} | {r['sigma_equiv']:.1f} | "
                  f"{r['free']['f_ics']:.3f} → {r['iso_fixed']['f_ics']:.3f} | "
                  f"{r['free']['f_halo']:.4g} → {r['iso_fixed']['f_halo']:.4g} |")
    md += ["", "## 補助測定: 各テンプレートの |b| 依存 (自分の平均 = 1 に規格化)", "",
           "平坦な成分ならどの帯でも 1.0 に近い。iso と ICS の形が違えば fit は両者を区別できる。", "",
           "| ビン | 成分 | " + " | ".join(f"{a}-{b}°" for a, b in bands) + " | 最大/最小 |",
           "| --- | --- | " + " | ".join(["---:"] * (len(bands) + 1)) + " |"]
    for key, comps in profiles.items():
        for cname, p in comps.items():
            md.append(f"| {key} | {cname} | " + " | ".join(f"{x:.3f}" for x in p)
                      + f" | {max(p) / min(p):.2f} |")
    (outdir / "SUMMARY.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"\n[iso-collapse] 出力: {outdir.relative_to(BASE)}/SUMMARY.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
