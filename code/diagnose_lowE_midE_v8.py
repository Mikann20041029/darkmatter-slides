"""[2026-07-18] v8(disk込みバブル=Totani baseline相当)の残差を空間分解し、
(a) 低E形ずれ と (b) mid-E GALPROP緯度形状差 を定量する診断。

背景(v8 vs Totani Fig.9 ΔlnL):
  Bin1 1.5GeV : Totani=101, うち=0.3   (f_halo=-14.5 だが無有意)  → うちが過小
  Bin2 2.5GeV : Totani=0,   うち=121   (f_halo=+110, 15.6σ)       → 巨大な偽halo残存
  Bin3-10     : ΔlnL比 3.2〜11倍(=halo振幅 √比 ≈1.8〜3.3倍過大)  → mid-E系統
  Bin11-13    : 比1〜2でほぼ一致

(a) 低E: Bin1/Bin2 の no-halo 残差を空間分解し、halo が何を吸っているかを特定。
(b) mid-E: no-halo 残差を「緯度のみ」「経度構造のみ」に分解した halo テンプレートと
    相関させ、mid-E の見かけhaloが (i)中心集中したDM的超過 か (ii)緯度一様な
    GALPROP不一致 のどちらかを判定する。

出力: results/mcmc_allbins_gasICS_v8_diskbubble/ に
  diag_lowE_midE_v8.json   (全数値の正本)
  diag_fig9_v8_deltalnL.png (ΔlnL v8 vs Totani)
  diag_lowE_residual_v8.png (Bin1/Bin2 残差)
  diag_midE_latlon_v8.png   (mid-E 緯度/経度プロファイル分解)
"""
from __future__ import annotations
import os
# v8 = disk込みバブル。import 前に必ず立てる(モジュールが import 時に env を読む)。
os.environ.setdefault("MCMC_DISK_BUBBLE", "1")
# v8 実測フラグ(halo_spectrum.json): ICS分割なし / セル束ねなし / f_halo符号自由
# (signfree_idx=[6,7]=f_fb_neg,f_halo; Bin1 の f_halo=-14.5 が符号自由の証拠)。
# 残差再構築は保存済み params を直接使うため符号自由/非負はテンプレ構築に無影響だが、
# 再現性のため v8 と同一フラグに固定する。
os.environ.setdefault("MCMC_ICS_SPLIT", "0")
os.environ.setdefault("MCMC_CELL_LIKELIHOOD", "0")
os.environ.setdefault("MCMC_SIGNFREE_HALO", "1")

import sys, json
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.ndimage import gaussian_filter
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
plt.rcParams["font.family"] = "Noto Sans CJK JP"

sys.path.insert(0, "code")
import mcmc_fit_all_bins as m
import plot_skymap_all_subtracted as _sub

OUT = Path("results/mcmc_allbins_gasICS_v8_diskbubble")
RES = json.load(open(OUT / "halo_spectrum.json"))

# v8 が本当に disk-bubble / 非セル / 非符号自由で走ったか自己検証(再現性)
assert not RES.get("likelihood_cell_mode", False), "v8はセル束ねOFFのはず"
assert RES.get("f_halo_sign_free", False), "v8はf_halo符号自由のはず(signfree_idx=[6,7])"
assert m.DISK_BUBBLE, "MCMC_DISK_BUBBLE=1 が効いていない"

# Totani Fig.9 NFW-ρ² 目視読み取り(±20%、plot_totani_fig9_deltalnL.py と同一)
TOTANI_DLNL = [101, 0, 22, 79, 93, 101, 51, 22, 7, 5, 1, 0, 0]

# --- 共通基盤(main() と同一手順で v8 テンプレートを再構築) ---
print("露出/イベント/J-map/バブル(disk込み)を構築中...")
expmaps, exp_centers = m.load_exposure_maps()
df_all = m.load_all_events()
j_map = m.nfw_j_map()
nfw_norm, _ = m.calibrate_nfw_norm(expmaps[5], j_map)
df_bubble = m.load_events_with_disk()           # disk込み(v8の肝)
bpos, bneg = m.build_bubble_counts_template(df_bubble)
s1, s2 = _sub.loop_i_shell_templates()

