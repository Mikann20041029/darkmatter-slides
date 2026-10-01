# Physical Review (iter 002)

## 判断（結論先頭）

**依然として採用不可。** ただし理由は iter-001 とは変質した。iter-001 の CRITICAL
（f_halo 符号自由）は非負制約で正しく閉じられ、Bin1 の f_halo=-173.6 / 90.29σ という
非物理値は再発しない。しかし iter-001 IMPORTANT で指摘した **ICS↔halo 空間縮退は未解決**で、
今回さらに **halo↔フェルミバブル空間縮退**が加わった。ROI 分割の生データが示すのは
「符号反転の解消」ではなく、**非負制約による符号反転の隠蔽**である。

決定的事実（`results/mcmc_allbins_gasICS_v1/roi_partition_gasics.json` から確認）:
高緯度バブル外領域 C で with-halo の NLL は no-halo と 13 桁一致（fun_spread≈2e-13、
f_halo が下限 0 で active）。KKT 条件により、**制約が boundary-active であることは
無制約 MLE が f_halo<0（実行不能側）にあることを意味する**。すなわち領域 C のデータは
依然として「負の halo」を要求しており（legacy 版で -4.05/8.89σ, -18.4/15.5σ と
出ていたのと同じ物理）、非負制約はそれを 0 で床止めして 0.00σ に見せているだけである。
バブル領域 A（f_halo≈+3.5, 9.2σ）と領域 C（無制約なら負）の**空間的非整合は消えていない**。
球対称・全天の NFW ハローは単一の f_halo で両領域を同時に満たさねばならず、この結果は
それを満たさない。→ Totani (2025) の 20 GeV 全天 NFW ハロー超過の再現としては採用不可。

---

## 🔴 CRITICAL

### C-1. halo↔bubble 空間縮退：halo 信号がバブル領域に限局し、DM ハローの空間固定性を満たさない
- [`code/plot_skymap_all_subtracted.py:532-543` `build_fermi_bubble_templates_posneg`],
  [`code/diagnose_halo_degeneracy_gasics_roi.py:39,129-130`]
- バブルテンプレート（正 `fb`・負 `fb_neg`）は `valid_px = bubble_region & ~isnan` の外を
  ゼロにしており、空間的に **|l|<22°, 10°<|b|<55°（=領域 A）に完全限局**する。
  一方 NFW halo テンプレートは全 ROI（|b|≥10）に広がる。したがって領域 C（|b|≥30 かつ
  バブル外）には halo テンプレートのみが存在し、バブルとの競合は無い。
- それにもかかわらず f_halo は **A で 9-10σ 検出／C で 0.00σ**。physical には
  f_halo は NFW 規格化の単一乗数（空間変化は j_map に内包済み）なので、真の球対称 NFW なら
  A と C で **同一値**になるはず。実測は Bin6 で A=3.499 vs C=0.030（約 116 倍）、
  Bin5 で A=9.584 vs C=0.050（約 190 倍）。この桁違いの非整合は J-factor の空間変化
  （テンプレートに既に入っている）では説明できず、**halo 振幅が空間固定でない**ことを示す。
- さらに領域 C は boundary-active（無制約 MLE は f_halo<0）。**A は正の halo を、C は負の
  halo を要求する**という iter-001 と同じ空間的対立が、非負制約で C を 0 に床止めした
  結果 0.00σ に化けているだけである。「符号反転の解消」ではなく「符号反転の隠蔽」。
- 加えてバブルテンプレートは **Bin3(4.31 GeV) の [iso+GALPROP+PS] 差引残差**から構築され
  （`:528-540`）、Bin3 に halo 信号が存在すればそれを既に含む。halo(NFW) と fb(∝Bin3残差)
  が領域 A で空間的に共存し、かつ fb_neg が符号自由なため、A 内では **halo・fb・fb_neg・ics の
  4 成分が同一空間で相殺・肩代わりできる**。A の 9-10σ は「NFW 形状の実信号が確かに在る」
  ことは示すが、それが DM か「バブル／GALPROP mismodeling の形状誤差を NFW が吸ったもの」かを
  **原理的に切り分けられない**。
- **推奨（採用可否を判定するための決定的テスト）**:
  1. **バブルを含まない領域 C のみで全 13 ビンの halo フィット**を行う。全天 NFW なら C にも
     20 GeV halo が（S/N は落ちても）出るはず。C で全ビン 0.00σ（無制約なら負）なら、
     Totani の全天ハローは本パイプラインでは再現されないと結論できる。
  2. あるいは A と C で **f_halo を共有した同時フィット**を行い、共有 f_halo を課したときの
     ΔlnL 悪化を LRT で評価する。悪化が有意なら「空間固定 NFW 仮説」を棄却できる。
  3. バブルテンプレートを halo を含みうる Bin3 自己参照から作らない（外部スペクトル／
     形状に基づく独立テンプレート化、または Bin3 の halo 寄与を先に差し引く）。

