# Numerical Review (iter 002)

## 総合判断

**iter-001でCRITICAL指摘した数値不安定性(no-halo未収束・符号自由パラメータのabs強制正値化)は解消を確認した。**
点推定はL-BFGS-B+解析的勾配で決定的に大域最適へ収束しており、9-17σの有意度は真のΔlnLに基づく。
バグ修正2件(`PARAM_TO_TEMPLATE_KEY`経由の勾配・`jac=True`追従)はいずれも正しい。

ただし**ROI region C(高緯度バブル外)の「f_halo=0.00σ」は、尤度が本質的に負のf_haloを
強く選好している(ΔlnL=22-61、6.7-11σ相当)のを非負制約が0にクリップした境界MLEである**。
これは数値的には信頼できる境界MLE(iter-001 Bin1の収束失敗パターンとは別物)だが、
「符号反転の解消」ではなく「符号反転の隠蔽」に相当する。物理レビュアと要相談。

検証コード・結果(scratchpadに保存、再現用):
- `verify_iter002.py` / `verify_result.json` — 解析的勾配 vs 有限差分(全3ビン)
- `verify_iter002b.py` / `verify_result_b.json` — 境界MLE検証(制約on/off)・広域50始点凸性
- `verify_repro.py` / `verify_result_c.json` — 点推定決定性・emcee seed再現性
- 環境: `/tmp/darkmatter_venv` Python 3.12.3, numpy/scipy/emcee, seed=42明示

---

## 🔴 CRITICAL

なし(iter-001のCRITICAL 2件はいずれも解消を確認)。

---

## 🟡 IMPORTANT

- **[I-1] ROI region Cの「0.00σ」は真の境界MLEだが、負の高有意度シグナルを非負制約が隠蔽している**
  (`diagnose_halo_degeneracy_gasics_roi.py`, `roi_partition_gasics.json`)。
  ユーザー質問「境界値f_halo=0.00σは数値的に信頼できるか(収束の問題ではないか)」への回答:
  - **収束の問題ではない。** 制約付き最適化はf_halo=0で `ΔlnL=0`(厳密に0、no-haloと同一fun値)に
    到達しており、これは正しい境界MLE。iter-001 Bin1の「点推定が-0.11〜-216で2000倍振れる識別不能」とは
    **明確に別物**。証拠: f_haloの非負制約を外して再最適化すると、
    - Bin5 region C: 正始点・負始点いずれからも f_halo = **-10.198**(完全一致)、ΔlnL=61.4(11.1σ相当)
    - Bin6 region C: 正始点・負始点いずれからも f_halo = **-2.376**(完全一致)、ΔlnL=22.3(6.68σ相当)
    両始点から同一解に収束する = 尤度は単峰で負側に安定した最適解を持つ。収束失敗ではない。
  - **しかしこれは物理的に重大。** 高緯度バブル外領域では、データは負のf_haloを高有意度で選好している。
    旧f_gal版のlegacy値(Bin6 -4.05[8.89σ]、Bin5 -18.4[15.5σ])と**同じ定性パターンが残存**しており
    (振幅はテンプレート集合が違うため異なるが、符号と高有意度は一致)、非負制約はこの負の選好を
    ΔlnL=0にクリップして見かけ上「0σのクリーンなnull」に変換しているにすぎない。
    Implementerのimpl-state.md「符号反転そのものは再現しなかった…ただし非負制約下でしか最適化して
    いないという構造上、負のMLEが原理的に出現しえなくなったことによる」という報告は**正確**。
  - 数値的推奨: region分割の診断では「非負制約なしのf_halo点推定とΔlnL」も併記すべき。
    現状のroi_partition_gasics.jsonは制約付き値(0.030/0.050, 0σ)しか記録しておらず、
    負の選好(6.7-11σ)が完全に不可視になっている。物理解釈の材料として必須。

- **[I-2] 境界MLEビンのemcee事後 median/16-84% は無効。上限として報告すべき**
  (`fit_one_bin:538-539`, `mcmc_bin01.json`)。
  Bin1は点推定f_halo=0(ΔlnL=9.3e-10 → 0σ)だが、emcee事後は median=0.811 [0.049, 2.655]。
  非負prior壁でtruncateされた半分布からwalkerが正側に堆積した産物で、
  **median=0.81は点推定0と10桁以上乖離しており誤差棒に物理的意味がない**。
  iter-001 cross-review [P C-1補強]で既に「境界MLEビンは区間でなく片側upper limitで報告すべき」と
  指摘済みだが未対応。Bin1/Bin12/Bin13/ROI region C全ケースが該当。有意度計算(点推定ベース)には
  影響しないが、halo_spectrum.pngの誤差棒・halo_spectrum.jsonのlo16/hi84は境界ビンで誤解を招く。

- **[I-3] autocorrelation 50τ基準が全ケース未達(既知)。事後分布の誤差棒に影響、有意度には無影響**
  (`autocorr_check`, 全13ビン+ROI 6ケースで `meets_50tau_recommendation=false`)。
  τ_max≈200-354に対しpost-burn≈5600(post-burn/τ≈16-28、要求50τに未達)。
  ユーザー質問「9-10σは数値アーティファクトか」への回答: **アーティファクトではない。**
  有意度は `sig=sqrt(2·max(ΔlnL,0))` で、ΔlnLは**L-BFGS-B点推定のみ**から算出される
  (`fit_one_bin:519,527,533-534`、emcee事後を一切参照しない)。点推定は決定的に大域最適へ収束
  (下記✓参照)しており、τ不足の影響を受けない。Bin3: sqrt(2·86.46)=13.15σ、
  Bin4: sqrt(2·151.30)=17.40σ 等、算術も正しい。**τ不足が汚染するのはmedian/16-84%のみ**。
  したがってheadlineの有意度スペクトルは信頼できるが、誤差棒の信頼性は要求水準未達。
  `max_n_steps=6000`を10τ→50τ充足まで引き上げる(≈18000)のは計算コストとの兼ね合いで
  Manager判断。ただし境界ビン(I-2)ではそもそもemcee事後が無効なので、τ改善の優先度は
  非境界ビン(Bin2-9)に限る。

