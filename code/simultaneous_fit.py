"""
Totani (2025) §2.2-2.3 に準拠した同時フィット

全成分を Poisson 最大尤度で同時フィット：
  観測カウント = f_iso × 1
              + f_gal × (GALPROP テンプレート)
              + f_loopI_a × (ループI 内シェル)
              + f_loopI_b × (ループI 外シェル)
              + f_fb × (フェルミバブルテンプレート)
              + f_halo × (NFW J因子マップ)

各係数 f_xxx ≥ 0 で最適化（ただし f_halo は負も許容）

出力:
  results/simultaneous_fit/fit_result_bin6.json  — フィット結果
  results/simultaneous_fit/fit_components_bin6.png — 成分マップ
"""
import pathlib as _pathlib

import sys
sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))

import numpy as np
import pandas as pd
from pathlib import Path
import json
import warnings
warnings.filterwarnings("ignore")
from scipy.optimize import minimize
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
import matplotlib
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"

import plot_skymap_all_subtracted as _sub

BASE    = _pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = BASE / "results/simultaneous_fit"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Bin6
EMIN, EMAX, ECEN = 15.35, 28.07, 20.76

L_C = (_sub.L_BINS[:-1] + _sub.L_BINS[1:]) / 2
B_C = (_sub.B_BINS[:-1] + _sub.B_BINS[1:]) / 2
B_ABS = np.abs(B_C)


def load_data():
    print("データ読み込み中...")
    df = pd.read_csv(BASE / "data/CSV/filtered_events_week780.csv",
                     comment="#", low_memory=False)
    df = df[(df.b_deg.abs() >= 10) & (df.b_deg.abs() <= 60) &
            (df.l_deg.abs() <= 60)]
    sel = df[(df.energy_GeV >= EMIN) & (df.energy_GeV < EMAX)]
    raw, _, _ = np.histogram2d(sel.l_deg, sel.b_deg,
                                bins=[_sub.L_BINS, _sub.B_BINS])
    return raw.astype(float)


def build_templates(counts):
    """全テンプレートを (N_l, N_b) の配列として返す"""
    templates = {}

    # ① 等方背景テンプレート：全ピクセルで 1（定数）
    templates["iso"] = np.ones_like(counts)

    # ② GALPROP テンプレート（raw）
    templates["gal"] = _sub._load_galprop_template(EMIN, EMAX)

    # ③ Loop I テンプレート（2シェル独立）
    from astropy.coordinates import SkyCoord
    import astropy.units as u

    # ループI 中心: l=-31°, b=18°（Wolleben 2007）
    LI_L, LI_B = -31.0, 18.0
    LG, BG = np.meshgrid(L_C, B_C, indexing="ij")
    # 角度距離計算（球面三角法）
    cos_ang = (np.sin(np.radians(BG)) * np.sin(np.radians(LI_B)) +
               np.cos(np.radians(BG)) * np.cos(np.radians(LI_B)) *
               np.cos(np.radians(LG - LI_L)))
    cos_ang = np.clip(cos_ang, -1, 1)
    ang = np.degrees(np.arccos(cos_ang))  # GC からの角度

    # 内シェル: 40–55°、外シェル: 55–70°
    li_a = ((ang >= 40) & (ang <= 55)).astype(float)
    li_b = ((ang >= 55) & (ang <= 70)).astype(float)
    templates["loopI_a"] = li_a
    templates["loopI_b"] = li_b

    # ④ フェルミバブルテンプレート（Bin3残差から構築）
    bubble_tmpl = _sub.build_fermi_bubble_template(
        pd.read_csv(BASE / "data/CSV/filtered_events_week780.csv",
                    comment="#", low_memory=False)
        .pipe(lambda d: d[(d.b_deg.abs() >= 10) & (d.b_deg.abs() <= 60) &
                          (d.l_deg.abs() <= 60)])
    )
    # 負値をゼロにクリップ（テンプレートは非負）
    templates["fb"] = np.maximum(bubble_tmpl, 0)

    # ⑤ NFW ハローテンプレート（J因子マップ）
    # ρ² の視線積分：NFW-ρ²（消滅）
    D_SUN = 8.0  # kpc
    RS    = 21.0  # kpc（スケール半径）

    def nfw_j(l_deg, b_deg, n_los=200):
        """NFW ρ² の視線積分（近似）"""
        l_rad = np.radians(l_deg)
        b_rad = np.radians(b_deg)
        s_max = 60.0  # kpc
        s = np.linspace(0.01, s_max, n_los)
        ds = s[1] - s[0]
        # 太陽から視線方向の距離 s での GC からの距離
        r2 = (D_SUN**2 + s**2 - 2*D_SUN*s*np.cos(b_rad)*np.cos(l_rad))
        r = np.sqrt(np.maximum(r2, 0.01))
        x = r / RS
        rho = 1.0 / (x * (1 + x)**2)  # NFW
        return np.sum(rho**2 * ds)

    nfw = np.zeros_like(counts)
    for i, l in enumerate(L_C):
        for j, b in enumerate(B_C):
            if abs(b) >= 10:
                nfw[i, j] = nfw_j(l, b)
    # 最大値で規格化
    nfw /= nfw[np.isfinite(nfw) & (nfw > 0)].max()
    templates["halo"] = nfw

    return templates


