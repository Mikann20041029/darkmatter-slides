"""
2026-07-13 ユーザー指摘への対応: PPTのMethodセクション(スライド9-13、
GALPROP・フェルミバブル特に)が古い手法(MCMC導入前・バブル正のみ)の説明の
ままで、かつ説明が難しすぎるとの指摘を受け、MCMC_VERIFICATION.md と同じ
平易さで書き直す。

主な間違い(修正前):
  - スライド10(GALPROP): 「MCMCは未実装」「scipy.optimizeでPoisson MLE」
    と書かれているが、現在は他5成分と一緒にMCMC(emcee)で同時フィットして
    いる。「有意性に±数σの系統誤差」という古い注記も、GALPROPのgas/ICS
    分離未実装という今の正確な課題設定に置き換える
  - スライド12(フェルミバブル): 「各ビンでPoisson MLEにより振幅Aを決定」
    と単一テンプレート前提で書かれているが、2026-07-13にTotani §3.1準拠の
    正負2テンプレート化(f_fb, f_fb_neg)を実装済み
  - スライド9(等方背景): 「Step1〜5を順に引き算する」という枠組み自体が、
    現在の「6成分同時MCMCフィット」という実際の手法と食い違うため、
    最初のStepスライドに一言補足を追加する
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

    # ------------------------------------------------------------------
    # slide9 (0-idx 8): Step1 等方背景 — 冒頭に全体の枠組み補足を追加
    # ------------------------------------------------------------------
    sl = prs.slides[8]
    sh = by_text(sl.shapes, "エネルギービンごとに独立に計算")
    runs = sh.text_frame.paragraphs[0].runs
    runs[-1].text += (
        "\n\n※ Step1〜5は「順番に引き算する」という意味ではなく、実際にはStep2〜5の"
        "6つの倍率(つまみ)をMCMCで同時に求める(Step1の等方背景だけは固定値)。"
        "詳しくはStep2(GALPROP)参照"
    )

    # ------------------------------------------------------------------
    # slide10 (0-idx 9): Step2 GALPROP — 全面書き直し
    # ------------------------------------------------------------------
    sl = prs.slides[9]
    shapes = sl.shapes

    sh = by_text(shapes, "MCMCは未実装")
    tf = sh.text_frame
    runs = tf.paragraphs[0].runs
    runs[0].text = (
        "同じファイル（gll_iem_v07.fits）を使用。「GALPROPの明るさを何倍すれば"
        "実測に合うか」という倍率(f_gal)を、\n他の4成分(ループI・バブル・ハロー)と"
        "一緒にMCMC(emcee)で同時に求める\n現在の値(Bin6, 20.76GeV): f_gal ≈ 0.69"
    )
    for r in runs[1:]:
        r.text = ""

    sh = by_text(shapes, "手法近似あり（MCMCなし")
    tf = sh.text_frame
    runs = tf.paragraphs[0].runs
    runs[0].text = "△ "
    runs[1].text = "gas/ICS分離が未実装"
    runs[2].text = "。"
    runs[3].text = "f_gal=0.69は「GALPROPの生の予測は実測より約45%明るすぎた」という意味"

    sh = by_text(shapes, "Poisson 尤度最大化の式")
    sh.text_frame.paragraphs[0].runs[0].text = "「予測」と「実測」を比べる考え方"

    sh = by_text(shapes, "フィットモデル")
    tf = sh.text_frame
    runs = tf.paragraphs[0].runs
    new_text = (
        "予測 μ = 等方背景 + f_gal×GALPROP + …(他4成分)\n\n"
        "実測カウント数 n が、この予測 μ とどれだけ合うかを、\n"
        "Poisson統計の式で数値化する:\n\n"
        "  当てはまり度 = n × ln(μ) − μ\n\n"
        "6個の倍率つまみ(f_gal含む)を、コンピュータが\n"
        "自動で「一番当てはまりが良い値」に調整する。\n"
        "5個の成分をバラバラに引き算するのではなく、\n"
        "全部まとめて1回で最適化する。\n\n"
        "GALPROPの生の予測は実測より約45%明るすぎた\n"
        "(f_gal≈0.69にすると実測に合う)\n\n"
        "詳しい導出・検算は MCMC_VERIFICATION.md 参照"
    )
    runs[0].text = new_text
    for r in runs[1:]:
        r.text = ""

    # ------------------------------------------------------------------
    # slide12 (0-idx 11): Step4 フェルミバブル — 正負2テンプレート化を反映
    # ------------------------------------------------------------------
    sl = prs.slides[11]
    shapes = sl.shapes

    sh = by_text(shapes, "4.3 GeV（Bin3）の[Iso+GALPROP+PS]残差マップを")
    tf = sh.text_frame
    p = tf.paragraphs[0]
    p.runs[0].text = (
        "4.3 GeV（Bin3）の[Iso+GALPROP+PS]残差マップのうち、\n"
        "正の残差(バブル本体)と負の残差(GALPROPのズレ由来)を\n"
        "別々のテンプレートとして使い、各ビンで振幅をフィット"
    )

    sh = by_text(shapes, "同じ手法を実装 ✓")
    tf = sh.text_frame
    p = tf.paragraphs[0]
    p.runs[0].text = (
        "2026-07-13更新: 正負2テンプレート化 ✓\n"
        "Bin3（4.31 GeV）残差を「正の部分」「負の部分」に分けてテンプレート化\n"
        "(Gaussianぼかし σ=1° も追加)\n"
        "他4成分と一緒にMCMCで振幅(f_fb, f_fb_neg)を同時に決定"
    )

    sh = by_text(shapes, "Totaniの手法を再現（データ駆動テンプレート）")
    sh.text_frame.paragraphs[0].runs[0].text = (
        "✓ Totaniの手法に完全準拠（正負2テンプレート、2026-07-13修正済み）"
    )

    prs.save(str(PPT_PATH))
    print("保存完了:", PPT_PATH)


if __name__ == "__main__":
    main()
