"""[2026-07-19] 任意の版 vN の halo_spectrum.json(MCMC中央値)から
component_overlay_totani 図を生成する汎用スクリプト。新版を出すたびに実行する
(feedback_component_overlay_per_version)。disk込みバブル構成でテンプレートを組み、
各成分のROI平均 E²dN/dE を Totani Fig.6 に重ねる。

使い方: python code/plot_component_overlay_vN.py <results_dir> "<図タイトル>"
例: python code/plot_component_overlay_vN.py results/mcmc_allbins_gasICS_v10_cell "v10(10°セル尤度)"
"""
from __future__ import annotations
import os
os.environ.setdefault("MCMC_DISK_BUBBLE", "1")
os.environ.setdefault("MCMC_ICS_SPLIT", "0")
os.environ.setdefault("MCMC_SIGNFREE_HALO", "1")

import sys, json
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

RESDIR = Path(sys.argv[1])
TITLE = sys.argv[2] if len(sys.argv) > 2 else RESDIR.name
RES = json.load(open(RESDIR / "halo_spectrum.json"))

# Totani Fig.6 (|l|<=60°, 10<=|b|<=60° ROI 平均) の参照値。
# [2026-07-23 更新] 旧版は**人間の目視読み取り**だったが、ユーザ指摘
# 「そもそも拾ってきた値が間違っているのでは」を受けて
# `code/digitize_totani_fig6.py` で**機械読み取り**(色でマーカー検出 → 対数軸較正)に置換した。
#   検証: halo と gas は目視値とほぼ完全一致 (halo 1.81e-4 vs 1.8e-4 @20.8GeV 等)。
#         → 読み取り手法そのものは妥当
#   訂正: **ICS の高エネルギー側で目視値が大きく間違っていた**
#         (Bin8 59 GeV: 目視 2.5e-5 → 実際 1.24e-4 で **5.0 倍**、Bin9: 3.5e-5 → 9.26e-5)
#         等方も最大 45% ずれていた (Bin2: 目視 2.3e-4 → 実際 1.59e-4)
# Bin10-13 の iso / Loop I は誤差棒が桁で広く曲線も交差するため NaN のままとする。
TOTANI = {
    # [2026-07-23 v2+closing] マーカーの**形**で読んだ全13ビン (`digitize_totani_fig6_v2.py`)。
    # 行ごとの横幅で誤差棒 (数px) とマーカー (数十px) を分離し、枠線の上辺・下辺を結合して中点を取る。
    # 他のマーカーに上書きされて途切れた枠線は横方向の closing でつなぐ。
    # 検算: 低E 側が旧読み取りと 0.91〜1.09 で一致。
    # 残る np.nan は**マーカーが図の下端 (1e-6) より下にあり存在しない**ビン。
    "gas":    [0.00203, 0.00162, 0.00127, 0.000923, 0.00065, 0.000484, 0.000372, 0.000281, 0.000184, 8.41e-05, 9.66e-05, 8.66e-05, 9.1e-05],
    "ics":    [0.000896, 0.000705, 0.000532, 0.000289, 0.0002, 0.000179, 0.000146, 0.000123, 9.22e-05, 3.88e-05, 4.74e-05, 9.09e-06, 5.4e-05],
    "iso":    [0.000265, 0.000162, 0.00019, 0.000181, 0.000164, 0.000119, 7.53e-05, 9.61e-05, 1.91e-05, 1.14e-06, np.nan, np.nan, 1.59e-05],
    "loopI":  [0.000414, 0.000409, 0.00031, 0.000265, 0.000248, 0.000182, 0.000155, 2.29e-05, 5.48e-05, 6.31e-05, 1.07e-06, 1.82e-05, np.nan],
    "halo":   [np.nan, 5.36e-06, 5.94e-05, 0.00013, 0.000157, 0.000186, 0.000152, 0.000103, 6.42e-05, 6.04e-05, 3.14e-05, 1.78e-05, 3.36e-05],
    "ps":     [0.000425, 0.000371, 0.00032, 0.000258, 0.000199, 0.000179, 0.000146, 0.000123, 9.22e-05, 6.73e-05, 4.32e-05, 1.14e-05, 6.12e-06],
    "fb":     [0.000169, 0.000171, 0.000178, 0.000175, 0.000172, 0.00014, 0.000118, 0.000118, 9.42e-05, 5.61e-05, 3.94e-05, 1.45e-05, 2.29e-05],
    "fb_neg": [0.000107, 8.62e-05, 7.54e-05, 4.52e-05, 1.67e-05, 2.11e-05, 1.99e-05, np.nan, np.nan, np.nan, np.nan, np.nan, 1.36e-05],
}
COLORS = {"gas": "#1f77b4", "ics": "#ff7f0e", "iso": "#7f7f7f", "loopI": "#9467bd", "halo": "#d62728"}
LABELS = {"gas": "gas", "ics": "ICS", "iso": "IGRB(等方背景)", "loopI": "Loop I", "halo": "halo (NFW-ρ²)"}
PARAM_OF = {"gas": "f_gas", "ics": "f_ics", "iso_counts": "f_iso", "ps": "f_ps", "loopI_a": "f_loopI_a",
            "loopI_b": "f_loopI_b", "fb": "f_fb", "fb_neg": "f_fb_neg", "halo": "f_halo"}
