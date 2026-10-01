"""
Totani (2025) §2.2-2.3 準拠の MCMC 同時フィット（Bin6: 20.76 GeV）

等方背景は |b|≥50° 平均（2.443 cnt/pix）で固定し、
残り5成分を Poisson 最大尤度の MCMC でフィット：

  μ_i = ISO_LEVEL × 1
       + f_gal     × G_i   (GALPROP)
       + f_loopI_a × L_a_i (ループI 内シェル)
       + f_loopI_b × L_b_i (ループI 外シェル)
       + f_fb      × B_i   (フェルミバブル)
       + f_halo    × H_i   (NFW ハロー, 負も許容)

フィットパラメータ: θ = [f_gal, f_loopI_a, f_loopI_b, f_fb, f_halo]
（f_gal, f_loopI_a, f_loopI_b, f_fb ≥ 0; f_halo は自由）

出力:
  results/mcmc/mcmc_results_bin6.json
  results/mcmc/corner_bin6.png  (コーナープロット)
  results/mcmc/components_bin6.png (成分マップ)
"""
import pathlib as _pathlib

import sys
sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))

import numpy as np
import pandas as pd
import json
from pathlib import Path
import warnings; warnings.filterwarnings("ignore")
import emcee
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as mcolors
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"

import plot_skymap_all_subtracted as _sub

BASE    = _pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = BASE / "results/mcmc"
OUT_DIR.mkdir(parents=True, exist_ok=True)

EMIN, EMAX = 15.35, 28.07

# 等方背景固定値（|b|≥50° の平均 → Totani §2.3 と同じ考え方）
ISO_LEVEL = 2.443   # cnt/pix

PARAM_NAMES = ["f_gal", "f_loopI_a", "f_loopI_b", "f_fb", "f_halo"]
NDIM = len(PARAM_NAMES)

# Poisson尤度計算の有効ピクセル(Totani ROI: |b|>=10かつ|b|<=60。詳細は
# log_likelihood のコメント参照)
_L_C = (_sub.L_BINS[:-1] + _sub.L_BINS[1:]) / 2
_B_C = (_sub.B_BINS[:-1] + _sub.B_BINS[1:]) / 2
_, _BG_GRID = np.meshgrid(_L_C, _B_C, indexing="ij")
VALID_MASK = (np.abs(_BG_GRID) >= 10) & (np.abs(_BG_GRID) <= 60)

C_BG = "#05051A"
CMAP_DIV = LinearSegmentedColormap.from_list("totani_div", [
    (0.0, "#00FFFF"), (0.17, "#0000FF"), (0.33, "#000080"),
    (0.45, "#000020"), (0.50, "#000000"), (0.55, "#200000"),
    (0.67, "#800000"), (0.83, "#FF4400"), (0.92, "#FFCC00"),
    (1.0,  "#FFFF00"),
])


# ── データ＆テンプレート読み込み ─────────────────────────────────────────────

def load_data():
    print("データ読み込み中...")
    df = pd.read_csv(BASE / "data/CSV/filtered_events_week780.csv",
                     comment="#", low_memory=False)
    df = df[(df.b_deg.abs() >= 10) & (df.b_deg.abs() <= 60) &
            (df.l_deg.abs() <= 60)]
    sel = df[(df.energy_GeV >= EMIN) & (df.energy_GeV < EMAX)]
    raw, _, _ = np.histogram2d(sel.l_deg, sel.b_deg,
                                bins=[_sub.L_BINS, _sub.B_BINS])
    print(f"  Bin6 総カウント: {raw.sum():.0f}")
    return raw.astype(float)


