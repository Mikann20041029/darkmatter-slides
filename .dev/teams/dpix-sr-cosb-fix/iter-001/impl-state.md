# Implementer State (iter 001) — DPIX_SR cos(b) 立体角補正

## 結論(先頭)

cos(b) 欠落バグを4ファイルで修正した。修正は物理的に正しく、数値健全性も保たれる。
ただし**当初仮説(cos(b)バグが非物理的高有意度の一因)は逆方向だった**: cos(b) を
入れると全13ビンで有意度は**上昇**する(低下しない)。一方、領域A/C の f_halo 空間
不整合は**大幅に減少**し、球対称ハロー解釈との整合はむしろ改善した。

## 変更ファイル

- `code/mcmc_fit_all_bins.py`: スカラー `DPIX_SR` を緯度依存配列 `PIX_SOLID_ANGLE_SR = (π/180)²·cos(b)` に改名・変更(定義は `BG` 定義直後へ移動)。`calibrate_nfw_norm` は参照ピクセルのスカラー値 `dpix_ref` を分子分母双方に使い約分を厳密化。`build_templates_for_bin` の gas/ics/halo 3テンプレートに配列を適用。再現性スタンプ関数 `env_stamp()` を追加し summary JSON に埋め込み。出力先を環境変数 `MCMC_ALLBINS_OUTDIR` で切替可能化(既定は従来 v1、後方互換)。
- `code/mcmc_fit.py`: Bin6専用旧スクリプト。`build_templates()` 内の局所 `DPIX_SR` を `PIX_SOLID_ANGLE_SR = (π/180)²·cos(BG)` 配列に同期(`E_EFF` 定数はそのまま)。
- `code/mcmc_fit_all_bins_galprop_webrun_check.py`: 却下済み比較用。モジュール先頭のスカラー `DPIX_SR` を削除し、`BG` 定義後に配列 `PIX_SOLID_ANGLE_SR` を定義。`calibrate_nfw_norm`/`build_templates_for_bin` を同期。`from numpy.typing import NDArray` を追加。
- `code/mcmc_fit_all_bins_galprop_webrun_v2.py`: `mfa.DPIX_SR` 参照3箇所を `mfa.PIX_SOLID_ANGLE_SR` に追従(#1修正が自動反映される構造だが改名のため明示追従)。
- `code/diagnose_regionAC_lrt_all_bins.py`: 出力先を argv[1] / 環境変数 `REGIONAC_LRT_OUTDIR` で切替可能化(既定は従来 v1)。summary に `env_stamp()` を追加。テンプレート・尤度は `mfa.*` 経由で cos(b) 修正を自動反映(ロジック不変)。
- `code/check_dpix_cosb_health.py`: 新規。数値健全性チェック(物理極限・対称性・次元整合 + Bin6 解析勾配 vs 有限差分 + fun_spread)。結果を `results/mcmc_allbins_gasICS_v2_cosb/health_check.json` に保存。

## 主要決定

- 変数改名 `DPIX_SR → PIX_SOLID_ANGLE_SR`(採用): 「もう定数でない」ことを明示。却下案=名前維持のまま配列化(スカラーを想起させ誤読リスク)。全参照(mfa.DPIX_SR含む4ファイル)を grep 確認のうえ追従。
- 校正の約分保証(採用): `calibrate_nfw_norm` で参照ピクセル `(ib_ref,jb_ref)` の**スカラー値** `dpix_ref` を分子分母双方に使用。これにより `norm = flux/j_ref` へ厳密に約分され、nfw_norm は修正前後で不変(数学的に確認)。却下案=配列のまま演算(分子分母で異形状ブロードキャストの誤りリスク)。
- 出力先を上書きせず環境変数で切替(採用): `mcmc_fit_all_bins.py` の `OUT_DIR` はハードコードで v1 を指す。そのまま実行すると v1 headline を上書きするため環境変数化。既存 v1 結果は保全。

## 明示した assumption / approximation

- cos(b) は物理フラックス→counts 変換を伴う gas/ics/halo にのみ掛かる。iso(データ由来 count 密度)・loopI(幾何モデル)・fb/fb_neg(データ残差×露出比)は既に count 空間なので cos(b) は掛けない。この非対称性が緯度依存でテンプレート相対比を変え、フィット結果を動かす。
- 勾配コード `neg_log_likelihood_and_grad` はテンプレート配列 `t[...]` のみを参照し `PIX_SOLID_ANGLE_SR` を直接参照しないことを確認済み(spec の前提を満たす。修正不要)。
- NFW J-factor 視線積分 `nfw_j_map()` はこの立体角バグと独立(未修正、spec 通り)。
- 有意度 `significance_sigma = √(2ΔlnL)` は L-BFGS-B 点推定由来で決定論的(MCMC 乱数に非依存)。f_halo 中央値・信頼区間のみ MCMC 依存。

## 数値健全性チェック結果(`health_check.json`)

物理(`PIX_SOLID_ANGLE_SR`):
- b≈0 極限: 比 = 0.99996(= cos(0.5°)、最近傍セルが b=±0.5°。旧スカラーと一致)
- b≈60 セル: 比 = 0.5075(= cos(59.5°)、最近傍セル。理論 cos(60°)=0.5)
- b→−b 対称性: 最大絶対誤差 = 0.00e+00(cos は偶関数、厳密一致)
- 次元整合: ROI(|b|∈[10,60])総立体角 数値=2.900 sr vs 解析積分 2.900 sr、相対誤差 ~0(midpoint則)。旧スカラーは 3.655 sr(全体で約1.26倍過大、緯度依存でさらに偏る)

数値(Bin6):
- 解析勾配 vs 有限差分: x0 点で max 相対誤差 8.6e-8(優)。最適点では勾配≈0 のため絶対誤差 1.8e-4(分母1で相対化した見かけ値、勾配ゼロ近傍の有限差分ノイズ由来で正常)
- fun_spread: no-halo 3.6e-12 / with-halo 1.1e-11(修正前と同水準、悪化なし)
- 全13ビン: fun_spread は Bin1-12 で ≤2e-10(良好)。Bin13 with-halo のみ 3744(f_halo≈0 の平坦方向由来。v1 も 3779 で**既存の性質**、cos(b)修正による退行ではない)。max_fun_spread: v1=3779.6 → v2=3744.0(同水準)
- ΔlnL≥0(no-halo⊂with-halo 入れ子制約)は全13ビンで成立

## ヘッドライン結果の変化

### Bin6(最優先)

| 量 | 修正前 v1 | 修正後 v2_cosb | 差 |
| --- | --- | --- | --- |
| f_halo(中央値) | 3.675 | 4.496 | +0.82 |
| 有意度 | 25.45σ | 28.10σ | +2.66σ |

### 全13ビンの傾向

cos(b)修正で**全ビンの有意度が上昇**した(低下したビンは無い)。増加幅は低エネルギー側で最大:

| Bin | E[GeV] | sig v1 | sig v2 | Δsig |
| --- | --- | --- | --- | --- |
| 1 | 1.51 | 0.00 | 16.45 | **+16.45** |
| 2 | 2.55 | 12.86 | 26.29 | +13.43 |
| 3 | 4.31 | 20.73 | 30.23 | +9.50 |
| 4 | 7.28 | 28.50 | 34.59 | +6.09 |
| 5 | 12.29 | 27.94 | 31.97 | +4.03 |
| 6 | 20.76 | 25.45 | 28.10 | +2.66 |
| 7 | 35.06 | 18.99 | 20.85 | +1.86 |
| 8-13 | 59-814 | (14.4→0.48) | (15.5→0.52) | +1.1〜+0.04 |

スペクトルの形: f_halo は全ビンで増加。ピーク有意度ビンは Bin4(7.28 GeV, 34.59σ)で不変だが、低エネルギー側(Bin1-3)の跳ね上がりが顕著で、修正後スペクトルは低エネルギー側がより持ち上がった形になる。**修正後の最大有意度は 34.59σ(Bin4)で、Totani(2025)報告の 13-19σ をさらに大きく上回る**。したがって cos(b) バグは高有意度問題の原因ではなく、修正するとむしろ乖離が拡大する。

### 領域A/C LRT検定の変化

cos(b)修正で**領域A(バブル内・低〜中緯度)と領域C(バブル外・高緯度)の f_halo が大幅に整合**し、A/C不整合の等価有意度が激減した(球対称ハロー仮説への反証が弱まった):

| Bin | f_halo_A/C v1 | eqSig v1 | f_halo_A/C v2 | eqSig v2 |
| --- | --- | --- | --- | --- |
| 3 | 46.2 / 10.3 | 4.21σ | 26.5 / 55.7 | 2.74σ |
| 4 | 24.7 / 6.08 | 5.40σ | 21.5 / 22.5 | **0.24σ** |
| 5 | 8.65 / 4.26 | 3.13σ | 7.94 / 9.23 | 0.74σ |
| 6 | 3.26 / 1.73 | 2.76σ | 3.20 / 3.25 | **0.07σ** |
| 7 | 1.14 / 0.214 | 4.15σ | 1.20 / 0.555 | 2.34σ |

物理的解釈(数値のみ、断定は避ける): 緯度依存の cos(b) バグが領域A(低緯度側)と領域C(高緯度側)の f_halo を非対称に歪めていたため、修正で両領域の振幅が一致に近づいた。Bin4/5/6 で A/C 不整合がほぼ消滅した(≤0.74σ)。ΔlnL≥0 は全13ビンで成立。LRT収束: 10/13ビンで fun_spread<1e-6(未収束は Bin1/12/13、いずれも f_halo≈0 かバブル支配で eqSig≤3.31、v1 同様の平坦方向由来)。

## 既知の懸念(レビュアに見てほしい点)

- **仮説の反証**: 「cos(b)バグが非物理的高有意度の一因」という当初仮説は否定された(有意度は上昇)。この修正は Totani 再現には寄与せず、乖離を拡大する。ただし修正自体は物理的に必須。高有意度の真因は別(GALPROP テンプレートと柔軟テンプレートの縮退等、`galprop-gas-ics-separation/verdict.md` 参照)に残る。
- **b60比が 0.5075**(0.5でない): グリッドセル中心が最大 |b|=59.5° のため。厳密に |b|=60° のセルは存在しない(1°刻みグリッドの離散化)。物理的に正しい。
- **50τ充足 0/13**: MCMC チェイン長が全ビンで 50τ 未満(v1 と同一、既存の性質)。有意度は点推定由来で影響なし。信頼区間(f_halo lo16/hi84)のみ「参考値」。cos(b)修正とは独立の未解決点。
- **Bin13 fun_spread=3744**: f_halo≈0 の平坦方向由来(v1=3779 と同水準、既存)。Bin13 は 0.52σ で物理的に無関係。
- `check_dpix_cosb_health.py` は cwd=リポジトリルート前提(`sys.path.insert(0, "code")`)。他所から実行する場合は要調整。

## 再現性

- git commit: `f1d158c`(working tree dirty=True、本修正が未コミットのため)
- seed: `np.random.seed(42)`(mfa.SEED)
- python 3.12.3 / numpy 2.5.1 / scipy 1.18.0 / emcee 3.1.6(venv `/tmp/darkmatter_venv`)
- 実行: `MCMC_ALLBINS_OUTDIR=$PWD/results/mcmc_allbins_gasICS_v2_cosb python3 code/mcmc_fit_all_bins.py`、`python3 code/diagnose_regionAC_lrt_all_bins.py $PWD/results/mcmc_allbins_gasICS_v2_cosb`
- 出力: `results/mcmc_allbins_gasICS_v2_cosb/`(mcmc_bin01-13.json, halo_spectrum.json/png, regionAC_lrt_all_bins.json/log, health_check.json, run_allbins.log)。既存 `results/mcmc_allbins_gasICS_v1/` は不変。
