"""
Slide 7 の直後に ROI 物理根拠スライドを3枚挿入する。

挿入スライド:
  7b: なぜ銀河面（|b|<10°）を解析から除外したか
  7c: 除外しない場合に得られる情報（デメリットとのトレードオフ）
  7d: NFW J-factor 全球マップ（物理スケール付き）
"""
import pathlib as _pathlib

import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from lxml import etree

PPTX_PATH = "/mnt/c/Users/arsei/Downloads/slides_v3_detailed.pptx"
FIG_DIR   = str(_pathlib.Path(__file__).resolve().parent.parent / "data/figure-roi-physics")

# ── カラーパレット ──
C_BG     = RGBColor(0x05, 0x05, 0x1A)
C_TITLE  = RGBColor(0xFF, 0xCC, 0x00)
C_HEAD   = RGBColor(0x44, 0xCC, 0xFF)
C_BODY   = RGBColor(0xFF, 0xFF, 0xFF)
C_GREEN  = RGBColor(0x44, 0xFF, 0x88)
C_ORANGE = RGBColor(0xFF, 0x88, 0x00)
C_RED    = RGBColor(0xFF, 0x44, 0x44)
C_GRAY   = RGBColor(0xAA, 0xAA, 0xAA)

SW = Inches(13.33)
SH = Inches(7.50)


# ─────────────────────────────────────────────────────────────────────────
# ヘルパー
# ─────────────────────────────────────────────────────────────────────────

def set_bg(slide):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = C_BG


def rm_shapes(slide):
    sp_tree = slide.shapes._spTree
    for sp in list(sp_tree):
        tag = sp.tag.split("}")[-1] if "}" in sp.tag else sp.tag
        if tag in ("sp", "pic", "grpSp", "graphicFrame", "cxnSp"):
            sp_tree.remove(sp)


def add_tb(slide, left, top, width, height, lines,
           default_size=14, default_color=C_BODY, default_bold=False,
           word_wrap=True):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = word_wrap
    tf.auto_size = None
    sp_pr = txBox._element.spPr
    ln = sp_pr.find(qn("a:ln"))
    if ln is None:
        ln = etree.SubElement(sp_pr, qn("a:ln"))
    ln.set("w", "0")
    if ln.find(qn("a:noFill")) is None:
        etree.SubElement(ln, qn("a:noFill"))
    for i, item in enumerate(lines):
        if isinstance(item, str):
            text, size, color, bold = item, default_size, default_color, default_bold
        else:
            text  = item.get("t", "")
            size  = item.get("s", default_size)
            color = item.get("c", default_color)
            bold  = item.get("b", default_bold)
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.space_after = Pt(3)
        run = para.add_run()
        run.text = text
        run.font.size  = Pt(size)
        run.font.color.rgb = color
        run.font.bold  = bold
    return txBox


def add_title(slide, text, subtitle=None):
    add_tb(slide, Inches(0.3), Inches(0.05), Inches(12.7), Inches(0.6),
           [{"t": text, "s": 22, "c": C_TITLE, "b": True}])
    if subtitle:
        add_tb(slide, Inches(0.3), Inches(0.63), Inches(12.7), Inches(0.35),
               [{"t": subtitle, "s": 15, "c": C_HEAD, "b": False}])


def add_picture_centered(slide, img_path, top, max_width, max_height):
    """画像をアスペクト比維持で挿入し水平中央揃え"""
    pic = slide.shapes.add_picture(img_path, Inches(0), top, width=max_width)
    if pic.height > max_height:
        ratio = max_height / pic.height
        pic.height = max_height
        pic.width = int(pic.width * ratio)
    pic.left = int((SW - pic.width) / 2)
    return pic


def set_notes(slide, text):
    if not slide.has_notes_slide:
        return
    tf = slide.notes_slide.notes_text_frame
    if tf is None:
        return
    tf.clear()
    for i, line in enumerate(text.split("\n")):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.text = line
        if para.runs:
            para.runs[0].font.size = Pt(11)


def insert_after(prs, after_idx, new_slide):
    """new_slide を after_idx の直後に移動（末尾に追加してから移動）"""
    xml_slides = prs.slides._sldIdLst
    new_elem = xml_slides[-1]
    xml_slides.remove(new_elem)
    xml_slides.insert(after_idx + 1, new_elem)


def blank_layout(prs):
    for layout in prs.slide_layouts:
        if layout.name in ("空白", "Blank", "空のスライド", "Blank Slide"):
            return layout
    return prs.slide_layouts[6]


def find_slide_idx(prs, title_kw):
    for i, slide in enumerate(prs.slides):
        for shape in slide.shapes:
            if shape.has_text_frame and title_kw in shape.text_frame.text:
                return i
    return -1


