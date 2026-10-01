# スライド6の図: 「本当のばらつき σ」と「解析が仮定する幅 σ_L」を比べるイメージ図
# 正規分布 (ベル型の曲線) を2本描くだけ。論文のデータは使っていない。

import numpy as np                # 数値計算のライブラリ (配列や exp を使う)
import matplotlib.pyplot as plt   # グラフを描くライブラリ

# --- 1. 2つの幅を決める (値はイメージ用。論文の値ではない) ---
sigma_L = 0.6   # 解析ソフトに「誤差はこのくらい」と仮定させる幅 (狭い)
sigma   = 1.1   # J の推定値が実際にばらつく幅 (広い)

# --- 2. 横軸の点を用意する ---
# 横軸 = 「推定した log10 J」と「本当の log10 J」のずれ
# -3 から 3 までを 601 個の点に細かく区切る (点が多いほど曲線がなめらか)
x = np.linspace(-3, 3, 601)

# --- 3. 正規分布の式を関数にする ---
# 平均 0、幅 s の正規分布:  f(x) = exp(-x^2 / (2 s^2)) / (s * sqrt(2π))
# 幅 s が大きいほど、山が低く・すそが広くなる (曲線の下の面積はどちらも 1)
def gauss(x, s):
    return np.exp(-x**2 / (2 * s**2)) / (s * np.sqrt(2 * np.pi))

# --- 4. グラフを描く ---
fig, ax = plt.subplots(figsize=(6, 4))   # 横6インチ×縦4インチの図を1枚作る

# 白黒でも区別できるように、実線と破線で描き分ける
ax.plot(x, gauss(x, sigma_L), color="black", linestyle="-",  linewidth=2.5,
        label=r"assumed width $\sigma_L$ (narrow)")   # r"...$...$" で σ などの記号が書ける
ax.plot(x, gauss(x, sigma),   color="black", linestyle="--", linewidth=2.5,
        label=r"true scatter $\sigma$ (wide)")

# --- 5. 見た目を整える ---
ax.set_xlabel(r"$\log_{10} J_{\rm estimated} - \log_{10} J_{\rm true}$", fontsize=12)
ax.set_ylabel("probability density", fontsize=12)
ax.set_xlim(-3, 3)
ax.set_ylim(0, 0.85)                      # 縦軸は 0 から。上に余白を作って凡例と曲線が重ならないようにする
ax.legend(loc="upper left", frameon=False, fontsize=11)   # 凡例 (左上・枠なし)
ax.spines["top"].set_visible(False)       # 上と右の枠線を消してすっきりさせる
ax.spines["right"].set_visible(False)

# --- 6. 画像として保存する ---
fig.tight_layout()                        # 文字がはみ出さないように余白を自動調整
fig.savefig("fig_sigma_vs_sigmaL.png", dpi=200)   # dpi=200 でスライドでもくっきり
print("saved fig_sigma_vs_sigmaL.png")
