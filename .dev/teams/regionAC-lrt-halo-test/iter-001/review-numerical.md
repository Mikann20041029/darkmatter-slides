# Numerical Review (iter 001)

対象: `code/diagnose_regionAC_lrt_all_bins.py`(新規)、
`results/mcmc_allbins_gasICS_v1/regionAC_lrt_all_bins.json`、
`.dev/teams/regionAC-lrt-halo-test/iter-001/impl-state.md`。
検証方法: コードは全てRead toolで読了。加えて、`code/mcmc_fit_all_bins.py`の
`_multistart_minimize()`実装をJSON `convexity_check`詳細と突き合わせて再現検証し、
`_joint_neg_ll_and_grad()`の有限差分勾配チェック、およびBin9のパラメトリック
ブートストラップ(N=200)を実際にこのレビューの中で実行した(以下に手順・結果を記載)。

## 判断(結論先頭)

**Wilks境界問題はCRITICALに該当する**が、方向はManagerの懸念(有意度の過大評価)と
**逆**である。実際にBin9でパラメトリックブートストラップを実行したところ、
真の帰無分布はchi2(1)よりも上側裾が薄く(chi2(1)は保守的な近似)、
naive chi2(1)を使うと**有意度を過小評価する**方向にバイアスがかかっている
可能性が高いことを確認した(詳細はCRITICAL-1)。したがって「3.15σは過大評価」という
向きの懸念は否定されるが、「reportされている数値(p=1.65e-3, 3.15σ)が正確な値として
そのまま使えない」という核心の懸念自体は正しく、CRITICALとして扱うべきである。
点推定値(f_halo_A/C/shared)自体・勾配実装・入れ子制約(ΔlnL≥0)には数値的な誤りは
見つからなかった。

---

## 🔴 CRITICAL

### C-1. Wilks境界問題は実在し、境界解を持つBin9/11/12/13のp値・equiv_sigmaは字面通りには使えない。ただし方向はManager想定と逆(chi2(1)は保守的)

**問題の所在**: 本タスクのLRTは「モデル1(領域A・C独立、f_halo_A,f_halo_C≥0の直積錐)」対
「モデル2(f_halo共有、対角線上の錐)」という**不等式制約付きパラメータ空間上の等式検定**
であり、標準Wilks定理が要求する「帰無仮説下でパラメータがパラメータ空間の内点」という
正則条件は、以下の意味で崩れている。

- Bin9: モデル1の領域C解が境界(f_halo_C=0)、領域A解は内点(f_halo_A=+0.101)、
  共有解(モデル2)は内点(f_halo_shared=+0.046)。→「片腕だけ境界」という非対称ケース。
- Bin11・Bin12: モデル1の領域A解が境界(f_halo_A=0)、共有解(モデル2)も境界
  (f_halo_shared=0)。→ 古典的Chernoff/Self-Liang型(帰無仮説の真値自体が境界)に近い。
- Bin13: 両領域・共有解すべて境界(f_halo=0)で完全退化(ΔlnL=0が厳密に0、この場合は
  そもそも検定統計量自体が0なのでp=1は自明に正しく、追加検証不要)。

**このレビューで実施した検証**: Bin9についてパラメトリックブートストラップを実行した。
手順: (1) JSON中のBin9のモデル2(共有)ベストフィットパラメータ(`best_params_13`)を
「真値」とみなし、領域A・Cそれぞれのmu(期待カウント)を計算、(2) そのmuからPoisson
乱数でカウントを200回再生成、(3) 各再生成データに対し実装コードの
`fit_region_independent()`・`fit_shared_halo()`をそのまま呼び出してモデル1・モデル2を
再フィットし、test_statistic(2ΔlnL)を200個収集(乱数seed=20260716の
`np.random.default_rng`で固定、コード:
`/tmp/claude-*/scratchpad/bootstrap_bin9.py`、実行時間 約28分)。