BG, LG = m.BG, m.LG
NONHALO_ORDER = ["f_iso", "f_gas", "f_ics", "f_loopI_a", "f_loopI_b", "f_fb", "f_fb_neg"]
NONHALO_KEYS = ["iso_counts", "gas", "ics", "loopI_a", "loopI_b", "fb", "fb_neg"]


def reconstruct(ib: int) -> dict:
    """Bin ib(0-indexed)の v8 テンプレート・no-halo残差・ROIマスクを再構築。"""
    emin, emax = m.BIN_EDGES[ib], m.BIN_EDGES[ib + 1]
    sel = df_all[(df_all.energy_GeV >= emin) & (df_all.energy_GeV < emax)]
    counts, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[_sub.L_BINS, _sub.B_BINS])
    gas_i, ics_i = _sub._load_galprop_gas_ics_templates(emin, emax)
    t = m.build_templates_for_bin(
        ib, counts, expmaps[ib], gas_i, ics_i,
        bubble_counts_bin3_pos=bpos, bubble_counts_bin3_neg=bneg,
        expmap_bubble_bin=expmaps[m.BUBBLE_BIN], j_map=j_map, nfw_norm=nfw_norm,
        loop_shell1=s1, loop_shell2=s2)
    masked, _ = _sub.mask_point_sources(counts.copy())
    roi = (np.abs(BG) >= 10) & (np.abs(BG) <= 60) & ~np.isnan(masked)

    pnh = RES["bins"][ib]["params_no_halo_pointest"]
    mnh = np.zeros_like(counts)
    for pk, tk in zip(NONHALO_ORDER, NONHALO_KEYS):
        mnh += pnh[pk] * t[tk]
    resid = counts - mnh                      # no-halo 残差(データ - halo無しモデル)

    p = RES["bins"][ib]["params"]
    f_halo = p["f_halo"]["median"]
    halo_fit = f_halo * t["halo"]             # フィットされた halo counts
    return dict(ib=ib, e=m.BIN_CENTERS[ib], counts=counts, roi=roi, resid=resid,
                t=t, f_halo=f_halo, halo_fit=halo_fit, halo_tmpl=t["halo"],
                dlnL=RES["bins"][ib]["delta_lnL"], sig=RES["bins"][ib]["significance_sigma"])


def corr(a, b, mask):
    aa, bb = a[mask], b[mask]
    if aa.std() < 1e-12 or bb.std() < 1e-12:
        return 0.0
    return float(np.corrcoef(aa, bb)[0, 1])


# ============================================================
# (a) 低E形ずれ: Bin1/Bin2 の残差を空間分解
# ============================================================
print("\n=== (a) 低E形ずれ (Bin1=1.5GeV, Bin2=2.5GeV) ===")
lowE = {}
for ib in [0, 1]:
    r = reconstruct(ib)
    roi = r["roi"]
    # 残差 vs 各テンプレの空間相関(何を吸っているか)
    cc = {tk: corr(r["resid"], r["t"][tk], roi)
          for tk in ["halo", "gas", "ics", "iso_counts", "loopI_a", "fb", "fb_neg"]}
    # バブル領域(|l|<22, 10<|b|<55)内外の残差合計
    bub = (np.abs(LG) < 22) & (np.abs(BG) >= 10) & (np.abs(BG) < 55) & roi
    out = roi & ~bub
    # 高緯度(|b|>=30)vs 低緯度(10<=|b|<20)の残差平均(緯度勾配)
    hib = roi & (np.abs(BG) >= 30)
    lob = roi & (np.abs(BG) >= 10) & (np.abs(BG) < 20)
    lowE[f"bin{ib+1}"] = dict(
        e=r["e"], f_halo=r["f_halo"], dlnL=r["dlnL"], sig=r["sig"],
        totani_dlnL=TOTANI_DLNL[ib],
        resid_sum_bubble=float(r["resid"][bub].sum()),
        resid_sum_outside=float(r["resid"][out].sum()),
        resid_mean_hib=float(r["resid"][hib].mean()),
        resid_mean_lob=float(r["resid"][lob].mean()),
        corr_resid_template=cc,
    )
    print(f"Bin{ib+1} {r['e']:.2f}GeV: f_halo={r['f_halo']:+.2f} ΔlnL={r['dlnL']:.1f}(Totani={TOTANI_DLNL[ib]}) σ={r['sig']:.1f}")
    print("   残差×テンプレ相関: " + " ".join(f"{k}={v:+.2f}" for k, v in cc.items()))
    print(f"   残差合計 バブル内={r['resid'][bub].sum():+.0f} 外={r['resid'][out].sum():+.0f}"
          f" | 残差平均 |b|<20={r['resid'][lob].mean():+.2f} |b|>=30={r['resid'][hib].mean():+.2f}")

