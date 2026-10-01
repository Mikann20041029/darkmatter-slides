"""[クラウド・2026-10-01] ICS が「銀河中心寄りの領域でだけ何割か明るい」と、ハローと区別できるか。

Totani §4.1: 「ICS モデルの不確かさで説明するには、ICS の地図の形を大きく変える必要がある」。
その「大きく」を数字にする。

方法 (Bin6、v20 と同じテンプレート。2026-10-01_fics_response.py のキャッシュを使う):
  ICS テンプレートを領域 R の内側と外側に分け、別々の倍率 f_ics_in / f_ics_out でフィットする。
  - ハロー無しフィットの f_ics_in / f_ics_out = 「ハローの代わりに ICS の内側だけ何倍明るくすればよいか」
  - その設定でハローを足したときの有意度 = 「その自由度があってもハローが残るか」
  R は 2 種類: (a) バブル矩形 |l|<22°, 10°<|b|<55°  (b) 経度だけで切る |l|<30° (全緯度)

読み方:
  - 必要な倍率が 1.2–1.4 程度で、そのときハローの有意度が大きく下がる
    → ハローは「内側で 2–4 割明るい ICS」と区別できない。非等方 ICS などの既知の不確かさの範囲
  - 必要な倍率が 2 倍を超える、またはハローがほぼ残る → ICS の誤差では説明しにくい (Totani の主張を支持)
"""
import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "code"))
import os  # noqa: E402
for k, v in dict(MCMC_ULTRACLEAN="1", MCMC_PIXEL_DEG="0.125", MCMC_DISK_BUBBLE="1",
                 MCMC_CELL_LIKELIHOOD="1", MCMC_SIGNFREE_HALO="1").items():
    if os.environ.get(k) != v:
        sys.exit(f"環境変数 {k}={v} を付けて実行してください")
import mcmc_fit_all_bins as M  # noqa: E402

CACHE = Path("/tmp/fics_response_tmpl.npz")
if not CACHE.exists():
    sys.exit("先に cloud_reports/2026-10-01_fics_response.py を実行してテンプレートのキャッシュを作ってください")
z = np.load(CACHE)
counts = z["counts"]
_sub = M._sub
valid = (~_sub.extended_source_mask() & (np.abs(M.BG) >= M.B_MIN_DEG) & (np.abs(M.BG) <= 60))
cell = M.CELL_ID.ravel()


def agg(a):
    return np.bincount(cell, weights=np.where(valid.ravel(), a.ravel(), 0.0), minlength=M.N_CELLS)


ok = agg(valid.astype(float)) > 0
cc = agg(counts)[ok]

# v20 の成分 (f_ics だけ内外 2 つに分ける)
base_names = ["f_iso", "f_gas", "f_ps", "f_loopI_a", "f_loopI_b", "f_fb", "f_fb_neg"]
signfree = {"f_fb_neg", "f_halo"}


def run(region, with_halo):
    ics = z["ics"]
    T = {n: agg(z[M.PARAM_TO_TEMPLATE_KEY[n]])[ok] for n in base_names}
    T["f_ics_in"] = agg(ics * region)[ok]
    T["f_ics_out"] = agg(ics * (~region))[ok]
    if with_halo:
        T["f_halo"] = agg(z["halo"])[ok]
    names = list(T)
    X = np.stack([T[n] for n in names], 1)

    def nll(p):
        mu = np.maximum(X @ p, 1e-10)
        return float(np.sum(mu - cc * np.log(mu))), X.T @ (1 - cc / mu)

    bounds = [(None, None) if n in signfree else (0.0, None) for n in names]
    # 初期値: v20 の最尤値に近いところ (f_ics は内外とも 1)
    x0 = dict(f_iso=0.004, f_gas=1.1, f_ps=1.1, f_loopI_a=0.005, f_loopI_b=0.0005,
              f_fb=0.5, f_fb_neg=-0.3, f_ics_in=1.0, f_ics_out=1.0, f_halo=1.0)
    best = None
    for s in (0.3, 0.6, 1.0, 1.5):
        st = np.array([x0[n] * s for n in names])
        st = np.clip(st, [b[0] if b[0] is not None else -np.inf for b in bounds], np.inf)
        r = minimize(nll, st, jac=True, method="L-BFGS-B", bounds=bounds,
                     options=dict(maxiter=5000, maxfun=10000, ftol=1e-15, gtol=1e-12))
        if best is None or r.fun < best.fun:
            best = r
    return dict(zip(names, best.x)), -best.fun


regions = {
    "バブル矩形 |l|<22, 10<|b|<55": (np.abs(M.LG) < 22) & (np.abs(M.BG) > 10) & (np.abs(M.BG) < 55),
    "経度 |l|<30 (全緯度)": np.abs(M.LG) < 30,
}
out = {}
# 基準: ICS 1 枚 (v20 と同じ) の有意度
full = np.ones_like(M.LG, dtype=bool)
p0n, l0n = run(full, False)   # region=全域 → f_ics_out テンプレートは 0 になるので in だけが効く
p0h, l0h = run(full, True)
sig0 = np.sqrt(2 * max(l0h - l0n, 0))
print(f"基準 (ICS 1 枚): ハロー有意度 {sig0:.2f}σ, f_halo={p0h['f_halo']:.3f}, f_ics={p0h['f_ics_in']:.3f}")
out["baseline"] = dict(sigma=sig0, with_halo=p0h, no_halo=p0n)

for label, R in regions.items():
    pn, ln = run(R, False)
    ph, lh = run(R, True)
    sig = np.sqrt(2 * max(lh - ln, 0))
    gain = ln - l0n  # ICS を内外に分けただけで (ハロー無しで) どれだけ当てはまりが良くなるか
    print(f"\n[{label}]")
    print(f"  ハロー無し: f_ics_in={pn['f_ics_in']:.3f}, f_ics_out={pn['f_ics_out']:.3f}, "
          f"内/外 = {pn['f_ics_in'] / pn['f_ics_out']:.2f} 倍 (ICS 1 枚より ΔlnL=+{gain:.1f})")
    print(f"  ハロー有り: f_halo={ph['f_halo']:.3f}, ハロー有意度 {sig:.2f}σ (基準 {sig0:.2f}σ)")
    out[label] = dict(no_halo=pn, with_halo=ph, sigma_halo=sig, delta_lnL_split_vs_single=gain,
                      inner_to_outer_no_halo=pn["f_ics_in"] / pn["f_ics_out"])

dst = BASE / "cloud_reports/2026-10-01_ics_inner_boost_result.json"
json.dump(out, open(dst, "w"), ensure_ascii=False, indent=2, default=float)
print(f"\nsaved {dst.relative_to(BASE)}")
