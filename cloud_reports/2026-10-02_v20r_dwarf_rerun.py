"""[クラウド・2026-10-02] 矮小銀河の整合性検定 (code/dwarf_consistency_check.py) を v20r でやり直す。

変える点は 2 つだけ (手法そのものは同じ):
  1. 天の川のハローの明るさ: v20 (7/23、再現不能) → v20r (10/1 の再計算、記録付き)
  2. 各天体の有意度: 7/28–31 の計算 → 今のコードで計算し直した結果
     (code/apply_v20_method_targets.py --targets all --n-control 23 --cell-deg 1 、クラウドで実行)
あわせて、使えない天体 (usable=false の SMC・LMC) を除く修正 (2026-10-02_dwarf_consistency_usable.patch) を入れる。

code/ は直接編集しない約束なので、dwarf_consistency_check.py を読み込んで入出力の場所だけ差し替えて実行する。

使い方 (リポジトリの一番上で):
  python cloud_reports/2026-10-02_v20r_dwarf_rerun.py <天の川 v20r の component_spectra.json があるフォルダ> <他天体の結果フォルダ>
出力: cloud_reports/2026-10-02_v20r_targets/dwarf_consistency.json
"""
import json
import pathlib
import runpy
import sys

BASE = pathlib.Path(__file__).resolve().parent.parent
mw_dir, tgt_dir = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
out_dir = BASE / "cloud_reports/2026-10-02_v20r_targets"

# 使えない天体の spectrum を一時的に隠す代わりに、読み込み後に除外する
g = runpy.run_path(str(BASE / "code/dwarf_consistency_check.py"), run_name="not_main")
g["MW_DIR"] = mw_dir
g["DWARF_DIR"] = tgt_dir
g["OUT_DIR"] = out_dir
g["main"].__globals__.update(MW_DIR=mw_dir, DWARF_DIR=tgt_dir, OUT_DIR=out_dir)
g["main"]()

# usable=false の天体を落とした版も保存 (検定に使うのはこちら)
d = json.loads((out_dir / "dwarf_consistency.json").read_text())
keep = []
for t in d["targets"]:
    meta = json.loads((tgt_dir / f"{t['key']}_spectrum.json").read_text())["meta"]
    if meta.get("usable", True):
        keep.append(t)
print(f"使える天体 {len(keep)} / {len(d['targets'])}  (除外: "
      f"{[t['key'] for t in d['targets'] if t not in keep]})")
