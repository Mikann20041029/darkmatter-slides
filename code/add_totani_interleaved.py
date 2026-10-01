"""
Totani (2025) 全図の解説→再現インタリーブスライドをPPTに追加する。

構成: Fig.1〜Fig.16 それぞれについて
  1. 解説スライド（日本語で図の読み方・意義を説明）
  2. 再現スライド（我々の図／または再現困難の説明）

追加場所: BACKUP セクションの末尾（現在の最終スライドの後）
"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

PPT_PATH = Path("PPT/slides_v3_detailed_fixed2_final.pptx  -  Repaired.pptx")
prs = Presentation(str(PPT_PATH))

W = prs.slide_width
H = prs.slide_height

C_BG    = RGBColor(0x05, 0x05, 0x1A)
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
C_TITLE = RGBColor(0xFF, 0xCC, 0x00)
C_CYAN  = RGBColor(0x00, 0xFF, 0xFF)
C_RED   = RGBColor(0xFF, 0x44, 0x00)
C_GREEN = RGBColor(0x44, 0xFF, 0x88)
C_GRAY  = RGBColor(0xAA, 0xAA, 0xAA)
C_ORANGE = RGBColor(0xFF, 0x88, 0x00)

BASE = Path(".")

def blank_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])

def set_bg(sl):
    bg = sl.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = C_BG

def add_title(sl, text, color=C_TITLE, font_size=24):
    tb = sl.shapes.add_textbox(Inches(0.15), Inches(0.05), W - Inches(0.3), Inches(0.55))
    tf = tb.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.color.rgb = color
    run.font.bold = True

def add_sep(sl):
    box = sl.shapes.add_shape(1, Inches(0.15), Inches(0.62), W - Inches(0.3), Inches(0.02))
    box.fill.solid()
    box.fill.fore_color.rgb = C_CYAN
    box.line.fill.background()

def add_text(sl, lines, left, top, width, height, font_size=13, color=C_WHITE, bold=False):
    tb = sl.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    if isinstance(lines, str):
        lines = [(lines, color, bold, font_size)]
    first = True
    for item in lines:
        if isinstance(item, str):
            item = (item, color, bold, font_size)
        txt, col, bld, sz = item
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_before = Pt(2)
        run = p.add_run()
        run.text = txt
        run.font.size = Pt(sz)
        run.font.color.rgb = col
        run.font.bold = bld

def add_img(sl, path, left, top, width=None, height=None):
    if not Path(path).exists():
        return False
    if width and height:
        sl.shapes.add_picture(str(path), left, top, width, height)
    elif width:
        sl.shapes.add_picture(str(path), left, top, width=width)
    elif height:
        sl.shapes.add_picture(str(path), left, top, height=height)
    else:
        sl.shapes.add_picture(str(path), left, top)
    return True

def make_no_repr_slide(prs, fig_num, reason_lines):
    """再現困難の場合のスライド"""
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, f"【Totani Fig.{fig_num} 再現】— 完全再現は困難（理由と代替）", color=C_ORANGE)
    add_sep(sl)
    add_text(sl, [
        ("再現困難な理由", C_RED, True, 15),
    ] + [(r, C_WHITE, False, 13) for r in reason_lines] + [
        ("", C_WHITE, False, 8),
        ("→ この図の本質的な情報は前スライドの解説に記載", C_GRAY, False, 12),
    ], Inches(0.2), Inches(0.7), W - Inches(0.4), H - Inches(0.8))
    return sl


# ─────────────────────────────────────────────────────────────────────────────
# SECTION HEADER
# ─────────────────────────────────────────────────────────────────────────────

def make_section_header(prs):
    sl = blank_slide(prs)
    set_bg(sl)
    add_text(sl, [
        ("【Totani (2025) 全図解説と再現】", C_TITLE, True, 32),
        ("", C_WHITE, False, 10),
        ("Fig.1 〜 Fig.16 それぞれについて:", C_CYAN, True, 20),
        ("  ① 解説スライド — この図は何を示すか、どう読むか", C_WHITE, False, 16),
        ("  ② 再現スライド — 我々のデータによる対応図（再現困難な場合はその理由）", C_WHITE, False, 16),
        ("", C_WHITE, False, 12),
        ("再現可能な図: Fig.1, 8, 9, 11, 12, 13, 14", C_GREEN, True, 16),
        ("再現困難な図: Fig.2-7, 10, 15, 16", C_ORANGE, True, 16),
        ("（MCMC尤度フィットが必要なため）", C_GRAY, False, 14),
    ], Inches(1.5), Inches(1.5), W - Inches(3), H - Inches(2))
    return sl


# ─────────────────────────────────────────────────────────────────────────────
# Fig.1
# ─────────────────────────────────────────────────────────────────────────────

def make_fig1_explain(prs):
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Totani Fig.1 解説】フェルミバブルのスカイマップ（1.5 & 4.3 GeV）")
    add_sep(sl)
    add_text(sl, [
        ("この図は何を示すか", C_CYAN, True, 15),
        ("Section 3.1 で作成したフェルミバブルのテンプレートを視覚化した図。", C_WHITE, False, 13),
        ("1.5 GeV（左）と 4.3 GeV（右）の2つのエネルギービンでのスカイマップ。", C_WHITE, False, 13),
        ("白線: 最終的なフラットテンプレートの境界", C_WHITE, False, 13),
        ("灰色円領域: CenA ローブ・SMC などを除外", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("なぜ4.3 GeVを使うのか", C_CYAN, True, 15),
        ("• フェルミバブルが最もはっきり見えるエネルギービン", C_WHITE, False, 13),
        ("• 1.5 GeV では銀河面付近（b~10-15°）に強い負の残差 → GALPROP モデルの誤差", C_WHITE, False, 13),
        ("• この負残差が構造的バブルテンプレートを歪めるため、正の領域のみ使用", C_WHITE, False, 13),
        ("• 4.3 GeV マップの正の残差（バブル内外問わず）→ テンプレートとして採用", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("読み方", C_CYAN, True, 15),
        ("• 赤/黄 = 正の残差（バブルのシグナル）", C_WHITE, False, 13),
        ("• 青 = 負の残差（GALPROP が過剰推定）", C_WHITE, False, 13),
        ("• バブル内部（白線内）が全体的に明るい → フラットテンプレートの根拠", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("私たちの解析との関係", C_GREEN, True, 14),
        ("我々も 4.3 GeV (Bin3) の残差マップからフェルミバブルテンプレートを作成している", C_WHITE, False, 13),
        ("→ data/figure-totani-fig1/ に再現図あり", C_WHITE, False, 13),
    ], Inches(0.2), Inches(0.7), W - Inches(0.4), H - Inches(0.8))
    return sl

def make_fig1_repr(prs):
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Totani Fig.1 再現】フェルミバブル 1.5 & 4.3 GeV スカイマップ（我々の版）")
    add_sep(sl)
    img_path = "data/figure-totani-fig1/fermi_bubbles_1p5_4p3_GeV.png"
    if not add_img(sl, img_path, Inches(0.15), Inches(0.7), width=W - Inches(0.3)):
        add_text(sl, ["画像未生成: python3 code/plot_totani_fig11_13_equiv.py を実行",
                      f"期待パス: {img_path}"],
                 Inches(1), Inches(2), W - Inches(2), Inches(2))
    add_text(sl, [
        ("（注）戸谷論文と同じFermi-LATデータ・同じ手法で作成。1.5 GeVと4.3 GeVのBin残差マップ。", C_GRAY, False, 11),
    ], Inches(0.2), H - Inches(0.4), W - Inches(0.4), Inches(0.35))
    return sl


# ─────────────────────────────────────────────────────────────────────────────
# Fig.2
# ─────────────────────────────────────────────────────────────────────────────

def make_fig2_explain(prs):
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Totani Fig.2 解説】全成分のベストフィットスペクトル（銀河面込み）")
    add_sep(sl)
    add_text(sl, [
        ("この図は何を示すか", C_CYAN, True, 15),
        ("MCMCフィッティング後の全モデル成分のSED（スペクトルエネルギー分布）。", C_WHITE, False, 13),
        ("ROI全体（銀河面 |b|<10° 含む）での平均背景フラックスを示す。", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("各成分の記号（凡例）", C_CYAN, True, 15),
        ("■ gas（黒）:      GALPROPガス成分（最大）、~10⁻³ MeV cm⁻² s⁻¹ sr⁻¹", C_WHITE, False, 13),
        ("○ ICS（黒）:      逆Compton散乱成分", C_WHITE, False, 13),
        ("◇ point sources:  既知点源成分（緑）", C_WHITE, False, 13),
        ("△ isotropic（灰）: 等方背景（電弱スケール）", C_WHITE, False, 13),
        ("▷ Loop I（マゼンタ）: ループI 2シェル幾何モデル", C_WHITE, False, 13),
        ("▲ FB flat（青）:  フラットフェルミバブルテンプレート", C_WHITE, False, 13),
        ("○ NFW-ρ²·⁵ GCE（赤）: 銀河中心GeV超過", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("注目点", C_CYAN, True, 15),
        ("• ガス成分（GALPROP）が最大 → 銀河面の宇宙線相互作用が支配的", C_WHITE, False, 13),
        ("• GCE（NFW-ρ²·⁵）は~2GeVにピーク → これがGC GeV超過の既知信号", C_WHITE, False, 13),
        ("• 縦軸: E²dN/dE [MeV cm⁻² s⁻¹ sr⁻¹] (ν Fν 表示)", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("私たちとの違い", C_RED, True, 14),
        ("• Totaniは全成分をMCMCで同時フィット → 我々は逐次差し引き", C_WHITE, False, 13),
        ("• Totaniの |b|<10°含む vs 我々の |b|≥10°のみ", C_WHITE, False, 13),
    ], Inches(0.2), Inches(0.7), W - Inches(0.4), H - Inches(0.8))
    return sl

def make_fig23_no_repr(prs, num):
    return make_no_repr_slide(prs, num, [
        "• Fig.2-3 はMCMCによる全成分同時フィット結果（6成分＋ハロー）",
        "• 我々の解析では逐次差し引き（sequential subtraction）を採用",
        "• 同等の情報: スライド22（Results — NFWフィット）で個別成分の差し引き結果を表示",
        "• 参考: 我々の compare_6component_totani.py が定量的な比較表を出力",
    ])


# ─────────────────────────────────────────────────────────────────────────────
# Fig.3
# ─────────────────────────────────────────────────────────────────────────────

def make_fig3_explain(prs):
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Totani Fig.3 解説】全成分スペクトル（銀河面除外 |b|≥10°）")
    add_sep(sl)
    add_text(sl, [
        ("Fig.2との違い", C_CYAN, True, 15),
        ("Fig.2と同じMCMCフィット結果だが、銀河面（|b|<10°）を除外したROIでの平均フラックス。", C_WHITE, False, 13),
        ("フィッティング自体は銀河面込みで行い、表示のみ除外している。", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("この図が重要な理由", C_CYAN, True, 15),
        ("銀河面を除外することで:", C_WHITE, False, 13),
        ("• ガス成分（GALPROP）が大幅に減少 → ハロー成分が相対的に見やすくなる", C_WHITE, False, 13),
        ("• ICS成分が銀河面込みより軟化 → ICS の銀緯依存性がわかる", C_WHITE, False, 13),
        ("• GCE（NFW-ρ²·⁵）はほぼ変わらない → 主に |b|≥10° に広がっている", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("注目数値", C_CYAN, True, 15),
        ("• Fig.3 で見ると GCE の 2.5 GeVフラックス ≈ 2.5×10⁻⁹ cm⁻² s⁻¹ sr⁻¹ MeV⁻¹", C_WHITE, False, 13),
        ("  → LAT チーム先行研究と整合（GC から1°での値）", C_WHITE, False, 13),
        ("• フェルミバブル（青三角）は ~10⁻⁴ オーダー → ガスの1/10 程度", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("私たちの解析: スライド22のResults参照", C_GREEN, True, 14),
        ("我々の逐次差し引き後の結果は Totani Fig.3 に最も近い", C_WHITE, False, 13),
        ("（|b|≥10°のみ使用、銀河面除外済み）", C_WHITE, False, 13),
    ], Inches(0.2), Inches(0.7), W - Inches(0.4), H - Inches(0.8))
    return sl


# ─────────────────────────────────────────────────────────────────────────────
# Fig.4-7: ハロー成分フィットのスペクトル系列
# ─────────────────────────────────────────────────────────────────────────────

def make_fig4567_explain(prs):
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Totani Fig.4-7 解説】ハロー成分フィット — 3プロファイル比較スペクトル", font_size=22)
    add_sep(sl)
    add_text(sl, [
        ("Fig.4-7 の構成", C_CYAN, True, 15),
        ("Fig.4: フラットFB → residual(+/-)テンプレートに置換、ハローなし（GCEなし）", C_WHITE, False, 12),
        ("Fig.5: Fig.4 + GCE（NFW-ρ²·⁵）追加", C_WHITE, False, 12),
        ("Fig.6: Fig.5のGCEをNFW-ρ²（滑らかDM消滅）に変更", C_WHITE, False, 12),
        ("Fig.7: Fig.5のGCEをNFW-ρ¹（サブハロー主体）に変更", C_WHITE, False, 12),
        ("", C_WHITE, False, 8),
        ("なぜフラットFBをresidualテンプレートに置換するのか？", C_CYAN, True, 14),
        ("4.3 GeV のフェルミバブルテンプレートには構造的な誤差があるため、", C_WHITE, False, 13),
        ("フラットバブル + 正・負残差の2テンプレートに分解して対処。", C_WHITE, False, 13),
        ("これにより、異なるエネルギーでの正確なハローフィットが可能。", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("3つのNFWモデルの違い", C_CYAN, True, 14),
        ("NFW-ρ²·⁵ (GCE): ε∝r⁻²·⁵ → GC中心に急激に集中 → GCGeV超過と同じモデル", C_WHITE, False, 13),
        ("NFW-ρ²   :    ε∝r⁻² → 滑らかなDM消滅（標準NFW）→ 最良フィット", C_WHITE, False, 13),
        ("NFW-ρ¹   :    ε∝r⁻¹ → サブハロー主体（崩壊）→ フィット最悪", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("Fig.5-7 で見えること", C_CYAN, True, 14),
        ("全3モデルで 10-20 GeV 付近にピーク（13-19σ）→ 20 GeV 過剰の統計的証拠", C_GREEN, False, 13),
        ("NFW-ρ² が 95% CL で NFW-ρ²·⁵ より良い → 密度プロファイルは浅め", C_WHITE, False, 13),
        ("NFW-ρ¹ は NFW-ρ² より有意に悪い → 浅すぎるプロファイルは不適", C_WHITE, False, 13),
    ], Inches(0.2), Inches(0.7), W - Inches(0.4), H - Inches(0.8))
    return sl

def make_fig4567_no_repr(prs):
    return make_no_repr_slide(prs, "4-7", [
        "• Fig.4-7 は MCMC によるハロー成分同時フィット（6成分＋ハロー）の結果",
        "• フラットFBを residual(+/-) テンプレートに置換する作業も MCMC フレームワーク内",
        "• 我々の手法: 逐次差し引き後に NFW J因子マップを乗算してフィット",
        "• 代替: スライド29-31（NFW振幅スペクトル）が Fig.5-7 に最も近い情報を提供",
        "• 代替: code/compare_6component_totani.py で定量比較",
    ])


# ─────────────────────────────────────────────────────────────────────────────
# Fig.8
# ─────────────────────────────────────────────────────────────────────────────

def make_fig8_explain(prs):
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Totani Fig.8 解説】ハローモデルのスペクトル（線形プロット） ★メイン結果")
    add_sep(sl)
    add_text(sl, [
        ("この図は論文の核心 — 20 GeV 過剰の発見", C_RED, True, 16),
        ("", C_WHITE, False, 6),
        ("縦軸: 銀河極（b=±90°）でのフラックス E²dN/dE [MeV cm⁻² s⁻¹ sr⁻¹]", C_WHITE, False, 13),
        ("→ 線形プロット = ゼロとの有意な差がはっきり見える", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("読み取るべき情報", C_CYAN, True, 15),
        ("• 全3モデル（NFW-ρ²·⁵, ρ², ρ¹）で 10-20 GeV にピーク", C_WHITE, False, 13),
        ("• 1.5 GeV では負値 → バブルテンプレートへの吸収（系統誤差の証拠）", C_WHITE, False, 13),
        ("• 21 GeV ビンで 13-19σ の統計的有意度", C_GREEN, False, 13),
        ("• 200 GeV以上はほぼゼロ → 非べき乗スペクトル（DM消滅の特徴）", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("3モデルの比較", C_CYAN, True, 15),
        ("NFW-ρ²·⁵: 銀河極での値が最も小さい（GCに集中しているから銀河極では弱い）", C_WHITE, False, 13),
        ("NFW-ρ²  : 中程度 → 最良フィット、20 GeVピーク最明瞭", C_WHITE, False, 13),
        ("NFW-ρ¹  : 最大（GCから遠くても高い） → ただしフィット質は最悪", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("我々の再現", C_GREEN, True, 14),
        ("code/plot_nfw_halo_fit.py が同等の図を生成 → スライド29-31 参照", C_WHITE, False, 13),
        ("我々の版: 13ビン全てのNFW振幅（≠フラックス）をプロット", C_WHITE, False, 13),
    ], Inches(0.2), Inches(0.7), W - Inches(0.4), H - Inches(0.8))
    return sl

def make_fig8_repr(prs):
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Totani Fig.8 再現】NFW振幅スペクトル — 全13エネルギービン")
    add_sep(sl)
    img_path = "data/figure-allbins-nfw/nfw_amplitude_spectrum_all13.png"
    added = add_img(sl, img_path, Inches(0.15), Inches(0.7), width=W - Inches(0.3))
    if not added:
        add_text(sl, ["画像未生成: python3 code/plot_nfw_halo_fit.py を実行",
                      f"期待パス: {img_path}"],
                 Inches(1), Inches(2), W - Inches(2), Inches(2))
    add_text(sl, [
        ("（注）縦軸は Totani と異なり「NFW振幅（フラックスではなく相対値）」。",
         C_GRAY, False, 11),
        ("20 GeV（Bin6）でピーク構造が確認できる。詳細はスライド29-31。", C_GRAY, False, 11),
    ], Inches(0.2), H - Inches(0.45), W - Inches(0.4), Inches(0.4))
    return sl


# ─────────────────────────────────────────────────────────────────────────────
# Fig.9
# ─────────────────────────────────────────────────────────────────────────────

def make_fig9_explain(prs):
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Totani Fig.9 解説】対数尤度差 Δln L — ハローモデルの有意度")
    add_sep(sl)
    add_text(sl, [
        ("この図は何を示すか", C_CYAN, True, 15),
        ("各エネルギービンでの「ハローありフィット」と「ハローなしフィット」の対数尤度差。", C_WHITE, False, 13),
        ("Δln L = ln L(ハローあり) − ln L(ハローなし)", C_WHITE, False, 13),
        ("→ Δln L > 0 : ハロー成分が統計的に必要 → 超過の証拠", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("読み方", C_CYAN, True, 15),
        ("• 太線: MCMC ベストフィット（最大尤度）", C_WHITE, False, 13),
        ("• 細線: 上位 95% の境界（MCMC チェーンの 95% 信頼区間）", C_WHITE, False, 13),
        ("• 3色: NFW-ρ²·⁵（点鎖線）, NFW-ρ²（実線赤）, NFW-ρ¹（破線青）", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("重要な数値", C_CYAN, True, 15),
        ("• 21 GeVビン: Δln L ≈ 100 (NFW-ρ²) → √(2×100) ≈ 14σ の有意度", C_GREEN, True, 14),
        ("• 2.5 GeVビン: Δln L ≈ 100 (全モデル) → GCE の吸収（4.3 GeVテンプレートに）", C_WHITE, False, 13),
        ("• NFW-ρ² が他より高い Δln L → 最良モデル", C_WHITE, False, 13),
        ("• 200 GeV以上: Δln L ≈ 0 → ハロー成分はゼロと整合", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("我々との対応", C_GREEN, True, 14),
        ("我々の Δχ² = (S/N)² スペクトル（スライド32）が Fig.9 に対応。", C_WHITE, False, 13),
        ("ただし Totani は MCMC、我々は直接の S/N 比。", C_WHITE, False, 13),
    ], Inches(0.2), Inches(0.7), W - Inches(0.4), H - Inches(0.8))
    return sl

def make_fig9_repr(prs):
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Totani Fig.9 再現】Δχ² = (S/N)² スペクトル — 我々の版")
    add_sep(sl)
    # Get image from existing slide 32 (0-indexed: 31)
    existing_sl = prs.slides[31]
    imgs = [sh for sh in existing_sl.shapes if sh.shape_type == 13]
    if imgs:
        img_blob = imgs[0].image.blob
        ext = imgs[0].image.ext
        tmp_path = f"/tmp/fig9_repr.{ext}"
        with open(tmp_path, "wb") as f:
            f.write(img_blob)
        add_img(sl, tmp_path, Inches(0.15), Inches(0.7), width=W - Inches(0.3))
    else:
        add_text(sl, ["スライド32から画像を取得できませんでした"],
                 Inches(1), Inches(2), W - Inches(2), Inches(2))
    add_text(sl, [
        ("（注）Totani Fig.9は対数尤度差 Δln L。我々の版はNFW振幅を(S/N)²で表示。",
         C_GRAY, False, 11),
        ("20 GeV（Bin6）での有意なピーク構造は共通。", C_GRAY, False, 11),
    ], Inches(0.2), H - Inches(0.45), W - Inches(0.4), Inches(0.4))
    return sl


# ─────────────────────────────────────────────────────────────────────────────
# Fig.10
# ─────────────────────────────────────────────────────────────────────────────

def make_fig10_explain(prs):
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Totani Fig.10 解説】21 GeVでの動径角度プロファイル")
    add_sep(sl)
    add_text(sl, [
        ("この図は何を示すか", C_CYAN, True, 15),
        ("GC（銀河中心）からの角度に対するフラックスプロファイル（21 GeVビン）。", C_WHITE, False, 13),
        ("3つのハローモデルのカーブ + データ点（ベストフィット＋残差の総和）を比較。", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("読み方", C_CYAN, True, 15),
        ("• 点: ベストフィットモデル＋残差（リング状領域の GC からの角度別平均フラックス）", C_WHITE, False, 13),
        ("• 曲線: 各ハローモデルのベストフィット動径プロファイル", C_WHITE, False, 13),
        ("• 水平点線: 未分解等方背景フラックス（Fermi-LAT 2015）", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("重要な発見", C_CYAN, True, 15),
        ("• NFW-ρ² モデルが データ点に最も良く合致（2σ以上で NFW-ρ²·⁵ より優れる）", C_GREEN, False, 13),
        ("• NFW-ρ¹ モデルでは: 等方背景フラックスを等方成分に残す「余裕」がなくなる", C_WHITE, False, 13),
        ("  → NFW-ρ¹ は不適（物理的に非現実的）", C_WHITE, False, 13),
        ("• データ点は 0-20° で NFW-ρ² より少し浅いプロファイルを示唆", C_WHITE, False, 13),
        ("  → 中心部でのサブハロー効果か、密度プロファイルの不確かさ", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("再現困難な理由と代替", C_RED, True, 14),
        ("動径プロファイルの計算には MCMC フィット後の「残差マップ」が必要。", C_WHITE, False, 13),
        ("我々の代替: data/figure-week780-nfw-fit/nfw_j_factor_map.png（NFW J因子マップ）", C_WHITE, False, 13),
    ], Inches(0.2), Inches(0.7), W - Inches(0.4), H - Inches(0.8))
    return sl

def make_fig10_repr(prs):
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Totani Fig.10 代替】NFW J因子マップ（動径プロファイルの代わり）")
    add_sep(sl)
    img_path = "data/figure-week780-nfw-fit/nfw_j_factor_map.png"
    added = add_img(sl, img_path, Inches(0.15), Inches(0.7), height=H - Inches(1.3))
    if not added:
        add_text(sl, ["画像未生成", f"期待パス: {img_path}"],
                 Inches(1), Inches(2), W - Inches(2), Inches(2))
    add_text(sl, [
        ("（代替図）NFW J因子マップ（ρ² の視線積分）。Fig.10の動径プロファイル曲線の形状に対応。",
         C_GRAY, False, 11),
        ("GCに向かって急増するプロファイルを確認できる。", C_GRAY, False, 11),
    ], Inches(0.2), H - Inches(0.45), W - Inches(0.4), Inches(0.4))
    return sl


# ─────────────────────────────────────────────────────────────────────────────
# Fig.11
# ─────────────────────────────────────────────────────────────────────────────

def make_fig11_explain(prs):
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Totani Fig.11 解説】21 GeV スカイマップ 2×2 — ハロー構造の可視化")
    add_sep(sl)
    add_text(sl, [
        ("この図は何を示すか", C_CYAN, True, 15),
        ("NFW-ρ² モデルを 21 GeVビンに適用したときの4種類のマップ。", C_WHITE, False, 13),
        ("", C_WHITE, False, 6),
        ("4つのパネル", C_CYAN, True, 15),
        ("左上: ハローなしフィットの残差マップ", C_WHITE, False, 13),
        ("  → ハロー成分を考慮しない場合でも、球対称の超過が見えている（下限値）", C_WHITE, False, 13),
        ("右上: NFW-ρ²モデル + 残差（= 全ハロー関連フラックス）", C_WHITE, False, 13),
        ("  → これが「モデルデータが全体的にどう見えるか」→ 球対称な赤い構造", C_GREEN, False, 13),
        ("左下: NFW-ρ²モデルのみ（= 理想的なNFWプロファイル）", C_WHITE, False, 13),
        ("  → 中心が明るく周辺に向かって暗くなる理想的なDMハロー分布", C_WHITE, False, 13),
        ("右下: NFW-ρ²フィット後の残差（= モデルを引いた後）", C_WHITE, False, 13),
        ("  → ほぼゼロ（ランダムノイズ）→ モデルがよくフィットしている", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("重要なポイント", C_CYAN, True, 15),
        ("• 右上の構造: 球対称 + NFWプロファイルと整合 → DMハローと一致", C_GREEN, False, 13),
        ("• 右下の残差: ほぼ平坦 → フィットが成功", C_WHITE, False, 13),
        ("• 銀河面（|b|<10°、灰色帯）は除外して解析", C_WHITE, False, 13),
    ], Inches(0.2), Inches(0.7), W - Inches(0.4), H - Inches(0.8))
    return sl

def make_fig11_repr(prs):
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Totani Fig.11 再現】Bin6 (20.76 GeV) 残差マップ 2×2")
    add_sep(sl)
    existing_sl = prs.slides[32]
    imgs = [sh for sh in existing_sl.shapes if sh.shape_type == 13]
    if imgs:
        img_blob = imgs[0].image.blob
        ext = imgs[0].image.ext
        tmp_path = f"/tmp/fig11_repr.{ext}"
        with open(tmp_path, "wb") as f:
            f.write(img_blob)
        add_img(sl, tmp_path, Inches(0.15), Inches(0.7), width=W - Inches(0.3))
    add_text(sl, [
        ("（注）スライド33と同一。Totani版（0.125°/pix、MCMC残差）vs 我々（1°/pix、逐次差し引き残差）。",
         C_GRAY, False, 11),
        ("中心付近のNFW構造と高エネルギー（Bin6: 20.76 GeV）での球対称を確認できる。", C_GRAY, False, 11),
    ], Inches(0.2), H - Inches(0.45), W - Inches(0.4), Inches(0.4))
    return sl


# ─────────────────────────────────────────────────────────────────────────────
# Fig.12
# ─────────────────────────────────────────────────────────────────────────────

def make_fig12_explain(prs):
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Totani Fig.12 解説】低エネルギー4ビン スカイマップ（<21 GeV）")
    add_sep(sl)
    add_text(sl, [
        ("この図は何を示すか", C_CYAN, True, 15),
        ("NFW-ρ² フィットの「モデル+残差」マップを、21 GeV より低い4ビンで表示。", C_WHITE, False, 13),
        ("（Fig.11 右上パネルのエネルギー系列）", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("4ビンの読み方", C_CYAN, True, 15),
        ("1.5 GeV（左上）:", C_WHITE, False, 13),
        ("  • 北半球（b>0）が青 → ハロー成分が大幅にマイナス", C_WHITE, False, 13),
        ("  • GALPROP ガス成分の誤差がこのビンで最大（銀河面付近の負残差）", C_WHITE, False, 13),
        ("  • ハロー成分は 1.5 GeV では弱い（スペクトルの低エネルギー端）", C_WHITE, False, 13),
        ("2.5 GeV（右上）:", C_WHITE, False, 13),
        ("  • ほぼゼロ → Fig.8 でも 2.5 GeV は最小値（GCEテンプレートに吸収）", C_WHITE, False, 13),
        ("4.3 GeV（左下）:", C_WHITE, False, 13),
        ("  • 球対称の超過が弱く見え始める", C_WHITE, False, 13),
        ("12 GeV（右下）:", C_WHITE, False, 13),
        ("  • 球対称構造が明確に → ハロー成分が強くなってきた証拠", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("我々の再現", C_GREEN, True, 14),
        ("スライド34（低エネルギー4ビン残差マップ）が Fig.12 に対応。", C_WHITE, False, 13),
        ("1°解像度のため細部は異なるが、エネルギー依存性のトレンドは再現できる。", C_WHITE, False, 13),
    ], Inches(0.2), Inches(0.7), W - Inches(0.4), H - Inches(0.8))
    return sl

def make_fig12_repr(prs):
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Totani Fig.12 再現】低エネルギー4ビン 残差マップ（我々の版）")
    add_sep(sl)
    existing_sl = prs.slides[33]
    imgs = [sh for sh in existing_sl.shapes if sh.shape_type == 13]
    if imgs:
        img_blob = imgs[0].image.blob
        ext = imgs[0].image.ext
        tmp_path = f"/tmp/fig12_repr.{ext}"
        with open(tmp_path, "wb") as f:
            f.write(img_blob)
        add_img(sl, tmp_path, Inches(0.15), Inches(0.7), width=W - Inches(0.3))
    add_text(sl, [("（注）スライド34と同一。", C_GRAY, False, 11)],
             Inches(0.2), H - Inches(0.45), W - Inches(0.4), Inches(0.4))
    return sl


# ─────────────────────────────────────────────────────────────────────────────
# Fig.13
# ─────────────────────────────────────────────────────────────────────────────

def make_fig13_explain(prs):
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Totani Fig.13 解説】高エネルギー4ビン スカイマップ（>21 GeV）")
    add_sep(sl)
    add_text(sl, [
        ("この図は何を示すか", C_CYAN, True, 15),
        ("NFW-ρ² フィットの「モデル+残差」マップを、21 GeV より高い4ビンで表示。", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("4ビンの読み方", C_CYAN, True, 15),
        ("35 GeV（左上）:", C_WHITE, False, 13),
        ("  • まだ球対称の超過が見える → 21 GeVピークの裾野", C_WHITE, False, 13),
        ("59 GeV（右上）:", C_WHITE, False, 13),
        ("  • 超過が大幅に減少 → ハローが急速に弱くなっている", C_WHITE, False, 13),
        ("100 GeV（左下）:", C_WHITE, False, 13),
        ("  • ほぼランダムノイズ → ハロー成分はゼロに近い", C_WHITE, False, 13),
        ("170 GeV（右下）:", C_WHITE, False, 13),
        ("  • 完全にノイズのみ → ハロー成分は検出不可", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("20 GeVピークの証拠として重要", C_CYAN, True, 15),
        ("• Fig.12（<21 GeV）で増加 → Fig.13（>21 GeV）で急減 → 21 GeVにピーク", C_GREEN, True, 13),
        ("• これがDM消滅スペクトルのブロードなピーク（mχ~500 GeV の bb̄ チャンネル）", C_WHITE, False, 13),
        ("• 200 GeV以上でゼロ → べき乗則（点源や拡散放射）では説明できない", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("我々の再現", C_GREEN, True, 14),
        ("スライド35（高エネルギー4ビン残差マップ）が Fig.13 に対応。", C_WHITE, False, 13),
    ], Inches(0.2), Inches(0.7), W - Inches(0.4), H - Inches(0.8))
    return sl

def make_fig13_repr(prs):
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Totani Fig.13 再現】高エネルギー4ビン 残差マップ（我々の版）")
    add_sep(sl)
    existing_sl = prs.slides[34]
    imgs = [sh for sh in existing_sl.shapes if sh.shape_type == 13]
    if imgs:
        img_blob = imgs[0].image.blob
        ext = imgs[0].image.ext
        tmp_path = f"/tmp/fig13_repr.{ext}"
        with open(tmp_path, "wb") as f:
            f.write(img_blob)
        add_img(sl, tmp_path, Inches(0.15), Inches(0.7), width=W - Inches(0.3))
    add_text(sl, [("（注）スライド35と同一。", C_GRAY, False, 11)],
             Inches(0.2), H - Inches(0.45), W - Inches(0.4), Inches(0.4))
    return sl


# ─────────────────────────────────────────────────────────────────────────────
# Fig.14
# ─────────────────────────────────────────────────────────────────────────────

def make_fig14_explain(prs):
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Totani Fig.14 解説】モデルテンプレートのスカイマップ（全成分）")
    add_sep(sl)
    add_text(sl, [
        ("この図は何を示すか", C_CYAN, True, 15),
        ("NFW-ρ² フィット（21 GeV）における全モデルテンプレートの空間分布。", C_WHITE, False, 13),
        ("ハロー成分以外の全6テンプレートを個別に可視化。", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("6つのテンプレート", C_CYAN, True, 15),
        ("上段左: GALPROP gas（π崩壊+制動放射）— 銀河面に集中した複雑な構造", C_WHITE, False, 13),
        ("上段中: Loop I-A シェル（内側シェル, r=50-100° from center l=-31,b=18）", C_WHITE, False, 13),
        ("上段右: Loop I-B シェル（外側シェル, r=100-140°）", C_WHITE, False, 13),
        ("下段左: GALPROP ICS 光学（光学放射場との逆Compton）", C_WHITE, False, 13),
        ("下段中: GALPROP ICS 赤外（IR 放射場との逆Compton）", C_WHITE, False, 13),
        ("下段右: GALPROP ICS CMB（宇宙マイクロ波背景放射との逆Compton）", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("重要な観点", C_CYAN, True, 15),
        ("• GALPROP gas が最も複雑な構造 → ハロー成分との縮退の主な原因", C_WHITE, False, 13),
        ("• ICS 光学/赤外 は球対称ハローに似た形状 → ICS/ハロー縮退のリスクあり", C_RED, False, 13),
        ("• ただし ICS スペクトルはべき乗則 → 20 GeVピークとは異なる", C_WHITE, False, 13),
        ("• Loop I は2シェル構造（A と B が異なる空間分布）", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("我々の再現", C_GREEN, True, 14),
        ("スライド36（テンプレートスカイマップ）+ data/figure-5component/totani_fig14_equiv.png", C_WHITE, False, 13),
    ], Inches(0.2), Inches(0.7), W - Inches(0.4), H - Inches(0.8))
    return sl

def make_fig14_repr(prs):
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Totani Fig.14 再現】各成分のスカイマップ（我々の5成分版）")
    add_sep(sl)
    img_path = "data/figure-5component/totani_fig14_equiv.png"
    if not Path(img_path).exists():
        img_path = "data/figure-5component/all5_overview.png"
    added = add_img(sl, img_path, Inches(0.15), Inches(0.7), width=W - Inches(0.3))
    if not added:
        add_text(sl, [f"画像なし: {img_path}"], Inches(1), Inches(2), W - Inches(2), Inches(2))
    add_text(sl, [
        ("（注）スライド36/data/figure-5component と同一。我々は6成分中5成分を差し引き形で可視化。",
         C_GRAY, False, 11),
    ], Inches(0.2), H - Inches(0.45), W - Inches(0.4), Inches(0.4))
    return sl


# ─────────────────────────────────────────────────────────────────────────────
# Fig.15
# ─────────────────────────────────────────────────────────────────────────────

def make_fig15_explain(prs):
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Totani Fig.15 解説】系統誤差の検討 — 3つの観点", font_size=24)
    add_sep(sl)
    add_text(sl, [
        ("この図の目的", C_CYAN, True, 15),
        ("ハロー超過スペクトル（NFW-ρ²）がモデルパラメータの変更に対してロバストか検証。", C_WHITE, False, 13),
        "3つのパネル（各複数の系統誤差シナリオ）で20 GeVピークが残ることを確認する。",
        ("", C_WHITE, False, 8),
        ("上段: 四象限分割（l>0,b>0 / l<0,b>0 / l<0,b<0 / l>0,b<0 / 平面/極方向）", C_CYAN, True, 14),
        ("→ 20 GeV 以下では全象限で一致したスペクトルトレンド", C_GREEN, False, 13),
        ("→ 30 GeV 以上では統計誤差が大きく象限間のばらつきが増加", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("中段: フェルミバブルテンプレートの変更", C_CYAN, True, 14),
        ("• FB: 4.3→1.5 GeV: 1.5 GeV マップでテンプレート作成 → ゼロ交差が低エネルギー側にシフト", C_WHITE, False, 13),
        ("• FB: structured→flat: フラットテンプレートを使用 → 20 GeV ピークは持続、9.1σ", C_WHITE, False, 13),
        ("• resid.(-) masked: 負残差領域を除外 → 変化なし", C_WHITE, False, 13),
        ("• PS masked: 点源をマスク → 変化なし", C_WHITE, False, 13),
        ("• gas rings & 3 ICS: GALPROP ガスを5リング、ICS3成分に分割 → 21 GeV は不変", C_WHITE, False, 13),
        ("• from LAT GIEM: GIEM を基準にした場合 → 6.7-7.4σ で過剰が残存", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("下段: GALPROPパラメータ変更（5パターン）", C_CYAN, True, 14),
        ("SNR/Z10/R20/T1e5/C5 — いずれも20 GeVピークは持続", C_GREEN, False, 13),
        ("→ 20 GeVハロー過剰はモデル依存性に対してロバスト", C_GREEN, True, 14),
    ], Inches(0.2), Inches(0.7), W - Inches(0.4), H - Inches(0.8))
    return sl

def make_fig15_no_repr(prs):
    return make_no_repr_slide(prs, 15, [
        "• Fig.15 は MCMC を系統誤差シナリオ（10種類以上）で繰り返した結果",
        "• 各系統誤差シナリオに MCMCフィットが必要 → 我々の逐次差し引きでは再現不可",
        "• スライド40（系統誤差の限界論）が Fig.15 の議論に対応する定性的説明",
        "• 本質的な結論: 系統誤差の下でも 20 GeV ピークは持続する（論文の主要結論の一つ）",
    ])


# ─────────────────────────────────────────────────────────────────────────────
# Fig.16
# ─────────────────────────────────────────────────────────────────────────────

def make_fig16_explain(prs):
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Totani Fig.16 解説】DM消滅スペクトルのフィット — WIMPパラメータ導出")
    add_sep(sl)
    add_text(sl, [
        ("この図は何を示すか (§4.2)", C_CYAN, True, 15),
        ("ハロー超過スペクトルを DM消滅γ線スペクトルでフィット → mχ と ⟨σv⟩ を決定。", C_WHITE, False, 13),
        ("4つのパネル（3つの系統誤差シナリオ × NFW-ρ² + 1つの NFW-ρ¹）を比較。", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("フィットの計算式", C_CYAN, True, 15),
        ("dFγ/dEγ = (⟨σv⟩ / 8πmχ²) × dNγ/dEγ × ∫ρ²dl", C_WHITE, False, 13),
        ("∫ρ²dl|G.P. = 8.93×10¹⁴ [M⊙² kpc⁻⁵]（Via Lactea II シミュレーション）", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("3つの消滅チャンネルのフィット結果", C_CYAN, True, 15),
        ("bb̄チャンネル（赤実線）: mχ ≈ 0.5 TeV, ⟨σv⟩ ≈ (5-9)×10⁻²⁵ cm³/s", C_GREEN, True, 14),
        ("W⁺W⁻チャンネル（青破線）: mχ ≈ 0.4-0.6 TeV, ⟨σv⟩ ≈ (5-9)×10⁻²⁵ cm³/s", C_WHITE, False, 13),
        ("τ⁺τ⁻チャンネル（緑点鎖線）: mχ ≈ 0.04-0.08 TeV, ⟨σv⟩ ≈ (7-9)×10⁻²⁶ cm³/s", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("矮小銀河制約との張力", C_RED, True, 14),
        ("⟨σv⟩ ~ 6×10⁻²⁵ cm³/s は矮小銀河の95% 上限値（1×10⁻²⁶ cm³/s）より", C_WHITE, False, 13),
        "約60倍大きい → 標準的な DM密度プロファイルの不確かさでカバーされる範囲内",
        "「~500 GeV DM の bb̄ 消滅」として一貫した解釈が可能（Totaniの主張）",
        ("", C_WHITE, False, 6),
        ("Totani vs DAMPE: mχ ≈ 500 GeV vs 49 GeV — 全く異なる質量スケール！", C_RED, True, 14),
    ], Inches(0.2), Inches(0.7), W - Inches(0.4), H - Inches(0.8))
    return sl

def make_fig16_repr(prs):
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Totani Fig.16 代替】NFWハロースペクトルと予測DMスペクトルの比較")
    add_sep(sl)
    img_path = "data/figure-week780-nfw-fit/nfw_halo_spectrum.png"
    added = add_img(sl, img_path, Inches(0.15), Inches(0.7), height=H - Inches(1.3))
    if not added:
        add_text(sl, [f"画像なし: {img_path}",
                      "python3 code/plot_nfw_halo_fit.py を実行"],
                 Inches(1), Inches(2), W - Inches(2), Inches(2))
    add_text(sl, [
        ("（代替図）我々の NFW ハロースペクトル。DM消滅モデルとの重ね描きは今後の課題。",
         C_GRAY, False, 11),
        ("Totani Fig.16: mχ≈500 GeV, bb̄チャンネルでのフィット曲線（スペクトル形状比較）。",
         C_GRAY, False, 11),
    ], Inches(0.2), H - Inches(0.45), W - Inches(0.4), Inches(0.4))
    return sl


# ─────────────────────────────────────────────────────────────────────────────
# 全スライドを追加
# ─────────────────────────────────────────────────────────────────────────────

new_slides = [
    make_section_header(prs),
    make_fig1_explain(prs),
    make_fig1_repr(prs),
    make_fig2_explain(prs),
    make_fig23_no_repr(prs, 2),
    make_fig3_explain(prs),
    make_fig23_no_repr(prs, 3),
    make_fig4567_explain(prs),
    make_fig4567_no_repr(prs),
    make_fig8_explain(prs),
    make_fig8_repr(prs),
    make_fig9_explain(prs),
    make_fig9_repr(prs),
    make_fig10_explain(prs),
    make_fig10_repr(prs),
    make_fig11_explain(prs),
    make_fig11_repr(prs),
    make_fig12_explain(prs),
    make_fig12_repr(prs),
    make_fig13_explain(prs),
    make_fig13_repr(prs),
    make_fig14_explain(prs),
    make_fig14_repr(prs),
    make_fig15_explain(prs),
    make_fig15_no_repr(prs),
    make_fig16_explain(prs),
    make_fig16_repr(prs),
]

# 末尾に追加されたので位置を調整（全スライドの末尾に配置するので移動不要）
print(f"総スライド数: {len(prs.slides)}")
print(f"追加したスライド数: {len(new_slides)}")

prs.save(str(PPT_PATH))
print("保存完了")
