"""Results section に 6 枚の新規再現図スライドを挿入する (Fig8 3-profile / Fig9 / Fig11-13 相当).

対象: slides_v3_detailed_18pt.pptx, slides_v3_detailed_fixed2.pptx
両ファイルで (id, r:id) マッピングが異なるため、各ファイルを独立に処理する。
p14:sectionLst の Results セクション (id 306 の直後) にも同期して挿入する。
"""

from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

from lxml import etree
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = REPO_ROOT / "data" / "figure-all-bins"

NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "p14": "http://schemas.microsoft.com/office/powerpoint/2010/main",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "ct": "http://schemas.openxmlformats.org/package/2006/content-types",
}

ANCHOR_ID = "306"  # slide29.xml = 既存「全13ビンNFW振幅スペクトル(Fig8相当)」, この直後に挿入
IMG_CY = 5029200
IMG_Y = 822960
CONTENT_CENTER_X = 4572000
TITLE_BOX = dict(x=274320, y=91440, cx=8595360, cy=640080)
CAPTION_BOX = dict(x=274320, y=5897880, cx=8595360, cy=685800)

NEW_SLIDES = [
    dict(
        image_file="fig8_3profile_amplitude.png",
        title="【再現図】NFW振幅 3プロファイル比較 — Totani Fig.8拡張",
        caption=[
            "全13ビンでのNFW振幅A（ρ^2.5/ρ²/ρ¹の3パネル）。",
            "低エネルギービン(1.5-7GeV)で振幅最大、21GeV以降ほぼゼロに単調減少（Totaniの山型ピークとは形状が逆）。",
        ],
        notes=[
            "【ページの役割】",
            "再現図。全13ビンでのNFWハロー振幅A（プロファイルρ^2.5/ρ²/ρ¹）のスペクトル。Totani Fig.8の構造的アナログ（3パネル比較）。スライド29（Bin6, ρ²のみ）を全13ビン・3プロファイルに拡張したもの。",
            "",
            "生成スクリプト: code/all_bins_nfw_fit.py（本フェーズで末尾に追加）",
            "出力ファイル: data/figure-all-bins/fig8_3profile_amplitude.png, fig8_3profile_results.txt",
            "",
            "【図の内容】",
            "3パネル（上段ρ^2.5、中段ρ²、下段ρ¹）で、各エネルギービンのOLS振幅A（±1σ）をプロット。",
            "",
            "【重要な定性的相違 ― Totaniとの違い】",
            "Totaniの3パネルはいずれも「1.5GeVでゼロ付近→10-20GeVでピーク→高エネルギーで減衰」の山型（21GeVビンで13-19σの有意ピーク）。",
            "本解析の3パネルは逆に、全プロファイルで低エネルギービン(1.5-7GeV)が最大振幅、21GeV以降はほぼゼロに収束する単調減少 ― 山型ピークは見られない。",
            "",
            "【原因】",
            "本解析の逐次差引き（等方→GALPROP近似→点源マスク→FB→LoopI→NFW）では、低エネルギーで顕著なGALPROP/データの不一致（Totani自身も「1.5GeVで負残差が特に強い」と指摘, p.8）がNFWテンプレートに漏れ込み、低Eで振幅が膨らむ。Totaniの同時MCMCフィットでは他テンプレートが同時調整されるため、この漏れ込みがNFW成分に出にくい。",
            "",
            "【注意】縦軸は count-based arbitrary unit（flux変換にはexposure mapが必要）。プロファイル間で振幅は直接比較不可（各パネル内の形状のみ比較可能）。",
        ],
    ),
    dict(
        image_file="fig8_3profile_significance.png",
        title="【再現図】NFW有意度(S/N) 3プロファイル比較 — Totani Fig.8拡張",
        caption=[
            "全13ビンでのS/N=A/σ_A（3プロファイル比較）。",
            "ρ²のBin6(20.76GeV)でS/N=+0.24σ ― 有意な検出なし。ρ¹は系統誤差未考慮で過大評価。",
        ],
        notes=[
            "【ページの役割】",
            "再現図。前スライド(fig8_3profile_amplitude.png)と対の有意度版。各エネルギービンでのS/N=A/σ_Aを3プロファイルで比較。",
            "",
            "生成スクリプト/出力: 同上（fig8_3profile_amplitude.pngと同一実行で生成）",
            "出力ファイル: data/figure-all-bins/fig8_3profile_significance.png",
            "",
            "【図の内容】",
            "3パネル（ρ^2.5/ρ²/ρ¹）で各ビンのS/Nをプロット。スライド29のBin6 S/N=+0.24σ（ρ²）は本図中段Bin6に対応。",
            "",
            "【重要な数値（fig8_3profile_results.txt より）】",
            "・ρ²（中段, 標準NFW対消滅プロファイル）: 全13ビンで|S/N|<2.4。Bin6=+0.242σ（有意なし）",
            "・ρ^2.5（上段, GCEプロファイル）: Bin5で最大+6.81σ ― 低エネルギー側のGALPROPミスマッチ漏れ込みによる系統的過大評価（前スライドのノート参照）",
            "・ρ¹（下段）: 低エネルギービンで|S/N|>20 ― 統計量の非現実的な過大評価（OLSが系統誤差を1σに含まない）",
            "",
            "【相違点】",
            "Totaniは21GeVビンで13-19σの有意ピーク。本解析は単調減少形状で山型ピークなし（原因は前スライドのノート参照）。",
        ],
    ),
    dict(
        image_file="fig9_dchi2_spectrum.png",
        title="【再現図】Δχ²=(S/N)² スペクトル — Totani Fig.9相当",
        caption=[
            "3モデルのΔχ²=(S/N)²（Gaussian近似下でΔlnL≈Δχ²/2）。",
            "Bin6(20.76GeV)のρ²でΔχ²=0.059 ― no-haloフィットとの差はほぼ無し。",
        ],
        notes=[
            "【ページの役割】",
            "再現図。Totani Fig.9（3モデルのΔlnL=lnL-lnL_no-halo）の構造的アナログ。追加計算ゼロ（fig8_3profile_results.txtのS/Nを2乗するだけ）。",
            "",
            "生成スクリプト: code/all_bins_nfw_fit.py 末尾に追加（本フェーズで実装）",
            "出力ファイル: data/figure-all-bins/fig9_dchi2_spectrum.png, fig9_dchi2_results.txt",
            "",
            "【図の内容】",
            "Δχ² = (A_hat/σ_A)² = (S/N)²。Gaussian近似下でΔlnL≈Δχ²/2。3パネル（ρ^2.5/ρ²/ρ¹）、Bin6を赤強調。",
            "",
            "【重要な数値（fig9_dchi2_results.txt より）】",
            "・ρ²（中段, Bin6=20.76GeV）: Δχ²=0.0587 ― 全13ビン中で最小ではないが「no-haloとの差が無い」点の一つ",
            "・ρ^2.5（上段, Bin6）: Δχ²=52.85（13ビン中最大）",
            "・ρ¹（下段, Bin6）: Δχ²=249.5（13ビン中6番目、中位）",
            "",
            "【Totaniとの対応】",
            "Totaniは「21GeVビンに有意なΔlnLピーク」（太線がチェイン95%境界を大きく超える）。本解析ではBin6が最大または中位のΔχ²を示すプロファイルもあるが、いずれも他ビンと同程度かそれ以下の改善量に留まり、対応するピークではない（前スライドの観察事項と同根）。",
            "",
            "【相違点】",
            "(1) MCMCチェインの95%境界線は再現不可（OLSは点推定のみ）。(2) Δχ²とΔlnLの対応はGaussian近似下でのみ成立し、Poisson統計の厳密な尤度比ではない。",
        ],
    ),
    dict(
        image_file="fig11_equiv_bin6_maps.png",
        title="【再現図】Bin6 残差マップ2×2 — Totani Fig.11相当",
        caption=[
            "Bin6(20.76GeV)の2×2マップ：①no-halo残差 ②ハロー込み残差 ③NFW-ρ²モデル(A_hat*J_2) ④③減算後残差。",
            "③はA_hat=+1.23e-18でほぼ無地（S/N=+0.24） ― ④≈②。",
        ],
        notes=[
            "【ページの役割】",
            "再現図。Totani Fig.11（top-left=no-haloフィット残差、top-right=ハロー込み残差、bottom-left=ハローモデル、bottom-right=減算後残差）の構造的アナログ。",
            "",
            "生成スクリプト: code/plot_totani_fig11_13_equiv.py（本フェーズで新規作成）",
            "出力ファイル: data/figure-all-bins/fig11_equiv_bin6_maps.png, fig11_13_equiv_summary.txt",
            "",
            "【図の内容・実装対応】",
            "①top-left ↔ residual_masked（②と同一。本解析の逐次差引きには成分degeneracyが無いため）",
            "②top-right ↔ residual_masked",
            "③bottom-left ↔ A_hat * J_2map（NFW-ρ²ハローモデル, A_hat=+1.228e-18, S/N=+0.242）",
            "④bottom-right ↔ residual_masked - A_hat*J_2map",
            "①②③④は同一カラースケール（②の98パーセンタイル基準, RdBu_r, ±vlim）",
            "",
            "【観察事項】",
            "③（ハローモデル）は④・①・②に比べ視覚的にほぼ無地（一様にゼロ近傍）。A_hat=+1.228e-18はJ_2~O(10^13-10^14)で振幅換算後も残差マップのスケールに対し無視できる大きさ ― Bin6 S/N=+0.242（ほぼゼロ）の直接的可視化。④≈②となり「ハロー成分を引いても引かなくても残差マップはほぼ変わらない」ことが一目で分かる。",
            "",
            "【相違点】",
            "count-based arbitrary unit（flux単位 cm^-2 s^-1 sr^-1 MeV^-1 に変換不可）。カラースケールは独自設定（98パーセンタイル基準）。①top-leftは②top-rightと同一（Totaniの同時フィットにおける成分degeneracyは本解析の逐次差引きパイプラインには存在しないため）。Totaniのカラースケールは±2e-12 [cm^-2s^-1sr^-1MeV^-1]固定。",
        ],
    ),
    dict(
        image_file="fig12_equiv_lowE_maps.png",
        title="【再現図】低エネルギー4ビン 残差マップ — Totani Fig.12相当",
        caption=[
            "Bin{1,2,3,5}(1.5/2.5/4.3/12.3GeV)のハロー込み残差マップ（residual_masked）。",
            "4ビン共通でl~0-30°,b~+20-40°に強い正残差（フェルミバブル起源）。NFW-ρ²のS/Nは全て負。",
        ],
        notes=[
            "【ページの役割】",
            "再現図。Totani Fig.12（NFW-ρ²の「ハローモデル+残差」マップ, 21GeV未満の4ビン）の構造的アナログ。Fig.8で見た「低エネルギーでハロー成分ほぼゼロ〜負」の傾向を視覚確認。",
            "",
            "生成スクリプト: code/plot_totani_fig11_13_equiv.py（本フェーズで新規作成）",
            "出力ファイル: data/figure-all-bins/fig12_equiv_lowE_maps.png, fig11_13_equiv_summary.txt",
            "",
            "【図の内容】",
            "Bin{1,2,3,5}（E=1.51/2.55/4.31/12.29GeV）のresidual_maskedを4パネル表示。各パネル独立のカラースケール（98パーセンタイル基準, RdBu_r）。",
            "",
            "【重要な数値（fig11_13_equiv_summary.txt より）】",
            "・Bin1(1.51GeV): A_hat=-1.591e-16, S/N=-1.177",
            "・Bin2(2.55GeV): A_hat=-1.584e-16, S/N=-2.308",
            "・Bin3(4.31GeV): A_hat=-7.503e-17, S/N=-2.281",
            "・Bin5(12.29GeV): A_hat=-1.172e-17, S/N=-1.340",
            "",
            "【観察事項】",
            "4ビンとも l~0-30°, b~+20-40°付近（GC近傍・正銀緯側）に強い正の残差構造（フェルミバブル起源、Fig1相当のスライドと対応）が共通して現れる。NFW-ρ²振幅は全4ビンで負（=ハローというよりバックグラウンドモデルの過大評価方向）。",
            "",
            "【相違点】",
            "count-based arbitrary unit。カラースケールは98パーセンタイル基準で独自設定（Totaniは±2e-12固定）。",
        ],
    ),
    dict(
        image_file="fig13_equiv_highE_maps.png",
        title="【再現図】高エネルギー4ビン 残差マップ — Totani Fig.13相当",
        caption=[
            "Bin{7,8,9,10}(35/59/100/169GeV)のハロー込み残差マップ（residual_masked）。",
            "統計が乏しくショットノイズが優勢、構造化パターンなし。全て|S/N|<1.5。",
        ],
        notes=[
            "【ページの役割】",
            "再現図。Totani Fig.13（同上、21GeV超の4ビン: 35/59/100/170GeV）の構造的アナログ。21GeVをピークに急速に弱まる傾向を視覚確認。",
            "",
            "生成スクリプト: code/plot_totani_fig11_13_equiv.py（本フェーズで新規作成）",
            "出力ファイル: data/figure-all-bins/fig13_equiv_highE_maps.png, fig11_13_equiv_summary.txt",
            "",
            "【図の内容】",
            "Bin{7,8,9,10}（E=35.06/59.22/100.02/168.93GeV）のresidual_maskedを4パネル表示。各パネル独立のカラースケール（98パーセンタイル基準, RdBu_r）。",
            "",
            "【重要な数値（fig11_13_equiv_summary.txt より）】",
            "・Bin7(35.06GeV): A_hat=-2.028e-18, S/N=-0.640",
            "・Bin8(59.22GeV): A_hat=-2.106e-18, S/N=-1.033",
            "・Bin9(100.02GeV): A_hat=-1.906e-18, S/N=-1.467",
            "・Bin10(168.93GeV): A_hat=+9.878e-19, S/N=+1.118",
            "",
            "【観察事項】",
            "高エネルギーになるほど統計が乏しくショットノイズが優勢になり、Fig12のような構造化された残差パターンは視認できない。全4ビンで|S/N|<1.5 ― 有意な検出なし。",
            "",
            "【相違点】",
            "count-based arbitrary unit。カラースケールは98パーセンタイル基準で独自設定。",
        ],
    ),
]


