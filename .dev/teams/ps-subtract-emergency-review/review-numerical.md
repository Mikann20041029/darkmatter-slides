# Numerical Review (emergency, Bin6 PS-subtract check)

## 結論

`code/diagnose_ps_subtract_check.py` に **実装ミス（インデックス誤り・符号ミス・valid/counts の取り違え等）は見つからなかった**。`subtract_point_sources_corrected()` は `plot_skymap_all_subtracted.subtract_point_sources()` とロジックが完全に一致しており（差分は `_PS_EXPOSURE` 定数 → `expmap[il,ib]` への置換と `exp_here<=0` ガード追加のみ）、`refit_bin()` の `valid`/`counts` の対応付けも壊れていない。(A) を本スクリプトで独立に再計算した結果、`lnL_no_halo`・`lnL_with_halo`・`delta_lnL`・`significance_sigma` は `results/mcmc_allbins_gasICS_v1/mcmc_bin06.json` の値と**完全一致**（25.445982812314362σ、桁レベルで同一）しており、テンプレート共有・マスク処理に破損がないことを裏付ける。

しかし、**「補正版」自体に統計的に無視できない欠陥が1つある（CRITICAL）**: `subtract_point_sources_corrected()` が生成する `counts_sub` は Bin6 で **127/12000 ピクセル（1.06%）が負値**（最悪 -114.8）になっており、これがそのまま Poisson 尤度 `counts[valid]*log(mu)-mu` に投入されている。25.45σ→26.66σ という有意度上昇は、(A)と(B)で有効ピクセル数が違う（点源ピクセルをマスクで捨てるか、含めるか）という設計上の差から大部分は説明できる自然な変化幅だが、上記の負カウント問題が(B)側の `f_gas/f_ics/f_halo` を歪めている可能性があり、**「26.66σが本当に物理的に正しい値か」は現状の実装のままでは判定できない**。バグではなく統計モデルの前提破れ（Poisson データが負になってはいけない）である。

以下、詳細。

---

## 🔴 CRITICAL

- **[`code/diagnose_ps_subtract_check.py:82` / `code/plot_skymap_all_subtracted.py:457`] 点源差し引き後のカウントが負値になり、そのままPoisson尤度に投入されている。**
  実測: Bin6で `subtract_point_sources_corrected()` を実行すると、有効ピクセル12000枚中 **127枚(1.06%)が負**、最悪値は `l=21.5°, b=43.5°` で `counts=296` に対し予測期待カウント `n_expect=410.8`（実測露出 `expmap=5.56e11 cm²·s` 使用）となり `counts_sub=-114.79`。負の合計デフィシットは `Σ counts_sub[counts_sub<0] = -330.5` カウント。
  原因は主にカタログ源467（LogParabola, pivot=3.698 GeV, α=1.580, β=0.0951）を pivot から **E/E0 = 4.15〜7.59倍**（=対数比 1.42〜2.03）も離れたBin6（15.35–28.07 GeV）へ外挿していること。LogParabolaモデルは pivot 近傍でのみ検証された形状であり、この程度の外挿は系統的過大評価を生みやすい。**旧定数版**(`_PS_EXPOSURE=1.24e11`)でも同じ源で `n_expect_old ≈ 91.6`（`< counts=296`のため負にならず問題が隠れていた）。今回、実測露出(平均4.68倍)へ切り替えたことでこの既存の外挿誤差が可視化され、Poissonモデルの前提（`counts>=0`）を破る値が生じた。
  `subtract_point_sources_corrected()`にも元の`subtract_point_sources()`にも負値のクリップ/ガードは存在せず、`refit_bin()`→`mfa.fit_one_bin()`→`neg_log_likelihood_and_grad()`は`counts[valid]`を無条件に使う。`c<0`のとき `dNLL/dmu = 1 - c/mu = 1+|c|/mu > 0` (常に正)となり、最適化はそのピクセルでの`mu`を可能な限り下げようとする（＝そのピクセルの`gas/ics/halo`等のテンプレート値を通じて他ピクセルの推定を歪める）。この歪みが(B)のf_gas/f_ics/f_halo(=1.377/0.549/3.480)にどれだけ寄与しているか定量化されていない。
  **なお、この「差し引き後に負値が出る」こと自体は本コードベースで前例がある**: `plot_skymap_all_subtracted.py:628-632`の`plot_bin()`は`counts_sub<=0`を可視化上マスクしている(`disp[disp<=0]=np.nan`)。つまり負値の発生は既知の現象だが、**尤度計算側には対応する処理が一切実装されていない**。
  **推奨修正**（いずれか、または併用）:
  1. 最小限: `counts_sub = np.maximum(counts_sub, 0.0)` でクリップし、クリップされたピクセル数・合計量をJSON等に記録する（Poissonデータとしての妥当性を回復。ただし物理的には「その源のフラックスモデルが信用できない」ことの隠蔽にもなるため要注意）。
  2. より正確: 過大外挿を起こす源（`|E_grid/E0|`が例えば3倍を超える等、pivotから著しく離れたビン）はその源だけNaNマスクにフォールバックする(A)方式とのハイブリッド。
  3. 根本対処: LogParabola/PLSuperExpCutoffのモデル外挿を pivot からの許容範囲でバリデートし、範囲外は打ち切るか保守的なベキ乗則へフォールバックする。
  いずれにせよ、**現状のB結果(f_halo=+3.48, sig=26.66σ)は「クリップなしの負データ入りPoisson尤度」で得られた数値であり、この修正なしにheadline候補として採用すべきではない。**

