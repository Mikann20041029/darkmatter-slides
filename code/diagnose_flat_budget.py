#!/usr/bin/env python3
"""平坦成分の「合算予算」(iso + Loop I) が Totani の約半分しかない原因を特定する。

前段 (commit 4bc8d5b):
    Loop I shell1 は太陽が殻の壁の中 (62 < d=78 < 81 pc) にあるため ROI の 100% を覆い、
    等方テンプレより平坦。よって **iso 単独 / Loop I 単独の比較は意味を持たない**。
    データが決めるのは合算だけであり、その合算比は全エネルギーで 0.41〜0.65 =
    **一律に約 50% 不足**。低E 特有の症状ではなかった。

本スクリプトの問い:
    **その不足分はどこへ行っているのか。**

方法:
    前段と同じ leave-one-out だが、**指標を「iso + Loop I の物理フラックス合算」**に変える
    (前段は f_iso 単独を見ていたため、Loop I が肩代わりする経路に隠されていた)。
    ある成分 X を外して合算予算が Totani 値に戻れば、X が予算を食っていた犯人。

容疑者:
    - `fb_neg` : バブル**負**テンプレ。符号自由で、低E では f_fb_neg < 0。
      ROI の 41% を覆う広域テンプレなので、**広く薄い負の下駄**として働き
      平坦成分の予算を食いうる (最有力容疑)
    - `fb`     : バブル正テンプレ (同様に広域)
    - `ps`     : 点源 (f_ps が 1.2〜1.4 と過剰気味)
    - `gas` / `ics` : GALPROP (高E で f_gas が 1.7 超)
    - `halo`   : ハロー

出力: results/audits/flat_budget_<timestamp>/
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

# Totani Fig.6 目視読み取り (plot_component_overlay_vN.py と同一)
T_ISO = [3.0e-4, 2.3e-4, 1.9e-4, 1.6e-4, 1.3e-4, 1.0e-4, 8.0e-5, 8.0e-5, 3.0e-5]
T_LI = [4.5e-4, 4.0e-4, 3.5e-4, 3.3e-4, 2.0e-4, 1.4e-4, 1.3e-4, 2.0e-5, None]
TEST_BINS = [0, 2, 5, 7]                      # 1.51 / 4.31 / 20.76 / 59.22 GeV

CASES: dict[str, dict[str, float]] = {
    "自由(基準)":          {},
    "バブル負を外す":      {"f_fb_neg": 0.0},
    "バブル正を外す":      {"f_fb": 0.0},
    "バブル正負とも外す":  {"f_fb": 0.0, "f_fb_neg": 0.0},
    "点源を 1 に固定":     {"f_ps": 1.0},
    "gas を 1 に固定":     {"f_gas": 1.0},
    "ICS を 1 に固定":     {"f_ics": 1.0},
    "halo を外す":         {"f_halo": 0.0},
}


def main() -> int:
    expmaps, _ = m.load_exposure_maps()
    df_all = m.load_all_events()
    j_map = m.nfw_j_map()
    nfw_norm, _ = m.calibrate_nfw_norm(expmaps[5], j_map)
    s1, s2 = _sub.loop_i_shell_templates()
    bpos, bneg = m.build_bubble_counts_template(m.load_events_with_disk())
    idx = {n: i for i, n in enumerate(m.PARAM_NAMES)}

    out = []
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
        counts_ll, t_ll = (m.cellize_counts_and_templates(counts, t_pix, valid)
                           if m.CELL_MODE else (counts, t_pix))

        # counts テンプレ → 物理 E²dN/dE への換算 (plot_component_overlay_vN.py と同式)
        denom = float(np.sum(expmaps[ib][valid] * m.PIX_SOLID_ANGLE_SR[valid] * de_mev))
        e2 = m.BIN_CENTERS[ib] ** 2 * 1e6

        def phys(key: str, f: float) -> float:
            return e2 * float(np.sum(f * t_pix[key][valid])) / denom

        x0 = np.array([1e-4 * float((expmaps[ib] * m.PIX_SOLID_ANGLE_SR * de_mev).mean()) / e2
                       if n == "f_iso" else
                       (1.0 if (n == "f_gas" or n.startswith("f_ics") or n == "f_ps") else 0.0)
                       for n in m.PARAM_NAMES])

        t_flat = T_ISO[ib] + (T_LI[ib] or 0.0)
        rows, base_fun = [], None
        for label, fixes in CASES.items():
            b = list(m._bounds_with_halo())
            xs = np.array(x0, dtype=float)
            for name, val in fixes.items():
                b[idx[name]] = (val, val)
                xs[idx[name]] = val
            r = minimize(lambda p: m.neg_log_likelihood_and_grad(p, counts_ll, t_ll),
                         x0=xs, jac=True, method="L-BFGS-B", bounds=b,
                         options={"maxiter": 5000, "ftol": 1e-14})
            if base_fun is None:
                base_fun = float(r.fun)
            f = {n: float(v) for n, v in zip(m.PARAM_NAMES, r.x)}
            iso_p = phys("iso_counts", f["f_iso"])
            li_p = phys("loopI_a", f["f_loopI_a"]) + phys("loopI_b", f["f_loopI_b"])
            rows.append({
                "label": label, "fixes": fixes,
                "iso_e2dnde": iso_p, "loopI_e2dnde": li_p, "flat_sum_e2dnde": iso_p + li_p,
                "flat_sum_ratio_vs_totani": (iso_p + li_p) / t_flat,
                "delta_lnL_vs_free": float(base_fun - r.fun),
                "params": f,
            })
            print(f"[bin{ib + 1:2d}] {label:<20} 合算/Totani = "
                  f"{rows[-1]['flat_sum_ratio_vs_totani']:6.3f}   "
                  f"ΔlnL(基準比) = {rows[-1]['delta_lnL_vs_free']:9.2f}", flush=True)

        out.append({"bin": ib + 1, "e_center_gev": float(m.BIN_CENTERS[ib]),
                    "totani_flat_sum_e2dnde": t_flat, "cases": rows})
        print(flush=True)

    # バブル負テンプレの空間的な広がり (「広く薄い下駄」になっていないかの確認)
    valid_any = (np.abs(m.BG) >= 10) & (np.abs(m.BG) <= 60)
    rect = (np.abs(m.LG) < 22) & (np.abs(m.BG) >= 10) & (np.abs(m.BG) < 55)
    cover = {
        "fb_neg_nonzero_frac_in_roi": float((bneg[valid_any] > 0).mean()),
        "fb_pos_nonzero_frac_in_roi": float((bpos[valid_any] > 0).mean()),
        "fb_neg_frac_of_total_inside_bubble_rect": float(
            bneg[rect].sum() / max(bneg[valid_any].sum(), 1e-300)),
        "bubble_rect_area_frac": float(rect[valid_any].sum() / valid_any.sum()),
    }
    print("バブル負テンプレの広がり: ROI の "
          f"{cover['fb_neg_nonzero_frac_in_roi'] * 100:.1f}% が非ゼロ / "
          f"矩形内に総量の {cover['fb_neg_frac_of_total_inside_bubble_rect'] * 100:.1f}% "
          f"(矩形の面積比 {cover['bubble_rect_area_frac'] * 100:.1f}%)")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outdir = BASE / "results/audits" / f"flat_budget_{stamp}"
    outdir.mkdir(parents=True, exist_ok=True)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=BASE, text=True).strip()
    (outdir / "flat_budget.json").write_text(json.dumps({
        "purpose": "平坦成分の合算予算 (iso + Loop I) が Totani の約半分しかない原因の特定",
        "commit": commit, "timestamp_utc": stamp, "seed": None,
        "env": {k: os.environ.get(k) for k in
                ("MCMC_ULTRACLEAN", "MCMC_PIXEL_DEG", "MCMC_DISK_BUBBLE",
                 "MCMC_CELL_LIKELIHOOD", "MCMC_SIGNFREE_HALO")},
        "totani_iso": T_ISO, "totani_loopI": T_LI,
        "bubble_template_coverage": cover, "bins": out,
    }, indent=1, ensure_ascii=False), encoding="utf-8")

    md = ["# 平坦成分の合算予算 (iso + Loop I) の欠損の帰属", "",
          f"- commit: `{commit}` / 実行(UTC): {stamp}",
          "- 指標は **iso + Loop I の物理フラックス合算 / Totani 合算**。",
          "  iso 単独では Loop I が肩代わりする経路に隠れるため合算で見る", ""]
    for b in out:
        md += [f"## Bin{b['bin']} ({b['e_center_gev']:.2f} GeV)", "",
               "| 条件 | 合算/Totani | ΔlnL(基準比) |", "| --- | ---:| ---:|"]
        for c in b["cases"]:
            md.append(f"| {c['label']} | {c['flat_sum_ratio_vs_totani']:.3f} | "
                      f"{c['delta_lnL_vs_free']:+.2f} |")
        md.append("")
    md += ["## バブルテンプレの空間的な広がり", "",
           f"- 負テンプレが ROI で非ゼロの画素: **{cover['fb_neg_nonzero_frac_in_roi'] * 100:.1f}%**",
           f"- 正テンプレが ROI で非ゼロの画素: {cover['fb_pos_nonzero_frac_in_roi'] * 100:.1f}%",
           f"- 負テンプレの総量のうちバブル矩形の内側: "
           f"{cover['fb_neg_frac_of_total_inside_bubble_rect'] * 100:.1f}% "
           f"(矩形の面積比 {cover['bubble_rect_area_frac'] * 100:.1f}%)"]
    (outdir / "SUMMARY.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"[flat-budget] 出力: {outdir.relative_to(BASE)}/SUMMARY.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
