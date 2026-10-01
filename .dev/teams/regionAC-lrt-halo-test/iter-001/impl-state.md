# Implementer State (iter 001)

## 変更ファイル
- `code/diagnose_regionAC_lrt_all_bins.py`(新規): 領域A(バブル内)/C(バブル外高緯度)でf_haloを共有した場合のLRTを全13ビンで実行するスクリプト。既存の`mcmc_fit_all_bins.py`(`neg_log_likelihood_and_grad`, `_multistart_minimize`, `_bounds_no_halo`, `_bounds_with_halo`, `build_templates_for_bin`等)と`plot_skymap_all_subtracted.py`(`L_GRID`/`B_GRID`, `loop_i_shell_templates`, `_load_galprop_gas_ics_templates`, `mask_point_sources`)を再利用し、テンプレート構築・valid mask・尤度計算のロジックは重複実装していない。

## 実行結果
- コマンド: `/tmp/darkmatter_venv/bin/python code/diagnose_regionAC_lrt_all_bins.py`
- コミットハッシュ: 実装時点のHEAD = `af5e3c1`(このタスク開始前の最新コミット。本ファイルはこのコミットの後に追加した新規ファイル、まだcommit未実施)
- 再現性シード: `np.random.seed(mfa.SEED=42)`(スクリプト冒頭で固定)
- 実行環境: `/tmp/darkmatter_venv`(Python 3.12, numpy/scipy/emcee/healpy/astropy/matplotlib/pandas)
- 総実行時間: 約3分半(13ビン×2モデル、L-BFGS-B多点始動点推定のみ。MCMCは省略)
- 出力: `results/mcmc_allbins_gasICS_v1/regionAC_lrt_all_bins.json`(全13ビン詳細)、`results/mcmc_allbins_gasICS_v1/regionAC_lrt_all_bins.log`(実行ログ全文)

### 全13ビン結果サマリ

| Bin | E [GeV] | f_halo_A | f_halo_C | f_halo_shared | ΔlnL_LRT | test_stat(2ΔlnL) | p値 | equiv_σ | fun_spread_max | Δ≥0 | 収束<1e-6 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1.51 | +594.10 | +0.00 | +71.59 | 126.44 | 252.89 | 6.09e-57 | 15.90 | 2.24e-08 | True | True |
| 2 | 2.55 | +217.33 | +0.00 | +58.92 | 102.51 | 205.01 | 1.68e-46 | 14.32 | 1.40e-09 | True | True |
| 3 | 4.31 | +46.18 | +10.34 | +30.40 | 8.87 | 17.74 | 2.53e-05 | 4.21 | 6.98e-10 | True | True |
| 4 | 7.28 | +24.75 | +6.08 | +16.33 | 14.56 | 29.11 | 6.83e-08 | 5.40 | 2.91e-10 | True | True |
| 5 | 12.29 | +8.65 | +4.26 | +6.66 | 4.91 | 9.82 | 1.72e-03 | 3.13 | 1.31e-10 | True | True |
| 6 | 20.76 | +3.26 | +1.73 | +2.54 | 3.80 | 7.60 | 5.83e-03 | 2.76 | 2.18e-11 | True | True |
| 7 | 35.06 | +1.14 | +0.21 | +0.71 | 8.60 | 17.20 | 3.36e-05 | 4.15 | 1.36e-12 | True | True |
| 8 | 59.22 | +0.29 | +0.04 | +0.17 | 3.71 | 7.42 | 6.44e-03 | 2.73 | 5.46e-12 | True | True |
| 9 | 100.02 | +0.10 | +0.00 | +0.05 | 4.95 | 9.90 | 1.65e-03 | 3.15 | 3.27e-11 | True | True |
| 10 | 168.93 | +0.02 | +0.01 | +0.02 | 0.17 | 0.34 | 5.59e-01 | 0.58 | 1.47e-10 | True | True |
| 11 | 285.33 | +0.00 | +0.004 | +0.00 | 0.11 | 0.23 | 6.33e-01 | 0.48 | 1.06e-07 | True | True |
| 12 | 481.93 | +0.00 | +0.0001 | +0.00 | 0.0006 | 0.0011 | 9.73e-01 | 0.03 | **2288** | True | **False** |
| 13 | 814.00 | +0.00 | +0.00 | +0.00 | 0.00 | 0.00 | 1.000 | 0.00 | **2439** | True | **False** |