## 🟡 IMPORTANT

- **[`code/diagnose_ps_subtract_check.py:88-103`, `:147`] (A)と(B)のMCMC中央値比較にRNGストリーム順序の交絡がある。** `main()`は`np.random.seed(mfa.SEED)`を一度だけ実行し、(A)→(B)の順に同一グローバルRNGストリームを消費する(`run_mcmc_with_autocorr_check`内のwalker初期化`np.random.randn(...)`)。有意度(`significance_sigma`)はMLE(`res.x`, L-BFGS-B, 決定的)由来なのでRNGに依存しないが、報告されている`f_gas/f_ics/f_halo`の中央値はMCMC事後分布(`np.median(flat,...)`)由来でありRNG位置に依存する。
  検証: 本レビューで(A)を独立に再実行し、`lnL_no_halo/lnL_with_halo/delta_lnL/significance_sigma`は`mcmc_bin06.json`と完全一致した一方、MCMC中央値は `f_gas: 1.4186(本スクリプト) vs 1.41766(headline)`、`f_ics: 0.6041 vs 0.60209`、`f_halo: 3.6638 vs 3.674862` と最大0.34%ずれる(headlineは13ビン通し実行でBin6到達時点までにRNGが5ビン分消費されているため)。
  この量(<0.4%)は(A)→(B)間の実効果(f_gas -3.0%, f_ics -9.2%, f_halo -5.0%)より一桁小さく、**定性的結論を覆すものではない**が、有効数字4桁で比較している以上、無視できる保証はない。
  **推奨修正**: `refit_bin()`呼び出し直前に毎回`np.random.seed(mfa.SEED)`を入れ直し、(A)と(B)が同一walker初期化列を共有するようにする。これで比較のノイズ源をRNGから完全に排除できる。

- **[`code/diagnose_ps_subtract_check.py:130-142`] 収束診断(`convexity_check`, `autocorr_check`)がJSONに保存されていない。** `fit_one_bin()`の戻り値には`convexity_check`(5点マルチスタートのfun値ばらつき)と`autocorr_check`(τ, 50τ充足)が含まれるが、`run_for_bin()`は`f_gas/f_ics/f_halo/sig/n_valid_pixels`のみ抽出しており、これらの診断情報は`ps_subtract_check.json`に残らない。
  本レビューで手動再計算した結果: 凸性は両者とも良好(`fun_spread_successful_only`: (A) no-halo 3.6e-12 / with-halo 0.0、(B) no-halo 0.0 / with-halo 7.3e-12 — いずれも収束は健全で局所解へのはまり込みは見られない)。ただし **`meets_50tau_recommendation`は(A)(B)とも`False`**(τ_max: (A)213.7〜(headline実行では287.6), (B)255.8; いずれも`max_n_steps=6000`で頭打ち、必要な post-burn 長 `50τ≈10683〜12791` に対し実際は5600)。これはheadline本体(`mcmc_bin06.json`)も同じ状態(τ_max=287.57, `meets_50tau_recommendation: false`)であり、本スクリプト固有の新規バグではなく**既存の制約の継承**。(A)(B)対称に発生しているため26.66σ>25.45σという方向性を歪めてはいないが、`f_gas=+1.419`のような4桁の有効数字表示は、この収束不足由来の追加誤差(16-84%区間の幅がτ不足でおそらく過小評価)を考慮すると正当化できない。
  **推奨修正**: `run_for_bin()`が`convexity_check`/`autocorr_check`を`ps_subtract_check.json`に含めるよう修正し、比較数値は有効数字2-3桁(例: `f_gas≈1.42 vs 1.38`)に丸めて報告する。