def _qn(prefix: str, tag: str) -> str:
    return f"{{{NS[prefix]}}}{tag}"


def _max_numbered(data: dict[str, bytes], pattern: str) -> int:
    import re

    nums = []
    for name in data:
        m = re.match(pattern, name)
        if m:
            nums.append(int(m.group(1)))
    return max(nums)


def build_slide_xml(template: bytes, spec: dict, img_cx: int, img_x: int) -> bytes:
    root = etree.fromstring(template)
    spTree = root.find(f".//{_qn('p','spTree')}")
    children = list(spTree)
    title_sp, pic, caption_sp = children[2], children[3], children[4]

    title_t = title_sp.find(f".//{_qn('a','t')}")
    title_t.text = spec["title"]

    cNvPr = pic.find(f".//{_qn('p','cNvPr')}")
    cNvPr.set("descr", spec["image_file"])
    xfrm = pic.find(f".//{_qn('a','xfrm')}")
    off = xfrm.find(_qn("a", "off"))
    ext = xfrm.find(_qn("a", "ext"))
    off.set("x", str(img_x))
    off.set("y", str(IMG_Y))
    ext.set("cx", str(img_cx))
    ext.set("cy", str(IMG_CY))

    # caption box: resize cy
    cap_xfrm = caption_sp.find(f".//{_qn('a','xfrm')}")
    cap_ext = cap_xfrm.find(_qn("a", "ext"))
    cap_ext.set("cy", str(CAPTION_BOX["cy"]))

    txBody = caption_sp.find(_qn("p", "txBody"))
    p_elem = txBody.find(_qn("a", "p"))
    for child in list(p_elem):
        p_elem.remove(child)
    for i, text in enumerate(spec["caption"]):
        if i > 0:
            p_elem.append(p_elem.makeelement(_qn("a", "br"), {}))
        run = p_elem.makeelement(_qn("a", "r"), {})
        rPr = run.makeelement(_qn("a", "rPr"), {"sz": "1100"})
        fill = rPr.makeelement(_qn("a", "solidFill"), {})
        fill.append(fill.makeelement(_qn("a", "srgbClr"), {"val": "FFFFFF"}))
        rPr.append(fill)
        run.append(rPr)
        t = run.makeelement(_qn("a", "t"), {})
        t.text = text
        run.append(t)
        p_elem.append(run)

    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def _rel_id_by_type(rels_root, type_suffix: str) -> str:
    for rel in rels_root:
        if rel.get("Type").endswith(type_suffix):
            return rel.get("Id")
    raise ValueError(f"no relationship with type ending {type_suffix!r}")


