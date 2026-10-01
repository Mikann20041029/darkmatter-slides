"""slide66.xml (論文Figureの再現計画トラッカー) の TextBox3 を更新する。

Fig8〜16 の状態 (docs/totani_figure_correspondence.md ベース) を
既存の Fig1-7 リストに追記する。プレースホルダ行
"Fig 8〜: 論文 p.12 以降を精読して追加" を 9 行の Fig8-16 status に置換する。

対象: slides_v3_detailed_18pt.pptx, slides_v3_detailed_fixed2.pptx
"""

import shutil
import zipfile
from pathlib import Path

from lxml import etree

NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}

# color codes (既存の Fig1-7 と同じ凡例に合わせる)
GREEN = "44FF88"   # ✓ 構造アナログ / 再現済
AMBER = "FFCC00"   # △ 部分対応・形状などに相違あり
ORANGE = "FF8800"  # → 要実装
RED = "FF4444"     # ⛔ blocked

NEW_LINES = [
    ("Fig 8: ハロー3プロファイル振幅スペクトル(銀極線形)  △ 構造アナログ(山型→単調減少)", AMBER),
    ("Fig 9: 3モデルΔlnL(=Δχ²/2)スペクトル              ✓ 構造アナログ再現済", GREEN),
    ("Fig 10: 21GeVビン ハロー動径プロファイル            → 要実装(Phase A2)", ORANGE),
    ("Fig 11: NFW-ρ² 2×2マップ(21GeVビン)                ✓ 構造アナログ再現済", GREEN),
    ("Fig 12: ハロー+残差マップ(低E4ビン: 1,2,3,5)        ✓ 構造アナログ再現済", GREEN),
    ("Fig 13: ハロー+残差マップ(高E4ビン: 7,8,9,10)       ✓ 構造アナログ再現済", GREEN),
    ("Fig 14: 21GeVモデルテンプレート(6パネル)            ✓ 再現済", GREEN),
    ("Fig 15: 系統誤差チェック(15種代替解析)              △ 部分対応のみ", AMBER),
    ("Fig 16: DM質量・断面積フィット(4パネル)             ⛔ blocked(exposure map要)", RED),
]


def _qn(prefix: str, tag: str) -> str:
    return f"{{{NS[prefix]}}}{tag}"


def process(pptx_path: Path) -> None:
    with zipfile.ZipFile(pptx_path, "r") as zin:
        names = zin.namelist()
        data = {name: zin.read(name) for name in names}

    slide_xml = data["ppt/slides/slide66.xml"]
    root = etree.fromstring(slide_xml)

    textbox = None
    for sp in root.iter(_qn("p", "sp")):
        nv = sp.find(f".//{_qn('p', 'cNvPr')}")
        if nv is not None and nv.get("name") == "TextBox 3":
            textbox = sp
            break
    assert textbox is not None, f"TextBox 3 not found in {pptx_path}"

    txBody = textbox.find(f".//{_qn('p', 'txBody')}")
    paras = txBody.findall(_qn("a", "p"))

    placeholder = paras[-1]
    run = placeholder.find(_qn("a", "r"))
    rpr = run.find(_qn("a", "rPr"))
    body_sz = rpr.get("sz")  # この pptx の本文行サイズ (fixed2:1400, p18:1800)

    if body_sz == "1800":
        # p18: header/body ともに 1800pt のままでは 17 行が
        # box (cy=5577840) を超えてスライド下端で切れる。
        # fixed2 と同じ header=1600 / body=1400 に揃えて全行収める。
        header = paras[0]
        header_rpr = header.find(_qn("a", "r")).find(_qn("a", "rPr"))
        header_rpr.set("sz", "1600")
        for p in paras[1:]:
            p.find(_qn("a", "r")).find(_qn("a", "rPr")).set("sz", "1400")
        body_sz = "1400"

    template = placeholder

    for text, color in NEW_LINES:
        new_p = etree.fromstring(etree.tostring(template))
        new_run = new_p.find(_qn("a", "r"))
        new_rpr = new_run.find(_qn("a", "rPr"))
        new_rpr.set("sz", body_sz)
        fill = new_rpr.find(f".//{_qn('a', 'srgbClr')}")
        fill.set("val", color)
        t = new_run.find(_qn("a", "t"))
        t.text = text
        txBody.append(new_p)

    txBody.remove(placeholder)

    data["ppt/slides/slide66.xml"] = etree.tostring(
        root, xml_declaration=True, encoding="UTF-8", standalone=True
    )

    tmp_path = pptx_path.with_suffix(".pptx.tmp")
    with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for name in names:
            zout.writestr(name, data[name])
    shutil.move(str(tmp_path), str(pptx_path))
    print(f"updated {pptx_path}: {len(paras) - 1 + len(NEW_LINES)} status lines in TextBox3")


def main() -> None:
    for path in [
        Path("/mnt/c/Users/arsei/Downloads/slides_v3_detailed_18pt.pptx"),
        Path("/mnt/c/Users/arsei/Downloads/slides_v3_detailed_fixed2.pptx"),
    ]:
        process(path)


if __name__ == "__main__":
    main()
