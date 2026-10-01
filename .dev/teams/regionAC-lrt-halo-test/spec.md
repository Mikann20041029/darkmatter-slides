# spec.md — 領域A(バブル内)/C(バブル外高緯度)のf_halo共有LRT検定・全13ビン

Tier: M（物理観点・数値観点の両方が関わるため）。担当: Implementer(sonnet) → reviewer-physical + reviewer-numerical(並列・クロスレビューあり)。

## 背景・目的

`.dev/teams/galprop-gas-ics-separation/verdict.md`の「次の一手」①: 「領域C(バブル除外)単独での全13ビンhaloフィット、またはA/C共有f_haloのLRT検定」を実行する。

既存の`code/diagnose_halo_degeneracy_gasics_roi.py`はBin5・Bin6のみで領域A/C独立フィットを実行済みで、iter-003のバブルテンプレート境界バグ修正後は符号反転(旧CRITICAL)は解消し、両領域とも正のf_haloになっている:

```
Bin5: full_roi f_halo=+10.24(27.9σ) | A(バブル内)=+8.64(9.18σ) | C(バブル外高緯度)=+3.43(2.83σ)
Bin6: full_roi f_halo=+3.68(25.5σ)  | A(バブル内)=+3.27(8.53σ) | C(バブル外高緯度)=+1.23(2.15σ)
```

しかし「Aの方がCよりずっと大きい」という振幅差が、①統計的揺らぎの範囲内(球対称ハローと矛盾しない)なのか、②有意な空間不整合(球対称ハロー仮説が棄却される)なのか、まだ定量検定していない。これを尤度比検定(LRT)で白黒つけるのが本タスクの目的。全13ビンに拡張する（Bin5/6だけでなく、低エネルギー側の負のハロー・高エネルギー側の統計揺らぎも含めて全体像を見る）。

## 物理的背景（実装者が理解しておくべき前提）

- 真の球対称NFWハローなら、視線積分J値は方向に依存するが、その依存性はテンプレート自体（`j_map`）に折り込み済み。つまり**同じ物理的ハローなら、領域A・Cで独立にフィットしても同じf_halo(規格化係数)が出るはず**。f_haloが領域ごとに違う値を要求するなら、ハロー形状と何か別の空間構造(フェルミバブルの引き残し等)が縮退している証拠。
- gas/ICS/Loop I/フェルミバブルの寄与（f_gas, f_ics, f_loopI_a, f_loopI_b, f_fb, f_fb_neg）は、領域ごとに独立でよい（背景成分の実効的な規格化は空間的にムラがあってもおかしくない）。**共有を強制すべきはf_haloのみ**。

## タスク

`code/diagnose_regionAC_lrt_all_bins.py`（新規）を作成し、以下を実装する。

### 1. 領域定義（既存スクリプトと同一にする）

```python
BUBBLE_REGION = (np.abs(L_GRID) < 22) & (np.abs(B_GRID) > 10) & (np.abs(B_GRID) < 55)
region_A = valid & BUBBLE_REGION
region_C = valid & (np.abs(BG) >= 30) & ~BUBBLE_REGION
```

### 2. 全13ビンで以下の2モデルをフィットする

**モデル1（制約なし = 独立フィット）**: 領域Aと領域Cをそれぞれ独立に7パラメータフィット(既存`refit()`と同じ)。
`lnL_unconstrained = lnL_A(θ_A*, f_halo_A*) + lnL_C(θ_C*, f_halo_C*)`（自由パラメータ数14 = 7×2）

**モデル2（制約あり = f_halo共有）**: 領域A・Cの6背景パラメータは独立のまま、f_haloだけ共有した13パラメータ同時フィット。
`lnL_shared = max_{θ_A,θ_C,f_halo共有} [ lnL_A(θ_A, f_halo) + lnL_C(θ_C, f_halo) ]`（自由パラメータ数13）

目的関数・勾配は`mfa.neg_log_likelihood_and_grad()`を領域ごとに呼んで単純加算すればよい（領域Aと領域Cのピクセルは排他的集合なので、対数尤度は加法的に分解できる。共有パラメータf_haloの勾配は両領域からの寄与の和になる）。最適化はL-BFGS-B（既存`_multistart_minimize`のパターンを踏襲、多点始動で局所解を回避）。

### 3. LRT統計量

```
delta_lnL_LRT = lnL_unconstrained - lnL_shared   # >= 0 のはず（モデル1はモデル2を包含する入れ子モデル）
test_statistic = 2 * delta_lnL_LRT               # Wilks' theorem: 自由度1のchi2に漸近
p_value = scipy.stats.chi2.sf(test_statistic, df=1)
equivalent_sigma = scipy.stats.norm.isf(p_value / 2)  # 両側→片側変換
```

**解釈の指針（実装者は解釈を先取りしない。数値のみ報告し、後段のreviewer/Managerが解釈する）**:
- test_statisticが小さい(pが大きい) → 「f_haloを共有しても当てはまりがほぼ悪化しない」→ 球対称ハロー仮説と矛盾しない
- test_statisticが大きい(pが小さい) → 「共有を強制すると当てはまりが大きく悪化する」→ 領域間でf_haloが実際に異なることの統計的証拠＝球対称仮定への反証

### 4. 出力

- 標準出力: 各ビン1行のサマリのみ（`output-discipline`遵守）: `Bin{N} ({E:.2f} GeV): f_halo_A={..} f_halo_C={..} LRT={..} p={..} equiv_sigma={..}`
- ファイル: `results/mcmc_allbins_gasICS_v1/regionAC_lrt_all_bins.json`（全13ビン、各ビンについて f_halo_A/C の中央値・独立フィットのlnL・共有フィットのlnL・LRT統計量・p値・収束診断(`_multistart_minimize`のfun_spread)を保存）

### 5. 再現性

`mfa.SEED = 42`を`np.random.seed()`で固定してから実行する（`mfa.run_mcmc_with_autocorr_check`はモデル2のMCMC事後分布取得に必要な場合のみ使用、必須ではない—点推定+LRTのみでも合格条件を満たせる。時間がかかる場合はMCMC事後分布の取得は省略してよい、ただしその場合はJSONに「MCMC省略、L-BFGS-B点推定のみ」と明記すること）。

## 合格条件

1. 全13ビンで両モデルのフィットが収束する（`_multistart_minimize`のfun_spreadが既存コードの基準内、目安<1e-6程度）
2. `delta_lnL_LRT >= 0`（入れ子モデルの理論的制約、負になった場合は最適化バグとして扱い修正必須）
3. 全13ビンの結果がJSONに保存され、標準出力は1-2行/ビンのサマリのみ
4. 既存の`code/mcmc_fit_all_bins.py`・`code/diagnose_halo_degeneracy_gasics_roi.py`のロジック（テンプレート構築・valid mask・neg_log_likelihood_and_grad）を重複実装せず再利用する
5. 解釈（「ハローは本物か縮退か」の結論）はこのスクリプト自身では出さない。数値のみ報告する（spec.md冒頭の「解釈の指針」通り、判断はManager/後続レビューが行う）

## 非対象（やらないこと）

- ISRFデータでのGALPROP再計算（`.dev/teams/galprop-gas-ics-separation/verdict.md`の次の一手②は、教授提供の`ref/galprop_webrun_10050003/`で既に実質解消済みと判断し対象外）
- issue-1のPPT反映（別タスク）
- iter-004で確定した「ICS-halo悪性縮退」自体の追加調査（これは別の決定的問題として既に最終判定済み。本タスクはそれとは独立に、A/C空間非一様性という別の論点を検定する）
