"""Coma Berenices +4.54σ/-0.93σ 不整合修正 (Phase 2)。

`fix_comaber_consistency.py` (slide35/slide36) で確立した
「ON領域内4FGL点源3個の混入による偽陽性 (4.54σ(生) -> 点源マスク後 -0.93σ
-> 矮小銀河5天体すべて non-detection)」という記述を、未対応だった以下の
スライドへ展開する。

- slide34.xml (「Discussion (3/3) — 矮小銀河5天体への展開」表): ★+4.54σ →
  -0.93σ、判定セル「過剰の兆候」→「なし」、結論ボックス書き換え
- slide45.xml (【BACKUP】矮小銀河5天体への展開結果): 同上の表セル+結論
- slide5.xml (Introduction (3/3) 解析フロー結果欄): 「4.54σ の兆候」→
  「4.54σ(生)→点源汚染、-0.93σ（非検出）」
- slide37.xml (【BACKUP】Coma Berenices ON/OFF タイトル): 「+4.54σ」→
  「+4.54σ(生)」
- slide40.xml (Conclusion): 「→ Coma Berenices 4.54σ」→
  「→ 矮小銀河5天体は全て非検出（Coma Ber.の4.54σ(生)は点源汚染、
  マスク後-0.93σ）」
- slide46.xml (【BACKUP】統計的有意性 σ とは): Coma Berenices Bin6 行に
  (生)/マスク後-0.93σ（非検出）を追記
- slide64.xml (矮小銀河詳細 — Coma Berenices): 「4.54σ検出（Bin 6）←
  本研究の主要結果」(既存の「+4.54σ(生)/-0.93(マスク後)σ」行と矛盾) を
  「4.54σ(生)は点源汚染→マスク後-0.93σ（非検出）」に書き換え

加えて、slides_v3_detailed_18pt.pptx (p18) のみに存在する別件の破損
(slide5.xml TextBox16「目的」主文が "X" 1文字に欠落している) を
slides_v3_detailed_fixed2.pptx の同テキストボックス内容で復元する。

対象: slides_v3_detailed_18pt.pptx, slides_v3_detailed_fixed2.pptx
全置換は /tmp/pptx_verify_comaber/ 配下のスローアウェイコピーで
render-verify済み (pos5, pos40, pos51, pos52, pos57, pos62, pos63 を
soffice --headless --convert-to pdf + pdftoppm でレンダリングし、
新規の文字切れ・重なりが無いことを確認)。
"""

import shutil
import zipfile
from pathlib import Path

from lxml import etree

NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"

