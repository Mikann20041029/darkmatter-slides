"""[2026-07-18] 案1(判定ルール事前登録): GALPROP中心過小予測が20GeV超過過大の
十分な原因か、を「中心ブースト実験」で決着させる。鼬ごっこ(犯人交代)を断つため、
実行前に判定ルールを固定する。

背景: 今日の診断(diagnose_lowE_midE_v8)で、v8のno-halo残差は銀河中心方向(l≈0)に
集中し、NFW haloがそれを吸って有意度が対Totani 3-11倍過大と判明。一方、成分の
ROI平均スペクトルではgas/ICSはTotani Fig.6と一致(=平均では無罪)。中心だけの
過小予測を平均が隠している可能性を、中心を直接明るくして検証する。

方法: GALPROP gas+ICS テンプレを中心経度ブースト
  boosted = base * (1 + a * exp(-(l/15deg)^2))     a=0,0.1,...,0.5
で明るくし(a=中心での過小予測率、GALPROPのFig.6読み取り不確かさ±30%が目安上限)、
各 a で no-halo/with-halo の点推定(L-BFGS-B, MCMCなし)ΔlnLを再計算し
有意度 sig=sqrt(2*ΔlnL) を追う。f_gas/f_ics は自由振幅なので全体レベルは吸収され、
「中心が周縁より明るい」形の変化のみが halo と競合する。

【事前登録した判定ルール】(Bin6=20.76GeV基準)
  a* = 有意度がTotani帯上限(19σ)以下に初めて入るブースト率。
  - a* <= 0.30 なら: 30%以内(=GALPROP Fig.6の系統不確かさ範囲内)の中心増光で
    Totani帯に収まる → 中心過小予測が超過過大の"十分な原因"。超過振幅は系統誤差支配。
    結論: 主張を頑健域に絞り、系統誤差幅として報告。犯人探しループ終了。
  - a* > 0.30 or a=0.5でも帯に届かない → 中心増光だけでは説明不可。
    戸谷本人のGALPROP出力が必要(外部依存)。到達した幅を報告しループ終了。

出力: results/mcmc_allbins_gasICS_v8_diskbubble/diag_center_boost_scan.{json,png}
"""
from __future__ import annotations
import os
os.environ.setdefault("MCMC_DISK_BUBBLE", "1")
os.environ.setdefault("MCMC_ICS_SPLIT", "0")
os.environ.setdefault("MCMC_CELL_LIKELIHOOD", "0")
os.environ.setdefault("MCMC_SIGNFREE_HALO", "1")  # v8実測フラグに一致

import sys, json, subprocess
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
plt.rcParams["font.family"] = "Noto Sans CJK JP"

sys.path.insert(0, "code")
import mcmc_fit_all_bins as m
import plot_skymap_all_subtracted as _sub

OUT = Path("results/mcmc_allbins_gasICS_v8_diskbubble")
BG, LG = m.BG, m.LG

# 中心経度ブースト窓(l=0で1, |l|=15degで1/e)。GALPROP自身のb形状はそのまま残すため
# 経度のみの窓にする(今日の発見=残差は経度中心集中)。
BOOST_WINDOW = np.exp(-(LG / 15.0) ** 2)
BOOSTS = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
TOTANI_BAND = (13.0, 19.0)     # Totani報告帯
DECISION_A = 0.30              # 事前登録: 30%以内で帯入りなら「中心過小が十分な原因」
SCAN_BINS = [3, 5, 7]          # Bin4(7.3), Bin6(20.8), Bin8(59.2) 0-indexed

print("露出/イベント/J-map/バブル(disk込み)を構築中...")
expmaps, _ = m.load_exposure_maps()
df_all = m.load_all_events()
j_map = m.nfw_j_map()
nfw_norm, _ = m.calibrate_nfw_norm(expmaps[5], j_map)
df_bubble = m.load_events_with_disk()
bpos, bneg = m.build_bubble_counts_template(df_bubble)
s1, s2 = _sub.loop_i_shell_templates()


def point_delta_lnL(counts, templates, x0):
    """fit_one_bin の点推定部分のみ(MCMCなし)。ΔlnL と点推定 params を返す。"""
    _nnh = m.NDIM - 1

    def neg_ll_nohalo(p_nh):
        val, grad = m.neg_log_likelihood_and_grad(list(p_nh) + [0.0], counts, templates)
        return val, grad[:_nnh]
    res_nh, _ = m._multistart_minimize(neg_ll_nohalo, x0[:_nnh], m._bounds_no_halo())
    lnL_noh = -res_nh.fun

    def neg_ll(p):
        return m.neg_log_likelihood_and_grad(p, counts, templates)
    x0_wh = list(res_nh.x) + [x0[_nnh]]
    res, _ = m._multistart_minimize(neg_ll, x0_wh, m._bounds_with_halo())
    lnL_with = -res.fun
    if lnL_with < lnL_noh:
        res_x = np.array(list(res_nh.x) + [0.0]); lnL_with = lnL_noh
    else:
        res_x = res.x
    dl = max(lnL_with - lnL_noh, 0.0)
    return dl, float(np.sqrt(2 * dl)), res_nh.x, res_x


