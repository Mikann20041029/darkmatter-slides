# SPEC — GALPROP gas/ICS 独立テンプレート化 (galdef SLZ6R30T150C2)

## 背景・目的

Totani (2025) §2.3 のbaseline手法は、銀河系拡散放射を gas 成分(pion decay + bremsstrahlung)と
ICS 成分(inverse Compton, baseline は isotropic 合算のみ)の**独立した2テンプレート**として
Poisson尤度フィットする。現行パイプラインは `ref/gll_iem_v07.fits` 単一テンプレート(自由パラメータ
`f_gal` 1個)で代用しており、CRITICAL TODOとして記録済み(`.dev/TODO.md`進行中セクション参照)。

2026-07-15、教授から galdef `SLZ6R30T150C2` (Title: "Lorimer distribution, z_h = 6, R_h = 30,
T_S = 150, and E(B-V) cut = 2") で計算済みのGALPROP webrun出力(`ref/galprop_webrun_10050003/`)
を入手した。以下で照合済み:
- `HIR_filename = rbands_hi12_v2_qdeg_zmax1_Ts150_EBV_mag2_limit.fits.gz` (Ts150、却下済みTs125と別物)
- `source_parameters_1=1.9, source_parameters_2=5.0` (Lorimer+2006標準値と一致)
- `ISRF_file = ISRF/Standard/Standard.dat`, filetype=3

## データ仕様

`ref/galprop_webrun_10050003/*.gz` は HEALPix形式FITS (astropy.io.fitsでgzip透過的に開ける):
- `PIXTYPE=HEALPIX`, `ORDERING=RING`, `NSIDE=128` (196608ピクセル)
- 拡張1 (`SKYMAP`): 各ピクセルに38個のエネルギービンの強度値(`Spectra`列, 単位: intensity, GALPROP標準の
  ph cm^-2 s^-1 sr^-1 MeV^-1 のはず。既存 `_load_webrun_grid_template` の単位系と要照合)
- 拡張2 (`ENERGIES`): 38個のエネルギー値(MeV, 50 MeV〜814 GeVの対数等間隔)

使う総和済みファイル(17リング×3ガス種別の手計算は不要、GALPROPが既に合算済み):
- `pi0_decay_healpix_54_10050003.gz` + `bremss_healpix_54_10050003.gz` → **gas成分**
- `ics_isotropic_healpix_54_10050003.gz` → **ICS成分** (baseline、isotropic合算のみ。
  `ics_isotropic_comp_{1,2,3}_healpix` は光学/FIR/CMB個別成分で今回は使わない)

galdef本体は `ref/galprop_webrun_10050003/galdef_54_10050003` に保存済み(小さいのでgit管理下)。

## やること

1. **HEALPix→解析グリッド変換関数の新規実装**
   - `code/plot_skymap_all_subtracted.py` に `_load_healpix_gas_ics_templates(emin_gev, emax_gev)` を追加
   - `healpy.ang2pix(nside=128, l, b, lonlat=True, nest=False)` で `L_GRID`/`B_GRID` の各セル中心が
     属するHEALPixピクセルを求め、該当ピクセルの `Spectra` 列から該当エネルギービンの値を取り出す
   - エネルギービンの選び方は既存 `_load_galprop_template`/`_load_webrun_grid_template` と同じ
     「中心エネルギーに最も近い1binを採用」方式を踏襲する([ASSUMPTION]として明記。38 native binsは
     Totani 13binとほぼ同程度の対数幅なので粗い積分誤差は小さいはずだが、定量検証はしていない)
   - 既存の `_load_galprop_gas_ics_templates()` (旧`galprop_webrun_10000001`用、CAR格子読み込み)は
     置き換えるか、`_load_galprop_gas_ics_templates_v2`等の新関数として追加し、呼び出し元を新関数に
     切り替える。旧関数・旧WEBRUN_DIR定数は「却下済みデータ、比較用に残す」ことが分かるコメントを付けて残置してよい

2. **`subtract_galactic_diffuse()` および `mcmc_fit_all_bins.py` の更新**
   - 現在は `f_gal` 1パラメータで `template = _load_galprop_template(...)` (gll_iem_v07.fits) を使っている
   - これを `f_gas`, `f_ics` の2パラメータ + 2テンプレートに置き換える
   - MCMC自由パラメータ次元 `NDIM` を6→7に拡張(既存: iso固定, f_gal, f_fb, f_fb_neg, f_loop1, f_loop2, f_halo
     → 変更後: iso固定, f_gas, f_ics, f_fb, f_fb_neg, f_loop1, f_loop2, f_halo)
   - `_multistart_minimize` の `n_restarts=30` は現行のまま維持(パラメータ数拡大で局所解バグが
     再発した前例があるため、まずは30のままで様子を見る。再発時のみ増やす)
   - 初期値・prior boundsは既存の `f_gal` の範囲を参考に `f_gas`/`f_ics` それぞれに妥当な範囲を設定

3. **全13ビン再フィット・結果保存**
   - `results/mcmc_allbins_gasICS_v1/` (新規、既存 `results/mcmc_allbins/` は上書きしない)
   - 各ビンの `f_gas`, `f_ics`, `f_halo` 等と有意度を出力

4. **頑健性再検証**
   - `code/diagnose_halo_degeneracy_3_posneg.py` 相当のROI分割再フィット(フェルミバブル領域内 vs
     高緯度域外)をこの新パイプラインで再実行し、符号反転(+7.78σ↔−9.04σ、Bin6基準)が解消するか確認

## 合格条件

- [ ] HEALPix→グリッド変換が動作し、gas/ICSテンプレートがNaN無し・物理的に妥当な値域(非負)で得られる
- [ ] 7パラメータ版MCMCが全13ビンで収束する(局所解バグの再発がないことを`n_restarts=30`で確認)
- [ ] Bin6の `f_gas`, `f_ics` が物理的に妥当な範囲(既存 `f_gal=0.27〜0.85` の桁と大きく矛盾しない)
- [ ] ROI分割再検証の結果(符号反転が解消したか否か)を数値で報告する。**解消を前提にしない**
      (CRITICAL: 解消しなかった場合もそれ自体が重要な結果であり、失敗として隠さず報告すること)
- [ ] 単位・次元(dimensional-check相当)、Poisson尤度計算の`|b|>=10 & |b|<=60`マスク適用(既存不変条件)を
      物理・数値レビュアがそれぞれ検証する

## 追記 (iter-003、2026-07-16): フェルミバブル正負テンプレートのROI制限バグ

iter-002のレビューで、gas/ICS分離後も「バブル領域内外でのf_haloの空間非一様性」
(高緯度バブル外で無制約フィットが負のhaloを要求する)が解消しないことが判明した。
ユーザーとの議論の結果、Totani (2025) §3.1原文を再確認したところ、決定的な実装の
乖離が見つかった。

**論文原文(p.6-7)**: "the map of positive regions, **regardless of whether it is
inside or outside the boundaries of the flat template**, will be used as the
energy-independent template for the bubbles"

→ Totaniの正負残差テンプレートは**ROI全域**(|l|≤60°, 10°≤|b|≤60°)の残差マップを
符号で分けたものであり、矩形境界に制限されない。「flat template」(旧来の矩形バブル
モデル)への言及はあるが、構造化テンプレートはそれとは独立にROI全体に及ぶ。

**現状のバグ**: `code/plot_skymap_all_subtracted.py:493-552`
`build_fermi_bubble_templates_posneg()`が、残差を`bubble_region`
(`|l|<22° & 10°<|b|<55°`)という矩形の**外側で強制的にゼロ**にしている
(`resid = np.zeros_like(counts); resid[valid_px] = counts[valid_px]`、
`valid_px = bubble_region & ~isnan`)。この結果、高緯度バブル外領域では
`f_fb_neg`(GALPROPモデル不一致由来の負残差を吸収するはずのテンプレート)が
常にゼロとなり、そこにある負の残差を吸収する手段が無いため、代わりに`f_halo`が
負に引っ張られていた可能性が高い。これがiter-001/002で見えていた
「符号反転」「縮退」の真因候補である。

### iter-003でやること

1. `build_fermi_bubble_templates_posneg()`を、`bubble_region`矩形制限を撤廃し、
   ROI全域(既存の有効ピクセルマスク `|b|>=10 & |b|<=60`、`|l|<=60`)の残差を
   使うよう修正する。正負分割・Gaussian smoothing(σ=1°)のロジックは変更しない。
2. `bubble_region`変数が他の箇所(ROI分割診断`diagnose_halo_degeneracy_gasics_roi.py`
   の領域定義等)でも使われている場合、意図を確認した上で影響を精査する
   (診断スクリプト側の「バブル領域内 vs 高緯度域外」という领域分割自体は
   引き続き妥当な診断手法なので、テンプレート構築側の制限撤廃と混同しないこと)
3. 全13ビン再フィット・ROI分割再検証(Bin5・Bin6)を再実行し、高緯度バブル外領域の
   f_haloが今度こそ0近傍(境界MLEではなく、非負制約時に正の側から見て0)に
   収束するか、あるいは無制約再最適化でもう負に落ちなくなるかを確認する

## 追記 (iter-004、2026-07-16): 有意度超過の原因究明 + 数値バグ(N-1)修正

iter-003でバブルテンプレートのROI制限バグを修正した結果、region A/Cの符号反転は
解消したが、全13ビンで有意度がTotani報告値(13-19σ)を大きく上回った
(Bin6: 15.55σ→25.45σ)。原因は未解明のまま。iter-003の物理レビュアが提案した
「gas:ICS比固定テスト」はTotani (2025) p.4「The GALPROP model radiation is divided
into two components, gas and ICS, which are fitted independently」と矛盾するため
**却下済み**(Managerがconsolidated-feedbackで訂正)。代わりに以下を行う。

### iter-004でやること

1. **[数値、優先] N-1修正**: `neg_log_likelihood_and_grad`(`code/mcmc_fit_all_bins.py:323`
   付近)の解析的勾配が`make_mu`のクリップ(mu下限1e-10)を考慮していない。クリップが
   発火する画素では勾配寄与を0にする(`clipped = raw_mu < 1e-10; factor[clipped]=0`)
   よう修正すること。現状のheadline結果(有意ビン1-11)は汚染されていないが、
   Bin12/13のwith-halo最適化で全5始点がABNORMAL終了する原因になっており、
   将来的なsilent誤収束リスクを塞ぐ。修正後、全13ビン(特にBin12/13)を再フィットし、
   ABNORMAL終了が解消したか確認すること。
2. **[物理、優先] Totani §4.1のICSスペクトル自然性チェックを定量再現する**:
   論文原文(p.21-22)の基準は「ハローを含めてフィットしてもICSスペクトルが
   不自然(non-power-law)にならなければ、ICS-halo縮退は深刻ではない」という
   ものである。具体的には:
   - with-halo(現行7パラメータ)とno-halo(6パラメータ、halo除外)それぞれで
     全13ビンのICSフラックス(f_ics × テンプレート平均値、物理単位)を計算する
   - 両者のICSスペクトル形状(log E vs log flux)を比較し、halo追加によって
     ICSスペクトルが大きく歪む(power-law的でなくなる)かどうかを定量評価する
     (例: 隣接ビン間のべき指数の変化、またはpower-law fitの残差)
   - Totaniは「59 GeVビンのdipはhalo無しでも存在する既知の異常で、21 GeVビン
     (halo最大)ではdipが見られない」ことを歪みが小さい根拠としている。
     本実装で同様の比較を行い、結果を報告する
3. **[物理] 有意度超過(25-28σ vs Totani 13-19σ)の機構分析**: iter-002→iter-003で
   何が変わったことでΔlnLが増加したのか、以下の観点で分析する:
   - no-haloモデル・with-haloモデルそれぞれのlnL値(絶対値)がiter-002→iter-003で
     どう変化したか(ΔlnLの増加が、片方だけの改善によるものか両方の変化によるものか)
   - fb_neg(ROI全域に拡大)とhaloテンプレートの空間相関(iter-003物理レビュアが
     一部計算済み、`iter003_template_correlation.json`参照)が、有意度上昇と
     定量的にどう関係するか

### 合格条件(iter-004)

- [ ] N-1修正後、全13ビンでABNORMAL終了(特にBin12/13)が解消するか確認済み
- [ ] Totani §4.1基準でのICSスペクトル自然性チェックの結果を数値で報告済み
      (歪みが小さい/大きいの両方の可能性を排除せず報告すること)
- [ ] 有意度超過の機構分析の結果を報告済み(原因が特定できなくても、調査した
      内容と結果を正直に報告すること)

## やらないこと (今回のスコープ外)

- ICS成分のanisotropic分離(baseline=isotropicのみ、Totaniの手法通り)
- ガスリング別(17本)の個別フィット(Totani baselineは合算1テンプレートのみ)
- GALPROP系統誤差チェック(gll_iem_v07.fits版との差分定量化)は次のタスクとして後回し
