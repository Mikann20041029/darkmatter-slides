# Numerical Review (iter 001)

## 総合判断: **この結果は採用不可。数値的収束不良(既知バグの再発)が確定的。再修正が必要。**

有意度・f_halo が `n_restarts` と乱数 seed に対して**桁レベルで不安定**であることを再実行で定量確認した。
`_multistart_minimize` の docstring 自身が警告している「no-halo 側の局所解はまり込みが有意度を水増しする」
バグ(2026-07-12/13 に Bin3/Bin7 で発見・修正済み)が、6→7 次元拡大により**再発**している。
`halo_spectrum.json` の全有意度は over-converge していない no-halo フィットに由来する**過大評価アーティファクト**。

検証コード・結果(再現用、全て `results/mcmc_allbins_gasICS_v1/` に保存):
- `restart_scan_check.json` — Bin1/Bin6 の n_restarts∈{30,50,100}・seed∈{0,1,2,3} スキャン
- `emcee_convergence_check.json` — autocorr time・walker 間分散・受容率
- `gas_ics_correlation.json` — gas/ICS テンプレート相関(全13ビン)
- スクリプト: scratchpad `refit_check.py`, `emcee_check.py`, `corr_check.py`
- 環境: `/tmp/darkmatter_venv` Python 3.12, numpy 2.5.1, emcee 3.1.6, scipy 1.18.0, seed 明示

---

## 🔴 CRITICAL (数値結果が信頼できない)

