import pathlib as _pathlib
#!/usr/bin/env python3
"""
5成分逐次差引き — 各成分ごとに 3パネル可視化
  左: 差引き前の skymap
  中: 差引くテンプレートの形状
  右: 差引き後の skymap

出力: data/figure-5component/
  comp01_isotropic_3panel.png
  comp02_galprop_3panel.png
  comp03_pointsource_3panel.png
  comp04_fermi_bubble_3panel.png
  comp05_loop_i_3panel.png
  all5_overview.png  (5成分まとめ俯瞰図)

対応する Totani (2025) Figure:
  Fig.1   → comp04 のバブルテンプレート
  Fig.14  → comp02 GALPROP gas, comp05 Loop I テンプレート
"""
import sys
sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap

# Totani (2025) Fig.11-13 に準拠: 差し引き後は発散型、テンプレートは hot
CMAP_DIV = LinearSegmentedColormap.from_list(
    "totani_div",
    [
        (0.000, "#00FFFF"),
        (0.170, "#0000FF"),
        (0.330, "#000080"),
        (0.450, "#000020"),
        (0.500, "#000000"),
        (0.550, "#200000"),
        (0.670, "#800000"),
        (0.830, "#FF4400"),
        (0.920, "#FFCC00"),
        (1.000, "#FFFF00"),
    ],
)
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"

from pathlib import Path
import plot_skymap_all_subtracted as _sub

BASE    = _pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = BASE / "data/figure-5component"
OUT_DIR.mkdir(parents=True, exist_ok=True)
CSV_PATH = BASE / "data/CSV/filtered_events_week780.csv"

# Bin6 (20.76 GeV)
BIN_IDX = 5
EMIN = _sub.BIN_EDGES[BIN_IDX]
EMAX = _sub.BIN_EDGES[BIN_IDX + 1]
ECEN = _sub.BIN_CENTERS[BIN_IDX]

L_BINS, B_BINS = _sub.L_BINS, _sub.B_BINS
L_CENTERS, B_CENTERS = _sub.L_CENTERS, _sub.B_CENTERS
L_GRID, B_GRID = _sub.L_GRID, _sub.B_GRID

# ── データ読み込み ──
print(f"CSV 読み込み (Bin6 {ECEN:.1f} GeV)...")
df = pd.read_csv(CSV_PATH, comment="#", low_memory=False)
sel = df[(df["energy_GeV"] >= EMIN) & (df["energy_GeV"] < EMAX)]
raw_2d, _, _ = np.histogram2d(sel["l_deg"], sel["b_deg"], bins=[L_BINS, B_BINS])
raw_2d = raw_2d.astype(float)

print(f"  Bin6: {int(raw_2d.sum())} events")

# ── 全バブルテンプレート作成 ──
print("バブルテンプレート構築中...")
df_all = pd.read_csv(CSV_PATH, comment="#", low_memory=False)
bubble_template = _sub.build_fermi_bubble_template(df_all)


# ── 差引きパイプラインを逐次実行してスナップショットを取得 ──
steps = {}

# Step 0: 生データ
steps["raw"] = raw_2d.copy()

# Step 1: 等方背景差引き
step1, iso_level = _sub.subtract_isotropic(raw_2d.copy())
steps["after_iso"] = step1.copy()
steps["template_iso"] = np.full_like(raw_2d, iso_level)

# Step 2: GALPROP差引き
step2, galprop_sub, _ = _sub.subtract_galactic_diffuse(step1.copy(), EMIN, EMAX)
steps["after_galprop"] = step2.copy()
# 中央パネル表示用: 生テンプレート (A*tmpl+offset は offset ≈ 3 で均一に見えるため)
# Totani Fig.14 と同様に gll_iem_v07.fits の空間構造を表示
steps["template_galprop"] = _sub._load_galprop_template(EMIN, EMAX)

# Step 3: 点源差し引き（スペクトルモデル×較正済み露出量）
step3, ps_submap, n_masked = _sub.subtract_point_sources(step2.copy(), EMIN, EMAX)
steps["after_ps"] = step3.copy()
# 中央パネル: 差し引いたカウントマップ（点源ごとの貢献量を可視化）
steps["template_ps"] = ps_submap

# Step 4: フェルミバブル差引き
step4, bubble_amp, bubble_sub = _sub.subtract_fermi_bubbles(step3.copy(), bubble_template)
steps["after_bubble"] = step4.copy()
steps["template_bubble"] = bubble_sub

