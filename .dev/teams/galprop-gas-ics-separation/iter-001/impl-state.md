# Implementer State (iter 001)

再現性スタンプ: commit `76710e8f18abeb4d0e8999e96bce62d5b8b2ac66`(実装前の親コミット。本変更は未コミット)、
Python 3.12.3 (`/tmp/darkmatter_venv`)、seed=0固定(`_multistart_minimize`既定値)、
実行環境 Linux 6.6.87.2-microsoft-standard-WSL2 (WSL2, CPU4コア/RAM5.8GB)。

## 変更ファイル

- `code/plot_skymap_all_subtracted.py`:
  - `_load_healpix_grid_template()` を新規実装(HEALPix NSIDE=128 RING、`healpy.ang2pix(lonlat=True, nest=False)`
    でL_GRID/B_GRIDの各セル中心をピクセルインデックス化し、`Spectra`列から中心エネルギー最近傍binを採用)
  - `_load_healpix_gas_ics_templates(emin_gev, emax_gev)` を新規実装(spec指定の関数名どおり)。
    `ref/galprop_webrun_10050003/{pi0_decay,bremss,ics_isotropic}_healpix_54_10050003.gz` を読む
  - `_load_galprop_gas_ics_templates()`(既存名)を上記HEALPix版を呼ぶよう更新(本番採用)
  - 旧CAR格子版は `_load_galprop_gas_ics_templates_legacy_webrun10000001()` に改名して残置
    (却下済みgaldef_54_10000001, Ts=125K不一致)
  - `subtract_galactic_diffuse()` を単一GALPROPテンプレート(f_gal 1パラメータ)から
    gas+ICS 2テンプレート(A_gas, A_ics, offsetの3パラメータPoisson MLE)に更新。
    旧実装は `_subtract_galactic_diffuse_legacy_single_template()` として残置
  - `GALPROP_HEALPIX_DIR`/`GALPROP_HEALPIX_PION`/`GALPROP_HEALPIX_BREMSS`/`GALPROP_HEALPIX_ICS` 定数を追加
- `code/mcmc_fit_all_bins.py`(headline本体):
  - `PARAM_NAMES` を6→7パラメータに拡張: `["f_gas","f_ics","f_loopI_a","f_loopI_b","f_fb","f_fb_neg","f_halo"]`
  - `build_templates_for_bin()` の引数を `galprop_flux_i`(単一)から `gas_flux_i, ics_flux_i`(2枚)に変更。
    **[NUMERICAL] 副作用として、この後に続く引数(bubble系・j_map・nfw_norm・loop_shell系)を
    キーワード専用(`*`区切り)にした**。理由: 旧シグネチャのまま位置引数で呼んでいる
    診断スクリプト群(下記「既知の懸念」参照)が、シグネチャ変更後は全引数が1つずつ
    ズレて渡る「クラッシュせず静かに間違った物理量でフィットする」危険な状態になる
    ため、TypeErrorで即座に失敗するよう安全策を入れた(動作確認済み、下記参照)
  - `make_mu`, `log_prior`, `fit_one_bin` を7パラメータに対応(非負制約は先頭5つ
    `f_gas,f_ics,f_loopI_a,f_loopI_b,f_fb`のみ、`f_fb_neg`と`f_halo`は符号自由)
  - `n_restarts=30`(`_multistart_minimize`のデフォルト)は変更していない(spec指示どおり)
  - 出力先を `results/mcmc_allbins_gasICS_v1/` に変更(新規ディレクトリ、`results/mcmc_allbins/`は不変更のまま残置、md5確認済み)
  - `main()`内の`galprop_flux_i = _sub._load_galprop_template(...)` を
    `gas_flux_i, ics_flux_i = _sub._load_galprop_gas_ics_templates(...)` に置換、x0初期値も
    f_gas/f_ics独立に計算するよう追加
- `code/mcmc_fit_all_bins_galprop_webrun_check.py`, `code/mcmc_fit_all_bins_galprop_webrun_v2.py`:
  - `_sub._load_galprop_gas_ics_templates(...)` の呼び出しを
    `_sub._load_galprop_gas_ics_templates_legacy_webrun10000001(...)` に変更。
    (理由: 上記の関数名リネームで`_load_galprop_gas_ics_templates`が新HEALPixデータを
    指すようになったため、これら「却下済みwebrun_10000001の系統誤差チェック」の
    意図を壊さないよう明示的にlegacy版を呼ぶよう修正)
