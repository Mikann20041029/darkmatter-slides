#!/usr/bin/env python3
"""低E で等方成分 (iso) の席を奪っている成分を特定する (leave-one-out 帰属)。

前段の結果 (`code/diagnose_iso_collapse.py`, commit 9baf02f):
    低E 3 ビンで iso が Totani/IGRB 値の 1/200〜1/26 まで潰れる。
    iso を Totani 値に固定すると ΔlnL = 336 / 220 / 64 (25.9σ / 21.0σ / 11.3σ 相当) 悪化。
    Bin6 は 1.0 (1.4σ) で無傷。**縮退ではなくデータが積極的に拒否**している。
    iso テンプレート自体は次元・単位とも正しい → 原因は上流にある。

本スクリプトの問い:
    等方成分は Fermi が独立に測っている実在の光 (IGRB) なので iso≈0 は物理的にありえない。
    **どの成分がその席を奪っているのか。**

方法 (leave-one-out):
    ある成分 X を「論文どおりの値」に固定するか外すかして再フィットし、
    **f_iso が Totani 値に向かって戻るか**を見る。戻れば X が犯人。
      - `fb_neg=0`  : バブル負テンプレを外す (Bin1 で f_fb_neg=−1.74、寄与が IGRB と同オーダー)
      - `ics=1`     : GALPROP ICS を論文どおり「元の規格化=1」に固定 (低E で 1.93 と 2 倍に膨張)
      - `gas=1`     : GALPROP gas を同様に固定
      - `halo=0`    : halo を外す (低E で負)
      - `loopI=0`   : Loop I を外す
      - `ps=1`      : 点源を元の規格化に固定

    あわせて **iso を Totani 値に固定した模型の残差を |b| 帯ごと**に出し、
    どの緯度で過剰予測しているかを直接見る (犯人の空間的な指紋)。

出力: results/audits/iso_thief_<timestamp>/
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
TOTANI_ISO = [3.0e-4, 2.3e-4, 1.9e-4, 1.6e-4, 1.3e-4, 1.0e-4, 8.0e-5, 8.0e-5, 3.0e-5]
TEST_BINS = [0, 1, 2, 5]                       # Bin1,2,3 (症状) + Bin6 (対照)
BANDS = [(10, 20), (20, 30), (30, 40), (40, 50), (50, 60)]

# 成分を「論文どおりの値」に固定する条件。値 None は「外す(=0 固定)」
LEAVE_ONE_OUT: dict[str, dict[str, float]] = {
    "自由(基準)":            {},
    "バブル負を外す":        {"f_fb_neg": 0.0},
    "ICS を 1 に固定":       {"f_ics": 1.0},
    "gas を 1 に固定":       {"f_gas": 1.0},
    "halo を外す":           {"f_halo": 0.0},
    "Loop I を外す":         {"f_loopI_a": 0.0, "f_loopI_b": 0.0},
    "点源を 1 に固定":       {"f_ps": 1.0},
    "gas も ICS も 1 に固定": {"f_gas": 1.0, "f_ics": 1.0},
}


def fit(counts, t, bounds, x0):
    return minimize(lambda p: m.neg_log_likelihood_and_grad(p, counts, t),
                    x0=x0, jac=True, method="L-BFGS-B", bounds=bounds,
                    options={"maxiter": 5000, "ftol": 1e-14})


def main() -> int:
    expmaps, _ = m.load_exposure_maps()
    df_all = m.load_all_events()
    j_map = m.nfw_j_map()
    nfw_norm, _ = m.calibrate_nfw_norm(expmaps[5], j_map)
    s1, s2 = _sub.loop_i_shell_templates()
    bpos, bneg = m.build_bubble_counts_template(m.load_events_with_disk())
    idx = {n: i for i, n in enumerate(m.PARAM_NAMES)}

    out_bins = []
    for ib in TEST_BINS:
        lo, hi = m.BIN_EDGES[ib], m.BIN_EDGES[ib + 1]
        sel = df_all[(df_all.energy_GeV >= lo) & (df_all.energy_GeV < hi)]
        counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
        gas_i, ics_i = _sub._load_galprop_gas_ics_templates(lo, hi)
        t_pix = m.build_templates_for_bin(ib, counts, expmaps[ib], gas_i, ics_i,
                                          bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
                                          expmap_bubble_bin=expmaps[m.BUBBLE_BIN],
                                          j_map=j_map, nfw_norm=nfw_norm,
                                          loop_shell1=s1, loop_shell2=s2)
        valid = (~np.isnan(counts) & ~_sub.extended_source_mask()
                 & (np.abs(m.BG) >= 10) & (np.abs(m.BG) <= 60))
        t_pix["valid"] = valid
        t_pix["valid_pixel"] = valid
        counts_ll, t_ll = (m.cellize_counts_and_templates(counts, t_pix, valid)
                           if m.CELL_MODE else (counts, t_pix))

        unit_mean = float((expmaps[ib] * m.PIX_SOLID_ANGLE_SR * (hi - lo) * 1000.0).mean())
        e2 = m.BIN_CENTERS[ib] ** 2 * 1e6
        f_iso_totani = TOTANI_ISO[ib] * unit_mean / e2
        x0 = np.array([1e-4 * unit_mean / e2 if n == "f_iso" else
                       (1.0 if (n == "f_gas" or n.startswith("f_ics") or n == "f_ps") else 0.0)
                       for n in m.PARAM_NAMES])

        cases = []
        base_fun = None
        for label, fixes in LEAVE_ONE_OUT.items():
            b = list(m._bounds_with_halo())
            xs = np.array(x0, dtype=float)
            for name, val in fixes.items():
                b[idx[name]] = (val, val)
                xs[idx[name]] = val
            r = fit(counts_ll, t_ll, b, xs)
            if base_fun is None:
                base_fun = float(r.fun)
            cases.append({
                "label": label, "fixes": fixes,
                "f_iso": float(r.x[idx["f_iso"]]),
                "iso_ratio_vs_totani": float(r.x[idx["f_iso"]] / f_iso_totani),
                "delta_lnL_vs_free": float(base_fun - r.fun),     # 正なら基準より良い
                "params": {n: float(v) for n, v in zip(m.PARAM_NAMES, r.x)},
            })
            print(f"[bin{ib + 1:2d}] {label:<22} iso/Totani = "
                  f"{cases[-1]['iso_ratio_vs_totani']:8.4f}   "
                  f"ΔlnL(基準比) = {cases[-1]['delta_lnL_vs_free']:9.2f}", flush=True)

        # --- iso を Totani 値に固定した模型の残差を |b| 帯ごとに ---------------
        b_fix = list(m._bounds_with_halo())
        b_fix[idx["f_iso"]] = (f_iso_totani, f_iso_totani)
        xs = np.array(x0, dtype=float); xs[idx["f_iso"]] = f_iso_totani
        r_fix = fit(counts_ll, t_ll, b_fix, xs)
        mu_pix = m._raw_mu(r_fix.x, t_pix)          # ピクセル単位の模型予測
        prof = []
        for a, bb in BANDS:
            s = valid & (np.abs(m.BG) >= a) & (np.abs(m.BG) < bb)
            d, mo = float(counts[s].sum()), float(mu_pix[s].sum())
            prof.append({"band": f"{a}-{bb}", "data": d, "model": mo,
                         "model_over_data_pct": 100.0 * (mo / d - 1.0) if d > 0 else None})
            print(f"          |b|={a:2d}-{bb:2d}°  模型/データ − 1 = "
                  f"{prof[-1]['model_over_data_pct']:+7.3f}%", flush=True)

        out_bins.append({"bin": ib + 1, "e_center_gev": float(m.BIN_CENTERS[ib]),
                         "f_iso_totani": float(f_iso_totani),
                         "cases": cases, "residual_profile_iso_fixed": prof})
        print(flush=True)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outdir = BASE / "results/audits" / f"iso_thief_{stamp}"
    outdir.mkdir(parents=True, exist_ok=True)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=BASE, text=True).strip()
    payload = {"purpose": "低E で iso の席を奪っている成分の特定 (leave-one-out)",
               "commit": commit, "timestamp_utc": stamp, "seed": None,
               "env": {k: os.environ.get(k) for k in
                       ("MCMC_ULTRACLEAN", "MCMC_PIXEL_DEG", "MCMC_DISK_BUBBLE",
                        "MCMC_CELL_LIKELIHOOD", "MCMC_SIGNFREE_HALO")},
               "totani_iso_e2dnde": TOTANI_ISO, "bins": out_bins}
    (outdir / "iso_thief.json").write_text(json.dumps(payload, indent=1, ensure_ascii=False),
                                           encoding="utf-8")

    md = ["# iso の席を奪っている成分の特定 (leave-one-out)", "",
          f"- commit: `{commit}` / 実行(UTC): {stamp}",
          "- 各成分を「論文どおりの値」に固定/除去して再フィットし、**f_iso が Totani 値に"
          "戻るか**を見る。戻れば、その成分が席を奪っていた", ""]
    for b in out_bins:
        md += [f"## Bin{b['bin']} ({b['e_center_gev']:.2f} GeV)", "",
               "| 条件 | f_iso / Totani | ΔlnL(基準比) |", "| --- | ---:| ---:|"]
        for c in b["cases"]:
            md.append(f"| {c['label']} | {c['iso_ratio_vs_totani']:.4f} | "
                      f"{c['delta_lnL_vs_free']:+.2f} |")
        md += ["", "iso を Totani 値に固定した模型の残差 (正 = 模型が過剰):", "",
               "| \\|b\\| 帯 | 模型/データ − 1 |", "| --- | ---:|"]
        for p in b["residual_profile_iso_fixed"]:
            md.append(f"| {p['band']}° | {p['model_over_data_pct']:+.3f}% |")
        md.append("")
    (outdir / "SUMMARY.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"[iso-thief] 出力: {outdir.relative_to(BASE)}/SUMMARY.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