# ============================================================
# (b) mid-E GALPROP緯度形状差: halo を緯度のみ/経度構造のみに分解
# ============================================================
print("\n=== (b) mid-E GALPROP緯度形状差 (Bin3-10) ===")
print("halo テンプレを緯度平均(緯度のみ)と残り(経度構造のみ)に分け、no-halo残差がどちらと相関するか。")
midE = {}
for ib in range(2, 10):
    r = reconstruct(ib)
    roi = r["roi"]
    H = r["halo_tmpl"].copy()
    # halo テンプレを |b| ごとの ROI 平均に置換=「緯度のみ」版(経度構造を消す)
    H_lat = np.zeros_like(H)
    absb = np.round(np.abs(BG)).astype(int)
    for bval in np.unique(absb[roi]):
        sel = roi & (absb == bval)
        H_lat[sel] = H[sel].mean()
    H_lon = H - H_lat                          # 経度構造のみ(中心集中のDM的特徴)
    resid = r["resid"]
    c_full = corr(resid, H, roi)
    c_lat = corr(resid, H_lat, roi)
    c_lon = corr(resid, H_lon, roi)
    # 低緯度帯(10<=|b|<20)での経度コントラスト: 中心(|l|<15) vs 周縁(|l|>30)残差平均
    band = roi & (np.abs(BG) >= 10) & (np.abs(BG) < 20)
    cen = band & (np.abs(LG) < 15)
    per = band & (np.abs(LG) > 30)
    lon_contrast = float(resid[cen].mean() - resid[per].mean())
    # 同じコントラストを halo テンプレで(halo が期待する中心超過の大きさ)
    halo_contrast = float(r["halo_fit"][cen].mean() - r["halo_fit"][per].mean())
    midE[f"bin{ib+1}"] = dict(
        e=r["e"], f_halo=r["f_halo"], dlnL=r["dlnL"], sig=r["sig"],
        totani_dlnL=TOTANI_DLNL[ib], ratio=r["dlnL"] / max(TOTANI_DLNL[ib], 1e-9),
        corr_full=c_full, corr_lat_only=c_lat, corr_lon_only=c_lon,
        resid_lon_contrast=lon_contrast, halo_lon_contrast=halo_contrast,
    )
    print(f"Bin{ib+1} {r['e']:5.1f}GeV: 比={r['dlnL']/max(TOTANI_DLNL[ib],1e-9):4.1f}x | "
          f"相関 full={c_full:+.2f} 緯度のみ={c_lat:+.2f} 経度のみ={c_lon:+.2f} | "
          f"経度コントラスト 残差={lon_contrast:+.1f} halo期待={halo_contrast:+.1f}")

