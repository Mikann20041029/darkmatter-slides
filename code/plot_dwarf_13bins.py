"""
矮小銀河5天体 × 全13エネルギービン — Totani Fig.8/9 相当の解析

ON/OFF 開口測光法で各ビンの S/N を計算し：
  - Fig.8 相当: S/N スペクトル（線形プロット、全天体一枚）
  - Fig.9 相当: Δχ² = (S/N)² スペクトル
  - 各天体別: 全13ビンの ON/OFF カウント + S/N
  - σv 上限値: 95% CL 上限（Feldman-Cousins 近似）

出力:
  data/figure-dwarfs/all5_13bins_sn_spectrum.png   (Totani Fig.8 相当)
  data/figure-dwarfs/all5_13bins_dchi2.png          (Totani Fig.9 相当)
  data/figure-dwarfs/<name>/bins13_<name>.png       (各天体別)
  results/dwarf_13bins_results.json
"""
import pathlib as _pathlib

import sys
sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))

import numpy as np
import pandas as pd
import json
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"
from scipy.stats import norm as scipy_norm

BASE     = _pathlib.Path(__file__).resolve().parent.parent
DATA_DIR = BASE / "data"
OUT_DIR  = DATA_DIR / "figure-dwarfs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ─── Totani 13 ビン定義 ──────────────────────────────────────────────────────
N_BINS = 13
_centers = np.logspace(np.log10(1.51), np.log10(814.0), N_BINS)
_ratio   = (_centers[-1] / _centers[0]) ** (1 / (N_BINS - 1))
_e_low   = 1.51  / _ratio**0.5
_e_high  = 814.0 * _ratio**0.5
_edges   = np.concatenate([[_e_low], np.sqrt(_centers[:-1]*_centers[1:]), [_e_high]])
BIN_CENTERS = _centers
BIN_EDGES   = _edges

# ─── ON/OFF パラメータ（Ackermann+2015 標準）──────────────────────────────
ON_RAD   = 2.0   # deg
OFF_IN   = 2.0   # deg
OFF_OUT  = 5.0   # deg
ALPHA    = ON_RAD**2 / (OFF_OUT**2 - OFF_IN**2)   # = 4/21 ≈ 0.1905

# ─── 5天体の定義 ──────────────────────────────────────────────────────────
TARGETS = {
    "draco":      {"l": 86.37,  "b": 34.72,  "label": "Draco",       "color": "#FF6644"},
    "sculptor":   {"l": 287.53, "b": -83.16, "label": "Sculptor",    "color": "#44CCFF"},
    "ursa_minor": {"l": 104.97, "b": 44.80,  "label": "Ursa Minor",  "color": "#FFCC00"},
    "segue1":     {"l": 220.48, "b": 50.43,  "label": "Segue 1",     "color": "#CC44FF"},
    "coma_ber":   {"l": 241.89, "b": 83.61,  "label": "Coma Ber.",   "color": "#44FF88"},
}

# ─── J因子（Ackermann+2015 Table 1 準拠, 10^log10J [GeV² cm⁻⁵ sr⁻¹]）───
J_FACTORS = {
    "draco":      {"log10J": 18.8, "log10J_err": 0.16},
    "sculptor":   {"log10J": 18.5, "log10J_err": 0.18},
    "ursa_minor": {"log10J": 18.8, "log10J_err": 0.19},
    "segue1":     {"log10J": 19.3, "log10J_err": 0.29},
    "coma_ber":   {"log10J": 18.8, "log10J_err": 0.36},
}

C_BG = "#05051A"
CMAP_DIV = LinearSegmentedColormap.from_list("totani_div", [
    (0.0, "#00FFFF"), (0.17, "#0000FF"), (0.33, "#000080"),
    (0.45, "#000020"), (0.50, "#000000"), (0.55, "#200000"),
    (0.67, "#800000"), (0.83, "#FF4400"), (0.92, "#FFCC00"),
    (1.0,  "#FFFF00"),
])


