# Physical Review (iter 001) — DPIX_SR cos(b) 立体角補正

## 🔴 CRITICAL
なし。cos(b)補正の数式・calibrate_nfw_norm・勾配・NFW J-factorの独立性については、いずれも実装が物理的に正しいことを確認しました。

## 🟡 IMPORTANT

- **[`code/mcmc_fit.py:86-163`] Bin6専用旧スクリプトのハロー(NFW)テンプレートにcos(b)修正が未適用**。同ファイル101行目でGALPROPテンプレート`G`にのみ`PIX_SOLID_ANGLE_SR`を適用しているが、ハロー項`H`(129-152行)は`NFW_SCALE = 2.378e-3`という**ハードコードされた較正定数**を使っており、これは`PIX_SOLID_ANGLE_SR`を一切参照していません。この定数はTotani Fig.8較正点から手計算で導出されたもの(コメントのみで導出過程は再現不可)で、旧スカラー立体角を暗黙に前提にしています。
  impl-state.mdは「`build_templates()`内の局所`DPIX_SR`を...配列に同期」と記載していますが、これは`gal`テンプレートのみに当てはまり、`halo`テンプレートは未同期のままです。spec.mdは明示的に「同様に同期する」ことを要求しており(過去のVALID_MASK修正の前例踏襲)、この点で修正は不完全です。
  さらに重要なのは、**この不完全な同期がヘッドライン(`mcmc_fit_all_bins.py`)より状態を悪化させている**可能性です。修正前は`gal`も`halo`も同じ(誤った)フラットな立体角を共有しており、両者の相対形状には整合性がありました。修正後は`gal`だけがcos(b)込みに変わり、`halo`は変わらないため、両テンプレート間に新たな人為的な非整合が生じています。本ファイルはheadlineではないため実害の緊急性は低いですが、「同期済み」という記述は不正確であり、修正するか、最低限「halo項は未同期」と明記すべきです。

- **[`code/mcmc_fit_all_bins.py:301-334`, `plot_skymap_all_subtracted.py:234-284`] Loop Iテンプレートを「既にcounts空間」と分類した根拠が誤り**。impl-state.mdは「iso・loopI・fb/fb_negは既にcounts空間の量なのでcos(b)を掛けない」としていますが、`loop_i_shell_templates()`が返すのは3次元シェルの視線積分**経路長(kpc単位)**そのものであり、`build_templates_for_bin()`内で`li_a = loop_shell1`と代入されるだけで、`expmap_i`・`PIX_SOLID_ANGLE_SR`・`de_mev`のいずれも一切乗じられていません(iso/fb/fb_negとは異なり、そもそも物理フラックス→counts変換の経路を通っていません)。つまりLoop Iは「counts空間にある」のではなく「単位も較正もない自由振幅の形状テンプレート」であり、iso(実データcounts平均)やfb/fb_neg(実データcounts残差、後述参照)とは性質が全く異なります。
  実務上の判断(cos(b)を掛けない)自体は今回のスコープ外の問題(そもそもexposure/dE変換も欠落している)であり妥当と考えますが、**記載されている理由付けは事実と異なる**ため、コメント修正を推奨します(「loopIは既にcounts空間」ではなく「loopIは自由振幅の幾何形状テンプレートで、そもそも物理フラックス変換を経ていない。cos(b)単独の追加は、exposure/ΔEも同時に追加しない限り中途半端な部分修正になるため見送った」という記述が正確)。

## 🟢 SUGGEST