def build_slide_rels(template: bytes, img_target: str, notes_target: str) -> bytes:
    root = etree.fromstring(template)
    rid_image = _rel_id_by_type(root, "/image")
    rid_notes = _rel_id_by_type(root, "/notesSlide")
    for rel in root:
        if rel.get("Id") == rid_image:
            rel.set("Target", img_target)
        elif rel.get("Id") == rid_notes:
            rel.set("Target", notes_target)
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def build_notes_xml(template: bytes, lines: list[str]) -> bytes:
    root = etree.fromstring(template)
    sp = root.find(f".//{_qn('p','sp')}")
    txBody = sp.find(_qn("p", "txBody"))
    for child in list(txBody):
        if etree.QName(child).localname == "p":
            txBody.remove(child)
    for line in lines:
        p_elem = txBody.makeelement(_qn("a", "p"), {})
        run = p_elem.makeelement(_qn("a", "r"), {})
        t = run.makeelement(_qn("a", "t"), {})
        if line:
            t.text = line
        run.append(t)
        p_elem.append(run)
        txBody.append(p_elem)
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def build_notes_rels(template: bytes, slide_target: str) -> bytes:
    root = etree.fromstring(template)
    rid_slide = _rel_id_by_type(root, "/slide")
    for rel in root:
        if rel.get("Id") == rid_slide:
            rel.set("Target", slide_target)
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def process(pptx_path: Path) -> list[str]:
    with zipfile.ZipFile(pptx_path, "r") as z:
        data = {n: z.read(n) for n in z.namelist()}

    slide_tmpl = data["ppt/slides/slide29.xml"]
    slide_rels_tmpl = data["ppt/slides/_rels/slide29.xml.rels"]

    slide_rels_root = etree.fromstring(slide_rels_tmpl)
    rid_notes = _rel_id_by_type(slide_rels_root, "/notesSlide")
    notes_target_orig = next(
        rel.get("Target") for rel in slide_rels_root if rel.get("Id") == rid_notes
    )
    notes_filename = notes_target_orig.rsplit("/", 1)[-1]
    notes_tmpl = data[f"ppt/notesSlides/{notes_filename}"]
    notes_rels_tmpl = data[f"ppt/notesSlides/_rels/{notes_filename}.rels"]

    pres_root = etree.fromstring(data["ppt/presentation.xml"])
    pres_rels_root = etree.fromstring(data["ppt/_rels/presentation.xml.rels"])
    ct_root = etree.fromstring(data["[Content_Types].xml"])

    base_id = max(int(c.get("id")) for c in pres_root.find(_qn("p", "sldIdLst"))) + 1
    base_rid = max(int(rel.get("Id")[3:]) for rel in pres_rels_root) + 1
    base_slide = _max_numbered(data, r"ppt/slides/slide(\d+)\.xml$") + 1
    base_notes = _max_numbered(data, r"ppt/notesSlides/notesSlide(\d+)\.xml$") + 1
    base_img = _max_numbered(data, r"ppt/media/image(\d+)\.\w+$") + 1

    new_ids: list[str] = []
    new_rids: list[str] = []
    for i, spec in enumerate(NEW_SLIDES):
        sid = str(base_id + i)
        rid = f"rId{base_rid + i}"
        slide_num = base_slide + i
        notes_num = base_notes + i
        img_num = base_img + i
        ext = Path(spec["image_file"]).suffix
        new_ids.append(sid)
        new_rids.append(rid)

        img_path = FIG_DIR / spec["image_file"]
        w, h = Image.open(img_path).size
        img_cx = IMG_CY * w // h
        img_x = CONTENT_CENTER_X - img_cx // 2

        img_target = f"../media/image{img_num}{ext}"
        notes_target = f"../notesSlides/notesSlide{notes_num}.xml"
        slide_target = f"../slides/slide{slide_num}.xml"

        data[f"ppt/media/image{img_num}{ext}"] = img_path.read_bytes()
        data[f"ppt/slides/slide{slide_num}.xml"] = build_slide_xml(slide_tmpl, spec, img_cx, img_x)
        data[f"ppt/slides/_rels/slide{slide_num}.xml.rels"] = build_slide_rels(
            slide_rels_tmpl, img_target, notes_target
        )
        data[f"ppt/notesSlides/notesSlide{notes_num}.xml"] = build_notes_xml(notes_tmpl, spec["notes"])
        data[f"ppt/notesSlides/_rels/notesSlide{notes_num}.xml.rels"] = build_notes_rels(
            notes_rels_tmpl, slide_target
        )

        rel_elem = pres_rels_root.makeelement(
            _qn("rel", "Relationship"),
            {
                "Id": rid,
                "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide",
                "Target": f"slides/slide{slide_num}.xml",
            },
        )
        pres_rels_root.append(rel_elem)

        for partname, ctype in [
            (
                f"/ppt/slides/slide{slide_num}.xml",
                "application/vnd.openxmlformats-officedocument.presentationml.slide+xml",
            ),
            (
                f"/ppt/notesSlides/notesSlide{notes_num}.xml",
                "application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml",
            ),
        ]:
            ov = ct_root.makeelement(_qn("ct", "Override"), {"PartName": partname, "ContentType": ctype})
            ct_root.append(ov)

    # main sldIdLst: insert after id=306
    sldIdLst = pres_root.find(_qn("p", "sldIdLst"))
    idx_anchor = next(i for i, c in enumerate(sldIdLst) if c.get("id") == ANCHOR_ID)
    for offset, (sid, rid) in enumerate(zip(new_ids, new_rids)):
        elem = sldIdLst.makeelement(_qn("p", "sldId"), {"id": sid, _qn("r", "id"): rid})
        sldIdLst.insert(idx_anchor + 1 + offset, elem)

    # p14:sectionLst -> Results section sldIdLst: insert after id=306
    extLst = pres_root.find(_qn("p", "extLst"))
    results_sldIdLst = None
    insert_pos = None
    for ext in extLst:
        sectionLst = ext.find(_qn("p14", "sectionLst"))
        if sectionLst is None:
            continue
        for section in sectionLst:
            sec_sldIdLst = section.find(_qn("p14", "sldIdLst"))
            ids_here = [c.get("id") for c in sec_sldIdLst]
            if ANCHOR_ID in ids_here:
                idx = ids_here.index(ANCHOR_ID)
                if idx + 1 < len(ids_here) and ids_here[idx + 1] == "307":
                    results_sldIdLst = sec_sldIdLst
                    insert_pos = idx
                    break
        if results_sldIdLst is not None:
            break
    assert results_sldIdLst is not None, "Results section (id 306 -> 307) not found"

    for offset, sid in enumerate(new_ids):
        elem = results_sldIdLst.makeelement(_qn("p14", "sldId"), {"id": sid})
        results_sldIdLst.insert(insert_pos + 1 + offset, elem)

    data["ppt/presentation.xml"] = etree.tostring(
        pres_root, xml_declaration=True, encoding="UTF-8", standalone=True
    )
    data["ppt/_rels/presentation.xml.rels"] = etree.tostring(
        pres_rels_root, xml_declaration=True, encoding="UTF-8", standalone=True
    )
    data["[Content_Types].xml"] = etree.tostring(
        ct_root, xml_declaration=True, encoding="UTF-8", standalone=True
    )

    tmp_path = pptx_path.with_suffix(".pptx.tmp")
    with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, content in data.items():
            zout.writestr(name, content)
    shutil.move(str(tmp_path), str(pptx_path))
    return new_ids


def main() -> None:
    targets = [
        Path("/mnt/c/Users/arsei/Downloads/slides_v3_detailed_18pt.pptx"),
        Path("/mnt/c/Users/arsei/Downloads/slides_v3_detailed_fixed2.pptx"),
    ]
    for path in targets:
        new_ids = process(path)
        print(f"{path.name}: inserted slide ids {new_ids}")


if __name__ == "__main__":
    main()