def li_ma(n_on, n_off, alpha):
    """Li & Ma (1983) Eq.17 有意度。n_on,n_off はスカラーまたは配列"""
    n_on  = np.asarray(n_on,  dtype=float)
    n_off = np.asarray(n_off, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = (1+alpha)/alpha * n_on/(n_on + n_off)
        term1 = n_on  * np.log(ratio)
        ratio2 = (1+alpha) * n_off/(n_on + n_off)
        term2 = n_off * np.log(ratio2)
        s2 = 2 * (term1 + term2)
        s2 = np.where(n_on + n_off > 0, s2, 0.0)
        sign = np.where(n_on > alpha * n_off, 1.0, -1.0)
        sn = sign * np.sqrt(np.maximum(s2, 0.0))
    return sn


def feldman_cousins_ul95(n_on, n_off, alpha, n_sigma=1.645):
    """
    95% CL 上限の近似（Feldman-Cousins 感覚の簡易版）。
    背景 b = alpha * n_off として、信号 s_95 を返す。
    s_95 = max(0, n_on - b) + n_sigma * sqrt(n_on + alpha^2 * n_off)
    """
    b = alpha * n_off
    s95 = np.maximum(n_on - b, 0) + n_sigma * np.sqrt(n_on + alpha**2 * n_off)
    return s95


def counts_to_sigmav(s_counts, j_log10J, e_center_gev, dm_mass_gev=500.0):
    """
    信号カウントから σv を推定（bb̄チャンネル、DM 消滅）。

    φ = (⟨σv⟩ / 8π m²χ) × J × ∫ (dN/dE) dE × exposure
    s = φ × exposure

    簡易 DM スペクトル（bb̄ 近似）:
      dN/dE ≈ (N_tot/m) × exp(-8 E/m)
      ∫ dE over bin ≈ (m/8) × [exp(-8 E_lo/m) - exp(-8 E_hi/m)]

    returns σv [cm³/s]
    """
    # 露出量（Mrk501 較正値: 1.24e11 cm²·s）× ビン幅 × SR
    # ON領域の立体角: π × (ON_RAD × π/180)² sr
    EXPOSURE   = 1.24e11    # cm² s
    sr_on      = np.pi * (ON_RAD * np.pi/180)**2   # ~1.21e-3 sr
    J          = 10**j_log10J  # GeV² cm⁻⁵ sr⁻¹

    # ビン幅
    i_bin  = np.argmin(np.abs(BIN_CENTERS - e_center_gev))
    e_lo   = BIN_EDGES[i_bin]
    e_hi   = BIN_EDGES[i_bin+1]
    m      = dm_mass_gev

    # bb̄ スペクトルの bin 積分 [GeV⁻¹ 単位でなく counts per annihilation]
    def dNdE_bbar(E, m):
        # Cirelli+2011 PPPC4DMID の簡易近似（bb̄）
        x = E / m
        if x >= 1: return 0.0
        return (m**(-1)) * x**(-1.5) * (1-x)**3 * np.exp(-7*x) * 5

    n_pts = 50
    E_arr = np.linspace(e_lo, e_hi, n_pts)
    dN_arr = np.array([dNdE_bbar(e, m) for e in E_arr])
    int_dN = np.trapezoid(dN_arr, E_arr)  # [events per annihilation per GeV × GeV = events per ann]
    if int_dN <= 0:
        return np.nan

    # σv = s × 8π m² / (J × sr_on × EXPOSURE × int_dN)
    sigma_v = s_counts * 8 * np.pi * m**2 / (J * sr_on * EXPOSURE * int_dN)
    return sigma_v


def analyze_target(name, cfg):
    csv_path = DATA_DIR / "CSV" / "dwarfs" / f"dwarf_{name}_780w.csv"
    if not csv_path.exists():
        print(f"  {name}: CSVなし → スキップ")
        return None

    df = pd.read_csv(csv_path, comment="#", low_memory=False)

    results_bins = []
    for i, (e_lo, e_hi, e_cen) in enumerate(zip(BIN_EDGES[:-1], BIN_EDGES[1:], BIN_CENTERS)):
        sel = df[(df.energy_GeV >= e_lo) & (df.energy_GeV < e_hi)]

        n_on  = (sel.ang_dist_deg <= ON_RAD).sum()
        n_off = ((sel.ang_dist_deg > OFF_IN) & (sel.ang_dist_deg <= OFF_OUT)).sum()
        bg    = ALPHA * n_off
        excess = n_on - bg
        sn    = float(li_ma(n_on, n_off, ALPHA)) if (n_on + n_off) > 0 else 0.0

        # 95% CL 上限信号カウント
        s95   = float(feldman_cousins_ul95(n_on, n_off, ALPHA))
        # σv 上限（500 GeV DM, bb̄）
        j     = J_FACTORS[name]["log10J"]
        sv95  = counts_to_sigmav(s95, j, e_cen, dm_mass_gev=500.0)

        results_bins.append({
            "bin_idx":      i,
            "e_center_gev": float(e_cen),
            "e_lo":         float(e_lo),
            "e_hi":         float(e_hi),
            "n_on":         int(n_on),
            "n_off":        int(n_off),
            "bg":           float(bg),
            "excess":       float(excess),
            "sn":           sn,
            "s95_counts":   float(s95),
            "sigmav_ul95":  float(sv95) if np.isfinite(sv95) else None,
        })
        print(f"  {name} Bin{i+1:02d} ({e_cen:7.2f} GeV): "
              f"ON={n_on:4d} OFF={n_off:5d} BG={bg:6.1f} S/N={sn:+.2f}σ")

    return results_bins


def plot_target_spectrum(name, cfg, bins_data, out_dir):
    """各天体別: 全13ビンの ON/OFF + S/N"""
    out_dir.mkdir(parents=True, exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), facecolor=C_BG,
                                   gridspec_kw={"height_ratios": [1.5, 1]})
    fig.suptitle(f"{cfg['label']} — 全13ビン ON/OFF + S/N スペクトル\n"
                 f"780週 Fermi-LAT | ON=2°, OFF=2°-5° | α={ALPHA:.4f}",
                 color="white", fontsize=13)

    e_cens = [b["e_center_gev"] for b in bins_data]
    sns    = [b["sn"] for b in bins_data]
    ons    = [b["n_on"] for b in bins_data]
    bgs    = [b["bg"] for b in bins_data]

    # 上パネル: ON カウント + 背景
    ax1.set_facecolor(C_BG)
    ax1.plot(e_cens, ons, "o-", color="#FFCC00", lw=1.5, ms=5, label="ON カウント")
    ax1.plot(e_cens, bgs, "s--", color="#00FFFF", lw=1.2, ms=4, label="背景推定 (α×OFF)")
    ax1.set_xscale("log")
    ax1.set_ylabel("カウント数", color="white")
    ax1.tick_params(colors="white")
    ax1.legend(facecolor="#111", labelcolor="white", fontsize=10)
    for sp in ax1.spines.values(): sp.set_color("white")

    # 下パネル: S/N スペクトル
    ax2.set_facecolor(C_BG)
    colors = [("#FF4400" if s > 2 else "#44FF88" if s < -2 else "#FFCC00") for s in sns]
    for ec, sn, col in zip(e_cens, sns, colors):
        ax2.bar(ec, sn, width=ec*0.4, color=col, alpha=0.8)
    ax2.axhline(0,  color="white", lw=0.8, ls="-")
    ax2.axhline( 2, color="#FF4400", lw=1.2, ls="--", alpha=0.7, label="+2σ")
    ax2.axhline(-2, color="#44CCFF", lw=1.2, ls="--", alpha=0.7, label="-2σ")
    ax2.axvline(20.76, color="#FFFFFF", lw=1.5, ls=":", alpha=0.9, label="Bin6 (20.76 GeV)")
    ax2.set_xscale("log")
    ax2.set_xlabel("光子エネルギー [GeV]", color="white")
    ax2.set_ylabel("有意度 S/N [σ]", color="white")
    ax2.tick_params(colors="white")
    ax2.legend(facecolor="#111", labelcolor="white", fontsize=9)
    for sp in ax2.spines.values(): sp.set_color("white")

    plt.tight_layout(pad=1.5)
    out = out_dir / name / f"bins13_{name}.png"
    (out_dir / name).mkdir(exist_ok=True)
    plt.savefig(out, dpi=130, bbox_inches="tight", facecolor=C_BG)
    plt.close()
    print(f"  → {out}")


