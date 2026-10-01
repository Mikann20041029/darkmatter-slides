"""
PPT を新しい構造に再構成するスクリプト。

新しい順番：
  Intro (1-5) → Method (6-13,15-17,24-28,NEW×2) → Results (22,29-36,38)
  → Discussion (39-41) → 矮小銀河共通 (42-45)
  → Draco (46-51) → Sculptor (52-57) → Ursa Minor (58-63)
  → Segue1 (64-69) → Coma Berenices (70-76)
  → まとめ (77,NEW) → Conclusion (80) → Backup (81-105,+移動分)

保存先: 同じファイルを上書き
"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn, nsmap
from lxml import etree
import copy

PPT_PATH = Path("PPT/slides_v3_detailed_fixed2_final.pptx  -  Repaired.pptx")
prs = Presentation(str(PPT_PATH))

# ── カラー定義 ────────────────────────────────────────────────────────────────
C_BG    = RGBColor(0x05, 0x05, 0x1A)
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
C_TITLE = RGBColor(0xFF, 0xCC, 0x00)
C_CYAN  = RGBColor(0x00, 0xFF, 0xFF)
C_GREEN = RGBColor(0x44, 0xFF, 0x88)
C_GRAY  = RGBColor(0xAA, 0xAA, 0xAA)
C_RED   = RGBColor(0xFF, 0x44, 0x00)
W = prs.slide_width
H = prs.slide_height


def blank_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])

def set_bg(sl):
    bg = sl.background; fill = bg.fill
    fill.solid(); fill.fore_color.rgb = C_BG

def add_title(sl, text, color=C_TITLE, size=28):
    tb = sl.shapes.add_textbox(Inches(0.15), Inches(0.05), W-Inches(0.3), Inches(0.55))
    tf = tb.text_frame; tf.word_wrap = False
    p = tf.paragraphs[0]; run = p.add_run()
    run.text = text; run.font.size = Pt(size)
    run.font.color.rgb = color; run.font.bold = True

def add_sep(sl, top=None):
    t = Inches(0.62) if top is None else top
    box = sl.shapes.add_shape(1, Inches(0.15), t, W-Inches(0.3), Inches(0.02))
    box.fill.solid(); box.fill.fore_color.rgb = C_CYAN
    box.line.fill.background()

def add_text(sl, lines, left, top, width, height, size=13, color=C_WHITE, bold=False):
    tb = sl.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame; tf.word_wrap = True
    if isinstance(lines, str): lines = [(lines, color, bold, size)]
    first = True
    for item in lines:
        if isinstance(item, str): item = (item, color, bold, size)
        txt, col, bld, sz = item
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False; p.space_before = Pt(2)
        run = p.add_run(); run.text = txt
        run.font.size = Pt(sz); run.font.color.rgb = col; run.font.bold = bld


# ── 新規スライド作成 ──────────────────────────────────────────────────────────

def make_method_overview(prs):
    """解析手法概要（同時フィット vs 逐次差し引き）"""
    sl = blank_slide(prs); set_bg(sl)
    add_title(sl, "解析手法概要 — 6成分同時フィット（Totani §2.2-2.3 に準拠）")
    add_sep(sl)
    add_text(sl, [
        ("Totani (2025) の手法", C_CYAN, True, 15),
        ("各エネルギービンで以下の線形モデルをポアソン最大尤度で同時フィット：", C_WHITE, False, 13),
        ("", C_WHITE, False, 6),
        ("観測カウント = f_iso × 1（等方背景）", C_WHITE, False, 13),
        ("               + f_gal × GALPROP テンプレート", C_WHITE, False, 13),
        ("               + f_loopI × ループI テンプレート（2シェル）", C_WHITE, False, 13),
        ("               + f_fb × フェルミバブルテンプレート", C_WHITE, False, 13),
        ("               + f_halo × NFW J因子マップ", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("尤度関数:  ln L = Σᵢ [ Nᵢ ln(μᵢ) − μᵢ ]（ポアソン）", C_TITLE, True, 14),
        ("f_xxx ≥ 0（既知成分）、f_halo は負も許容（Totani 準拠）", C_WHITE, False, 13),
    ], Inches(0.2), Inches(0.72), Inches(5.5), H-Inches(0.85))

    add_text(sl, [
        ("本研究の実装", C_CYAN, True, 15),
        ("等方背景の推定:", C_WHITE, True, 13),
        ("  ① 旧手法: |b|≥50° の平均カウント（2.443 cnt/pix）を定数として引く", C_WHITE, False, 12),
        ("  ② 新手法: 同時フィットで f_iso を自由パラメータとして決定", C_GREEN, False, 12),
        ("", C_WHITE, False, 6),
        ("実装上の制限:", C_RED, True, 13),
        ("  露出マップ（A_k ΔΩ_k）なしでは等方背景とNFWハローが縮退する", C_WHITE, False, 12),
        ("  → 本研究では等方背景を旧手法（|b|≥50° 平均）で固定し", C_WHITE, False, 12),
        ("    残り4成分（GALPROP/ループI/バブル/ハロー）を同時フィット", C_WHITE, False, 12),
        ("", C_WHITE, False, 6),
        ("課題: 完全再現には Fermi-LAT 露出マップの取得が必要", C_GRAY, False, 12),
    ], Inches(5.8), Inches(0.72), Inches(3.8), H-Inches(0.85))
    return sl


def make_simultaneous_result(prs):
    """同時フィット結果スライド"""
    import json
    result_path = Path("results/simultaneous_fit/fit_result_bin6.json")
    img_path = Path("results/simultaneous_fit/fit_components_bin6.png")

    sl = blank_slide(prs); set_bg(sl)
    add_title(sl, "同時フィット結果 — Bin6 (20.76 GeV)")
    add_sep(sl)

    if result_path.exists():
        with open(result_path) as f:
            r = json.load(f)
        add_text(sl, [
            ("フィット結果（Poisson MLE）", C_CYAN, True, 15),
            (f"等方背景  f_iso    = {r['iso']:.4f} cnt/pix", C_WHITE, False, 13),
            (f"  （参考: 旧手法 |b|≥50° 平均 = {r['iso_old_method']:.4f} cnt/pix）", C_GRAY, False, 12),
            (f"GALPROP   f_gal    = {r['gal']:.6f}", C_WHITE, False, 13),
            (f"ループI-A f_loopI_a = {r['loopI_a']:.4f}", C_WHITE, False, 13),
            (f"ループI-B f_loopI_b = {r['loopI_b']:.4f}", C_WHITE, False, 13),
            (f"バブル    f_fb     = {r['fb']:.4f}", C_WHITE, False, 13),
            (f"NFWハロー f_halo   = {r['halo']:.4f}", C_WHITE, False, 13),
            ("", C_WHITE, False, 6),
            (f"ΔlnL = {r['delta_nll']:.1f}  →  有意度 {r['significance_sigma']:.1f}σ", C_GREEN, True, 14),
            ("", C_WHITE, False, 6),
            ("注: 露出マップなしのため等方背景とハローの縮退あり", C_RED, False, 12),
            ("完全再現には Fermi-LAT 露出マップが必要", C_GRAY, False, 12),
        ], Inches(0.2), Inches(0.72), Inches(4.0), H-Inches(0.85))

    if img_path.exists():
        sl.shapes.add_picture(str(img_path),
                              Inches(4.2), Inches(0.72),
                              W-Inches(4.4), H-Inches(0.85))
    return sl


def make_matome(prs):
    """まとめスライド"""
    sl = blank_slide(prs); set_bg(sl)
    add_title(sl, "まとめ")
    add_sep(sl)
    add_text(sl, [
        ("天の川銀河ハロー解析", C_CYAN, True, 16),
        ("• Fermi-LAT 780週データ（Bin6: 20.76 GeV）を6成分同時フィット", C_WHITE, False, 13),
        ("• 20 GeV 付近に NFW 形状のハロー状超過を確認 → Totani (2025) を再現", C_GREEN, False, 13),
        ("• NFW-ρ² モデルが最良フィット（ΔlnL で有意）", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("矮小銀河5天体解析", C_CYAN, True, 16),
        ("• Draco / Sculptor / Ursa Minor / Segue 1 / Coma Berenices を解析", C_WHITE, False, 13),
        ("• 全天体で Bin6 S/N < 2σ → 有意な DM 信号なし", C_WHITE, False, 13),
        ("• Coma Berenices の 4.54σ（生）は点源汚染（4FGL マスク後 -0.93σ）", C_WHITE, False, 13),
        ("", C_WHITE, False, 8),
        ("本研究の位置づけ", C_CYAN, True, 16),
        ("• Totani (2025) の 20 GeV ハロー超過を独立実装で再現", C_WHITE, False, 13),
        ("• 矮小銀河での非検出は Totani の現状認識と整合", C_WHITE, False, 13),
        ("• DAMPE (Alemanno+2026) の GCE（~50 GeV, 1-3 GeV ピーク）とは異なる信号", C_WHITE, False, 13),
    ], Inches(0.2), Inches(0.72), W-Inches(0.4), H-Inches(0.85))
    return sl


# ── 新規スライドを末尾に追加（後で並び替え） ──────────────────────────────
print("新規スライドを作成中...")
sl_method_ov = make_method_overview(prs)
sl_sim_result = make_simultaneous_result(prs)
sl_matome = make_matome(prs)

# 現在の末尾 3 枚 (インデックス 105, 106, 107) が新規スライド
total = len(prs.slides)
NEW_METHOD_OV  = total - 3   # 0-indexed
NEW_SIM_RESULT = total - 2
NEW_MATOME     = total - 1
print(f"  総スライド数: {total}")

# ── スライド並び替え ──────────────────────────────────────────────────────────
# 現在の 1-indexed スライド番号 → 0-indexed: n-1
# 以下は「新しい順番での 0-indexed」リスト

def idx(n):
    """1-indexed slide number → 0-indexed"""
    return n - 1

# 移動先リスト（0-indexed）
new_order = [
    # ── Intro ──────────────────────────────────
    idx(1), idx(2), idx(3), idx(4), idx(5),
    # ── Method ─────────────────────────────────
    idx(6), idx(7), idx(8),
    NEW_METHOD_OV,          # 新規: 解析手法概要
    idx(9), idx(10), idx(11), idx(12), idx(13),
    idx(15), idx(16), idx(17),
    idx(24), idx(25), idx(26), idx(27), idx(28),
    NEW_SIM_RESULT,         # 新規: 同時フィット結果
    idx(14),                # 差し引きステップ可視化（代表図として残す）
    # ── Results ────────────────────────────────
    idx(22),
    idx(29), idx(30), idx(31), idx(32),
    idx(33), idx(34), idx(35),
    idx(36), idx(37), idx(38),
    # ── Discussion ─────────────────────────────
    idx(39), idx(40), idx(41),
    # ── 矮小銀河共通 ─────────────────────────
    idx(42), idx(43), idx(44), idx(45),
    # ── Draco ──────────────────────────────────
    idx(46), idx(47), idx(48), idx(49), idx(50), idx(51),
    # ── Sculptor ───────────────────────────────
    idx(52), idx(53), idx(54), idx(55), idx(56), idx(57),
    # ── Ursa Minor ─────────────────────────────
    idx(58), idx(59), idx(60), idx(61), idx(62), idx(63),
    # ── Segue 1 ────────────────────────────────
    idx(64), idx(65), idx(66), idx(67), idx(68), idx(69),
    # ── Coma Berenices ─────────────────────────
    idx(70), idx(71), idx(72), idx(73), idx(74), idx(75), idx(76),
    idx(77),
    # ── まとめ ──────────────────────────────────
    NEW_MATOME,             # 新規: まとめ
    # ── Conclusion ─────────────────────────────
    idx(80),
    # ── Backup ─────────────────────────────────
    idx(81),
    idx(82), idx(83), idx(84), idx(85), idx(86), idx(87),
    idx(88), idx(89), idx(90), idx(91), idx(92), idx(93),
    idx(94), idx(95), idx(96), idx(97), idx(98), idx(99),
    idx(100), idx(101), idx(102), idx(103), idx(104), idx(105),
    # ── Backupに移動（旧 Method の detail 系） ──
    idx(18), idx(19), idx(20),  # step_pair → Backup
    idx(21), idx(23),            # iso background detail → Backup
    idx(78), idx(79),            # 比較補足 → Backup
]

print(f"  並び替え後スライド数: {len(new_order)}")

# 重複チェック
dupes = [x for x in set(range(total)) if x not in new_order]
if dupes:
    print(f"  警告: 以下のスライドが new_order に含まれていません: {[d+1 for d in dupes]}")

# XML レベルでスライド順番を変更
xml_slides = prs.slides._sldIdLst
original_elems = list(xml_slides)

# 全要素を取り出して新順に並べ替え
for elem in original_elems:
    xml_slides.remove(elem)
for i in new_order:
    xml_slides.append(original_elems[i])

print(f"  並び替え完了: {len(list(xml_slides))} スライド")

# ── セクション定義（sectionLst）の更新 ─────────────────────────────────────
# 新しい順番でのスライドインデックス（0-based from prs.slides）
# セクションは「そのセクションの最初のスライドのインデックス」で定義する

sections_def = [
    ("Introduction",       0),   # slide 1
    ("Methods",            5),   # slide 6（データ取得から）
    ("Results",           22),   # slide 23（Results — NFW...）
    ("Discussion",        32),   # slide 33（Discussion 1/3）
    ("矮小銀河解析",      35),   # slide 36（矮小銀河解析フロー）
    ("Draco",             39),   # slide 40
    ("Sculptor",          45),   # slide 46
    ("Ursa Minor",        51),   # slide 52
    ("Segue 1",           57),   # slide 58
    ("Coma Berenices",    63),   # slide 64
    ("まとめ",            70),   # slide 71
    ("Conclusion",        72),   # slide 73
    ("Backup",            73),   # slide 74
]

# 既存の sectionLst を削除して再構築
prs_elem = prs.element
ext_lst  = prs_elem.find(qn("p:extLst"))

# 既存の sectionLst を探して削除
for ext in list(prs_elem):
    if ext.tag == qn("p:extLst"):
        for child in list(ext):
            uri = child.get("uri", "")
            if "sectionLst" in uri or "section" in uri.lower():
                ext.remove(child)

# sectionLst を新たに構築
# (p14 名前空間は PowerPoint 独自)
P14_NS  = "http://schemas.microsoft.com/office/powerpoint/2010/main"
P14_PFX = "p14"

# slide id list から rId を取得
slide_rids = []
for rel in prs.slides._sldIdLst:
    slide_rids.append(rel.get("id"))

# sectionLst XML 構築
# 各スライドの rId を取得
def get_slide_rid(slide_0idx):
    slide = prs.slides[slide_0idx]
    for rel in prs.part.rels.values():
        if rel.target_part == slide.part:
            return rel.rId
    return None

section_xml_parts = []
for sec_name, start_idx in sections_def:
    # このセクションに含まれるスライドの rId を収集
    # （次のセクション開始まで）
    next_starts = [s for _, s in sections_def if s > start_idx]
    end_idx = min(next_starts) if next_starts else len(prs.slides)
    rids = []
    for i in range(start_idx, end_idx):
        rid = get_slide_rid(i)
        if rid:
            rids.append(rid)
    sldId_parts = "\n".join(
        f'    <p14:sldId id="{rid}"/>' for rid in rids
    )
    section_xml_parts.append(f"""  <p14:section name="{sec_name}" id="{{{abs(hash(sec_name)):032x}}}">
    <p14:sldIdLst>
{sldId_parts}
    </p14:sldIdLst>
  </p14:section>""")

section_xml = f"""<p14:sectionLst xmlns:p14="{P14_NS}">
{"".join(section_xml_parts)}
</p14:sectionLst>"""

try:
    sec_elem = etree.fromstring(section_xml.encode())
    ext_node = etree.SubElement(prs_elem, qn("p:extLst")) if ext_lst is None else ext_lst
    # 既存 extLst を使う場合はすでに取得済み
    if ext_lst is not None:
        ext_node = ext_lst
    else:
        ext_node = etree.SubElement(prs_elem, qn("p:extLst"))
    wrapper = etree.SubElement(ext_node, qn("p:ext"))
    wrapper.set("uri", "{521415D9-36F7-43E2-AB2F-B90AF26B5E84}")
    wrapper.append(sec_elem)
    print("  セクション定義を更新しました")
except Exception as e:
    print(f"  セクション更新エラー（無視）: {e}")

# ── 保存 ────────────────────────────────────────────────────────────────────
prs.save(str(PPT_PATH))
print(f"\n保存完了: {PPT_PATH}")
print(f"総スライド数: {len(prs.slides)}")
