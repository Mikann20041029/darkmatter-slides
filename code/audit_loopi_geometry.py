#!/usr/bin/env python3
"""Loop I シェル幾何が「全天ほぼ一様」になっていないかを検査する。

なぜ検査するか (2026-07-23、`code/diagnose_iso_thief.py` の leave-one-out 結果):
    低E で等方成分 (iso) が Totani/IGRB 値の 1/200 まで潰れる。
    **Loop I を外すと iso は 1.33〜1.54 倍まで戻る**(Bin1/2/3/6 の全てで)。
    他の成分 (バブル負・gas・halo・点源) を外しても戻らない。
    → Loop I が等方成分の席を奪っている。

疑う幾何:
    Loop I は「一様放射率の 2 球殻」で、パラメータは LAT team 論文 (Ackermann+2014/2017)
    由来 (Totani §2.3 も同じ模型を使うと明記)。
      shell1: 中心 (l,b)=(341°,3°)、太陽からの距離 d=78 pc、殻 r=62–81 pc
      shell2: 中心 (l,b)=(332°,37°)、d=95 pc、殻 r=58–82 pc
    **shell1 は r_in < d < r_out、すなわち太陽が殻の壁の中に埋まっている。**
    その場合、どの方向を見ても視線は直ちに放射体の中を通るので、
    地図が全天ほぼ一様になり、等方背景と数学的に区別がつかなくなる。

本スクリプトはこれを数値で確認する (MCMC を回さないので数秒で終わる)。
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

os.environ.setdefault("MCMC_PIXEL_DEG", "0.125")

import numpy as np

sys.path.insert(0, "code")
import plot_skymap_all_subtracted as _sub  # noqa: E402

BASE = Path(__file__).resolve().parent.parent
SHELLS = [
    dict(name="shell1", l=341.0, b=3.0, d_pc=78.0, r_in_pc=62.0, r_out_pc=81.0),
    dict(name="shell2", l=332.0, b=37.0, d_pc=95.0, r_in_pc=58.0, r_out_pc=82.0),
]
BANDS = [(10, 20), (20, 30), (30, 40), (40, 50), (50, 60)]


def main() -> int:
    s1, s2 = _sub.loop_i_shell_templates()
    BG = _sub.B_GRID
    valid = (np.abs(BG) >= 10) & (np.abs(BG) <= 60)

    rows = []
    for sh, tmpl in zip(SHELLS, (s1, s2)):
        sun_inside_wall = sh["r_in_pc"] < sh["d_pc"] < sh["r_out_pc"]
        prof = [float(tmpl[valid & (np.abs(BG) >= a) & (np.abs(BG) < b)].mean())
                for a, b in BANDS]
        mean_all = float(tmpl[valid].mean())
        prof_n = [p / mean_all for p in prof]
        nonzero = float((tmpl[valid] > 0).mean())
        rows.append({
            **sh,
            "sun_inside_shell_wall": bool(sun_inside_wall),
            "nonzero_fraction_in_roi": nonzero,
            "latitude_profile_normalized": prof_n,
            "flatness_max_over_min": float(max(prof_n) / min(prof_n)),
            "pixel_min_over_max": float(tmpl[valid].min() / tmpl[valid].max())
            if tmpl[valid].max() > 0 else None,
        })
        print(f"[{sh['name']}] 太陽が殻の壁の中: {'はい' if sun_inside_wall else 'いいえ'}"
              f"  (r_in={sh['r_in_pc']:.0f} < d={sh['d_pc']:.0f} < r_out={sh['r_out_pc']:.0f} pc?)")
        print(f"          ROI 内で値が非ゼロの画素の割合: {nonzero * 100:.1f}%")
        print(f"          |b| プロファイル(平均=1): "
              + " ".join(f"{x:.3f}" for x in prof_n)
              + f"  → 最大/最小 = {max(prof_n) / min(prof_n):.2f}")

    # 参照: 等方テンプレ (= 露出 × 立体角) の平坦さ。これより平坦なら iso と区別できない
    expmaps = np.load(str(BASE / "data/fermi_exposure/expmap_allbins.npz"))
    em = expmaps["expmaps"][0]
    if em.shape != BG.shape:
        from scipy.ndimage import zoom
        em = zoom(em, (BG.shape[0] / em.shape[0], BG.shape[1] / em.shape[1]), order=1)
    iso_t = em * (np.cos(np.radians(BG)))
    iso_prof = [float(iso_t[valid & (np.abs(BG) >= a) & (np.abs(BG) < b)].mean())
                for a, b in BANDS]
    iso_prof = [p / float(iso_t[valid].mean()) for p in iso_prof]
    iso_flat = max(iso_prof) / min(iso_prof)
    print(f"\n[参照] 等方テンプレの |b| プロファイル: "
          + " ".join(f"{x:.3f}" for x in iso_prof) + f"  → 最大/最小 = {iso_flat:.2f}")
    verdict = [r["name"] for r in rows if r["flatness_max_over_min"] < iso_flat]
    print(f"\n判定: 等方テンプレより平坦な Loop I シェル = {verdict or 'なし'}")
    if verdict:
        print("  → そのシェルは等方背景と数学的に区別できない。両者の分け方は"
              "データから決まらない (合計だけが決まる)")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outdir = BASE / "results/audits" / f"loopi_geometry_{stamp}"
    outdir.mkdir(parents=True, exist_ok=True)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=BASE, text=True).strip()
    (outdir / "loopi_geometry.json").write_text(json.dumps({
        "purpose": "Loop I シェルが全天ほぼ一様になり等方背景と縮退していないかの検査",
        "commit": commit, "timestamp_utc": stamp, "seed": None,
        "pixel_deg": os.environ.get("MCMC_PIXEL_DEG"),
        "latitude_bands_deg": BANDS,
        "iso_template_latitude_profile": iso_prof,
        "iso_template_flatness": iso_flat,
        "shells": rows,
        "flatter_than_isotropic": verdict,
    }, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"\n[loopi-geometry] 出力: {outdir.relative_to(BASE)}/loopi_geometry.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