def plot_all5_sn(all_results):
    """Totani Fig.8 相当: 全5天体の S/N スペクトル一枚"""
    fig, ax = plt.subplots(figsize=(13, 6), facecolor=C_BG)
    ax.set_facecolor(C_BG)
    fig.suptitle("矮小銀河5天体 — S/N スペクトル（Totani Fig.8 相当）\n"
                 "780週 Fermi-LAT | ON=2°, OFF=2°-5° | 水平線=Totaniの主要ビン(20.76 GeV)",
                 color="white", fontsize=12)

    for name, cfg in TARGETS.items():
        if name not in all_results or all_results[name] is None:
            continue
        bins = all_results[name]
        e_cens = [b["e_center_gev"] for b in bins]
        sns    = [b["sn"] for b in bins]
        ax.plot(e_cens, sns, "o-", color=cfg["color"], lw=1.5, ms=5,
                label=cfg["label"], alpha=0.9)

    ax.axhline(0,  color="white", lw=0.8)
    ax.axhline( 2, color="#FF4400", lw=1.2, ls="--", alpha=0.6)
    ax.axhline(-2, color="#44CCFF", lw=1.2, ls="--", alpha=0.6)
    ax.axvline(20.76, color="white", lw=1.5, ls=":", alpha=0.8,
               label="Totani 20 GeV ビン")
    ax.set_xscale("log")
    ax.set_xlabel("光子エネルギー [GeV]", color="white", fontsize=12)
    ax.set_ylabel("有意度 S/N [σ]", color="white", fontsize=12)
    ax.tick_params(colors="white")
    ax.legend(facecolor="#111", labelcolor="white", fontsize=11)
    for sp in ax.spines.values(): sp.set_color("white")
    ax.set_xlim(1, 900)
    ax.set_ylim(-4, 6)

    out = OUT_DIR / "all5_13bins_sn_spectrum.png"
    plt.savefig(out, dpi=130, bbox_inches="tight", facecolor=C_BG)
    plt.close()
    print(f"→ {out}")


