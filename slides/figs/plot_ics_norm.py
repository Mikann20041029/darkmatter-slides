# ICS の倍率 (GALPROP の予測の何倍か) を、ハローなし / ありの当てはめで比べる図
# 値は Totani (2025) §2.2 と同じ定義の「最良値」(MCMC で踏んだ点のうち尤度が最大の点) を使う
# 実行: python slides/figs/plot_ics_norm.py <結果フォルダ (mcmc_binNN.json がある所)> <出力 png>
import glob
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = ["Noto Sans CJK JP", "DejaVu Sans"]
res, out = sys.argv[1], sys.argv[2]
J = [json.load(open(f)) for f in sorted(glob.glob(res + "/mcmc_bin*.json"))]
E = np.array([j["e_center_gev"] for j in J])
key = "best" if "best" in J[0]["params"]["f_ics"] else "median"
ics_with = np.array([j["params"]["f_ics"][key] for j in J])          # ハローありの最良値
ics_without = np.array([j["params_no_halo_pointest"]["f_ics"] for j in J])  # ハローなしの最良値

n = 12  # 814 GeV は光子が数個で不安定なので外す
fig, ax = plt.subplots(figsize=(6.4, 4.4), dpi=150)
ax.plot(E[:n], ics_without[:n], "o--", color="k", label="ハローなしで当てはめ")
ax.plot(E[:n], ics_with[:n], "s-", color="k", label="ハローありで当てはめ")
ax.axhline(1.0, color="0.6", lw=0.8)
ax.set_xscale("log")
ax.set_xlabel("エネルギー [GeV]", fontsize=12)
ax.set_ylabel("ICS の明るさ (GALPROP の何倍か)", fontsize=12)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.legend(frameon=False, fontsize=10)
fig.tight_layout()
fig.savefig(out)
for e, a, b in zip(E[:n], ics_without[:n], ics_with[:n]):
    print(f"{e:7.1f} GeV  ハローなし {a:.3f}  あり {b:.3f}")
