#!/usr/bin/env python3
"""
矮小銀河5天体: 「生スカイマップ → ROI(ON/OFF)定義 → 背景モデル差し引き → 有意性」
の全段階を1天体1図で可視化するパイプライン。

教授指摘（2026-05-22）「何も引いてない銀河を見せてもらって、そこから一つ一つ
要素を引いて、その引く関数や、既存データについてもまとめて」への対応。

手法（Fermi-LAT 矮小銀河探索の標準: Ackermann+2015 等と同じ ON/OFF 比較）:
  - ON 領域: 天体中心から半径 ON_RAD = 2.0°
  - OFF 領域: 2.0°-5.0° の同心円環（背景見積もり用）
  - 規格化係数 α = ON 面積 / OFF 面積 = 2.0² / (5.0² - 2.0²) = 4/21 ≈ 0.1905
  - 背景モデル: BG = α × N_off （= ON 領域に「差し引く」量）
  - 超過: Excess = N_on - BG
  - 有意性: Li & Ma (1983) Eq.17（Fermi-LAT 標準式。analyze_dwarfs.py の
    簡易式 excess/sqrt(bg + α²×N_off) ではなく正式な対数尤度比に基づく式）

追加チェック（点源混入検証）:
  Coma Ber で全ビン共通の超過（Bin1: +11.1σ など、20 GeV 特有でない）が見つかったため、
  ON 領域内の既知 4FGL-DR2 点源を半径 MASK_RAD でマスクし、再計算して比較する。
  「引いた後にどれだけ変わるか」を可視化することで、信号が点源由来か DM 起源かを切り分ける。

既存データ: dwarf_<name>_780w.csv（5°半径、energy_GeV/ra_deg/dec_deg/ang_dist_deg）、
            ref/gll_psc_v35_dr4.fit（4FGL-DR4 点源カタログ、本解析の銀河中心 ROI と同じカタログ）
出力: data/figure-dwarfs/<name>/pipeline_<name>.png
      data/figure-dwarfs/<name>/psmask_check_<name>.png
      results/dwarf_pipeline_results.json
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd
from astropy.io import fits as afits
from astropy.coordinates import SkyCoord
import astropy.units as u
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# 日本語ラベルが図中に多いため CJK フォントを明示登録・指定
# （rcParams だけでは fontconfig 名と一致せず DejaVu Sans にフォールバックして文字化けする）
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUT_DIR  = DATA_DIR / "figure-dwarfs"
RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Totani (2025) 13ビン定義（対数等間隔, 1.51-814 GeV）
N_BINS      = 13
BIN_CENTERS = np.logspace(np.log10(1.51), np.log10(814.0), N_BINS)
_r          = (814.0 / 1.51) ** (1.0 / (N_BINS - 1))
BIN_EDGES   = np.concatenate([[1.51 / _r**0.5],
                              np.sqrt(BIN_CENTERS[:-1] * BIN_CENTERS[1:]),
                              [814.0 * _r**0.5]])
BIN6_IDX = 5  # 20.76 GeV

TARGETS = [
    ("draco",      260.052,  57.915, "Draco dSph"),
    ("sculptor",    15.039, -33.709, "Sculptor dSph"),
    ("ursa_minor", 227.285,  67.222, "Ursa Minor dSph"),
    ("segue1",     151.767,  16.082, "Segue 1"),
    ("coma_ber",   186.746,  23.904, "Coma Berenices"),
]

ON_RAD  = 2.0   # ON 領域半径 [deg]
OFF_RAD = 5.0   # OFF 領域外径 [deg]（CSV 自体が ang_dist < 5° で抽出されている）
ALPHA   = ON_RAD**2 / (OFF_RAD**2 - ON_RAD**2)   # = 4/21

# 点源マスク半径。本解析の銀河中心 ROI では 1°ピクセル単位でマスクしており
# （20 GeV の Fermi-LAT PSF ≈ 0.2° に対し十分大きい）、ここでも同程度に
# 「PSF を確実に覆う」半径として 0.5° を採用する（円形マスクの直径 1° は
# 銀河中心解析のピクセル法と同程度の除去効果）。
MASK_RAD = 0.5
CAT_PATH = Path(__file__).resolve().parent.parent / "ref" / "gll_psc_v35_dr4.fit"  # 4FGL-DR4(14年分); 旧DR2(12年分)から2026-07-10更新
N_MC = 300_000  # 有効面積比モンテカルロ評価の試行数


def _load_nearby_4fgl(ra0, dec0, radius_deg):
    """ターゲット中心から radius_deg 以内の 4FGL-DR2 点源を返す"""
    with afits.open(CAT_PATH) as hdul:
        data = hdul[1].data
        ra, dec, names = data["RAJ2000"], data["DEJ2000"], data["Source_Name"]
    target = SkyCoord(ra=ra0 * u.deg, dec=dec0 * u.deg)
    cat = SkyCoord(ra=np.asarray(ra) * u.deg, dec=np.asarray(dec) * u.deg)
    sep = target.separation(cat).deg
    sel = sep <= radius_deg
    return ra[sel], dec[sel], np.array([n.strip() for n in names[sel]]), sep[sel]


def _effective_alpha(ra0, dec0, src_ra, src_dec, mask_rad, rng):
    """ON/OFF 領域の有効面積比 α_eff をモンテカルロで評価する。

    マスクされた点源パッチが ON 領域・OFF 領域から非一様に面積を奪うため、
    幾何学的な α = ON面積/OFF面積 をそのまま使うと規格化が崩れる。
    一様乱数を OFF 円板内に N_MC 個ばらまき、マスク後に ON / OFF に
    残る点の比から実効的な面積比を求める。
    """
    # 接平面オフセットで一様乱数を生成（5° スケールでは平面近似誤差 <0.2% で無視できる）
    r = OFF_RAD * np.sqrt(rng.uniform(0, 1, N_MC))
    th = rng.uniform(0, 2 * np.pi, N_MC)
    dx, dy = r * np.cos(th), r * np.sin(th)
    d = np.hypot(dx, dy)

    masked = np.zeros(N_MC, dtype=bool)
    cosdec0 = np.cos(np.radians(dec0))
    for sra, sdec in zip(src_ra, src_dec):
        sdx = ((sra - ra0 + 180.0) % 360.0 - 180.0) * cosdec0
        sdy = sdec - dec0
        masked |= (np.hypot(dx - sdx, dy - sdy) < mask_rad)

    on_eff  = np.sum((d < ON_RAD) & ~masked)
    off_eff = np.sum((d >= ON_RAD) & (d < OFF_RAD) & ~masked)
    if off_eff == 0:
        return ALPHA
    return on_eff / off_eff


def li_ma_significance(n_on, n_off, alpha):
    """Li & Ma (1983) ApJ 272, 317, Eq.17 による有意性（符号付き）。

    S = sign(N_on - α N_off) * sqrt(2 [ N_on ln( (1+α)/α * N_on/(N_on+N_off) )
                                         + N_off ln( (1+α) * N_off/(N_on+N_off) ) ])
    N_on=0 または N_off=0 のビンは対数項が定義できないため 0 を返す。
    """
    if n_on <= 0 or n_off <= 0:
        return 0.0
    total = n_on + n_off
    term1 = n_on * np.log((1.0 + alpha) / alpha * (n_on / total))
    term2 = n_off * np.log((1.0 + alpha) * (n_off / total))
    inner = 2.0 * (term1 + term2)
    if inner < 0:
        inner = 0.0
    sig = np.sqrt(inner)
    sign = 1.0 if n_on > alpha * n_off else -1.0
    return sign * sig


def analyze_target(name, ra0, dec0, label):
    csv_path = DATA_DIR / "CSV" / "dwarfs" / f"dwarf_{name}_780w.csv"
    if not csv_path.exists():
        print(f"  {name}: CSV なし、スキップ")
        return None

    df = pd.read_csv(csv_path)
    d  = df["ang_dist_deg"].values
    e  = df["energy_GeV"].values
    ra, dec = df["ra_deg"].values, df["dec_deg"].values

    # 接平面オフセット座標（5°スケールでは平面近似誤差 < (5°)^2/2 ~ 0.15° で無視できる）
    dra  = (ra - ra0 + 180.0) % 360.0 - 180.0
    dx   = dra * np.cos(np.radians(dec0))   # 赤経方向オフセット [deg]
    dy   = dec - dec0                       # 赤緯方向オフセット [deg]

    on_mask  = d < ON_RAD
    off_mask = (d >= ON_RAD) & (d < OFF_RAD)

    n_on  = np.zeros(N_BINS)
    n_off = np.zeros(N_BINS)
    for i in range(N_BINS):
        e_mask = (e >= BIN_EDGES[i]) & (e < BIN_EDGES[i + 1])
        n_on[i]  = (on_mask  & e_mask).sum()
        n_off[i] = (off_mask & e_mask).sum()

    bg     = ALPHA * n_off
    excess = n_on - bg
    sigma  = np.array([li_ma_significance(n_on[i], n_off[i], ALPHA) for i in range(N_BINS)])

    # --- 点源混入チェック: ON 領域内に入る 4FGL-DR2 点源を半径 MASK_RAD で除去して再計算 ---
    src_ra, src_dec, src_name, src_sep = _load_nearby_4fgl(ra0, dec0, OFF_RAD)
    in_on = src_sep < ON_RAD
    rng = np.random.default_rng(seed=42)  # 再現性のため固定 seed（reproducibility-stamp 対応）
    alpha_eff = _effective_alpha(ra0, dec0, src_ra, src_dec, MASK_RAD, rng)

    sdx = ((src_ra - ra0 + 180.0) % 360.0 - 180.0) * np.cos(np.radians(dec0))
    sdy = src_dec - dec0
    photon_masked = np.zeros(len(d), dtype=bool)
    for k in range(len(src_ra)):
        photon_masked |= (np.hypot(dx - sdx[k], dy - sdy[k]) < MASK_RAD)

    on_mask_m  = on_mask  & ~photon_masked
    off_mask_m = off_mask & ~photon_masked
    n_on_m  = np.zeros(N_BINS)
    n_off_m = np.zeros(N_BINS)
    for i in range(N_BINS):
        e_mask = (e >= BIN_EDGES[i]) & (e < BIN_EDGES[i + 1])
        n_on_m[i]  = (on_mask_m  & e_mask).sum()
        n_off_m[i] = (off_mask_m & e_mask).sum()
    bg_m     = alpha_eff * n_off_m
    excess_m = n_on_m - bg_m
    sigma_m  = np.array([li_ma_significance(n_on_m[i], n_off_m[i], alpha_eff) for i in range(N_BINS)])

    return {
        "name": name, "label": label, "ra0": ra0, "dec0": dec0,
        "dx": dx, "dy": dy, "d": d, "e": e,
        "on": n_on, "off": n_off, "bg": bg, "excess": excess, "sigma": sigma,
        "src_ra": src_ra, "src_dec": src_dec, "src_name": src_name, "src_sep": src_sep,
        "src_in_on": in_on, "alpha_eff": alpha_eff,
        "on_m": n_on_m, "off_m": n_off_m, "bg_m": bg_m,
        "excess_m": excess_m, "sigma_m": sigma_m,
    }


def plot_pipeline(res):
    """1天体: [生マップ+ROI] [ON vs 背景モデル(=引く量)] [超過と有意性] の3パネル"""
    name, label = res["name"], res["label"]
    out_dir = OUT_DIR / name
    out_dir.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(20, 5.6))
    fig.patch.set_facecolor("#05051a")
    fig.suptitle(f"{name.upper()} ({label}) — 生マップ→ROI→背景差引→有意性  [全エネルギー, 780週]",
                 color="white", fontsize=13, fontweight="bold")

    # --- Panel 1: 生スカイマップ（何も引いていない）+ ON/OFF ROI ---
    ax = axes[0]
    ax.set_facecolor("#0d0d2a")
    nbin2d = 40
    h, xedges, yedges = np.histogram2d(res["dx"], res["dy"], bins=nbin2d,
                                        range=[[-OFF_RAD, OFF_RAD], [-OFF_RAD, OFF_RAD]])
    disp = np.where(h > 0, h, np.nan)
    im = ax.pcolormesh(xedges, yedges, disp.T, cmap="inferno",
                       norm=mcolors.LogNorm(vmin=1, vmax=np.nanmax(disp)))
    on_circle  = plt.Circle((0, 0), ON_RAD,  fill=False, ec="#44ccff", lw=2.0, ls="--",
                            label=f"ON  (r<{ON_RAD:.0f}°)")
    off_circle = plt.Circle((0, 0), OFF_RAD, fill=False, ec="#ffcc00", lw=2.0, ls="--",
                            label=f"OFF ({ON_RAD:.0f}°–{OFF_RAD:.0f}°)")
    ax.add_patch(on_circle); ax.add_patch(off_circle)
    ax.set_aspect("equal")
    ax.set_xlim(OFF_RAD, -OFF_RAD); ax.set_ylim(-OFF_RAD, OFF_RAD)  # RA は左が増える向き
    ax.set_xlabel(r"$\Delta\alpha \cos\delta$ [deg]", color="white")
    ax.set_ylabel(r"$\Delta\delta$ [deg]", color="white")
    ax.set_title("① 生フォトンマップ（何も差し引いていない）", color="white", fontsize=10)
    ax.tick_params(colors="white")
    for sp in ax.spines.values():
        sp.set_edgecolor("#444")
    ax.legend(fontsize=8, loc="upper right", facecolor="#0d0d2a", labelcolor="white")
    fig.colorbar(im, ax=ax, label="counts / pixel", shrink=0.85)

    # --- Panel 2: ON vs 背景モデル(α×OFF) = 「引く量」のスペクトル比較 ---
    ax = axes[1]
    ax.set_facecolor("#0d0d2a")
    x = np.arange(N_BINS)
    ax.bar(x - 0.2, res["on"],  width=0.4, color="#4488ff", alpha=0.85,
           label=f"$N_{{on}}$ (r<{ON_RAD:.0f}°)")
    ax.bar(x + 0.2, res["bg"],  width=0.4, color="#ff8800", alpha=0.85,
           label=fr"背景モデル $\alpha N_{{off}}$ ($\alpha$={ALPHA:.4f})")
    ax.axvline(BIN6_IDX, color="gold", ls="--", lw=1.5, label="Bin6 (20.76 GeV)")
    ax.set_xticks(x)
    ax.set_xticklabels([f"{c:.1f}" for c in BIN_CENTERS], rotation=45, fontsize=8, color="white")
    ax.set_xlabel("Energy bin center [GeV]", color="white")
    ax.set_ylabel("Photon counts", color="white")
    ax.set_title(r"② $N_{on}$ と「差し引く」背景モデル $\alpha N_{off}$", color="white", fontsize=10)
    ax.tick_params(colors="white")
    for sp in ax.spines.values():
        sp.set_edgecolor("#444")
    ax.legend(fontsize=8); ax.grid(alpha=0.2)

    # --- Panel 3: 超過 (Excess = N_on - BG) と Li&Ma 有意性 ---
    ax = axes[2]
    ax.set_facecolor("#0d0d2a")
    colors = ["#ff4444" if abs(s) > 2 else "#4488ff" for s in res["sigma"]]
    ax2 = ax.twinx()
    ax2.step(x, res["excess"], where="mid", color="#888888", lw=1.3, alpha=0.7,
             label="Excess = $N_{on}-\\alpha N_{off}$")
    ax2.set_ylabel("Excess counts", color="#aaaaaa")
    ax2.tick_params(colors="#aaaaaa")
    ax.bar(x, res["sigma"], color=colors, alpha=0.9, zorder=3)
    ax.axhline(0, color="white", lw=0.8)
    ax.axhline(2, color="gold", lw=1, ls="--")
    ax.axhline(-2, color="gold", lw=1, ls="--")
    ax.axvline(BIN6_IDX, color="gold", lw=2, alpha=0.6)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{c:.1f}" for c in BIN_CENTERS], rotation=45, fontsize=8, color="white")
    ax.set_xlabel("Energy bin center [GeV]", color="white")
    ax.set_ylabel("Li & Ma significance σ", color="white")
    ax.set_title("③ 超過と Li & Ma (1983) 有意性", color="white", fontsize=10)
    ax.tick_params(colors="white")
    for sp in ax.spines.values():
        sp.set_edgecolor("#444")
    ax.set_zorder(ax2.get_zorder() + 1)
    ax.patch.set_visible(False)
    ax.grid(alpha=0.2)

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    out = out_dir / f"pipeline_{name}.png"
    fig.savefig(out, dpi=140, bbox_inches="tight", facecolor="#05051a")
    plt.close(fig)
    return out


def plot_ps_contamination_check(res):
    """点源混入チェック: [生マップ+点源位置] [マスク前後の有意性スペクトル比較]

    全ビン共通の超過（DM起源なら 20 GeV 付近にのみ現れるはず）が、
    既知 4FGL 点源の混入で説明できるかを検証する sanity check 図。
    """
    name, label = res["name"], res["label"]
    out_dir = OUT_DIR / name
    out_dir.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(15, 5.6))
    fig.patch.set_facecolor("#05051a")
    n_in_on = int(res["src_in_on"].sum())
    fig.suptitle(f"{name.upper()} ({label}) — 点源混入チェック  "
                 f"（ON 領域内 4FGL 点源 {n_in_on} 個, マスク半径 {MASK_RAD:.1f}°）",
                 color="white", fontsize=12, fontweight="bold")

    # --- Panel A: 生マップ + 4FGL 点源位置・マスク円 ---
    ax = axes[0]
    ax.set_facecolor("#0d0d2a")
    nbin2d = 40
    h, xedges, yedges = np.histogram2d(res["dx"], res["dy"], bins=nbin2d,
                                        range=[[-OFF_RAD, OFF_RAD], [-OFF_RAD, OFF_RAD]])
    disp = np.where(h > 0, h, np.nan)
    im = ax.pcolormesh(xedges, yedges, disp.T, cmap="inferno",
                       norm=mcolors.LogNorm(vmin=1, vmax=np.nanmax(disp)))
    ax.add_patch(plt.Circle((0, 0), ON_RAD, fill=False, ec="#44ccff", lw=2.0, ls="--"))
    ax.add_patch(plt.Circle((0, 0), OFF_RAD, fill=False, ec="#ffcc00", lw=1.5, ls="--"))
    cosdec0 = np.cos(np.radians(res["dec0"]))
    for sra, sdec, sname, ssep, sin in zip(res["src_ra"], res["src_dec"],
                                            res["src_name"], res["src_sep"], res["src_in_on"]):
        sdx = ((sra - res["ra0"] + 180.0) % 360.0 - 180.0) * cosdec0
        sdy = sdec - res["dec0"]
        col = "#ff4444" if sin else "#888888"
        ax.plot(sdx, sdy, marker="x", ms=10, mew=2, color=col)
        ax.add_patch(plt.Circle((sdx, sdy), MASK_RAD, fill=False, ec=col, lw=1.2, ls=":"))
        ax.text(sdx, sdy - MASK_RAD - 0.15, f"{sname}\n({ssep:.2f}°)",
                color=col, fontsize=6.5, ha="center", va="top")
    ax.set_aspect("equal")
    ax.set_xlim(OFF_RAD, -OFF_RAD); ax.set_ylim(-OFF_RAD, OFF_RAD)
    ax.set_xlabel(r"$\Delta\alpha \cos\delta$ [deg]", color="white")
    ax.set_ylabel(r"$\Delta\delta$ [deg]", color="white")
    ax.set_title("4FGL-DR2 点源位置（赤 x = ON 領域内、灰 x = ON 領域外）", color="white", fontsize=9.5)
    ax.tick_params(colors="white")
    for sp in ax.spines.values():
        sp.set_edgecolor("#444")
    fig.colorbar(im, ax=ax, label="counts / pixel", shrink=0.85)

    # --- Panel B: マスク前後の有意性スペクトル比較 ---
    ax = axes[1]
    ax.set_facecolor("#0d0d2a")
    x = np.arange(N_BINS)
    ax.bar(x - 0.2, res["sigma"],   width=0.4, color="#ff8800", alpha=0.85,
           label="マスク前（点源混入あり）")
    ax.bar(x + 0.2, res["sigma_m"], width=0.4, color="#44ccff", alpha=0.9,
           label=fr"マスク後（$\alpha_{{eff}}$={res['alpha_eff']:.4f}）")
    ax.axhline(0, color="white", lw=0.8)
    ax.axhline(2, color="gold", lw=1, ls="--")
    ax.axhline(-2, color="gold", lw=1, ls="--")
    ax.axvline(BIN6_IDX, color="gold", lw=2, alpha=0.5, label="Bin6 (20.76 GeV)")
    ax.set_xticks(x)
    ax.set_xticklabels([f"{c:.1f}" for c in BIN_CENTERS], rotation=45, fontsize=8, color="white")
    ax.set_xlabel("Energy bin center [GeV]", color="white")
    ax.set_ylabel("Li & Ma 有意性 σ", color="white")
    ax.set_title("点源マスク前後の有意性スペクトル", color="white", fontsize=9.5)
    ax.tick_params(colors="white")
    for sp in ax.spines.values():
        sp.set_edgecolor("#444")
    ax.legend(fontsize=8); ax.grid(alpha=0.2)

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    out = out_dir / f"psmask_check_{name}.png"
    fig.savefig(out, dpi=140, bbox_inches="tight", facecolor="#05051a")
    plt.close(fig)
    return out


def plot_summary(results):
    """5天体 Bin6 有意性まとめ（Li & Ma 正式式）"""
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#05051a")
    ax.set_facecolor("#0d0d2a")

    names  = [r["name"].replace("_", " ").title() for r in results]
    sigmas = [r["sigma"][BIN6_IDX] for r in results]
    colors = ["#ff4444" if s > 2 else "#4488ff" for s in sigmas]

    bars = ax.bar(names, sigmas, color=colors, alpha=0.85, width=0.5)
    ax.axhline(0, color="white", lw=0.8)
    ax.axhline(2, color="gold", lw=1.5, ls="--", label="2σ 目安")
    ax.axhline(-2, color="gold", lw=1.5, ls="--")
    for bar, s in zip(bars, sigmas):
        ax.text(bar.get_x() + bar.get_width() / 2, s + 0.05 if s >= 0 else s - 0.15,
                f"{s:.2f}σ", ha="center", va="bottom" if s >= 0 else "top",
                color="white", fontsize=11, fontweight="bold")

    ax.set_ylabel("Bin6 (20.76 GeV) Li & Ma 有意性 σ", color="white", fontsize=12)
    ax.set_title("矮小銀河5天体 — 20.76 GeV 過剰の有意性（Li & Ma 1983 正式式, 780週）",
                 color="white", fontsize=13, fontweight="bold")
    ax.tick_params(colors="white")
    for sp in ax.spines.values():
        sp.set_edgecolor("#444")
    ax.legend(fontsize=10); ax.grid(axis="y", alpha=0.2)

    plt.tight_layout()
    out = OUT_DIR / "dwarf_summary_bin6_lima.png"
    fig.savefig(out, dpi=130, bbox_inches="tight", facecolor="#05051a")
    plt.close(fig)
    return out


def main():
    print("矮小銀河パイプライン解析開始")
    print(f"ON_RAD={ON_RAD}°, OFF_RAD={OFF_RAD}°, alpha={ALPHA:.6f} (=4/21)\n")

    results = []
    summary = {
        "method": "ON/OFF aperture photometry (Fermi-LAT dSph standard, cf. Ackermann+2015)",
        "on_radius_deg": ON_RAD,
        "off_radius_deg": OFF_RAD,
        "alpha": ALPHA,
        "alpha_formula": "ON_RAD^2 / (OFF_RAD^2 - ON_RAD^2) = 4/21",
        "significance_formula": "Li & Ma (1983) ApJ 272, 317, Eq.17",
        "bin_centers_GeV": BIN_CENTERS.tolist(),
        "targets": {},
    }

    for name, ra0, dec0, label in TARGETS:
        print(f">>> {name}")
        res = analyze_target(name, ra0, dec0, label)
        if res is None:
            continue
        out = plot_pipeline(res)
        b6 = res["sigma"][BIN6_IDX]
        print(f"    Bin6: N_on={res['on'][BIN6_IDX]:.0f}  N_off={res['off'][BIN6_IDX]:.0f}  "
              f"BG={res['bg'][BIN6_IDX]:.2f}  Excess={res['excess'][BIN6_IDX]:+.2f}  "
              f"sigma={b6:+.3f}sigma (Li&Ma)")
        print(f"    -> {out.relative_to(DATA_DIR.parent)}")

        n_in_on = int(res["src_in_on"].sum())
        out2 = plot_ps_contamination_check(res)
        b6m = res["sigma_m"][BIN6_IDX]
        print(f"    点源混入チェック: ON内 4FGL点源={n_in_on}個, alpha_eff={res['alpha_eff']:.4f} "
              f"(geom alpha={ALPHA:.4f})")
        print(f"      Bin6 マスク前 sigma={b6:+.3f} -> マスク後 sigma={b6m:+.3f}")
        print(f"    -> {out2.relative_to(DATA_DIR.parent)}")

        results.append(res)
        summary["targets"][name] = {
            "label": label, "ra0_deg": ra0, "dec0_deg": dec0,
            "n_on": res["on"].tolist(), "n_off": res["off"].tolist(),
            "bg": res["bg"].tolist(), "excess": res["excess"].tolist(),
            "sigma_lima": res["sigma"].tolist(),
            "ps_contamination_check": {
                "mask_radius_deg": MASK_RAD,
                "n_4fgl_in_on_region": n_in_on,
                "4fgl_sources_within_off_radius": [
                    {"name": n, "sep_deg": float(s), "in_on_region": bool(b)}
                    for n, s, b in zip(res["src_name"], res["src_sep"], res["src_in_on"])
                ],
                "alpha_effective_after_mask": res["alpha_eff"],
                "n_on_masked": res["on_m"].tolist(),
                "n_off_masked": res["off_m"].tolist(),
                "bg_masked": res["bg_m"].tolist(),
                "excess_masked": res["excess_m"].tolist(),
                "sigma_lima_masked": res["sigma_m"].tolist(),
            },
        }

    if results:
        out = plot_summary(results)
        print(f"\nサマリー図 -> {out.relative_to(DATA_DIR.parent)}")
        print("\n=== Bin6 (20.76 GeV) Li & Ma 有意性まとめ ===")
        for r in results:
            flag = "*" if abs(r["sigma"][BIN6_IDX]) > 2 else " "
            print(f"  {flag} {r['name']:12s}: {r['sigma'][BIN6_IDX]:+.3f} sigma")

    json_path = RESULTS_DIR / "dwarf_pipeline_results.json"
    with open(json_path, "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"\n結果 JSON -> {json_path.relative_to(DATA_DIR.parent)}")
    print(f"完了 -> {OUT_DIR}")


if __name__ == "__main__":
    main()
