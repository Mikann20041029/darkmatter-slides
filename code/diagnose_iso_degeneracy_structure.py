"""[2026-07-31] 等方成分 (IGRB) が潰れる原因を「誰と区別できないのか」から特定する。

これまでの経緯:
  - leave-one-out (7/23): Loop I シェル1 を外すと iso が 1.43 倍に戻る
  - flat budget (7/23): バブル正テンプレを外すと合算比が 0.55 → 0.90 に戻る
  - ICS 犯人説 (7/24) は **2026-07-31 に軸取り違えのバグと判明し撤回**
  - 高銀緯フィット (7/31): |b|>=40 で iso が 55 倍に回復 (Totani 比 0.005 → 0.27)

leave-one-out は「外すと戻る」ことしか言えず、**外した成分が本当に犯人なのか、
単に自由度が減って別の成分が肩代わりしただけなのか**を区別できない。
本スクリプトは**フィットを介さず、テンプレートの幾何そのもの**から degeneracy を測る。

測るもの (すべて実際の尤度計算に使う 10° セル上で):
  1. 各テンプレートと iso テンプレートの相関係数
  2. **iso を他の全テンプレートの線形結合でどれだけ再現できるか (R^2)**。
     R^2 が 1 に近ければ iso は独立な情報を持たず、振幅は決まらない
  3. iso を落としたときの寄与の付け替え先 (回帰係数)
  4. 各テンプレートの平坦さ (セル間の max/min と変動係数)

これらは**フィット結果にも初期値にも依存しない幾何量**なので、
「外したら戻った」より強い証拠になる。

出力: results/audits/iso_degeneracy_structure_<UTC>/structure.json
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

# v20 と同一条件で読み込む (テンプレートの作り方が変わるので必須)
os.environ.setdefault("MCMC_ULTRACLEAN", "1")
os.environ.setdefault("MCMC_PIXEL_DEG", "0.125")
os.environ.setdefault("MCMC_DISK_BUBBLE", "1")
os.environ.setdefault("MCMC_CELL_LIKELIHOOD", "1")
os.environ.setdefault("MCMC_SIGNFREE_HALO", "1")

BASE = _pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "code"))

import plot_skymap_all_subtracted as _sub   # noqa: E402
import mcmc_fit_all_bins as m               # noqa: E402

TEST_BINS = [0, 1, 2, 5]          # 1.51 / 2.55 / 4.31 / 20.76 GeV
B_MINS = [10.0, 30.0, 40.0]       # 尤度に使う |b| の下限
# iso 以外で「平坦さの予算」を争う候補
KEYS = ["iso_counts", "gas", "ics", "ps", "loopI_a", "loopI_b", "fb", "fb_neg", "halo"]
LABEL = {"iso_counts": "iso (IGRB)", "gas": "gas", "ics": "ICS", "ps": "点源",
         "loopI_a": "Loop I シェル1", "loopI_b": "Loop I シェル2",
         "fb": "バブル正", "fb_neg": "バブル負", "halo": "halo (NFW)"}


def _r2_of_iso_on_others(cols: dict[str, NDArray[np.float64]]) -> tuple[float, dict[str, float]]:
    """iso を他テンプレートの線形結合で回帰し、決定係数と係数を返す。

    切片は入れない (テンプレートは全て「強度そのもの」であり、
    定数項を足すことは iso をもう 1 本足すのと同じで意味が無いため)。
    """
    y = cols["iso_counts"]
    names = [k for k in cols if k != "iso_counts"]
    X = np.stack([cols[k] for k in names], axis=1)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    ss_tot = float(((y - y.mean()) ** 2).sum())
    ss_res = float((resid ** 2).sum())
    r2 = 1.0 - ss_res / max(ss_tot, 1e-300)
    # 寄与の大きさ = |係数 x そのテンプレートの平均| を iso の平均で割ったもの
    share = {n: float(abs(b * cols[n].mean()) / max(abs(y.mean()), 1e-300))
             for n, b in zip(names, beta)}
    return r2, share


def main() -> None:
    expmaps, _ = m.load_exposure_maps()
    df_all = m.load_all_events()
    j_map = m.nfw_j_map()
    nfw_norm, _ = m.calibrate_nfw_norm(expmaps[5], j_map)
    s1, s2 = _sub.loop_i_shell_templates()
    bpos, bneg = m.build_bubble_counts_template(m.load_events_with_disk())

    out: dict[str, Any] = {
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "pixel_deg": _sub.PIXEL_DEG, "cell_mode": m.CELL_MODE, "b_min_deg_default": m.B_MIN_DEG, "bins": {},
    }
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
        t_pix = m.build_templates_for_bin(
            ib, counts, expmaps[ib], gas_i, ics_i,
            bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
            expmap_bubble_bin=expmaps[m.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
            loop_shell1=s1, loop_shell2=s2)

        rec: dict[str, Any] = {"e_center_gev": float(m.BIN_CENTERS[ib]), "by_bmin": {}}
        for bmin in B_MINS:
            valid = (~np.isnan(counts) & ~_sub.extended_source_mask()
                     & (np.abs(m.BG) >= bmin) & (np.abs(m.BG) <= 60))
            tp = dict(t_pix)
            tp["valid"] = valid
            tp["valid_pixel"] = valid
            _, t_ll = m.cellize_counts_and_templates(counts, tp, valid)
            # [重要] cellize は 144 セルすべてを返し、無効セルは 0 になる。
            # そのゼロを相関に含めると「全成分が同時に 0」という共通項が入り、
            # 相関も R^2 も人為的に 1 に近づく。必ず有効セルだけで測る。
            cell_ok = np.asarray(t_ll["valid"], dtype=bool)
            cols = {k: np.asarray(t_ll[k], dtype=float).ravel()[cell_ok]
                    for k in KEYS if k in t_ll}
            cols = {k: v for k, v in cols.items() if np.isfinite(v).all() and v.std() > 0}

            iso = cols["iso_counts"]
            corr = {k: float(np.corrcoef(iso, v)[0, 1]) for k, v in cols.items() if k != "iso_counts"}
            r2, share = _r2_of_iso_on_others(cols)
            flat = {k: {"max_over_min": float(v.max() / max(v.min(), 1e-300)),
                        "cv": float(v.std() / max(abs(v.mean()), 1e-300))}
                    for k, v in cols.items()}
            rec["by_bmin"][str(bmin)] = {
                "n_cells": int(iso.size), "n_cells_total": int(cell_ok.size), "corr_with_iso": corr,
                "r2_iso_from_others": r2, "share": share, "flatness": flat,
            }
        out["bins"][str(ib + 1)] = rec
        c = rec["by_bmin"]["10.0"]
        top = sorted(c["corr_with_iso"].items(), key=lambda kv: -kv[1])[:3]
        print(f"Bin{ib+1} ({m.BIN_CENTERS[ib]:.2f} GeV, {c['n_cells']} セル): "
              f"iso の R^2 = {c['r2_iso_from_others']:.4f}  "
              f"最も iso と似ている: " + ", ".join(f"{LABEL[k]} {v:.3f}" for k, v in top))

    d = BASE / f"results/audits/iso_degeneracy_structure_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    d.mkdir(parents=True, exist_ok=True)
    (d / "structure.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\n→ {d}/structure.json")


if __name__ == "__main__":
    main()
