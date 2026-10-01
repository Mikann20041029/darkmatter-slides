"""[2026-07-31] GALPROP の生テンプレート (フィット前、f=1) を Totani Fig.6 と直接比べる。

**目的**: 「本研究の ICS が Totani より 1.44 倍明るく、その分 IGRB が消えている」ことは
同定済み (2026-07-31)。残る問いは **それが GALPROP 出力そのものの違いなのか、
それともフィットが違う分け方を選んだ結果なのか**である。

  - 生テンプレート (f=1) が既に Totani とずれている → **GALPROP 出力の違い**。
    教授提供の webrun 出力と Totani の出力が違うということになる
  - 生テンプレートは一致するのに、フィット後だけずれる → **分解の問題**。
    テンプレートは正しく、尤度が別の最適点を選んでいる

あわせて、明示的に「定量検証はしていない」と書かれている近似を検証する:

  **エネルギービンの取り方**。`_load_healpix_grid_template` は「ビン中心に最も近い
  1 枚の面」を採り、それに dE (線形幅) を掛けている。正しくは ∫ flux dE。
  GALPROP の面は対数比 1.2997 刻みで、Totani の 1 ビン (比 1.69) はちょうど 2 面ぶん。
  スペクトルが急なら中心値 x 幅 は積分からずれ、**そのずれ方は成分ごとの
  スペクトル指数に依存する**ので、gas と ICS の相対関係を歪めうる。

出力: results/audits/galprop_vs_totani_<UTC>/audit.json
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
from astropy.io import fits as afits
import healpy as hp

os.environ.setdefault("MCMC_PIXEL_DEG", "1.0")

BASE = _pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "code"))

import plot_skymap_all_subtracted as _sub   # noqa: E402

FIG6 = sorted((BASE / "results/audits").glob("totani_fig6_digitized_v2_*/digitized_v2.json"))[-1]
FILES = {"gas": [_sub.GALPROP_HEALPIX_PION, _sub.GALPROP_HEALPIX_BREMSS],
         "ics": [_sub.GALPROP_HEALPIX_ICS]}


def _planes(path: _pathlib.Path) -> tuple[NDArray[np.float64], NDArray[np.float64], int]:
    with afits.open(path) as hdul:
        spec = np.asarray(hdul[1].data["Spectra"], dtype=np.float64)   # (npix, 38)
        e_mev = np.asarray(hdul[2].data["MeV"], dtype=np.float64).ravel()
        nside = int(hdul[1].header["NSIDE"])
    return spec, e_mev, nside


def main() -> None:
    tot = json.loads(FIG6.read_text())
    T = tot["digitized"]
    be = _sub.BIN_EDGES
    bc = np.array(tot["bin_centers_gev"], dtype=float)

    # ROI (|l|,|b| <= 60, |b| >= 10) の画素を HEALPix 上で選ぶ
    lg, bg = _sub.L_GRID.ravel(), _sub.B_GRID.ravel()
    roi = (np.abs(lg) <= 60) & (np.abs(bg) >= 10) & (np.abs(bg) <= 60)

    out: dict[str, Any] = {"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                           "fig6_source": str(FIG6.relative_to(BASE)), "components": {}}
    try:
        out["commit"] = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=BASE,
                                       capture_output=True, text=True).stdout.strip()
    except Exception:
        out["commit"] = "unknown"

    print("生テンプレート (f=1) の ROI 平均 E^2 dN/dE を Totani Fig.6 と比較")
    print("あわせて『中心 1 枚 x 幅』と『正しい積分』の比 (エネルギービンの取り方の誤差)")
    for comp, paths in FILES.items():
        specs = []
        for p in paths:
            s, e_mev, nside = _planes(p)
            specs.append(s)
        spec = sum(specs)
        pix = hp.ang2pix(nside, lg[roi], bg[roi], lonlat=True, nest=False)
        prof = spec[pix].mean(axis=0)          # (38,) ROI 平均のフラックス密度

        rows = []
        print(f"\n--- {comp} ---")
        print(f"  {'E[GeV]':>8} {'生(中心1枚)':>12} {'生(積分)':>12} {'積分/中心':>10} "
              f"{'Totani':>12} {'生/Totani':>10}")
        for i in range(13):
            lo_mev, hi_mev = be[i] * 1000.0, be[i + 1] * 1000.0
            j = int(np.argmin(np.abs(e_mev - bc[i] * 1000.0)))
            # (1) 現行: 中心に最も近い面 x 線形幅
            approx = prof[j] * (hi_mev - lo_mev)
            # (2) 正しい積分: 対数-対数で内挿して台形則
            ee = np.geomspace(lo_mev, hi_mev, 64)
            ff = np.exp(np.interp(np.log(ee), np.log(e_mev), np.log(np.maximum(prof, 1e-300))))
            exact = float(np.trapezoid(ff, ee))
            e2 = (bc[i] * 1000.0) ** 2
            # E^2 dN/dE 相当に直す (積分値を幅で割って中心の E^2 を掛ける)
            a_e2 = e2 * approx / (hi_mev - lo_mev)
            x_e2 = e2 * exact / (hi_mev - lo_mev)
            t = T[comp][i]
            rows.append({"e_gev": float(bc[i]), "approx_e2dnde": a_e2, "exact_e2dnde": x_e2,
                         "exact_over_approx": x_e2 / a_e2,
                         "totani_e2dnde": t,
                         "raw_over_totani": (a_e2 / t) if t else None})
            ts = f"{t:12.3e}" if t else f"{'-':>12}"
            rs = f"{a_e2/t:10.2f}" if t else f"{'-':>10}"
            print(f"  {bc[i]:8.1f} {a_e2:12.3e} {x_e2:12.3e} {x_e2/a_e2:10.4f} {ts} {rs}")
        out["components"][comp] = rows

    d = BASE / f"results/audits/galprop_vs_totani_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    d.mkdir(parents=True, exist_ok=True)
    (d / "audit.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\n→ {d}/audit.json")


if __name__ == "__main__":
    main()