# (slide xml filename, old text, new text, match_type)
# match_type: "substring" (最初に old を含む <a:t> 内で1回置換)
#              "exact"     (最初に text == old と完全一致する <a:t> を置換)
REPLACEMENTS: list[tuple[str, str, str, str]] = [
    # --- slide34.xml (「Discussion (3/3) — 矮小銀河5天体への展開」表) ---
    (
        "ppt/slides/slide34.xml",
        "★+4.54σ",
        "-0.93σ",
        "substring",
    ),
    (
        "ppt/slides/slide34.xml",
        "過剰の兆候",
        "なし",
        "substring",
    ),
    (
        "ppt/slides/slide34.xml",
        "4.54σ は発見基準（5σ）に届かないが「兆候」（3σ以上）。\n"
        "天の川銀河ハロー（42σ）と合わせて「独立天体での20 GeV過剰」として議論できる。",
        "Coma Ber.の4.54σ(生)は点源3個混入の偽陽性（マスク後-0.93σ）。\n"
        "矮小銀河5天体は全て非検出。天の川ハロー(42σ)の起源は未確認のまま。",
        "substring",
    ),
    # --- slide45.xml (【BACKUP】矮小銀河5天体への展開結果) ---
    (
        "ppt/slides/slide45.xml",
        "★+4.54σ",
        "-0.93σ",
        "substring",
    ),
    (
        "ppt/slides/slide45.xml",
        "過剰の兆候",
        "なし",
        "substring",
    ),
    (
        "ppt/slides/slide45.xml",
        "Coma Berenicesは超淡銀河（M/L比が非常に高い）。4.54σは発見基準（5σ）には届かないが\n"
        "天の川と合わせて「複数天体での20 GeV過剰」として卒論で議論できる価値ある結果。",
        "Coma Berenicesは超淡銀河だが、4.54σ(生)は点源混入の偽陽性。\n"
        "マスク後 S/N = -0.93σ → 矮小銀河5天体すべて非検出。",
        "substring",
    ),
    # --- slide5.xml (Introduction (3/3) 解析フロー結果欄) ---
    (
        "ppt/slides/slide5.xml",
        " Berenices で 4.54σ ",
        " Ber.で4.54σ(生)→点源汚染、",
        "exact",
    ),
    (
        "ppt/slides/slide5.xml",
        "の兆候",
        "-0.93σ（非検出）",
        "exact",
    ),
    # --- slide37.xml (【BACKUP】Coma Berenices ON/OFF タイトル) ---
    (
        "ppt/slides/slide37.xml",
        "(Bin6: +4.54σ)",
        "(Bin6: +4.54σ(生))",
        "substring",
    ),
    # --- slide40.xml (Conclusion) ---
    (
        "ppt/slides/slide40.xml",
        "Coma Berenices 4.54",
        "矮小銀河5天体は全て非検出（Coma Ber.の4.54",
        "exact",
    ),
    (
        "ppt/slides/slide40.xml",
        "σ",
        "σ(生)は点源汚染、マスク後-0.93σ）",
        "exact",
    ),
    # --- slide46.xml (【BACKUP】統計的有意性 σ とは) ---
    (
        "ppt/slides/slide46.xml",
        "Coma Berenices Bin6（20.76 GeV）：4.54σ  → 発見基準には届かないが注目値",
        "Coma Berenices Bin6（20.76 GeV）：4.54σ(生) → 点源汚染後-0.93σ（非検出）",
        "substring",
    ),
    # --- slide64.xml (矮小銀河詳細 — Coma Berenices) ---
    (
        "ppt/slides/slide64.xml",
        "4.54σ 検出（Bin 6）← 本研究の主要結果",
        "4.54σ(生)は点源汚染→マスク後-0.93σ（非検出）",
        "substring",
    ),
]


def apply_text_replacements(data: dict[str, bytes]) -> int:
    roots: dict[str, etree._Element] = {}
    applied = 0
    for slide_name, old, new, match_type in REPLACEMENTS:
        if slide_name not in roots:
            roots[slide_name] = etree.fromstring(data[slide_name])
        root = roots[slide_name]
        found = False
        for t in root.iter(f"{{{NS_A}}}t"):
            if t.text is None:
                continue
            if match_type == "exact":
                if t.text == old:
                    t.text = new
                    found = True
                    applied += 1
                    break
            else:
                if old in t.text:
                    t.text = t.text.replace(old, new, 1)
                    found = True
                    applied += 1
                    break
        assert found, f"old text not found in {slide_name}: {old!r}"

    for slide_name, root in roots.items():
        data[slide_name] = etree.tostring(
            root, xml_declaration=True, encoding="UTF-8", standalone=True
        )
    return applied


def find_textbox16(root: etree._Element) -> etree._Element:
    for sp in root.iter(f"{{{NS_P}}}sp"):
        cNvPr = sp.find(f".//{{{NS_P}}}cNvPr")
        if cNvPr is not None and cNvPr.get("id") == "17" and cNvPr.get("name") == "TextBox 16":
            return sp
    raise AssertionError("TextBox 16 (id=17) not found")