def poisson_nll(params, counts, templates, names):
    """ポアソン負対数尤度（最小化するので -ln L）"""
    mu = np.zeros_like(counts)
    for i, name in enumerate(names):
        mu += params[i] * templates[name]
    # mu が負になると log が計算できないのでクリップ
    mu = np.maximum(mu, 1e-10)
    # -ln L = Σ (mu - N*ln(mu))
    return np.sum(mu - counts * np.log(mu))


def run_fit(counts, templates):
    names = ["iso", "gal", "loopI_a", "loopI_b", "fb", "halo"]
    n = len(names)

    # 初期値
    # iso: |b|≥50° の従来推定値
    iso_init = float(counts[:, B_ABS >= 50].mean())
    # gal: GALPROP をスケール調整
    gal_max = float(templates["gal"].max())
    x0 = np.array([iso_init, 0.01, 0.5, 0.3, 0.1, 0.0])

    # 制約：iso, gal, loopI_a, loopI_b, fb は ≥ 0
    #        halo は負も許容（Totani に準拠）
    bounds = [
        (0.0, None),   # iso
        (0.0, None),   # gal
        (0.0, None),   # loopI_a
        (0.0, None),   # loopI_b
        (0.0, None),   # fb
        (None, None),  # halo（負も許容）
    ]

    print("フィット実行中...")
    result = minimize(
        poisson_nll,
        x0,
        args=(counts, templates, names),
        method="L-BFGS-B",
        bounds=bounds,
        options={"maxiter": 2000, "ftol": 1e-12}
    )

    if not result.success:
        print(f"  警告: {result.message}")

    # 結果まとめ
    fit = {name: float(result.x[i]) for i, name in enumerate(names)}
    fit["nll"] = float(result.fun)
    fit["success"] = bool(result.success)

    # ハローなしフィット（有意度計算用）
    x0_nohalo = result.x.copy()
    x0_nohalo[-1] = 0.0
    bounds_nohalo = bounds[:-1] + [(0.0, 0.0)]
    result_nohalo = minimize(
        poisson_nll, x0_nohalo,
        args=(counts, templates, names),
        method="L-BFGS-B", bounds=bounds_nohalo,
        options={"maxiter": 2000, "ftol": 1e-12}
    )
    fit["nll_nohalo"] = float(result_nohalo.fun)
    fit["delta_nll"] = float(result_nohalo.fun - result.fun)  # > 0 なら halo あり
    fit["significance_sigma"] = float(np.sqrt(2 * max(fit["delta_nll"], 0)))

    # 旧手法の等方背景値（比較用）
    fit["iso_old_method"] = float(counts[:, B_ABS >= 50].mean())

    return fit, names, result.x