---

## 🟢 SUGGEST

- **[S-1] 有意度9-17σは「信号検出」でなく「適合不足」を測っている可能性(iter-001 S-1の継続)**。
  Bin3-6は事象数55万-230万で、剛直テンプレート+iso固定下ではモデル誤設定が不可避に大ΔlnLを生む。
  数値的には真のΔlnLだが、物理的信号か系統誤差かの判別は物理レビュア領域。I-1の「高緯度で負選好」は
  まさにモデル残差をhaloテンプレートが吸収している兆候であり、S-1を補強する。
- **[S-2] `make_mu`のclip(mu,1e-10)と解析的勾配の整合は問題なし**。iso_level>0(全ビン18-72)のため
  mu≥iso_level>1e-10が常に成立し、clipは発火しない。よって勾配のsubgradient不整合は生じない(実害なし)。
- **[S-3] scales=(0.1,0.3,0.6,1.0,1.5)は凸性検証に十分**。広域ランダム50始点(f_halo∈[0.01,3], 加法散布)
  でもBin6 with-haloは spread=3.6e-11(n_success=46/50、失敗4はABNORMAL_LNSRCHで多峰性ではない)。
  10x除外による凸性検証の弱まりは実証的に無視できる。
- **[S-4] 非headlineスクリプト(`_webrun_check.py`/`_v2.py`)のシグネチャ追従漏れは要記録**。
  impl-state.md懸念4の通り。次に使う際`bounds`必須・`jac=True`タプル返しへの追従が必要。スコープ外で妥当。

---

## ✓ 通過した検証

- **バグ修正1(勾配のテンプレートキー参照)**: `neg_log_likelihood_and_grad`が
  `PARAM_TO_TEMPLATE_KEY`経由で正しく参照。解析的勾配 vs 中心差分の相対誤差 max:
  Bin1=1.7e-4(事象数2.3M・fun~8e6で有限差分の丸めが支配)、Bin3=1.3e-5、Bin6=5.0e-7。
  全て有限差分の打切り/丸め精度の範囲内で一致。勾配は正しい(`verify_result.json`)。
- **バグ修正2(`jac=True`追従)**: `diagnose_halo_degeneracy_gasics_roi.py`の`neg_ll_nohalo`/`neg_ll`が
  `(値,勾配)`タプルを返す形に修正済み。実際にroi_partition_gasics.jsonが生成完了
  (Jul 16 00:46、全bin fit 00:34-00:40の後)しており実行成功を確認。
- **点推定の決定性・凸性**: Bin6 with-haloを異なる2始点から最適化 → fun完全一致(-25754.774000)、
  x_maxdiff=2.0e-8。広域50始点でも spread=3.6e-11(`verify_result_b/c.json`)。大域最適解の一意性を実証。
- **凸性(全13ビン+ROI)**: `fun_spread_successful_only` は 2.3e-13〜3.7e-09(Implementer報告を再現・追認)。
- **再現性**: `np.random.seed(42)`固定でemcee 2回実行 → median完全一致(max_abs_diff=**0.0**)。
  point estimateはseed非依存で決定的。SOUL.md「乱数シード併記」を満たす(iter-001 I-1解消)。
- **有意度がτ不足の影響を受けない**: 有意度はL-BFGS-B点推定のみに基づき(コード読解で確認)、
  emcee事後を参照しない。9-17σは真のΔlnL。
- **HEALPix単位変換の次元整合**: `gas_flux[ph cm⁻²s⁻¹sr⁻¹MeV⁻¹]×expmap[cm²s]×DPIX_SR[sr]×de_mev[MeV]=counts`。
  `Spectra`列・`energies`列とも`np.float64`明示読み込み(`_load_healpix_grid_template:195-196`)。
  dtype昇格・float32混入なし。次元は整合(物理的妥当性は物理レビュア担当)。

---

## Managerへの要点

1. **iter-001 CRITICAL 2件は解消**。バグ修正2件も正しい。数値的にPASS相当。
2. **ユーザー質問への直接回答**:
   - 「f_halo=0.00σは数値的に信頼できるか(収束問題か)」→ **境界MLEとして信頼できる。収束問題ではない**
     (制約off時に正負両始点から同一の負値へ収束、ΔlnL_constrained厳密0)。iter-001 Bin1とは別物。
   - 「9-10σは数値アーティファクトか」→ **アーティファクトではない。真のΔlnLに基づく**
     (点推定のみ由来、τ不足の影響を受けない、算術も正しい)。
3. **ただしI-1が物理的に重大**: region Cの0σは負の高有意度選好(6.7-11σ)を非負制約が隠蔽したもの。
   「符号反転の解消」との結論は数値的に支持できない(隠蔽であって解消ではない)。物理レビュアの判断を要する。
4. I-2(境界ビンのemcee誤差棒無効・upper limit化)はiter-001から継続の未対応事項。