結果(N=200、観測値 t_obs=9.899):

| 統計量 | ブートストラップ実測 | chi2(1)理論値 | 比率 |
|---|---|---|---|
| 平均 | 0.824 | 1.000 | 0.82 |
| 中央値 | 0.446 | 0.455 | 0.98 |
| 68%点 | 0.790 | 0.989 | 0.80 |
| 90%点 | 2.329 | 2.706 | 0.86 |
| 95%点 | 2.919 | 3.842 | 0.76 |
| 99%点 | 3.830 | 6.635 | 0.58 |
| 200回中の最大値 | 5.223 | — | (t_obsの半分程度) |
| P(T≥t_obs) 実測 | 0/200(推定誤差により<0.5%程度) | 1.65e-3 | — |

**解釈**: 中央値付近ではブートストラップ分布とchi2(1)はほぼ一致する(0.446 vs
0.455)が、上側裾に向かうにつれ系統的にブートストラップ分布の方が薄くなる
(99%点で理論値の58%まで圧縮)。これは境界解を持つ検定で理論的に予想される、
「0への点質量を含む混合分布はchi2(1)に確率的に劣位(stochastically dominated)する」
という一般論(Chernoff 1954; Self & Liang 1987)と定性的に整合する。この場合、
naive chi2(1)で計算したp値は**真のp値より大きく**なる(=chi2(1)は保守的で、
有意度を過小評価する)。200回中t_obsを超えた例は0件で、直接そのままt_obs=9.899での
真のP値を高精度に推定するには足りない(理論値0.165%からは200回中0.33回が期待値であり
0件はどちらの仮説とも矛盾しない)が、50〜99パーセンタイルにわたる一貫した単調な
圧縮傾向から、t_obsのように分布の遥か上側裾でも同じ方向のバイアス(chi2(1)が真の値より
大きい)が続くと考えるのが自然である。

**したがって**: Managerが懸念していた「境界解に近いビンで有意度を過大評価する方向」
という仮説は、少なくともBin9についてはデータで**否定**される。むしろ真の有意度は
3.15σ以上である可能性が高い(過小評価の方向)。Bin11・Bin12(共有解も境界)は
古典的Chernoff型ケースに近く、この場合も理論上0.5×χ²(0)+0.5×χ²(1)混合はchi2(1)に
確率的に劣位する(同じ「chi2(1)は保守的」方向)ことが解析的に示せる
(S_mix(t)=0.5·S_chi2(t)≤S_chi2(t))。ただしBin11・Bin12は現状でequiv_sigma=0.48σ・
0.03σと元々非有意なので、この補正で結論(「有意でない」)が覆ることはない。

**CRITICALと判定する理由**: 方向は保守的側だが、それでもBin9のp=1.65e-3・
equiv_sigma=3.15という**数値そのもの**は不正確であり、有効数字3桁で報告するには
根拠がない。このタスクの成果物の核心(LRT p値・equiv_sigma)が字面通りの精度を
持たないにもかかわらず、JSONにはその旨のフラグが一切なく(`boundary_solution`や
`wilks_valid`のようなフィールドが存在しない)、prose(impl-state.mdの「既知の懸念」)
でのみ触れられている。この状態で3.15σという数値が後段の解釈・報告に「検証済みの値」
として一人歩きするリスクが高い。

**推奨修正**:
1. JSON各ビンに`f_halo_A_at_boundary`/`f_halo_C_at_boundary`/`f_halo_shared_at_boundary`
   (bool)と`wilks_asymptotics_valid`(bool、3つとも内点ならTrue)フィールドを追加する。
2. Bin9(実質的に結論に影響する唯一の境界ビン)については、本レビューで実施した方式の
   パラメトリックブートストラップ(N≥2000程度、tailを直接P(T≥t_obs)で評価できる規模)を
   正式に実行し、校正済みp値をJSONに追記する。計算コストの目安: 1回の
   再フィットに約8.4秒(このレビューでの実測)、N=2000で約4.7時間。
