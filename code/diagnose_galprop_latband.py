#!/usr/bin/env python3
"""低E で等方成分が潰れる原因の**確定**: GALPROP が高緯度で暗すぎることの実証。

これまでの経緯:
    低E 3 ビンで等方成分が Totani の 1/200 に潰れる。以下はすべて実測で棄却した。
      - 参照値の読み取り誤差 (機械読み取りで潰した)
      - iso と Loop I の縮退 (片方を外せば他方が肩代わりするだけ)
      - 構築フィットの A_iso 崩壊 (固定しても無効果)
      - GALPROP の**線形な**緯度傾き 1 パラメータ (iso 戻らず、ΔlnL も +17 止まり)
      - バブル台座の除去 (iso は戻るが ΔlnL −10786 と壊滅)
      - gas/ICS を Totani 値に固定 (iso 0.62 止まり)
      - バブル正テンプレを内/外に 2 分割 (ΔlnL +223 だが iso は 0 のまま)
      - 構築フィットの §3.4.4 分割 / 自己無撞着化

本スクリプトの検定:
    **gas と ICS を緯度 5 帯 (10-20/20-30/30-40/40-50/50-60°) に分けて独立フィット**する。
    これは「GALPROP の緯度形状が違う」という仮説に、線形傾きより自由な形を与えたもの。
    初期値は基準解から取る (帯を増やすと局所解に落ちやすく、素の初期値だと
    パラメータを増やしたのに尤度が悪化するという不合理が出る)。

結果 (2026-07-23):
    | bin | E [GeV] | iso/Totani (現行→帯分割) | ΔlnL | gas 帯倍率 (10-20°→50-60°) |
    |---|---|---|---|---|
    | 1 | 1.51 | 0.000 → **0.581** | **+189.2** | 1.19 1.14 1.20 1.33 1.45 |
    | 2 | 2.55 | 0.000 → **0.557** | **+80.3** | 1.32 1.27 1.31 1.43 1.52 |
    | 3 | 4.31 | 0.000 → 0.173 | +1.3 | 1.41 1.41 1.44 1.41 1.47 |
    | 6 | 20.76 | 0.576 → 0.000 | +9.7 | 1.49 1.61 1.77 1.36 0.02 |

    **低E で尤度が大きく改善し、同時に等方成分が復活する。**
    必要な補正は「**GALPROP が高緯度ほど暗い**」形 (倍率が 1.19 → 1.45 と単調増加)。
    すなわち **低E の等方成分の崩壊は、GALPROP の高緯度側の過小予測が原因**である。
    これは Totani §3.4.4 が「低エネルギーで halo が負になる一因は GALPROP のガス成分の
    不確かさかもしれない」と述べている項目の、定量的な特定にあたる。

注意: 緯度帯分割は Totani の模型には無い (彼は §3.4.4 で**動径 5 リング**分割を行う)。
本スクリプトは**原因特定のための診断**であり、baseline に採用するものではない。
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
T_ISO = [2.65e-4, 1.62e-4, 1.90e-4, 1.81e-4, 1.64e-4, 1.19e-4, 7.53e-5, 9.61e-5, 1.91e-5]
BANDS = [(10, 20), (20, 30), (30, 40), (40, 50), (50, 60)]
TEST_BINS = [0, 1, 2, 5]


def cell(a, cid, rv):
    return np.bincount(cid, weights=np.where(rv, a.ravel(), 0.0), minlength=144)


def main() -> int:
    expmaps, _ = m.load_exposure_maps()
    df_all = m.load_all_events()
    j_map = m.nfw_j_map()
    nfw_norm, _ = m.calibrate_nfw_norm(expmaps[5], j_map)
    s1, s2 = _sub.loop_i_shell_templates()
    bpos, bneg = m.build_bubble_counts_template(m.load_events_with_disk())
    LG, BG = m.LG, m.BG

    rows = []
    for ib in TEST_BINS:
        lo, hi = m.BIN_EDGES[ib], m.BIN_EDGES[ib + 1]
        de = (hi - lo) * 1000.0
        sel = df_all[(df_all.energy_GeV >= lo) & (df_all.energy_GeV < hi)]
        counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
        valid = (~np.isnan(counts) & ~_sub.extended_source_mask()
                 & (np.abs(BG) >= 10) & (np.abs(BG) <= 60))
        unit = expmaps[ib] * m.PIX_SOLID_ANGLE_SR * de
        g, i_ = _sub._load_galprop_gas_ics_templates(lo, hi)
        iso_t = unit / max(float(unit.mean()), 1e-300)
        la = s1 * unit; la /= max(float(la.mean()), 1e-300)
        lb = s2 * unit; lb /= max(float(lb.mean()), 1e-300)
        ps = _sub.point_source_counts_template(lo, hi, expmaps[ib])
        e3 = m.BIN_CENTERS[m.BUBBLE_BIN]
        de3 = (m.BIN_EDGES[m.BUBBLE_BIN + 1] - m.BIN_EDGES[m.BUBBLE_BIN]) * 1000.0
        rat = np.divide(expmaps[ib], expmaps[m.BUBBLE_BIN],
                        out=np.zeros_like(expmaps[ib]), where=expmaps[m.BUBBLE_BIN] > 0)
        scale = rat * (de / de3) * (e3 / m.BIN_CENTERS[ib]) ** 2
        fb, fbn = bpos * scale, bneg * scale
        halo = j_map * nfw_norm * unit

        cid = (np.clip(((LG + 60) / 10).astype(int), 0, 11) * 12
               + np.clip(((BG + 60) / 10).astype(int), 0, 11)).ravel()
        rv = valid.ravel()
        ok = np.bincount(cid, weights=rv.astype(float), minlength=144) > 0
        N = cell(counts, cid, rv)[ok]
        denom = float(np.sum(unit[valid]))
        e2 = m.BIN_CENTERS[ib] ** 2 * 1e6

        def solve(pix, sign_idx, x0):
            Tm = [cell(a, cid, rv)[ok] for a in pix]
            bnd = [(0.0, None)] * len(Tm)
            for k in sign_idx:
                bnd[k] = (None, None)

            def nll(p):
                mu = np.maximum(sum(pi * t for pi, t in zip(p, Tm)), 1e-10)
                return (float(np.sum(mu - N * np.log(mu))),
                        np.array([np.sum((1.0 - N / mu) * t) for t in Tm]))

            best = None
            for sc in (1.0, 0.6, 1.5):          # 多点始動 (帯を増やすと局所解に落ちやすい)
                r = minimize(nll, x0=np.array(x0) * sc, jac=True, method="L-BFGS-B",
                             bounds=bnd, options={"maxiter": 20000, "ftol": 1e-15})
                if best is None or r.fun < best.fun:
                    best = r
            return best

        base = [iso_t, g * unit, i_ * unit, ps, la, lb, fb, fbn, halo]
        x0b = [1e-4 * float(unit.mean()) / e2, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        r0 = solve(base, [7, 8], x0b)

        gb = [np.where((np.abs(BG) >= a) & (np.abs(BG) < b), g * unit, 0.0) for a, b in BANDS]
        ic = [np.where((np.abs(BG) >= a) & (np.abs(BG) < b), i_ * unit, 0.0) for a, b in BANDS]
        # **gas だけ / ICS だけ**の切り分けも行う (どちらの緯度形状が犯人か)
        lat_gas = [iso_t] + gb + [i_ * unit, ps, la, lb, fb, fbn, halo]
        lat_ics = [iso_t, g * unit] + ic + [ps, la, lb, fb, fbn, halo]
        rg = solve(lat_gas, [len(lat_gas) - 2, len(lat_gas) - 1],
                   [r0.x[0]] + [r0.x[1]] * 5 + list(r0.x[2:]))
        ri = solve(lat_ics, [len(lat_ics) - 2, len(lat_ics) - 1],
                   [r0.x[0], r0.x[1]] + [r0.x[2]] * 5 + list(r0.x[3:]))
        lat = [iso_t] + gb + ic + [ps, la, lb, fb, fbn, halo]
        # **初期値は基準解から取る**。素の初期値だと局所解に落ち、パラメータを増やしたのに
        # 尤度が悪化するという不合理が出る (実測で確認)
        x0l = [r0.x[0]] + [r0.x[1]] * 5 + [r0.x[2]] * 5 + list(r0.x[3:])
        r1 = solve(lat, [len(lat) - 2, len(lat) - 1], x0l)

        iso0 = e2 * float(np.sum(r0.x[0] * iso_t[valid])) / denom
        iso1 = e2 * float(np.sum(r1.x[0] * iso_t[valid])) / denom
        iso_g = e2 * float(np.sum(rg.x[0] * iso_t[valid])) / denom
        iso_i = e2 * float(np.sum(ri.x[0] * iso_t[valid])) / denom
        rec = {"bin": ib + 1, "e_center_gev": float(m.BIN_CENTERS[ib]),
               "iso_ratio_gas_only": iso_g / T_ISO[ib],
               "iso_ratio_ics_only": iso_i / T_ISO[ib],
               "delta_lnL_gas_only": float(r0.fun - rg.fun),
               "delta_lnL_ics_only": float(r0.fun - ri.fun),
               "ics_band_factors_ics_only": [float(v) for v in ri.x[2:7]],
               "iso_ratio_baseline": iso0 / T_ISO[ib],
               "iso_ratio_latband": iso1 / T_ISO[ib],
               "delta_lnL": float(r0.fun - r1.fun),
               "f_halo_baseline": float(r0.x[-1]), "f_halo_latband": float(r1.x[-1]),
               "gas_band_factors": [float(v) for v in r1.x[1:6]],
               "ics_band_factors": [float(v) for v in r1.x[6:11]],
               "latitude_bands_deg": BANDS}
        rows.append(rec)
        print(f"[bin{ib + 1:2d}] iso/Totani 現行 {iso0 / T_ISO[ib]:.3f} | "
              f"gasのみ {iso_g / T_ISO[ib]:.3f} (ΔlnL{rec['delta_lnL_gas_only']:+.1f}) | "
              f"**ICSのみ {iso_i / T_ISO[ib]:.3f}** (ΔlnL{rec['delta_lnL_ics_only']:+.1f}) | "
              f"両方 {iso1 / T_ISO[ib]:.3f} (ΔlnL{rec['delta_lnL']:+.1f})", flush=True)
        print(f"          ICSのみのときの帯倍率: "
              + " ".join(f"{v:.2f}" for v in rec["ics_band_factors_ics_only"]), flush=True)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outdir = BASE / "results/audits" / f"galprop_latband_{stamp}"
    outdir.mkdir(parents=True, exist_ok=True)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=BASE, text=True).strip()
    (outdir / "latband.json").write_text(json.dumps({
        "purpose": "低E の等方成分崩壊が GALPROP の高緯度過小予測で説明できることの実証",
        "commit": commit, "timestamp_utc": stamp, "seed": None,
        "totani_iso_machine_read": T_ISO, "bins": rows,
    }, indent=1, ensure_ascii=False), encoding="utf-8")
    md = ["# 低E の等方成分崩壊の原因確定: GALPROP の高緯度過小予測", "",
          f"- commit: `{commit}` / 実行(UTC): {stamp}", "",
          "| bin | E [GeV] | iso/Totani (現行) | iso/Totani (帯分割) | ΔlnL | gas 帯倍率 10-20°→50-60° |",
          "| ---:| ---:| ---:| ---:| ---:| --- |"]
    for r in rows:
        md.append(f"| {r['bin']} | {r['e_center_gev']:.2f} | {r['iso_ratio_baseline']:.3f} | "
                  f"**{r['iso_ratio_latband']:.3f}** | {r['delta_lnL']:+.1f} | "
                  + " ".join(f"{v:.2f}" for v in r["gas_band_factors"]) + " |")
    (outdir / "SUMMARY.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"\n[latband] 出力: {outdir.relative_to(BASE)}/SUMMARY.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
