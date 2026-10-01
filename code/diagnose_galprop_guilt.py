"""[2026-07-19] 「GALPROPが本当に犯人か」を白黒つける。GALPROPに逃げないための検証。
UltraClean(v11データ)で、halo無しモデル(iso+gas+ICS+LoopI+バブル)を実データにフィットし:
 (1) 高緯度クリーン域(|b|>=30)でgas+ICS+isoだけをフィット→ f_ics が異常値(~2)を要求するか
     (要求するなら、うちのICSテンプレが物理的に過小=うち側の問題。~1ならGALPROP健全)
 (2) 全ROIのhalo無し残差の緯度・経度プロファイル→ 中心過小の場所と量を実測
出力: results/mcmc_allbins_gasICS_v11_ultraclean_hires/diag_galprop_guilt.{png,txt}
"""
from __future__ import annotations
import os
os.environ.setdefault("MCMC_ULTRACLEAN", "1")
os.environ.setdefault("MCMC_PIXEL_DEG", "1.0")
os.environ.setdefault("MCMC_DISK_BUBBLE", "1")
os.environ.setdefault("MCMC_SIGNFREE_HALO", "1")
os.environ.setdefault("MCMC_CELL_LIKELIHOOD", "0")

import sys
import numpy as np
from scipy.optimize import minimize
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
plt.rcParams["font.family"] = "Noto Sans CJK JP"
sys.path.insert(0, "code")
import mcmc_fit_all_bins as m
import plot_skymap_all_subtracted as _sub

OUT = "results/mcmc_allbins_gasICS_v11_ultraclean_hires"
BG, LG = m.BG, m.LG
expmaps, _ = m.load_exposure_maps()
df = m.load_all_events()
j_map = m.nfw_j_map(); nfw_norm, _ = m.calibrate_nfw_norm(expmaps[5], j_map)
dfb = m.load_events_with_disk(); bpos, bneg = m.build_bubble_counts_template(dfb)
s1, s2 = _sub.loop_i_shell_templates()

