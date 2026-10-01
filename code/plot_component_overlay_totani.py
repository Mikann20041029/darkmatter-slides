"""[2026-07-18] うちのv8(disk込みバブル)成分スペクトル(全13ビン)にTotani (2025) Fig.6を重ねた比較図。
[注記 2026-07-18] 入力は results/mcmc_allbins_gasICS_v8_diskbubble/component_spectra.json(=v8データ)。
新しい版 vN を出すたびに、このオーバーレイ図を該当 vN ディレクトリで再生成すること(教授説明用の定番図)。

目的: Bin6単独ではなく全エネルギー帯で、各成分(gas/ICS/iso/Loop I/halo)がTotaniと
どうズレるかを一望する。gas/ICSは一致し、iso/haloが過大・Loop Iが過小である
「なめらか成分の割り振り崩れ」が全ビンでどう出るかを診断する。

Totaniの値は Fig.6(NFW-ρ²、|l|<=60°, 10°<=|b|<=60°)からの目視読み取り(±30%程度)。
出典を図の目盛りに合わせて1桁精度で記録した近似値であり、厳密なデジタイズではない。
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
OURS = json.load(open(BASE / "results/mcmc_allbins_gasICS_v8_diskbubble/component_spectra.json"))
E = np.array(OURS["energies_gev"])
S = OURS["e2dnde"]
ours_loopI = np.array(S["loopI_a"]) + np.array(S["loopI_b"])

# --- Totani Fig.6 目視読み取り値(E²dN/dE, MeV cm⁻²s⁻¹sr⁻¹)。±30%程度の近似 ---
# エネルギー: 1.51 2.55 4.31 7.28 12.29 20.76 35.06 59.22 100 169 285 482 814 GeV
TOTANI = {
    "gas":   [2.1e-3, 1.6e-3, 1.2e-3, 9.5e-4, 6.5e-4, 5.0e-4, 3.8e-4, 2.8e-4, 1.9e-4, 1.0e-4, 9e-5, 9e-5, 6e-5],
    "ics":   [9.0e-4, 7.0e-4, 5.5e-4, 3.5e-4, 2.0e-4, 1.3e-4, 1.0e-4, 2.5e-5, 3.5e-5, 3.0e-5, 1.5e-5, 5e-6, 6e-5],
    "iso":   [3.0e-4, 2.3e-4, 1.9e-4, 1.6e-4, 1.3e-4, 1.0e-4, 8.0e-5, 8.0e-5, 3.0e-5, np.nan, np.nan, np.nan, np.nan],
    "loopI": [4.5e-4, 4.0e-4, 3.5e-4, 3.3e-4, 2.0e-4, 1.4e-4, 1.3e-4, 2.0e-5, np.nan, np.nan, np.nan, np.nan, np.nan],
    "halo":  [np.nan, 5.0e-6, 6.0e-5, 1.3e-4, 1.7e-4, 1.8e-4, 1.5e-4, 1.05e-4, 7.0e-5, 6.0e-5, 3.0e-5, 1.8e-5, 3.0e-5],
}
OURS_MAP = {"gas": np.array(S["gas"]), "ics": np.array(S["ics"]),
            "iso": np.array(S["iso_counts"]), "loopI": ours_loopI, "halo": np.array(S["halo"])}
COLORS = {"gas": "#1f77b4", "ics": "#ff7f0e", "iso": "#7f7f7f", "loopI": "#9467bd", "halo": "#d62728"}
LABELS = {"gas": "gas", "ics": "ICS", "iso": "等方(iso)", "loopI": "Loop I", "halo": "halo (NFW-ρ²)"}

fig, (axL, axR) = plt.subplots(1, 2, figsize=(15, 6.5))

# 左: 全成分オーバーレイ(実線=うちv6、○=Totani Fig.6)
for c in ["gas", "ics", "iso", "loopI", "halo"]:
    axL.plot(E, OURS_MAP[c], "-", color=COLORS[c], lw=2.2, label=f"{LABELS[c]}(本研究)")
    axL.plot(E, TOTANI[c], "o", color=COLORS[c], mfc="none", ms=8, mew=1.8,
             ls=":", lw=1.0, label=f"{LABELS[c]}(Totani)")
axL.axvline(20.76, color="gold", ls="--", alpha=0.5)
axL.set_xscale("log"); axL.set_yscale("log")
axL.set_ylim(3e-6, 3e-3)
axL.set_xlabel("Energy [GeV]"); axL.set_ylabel(r"$E^2 dN/dE$ [MeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]")
axL.set_title("全成分: 本研究(実線) vs Totani Fig.6(○, 目視±30%)")
axL.legend(fontsize=7.5, ncol=2, loc="lower left")

# 右: 比(本研究/Totani)。1.0からの乖離が「割り振り崩れ」の大きさ
for c in ["gas", "ics", "iso", "loopI", "halo"]:
    ratio = OURS_MAP[c] / np.array(TOTANI[c])
    axR.plot(E, ratio, "o-", color=COLORS[c], lw=2, ms=6, label=LABELS[c])
axR.axhline(1.0, color="k", ls="-", lw=1.0)
axR.axhspan(0.7, 1.4, color="green", alpha=0.10)  # ±40%を一致帯とみなす目安
axR.axvline(20.76, color="gold", ls="--", alpha=0.5)
axR.set_xscale("log"); axR.set_yscale("log")
axR.set_ylim(0.1, 10)
axR.set_xlabel("Energy [GeV]"); axR.set_ylabel("本研究 / Totani")
axR.set_title("成分ごとの比(1.0=一致)\ngas/ICSは緑帯内、iso/haloは上振れ、Loop Iは下振れ")
axR.legend(fontsize=9, ncol=2)

fig.suptitle("天の川halo解析 成分スペクトル全13ビン比較(v6 iso自由化, GALPROP baseline)", fontsize=13)
fig.tight_layout(rect=(0, 0, 1, 0.96))
out = BASE / "results/mcmc_allbins_gasICS_v8_diskbubble/component_overlay_totani.png"
fig.savefig(out, dpi=130)
plt.close()
print(f"完成: {out}")

# 比の要約を出力
print("\n各成分 本研究/Totani 比(全ビン中央値, 20 GeV):")
for c in ["gas", "ics", "iso", "loopI", "halo"]:
    r = OURS_MAP[c] / np.array(TOTANI[c])
    print(f"  {LABELS[c]:14s} 中央値={np.nanmedian(r):.2f}  @20GeV={r[5]:.2f}")