### C-2. ICS↔halo 縮退（iter-001 I-1）が未解決、領域依存で f_ics が 170 倍振れる
- [`code/mcmc_fit_all_bins.py:286-289` `make_mu`], 結果 `roi_partition_gasics.json`
- f_ics は Bin6 で 領域C=0.0136 / 全ROI=0.125 / 領域A=0.552、Bin5 で C=0.00504 /
  全ROI=0.325 / A=0.853。物理的に GALPROP 規格化済みの ICS 振幅は O(1) で空間的に安定すべき
  （iter-001 I-2: ICS/gas 比は高緯度でむしろ上昇）。それが領域 C で ~0（消失）まで潰れるのは、
  **ICS が halo/iso と縮退し、smooth 成分がどれか一つに吸われる**症状。領域 C では
  f_ics≈0 かつ f_halo≈0 で、fit は実質 iso+gas+loopI のみ。領域 A では f_ics も f_halo も
  増える。**smooth 成分（iso/ics/halo/bubble）の縮退が pervasive** であり、f_halo は
  安定な物理振幅として測れていない。
- 非負制約は f_halo の負側暴走を止めたが、**縮退そのもの（自由度過剰）を除去していない**。
  iter-001 の指摘（f_gas/f_ics への物理事前分布 or gas:ICS 比固定）は依然有効。ただし
  cross-review P-5 の通り、Totani baseline（独立 2 成分）からの逸脱として明示的に扱うこと。

---

## 🟡 IMPORTANT

### I-1. 非負制約の片側性が f_halo の中央値・信頼区間を上方バイアスさせる（有意度は別問題）
- [`code/mcmc_fit_all_bins.py:302-306` `log_prior`], [`:538-539`]
- 依頼観点 3 への回答: 片側制約は真値≈0・モデル誤差ランダム揺らぎ下で必ず非負側に偏った
  事後分布を生む。実際 Bin1(1.51 GeV) は 0.00σ（無検出）なのに median f_halo=0.811、
  16-84% CI=[0.049, 2.655] と 0 から浮いている。**これは検出ではなく clip 由来のバイアス**で、
  この median を「測定値」として引用してはならない（下端 0.049 が示す通り実質 0 と無矛盾）。
- ただし **A の 9-10σ は片側バイアスでは作れない**。sig=9 は ΔlnL≈40 に相当し、boundary
  バイアスが null から作り出せる見かけの有意度は高々 ~1σ 規模（χ²₁→½δ₀+½χ²₁ 混合）。
  A には NFW 形状の**実信号**が確かに在る。問題はその正体（DM か bubble 残差か）であって
  bias 由来の偽検出ではない。→ 観点 3 の「9-10σ が構造的バイアスで説明できるか」への回答は
  **No、バイアスだけでは説明できない**。だが C-1 の通り DM とは同定できない。

### I-2. 有意度公式 sig=sqrt(2·max(ΔlnL,0)) は境界パラメータとして正しい（iter-001 の Chernoff 懸念は充足）
- [`code/mcmc_fit_all_bins.py:534`]
- 前 iter cross-review P-6 で Chernoff 境界補正を要求したが、f_halo≥0 の境界検定の漸近有意度は
  Z=sqrt(q₀)=sqrt(2ΔlnL)（Cowan et al. 2011, Chernoff 1954 の 50:50 混合と整合）であり、
  現行実装は正しい。境界 MLE で自動的に 0σ になる挙動（Bin1, Bin12-13, 領域 C）も正しい。
  → この点は **通過**（新たな修正不要）。

### I-3. スペクトル形状は Totani と整合するが、それだけでは DM を支持しない
- 依頼観点 4 への回答。halo テンプレートは dN/dE=const（E²dN/dE∝E²）を内包し、f_halo_i が
  補正するので、再構成 E²dN/dE ∝ f_halo_i·E_i²。数値化すると（相対値）:
  Bin1≈1.9, Bin3≈617, Bin4≈939, Bin5≈1007, **Bin6≈1088（ピーク）**, Bin7≈890, Bin8≈625,
  Bin9≈401, …, Bin11-13≈90-100。**12-21 GeV でピーク、Bin1(1.5GeV) 無検出、高エネで低下**は
  Totani (2025) の 20 GeV ピーク・2 GeV 以下ゼロと**定性的に整合**。ただし有意度のピークは
  Bin4(7.28 GeV, 17.4σ) で 20 GeV より低エネ側に寄る。
