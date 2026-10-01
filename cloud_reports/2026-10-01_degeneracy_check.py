# ICS とハローの縮退を、手元の結果ファイルだけで調べるスクリプト
# 入力: results/mcmc_allbins_gasICS_v20_constructsplit/halo_spectrum.json, component_spectra.json (v20 の出力)
# 出力: 表 (画面) と cloud_reports/2026-10-01_fig_ics_norm_vs_energy.png
# 本体の解析コードやイベントデータは使わない (結果 JSON を読むだけ)

import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
halo = json.load(open(ROOT / "results/mcmc_allbins_gasICS_v20_constructsplit/halo_spectrum.json"))
comp = json.load(open(ROOT / "results/mcmc_allbins_gasICS_v20_constructsplit/component_spectra.json"))

E = np.array(comp["energies_gev"])          # 13 ビンの中心エネルギー [GeV]
e2 = comp["e2dnde"]                          # ROI 平均の E^2 dN/dE (ハロー入りフィット)

# --- 1. ハローの有り無しで ICS の倍率 f_ics がどう変わるか ---
# params_no_halo_pointest = ハロー無しフィットの最尤値
# params[...]["median"]  = ハロー入りフィット (MCMC) の中央値
f_ics_noH = np.array([b["params_no_halo_pointest"]["f_ics"] for b in halo["bins"]])
f_ics_H = np.array([b["params"]["f_ics"]["median"] for b in halo["bins"]])
sig = np.array([b["significance_sigma"] for b in halo["bins"]])

# --- 2. ハローを入れたとき ICS から減った光と、ハローの光を比べる ---
# e2["ics"] は f_ics_H 倍済みなので、f_ics=1 あたりの明るさに戻してから差をとる
ics_unit = np.array(e2["ics"]) / f_ics_H
d_ics = (f_ics_noH - f_ics_H) * ics_unit     # ハローを入れて ICS から減った分
halo_flux = np.array(e2["halo"])

print(f"{'E[GeV]':>7} {'σ':>6} {'f_ics(ハロー無)':>14} {'f_ics(ハロー有)':>14} {'ICSの減少/ハロー':>16}")
for i in range(len(E)):
    ratio = d_ics[i] / halo_flux[i] if halo_flux[i] != 0 else float("nan")
    print(f"{E[i]:>7.2f} {sig[i]:>6.2f} {f_ics_noH[i]:>14.3f} {f_ics_H[i]:>14.3f} {ratio:>16.2f}")
# 注意: 倍率を自由にした Poisson 最尤法では「モデルの合計カウント = データの合計」になるので、
# ハローを入れると必ずどこかの成分が同じだけ減る。意味があるのは「どの成分が減ったか」で、
# ここでは ICS がハローの 8〜10 割を肩代わりしている (ガス・バブルはそれぞれ 1 割程度)。

# --- 3. ハロー (NFW ρ²) の緯度方向の形 ---
# 本体 nfw_j_map と同じ設定: 太陽距離 8 kpc、r_s = 21 kpc、視線 0.01〜60 kpc を 150 分割
D_SUN, R_S = 8.0, 21.0
s = np.linspace(0.01, 60, 150)

def j_nfw(l_deg, b_deg):
    """方向 (l, b) の J (ρ_s=1 単位)。密度の2乗を視線方向に積分する"""
    cos_psi = np.cos(np.radians(l_deg)) * np.cos(np.radians(b_deg))
    r = np.sqrt(D_SUN**2 + s[:, None]**2 - 2 * D_SUN * s[:, None] * cos_psi[None, :])
    x = r / R_S
    rho = 1.0 / (x * (1 + x) ** 2)
    return np.trapezoid(rho**2, s, axis=0)

L = np.arange(-59.75, 60, 0.5)               # ROI の経度 |l| <= 60
def lat_profile(b):                          # 経度方向に平均した J
    return j_nfw(L, np.full_like(L, b)).mean()

drop_halo = lat_profile(25) / lat_profile(55)
drop_halo_l0 = (j_nfw(np.array([0.0]), np.array([25.0])) / j_nfw(np.array([0.0]), np.array([55.0])))[0]
print()
print("|b| = 25° → 55° で何倍暗くなるか")
print(f"  ハロー (経度平均): {drop_halo:.2f} 倍 / ハロー (l=0 のみ): {drop_halo_l0:.2f} 倍")
print("  ICS (results/figures_interim2026/fig_ics_latitude_profile_vs_totani.png より): 星の光 2.75 / 赤外 2.62 / CMB 2.07 倍")
print("  等方成分: 1.00 倍")

# --- 4. 図: ICS の倍率をエネルギーごとに並べる (白黒) ---
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(E[:12], f_ics_noH[:12], "o--", color="black", label="without halo")   # 814 GeV は光子が少なく不安定なので外す
ax.plot(E[:12], f_ics_H[:12], "s-", color="black", label="with halo")
ax.axhline(1.0, color="gray", linewidth=1)                                   # GALPROP の予測そのまま = 1
ax.set_xscale("log")
ax.set_xlabel("energy [GeV]", fontsize=12)
ax.set_ylabel(r"ICS normalization $f_{\rm ics}$", fontsize=12)
ax.set_ylim(0, 3)
ax.legend(frameon=False, fontsize=11)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
out = ROOT / "cloud_reports/2026-10-01_fig_ics_norm_vs_energy.png"
fig.savefig(out, dpi=200)
print(f"\nsaved {out.relative_to(ROOT)}")