- **[`code/mcmc_fit_all_bins_galprop_webrun_v2.py:150,159`] `mfa._multistart_minimize()`呼び出しが`bounds`引数を欠いており、既にTypeErrorで実行不能**。これは2026-07-15 iter-2で`_multistart_minimize`に`bounds`必須引数が追加された際に本ファイルが追従していなかったためで、今回のcos(b)修正とは無関係の既存の技術的負債です。spec.mdが要求する「グリッド形状の整合確認」自体は`mfa.PIX_SOLID_ANGLE_SR`参照(78,88,89,100行目)がshape (120,120)で正しく揃っており問題ありません。ただし「#1の修正が自動反映される」という前提は、そもそも本ファイルが実行できないため検証不能である点は明記すべきです。
- **iso(等方背景)の緯度依存性の非対称な扱い**: `iso_level`は`|b|>=50`平均カウントを算出し、ROI全域(`|b|=10-60`)にフラットに適用しています。cos(b)修正後、gas/ics/haloは正しく高緯度で減衰しますがisoは不変のままです。これは物理的に「isoは実データcounts平均であり二重に立体角を掛けるべきでない」という判断自体は正しいものの、`|b|=10-60`の範囲でcos(10°)/cos(60°)=1.97倍の立体角変化があるため、「真に等方な物理フラックス」を仮定するなら本来isoもb依存で変化すべきという別の(今回のバグとは独立な)モデリング上の単純化が存在します。今回の修正範囲外ですが、低エネルギービンでの残差の系統的な取りこぼしに寄与しうる観点として記録に値します。

## ✓ 通過した検証

