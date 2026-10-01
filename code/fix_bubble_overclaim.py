"""
2026-07-13 ユーザー指摘への対応その2。

diagnose_bubble_check.py で、バブル領域内のf_fb(バブル振幅)が0.395-0.459という
妥当な範囲に収まっており(境界に張り付いていない)、「バブルテンプレートの規格化不足で
NFWがそれを肩代わりしている」という説明が支持されないことが判明した。
一方でf_gal(GALPROP振幅)はバブル領域内0.682・全ROI0.692に対し高緯度域のみでは0.576と
約15-20%系統的にズレており、GALPROP単一テンプレート(gas/ICS分離なし)の空間形状不一致
の方がより支持される説明であることが分かった。スライド36・80・81の該当記述を訂正する。
"""
from pathlib import Path
from pptx import Presentation

ROOT = Path(__file__).resolve().parent.parent
PPT_PATH = ROOT / "PPT" / "slides_v3_detailed_fixed2_final.pptx  -  Repaired.pptx"


def by_text(shapes, needle):
    for sh in shapes:
        if sh.has_text_frame and needle in sh.text_frame.text:
            return sh
    raise ValueError(f"shape not found containing {needle!r}")


def main():
    prs = Presentation(str(PPT_PATH))

    # ---------------- slide36: 頑健性検証スライド ----------------
    sl = prs.slides[35]
    sh = by_text(sl.shapes, "検証方法")
    tf = sh.text_frame
    tf.paragraphs[9].runs[0].text = (
        "・追加検証: バブル領域内でf_fb(バブル振幅)を自由にしても0.40〜0.46という妥当な範囲に収まり"
        "(境界に張り付かない)、「バブル規格化不足」という説明は支持されなかった → 撤回"
    )
    tf.paragraphs[10].runs[0].text = (
        "・一方f_gal(GALPROP振幅)はバブル領域内0.68・全ROI0.69に対し、バブル外の高緯度のみでは0.58と"
        "約15-20%系統的にズレる。GALPROP単一テンプレート(gas/ICS分離なし)の空間形状不一致がより支持される"
    )
    tf.paragraphs[11].runs[0].text = (
        "(f_gal shiftは実測値。原因の直接検証にはgalprop.stanford.edu復旧後のgas/ICS分離webrunが必要)"
    )

    # ---------------- slide81: Conclusion ----------------
    sl = prs.slides[80]
    sh = by_text(sl.shapes, "バブル外挿")
    sh.text_frame.paragraphs[0].runs[0].text = (
        "GALPROP gas/ICS分離実装（Stanford webrun復旧待ち）。"
        "追加検証でGALPROP振幅が領域により15-20%系統的にズレることを確認済み(バブル振幅は正常範囲、"
        "バブル規格化不足という説明は撤回)。現状は「Totaniの20GeV超過を頑健に再現できなかった」ことと、"
        "その原因がGALPROP単一テンプレートの空間形状不一致である可能性が高いことが本研究の結論"
    )

    prs.save(str(PPT_PATH))
    print("保存完了:", PPT_PATH)


if __name__ == "__main__":
    main()