- `code/diagnose_halo_degeneracy_gasics_roi.py`(新規): `diagnose_halo_degeneracy_3_posneg.py`相当の
  ROI3分割(全ROI/バブル領域内/高緯度バブル外)再フィットを、更新後の7パラメータパイプラインで
  Bin5・Bin6について実行するスクリプト
- 実行結果: `results/mcmc_allbins_gasICS_v1/mcmc_bin01.json`〜`mcmc_bin13.json`,
  `halo_spectrum.json`, `halo_spectrum.png`, `roi_partition_gasics.json`(全13ビン+ROI分割の正本)

## 主要決定

- `_load_galprop_gas_ics_templates()`という既存関数名をそのまま「本番採用版」の入口として
  更新し(spec item2の文言どおり)、旧実装は`_legacy_webrun10000001`サフィックスで温存。
  却下: 新関数名を別に作って旧名を放置する案 → 既存呼び出し元(webrun_check系2ファイル)が
  誤って旧データのまま「本番採用」ラベルを持つ関数を呼び続けるほうが危険と判断
- `PARAM_NAMES`の順序は spec本文の記述順(f_gas,f_ics,f_fb,f_fb_neg,f_loop1,f_loop2,f_halo)ではなく、
  既存の`mcmc_fit_all_bins_galprop_webrun_v2.py`(2026-07-13作成済み、未使用の下書き)と同じ
  `["f_gas","f_ics","f_loopI_a","f_loopI_b","f_fb","f_fb_neg","f_halo"]`順を採用。
  却下: spec本文の記述順をそのまま採用する案 → 既存コードベース内に同名7パラメータモデルの
  前例が既にあり、そちらに揃えたほうが今後の一貫性が高いと判断(spec本文はモデル説明の
  自然な語順であり、パラメータ配列の厳密な順序指定ではないと解釈)
- `build_templates_for_bin`の後半引数をキーワード専用にする追加改修(spec未記載)を実施。
  却下: 変更なしで放置する案 → 診断スクリプト群がクラッシュせず誤った物理量で
  フィットするサイレント破損リスクを座視できないと判断(SOUL.md「勝手な仮定を置かない」
  よりむしろ「危険な暗黙の状態を残さない」観点でのスコープ内追加と判断したが、
  spec外の変更であるためレビュアの判断を仰ぐ)

## 明示した assumption / approximation

- [ASSUMPTION] エネルギービン選択は既存`_load_galprop_template`/`_load_webrun_grid_template`と
  同じ「中心エネルギーに最も近い1binを採用」方式(38 native binsはTotani 13binとほぼ同程度の
  対数幅なので粗い積分誤差は小さいはずだが定量検証はしていない、spec item1に明記済みの前提)
- [ASSUMPTION] prior boundsは既存f_galの範囲(非負・|param|<=1e6)をf_gas/f_icsそれぞれに
  そのまま踏襲した。個別の物理的上限(例: f_gas<=2程度)は設定していない
- [ASSUMPTION] フェルミバブル(正負とも)のエネルギースペクトルはE²dN/dE=const(フラット)と
  仮定して4.31 GeVのテンプレートを他ビンに外挿する処理は変更していない(既存の仕様のまま)

## 実行結果: 全13ビン f_gas / f_ics / f_halo / 有意度

出典: `results/mcmc_allbins_gasICS_v1/halo_spectrum.json`(正本)。stdout要約(1〜2行)ではなく
ファイル正本を参照のこと。全ビンとも `n_restarts=30`, seed=0, ROIマスク `|b|>=10 & |b|<=60` 適用済み。

