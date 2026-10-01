# Numerical Review (iter 001) — DPIX_SR cos(b) 修正

読んだファイル: `.dev/teams/dpix-sr-cosb-fix/spec.md`, `iter-001/impl-state.md`, `code/mcmc_fit_all_bins.py`, `code/check_dpix_cosb_health.py`, `code/diagnose_regionAC_lrt_all_bins.py`, `code/mcmc_fit.py`, `code/mcmc_fit_all_bins_galprop_webrun_check.py`, `code/mcmc_fit_all_bins_galprop_webrun_v2.py`, `results/mcmc_allbins_gasICS_v1/{halo_spectrum,regionAC_lrt_all_bins}.json`, `results/mcmc_allbins_gasICS_v2_cosb/{halo_spectrum,regionAC_lrt_all_bins,health_check}.json`, および `.dev/teams/regionAC-lrt-halo-test/verdict.md`。

## 🟡 IMPORTANT (再現性・精度に懸念)

- **[`results/mcmc_allbins_gasICS_v2_cosb/regionAC_lrt_all_bins.json` Bin1] impl-state.mdの非収束原因説明が事実と不整合。** impl-state.mdは「LRT収束: 10/13ビンで fun_spread<1e-6(未収束は Bin1/12/13、いずれも f_halo≈0…由来)」と書いているが、実際のjsonを追跡すると Bin1 は `f_halo_A_pointest=145.2`(ゼロから程遠い)であり「f_halo≈0」という説明は当てはまらない。実測すると、非収束の原因は `model2_shared_fit_detail.convexity_check_per_halo0` の halo0=145.2 候補における5点multistartのうち1点だけが `fun=-5237502.946...` と他4点(`-5237502.9759...`)から0.03(相対 5.7e-9)ずれて停止したこと(他の候補・領域独立フィットはすべて厳密収束、region_A自体はfun_spread=0.0)。つまり15回のサブ最適化中1回だけがL-BFGS-Bの早期停止(gtol/ftol境界近傍での打ち切り)を起こしており、`fun_spread_max`定義(全サブ最適化にわたるmax-min)がこの1点の外れ値を拾って`convergence_flag_ok=False`と正しく警告している。**最終的に採用される`best_res`は3候補中の最小値(=収束した値)なので報告値`eqSig=3.315σ`自体は汚染されていないと考えられるが、impl-stateの「f_halo≈0由来」という説明はミスリーディングであり、`.dev/teams/regionAC-lrt-halo-test/verdict.md`が既に指摘した「Bin1/2はテンプレート共線性由来で解釈不能」という先行知見とも矛盾しない形で書き直すべき。** また `n_bins_convergence_ok_fun_spread_below_1em6` が v1=11→v2=10 に悪化(退行)している点は、cos(b)修正の副作用として明記が必要(現状spec合格条件3で要求される「定量的比較」に collision/convergence の悪化が含まれていない)。
  - 推奨修正: (a) `_multistart_minimize`/`fit_shared_halo`のdiagnosticsに各multistart実行の終端理由(`res.message`)とx値(またはL2ノルム差)を記録し、fun値だけでなくパラメータ値の一致も検証できるようにする。(b) `regionAC_lrt_all_bins.json`のBin1エントリまたはhalo_spectrum系のnoteフィールドに「Bin1(および必要ならBin2)は既知のテンプレート共線性により解釈不能、regionAC-lrt-halo-test/verdict.md参照」という文言を機械的に埋め込む(現状jsonにその注記が一切ない)。

- **[`results/mcmc_allbins_gasICS_v2_cosb/mcmc_bin01.json`] Bin1のヘッドライン結果でf_haloが3.20→284.3(約89倍)に跳躍し、MCMC信頼区間も[0.26,9.58](ほぼ0を含む)から[266.9,301.5](0から大きく離れタイト)へ質的に変化している。** 一方、この変化を部分的に説明しうる `f_ics`(1.566→1.470)の変化は小さく、`log_prior`docstringが言及するICS↔halo縮退(r=0.747、中程度)だけでは89倍の跳躍は説明しづらい。ヘッドラインの`convexity_check`(`fun_spread`~1.86e-9)は関数値の一致のみを検証しており、パラメータベクトル自体が5始点で一致しているかは記録されていない(regionAC LRTで実際に「fun値は一致するがパラメータ空間ではridge上」というケースが今回確認できたため、この懸念は仮説的ではなく実証済みの失敗モードである)。有意度算出自体(点推定ベース、MCMC非依存)は数値的に妥当だが、**Bin1のような「無→有意」の劇的な変化を報告する際は、最低限x値の5始点一致(パラメータ空間でのfun_spread相当)を確認してから「上昇のみ・低下ゼロ」という結論を確定させるべき。**

## 🟢 SUGGEST (改善余地)