## 🟢 SUGGEST

- **[`code/diagnose_ps_subtract_check.py:35-85`]** 負カウント問題(CRITICAL項目)を将来また見落とさないよう、`subtract_point_sources_corrected()`の戻り値に`n_negative_pixels`・`total_negative_deficit`のような診断値を追加し、`run_for_bin()`経由でJSONに保存することを推奨する。現状は本レビューのような個別のアドホックなPythonスクリプトを書かないと検出できない。
- **[`code/diagnose_ps_subtract_check.py:44`]** `result = counts.copy().astype(float)` は`np.histogram2d`の戻り値が既に`float64`のため実質no-opだが、`.astype(float)`はPythonの`float`エイリアス経由で`np.float64`に解決される。`.dev/SOUL_addon.md`のdtype明示規律に合わせ、`.astype(np.float64)`と明示することを推奨する(数値的な影響はない、可読性のみ)。

## ✓ 通過した検証

- **ロジック同一性**: `subtract_point_sources_corrected()`(diagnose_ps_subtract_check.py:35-85) と `subtract_point_sources()`(plot_skymap_all_subtracted.py:397-460) を1行ずつ突き合わせ、差分は (1) `_PS_EXPOSURE`定数 → `expmap[il,ib]`実測値への置換、(2) `exp_here<=0`ガードの追加、(3) `n_submap`配列(未使用のため省略)のみと確認。カタログ添字(`il`/`ib`)、LogParabola/PLSuperExpCutoff/PowerLawの分岐、台形積分(`np.trapezoid`)は全て一致。符号・添字の取り違えなし。
- **valid/counts の対応付け**: `refit_bin()`は`t=dict(t)`の浅いコピーで`valid`のみ差し替え、共有テンプレート配列(gas/ics/halo等)を(A)(B)間で汚染しない。(A)は`counts`(元の配列)、(B)は`counts_sub`をそれぞれ正しく`mfa.fit_one_bin()`に渡している(実測データで再確認: (A)側`counts.sum()=56533`がheadlineの`n_events=56533`と一致)。
- **validマスクの画素数整合**: `n_valid_a(10625) = n_valid_b(12000) − n_unique_masked_pixels(1375)`が厳密に成立(カタログから独立に計算した「点源が当たる一意ピクセル数」= 1375と一致)。オフバイワン・座標系反転などのインデックスバグがあれば必ずこの等式が崩れるため、強い反証材料になる。
- **(A)のheadline再現性**: 本スクリプトで独立に再計算した(A)の`lnL_no_halo=26320.349613089096`, `lnL_with_halo=26644.098633731395`, `delta_lnL=323.749020642299`, `significance_sigma=25.445982812314362`は、`results/mcmc_allbins_gasICS_v1/mcmc_bin06.json`の値と完全一致(decimal桁まで)。テンプレート受け渡し・x0構築ロジックに破損がないことの強い証拠。
- **有意度上昇の数値的妥当性**: `sig=sqrt(2*ΔlnL)`を手計算で検証: `sqrt(2*323.749020642299)=25.445983`, `sqrt(2*355.29545051306195)=26.656911`、共に報告値と一致。ΔlnL/有効ピクセル数は(A) 0.03047, (B) 0.02961とほぼ同水準であり、σ上昇は主に有効ピクセル数の増加(10625→12000, +13%、点源ピクセルをマスクで捨てずに含めたため)で説明でき、桁が飛ぶような異常な変化ではない。
- **収束診断**: 5点マルチスタートL-BFGS-Bの`fun_spread_successful_only`は(A)(B)とも1e-12〜7e-12オーダーで両者とも良好に単一の大域最適解へ収束しており、いずれかの側だけが局所解に落ちて有意度差を生んだという可能性は排除できる。
- **dtype整合性**: `expmaps`(float64, shape (13,120,120))、`counts`/`counts_sub`(float64)で暗黙のfloat32→float64混在や精度低下は確認されなかった。
- **再現性シード**: `np.random.seed(mfa.SEED=42)`が`main()`冒頭で固定されている点自体は再現性要件を満たす(ただし上記IMPORTANT項目の通り(A)(B)間の相対比較には未対応)。