# Step 5: ループI差引き（2026-07-12更新: Ackermann+2014/2017の2シェル3次元モデル）
step5, li_a1, li_a2 = _sub.subtract_loop_i(step4.copy())
steps["after_loopi"] = step5.copy()
# Loop I テンプレート: 実際に差し引いた振幅×シェル形状を可視化
_shell1, _shell2 = _sub.loop_i_shell_templates()
steps["template_loopi"] = li_a1 * _shell1 + li_a2 * _shell2

print(f"  等方背景: {iso_level:.3f} cnt/pix")
print(f"  GALPROP総差引量: {np.nansum(galprop_sub):.1f} cnt")
print(f"  点源マスク数: {n_masked}")
print(f"  バブル振幅: {bubble_amp:.4f}")
print(f"  LoopI (shell1/shell2振幅): {li_a1:.4f}/{li_a2:.4f}")


# ── 補助: skymap プロット関数 ──
def plot_skymap(ax, data, title, vmin=None, vmax=None, cmap="hot",
                log=False, cbar_label="counts/pixel",
                show_disk_mask=True, show_nfw_circles=True):
    """
    2D skymap を l-b 座標でプロット。
    data shape: (n_l, n_b), axes: l-axis × b-axis
    """
    # データをプロット用に転置: pcolormesh は (n_b, n_l) を期待
    d = data.T  # (n_b, n_l)

    if log:
        d_plot = np.where(d > 0, d, np.nan)
        norm = mcolors.LogNorm(vmin=vmin or 0.3, vmax=vmax)
    else:
        d_plot = d
        norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

    im = ax.pcolormesh(L_BINS, B_BINS, d_plot, norm=norm, cmap=cmap,
                       shading="flat")
    ax.set_xlim(60, -60)
    ax.set_ylim(-60, 60)
    ax.set_xlabel("銀経 l [deg]", fontsize=8)
    ax.set_ylabel("銀緯 b [deg]", fontsize=8)
    ax.set_title(title, fontsize=9, pad=3)
    ax.tick_params(labelsize=7)

    if show_disk_mask:
        ax.axhspan(-10, 10, color="gray", alpha=0.3, zorder=3)

    if show_nfw_circles:
        # NFW rs=21 kpc の投影角度: arctan(21/8) ≈ 69°
        # b=10 kpc の角度: arctan(10/8) ≈ 51°
        for rad, color, ls, lbl in [(51.3, "yellow", "--", "10kpc"),
                                     (69.1, "cyan", "-", "rs=21kpc")]:
            theta = np.linspace(0, 2*np.pi, 200)
            ax.plot(rad*np.cos(theta), rad*np.sin(theta),
                    color=color, ls=ls, lw=0.8, alpha=0.6)

    return im


def add_cbar(fig, im, ax, label, fontsize=7):
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="4%", pad=0.05)
    cb = fig.colorbar(im, cax=cax)
    cb.set_label(label, fontsize=fontsize)
    cb.ax.tick_params(labelsize=6)
    return cb


# ── 各成分の3パネル図 ──

