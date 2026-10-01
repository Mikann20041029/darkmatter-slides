"""[2026-07-28] 他天体フィット (`apply_v20_method_targets.py`) の較正を合成データで検証する。

実データを使わずに、フィット機構そのものが正しいかを 2 点で確かめる:

  1. **注入回収**: 既知の f_halo を入れた Poisson 実現から、偏りなく f_halo を戻せるか
  2. **帰無分布**: f_halo = 0 のとき sigma = sign(f)*sqrt(2 dlnL) が |N(0,1)| に従うか

(2) が重要である。halo は符号自由な 1 パラメータなので、帰無仮説の下では
2 dlnL ~ chi^2_1、したがって sigma ~ |N(0,1)| になるはずである。ここがずれていれば
「信号が無いのに有意度が出る」ことになり、他天体の非検出という結論自体が信用できない。

テンプレートは実データの形を模した合成物 (平坦 / 緯度勾配 / 中心集中 / 点源 / ハロー) で、
実データの読み込みも露出マップも要らない。画素数は 60x60 = 3,600 で足りる
(較正は画素数に依存しない)。

出力: results/audits/target_fit_calibration_<UTC>/calibration.json (実行環境つき)
"""
from __future__ import annotations

import json
import pathlib as _pathlib
import platform
import subprocess
import sys
import time
from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy.ndimage import gaussian_filter

sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))
import apply_v20_method_targets as av

BASE = _pathlib.Path(__file__).resolve().parent.parent
SEED = 20260728
N_PIX_SIDE = 60
N_NULL = 200          # 帰無分布の実現数
N_INJECT = 24         # 各注入強度あたりの実現数
INJECT_LEVELS = (0.0, 0.02, 0.05, 0.10, 0.30)   # ROI 平均 1 に正規化した halo の振幅
TRUE_BG = np.array([3.0, 2.0, 1.5, 50.0])       # f_iso, f_gas, f_ics, f_ps


def build_templates() -> tuple[list[NDArray[np.float64]], NDArray[np.float64], float]:
    x = np.linspace(-1, 1, N_PIX_SIDE)
    X, Y = np.meshgrid(x, x, indexing="ij")
    R = np.sqrt(X ** 2 + Y ** 2)
    t_iso = np.ones((N_PIX_SIDE, N_PIX_SIDE))
    t_gas = 1.0 + 0.8 * np.exp(-((Y + 0.5) / 0.4) ** 2)     # 緯度方向の勾配を模す
    t_ics = 1.0 + 0.5 * np.exp(-(R / 1.2) ** 2)             # なだらかな中心集中
    t_ps = np.zeros((N_PIX_SIDE, N_PIX_SIDE))
    t_ps[20, 40] = 1.0
    t_ps[45, 15] = 0.6
    t_ps = gaussian_filter(t_ps, 1.5)                        # PSF で広げた点源 2 個
    t_halo = np.exp(-(R / 0.10) ** 2)                        # PSF 畳み込み後のハロー相当
    t_halo /= t_halo.mean()
    tm = [t.ravel() for t in (t_iso, t_gas, t_ics, t_ps)]
    bg = float(sum(p * t for p, t in zip(TRUE_BG, tm)).sum())
    return tm, t_halo.ravel(), bg


def one_realization(f_true: float, tm: list[NDArray[np.float64]], th: NDArray[np.float64],
                    rng: np.random.Generator) -> tuple[float, float]:
    mu = sum(p * t for p, t in zip(TRUE_BG, tm)) + f_true * th
    counts = rng.poisson(np.clip(mu, 1e-9, None)).astype(float)
    bnd: list[tuple[float, float | None]] = [(0.0, None)] * 4
    f_nh, x_nh = av._fit(counts, tm, bnd, TRUE_BG.copy())
    f_h, x_h = av._fit(counts, tm + [th], bnd + [(None, None)], np.append(x_nh, 0.0))
    fh = float(x_h[-1])
    return fh, float(np.sign(fh) * np.sqrt(2.0 * max(f_nh - f_h, 0.0)))


def env_stamp() -> dict[str, str]:
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=BASE,
                                capture_output=True, text=True).stdout.strip()
    except Exception:
        commit = "unknown"
    return {"commit": commit, "python": sys.version.split()[0], "numpy": np.__version__,
            "platform": platform.platform(),
            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}


def main() -> None:
    rng = np.random.default_rng(SEED)
    tm, th, bg = build_templates()
    halo_counts_per_unit = float(th.sum())
    out: dict[str, Any] = {"meta": {**env_stamp(), "seed": SEED, "n_pix": N_PIX_SIDE ** 2,
                                    "bg_total_counts": bg,
                                    "halo_counts_per_unit_f": halo_counts_per_unit},
                           "injection": [], "null": {}}

    print(f"背景の総カウント = {bg:.0f} (halo は f=1 で {halo_counts_per_unit:.0f} カウント)")
    print("注入回収:")
    for f_true in INJECT_LEVELS:
        rec = [one_realization(f_true, tm, th, rng) for _ in range(N_INJECT)]
        fh = np.array([r[0] for r in rec])
        sg = np.array([r[1] for r in rec])
        row = {"f_true": f_true, "signal_counts": f_true * halo_counts_per_unit,
               "signal_frac_of_bg": f_true * halo_counts_per_unit / bg,
               "f_mean": float(fh.mean()), "f_std": float(fh.std()),
               "bias": float(fh.mean() - f_true),
               "sigma_mean": float(sg.mean()), "sigma_std": float(sg.std())}
        out["injection"].append(row)
        print(f"  f={f_true:5.2f} (背景の {100*row['signal_frac_of_bg']:5.2f}%) → "
              f"回収 {row['f_mean']:+7.4f} ± {row['f_std']:6.4f} "
              f"(偏り {row['bias']:+7.4f})  sigma {row['sigma_mean']:+6.2f} ± {row['sigma_std']:4.2f}")

    print(f"帰無分布 ({N_NULL} 実現):")
    sg = np.array([one_realization(0.0, tm, th, rng)[1] for _ in range(N_NULL)])
    a = np.abs(sg)
    out["null"] = {"n": N_NULL, "abs_mean": float(a.mean()), "abs_median": float(np.median(a)),
                   "frac_gt1": float(np.mean(a > 1)), "frac_gt2": float(np.mean(a > 2)),
                   "frac_positive": float(np.mean(sg > 0)),
                   "expected": {"abs_mean": 0.7979, "abs_median": 0.6745,
                                "frac_gt1": 0.3173, "frac_gt2": 0.0455, "frac_positive": 0.5}}
    e = out["null"]["expected"]
    print(f"  |sigma| 平均 {a.mean():.3f} (期待 {e['abs_mean']:.3f}) / "
          f"中央値 {np.median(a):.3f} (期待 {e['abs_median']:.3f})")
    print(f"  |sigma|>1 {100*np.mean(a>1):.1f}% (期待 {100*e['frac_gt1']:.1f}%) / "
          f"|sigma|>2 {100*np.mean(a>2):.1f}% (期待 {100*e['frac_gt2']:.1f}%)")

    d = BASE / f"results/audits/target_fit_calibration_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    d.mkdir(parents=True, exist_ok=True)
    (d / "calibration.json").write_text(json.dumps(out, indent=2))
    print(f"→ {d}/calibration.json")


if __name__ == "__main__":
    main()
