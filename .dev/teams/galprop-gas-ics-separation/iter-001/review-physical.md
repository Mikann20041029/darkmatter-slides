# Physical Review (iter 001)

## 判断（結論先頭）

**この結果は採用不可。ただし「テンプレートの単位・符号・エネルギービン選択のバグ」ではない。**
gas/ICS テンプレート自体は物理的に健全（次元整合・エネルギー整合・非負・ics/gas≈0.75）。
病理はフィットモデルの仕様にある。最大の原因は **f_halo に符号自由を許していること**
（物理的に DM ハローは非負）で、これに **ICS↔halo の中程度の空間縮退**（相関 r≈0.75）と
**最適化の未収束による ΔlnL 水増し**が重畳している。Bin1 の f_halo=-173.6 / 90.29σ は
「負の NFW 成分の検出」であり物理的に無意味。再修正（下記 CRITICAL）後に再走が必要。

---

## 🔴 CRITICAL

### C-1. f_halo が符号自由 — DM ハロー振幅の非負性違反（最重要）
- [`code/mcmc_fit_all_bins.py:238-249` `log_prior`], [`:316-339` `fit_one_bin`]
- DM 由来フラックスは annihilation なら ∝ ρ²（J-factor, 常に ≥0）、decay なら ∝ ρ（≥0）。
  NFW J-map (`nfw_j_map`) は全域 ≥0。したがって物理的に `f_halo ≥ 0` が必須。
  現状 `log_prior` は非負制約を先頭5パラメータ (`f_gas,f_ics,f_loopI_a,f_loopI_b,f_fb`) のみに課し、
  `f_halo` は符号自由。結果、Bin1 で f_halo=-173.6（90.29σ）等、**負の NFW 形状成分**を
  「検出」している。これは DM 信号ではなく、モデル残差を NFW 形状で吸わせているだけ。
- 有意度 `significance = sqrt(2·ΔlnL)` は片側検定量だが、MLE が f_halo<0 に落ちた場合の σ は
  DM 検出の証拠として意味を持たない。全 13 ビンの σ 値（および符号）は現状では信頼できない。
- **推奨修正**:
  1. `log_prior` と `fit_one_bin` の非負制約に `f_halo ≥ 0` を追加（6→先頭6パラメータ、
     ただし `f_fb_neg` の扱いは C-3 参照）。
  2. 有意度は Chernoff (1954) の境界補正付き片側 LRT に統一：
     `sig = sqrt(2·max(ΔlnL,0))` を `f_halo_MLE > 0` のときのみ非ゼロとし、
     境界 (f_halo=0) の MLE では 0σ とする。
  3. 再走後、f_halo=-173 のような非物理値と 90σ は消えるはず。まずこれで切り分ける。

---

## 🟡 IMPORTANT

### I-1. ICS↔halo の空間縮退が halo 振幅を暴走させる二次原因
- ROI（|b|=10–60, |l|≤60, 1°×1°）での標準化テンプレート形状の Pearson 相関（Bin6）:
  gas-ics=0.705, **ics-halo=0.747**, gas-halo=0.605。
  halo 形状を {gas,ics,loopI} で最小二乗再構成した決定係数 R²(halo|gas,ics)=0.57
  （Bin1 0.62 / Bin6 0.57 / Bin8 0.55）。→ NFW ハロー形状の約 55–60% は拡散テンプレートで
  再現可能。5テンプレート標準化設計の条件数は ~3.5（特異ではない＝**中程度**の縮退）。
- ただし f_halo が符号自由（C-1）だと、この中程度の縮退でも ICS と halo が大きな
  相殺振幅を取り合える。実際の結果がこれを裏付ける:
  - **f_ics が非物理的に抑圧**: Bin6 で f_gas=1.262 に対し f_ics=0.124。
    テンプレートは物理的に ics≈0.75×gas（下記 I-2）なので、GALPROP 規格化が正しければ
    f_gas≈f_ics≈1 のはず。ICS を物理値の ~1/8 まで潰して、その分を halo（f_halo=2.5）が
    肩代わりしている。
  - **ROI 分割での f_ics↔f_halo 連動**: バブル領域内 (f_ics=0.57, f_halo=+3.5) と
    高緯度バブル外 (f_ics=0.005, f_halo=-2.5)。ICS が許される所では halo が大きな正、
    ICS が 0 に潰れる所では halo が負。真の DM ハローは空間固定で振幅が
    サブ ROI 間で符号反転しない。この反転は縮退吸収の兆候であり、符号反転が
    「解消しなかった」のは freeing ICS が原因を除去せずむしろ自由度を増やしたため（想定通り）。
  - **f_ics のビン間挙動が erratic**: 0.91,0.73,0.58,0.42,0.33,0.12,0.23,0.009,0.45,1.18,1.98,1.69,11.6。
    較正振幅なら O(1) で安定すべき。~0 や 11.6 まで振れるのは ICS がこの ROI/解像度で
    実質的に制約されていない証拠。一方 f_gas は Bin1–8 で 1.0–1.6 と安定（gas は円盤集中で
    よく決まる）。→ 「gas は分離できるが ICS は halo/iso と縮退」という当初懸念は的中。