def build_templates(counts):
    print("テンプレート構築中...")
    L_C = (_sub.L_BINS[:-1] + _sub.L_BINS[1:]) / 2
    B_C = (_sub.B_BINS[:-1] + _sub.B_BINS[1:]) / 2
    LG, BG = np.meshgrid(L_C, B_C, indexing="ij")

    # GALPROP — 物理フラックス単位 → カウント/pix に変換
    # G_raw 単位: ph/cm²/s/sr/MeV
    # カウント = G_raw × E_eff × ΔΩ × ΔE
    G_raw   = _sub._load_galprop_template(EMIN, EMAX)
    E_EFF   = 1.24e11            # cm²·s (Mrk 501 較正)
    # [2026-07-17 DPIX_SR cos(b) 修正] (l,b)グリッド1ピクセルの真の立体角
    # ΔΩ(b)=Δl·Δb·cos(b)=(π/180)^2·cos(b) [sr]。旧スカラー (π/180)^2 は b=0 でのみ正しく
    # |b|=60°で最大2倍過大評価。BG(shape=(120,120))と同形状の配列に変更(headline
    # mcmc_fit_all_bins.py と同期)。G_raw と要素ごとに掛かる。
    PIX_SOLID_ANGLE_SR = (np.pi/180)**2 * np.cos(np.radians(BG))  # 緯度依存 [sr]
    DE_MEV  = (EMAX - EMIN)*1000 # Bin6 幅 [MeV]
    G = G_raw * (E_EFF * PIX_SOLID_ANGLE_SR * DE_MEV)  # → counts/pix
    G_norm = G  # 物理単位のまま使う（f_gal ≈ 1.0 が標準）
    print(f"  GALPROP (物理変換後) 平均 = {G.mean():.3f} cnt/pix")

    # ループI（2シェル）
    LI_L, LI_B = -31.0, 18.0
    cos_ang = (np.sin(np.radians(BG)) * np.sin(np.radians(LI_B)) +
               np.cos(np.radians(BG)) * np.cos(np.radians(LI_B)) *
               np.cos(np.radians(LG - LI_L)))
    ang = np.degrees(np.arccos(np.clip(cos_ang, -1, 1)))
    L_a = ((ang >= 40) & (ang <= 55)).astype(float)
    L_b = ((ang >= 55) & (ang <= 70)).astype(float)

    # フェルミバブル — Bin3 カウントを Bin6 物理スケールに変換
    # フラットスペクトル(E²dN/dE=const) → Bin3→Bin6 変換係数
    # = (E3/E6)² × (ΔE6/ΔE3) × (Aeff6/Aeff3)
    # = (4.31/20.76)² × (12720/4700) × (7500/6000) = 0.1458
    BUBBLE_SCALE = 0.1458
    df_all = pd.read_csv(BASE / "data/CSV/filtered_events_week780.csv",
                         comment="#", low_memory=False)
    df_all = df_all[(df_all.b_deg.abs() >= 10) & (df_all.b_deg.abs() <= 60) &
                    (df_all.l_deg.abs() <= 60)]
    B_raw = _sub.build_fermi_bubble_template(df_all)
    B_pos = np.maximum(B_raw, 0) * BUBBLE_SCALE  # Bin6 カウント単位に変換
    print(f"  バブルテンプレート (Bin6換算) 最大 = {B_pos.max():.4f} cnt/pix")

    # NFW ハロー（視線積分 ρ²）
    print("  NFW J因子マップ計算中（数分かかります）...")
    D_SUN, RS = 8.0, 21.0
    def nfw_j(l_deg, b_deg, n_los=150):
        l_r = np.radians(l_deg); b_r = np.radians(b_deg)
        s = np.linspace(0.01, 60.0, n_los); ds = s[1] - s[0]
        r2 = D_SUN**2 + s**2 - 2*D_SUN*s*np.cos(b_r)*np.cos(l_r)
        r  = np.sqrt(np.maximum(r2, 0.01))
        x  = r / RS
        rho = 1.0 / (x * (1 + x)**2)
        return np.sum(rho**2 * ds)

    H = np.zeros_like(counts)
    for i, l in enumerate(L_C):
        for j, b in enumerate(B_C):
            if abs(b) >= 10:
                H[i, j] = nfw_j(l, b)
    # NFW を物理カウント単位に変換
    # Totani Fig.8: b=90°で E²dN/dE ≈ 3×10⁻⁵ MeV/cm²/s/sr at 21 GeV
    # → 0.0334 counts/pix at b=90°
    # H(b=90°, l=0°) = 14.065 (積分値)
    # → スケール = 0.0334 / 14.065 = 2.378×10⁻³
    NFW_SCALE = 2.378e-3  # counts/unit (f_halo=1 = Totani 検出レベル)
    H *= NFW_SCALE
    print(f"  NFW テンプレート (Bin6換算) b=10°最大 = {H.max():.4f} cnt/pix")

    templates = {
        "gal":      G_norm,
        "loopI_a":  L_a,
        "loopI_b":  L_b,
        "fb":       B_pos,
        "halo":     H,
    }
    print("  テンプレート構築完了")
    return templates


