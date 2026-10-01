# Numerical Review — Totani比較表 数値突合せ (緊急, 2026-07-16)

対象: ユーザー提案の比較表(Bin5/6/7)。JSON値の一致とsig定義の確認に限定。

## 1. 最新版か → OK。ただしgit確認は独自に実施

- `results/mcmc_allbins_gasICS_v1/halo_spectrum.json` はcommit `a095b0b`
  (`git log -1 -- <file>` で確認、mtime 09:00と一致)で追加された、リポジトリの
  HEAD。`iter004_before_N1fix/`(08:50, N-1修正**前**)より新しく、混同なし。
- JSON値 突合せ: `significance_sigma` = 27.938174619303204 / 25.445982812314362 /
  18.98854734859232 → 丸めるとユーザー案の27.94 / 25.45 / 18.99 と完全一致。
  `f_halo`欄の10.235 / 3.675 / 1.110も`params.f_halo.median`と一致
  (10.235496.../3.674862.../1.109848...)。転記ミスなし。

## 2. sig定義とinterior解 → OK、ただしf_halo表示値の推定量に注意 (IMPORTANT)

- `significance_sigma = sqrt(2*delta_lnL)`を数値的に確認 (Bin5: 2×390.271=780.54,
  √=27.9382…で一致)。Wilks近似、1自由度。
- interior解: Bin5のf_halo `lo16=9.857, hi84=10.609`で0から大きく離れており、
  境界解(f_halo=0)ではない。よって別タスクで見つかった「境界解でのWilks近似の
  保守性バイアス」は適用対象外 — 確認済み(ユーザー想定通り)。
- **ただし表に載せる`f_halo`は MCMC posterior median、`significance_sigma`は
  L-BFGS-B点推定由来の`delta_lnL`から算出**という異なる推定量の混在。
  `.dev/teams/galprop-gas-ics-separation/iter-004/review-numerical.md` I-2で
  「σ/ΔlnLの点推定はN-1修正で不変(|Δσ|<1e-12)だが、MCMC posterior medianは
  同修正で最大12%変動した(50τ未達chainでの増幅)」ことが確認済み。
  この3ビンとも`autocorr_check.meets_50tau_recommendation: false`
  (tau_max 249–287、post-burn 5600 → 実効独立サンプル ~20–23個)。
  → **f_halo=+10.235のような小数点3桁表示は有効数字として過剰**。実際の
  16-84%区間は Bin5: [9.86, 10.61] (半幅 ~4-7%)、Bin6: [3.53, 3.82] (~4%)、
  Bin7: [1.05, 1.17] (~5%)。教授報告では `f_halo ≈ 10.2 (+0.4/-0.4)` 程度に
  丸め、区間 or 有効数字2桁で示すことを推奨。sig(σ)側は決定論的点推定で
  問題ないので3桁のままでよい。

## 3. 多重検定の注記 → 必要 (IMPORTANT)

- `regionAC-lrt-halo-test/verdict.md`に既存の明記あり:「13ビンにわたる多重検定の
  トライアルファクター補正は未実施…単一ビンの値として報告し『13ビン中最大』等の
  文脈で強調しないこと」。今回のBin5/6/7選定はTotani本文記載の12/21/35 GeVに
  対応する最寄りビンの機械的選択(12.29/20.76/35.06 GeV)であり、cherry-pick根拠は
  ない。ただし**スライド上に選定基準を1行明記すべき**(「戸谷報告値に最寄りの
  3ビンを機械的に選択、13ビン中の最大値選抜ではない」)。省略すると
  post-hoc selectionと誤解されるリスクがある。

## ✓ 通過した検証

- JSON値の転記(f_halo, significance_sigma)は3ビンとも完全一致、桁の取り違えなし
- 最新版(N-1修正後、commit a095b0b = HEAD)であることをgit logで独立確認
- sig = sqrt(2ΔlnL)、interior解であることを数値的に確認
