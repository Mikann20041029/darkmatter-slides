"""slide35.xml / slide36.xml の Coma Berenices +4.54σ/-0.93σ 不整合を修正する。

commit 069c8b2 で確定した「ON領域内4FGL点源3個の混入による偽陽性
(4.54σ(生) -> 点源マスク後 -0.93σ)」を、これまでノートのみに記載され
本文(スライド表示)には反映されていなかった2スライドに反映する。

- slide35.xml (「矮小銀河詳細：Coma Berenices」): タイトル/計算ボックス末尾/結論ボックスを修正
- slide36.xml (5天体比較表 + 結論): タイトル/Coma Berenices行(有意性・理由)/結論を修正

対象: slides_v3_detailed_18pt.pptx, slides_v3_detailed_fixed2.pptx
(両ファイルで slide35.xml/slide36.xml はテキスト内容が同一、フォントサイズ指定のみ異なる)
"""

import shutil
import zipfile
from pathlib import Path

from lxml import etree

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}

# (slide xml filename, old text, new text)
REPLACEMENTS = [
    (
        "ppt/slides/slide35.xml",
        "矮小銀河詳細：Coma Berenices — 4.54σ 過剰の根拠",
        "矮小銀河詳細：Coma Berenices — 4.54σ過剰の正体（点源汚染-0.93σ）",
    ),
    (
        "ppt/slides/slide35.xml",
        "= 33.7 / 7.42 = 4.54σ",
        "= 33.7 / 7.42 = 4.54σ（生）",
    ),
    (
        "ppt/slides/slide35.xml",
        "★ なぜComa Berenicesだけ見えたか：\n"
        "   距離44kpc（近い）× M/L~1000（DM量多い）× 露出良好 → 光子80個確保できた",
        "★ 4.54σ(生)の正体：ON領域に4FGL点源3個が混入（α_eff=0.167）→ 点源汚染\n"
        "   点源マスク後 S/N = -0.93σ → DM対消滅信号ではない（non-detection、Ackermann 2015と整合）",
    ),
    (
        "ppt/slides/slide36.xml",
        "矮小銀河：なぜ他の4天体では見えないか",
        "矮小銀河5天体：いずれも有意なDM検出なし（Coma Ber. 4.54σ=点源汚染）",
    ),
    (
        "ppt/slides/slide36.xml",
        "★+4.54σ",
        "-0.93σ",
    ),
    (
        "ppt/slides/slide36.xml",
        "ON=80個でBG=46.3を33.7個超過。\n距離・DM量・露出の条件が最良。",
        "+4.54σ(生)→点源3個混入\nマスク後-0.93σ(偽陽性)",
    ),
    (
        "ppt/slides/slide36.xml",
        "→ 天の川（42σ）+ Coma Berenices（4.54σ）= 全く異なる環境での20 GeV過剰の一致\n"
        "   フェルミバブルもループIも存在しない場所での信号 → 「引き残し」と言えない",
        "→ Coma Berenicesの+4.54σ(生)はON域4FGL点源3個の混入による偽陽性\n"
        "   マスク後 S/N=-0.93σ。矮小銀河5天体すべて非検出（Ackermann 2015と整合）",
    ),
]


def process(pptx_path: Path) -> None:
    with zipfile.ZipFile(pptx_path, "r") as zin:
        names = zin.namelist()
        data = {name: zin.read(name) for name in names}

    roots: dict[str, etree._Element] = {}
    applied = 0
    for slide_name, old, new in REPLACEMENTS:
        if slide_name not in roots:
            roots[slide_name] = etree.fromstring(data[slide_name])
        root = roots[slide_name]
        found = False
        for t in root.iter(f"{{{NS['a']}}}t"):
            if t.text is not None and old in t.text:
                t.text = t.text.replace(old, new, 1)
                found = True
                applied += 1
                break
        assert found, f"old text not found in {slide_name}: {old!r}"

    for slide_name, root in roots.items():
        data[slide_name] = etree.tostring(
            root, xml_declaration=True, encoding="UTF-8", standalone=True
        )

    tmp_path = pptx_path.with_suffix(".pptx.tmp")
    with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for name in names:
            zout.writestr(name, data[name])
    shutil.move(str(tmp_path), str(pptx_path))
    print(f"updated {pptx_path}: {applied} text replacements applied")


def main() -> None:
    for path in [
        Path("/mnt/c/Users/arsei/Downloads/slides_v3_detailed_18pt.pptx"),
        Path("/mnt/c/Users/arsei/Downloads/slides_v3_detailed_fixed2.pptx"),
    ]:
        process(path)


if __name__ == "__main__":
    main()
