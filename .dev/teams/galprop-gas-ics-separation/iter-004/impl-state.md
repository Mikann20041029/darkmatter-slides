# Implementer State (iter 004)

## 変更ファイル

- `code/mcmc_fit_all_bins.py`:
  - **N-1修正**: `make_mu`のクリップ計算を`_raw_mu()`として分離し、
    `neg_log_likelihood_and_grad()`でクリップ発火画素(`raw_mu < 1e-10`)の
    勾配寄与を`factor=0`にするよう修正(`np.where(clipped, 0.0, 1.0 - c/mu)`)。
  - `build_templates_for_bin()`の戻り値に`gas_flux_raw`/`ics_flux_raw`
    (物理単位のGALPROP生フラックス、ph cm^-2 s^-1 sr^-1 MeV^-1)を追加。
  - `fit_one_bin()`の戻り値に`params_no_halo_pointest`(no-haloモデル6パラメータの
    L-BFGS-B点推定)、`lnL_no_halo`/`lnL_with_halo`(絶対NLL値の符号反転)、
    `gas_flux_mean_valid_phcm2sMeV`/`ics_flux_mean_valid_phcm2sMeV`
    (有効ピクセル平均の生フラックス)を追加。ICSスペクトル自然性チェックと
    有意度機構分析の両方がこれらのフィールドに依存する。
- `results/mcmc_allbins_gasICS_v1/mcmc_bin01.json`〜`mcmc_bin13.json`,
  `halo_spectrum.json`, `halo_spectrum.png`: N-1修正後コードで13ビン再フィットし
  上書き保存(`np.random.seed(42)`固定)。
- `results/mcmc_allbins_gasICS_v1/iter004_before_N1fix/mcmc_bin{01..13}_before.json`,
  `halo_spectrum_before.json`: N-1修正**前**の状態を退避(iter-003終了時点、
  比較用に保持)。
- `results/mcmc_allbins_gasICS_v1/_iter004_lnL_mechanism_analysis.py` +
  `iter004_lnL_mechanism_analysis.json`: 有意度超過の機構分析用診断スクリプト・
  正本データ(下記「機構分析」参照)。
- `results/mcmc_allbins_gasICS_v1/_iter004_ics_naturalness_check.py` +
  `iter004_ics_naturalness_check.json`, `ics_sed_comparison.png`:
  ICSスペクトル自然性チェック用スクリプト・正本データ・図。

## 主要決定

- no-haloモデルの不確実性はMCMC事後分布を別途走らせず、L-BFGS-B点推定
  (`res_nh.x`)のみを保存する方針を採用。代替案(no-haloモデルもMCMCで走らせる)は
  却下: with-haloモデルは既にMCMC実行済みで、no-halo側は「スペクトル形状比較の
  中心値」だけが目的(spec item 2は「振幅の点推定の比較」で成立する要求であり、
  誤差帯の要求はない)なので、13ビン×2回のMCMC実行という追加コストに見合わないと判断。
- 有意度超過の機構分析は、iter-002のraw JSONバックアップが本タスク開始前に
  削除済みで参照不能だったため、OLD(bubble_region矩形制限、iter-002以前の
  バグを再現)とNEW(ROI全域、iter-003修正後=現行本番)の2種類のバブルテンプレートを
  **本iterのスクリプト内で独立に再構築**し、それ以外(N-1修正済みの勾配関数、
  イベントデータ、gas/ICS/LoopI/NFWテンプレート、乱数シード)を完全に同一にして
  比較する方式を採った。これによりiter-002→iter-003の変化のうち「バブル
  テンプレートのROI拡大」だけを厳密に分離でき、N-1バグの影響(以前の本番結果に
  混入していた可能性)を排除した「クリーンな」比較になる。代替案(iter-002を
  git等から復元する)は、`results/mcmc_allbins_gasICS_v1/`がgit未追跡
  (untracked、当初のgit status参照)でiter-002時点のコミットが存在しないため
  不可能だった。
- ICSスペクトルの物理量は「f_ics(振幅)× ROI有効ピクセル平均の生ICSフラックス
  (GALPROP予測値そのもの、ph/cm2/s/sr/MeV)× E^2」と定義した。代替案
  (ピクセルごとのマップとして比較する)は却下: Totani §4.1の主張は「スペクトル
  **形状**が不自然にならないか」という積分的な問いであり、ROI平均intensityの
  エネルギー依存性を見るのが直接対応する([ASSUMPTION]として明記)。

## 明示した assumption / approximation

- [ASSUMPTION] no-haloモデルの不確実性はL-BFGS-B点推定のみ(MCMC事後分布なし)。
- [ASSUMPTION] ICSスペクトル自然性チェックは「f_ics × ROI平均生フラックス × E²」を
  SEDの代理指標とする。ピクセル単位の空間分布の歪みは評価対象外。
