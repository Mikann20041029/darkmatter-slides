"""[2026-07-17] 他天体(矮小銀河5+M31)のDM探索まとめ図。
2手法(Totaniテンプレート法=本研究 / ON-OFF Li-Ma法=過去論文標準)の有意度スペクトルを
天体ごとに並べ、いずれも非検出であることを示す。MW halo(20 GeVで有意)との対比も注記。
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
plt.rcParams["font.family"] = "Noto Sans CJK JP"

BASE = Path(__file__).resolve().parent.parent
tmpl = json.load(open(BASE / "results/other_targets_totani/all_targets_spectrum.json"))
onoff = json.load(open(BASE / "results/dwarf_13bins_results.json"))["targets"]
mw = json.load(open(BASE / "results/mcmc_allbins_gasICS_v2_cosb/halo_spectrum.json"))

LABELS = {"draco": "Draco", "sculptor": "Sculptor", "ursa_minor": "Ursa Minor",
          "segue1": "Segue 1", "coma_ber": "Coma Berenices", "m31": "M31 (アンドロメダ)"}
order = ["draco", "sculptor", "ursa_minor", "segue1", "coma_ber", "m31"]

fig, axes = plt.subplots(2, 3, figsize=(15, 8), sharex=True)
axes = axes.ravel()
for i, name in enumerate(order):
    ax = axes[i]
    e = tmpl[name]["e_center_gev"]
    sig_t = tmpl[name]["significance_sigma"]
    ax.plot(e, sig_t, "o-", color="#1f77b4", label="Totaniテンプレート法(本研究)")
    if name in onoff:
        sn = [b["sn"] for b in onoff[name]]
        ax.plot(e, sn, "s--", color="#ff7f0e", alpha=0.8, label="ON-OFF Li-Ma法(過去論文標準)")
    ax.axhspan(-3, 3, color="gray", alpha=0.10)   # 非検出帯(|σ|<3)
    ax.axhline(0, color="gray", ls=":", lw=0.8)
    ax.set_xscale("log")
    ax.set_ylim(-5, 13)
    ax.set_title(LABELS[name], fontsize=12)
    ax.set_ylabel("有意度 [σ]")
    if i >= 3:
        ax.set_xlabel("Energy [GeV]")
    if i == 0:
        ax.legend(fontsize=8, loc="upper left")

# MW halo との対比を図全体の注記に
mw_bin6 = mw["bins"][5]["significance_sigma"]
fig.suptitle(f"矮小銀河5天体・M31: 20 GeV(DMピーク)では全て非検出\n"
             f"低E側の超過(Sculptor/Coma Ber)は点源混入・前景で、DMなら20 GeVでピークするはず — "
             f"対照: 天の川haloは20 GeVで{mw_bin6:.0f}σ",
             fontsize=12)
fig.tight_layout(rect=(0, 0, 1, 0.94))
out = BASE / "results/other_targets_totani/other_targets_summary.png"
fig.savefig(out, dpi=130)
plt.close()
print(f"完成: {out}")
