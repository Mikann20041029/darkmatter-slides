#!/usr/bin/env python3
"""
6成分モデル（点源・GALPROP・等方背景・LoopI・フェルミバブル・NFWハロー）について、
Totani (2025) の手法・パラメータと本解析の実装を直接突き合わせ、数値ズレ（%）または
手法上の相違点を定量化する。

教授指摘（2026-05-22）「6成分モデルがTotaniとどれくらいズレているか定量化して」への対応。

方針（観察 と 推測 の区別を明示）:
  - 数値として直接比較できる成分 (NFW, GALPROP) は % ズレを計算する
  - テンプレート構築の「手法」自体が異なる成分 (等方背景, LoopI, フェルミバブル, 点源)
    は、% という単一指標に圧縮すると誤解を招くため、「手法上の相違点」として
    両者の値・前提を並べて記述する（無理に % 化しない）

参照:
  - Totani (2025) 原文 (ref/20Gev_gamma_ray.paper.2025-Nov-23.pdf) §2.3, §3.1
  - 本解析: code/plot_skymap_all_subtracted.py, code/plot_roi_physics.py,
            data/figure-galprop/deviation_table.txt (galprop_comparison.py で既出)

出力: data/figure-component-comparison/six_component_comparison.png
      data/figure-component-comparison/six_component_comparison_table.txt
"""

from pathlib import Path
import sys
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf")
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))
DATA_DIR = ROOT / "data"
OUT_DIR = DATA_DIR / "figure-component-comparison"
OUT_DIR.mkdir(parents=True, exist_ok=True)

import plot_skymap_all_subtracted as _sub  # noqa: E402

BIN6_EMIN, BIN6_EMAX, BIN6_CEN = 15.35, 28.07, 20.76


def measure_pipeline_values():
    """Bin6 (20.76 GeV) で本解析パイプラインが実際に算出する各成分の値を取得する。

    observation: 既存の差し引き関数をそのまま呼び出して得た実測値であり、
    新しいフィットや近似は導入していない。
    """
    csv = DATA_DIR / "CSV" / "filtered_events_week780.csv"
    df = pd.read_csv(csv, comment="#", low_memory=False)  # comment='#'でヘッダー行のコメントをスキップ。low_memory=Trueだとこのファイルサイズでpandasのchunk化バグ(IndexError)を踏む
    sel = df[(df["energy_GeV"] >= BIN6_EMIN) & (df["energy_GeV"] < BIN6_EMAX)]

    L_BINS, B_BINS = _sub.L_BINS, _sub.B_BINS
    counts, _, _ = np.histogram2d(sel["l_deg"], sel["b_deg"], bins=[L_BINS, B_BINS])

    c1, iso_lv = _sub.subtract_isotropic(counts.copy())
    c2, _, _ = _sub.subtract_galactic_diffuse(c1.copy(), BIN6_EMIN, BIN6_EMAX)
    c3, _ = _sub.mask_point_sources(c2.copy())
    bubble_template = _sub.build_fermi_bubble_template(df)
    c4, A_bub, _ = _sub.subtract_fermi_bubbles(c3.copy(), bubble_template)
    _c5, li_in, li_out = _sub.subtract_loop_i(c4.copy())

    return {
        "iso_level_cnt_per_pix": iso_lv,
        "bubble_amplitude_A": A_bub,
        "loopI_inner_cnt_per_pix": li_in,
        "loopI_outer_cnt_per_pix": li_out,
    }


def load_galprop_deviation_table():
    """既出 (de7a295) の GALPROP vs 指数関数近似 偏差テーブルを読み込む。"""
    p = DATA_DIR / "figure-galprop" / "deviation_table.txt"
    rows = []
    for line in p.read_text().splitlines():
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split()
        rows.append((float(parts[0]), float(parts[3])))  # (E_center, deviation%)
    return rows


