"""[2026-07-31] 等方成分が潰れる原因を「緯度帯ごとの残差」で決着させる。

これまでの診断は「外すと戻る」(leave-one-out) と「テンプレート同士の似方」
(degeneracy) だったが、どちらも**どの緯度でモデルがデータと合っていないか**を見ていない。
本スクリプトはそこを直接測る。

背景 (2026-07-31 に判明したこと):
  - iso を他テンプレートの線形結合で再現したときの R^2 は **0.36** (|b|>=10、有効セルのみ)。
    つまり iso は幾何的にはさほど縮退していない。「縮退で潰れている」では説明がつかない
  - にもかかわらず v20 の f_iso は相対幅 165% で 0 と無区別。一方 |b|>=40 に絞ると
    f_iso は 55 倍・相対幅 45% と**よく決まる**。R^2 はむしろ高くなる (0.74) のに、である

したがって効いているのは幾何ではなく**尤度の重み**だと考えられる。低銀緯のセルは
明るく光子数が桁違いに多いので、フィットはそこを合わせに行く。その結果として決まった
gas/ICS の規格化が高銀緯で過剰予測になっていれば、**iso は 0 に潰れて辻褄を合わせるしかない**。

測るもの (Bin1, 2, 3, 6):
  1. v20 の最良フィット値での、|b| 帯ごとの観測 / モデル / 残差
  2. iso を Totani 値に固定したときの同じ表 (どの帯で悪化するか)
  3. 各成分が |b| 帯ごとにどれだけ寄与しているか

**予測**: もし「低銀緯に引っ張られた gas/ICS が高銀緯で過剰予測」が真なら、
v20 の残差は高銀緯で**負** (モデル > 観測) になっているはずである。

出力: results/audits/iso_latitude_residual_<UTC>/residual.json
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

os.environ.setdefault("MCMC_ULTRACLEAN", "1")
os.environ.setdefault("MCMC_PIXEL_DEG", "0.125")
os.environ.setdefault("MCMC_DISK_BUBBLE", "1")
os.environ.setdefault("MCMC_CELL_LIKELIHOOD", "1")
os.environ.setdefault("MCMC_SIGNFREE_HALO", "1")

BASE = _pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "code"))

import plot_skymap_all_subtracted as _sub   # noqa: E402
import mcmc_fit_all_bins as m               # noqa: E402

V20 = BASE / "results/mcmc_allbins_gasICS_v20_constructsplit"
TEST_BINS = [0, 1, 2, 5]
BANDS = [(10, 20), (20, 30), (30, 40), (40, 50), (50, 60)]
# Totani Fig.6 から読んだ等方成分の E^2 dN/dE [MeV cm^-2 s^-1 sr^-1]
# (diagnose_iso_thief.py と同一の値を使う)
TOTANI_ISO = [3.0e-4, 2.3e-4, 1.9e-4, 1.6e-4, 1.3e-4, 1.0e-4, 8.0e-5, 8.0e-5, 3.0e-5]


def main() -> None:
    expmaps, _ = m.load_exposure_maps()
    df_all = m.load_all_events()
    j_map = m.nfw_j_map()
    nfw_norm, _ = m.calibrate_nfw_norm(expmaps[5], j_map)
    s1, s2 = _sub.loop_i_shell_templates()
    bpos, bneg = m.build_bubble_counts_template(m.load_events_with_disk())

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
        t = m.build_templates_for_bin(
            ib, counts, expmaps[ib], gas_i, ics_i,
            bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
            expmap_bubble_bin=expmaps[m.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
            loop_shell1=s1, loop_shell2=s2)

        fit = json.loads((V20 / f"mcmc_bin{ib+1:02d}.json").read_text())
        p = {k: v["median"] for k, v in fit["params"].items()}

        valid = (~np.isnan(counts) & ~_sub.extended_source_mask()
                 & (np.abs(m.BG) >= 10) & (np.abs(m.BG) <= 60))

        # v20 の最良フィットでのモデル (画素単位)
        def model(pp: dict[str, float]) -> NDArray[np.float64]:
            mu = np.zeros_like(counts)
            for name, key in m.PARAM_TO_TEMPLATE_KEY.items():
                if name in pp:
                    mu = mu + pp[name] * t[key]
            return mu

        mu_v20 = model(p)
        # iso だけ Totani 値に置き換えたモデル (他は v20 のまま)
        unit_mean = float((expmaps[ib] * m.PIX_SOLID_ANGLE_SR * (hi - lo) * 1000.0).mean())
        e2 = m.BIN_CENTERS[ib] ** 2 * 1e6
        f_iso_totani = TOTANI_ISO[ib] * unit_mean / e2
        p_tot = dict(p)
        p_tot["f_iso"] = f_iso_totani
        mu_tot = model(p_tot)

        rec: dict[str, Any] = {"e_center_gev": float(m.BIN_CENTERS[ib]),
                               "f_iso_v20": p["f_iso"], "f_iso_totani": f_iso_totani,
                               "ratio_v20_over_totani": p["f_iso"] / f_iso_totani,
                               "bands": []}
        print(f"\n=== Bin{ib+1} ({m.BIN_CENTERS[ib]:.2f} GeV) "
              f"f_iso: v20={p['f_iso']:.5f} / Totani 相当={f_iso_totani:.5f} "
              f"(比 {p['f_iso']/f_iso_totani:.4f}) ===")
        print(f"  {'|b| 帯':>10} {'観測':>12} {'v20 モデル':>12} {'残差%':>8} "
              f"{'iso=Totani':>12} {'残差%':>8}   {'iso の占める割合':>14}")
        for b0, b1 in BANDS:
            mband = valid & (np.abs(m.BG) >= b0) & (np.abs(m.BG) < b1)
            obs = float(counts[mband].sum())
            mv = float(mu_v20[mband].sum())
            mt = float(mu_tot[mband].sum())
            iso_share = float((p_tot["f_iso"] * t["iso_counts"])[mband].sum() / max(mt, 1e-300))
            rec["bands"].append({"b_range": [b0, b1], "observed": obs,
                                 "model_v20": mv, "resid_frac_v20": (obs - mv) / max(obs, 1e-300),
                                 "model_iso_totani": mt,
                                 "resid_frac_iso_totani": (obs - mt) / max(obs, 1e-300),
                                 "iso_share_if_totani": iso_share})
            print(f"  {b0:4d}-{b1:<5d} {obs:12.0f} {mv:12.0f} "
                  f"{100*(obs-mv)/max(obs,1e-300):+7.2f}% {mt:12.0f} "
                  f"{100*(obs-mt)/max(obs,1e-300):+7.2f}% {100*iso_share:13.1f}%")
        out["bins"][str(ib + 1)] = rec

    d = BASE / f"results/audits/iso_latitude_residual_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    d.mkdir(parents=True, exist_ok=True)
    (d / "residual.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\n→ {d}/residual.json")


if __name__ == "__main__":
    main()