def plot_all5_dchi2(all_results):
    """Totani Fig.9 相当: Δχ² = (S/N)² スペクトル"""
    fig, ax = plt.subplots(figsize=(13, 6), facecolor=C_BG)
    ax.set_facecolor(C_BG)
    fig.suptitle("矮小銀河5天体 — Δχ² = (S/N)² スペクトル（Totani Fig.9 相当）",
                 color="white", fontsize=12)

    for name, cfg in TARGETS.items():
        if name not in all_results or all_results[name] is None:
            continue
        bins = all_results[name]
        e_cens = [b["e_center_gev"] for b in bins]
        dchi2  = [b["sn"]**2 * np.sign(b["sn"]) for b in bins]
        ax.plot(e_cens, dchi2, "o-", color=cfg["color"], lw=1.5, ms=5,
                label=cfg["label"], alpha=0.9)

    ax.axhline(0, color="white", lw=0.8)
    ax.axvline(20.76, color="white", lw=1.5, ls=":", alpha=0.8,
               label="Totani 20 GeV ビン")
    ax.set_xscale("log")
    ax.set_xlabel("光子エネルギー [GeV]", color="white", fontsize=12)
    ax.set_ylabel("Δχ² = S/N² × sign(S/N)", color="white", fontsize=12)
    ax.tick_params(colors="white")
    ax.legend(facecolor="#111", labelcolor="white", fontsize=11)
    for sp in ax.spines.values(): sp.set_color("white")

    out = OUT_DIR / "all5_13bins_dchi2.png"
    plt.savefig(out, dpi=130, bbox_inches="tight", facecolor=C_BG)
    plt.close()
    print(f"→ {out}")


