# Implementer State (iter 003)

## 変更ファイル

- `code/plot_skymap_all_subtracted.py`: `build_fermi_bubble_templates_posneg()`内の
  `bubble_region`（`|l|<22° & 10°<|b|<55°`の矩形）による強制ゼロ化を撤廃し、他の
  残差処理関数(`subtract_galactic_diffuse`等)と同じ有効ピクセルマスク
  `(np.abs(B_GRID) >= 10) & ~np.isnan(counts)`（ROI全域）を使うよう修正。正負分割
  (`np.maximum(resid,0)`/`np.maximum(-resid,0)`)・Gaussian smoothing(σ=1°)のロジックは
  変更なし。`code/mcmc_fit_all_bins.py`・`code/diagnose_halo_degeneracy_gasics_roi.py`
  は無変更（後者は自前で`BUBBLE_REGION`をROI分割診断目的のみに定義しており、テンプレート
  構築側のバグとは独立。混同なきよう確認済み、詳細は下記「確認事項2」）。
- `results/mcmc_allbins_gasICS_v1/mcmc_bin01.json`〜`mcmc_bin13.json`,
  `halo_spectrum.json`, `halo_spectrum.png`: 修正後コードで13ビン再フィットし上書き保存。
- `results/mcmc_allbins_gasICS_v1/roi_partition_gasics.json`: Bin5・Bin6のROI分割
  再検証結果を上書き保存。
- `results/mcmc_allbins_gasICS_v1/iter003_*.log`, `iter003_vs_iter002_comparison.txt`,
  `_iter003_*.py`: 本iterで実施した診断（テンプレート非ゼロ化確認、修正前後比較、
  region C非負制約なし再最適化）の正本・再現用スクリプト。stdout簡易サマリはこの
  回答内、数値の正本はこれらファイル。

## 主要決定

- ROI全域マスクは`bubble_region`固有の定義を作らず、コードベース内で既に
  `subtract_galactic_diffuse`・`subtract_point_sources`後段の全てのPoisson尤度計算
  (`plot_skymap_all_subtracted.py:300,337,560,596`)が使っている
  `(np.abs(B_GRID) >= 10) & ~np.isnan(counts)`パターンをそのまま再利用した。
  代替案(独自に`|l|<=60 & |b|<=60`を明示的に追加する)は却下: `L_GRID`/`B_GRID`は
  `L_BINS=np.arange(-60,61,1)`/`B_BINS`で既に±60°の範囲でしか定義されていない
  （`code/plot_skymap_all_subtracted.py:71-76`）ため、明示条件を足しても数学的に
  何も変わらず、逆に既存コードとマスク定義がずれるリスクの方が大きいと判断した。
- `bubble_region`変数自体は本関数から削除した(残すと将来また誤用されるリスクが
  あるため)。コメントとして経緯だけ残置。

## 明示した assumption / approximation

- なし(本修正は既存の他関数と同じマスクパターンへの置き換えであり、新たな近似は
  導入していない)。

## 確認事項1: 修正前後でテンプレートが高緯度バブル外領域で非ゼロになったことの確認

`bubble_region`矩形の外側かつ`|b|>=10`の8040ピクセルについて、Bin3(4.31 GeV)の
正負残差テンプレート(Gaussian smoothing後)を比較した
(`results/mcmc_allbins_gasICS_v1/iter003_bubble_template_old_vs_new.log`)。

| | 非ゼロピクセル数(/8040) | 平均値 | 最大値 |
|---|---|---|---|
| 修正前(template_pos) | 1069 | 0.0887 | 64.50 |
| 修正後(template_pos) | 8030 | 4.220 | 445.74 |
| 修正前(template_neg) | 1131 | 0.0607 | 6.977 |
| 修正後(template_neg) | 8040 | 4.603 | 22.85 |

修正前の非ゼロ値(1069/1131ピクセル)はGaussian smoothing(σ=1°)がbubble_region境界から
数度分「にじみ出た」ものであり、遠方の高緯度バブル外領域は文字通りゼロだった。
修正後は全域でほぼ全ピクセルが非ゼロ(8030/8040, 8040/8040)になっており、
`f_fb_neg`（負残差吸収テンプレート）が高緯度バブル外でも機能するようになったことを
数値で確認した。

## 確認事項2: `bubble_region`概念の他箇所での使用

`grep -rn "bubble_region" code/`で確認した結果:

- `code/plot_skymap_all_subtracted.py`: 本修正で変数削除済み(コメントのみ残置)
- `code/diagnose_halo_degeneracy_gasics_roi.py:39`: `BUBBLE_REGION`を独自定義
  (`(np.abs(_sub.L_GRID) < 22) & (np.abs(_sub.B_GRID) > 10) & (np.abs(_sub.B_GRID) < 55)`)。
  これは指示通り**ROI分割診断（バブル領域内 vs 高緯度域外）専用の変数**であり、
  テンプレート構築関数を一切importしていない独立実装。今回の修正対象外と判断し、
  無変更のまま維持した。
