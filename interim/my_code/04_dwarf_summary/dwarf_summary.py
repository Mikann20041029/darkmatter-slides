"""
スライド9「矮小銀河5天体 — 20.76 GeV過剰の有意性」

★これは完成済みの、そのまま動くコードです★
まず何も変えずに1回実行してください:

  cd /home/arsei/univ/nakamura-darkmatter
  /tmp/darkmatter_venv/bin/python3 interim/my_code/04_dwarf_summary/dwarf_summary.py

そのあと「🔧 ここを変えてみよう」の場所を書き換えて再実行し、見比べてください。

このグラフは棒グラフ(bar chart)です。5天体それぞれについて、
Bin6(20.76 GeV)での有意度(σ)を1本の棒として並べます。
"""

import json
import matplotlib.pyplot as plt

from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
plt.rcParams["font.family"] = "Noto Sans CJK JP"

JSON_PATH = "results/dwarf_pipeline_results.json"

with open(JSON_PATH) as f:
    d = json.load(f)

BIN6_INDEX = 5  # 0番から数えて6番目 = Bin6(20.76 GeV)。13ビン中央付近。
# 🔧 ここを変えてみよう: BIN6_INDEXを0(Bin1)や12(Bin13)に変えると、
#    別のエネルギービンでの有意度に切り替わります。

# d["targets"] は「天体名 → その天体の結果」という辞書(dict)です。
# 辞書は {キー: 値, キー: 値, ...} という形で、リストと違って
# 「名前」で中身を取り出せます（targets["draco"] のように）。
targets = d["targets"]

names  = []  # 表示用の名前(ラベル)
values = []  # 棒の高さ(Bin6での有意度)

# 辞書の中身を1個ずつ取り出すには .items() を使います。
# name には天体のキー名(例:"draco")、info にはその中身の辞書が入ります。
for name, info in targets.items():
    names.append(info["label"])              # 例: "Draco dSph"
    values.append(info["sigma_lima"][BIN6_INDEX])  # 13個のリストからBin6だけ取り出す

# 棒の色を「2σを超えているかどうか」で変える(赤=注目、青=通常)。
colors = ["red" if abs(v) > 2 else "blue" for v in values]
# 🔧 ここを変えてみよう: "red"/"blue" を "orange"/"green" などに変えると
#    色が変わります。matplotlibが分かる色名なら何でも使えます。

fig, ax = plt.subplots(figsize=(9, 6))

bars = ax.bar(names, values, color=colors)

# 棒の上(または下)に、数値を文字として書き添える
for bar, v in zip(bars, values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,  # 文字のx位置=棒の中心
        v + (0.1 if v >= 0 else -0.25),      # 文字のy位置=棒の先端の少し外側
        f"{v:+.2f}σ",                        # 表示する文字列(符号付き, 小数点2桁)
        ha="center", fontsize=11,
    )

ax.axhline(0, color="black", lw=0.8)
ax.axhline(2, color="gray", ls="--", lw=1, label="2σ 目安")
ax.axhline(-2, color="gray", ls="--", lw=1)
ax.set_ylabel("Bin6 (20.76 GeV) Li & Ma 有意性 σ")
ax.set_title("矮小銀河5天体 — 20.76 GeV 過剰の有意性 (Li & Ma 1983 正式式, 780週)")
ax.legend()

fig.tight_layout()
fig.savefig("interim/my_code/04_dwarf_summary/my_dwarf_summary_bin6.png",
            dpi=130)
plt.close()
print("完成: interim/my_code/04_dwarf_summary/my_dwarf_summary_bin6.png")
