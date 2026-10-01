import json,numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
plt.rcParams["font.family"]="Noto Sans CJK JP"
v6=json.load(open("results/mcmc_allbins_gasICS_v6_isofree/halo_spectrum.json"))
v8=json.load(open("results/mcmc_allbins_gasICS_v8_diskbubble/halo_spectrum.json"))
E=[b["e_center_gev"] for b in v8["bins"]]
d6=[b["delta_lnL"] for b in v6["bins"]]; d8=[b["delta_lnL"] for b in v8["bins"]]
tot=[101,0,22,79,93,101,51,22,7,5,1,0,0]
fig,(a1,a2)=plt.subplots(1,2,figsize=(15,6))
for ax in (a1,a2):
    ax.plot(E,d6,"o-",color="#d62728",lw=2,ms=6,label="v6(disk無しバブル)",alpha=0.6)
    ax.plot(E,d8,"o-",color="#1f77b4",lw=2.5,ms=7,label="v8(disk込みバブル)")
    ax.plot(E,tot,"s--",color="navy",lw=2,ms=6,mfc="none",label="Totani Fig.9(目視)")
    ax.axvline(20.76,color="gold",ls="--",alpha=0.6)
    ax.set_xscale("log"); ax.set_xlabel("Energy [GeV]")
    ax.set_ylabel(r"$\Delta\ln L$"); ax.legend(fontsize=9)
a1.set_title("線形: v8で低E偽halo(バブル漏れ)が大きく低下")
a2.set_yscale("log"); a2.set_ylim(0.5,1500)
a2.set_title("対数: 全ビンでv6→v8とTotaniへ接近(まだ差は残る)")
fig.suptitle("disk込みバブル構築の効果: haloのΔlnL(=有意度)がTotaniへ接近",fontsize=13)
fig.tight_layout(rect=(0,0,1,0.95))
fig.savefig("results/mcmc_allbins_gasICS_v8_diskbubble/deltalnL_v6_v8_totani.png",dpi=120)
print("完成: results/mcmc_allbins_gasICS_v8_diskbubble/deltalnL_v6_v8_totani.png")
