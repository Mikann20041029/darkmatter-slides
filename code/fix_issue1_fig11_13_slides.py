"""
slide33/34/35 (【再現図】Fig.11/12/13相当) の画像・キャプション・ノートを、
2026-07-13にMCMCベースへ再生成した code/plot_totani_fig11_13_equiv.py の
出力(data/figure-all-bins/fig11_13_equiv_summary.txt 等)に合わせて更新する。
issue-1 T-1.033/034/035 対応。
"""
from pathlib import Path
from pptx import Presentation

ROOT = Path(__file__).resolve().parent.parent
PPT_PATH = ROOT / "PPT" / "slides_v3_detailed_fixed2_final.pptx  -  Repaired.pptx"
FIG_DIR = ROOT / "data" / "figure-all-bins"


def replace_picture(slide, image_path):
    for sh in list(slide.shapes):
        if sh.shape_type == 13:
            left, top, width, height = sh.left, sh.top, sh.width, sh.height
            sh._element.getparent().remove(sh._element)
            slide.shapes.add_picture(str(image_path), left, top, width=width, height=height)
            return
    raise ValueError("no picture shape found")


def by_text(shapes, needle):
    for sh in shapes:
        if sh.has_text_frame and needle in sh.text_frame.text:
            return sh
    raise ValueError(f"shape not found containing {needle!r}")


def set_notes(slide, lines):
    notes_tf = slide.notes_slide.notes_text_frame
    notes_tf.clear()
    notes_tf.paragraphs[0].text = lines[0]
    for line in lines[1:]:
        p = notes_tf.add_paragraph()
        p.text = line


