# Implementer State (iter 002)

作業ベースコミット: `76710e8` (本iterの変更は未コミット)。実行環境:
`/tmp/darkmatter_venv/bin/python3` (Python 3.12.3, Linux 6.6.87.2-microsoft-standard-WSL2)。
再現性シード: `SEED=42` (`mcmc_fit_all_bins.py`冒頭 `np.random.seed(SEED)`)。

前任者(中断されたセッション)が iter-002 の大部分(L-BFGS-B化、f_halo非負制約、
np.random.seed固定、convexity_check/autocorr_check診断機構)を実装済みだった。
本セッションはその続きとして、依頼された既知バグの修正・全体通読による追加バグの発見/修正・
全13ビン再フィット・ROI分割再検証を行った。

## 変更ファイル

- `code/mcmc_fit_all_bins.py`:
  1. **[依頼された既知バグ]** 652-653行目の集計処理で `r["convexity_check"]["no_halo"]["fun_spread"]`
     という存在しないキーを参照していたのを `"fun_spread_successful_only"` に修正。
     加えて、値が `None`(全restart失敗時)のビンを `max()` に渡すとTypeErrorになるため、
     `None`を除外するフィルタも追加した(前任者の実装にもこのガードは無かった)。
  2. **[依頼された既知バグ]** `convexity_check_summary.description` の
     「0.1x-10xの5スケール」という記述が実際の `_multistart_minimize` の既定 `scales`
     (`(0.1, 0.3, 0.6, 1.0, 1.5)`, 386行目付近のコメントにABNORMAL終了回避の理由が記載済み)
     と不一致だったため、実際の値・理由を反映するよう書き換えた。
  3. **[新規発見・CRITICAL]** `neg_log_likelihood_and_grad()`(311-333行目付近、iter-2で
     前任者が解析的勾配用に新規追加)が、勾配ベクトルの各成分を
     `t[name][valid]`(`name`は`PARAM_NAMES`の要素、例: `"f_gas"`)として取得していたが、
     `build_templates_for_bin()`が返す`TemplateDict`のキーは接頭辞なしの
     `"gas"`/`"ics"`/`"loopI_a"`等であり、キー名が一致していなかった。全13ビンフィット実行時に
     `KeyError('f_gas')`で**全ビンがフィット失敗**していた(前任者の docstring 中の
     「単体テストでbin1のfun_spreadが1.86→9.3e-10に改善」という記述は、この不一致下では
     再現できないはずであり、end-to-endの実行確認が不十分だったと判断される)。
     `PARAM_NAMES`→`TemplateDict`キーの対応表 `PARAM_TO_TEMPLATE_KEY` を新設し、
     `t[PARAM_TO_TEMPLATE_KEY[name]][valid]` に修正した。

- `code/diagnose_halo_degeneracy_gasics_roi.py`:
  - **[新規発見・CRITICAL]** `refit()`内の `neg_ll_nohalo`/`neg_ll` が
    `-mfa.log_likelihood(...)`(スカラーのみ返す)を定義していたが、
    `mfa._multistart_minimize()`はiter-2で`scipy.optimize.minimize(..., jac=True)`に
    刷新済みであり、`jac=True`は目的関数が`(値, 勾配)`のタプルを返すことを要求する。
    スカラーを返すと`scipy`内部で`fg[1]`のインデックス参照時にTypeErrorになるため、
    実行不能だった(実際にこのファイルは前回セッションで一度も最後まで実行されて
    いなかったとみられる)。`fit_one_bin()`と同じパターンで
    `mfa.neg_log_likelihood_and_grad()`(解析的勾配)を使う関数に置き換えた。

- `results/mcmc_allbins_gasICS_v1/mcmc_bin01.json`〜`mcmc_bin13.json`,
  `halo_spectrum.json`, `halo_spectrum.png`, `roi_partition_gasics.json`:
  上記修正後のコードで再生成(2026-07-16実行分で上書き)。

## 主要決定

- 前任者の設計(L-BFGS-B有界最適化、f_halo非負制約、解析的勾配、convexity_check/
  autocorr_check診断)はconsolidated-feedback.mdの指摘に正しく対応していたため、
  そのまま踏襲した。代替案(Nelder-Mead復活等)は検討していない — feedbackで
  明確に否定されているため。
- `PARAM_TO_TEMPLATE_KEY`のような明示的対応表を追加する代わりに`TemplateDict`の
  キー名自体を`PARAM_NAMES`と揃える(接頭辞`f_`を外す/付ける統一)というリファクタ案も
  検討したが、`make_mu()`・`build_templates_for_bin()`など他の既存コードが
  現行キー名(`"gas"`,`"ics"`等)に広く依存しており、本iterのスコープ(バグ修正+
  再フィット)を超える改修になるため見送った。対応表方式はdiffが最小で
  意図(パラメータ名とテンプレートキーは別の命名規則である)も明示できる。

