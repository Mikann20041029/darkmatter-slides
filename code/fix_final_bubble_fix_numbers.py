"""
2026-07-13 最終更新: フェルミバブル正負2テンプレート化(Totani §3.1準拠)+多点始動
再始動回数バグ修正(8→30)後の最終13ビン結果をPPT全体に反映する。

背景: ユーザーから「フェルミバブルくらいは正しく実装しろ」という指摘を受け、
Totani (2025) §3.1 原文を精読したところ、正の残差(バブル本体)だけでなく
負の残差(GALPROPモデルとの不一致に由来)も独立テンプレートとして使う設計だと判明。
これを実装(f_fb_neg追加、6パラメータモデル化)したところ、副作用として多点始動の
再始動回数(8回)が新しい探索空間で不足し、Bin3/4/7で非物理的な高有意度が出る
バグを誘発した。これを30回に修正した最終版で全13ビンを再計算した結果:

  Bin6(ヘッドライン): f_halo=+0.665→+0.664(ほぼ不変), 有意度8.73σ→4.83σ
  Bin5: 8.71σ→1.90σ(検出消失)
  領域分割頑健性再検証(Bin6): バブル領域内 7.78σ→1.60σ(ほぼ解消)、
                              高緯度バブル外 -9.04σ→-8.89σ(不変)

結論: バブル領域内の見かけの超過はバブルの不完全実装が原因だったと実証されたが、
高緯度側の強い負の有意度(GALPROP単一テンプレート起因と推定)は未解決のまま残り、
全体としての結論(頑健な検出とは言えない)は変わらない。
"""
import json
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
    halo = json.load(open(ROOT / "results" / "mcmc_allbins" / "halo_spectrum.json"))

    # ------------------------------------------------------------------
    # slide29 (0-idx 28): 全13ビンスペクトル(ヘッドライン図)
    # ------------------------------------------------------------------
    sl = prs.slides[28]
    sh = by_text(sl.shapes, "NFW ハロー振幅")
    p = sh.text_frame.paragraphs[0]
    p.runs[0].text = (
        "全13エネルギービンでの NFW ハロー振幅 f_halo とその1σ不確かさ（MCMC同時フィット、6自由パラメータ、"
        "フェルミバブル正負2テンプレート化・多点始動30回化済み）。等方背景はビンごとに固定。"
    )
    p.runs[1].text = (
        "Bin4/6/7で見かけの超過(4.8-8.4σ)があるが、頑健性検証(スライド36)で全て頑健な検出とは言えないと判明。"
    )
    notes_tf = sl.notes_slide.notes_text_frame
    notes_tf.text += (
        "\n\n【2026-07-13 追記2: バブル修正+最適化バグ修正後】\n"
        "フェルミバブルを正負2テンプレート化(Totani §3.1準拠)し、これに伴い再発した多点始動の"
        "局所解バグ(n_restarts 8→30に修正)を解消した最終版。Bin6は8.73σ→4.83σに、Bin5は"
        "8.71σ→1.90σ(検出消失)に変化。Bin3/4は参照ビン(バブルテンプレートの構築元)近傍のため"
        "解釈に注意が必要(Totani自身も同様の注意を論文中で明記)。"
        "詳細: data/figure-halo-diagnostics/, .dev/CHANGELOG.md参照。"
    )

    # ------------------------------------------------------------------
    # slide36 (0-idx 35): 頑健性検証スライド(全面刷新)
    # ------------------------------------------------------------------
    sl = prs.slides[35]
    sh = by_text(sl.shapes, "検証方法")
    tf = sh.text_frame
    tf.paragraphs[4].runs[0].text = (
        "結果(f_halo中央値, 有意度) — バブル正負2テンプレート化+多点始動30回化 最終版"
    )
    tf.paragraphs[5].runs[0].text = (
        "Bin6(20.76GeV):  全ROI +0.664(4.8σ)  |  ①バブル領域 +0.295(1.6σ)  |  ③バブル外・|b|≥30° −4.05(8.9σ)"
    )
    tf.paragraphs[6].runs[0].text = (
        "Bin5(12.29GeV):  全ROI +0.608(1.9σ)  |  ①バブル領域 −1.82(3.0σ)  |  ③バブル外・|b|≥30° −18.4(15.5σ)"
    )
    tf.paragraphs[8].runs[0].text = "解釈(2026-07-13 バブル修正後に更新)"
    tf.paragraphs[9].runs[0].text = (
        "・バブル領域内の見かけの超過はTotani §3.1準拠の正負2テンプレート化でほぼ解消(Bin6: 7.8σ→1.6σ、"
        "Bin5は符号反転して弱含み) → 「バブル規格化不足」ではなく「バブルテンプレートの形状不完全性"
        "(負の残差成分の欠落)」が正しい原因だったと確定"
    )
    tf.paragraphs[10].runs[0].text = (
        "・一方、高緯度側(バブル外)の強い負の有意度はバブル修正の影響を全く受けず不変(−9.0σ→−8.9σ)。"
        "GALPROP単一テンプレート(gas/ICS分離なし)の空間形状不一致が引き続き未解決の主因"
    )
    tf.paragraphs[11].runs[0].text = (
        "・全ROIでの見かけの検出(Bin6=4.8σ)は、弱まったバブル領域の寄与(1.6σ)と、"
        "変わらず強い高緯度の負の寄与(-8.9σ)の綱引きの結果であり、依然として頑健な単一の物理信号ではない"
    )
    tf.paragraphs[13].runs[0].text = "結論(更新)"
    tf.paragraphs[14].runs[0].text = (
        "バブル実装は修正・改善したが、GALPROP起因とみられる高緯度側の系統誤差が未解決のため、"
        "Bin6の4.8σを「Totaniの20GeV超過の再現」として主張することはまだできない"
    )
    tf.paragraphs[15].runs[0].text = (
        "生成: code/diagnose_halo_degeneracy_3_posneg.py, diagnose_restart_stability.py"
    )

    # ------------------------------------------------------------------
    # slide81 (0-idx 80): Conclusion
    # ------------------------------------------------------------------
    sl = prs.slides[80]
    sh = by_text(sl.shapes, "8.73σは頑健性検証で符号反転")
    sh.text_frame.paragraphs[0].runs[0].text = (
        "✗ Bin6（20.76 GeV）の見かけの検出は4.83σまで低下・依然頑健でない"
    )
    sh2 = by_text(sl.shapes, "追加検証でGALPROP振幅が領域により")
    p = sh2.text_frame.paragraphs[0]
    p.runs[0].text = (
        "フェルミバブルをTotani §3.1準拠(正負2テンプレート)に修正した結果、バブル領域内の見かけの超過は"
        "7.8σ→1.6σにほぼ解消(旧説明「バブル規格化不足」は撤回済み、正しい原因は形状不完全性だった)。"
    )
    p.runs[1].text = "しかし高緯度側の強い負の有意度(-8.9σ)は不変で、GALPROP系統誤差が未解決のまま残る"
    sh3 = by_text(sl.shapes, "バブル外挿・GALPROP系統誤差")
    sh3.text_frame.paragraphs[0].runs[0].text = (
        "GALPROP gas/ICS分離実装（Stanford webrun復旧待ち、これが最後の主要な未解決差異）。"
        "フェルミバブルはTotani準拠に修正済み。現状は「Totaniの20GeV超過を頑健に再現できなかった」ことと、"
        "その原因を段階的に特定・一部解消した(バブル起因を解消、GALPROP起因が残存)ことが本研究の結論"
    )

    # ------------------------------------------------------------------
    # slide93 (0-idx 92): 6成分モデル定量比較 — フェルミバブル行を更新
    # ------------------------------------------------------------------
    sl = prs.slides[92]
    sh = by_text(sl.shapes, "フェルミバブル")
    tf = sh.text_frame
    for p in tf.paragraphs:
        if p.runs and "フェルミバブル" in p.runs[0].text:
            p.runs[0].text = (
                "フェルミバブル 正負2テンプレート(Bin3基準)+σ=1°smoothing  正負2テンプレート+σ=1°  "
                "2026-07-13にTotani §3.1準拠(負テンプレート追加)に修正済み。境界は固定矩形のまま(Totaniは反復改善)"
            )
            break

    # ------------------------------------------------------------------
    # slide94 (0-idx 93): 全13ビンスペクトル表
    # ------------------------------------------------------------------
    sl = prs.slides[93]
    sh = by_text(sl.shapes, "結果一覧")
    tf = sh.text_frame
    rows = []
    for b in halo["bins"]:
        fh = b["params"]["f_halo"]["median"]
        sig = b["significance_sigma"]
        signed = sig if fh >= 0 else -sig
        sign_txt = "正" if fh >= 0 else "負"
        mark = " ★" if b["bin"] == 6 else ""
        rows.append(f" {b['bin']:02d}  {b['e_center_gev']:7.2f}   {signed:+6.2f} σ{mark}   {sign_txt}")
    tf.paragraphs[1].runs[0].text = (
        "▼ 結果一覧（mcmc_fit_all_bins.py, 2026-07-13 バブル正負2テンプレート化+多点始動30回化 最終版）"
    )
    for i, row in enumerate(rows):
        tf.paragraphs[3 + i].runs[0].text = row
    tf.paragraphs[16].runs[0].text = (
        "Bin4=8.37σ(参照ビン近傍のため解釈注意)、Bin6=4.83σ、Bin1-3は−4.8〜−15.2σの負の有意度"
        "(参照: results/mcmc_allbins/halo_spectrum.json)\n"
        "※有意度はWilks近似によるものであり近似の妥当性は未検証。頑健性検証(スライド36)ではBin6の"
        "4.83σも領域分割で崩れることを確認済み"
    )

    sh2 = by_text(sl.shapes, "スペクトルの読み方")
    tf2 = sh2.text_frame
    tf2.paragraphs[5].runs[0].text = (
        "・Bin4/6/7 (7.3/20.8/35.1 GeV) で見かけの正の超過(4.8-8.4σ) — ただし頑健性検証(スライド36)で"
        "領域分割すると崩れることを確認済み、いずれも頑健な検出ではない"
    )
    tf2.paragraphs[6].runs[0].text = (
        "・低エネルギー(<4.3 GeV)は強い負の有意度(最大-15.2σ) — GALPROPガス成分不確かさに由来と推定(Discussion参照)"
    )
    tf2.paragraphs[8].runs[0].text = "→ 全体として理想的なDMスペクトル形状(低高E→0、中間でピーク)とは一致しない"

    # ------------------------------------------------------------------
    # slide105 (0-idx 104): MCMC本体スライド
    # ------------------------------------------------------------------
    sl = prs.slides[104]
    sh = by_text(sl.shapes, "Bin6(20.76GeV)現行値")
    sh.text_frame.paragraphs[0].runs[0].text = (
        "Bin6(20.76GeV)現行値: f_gal=0.69, f_halo=0.66, 見かけの有意度4.83σ(2026-07-13、"
        "フェルミバブル正負2テンプレート化+多点始動30回化 最終版)。"
        "領域分割頑健性検証済み(バブル領域内1.6σ・高緯度域8.9σ、符号不一致)"
    )

    prs.save(str(PPT_PATH))
    print("保存完了:", PPT_PATH)


if __name__ == "__main__":
    main()