COMPONENTS = [
    {
        "name": "comp01_isotropic",
        "title": "① 等方背景差引き（Isotropic Background Subtraction）",
        "before_key": "raw",
        "template_key": "template_iso",
        "after_key": "after_iso",
        "before_label": "Step 0: 生データ（差引き前）",
        "template_label": f"等方背景テンプレート\n（平均カウント密度 = {iso_level:.3f} cnt/pix）\n|b|>50° 領域の平均値",
        "after_label": "Step 1: 等方背景差引き後",
        "template_cmap": "YlOrRd",
        "template_log": False,
        "totani_note": "Totani §2.3: isotropic background f_l は MCMC で独立フィット",
    },
    {
        "name": "comp02_galprop",
        "title": "② 銀河拡散放射差引き（GALPROP ICS/Gas）",
        "before_key": "after_iso",
        "template_key": "template_galprop",
        "after_key": "after_galprop",
        "before_label": "Step 1: 等方背景差引き後",
        "template_label": "GALPROPテンプレート（gll_iem_v07.fits直接フィット、2026-07-11更新）\nTotani: 同じgll_iem_v07.fitsを使用（gas/ICS分離は未対応）",
        "after_label": "Step 2: GALPROP差引き後",
        "template_cmap": "hot",
        "template_log": True,
        "totani_note": "Totani §2.3 Fig.14: GALPROP gas + ICS(optical/IR/CMB) を\n独立成分として MCMC フィット",
    },
    {
        "name": "comp03_pointsource",
        "title": "③ 点源マスク（Point Source Masking）",
        "before_key": "after_galprop",
        "template_key": "template_ps",
        "after_key": "after_ps",
        "before_label": "Step 2: GALPROP差引き後",
        "template_label": f"4FGL-DR4 点源マスク\n({n_masked} sources in ROI)\n半径1°の円形マスク（NaN化）",
        "after_label": "Step 3: 点源マスク後（NaN=黒）",
        "template_cmap": "Reds",
        "template_log": False,
        "totani_note": "Totani §2.3: 4FGL-DR4 (gll_psc_v35.fit)\nPSFスペクトルモデルで差し引き（本解析はマスク方式）",
    },
    {
        "name": "comp04_fermi_bubble",
        "title": "④ フェルミバブル差引き（Fermi Bubble Subtraction）",
        "before_key": "after_ps",
        "template_key": "template_bubble",
        "after_key": "after_bubble",
        "before_label": "Step 3: 点源マスク後",
        "template_label": f"フェルミバブルテンプレート\n（Bin3=4.31 GeV残差マップ）\n振幅 A={bubble_amp:.4f}\nTotani Fig.1 対応",
        "after_label": "Step 4: バブル差引き後",
        "template_cmap": "hot",
        "template_log": False,
        "totani_note": "Totani §3.1 Fig.1: 4.3 GeV残差を positive/negative\n2テンプレートとして分離してフィット",
    },
    {
        "name": "comp05_loop_i",
        "title": "⑤ ループI差引き（Loop I Subtraction）",
        "before_key": "after_bubble",
        "template_key": "template_loopi",
        "after_key": "after_loopi",
        "before_label": "Step 4: バブル差引き後",
        "template_label": f"ループIテンプレート（Ackermann+2014/2017の2シェル3次元モデル）\nshell1 (l=341°,b=3°,d=78pc, 振幅={li_a1:.3f})\nshell2 (l=332°,b=37°,d=95pc, 振幅={li_a2:.3f})",
        "after_label": "Step 5: ループI差引き後（最終残差）",
        "template_cmap": "YlOrRd",
        "template_log": False,
        "totani_note": "Totani §2.3 Fig.14: 2シェル幾何モデル\n(r=50-100 pc) の振幅を独立フィット",
    },
]


def make_3panel(comp):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))
    fig.patch.set_facecolor("white")
    fig.suptitle(
        f"Bin 6 ({ECEN:.1f} GeV) — {comp['title']}",
        fontsize=12, fontweight="bold", y=0.98
    )

    before = steps[comp["before_key"]]
    template = steps[comp["template_key"]]
    after = steps[comp["after_key"]]

    # 左右: 同一スケール（輪講指摘③「左右のカラーバー値を合わせる」）
    # before と after の両方を含む abs 最大値で共有
    both_vals = np.concatenate([
        before[np.isfinite(before)].ravel(),
        after[~np.isnan(after)].ravel()
    ])
    shared_vmax = float(np.nanpercentile(np.abs(both_vals), 99.5)) if len(both_vals) else 10

    # 左: 差引き前
    im0 = plot_skymap(axes[0], before, comp["before_label"],
                      vmin=-shared_vmax, vmax=shared_vmax, cmap=CMAP_DIV, log=False)
    add_cbar(fig, im0, axes[0], "counts/pixel")

    # 中: テンプレート — Totani Fig.14 スタイル（hot + 独自スケール）
    # 正値のみの空間構造テンプレートは hot + log で表示（形が見える）
    # 左右の totani_div とは異なるが意図的: テンプレート=引く量の形状を示す
    tmpl_pos = template[np.isfinite(template) & (template > 0)]
    if comp["template_log"] and len(tmpl_pos) > 0:
        # GALPROP / フェルミバブル: 正値のみ → hot + LogNorm
        tv_min = float(np.nanpercentile(tmpl_pos, 1))
        tv_max = float(np.nanpercentile(tmpl_pos, 99.5))
        im1 = plot_skymap(axes[1], template, comp["template_label"],
                          vmin=tv_min, vmax=tv_max,
                          cmap="hot", log=True,
                          show_nfw_circles=False)
    else:
        tmpl_vals = template[np.isfinite(template) & (template != 0)]
        tv_max = float(np.nanpercentile(np.abs(tmpl_vals), 99.5)) if len(tmpl_vals) else 1.0
        tv_max = max(tv_max, 1e-9)
        # 負値を含む場合（Loop I など）: 発散型で両シェルを可視化
        has_neg = len(tmpl_vals) > 0 and float(np.min(tmpl_vals)) < -1e-6
        if has_neg:
            im1 = plot_skymap(axes[1], template, comp["template_label"],
                              vmin=-tv_max, vmax=tv_max,
                              cmap=CMAP_DIV, log=False,
                              show_nfw_circles=False)
        else:
            # ISO（均一正値）/ PS 差し引きマップ: hot
            im1 = plot_skymap(axes[1], template, comp["template_label"],
                              vmin=0, vmax=tv_max,
                              cmap="hot", log=False,
                              show_nfw_circles=False)
    add_cbar(fig, im1, axes[1], "counts/pixel")

    # 右: 差引き後（左と同一スケール）
    im2 = plot_skymap(axes[2], after, comp["after_label"],
                      vmin=-shared_vmax, vmax=shared_vmax, cmap=CMAP_DIV, log=False)
    add_cbar(fig, im2, axes[2], "counts/pixel")

    # Totani 注記
    fig.text(0.5, 0.01, f"Cf. {comp['totani_note']}",
             ha="center", va="bottom", fontsize=7, color="gray",
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow",
                       edgecolor="gray", alpha=0.8))

    plt.tight_layout(rect=[0, 0.08, 1, 0.96])
    out = OUT_DIR / f"{comp['name']}_3panel.png"
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved: {out}")
    return out