# ── MCMC ────────────────────────────────────────────────────────────────────

def make_mu(params, templates, iso_level):
    f_gal, f_la, f_lb, f_fb, f_halo = params
    mu = (iso_level
          + f_gal    * templates["gal"]
          + f_la     * templates["loopI_a"]
          + f_lb     * templates["loopI_b"]
          + f_fb     * templates["fb"]
          + f_halo   * templates["halo"])
    return np.maximum(mu, 1e-10)


def log_prior(params):
    f_gal, f_la, f_lb, f_fb, f_halo = params
    # 非負制約（ハロー以外）
    if any(p < 0 for p in [f_gal, f_la, f_lb, f_fb]):
        return -np.inf
    # 緩やかな上限（数値安定のため）
    if any(p > 1000 for p in params):
        return -np.inf
    return 0.0


def log_likelihood(params, counts, templates, iso_level):
    mu = make_mu(params, templates, iso_level)
    # [CRITICAL FIX 2026-07-11] L_BINS/B_BINSグリッドは|b|=-60〜60を覆うため、
    # Totani ROIで除外される|b|<10のピクセルも配列上に存在する。実データは
    # そこで常にカウント0だが、GALPROPテンプレートは銀河面に向かって急増する
    # ため除外しないと「counts=0の場所にmu最大259/pixelを予測」という
    # 壊滅的なPoissonペナルティが生じ、f_galが常にゼロに潰れる
    # (code/mcmc_fit_all_bins.pyで発見、詳細は.dev/CHANGELOG.md参照)。
    return float(np.sum(counts[VALID_MASK] * np.log(mu[VALID_MASK]) - mu[VALID_MASK]))


def log_probability(params, counts, templates, iso_level):
    lp = log_prior(params)
    if not np.isfinite(lp):
        return -np.inf
    ll = log_likelihood(params, counts, templates, iso_level)
    if not np.isfinite(ll):
        return -np.inf
    return lp + ll


