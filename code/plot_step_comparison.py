"""
Bin 6（20.76 GeV）の5成分逐次差引を各ステップ保存し、
2パネル比較画像（ログカラーバー値付き）を3枚生成する。

出力:
  data/figure-step-comparison/
    step_pair_01_02.png  (生データ → ①等方背景差引後)
    step_pair_03_04.png  (②GALPROP差引後 → ③点源マスク後)
    step_pair_05_06.png  (④フェルミバブル差引後 → ⑤ループI差引後)

スライド 22-24 の既存画像を上記で置き換える。
"""
import pathlib as _pathlib

import sys
sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))

import numpy as np
import pandas as pd
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
import matplotlib
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"

# ── 設定 ─────────────────────────────────────────────────────────────────
BASE    = _pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = BASE / "data/figure-step-comparison"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CSV_PATH = BASE / "data/CSV/filtered_events_week780.csv"

# Bin 6
BIN6_EMIN, BIN6_EMAX, BIN6_CEN = 15.35, 28.07, 20.76
D_SUN = 8.0  # kpc

# ────────────────────────────────────────────────────────────────────────
# 差し引き関数: plot_skymap_all_subtracted.py から直接インポート
# （独自実装を一切使わない → GALPROP エネルギー取得・WCS・最適化が正しい保証）
# ────────────────────────────────────────────────────────────────────────
import plot_skymap_all_subtracted as _sub

# グリッド変数は _sub モジュールのものを再利用（同じ ROI・解像度）
L_BINS = _sub.L_BINS
B_BINS = _sub.B_BINS
L_C    = (L_BINS[:-1] + L_BINS[1:]) / 2
B_C    = (B_BINS[:-1] + B_BINS[1:]) / 2
LG, BG = np.meshgrid(L_C, B_C, indexing="ij")

def subtract_isotropic(c):
    return _sub.subtract_isotropic(c)

def subtract_galprop(c, emin, emax):
    res, _, label = _sub.subtract_galactic_diffuse(c, emin, emax)
    return res, label

def mask_point_sources(c, emin=None, emax=None):
    if emin is not None:
        result, _, n = _sub.subtract_point_sources(c, emin, emax)
        return result, n
    return _sub.mask_point_sources(c)

def build_bubble_template(df):
    return _sub.build_fermi_bubble_template(df)

def subtract_bubble(c, tmpl):
    res, A, _ = _sub.subtract_fermi_bubbles(c, tmpl)
    return res, A

def subtract_loop_i(c):
    res, _inner, _outer = _sub.subtract_loop_i(c)
    return res


# ────────────────────────────────────────────────────────────────────────
# 図作成ヘルパー
# ────────────────────────────────────────────────────────────────────────

C_BG = "#05051A"

# Totani (2025) Fig.11-13 スタイル: 全パネル共通の発散型カラーマップ
# シアン(負大) → 黒(0) → 黄(正大)
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


def make_panel(ax, data, title, step_n, is_log=True, shared_vmax=None):
    """
    全ステップ共通: Totani (2025) スタイルの発散型カラーマップ（0対称）。
    生データ（正値のみ）は右半分（暗→黄）に収まる。
    差し引き後（正負あり）は両側を使って過不足を可視化。
    """
    ax.set_facecolor(C_BG)
    ax.axhspan(-10, 10, alpha=0.2, color="gray")

    d = data.copy()

    # 0対称スケール: 生データ最大値を基準に設定
    fin = d[np.isfinite(d)]
    abs_max = float(np.nanpercentile(np.abs(fin), 99.5)) if len(fin) else 10.0
    if shared_vmax is not None:
        abs_max = shared_vmax
    abs_max = max(abs_max, 0.5)

    im = ax.pcolormesh(L_C, B_C, d.T,
                       norm=mcolors.Normalize(vmin=-abs_max, vmax=abs_max),
                       cmap=CMAP_DIV, shading="auto")
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("カウント / pixel",
                   color="white", fontsize=12)
    cbar.ax.yaxis.set_tick_params(color="white", labelsize=11)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color="white", fontsize=11)

    # 軸設定（1° = 1° の正方形を維持）
    ax.set_xlim(60, -60)      # l は右→左（天文慣行）
    ax.set_ylim(-60, 60)
    ax.set_aspect("equal")    # 1deg_l = 1deg_b → 物理的に正方形
    ax.set_xlabel("銀経 l [deg]", color="white", fontsize=11)
    ax.set_ylabel("銀緯 b [deg]", color="white", fontsize=11)
    ax.tick_params(colors="white", labelsize=10)
    for sp in ax.spines.values():
        sp.set_color("white")

    # kpc スケール線
    for d_kpc, col, lbl in [(10, "#FFCC00", "10kpc"),
                             (21, "#44CCFF", "rs=21kpc")]:
        b_ang = np.degrees(np.arctan(d_kpc / D_SUN))
        ax.axhline( b_ang, color=col, lw=0.9, ls=":", alpha=0.8)
        ax.axhline(-b_ang, color=col, lw=0.9, ls=":", alpha=0.8)
        ax.text(-58, b_ang + 1, lbl, color=col, fontsize=8)

    # タイトル（シアン=負=引きすぎ、黄=正=超過）
    ax.set_title(f"Step {step_n}:  {title}",
                 color="white", fontsize=12, pad=6)

    return cbar