# ─────────────────────────────────────────────────────────────────────────
# 各スライドの構築
# ─────────────────────────────────────────────────────────────────────────

def build_slide_why_cut(slide):
    """なぜ銀河面（|b|<10°）を除外したか"""
    set_bg(slide)
    rm_shapes(slide)
    add_title(slide,
              "なぜ銀河面（|b|<10°）と遠方を ROI から除いたか",
              "ROI = |l|≤60°, 10°≤|b|≤60° の物理的根拠")

    add_tb(slide, Inches(0.3), Inches(0.95), Inches(6.1), Inches(6.2), [
        {"t": "▼ |b| < 10°（銀河面）を除外する理由", "s": 16, "c": C_RED, "b": True},
        {"t": "銀河面はγ線の最大汚染源:", "s": 14, "c": C_BODY},
        {"t": "  ① π⁰崩壊γ線（宇宙線×銀河ガス）が最も強い", "s": 14, "c": C_BODY},
        {"t": "  ② GALPROP モデルの誤差が最大（銀河面構造が複雑）", "s": 14, "c": C_ORANGE, "b": True},
        {"t": "  ③ GC GeV 過剰との空間縮退（DM シグナルと区別困難）", "s": 14, "c": C_BODY},
        {"t": "", "s": 8, "c": C_BODY},
        {"t": "物理スケールで考えると:", "s": 14, "c": C_BODY},
        {"t": "  b=10° の高さ = 8 kpc × tan(10°) ≈ 1.4 kpc", "s": 14, "c": C_BODY},
        {"t": "  → ガス円盤（厚さ ~0.3 kpc）+ 宇宙線ハローを全部含む", "s": 14, "c": C_ORANGE},
        {"t": "", "s": 8, "c": C_BODY},
        {"t": "▼ |b| > 60° を除外する理由", "s": 16, "c": C_HEAD, "b": True},
        {"t": "  ・NFW J-factor が急速に減少（DM 信号が弱い）", "s": 14, "c": C_BODY},
        {"t": "  ・光子数が少ない → 統計精度が低下", "s": 14, "c": C_BODY},
        {"t": "", "s": 8, "c": C_BODY},
        {"t": "▼ |l| > 60° を除外する理由", "s": 16, "c": C_HEAD, "b": True},
        {"t": "  ・銀河中心から遠ざかる → NFW J-factor 低下", "s": 14, "c": C_BODY},
        {"t": "  ・銀河外縁の複雑な構造（巻き腕など）", "s": 14, "c": C_BODY},
    ])

    add_tb(slide, Inches(6.6), Inches(0.95), Inches(6.4), Inches(6.2), [
        {"t": "▼ Totani の判断（論文 Section 2.1）", "s": 16, "c": C_GREEN, "b": True},
        {"t": "「GC 及び |b|<10° を除くことで", "s": 14, "c": C_BODY},
        {"t": "銀河面の強い拡散放射の影響を避ける」", "s": 14, "c": C_BODY},
        {"t": "→ 本研究も同一の ROI を採用", "s": 14, "c": C_GREEN, "b": True},
        {"t": "", "s": 8, "c": C_BODY},
        {"t": "▼ ROI の意味（まとめ）", "s": 16, "c": C_HEAD, "b": True},
        {"t": "高さ 1.4〜13.9 kpc のハローを探索:", "s": 14, "c": C_BODY},
        {"t": "  ・低い方（1.4 kpc）: ガス円盤を避けた最小高さ", "s": 14, "c": C_BODY},
        {"t": "  ・高い方（13.9 kpc）: NFW rs=21 kpc より内側", "s": 14, "c": C_BODY},
        {"t": "→ ROI は NFW の「スケール半径内」の", "s": 14, "c": C_BODY},
        {"t": "   密度が高い領域だけを狙っている", "s": 14, "c": C_ORANGE, "b": True},
        {"t": "", "s": 8, "c": C_BODY},
        {"t": "▼ rs = 21 kpc との関係", "s": 16, "c": C_HEAD, "b": True},
        {"t": "NFW ρ(r) はスケール半径 rs = 21 kpc より内側で", "s": 14, "c": C_BODY},
        {"t": "より急峻（∝ r⁻¹）。ROI はその内側のみを積分。", "s": 14, "c": C_BODY},
        {"t": "外側（r > rs）は ρ ∝ r⁻³ で急速に減少。", "s": 14, "c": C_GRAY},
    ])

    set_notes(slide, """\
【ページの役割】
ROI の物理的根拠（なぜ銀河面を除くか）を定量的に説明する補足スライド。
月曜の発表で「銀河面を含めないのはなぜか」という質問への正面からの回答。

【発表のポイント】
・「銀河面（|b|<10°）は DM シグナルが最も大きいが、バックグラウンドも最大 → S/N が改善しない」
・「GALPROP モデルの誤差が最大になる領域であり、本研究の手法では正確に引けない」
・「Totani が同じ ROI を選んだのは、この誤差とシグナルのトレードオフを最適化した結果」

【Totaniとの違い】
ROI 設定は完全に同一。この判断は本研究とTotaniで共有している。
""")


