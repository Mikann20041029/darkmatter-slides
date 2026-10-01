"""
Bin6(20.76 GeV)の「差引前」と「完全差引後」のスカイマップ2枚

★これは完成済みの、そのまま動くコードです★
まず何も変えずに1回実行してください:

  cd /home/arsei/univ/nakamura-darkmatter
  /tmp/darkmatter_venv/bin/python3 interim/my_code/02_bin6_before_after/bin6_before_after.py

そのあと「🔧 ここを変えてみよう」の場所を書き換えて再実行し、見比べてください。

前提となる考え方:
  望遠鏡が見た生のデータ(①差引前)には、点源・ガス・ICS・Loop I・
  フェルミバブル・(あれば)ハローが全部混ざって写り込んでいます。
  そこから分かっている7成分の最良推定値を全部引き算すると(②完全差引後)、
  理想的には「何も残っていない、ノイズだけの模様」になるはずです。
  この2枚を並べて見せることで「何を引いたのか」を視覚的に説明します。

このコードは、重い計算(イベント読み込み・GALPROP読み込み・視線積分)を
一切していません。事前に計算しておいた2次元配列(.npyファイル)を
読み込んで、画像として表示するだけです(重い計算は
results/mcmc_allbins_gasICS_v1/_precompute_bin6_skymaps.py が担当済み)。
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize

from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
plt.rcParams["font.family"] = "Noto Sans CJK JP"

DATA_DIR = "interim/my_code_data"

# np.load()でnumpy配列(.npyファイル)を読み込む。CSVやJSONと違い、
# 数値の2次元配列(行列)をそのまま高速に保存・読み込みできる形式です。
raw_counts = np.load(f"{DATA_DIR}/bin6_raw_counts.npy")     # 差引前(生カウント)
residual   = np.load(f"{DATA_DIR}/bin6_residual.npy")        # 完全差引後(残差)
# 🔧 ここを変えてみよう: print(raw_counts.shape) を1行追加すると、
#    この配列が何行×何列(何ピクセル×何ピクセル)かが分かります。

with open(f"{DATA_DIR}/bin6_extent.json") as f:
    extent_info = json.load(f)

# imshowの extent引数は [左端, 右端, 下端, 上端] の順で軸の範囲を指定する。
# 銀経(l)は伝統的に右に行くほど値が小さくなる向きに描く(天文学の慣習)ので、
# 左端に大きい値・右端に小さい値を入れる。
extent = [extent_info["l_max"], extent_info["l_min"],
          extent_info["b_min"], extent_info["b_max"]]

# 【重要】このプロジェクトの全スカイマップ図で統一して使われている専用カラーマップ
# "totani_div"（シアン→青→黒→赤→黄、0を中心に対称）。他の図と見た目を統一する
# ために、汎用カラーマップ(inferno等)ではなくこれを必ず使う
# (code/mcmc_fit.py:63-68 と同一定義)。
TOTANI_DIV = LinearSegmentedColormap.from_list("totani_div", [
    (0.0, "#00FFFF"), (0.17, "#0000FF"), (0.33, "#000080"),
    (0.45, "#000020"), (0.50, "#000000"), (0.55, "#200000"),
    (0.67, "#800000"), (0.83, "#FF4400"), (0.92, "#FFCC00"),
    (1.0,  "#FFFF00"),
])
# 🔧 ここを変えてみよう: 上のTOTANI_DIVをコメントアウトし、下の行の
#    コメントを外すと、汎用カラーマップ"inferno"に切り替わります。
#    見た目がどう変わるか(そして他のスライドと合わなくなること)を確認できます。
# TOTANI_DIV = "inferno"

# ------------------------------------------------------------
# 2枚並べた図を用意する(1行2列)
# ------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))

# --- 左: 差引前(点源マスク・銀河面除外後、まだ背景モデルは引いていない生カウント) ---
# vmaxはpercentile(99.5%)で決める(外れ値1点に引っ張られて大部分が真っ黒に
# なるのを防ぐ、code/mcmc_fit.pyと同じやり方)
fin0 = raw_counts[np.isfinite(raw_counts)]
vmax0 = float(np.nanpercentile(np.abs(fin0), 99.5))
# 🔧 ここを変えてみよう: "99.5" を "90" にすると、色の振り切れ方が変わります
#    (外れ値をより強く切り捨てるので、中間的な明るさの違いが見やすくなります)
im0 = axes[0].imshow(
    raw_counts.T,        # 配列を転置(.T)するのは、imshowが(縦,横)の順で
                          # 配列を読むのに対し、元データは(横=l, 縦=b)の
                          # 順で作ってあるため、向きを合わせる必要がある
    origin="lower",       # 配列の0行目を「グラフの下」に描く(通常は上なので反転)
    extent=extent,        # 軸の目盛りの範囲
    aspect="auto",
    cmap=TOTANI_DIV,
    norm=Normalize(-vmax0, vmax0),  # 0を中心に対称(このプロジェクトの統一配色規則)
)
axes[0].set_title("① 差引前（点源マスク後・背景モデルは未差引、Bin6）")
axes[0].set_xlabel("銀経 l [deg]")
axes[0].set_ylabel("銀緯 b [deg]")
fig.colorbar(im0, ax=axes[0], label="counts / pixel")

# --- 右: 完全差引後(残差) ---
fin1 = residual[np.isfinite(residual)]
vmax1 = float(np.nanpercentile(np.abs(fin1), 99.5))
im1 = axes[1].imshow(
    residual.T,
    origin="lower",
    extent=extent,
    aspect="auto",
    cmap=TOTANI_DIV,
    norm=Normalize(-vmax1, vmax1),
)
axes[1].set_title("② 完全差引後（残差、Bin6）")
axes[1].set_xlabel("銀経 l [deg]")
axes[1].set_ylabel("銀緯 b [deg]")
fig.colorbar(im1, ax=axes[1], label="残差 counts / pixel")

fig.suptitle("Bin6 (20.76 GeV): 差引前 → 完全差引後", fontsize=14)
# 🔧 ここを変えてみよう: fontsize=14 の数字を変えるとタイトルの文字の大きさが変わります
fig.tight_layout()
fig.savefig("interim/my_code/02_bin6_before_after/my_bin6_before_after.png", dpi=130)
plt.close()
print("完成: interim/my_code/02_bin6_before_after/my_bin6_before_after.png")
