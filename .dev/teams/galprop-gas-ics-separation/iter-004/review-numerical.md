# Numerical Review (iter 004)

## 総合判断

**N-1修正(勾配のクリップ整合)は数値的に正しい。有意ビン(1-11)の headline 結果
(有意度・ΔlnL の点推定)は N-1修正の前後で完全に不変(|Δσ| < 1.04e-12,
|ΔΔlnL| < 2.9e-11)であり、数値的に汚染されていない。** Bin12/13 の
ABNORMAL 全滅も解消した(n_failed_starts 5→0)。有意度超過の機構分析
(OLD/NEW 再構築)は健全で、`sig OLD` が iter-003 impl-state と一致し、NEW が
本番バブル関数と `np.allclose` 一致することを確認した。

ただし **N-1修正は「勾配の正しさ」としては完全だが「最適化の robust 性」としては
不完全**である。クリップ(mu 下限 1e-10)は目的関数に高 NLL の平坦プラトー(棚)を
作る非凸化要因であり、修正後の勾配はこの棚で正しくゼロになるため、L-BFGS-B が
そこで `success=True` のまま停止する新しい silent 失敗様式を生む。これが Bin13
with-halo の `fun_spread_successful_only=3779.59` の正体である(下記 I-1)。現状は
`best_res`(min-fun 選択)+ 多始点(5点中4点が棚を回避)で無害化されているが、
根本(クリップの非平滑性)は残存する。

さらに **MCMC 由来の posterior median / 誤差棒は N-1修正前後で最大12%変化して
おり(点推定の不変性とは別)**、「完全に不変」は点推定(σ, ΔlnL)に限定される
(下記 I-2)。

検証コード・結果(scratchpad に保存):
- `verify_grad.py` / `verify_grad.json` — 合成テンプレートでの解析勾配 vs 中心差分
  (クリップ非発火/一部発火/全発火の3レジーム)+ プラトー false-success 再現
- `compare_before_after.py` / `compare_before_after.json` — iter004_before_N1fix vs
  本番の全13ビン点推定・median・convexity 診断突き合わせ
- 環境: `/tmp/darkmatter_venv` Python 3.12.3, numpy/scipy, seed 固定

---

## 🔴 CRITICAL

なし。有意ビン(1-11)の点推定・有意度は N-1修正で汚染されていない(検証済み、下記✓)。

---

## 🟡 IMPORTANT

- **[I-1] クリップの非平滑性が非凸プラトーを作り、L-BFGS-B が `success=True` のまま
  誤収束しうる(Bin13 with-halo で顕在化)。best_res が現状は救済しているが安全網は脆い**
  (`mcmc_fit_all_bins.py:298,368-370`, `mcmc_bin13.json` convexity_check.with_halo)。
  - **切り分け結果: これは「収束判定の閾値問題」ではなく、クリップ由来の非凸性
    (プラトー)である。** クリップ無しなら mu はパラメータについてアフィンで NLL は
    凸(停留点は一意)。唯一の非凸化要因は `mu=max(raw_mu,1e-10)` のクリップだけ
    なので、fun=1014.90 と 4794.49 のように**大域最適から乖離した停留点が
    `success=True` で出現した時点で、それはクリップ棚に由来すると論理的に確定する**
    (他に非凸性の源が無い)。
  - **合成テストで機構を決定的に再現した**(`verify_grad.json` plateau_false_success):
    全画素がクリップ発火する始点から with-halo 最適化を回すと、勾配ノルムが厳密に 0
    (`regime3_full_clip_plateau.grad_norm=0.0`, 400/400 clipped)になり、L-BFGS-B は
    **nit=0・success=True** で fun=552.62(真の最小 88.96、gap=463.66)に張り付いた。
    Bin13 の scale=1.5 が fun=4794.49 で success=True に止まったのと同型。
  - **リスク**: `best_res = min(successful, key=fun)`(`_multistart_minimize:461-462`)は
    「棚でない始点が1つでもある」ことに依存する。現状 Bin12/13 は 5点中4点が棚を回避
    するが、将来のデータ/ビンで**全5始点が棚に落ちれば best_res は棚(高 NLL)を
    採用し、ΔlnL を過小評価した誤った有意度を `success=True` で silent に出す**。
    N-1修正は失敗様式を「ABNORMAL(可視)」から「success=True(不可視)」へ移した側面が
    あり、可視性はむしろ低下した。
  - **推奨(いずれか)**:
    (a) 診断に「best_res で発火したクリップ画素数」と「success 始点間の fun_spread が
       ある閾値(例 1.0)を超えたら WARN」を記録し、棚採用を検知可能にする。
    (b) クリップ下限を尤度計算のみに使い、最適化の始点生成で raw_mu が広範囲に負に
       ならないよう始点を制約する(f_fb_neg のスケール上限など)。
    (c) 棚に落ちた始点を `success=False` 扱いに再分類する後処理(fun が median から
       大きく外れる success 始点を除外)。
  - 現 iter の headline は無害だが、silent 誤収束リスクとして記録必須。