def main():
    prs = Presentation(str(PPT_PATH))

    # ---------------- slide33: Bin6 2x2 (Fig11相当) ----------------
    sl = prs.slides[32]
    replace_picture(sl, FIG_DIR / "fig11_equiv_bin6_maps.png")
    cap = by_text(sl.shapes, "no-halo残差").text_frame.paragraphs[0]
    cap.runs[0].text = (
        "Bin6(20.76GeV)の2×2マップ(MCMC同時フィット)：①no-halo最適化残差 ②with-halo最適化残差(ハロー項抜き) "
        "③NFW-ρ²ハローモデル(f_halo=+0.665) ④②−③。"
    )
    cap.runs[1].text = "有意度=+8.73σ（結果はresults/mcmc_allbins/mcmc_bin06.jsonと同一の中央値を使用）。"
    set_notes(sl, [
        "【ページの役割】",
        "再現図。Totani Fig.11（top-left=no-haloフィット残差、top-right=ハロー込み残差、bottom-left=ハローモデル、bottom-right=減算後残差）の構造的アナログ。",
        "",
        "2026-07-13改訂: MCMC同時フィット(code/mcmc_fit_all_bins.py)導入に伴い再生成。",
        "生成スクリプト: code/plot_totani_fig11_13_equiv.py（mcmc_fit_all_bins.pyの関数・保存済みベストフィット値を再利用）",
        "出力ファイル: data/figure-all-bins/fig11_equiv_bin6_maps.png, fig11_13_equiv_summary.txt",
        "",
        "【図の内容・実装対応】",
        "①top-left = data − no-halo(4パラメータ)最適化モデル。no-halo側は本図生成時にその場で多点始動Nelder-Meadで再計算(MCMCは行わない)",
        "②top-right = data − with-halo(5パラメータ, MCMC中央値)最適化モデルのうちハロー項を除いた部分。旧版と異なり①とは別の背景パラメータを使うため完全同一ではない",
        "③bottom-left = f_halo(MCMC中央値=+0.665) × NFW-ρ² J_2マップ",
        "④bottom-right = ② − ③",
        "①②③④は同一カラースケール（②の98パーセンタイル基準, RdBu_r）",
        "",
        "【観察事項】",
        "③（ハローモデル）は銀河中心方向(l~0°)にわずかな正の増光が見えるが振幅は小さい。④は②とほぼ同じ構造を保持しており、"
        "フェルミバブル起源とみられる正の残差(l~0-20°, b~10-30°)がハロー差引き後も残ることが見える。",
        "",
        "【相違点】",
        "count-based arbitrary unit（flux単位 cm^-2 s^-1 sr^-1 MeV^-1 に変換不可）。Totaniのカラースケールは±2e-12 [cm^-2s^-1sr^-1MeV^-1]固定。",
    ])

    # ---------------- slide34: 低エネルギー4ビン (Fig12相当) ----------------
    sl = prs.slides[33]
    replace_picture(sl, FIG_DIR / "fig12_equiv_lowE_maps.png")
    cap = by_text(sl.shapes, "Bin{1,2,3,5}").text_frame.paragraphs[0]
    cap.runs[0].text = (
        "Bin{1,2,3,5}(1.5/2.5/4.3/12.3GeV)のハロー込み残差マップ(MCMC同時フィット、with-haloモデルからハロー項を除いた残差)。"
    )
    cap.runs[1].text = (
        "4ビン共通でl~0-30°,b~+15-30°に強い正残差（フェルミバブル起源）。全4ビンでf_haloは大きく負(有意度-15〜-23σ、GALPROPガス成分不確かさに由来と推定)。"
    )
    set_notes(sl, [
        "【ページの役割】",
        "再現図。Totani Fig.12（NFW-ρ²の「ハローモデル+残差」マップ, 21GeV未満の4ビン）の構造的アナログ。",
        "",
        "2026-07-13改訂: MCMC同時フィット(code/mcmc_fit_all_bins.py)導入に伴い再生成。",
        "生成スクリプト: code/plot_totani_fig11_13_equiv.py",
        "出力ファイル: data/figure-all-bins/fig12_equiv_lowE_maps.png, fig11_13_equiv_summary.txt",
        "",
        "【図の内容】",
        "Bin{1,2,3,5}（E=1.51/2.55/4.31/12.29GeV）のwith-halo残差(ハロー項抜き)を4パネル表示。各パネル独立のカラースケール。",
        "",
        "【重要な数値（fig11_13_equiv_summary.txt より、f_halo=MCMC中央値）】",
        "・Bin1(1.51GeV): f_halo=-2.93e+02, 有意度=-22.66σ",
        "・Bin2(2.55GeV): f_halo=-7.73e+01, 有意度=-17.51σ",
        "・Bin3(4.31GeV): f_halo=-3.09e+01, 有意度=-15.31σ",
        "・Bin5(12.29GeV): f_halo=+6.20e-01, 有意度=+8.71σ",
        "",
        "【観察事項】",
        "Bin1-3は強い負の有意度(欠損)を示す一方、Bin5は正に転じ8.71σに達している(Bin6の8.73σとほぼ同水準、"
        "スライド29のスペクトルで見えるBin5-6ピークに対応)。低エネルギー3ビンの負の有意度はDiscussion(2/3)で議論するGALPROPガス成分の不確かさが主要因と推定される。",
        "",
        "【相違点】",
        "count-based arbitrary unit。カラースケールは98パーセンタイル基準で独自設定（Totaniは±2e-12固定）。",
    ])

    # ---------------- slide35: 高エネルギー4ビン (Fig13相当) ----------------
    sl = prs.slides[34]
    replace_picture(sl, FIG_DIR / "fig13_equiv_highE_maps.png")
    cap = by_text(sl.shapes, "Bin{7,8,9,10}").text_frame.paragraphs[0]
    cap.runs[0].text = (
        "Bin{7,8,9,10}(35/59/100/169GeV)のハロー込み残差マップ(MCMC同時フィット、with-haloモデルからハロー項を除いた残差)。"
    )
    cap.runs[1].text = "統計が乏しくショットノイズが優勢。有意度は+1.1〜+4.0σでBin7が最大、以降エネルギーとともに減少。"
    set_notes(sl, [
        "【ページの役割】",
        "再現図。Totani Fig.13（同上、21GeV超の4ビン: 35/59/100/170GeV）の構造的アナログ。",
        "",
        "2026-07-13改訂: MCMC同時フィット(code/mcmc_fit_all_bins.py)導入に伴い再生成。",
        "生成スクリプト: code/plot_totani_fig11_13_equiv.py",
        "出力ファイル: data/figure-all-bins/fig13_equiv_highE_maps.png, fig11_13_equiv_summary.txt",
        "",
        "【図の内容】",
        "Bin{7,8,9,10}（E=35.06/59.22/100.02/168.93GeV）のwith-halo残差(ハロー項抜き)を4パネル表示。各パネル独立のカラースケール。",
        "",
        "【重要な数値（fig11_13_equiv_summary.txt より、f_halo=MCMC中央値）】",
        "・Bin7(35.06GeV): f_halo=+2.58e-01, 有意度=+4.01σ",
        "・Bin8(59.22GeV): f_halo=+5.84e-02, 有意度=+3.16σ",
        "・Bin9(100.02GeV): f_halo=+8.31e-03, 有意度=+1.35σ",
        "・Bin10(168.93GeV): f_halo=+1.09e-03, 有意度=+1.14σ",
        "",
        "【観察事項】",
        "高エネルギーになるほど統計が乏しくショットノイズが優勢になり、Fig12のような構造化された残差パターンは視認できない。"
        "有意度はBin7(35GeV)の+4.01σを頂点にBin10(169GeV)の+1.14σまで単調に減衰する。",
        "",
        "【相違点】",
        "count-based arbitrary unit。カラースケールは98パーセンタイル基準で独自設定。",
    ])

    prs.save(str(PPT_PATH))
    print("保存完了:", PPT_PATH)


if __name__ == "__main__":
    main()