# ============================================================
# 統一表: 全ビン(1-10)の中心集中コントラスト
# 低緯度帯 10<=|b|<20 で「中心 |l|<10」平均 −「周縁 20<|l|<50」中央値。
# 周縁に中央値を使うのは l≈-37 の局所負アーティファクト(点源/バブル縁)の影響を除くため。
# これが正=残差が銀河中心方向(l≈0)に集中=NFW halo が吸う中心超過。
# ============================================================
print("\n=== 統一: 全ビン 中心集中コントラスト(残差 vs halo期待) ===")
print("bin  E[GeV]  ΔlnL  Totani  比    残差中心集中  halo中心集中  残差/halo")
unified = {}
for ib in range(0, 10):
    r = reconstruct(ib); roi = r["roi"]
    band = roi & (np.abs(BG) >= 10) & (np.abs(BG) < 20)
    cen = band & (np.abs(LG) < 10)
    per = band & (np.abs(LG) > 20) & (np.abs(LG) < 50)
    def contrast(a):
        return float(a[cen].mean() - np.median(a[per]))
    rc = contrast(r["resid"]); hc = contrast(r["halo_fit"])
    frac = rc / hc if abs(hc) > 1e-9 else float("nan")
    unified[f"bin{ib+1}"] = dict(e=r["e"], dlnL=r["dlnL"], totani=TOTANI_DLNL[ib],
                                 resid_central=rc, halo_central=hc, resid_over_halo=frac)
    print(f"{ib+1:2d}  {r['e']:6.1f}  {r['dlnL']:5.0f}  {TOTANI_DLNL[ib]:5d}  "
          f"{r['dlnL']/max(TOTANI_DLNL[ib],1e-9):4.1f}  {rc:+11.2f}  {hc:+11.2f}  "
          f"{frac:+.2f}" if abs(hc) > 1e-9 else f"{ib+1:2d}  {r['e']:6.1f}  ...")

# ============================================================
# 図1: ΔlnL v8 vs Totani Fig.9
# ============================================================
E = m.BIN_CENTERS
ours = [RES["bins"][i]["delta_lnL"] for i in range(13)]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(15, 6))
for ax in (a1, a2):
    ax.plot(E, ours, "o-", color="crimson", lw=2.5, ms=7, label="本研究 v8 (disk込みバブル)")
    ax.plot(E, TOTANI_DLNL, "s--", color="navy", lw=2, ms=6, mfc="none", label="Totani Fig.9 (目視)")
    ax.axvline(20.76, color="gold", ls="--", alpha=0.6, label="20 GeV")
    ax.set_xscale("log"); ax.set_xlabel("Energy [GeV]")
    ax.set_ylabel(r"$\Delta\ln L$"); ax.legend(fontsize=9)
a1.set_title("線形: Bin2(2.5GeV)偽halo残存・mid-E過大")
a2.set_yscale("log"); a2.set_ylim(0.05, 2000)
a2.set_title("対数: 高E一致・mid-E 3-11倍・Bin1形反転")
fig.suptitle("Totani Fig.9 再現(v8): ΔlnL スペクトル比較", fontsize=13)
fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig(OUT / "diag_fig9_v8_deltalnL.png", dpi=120)
plt.close(fig)

# ============================================================
# 図2: 低E残差マップ(Bin1/Bin2)
# ============================================================
def sky(ax, a, roi, title, div=True):
    aa = a.copy().astype(float); aa[~roi] = np.nan
    aa[~roi] = np.nan
    sm = aa.copy(); sm[np.isnan(sm)] = 0.0; sm = gaussian_filter(sm, 1.0); sm[~roi] = np.nan
    if div:
        lim = np.nanpercentile(np.abs(a[roi]), 98) or 1.0
        im = ax.pcolormesh(_sub.L_BINS, _sub.B_BINS, sm.T, cmap="RdBu_r",
                           norm=mcolors.TwoSlopeNorm(0, -lim, lim))
    else:
        im = ax.pcolormesh(_sub.L_BINS, _sub.B_BINS, sm.T, cmap="inferno")
    ax.axhspan(-10, 10, color="gray", alpha=0.5)
    ax.set_xlim(-60, 60); ax.set_ylim(-60, 60)
    ax.set_title(title, fontsize=9); ax.set_xlabel("l", fontsize=8); ax.set_ylabel("b", fontsize=8)
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

fig, axs = plt.subplots(2, 3, figsize=(17, 10))
for row, ib in enumerate([0, 1]):
    r = reconstruct(ib)
    sky(axs[row, 0], r["resid"], r["roi"], f"Bin{ib+1} {r['e']:.1f}GeV no-halo残差 (σ={r['sig']:.0f})")
    sky(axs[row, 1], r["halo_fit"], r["roi"], f"halo×f_halo(={r['f_halo']:+.1f})")
    sky(axs[row, 2], r["t"]["fb"], r["roi"], "バブル正テンプレ", div=False)