# ─────────────────────────────────────────────────────────────────────
# 6成分の比較テーブル定義（Totani 原文の値・出典 と 本解析の値・出典を並記）
# ─────────────────────────────────────────────────────────────────────
def build_component_table(pipeline_vals, galprop_dev):
    galprop_e = [r[0] for r in galprop_dev]
    galprop_d = [r[1] for r in galprop_dev]
    galprop_range = f"+{min(galprop_d):.1f}% (E={galprop_e[galprop_d.index(min(galprop_d))]:.2f} GeV) " \
                    f"〜 +{max(galprop_d):.1f}% (E={galprop_e[galprop_d.index(max(galprop_d))]:.2f} GeV)"

    return [
        dict(
            name="① 点源 (Point sources)",
            kind="catalog",
            totani="4FGL-DR4 (gll_psc_v35.fit, 14年分) + LAT PSF 畳み込み (§2.3, p.4)",
            ours="4FGL-DR4 (gll_psc_v35_dr4.fit, 14年分) — 2026-07-10にDR2から更新済み",
            deviation="同一カタログ世代 (DR4) を使用。source-by-source のフラックス差分は未計算だが、"
                      "カタログ世代差による系統的なズレは解消済み",
            status="resolved",
        ),
        dict(
            name="② GALPROP拡散放射 (Galactic diffuse)",
            kind="numeric",
            totani="GALPROP S_LZ_6R_30T_150C_2 model, gll_iem_v07.fits (LAT team 推奨モデル) (§2.3, p.4)",
            ours=f"同じ gll_iem_v07.fits を使用 (SPEC.md) するが、フィットには指数関数近似を採用。"
                 f"GALPROP実測マップとの偏差 = {galprop_range}",
            deviation=galprop_range,
            status="quantified",
        ),
        dict(
            name="③ 等方背景放射 (Isotropic)",
            kind="method",
            totani="物理的初期値 E²dN/dE=1e-4 MeV cm⁻²s⁻¹sr⁻¹ (典型的な未分解 EGB フラックス, [56])"
                   " を与えテンプレートとして MCMC でフィット (§2.3, p.4)",
            ours=f"|b|≥50° の平均カウント密度 = {pipeline_vals['iso_level_cnt_per_pix']:.3f} counts/pixel"
                 f" (Bin6) を一定値として全ピクセルから差し引く（テンプレートフィットではない）",
            deviation="手法が物理テンプレート(MCMC fit)と経験的フロア値(定数差し引き)で根本的に異なる。"
                      "counts/pixel → MeV cm⁻²s⁻¹sr⁻¹ への単位換算には exposure map が必要で未実施のため、"
                      "% 比較は不可能（無理に数値化しない）",
            status="method-diff",
        ),
        dict(
            name="④ Loop I",
            kind="method",
            totani="物理幾何モデル（半径50-100pcの2シェルで一様発光率を仮定, Wolleben 系)"
                   "の正規化2パラメータを MCMC でフィット (§2.3, p.4)",
            ours=f"画像残差に対する経験的2成分(内側/外側)独立フィット。Bin6実測値: "
                 f"inner={pipeline_vals['loopI_inner_cnt_per_pix']:.3f}, "
                 f"outer={pipeline_vals['loopI_outer_cnt_per_pix']:.3f} counts/pixel"
                 f"（負値 = 過剰差引きを補正する形でフィットされている）",
            deviation="物理シェルモデル(Totani)とデータ駆動経験的フィット(本解析)で"
                      "テンプレートの形状自体が異なるため% 比較は不適切。"
                      "本解析が物理的シェル形状を仮定していない点が主要な相違",
            status="method-diff",
        ),
        dict(
            name="⑤ フェルミバブル (Fermi bubbles)",
            kind="method",
            totani="Bin3(4.3 GeV)残差から「正領域=バブル(fl≥0)」「負領域=GALPROP不一致補正(符号自由)」の"
                   "2テンプレートを作成し、Gaussian smoothing(σ=1°)を適用、境界は反復改善 (§3.1, p.5-6)",
            ours=f"同じ Bin3(4.31 GeV) 残差を使用するが、固定矩形領域(|l|<22°,10°<|b|<55°)内の"
                 f"正値のみを単一テンプレート化、Poisson MLE で振幅 A={pipeline_vals['bubble_amplitude_A']:.3f} に1パラメータフィット"
                 f"（負残差テンプレート・Gaussian smoothing は未実装）",
            deviation="使用エネルギービン(4.3 GeV)の選定根拠は Totani と一致 (§3.1 で明記)。"
                      "ただしテンプレート構築法は簡略化されており（負残差テンプレート省略、"
                      "境界が固定矩形、smoothing なし）、% ズレでなく構成要素の有無で比較すべき",
            status="method-diff",
        ),
        dict(
            name="⑥ NFWハロー (DM halo)",
            kind="numeric+method-diff",
            totani="ρ(r)=ρs·x⁻¹(1+x)⁻², x=r/rs, rs=21kpc, ρs=8.1×10⁶ M☉kpc⁻³, "
                   "rvir=402kpc, ρ☉=0.42 GeV/cm³ (Via Lactea II) (§2.3, p.4)。"
                   "有意性は単一ビンのS/Nでなくモデル比較で評価: "
                   "『NFW-ρ2 が他の密度プロファイルより統計的に2σ以上優位』(§3.2, p.10)。"
                   "Fig 8 は NFW-ρ2.5/ρ2/ρ1 の3プロファイルでハロー成分の"
                   "ベストフィットflux E²dN/dEスペクトル(銀極, b=±90°)を3パネル比較",
            ours="パラメータ rs=21.0kpc, rho_s=8.1e6 M☉/kpc³, r_vir=402.0kpc は"
                 "完全一致 (plot_roi_physics.py:22-25, plot_nfw_halo_fit.py:64)。"
                 "Bin6(20.76GeV) 振幅 S/N=+0.24 (all_bins_nfw_fit.py、2026-06-12に"
                 "Fig8相当3プロファイル(ρ2.5/ρ2/ρ1)拡張版として再実行し3回目の再現確認済み、"
                 "slide29/plot_allbins_before_after.pyの+0.24σと一致)。全13ビンで|S/N|<2.4",
            deviation="入力パラメータの数値ズレ = 0%（完全一致）。"
                      "[2026-06-08 f91845c で解消済み] かつて存在したBin6 S/N内部不整合"
                      "(-5.27 vs +26.5) は、旧コードのGALPROP指数フィットが"
                      "residual>0の画素のみを使う選択バイアスを持っていたことが原因と判明・修正済み"
                      "（修正後 -5.27 は再現しない）。data/figure-allbins-nfw/all_bins_nfw_results.json "
                      "(a8195cd, +26.5) は生成スクリプト未コミットで再現不能のため数値として不採用のまま。"
                      "残る相違は方法論: Totaniの有意性主張(NFW-ρ2が2σ以上優位, §3.2 p.10)はΔlnL "
                      "モデル比較によるもので、本解析の単一テンプレートOLS振幅のS/Nとは統計量が"
                      "異なり数値の直接比較は不可（構造比較のみ可: fig8_3profile_*.png）",
            status="resolved-method-diff",
        ),
    ]