- **[I-2] N-1修正で MCMC posterior median / 16-84% 誤差棒が最大 ~12% 変化した。
  「完全に不変」は点推定(σ, ΔlnL)に限る**
  (`compare_before_after.json`)。
  - 点推定は完全不変: bins1-11 で **max|Δσ|=1.04e-12, max|ΔΔlnL|=2.9e-11**(丸め誤差
    水準)。σ/ΔlnL は決定的な L-BFGS-B 点推定のみから算出され、有意ビンの最適点は
    クリップ非発火領域にあるため N-1修正の影響を受けない。ここは implementer の
    主張どおり。
  - 一方 **MCMC median は Bin6 `f_loopI_a` で 0.0113→0.0127(+12.2%)**、
    f_halo median も Bin8 で +4.7%, Bin11 +1.1%, Bin12 +8.7% 変化した。原因は
    N-1修正で with-halo 最適化の軌跡(前は nfail 1〜4、後は 0)が変わり、MCMC の
    seed 点 `best` が丸め水準(~1e-8〜1e-12)で動いたのが、**post-burn 5600 / τ≈200-375
    (実効独立サンプル ~15-28個)という 50τ 未達の under-converged chain で増幅された**
    ため(既知 iter-002 I-3 の帰結)。RNG ストリーム整列(全ビン n_steps=6000 固定)は
    保たれているので RNG ずれではない。
  - **判断**: headline(σ, f_halo 点推定)は汚染されていない。ただし impl-state の
    「点推定・有意度は完全に不変(全て小数点以下まで一致)」は誤差棒(MCMC median)には
    当てはまらない。halo_spectrum の誤差棒は 50τ 未達も相まって percent 水準で
    再現しない。誤差棒を科学的主張に使うなら 50τ 充足(max_n_steps 引き上げ)が前提。

- **[I-3] ICS 自然性チェックが with-halo=MCMC median と no-halo=L-BFGS-B 点推定という
  異種推定量を混在比較しており、歪み指標に推定量差(median vs MLE)由来のバイアスが
  混入しうる**(`iter004_ics_naturalness_check.json`, `fit_one_bin:580-582`)。
  - `sed_with_halo` は `f_ics` の MCMC median、`sed_no_halo` は点推定を使う。skewed
    posterior では median≠MLE なので、`rms_index_diff=0.843` 等の「halo による歪み」の
    一部が halo の効果ではなく median-MLE 差の artifact になりうる。like-with-like
    (両方 MLE、または両方 median)で比較すべき。物理判断は物理レビュア領域だが、
    推定量の非対称性は数値的な混同要因として記録する。

---

## 🟢 SUGGEST

- **[S-1] Bin10 no-halo の 1/5 始点失敗は無害(best_res 不変)。原因は最適点直上での
  benign な line-search 終了**(`mcmc_bin10.json` convexity_check.no_halo)。
  5始点の fun は全て 5072.7436(12桁一致, `fun_spread_successful_only=0.0`)で、
  失敗した scale=0.6 も**同一の最適点に到達**している。L-BFGS-B が最適点直上で Wolfe
  条件を満たすステップを見つけられず ABNORMAL_TERMINATION_IN_LNSRCH を返した典型で、
  I-1 のクリップ棚(fun が乖離)とは別物。fun が全一致なので棚ではない。best_res は
  min-fun で正しい点を選び、結果は汚染されない。診断の可読性向上のため、
  「fun が median と一致する success=False」を benign と明示注記すると誤解を防げる。

