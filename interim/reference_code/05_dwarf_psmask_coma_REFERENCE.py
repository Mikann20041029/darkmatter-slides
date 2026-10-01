"""
【答えコード】スライド9「Coma Berenices: 点源マスク前後の有意性スペクトル」の作り方

Coma Berenicesだけ、他の4天体と違って一見大きな有意度(Bin6で+4σ程度)が
出ていました。理由を調べたところ、ON領域(天体中心から2°以内)に既知の
4FGL点源(=ダークマターと無関係な、既に発見済みの天体)が3個紛れ込んで
いたことが原因でした。この図は「点源を隠す(マスクする)前」と「隠した後」の
有意度スペクトルを重ねて描き、「隠したら消えた」ことを見せるグラフです。
"""

import json
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
plt.rcParams["font.family"] = "Noto Sans CJK JP"

JSON_PATH = "results/dwarf_pipeline_results.json"

with open(JSON_PATH) as f:
    d = json.load(f)

energy = d["bin_centers_GeV"]                       # 13個のエネルギー値
coma = d["targets"]["coma_ber"]

sigma_before = coma["sigma_lima"]                              # マスク前(13個)
sigma_after  = coma["ps_contamination_check"]["sigma_lima_masked"]  # マスク後(13個)

fig, ax = plt.subplots(figsize=(10, 6))

# 棒グラフを2本並べて比較する場合、同じx位置に2本重ねると見えなくなるので、
# 少し左右にずらして描きます。np.arange(13) は [0,1,2,...,12] という配列。
x = np.arange(len(energy))
width = 0.35  # 棒1本分の幅

ax.bar(x - width / 2, sigma_before, width=width, label="マスク前（点源混入あり）")
ax.bar(x + width / 2, sigma_after,  width=width, label="マスク後（点源除去済み）")

ax.axhline(0, color="black", lw=0.8)
ax.axhline(2, color="gray", ls="--", lw=1)
ax.axhline(-2, color="gray", ls="--", lw=1)
ax.axvline(5, color="gray", ls="-", lw=1.2, alpha=0.7)  # Bin6(index=5)の位置に縦線

ax.set_xticks(x)
ax.set_xticklabels([f"{e:.1f}" for e in energy], rotation=45)
ax.set_xlabel("Energy bin center [GeV]")
ax.set_ylabel("Li & Ma 有意性 σ")
ax.set_title("COMA BERENICES — 点源マスク前後の有意性スペクトル")
ax.legend()

fig.tight_layout()
fig.savefig("interim/my_code/05_dwarf_psmask_coma/my_psmask_check_coma_ber.png",
            dpi=130)
plt.close()
print("完成: interim/my_code/05_dwarf_psmask_coma/my_psmask_check_coma_ber.png")