def save_pair(name, left_data, right_data, left_title, right_title,
              left_step, right_step, left_log, right_log,
              shared_vmax_left=None, shared_vmax_right=None):
    """2パネルの横並び比較図を保存"""
    # 各パネル 120°×120° で正方形。カラーバー込みで横 14 × 縦 7 インチ
    fig, axes = plt.subplots(1, 2, figsize=(14, 7), facecolor=C_BG)
    fig.subplots_adjust(wspace=0.45)

    make_panel(axes[0], left_data,  left_title,  left_step,
               is_log=left_log,  shared_vmax=shared_vmax_left)
    make_panel(axes[1], right_data, right_title, right_step,
               is_log=right_log, shared_vmax=shared_vmax_right)

    fig.suptitle(
        f"Bin 6（20.76 GeV）— 差し引きステップ比較  |  780週 Fermi-LAT データ\n"
        f"ROI: |l|≤60°, |b|=10°–60°  |  点線: 10 kpc（黄）/ rs=21 kpc（青）",
        color="white", fontsize=12, y=1.01
    )
    out = OUT_DIR / name
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=C_BG)
    plt.close()
    print(f"  → {out}")
    return out


# ────────────────────────────────────────────────────────────────────────
# メイン処理
# ────────────────────────────────────────────────────────────────────────
def main():
    print("データ読み込み中...")
    df = pd.read_csv(CSV_PATH, comment="#", low_memory=False)
    df = df[(df.b_deg.abs() >= 10) & (df.b_deg.abs() <= 60) &
            (df.l_deg.abs() <= 60)]
    print(f"  ROI 全ビン: {len(df):,} イベント")

    # Bin 6 抽出
    sel = df[(df.energy_GeV >= BIN6_EMIN) & (df.energy_GeV < BIN6_EMAX)]
    raw, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[L_BINS, B_BINS])
    raw = raw.astype(float)
    print(f"  Bin6 ({BIN6_CEN} GeV): {len(sel):,} イベント")

    # Fermi Bubble テンプレート構築（全データ使用）
    print("Fermi Bubble テンプレート構築中...")
    bubble_tmpl = build_bubble_template(df)

    # --- 逐次差し引き ---
    print("差し引き処理中...")

    # Step 0: 生データ
    s0 = raw.copy()

    # Step 1: 等方背景差引
    s1, iso_lv = subtract_isotropic(s0.copy())
    print(f"  Step1 等方BG: {iso_lv:.3f} counts/pixel")

    # Step 2: GALPROP
    s2, gal_lbl = subtract_galprop(s1.copy(), BIN6_EMIN, BIN6_EMAX)
    print(f"  Step2 GALPROP: {gal_lbl}")

    # Step 3: 点源差し引き（スペクトルモデル）
    s3, n_ps = mask_point_sources(s2.copy(), BIN6_EMIN, BIN6_EMAX)
    print(f"  Step3 点源差し引き: {n_ps} 天体")

    # Step 4: フェルミバブル
    s4, bbl_A = subtract_bubble(s3.copy(), bubble_tmpl)
    print(f"  Step4 フェルミバブル: A={bbl_A:.4f}")

    # Step 5: ループI
    s5 = subtract_loop_i(s4.copy())
    print("  Step5 ループI完了")

    # log_scale 判断: Step0〜3 は正値多い → log
    #                Step4〜5 は残差 → 線形 diverging
    # ただし Step3 はマスク（NaN）が多いので log のほうが見やすい
    # vmax を Step0 に合わせて共通化（同じスケールで差し引きの変化を比較）
    raw_pos = np.where(np.isfinite(s0) & (s0 > 0), s0, np.nan)
    vmax_raw = np.nanpercentile(raw_pos, 99.5)

    # --- 3ペア図を保存 ---
    print("\n図を生成中...")
    out1 = save_pair(
        "step_pair_01_02.png",
        left_data=s0,  right_data=s1,
        left_title="Step 0: 生データ（差し引き前）",
        right_title="Step 1: ①等方背景差し引き後\n（|b|>50° の平均カウントを全ピクセルから差引）",
        left_step="0", right_step="1",
        left_log=True, right_log=True,
        shared_vmax_left=vmax_raw, shared_vmax_right=vmax_raw,
    )

    out2 = save_pair(
        "step_pair_03_04.png",
        left_data=s2,  right_data=s3,
        left_title="Step 2: ②銀河面拡散放射（GALPROP）差し引き後\n（gll_iem_v07.fits を使用）",
        right_title="Step 3: ③点源マスク後\n（4FGL-DR2 の既知天体を NaN マスク）",
        left_step="2", right_step="3",
        left_log=True, right_log=True,
        shared_vmax_left=vmax_raw, shared_vmax_right=vmax_raw,
    )

    out3 = save_pair(
        "step_pair_05_06.png",
        left_data=s4,  right_data=s5,
        left_title="Step 4: ④フェルミバブル差し引き後\n（4.3 GeV 残差テンプレート使用）",
        right_title="Step 5: ⑤ループI差し引き後（完成）\n← NFW フィット対象の最終残差マップ",
        left_step="4", right_step="5",
        left_log=True, right_log=True,
        shared_vmax_left=vmax_raw, shared_vmax_right=vmax_raw,
    )

    print(f"\n完了。出力先: {OUT_DIR}")
    return out1, out2, out3


if __name__ == "__main__":
    main()