def build_slide_if_not_cut(slide):
    """除外しない場合に得られる情報"""
    set_bg(slide)
    rm_shapes(slide)
    add_title(slide,
              "銀河面を含めた場合に得られる情報（トレードオフの整理）",
              "各領域の NFW J-factor 比較（Via Lactea II NFW-ρ² による理論計算）")

    add_tb(slide, Inches(0.3), Inches(0.95), Inches(6.1), Inches(6.2), [
        {"t": "▼ J-factor 定量比較（全球 2D 積分）", "s": 16, "c": C_HEAD, "b": True},
        {"t": "領域                  J-factor 合計（ROI=1.0 基準）", "s": 13, "c": C_GRAY},
        {"t": "銀河面 |b|<10°          ★ 1.39×（最大）", "s": 14, "c": C_RED, "b": True},
        {"t": "ROI（本研究）            1.00×（基準）", "s": 14, "c": C_GREEN, "b": True},
        {"t": "|b|>60°（高銀緯）        0.37×", "s": 14, "c": C_BODY},
        {"t": "|l|>60°かつ10°≤|b|≤60°  0.33×", "s": 14, "c": C_BODY},
        {"t": "", "s": 8, "c": C_BODY},
        {"t": "▼ 解釈", "s": 16, "c": C_HEAD, "b": True},
        {"t": "銀河面（|b|<10°）= ROI の 1.39 倍の DM 信号期待量", "s": 14, "c": C_BODY},
        {"t": "→ 含めると S/N が改善する「はず」だが…", "s": 14, "c": C_ORANGE},
        {"t": "   GALPROP 誤差が最大の領域 → 系統誤差が支配的", "s": 14, "c": C_RED, "b": True},
        {"t": "   GC GeV 過剰との空間縮退も解けない", "s": 14, "c": C_BODY},
    ])

    add_tb(slide, Inches(6.6), Inches(0.95), Inches(6.4), Inches(6.2), [
        {"t": "▼ 含めた場合に「得られる」情報", "s": 16, "c": C_GREEN, "b": True},
        {"t": "① 銀河中心付近（b~0°）の DM 密度分布", "s": 14, "c": C_BODY},
        {"t": "   → NFW vs cusp/core の判別が可能になる", "s": 14, "c": C_GREEN},
        {"t": "② GC GeV 過剰（2〜3 GeV ピーク）との比較", "s": 14, "c": C_BODY},
        {"t": "   → 本研究の 20 GeV 過剰との空間的関係", "s": 14, "c": C_GREEN},
        {"t": "③ 銀河面の NFW 振幅が ROI と一致するか確認", "s": 14, "c": C_BODY},
        {"t": "   → DM シグナルの空間的一貫性の検証", "s": 14, "c": C_GREEN},
        {"t": "", "s": 8, "c": C_BODY},
        {"t": "▼ 含めない理由（なぜ Totani も外したか）", "s": 16, "c": C_RED, "b": True},
        {"t": "・GALPROP の ±20% 超の誤差が引けない", "s": 14, "c": C_BODY},
        {"t": "・GC GeV 過剰と DM の縮退が解けない", "s": 14, "c": C_BODY},
        {"t": "・系統誤差 >> 統計誤差 → 信頼性が下がる", "s": 14, "c": C_BODY},
        {"t": "", "s": 8, "c": C_BODY},
        {"t": "▼ 今後の展開", "s": 16, "c": C_HEAD, "b": True},
        {"t": "GALPROP の精度向上（MCMC 実装）後に", "s": 14, "c": C_BODY},
        {"t": "銀河面を含めた解析を実施すれば、", "s": 14, "c": C_BODY},
        {"t": "より強力な DM 検出が可能になる。", "s": 14, "c": C_GREEN},
    ])

    set_notes(slide, """\
【ページの役割】
「銀河面を含めなかった場合に失う情報は何か」「含めたら何が分かるか」の整理スライド。
発表では「ROI 設定はトレードオフの結果」であることを強調。

【定量的根拠】
銀河面（|b|<10°）の J-factor は ROI の 1.39 倍（全球 2D 積分）。
ただし、GALPROP 誤差（本研究では +3〜22%）が銀河面で最大になるため、
系統誤差が統計誤差を上回り、信頼性のある解析ができない。

【Totaniとの違い】
Totani は MCMC で GALPROP を精密にフィットしているが、それでも銀河面を除外している。
これは「GALPROP モデル自体の不確かさ（モデルそのものの限界）」が銀河面で最大だから。

【発表のポイント】
・「1.39 倍の DM 信号を捨てているが、それと引き換えに系統誤差を排除している」
・「将来的（MCMC 実装後）に銀河面を含めるのが卒論の次のステップ」
""")