def write_table(rows):
    out = OUT_DIR / "six_component_comparison_table.txt"
    lines = ["# 6成分モデル: Totani (2025) と本解析の数値・手法比較",
             "# kind: numeric=数値直接比較可 / method=テンプレート構築手法が異なるため%化は不適切",
             "# 出典は Totani 原稿 PDF のセクション・ページ番号、本解析はファイル:行番号で明記",
             ""]
    for r in rows:
        lines += [
            f"## {r['name']}  [{r['kind']}, status={r['status']}]",
            f"  Totani (2025): {r['totani']}",
            f"  本解析       : {r['ours']}",
            f"  ズレ/相違    : {r['deviation']}",
            "",
        ]
    out.write_text("\n".join(lines))
    print(f"  -> {out}")


def panel_quantified_deviation(ax, galprop_dev):
    """数値として% 比較できる成分のみを示す（NFWパラメータ一致、GALPROP偏差レンジ）。"""
    e = [r[0] for r in galprop_dev]
    d = [r[1] for r in galprop_dev]
    ax.set_facecolor("#0d0d2a")
    ax.plot(e, d, "o-", color="#ff8844", lw=2, ms=6,
            label="② GALPROP実測 vs 指数関数近似 [既出 de7a295]")
    ax.axhline(0, color="#44ff88", lw=2, ls=":",
               label="⑥ NFWハロー: パラメータ完全一致 (0%, rs/ρs/rvir とも同一)")
    ax.fill_between(e, 0, d, color="#ff8844", alpha=0.12)
    ax.axvline(BIN6_CEN, color="gold", ls="-.", lw=1.2, alpha=0.8, label=f"Bin6 = {BIN6_CEN} GeV")

    ax.set_xscale("log")
    ax.set_xlabel("Photon energy [GeV]", color="white")
    ax.set_ylabel("本解析の近似値が GALPROP/Totani 値から外れる量 [%]", color="white")
    ax.set_title("数値として直接比較できる成分（②GALPROP, ⑥NFW）のズレ", color="white", fontsize=11)
    ax.tick_params(colors="white")
    ax.legend(fontsize=8, loc="upper left", facecolor="#05051a", labelcolor="white", framealpha=0.9)
    ax.grid(alpha=0.2, which="both")
    for sp in ax.spines.values():
        sp.set_edgecolor("#444")