- **[C-1] 有意度が n_restarts で未収束。既知の「no-halo 局所解 → 有意度水増し」バグの再発**
  (`mcmc_fit_all_bins.py:266-295 _multistart_minimize`, `:316-339 fit_one_bin`)
  `significance = sqrt(2·(lnL_with − lnL_nohalo))` は 2 本の独立最適化の**差**に依存する。
  no-halo 側が収束不足だと lnL_nohalo が過小になり ΔlnL が水増しされる。実測:
  - **Bin1**: ΔlnL = 4076 (n=30) → 2593 (n=50) → 750 (n=100)、有意度 90.3σ → 72.0σ → 38.7σ。
    lnL_nohalo が 8308936 → 8310460 → 8312299 と**単調改善し続けており、n=100 でもまだ収束していない**
    (プラトーに達していない)。つまり真の有意度は 38.7σ よりさらに低い可能性が高い。
  - **Bin6**: 有意度 18.70σ (n=30) → 17.57σ (n=100)。lnL_nohalo が 25579.85 → 25600.43 と改善。
    f_halo=2.53 自体は安定だが**有意度は依然として ±数σ の数値ノイズを持つ**。
  - seed 依存(n_restarts=30 固定): Bin1 有意度 = 32.6σ(seed1)/32.0σ(seed2)/**17.9σ(seed3)**、
    Bin6 = 17.2σ/17.6σ/**25.4σ(seed3, 悪い no-halo 解を引いて水増し)**。
  → `_multistart_minimize` docstring (`:273-279`) が明記する再発条件そのもの。spec 指示で n_restarts=30 据置きだが、
    **7 次元では全く不足**。推奨修正: (a) no-halo 最適化を収束するまで restart を増やす(Bin1 は n=100 でも未収束
    なので、ΔlnL が restart 数に対してプラトーに達したことを**各ビンで検証してから**採用する)、
    (b) Nelder-Mead ではなく勾配情報を使う手法 (L-BFGS-B。`subtract_galactic_diffuse` では既に使用) か、
    Poisson-GLM の解析的初期値からの局所最適に切り替える。

- **[C-2] Bin1 の f_halo=−173.6 は「真のグローバル最適解」ではなく識別不能方向 + 収束失敗の産物**
  (Q4 への回答)。点推定 f_halo は seed/restart で **−0.11, −17.7, −171.6, −216.2** と約 2000 倍のレンジで振れる。
  最適化点推定(n=30,seed0 で −17.7)と保存済み事後分布中央値(−173.6, 区間[−189,−154])が **10 倍乖離**。
  emcee は初期値近傍の局所ベイスンを狭く探索している(`emcee_convergence_check.json`: Bin1 の f_halo
  walker 間 std=5.8 ≪ 最適化点推定の振れ幅)ため、事後区間 [−189,−154] の狭さは**見かけ上の精度**にすぎず、
  真の尤度は f_halo 方向にほぼ平坦・縮退している。**f_halo=−173.6 は有効数字ゼロ**(1 桁も信頼できない)。
  非物理値(NFW ハローの負値・校正 norm の 173 倍)を「測定」と解釈してはならない。

---

## 🟡 IMPORTANT (再現性・精度に懸念)

- **[I-1] emcee 事後分布の非再現性**(`mcmc_fit_all_bins.py:342`)。`main()` は `np.random.seed` を
  一度も設定せず、walker 初期化 `pos = best + 1e-3·… · np.random.randn(...)` と emcee 内部 RNG が
  グローバル状態依存。`_multistart_minimize` の点推定(seed=0)は再現するが、**保存済み JSON の median/
  lo16/hi84 は実行ごとに変わる**。SOUL.md「乱数シード併記」違反。修正: `main()` 冒頭で `np.random.seed(N)`
  を設定し、`EnsembleSampler` にも seed を渡す。

- **[I-2] emcee チェイン長が autocorr time 基準で不足気味**(`fit_one_bin:341` n_steps=1500, n_burn=400)。
  実測 tau ≈ 53〜102 steps(loop 系で最長)。post-burn 1100 steps は **tau の約 11〜20 倍**にとどまり、
  emcee 推奨(≥50·tau)を下回る(`get_autocorr_time` は tol=0 を渡さないと例外を投げる状態)。
  burn-in 400 steps も tau の約 4 倍で境界的。中央値は概ね出るが尾部(16/84 %ile)の精度に影響。
  推奨: n_steps を tau ベース(例 ≥5000)に、収束判定を tau 監視で自動化。

- **[I-3] `_multistart_minimize` の restart サンプリングが符号自由方向を探索しない**
  (`mcmc_fit_all_bins.py:288-289`)。`start = x0·(1+U(−1,3)) + scale·N(0,1)` 後に `start = np.abs(start)` で
  **全座標を強制的に正**にしている。f_fb_neg・f_halo は符号自由なのに、restart 初期点は常に正値のみ。
  Bin1 の最適解が f_halo≈−170 なので、restart は負領域を一切カバーせず、Nelder-Mead の谷下り任せ。
  これが C-1/C-2 の不安定性の機構的原因。さらに乗法散布 `x0·(1+U(−1,3))` は x0 に強く錨づけされ、
  x0=0.5 から −170 まで離れた最適解の探索に不向き。修正: 符号自由パラメータは `abs` を適用せず、
  加法的に広く散布する(例 `start[sign_free] = rng.normal(0, scale_broad)`)。

- **[I-4] prior 上限 |f_halo|≤1e6 が広すぎ、縮退の受け皿になっている**(`log_prior:247`)。
  gas/ICS の空間相関は r≈0.70(`gas_ics_correlation.json`、全ビンで 0.69〜0.71、エネルギー依存ほぼ無し)で
  **それ自体は致命的縮退ではない**が、符号自由・上限 1e6 の halo テンプレートが gas/ICS/bubble の
  モデル残差を吸収できてしまう。低エネルギー(2.28M events の Bin1)ほどモデル誤差の絶対量が大きく、
  halo が巨大負値に暴走する。推奨: f_halo に物理的境界(例 J-factor 校正 norm の数倍程度)を課すか、
  そもそも「有意度」を Wilks 近似ではなく縮退を考慮した profile likelihood / 事後で評価する。

---

## 🟢 SUGGEST (改善余地)

- **[S-1] 有意度指標 `sqrt(2·ΔlnL)` の解釈上の限界**。Bin1 は 2.28M events あり、per-pixel Poisson で
  iso 固定・剛直テンプレートを使う限りモデル誤設定が不可避。統計量が巨大でも「信号検出」ではなく
  「適合度不足」を測っている。収束を直しても大有意度が残る場合、これは物理的信号ではなく系統誤差の
  可能性が高い(物理レビュアと要相談)。
- **[S-2] dtype は良好**。`_load_healpix_grid_template` で `np.float64` 明示、shape 注釈あり。
  make_mu/log_likelihood に暗黙昇格や float32 混入は見当たらない。
- **[S-3] `build_templates_for_bin` のキーワード専用化(spec 外変更)は数値観点では妥当**。
  引数ズレによる silent 破損を TypeError 化する安全策で、数値精度への悪影響なし。

---

## ✓ 通過した検証

- テンプレート健全性: gas/ICS とも全13ビンで NaN=0・負値=0(`gas_ics_correlation.json` で再確認)。
- gas/ICS 相関は r≈0.70 で線形従属ではない(縮退度は中程度)。gas/ICS 分離自体が破綻の主因ではない。
- Bin6 の f_halo=2.53 は seed/restart に対して**点推定は安定**(有意度のみ未収束)。
- emcee 受容率 0.42〜0.43 は健全(過小・過大でない)。

---

## Manager への要点

1. **採用不可**。`halo_spectrum.json` の有意度は no-halo フィット収束不足による過大評価。
   spec 合格条件「局所解バグの再発がないことを n_restarts=30 で確認」は**満たされていない**(再発を確認)。
2. 最小修正: (a) no-halo/with-halo 両最適化を ΔlnL が restart 数でプラトーに達するまで収束させる
   (各ビンで検証を義務化)、(b) restart の `np.abs` 強制正値化を符号自由パラメータで撤廃、
   (c) emcee に seed 設定 + tau ベースのチェイン長。
3. Bin1 の f_halo=−173.6 は物理値として報告してはならない(識別不能)。
