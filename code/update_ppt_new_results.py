"""
新しい解析結果をPPTに追加：
1. MCMC同時フィット結果（スライド23 同時フィット結果を更新）
2. 新アプローチ①②③④ の結果（Discussion後に追加）
3. 主要発見「MWで11σ、M31で非検出」スライド
"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

PPT_PATH = Path("PPT/slides_v3_detailed_fixed2_final.pptx  -  Repaired.pptx")
prs = Presentation(str(PPT_PATH))

W = prs.slide_width; H = prs.slide_height
C_BG    = RGBColor(0x05, 0x05, 0x1A)
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
C_TITLE = RGBColor(0xFF, 0xCC, 0x00)
C_CYAN  = RGBColor(0x00, 0xFF, 0xFF)
C_GREEN = RGBColor(0x44, 0xFF, 0x88)
C_RED   = RGBColor(0xFF, 0x44, 0x00)
C_GRAY  = RGBColor(0xAA, 0xAA, 0xAA)
C_ORANGE= RGBColor(0xFF, 0x88, 0x00)

def blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])

def bg(sl):
    f = sl.background.fill; f.solid(); f.fore_color.rgb = C_BG

def title(sl, text, color=C_TITLE, size=24):
    tb = sl.shapes.add_textbox(Inches(0.15), Inches(0.05), W-Inches(0.3), Inches(0.52))
    tf = tb.text_frame; tf.word_wrap = False
    p = tf.paragraphs[0]; r = p.add_run()
    r.text = text; r.font.size = Pt(size)
    r.font.color.rgb = color; r.font.bold = True

def sep(sl):
    b = sl.shapes.add_shape(1, Inches(0.15), Inches(0.60), W-Inches(0.3), Inches(0.018))
    b.fill.solid(); b.fill.fore_color.rgb = C_CYAN; b.line.fill.background()

def txt(sl, lines, left, top, width, height, size=13, color=C_WHITE, bold=False):
    tb = sl.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame; tf.word_wrap = True
    if isinstance(lines, str): lines = [(lines, color, bold, size)]
    first = True
    for item in lines:
        if isinstance(item, str): item = (item, color, bold, size)
        t, c, b2, s = item
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False; p.space_before = Pt(2)
        r = p.add_run(); r.text = t
        r.font.size = Pt(s); r.font.color.rgb = c; r.font.bold = b2

def img(sl, path, left, top, width=None, height=None):
    p = Path(path)
    if not p.exists(): return False
    if width and height: sl.shapes.add_picture(str(p), left, top, width, height)
    elif width: sl.shapes.add_picture(str(p), left, top, width=width)
    elif height: sl.shapes.add_picture(str(p), left, top, height=height)
    else: sl.shapes.add_picture(str(p), left, top)
    return True


# ─── スライド作成 ─────────────────────────────────────────────────────────────

def make_mcmc_result():
    sl = blank(prs); bg(sl)
    title(sl, "MCMC 同時フィット結果 — Bin6 (20.76 GeV) ★新手法")
    sep(sl)
    txt(sl, [
        ("手法（Totani §2.2-2.3 準拠）", C_CYAN, True, 14),
        ("等方背景を|b|≥50° 平均(2.443 cnt/pix)で固定し、残り5成分を Poisson 最大尤度で同時フィット", C_WHITE, False, 12),
        ("μᵢ = 等方背景 + f_gal×GALPROP + f_loopI×LoopI + f_fb×バブル + f_halo×NFW", C_WHITE, False, 12),
        ("", C_WHITE, False, 6),
        ("フィット結果（MCMC 中央値 ± 1σ）", C_CYAN, True, 14),
        ("f_fb   = 0.978 ± 0.02  → バブル較正が物理的期待値 1.0 に整合 ✓", C_GREEN, False, 13),
        ("f_halo = 16.6  ± 0.14  → NFW ハロー成分が明確に非ゼロ", C_GREEN, True, 13),
        ("f_gal  ≈ 0              → GALPROP は高銀緯で寄与小（物理的に正常）", C_WHITE, False, 12),
        ("", C_WHITE, False, 6),
        ("有意度（ピクセル1°×1°ベース）", C_CYAN, True, 14),
        ("ΔlnL = 5651  →  セルスケール(10°×10°)換算: 約 11σ", C_GREEN, True, 14),
        ("→ Totani (2025) の 14σ と同オーダーで整合", C_WHITE, False, 13),
        ("", C_WHITE, False, 6),
        ("物理単位較正（露出マップ近似）", C_CYAN, True, 14),
        ("GALPROP: ph/cm²/s/sr/MeV × Mrk501 較正値 × ΔΩ × ΔE → counts/pix", C_WHITE, False, 12),
        ("バブル: Bin3カウント × 0.146（スペクトル傾き・ΔE・A_eff比）→ Bin6相当", C_WHITE, False, 12),
        ("NFW: Totani Fig.8 (3×10⁻⁵ MeV/cm²/s/sr at b=90°) から較正", C_WHITE, False, 12),
    ], Inches(0.2), Inches(0.68), Inches(5.5), H-Inches(0.8))
    img(sl, "results/mcmc/corner_bin6.png",
        Inches(5.8), Inches(0.68), width=Inches(3.7))
    return sl


def make_new_approaches():
    sl = blank(prs); bg(sl)
    title(sl, "新アプローチ ①〜④ — 「天の川銀河だけじゃない」検証")
    sep(sl)
    txt(sl, [
        ("動機", C_CYAN, True, 14),
        ("MWハローで信号が出たが、それがDMなら他のDM密集領域でも同じ信号が出るはず。", C_WHITE, False, 13),
        ("→ 4つのアプローチで独立検証を試みた。", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("① 等方背景スペクトル（|b|≥50°）", C_CYAN, True, 13),
        ("DM消滅が宇宙全体で起きるなら、等方背景に20 GeVのバンプが現れるはず", C_WHITE, False, 12),
        ("→ バンプなし。宇宙論的DM寄与は現在の感度では見えない。", C_GRAY, False, 12),
        ("", C_WHITE, False, 6),
        ("② M31（アンドロメダ銀河, 780週）", C_CYAN, True, 13),
        ("天の川と同規模のDMハローを持つ最近傍の大型銀河", C_WHITE, False, 12),
        ("Bin6 S/N = 0.95σ → 非検出", C_RED, True, 13),
        ("", C_WHITE, False, 6),
        ("③ Perseus/Coma 銀河団（780週）", C_CYAN, True, 13),
        ("Perseus: Bin6 S/N = 5.56σ → 中心AGN（NGC 1275）のγ線と判断", C_ORANGE, True, 13),
        ("Coma: データ不足（|b|=88°でOFFリングが空）", C_GRAY, False, 12),
        ("", C_WHITE, False, 6),
        ("④ GC距離プロファイル（相互相関）", C_CYAN, True, 13),
        ("残差マップの銀河中心からの角度依存性を解析", C_WHITE, False, 12),
        ("→ NFWプロファイルと完全一致せず。LoopI差し引きの過補正の可能性。", C_GRAY, False, 12),
    ], Inches(0.2), Inches(0.68), W-Inches(0.4), H-Inches(0.8))
    return sl


def make_m31_result():
    sl = blank(prs); bg(sl)
    title(sl, "② M31（アンドロメダ銀河）S/N スペクトル — Totani の信号は見えるか？")
    sep(sl)
    img(sl, "data/figure-new-approach/m31_cluster_sn_780w.png",
        Inches(0.15), Inches(0.68), width=W-Inches(0.3))
    return sl


def make_key_finding():
    sl = blank(prs); bg(sl)
    title(sl, "★ 主要発見 — MW で 11σ、M31 で非検出", color=C_RED, size=24)
    sep(sl)
    txt(sl, [
        ("結果の比較", C_CYAN, True, 16),
        ("", C_WHITE, False, 6),
    ], Inches(0.2), Inches(0.68), W-Inches(0.4), Inches(0.5))

    # 比較表
    rows = [
        ("天体",                "Bin6 S/N",    "解釈"),
        ("天の川銀河ハロー(MW)",  "≈ 11σ",      "NFW ハロー信号を検出"),
        ("M31（アンドロメダ）",   "0.95σ",      "非検出（統計的に有意でない）"),
        ("矮小銀河 5天体",        "全て ±2σ",  "非検出（全天体）"),
        ("Perseus 銀河団",        "5.56σ",      "AGN（NGC 1275）汚染と判断"),
    ]
    y0 = Inches(1.25)
    colors_row = [C_CYAN, C_GREEN, C_RED, C_GRAY, C_ORANGE]
    for i, (a, b2, c) in enumerate(rows):
        y = y0 + Inches(i*0.48)
        clr = colors_row[i]
        bold = (i==0)
        txt(sl, [(a, clr, bold, 13)], Inches(0.2), y, Inches(3.5), Inches(0.45))
        txt(sl, [(b2, clr, bold, 13)], Inches(3.8), y, Inches(1.8), Inches(0.45))
        txt(sl, [(c, clr, bold, 13)], Inches(5.7), y, Inches(3.8), Inches(0.45))

    txt(sl, [
        ("", C_WHITE, False, 8),
        ("解釈", C_CYAN, True, 16),
        ("もし Totani の20 GeV信号が DM消滅なら、M31（J因子がMW と同程度）でも見えるはず。", C_WHITE, False, 13),
        ("→ M31での非検出は、信号が MW 固有の天体物理現象に由来する可能性を示唆。", C_RED, True, 14),
        ("", C_WHITE, False, 8),
        ("MW固有の天体物理的起源の候補：", C_WHITE, True, 13),
        ("• ICS（逆コンプトン散乱）: 宇宙線電子 × MW 固有の星間放射場 → 20 GeV ピーク", C_WHITE, False, 13),
        ("• GALPROPモデル誤差: MW の銀河拡散放射が20 GeVで過小推定されている可能性", C_WHITE, False, 13),
        ("• フェルミバブルテンプレートの不完全性: バブル境界付近の残差", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("→ 本研究の独自貢献: M31 非検出はTotani (2025) への新しい制約", C_GREEN, True, 14),
    ], Inches(0.2), y0 + Inches(5*0.48) + Inches(0.1), W-Inches(0.4), H-Inches(0.8))
    return sl


# ─── 挿入位置を決定 ─────────────────────────────────────────────────────────
# Discussion (3/3)の後（スライド38のインデックスを探す）
def find_slide(keyword):
    for i, sl in enumerate(prs.slides):
        for sh in sl.shapes:
            if sh.has_text_frame and keyword in sh.text_frame.text:
                return i
    return None

insert_after = find_slide("Discussion (3/3)")
if insert_after is None:
    insert_after = find_slide("矮小銀河解析フロー") - 1
print(f"挿入位置: スライド{insert_after+1}の後")

new_slides = [
    make_mcmc_result(),
    make_new_approaches(),
    make_m31_result(),
    make_key_finding(),
]

# 末尾に追加→挿入位置へ移動
n = len(new_slides)
total = len(prs.slides)
xml_slides = prs.slides._sldIdLst
original = list(xml_slides)
moved = original[total-n:]
for e in moved: xml_slides.remove(e)
for i, e in enumerate(moved):
    xml_slides.insert(insert_after + 1 + i, e)

print(f"スライド数: {len(prs.slides)}")
prs.save(str(PPT_PATH))
print("保存完了")
