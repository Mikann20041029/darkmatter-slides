"""
生成した解析図を slides_v3_detailed.pptx の適切な位置に挿入するスクリプト。

挿入ルール:
- 既存スライドのテキスト・ノートには一切触れない
- 図を挿入する新スライドを指定位置（after_idx）に追加する
- スライド順: Methods → Fermi bubble Fig1 → 差引ステップ → Results → 全Bin → Discussion → ...
"""

import os
import copy
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from lxml import etree

PPTX_PATH = "/mnt/c/Users/arsei/Downloads/slides_v3_detailed.pptx"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 生成された図のパス
FIGS = {
    "fermi_bubble":  os.path.join(BASE, "data/figure-totani-fig1/fermi_bubbles_1p5_4p3_GeV.png"),
    "nfw_amplitude": os.path.join(BASE, "data/figure-week780-nfw-fit/nfw_halo_spectrum.png"),
    "nfw_jmap":      os.path.join(BASE, "data/figure-week780-nfw-fit/nfw_j_factor_map.png"),
    "galprop_comp":  os.path.join(BASE, "data/figure-galprop/galprop_comparison_spectra.png"),
}

# 各図スライドの定義:
# after_slide_title: このタイトルを持つスライドの「直後」に挿入
# title: 新スライドのタイトル
# caption: 図の説明文
# fig_key: FIGS dict のキー
# notes: スピーカーノート

FIGURE_SLIDES = [
    {
        "after_slide_title": "補足：フェルミバブルテンプレートの構築（Totani Section 3.1）",
        "title": "【再現図】Fermi バブル像（1.5 GeV & 4.3 GeV）— Totani Fig.1 相当",
        "caption": "本研究の CSV データから生成。左: 1.51 GeV ビン, 右: 4.31 GeV ビン。\n"
                   "4.3 GeV でバブルがより明確に見える → フェルミバブルテンプレートに採用。",
        "fig_key": "fermi_bubble",
        "notes": (
            "【言うこと】\n"
            "この図は Totani (2025) の Fig.1 に相当する、本研究での再現図です。\n"
            "左が 1.51 GeV、右が 4.31 GeV のスカイマップです。\n\n"
            "4.3 GeV でフェルミバブルがより明確に浮き上がっているのが確認できます。\n"
            "Totani さんはこの 4.3 GeV マップの残差を使ってフェルミバブルのテンプレートを構築します。\n\n"
            "白線: 幾何テンプレートの境界（|l|<22°, |b|=15°〜50°）\n"
            "グレー帯: 銀河面 |b|<10°（解析除外領域）"
        ),
    },
    {
        "after_slide_title": "Results — NFW フィットとスペクトル",
        "title": "【再現図】全13ビン NFW 振幅スペクトル — Totani Fig.8 相当",
        "caption": "全13エネルギービンでの NFW フィット振幅 A とその 1σ 不確かさ（OLS）。\n"
                   "Bin 6 (20.76 GeV) で最大の有意性を検出（OLS 過大評価を含む）。",
        "fig_key": "nfw_amplitude",
        "notes": (
            "【言うこと】\n"
            "この図は全 13 エネルギービンで NFW フィットを実施した結果のスペクトルです。\n"
            "Totani (2025) の Fig.8 に相当します。\n\n"
            "縦軸の振幅 A > 0 → そのビンで NFW 形状の過剰が存在することを示します。\n"
            "A < 0 → 差し引きすぎ（バックグラウンドモデルの過大評価）。\n\n"
            "Bin 6（20.76 GeV）で最大の過剰を検出しています。\n"
            "これは b クォーク対消滅 DM のγ線スペクトルのピーク位置と一致します。\n"
            "低・高エネルギービンでは振幅が小さく、DM シグナルの選択性を示しています。\n\n"
            "注：S/N 値は OLS のため Totani（13〜19σ）より大きい過大評価を含む。\n"
            "今後 MCMC 実装により改善予定。"
        ),
    },
    {
        "after_slide_title": "【再現図】全13ビン NFW 振幅スペクトル — Totani Fig.8 相当",
        "title": "【補足図】NFW J-factor マップ（DM 密度の視線積分）",
        "caption": "ρ_NFW² の視線積分 J(l,b) = ∫ρ²ds。銀河中心（l=0,b=0）付近が最大。\n"
                   "このマップを DM シグナルのテンプレートとして使用。",
        "fig_key": "nfw_jmap",
        "notes": (
            "【言うこと】\n"
            "この図は DM 対消滅シグナルの空間テンプレートとなる J-factor マップです。\n\n"
            "J(l,b) = ∫ ρ_NFW²(r(s,l,b)) ds\n"
            "（視線方向に DM 密度の2乗を積分）\n\n"
            "明るい（高J-factor）領域 → DM シグナルが強く出ると期待される方向\n"
            "銀河中心付近が最も明るく、外側に向かってなだらかに減少する球対称分布。\n\n"
            "NFW パラメータ（Via Lactea II シミュレーション）:\n"
            "  rs = 21 kpc（スケール半径）\n"
            "  ρs = 8.1×10⁶ M☉/kpc³（スケール密度）\n"
            "  d_sun = 8 kpc（太陽–GC 距離）\n\n"
            "このテンプレートを残差マップにフィットして振幅 A を求める。"
        ),
    },
    {
        "after_slide_title": "補足：Totani (2025) との手法・設定の詳細比較",
        "title": "【再現図】GALPROP vs 指数関数近似の比較スペクトル",
        "caption": "ROI 平均フラックス: GALPROP モデル（gll_iem_v07.fits）vs 本研究の指数関数近似。\n"
                   "各ビンのズレ（%）を右軸に表示。",
        "fig_key": "galprop_comp",
        "notes": (
            "【言うこと】\n"
            "この図は GALPROP 公式モデルと本研究の指数関数近似の比較です。\n\n"
            "青線: gll_iem_v07.fits（GALPROP 公式、Totani が使用）のROI平均フラックス\n"
            "橙線: 本研究の exp(−|b|/b₀) フィットによる近似\n"
            "右軸: 各ビンでの % 差\n\n"
            "特に低エネルギー側（<10 GeV）で差が大きいことが予想される。\n"
            "この差が 31σ vs 13〜19σ の要因の一つ。\n\n"
            "対応策: gll_iem_v07.fits を直接使った差し引きに置き換える（実装予定）。"
        ),
    },
]