- `code/mcmc_fit_bin6_hi_proxy_check.py:202`, `code/plot_4panel_bin6.py:152`:
  同様に各スクリプト内で独自定義された表示・診断用ローカル変数であり、
  `build_fermi_bubble_templates_posneg()`とは無関係(import元も別)。今回のspecの
  スコープ外(既存のTotani baselineパイプライン=`mcmc_fit_all_bins.py`が実際に呼ぶ
  関数はplot_skymap_all_subtracted.py内の1箇所のみ)なので変更していない。

## 全13ビン f_gas/f_ics/f_halo/有意度: 修正前(iter-002)vs修正後(iter-003)

正本: `results/mcmc_allbins_gasICS_v1/iter003_vs_iter002_comparison.txt`
(iter-002側の値は本タスク開始前に`mcmc_bin*.json`をバックアップ退避したものを使用)。

| Bin | E(GeV) | f_gas旧 | f_gas新 | f_ics旧 | f_ics新 | f_halo旧 | f_halo新 | 有意度旧 | 有意度新 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1.51 | 1.018 | 1.068 | 0.806 | 1.563 | 0.811 | 3.203 | 0.0σ | 0.0σ |
| 2 | 2.55 | 1.083 | 1.150 | 0.730 | 1.377 | 22.96 | 75.78 | 3.63σ | 12.86σ |
| 3 | 4.31 | 1.161 | 1.240 | 0.581 | 1.294 | 33.20 | 48.06 | 13.15σ | 20.73σ |
| 4 | 7.28 | 1.218 | 1.323 | 0.420 | 0.949 | 17.72 | 26.16 | 17.40σ | 28.50σ |
| 5 | 12.29 | 1.255 | 1.391 | 0.329 | 0.820 | 6.669 | 10.24 | 16.37σ | 27.94σ |
| 6 | 20.76 | 1.265 | 1.419 | 0.122 | 0.599 | 2.525 | 3.680 | 15.55σ | 25.45σ |
| 7 | 35.06 | 1.385 | 1.600 | 0.240 | 0.710 | 0.724 | 1.110 | 11.02σ | 18.99σ |
| 8 | 59.22 | 1.551 | 1.882 | 0.083 | 0.240 | 0.178 | 0.330 | 7.59σ | 14.40σ |
| 9 | 100.02 | 1.491 | 1.791 | 0.458 | 0.868 | 0.0400 | 0.0811 | 4.03σ | 8.99σ |
| 10 | 168.93 | 0.823 | 1.195 | 1.176 | 1.257 | 0.0096 | 0.0222 | 2.45σ | 6.37σ |
| 11 | 285.33 | 1.928 | 2.175 | 1.572 | 1.937 | 0.00127 | 0.00245 | 0.43σ | 1.69σ |
| 12 | 481.93 | 3.307 | 3.961 | 1.066 | 1.605 | 0.00037 | 0.00060 | 0.0σ | 0.0σ |
| 13 | 814.00 | 1.549 | 1.943 | 6.121 | 8.166 | 0.00014 | 0.00020 | 0.0σ | 0.0σ |

事実として報告する(解釈・妥当性はレビュアに委ねる):
`f_fb_neg`テンプレートがROI全域で非ゼロになったことにより、全13ビンで`f_gas`,
`f_ics`, `f_halo`のいずれもが系統的に**増加**し、halo有意度も**軒並み上昇**した
(例: Bin6は15.55σ→25.45σ、Bin4は17.40σ→28.50σ)。これは「バブルテンプレートの
制限を外せば縮退が緩和されhalo有意度が下がる」という期待とは逆方向であり、
恣意的な解釈を避けるためそのまま報告する。全13ビンの完全な結果ファイルは
`results/mcmc_allbins_gasICS_v1/mcmc_bin{01..13}.json`, `halo_spectrum.json`参照。

## ROI分割再検証(Bin5・Bin6): 高緯度バブル外領域(region C)のf_haloは変化したか

正本: `results/mcmc_allbins_gasICS_v1/roi_partition_gasics.json`
(旧版は`iter002_backup/roi_partition_gasics_iter002.json`として保持、本レポート内に転記)。

### (a) 非負制約付き再フィット(`diagnose_halo_degeneracy_gasics_roi.py`本体、既存の合格判定に使う値)