def panel_method_diff_summary(ax, rows):
    """手法が異なる4成分について、構成要素の有無を○×でまとめる(質的比較のヒートマップ風)。"""
    method_rows = [r for r in rows if r["kind"] in ("method", "catalog")]
    items = ["物理\nテンプレート", "MCMC\nフィット", "複数\nサブテンプレート", "Smoothing /\nPSF畳み込み"]

    # observation: 各成分で Totani が採用し、本解析が省略/簡略化している要素を○×表示
    # (① 点源: カタログ世代差のため別軸、 ②⑥ は numeric なのでここに含めない)
    grid = np.array([
        # 物理テンプレ, MCMC, 複数サブテンプレ, smoothing/PSF
        [1, 0, 0, 1],   # ① 点源 (Totani: PSF畳み込みあり / 本解析: カタログはDR4で一致、PSF畳み込みなし)
        [1, 0, 0, 0],   # ③ 等方背景 (Totani: 物理テンプレ+MCMC / 本解析: 経験的floor)
        [1, 0, 0, 0],   # ④ Loop I (Totani: 2シェル物理モデル+MCMC / 本解析: 経験的2成分フィット)
        [0, 0, 1, 1],   # ⑤ フェルミバブル (Totani: 正/負2テンプレ+smoothing / 本解析: 単一矩形+MLE)
    ])
    # Totani 側は全て実装 (1)。本解析側の実装有無を別グリッドで重ねて○×表示
    ours_grid = np.array([
        [0, 0, 0, 0],   # 点源: カタログ世代(DR4)は一致、PSF畳み込みは未実装 (簡略化として0扱い)
        [0, 0, 0, 0],   # 等方背景: 物理テンプレ無し
        [0, 0, 0, 0],   # Loop I: 物理シェルモデル無し
        [0, 0, 0, 0],   # バブル: 単一矩形・smoothing無し
    ])

    ax.set_facecolor("#0d0d2a")
    n_rows, n_cols = grid.shape
    for i in range(n_rows):
        for j in range(n_cols):
            totani_has = grid[i, j] == 1
            ours_has = ours_grid[i, j] == 1
            if totani_has and ours_has:
                color, mark = "#44ff88", "○○"
            elif totani_has and not ours_has:
                color, mark = "#ff4444", "● ×"
            else:
                color, mark = "#555577", "─ ─"
            ax.add_patch(plt.Rectangle((j, n_rows - 1 - i), 1, 1, facecolor=color, alpha=0.35,
                                       edgecolor="white", lw=0.6))
            ax.text(j + 0.5, n_rows - 1 - i + 0.5, mark, ha="center", va="center",
                    color="white", fontsize=10)

    ax.set_xlim(0, n_cols); ax.set_ylim(0, n_rows)
    ax.set_xticks(np.arange(n_cols) + 0.5)
    ax.set_xticklabels(items, color="white", fontsize=8.5)
    ax.set_yticks(np.arange(n_rows) + 0.5)
    ax.set_yticklabels(["⑤ フェルミバブル", "④ Loop I", "③ 等方背景", "① 点源 (PSF畳み込み)"][::-1],
                       color="white", fontsize=9)
    ax.set_title("手法が異なる4成分: Totani が採用し本解析が簡略化/省略している要素\n"
                 "(● ×:Totaniのみ実装 / ─:両者とも未使用 / 凡例参照)",
                 color="white", fontsize=10.5)
    ax.tick_params(colors="white", length=0)
    for sp in ax.spines.values():
        sp.set_edgecolor("#444")
    # 凡例の代用テキスト
    ax.text(0.0, -0.55, "● ×  = Totaniは採用、本解析は未実装/簡略化（赤）　|　"
                        "─ ─  = 両者とも不使用（グレー）",
            transform=ax.transData, color="#cccccc", fontsize=8)


def main():
    print("6成分モデル: Totani (2025) との数値ズレ・手法比較を整理")
    pipeline_vals = measure_pipeline_values()
    galprop_dev = load_galprop_deviation_table()
    rows = build_component_table(pipeline_vals, galprop_dev)
    write_table(rows)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6.5), gridspec_kw={"width_ratios": [1.1, 1]})
    fig.patch.set_facecolor("#05051a")
    fig.suptitle("6成分モデル: Totani (2025) との数値ズレ・手法比較\n"
                 "(② GALPROP・⑥ NFW は数値直接比較、① 等方背景・③ LoopI・④ バブル・⑤ 点源は手法比較)",
                 color="white", fontsize=13, fontweight="bold")
    panel_quantified_deviation(axes[0], galprop_dev)
    panel_method_diff_summary(axes[1], rows)
    fig.tight_layout(rect=[0, 0.03, 1, 0.90])
    out = OUT_DIR / "six_component_comparison.png"
    fig.savefig(out, dpi=140, bbox_inches="tight", facecolor="#05051a")
    plt.close(fig)
    print(f"  -> {out}")
    print("完了 ->", OUT_DIR)


if __name__ == "__main__":
    main()
