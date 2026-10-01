#!/usr/bin/env python3
"""
矮小銀河 ON/OFF アパーチャ設定（半径・面積比 alpha）の物理的根拠を可視化する。

教授指摘（2026-05-22, ROI設定について）「半径や面積比 alpha をどうやって決めたのか
説明してほしい」への対応。plot_dwarf_pipeline.py の ON_RAD/OFF_RAD/ALPHA は
天下り的に与えていたため、ここで根拠を 2 つの図で示す。

根拠 1: ON_RAD = 2.0° は LAT PSF（68%収容角）の観点で最低エネルギービン
        （1.51 GeV）でも信号をほぼ完全に収容できる半径か
  - Totani (2025) §2.1 (p.3): 「68% containment angle は 1, 10, 100 GeV で
    それぞれ 0.85°, 0.16°, 0.10°」(出典 [41] = LAT performance ページ)
  - この 3 点を E^p 形のべき乗則で補間し、解析する最低エネルギー (1.51 GeV)
    での 68%/95% 収容角を見積もる
  - 95% 収容角は King 関数 PSF で概ね 68% 収容角の 1.5-2 倍程度
    （厳密な係数は IRF 依存だが、ここでは 1.7 倍を仮定して上限の目安とする
    -- assumption であることを明示）
  - ON_RAD=2.0° が 1.51 GeV での 95% 収容角の見積りを上回ることを確認する

根拠 2: alpha = ON²/(OFF²-ON²)（円環の面積比）が妥当であるための前提条件
        「OFF リング内で背景が局所一様」を、実データで直接検証する
  - OFF リング (2.0-5.0°) を 4 分割した副リングごとに光子の面密度
    [counts/deg^2] を計算し、ばらつき（max/min 比）を定量化する
  - 4 天体は ~3-11% の範囲に収まり一様性を支持する一方、Coma Ber のみ
    内側リングが外側の ~2.5 倍の密度となる -- これは plot_dwarf_pipeline.py
    で見つかった「ON 領域内 4FGL 点源 3 個」と独立に整合し、Coma Ber の
    "信号" が点源混入由来であることのもう一つの証拠となる

出力: data/figure-roi-rationale/on_off_aperture_rationale.png
      data/figure-roi-rationale/off_ring_uniformity_table.txt
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUT_DIR = DATA_DIR / "figure-roi-rationale"
OUT_DIR.mkdir(parents=True, exist_ok=True)

ON_RAD = 2.0
OFF_RAD = 5.0
ALPHA = ON_RAD**2 / (OFF_RAD**2 - ON_RAD**2)
E_LOW_BIN = 1.51   # Totani (2025) Bin1 中心エネルギー [GeV] -- 解析する最低エネルギー

# Totani (2025) §2.1 (p.3, 本文): 「68% containment angles は 1, 10, 100 GeV で
# それぞれ 0.85°, 0.16°, 0.10°」(出典: 脚注 [41] = LAT performance ページ)
# observation: 論文本文に明記された値そのもの（再計算ではない）
PSF_E_GEV   = np.array([1.0, 10.0, 100.0])
PSF_R68_DEG = np.array([0.85, 0.16, 0.10])

# assumption: 95% containment / 68% containment 比。King 関数形 PSF では
# この比はおよそ 1.5-2 程度（IRF・エネルギー依存）。ここでは 1.7 を仮定し、
# 「上限の目安」として扱う（精密な値は gtpsf 等の IRF 計算が必要、後回し）。
R95_OVER_R68_ASSUMED = 1.7


def fit_psf_powerlaw():
    """68% containment角 R68(E) = A * E^p を3点フィット (loglog線形回帰)。"""
    logE = np.log10(PSF_E_GEV)
    logR = np.log10(PSF_R68_DEG)
    p, logA = np.polyfit(logE, logR, 1)
    A = 10**logA
    return A, p


def panel_psf_rationale(ax):
    A, p = fit_psf_powerlaw()
    E_grid = np.logspace(np.log10(0.5), np.log10(200), 200)
    R68_grid = A * E_grid**p
    R95_grid = R95_OVER_R68_ASSUMED * R68_grid

    R68_low = A * E_LOW_BIN**p
    R95_low = R95_OVER_R68_ASSUMED * R68_low

    ax.set_facecolor("#0d0d2a")
    ax.plot(E_grid, R68_grid, color="#4488ff", lw=2,
            label=r"$R_{68}$ (Totani 2025 §2.1 実測値をべき乗則補間, $\propto E^{%.2f}$)" % p)
    ax.plot(E_grid, R95_grid, color="#ff8844", lw=2, ls="--",
            label=r"$R_{95} \approx %.1f \times R_{68}$ (assumption: King PSF 形状から)" % R95_OVER_R68_ASSUMED)
    ax.scatter(PSF_E_GEV, PSF_R68_DEG, color="#4488ff", s=70, zorder=5, edgecolor="white",
               label=r"$R_{68}$ 実測値 (Totani 2025, [41]: 0.85°/0.16°/0.10° @ 1/10/100 GeV)")

    ax.axhline(ON_RAD, color="#44ff88", lw=2, ls=":", label=f"ON_RAD = {ON_RAD:.1f}°（採用値）")
    ax.axvline(E_LOW_BIN, color="gold", lw=1.3, ls="-.", alpha=0.8,
               label=f"最低解析エネルギー Bin1 = {E_LOW_BIN:.2f} GeV")

    ax.scatter([E_LOW_BIN], [R95_low], color="#ff8844", marker="D", s=90, zorder=6,
               edgecolor="white")
    ax.annotate(f"$R_{{95}}$({E_LOW_BIN:.2f} GeV) ≈ {R95_low:.2f}°\n"
                f"($R_{{68}}$ ≈ {R68_low:.2f}° → ON_RAD/$R_{{95}}$ ≈ {ON_RAD/R95_low:.1f})",
                xy=(E_LOW_BIN, R95_low), xytext=(2.0, R95_low * 2.6),
                color="white", fontsize=9, ha="left",
                arrowprops=dict(arrowstyle="->", color="white", alpha=0.7))

    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("Photon energy [GeV]", color="white")
    ax.set_ylabel("PSF containment radius [deg]", color="white")
    ax.set_title("根拠1: ON_RAD=2.0° は最低エネルギー(1.51 GeV)でも\nLAT PSF の収容角を十分上回る",
                 color="white", fontsize=11)
    ax.tick_params(colors="white")
    ax.legend(fontsize=7.5, loc="lower left", facecolor="#05051a", labelcolor="white", framealpha=0.9)
    ax.grid(alpha=0.2, which="both")
    for sp in ax.spines.values():
        sp.set_edgecolor("#444")


def compute_off_ring_uniformity(targets):
    """OFFリング(2.0-5.0°)を4分割し、副リングごとの面密度[counts/deg^2]を算出。"""
    sub_edges = np.array([ON_RAD, 2.6, 3.3, 4.1, OFF_RAD])
    sub_areas = np.pi * (sub_edges[1:]**2 - sub_edges[:-1]**2)
    rows = []
    for name, _ra, _dec, label in targets:
        csv_path = DATA_DIR / "CSV" / "dwarfs" / f"dwarf_{name}_780w.csv"
        if not csv_path.exists():
            continue
        d = pd.read_csv(csv_path)["ang_dist_deg"].values
        dens = np.array([
            ((d >= sub_edges[i]) & (d < sub_edges[i + 1])).sum() / sub_areas[i]
            for i in range(4)
        ])
        rows.append((name, label, dens))
    return sub_edges, rows


def panel_uniformity(ax, sub_edges, rows):
    n_target = len(rows)
    n_sub = len(sub_edges) - 1
    width = 0.8 / n_target
    centers = 0.5 * (sub_edges[:-1] + sub_edges[1:])
    cmap = plt.get_cmap("plasma")

    ax.set_facecolor("#0d0d2a")
    for i, (name, label, dens) in enumerate(rows):
        x = np.arange(n_sub) + (i - (n_target - 1) / 2) * width
        ratio = dens.max() / dens.min()
        marker = " ⚠" if ratio > 1.5 else ""
        color = "#ff4444" if ratio > 1.5 else cmap(i / max(n_target - 1, 1))
        ax.bar(x, dens, width=width * 0.92, color=color, edgecolor="white", linewidth=0.4,
               label=f"{label}: max/min={ratio:.2f}{marker}")

    ax.set_xticks(np.arange(n_sub))
    ax.set_xticklabels([f"[{sub_edges[i]:.1f}, {sub_edges[i+1]:.1f}]°"
                        for i in range(n_sub)], color="white", fontsize=9)
    ax.set_xlabel("OFF リング内の副リング (中心からの角距離)", color="white")
    ax.set_ylabel(r"光子面密度 [counts / deg$^2$] (全エネルギー, $E$>1.51 GeV)", color="white")
    ax.set_title(r"根拠2: $\alpha$=ON²/(OFF²-ON²) の前提「OFF内で背景が局所一様」を検証"
                 "\n(Coma Ber のみ内側リングで密度超過 → 点源混入と独立に整合)",
                 color="white", fontsize=10.5)
    ax.tick_params(colors="white")
    ax.legend(fontsize=7.5, loc="upper right", facecolor="#05051a", labelcolor="white", framealpha=0.9)
    ax.grid(alpha=0.2, axis="y")
    for sp in ax.spines.values():
        sp.set_edgecolor("#444")


def write_table(sub_edges, rows):
    out = OUT_DIR / "off_ring_uniformity_table.txt"
    lines = [
        "# OFF リング (2.0-5.0 deg) 副リング面密度 [counts/deg^2] (全エネルギー E>1.51 GeV)",
        "# alpha = ON^2/(OFF^2-ON^2) は『OFFリング内で背景が局所一様』が前提。",
        "# max/min が 1 に近いほど一様性が高い。",
        "# target       " + "  ".join(f"[{sub_edges[i]:.1f},{sub_edges[i+1]:.1f}]" for i in range(4))
        + "      max/min",
    ]
    for name, label, dens in rows:
        ratio = dens.max() / dens.min()
        flag = "  <- 一様性が崩れている（点源混入の疑い、要マスク再計算）" if ratio > 1.5 else ""
        lines.append(f"{name:12s} " + "  ".join(f"{v:9.2f}" for v in dens)
                     + f"   {ratio:6.3f}{flag}")
    out.write_text("\n".join(lines) + "\n")
    print(f"  -> {out}")


def main():
    from plot_dwarf_pipeline import TARGETS  # 既存 5 天体リストを再利用（重複定義を避ける）

    print("ROI / ON-OFF アパーチャ設定の物理的根拠を図示")
    print(f"ON_RAD={ON_RAD}°, OFF_RAD={OFF_RAD}°, alpha={ALPHA:.6f} (=4/21)")

    sub_edges, rows = compute_off_ring_uniformity(TARGETS)

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    fig.patch.set_facecolor("#05051a")
    fig.suptitle("矮小銀河 ON/OFF アパーチャ設定（半径・面積比 α）の物理的根拠",
                 color="white", fontsize=14, fontweight="bold")

    panel_psf_rationale(axes[0])
    panel_uniformity(axes[1], sub_edges, rows)

    fig.tight_layout(rect=[0, 0, 1, 0.94])
    out = OUT_DIR / "on_off_aperture_rationale.png"
    fig.savefig(out, dpi=140, bbox_inches="tight", facecolor="#05051a")
    plt.close(fig)
    print(f"  -> {out}")

    write_table(sub_edges, rows)
    print("完了 ->", OUT_DIR)


if __name__ == "__main__":
    main()