| Bin | 領域 | f_halo旧(iter-002) | 有意度旧 | f_halo新(iter-003) | 有意度新 |
|---|---|---|---|---|---|
| 5 (12.29 GeV) | full_roi | +6.696 | 16.37σ | +10.24 | 27.94σ |
| 5 | A_bubble_region | +9.584 | 10.25σ | +8.637 | 9.18σ |
| 5 | **C_highlat_ex_bubble** | **+0.0503**(≈0, 境界値) | **0.00σ** | **+3.429** | **2.83σ** |
| 6 (20.76 GeV) | full_roi | +2.523 | 15.55σ | +3.675 | 25.45σ |
| 6 | A_bubble_region | +3.499 | 9.22σ | +3.268 | 8.53σ |
| 6 | **C_highlat_ex_bubble** | **+0.0302**(≈0, 境界値) | **0.00σ** | **+1.226** | **2.15σ** |

iter-002では region C(高緯度バブル外)の`f_halo`は非負制約の境界値(≈0, sig=0.00σ)
に張り付いており、consolidated-feedback-002が指摘した通り「制約を外せば真に負」
という状態だった。iter-003修正後は region C の`f_halo`が境界値ではなく**内点解**
として正の値(Bin5: +3.429 [2.83σ], Bin6: +1.226 [2.15σ])に収束した。

### (b) 非負制約を完全に外した無制約再最適化(iter-002の数値レビュアが行った検証をiter-003版で再現)

`results/mcmc_allbins_gasICS_v1/iter003_regionC_unconstrained_check.log`
(`_iter003_regionC_unconstrained_check.py`が正本スクリプト)。region Cのf_halo
の非負制約のみを外し(`f_gas`等の他パラメータのbound、及びf_fb_negの符号自由設定は
`_bounds_with_halo()`と同一に維持)、正・負両方の初期値からL-BFGS-Bで再最適化した。

| Bin | 初期値=正 | 初期値=負 | 一致 |
|---|---|---|---|
| 5 | f_halo=+4.261 | f_halo=+4.261 | 一致 |
| 6 | f_halo=+1.726 | f_halo=+1.726 | 一致 |

正負どちらの初期値からも同一の**正の**値に収束しており、局所解ではなく単一の
大域解であることを確認した。iter-002では同じ検証手法で Bin5: -10.198, Bin6: -2.376
という負のMLEを得ていたのに対し、iter-003では符号が反転し正のMLEになっている。

**結論(数値ファクトのみ、解釈はレビュアに委ねる)**: 少なくともBin5・Bin6については、
高緯度バブル外領域の負のhalo選好は**解消した**。制約付き・無制約いずれの
再最適化でも、修正後は region C の f_halo が正で有意(sig>0)という結果を得た。
これはiter-002 consolidated-feedbackが「実装は正しいが科学的結論としては
空間非一様性が残る」と判定した根拠(region C で無制約MLEが負)が、テンプレート
構築側のバグ修正によって成立しなくなったことを意味する。

## 残った懸念・[ASSUMPTION]

- **[ASSUMPTION] region C の検証はBin5・Bin6の2ビンのみ**(spec指示通り)。他の
  11ビンについてはROI3分割の再検証を実施していない。全13ビンで同様の符号反転
  解消が成立するかは未検証。
- 全13ビンのautocorrelation 50τ基準は本iterでも未達(iter-002から継続する既知の
  懸念、`50τ充足=False`が全ビンのログに出力されている)。点推定(MLE, ΔlnL, sig)
  は凸最適化(L-BFGS-B)由来でMCMC非依存のため影響を受けないが、事後分布の
  16/84パーセンタイル幅の精度には引き続き注意が必要。
- 全13ビンで`f_gas`, `f_ics`, `f_halo`, 有意度が軒並み上昇したことの物理的解釈
  (例えば「バブルテンプレートのカバレッジが広がったことで、以前は`f_halo`が
  誤って吸収していた高緯度の残差成分の一部を`f_fb_neg`が正しく吸収するように
  なった」のか、あるいは別の縮退が生じているのか)は評価していない。物理レビュアの
  判断を仰ぐ。
- region Cのf_haloが「正で有意」になったことは、真のダークマターハロー検出を
  意味するのか、あるいは依然として何らかのテンプレート間縮退(例えば`f_fb_neg`
  とNFW J-mapの空間形状の残存する相関)の産物なのかは、本タスクのスコープでは
  判定していない。iter-002 verdictが提案していた「region A・Cでf_halo共有の
  同時フィット+尤度比検定」等の追加検証は今回実施していない。
- 全13ビンMCMC再フィット・ROI分割診断は`np.random.seed(42)`固定
  (`mfa.SEED`)、ベースコミット`76710e8`（未コミット差分あり: iter-001〜003の
  一連の変更が積み上がった状態）、実行環境: Python 3.12.3
  (`/tmp/darkmatter_venv/bin/python3`)、Linux 6.6.87.2-microsoft-standard-WSL2、
  2026-07-16実行。