f_halo_A/f_halo_C/f_halo_sharedは全てL-BFGS-B点推定(MLE)。MCMC事後分布は取得していない(理由は下記assumption参照)。

## 主要決定
- モデル1(独立フィット)は既存`diagnose_halo_degeneracy_gasics_roi.refit()`のロジック(no-halo 6パラメータ→with-halo 7パラメータの順にL-BFGS-B多点始動、ΔlnL<0ならno-halo解にフォールバック)からMCMC呼び出し部分だけを除いた`fit_region_independent()`として実装した。理由: spec.md §5でMCMC省略を明示的に許容しており、点推定のみでLRTの合格条件(delta_lnL_LRT>=0の検証、収束診断)を満たせるため。却下した代替案: MCMC事後中央値も取得する案 → 13ビン×3フィット(A独立、C独立、13次元共有)分のemcee実行はコスト高で「時間が掛かりすぎる場合は省略してよい」というspec条件に該当すると判断し不採用。
- モデル2(13パラメータ共有フィット)の目的関数・勾配は`_joint_neg_ll_and_grad()`という薄いラッパーで実装した。13次元ベクトルを`[gas_A,...,fbneg_A, gas_C,...,fbneg_C, halo_shared]`の順に定義し(spec.mdタスク節の指定順)、領域Aは`p13[0:6]+p13[12]`、領域Cは`p13[6:12]+p13[12]`の7次元ベクトルに組み替えて`mfa.neg_log_likelihood_and_grad()`をそれぞれ呼び出し、値は加算、共有halo勾配は`grad_a[6]+grad_c[6]`に再分配した(領域A/Cのピクセル集合が排他的であることに基づく対数尤度の加法分解、spec.md記載の通り)。boundsは`mfa._bounds_no_halo()`(6次元、非負5+符号自由1)を領域A/C分2回連結し、共有halo用の`(0.0, None)`を末尾に追加する形で構成した(既存の`_bounds_no_halo`/`_bounds_with_halo`をそのまま再利用、新規bounds定義ロジックは書いていない)。
- モデル2のx0は、モデル1(領域独立フィット)で得た6背景パラメータの点推定をそのまま使い、共有halo初期値だけ2通り(領域A独立推定のf_halo、領域C独立推定のf_halo)を試して`mfa._multistart_minimize()`(各候補で5スケール多点始動)を2回実行し、全体最小のfun値を採用した。却下した代替案: 単一x0(例えば両者の平均)のみで1回実行する案 → 実装後の検証でBin12/13においてL-BFGS-Bが`success=True`のまま局所解にトラップされる既知の挙動(`mfa._multistart_minimize()`docstringに「bin1,3,6,13でscale>=1.5からABNORMAL発生」と既に記載されている、本タスクで新規発見した問題ではない)を確認したため、頑健性のため2候補×5スケールの二重multistartに変更した。
- `fit_shared_halo()`の収束診断として、モデル1の2領域それぞれのwith-halo `fun_spread_successful_only` と、モデル2の複数halo候補間の`fun_spread_successful_only`のうち最大値を`fun_spread_max`として1ビンあたり1個の集約値にした。理由: spec.md合格条件1「fun_spreadが既存コードの基準内」を1ビン1指標で判定可能にするため。

