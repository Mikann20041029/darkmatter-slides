#!/usr/bin/env python3
"""v15 → v16 のバブル構築 3 変更を 1 つずつ切り分けて効果を測る (ablation)。

測る指標 (TOTANI_SPEC §7 の検証プロトコル):
    - inside_frac : 正テンプレの総量のうち、LAT team のバブル矩形
      (|l|<22°, 10°<|b|<55°) の内側に入っている割合。面積比 33.0% を大きく上回るほど
      「テンプレートにバブルが写っている」ことを意味する。目標 60% 以上
    - concentration: inside_frac / 面積比 (= 一様なら 1.0)
    - in_out_ratio : 枠内の画素平均 / 枠外の画素平均

使い方:
    MCMC_ULTRACLEAN=1 MCMC_PIXEL_DEG=0.125 MCMC_DISK_BUBBLE=1 \
        python code/audit_bubble_ablation.py

    本スクリプトは各条件を**別プロセスで順次**起動する (同時実行しない。
    本機は 4 コア / 5.8 GB で、過去に並列実行で OOM クラッシュ実績があるため)。
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

# (ラベル, 環境変数の上書き)
CASES: list[tuple[str, dict[str, str]]] = [
    ("v15 相当 (3変更すべて OFF)",
     {"MCMC_BUBBLE_FLUX_SMOOTH": "0", "MCMC_BUBBLE_BOUNDARY_2BIN": "0",
      "MCMC_BUBBLE_MASK_SMOOTH": "0"}),
    ("+ フラックス変換後に平滑化 (§4.6)",
     {"MCMC_BUBBLE_FLUX_SMOOTH": "1", "MCMC_BUBBLE_BOUNDARY_2BIN": "0",
      "MCMC_BUBBLE_MASK_SMOOTH": "0"}),
    ("+ 拡張源を平滑化から除外 (§3.2)",
     {"MCMC_BUBBLE_FLUX_SMOOTH": "1", "MCMC_BUBBLE_BOUNDARY_2BIN": "0",
      "MCMC_BUBBLE_MASK_SMOOTH": "1"}),
    ("+ 境界改善を 2 ビンで (§4.1) = v16",
     {"MCMC_BUBBLE_FLUX_SMOOTH": "1", "MCMC_BUBBLE_BOUNDARY_2BIN": "1",
      "MCMC_BUBBLE_MASK_SMOOTH": "1"}),
]

WORKER = r'''
import sys, json, numpy as np
sys.path.insert(0, "code")
import mcmc_fit_all_bins as M
import plot_skymap_all_subtracted as S

df = M.load_events_with_disk()
pos, neg = S.build_fermi_bubble_templates_posneg(df)
rect = (np.abs(S.L_GRID) < 22) & (np.abs(S.B_GRID) >= 10) & (np.abs(S.B_GRID) < 55)
reg  = (np.abs(S.B_GRID) >= 10) & (np.abs(S.B_GRID) <= 60)
area = float(rect[reg].sum()) / float(reg.sum())
inside = float(pos[rect].sum()) / max(float(pos[reg].sum()), 1e-30)
mi = float(pos[rect].mean()); mo = float(pos[reg & ~rect].mean())
out = {
    "area_frac": area,
    "inside_frac": inside,
    "concentration": inside / area,
    "in_out_ratio": mi / max(mo, 1e-30),
    "pos_sum": float(pos.sum()),
    "neg_sum": float(neg.sum()),
    "neg_over_pos": float(neg.sum()) / max(float(pos.sum()), 1e-30),
}
print("__JSON__" + json.dumps(out))
'''


def main() -> int:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outdir = BASE / "results/audits" / f"bubble_ablation_{stamp}"
    outdir.mkdir(parents=True, exist_ok=True)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=BASE, text=True).strip()

    rows = []
    for label, overrides in CASES:
        env = dict(os.environ)
        env.update(overrides)
        print(f"[ablation] 実行中: {label}", flush=True)
        r = subprocess.run([sys.executable, "-c", WORKER], cwd=BASE, env=env,
                           capture_output=True, text=True)
        (outdir / f"log_{len(rows) + 1}.txt").write_text(r.stdout + r.stderr, encoding="utf-8")
        line = next((ln for ln in r.stdout.splitlines() if ln.startswith("__JSON__")), None)
        if line is None:
            print(f"[ablation] 失敗: {label} (log_{len(rows) + 1}.txt を見てください)", file=sys.stderr)
            return 1
        rows.append({"label": label, "env": overrides, **json.loads(line[len("__JSON__"):])})
        print(f"           inside={rows[-1]['inside_frac'] * 100:.1f}% "
              f"concentration={rows[-1]['concentration']:.2f}x "
              f"in/out={rows[-1]['in_out_ratio']:.2f}", flush=True)

    payload = {
        "purpose": "v15→v16 のバブル構築 3 変更の個別効果 (TOTANI_SPEC §4.1/§4.6/§3.2)",
        "commit": commit,
        "timestamp_utc": stamp,
        "pixel_deg": os.environ.get("MCMC_PIXEL_DEG", "1.0"),
        "ultraclean": os.environ.get("MCMC_ULTRACLEAN", "0"),
        "disk_bubble": os.environ.get("MCMC_DISK_BUBBLE", "0"),
        "boundary_iters": os.environ.get("MCMC_BUBBLE_BOUNDARY_ITERS", "3"),
        "boundary_frac": os.environ.get("MCMC_BUBBLE_BOUNDARY_FRAC", "0.25"),
        "seed": None,
        "cases": rows,
    }
    (outdir / "ablation.json").write_text(json.dumps(payload, indent=1, ensure_ascii=False),
                                          encoding="utf-8")

    md = ["# バブル構築 ablation (v15 → v16)", "",
          f"- commit: `{commit}` / 実行(UTC): {stamp}",
          f"- 設定: PIXEL_DEG={payload['pixel_deg']}, ULTRACLEAN={payload['ultraclean']}, "
          f"DISK_BUBBLE={payload['disk_bubble']}, 境界反復={payload['boundary_iters']}回",
          f"- 面積比 (バブル矩形 / |b|≥10 の ROI) = {rows[0]['area_frac'] * 100:.1f}%",
          "", "| 条件 | 枠内割合 | 集中度 | 枠内/枠外 | 負/正 |",
          "| --- | ---:| ---:| ---:| ---:|"]
    for r in rows:
        md.append(f"| {r['label']} | {r['inside_frac'] * 100:.1f}% | {r['concentration']:.2f}× | "
                  f"{r['in_out_ratio']:.2f} | {r['neg_over_pos']:.3f} |")
    (outdir / "SUMMARY.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"[ablation] 出力: {outdir.relative_to(BASE)}/SUMMARY.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
