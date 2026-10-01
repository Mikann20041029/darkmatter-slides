"""
【答えコード】スライド10「ICSスペクトルの不自然な変形」の作り方

前提となる考え方:
  ICS(逆コンプトン散乱)という成分は、宇宙線の電子が星の光やCMB(宇宙背景放射)の
  光子を弾き飛ばして高エネルギーにする現象で、そのエネルギースペクトルは
  物理的になめらかな形になるはずです(急に落ちて急に戻る、といったギザギザには
  ならない)。このグラフは「ハローという成分を仲間に入れてフィットした場合」と
  「ハロー無しでフィットした場合」で、ICSのスペクトル形状がどう変わるかを
  比較しています。ハロー入りの方だけ不自然なV字(急落→反発)になっていれば、
  「ハローというツマミが、本当はICSの一部であるはずの何かを奪ってしまっている」
  可能性が高い、という意味になります。
"""

import json
import numpy as np  # 数値計算(対数を取る、配列の割り算など)をするための道具
import matplotlib.pyplot as plt

from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
plt.rcParams["font.family"] = "Noto Sans CJK JP"

JSON_PATH = "results/mcmc_allbins_gasICS_v1/iter004_ics_naturalness_check.json"

with open(JSON_PATH) as f:
    d = json.load(f)

energy       = d["e_center_gev"]                    # 13個のエネルギー点
sed_with     = d["sed_with_halo_MeVcm2sSr"]          # ハロー有りの時のICSスペクトル(13点)
sed_without  = d["sed_no_halo_MeVcm2sSr"]            # ハロー無しの時のICSスペクトル(13点)
slope_with   = d["local_powerlaw_index_with_halo"]   # 隣り合う点同士の傾き(12点、13点より1つ少ない)
slope_without= d["local_powerlaw_index_no_halo"]     # 同上、ハロー無し版

# 「隣り合う2点の傾き」は、2点の"間"の値なので、x軸には
# 「隣り合う2つのエネルギーの幾何平均(掛け算してルート)」を使います。
# 例: 1.51 GeVと2.55 GeVの間の傾きなら、x = sqrt(1.51 * 2.55)
energy_midpoints = [
    float(np.sqrt(energy[i] * energy[i + 1]))
    for i in range(len(energy) - 1)
]

fig, axes = plt.subplots(2, 1, figsize=(9, 9), sharex=True)
for ax in axes:
    ax.set_xscale("log")
# 【2026-07-16 方針】濃紺背景・凝った配色はやめ、初期設定+最低限の色分けのみ。

# --- 上段: SED(E^2 dN/dE)そのものの比較。桁が大きく変わるので縦軸も対数 ---
axes[0].set_yscale("log")
axes[0].plot(energy, sed_with, "o-", label="with-halo (ハロー有り)")
axes[0].plot(energy, sed_without, "s--", label="no-halo (ハロー無し)")
axes[0].set_ylabel(r"ICS SED: $E^2 dN/dE$" "\n" r"[MeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]")
axes[0].set_title("ICSスペクトル自然性チェック: with-halo vs no-halo")
axes[0].legend()

# --- 下段: 局所的な傾き(べき指数)。急激に折れ曲がっていないかを見る ---
axes[1].plot(energy_midpoints, slope_with, "o-", label="with-halo")
axes[1].plot(energy_midpoints, slope_without, "s--", label="no-halo")
axes[1].axhline(0, color="gray", ls=":")
axes[1].set_ylabel("局所 d(log SED)/d(log E)")
axes[1].set_xlabel("Energy [GeV]")
axes[1].legend()

fig.tight_layout()
fig.savefig("interim/my_code/03_ics_naturalness/my_ics_sed_comparison.png",
            dpi=130)
plt.close()
print("完成: interim/my_code/03_ics_naturalness/my_ics_sed_comparison.png")
