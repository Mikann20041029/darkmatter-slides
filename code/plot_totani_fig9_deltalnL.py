"""[2026-07-18] Totani (2025) Fig.9(haloのΔlnL=有意度の正体)を今の仕様(v6)で再現・比較。
教授指示のTotani図再現の一環。うちのΔlnLスペクトルはTotaniと2層でズレる:
中E(12-169GeV)で約6-8倍(=halo振幅2.4-2.8倍過大の帰結、ΔlnL∝振幅²)、
低E(2.5-7GeV)で13-48倍〜∞(Totaniはhaloゼロなのにうちは巨大=別種の低E破綻)。
Totani Fig.9のNFW-ρ²値は図からの目視読み取り(±20%程度)。"""
import json,numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
plt.rcParams["font.family"]="Noto Sans CJK JP"
d=json.load(open("results/mcmc_allbins_gasICS_v6_isofree/halo_spectrum.json"))
E=[b["e_center_gev"] for b in d["bins"]]
ours=[b["delta_lnL"] for b in d["bins"]]
# Totani Fig.9 NFW-ρ² 目視読み取り
tot=[101,0,22,79,93,101,51,22,7,5,1,0,0]
fig,(a1,a2)=plt.subplots(1,2,figsize=(15,6))
for ax in (a1,a2):
    ax.plot(E,ours,"o-",color="crimson",lw=2.5,ms=7,label="本研究 v6 (GALPROP)")
    ax.plot(E,tot,"s--",color="navy",lw=2,ms=6,mfc="none",label="Totani Fig.9 (NFW-ρ²,目視)")
    ax.axvline(20.76,color="gold",ls="--",alpha=0.6,label="20 GeV(Totaniのピーク)")
    ax.set_xscale("log"); ax.set_xlabel("Energy [GeV]")
    ax.set_ylabel(r"$\Delta\ln L = \ln L - \ln L_{no-halo}$")
    ax.legend(fontsize=9)
a1.set_title("線形: うちは低Eで爆発(ピーク位置が4-7GeV、Totaniは20GeV)")
a2.set_yscale("log"); a2.set_ylim(0.5,2000)
a2.set_title("対数: 高E(≥100GeV)では一致、20GeVで5.7倍、低Eで質的に乖離")
fig.suptitle("Totani Fig.9 再現: haloのΔlnL(=有意度の正体)スペクトル比較",fontsize=13)
fig.tight_layout(rect=(0,0,1,0.95))
fig.savefig("results/mcmc_allbins_gasICS_v6_isofree/repro_fig9_deltalnL.png",dpi=120)
print("完成: results/mcmc_allbins_gasICS_v6_isofree/repro_fig9_deltalnL.png")
print("\nΔlnL比(うち/Totani):")
for e,o,t in zip(E,ours,tot):
    r=o/t if t>0 else float('inf')
    print("  %7.2f GeV: うち=%7.1f Totani=%5.0f 比=%s"%(e,o,t,'%.1f'%r if t>0 else '∞(Totaniゼロ)'))