## 明示した assumption / approximation

- 前任者が明記済みのassumptionをそのまま維持:
  - HEALPix→グリッド変換のエネルギービン選択は「中心エネルギーに最も近い1binを採用」方式
    (定量的な積分誤差検証は未実施)。
  - フェルミバブル(正負とも)はE²dN/dE=const(フラットスペクトル)と仮定してBin3から外挿。
  - `_multistart_minimize`のscalesを`(0.1, 0.3, 0.6, 1.0, 1.5)`に限定(10x等の極端な
    スケールはLoop Iテンプレートの初期値ヒューリスティックが大きいためL-BFGS-Bの
    直線探索がABNORMAL終了することを確認済み、との前任者の記述を検証はしていないが
    そのまま採用。5点全てで`fun_spread_successful_only`が1e-9〜1e-13と極めて小さく
    一致しており、経験的な凸性の裏付けとしては妥当と判断した)。
- 本セッションで新たに追加したassumptionはない(既存の設計を修正・検証したのみ)。

## 既知の懸念(レビュアに見てほしい点)

1. **autocorrelation 50τ基準を全13ビン・ROI分割の全ケースで満たしていない**
   (`autocorr_check_summary.n_bins_meeting_50tau = 0 / 13`)。
   `run_mcmc_with_autocorr_check()`は`max_n_steps=6000`で頭打ちにしており、
   τ_maxが200〜350程度(50τ=10000〜17500+burn)に対して不足したまま`max_attempts=3`を
   使い切って打ち切られている。consolidated-feedback.mdでは優先度4(1-4より低い)と
   位置づけられていたため、`max_n_steps`の引き上げは行っていない。点推定
   (L-BFGS-B、fun_spread 1e-9〜1e-13)は高精度に収束しているため点推定自体への
   影響は小さいと考えられるが、事後分布の16/84パーセンタイル(誤差幅)の信頼性は
   本来の要求水準(≥50τ)を満たしていない。
2. **前任者のdocstring中の未検証の定量主張**: `neg_log_likelihood_and_grad()`の
   docstringに「単体テストでbin1のfun_spreadが1.86→9.3e-10に改善」という記述が
   残っているが、この関数自体に上記のKeyErrorバグがあったため、この主張がどの
   コード状態で得られたものか確認できていない。本iterでは数値自体を検証し直して
   おらず、bug修正後の実測値(全13ビンでfun_spread 1e-9〜1e-13)は別途本ファイルに
   記載した通り。docstringの記述の真偽は未検証のまま残っている。
3. **`results/mcmc_allbins_gasICS_v1/`内の孤立した診断ファイル**
   (`emcee_convergence_check.json`, `gas_ics_correlation.json`,
   `restart_scan_check.json`, 2026-07-15 16:36-16:53付、いずれもリポジトリに
   対応する`.py`スクリプトが見当たらない)は前任者が調査目的で生成したとみられる
   stale なファイルで、本iterでは再生成・削除のいずれも行っていない
   (スコープ外の判断のため保留。要否はManager/レビュアの判断に委ねる)。
4. **非headline系統誤差チェックスクリプトの追従漏れ**
   (`code/mcmc_fit_all_bins_galprop_webrun_check.py`,
   `code/mcmc_fit_all_bins_galprop_webrun_v2.py`)は、`mfa._multistart_minimize()`が
   iter-2で`bounds`必須引数を追加した現行シグネチャ、および`jac=True`要求
   (関数が`(値,勾配)`タプルを返す必要がある)に追従できていない
   (`_v2.py`は`mfa._multistart_minimize(neg_ll_nohalo, x0[:6])`と`bounds`無しで
   呼んでおり、`neg_ll_nohalo`もスカラーのみ返す)。これらは
   spec.mdで「非headline」「系統誤差感度チェック」と明記されたスクリプトで、
   今回の合格条件(全13ビン再フィット、ROI分割再検証)には含まれないため、
   本iterでは修正していない。次にこれらのスクリプトを使う際は同様の修正が
   必要になる。
5. **ROI分割再検証の結果は「符号反転の解消」を、f_haloの非負制約という構造的な
   手段で達成している**(下記「ROI分割再検証の結果」参照)。数値のみ以下に報告し、
   物理的解釈はレビュアに委ねる。

## 全13ビンの結果 (`results/mcmc_allbins_gasICS_v1/halo_spectrum.json`)

再現性: `np.random.seed(42)`固定・コミット`76710e8`ベースの未コミット差分・
`/tmp/darkmatter_venv/bin/python3` (Python 3.12.3)。