## 明示した assumption / approximation
- [ASSUMPTION] MCMC事後分布は取得しない。全結果はL-BFGS-B多点始動によるMLE点推定(spec.md §5で明示的に許容)。JSON出力の`description`フィールドと各種変数名(`f_halo_A_pointest`等)に「点推定である」ことを明記した。
- [ASSUMPTION] モデル2のx0共有halo候補は「領域A独立推定値・領域C独立推定値・0.5」の3通り(重複除去後は最大3、最小2)に限定した。理論的には凸問題(muがパラメータについてアフィン、Poisson NLLは凸、非負制約下でも有界凸計画)なので大域最適解は一意のはずだが、下記「既知の懸念」の通りL-BFGS-Bが実際には`success=True`のまま局所解にトラップされる既知の非理想的挙動があるため、この限定的な多点始動で全13ビンにおいて`delta_lnL_LRT>=0`(合格条件2、理論的制約)が経験的に満たされることを実行結果で確認した(結果セクション参照)。

## 既知の懸念(レビュアに見てほしい点)
- **Bin12・Bin13で`fun_spread_max`が合格条件1の目安(<1e-6)を大幅に超過している**(それぞれ2288、2439)。原因を調査したところ、これはこのタスクで新規に導入したコードのバグではなく、既存`mfa._multistart_minimize()`が抱える既知の挙動(同関数docstring: 「10x等より極端なスケールをx0に掛けるとL-BFGS-B直線探索がABNORMAL終了する、確認済みのビン: 1,3,6,13」)が、領域C限定(全ROIよりイベント数が少ない部分集合)のフィットで、既定のscales=(0.1,0.3,0.6,1.0,1.5)のうち1.0や1.5倍でも顕在化したものである。具体的には`scipy.optimize.minimize(method="L-BFGS-B")`が`success=True`を返しながら実際にはfun値が数百〜数千大きい劣った解に収束するケースを確認した(Bin12領域C: scale=1.0,1.5でfun=2855.2 vs 他スケールで567.2、詳細はJSON`region_C_fit_detail.convexity_check.with_halo`参照)。`_multistart_minimize()`自体は`success=True`の候補の中から`min(fun)`を採用する設計のため、**最終的に採用されるbest_res自体は正しく最良の解(fun=567.2側)を選んでいる**ことを確認済みで、`f_halo_A/C/shared`点推定値・`delta_lnL_LRT`(全13ビンで>=0)の正しさには影響していない。影響が及ぶのは「収束の頑健性を示す診断指標`fun_spread_successful_only`自体が、この2ビンに限り本来の目的(大域最適解の一意性の経験的裏付け)を果たせていない」という点のみである。
  - このタスクのspecは「既存の`mcmc_fit_all_bins.py`・`diagnose_halo_degeneracy_gasics_roi.py`のロジックを重複実装せず再利用する」ことを合格条件4で要求しており、`_multistart_minimize()`自体への修正はスコープ外と判断し、対応しなかった。修正が必要と判断される場合はエスカレーションが必要(`mfa._multistart_minimize()`側の改修は本タスクの直接のスコープを超える)。
- Bin1・Bin2でf_halo_Aが非常に大きい値(+594.1、+217.3)になっている。spec.md「非対象」節に明記された通り、これはiter-004で既に確定済みの「ICS-haloの悪性縮退」(低エネルギービンで顕著)に起因する既知の現象であり、本タスクのスコープ(A/C空間非一様性のLRT検定)とは独立の論点として扱い、追加調査は行っていない。
- Bin9・Bin11・Bin12でf_halo_A=0またはf_halo_C=0(bounds下限)になっているが、これはPoisson NLLの非負制約(f_halo>=0)が有効に効いている(境界解)ケースであり、Wilks' theoremのdf=1カイ二乗漸近近似が境界解のケースで厳密に成立するかは検証していない(標準的なLRTのWilks定理は内点解を仮定することが多く、パラメータが真の値の境界上にある場合は漸近分布が変わりうることが統計学の一般論として知られている)。spec.mdの式をそのまま実装したのみで、この統計的細部の妥当性判断はレビュア/Managerに委ねる。

## (iter >= 2) 前回 feedback への対応
- 該当なし(iter 001)