- [ASSUMPTION] Totani原文の「21 GeVビン」は本パイプラインのBin6(20.76 GeV)、
  「59 GeVビン」はBin8(59.22 GeV)に対応すると解釈した(既存のROI分割診断
  `diagnose_halo_degeneracy_gasics_roi.py`がBin5/Bin6を「haloが最大のビン」として
  扱っている既存の解釈と整合)。
- [ASSUMPTION] "dip"の定量的定義はTotani原文に明示の数式がないため、隣接ビン間の
  局所べき指数(`d(log SED)/d(log E)`)の符号・大きさで代替評価した。

## 1. N-1修正(数値バグ)の結果

### 修正内容

`neg_log_likelihood_and_grad()`の解析的勾配が`make_mu()`のクリップ(`mu`下限
1e-10)を考慮していなかった。`_raw_mu()`(クリップ前の生のmu)を新たに分離し、
`clipped = raw_mu < 1e-10`の画素では`factor=0`として勾配寄与をゼロにするよう
修正した。

### 全13ビンでのn_failed_starts(5始点中の失敗数)比較: 修正前 vs 修正後

| Bin | no_halo 修正前 | no_halo 修正後 | with_halo 修正前 | with_halo 修正後 |
|---|---|---|---|---|
| 1 | 1 | 0 | 0 | 0 |
| 2 | 3 | 0 | 1 | 0 |
| 3 | 3 | 0 | 1 | 0 |
| 4 | 2 | 0 | 1 | 0 |
| 5 | 2 | 0 | 1 | 0 |
| 6 | 2 | 0 | 1 | 0 |
| 7 | 2 | 0 | 1 | 0 |
| 8 | 2 | 0 | 1 | 0 |
| 9 | 2 | 0 | 2 | 0 |
| 10 | 1 | **1(未解消)** | 3 | 0 |
| 11 | 0 | 0 | 4 | 0 |
| 12 | 1 | 0 | **5(全滅)→0** | **0** |
| 13 | 1 | 0 | **5(全滅)→0** | **0** |

想定より影響範囲が広く、**with-haloモデルは全13ビンでABNORMAL終了が解消**した
(Bin12/13の全5始点全滅は完全に解消)。no-haloモデルもBin10を除く全ビンで解消。
Bin10のno-haloのみ1/5始点が修正後も失敗するが、成功した4始点は
`fun_spread_successful_only=0.0`で一致しており(`mcmc_bin10.json`参照)、
最終結果(best選択)には影響しない。原因はBin10固有の別の数値要因(クリップとは
無関係の可能性、scale=1.5開始点固有のscipy内部の収束判定)の可能性があるが、
本iterのスコープ外として深掘りしていない。

### Bin12/13の結果変化

| Bin | 有意度 修正前 | 有意度 修正後 | f_halo 修正前 | f_halo 修正後 |
|---|---|---|---|---|
| 12 (481.93 GeV) | 0.00σ(with-halo全滅によるno-haloフォールバック) | 1.33σ | 0.0 (フォールバック) | 0.000649 |
| 13 (814.00 GeV) | 0.00σ(同上) | 0.48σ | 0.0 (フォールバック) | 0.000195 |

Bin12/13は以前「with-halo最適化が全滅→no-haloに強制フォールバック(delta_lnL=0,
sig=0.00σ固定)」だったが、修正後は真のwith-halo最適化が収束し、微小だが非ゼロの
有意度(1.33σ, 0.48σ)を得た。**有意ビン(1-11)の点推定・有意度は完全に不変**
(全て小数点以下まで一致、下記iter-002→iter-003比較でも確認済み)であり、
consolidated-feedback-003の「headline結果は汚染されていない」という判断は
本修正でも裏付けられた。

### 残った懸念

- Bin13のwith-haloモデルで、5始点のうち1つ(scale=1.5)が`success=True`のまま
  他4始点と大きく異なる目的関数値(1014.90 vs 4794.49)に収束する
  (`fun_spread_successful_only=3779.59`、`mcmc_bin13.json`参照)。ABNORMAL終了
  ではなく「scipyがsuccessと判定する別の停留点」であり、`best_res`選択ロジック
  (min fun)により最終結果は汚染されていないが、N-1修正でクリップ由来の勾配誤りが
  消えたことで露呈した別の非平坦性(クリップの非平滑性由来の局所的な非凸性)の
  可能性がある。数値レビュアの判断を仰ぐ。
- Bin10のno-halo 1/5始点失敗は未解消(上記参照)。

## 2. Totani §4.1 ICSスペクトル自然性チェックの結果

正本: `results/mcmc_allbins_gasICS_v1/iter004_ics_naturalness_check.json`,
図: `results/mcmc_allbins_gasICS_v1/ics_sed_comparison.png`。