def make_figure(counts, templates, names, params, fit):
    fig, axes = plt.subplots(2, 4, figsize=(20, 9), facecolor="#05051A")
    fig.suptitle(
        f"Bin6 (20.76 GeV) 同時フィット結果\n"
        f"等方背景: 旧={fit['iso_old_method']:.3f} cnt/pix → "
        f"新（同時フィット）={fit['iso']:.3f} cnt/pix | "
        f"ΔlnL={fit['delta_nll']:.1f} → {fit['significance_sigma']:.1f}σ",
        color="white", fontsize=13, y=1.01
    )

    CMAP_DIV = LinearSegmentedColormap.from_list("totani_div", [
        (0.0, "#00FFFF"), (0.17, "#0000FF"), (0.33, "#000080"),
        (0.45, "#000020"), (0.50, "#000000"), (0.55, "#200000"),
        (0.67, "#800000"), (0.83, "#FF4400"), (0.92, "#FFCC00"),
        (1.0,  "#FFFF00"),
    ])

    LG, BG = np.meshgrid(L_C, B_C, indexing="ij")

    plot_items = [
        ("観測データ", counts),
        (f"等方背景\n(f={fit['iso']:.3f})", params[0] * templates["iso"]),
        (f"GALPROP\n(f={fit['gal']:.4f})", params[1] * templates["gal"]),
        (f"ループI-A\n(f={fit['loopI_a']:.3f})", params[2] * templates["loopI_a"]),
        (f"ループI-B\n(f={fit['loopI_b']:.3f})", params[3] * templates["loopI_b"]),
        (f"フェルミバブル\n(f={fit['fb']:.3f})", params[4] * templates["fb"]),
        (f"NFWハロー\n(f={fit['halo']:.4f})", params[5] * templates["halo"]),
        ("残差\n(データ − モデル合計)",
         counts - sum(params[i] * templates[n] for i, n in enumerate(names))),
    ]

    axes_flat = axes.flatten()
    for ax, (title, data) in zip(axes_flat, plot_items):
        ax.set_facecolor("#05051A")
        fin = data[np.isfinite(data)]
        vmax = float(np.nanpercentile(np.abs(fin), 99.5)) if len(fin) else 1.0
        vmax = max(vmax, 0.1)
        im = ax.pcolormesh(L_C, B_C, data.T,
                           norm=mcolors.Normalize(vmin=-vmax, vmax=vmax),
                           cmap=CMAP_DIV, shading="auto")
        cbar = plt.colorbar(im, ax=ax)
        cbar.ax.yaxis.set_tick_params(labelsize=8, color="white")
        plt.setp(cbar.ax.yaxis.get_ticklabels(), color="white")
        ax.set_xlim(60, -60)
        ax.set_ylim(-60, 60)
        ax.set_title(title, color="white", fontsize=10)
        ax.tick_params(colors="white", labelsize=8)
        for sp in ax.spines.values(): sp.set_color("white")

    fig.tight_layout(pad=1.5)
    out = OUT_DIR / "fit_components_bin6.png"
    plt.savefig(out, dpi=120, bbox_inches="tight", facecolor="#05051A")
    plt.close()
    print(f"  → {out}")


def main():
    counts = load_data()
    print(f"  Bin6 総カウント: {counts.sum():.0f}")

    print("テンプレート構築中（NFW 計算に数分かかります）...")
    templates = build_templates(counts)

    fit, names, params = run_fit(counts, templates)

    print("\n=== フィット結果 ===")
    print(f"  等方背景 f_iso    = {fit['iso']:.4f} cnt/pix")
    print(f"  （旧手法 |b|≥50° 平均 = {fit['iso_old_method']:.4f} cnt/pix）")
    print(f"  GALPROP  f_gal    = {fit['gal']:.6f}")
    print(f"  ループI-A f_loopI_a = {fit['loopI_a']:.4f}")
    print(f"  ループI-B f_loopI_b = {fit['loopI_b']:.4f}")
    print(f"  バブル    f_fb     = {fit['fb']:.4f}")
    print(f"  NFWハロー f_halo   = {fit['halo']:.6f}")
    print(f"  ΔlnL（ハローあり vs なし）= {fit['delta_nll']:.2f}")
    print(f"  有意度 = {fit['significance_sigma']:.2f}σ")

    # 結果保存
    out_json = OUT_DIR / "fit_result_bin6.json"
    with open(out_json, "w") as f:
        json.dump(fit, f, indent=2, ensure_ascii=False)
    print(f"\n  → {out_json}")

    print("図を生成中...")
    make_figure(counts, templates, names, params, fit)
    print("完了。")
    return fit


if __name__ == "__main__":
    main()
