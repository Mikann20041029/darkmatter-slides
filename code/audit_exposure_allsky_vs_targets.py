"""[2026-07-31] 全天 HEALPix 露出マップと、旧・天体ごと接平面露出マップの一致を検証する。

解析対象が 80 天体規模になったため、露出を天体ごとに計算する方式
(`compute_exposure_map_targets.py`、6 天体 x 24x24 の接平面 1° グリッド) から
全天 1 枚 (`compute_exposure_map_allsky.py`、HEALPix NSIDE=32 = 1.8°) に切り替えた。
**解像度を粗くしたので、切り替えで値が変わっていないことを実測で確かめる必要がある。**

比較方法: 旧マップが定義されている 6 天体の接平面グリッド点そのもので、
全天マップを球面双線形内挿した値と突き合わせ、相対差の分布を見る。

出力: results/audits/exposure_allsky_vs_targets_<UTC>/audit.json
"""
from __future__ import annotations

import json
import pathlib as _pathlib
import subprocess
import sys
import time

import numpy as np
import healpy as hp

sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))
import target_geometry as tg

BASE = _pathlib.Path(__file__).resolve().parent.parent
OLD = BASE / "data/fermi_exposure/expmap_targets.npz"
NEW = BASE / "data/fermi_exposure/expmap_allsky_healpix.npz"


def main() -> None:
    if not OLD.exists():
        raise SystemExit(f"旧マップが無い: {OLD}")
    o = np.load(OLD, allow_pickle=False)
    n = np.load(NEW, allow_pickle=False)
    names = [str(x) for x in o["names"]]
    old_maps = o["expmaps"]            # (n_t, 13, ng, ng)
    l_grid_all, b_grid_all = o["l_grid"], o["b_grid"]
    new_maps = n["expmaps"]            # (13, npix)
    nside = int(n["nside"])

    result: dict[str, object] = {
        "old_weeks": int(o["n_weeks_ok"]), "new_weeks": int(n["n_weeks_ok"]),
        "nside": nside, "per_target": {},
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    try:
        result["commit"] = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=BASE,
                                          capture_output=True, text=True).stdout.strip()
    except Exception:
        result["commit"] = "unknown"

    print(f"旧: {int(o['n_weeks_ok'])}週 / 新: {int(n['n_weeks_ok'])}週 (NSIDE={nside})")
    print(f"{'天体':14s} {'相対差 平均':>12s} {'標準偏差':>10s} {'最大|差|':>10s}")
    worst = 0.0
    for it, name in enumerate(names):
        lg, bg = l_grid_all[it], b_grid_all[it]
        rel_all = []
        for ib in range(old_maps.shape[1]):
            new_val = hp.get_interp_val(new_maps[ib], lg.ravel(), bg.ravel(), lonlat=True)
            old_val = old_maps[it, ib].ravel()
            rel_all.append((new_val - old_val) / old_val)
        rel = np.concatenate(rel_all)
        result["per_target"][name] = {          # type: ignore[index]
            "mean_rel": float(rel.mean()), "std_rel": float(rel.std()),
            "max_abs_rel": float(np.abs(rel).max()),
        }
        worst = max(worst, float(np.abs(rel).max()))
        print(f"{name:14s} {100*rel.mean():+11.3f}% {100*rel.std():9.3f}% "
              f"{100*np.abs(rel).max():9.3f}%")

    result["worst_abs_rel"] = worst
    d = BASE / f"results/audits/exposure_allsky_vs_targets_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    d.mkdir(parents=True, exist_ok=True)
    (d / "audit.json").write_text(json.dumps(result, indent=2))
    print(f"\n最大の相対差: {100*worst:.3f}%")
    print(f"→ {d}/audit.json")


if __name__ == "__main__":
    main()