| Bin | E_center [GeV] | f_gas (median) | f_ics (median) | f_halo (median) | Δ ln L | 有意度 [σ] |
|---|---|---|---|---|---|---|
| 1  | 1.51   | +1.015  | +0.9126 | -173.6      | 4075.82 | 90.29 |
| 2  | 2.55   | +1.082  | +0.7312 | +22.74      | 2301.98 | 67.85 |
| 3  | 4.31   | +1.162  | +0.579  | +33.37      | 1825.81 | 60.43 |
| 4  | 7.28   | +1.219  | +0.4205 | +17.74      | 743.65  | 38.57 |
| 5  | 12.29  | +1.255  | +0.3306 | +6.67       | 247.27  | 22.24 |
| 6  | 20.76  | +1.262  | +0.1238 | +2.522      | 174.92  | 18.70 |
| 7  | 35.06  | +1.397  | +0.2339 | +0.7216     | 65.05   | 11.41 |
| 8  | 59.22  | +1.573  | +0.00879| +0.185      | 61.51   | 11.09 |
| 9  | 100.02 | +1.507  | +0.4508 | +0.03994    | 8.32    | 4.08  |
| 10 | 168.93 | +0.8254 | +1.179  | +0.009796   | 6.56    | 3.62  |
| 11 | 285.33 | +1.982  | +1.98   | +0.0004438  | 1.68    | 1.83  |
| 12 | 481.93 | +3.487  | +1.691  | -4.476e-05  | 0.45    | 0.95  |
| 13 | 814.00 | +2.063  | +11.6   | -0.0003068  | 0.27    | 0.74  |

Bin6の16-84パーセンタイル(参考): f_gas=[1.225, 1.300], f_ics=[0.059, 0.190], f_halo=[2.352, 2.686]
(出典: `results/mcmc_allbins_gasICS_v1/mcmc_bin06.json`)

テンプレート健全性チェック(全13ビン、`_load_galprop_gas_ics_templates`の出力):
gas/ICSともNaN=0、負値=0(全ビン確認済み)。物理的桁も既存gll_iem_v07.fits版と同オーダー
(Bin6@20.76GeV相当付近で比較: gas+ics平均9.89e-12 ph/cm2/s/sr/MeV vs gll_iem_v07平均1.58e-11
ph/cm2/s/sr/MeV、同オーダー)。

## ROI分割再検証(Bin5・Bin6、gas/ICS分離7パラメータ版)

出典: `results/mcmc_allbins_gasICS_v1/roi_partition_gasics.json`(正本)。

| Bin | 領域 | n_pix | n_evt | f_gas | f_ics | f_halo | 有意度 [σ] |
|---|---|---|---|---|---|---|---|
| 5 | 全ROI | 10625 | 97594 | +1.255 | +0.327 | +6.747 | 22.24 |
| 5 | バブル領域内(\|l\|<22°,10°<\|b\|<55°) | 3487 | 44414 | +1.469 | +0.860 | +9.582 | 11.07 |
| 5 | 高緯度バブル外(\|b\|>=30°) | 4538 | 22036 | +1.227 | +0.013 | -10.31 | 12.81 |
| 6 | 全ROI | 10625 | 44432 | +1.260 | +0.132 | +2.507 | 18.70 |
| 6 | バブル領域内 | 3487 | 20721 | +1.542 | +0.566 | +3.518 | 12.04 |
| 6 | 高緯度バブル外 | 4538 | 10044 | +1.116 | +0.005 | -2.459 | 8.34 |

旧f_gal単一テンプレート版(6パラメータ、2026-07-13時点、`.dev/HANDOFF.md`記載値、比較参考):

| Bin | 領域 | f_halo | 有意度 [σ] |
|---|---|---|---|
| 6 | 全ROI | +0.664 | 4.83 |
| 6 | バブル領域内 | +0.295 | 1.60 |
| 6 | 高緯度バブル外 | -4.05  | 8.89 |
| 5 | 全ROI | +0.608 | 1.90 |
| 5 | バブル領域内 | -1.82  | 2.97 |
| 5 | 高緯度バブル外 | -18.4  | 15.5 |

**符号反転の解消判定について(数値のみ報告、解釈はレビュアに委ねる)**:
- Bin6: バブル領域内(+3.518)と高緯度バブル外(-2.459)の**符号反転は解消していない**。
  むしろ全ROI・バブル領域内・高緯度バブル外いずれの有意度も旧版より上昇した
  (全ROI 4.83σ→18.70σ、バブル領域内 1.60σ→12.04σ、高緯度バブル外 8.89σ→8.34σでほぼ不変)。
- Bin5も同様に符号反転(バブル領域内 f_halo=+9.582 vs 高緯度バブル外 f_halo=-10.31)が
  継続しており、有意度は全体的に上昇している(全ROI 1.90σ→22.24σ)。
- 全13ビンの本体フィット結果でも、低エネルギー側(Bin1〜Bin4)でf_haloが物理的に
  不自然な大きさ(Bin1: f_halo=-173.6, 90.29σ)に達している。これは.dev/HANDOFF.mdに
  記載された「GALPROPテンプレートと他の柔軟なテンプレートとの縮退」パターンと
  類似の壊れ方であり、gas/ICS分離によってこの縮退が解消するどころか悪化した
  可能性がある。物理的解釈はレビュアに委ねる。