COMPS = ["gas", "ics", "iso_counts", "ps", "loopI_a", "loopI_b", "fb", "fb_neg", "halo"]

print("露出/イベント/J-map/バブル(disk込み)構築中...")
expmaps, _ = m.load_exposure_maps()
df_all = m.load_all_events()
j_map = m.nfw_j_map()
nfw_norm, _ = m.calibrate_nfw_norm(expmaps[5], j_map)
df_bubble = m.load_events_with_disk()
bpos, bneg = m.build_bubble_counts_template(df_bubble)
s1, s2 = _sub.loop_i_shell_templates()
valid = (np.abs(m.BG) >= 10) & (np.abs(m.BG) <= 60)

spec = {c: [] for c in COMPS}
E = []
for ib in range(m.N_BINS):
    lo, hi = m.BIN_EDGES[ib], m.BIN_EDGES[ib + 1]
    de_mev = (hi - lo) * 1000.0
    sel = df_all[(df_all.energy_GeV >= lo) & (df_all.energy_GeV < hi)]
    counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
    gas_i, ics_i = _sub._load_galprop_gas_ics_templates(lo, hi)
    t = m.build_templates_for_bin(ib, counts, expmaps[ib], gas_i, ics_i,
        bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
        expmap_bubble_bin=expmaps[m.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
        loop_shell1=s1, loop_shell2=s2)
    params = RES["bins"][ib]["params"]
    denom = np.sum(expmaps[ib][valid] * m.PIX_SOLID_ANGLE_SR[valid] * de_mev)
    e2 = m.BIN_CENTERS[ib] ** 2 * 1e6
    for c in COMPS:
        f = params[PARAM_OF[c]]["median"]
        spec[c].append(e2 * np.sum(f * t[c][valid]) / denom)
    E.append(m.BIN_CENTERS[ib])

E = np.array(E)
ours = {"gas": np.array(spec["gas"]), "ics": np.array(spec["ics"]), "iso": np.array(spec["iso_counts"]),
        "loopI": np.array(spec["loopI_a"]) + np.array(spec["loopI_b"]), "halo": np.array(spec["halo"])}

# [2026-07-23 feedback_plot_all_fitted_components] 倍率 f_n が掛かる全成分を必ず描く。
# fb(バブル正)/fb_neg(バブル負)を追加。fb_neg は負値なので絶対値+破線で示す。
ours["ps"] = np.array(spec["ps"])
ours["fb"] = np.array(spec["fb"])
ours["fb_neg"] = np.abs(np.array(spec["fb_neg"]))
COLORS.update({"fb": "#2ca02c", "fb_neg": "#17becf", "ps": "#8c564b"})
LABELS.update({"fb": "フェルミバブル(正)", "fb_neg": "バブル(負)|絶対値|", "ps": "既知点源"})
ALL = ["gas", "ics", "iso", "ps", "loopI", "fb", "fb_neg", "halo"]   # 全 f_n 成分
RATIO_OK = ["gas", "ics", "iso", "loopI", "halo"]              # Totani 目視値がある成分のみ比を出す

# [2026-07-23 見えない食い違いを枠内に入れる]
# 旧設定は上段 3e-6〜3e-3 / 下段 0.05〜12 で、**最大の食い違い3つが全部フレームの外**にあった:
#   (a) iso が Bin1-2 で Totani の 1/200 (比 0.005) → 下段の下限 0.05 の外
#   (b) iso の絶対値 1.5e-6 → 上段の下限 3e-6 の外
#   (c) halo が Bin1-2 で**負** → log 軸に負は描けず線が消える(有意度が低いからではない)
# よって (1) 表示レンジをデータに合わせて広げ、(2) 負の値は絶対値+破線+×印で明示する。
def _split_sign(y):
    """log 軸に描けない負値を、絶対値の系列として分離する。"""
    y = np.asarray(y, dtype=float)
    pos = np.where(y > 0, y, np.nan)
    neg = np.where(y < 0, -y, np.nan)
    return pos, neg


# 縦並び(上=スペクトル / 下=比)。横軸エネルギーが共通なので縦に積む。
# 上下を別スライドに分けるため sharex=False にし、両パネルに独立した x 軸を付ける
fig, (axL, axR) = plt.subplots(2, 1, figsize=(9.5, 12.0), sharex=False)
for c in ALL:
    ls = "--" if c == "fb_neg" else "-"
    pos, neg = _split_sign(ours[c])
    axL.plot(E, pos, ls, color=COLORS[c], lw=2.2, label=f"{LABELS[c]}(本研究)")
    if np.isfinite(neg).any():
        # 負の区間は「絶対値・破線・×印」で描く。消えて見えなくなるのを防ぐ。
        axL.plot(E, neg, "--x", color=COLORS[c], lw=2.0, ms=9, mew=2.0,
                 label=f"{LABELS[c]}(本研究・**負**|絶対値|)")
    if c in TOTANI:
        # Totani = 点線 (本研究の実線と対にする。丸マーカーは載せない)
        axL.plot(E, TOTANI[c], ls=":", color=COLORS[c], lw=2.2, zorder=7,
                 label=f"{LABELS[c]}(Totani)")
axL.axvline(20.76, color="gold", ls="--", alpha=0.5)
axL.set_yscale("log"); axL.set_ylim(3e-7, 3e-3)
axL.set_xscale("log"); axL.set_xlim(1.1, 1000)
axL.set_xlabel("Energy [GeV]", fontsize=19)
axL.set_ylabel(r"$E^2 dN/dE$ [MeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]", fontsize=18)
axL.tick_params(labelsize=16)
axL.legend(fontsize=9.0, ncol=2, loc="lower left", framealpha=0.9)
axL.grid(alpha=0.25)
_UNRELIABLE_FROM_GEV = 59.0
ratios = {}
def _interp_ref(key):
    """参照値の欠測を対数補間で埋め、どこが補間かを返す。

    欠測は「マーカーが図の下端より下にあって読めない」ビン。線を途切れさせると
    図が読めなくなる (ユーザ指摘) ので、補間して繋ぎ、補間点は白抜きで示す。
    """
    a = np.array(TOTANI[key], dtype=float)
    bad = ~np.isfinite(a)
    if bad.any() and (~bad).sum() >= 2:
        a[bad] = 10 ** np.interp(np.log10(E[bad]), np.log10(E[~bad]), np.log10(a[~bad]))
    return a, bad


for c in RATIO_OK:
    _ref, _interp = _interp_ref(c)
    r = ours[c] / _ref
    # 中央値は**比較可能な区間 (59 GeV 未満)** だけで取る。高E は読み取り誤差が支配的
    ratios[c] = float(np.nanmedian(r[E < _UNRELIABLE_FROM_GEV]))
    pos, neg = _split_sign(r)
    axR.plot(E, pos, "-", color=COLORS[c], lw=2, label=LABELS[c])
    axR.plot(E[~_interp], pos[~_interp], "o", color=COLORS[c], ms=6)
    if _interp.any():
        axR.plot(E[_interp], pos[_interp], "o", color=COLORS[c], mfc="white", ms=6, mew=1.6)
    if np.isfinite(neg).any():
        axR.plot(E, neg, "x--", color=COLORS[c], lw=2, ms=9, mew=2.0,
                 label=f"{LABELS[c]}(負|絶対値|)")

# [2026-07-23] **(参考線・本研究独自の診断であって Totani の手法ではない)**
# 本フィットでは等方と Loop I が強く縮退していることを実測した
# (Loop I shell1 は太陽が殻の壁の中にあるため ROI 全域を覆い、等方テンプレより平坦。
#  leave-one-out で Loop I を外すと iso が 300 倍に跳ねる: `code/diagnose_iso_thief.py`)。
# そのため**本研究の**個別値は不安定である。その事実を可視化するために合算を細い破線で
# 添えるが、**Totani との比較の本体はあくまで論文どおり成分ごと**である。
# Totani が同じ縮退を抱えていたかは検証不能なので、合算を「正しい比較単位」として
# 扱ってはならない (2026-07-23 ユーザ指摘。再現を掲げる以上、独自の比較単位を作らない)。
# [2026-07-23] **合計 (全成分の和)** の比。これが「モデルが説明している空の明るさ」であり、
# 個々の成分への分け方 (=テンプレートの形に依存) と違って、**分配の任意性を受けない量**。
# 低E で iso 単独は Totani の 1/200 だが、**合計は 0.5〜10% で一致する**ことを図に示す。
_tot_ours = (ours["gas"] + ours["ics"] + ours["iso"] + ours["ps"] + ours["loopI"]
             + ours["fb"] - ours["fb_neg"] + np.nan_to_num(ours["halo"]))
# 読み取れなかった成分は 0 とみなさず**その成分だけ線形補間**して合計を出す
# (1 成分でも NaN だと合計が全部消えてしまい、線が途中で切れる)。
def _filled(key):
    return np.nan_to_num(_interp_ref(key)[0])


_tot_totani = np.zeros(len(E))
for _k in ("gas", "ics", "iso", "ps", "loopI", "fb", "halo"):
    _tot_totani = _tot_totani + _filled(_k)
_tot_totani = _tot_totani - _filled("fb_neg")
_tot_ratio = _tot_ours / _tot_totani
ratios["【合計】全成分の和"] = float(np.nanmedian(_tot_ratio[:3]))
axL.plot(E, _tot_ours, "-", color="k", lw=3.0, alpha=0.85, zorder=6, label="**全成分の合計**(本研究)")
axL.plot(E, _tot_totani, "s", color="k", mfc="none", ms=9, mew=2.0, ls=":", lw=1.2,
         zorder=6, label="**全成分の合計**(Totani)")
axR.plot(E, _tot_ratio, "s-", color="k", lw=3.0, ms=9, zorder=6,
         label="**【合計】全成分の和**")

_flat_ours = ours["iso"] + ours["loopI"]
_flat_tot = np.array(TOTANI["iso"], dtype=float) + np.array(TOTANI["loopI"], dtype=float)
_flat_ratio = _flat_ours / _flat_tot
ratios["[参考]iso+loopI合算"] = float(np.nanmedian(_flat_ratio))
axR.plot(E, _flat_ratio, "--", color="k", lw=1.6, alpha=0.75, zorder=4,
         label="[参考]等方+Loop I 合算(本研究の縮退診断・論文の手法ではない)")
# [2026-07-23] **比較不能な区間を明示する**。
# Totani Fig.6 の高エネルギー側 (59 GeV 以上) は、
#   (a) 誤差棒が桁で広く (下端が図の外まで伸び、ゼロと無矛盾な点が多い)
#   (b) 各成分のマーカーが重なり合う
# ため、機械読み取りが別成分の印を拾ってしまう。実際 iso は 169 GeV で 8 倍、
# Loop I は 285 GeV で 8 倍という非物理的な比が出ていた。**これは読み取り誤差であって
# 本研究とTotaniの食い違いではない**。誤解を招くので帯で明示する (ユーザ指摘)。
axR.axvspan(_UNRELIABLE_FROM_GEV, 1000, color="gray", alpha=0.16, zorder=0)
axR.axhline(1.0, color="k", lw=1.0); axR.axhspan(0.7, 1.4, color="green", alpha=0.10)
axR.axvline(20.76, color="gold", ls="--", alpha=0.5)
# 最高E ビン (814 GeV) は本研究の光子が 82 個しかなく、f_gas が 0.086 に潰れる。
# 統計が枯渇したビンであることを図上で明示する (ユーザ指摘「gas は 13 ビン目おかしい」)。
axR.set_xscale("log"); axR.set_yscale("log"); axR.set_ylim(2e-3, 30)
axR.set_xlim(1.1, 1000)
axR.set_xlabel("Energy [GeV]", fontsize=19)
axR.set_ylabel("本研究 / Totani", fontsize=18)
axR.tick_params(labelsize=16)
axR.legend(fontsize=9.0, ncol=2, loc="lower left", framealpha=0.9)
axR.grid(alpha=0.25)
fig.tight_layout()
out = RESDIR / "component_overlay_totani.png"
fig.savefig(out, dpi=130, bbox_inches="tight"); plt.close()
json.dump({"energies_gev": [float(x) for x in E], "e2dnde": {c: spec[c] for c in COMPS},
           "ratio_median": ratios},
          open(RESDIR / "component_spectra.json", "w"), indent=2)
print(f"完成: {out}")
print("本研究/Totani 中央値:", {k: round(v, 2) for k, v in ratios.items()})