- **[S-2] I-1(a) の WARN 実装は低コストで silent 誤収束リスクを塞ぐ**。
  `_multistart_minimize` の diag に `best_clipped_px_frac` と
  `fun_spread_flag = fun_spread_successful_only > 1.0` を追加するだけで、Bin13 型の
  棚採用が将来発生した場合に可視化できる。

---

## ✓ 通過した検証

- **N-1修正の勾配は正しい(クリップ発火領域を含め有限差分と一致)**
  (`verify_grad.json`)。合成テンプレート(400画素)で解析勾配 vs 中心差分:
  - クリップ非発火(regime1): max 相対誤差 **2.5e-6**。
  - 一部クリップ発火(regime2, 237/400 画素発火): 修正後 max 相対誤差 **7.5e-5**
    に対し、**旧(バグ)勾配は max 相対誤差 1.5e8** — クリップ発火領域で旧実装が
    破滅的に誤っていたことと修正の正しさを定量確認。
  - 全クリップ(regime3): 勾配ノルム厳密 0.0(プラトー、I-1 の機構)。
- **有意ビン(1-11)の点推定は N-1修正で不変**(`compare_before_after.json`):
  max|Δσ|=1.04e-12, max|ΔΔlnL|=2.9e-11(全て丸め水準)。汚染なし。
- **Bin12/13 の ABNORMAL 全滅解消**: with-halo n_failed_starts が 5→0(全13ビンで
  no-halo/with-halo とも解消、残存は Bin10 no-halo の 1 のみで S-1 のとおり無害)。
  Bin12 with-halo `fun_spread_successful_only=4.5e-13`(真に凸収束)。
- **有意度機構分析(OLD/NEW 再構築)の数値的健全性**(`iter004_lnL_mechanism_analysis.json`):
  - `production_match: pos=true, neg=true`(NEW 再構築が本番
    `build_fermi_bubble_templates_posneg` と `np.allclose` 一致)。
  - `sig OLD`(OLD_restricted significance)が iter-003 impl-state「有意度旧(iter-002)」と
    Bin2-10 まで一致(例 Bin6 15.546 vs 15.55, Bin4 17.395 vs 17.40)。`sig NEW` も
    「有意度新(iter-003)」と一致(Bin6 25.446 vs 25.45)。iter-002 相当状態の再現に
    成功しており、バブルテンプレート ROI 拡大だけを分離した比較として妥当。
  - NEW の point-estimate σ は本番 mcmc_bin*.json の significance と一致
    (Bin10 6.372, Bin12 1.332, Bin13 0.4798)。
- **配列 dtype**: `_raw_mu` の合成が `NDArray[np.float64]` を維持(生テンプレートは
  `.astype(np.float64)` 明示)。`gas_flux_raw`/`ics_flux_raw` の生フラックス保存
  (~1e-17〜1e-15)に NaN/Inf・float32 混入なし。ICS 自然性 JSON の SED 値も全て有限・非負。

---

## Manager への要点(2つの headline 質問への回答)

1. **「N-1修正は正しく完全か」**:
   - **勾配の正しさ = 完全**。クリップ後目的関数の劣勾配と一致し、発火領域で
     旧実装(相対誤差 1.5e8)を修正した。ABNORMAL 全滅も解消。
   - **最適化 robust 性 = 不完全**。クリップは非凸プラトーを作り、修正後の勾配は
     そこで正しくゼロになるため L-BFGS-B が `success=True` で棚に止まりうる
     (Bin13 で顕在化、合成テストで再現)。失敗様式が ABNORMAL(可視)→ success=True
     (不可視)に移った。現状は best_res + 多始点で無害だが、根本は残存(I-1)。

2. **「有意ビンの結果は数値的に汚染されていないか」**:
   - **点推定(σ, ΔlnL, f_halo 点推定)= 汚染なし**(bins1-11 で |Δσ|<1.04e-12)。
     headline スペクトルは信頼できる。
   - **MCMC median / 誤差棒 = percent 水準で変化(最大12%)**。impl-state の
     「完全に不変」は点推定に限る。誤差棒は 50τ 未達(既知)も相まって再現性が
     弱く、科学的主張に使うなら chain 長の是正が前提(I-2)。