def run_mcmc(counts, templates, iso_level,
             n_walkers=32, n_steps=2000, n_burn=500):

    from scipy.optimize import minimize

    # まず最適値を求める（MCMC の初期値に使う）
    print("初期最適解を計算中...")
    def neg_ll(p):
        if any(x < 0 for x in p[:4]):
            return 1e10
        return -log_likelihood(p, counts, templates, iso_level)

    # 物理較正後の初期値: f_gal≈1, f_loopI≈0, f_fb≈1, f_halo≈1
    x0 = [1.0, 0.5, 0.5, 1.0, 1.0]
    res = minimize(neg_ll, x0, method="Nelder-Mead",
                   options={"maxiter": 5000, "fatol": 1e-8})
    best = res.x
    print(f"  最適解: {dict(zip(PARAM_NAMES, best))}")
    print(f"  -lnL(MAP) = {res.fun:.2f}")

    # ハローなしフィット（f_halo=0 に固定して残りを最適化）
    def neg_ll_nohalo(p4):
        """f_halo=0 固定で4パラメータのみ最適化"""
        if any(x < 0 for x in p4):
            return 1e10
        params5 = list(p4) + [0.0]
        return -log_likelihood(params5, counts, templates, iso_level)

    from scipy.optimize import minimize as _min
    x0_nh4 = best[:4].copy()
    res_nh = _min(neg_ll_nohalo, x0_nh4, method="Nelder-Mead",
                  options={"maxiter": 5000, "fatol": 1e-8})
    # full likelihood at the no-halo optimum
    lnL_with  = -res.fun
    lnL_nohalo = log_likelihood(
        list(res_nh.x) + [0.0], counts, templates, iso_level
    )
    print(f"  lnL(with halo)  = {lnL_with:.2f}")
    print(f"  lnL(no-halo)    = {lnL_nohalo:.2f}")
    delta_lnL = lnL_with - lnL_nohalo   # > 0 なら halo あり
    significance = float(np.sqrt(2 * max(delta_lnL, 0)))
    print(f"  ΔlnL = {delta_lnL:.2f}  →  {significance:.2f}σ")

    # MCMC サンプリング
    print(f"\nMCMC 実行中（{n_walkers} walkers × {n_steps} steps）...")
    pos = best + 1e-3 * np.random.randn(n_walkers, NDIM)
    # ハロー以外は非負に clamp
    pos[:, :4] = np.abs(pos[:, :4])

    sampler = emcee.EnsembleSampler(
        n_walkers, NDIM, log_probability,
        args=(counts, templates, iso_level)
    )
    sampler.run_mcmc(pos, n_steps, progress=True)

    # バーンイン除去
    flat = sampler.get_chain(discard=n_burn, thin=5, flat=True)
    print(f"  有効サンプル数: {len(flat)}")

    return best, flat, delta_lnL, significance, sampler


# ── 出力図 ──────────────────────────────────────────────────────────────────

def plot_corner(flat, out_path):
    try:
        import corner
        labels = [r"$f_{\rm gal}$", r"$f_{\rm LI,A}$", r"$f_{\rm LI,B}$",
                  r"$f_{\rm fb}$", r"$f_{\rm halo}$"]
        fig = corner.corner(flat, labels=labels,
                            quantiles=[0.16, 0.5, 0.84],
                            show_titles=True, title_kwargs={"fontsize": 10})
        fig.suptitle("MCMC 事後分布（Bin6, 20.76 GeV）", fontsize=13, y=1.01)
        fig.savefig(out_path, dpi=120, bbox_inches="tight")
        plt.close()
        print(f"  → {out_path}")
    except ImportError:
        # corner がない場合は1次元ヒストグラム
        fig, axes = plt.subplots(1, NDIM, figsize=(15, 3), facecolor=C_BG)
        for ax, samples, name in zip(axes, flat.T, PARAM_NAMES):
            ax.set_facecolor(C_BG)
            ax.hist(samples, bins=50, color="#FFCC00", alpha=0.8)
            ax.set_title(name, color="white", fontsize=10)
            ax.tick_params(colors="white")
            for sp in ax.spines.values(): sp.set_color("white")
        fig.tight_layout()
        fig.savefig(out_path, dpi=120, bbox_inches="tight", facecolor=C_BG)
        plt.close()
        print(f"  → {out_path}")