with-halo(7パラメータ、MCMC中央値f_ics)とno-halo(6パラメータ、L-BFGS-B点推定
f_ics)それぞれについて、ICS SED(= f_ics × ROI平均生ICSフラックス × E²、単位
MeV cm^-2 s^-1 sr^-1)を全13ビンで計算した。

### 全体的な歪み指標

- 隣接ビン間の局所べき指数(`d(log SED)/d(log E)`)の差(with − no-halo)の
  RMS = **0.843**、最大絶対差 = **1.888**(Bin8-9ペア、59.22→100.02 GeV)。
- 全13ビンでの単純global power-law fit(log SED vs log E, 最小二乗)の
  傾き: with-halo = -0.553、no-halo = -0.472(近い値)。
  ただし残差RMS: with-halo = 0.472、no-halo = 0.239。**with-haloの方が
  単純べき乗則からの残差が約2倍大きい** = with-haloのSEDはno-haloよりも
  単一power-lawからの逸脱が大きい。

### Totaniが言及する具体的な特徴点との対応

- **Bin8(59.22 GeV)の"dip"**: 隣接ペア「7-8」の局所指数は with-halo=-2.763,
  no-halo=-0.987。**両モデルともBin7→Bin8で急減(dip自体はhalo無しでも存在)**
  というTotaniの記述と定性的に整合する。ただしdipの深さ自体はwith-haloの方が
  約2.8倍急峻(-2.76 vs -0.99)であり、「halo無しでも存在するのと**全く同じ形**」
  とまでは言えない。
- **Bin6(20.76 GeV、halo最大)の周辺**: 隣接ペア「5-6」の局所指数はwith-halo=
  -1.084, no-halo=-0.468(差-0.615)、ペア「6-7」はwith-halo=-0.262,
  no-halo=-0.290(差+0.027、ほぼ一致)。Bin6直後(6-7)ではwith/no-haloの形状差は
  ほぼ消えるが、Bin6直前(5-6)では顕著な差がある。「21 GeVビンでdipが見られない」
  というTotaniの記述(dipという急減構造がないこと)自体はBin6周辺で両モデルとも
  確認でき整合するが、Bin6直前の傾きの差は無視できない大きさである。

**結論(事実のみ、解釈は物理レビュアに委ねる)**: Totaniが明示的に言及する
「Bin8のdipの存在」「Bin6でdipが見られないこと」という**定性的**特徴は本実装でも
再現された。しかし歪みの**定量的な大きさ**(RMS index diff=0.843、global
power-law残差がwith-haloで約2倍)は無視できるほど小さいとは言えず、
「ICS-halo縮退は深刻ではない」と結論するにはさらなる判断基準が必要である。
歪みが小さい/大きいのどちらの解釈も排除せず報告する。

## 3. 有意度超過(25-28σ vs Totani 13-19σ)の機構分析

正本: `results/mcmc_allbins_gasICS_v1/iter004_lnL_mechanism_analysis.json`
(N-1修正済みの勾配関数を使い、OLD=bubble_region矩形制限テンプレート、
NEW=ROI全域テンプレートの2バージョンで完全に同一条件下(同一イベントデータ、
同一gas/ICS/LoopI/NFW、同一シード)の点推定lnLを比較。NEWは
`_sub.build_fermi_bubble_templates_posneg()`本番関数と数値的に一致することを
`np.allclose`で確認済み)。

### no-halo/with-haloそれぞれのlnL絶対値変化(iter-002相当→iter-003相当)

| Bin | E(GeV) | lnL_noh OLD | lnL_noh NEW | ΔlnL_noh | lnL_wh OLD | lnL_wh NEW | ΔlnL_wh | sig OLD | sig NEW |
|---|---|---|---|---|---|---|---|---|---|
| 2 | 2.55 | 3496888.34 | 3516048.19 | +19159.86 | 3496894.91 | 3516130.91 | +19236.00 | 3.63 | 12.86 |
| 3 | 4.31 | 1313316.30 | 1324191.43 | +10875.13 | 1313402.76 | 1324406.39 | +11003.63 | 13.15 | 20.73 |
| 4 | 7.28 | 445019.70 | 448920.77 | +3901.08 | 445170.99 | 449326.99 | +4155.99 | 17.40 | 28.50 |
| 5 | 12.29 | 133796.45 | 135391.33 | +1594.88 | 133930.51 | 135781.60 | +1851.09 | 16.37 | 27.94 |
| 6 | 20.76 | 25633.94 | 26320.35 | +686.41 | 25754.77 | 26644.10 | +889.32 | 15.55 | 25.45 |
| 7 | 35.06 | -3157.61 | -2924.40 | +233.22 | -3096.84 | -2744.11 | +352.73 | 11.02 | 18.99 |
| 8 | 59.22 | -9185.49 | -9123.96 | +61.52 | -9156.65 | -9020.25 | +136.41 | 7.59 | 14.40 |
| 9 | 100.02 | -7509.50 | -7466.35 | +43.15 | -7501.37 | -7425.92 | +75.45 | 4.03 | 8.99 |
| 10 | 168.93 | -5061.33 | -5072.74 | -11.41 | -5058.32 | -5052.44 | +5.88 | 2.45 | 6.37 |