- `_multistart_minimize`のL-BFGS-Bオプション(`ftol=1e-15, gtol=1e-12`)は勾配のスケール(健全性チェックで確認された解析勾配値は数千のオーダー)に対して`gtol=1e-12`は絶対閾値としては極めて厳しい一方、Bin1 regionAC の1点で見られたような早期停止も発生しており、収束モニタリングの感度が場合により低すぎたり(実際にはgtol到達前に別要因で打ち切り)一貫していない可能性がある。`res.message`のロギングを追加して停止理由の分布を可視化することを推奨。
- `check_dpix_cosb_health.py`のBin6解析勾配 vs 有限差分チェックは1ビンのみ(spec要求通り)。全13ビンでの同種チェック(少なくとも最も跳躍幅の大きいBin1)を追加すれば、上記IMPORTANT指摘への直接的な反証・補強材料になる。
- 正式なpytest/回帰テストは存在せず、`check_dpix_cosb_health.py`という単発診断スクリプトのみで健全性を担保している。プロジェクトの既存慣行(診断スクリプト中心)と整合しているため必須ではないが、`results/tests/`配下への回帰テスト化を今後検討する価値はある。

## ✓ 通過した検証

- **解析勾配の正しさ**: `neg_log_likelihood_and_grad`/`_raw_mu`を実際にReadして確認。`PIX_SOLID_ANGLE_SR`を直接参照せず`t[PARAM_TO_TEMPLATE_KEY[name]]`(テンプレート配列)のみを使用しており、勾配公式 `dNLL/df_k = Σ(1-c/μ)·T_k`(クリップ発火画素は0)はT_kの内部構成(スカラーかcos(b)配列か)に依らず数学的に成立する。Implementerの主張は正しい。`health_check.json`のx0点で解析 vs 有限差分の最大相対誤差8.62e-8(優)、best点(勾配≈0近傍)で絶対誤差1.77e-4(分母1で相対化した見かけ値、正常)を実際の数値で確認・追試済み。
- **calibrate_nfw_norm()の約分保証**: `dpix_ref = float(PIX_SOLID_ANGLE_SR[ib_ref, jb_ref])`をスカラーとして分子分母双方に使用しており、配列ブロードキャストの誤りは無い。v1/v2の`nfw_calibration`(flux, exp_ref, j_ref, b_ref)は完全一致(dpix自体に依存しない量のため当然)。norm = flux/j_ref に代数的に帰着し、cos(b)修正前後で数学的に不変であることをコード上・数値上の両面で確認。
- **物理極限・対称性・次元整合**: b→0極限比0.99996(cos(0.5°)と一致)、b→-b対称誤差0.00e+00(厳密)、ROI総立体角の数値積分2.9003 sr vs 解析値2.9002 sr(相対誤差1.27e-5、1°グリッドのmidpoint則丸め誤差として妥当な大きさ)。旧スカラー版のROI総立体角3.655 sr(1.26倍過大)は修正が捉えた誤差と整合。
- **収束(全13ビン)**: ΔlnL≥0(no-halo⊂with-halo入れ子制約)が全13ビン・v1/v2ともに成立。fun_spreadはBin1-12で≤2e-10(v1/v2とも良好)。Bin13のwith-halo fun_spread(v1=3779.6→v2=3744.0)はf_halo中央値が両版とも≈2-3e-4(ほぼ境界解)であることを実際に確認し、既存の性質(cos(b)修正による新規退行ではない)という判断を支持。
- **全13ビン有意度表の検算**: `halo_spectrum.json`(v1/v2)を実際に突合し、impl-state.mdの表(Bin1: 0→16.45σ、Bin4: 28.50→34.59σ等、Bin8-13の範囲含め)がすべて実測値と一致することを確認。「全ビンで上昇・低下ゼロ」の主張は数値的に正しい。
- **領域A/C LRT反転(Bin4/Bin6等)**: `regionAC_lrt_all_bins.json`を突合し、Bin3(4.21→2.74σ)、Bin4(5.40→0.24σ)、Bin5(3.13→0.74σ)、Bin6(2.76→0.07σ)、Bin7(4.15→2.34σ)がいずれも`convergence_flag_ok=True`かつ`delta_lnL_nonneg_ok=True`の下で得られており、数値的に信頼できる(境界解でも収束不良でもない)ことを確認。
- **再現性メタデータ**: `env_stamp()`(git_commit, dirty flag, python/numpy/scipy/emcee version)が`halo_spectrum.json`・`regionAC_lrt_all_bins.json`・`health_check.json`すべてに実際に埋め込まれていることを確認。

## Managerへの一言要旨

数値的には**採用可**。cos(b)修正のコア実装(勾配・約分・物理極限)は正しく、健全性チェックも実測で裏付けが取れた。ただし (1) regionAC LRTのBin1でv1→v2で収束フラグがTrue→Falseに悪化しており、impl-state.mdの原因説明(「f_halo≈0由来」)が実際の数値(`f_halo_A=145.2`)と矛盾するため訂正が必要、(2) ヘッドラインBin1のf_halo 3.2→284.3という89倍の跳躍は関数値ベースのfun_spreadだけでは(x値一致性未検証のため)完全には保証されていない。いずれもCRITICALではなくIMPORTANTと判断(退行ではなく主に「報告の正確さ」と「診断の粒度不足」の問題であり、コアの数値修正自体を覆すものではない)。次iterでBin1のx値一致性チェック追加とimpl-state.mdの訂正を行えばPASSで良い。
