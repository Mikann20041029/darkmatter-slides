#!/usr/bin/env python3
"""
2026-07-16 中間卒論発表(8分、教授多数)用 PPT (interim_report) をゼロから再構築する。

タイトル:「銀河の中心からのガンマ線過剰を統計的に探る」神奈川大学 中村惺一

旧版(2026-07-03作成)は GALPROP=gll_iem_v07.fits・露出マップ未取得・6成分・
f_halo=16.6(約11σ)前提で書かれており、その後の全ての進展
(実測露出マップ取得, GALPROP gas/ICS分離実装, 4FGL-DR4更新, 全13ビンMCMC,
本日のフェルミバブル内外ロバスト性検証・戸谷比較表)で内容が古くなっていた。
本スクリプトは2026-07-16時点の到達点(`.dev/HANDOFF.md`,
`.dev/teams/galprop-gas-ics-separation/verdict.md`,
`.dev/teams/regionAC-lrt-halo-test/verdict.md`)に基づき全面的に書き直す。

方針: テキスト少なめ・画像中心。スライドの文字は読み上げず、話す内容は
ノートに書く(ユーザー指示、2026-07-16)。

出力: interim/interim_report.pptx

[2026-07-16] 出力先をPPT/interim/からリポジトリ直下のinterim/に変更した。
ユーザーがinterim/を「グラフを自分のコードで書き直す作業場所」として新設し、
そこにPPTファイルも一緒に置く方針としたため(interim/README.md参照)。
"""

import pathlib as _pathlib
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

BASE = _pathlib.Path(__file__).resolve().parent.parent
OUT = BASE / "interim/interim_report.pptx"
OUT.parent.mkdir(parents=True, exist_ok=True)