3. それが困難な場合、最低限「equivalent_sigma=3.15はchi2(1)近似による下限相当の
   値であり、境界解の影響で真の値はこれ以上である可能性が高い(本レビューの
   N=200ブートストラップで確認)」という一文をJSON descriptionまたはimpl-state.mdの
   数値そのものに付記すること。

---

## 🟡 IMPORTANT

### I-1. `fun_spread_max`診断は真の非収束と既知のABNORMAL終了アーティファクトを混同しており、Bin12/13の「収束<1e-6: False」表示だけでは点推定の信頼性を判断できない

impl-state.mdの「`_multistart_minimize()`が`success=True`のまま劣った局所解を返すが、
最終的な`min(fun)`採用ロジックは正しい解を選んでいる」という主張は、JSON
`convexity_check`詳細を直接確認して**検証できた**(以下参照)。しかし懸念自体は
残る。

- Bin12 region_C: `fun_values=[567.178, 567.178, 567.178, 2855.206, 2855.206]`,
  `success=[True]*5`。`_multistart_minimize`は`candidates=successful`(5件全てTrue)の中から
  `min(fun)`(567.178)を正しく選択している。→ 点推定は正しい。
- Bin13 region_C: `fun_values=[278.911, 1174.318, 278.911, 278.911, 1174.318]`も同様、
  3/5が278.911に一致・2/5がABNORMAL相当の劣った解。`min`選択は278.911側で正しい。

問題は、`fun_spread_successful_only`という**単一の集約指標**が「5スケール全てが
success=Trueを返しながら真の最適値から300〜1000超乖離した劣った解に収束する」という
scipy L-BFGS-Bの既知の欠陥(success flagが線形探索のABNORMAL終了を正しく捕捉しない)を
そのまま伝播させてしまい、「収束の頑健性の経験的裏付け」という本来の目的を
果たしていない点である。今回は幸い3/5以上のスケールが正解に一致していたため
`min`選択で事なきを得たが、**もし正解に一致するスケールが1個以下だった場合、
`min`選択も偶然にしか正解を拾えない**という構造的な脆弱性が残る。今回の13ビンでは
「たまたま」全ビンで正しく選択できていることを本レビューでJSON全件突合せにより
確認したが、これは今回のデータでの経験的事実であり、`_multistart_minimize()`自体の
一般的な信頼性の証明にはならない。

**推奨**: 本タスクのスコープ(spec.md合格条件4、既存コード再利用)を尊重しつつ、
`_multistart_minimize()`側の改修(scipyの`res.message`を見て
`b'ABNORMAL_TERMINATION_IN_LNSRCH'`相当を`success`から除外する)を
別タスクとしてTODOに起票することを推奨する(このレビューの指摘は実装バグではなく
既存コードの診断ロジックの限界の指摘である)。

### I-2. JSON成果物自体にコミットハッシュ・ライブラリバージョン・timestampが記録されていない(reproducibility-stamp skill要件、SOUL_addon.md「Reproducibility」)

`results/mcmc_allbins_gasICS_v1/regionAC_lrt_all_bins.json`のトップレベルには
`reproducibility_seed`と`mcmc_omitted`のみが記録され、`commit`・`python_version`・
`key_libs`(numpy/scipy等のバージョン)・`timestamp`が欠落している。これらは
impl-state.md(prose)には記載されている(commit af5e3c1、Python 3.12、
`/tmp/darkmatter_venv`)が、`.dev/TEAM_PROTOCOL.md`§7・`reproducibility-stamp`
skillが求めるのは「数値結果の正本(JSON)自体」への埋め込みである。impl-state.mdは
本タスク限りの一時的な作業記録であり、JSONだけが独立して参照される将来のシナリオ
(例: 別スクリプトからこのJSONを読み込んでプロット生成する等)では、
どのコミット・どの環境で生成された数値かの追跡が不可能になる。