# ────────────────────────────────────────────────
# ヘルパー: スライドを特定タイトルの後ろに挿入
# ────────────────────────────────────────────────

def find_slide_index_by_title(prs: Presentation, title_text: str) -> int:
    for i, slide in enumerate(prs.slides):
        for shape in slide.shapes:
            if shape.has_text_frame and title_text in shape.text_frame.text:
                return i
    return -1


def duplicate_blank_layout(prs: Presentation):
    for layout in prs.slide_layouts:
        if layout.name in ("空白", "Blank", "空のスライド"):
            return layout
    return prs.slide_layouts[6]


def add_slide_after(prs: Presentation, after_idx: int, slide_data: dict) -> None:
    """after_idx の後ろに図スライドを挿入する"""
    # 使用可能な図かチェック
    fig_path = FIGS.get(slide_data["fig_key"], "")
    if not fig_path or not os.path.exists(fig_path):
        print(f"  ⚠ 図が存在しない: {fig_path} → スキップ")
        return

    # スライド追加（末尾に追加してから移動）
    layout = duplicate_blank_layout(prs)
    new_slide = prs.slides.add_slide(layout)

    # タイトルテキスト
    txBox = new_slide.shapes.add_textbox(Inches(0.3), Inches(0.1), Inches(9.4), Inches(0.7))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = slide_data["title"]
    p.runs[0].font.size = Pt(18)
    p.runs[0].font.bold = True

    # 図を挿入（高さ優先でアスペクト比保持）
    pic = new_slide.shapes.add_picture(fig_path, Inches(0.3), Inches(0.9),
                                        width=Inches(9.2))
    # 高さが画面に収まるよう調整
    max_h = Inches(5.5)
    if pic.height > max_h:
        ratio = max_h / pic.height
        pic.height = max_h
        pic.width = int(pic.width * ratio)
        pic.left = int((Inches(10) - pic.width) / 2)

    # キャプション
    cap_top = pic.top + pic.height + Inches(0.05)
    if cap_top < Inches(6.8):
        txCap = new_slide.shapes.add_textbox(Inches(0.3), cap_top, Inches(9.4), Inches(0.5))
        tf_cap = txCap.text_frame
        tf_cap.word_wrap = True
        p_cap = tf_cap.paragraphs[0]
        p_cap.text = slide_data["caption"]
        for run in p_cap.runs:
            run.font.size = Pt(11)
            run.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    # ノートを追加
    if slide_data.get("notes") and new_slide.has_notes_slide:
        tf_n = new_slide.notes_slide.notes_text_frame
        if tf_n:
            tf_n.clear()
            for i, line in enumerate(slide_data["notes"].split("\n")):
                if i == 0:
                    para = tf_n.paragraphs[0]
                else:
                    para = tf_n.add_paragraph()
                para.text = line

    # スライドを after_idx+1 の位置に移動
    # python-pptx はスライドの並び替えを直接サポートしないため XML を操作
    xml_slides = prs.slides._sldIdLst
    new_id_elem = xml_slides[-1]  # 末尾に追加されたはず
    xml_slides.remove(new_id_elem)
    # after_idx + 1 の位置に挿入（0-indexed）
    target_pos = min(after_idx + 1, len(xml_slides))
    xml_slides.insert(target_pos, new_id_elem)

    title_short = slide_data["title"][:50]
    print(f"  ✓ 挿入: [Slide {after_idx+2}] {title_short!r}")


# ────────────────────────────────────────────────
# メイン
# ────────────────────────────────────────────────

def main():
    # 存在する図だけ処理
    available = {k: v for k, v in FIGS.items() if os.path.exists(v)}
    missing = {k: v for k, v in FIGS.items() if not os.path.exists(v)}
    print(f"利用可能な図: {list(available.keys())}")
    if missing:
        print(f"未生成の図 (スキップ): {list(missing.keys())}")

    prs = Presentation(PPTX_PATH)

    for slide_data in FIGURE_SLIDES:
        if slide_data["fig_key"] not in available:
            continue
        after_title = slide_data["after_slide_title"]
        idx = find_slide_index_by_title(prs, after_title)
        if idx < 0:
            print(f"  ⚠ タイトルが見つからない: {after_title!r} → 末尾に追加")
            idx = len(prs.slides) - 1
        add_slide_after(prs, idx, slide_data)
        # 挿入後はインデックスがずれるので次の検索は再ロードされた状態で行われる

    prs.save(PPTX_PATH)
    print(f"\n完了。総スライド数: {len(prs.slides)}")
    print(f"保存先: {PPTX_PATH}")


if __name__ == "__main__":
    main()