DARK_BG = RGBColor(0x05, 0x05, 0x1A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
ACCENT = RGBColor(0xFF, 0xCC, 0x00)
GREY = RGBColor(0xAA, 0xAA, 0xAA)
RED = RGBColor(0xFF, 0x55, 0x55)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def add_slide():
    return prs.slides.add_slide(BLANK)


def set_bg(slide, color=DARK_BG):
    bg = slide.background
    bg.fill.solid()
    bg.fill.fore_color.rgb = color


def add_title(slide, text, size=30, top=Inches(0.3), color=WHITE):
    box = slide.shapes.add_textbox(Inches(0.5), top, Inches(12.3), Inches(0.9))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = True
    p.font.color.rgb = color
    return box


def add_bullets(slide, items, left=Inches(0.6), top=Inches(1.35),
                 width=Inches(12.0), height=Inches(5.3), size=19, color=WHITE):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"・ {item}"
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.space_after = Pt(8)
    return box


def add_image_centered(slide, path, top=Inches(1.25), max_h=Inches(5.8), max_w=Inches(12.3)):
    from PIL import Image
    with Image.open(path) as im:
        w_px, h_px = im.size
    ratio = w_px / h_px
    h = max_h
    w = Emu(int(h * ratio))
    if w > max_w:
        w = max_w
        h = Emu(int(w / ratio))
    left = Emu(int((prs.slide_width - w) / 2))
    slide.shapes.add_picture(str(path), left, top, height=h, width=w)
    return top, h


def add_image_at(slide, path, left, top, max_h=None, max_w=None):
    from PIL import Image
    with Image.open(path) as im:
        w_px, h_px = im.size
    ratio = w_px / h_px
    if max_h is not None:
        h = max_h
        w = Emu(int(h * ratio))
        if max_w is not None and w > max_w:
            w = max_w
            h = Emu(int(w / ratio))
    else:
        w = max_w
        h = Emu(int(w / ratio))
    slide.shapes.add_picture(str(path), left, top, height=h, width=w)
    return w, h


def add_caption(slide, text, top, color=GREY, size=13, align=PP_ALIGN.CENTER):
    box = slide.shapes.add_textbox(Inches(0.5), top, Inches(12.3), Inches(0.5))
    p = box.text_frame.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.color.rgb = color
    p.alignment = align


def set_notes(slide, text):
    notes = slide.notes_slide
    notes.notes_text_frame.text = text


def add_table(slide, rows, col_widths, left=Inches(0.7), top=Inches(1.3),
              row_h=Inches(0.55), header_color=RGBColor(0x22, 0x22, 0x44),
              font_size=15):
    n_rows = len(rows)
    n_cols = len(col_widths)
    width = sum(col_widths, Emu(0))
    height = row_h * n_rows
    gshape = slide.shapes.add_table(n_rows, n_cols, left, top, width, height)
    table = gshape.table
    for c, w in enumerate(col_widths):
        table.columns[c].width = w
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            cell = table.cell(r, c)
            cell.text = str(val)
            cell.fill.solid()
            cell.fill.fore_color.rgb = header_color if r == 0 else DARK_BG
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(font_size)
                p.font.bold = (r == 0)
                p.font.color.rgb = ACCENT if r == 0 else WHITE
    return gshape


FIG = BASE / "data"
RES = BASE / "results"

# ============================================================
# Slide 1 — Title
# ============================================================
s = add_slide(); set_bg(s)
box = s.shapes.add_textbox(Inches(0.8), Inches(2.3), Inches(11.7), Inches(1.6))
p = box.text_frame.paragraphs[0]
p.text = "銀河の中心からのガンマ線過剰を統計的に探る"
p.font.size = Pt(40); p.font.bold = True; p.font.color.rgb = WHITE
p.alignment = PP_ALIGN.CENTER
box2 = s.shapes.add_textbox(Inches(0.8), Inches(3.9), Inches(11.7), Inches(0.8))
p2 = box2.text_frame.paragraphs[0]
p2.text = "中間発表 — Totani (2025) 20 GeV ガンマ線超過の検証と矮小銀河・M31への応用"
p2.font.size = Pt(20); p2.font.color.rgb = ACCENT
p2.alignment = PP_ALIGN.CENTER
box3 = s.shapes.add_textbox(Inches(0.8), Inches(5.6), Inches(11.7), Inches(0.6))
p3 = box3.text_frame.paragraphs[0]
p3.text = "神奈川大学　中村惺一"
p3.font.size = Pt(20); p3.font.color.rgb = WHITE
p3.alignment = PP_ALIGN.CENTER
set_notes(s, (
    "持ち時間8分。研究テーマは「Fermi-LATデータを用いたTotani(2025) 20 GeVガンマ線超過の"
    "独立検証」と「同じ手法を5つの矮小銀河・M31に応用した探索」の2本柱。スライドの文字は"
    "読み上げず、画像を指しながら口頭で説明する方針で進める。"
))

# ============================================================
# Slide 2 — Index
# ============================================================
s = add_slide(); set_bg(s)
add_title(s, "目次")
add_bullets(s, [
    "研究の背景と目的（WIMP対消滅とガンマ線）",
    "手法：解析対象領域と7成分モデル",
    "手法：MCMC同時フィット・GALPROP gas/ICS分離",
    "手法：矮小銀河5天体・M31への拡張（ON/OFF法）",
    "結果：全13ビンでのハロー有意度スペクトル",
    "結果：Totani (2025) との比較・領域分割ロバスト性検証",
    "結果：矮小銀河5天体・M31への適用",
    "Discussion：見つかった2つの未解決の縮退",
    "Conclusion と今後の方針",
], size=21)
set_notes(s, "全体の流れを30秒で提示。項目名を読み上げるだけに留め、詳細は各セクションで話す。")

# ============================================================
# Slide 3 — Introduction with Feynman diagram
# ============================================================
s = add_slide(); set_bg(s)
add_title(s, "研究の背景・目的", size=28)
add_image_centered(s, FIG / "figure-intro/wimp_feynman.png", top=Inches(1.35), max_h=Inches(4.25))
add_bullets(s, [
    "データ: Fermi-LAT Pass 8, 780週分（15年分, HEASARC公開データ）",
    "先行研究: Totani (2025) が銀河ハロー高緯度領域(|b|=10–60°)で 20 GeV 付近に"
    "ダークマター対消滅起源とみられるガンマ線超過を報告",
    "目的①独立再現　目的②矮小銀河5天体・M31への応用探索",
], top=Inches(5.75), size=16, height=Inches(1.6))
set_notes(s, (
    "図の説明: WIMP同士(χχ)が対消滅し、クォーク対(qq̄)を経てハドロン化、"
    "中性パイオン(π⁰)が2本のガンマ線に崩壊する、というのがダークマター起源説の"
    "標準的な生成過程。ガンマ線のエネルギーはWIMP質量のおおよそ数分の1〜十分の1に"
    "対応するため、20 GeVというピークエネルギーは数百GeV〜1TeV程度のWIMP質量を"
    "示唆する（これは後述のDiscussionで示す我々のスペクトルフィット結果とも関連づける）。"
    "データはFermi Gamma-ray Space Telescope搭載LAT検出器のPass 8イベント、"
    "HEASARCから週次FITSとして公開されているものを780週(15年)分使用、"
    "Totaniと同じデータソース・観測期間。研究は「独立再現」と「矮小銀河・M31への拡張」"
    "の2本柱であることを明言する。"
))

# ============================================================
# Slide 4 — ROI and 7-component model
# ============================================================
s = add_slide(); set_bg(s)
add_title(s, "解析対象領域と7成分モデル", size=26)
add_image_centered(s, FIG / "figure-5component/all5_overview.png", max_h=Inches(5.6))
set_notes(s, (
    "ROI: |l|≤60°, 10°≤|b|≤60°（銀河面を除いた高銀緯領域、Totaniと同じROI定義）。"
    "観測データを ①点源(4FGL-DR4カタログでマスク) ②GALPROP銀河拡散放射 "
    "③等方背景放射(高銀緯平均で固定) ④Loop I(北極スパー、2つの独立球殻モデル) "
    "⑤フェルミバブル(正負2テンプレート) ⑥NFWダークマターハロー、の重ね合わせで"
    "モデル化する。図はGALPROPがまだ単一テンプレートだった段階の可視化だが、"
    "後述の通りGALPROPは現在gas成分・ICS成分の2つに分離しており、実質7自由"
    "パラメータで同時フィットしている。最終的に残る超過がハロー起源だと"
    "主張するロジックをここで説明する。"
))

# ============================================================
# Slide 5 — Method: MCMC + gas/ICS separation
# ============================================================
s = add_slide(); set_bg(s)
add_title(s, "手法：MCMC同時フィットと GALPROP gas/ICS 分離", size=25)
add_bullets(s, [
    "各成分の規格化係数 f_n（n=gas, ICS, LoopI×2, バブル正負, ハロー）を"
    "物理モデル形状に掛けてPoisson尤度で同時フィット（emcee, 32 walkers）",
    "f_halo が NFW-ρ² ハロー形状と実データの一致度（規格化係数）を表す",
    "【今回の主要更新】教授提供の正しいgaldef(SLZ6R30T150C2)によるGALPROP "
    "webrun出力を用い、gas成分(π⁰崩壊+制動放射)とICS成分(逆コンプトン)を"
    "Totani (2025) 通り独立2テンプレート化（従来は単一テンプレートで代用していた）",
    "実測露出マップ（平均5.80e11 cm²·s）で物理単位に変換、全13エネルギービンに拡張",
], size=18)
set_notes(s, (
    "f_nの意味を「モデル形状は固定、大きさだけ実データに合わせて何倍するか」という"
    "スケーリング係数として説明する。f_halo=0なら『ハロー無し』、f_halo>0なら"
    "『その分だけNFW形状の超過がある』と読む。今回の中心的な技術更新はGALPROPの"
    "gas/ICS分離: 教授から2026-07-15に正しいgaldef実行結果を受領し、これまで"
    "1つのテンプレートで近似していたGALPROP銀河拡散放射を、Totaniの手法通り"
    "gas成分とICS成分の2つの独立テンプレートに分離した。これにより7自由パラメータの"
    "モデルになった。"
))

# ============================================================
# Slide 6 — Method: dwarf/M31 extension
# ============================================================
s = add_slide(); set_bg(s)
add_title(s, "手法：矮小銀河5天体・M31への拡張", size=26)
add_bullets(s, [
    "対象: Draco, Sculptor, Ursa Minor, Segue 1, Coma Berenices（矮小銀河）+ M31",
    "銀河ハロー解析とは別の標準的手法（Ackermann+2015等に準拠したON/OFF比較）を採用",
    "ON領域: 天体中心から半径2°　OFF領域: 2°–5°の同心円環（背景の実測見積り）",
    "有意度は Li & Ma (1983) の正式な対数尤度比の式で評価",
    "この手法はGALPROPモデルの選択に依存しない（背景を実測で差し引くため）",
], size=18)
set_notes(s, (
    "矮小銀河・M31は銀河ハローの全天フィットとは異なる、天体ごとのON/OFF解析。"
    "小さい天体を狙うので、天体中心とその周りの環でカウントを比較するだけで"
    "背景がキャンセルされる設計になっており、GALPROPモデルの精密な形状は"
    "使わない（この点は今日改めてコードを読み直して確認した）。Li&Ma(1983)は"
    "Fermi-LAT分野で標準的に使われる有意度の公式。"
))

# ============================================================
# Slide 7 — Result: 13-bin significance spectrum
# ============================================================
s = add_slide(); set_bg(s)
add_title(s, "結果：全13ビンでのハロー有意度スペクトル", size=26)
add_image_centered(s, RES / "mcmc_allbins_gasICS_v1/halo_spectrum.png", max_h=Inches(5.8))
set_notes(s, (
    "gas/ICS分離後の7パラメータモデルで全13ビン(1.51–814 GeV)を同時フィットした"
    "最新結果。上段がf_halo(振幅)、下段が有意度。7.28 GeV(Bin4)付近で最大"
    "28.5σに達し、Totaniの報告するピーク(21 GeV, 13–19σ)とはピーク位置も"
    "大きさも異なる。この不一致自体が次のスライドの主題であり、ここでは"
    "『きれいに戸谷さんと同じ形にはならなかった』という事実を正直に提示する。"
))

# ============================================================
# Slide 8 — Result: Totani comparison + A/C robustness
# ============================================================
s = add_slide(); set_bg(s)
add_title(s, "結果：Totani (2025) との比較・領域分割ロバスト性検証", size=23)

table_rows = [
    ["エネルギー", "Totani (2025) headline", "本解析 (gas/ICS分離後, full ROI)"],
    ["~21 GeV(ピーク)", "13–19σ (NFW-ρ², 論文Fig.9)", "Bin6(20.76GeV): 25.5σ"],
    ["12 / 21 / 35 GeV(参考,GIEM系統誤差)", "6.7 / 7.4 / 5.1σ (baseline不一致のため直接比較不可)", "27.9 / 25.5 / 19.0σ"],
]
add_table(s, table_rows, [Inches(3.6), Inches(4.3), Inches(4.3)],
          top=Inches(1.35), row_h=Inches(0.5), font_size=13.5)

add_caption(s, "⚠ 有意度が戸谷を上回ることは「優れている」ではない：ICS-halo縮退(r=0.71-0.86)による過大評価の疑い",
            top=Inches(3.0), color=RED, size=13.5)

add_image_at(s, RES / "mcmc_allbins_gasICS_v1/regionAC_lrt_summary.png",
             left=Inches(1.6), top=Inches(3.55), max_h=Inches(3.8))

set_notes(s, (
    "戸谷論文は数値表を持たず、Fig.9のグラフと本文の限られた数値のみが公式値。"
    "本解析はピーク近傍で戸谷より高い有意度になっており、これは『我々の方が優れている』"
    "のではなく、ICS成分とハロー成分のテンプレートがほぼ同じ形になる縮退が"
    "疑われる悪いニュースだと明言する。さらに本日、フェルミバブル領域内(A)と"
    "領域外高緯度(C)で独立にハロー強度をフィットし、f_haloを両領域で共有すると"
    "仮定した場合の尤度比検定(LRT)を全13ビンで実行した。4.31〜59.22 GeVの6ビンで"
    "統計的に有意な不一致(A>C、2.7〜5.4σ)を発見。真に球対称なNFWハローなら"
    "領域によらず同じ値になるはずなので、これは「ハロー単体では説明できない何かが"
    "混ざっている」ことの新しい独立証拠。グラフの灰色点(Bin1-2)はテンプレート"
    "共線性による統計的病理と判明したため解釈対象から除外している。"
))

# ============================================================
# Slide 9 — Result: dwarfs + M31
# ============================================================
s = add_slide(); set_bg(s)
add_title(s, "結果：矮小銀河5天体・M31への適用", size=26)
add_image_at(s, FIG / "figure-dwarfs/dwarf_summary_bin6_lima.png",
             left=Inches(0.5), top=Inches(1.2), max_h=Inches(3.6))
add_image_at(s, FIG / "figure-dwarfs/coma_ber/psmask_check_coma_ber.png",
             left=Inches(0.5), top=Inches(5.0), max_h=Inches(2.35))
set_notes(s, (
    "矮小銀河5天体のBin6(20.76GeV)有意度: Draco=-1.33σ, Sculptor=1.27σ, "
    "Ursa Minor=1.61σ, Segue1=-0.38σ, Coma Ber=4.04σ(未マスク)。Coma Berenicesのみ"
    "一見有意に見えるが、ON領域内に4FGL点源が3個混入しているためで、点源マスク後は"
    "-0.93σに反転する（下図右パネルの青棒）。5天体・M31いずれも有意な検出には"
    "至っていない。矮小銀河はダークマター密度が銀河ハローより低いと理論的に"
    "予想されるため、非検出という結果自体が理論と矛盾しない一貫性チェックに"
    "なっている点を述べる。"
))

# ============================================================
# Slide 10 — Discussion
# ============================================================
s = add_slide(); set_bg(s)
add_title(s, "Discussion：見つかった2つの未解決の縮退", size=25)
add_image_at(s, RES / "mcmc_allbins_gasICS_v1/ics_sed_comparison.png",
             left=Inches(3.3), top=Inches(1.3), max_h=Inches(4.35))
add_bullets(s, [
    "① ICS-halo縮退（悪性）: ハロー成分を含めるとICSスペクトルが物理的に"
    "ありえないV字形状に変形（右図）。Totani §4.1の自然性基準に不合格",
    "② バブル内外の空間非一様性: A(バブル内)がC(バブル外)より系統的に大きい"
    "（6ビンで統計的に有意）。真に球対称なハローなら起きないはずの挙動",
    "UCL独立追試(Stenhouse+2026, arXiv:2607.08552)でもGALPROP選択が"
    "「最大の系統誤差」と報告 → 分野共通の課題だが、我々のICS縮退は"
    "彼らの報告(±10%)より深刻（2-7倍抑圧）で要因が未解明",
], left=Inches(0.5), top=Inches(1.3), width=Inches(2.6), size=13.5)
set_notes(s, (
    "今回の最大の成果は『きれいな検出』ではなく『どこに縮退が残っているかを"
    "定量的に特定したこと』だと位置づける。①GALPROPのgas/ICS分離を正しい"
    "webrunデータで実装した結果、ハローを入れるとICS成分のスペクトルが"
    "物理的にありえない形になることが分かった(V字、右図の実線)。②同時に"
    "フェルミバブル領域の内外で独立にハロー強度をフィットすると値が2-5倍"
    "違うという新しい頑健性検証結果も出た。これら2つは独立に見つかった別々の"
    "問題で、どちらも『20 GeV超過がハロー単体で説明できる』という主張を"
    "弱める。UCL大学の独立追試論文でも同種の系統誤差(GALPROP vs GIEM)が"
    "『最大の系統誤差』と報告されており、この分野全体が抱える構造的な課題だと"
    "位置づけられる一方、我々のICS縮退は彼らの報告より深刻で、その理由は"
    "まだ分かっていないと正直に述べる。"
))

# ============================================================
# Slide 11 — Conclusion + Future direction
# ============================================================
s = add_slide(); set_bg(s)
add_title(s, "Conclusion と今後の方針", size=28)
add_bullets(s, [
    "Conclusion: Totani (2025) の手法（GALPROP gas/ICS分離含む）を忠実に実装し"
    "実装自体は複数のレビューで合格。しかし戸谷と同じ『きれいな検出』には至らず、"
    "ICS-halo縮退とバブル内外の空間非一様性という2つの具体的な原因を特定した",
    "矮小銀河5天体・M31は理論予想と整合する非検出、こちらは頑健な結果",
    "今後の方針①: injection-null test（UCL論文の手法を借用）でGALPROP"
    "モデリング誤差だけからどれだけ偽のハロー信号が作られうるか定量化",
    "今後の方針②: 南北半球分割による相補的ロバスト性検証",
    "今後の方針③: なぜ我々のICS縮退がUCL論文の報告より深刻か（GALPROP"
    "テンプレートの質か、パイプライン設計の違いか）を切り分ける",
], size=16.5)
set_notes(s, (
    "研究の到達点を『実装は正しく完成させたが、戸谷と同じ検出結果には"
    "ならなかった。その理由を2つ具体的に特定した』とまとめる。これは"
    "後ろ向きな結果ではなく、20 GeV超過の頑健性という科学的に重要な問いに"
    "対する明確な答えだと位置づける。矮小銀河・M31の非検出は安定した結果として"
    "強調する。今後の方針は、UCL大学の独立追試論文(2607.08552)が使った"
    "injection-null test（真のハローが無い擬似データにわざと歪んだ拡散放射を"
    "仕込み、パイプラインがどれだけ偽のハローを検出するか測る手法）を我々にも"
    "実装することを最優先に据える。合計8分に収まるよう、質疑に時間を残す。"
))

prs.save(str(OUT))
print(f"保存完了: {OUT} ({len(prs.slides)} スライド)")