**推奨修正**: `main()`の`summary`辞書に`git_commit`(`subprocess.run(["git","rev-parse","HEAD"])`)・
`python_version`(`sys.version.split()[0]`)・`key_libs`(numpy/scipy/emcee/healpy/astropy/pandas
の`__version__`)・`generated_at`(UTC ISO timestamp)を追加する。

### I-3. `np.random.seed(mfa.SEED)`は本パイプラインでは実質的にdead codeであり、コード内コメントの説明が不正確

`diagnose_regionAC_lrt_all_bins.py:54-56`のdocstringは「乱数依存はmultistartの
初期点スケール選択のみ」と説明しているが、実際に`code/mcmc_fit_all_bins.py`
`_multistart_minimize()`を確認したところ、スケール選択は固定タプル
`scales=(0.1, 0.3, 0.6, 1.0, 1.5)`(乱数不使用)であり、`np.random`呼び出しは
コードベース全体で`run_mcmc_with_autocorr_check()`内の1箇所
(`mcmc_fit_all_bins.py:502`, `np.random.randn`)にしか存在しない。本タスクは
MCMCを明示的に省略している(spec.md §5、JSON `mcmc_omitted=True`)ため、この
唯一の乱数呼び出し経路は一度も実行されない。したがって`np.random.seed(42)`は
**このスクリプトの出力に一切影響を与えない**(データ・テンプレート構築・
L-BFGS-B最適化は全て決定論的)。

これ自体はバグではない(結果はseedに依らず完全再現可能で、むしろ乱数依存の
reproducibility-stampより強い保証)が、コード内コメント「乱数依存はmultistartの
初期点スケール選択のみ」という記述は事実と異なり(スケール選択に乱数は使われていない)、
将来このコードを読む人がMCMC以外にも乱数依存があると誤解する可能性がある。

**推奨修正**: docstringを「本スクリプトの計算経路(MCMC省略時)にはnp.random依存箇所が
存在しない。np.random.seed(42)は既存スクリプト群との慣行を踏襲した形式的な処置であり、
本タスクの数値結果はこのseedの値に依存しない(完全決定論的)」に修正する。

### I-4. 13ビンにわたる多重検定(look-elsewhere effect)がequivalent_sigmaの解釈に反映されていない

Bin9のequiv_sigma=3.15σは、13ビン中で最初から特定して検定したものではなく、
「13ビンをスキャンして最も強い(または中程度の)有意性を示したビンの1つ」という
文脈で読まれる可能性が高い。単一ビンを独立検定として3.15σと報告するのと、
13回の検定のうち少なくとも1回が3.15σ相当の偏差を示す確率(トライアルファクター
補正後)を報告するのとでは、意味が異なる。本タスクのspec.md合格条件5は
「解釈はこのスクリプトでは行わない」と明記しており実装への要求ではないが、
数値レビューとしては、後段のManager/報告書がequivalent_sigmaを「単一の
pre-registeredな検定」であるかのように引用しないよう、JSONまたはimpl-state.mdに
「13ビンにわたる多重比較のトライアルファクターは未補正」という一文を明記すべきと
指摘する。

---

## 🟢 SUGGEST

### S-1. `_joint_neg_ll_and_grad()`の正しさを検証する回帰テストが存在しない

本レビューでBin6の実データテンプレートを使い、13次元の目的関数値・勾配を
中心差分(`h=1e-5×max(1,|param|)`)と比較したところ、全13パラメータで
相対誤差の最大値は2.517e-9であり、解析的勾配は正しいことを確認した
(共有haloパラメータの勾配`grad_analytic[12]=2123.519885`と、領域別に呼び出した
`grad_a[6]+grad_c[6]=2123.519885`が完全一致することも確認、chain ruleに基づく
加法分解の実装は数式通り)。しかしこの検証は本レビューでの手動実行であり、
リポジトリにコミットされた回帰テストが存在しないため、将来`neg_log_likelihood_and_grad()`
や`_joint_neg_ll_and_grad()`が変更された際に自動検出されない。`tests/`配下や
`code/`内に軽量な有限差分チェックスクリプトとして残すことを推奨する。