def plot_sigmav_comparison(all_results):
    """A案: σv 上限値 vs Totani の示唆値"""
    fig, ax = plt.subplots(figsize=(12, 7), facecolor=C_BG)
    ax.set_facecolor(C_BG)

    # Totaniの示唆するσv (mχ≈500 GeV, bb̄)
    TOTANI_SV = 6e-25

    for name, cfg in TARGETS.items():
        if name not in all_results or all_results[name] is None:
            continue
        bins = all_results[name]
        # Bin6 (20.76 GeV) の上限を代表値として使用
        bin6 = [b for b in bins if abs(b["e_center_gev"] - 20.76) < 5][0]
        sv   = bin6.get("sigmav_ul95")
        if sv and np.isfinite(sv):
            ax.errorbar([20.76], [sv], fmt="o", color=cfg["color"],
                        ms=8, label=f"{cfg['label']} (<σv> 95%UL, Bin6)")

    # Totaniの示唆値
    ax.axhline(TOTANI_SV, color="#FF4400", lw=2.5, ls="-",
               label=f"Totani (2025) 示唆値\n⟨σv⟩≈6×10⁻²⁵ cm³/s (mχ≈500 GeV, bb̄)")

    # 熱的遺物断面積
    ax.axhline(3e-26, color="#FFCC00", lw=1.5, ls="--",
               label="熱的遺物 ⟨σv⟩ ~ 3×10⁻²⁶ cm³/s")

    ax.set_xlabel("光子エネルギー [GeV]", color="white", fontsize=12)
    ax.set_ylabel("⟨σv⟩ [cm³/s]", color="white", fontsize=12)
    ax.set_title("矮小銀河5天体 σv 上限値 vs Totani (2025) 示唆値\n"
                 "（mχ = 500 GeV, bb̄ チャンネル, Bin6 = 20.76 GeV）",
                 color="white", fontsize=12)
    ax.set_yscale("log")
    ax.tick_params(colors="white")
    ax.legend(facecolor="#111", labelcolor="white", fontsize=10)
    for sp in ax.spines.values(): sp.set_color("white")

    out = OUT_DIR / "sigmav_comparison_totani.png"
    plt.savefig(out, dpi=130, bbox_inches="tight", facecolor=C_BG)
    plt.close()
    print(f"→ {out}")


def main():
    print("矮小銀河5天体 × 全13ビン解析開始\n")

    all_results = {}
    for name, cfg in TARGETS.items():
        print(f"--- {cfg['label']} ---")
        bins = analyze_target(name, cfg)
        all_results[name] = bins
        if bins:
            plot_target_spectrum(name, cfg, bins, OUT_DIR)
        print()

    print("全天体比較図を生成中...")
    plot_all5_sn(all_results)
    plot_all5_dchi2(all_results)
    plot_sigmav_comparison(all_results)

    # 結果を JSON 保存
    out_json = BASE / "results" / "dwarf_13bins_results.json"
    with open(out_json, "w") as f:
        json.dump({
            "method": "ON/OFF aperture (Li-Ma 1983 Eq.17)",
            "on_rad_deg": ON_RAD, "off_in_deg": OFF_IN, "off_out_deg": OFF_OUT,
            "alpha": ALPHA,
            "bin_centers_gev": BIN_CENTERS.tolist(),
            "targets": all_results
        }, f, indent=2, ensure_ascii=False)
    print(f"\n→ {out_json}")
    print("\n完了。")


if __name__ == "__main__":
    main()
