"""[2026-07-19 診断] v12 bin6(20.76 GeV)で ICS-halo 悪性縮退を定量する。

問い: v12 の 18.3σ のうち、どれだけが「haloがICSを食う」縮退の産物か。
方法: v12 と同一構成(UltraClean/0.125°/セル尤度/disk込みバブル/符号自由halo)で
bin6 テンプレートを組み、f_ics を (a)自由 (b)物理規格化に固定 した場合の
no-halo/with-halo MLE を比較する。emcee は使わず点推定 ΔlnL のみ(軽量・C:非増加)。

σ = sqrt(2·ΔlnL)(1 dof, パイプライン本体と同一定義)。
"""
from __future__ import annotations
import os
# --- v12 と同一の環境フラグ(import 前に設定) ---
os.environ["MCMC_ULTRACLEAN"] = "1"
os.environ["MCMC_PIXEL_DEG"] = "0.125"
os.environ["MCMC_DISK_BUBBLE"] = "1"
os.environ["MCMC_CELL_LIKELIHOOD"] = "1"
os.environ["MCMC_SIGNFREE_HALO"] = "1"
os.environ["MCMC_ICS_SPLIT"] = "0"

import sys, json
import numpy as np
sys.path.insert(0, "code")
import mcmc_fit_all_bins as m
import plot_skymap_all_subtracted as _sub

IB = 5  # bin6 (0-indexed)
print(f"PARAM_NAMES = {m.PARAM_NAMES}")
IDX_ICS = m.PARAM_NAMES.index("f_ics")
print(f"f_ics index = {IDX_ICS}, NDIM={m.NDIM}, CELL_MODE={m.CELL_MODE}")

print("露出/イベント/J-map/バブル(disk込み)構築中...")
expmaps, _ = m.load_exposure_maps()
df_all = m.load_all_events()
j_map = m.nfw_j_map()
nfw_norm, _ = m.calibrate_nfw_norm(expmaps[5], j_map)
df_bubble = m.load_events_with_disk()
bpos, bneg = m.build_bubble_counts_template(df_bubble)
s1, s2 = _sub.loop_i_shell_templates()
valid = (np.abs(m.BG) >= 10) & (np.abs(m.BG) <= 60)

lo, hi = m.BIN_EDGES[IB], m.BIN_EDGES[IB + 1]
sel = df_all[(df_all.energy_GeV >= lo) & (df_all.energy_GeV < hi)]
counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
gas_i, ics_i = _sub._load_galprop_gas_ics_templates(lo, hi)
t_pix = m.build_templates_for_bin(
    IB, counts, expmaps[IB], gas_i, ics_i,
    bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
    expmap_bubble_bin=expmaps[m.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
    loop_shell1=s1, loop_shell2=s2)

# v12 はセル尤度。counts/テンプレートを 10°セルに束ねる。
if m.CELL_MODE:
    counts_fit, t = m.cellize_counts_and_templates(counts, t_pix, valid)
else:
    counts_fit, t = counts, t_pix

_nnh = m.NDIM - 1  # no-halo 次元(f_halo は末尾)


def fit(anchor_ics=None):
    """anchor_ics=None なら f_ics 自由。値を渡すとその値に固定。
    戻り: (lnL_nohalo, lnL_halo, params_halo)"""
    # 初期値: テンプレ平均の逆数スケール(パイプライン踏襲の簡易版)
    x0 = np.array([1.0, 1.0, 1.0, 1.0, 0.01, 0.5, -0.2, 1.0])

    b_nh = m._bounds_no_halo()
    b_h = m._bounds_with_halo()
    if anchor_ics is not None:
        b_nh[IDX_ICS] = (anchor_ics, anchor_ics)
        b_h[IDX_ICS] = (anchor_ics, anchor_ics)
        x0 = x0.copy(); x0[IDX_ICS] = anchor_ics

    def nll_nh(p_nh):
        val, grad = m.neg_log_likelihood_and_grad(list(p_nh) + [0.0], counts_fit, t)
        return val, grad[:_nnh]

    def nll_h(p):
        return m.neg_log_likelihood_and_grad(p, counts_fit, t)

    res_nh, _ = m._multistart_minimize(nll_nh, x0[:_nnh], b_nh)
    x0_h = list(res_nh.x) + [x0[-1]]
    res_h, _ = m._multistart_minimize(nll_h, x0_h, b_h)
    return -res_nh.fun, -res_h.fun, res_h.x


def report(label, anchor_ics=None):
    lnL_nh, lnL_h, p = fit(anchor_ics)
    dlnL = lnL_h - lnL_nh
    sig = np.sqrt(max(2 * dlnL, 0.0))
    pd = dict(zip(m.PARAM_NAMES, p))
    print(f"\n=== {label} ===")
    print(f"  ΔlnL={dlnL:8.2f}  σ={sig:6.2f}")
    print(f"  f_iso={pd['f_iso']:.4f} f_gas={pd['f_gas']:.4f} f_ics={pd['f_ics']:.4f} "
          f"f_loopI_a={pd['f_loopI_a']:.4f}")
    print(f"  f_fb={pd['f_fb']:.4f} f_fb_neg={pd['f_fb_neg']:.4f} f_halo={pd['f_halo']:.4f}")
    return dict(label=label, anchor_ics=anchor_ics, dlnL=float(dlnL), sigma=float(sig),
                params={k: float(v) for k, v in pd.items()})


results = []
# (a) 自由(v12 再現、点推定)
results.append(report("(a) f_ics 自由 [v12再現・点推定]"))
# no-halo 時の f_ics を取得(縮退の "halo無し選好")
_, _, _ = fit()  # ensure computed
# (b) f_ics を no-halo 選好値付近に固定して halo を足す → halo が ICS を食えなくする
#     no-halo の f_ics を測る
b_nh = m._bounds_no_halo()
x0 = np.array([1.0, 1.0, 1.0, 1.0, 0.01, 0.5, -0.2])
def nll_nh0(p_nh):
    val, grad = m.neg_log_likelihood_and_grad(list(p_nh) + [0.0], counts_fit, t)
    return val, grad[:_nnh]
res_nh0, _ = m._multistart_minimize(nll_nh0, x0, b_nh)
f_ics_nohalo = res_nh0.x[IDX_ICS]
print(f"\n[no-halo 選好] f_ics = {f_ics_nohalo:.4f}")
results.append(report(f"(b) f_ics={f_ics_nohalo:.3f} 固定 [no-halo選好で固定]", f_ics_nohalo))
# (c) f_ics=1.0 に固定(GALPROP 物理規格化)
results.append(report("(c) f_ics=1.0 固定 [GALPROP物理規格化]", 1.0))
# (d) f_ics=0.65 固定(ROI平均でTotani ICS一致=1.3e-4/2.0e-4)
results.append(report("(d) f_ics=0.65 固定 [ROI平均でTotani ICS一致]", 0.65))

out = "results/mcmc_allbins_gasICS_v12_bubblefix/diag_ics_halo_bin6.json"
json.dump({"bin": 6, "e_center_gev": 20.76, "config": "v12 (UltraClean/0.125/cell/diskbubble)",
           "f_ics_nohalo_preference": float(f_ics_nohalo),
           "note": "sigma = sqrt(2*dlnL), point-estimate MLE (no emcee)",
           "cases": results}, open(out, "w"), indent=2)
print(f"\n保存: {out}")