### S-2. `halo0_candidates`の多点始動が「たまたま」全13ビンで正解を拾えているに過ぎない点を明記

`fit_shared_halo()`のx0候補(領域A独立推定値・領域C独立推定値・0.5の最大3通り)は、
凸性を前提とした頑健化であり本レビューでも全13ビンで正しい大域最適解に到達している
ことを確認したが(I-1参照)、候補選択のロジック自体に理論的な収束保証があるわけでは
ない(あくまで経験的な頑健化)。将来ビン数やモデルが拡張された際に同じ設計を
流用する場合は、この経験的性質への依存を明示しておくとよい。

---

## ✓ 通過した検証

- **勾配・目的関数の加法分解**(依頼観点3): `_joint_neg_ll_and_grad()`の13次元
  解析的勾配を有限差分(中心差分)と比較し、最大相対誤差2.517e-9で一致することを
  実データ(Bin6テンプレート)で確認した。共有f_haloパラメータの勾配が
  `grad_a[6]+grad_c[6]`(両領域からの寄与の単純和)になっていることも数式通りかつ
  数値的に完全一致(diff=0.0)で確認した。
- **入れ子モデルの理論的制約delta_lnL_LRT≥0**(依頼観点4): 全13ビンのJSON値を
  精査し、負になっているケースはゼロ。最小値はBin13の0.0(両領域f_halo=0で完全退化、
  厳密に0)、次点はBin12の0.000564(浮動小数点誤差(~1e-10オーダー)よりも
  遥かに大きい実信号)であり、丸め誤差起因の理論制約違反は確認されなかった。
- **Bin12・Bin13の収束診断**(依頼観点2): `fun_spread_max`(2288, 2439)は
  `mfa._multistart_minimize()`が一部スケール(scale=1.0,1.5)でscipy L-BFGS-Bの
  ABNORMAL相当の劣った局所解を`success=True`のまま返す既知の挙動によるものであることを
  JSON `convexity_check`詳細から直接確認した。`min(fun)`選択ロジック自体は両ビンとも
  正しい方(小さいfun値側)を採用しており、点推定(`f_halo_A/C/shared`)の正しさには
  影響していないという実装者の主張は検証の結果**正しい**(ただしI-1参照、診断指標
  自体の信頼性には別途懸念あり)。
- **領域A/Cのピクセル排他性**: `region_A = valid & BUBBLE_REGION`、
  `region_C = valid & highlat & ~BUBBLE_REGION`という定義から、`~BUBBLE_REGION`により
  A∩C=∅がブール論理として構文的に保証されている(近似ではなく厳密)。
  対数尤度の加法分解(`lnL_shared = lnL_A + lnL_C`)の前提は正確に成立する。
- **再現性(乱数以外)**(依頼観点5): テンプレート構築(`build_templates_for_bin`,
  `nfw_j_map`, `build_bubble_counts_template`, `loop_i_shell_templates`,
  `_load_galprop_gas_ics_templates`, `mask_point_sources`)・L-BFGS-B多点始動の
  いずれにも乱数呼び出しが存在しないことをgrepで確認した(I-3参照)。
  したがって本パイプラインの数値結果はコード・データが同一である限り、seedの値に
  依らず完全に決定論的に再現される。
- **bounds構成の正しさ**: `bounds13 = mfa._bounds_no_halo() + mfa._bounds_no_halo() +
  [(0.0, None)]`が`p13`の13次元順序(`[gas_A,...,fbneg_A, gas_C,...,fbneg_C,
  halo_shared]`)と整合していることを確認した(先頭5非負+fbneg符号自由の
  6次元パターンが領域A・C分×2、末尾に共有halo非負制約1次元)。