print("\n各成分 3パネル図を生成中...")
saved_files = []
for comp in COMPONENTS:
    f = make_3panel(comp)
    saved_files.append(f)


# ── 5成分まとめ俯瞰図 (概要) ──
print("\n5成分まとめ図を生成中...")
fig_all, axes_all = plt.subplots(5, 3, figsize=(18, 28))
fig_all.patch.set_facecolor("white")
fig_all.suptitle(
    f"Bin 6 ({ECEN:.1f} GeV) — 5成分逐次差引き一覧\n"
    f"各行: 差引き前 | テンプレート形状 | 差引き後",
    fontsize=14, fontweight="bold", y=0.995
)

col_labels = ["差引き前", "テンプレート形状", "差引き後"]
for j, lbl in enumerate(col_labels):
    axes_all[0, j].set_title(lbl, fontsize=12, fontweight="bold",
                              pad=8, color="navy")

row_labels = [
    "① 等方背景\n(Isotropic)",
    "② GALPROP\n(銀河拡散放射)",
    "③ 点源マスク\n(Point Sources)",
    "④ フェルミバブル\n(Fermi Bubbles)",
    "⑤ ループI\n(Loop I)",
]

for i, (comp, row_lbl) in enumerate(zip(COMPONENTS, row_labels)):
    before   = steps[comp["before_key"]]
    template = steps[comp["template_key"]]
    after    = steps[comp["after_key"]]

    ax_b, ax_t, ax_a = axes_all[i, 0], axes_all[i, 1], axes_all[i, 2]

    # 行ラベル
    ax_b.set_ylabel(row_lbl, fontsize=10, fontweight="bold", labelpad=5)

    # 左
    vmax_b = float(np.nanpercentile(before[before > 0], 99.5)) if np.any(before > 0) else 10
    im_b = plot_skymap(ax_b, before, "", vmin=0.3, vmax=vmax_b,
                       cmap="hot", log=True, show_nfw_circles=False)

    # 中
    if comp["template_log"] and np.any(template > 0):
        vmin_t = float(np.nanpercentile(template[template > 0], 1))
        vmax_t = float(np.nanpercentile(template[template > 0], 99))
        im_t = plot_skymap(ax_t, template, "", vmin=vmin_t, vmax=vmax_t,
                           cmap=comp["template_cmap"], log=True, show_nfw_circles=False)
    else:
        vmax_t = float(np.nanmax(np.abs(template))) if np.any(template != 0) else 1
        im_t = plot_skymap(ax_t, template, "", vmin=0, vmax=max(vmax_t, 1e-9),
                           cmap=comp["template_cmap"], log=False, show_nfw_circles=False)

    # 右
    after_pos = after[~np.isnan(after) & (after > 0)]
    vmax_a = float(np.nanpercentile(after_pos, 99.5)) if len(after_pos) > 0 else 10
    im_a = plot_skymap(ax_a, after, "", vmin=0.3, vmax=vmax_a,
                       cmap="hot", log=True, show_nfw_circles=False)

    for im, ax in [(im_b, ax_b), (im_t, ax_t), (im_a, ax_a)]:
        add_cbar(fig_all, im, ax, "cnt/pix", fontsize=6)

plt.tight_layout(rect=[0, 0, 1, 0.99])
out_all = OUT_DIR / "all5_overview.png"
fig_all.savefig(out_all, dpi=120, bbox_inches="tight", facecolor="white")
plt.close(fig_all)
print(f"  Saved: {out_all}")

print(f"\n完了 → {OUT_DIR}")