- **重要**: この Totani 的スペクトルは C-1 と両立してしまう。20 GeV 付近にスペクトル構造を持つ
  何か（バブル本体の spectral feature、あるいは GALPROP ICS/gas の mismodeling）が
  バブル領域に在り、NFW テンプレートがそれを吸えば、同じスペクトルを再現できる。
  **スペクトルの一致は DM の十分条件ではない**。空間分布（C-1）が判定を支配する。

### I-4. Bin1 と高エネ側の 0.00σ は物理的に矛盾しないが、noise floor と縮退で解釈が限定される
- Bin1 0.00σ は Totani の低エネ側ゼロと整合（I-1 の通り median は無視）。
- Bin11-13 の f_halo 極小・0.00σ は、再構成 E²dN/dE がピークの ~8-10% まで低下しており
  「高エネ側で低下」と整合的だが、これらのビンは全 ROI 集計でも縮退（f_ics が 1.5-6.1 に
  暴れる: Bin13 f_ics=6.121）が激しく、halo が noise floor に埋もれているだけの可能性が高い。
  「200 GeV 以上でゼロ」の積極的確認とまでは言えない。

---

## 🟢 SUGGEST

### S-1. autocorrelation 50τ 未達は誤差幅（16/84%）の信頼性のみに影響（数値レビュア領域）
- τ_max≈200-266 に対し post-burn 5700（50τ=10000-13300 に不足、全 13 ビン・ROI 6 ケースで
  0/... 未達）。点推定（L-BFGS-B, fun_spread 1e-11〜1e-13）は凸性が経験的に裏付けられ堅牢。
  ただし I-1 の CI 上方バイアス議論は事後分布の裾に依存するため、C-1 の決定的テスト実施時は
  併せて max_n_steps 引き上げ（≥13000）を推奨。物理判定（採用不可）は誤差幅精度に依存しない。

### S-2. NFW 校正基準（緯度）の記述と実装の不一致は f_halo 絶対値の意味づけに残る（iter-001 S-2 継続）
- [`code/mcmc_fit_all_bins.py:204-222` `calibrate_nfw_norm`]: docstring は b=90° 基準だが
  実装は `jb_ref=argmax|B_C|`（グリッド最大 |b|≈59.5°）。f_halo の絶対スケール（=Totani flux との
  直接比較）を論じる前に要整理。今回の採用可否判定（空間非整合）はスケール不定に依存しないため
  CRITICAL ではないが、DM フラックスとして数値を引用する段階で必須。

---

## ✓ 通過した検証

- **f_halo 非負性（iter-001 C-1 の修正確認）**: `log_prior:302` の `NONNEG_IDX=(0,1,2,3,4,6)` と
  L-BFGS-B bounds（`_bounds_with_halo:354-356`）で全 13 ビン・ROI 6 ケースとも f_halo≥0。
  Bin1 の -173.6/90.29σ 非物理値は再発せず。
- **凸性（有界凸計画の一意性）**: μ は f についてアフィン→Poisson NLL は凸。box 制約下で
  大域最適一意。実測 fun_spread_successful_only=2e-13〜3e-9（`halo_spectrum.json` 集計
  max=3.725e-09）で経験的に裏付け。L-BFGS-B+解析勾配への切替（iter-001 数値指摘）は物理的に妥当。
- **有意度公式の境界処理**: sig=sqrt(2·max(ΔlnL,0)) は f_halo≥0 の境界検定で正しい（I-2）。
- **次元解析（iter-001 から不変）**: gas/ics/halo テンプレートとも
  [flux ph cm⁻²s⁻¹sr⁻¹MeV⁻¹]×[expmap cm²s]×[DPIX_SR sr]×[de MeV]=[counts] で整合
  （`build_templates_for_bin:249-274`）。
- **入れ子モデルの単調性保証**: no-halo 解を出発点に with-halo を解き lnL_with<lnL_noh なら
  no-halo に戻す（`fit_one_bin:529-531`）ことで ΔlnL≥0 を保証。境界 MLE で ΔlnL=0→0σ が
  領域 C・Bin1・Bin12-13 で正しく発火。
- **再現性メタ**: SEED=42 固定、base commit 76710e8＋未コミット差分、Python 3.12.3。
  結果は `results/mcmc_allbins_gasICS_v1/` にファイル化（stdout 非依存で確認）。

---

## Manager への要旨

採用可否の問いへの直接回答: **バブル-halo（および未解決の ICS-halo）空間縮退のため、Totani
20 GeV ハロー超過の再現としては依然採用不可。** 非負制約は iter-001 の非物理値を除去した点で
前進だが、その代償として「領域 A は正・領域 C は負」という空間非整合を 0 で床止めして隠蔽した。
これは「符号反転の解消」ではなく「置き換え」である。判定を確定するには C-1 推奨のテスト
（バブル外領域 C 単独での全ビン halo フィット、または A/C 共有 f_halo の LRT）が必要。
