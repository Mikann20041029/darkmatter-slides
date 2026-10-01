"""
Bin 6（20.76 GeV）の5成分逐次差引（Step0〜Step5）を 2x3 グリッド1枚に
まとめた俯瞰図を生成する。

`plot_step_comparison.py` が生成する step_pair_*.png（スライド22-24用、
2パネルずつ3枚）と同じ計算・同じ make_panel() を再利用し、
スライド14「差し引きステップ可視化：Bin6（20.76 GeV）[780週]」用に
全6ステップを1枚のグリッドにまとめる。

出力:
  data/figure-step-comparison/step_grid_0to5.png
"""
import pathlib as _pathlib

import sys
sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import plot_step_comparison as spc

OUT_DIR = spc.OUT_DIR
CSV_PATH = spc.CSV_PATH
BIN6_EMIN, BIN6_EMAX, BIN6_CEN = spc.BIN6_EMIN, spc.BIN6_EMAX, spc.BIN6_CEN
L_BINS, B_BINS = spc.L_BINS, spc.B_BINS


def main():
    print("データ読み込み中...")
    df = pd.read_csv(CSV_PATH, comment="#", low_memory=False)
    df = df[(df.b_deg.abs() >= 10) & (df.b_deg.abs() <= 60) &
            (df.l_deg.abs() <= 60)]
    print(f"  ROI 全ビン: {len(df):,} イベント")

    sel = df[(df.energy_GeV >= BIN6_EMIN) & (df.energy_GeV < BIN6_EMAX)]
    raw, _, _ = np.histogram2d(sel.l_deg, sel.b_deg, bins=[L_BINS, B_BINS])
    raw = raw.astype(float)
    print(f"  Bin6 ({BIN6_CEN} GeV): {len(sel):,} イベント")

    print("Fermi Bubble テンプレート構築中...")
    bubble_tmpl = spc.build_bubble_template(df)

    print("差し引き処理中...")
    s0 = raw.copy()
    s1, iso_lv = spc.subtract_isotropic(s0.copy())
    print(f"  Step1 等方BG: {iso_lv:.3f} counts/pixel")
    s2, gal_lbl = spc.subtract_galprop(s1.copy(), BIN6_EMIN, BIN6_EMAX)
    print(f"  Step2 GALPROP: {gal_lbl}")
    s3, n_ps = spc.mask_point_sources(s2.copy())
    print(f"  Step3 点源マスク: {n_ps} ピクセル")
    s4, bbl_A = spc.subtract_bubble(s3.copy(), bubble_tmpl)
    print(f"  Step4 フェルミバブル: A={bbl_A:.4f}")
    s5 = spc.subtract_loop_i(s4.copy())
    print("  Step5 ループI完了")

    raw_pos = np.where(np.isfinite(s0) & (s0 > 0), s0, np.nan)
    vmax_raw = np.nanpercentile(raw_pos, 99.5)

    steps = [
        (s0, "0", "生データ（差し引き前）"),
        (s1, "1", "①等方背景差し引き後"),
        (s2, "2", "②GALPROP差し引き後"),
        (s3, "3", "③点源マスク後"),
        (s4, "4", "④フェルミバブル差し引き後"),
        (s5, "5", "⑤ループI差し引き後（最終残差）"),
    ]

    print("\n図を生成中...")
    fig, axes = plt.subplots(2, 3, figsize=(19, 12), facecolor=spc.C_BG)
    for (data, step_n, title), ax in zip(steps, axes.flat):
        spc.make_panel(ax, data, title, step_n, is_log=True,
                        shared_vmax=vmax_raw)

    fig.suptitle(
        "差し引きステップ可視化：Bin6（20.76 GeV）[780週]\n"
        "left→right, top→bottom: Step0（生データ）→ Step1（等方背景）→ "
        "Step2（GALPROP）→ Step3（点源マスク）→ Step4（Fermiバブル）→ "
        "Step5（LoopI・最終残差）",
        color="white", fontsize=13, y=1.02,
    )
    fig.subplots_adjust(wspace=0.45, hspace=0.35)

    out = OUT_DIR / "step_grid_0to5.png"
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=spc.C_BG)
    plt.close(fig)
    print(f"\n完了 → {out}")
    return out


if __name__ == "__main__":
    main()