- **次元解析**: `gas_tmpl = gas_flux_i[ph cm⁻² s⁻¹ sr⁻¹ MeV⁻¹] × expmap_i[cm² s] × PIX_SOLID_ANGLE_SR[sr] × de_mev[MeV] = ph`(無次元カウント)で、スカラーから配列への変更後も次元は保たれる。
- **cos(b)公式の導出**: 球面座標で緯度bを赤道(銀河面)からの角度と定義すると`dΩ = cos(b)·db·dl`(極角θ=90°-bとしてdΩ=sinθ dθ dφの標準形と一致)。1°グリッドで`ΔΩ(b) = (π/180)²·cos(b)`は正しい微小面積要素。
- **極限b=0**: `health_check.json`で`ratio_at_b0_over_scalar = 0.99996`(最近傍セルb=-0.5°、cos(0.5°)相当)。旧スカラーと厳密一致。
- **対称性b→-b**: `health_check.json`で`symmetry_max_abs_err = 0.0`(cosは偶関数、厳密一致)。
- **b=60極限**: `ratio_at_b60_over_scalar = 0.5075`(理論cos(60°)=0.5、最近傍セルb=59.5°の離散化誤差として整合)。
- **ROI総立体角の解析積分との一致**: `check_dpix_cosb_health.py`の解析式`analytic = Δl_rad × 2×(sin60°-sin10°)`と数値和`sum(PIX_SOLID_ANGLE_SR[valid])`が相対誤差1.27e-5で一致(`health_check.json`)。
- **calibrate_nfw_norm()の約分保証**(`mcmc_fit_all_bins.py:247-269`): `dpix_ref = float(PIX_SOLID_ANGLE_SR[ib_ref, jb_ref])`が分子`counts_ref`・分母`norm`双方に同一のPythonスカラーとして使われており、`norm = flux/j_ref`に厳密に代数的に帰着(dpix_refの値そのものに依らず消える)。実装は主張通り正しい。
- **勾配コードのDPIX_SR非依存**(`mcmc_fit_all_bins.py:419`): `neg_log_likelihood_and_grad`はテンプレート辞書`t[...]`のみ参照し、`PIX_SOLID_ANGLE_SR`を直接参照していないことをコード上確認。
- **NFW J-factorのスコープ外妥当性**(`mcmc_fit_all_bins.py:220-236`): `nfw_j_map()`は視線積分ρ²(物理座標s,r,x)のみに依存し、ピクセルの角度サイズと無関係。立体角補正は下流の`halo_tmpl = j_map * nfw_norm * expmap_i * PIX_SOLID_ANGLE_SR * de_mev`でのみ発生しており、修正不要という主張は正しい。
- **fb/fb_negの厳密なcos(b)非依存性**(`mcmc_fit_all_bins.py:314-321`): `bubble_counts_bin3_pos/neg`は実データの残差カウント(`plot_skymap_all_subtracted.py`の`build_fermi_bubble_templates_posneg()`、iso/GALPROP/点源差引後の実測countsそのもの)であり、Bin間外挿は`exp_ratio = expmap_i/expmap_bubble_bin`という**同一ピクセル・同一グリッドでの露出比**を用いている。立体角ΔΩ(b)は分子・分母で同一ピクセルのため厳密に相殺し、Bin3→Bin_iの外挿にcos(b)を追加で掛ける必要はない。iso/fb/fb_negに関する実装の判断は物理的に正しい。
- **diagnose_regionAC_lrt_all_bins.pyの自動反映**: `mfa.build_templates_for_bin()`を再利用しているため、cos(b)修正はコード変更なしで領域A/C LRT検定に反映される構造を確認(重複実装なし)。
- **領域A/C反転の物理的整合性**: 領域A(BUBBLE_REGION、`|l|<22°, 10°<|b|<55°`)と領域C(`|b|>=30°`かつバブル外)は平均緯度が異なり、Cの方が高緯度側に偏る。修正前(v1)は高緯度ほど旧スカラー立体角が真値を過大評価する(最大2倍)ため、領域Cのhaloテンプレートが相対的に過大評価され、その分`f_halo_C`が過小(実測: Bin4でA=24.7/C=6.08)に推定されていたと考えられる。修正後、Cのテンプレートが正しく縮小されるためf_halo_Cが増加してAに近づく(Bin4でA=21.5/C=22.5、eqSig 5.40σ→0.24σ)という方向性は、この機構と定量的に整合する。数値も`results/mcmc_allbins_gasICS_v1/regionAC_lrt_all_bins.json`と`results/mcmc_allbins_gasICS_v2_cosb/regionAC_lrt_all_bins.json`を実測し、impl-state.mdの報告値と完全一致することを確認した。
- **全体13ビンで有意度が上昇する方向性**: gas(銀河面近くに強く集中、|b|=10-60内でも低b側にウェイト大)とhalo/ICS(NFWのスケール半径21kpcは銀河ガス円盤(スケール高~100pc)よりはるかに広がっており、視線積分J値はbに対してgasよりずっと緩やかにしか減衰しない)の角度分布形状の違いから、cos(b)補正(高緯度ほど強く減衰させる)はhalo/ICSの総重みをgasより相対的に大きく削る。データは変化しないため、この削られた分を補うようf_halo(およびf_ics)が増加する方向に働く。これは実測結果(全ビンでf_halo増加、低エネルギー側ほど増加幅大)と定性的に整合する。
- **数値結果の再現性**: `results/mcmc_allbins_gasICS_v2_cosb/mcmc_bin01.json`(f_halo=284.30, sig=16.45σ)、`mcmc_bin04.json`(sig=34.59σ)、`health_check.json`(Bin6: f_halo=4.487, sig=28.10σ)を直接読み、impl-state.mdの報告値と完全一致することを確認した。

## Managerへの一言要旨

**条件付き採用可**。cos(b)補正の物理・数式・calibrate_nfw_norm・勾配・NFW非依存性はすべて実装通り正しく、報告された数値もファイルから直接確認して一致した。ただし(1) `code/mcmc_fit.py`のハロー項が実際には未同期(IMPORTANT、記述訂正または追加修正が必要)、(2) Loop Iを「counts空間」と分類した記載理由が事実誤認(IMPORTANT、コメント修正推奨、結論=据え置きは妥当)の2点は次iterで手当てすべき。Bin1のf_halo(3.20→284.30、約89倍)のような極端な変動は、収束は健全(fun_spread~1.86e-9)だが強いパラメータ縮退の存在を示唆しており、「有意度上昇」を額面通りDM検出強化の根拠として扱わないよう報告書に明記することを推奨する(implementer自身も既にこの点を認識し断定を避けている)。領域A/C反転自体は数値アーティファクトではなく、cos(b)がbに応じて非対称に効くという物理的機構で定量的に説明可能であり、`.dev/teams/regionAC-lrt-halo-test/verdict.md`の結論見直しを検討する根拠として妥当と判断する。