- **推奨修正（C-1 修正後になお過剰有意度が残る場合）**:
  - f_gas, f_ics に物理事前分布を課す。これらは GALPROP 規格化済み拡散成分であり
    自由振幅ではない。例: 各々 log-normal もしくは Gaussian prior を 1.0 中心・σ~0.3 程度に。
    現状の flat [1e-6, 1e6] は ICS に halo と取り合う無制限の自由を与えている。
  - あるいは gas+ICS を単一の物理和として規格化を 1 パラメータで括り、
    gas:ICS 比を GALPROP 予測値に固定（Totani baseline は独立2成分だが、
    高緯度低解像度で分離不能なら比固定が保守的）。

### I-2. gas:ICS 光度比の物理妥当性 — テンプレートは正常
- 懸念された「ICS が gas の 1/10」は **フィット値 f_ics/f_gas の見かけ**であって
  テンプレートの物理比ではない。テンプレート実測比（Bin6, ROI 合算）は
  **sum(ics)/sum(gas)=0.75**、ピクセル中央値 0.89。緯度依存も物理的
  （|b|10–20°:0.76, 20–30°:0.68, 30–45°:0.72, 45–60°:0.93 — 高緯度で ICS 比が上昇、
  拡散度の高い ICS が高緯度で相対的に効くという GALPROP 標準挙動と整合）。
  → gas/ICS テンプレートの規格化・符号は物理的に妥当。ここにバグはない。

### I-3. 最適化未収束による有意度水増し（数値レビュア領域、物理影響あり）
- `significance=sqrt(2ΔlnL)`、ΔlnL は no-halo(6D) と with-halo(7D) の独立 multistart
  Nelder-Mead 差分。`f_ics` 追加で no-halo 空間が 5D→6D に拡大。
  `_multistart_minimize` のコメント自身が前例を記録: Bin3 で n_restarts 8→30→60 に対し
  29.4σ→20.6σ→4.68σ（restart 増で no-halo 側が改善し σ 低下）。パラメータが 1 つ増えた今、
  **n_restarts=30 が再び不足し ΔlnL を水増ししている疑い**が強い（旧版 4.83σ→新版 18.70σ の
  跳ね上がりの一部はこれで説明可能）。数値レビュアに no-halo 収束の再検証（restart 増や
  収束判定）を依頼すべき。物理的には C-1 修正と併せてこれを潰さない限り σ 値は採用不可。

---

## 🟢 SUGGEST

### S-1. 符号自由な広がった成分が2つ（f_fb_neg と f_halo）＋抑圧可能な ICS でモデルが過柔軟
- `f_fb_neg`（バブル負テンプレート, 符号自由）も広がった残差を吸う nuisance。
  f_halo 非負化（C-1）後も、f_fb_neg と ICS と halo の間に残る自由度が過剰有意度を
  残しうる。モデル自由度の最小化（f_fb_neg を本当に必要か再検討、または prior で締める）を推奨。

### S-2. NFW 校正基準の記述と実装の緯度不一致（既存・今回スコープ外）
- `calibrate_nfw_norm` のコメントは「b=90°」だが実装はグリッド最大 |b|≈59.5° を使用
  (`jb_ref=argmax|B_C|`)。norm の絶対スケール（=f_halo の絶対値の意味づけ）に効く。
  今回の変更点ではないが、f_halo の物理解釈を論じる前に要整理。

---

## ✓ 通過した検証

- **次元解析**: `gas_tmpl = gas_flux[ph cm⁻² s⁻¹ sr⁻¹ MeV⁻¹] × expmap[cm² s] × DPIX_SR[sr] × de_mev[MeV]
  = [counts]`。ICS・halo も同一構造で counts に帰着。μ=iso+Σfᵢ·Tᵢ の各項が counts で整合
  （`build_templates_for_bin`, `plot_skymap_all_subtracted.subtract_galactic_diffuse`）。
- **エネルギービン選択**: GALPROP native 38 bins（50 MeV–814 GeV）の最近傍採用は全 13 ビンで
  Totani 中心の 0.966 倍（≤3.4% ずれ）に収まり、off-by-one/軸取り違えなし。
- **テンプレート健全性**: gas/ICS とも NaN=0・負値=0（impl 報告を追認、Bin6 で再確認）。
  ics/gas 比 0.75（ROI 合算）は GALPROP 標準の高緯度 gas:ICS 比と整合。
- **HEALPix 投影**: `hp.ang2pix(nside=128, lonlat=True, nest=False)` は ORDERING=RING と整合。