fig.suptitle("(a)低E: Bin1(上)Totani101なのに残差ほぼ無/Bin2(下)偽halo121が吸う残差の形", fontsize=13)
fig.tight_layout(rect=(0, 0, 1, 0.96))
fig.savefig(OUT / "diag_lowE_residual_v8.png", dpi=110)
plt.close(fig)

# ============================================================
# 図3: mid-E 緯度/経度プロファイル分解(Bin4,6,8 代表)
# ============================================================
fig, axs = plt.subplots(2, 3, figsize=(17, 10))
babs = np.arange(10, 61)
for col, ib in enumerate([3, 5, 7]):   # Bin4=7.3, Bin6=20.8, Bin8=59
    r = reconstruct(ib); roi = r["roi"]
    absb = np.round(np.abs(BG)).astype(int)
    rp, hp = [], []
    for bv in babs:
        sel = roi & (absb == bv)
        rp.append(r["resid"][sel].mean() if sel.sum() else np.nan)
        hp.append(r["halo_fit"][sel].mean() if sel.sum() else np.nan)
    ax = axs[0, col]
    ax.plot(babs, rp, "o-", color="crimson", ms=3, label="no-halo残差")
    ax.plot(babs, hp, "s--", color="navy", ms=3, mfc="none", label="halo×f_halo")
    ax.axhline(0, color="gray", lw=0.7); ax.set_xlabel("|b| [deg]"); ax.set_ylabel("平均 counts/pix")
    ax.set_title(f"Bin{ib+1} {r['e']:.1f}GeV 緯度プロファイル"); ax.legend(fontsize=8)
    # 経度プロファイル(低緯度帯 10<=|b|<20)
    band = roi & (np.abs(BG) >= 10) & (np.abs(BG) < 20)
    lc = np.round(LG).astype(int)
    lg_ax, rlon, hlon = [], [], []
    for lv in range(-60, 61, 3):
        sel = band & (lc >= lv) & (lc < lv + 3)
        if sel.sum():
            lg_ax.append(lv + 1.5)
            rlon.append(r["resid"][sel].mean()); hlon.append(r["halo_fit"][sel].mean())
    ax2 = axs[1, col]
    ax2.plot(lg_ax, rlon, "o-", color="crimson", ms=3, label="no-halo残差")
    ax2.plot(lg_ax, hlon, "s--", color="navy", ms=3, mfc="none", label="halo×f_halo")
    ax2.axhline(0, color="gray", lw=0.7); ax2.axvline(0, color="gold", ls=":", alpha=0.7)
    ax2.set_xlabel("l [deg]"); ax2.set_ylabel("平均 counts/pix")
    ax2.set_title(f"Bin{ib+1} 経度プロファイル(10<=|b|<20)\n中心集中=DM的 / 平坦=GALPROP緯度不一致")
    ax2.legend(fontsize=8)
fig.suptitle("(b)mid-E: 残差(赤)がhalo(青)と緯度で合っても経度で中心集中しなければGALPROP緯度不一致", fontsize=13)
fig.tight_layout(rect=(0, 0, 1, 0.96))
fig.savefig(OUT / "diag_midE_latlon_v8.png", dpi=110)
plt.close(fig)

# ============================================================
# JSON 正本
# ============================================================
import subprocess
try:
    githash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
except Exception:
    githash = "unknown"
out = dict(
    generated="2026-07-18", git_hash=githash,
    source="results/mcmc_allbins_gasICS_v8_diskbubble/halo_spectrum.json",
    env=dict(MCMC_DISK_BUBBLE="1", MCMC_ICS_SPLIT="0", MCMC_CELL_LIKELIHOOD="0", MCMC_SIGNFREE_HALO="1"),
    totani_fig9_dlnL=TOTANI_DLNL,
    ours_v8_dlnL=[float(x) for x in ours],
    lowE_a=lowE, midE_b=midE, unified_central_contrast=unified,
)
json.dump(out, open(OUT / "diag_lowE_midE_v8.json", "w"), ensure_ascii=False, indent=2)
print("\n完成:")
for f in ["diag_lowE_midE_v8.json", "diag_fig9_v8_deltalnL.png",
          "diag_lowE_residual_v8.png", "diag_midE_latlon_v8.png"]:
    print("  ", OUT / f)