ib = 5  # Bin6 20.76 GeV
lo, hi = m.BIN_EDGES[ib], m.BIN_EDGES[ib + 1]
sel = df[(df.energy_GeV >= lo) & (df.energy_GeV < hi)]
counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
gas_i, ics_i = _sub._load_galprop_gas_ics_templates(lo, hi)
t = m.build_templates_for_bin(ib, counts, expmaps[ib], gas_i, ics_i,
    bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
    expmap_bubble_bin=expmaps[m.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
    loop_shell1=s1, loop_shell2=s2)
masked, _ = _sub.mask_point_sources(counts.copy())
roi = (~np.isnan(masked)) & (np.abs(BG) >= 10) & (np.abs(BG) <= 60)

def poisson_fit(templ_keys, mask):
    """指定テンプレのみで Poisson MLE(振幅>=0)。mask 内でフィット。返り: 振幅dict, model."""
    T = [t[k] for k in templ_keys]
    c = counts[mask]
    A = np.array([Tk[mask] for Tk in T])  # (nk, npix)
    def nll(f):
        mu = np.maximum(f @ A, 1e-10)
        return -np.sum(c * np.log(mu) - mu)
    x0 = np.full(len(T), 0.5)
    r = minimize(nll, x0, method="L-BFGS-B", bounds=[(0, None)] * len(T))
    return dict(zip(templ_keys, r.x)), r.x

# === (1) 高緯度クリーン域 |b|>=30 で gas+ICS+iso のみ ===
hi_b = roi & (np.abs(BG) >= 30)
f_hi, _ = poisson_fit(["iso_counts", "gas", "ics"], hi_b)
# 中緯度 10<=|b|<30(halo/バブルが効く域)でも
mid_b = roi & (np.abs(BG) >= 10) & (np.abs(BG) < 30)
f_mid, _ = poisson_fit(["iso_counts", "gas", "ics"], mid_b)

# === (2) 全ROIで halo無しフル(iso+gas+ICS+LoopI+バブル正負)フィット→残差 ===
nh_keys = ["iso_counts", "gas", "ics", "loopI_a", "loopI_b", "fb"]
# fb_negは符号自由なので別扱い: まず非負成分、fb_negは線形最小二乗的に許容するため簡易に含める
f_nh, _ = poisson_fit(nh_keys, roi)
model_nh = np.zeros_like(counts)
for k in nh_keys: model_nh += f_nh[k] * t[k]
resid = counts - model_nh

# 緯度プロファイル(残差 / gas / ICS / haloテンプレ)
absb = np.round(np.abs(BG)).astype(int)
babs = np.arange(10, 61)
def latprof(arr):
    return np.array([arr[roi & (absb == b)].mean() if (roi & (absb == b)).sum() else np.nan for b in babs])
rp = latprof(resid)
halo_shape = t["halo"] * (np.nanmax(latprof(resid)) / max(np.nanmax(latprof(t["halo"])), 1e-30))  # スケール合わせ
hp_ = latprof(halo_shape)
# 経度プロファイル(低緯度帯 10<=|b|<20 の残差 中心集中)
band = roi & (np.abs(BG) >= 10) & (np.abs(BG) < 20)
lc = np.round(LG).astype(int)
lax = np.arange(-58, 60, 4)
def lonprof(arr):
    return np.array([arr[band & (lc >= l) & (lc < l + 4)].mean() if (band & (lc >= l) & (lc < l + 4)).sum() else np.nan for l in lax])
rlon = lonprof(resid)

# 残差の総量(中心 |l|<15,10<=|b|<25 の正残差 counts)
cen = roi & (np.abs(LG) < 15) & (np.abs(BG) >= 10) & (np.abs(BG) < 25)
resid_cen = float(resid[cen].sum())
data_cen = float(counts[cen].sum())

lines = []
lines.append("=== (1) gas+ICS+iso のみフィット, 振幅 ===")
lines.append(f"高緯度クリーン域|b|>=30: f_iso={f_hi['iso_counts']:.3f} f_gas={f_hi['gas']:.3f} f_ics={f_hi['ics']:.3f}")
lines.append(f"中緯度      10<=|b|<30: f_iso={f_mid['iso_counts']:.3f} f_gas={f_mid['gas']:.3f} f_ics={f_mid['ics']:.3f}")
lines.append("  → f_ics が高緯度で~1ならICS健全(GALPROP無罪寄り)、~2ならうちのICS過小(うち側)")
lines.append("")
lines.append("=== (2) halo無しフル残差(iso+gas+ICS+LoopI+バブル) ===")
lines.append(f"全ROIフィット振幅: " + " ".join(f"{k}={v:.3f}" for k, v in f_nh.items()))
lines.append(f"中心域(|l|<15,10<=|b|<25) 残差={resid_cen:+.0f} counts / データ={data_cen:.0f} (={100*resid_cen/data_cen:+.1f}%)")
lines.append(f"  → 中心に大きな正残差=GALPROP/バブルが中心を取り残し、haloがそれを吸う")
txt = "\n".join(lines)
print(txt)
open(f"{OUT}/diag_galprop_guilt.txt", "w").write(txt)

# 図
fig, (a1, a2) = plt.subplots(1, 2, figsize=(15, 6))
a1.plot(babs, rp, "o-", color="crimson", label="halo無し残差")
a1.plot(babs, hp_, "s--", color="navy", mfc="none", label="NFW haloテンプレ(スケール合わせ)")
a1.axhline(0, color="gray", lw=0.7); a1.set_xlabel("|b| [deg]"); a1.set_ylabel("平均 counts/pix")
a1.set_title("Bin6 20GeV halo無し残差の緯度プロファイル\n残差がhalo形なら『中心取り残し』"); a1.legend()
a2.plot(lax, rlon, "o-", color="crimson"); a2.axhline(0, color="gray", lw=0.7); a2.axvline(0, color="gold", ls=":")
a2.set_xlabel("l [deg]"); a2.set_ylabel("平均 counts/pix")
a2.set_title("残差の経度プロファイル(10<=|b|<20)\nl=0中心集中=halo/DM的")
fig.suptitle("GALPROP有罪/無罪判定: halo無し残差はどこに出るか(UltraClean)", fontsize=13)
fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig(f"{OUT}/diag_galprop_guilt.png", dpi=120)
print(f"\n完成: {OUT}/diag_galprop_guilt.{{png,txt}}")