def build_slide_fullsky_map(slide, img_path_map, img_path_bar):
    """NFW J-factor 全球マップスライド（2分割）"""
    set_bg(slide)
    rm_shapes(slide)
    add_title(slide,
              "NFW J-factor 全球マップと各領域の定量比較",
              "全天スカイマップ: 銀河中心集中・50 kpc スケール・ROI 境界を重ねて表示")

    # 上段: 全球マップ
    add_picture_centered(slide, img_path_map,
                         top=Inches(0.9),
                         max_width=Inches(12.5),
                         max_height=Inches(3.5))

    # 下段: 棒グラフ
    add_picture_centered(slide, img_path_bar,
                         top=Inches(4.5),
                         max_width=Inches(7.0),
                         max_height=Inches(2.8))

    set_notes(slide, """\
【ページの役割】
NFW J-factor の全球分布と、各領域の定量比較を示す図スライド。
「全球のどの方向に DM シグナルが強いか」を視覚化する。

【上図（全球マップ）の説明】
横軸: 銀経 l（-180°〜+180°）, 縦軸: 銀緯 b（-90°〜+90°）
カラー: NFW J-factor（ρ² 視線積分）の対数スケール
  ・中心（l=0, b=0）が最大（銀河中心）
  ・緑破線: ROI 境界（本研究の解析領域）
  ・赤帯: 銀河面除外領域（|b|<10°）
  ・点線: GC からの物理スケール（10 kpc 黄, rs=21 kpc シアン, 50 kpc ピンク）

【データ・目的・手段】
データ: NFW パラメータ（Via Lactea II: rs=21 kpc, ρs=8.1×10⁶ M☉/kpc³）
目的: ROI 設定の物理的根拠を可視化
手段: code/plot_roi_physics.py の j_factor_pixel() を全球グリッドで計算

【下図（棒グラフ）の説明】
各領域の J-factor 合計（ROI=1.0 に規格化）:
  赤: 銀河面 |b|<10° = 1.39×（最大だが除外）
  緑: ROI（本研究）= 1.00×（基準）
  黄: |b|>60° = 0.37×
  青: |l|>60°かつ10°≤|b|≤60° = 0.33×

【Totaniとの違い】
NFW パラメータは Totani と同一（Via Lactea II, Kuhlen et al. 2008）。
全球マップ自体は本研究のオリジナル可視化。
Totani は ROI 内の J-factor マップを論文に掲載しているが、全球比較は行っていない。

【発表のポイント】
・「50 kpc の点線はほぼ銀河北極（b≈81°）に相当。ROI（b=60°）はその内側」
・「銀河面の 1.39 倍が失われているが、その代わりに系統誤差を制御できている」
・「ROI は NFW のスケール半径（21 kpc → b≈69°）より内側のみを積分」
""")


# ─────────────────────────────────────────────────────────────────────────
# メイン
# ─────────────────────────────────────────────────────────────────────────

def main():
    prs = Presentation(PPTX_PATH)
    layout = blank_layout(prs)

    # Slide 7 のインデックスを探す
    after_idx = find_slide_idx(prs, "ROIの物理スケール")
    if after_idx < 0:
        print("⚠ Slide 7（ROIの物理スケール）が見つかりません。末尾に追加します。")
        after_idx = len(list(prs.slides)) - 1
    print(f"Slide 7 インデックス: {after_idx} （このスライドの直後に挿入）")

    fig_map = os.path.join(FIG_DIR, "nfw_fullsky_jfactor.png")
    fig_bar = os.path.join(FIG_DIR, "region_jfactor_comparison.png")

    # 3枚を後ろから挿入（順序を保つため逆順）
    slides_to_add = [
        ("全球マップ",   build_slide_fullsky_map,  {"img_path_map": fig_map, "img_path_bar": fig_bar}),
        ("銀河面除外しない場合", build_slide_if_not_cut, {}),
        ("銀河面除外理由",     build_slide_why_cut,    {}),
    ]

    for label, builder, kwargs in slides_to_add:
        new_slide = prs.slides.add_slide(layout)
        builder(new_slide, **kwargs)
        insert_after(prs, after_idx, new_slide)
        print(f"  挿入: {label}")

    prs.save(PPTX_PATH)
    print(f"\n完了。総スライド数: {len(list(prs.slides))}")
    print(f"保存先: {PPTX_PATH}")


if __name__ == "__main__":
    main()