def fix_p18_slide5_textbox16(
    p18_data: dict[str, bytes], fixed2_data: dict[str, bytes]
) -> bool:
    """p18.pptx の slide5.xml TextBox16 ('目的' 主文) が "X" 1文字に欠落
    している破損を、fixed2.pptx の同テキストボックス内容で復元する。
    すでに修復済みなら何もしない (applied=False を返す)。
    """
    fixed2_root = etree.fromstring(fixed2_data["ppt/slides/slide5.xml"])
    fixed2_sp = find_textbox16(fixed2_root)
    fixed2_ext = fixed2_sp.find(f".//{{{NS_A}}}xfrm/{{{NS_A}}}ext")
    fixed2_p = fixed2_sp.find(f".//{{{NS_P}}}txBody/{{{NS_A}}}p")
    assert fixed2_ext is not None and fixed2_p is not None

    p18_root = etree.fromstring(p18_data["ppt/slides/slide5.xml"])
    p18_sp = find_textbox16(p18_root)
    p18_ext = p18_sp.find(f".//{{{NS_A}}}xfrm/{{{NS_A}}}ext")
    p18_txBody = p18_sp.find(f".//{{{NS_P}}}txBody")
    p18_p = p18_txBody.find(f"{{{NS_A}}}p")

    texts = [t.text for t in p18_p.iter(f"{{{NS_A}}}t")]
    if texts != ["X"]:
        return False

    p18_ext.set("cy", fixed2_ext.get("cy"))
    p18_txBody.replace(p18_p, etree.fromstring(etree.tostring(fixed2_p)))

    p18_data["ppt/slides/slide5.xml"] = etree.tostring(
        p18_root, xml_declaration=True, encoding="UTF-8", standalone=True
    )
    return True


def check_structure(pptx_path: Path) -> None:
    NS_P14 = "{http://schemas.microsoft.com/office/powerpoint/2010/main}"
    with zipfile.ZipFile(pptx_path, "r") as z:
        pres = etree.fromstring(z.read("ppt/presentation.xml"))
    sldIdLst = pres.find(f"{{{NS_P}}}sldIdLst")
    n_slides = len(sldIdLst)
    sections = pres.findall(f".//{NS_P14}section")
    n_sections = len(sections)
    print(f"  {pptx_path.name}: slides={n_slides}, sections={n_sections}")
    assert n_slides == 80, f"expected 80 slides, got {n_slides}"
    assert n_sections == 15, f"expected 15 sections, got {n_sections}"


def load(pptx_path: Path) -> tuple[list[str], dict[str, bytes]]:
    with zipfile.ZipFile(pptx_path, "r") as zin:
        names = zin.namelist()
        data = {name: zin.read(name) for name in names}
    return names, data


def save(pptx_path: Path, names: list[str], data: dict[str, bytes]) -> None:
    tmp_path = pptx_path.with_suffix(".pptx.tmp")
    with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for name in names:
            zout.writestr(name, data[name])
    shutil.move(str(tmp_path), str(pptx_path))


def main() -> None:
    p18_path = Path("/mnt/c/Users/arsei/Downloads/slides_v3_detailed_18pt.pptx")
    fixed2_path = Path("/mnt/c/Users/arsei/Downloads/slides_v3_detailed_fixed2.pptx")

    p18_names, p18_data = load(p18_path)
    fixed2_names, fixed2_data = load(fixed2_path)

    n1 = apply_text_replacements(p18_data)
    n2 = apply_text_replacements(fixed2_data)
    print(f"text replacements: p18={n1}, fixed2={n2} (expected {len(REPLACEMENTS)} each)")

    restored = fix_p18_slide5_textbox16(p18_data, fixed2_data)
    print(f"p18 slide5 TextBox16 'X' -> restored: {restored}")

    save(p18_path, p18_names, p18_data)
    save(fixed2_path, fixed2_names, fixed2_data)

    print("structure check:")
    check_structure(p18_path)
    check_structure(fixed2_path)


if __name__ == "__main__":
    main()
