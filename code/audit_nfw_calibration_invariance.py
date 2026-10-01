#!/usr/bin/env python3
"""NFW 規格化の基準点を変えても物理結果が不変であることを実測で確かめる。

主張 (`calibrate_nfw_norm` の docstring):
    ハローの寄与は常に `f_halo × norm × j_map` の積の形でしか現れないので、
    規格化 norm を c 倍すると f_halo が 1/c 倍になり、予測カウントは変わらない。
    したがって有意度・物理フラックス・Totani との成分比はすべて不変。

この主張を、基準点 b=−59.94°(旧) と b=90°(新) の 2 つの全13ビン結果を
直接つき合わせて検証する。**「変わらないはず」で済ませないための監査**である。

使い方:
    python code/audit_nfw_calibration_invariance.py <旧resdir> <新resdir>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent


def load(resdir: str) -> dict:
    return json.loads((BASE / resdir / "halo_spectrum.json").read_text())


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    old, new = load(sys.argv[1]), load(sys.argv[2])
    n_old = old["nfw_calibration"]["j_ref"]
    n_new = new["nfw_calibration"]["j_ref"]
    # norm ∝ 1/j_ref なので、f_halo は j_new/j_old 倍になるはず
    expected = n_new / n_old

    print(f"J_ref: 旧 {n_old:.5f} (b={old['nfw_calibration']['b_ref']}) → "
          f"新 {n_new:.5f} (b={new['nfw_calibration']['b_ref']})")
    print(f"f_halo の期待変化率 = J_new/J_old = {expected:.6f}\n")
    # f_halo の中央値は MCMC 事後分布の**サンプルから推定した量**なので、
    # 有意度が低いビン(事後分布が広いビン)では走らせるたびに数 % 揺れる。
    # したがって「相対何 %ずれたか」では判定できない。**事後分布の幅を単位にして**
    # 測る (統計的に区別できるずれか否かを見る) のが正しい基準。
    print(f"{'bin':>3}{'E[GeV]':>9}{'σ(旧)':>9}{'σ(新)':>9}{'Δσ':>9}"
          f"{'f_halo比':>11}{'ずれ%':>9}{'ずれ/事後幅':>12}")
    worst_sig, worst_rel, worst_pull = 0.0, 0.0, 0.0
    for a, b in zip(old["bins"], new["bins"]):
        sa, sb = a["significance_sigma"], b["significance_sigma"]
        fa, fb = a["params"]["f_halo"], b["params"]["f_halo"]
        ratio = fb["median"] / fa["median"] if fa["median"] != 0 else float("nan")
        pred = fa["median"] * expected              # 完全な再パラメータ化ならこうなるはず
        width = (fb["hi84"] - fb["lo16"]) / 2       # 事後分布の 1σ 相当
        rel = abs(fb["median"] / pred - 1.0)
        pull = abs(fb["median"] - pred) / width if width > 0 else float("inf")
        worst_sig = max(worst_sig, abs(sb - sa))
        worst_rel = max(worst_rel, rel)
        worst_pull = max(worst_pull, pull)
        print(f"{a['bin']:>3}{a['e_center_gev']:>9.2f}{sa:>9.3f}{sb:>9.3f}"
              f"{sb - sa:>+9.3f}{ratio:>11.5f}{rel * 100:>8.3f}%{pull:>12.4f}")

    print(f"\n有意度の最大変化: {worst_sig:.4f}σ")
    print(f"f_halo 中央値の期待値からのずれ: 相対で最大 {worst_rel * 100:.3f}%、"
          f"**事後分布の幅を単位にすると最大 {worst_pull:.3f}**")
    # 有意度は点推定(L-BFGS-B)から出るのでスケール同変=厳密に不変であるべき。
    # f_halo 中央値は MCMC 揺らぎを許すが、事後幅の 0.2 倍以内なら統計的に区別できない。
    ok = worst_sig < 1e-3 and worst_pull < 0.2
    print("\n判定: " + ("PASS — 再パラメータ化であり物理結果は不変"
                        " (残差は MCMC のサンプリング揺らぎの範囲)"
                        if ok else "FAIL — 不変でない。原因を調べること"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
