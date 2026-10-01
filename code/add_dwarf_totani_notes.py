"""矮小銀河5天体ブロックの結論スライドに、Totani(2025)との対応関係を
スピーカーノートとして追記する (Phase B)。

Totani Fig1-16はすべてMW halo ROI向けで、矮小銀河に対応するFigureは
存在しない（`docs/totani_figure_correspondence.md`「矮小銀河5天体 —
Totani Figure対応調査（Phase B）」参照）。対応関係は本文§4.3.2/§4.3.4の
みであるため、新規Figureではなくスピーカーノート追記で対応する。

追記対象（prs.slides[idx]、idx=position-1。sldIdLst+rels で検証済み）:
- prs.slides[52] (pos53 = slide36.xml,「矮小銀河5天体：いずれも有意な
  DM検出なし」): §4.3.2/§4.3.4 との対応関係の詳細版。
- prs.slides[53] (pos54 = slide35.xml,「矮小銀河詳細：Coma Berenices —
  4.54σ過剰の正体」): 上記の要約版（詳細はslide36ノート参照、と誘導）。

既存ノートへの追記のみ（上書きしない）。80スライド/15セクション構造を
維持することを `check_structure()` で確認する。
"""

import shutil
import zipfile
from pathlib import Path

from pptx import Presentation

NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS_P14 = "{http://schemas.microsoft.com/office/powerpoint/2010/main}"

NOTE_SLIDE36 = """

【Totani(2025)との関係（§4.3.2, §4.3.4）】
Totani Fig1-16は全てMW halo ROI向けで、矮小銀河に対応するFigureは存在しない。
§4.3.2(p.23-24): MW halo超過の<σv>~6e-25 cm3/s (mχ~500GeV, bb-barチャンネル)はdSph上限
（[12-15]、[15]の95%containment域の数倍）より大きいが、MW halo密度プロファイル
の不確かさを理由にDM解釈は排除されないとTotaniは結論。
§4.3.4(p.25-26): 「複数dSphで~2-3σのinteresting excessが既に観測されており
（最大はReticulum II [15,77-80]）、感度向上でDM検出が期待される」と将来展望。
本研究の5天体非検出（マスク後|S/N|<2σ）はこの現状認識と整合する。
Coma Berenicesの生4.54σはReticulum II型（~2-3σ）excessと同規模のシグナルが
点源混入の偽陽性だった具体例 → dSph excess解釈には系統誤差検証が必須、という
教訓を与える。"""

NOTE_SLIDE35 = """

【Totani(2025)との関係】
Comaに対応するTotani Figureは存在しない（Fig1-16は全てMW halo ROI）。
Totani §4.3.4(p.26)はReticulum IIの~2-3σ「interesting excess」に言及し、
複数dSphでの将来的なDM検出を展望している。本スライドの結果（生+4.54σ→
マスク後-0.93σ）は、その規模のexcessが点源混入で説明可能な例を示す
（詳細・引用箇所はまとめスライドのノート参照）。"""


def check_structure(pptx_path: Path) -> None:
    from lxml import etree

    with zipfile.ZipFile(pptx_path, "r") as z:
        pres = etree.fromstring(z.read("ppt/presentation.xml"))
    sldIdLst = pres.find(f"{{{NS_P}}}sldIdLst")
    n_slides = len(sldIdLst)
    sections = pres.findall(f".//{NS_P14}section")
    n_sections = len(sections)
    print(f"  {pptx_path.name}: slides={n_slides}, sections={n_sections}")
    assert n_slides == 80, f"expected 80 slides, got {n_slides}"
    assert n_sections == 15, f"expected 15 sections, got {n_sections}"


def append_notes(pptx_path: Path) -> None:
    prs = Presentation(str(pptx_path))

    slide36 = prs.slides[52]
    slide35 = prs.slides[53]

    tf36 = slide36.notes_slide.notes_text_frame
    tf35 = slide35.notes_slide.notes_text_frame

    assert "Coma Berenicesだけに信号が見えた理由" in tf36.text
    assert "本研究の主要結果の一つ" in tf35.text
    assert "Totani" not in tf36.text
    assert "Totani" not in tf35.text

    tf36.text = tf36.text + NOTE_SLIDE36
    tf35.text = tf35.text + NOTE_SLIDE35

    prs.save(str(pptx_path))


def main() -> None:
    targets = [
        Path("/mnt/c/Users/arsei/Downloads/slides_v3_detailed_18pt.pptx"),
        Path("/mnt/c/Users/arsei/Downloads/slides_v3_detailed_fixed2.pptx"),
    ]
    for path in targets:
        append_notes(path)
        check_structure(path)


if __name__ == "__main__":
    main()
