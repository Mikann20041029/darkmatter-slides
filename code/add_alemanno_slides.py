"""
Alemanno+2026 (DAMPE, ApJS 284, 22) の詳細解説スライドをPPTに追加する。

追加場所: スライド105 (既存Alemannoスライド) の直後
スライド構成:
  A1: DAMPE概要と論文の位置づけ
  A2: データ選択と解析手法 (Section 2)
  A3: Fig.1 — フェルミバブル検出 (26.5σ)
  A4: Fig.2-3 — バブルのテンプレートとエッジ形状
  A5: Fig.4-5 — バブルのSED（フェルミLAT比較）
  A6: Fig.6-7 — 銀河中心超過の検出 (7.5σ)
  A7: Fig.8 — 銀河中心超過のSED
  A8: Fig.9-10 — DM密度プロファイルと形態
  A9: Fig.13-14 — DM消滅パラメータ (mχ≈49 GeV)
  A10: Totani (2025) との比較 — 何が同じで何が違うか
"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from lxml import etree
import copy

PPT_PATH = Path("PPT/slides_v3_detailed_fixed2_final.pptx  -  Repaired.pptx")
prs = Presentation(str(PPT_PATH))

# スライドサイズ
W = prs.slide_width    # ~12188825 EMU = ~9.5 in
H = prs.slide_height   # ~6858000 EMU = ~5.33 in

# カラーパレット
C_BG    = RGBColor(0x05, 0x05, 0x1A)   # 紺黒背景
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
C_TITLE = RGBColor(0xFF, 0xCC, 0x00)   # 黄 (強調)
C_CYAN  = RGBColor(0x00, 0xFF, 0xFF)
C_RED   = RGBColor(0xFF, 0x44, 0x00)
C_GREEN = RGBColor(0x44, 0xFF, 0x88)
C_GRAY  = RGBColor(0xAA, 0xAA, 0xAA)


def blank_slide(prs):
    """ブランクレイアウトの新スライドを作成"""
    blank_layout = prs.slide_layouts[6]  # Blank
    return prs.slides.add_slide(blank_layout)


def set_bg(sl):
    """スライド背景を紺黒に設定"""
    bg = sl.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = C_BG


def add_title(sl, text, color=C_TITLE, font_size=28, top_emu=None):
    """タイトルテキストボックスを追加"""
    if top_emu is None:
        top_emu = Inches(0.05)
    tb = sl.shapes.add_textbox(Inches(0.15), top_emu,
                                W - Inches(0.3), Inches(0.55))
    tf = tb.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.color.rgb = color
    run.font.bold = True


def add_separator(sl, top_emu=None):
    """タイトル下の区切り線"""
    if top_emu is None:
        top_emu = Inches(0.62)
    from pptx.util import Emu
    box = sl.shapes.add_shape(
        1, Inches(0.15), top_emu, W - Inches(0.3), Inches(0.02)
    )
    box.fill.solid()
    box.fill.fore_color.rgb = C_CYAN
    box.line.fill.background()


def add_textbox(sl, text_lines, left, top, width, height,
                font_size=13, color=C_WHITE, bold=False):
    """複数行テキストボックスを追加。text_linesは [(テキスト, color, bold, size), ...] または str"""
    tb = sl.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True

    if isinstance(text_lines, str):
        text_lines = [(text_lines, color, bold, font_size)]

    first = True
    for item in text_lines:
        if isinstance(item, str):
            item = (item, color, bold, font_size)
        line_text, line_color, line_bold, line_size = item

        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()

        p.space_before = Pt(2)
        run = p.add_run()
        run.text = line_text
        run.font.size = Pt(line_size)
        run.font.color.rgb = line_color
        run.font.bold = line_bold


def make_box_bg(sl, left, top, width, height, color):
    """背景色付きの矩形（テキストなし）"""
    box = sl.shapes.add_shape(1, left, top, width, height)
    box.fill.solid()
    box.fill.fore_color.rgb = color
    box.line.fill.background()
    return box


# ─────────────────────────────────────────────────────────────────────────────
# 挿入位置を決定（スライド105の直後）
# ─────────────────────────────────────────────────────────────────────────────

INSERT_AFTER = 104  # 0-indexed: スライド105の次に挿入

def insert_slide_after(prs, index, new_slide):
    """new_slide を index の直後に移動する（add_slideで末尾に追加後に移動）"""
    xml_slides = prs.slides._sldIdLst
    # 末尾の要素（新スライド）を取り出して index+1 の位置に挿入
    last = xml_slides[-1]
    xml_slides.remove(last)
    xml_slides.insert(index + 1, last)


# ─────────────────────────────────────────────────────────────────────────────
# スライド作成関数
# ─────────────────────────────────────────────────────────────────────────────

def make_slide_A1(prs):
    """A1: DAMPE概要と論文の位置づけ"""
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【参考論文解説】Alemanno+2026 (DAMPE) — 概要と位置づけ")
    add_separator(sl)

    # 左カラム: DAMPEとは
    add_textbox(sl, [
        ("DAMPE とは何か", C_CYAN, True, 16),
        ("Dark Matter Particle Explorer（暗黒物質粒子探索機）", C_WHITE, False, 13),
        ("• 中国の宇宙望遠鏡（2015年12月打ち上げ）", C_WHITE, False, 12),
        ("• γ線・宇宙線を2GeV〜10TeVで観測", C_WHITE, False, 12),
        ("• 有効面積ピーク〜2000 cm²（Fermiの3〜4倍）", C_WHITE, False, 12),
        ("• 102ヶ月（8.5年）のデータ", C_WHITE, False, 12),
        ("• 高エネルギー分解能が強み", C_WHITE, False, 12),
        ("", C_WHITE, False, 8),
        ("この論文 (ApJS 284, 22, 2026) の主張", C_CYAN, True, 16),
        ("Fermi-LAT 以外の望遠鏡で初めて独立検証：", C_WHITE, False, 13),
        ("① フェルミバブルを 26.5σ で検出", C_GREEN, True, 14),
        ("② 銀河中心(GC)GeV過剰を 7.5σ で検出", C_GREEN, True, 14),
        ("", C_WHITE, False, 8),
        ("→ DM消滅解釈:", C_WHITE, False, 13),
        ("  mχ ≈ 49 GeV (bb̄チャンネル)", C_TITLE, True, 14),
        ("  <σv>bb ≈ 1.9×10⁻²⁶ cm³/s", C_TITLE, True, 14),
    ], Inches(0.2), Inches(0.7), Inches(5.8), Inches(5.0))

    # 右カラム: Totaniとの対比
    add_textbox(sl, [
        ("Totani (2025) との対比", C_RED, True, 16),
        ("", C_WHITE, False, 6),
        ("観測量", C_GRAY, True, 12),
        ("検出器     DAMPE vs Fermi-LAT", C_WHITE, False, 12),
        ("期間       8.5年 vs ~15年", C_WHITE, False, 12),
        ("エネルギー  2–200 GeV vs 1.5–814 GeV", C_WHITE, False, 12),
        ("", C_WHITE, False, 8),
        ("異なる点", C_CYAN, True, 13),
        ("GC超過の解釈:", C_WHITE, False, 12),
        ("  DAMPE:  mχ≈49 GeV (1–3 GeV で peak)", C_WHITE, False, 12),
        ("  Totani:  mχ≈500 GeV (20 GeV で peak)", C_WHITE, False, 12),
        ("", C_WHITE, False, 6),
        ("対象領域:", C_WHITE, False, 12),
        ("  DAMPE:  GC周辺 ROI=40°×40°", C_WHITE, False, 12),
        ("  Totani:  MW全体 |l|≤60°", C_WHITE, False, 12),
        ("", C_WHITE, False, 8),
        ("共通する点 ✓", C_GREEN, True, 13),
        ("• フェルミバブル・GC超過の両方を検出", C_WHITE, False, 12),
        ("• GALPROP+LoopI+点源を成分として考慮", C_WHITE, False, 12),
        ("• gNFW密度プロファイルを使用", C_WHITE, False, 12),
        ("• Fermi-LATデータと整合", C_WHITE, False, 12),
    ], Inches(6.2), Inches(0.7), Inches(5.5), Inches(5.0))

    return sl


def make_slide_A2(prs):
    """A2: データ選択と解析手法"""
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Alemanno+2026】§2 データ選択と解析手法")
    add_separator(sl)

    add_textbox(sl, [
        ("§2.1 DAMPEデータ", C_CYAN, True, 15),
        ("• 期間: 2016年1月〜2024年6月（102ヶ月）", C_WHITE, False, 13),
        ("• 光子イベント数: 約359,000個（2GeV以上）", C_WHITE, False, 13),
        ("• CR汚染除去: v.6.0.3アルゴリズム（陽子50%減、電子15%減、−3%の損失）", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("§2.2 γ線放射成分（Table 2）", C_CYAN, True, 15),
        ("フェルミバブル解析 ROI: 5°≤|b|≤60°, |ℓ|≤60°", C_WHITE, False, 13),
        ("GC超過解析 ROI: 1°≤|b|≤20°, |ℓ|≤20°", C_WHITE, False, 13),
        ("", C_WHITE, False, 6),
        ("考慮した成分:", C_WHITE, True, 14),
        ("  ① H1・H2ガス関連放射（GALPROP）", C_WHITE, False, 13),
        ("  ② 逆Compton散乱（IC）放射", C_WHITE, False, 13),
        ("  ③ Loop I（幾何テンプレート）", C_WHITE, False, 13),
        ("  ④ 等方背景（露出マップに比例）→ Fermiと異なる点！", C_RED, False, 13),
        ("  ⑤ 点源（DAMPEカタログ + Fermi 4FGL-DR4 弱点源）", C_WHITE, False, 13),
        ("  ⑥ フェルミバブル（フラットテンプレート）", C_WHITE, False, 13),
        ("  ⑦ GC超過（gNFW J因子マップ）", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("§2.3 尤度解析", C_CYAN, True, 15),
        ("ln L = Σᵢⱼ [Nᵢⱼ ln(μ̃ᵢⱼ) − μ̃ᵢⱼ]  （ポアソン対数尤度）", C_WHITE, False, 13),
        ("ビン×ビン解析でSEDを導出（エネルギービン20個: 2–200 GeV）", C_WHITE, False, 13),
    ], Inches(0.2), Inches(0.7), W - Inches(0.4), Inches(5.5))

    return sl


def make_slide_A3(prs):
    """A3: Fig.1 フェルミバブル検出"""
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Alemanno+2026 Fig.1】フェルミバブルの検出 (26.5σ)")
    add_separator(sl)

    add_textbox(sl, [
        ("Fig.1 の内容", C_CYAN, True, 15),
        ("(a) 観測強度マップ（2–500 GeV積分）", C_WHITE, False, 13),
        ("(b) ベストフィットモデルマップ（バブルなしnull model）", C_WHITE, False, 13),
        ("(c) 残差の有意度マップ（null model引き算後）", C_WHITE, False, 13),
        ("(d) バブルモデル込みの残差有意度マップ", C_WHITE, False, 13),
    ], Inches(0.2), Inches(0.7), Inches(6.0), Inches(2.5))

    add_textbox(sl, [
        ("読み取るべきポイント", C_TITLE, True, 15),
        ("• (c) でバブル領域に赤い超過（正の残差）が見える", C_WHITE, False, 13),
        ("• (d) でバブルを含めると残差が白くなる → well-fitted", C_WHITE, False, 13),
        ("• 有意度 TS（=−2ΔlnL）= 757 → 26.5σ", C_GREEN, True, 14),
        ("• バブルの形状はFermi-LAT (Su+2010) と〜6%の差で一致", C_WHITE, False, 13),
    ], Inches(0.2), Inches(3.3), Inches(6.0), Inches(2.8))

    add_textbox(sl, [
        ("重要な技術的注意点", C_RED, True, 15),
        ("• バブルのテンプレートを直接論文から取らず、", C_WHITE, False, 13),
        ("  残差マップから新たに導出している（Fig.2参照）", C_WHITE, False, 13),
        ("• 有意度の計算方法: (Nᵢ − μ̃ᵢ)/√μ̃ᵢ", C_WHITE, False, 13),
        ("", C_WHITE, False, 6),
        ("私たちの研究との関係", C_CYAN, True, 14),
        ("• 私たちはフェルミバブルを", C_WHITE, False, 13),
        ("  4.31 GeV残差テンプレートで差し引いている", C_WHITE, False, 13),
        ("• DAMPEも同様の「残差から導出」アプローチ", C_WHITE, False, 13),
        ("• ROIが異なる（DAMPE: 5°≤|b|≤60° vs 我々: 10°≤|b|≤60°）", C_WHITE, False, 13),
    ], Inches(6.2), Inches(0.7), Inches(5.5), Inches(5.0))

    return sl


def make_slide_A4(prs):
    """A4: Fig.2-3 バブルのテンプレート定義とエッジ形状"""
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Alemanno+2026 Fig.2-3】バブルのテンプレート定義とエッジ形状")
    add_separator(sl)

    add_textbox(sl, [
        ("Fig.2: バブル境界の定義（左・右）", C_CYAN, True, 15),
        ("左: null model 引き算後の残差有意度のヒストグラム", C_WHITE, False, 13),
        ("  • バブル内（赤）: 正側に偏っている", C_WHITE, False, 13),
        ("  • バブル外（緑）: ゼロ近傍に集中", C_WHITE, False, 13),
        ("  • 2σbg カットで境界を定義", C_WHITE, False, 13),
        ("右: 有意度マップ上のバブル境界（白実線）", C_WHITE, False, 13),
        ("  → Su+2010, Ackermann+2014, Keshet+2017 の境界と比較", C_WHITE, False, 13),
        ("  → DAMPEの境界はFermi-LATと概ね一致（南が〜6%小さい）", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("Fig.3: バブルエッジからの距離と平均残差フラックス", C_CYAN, True, 15),
        ("• 負（ゼロ左）= バブル内部", C_WHITE, False, 13),
        ("• 正（ゼロ右）= バブル外部", C_WHITE, False, 13),
        ("• エッジで急激なフラックス変化 → シャープなエッジ", C_WHITE, False, 13),
        ("• これはフラットバブルテンプレートの妥当性を支持", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("まとめ: なぜフラットテンプレートか？", C_TITLE, True, 14),
        ("バブル内部はフラックスがほぼ均一（フラットなSED）+ シャープなエッジ", C_WHITE, False, 13),
        ("→ フラットテンプレートが最適（私たちの解析と同じアプローチ）", C_GREEN, False, 13),
    ], Inches(0.2), Inches(0.7), W - Inches(0.4), Inches(5.5))

    return sl


def make_slide_A5(prs):
    """A5: Fig.4-5 フェルミバブルのSED"""
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Alemanno+2026 Fig.4-5】フェルミバブルのスペクトル (SED)")
    add_separator(sl)

    add_textbox(sl, [
        ("Fig.4: バブルのSED（全体）", C_CYAN, True, 15),
        ("左: 全成分の寄与（ROI内の平均フラックス）", C_WHITE, False, 13),
        ("  • データ(黒)、バブル(赤)、GALPROP、Loop I、等方背景などを表示", C_WHITE, False, 13),
        ("  • バブルはROIの光子の3〜10%程度", C_WHITE, False, 13),
        ("右: バブルのみのSED（Fermi-LAT Ackermann+2014 と比較）", C_WHITE, False, 13),
        ("  • DAMPE(赤)とFermi(青)が高い精度で一致", C_GREEN, False, 13),
        ("  • ハードスペクトル: Γ₁=−1.99、カットオフ Ecut=204 GeV", C_WHITE, False, 13),
        ("  • TS=757 → 有意度 26.5σ", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("Fig.5: 南北ローブ別のSED", C_CYAN, True, 15),
        ("• 北ローブ(青): Γ₁=−1.95, Ecut=174 GeV, TS=236.8 → 14σ", C_WHITE, False, 13),
        ("• 南ローブ(橙): Γ₁=−2.01, Ecut=221 GeV, TS=533.5 → 22σ", C_WHITE, False, 13),
        ("• 両スペクトルは非常によく一致 → 同一起源", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("Table 3: バブルSED（エネルギービンごと）", C_TITLE, True, 14),
        ("E=2–3.17 GeV: E²dN/dE = (6.14±0.75)×10⁻⁷ [単位: GeV cm⁻² s⁻¹ sr⁻¹]", C_WHITE, False, 12),
        ("E=3.17–5 GeV: (6.51±0.54)×10⁻⁷", C_WHITE, False, 12),
        ("...（計9ビン、TS値も記載）", C_GRAY, False, 12),
    ], Inches(0.2), Inches(0.7), W - Inches(0.4), Inches(5.5))

    return sl


def make_slide_A6(prs):
    """A6: Fig.6-7 銀河中心超過の検出"""
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Alemanno+2026 Fig.6-7】銀河中心GeV超過の検出 (7.5σ)")
    add_separator(sl)

    add_textbox(sl, [
        ("Fig.6: GC超過の強度マップと有意度マップ", C_CYAN, True, 15),
        ("(a) 観測強度マップ（2–200 GeV）— 銀河面がマスク（|b|<1°）", C_WHITE, False, 13),
        ("(b) ベストフィットnullモデル（GC超過なし）", C_WHITE, False, 13),
        ("(c) nullモデル残差: GC付近に赤い超過が見える", C_WHITE, False, 13),
        ("(d) gNFWモデル込み: 残差がほぼ消える", C_WHITE, False, 13),
        ("", C_WHITE, False, 6),
        ("ROI: 1°≤|b|≤20°, |ℓ|≤20°（GC付近に集中）", C_WHITE, False, 13),
        ("空間ビン: 0.1°×0.1°（CAR投影、400×400ピクセル）", C_WHITE, False, 13),
        ("TS_gNFW = 80.1 → 有意度 7.5σ（全エネルギー統合）", C_GREEN, True, 14),
        ("", C_WHITE, False, 8),
        ("Fig.7: GCからの角度別残差フラックス", C_CYAN, True, 15),
        ("灰色点: gNFWモデル（DM込み）の残差", C_WHITE, False, 13),
        ("青点: gNFW + GC超過テンプレートの残差", C_WHITE, False, 13),
        ("→ 超過は中心（r≤2°）に集中、外側はほぼゼロ", C_WHITE, False, 13),
        ("→ GC中心に向かうほど強い → DM密度プロファイルと矛盾しない", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("私たちとの違い", C_RED, True, 14),
        ("我々: 銀河全体（MW halo）でNFW振幅が20 GeVで上昇 (Totani)", C_WHITE, False, 13),
        ("DAMPE: GC中心部（40°×40°ROI）で1–3 GeVに集中したGeV超過", C_WHITE, False, 13),
    ], Inches(0.2), Inches(0.7), W - Inches(0.4), Inches(5.5))

    return sl


def make_slide_A7(prs):
    """A7: Fig.8 GC超過のSED"""
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Alemanno+2026 Fig.8】銀河中心GeV超過のスペクトル")
    add_separator(sl)

    add_textbox(sl, [
        ("Fig.8: GC超過のSED（Table 4）", C_CYAN, True, 15),
        ("左: ROI内の各成分寄与（GC中心5°から）", C_WHITE, False, 13),
        ("  • GC超過（赤）: Fermiバブルよりも小さいがGCに集中", C_WHITE, False, 13),
        ("  • 2–20 GeVのビンに有意な信号", C_WHITE, False, 13),
        ("右: GC超過のみのSED（GCから5°での積分フラックス）", C_WHITE, False, 13),
        ("  • 2–3.17 GeV: E²dN/dE = (3.27±0.67)×10⁻⁶ [GeV cm⁻² s⁻¹ sr⁻¹]", C_WHITE, False, 12),
        ("  • 3.17–5 GeV: (2.05±0.47)×10⁻⁶", C_WHITE, False, 12),
        ("  • 5–8 GeV: (2.05±0.44)×10⁻⁶", C_WHITE, False, 12),
        ("  • >12.6 GeV: 上限値のみ（TS<4）", C_GRAY, False, 12),
        ("  → スペクトルは1–3 GeVでピーク → 低エネルギーの超過", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("Fermi-LAT先行研究との比較", C_CYAN, True, 15),
        ("Calore+2015b、Cholis+2022: Fermi-LATでの従来のGCE解析", C_WHITE, False, 13),
        ("→ DAMPEの結果はFermi-LATと概ね整合", C_GREEN, False, 13),
        ("→ 8〜20 GeVで微妙な張力（DAMPE上限 < Fermi観測）", C_WHITE, False, 13),
        ("  原因: 20 GeV付近のGDE系統誤差の影響か？", C_GRAY, False, 13),
        ("", C_WHITE, False, 8),
        ("Totaniとの比較", C_RED, True, 14),
        ("Totani (2025): 20 GeV に鋭いピーク → mχ≈500 GeV", C_WHITE, False, 13),
        ("DAMPE (2026): 1–3 GeV でピーク → mχ≈49 GeV", C_WHITE, False, 13),
        ("→ 同じ「銀河中心超過」でも解釈が全く異なる！", C_RED, True, 13),
    ], Inches(0.2), Inches(0.7), W - Inches(0.4), Inches(5.5))

    return sl


def make_slide_A8(prs):
    """A8: Fig.9-10 DM密度プロファイルと形態"""
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Alemanno+2026 Fig.9-10】DM密度プロファイルと形態研究")
    add_separator(sl)

    add_textbox(sl, [
        ("Fig.9: gNFWプロファイルの内部密度勾配γ, 楕円率ε, 中心位置", C_CYAN, True, 15),
        ("最適密度プロファイル（全3パネル）:", C_WHITE, False, 13),
        ("  上: γ = 1.23±0.08（内部勾配）→ 通常NFW(γ=1.0)より急峻", C_WHITE, False, 13),
        ("    理由: バリオンによるDMハロー圧縮（adiabatic contraction）", C_WHITE, False, 13),
        ("  中: 楕円率 ε = 1.0+0.3−0.2 → 球対称と整合（ε>1でGP方向に伸長）", C_WHITE, False, 13),
        ("  下: 中心位置 dℓ = −0.1°, db = 0° → GC動力学中心と整合", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("Fig.10: 空間モデル比較（gNFW, Boxy Bulge, X-shaped Bulge）", C_CYAN, True, 15),
        ("(a) gNFW (γ=1.2): 球対称に中心に集中", C_WHITE, False, 13),
        ("(b) Boxy Bulge (C20NP): ボックス状の膨らみ", C_WHITE, False, 13),
        ("(c) X-shaped Bulge: X字型", C_WHITE, False, 13),
        ("", C_WHITE, False, 6),
        ("Table 5: TS値比較", C_WHITE, False, 13),
        ("gNFW(γ=1.2): TS=80.1（最良）", C_GREEN, False, 13),
        ("X-shaped:     TS=78.8", C_WHITE, False, 13),
        ("Boxy (C20NP): TS=77.8", C_WHITE, False, 13),
        ("→ gNFWが統計的に最良だが、バルジモデルも許容範囲内", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("物理的含意", C_TITLE, True, 14),
        ("超過が球対称でGC中心 → DM消滅の特徴と一致", C_WHITE, False, 13),
        ("MSPパルサー説（ミリ秒パルサー集団）は球対称を好まない → DM説が有利", C_WHITE, False, 13),
    ], Inches(0.2), Inches(0.7), W - Inches(0.4), Inches(5.5))

    return sl


def make_slide_A9(prs):
    """A9: Fig.13-14 DM消滅パラメータ"""
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Alemanno+2026 Fig.13-14】DM消滅パラメータの導出")
    add_separator(sl)

    add_textbox(sl, [
        ("§4.4 DM消滅パラメータ導出", C_CYAN, True, 15),
        ("GC超過スペクトルをDMプロンプトγ線スペクトルでフィット:", C_WHITE, False, 13),
        ("  dN/dE = (1/4π) × (⟨σv⟩/2mχ²) × (dNf/dE) × J", C_WHITE, False, 13),
        ("  J因子: DMハロー密度の視線積分（gNFW, rs=20 kpc）", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("Fig.13: GC超過のSEDとDM消滅モデルのフィット", C_CYAN, True, 15),
        ("• bb̄チャンネル（青点線, mχ=49 GeV）: スペクトルと良好一致", C_WHITE, False, 13),
        ("• τ⁺τ⁻チャンネル（橙点線, mχ=13 GeV）: 低エネルギー側を説明", C_WHITE, False, 13),
    ], Inches(0.2), Inches(0.7), Inches(6.0), Inches(3.2))

    add_textbox(sl, [
        ("Fig.14: mχ − ⟨σv⟩ 制約平面（bb̄ / τ⁺τ⁻）", C_CYAN, True, 15),
        ("bb̄ チャンネル（Fig.14a）:", C_WHITE, False, 13),
        ("  mχ = 49+16−12 GeV（1σ）", C_GREEN, True, 14),
        ("  ⟨σv⟩bb = 1.9+0.4−0.3 ×10⁻²⁶ cm³/s", C_GREEN, True, 14),
        ("", C_WHITE, False, 6),
        ("τ⁺τ⁻ チャンネル（Fig.14b）:", C_WHITE, False, 13),
        ("  mχ = 13.0+1.0−1.8 GeV", C_WHITE, False, 13),
        ("  ⟨σv⟩ττ = (6.0±0.9)×10⁻²⁷ cm³/s", C_WHITE, False, 13),
        ("", C_WHITE, False, 6),
        ("矮小銀河観測との比較（青点線）:", C_WHITE, False, 13),
        ("  一部のパラメータ空間は矮小銀河観測で除外される", C_WHITE, False, 13),
    ], Inches(6.2), Inches(0.7), Inches(5.5), Inches(3.5))

    add_textbox(sl, [
        ("Totani (2025) との決定的な違い", C_RED, True, 14),
        ("DAMPE GCE: mχ≈49 GeV (bb̄), 1–3 GeV にピーク", C_WHITE, False, 13),
        ("Totani MWハロー: mχ≈500 GeV, 20 GeV にピーク", C_WHITE, False, 13),
        ("→ 同じDM消滅でも全く異なる信号！異なる領域・エネルギーを観ている", C_RED, False, 13),
    ], Inches(0.2), Inches(4.2), W - Inches(0.4), Inches(1.5))

    return sl


def make_slide_A10(prs):
    """A10: Totani (2025)との総合比較"""
    sl = blank_slide(prs)
    set_bg(sl)
    add_title(sl, "【Alemanno+2026 vs Totani+2025】— 両論文の総合比較と本研究の位置づけ")
    add_separator(sl)

    # 比較表ヘッダー
    add_textbox(sl, [
        ("項目", C_GRAY, True, 13),
    ], Inches(0.2), Inches(0.75), Inches(2.5), Inches(0.4))
    add_textbox(sl, [
        ("DAMPE (Alemanno+2026)", C_CYAN, True, 13),
    ], Inches(2.7), Inches(0.75), Inches(4.0), Inches(0.4))
    add_textbox(sl, [
        ("Fermi-LAT (Totani+2025)", C_TITLE, True, 13),
    ], Inches(6.7), Inches(0.75), Inches(4.0), Inches(0.4))

    # テーブル行
    rows = [
        ("検出器", "DAMPE衛星（中国）", "Fermi-LAT衛星（NASA）"),
        ("データ期間", "2016–2024（8.5年）", "2008–2022（~15年）"),
        ("エネルギー範囲", "2–200 GeV（20ビン）", "1.5–814 GeV（13ビン）"),
        ("対象領域", "GC付近 40°×40°", "MW全体 |l|≤60°"),
        ("等方背景の扱い", "露出マップに比例（自由パラメータ）", "|b|≥50°平均値として差し引き"),
        ("GC超過の検出", "7.5σ（1–3 GeVに集中）", "20 GeVに過剰（NFW解析）"),
        ("フェルミバブル", "26.5σで検出", "テンプレートとして差し引き"),
        ("DM質量（bb̄）", "mχ≈49 GeV", "mχ≈500 GeV（試算）"),
        ("先行研究との整合", "Fermi-LATと良好一致", "Fermi-LATで過去未検出"),
    ]

    y_start = Inches(1.15)
    for i, (label, dampe_val, totani_val) in enumerate(rows):
        y = y_start + Inches(i * 0.43)
        bg_color = RGBColor(0x10, 0x10, 0x30) if i % 2 == 0 else RGBColor(0x15, 0x15, 0x40)
        make_box_bg(sl, Inches(0.15), y, W - Inches(0.3), Inches(0.42), bg_color)
        add_textbox(sl, [(label, C_GRAY, True, 11)],
                    Inches(0.2), y + Inches(0.04), Inches(2.4), Inches(0.38))
        add_textbox(sl, [(dampe_val, C_CYAN, False, 11)],
                    Inches(2.7), y + Inches(0.04), Inches(3.9), Inches(0.38))
        add_textbox(sl, [(totani_val, C_TITLE, False, 11)],
                    Inches(6.7), y + Inches(0.04), Inches(3.9), Inches(0.38))

    # 本研究の位置づけ
    y_bot = y_start + Inches(len(rows) * 0.43) + Inches(0.1)
    add_textbox(sl, [
        ("本研究（中村）の位置づけ:", C_GREEN, True, 13),
        ("TotaniのMWハロー20GeV信号を独立再現 → DAMPEのGCE(1–3 GeV)とは異なる信号を追う", C_WHITE, False, 12),
        ("矮小銀河5天体での非検出 → DAMPEと整合（矮小銀河では両方の信号ともTS<4）", C_WHITE, False, 12),
    ], Inches(0.2), y_bot, W - Inches(0.4), Inches(0.8))

    return sl


# ─────────────────────────────────────────────────────────────────────────────
# スライドを追加して位置を調整
# ─────────────────────────────────────────────────────────────────────────────

new_slides = [
    make_slide_A1(prs),
    make_slide_A2(prs),
    make_slide_A3(prs),
    make_slide_A4(prs),
    make_slide_A5(prs),
    make_slide_A6(prs),
    make_slide_A7(prs),
    make_slide_A8(prs),
    make_slide_A9(prs),
    make_slide_A10(prs),
]

# 追加したスライドをスライド105の直後に移動
# スライドは末尾に追加されているので、現在の末尾からINSERT_AFTER+1の位置に移動
n_new = len(new_slides)
total = len(prs.slides)
xml_slides = prs.slides._sldIdLst

# 末尾のn_new枚を取り出してINSERT_AFTER+1の位置に挿入
moved = list(xml_slides[-n_new:])
for elem in moved:
    xml_slides.remove(elem)
for i, elem in enumerate(moved):
    xml_slides.insert(INSERT_AFTER + 1 + i, elem)

print(f"スライド総数: {len(prs.slides)}")
print(f"挿入位置: スライド{INSERT_AFTER+1}の後 → スライド{INSERT_AFTER+2}〜{INSERT_AFTER+1+n_new}")

prs.save(str(PPT_PATH))
print("保存完了")