| Bin | E [GeV] | f_gas (median) | f_ics (median) | f_halo (median [16-84%]) | ΔlnL | 有意度[σ] |
|---|---:|---:|---:|---|---:|---:|
| 1  | 1.51   | 1.018 | 0.8061 | 0.8109 [0.0493, 2.655]     | 0.00   | 0.00 |
| 2  | 2.55   | 1.083 | 0.7297 | 22.96 [16.66, 29.32]       | 6.58   | 3.63 |
| 3  | 4.31   | 1.161 | 0.5815 | 33.2 [30.61, 35.79]        | 86.46  | 13.15 |
| 4  | 7.28   | 1.218 | 0.4201 | 17.72 [16.66, 18.80]       | 151.30 | 17.40 |
| 5  | 12.29  | 1.255 | 0.3291 | 6.669 [6.260, 7.075]       | 134.06 | 16.37 |
| 6  | 20.76  | 1.265 | 0.1218 | 2.525 [2.367, 2.680]       | 120.83 | 15.55 |
| 7  | 35.06  | 1.385 | 0.2402 | 0.7241 [0.6578, 0.7908]    | 60.77  | 11.02 |
| 8  | 59.22  | 1.551 | 0.08283| 0.1782 [0.1559, 0.2004]    | 28.84  | 7.59 |
| 9  | 100.02 | 1.491 | 0.4579 | 0.04004 [0.02978, 0.04984] | 8.14   | 4.03 |
| 10 | 168.93 | 0.8225| 1.176  | 0.009609 [0.005621,0.01378]| 3.00   | 2.45 |
| 11 | 285.33 | 1.928 | 1.572  | 0.001271 [0.000391,0.002546]| 0.09  | 0.43 |
| 12 | 481.93 | 3.307 | 1.066  | 0.0003738 [0.000106,0.000788]| 0.00 | 0.00 |
| 13 | 814.00 | 1.549 | 6.121  | 0.0001355 [0.0000336,0.000318]| 0.00 | 0.00 |

全13ビンで `f_halo` は非負(制約が正しく機能している)。旧iter-1(バグ有り)の
Bin1 `f_halo=-173.6, 90.29σ`のような非物理値は再発していない。

## 凸性検証(全13ビン)

`convexity_check_summary.max_fun_spread_across_all_bins = 3.725e-09`
(全13ビンのno-halo/with-halo双方、success=Trueの結果のみでの目的関数値の最大-最小)。
個別ビンの`fun_spread_successful_only`は 2.3e-13〜3.7e-09 の範囲(Bin01で最大、
高エネルギービンほど小さい)。5スケール(0.1x,0.3x,0.6x,1.0x,1.5x)いずれかで
L-BFGS-Bが`ABNORMAL_TERMINATION_IN_LNSRCH`(success=False)を出すケースがあったが
(例: Bin6のno-haloで1/5点が失敗)、success=Trueの点同士は上記の通り高精度に一致しており、
物理レビュアの指摘した凸性(有界凸計画・大域最適解の一意性)を経験的に裏付ける結果になった。

## emcee再現性・autocorrelation time確認

- `np.random.seed(42)`を`main()`冒頭に固定(`mcmc_fit_all_bins.py`本体・
  `diagnose_halo_degeneracy_gasics_roi.py`とも同じSEEDを使用)。
- `autocorr_check_summary.n_bins_meeting_50tau = 0 / 13`
  (全13ビンでτ_max≈200-350、`max_n_steps=6000`に対し50τ要求(1万〜1.75万+burn)を
  満たせていない。「既知の懸念」1.参照)。

## ROI分割再検証の結果(Bin5・Bin6、`results/mcmc_allbins_gasICS_v1/roi_partition_gasics.json`)

**旧f_gal単一テンプレート版(2026-07-13時点、参考値・`legacy_reference`として保存済み)**:

| Bin | 全ROI | バブル領域 | 高緯度バブル外 |
|---|---|---|---|
| 6 | +0.664 (4.83σ) | +0.295 (1.60σ) | **-4.05 (8.89σ)** |
| 5 | +0.608 (1.90σ) | -1.82 (2.97σ) | **-18.4 (15.5σ)** |

→ バブル領域と高緯度バブル外で `f_halo` の**符号が反転**していた(いずれも高緯度側が負)。

**本iter(gas/ICS分離7パラメータ、f_halo非負制約適用後)**:

| Bin | 全ROI | バブル領域 (A) | 高緯度バブル外 (C) |
|---|---|---|---|
| 6 | f_halo=+2.523, 15.55σ (n_pix=10625, n_evt=44432) | f_halo=+3.499, 9.22σ (n_pix=3487, n_evt=20721) | f_halo=+0.03019, **0.00σ** (n_pix=4538, n_evt=10044) |
| 5 | f_halo=+6.696, 16.37σ (n_pix=10625, n_evt=97594) | f_halo=+9.584, 10.25σ (n_pix=3487, n_evt=44414) | f_halo=+0.05033, **0.00σ** (n_pix=4538, n_evt=22036) |

凸性(fun_spread_successful_only)は全6ケースで 3.6e-13〜2.9e-11 と極めて小さく、
点推定は高精度に収束している(autocorrelation 50τ基準は全ケース未達、上記懸念1と同様)。

**数値的事実(解釈はレビュアに委ねる)**:
- 「バブル領域内で正・高緯度バブル外で負」という**符号反転そのものは再現しなかった**。
  ただしこれは`f_halo`を非負制約下でしか最適化していないという構造上、
  負のMLEが原理的に出現しえなくなったことによるものである。
- 高緯度バブル外(C)では、Bin5・Bin6とも `f_halo` の点推定が0に極めて近い値
  (0.050, 0.030)に張り付き、有意度は両ビンとも 0.00σ (ΔlnL≈0、境界MLE)になった。
  すなわち、この領域単独では「halo成分を追加してもwith-haloモデルがno-haloモデルより
  尤度改善しない」という結果であり、旧版で見られていた「高緯度側で大きな負の有意度
  (8.89σ, 15.5σ)」という強い統計的乖離は消えている。
- 一方、バブル領域内(A)では両ビンとも高い有意度(9-10σ)で`f_halo`が正に検出されている。
  すなわち、全13ビン集計・ROI全体で見えている「halo」信号の統計的have強度は、
  空間的にはフェルミバブル領域(|l|<22°かつ10°<|b|<55°)に集中しており、
  それを除いた高緯度領域では検出されていない。

以上が測定された生の数値である。これが「符号反転の解消」と呼べるか、あるいは
「別の形の物理的懸念(halo信号とバブルテンプレートの空間的縮退)」への置き換えに
過ぎないかは、物理・数値レビュアの判断に委ねる。本Implementerとしての結論の誘導は
意図的に避けている。

## (iter >= 2) 前回 feedback への対応

- [CRITICAL-1] 最適化手法の刷新(Nelder-Mead→L-BFGS-B): 前任者実装済み。本iterでは
  `neg_log_likelihood_and_grad()`のキー不一致バグ(上記「新規発見」参照)を修正し、
  実際に全13ビンで動作することを確認した。
- [CRITICAL-2] f_halo非負制約追加: 前任者実装済み(`NONNEG_IDX=(0,1,2,3,4,6)`)。
  全13ビン・ROI分割6ケースとも`f_halo`が非負であることを確認した。
- [CRITICAL-3] 有意度計算(`sig=sqrt(2*max(ΔlnL,0))`)の確認: 既存実装のまま
  (`fit_one_bin`)で問題なし。境界MLE(f_halo=0)のビン(Bin1, Bin12, Bin13、
  ROI分割のC region)で自動的にΔlnL≈0→sig=0.00σになることを確認した。
- [CRITICAL-4] emcee再現性: 前任者実装済み(`SEED=42`、`main()`冒頭で
  `np.random.seed`固定)。`diagnose_halo_degeneracy_gasics_roi.py`も同じSEEDを
  使うことを確認した。
- [CRITICAL-5] チェイン長妥当性確認: 前任者実装済み(`run_mcmc_with_autocorr_check`)。
  実行の結果、全13ビン・ROI分割6ケースとも50τ基準は未達(「既知の懸念」1.参照)。
  spec/feedbackで優先度が1-4より低いと明記されていたため、`max_n_steps`引き上げ等の
  追加対応はしていない。
- **依頼された既知バグ(fun_spreadキー不一致、scales記述不一致)**: 本ファイル冒頭
  「変更ファイル」1,2に記載の通り修正済み。
- **「他にも同様のキー名不一致・未完了の書き換え箇所がないか確認」の指示への対応**:
  `neg_log_likelihood_and_grad()`のPARAM_NAMES/TemplateDictキー不一致
  (全13ビンがKeyErrorでフィット失敗する致命的バグ)、および
  `diagnose_halo_degeneracy_gasics_roi.py`の`jac=True`インターフェース不整合
  (実行不能)の2件を新規発見・修正した。非headlineスクリプト
  (`mcmc_fit_all_bins_galprop_webrun_check.py`/`_v2.py`)にも同様の追従漏れが
  残っているが、spec.mdでスコープ外と明記された系統誤差チェック用スクリプトのため
  未修正のまま残した(「既知の懸念」4.参照)。