def plot_components(counts, templates, best, flat, out_path):
    L_C = (_sub.L_BINS[:-1] + _sub.L_BINS[1:]) / 2
    B_C = (_sub.B_BINS[:-1] + _sub.B_BINS[1:]) / 2

    medians = np.median(flat, axis=0)
    mu_best = make_mu(medians, templates, ISO_LEVEL)
    residual = counts - mu_best

    fig, axes = plt.subplots(2, 4, figsize=(20, 9), facecolor=C_BG)
    fig.suptitle(
        f"MCMC 同時フィット結果 — Bin6 (20.76 GeV)\n"
        f"等方背景固定 {ISO_LEVEL:.3f} cnt/pix | "
        f"f_halo = {medians[-1]:.4f}",
        color="white", fontsize=13, y=1.01
    )
    comps = [
        ("観測データ", counts),
        (f"GALPROP (f={medians[0]:.4f})", medians[0]*templates["gal"]),
        (f"ループI-A (f={medians[1]:.3f})", medians[1]*templates["loopI_a"]),
        (f"ループI-B (f={medians[2]:.3f})", medians[2]*templates["loopI_b"]),
        (f"バブル (f={medians[3]:.3f})", medians[3]*templates["fb"]),
        (f"NFWハロー (f={medians[4]:.4f})", medians[4]*templates["halo"]),
        (f"モデル合計", mu_best),
        (f"残差 (データ−モデル)", residual),
    ]
    for ax, (title, data) in zip(axes.flatten(), comps):
        ax.set_facecolor(C_BG)
        fin = data[np.isfinite(data)]
        vmax = float(np.nanpercentile(np.abs(fin), 99.5)) if len(fin) else 1.0
        vmax = max(vmax, 0.1)
        im = ax.pcolormesh(L_C, B_C, data.T,
                           norm=mcolors.Normalize(-vmax, vmax),
                           cmap=CMAP_DIV, shading="auto")
        cb = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
        cb.ax.yaxis.set_tick_params(labelsize=7, color="white")
        plt.setp(cb.ax.yaxis.get_ticklabels(), color="white", fontsize=7)
        ax.set_xlim(60, -60); ax.set_ylim(-60, 60)
        ax.set_title(title, color="white", fontsize=9)
        ax.tick_params(colors="white", labelsize=7)
        for sp in ax.spines.values(): sp.set_color("white")
    fig.tight_layout(pad=1.5)
    fig.savefig(out_path, dpi=110, bbox_inches="tight", facecolor=C_BG)
    plt.close()
    print(f"  → {out_path}")


# ── メイン ───────────────────────────────────────────────────────────────────

def main():
    counts    = load_data()
    templates = build_templates(counts)

    best, flat, delta_lnL, sig, sampler = run_mcmc(
        counts, templates, ISO_LEVEL,
        n_walkers=32, n_steps=2000, n_burn=500
    )

    medians = np.median(flat, axis=0)
    lo, hi  = np.percentile(flat, [16, 84], axis=0)

    print("\n=== MCMC 結果（中央値 ± 1σ）===")
    for name, med, l, h in zip(PARAM_NAMES, medians, lo, hi):
        print(f"  {name:12s} = {med:.4f}  +{h-med:.4f} / -{med-l:.4f}")
    print(f"\n  ΔlnL（ハローあり vs なし）= {delta_lnL:.2f}")
    print(f"  有意度 = {sig:.2f}σ")
    print(f"  等方背景 f_iso（固定）= {ISO_LEVEL:.3f} cnt/pix")

    # 結果保存
    result = {
        "method": "MCMC (emcee, Poisson log-likelihood)",
        "iso_level_fixed": ISO_LEVEL,
        "n_walkers": 32, "n_steps": 2000, "n_burn": 500,
        "params": {
            n: {"median": float(m), "lo16": float(l), "hi84": float(h)}
            for n, m, l, h in zip(PARAM_NAMES, medians, lo, hi)
        },
        "delta_lnL": float(delta_lnL),
        "significance_sigma": float(sig),
    }
    out_json = OUT_DIR / "mcmc_results_bin6.json"
    with open(out_json, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\n→ {out_json}")

    print("\n図を生成中...")
    plot_corner(flat, OUT_DIR / "corner_bin6.png")
    plot_components(counts, templates, best, flat,
                    OUT_DIR / "components_bin6.png")

    print("\n完了。")
    return result


if __name__ == "__main__":
    main()
