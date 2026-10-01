"""[クラウド・2026-10-02] 中間発表の図「差し引き前 → DM 以外を差し引いた後」(Bin6, 21 GeV) を v20r で作り直す。

元: code/plot_bin6_before_after_v20.py (v20 の MCMC 中央値を使っていた)。
変える点: 倍率 (f_l) を v20r の mcmc_bin06.json (MCMC 中央値) から読む。図の作り方・配色・単位・平滑化は同じ。
  左: 観測された光子の地図をフラックスに直したもの (差し引き前)
  右: 観測 − (ハロー以外の全成分のモデル) = ハローのモデル + 残差 (DM 以外を差し引いた後)

注意: 型紙 (テンプレート) はこの計算機 (クラウド) で作り直している。倍率は本人 PC の v20r の値。
クラウドと本人 PC で型紙がわずかに違う可能性があるので、クラウド自身の最尤値で引いた図も作り、
2 つの図の差を数字で出す。

使い方 (データを復元したチェックアウトで):
  python <この.py> <v20r の結果フォルダ> <出力 png>
"""
import os
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize, TwoSlopeNorm

BASE = Path.cwd()
sys.path.insert(0, str(BASE / "code"))
import plot_bin6_totani_fig11_v20 as f11  # noqa: E402
import mcmc_fit_all_bins as mfb  # noqa: E402
import plot_skymap_all_subtracted as _sub  # noqa: E402

RES = Path(sys.argv[1])
OUT = Path(sys.argv[2])
f11.RESDIR = RES  # 倍率を v20r から読む

_POS_HALF = LinearSegmentedColormap.from_list("totani_pos", f11._TOTANI_CMAP(np.linspace(0.5, 1.0, 256)))
_POS_HALF.set_bad("0.6")


def colorbar(ax, m, ticks, labels):
    cb = ax.figure.colorbar(m, ax=ax, orientation="horizontal", location="top",
                            fraction=0.05, pad=0.02, ticks=ticks)
    cb.ax.set_xticklabels(labels, fontsize=10)
    cb.set_label(r"flux [cm$^{-2}$s$^{-1}$sr$^{-1}$MeV$^{-1}$]", fontsize=10)


def excess_map(d, params):
    mu = mfb._raw_mu(params, d["tmpl"])
    halo = params[mfb.PARAM_NAMES.index("f_halo")] * d["tmpl"]["halo"]
    return f11._smooth_flux((d["counts"] - mu) + halo, d["unit"], d["valid"], d["grey"])


d = f11.build()
obs = f11._smooth_flux(d["counts"], d["unit"], d["valid"], d["grey"])
exc = excess_map(d, d["p_full"])

# 確認: クラウドで作った型紙に対する最尤値で引いた図との差
tm = dict(d["tmpl"])
tm["valid"] = d["valid"]
cc, ct = mfb.cellize_counts_and_templates(d["counts"], tm, d["valid"])  # 本番と同じ 10° セル尤度
nll = lambda p: mfb.neg_log_likelihood_and_grad(p, cc, ct)
from scipy.optimize import minimize  # noqa: E402
bounds = mfb._bounds_with_halo()
res = minimize(nll, np.asarray(d["p_full"], float), jac=True, method="L-BFGS-B", bounds=bounds)
exc_cloud = excess_map(d, list(res.x))
m = d["valid"]
diff = np.nanmax(np.abs(exc - exc_cloud)[m])
print("v20r の倍率 (MCMC 中央値):", dict(zip(mfb.PARAM_NAMES, np.round(d["p_full"], 4))))
print("クラウドの最尤値          :", dict(zip(mfb.PARAM_NAMES, np.round(res.x, 4))))
print(f"右の図の最大の差 |v20r − クラウド最尤| = {diff:.2e} (表示レンジ ±{f11.VLIM:.0e})")

edges = _sub.L_BINS
fig, (axL, axR) = plt.subplots(1, 2, figsize=(14.5, 7.6))
vmax = 9e-12  # 本人の中間発表の図と同じ表示レンジ
mL = axL.pcolormesh(edges, edges, obs.T, cmap=_POS_HALF, norm=Normalize(0.0, vmax), shading="flat", rasterized=True)
axL.text(0.03, 0.955, "21 GeV, before subtraction (observed)", transform=axL.transAxes,
         fontsize=10.5, color="white", family="monospace", weight="bold")
colorbar(axL, mL, [0, vmax / 2, vmax], ["0", r"$4.5\times10^{-12}$", r"$9\times10^{-12}$"])
vlim = f11.VLIM
mR = axR.pcolormesh(edges, edges, exc.T, cmap=f11._TOTANI_CMAP,
                    norm=TwoSlopeNorm(vmin=-vlim, vcenter=0.0, vmax=vlim), shading="flat", rasterized=True)
axR.text(0.03, 0.955, "21 GeV, all except halo subtracted (excess)", transform=axR.transAxes,
         fontsize=10.5, color="white", family="monospace", weight="bold")
colorbar(axR, mR, [-vlim, 0, vlim], [r"$-2\times10^{-12}$", "0", r"$2\times10^{-12}$"])
for ax in (axL, axR):
    ax.set_xlabel("longitude $l$ [deg]", fontsize=11)
    ax.set_ylabel("latitude $b$ [deg]", fontsize=11)
    ax.set_xlim(60, -60)
    ax.set_ylim(-60, 60)
    ax.set_aspect("equal")
fig.tight_layout()
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, dpi=150)
print(f"観測フラックスの 99.5% 点: {np.nanpercentile(obs, 99.5):.2e}  光子数 (有効領域): {int(np.nansum(d['counts'][m]))}")
print("saved", OUT)
