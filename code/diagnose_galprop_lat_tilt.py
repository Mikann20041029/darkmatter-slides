#!/usr/bin/env python3
"""低E の等方成分崩壊が「GALPROP の緯度形状のずれ」で説明できるかを決定的に検定する。

これまでに分かっていること:
    - 低E 3 ビンで等方成分が Totani の 1/200〜1/26 に潰れる (参照値を機械読み取りで
      検証済みなので、参照値の誤りではない: commit eb94cf3)
    - iso を Totani 値に固定すると ΔlnL が 336 / 220 / 64 悪化する (縮退ではない)
    - そのときの残差は **緯度に沿った 1〜2% の波** になる
      (|b|=10-20° で −1.1%、20-50° で +0.8〜+1.2%、50-60° で −0.5%)

検定:
    gas と ICS のテンプレートに **緯度の傾き 1 パラメータ**だけを追加する:
        T'(b) = T(b) · (1 + a · (|b| − 35°) / 25°)
    これは「拡散モデルの緯度形状が少しずれている」という仮説の最小限の表現である。
      - a を入れて **iso が Totani 値付近に戻り、かつ lnL が大きく改善する**
        → 低E の iso 崩壊は **GALPROP の緯度形状のずれが原因**と確定する
      - 戻らない / 改善しない → 別の原因を探す必要がある

注意: これは**診断であって本番の模型ではない**。Totani の模型に緯度傾きは無いので、
本フィットには入れない。原因の帰属にのみ使う。

出力: results/audits/galprop_lat_tilt_<timestamp>/
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
# Totani Fig.6 の等方成分 (機械読み取り値、`code/digitize_totani_fig6.py`)
T_ISO = [2.64e-4, 1.59e-4, 1.91e-4, 1.82e-4, 1.60e-4, 1.24e-4, 7.56e-5, 9.83e-5, 1.91e-5]
TEST_BINS = [0, 1, 2, 5]
BANDS = [(10, 20), (20, 30), (30, 40), (40, 50), (50, 60)]


def main() -> int:
    expmaps, _ = m.load_exposure_maps()
    df_all = m.load_all_events()
    j_map = m.nfw_j_map()
    nfw_norm, _ = m.calibrate_nfw_norm(expmaps[5], j_map)
    s1, s2 = _sub.loop_i_shell_templates()
    bpos, bneg = m.build_bubble_counts_template(m.load_events_with_disk())
    idx = {n: i for i, n in enumerate(m.PARAM_NAMES)}
    n_par = len(m.PARAM_NAMES)

    rows = []
    for ib in TEST_BINS:
        lo, hi = m.BIN_EDGES[ib], m.BIN_EDGES[ib + 1]
        de_mev = (hi - lo) * 1000.0
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

        # 緯度傾き因子 (|b|=35° を軸に、25° で ±a 変化)
        tilt = (np.abs(m.BG) - 35.0) / 25.0

        unit_mean = float((expmaps[ib] * m.PIX_SOLID_ANGLE_SR * de_mev).mean())
        e2 = m.BIN_CENTERS[ib] ** 2 * 1e6
        f_iso_totani = T_ISO[ib] * unit_mean / e2

        def build(a: float):
            """傾き a を gas/ICS に掛けたテンプレート一式 (セル束ね済み) を返す。"""
            t = dict(t_pix)
            fac = 1.0 + a * tilt
            t["gas"] = t_pix["gas"] * fac
            t["ics"] = t_pix["ics"] * fac
            t["valid"] = valid
            t["valid_pixel"] = valid
            return (m.cellize_counts_and_templates(counts, t, valid)
                    if m.CELL_MODE else (counts, t))

        def fit(a: float):
            c_ll, t_ll = build(a)
            x0 = np.array([1e-4 * unit_mean / e2 if n == "f_iso" else
                           (1.0 if (n == "f_gas" or n.startswith("f_ics") or n == "f_ps") else 0.0)
                           for n in m.PARAM_NAMES])
            r = minimize(lambda p: m.neg_log_likelihood_and_grad(p, c_ll, t_ll),
                         x0=x0, jac=True, method="L-BFGS-B", bounds=m._bounds_with_halo(),
                         options={"maxiter": 5000, "ftol": 1e-14})
            return r

        # a を粗くスキャンして最良を選ぶ (パラメータ 1 個なので 1 次元スキャンで十分)
        grid = np.linspace(-0.30, 0.30, 25)
        best = None
        for a in grid:
            r = fit(float(a))
            if best is None or r.fun < best[1].fun:
                best = (float(a), r)
        a_best, r_best = best
        r0 = fit(0.0)

        row = {
            "bin": ib + 1, "e_center_gev": float(m.BIN_CENTERS[ib]),
            "a_best": a_best,
            "delta_lnL_tilt_vs_none": float(r0.fun - r_best.fun),
            "iso_ratio_no_tilt": float(r0.x[idx["f_iso"]] / f_iso_totani),
            "iso_ratio_with_tilt": float(r_best.x[idx["f_iso"]] / f_iso_totani),
            "f_halo_no_tilt": float(r0.x[-1]), "f_halo_with_tilt": float(r_best.x[-1]),
            "f_gas_with_tilt": float(r_best.x[idx["f_gas"]]),
            "f_ics_with_tilt": float(r_best.x[idx["f_ics"]]),
        }
        rows.append(row)
        print(f"[bin{ib + 1:2d}] 最良の傾き a = {a_best:+.3f}  ΔlnL(傾きあり−なし) = "
              f"{row['delta_lnL_tilt_vs_none']:9.1f}  | iso/Totani "
              f"{row['iso_ratio_no_tilt']:.3f} → **{row['iso_ratio_with_tilt']:.3f}**  | "
              f"f_halo {row['f_halo_no_tilt']:.4g} → {row['f_halo_with_tilt']:.4g}", flush=True)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outdir = BASE / "results/audits" / f"galprop_lat_tilt_{stamp}"
    outdir.mkdir(parents=True, exist_ok=True)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=BASE, text=True).strip()
    (outdir / "lat_tilt.json").write_text(json.dumps({
        "purpose": "低E の等方成分崩壊が GALPROP の緯度形状ずれで説明できるかの検定",
        "model": "gas と ICS に T'(b) = T(b)·(1 + a·(|b|-35°)/25°) を掛ける (1 パラメータ)",
        "note": "診断専用。Totani の模型に緯度傾きは無いので本フィットには入れない",
        "commit": commit, "timestamp_utc": stamp, "seed": None,
        "totani_iso_machine_read": T_ISO, "bins": rows,
    }, indent=1, ensure_ascii=False), encoding="utf-8")
    md = ["# GALPROP 緯度形状ずれ仮説の検定", "",
          f"- commit: `{commit}` / 実行(UTC): {stamp}",
          "- gas と ICS に `T'(b) = T(b)·(1 + a·(|b|−35°)/25°)` を掛けて a を 1 次元スキャン", "",
          "| bin | E [GeV] | 最良の傾き a | ΔlnL(傾きあり−なし) | iso/Totani (傾き無) | iso/Totani (傾き有) | f_halo (傾き無→有) |",
          "| ---:| ---:| ---:| ---:| ---:| ---:| ---:|"]
    for r in rows:
        md.append(f"| {r['bin']} | {r['e_center_gev']:.2f} | {r['a_best']:+.3f} | "
                  f"{r['delta_lnL_tilt_vs_none']:.1f} | {r['iso_ratio_no_tilt']:.3f} | "
                  f"**{r['iso_ratio_with_tilt']:.3f}** | "
                  f"{r['f_halo_no_tilt']:.4g} → {r['f_halo_with_tilt']:.4g} |")
    (outdir / "SUMMARY.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"\n[lat-tilt] 出力: {outdir.relative_to(BASE)}/SUMMARY.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