(全13ビンの完全な値は`iter004_lnL_mechanism_analysis.json`参照。Bin1/11/12/13は
sig<2σと小さいため上表では省略。`sig OLD`はiter-003 impl-state記載の値と
Bin2-9まで完全一致し、この再構築方式が正しくiter-002相当の状態を再現している
ことを検証済み)。

**観測事実**: 全ビンで no-halo・with-halo **両方**のlnLがOLD→NEWで増加した
(=フィット全体が改善した)。しかし増分は**with-haloの方が常に大きい**
(例: Bin6は+686.41 vs +889.32、差+202.9)。これが有意度上昇(ΔlnL=lnL_wh-lnL_noh
の増加)の直接的な機構である。つまり:

1. **fb_neg(ROI全域拡大)を追加すると、halo無しモデルの適合度自体が大幅に改善する**
   (以前は矩形外の負残差を吸収する手段が無く、gas/ICS/LoopIが代わりに苦しい
   フィットを強いられていたと考えられる)。
2. **with-haloモデルの改善幅はno-haloモデルの改善幅を常に上回る**ため、
   両者の差(ΔlnL、有意度)が拡大する。

### fb_neg-halo空間相関との関係

`iter003_template_correlation.json`(iter-003物理レビュア計算、Bin3/5/6共通の
テンプレート形状相関、データのfit結果ではなくテンプレート同士の相関)によると、
fb_negとhaloのPearson相関は:

| 領域 | fb_neg-halo相関 | R²(halo on 全6テンプレート) |
|---|---|---|
| full_roi (10625px) | +0.145 | 0.53-0.56 |
| A_bubble (3487px) | +0.382 | 0.82-0.86 |
| C_highlat_ex_bubble (4538px) | -0.474 | 0.75-0.79 |

full_roi(実際のフィットに使われる領域)でのfb_neg-halo相関は+0.145と弱いが、
`R²_halo_on_all6`(6テンプレートでhalo空間パターンをどれだけ説明できるか)は
full_roiで0.53-0.56と中程度あり、領域分割(A/C)ではさらに高い(0.75-0.86)。
これは「fb_negが単独でhaloと強く相関している」というより「6テンプレート全体の
線形結合がhaloパターンをかなり説明できる」ことを示しており、fb_negのROI拡大が
この全体の説明力にどう寄与したかは本データだけでは分離できない。**fb_neg-halo
相関だけを見れば「弱い」が、モデル全体のROI全域への拡大が上記の通りno-halo/
with-halo両方のlnLを大きく改善させている以上、相関係数の大小だけで有意度上昇を
説明しきれるとは言えない**。この点はデータのみ報告し、解釈は物理レビュアに
委ねる。

## 既知の懸念(レビュアに見てほしい点、iter-003から継続)

- 全13ビンで`50τ充足=False`(既知の継続懸念、本iterでも未解消、対応スコープ外)。
- Bin1(1.51 GeV)は有意度0.00σだが、with-haloモデルのMCMC posterior medianの
  f_halo=3.20(90%区間0.26-9.58)と、point estimateのフォールバック挙動が
  整合しない可能性がある(delta_lnL=0.0のためフォールバックのはずだが、
  posterior medianは非ゼロ)。これは修正前後で値が完全一致しており本iterの
  変更由来ではないが、観察事実として記録する。深掘りはしていない。
- ICS↔halo縮退(iter-003指摘、r=0.71-0.86)は本iterでも未解決。

## 前回(iter-003)consolidated-feedbackへの対応

- [N-1、数値] 対応済み。上記「1. N-1修正の結果」参照。想定より広範囲
  (全13ビンのno-halo/with-halo双方)に影響していたことが判明。
- [ICSスペクトル自然性チェック、物理] 対応済み。上記「2.」参照。定性的特徴
  (Bin8 dip存在、Bin6 dip不在)は再現されたが、定量的な歪みの大きさは
  無視できるとは言えない結果になった。
- [有意度超過の機構分析、物理] 対応済み。上記「3.」参照。原因は「fb_negの
  ROI全域拡大がno-halo/with-halo両モデルのlnLを改善させ、その改善幅が
  with-haloで常に大きい」という機構までは特定できたが、**なぜwith-haloの
  改善幅がno-haloより一貫して大きいのか**(テンプレート間の真の縮退なのか、
  ROI全域のGALPROPモデル不一致構造とhaloのJ-factor空間分布がたまたま
  部分的に相関する縮退なのか)は未解明のまま。
