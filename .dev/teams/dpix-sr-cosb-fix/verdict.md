# Verdict — DPIX_SR cos(b) 立体角補正修正タスク

Tier: M。iter数: 1(PASS)。物理・数値の一次レビュー、クロスレビュー2本とも完了。
Tier昇格・降格なし。

## 発端

ユーザーが前回セッションの記憶(「有意度がTotani再現に使えないほど狂っていた」)を確認した際、
Managerがコードを読んで`code/mcmc_fit_all_bins.py:125`の`DPIX_SR = (π/180)²`が緯度によらない
定数として扱われており、真の(l,b)グリッド上のピクセル立体角`ΔΩ(b)=Δl・Δb・cos(b)`を反映して
いないことを発見した(既存の物理・数値レビューは「次元(単位がsr)」の確認はしていたが
「グリッド全域で数値が正しいか」は未検証だった)。ユーザーの明示的な依頼により本修正タスクを
M tierで起動した。

## 最終結論

**cos(b)補正の実装は物理的・数値的に正しいと確認した(PASS)。ただし当初の仮説
(このバグが非物理的高有意度の原因)は反証された。** 修正後は全13ビンで有意度が上昇し、
Totani(2025)報告値(13-19σ)との乖離はむしろ拡大した(Bin6: 25.45σ→28.10σ、最大はBin4の34.59σ)。

**一方、2つの重要な副産物が得られた**:

1. 前回チーム(`regionAC-lrt-halo-test`)が「球対称ハロー仮説と矛盾する独立証拠」とした
   領域A/C空間不整合の大部分(Bin4/Bin6等)は、本cos(b)バグに起因する数値的アーティファクト
   だったと判明した。物理的機構(領域Cは高緯度寄りで旧バグの影響を強く受ける)で定量的に
   説明可能であり、前回verdictの該当箇所は見直しが必要。
2. cos(b)修正前後のf_gas/f_ics/f_halo変化パターンから、ICS-halo間の強い縮退
   (`galprop-gas-ics-separation/iter-004`が既に発見した「ICS-halo悪性縮退」)の**独立した
   第2の証拠**が得られた。2つの異なる手法が同じ結論に到達しており、この問題への対応の
   優先度が上がった。

## 成果物

- コード: `code/mcmc_fit_all_bins.py`(本番)、`code/mcmc_fit.py`、
  `code/mcmc_fit_all_bins_galprop_webrun_check.py`、`code/mcmc_fit_all_bins_galprop_webrun_v2.py`、
  `code/diagnose_regionAC_lrt_all_bins.py`、`code/check_dpix_cosb_health.py`(新規)
- 結果: `results/mcmc_allbins_gasICS_v2_cosb/`(v1は不変・保全)
- 全記録: `.dev/teams/dpix-sr-cosb-fix/`(spec, iter-001の impl-state/review-physical/
  review-numerical/cross-physical-on-numerical/cross-numerical-on-physical/consolidated-feedback)

## 残課題(次の一手、ユーザー判断待ち)

1. `code/mcmc_fit.py`のhalo項未実装(立体角補正の経路がそもそも存在しない)の修正
2. Loop Iテンプレートのコメント修正(実害なし、ドキュメンテーションのみ)
3. Bin1-6の識別可能性低下(region応答反転・cos(b)感度異常)を結果ファイルに注記
4. MCMC事後分布のf_ics-f_halo相関係数の追加報告
5. `regionAC-lrt-halo-test/verdict.md`の結論見直し(A/C不整合はcos(b)バグ由来と判明した旨を反映)
6. ICS-halo縮退問題への本格対応(教授提供ISRFデータでのGALPROP再計算、または正則化モデルの検討)

## 未コミット

本タスクの全変更(コード6ファイル・結果ディレクトリ・.dev/teams/配下)はまだgit未コミット。
ユーザーの承認を得てからコミットする。