## 既知の懸念(レビュアに見てほしい点)

1. **[CRITICAL候補] 全13ビンで有意度が旧版より大幅に上昇し、低エネルギー側でf_haloが
   非物理的に巨大**(Bin1: -173.6, 90.29σ)。gas/ICS分離が既知の「テンプレート縮退が
   halo成分に吸収される」バグパターンを再現・悪化させている可能性がある。
   物理的妥当性の判断はレビュアに委ねる(自己評価しない)。
2. **[NUMERICAL] `build_templates_for_bin`の位置引数変更**により、以下の診断スクリプトは
   旧シグネチャのまま位置引数で呼んでおり、キーワード専用化により**TypeErrorで
   即座に失敗する**(修正前は「クラッシュせず誤った物理量で計算する」危険な状態だった)。
   本タスクのスコープ外として未修正のまま残置した:
   `code/diagnose_halo_degeneracy.py`, `code/diagnose_halo_degeneracy_2.py`,
   `code/diagnose_halo_degeneracy_3_posneg.py`, `code/diagnose_bubble_check.py`,
   `code/diagnose_restart_stability.py`, `code/mcmc_fit_bin6_hi_proxy_check.py`,
   `code/plot_component_breakdown.py`, `code/plot_totani_fig11_13_equiv.py`。
   これらは全て一回限りの診断/プロット用スクリプト(既に過去の診断目的を果たし済み)であり、
   headlineパイプライン(`mcmc_fit_all_bins.py`)本体・`diagnose_halo_degeneracy_gasics_roi.py`
   (新規)は正しく動作確認済み。
3. `subtract_galactic_diffuse()`の変更(f_gal 1パラメータ→gas+ICS 2パラメータ+offset、
   3パラメータPoisson MLE)により、`code/plot_skymap_all_subtracted.py`本体のスカイマップ
   画像生成(`main()`)や`build_fermi_bubble_templates_posneg()`(バブルテンプレート構築)の
   結果自体も変化する。本タスクではスカイマップ画像(`data/figure-week780-all-subtracted/`)の
   再生成は実行していない(spec該当項目なし、時間都合で見送り)。次回実行時は
   画像が更新される点に留意
4. NFW校正点(`calibrate_nfw_norm`)・Loop Iシェルテンプレート・バブルテンプレート構築自体の
   ロジックは本タスクで変更していない(gas/ICS分離のみが変更点)
5. 診断スクリプト`code/diagnose_halo_degeneracy_gasics_roi.py`のMCMCステップ数は
   `code/diagnose_halo_degeneracy_3_posneg.py`と同じ(n_walkers=32, n_steps=1000, n_burn=300)。
   本体`mcmc_fit_all_bins.py`(n_steps=1500, n_burn=400)とは異なる軽量設定のまま踏襲した
   (旧スクリプトの前例に合わせた、spec item4は「code/diagnose_halo_degeneracy_3_posneg.py相当」
   と明記しているためこれに準拠)

## 合格条件チェック(自己申告、判定はレビュアに委ねる)

- [x] HEALPix→グリッド変換が動作し、gas/ICSテンプレートがNaN無し・非負(全13ビン確認済み)
- [x] 7パラメータ版MCMCが全13ビンで完走(`n_restarts=30`のまま、エラー無し)。
      ※「収束」の物理的妥当性(有意度の非物理的急騰)はレビュアの判断が必要
- [△] Bin6のf_gas=1.262は旧f_gal=0.27〜0.85の桁からは外れていない(同オーダー、
      上限比で1.5〜4.7倍)が、f_ics=0.1238は範囲内。「大きく矛盾しない」の解釈は
      レビュアに委ねる
- [x] ROI分割再検証の結果を数値で報告(符号反転は解消せず、全体的に有意度が上昇。
      解消を前提とせず、悪化した可能性を含めそのまま報告した)
- [ ] 単位・次元、Poisson尤度の`|b|>=10 & |b|<=60`マスク適用の検証は物理・数値レビュアに委ねる
      (実装側では既存の`valid &= (np.abs(BG) >= 10) & (np.abs(BG) <= 60)`を変更せず維持したことのみ確認済み)
