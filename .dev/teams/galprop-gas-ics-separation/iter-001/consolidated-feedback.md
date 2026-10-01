# Consolidated Feedback (iter-001) — 判定: FAIL、iter-002へ差し戻し

## Manager調停

物理レビュア・数値レビュアは独立に同一実装を検証し、共に「採用不可」で一致した。
クロスレビューの結果、**両者の指摘に矛盾はなく、Manager調停を要する対立点は無い**。
むしろ2つの発見は同一病理の表裏であることが確定した:

1. **[物理] f_halo に非負制約が無い** — DMフラックスは物理的に非負(annihilation∝ρ²,
   decay∝ρ、共に≥0)なのに `log_prior` の非負制約が index 6 (`f_halo`) に及んでいない
   (`code/mcmc_fit_all_bins.py:238-249`)。
2. **[数値] `_multistart_minimize` の `np.abs(start)` が符号自由パラメータの再始動探索を
   正領域に限定してしまう** (`:288-289`)。

cross-physical-on-numerical.md の指摘が核心を突いている: **この2つの穴は「同じ負領域」を
指している**。f_halo を符号自由にしたことで縮退方向(ICS↔halo, r=0.747)の相殺解が
禁制の負領域(f_halo≈-170)に存在するようになったが、np.abs()バグにより restart は
その領域を一切探索できない。→ **どちらか一方だけ直しても不十分。同時に直す必要がある**。

さらに物理レビュア(P-3, cross-physical-on-numerical.md)は重要な構造的指摘をしている:
**μ は f について線形(アフィン)なので、Poisson NLL は f に関して凸関数である**。
全 fᵢ≥0 の制約下では凸最適化問題(有界凸計画)になり、大域最適解は一意。
「Nelder-Mead の局所解」に見えていた不安定性は、真の多峰性ではなく境界近傍の
ill-conditioningをNelder-Mead(勾配を使わない)が捌けていないだけの可能性が高い。
→ 数値レビュアが提案していた「(b) 勾配情報を使う手法(L-BFGS-B)への切り替え」を、
物理側の凸性の議論が裏付けている。

cross-numerical-on-physical.md はさらに重要な**修正順序**を指摘している:
物理修正(f_halo≥0)だけでは、**正のMLEが出るビン(Bin6等)の有意度水増しは解消しない**
(no-halo側6D最適化の未収束はf_halo制約と無関係に残るため)。従って:

**修正順序: (1) np.abs()バグ撤廃 + 最適化手法の見直し(凸性を活かす) → (2) f_halo≥0制約
→ (3) 全13ビン再実行・restart/seed非依存性の確認、の順で行うこと。逆順は手戻りになる。**

## iter-002 で必ず修正すること (CRITICAL、優先順)

1. **最適化手法の刷新**: `_multistart_minimize`(Nelder-Mead多点始動)を、
   `scipy.optimize.minimize(method="L-BFGS-B", bounds=...)` 等の勾配ベース有界凸最適化に
   置き換える(with-halo・no-haloモデル両方)。bounds は非負パラメータに `(0, None)`、
   符号自由パラメータ(`f_fb_neg`のみ)に `(None, None)` を設定する。
   凸性の検証として、複数の異なる初期値から実行し、目的関数値が高精度で一致することを
   確認すること(これが「restartプラトー確認」の代替になる)。
2. **f_halo の非負制約追加**: `log_prior`・`fit_one_bin` の非負インデックス集合を
   `[0,1,2,3,4]`(f_gas,f_ics,f_loopI_a,f_loopI_b,f_fb)から`[0,1,2,3,4,6]`(f_haloを追加)に
   変更する。符号自由は index 5 (`f_fb_neg`) のみに限定する。
3. **有意度計算の確認**: 数値レビュアのクロスレビューにより、`sig=sqrt(2·max(ΔlnL,0))`
   という境界補正済みの式は既に `fit_one_bin:334-339` に実装されていることが判明している
   (新規分岐は不要)。上記1,2を適用すれば、境界MLE(f_halo=0)のビンで自動的にΔlnL=0→sig=0に
   なることを確認するだけでよい。
4. **emcee再現性**: `main()` 冒頭に `np.random.seed(N)` を設定し、`EnsembleSampler`にもseedを
   渡す(数値レビュー I-1)。
5. **チェイン長の妥当性確認**: autocorrelation time τ に対し post-burn チェイン長が
   十分か(emcee推奨 ≥50τ)を全13ビンで確認し、不足していれば `n_steps` を増やす
   (数値レビュー I-2。ただし優先度は1-4より低い、cross-physical-on-numericalのR-2参照)。

## iter-002 で保留してよいこと(cross-reviewで「優先度低」と判定)

- f_gas/f_ics への物理事前分布(Gaussian/log-normal, 1.0中心)の追加(物理I-1後半)は、
  上記1-4を適用した後の残存有意度を見てから判断する。Totani (2025)・比較対象論文
  arXiv:2607.08552との手法整合性を崩すリスクがあるため(cross-physical-on-numerical P-5)、
  安易に追加しない。
- NFW校正基準の緯度不一致(物理S-2)は今回のスコープ外、既存の懸念として記録のみ。

## 次のステップ

Implementerへ差し戻し、上記1-4(5は時間が許せば)を実装した上で全13ビン再フィット+
ROI分割再検証(Bin5・Bin6)を再実行する。**符号反転が今度こそ解消するか、あるいは
解消しない場合はそれ自体を正直に報告すること**(前回同様、結論を誘導しない)。