def scan_bin(ib):
    emin, emax = m.BIN_EDGES[ib], m.BIN_EDGES[ib + 1]
    sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
    counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
    gas_i, ics_i = _sub._load_galprop_gas_ics_templates(emin, emax)
    masked, n_masked = _sub.mask_point_sources(counts.copy())
    valid = (~np.isnan(masked)) & (np.abs(BG) >= 10) & (np.abs(BG) <= 60)

    rows = []
    for a in BOOSTS:
        boost = 1.0 + a * BOOST_WINDOW
        t = m.build_templates_for_bin(
            ib, counts, expmaps[ib], gas_i * boost, ics_i * boost,
            bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
            expmap_bubble_bin=expmaps[m.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
            loop_shell1=s1, loop_shell2=s2)
        t["valid"] = valid; t["valid_pixel"] = valid
        c_mean = max(counts[valid].mean(), 1e-6)

        def _x0_for(name):
            if name in ("f_fb", "f_halo"):
                return 0.5
            key = m.PARAM_TO_TEMPLATE_KEY[name]
            tmean = float(t[key][valid].mean())
            if name == "f_fb_neg":
                return 0.3 * c_mean / tmean if tmean > 0 else 0.3
            coef = 0.5 if (name == "f_gas" or name.startswith("f_ics")) else 0.3
            return coef * c_mean / tmean if tmean > 0 else 0.3
        x0 = [_x0_for(n) for n in m.PARAM_NAMES]

        dl, sig, pnh, pwh = point_delta_lnL(counts, t, x0)
        pnh_d = {n: float(v) for n, v in zip(m.PARAM_NAMES[:m.NDIM - 1], pnh)}
        rows.append(dict(a=a, delta_lnL=dl, sig=sig,
                         f_gas=pnh_d["f_gas"], f_ics=pnh_d["f_ics"],
                         f_halo=float(pwh[-1])))
        print(f"  Bin{ib+1} a={a:.1f}: sig={sig:5.1f}σ ΔlnL={dl:7.1f} "
              f"f_gas={pnh_d['f_gas']:.3f} f_ics={pnh_d['f_ics']:.3f} f_halo={pwh[-1]:+.3f}")
    return rows


results = {}
for ib in SCAN_BINS:
    print(f"\n=== Bin{ib+1} ({m.BIN_CENTERS[ib]:.1f} GeV) 中心ブーストscan ===")
    results[f"bin{ib+1}"] = scan_bin(ib)

# --- 判定(Bin6基準) ---
b6 = results["bin6"]
a_star = None
for r in b6:
    if r["sig"] <= TOTANI_BAND[1]:
        a_star = r["a"]; break
if a_star is not None and a_star <= DECISION_A:
    verdict = (f"a*={a_star:.1f} <= {DECISION_A}: 30%以内の中心増光でTotani帯入り。"
               f"→ 中心過小予測が20GeV超過過大の十分な原因。系統誤差支配。主張は頑健域に絞る。")
elif a_star is not None:
    verdict = (f"a*={a_star:.1f} > {DECISION_A}: 帯入りに{a_star*100:.0f}%増光が必要(系統範囲外)。"
               f"→ 中心増光だけでは不足。戸谷実GALPROP出力が必要。")
else:
    verdict = (f"a=0.5でもsig={b6[-1]['sig']:.1f}σ>{TOTANI_BAND[1]}。"
               f"→ 中心増光では説明不可。戸谷実GALPROP出力が必要。到達幅={b6[0]['sig']:.1f}→{b6[-1]['sig']:.1f}σ。")
print("\n【判定】", verdict)

# --- 図 ---
fig, ax = plt.subplots(figsize=(9, 6))
colors = {"bin4": "#1f77b4", "bin6": "#d62728", "bin8": "#2ca02c"}
for key, rows in results.items():
    aa = [r["a"] * 100 for r in rows]; ss = [r["sig"] for r in rows]
    ax.plot(aa, ss, "o-", lw=2.2, ms=7, color=colors[key],
            label=f"{key} ({m.BIN_CENTERS[int(key[3:])-1]:.1f}GeV)")
ax.axhspan(*TOTANI_BAND, color="navy", alpha=0.12, label="Totani報告帯 13-19σ")
ax.axvline(DECISION_A * 100, color="gray", ls="--", alpha=0.7, label=f"判定閾値 {DECISION_A*100:.0f}%")
ax.set_xlabel("中心(l≈0)ブースト率 a [%](=GALPROP中心過小予測の仮定量)")
ax.set_ylabel("halo有意度 [σ]")
ax.set_title("中心ブースト実験: GALPROP中心を明るくすると20GeV halo有意度は落ちるか")
ax.legend(fontsize=9); ax.grid(alpha=0.3)
fig.text(0.5, -0.02, verdict, ha="center", fontsize=8, wrap=True)
fig.tight_layout()
fig.savefig(OUT / "diag_center_boost_scan.png", dpi=130, bbox_inches="tight")
plt.close()

try:
    githash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
except Exception:
    githash = "unknown"
json.dump(dict(generated="2026-07-18", git_hash=githash,
               boost_window="1+a*exp(-(l/15deg)^2)", boosts=BOOSTS,
               totani_band=TOTANI_BAND, decision_threshold_a=DECISION_A,
               a_star=a_star, verdict=verdict, scan=results),
          open(OUT / "diag_center_boost_scan.json", "w"), ensure_ascii=False, indent=2)
print("\n完成: diag_center_boost_scan.{json,png}")
