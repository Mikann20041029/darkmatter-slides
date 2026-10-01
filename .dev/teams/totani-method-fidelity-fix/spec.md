# Spec — Totani (2025) 手法忠実性の修正: 尤度セル粒度 + f_halo符号制約

Tier: M(物理+数値の両観点)。MAX_ITER: 5。opus使用(スコープが大きく、過去のCRITICAL判定の
一部を覆す内容を含むため)。

## 背景

Totani (2025) 原文(`ref/20Gev_gamma_ray.paper.2025-Nov-23.pdf`)を精読した結果、現行パイプラインが
これまで一度も検証していなかった2つの手法上の乖離を発見した。ユーザーからの明示的な指示
「論文を精読し、パイプラインが本当に論文を再現できているか初心に帰って検証する」に基づき、
この2点を修正し、修正が非物理的な高有意度(全13ビンでTotani報告13-19σを超える25-34σ)に
どう影響するかを検証する。

### 乖離1: 尤度計算のセル粒度(§2.2)

原文引用:
> "Photon count maps and exposure maps with pixel scales of ∆lp = ∆bp = 0.125° ... resulting
> in 960×960 pixels in the ROI... we divide the ROI into 12×12 cells with a width of
> ∆lc = ∆bc = 10° and calculate the likelihood based on photon counts and expectations
> **in these cells**... smoothing at coarse resolutions may reduce the impact of pixel-scale
> mismatches between a model map and data on the likelihood estimate."

Totaniはマップ自体は0.125°ピクセルで作るが、**Poisson尤度計算は10°×10°セル(ROI全体
|l|≤60°,|b|≤60°で12×12=144セル)に粗く束ねてから行う**。理由も明記されており、
「粗いセルで尤度計算すると、ピクセル単位のモデル-データ食い違いが尤度に与える影響を
減らせる」——つまりTotani自身が、細かい粒度で尤度計算すると偽の高有意度が出ることを
見越して、あえて粗くしている。

現行パイプライン(`code/mcmc_fit_all_bins.py`の`log_likelihood()`)は、1°ピクセル
(有効ピクセル約9,000-12,000個)を直接Poisson尤度の項として使っており、この粗め化を
一度もしていない。この事実は`docs/totani2025_reading_guide_ja.md:133`に2026-06-18時点で
既に記録されていたが、実装には反映されていなかった。

### 乖離2: f_haloの符号制約(§2.3, §3.2)

原文引用:
> "the fitting parameters are limited to the range fl > 0 for known components such as
> point sources, the GALPROP models, the isotropic component, and Loop I, **but fl < 0 is
> allowed for the halo components**, which are explored as unknown components."

§3.2では実際に「最低エネルギービンでhaloがマイナスになった」との記述があり(Fig.8)、
baselineはf_haloの符号を自由にしている。

現行ヘッドライン(`code/mcmc_fit_all_bins.py:145`)は`NONNEG_IDX = (0, 1, 2, 3, 4, 6)`
(index 6 = f_halo)としており、**f_haloを非負制約**している。これは`.dev/teams/
galprop-gas-ics-separation/iter-001`で「DM fluxは物理的に非負のはず」という物理的判断で
追加されたものだが、論文の実際の手法とは照合されていなかった。非負制約は統計的に
「境界MLE」を生み、ノイズがマイナス側に振れられないぶん有意度を一方的に押し上げる
バイアスを生む(弱い信号のビンほど深刻)。

## 修正方針

### 1. 尤度セル粒度の10°化

- 現行の1°ピクセルグリッド(L_C, B_C、120×120)上のカウント・各テンプレートを、10°×10°
  セル(l方向12セル、b方向12セル、うち|b|<10°の disk 2行は解析対象外なので実質10行×12列=120
  セルがhalo探索フィットで有効になるはず)に集約してからPoisson尤度を計算するよう変更する
- 集約方法: 各セル内の**有効(valid)ピクセルのみ**を合算する(点源マスク・|b|<10°除外は
  現行のpixel-levelマスクをそのまま踏襲し、セル単位ではなくピクセル単位でマスクしたものを
  セル内で合算する)。全ピクセルが無効なセルは尤度計算から除外する
- `Cexp,i`(セルiの期待カウント)は`Σ_{k∈cell i} μ_k`(μ_kはパラメータについてアフィンなので、
  セル合算後もアフィン性は保たれる)。勾配 `d(lnL)/df_k = Σ_i (Cobs,i/Cexp,i - 1) · T_k,i`
  (T_k,i はテンプレートkのセルi内合算値)として解析的勾配を再導出すること
  (ピクセル単位の既存の解析勾配の考え方をセル単位に一般化するだけでよい)
- クリップ(`mu = max(raw_mu, 1e-10)`)は**セル単位**の`Cexp,i`に対して適用する
  (ピクセル単位のクリップとは別物になることに注意)
- 論文の12×12という数字はROI全体(|l|≤60°,|b|≤60°、disk含む)に対するものである。
  halo探索フィット(disk除外|b|≥10°)では、10°セルの境界がちょうど|b|=10°と一致するため
  (10°の倍数)、disk内に完全に収まる2行のセル(b∈[-10,0], [0,10])は自然に除外される
  はずである。この整合を数値健全性チェックで確認すること

### 2. f_haloの符号制約撤廃

- `NONNEG_IDX`からindex 6(f_halo)を除外し、`SIGNFREE_IDX`に追加する
  (`SIGNFREE_IDX = (5, 6)`、f_fb_negとf_haloがともに符号自由になる)
- bounds生成関数(`_bounds_with_halo`等)のf_halo項を`(0.0, None)`から`(None, None)`に変更
- 多点始動(`_multistart_minimize`)がSIGNFREE_IDXパラメータに対して負領域も探索することを
  確認する(過去に`np.abs()`が符号自由パラメータの探索を破壊したバグがあったため、
  同種の問題が再発していないか必ず確認すること)
- 有意度の定義`sig = sqrt(2*max(ΔlnL,0))`は、f_halo=0がno-haloモデルとして常にwith-haloモデルの
  パラメータ空間の内点(境界ではない)になるため、Wilks定理のχ²(1)近似がより素直に成立する
  ことに注意(非負制約時に生じていた境界MLEの漸近論の不確実性が解消される、というのが
  期待される副次効果)

## 検証・合格条件

1. **ablation設計**: 以下3パターンを全13ビンで実行し、比較すること(原因の切り分けのため)
   - (a) セル粒度10°化のみ(f_haloは非負制約のまま)
   - (b) f_halo符号自由化のみ(尤度はピクセル粒度のまま)
   - (c) 両方(a)+(b)を同時適用
   - いずれもベースは現在のworking treeの状態(cos(b)修正済みのv2_cosb相当)に対する追加変更とする
2. **出力**: 各ablationを別ディレクトリに保存し、既存の`results/mcmc_allbins_gasICS_v2_cosb/`は
   上書きしない
   - (a): `results/mcmc_allbins_gasICS_v3a_cellbin/`
   - (b): `results/mcmc_allbins_gasICS_v3b_signfree/`
   - (c): `results/mcmc_allbins_gasICS_v3c_both/`
3. **物理**: セル集約後もCexp,iがf_kについてアフィンであること・クリップの位置(セル単位)・
   次元整合を確認する。負のf_haloが実際に出現した場合、Totani Fig.8のように低エネルギー
   ビンで負になるという定性的傾向と整合するか確認する
4. **数値**: 解析勾配と有限差分の一致確認(セル集約後の新しい勾配式で再検証必須)。
   全13ビンでの多点始動収束(fun_spread)。f_haloが符号自由になったことで多点始動が
   負領域を正しく探索しているかの確認(過去のnp.abs()バグの再発がないか)
5. **報告**: 3パターンそれぞれで全13ビンの有意度がどう変化したか定量的に報告する。
   「Totani報告値(13-19σ)に近づいた/近づかなかった」という評価は実際の数値に基づいて
   書くこと。断定を避け、まだ残る乖離があればそれも明記すること
6. 再現性メタデータ(seed, commit hash, python/numpy/scipy version)を結果jsonに埋め込むこと

## 非目標(スコープ外)

- ピクセル解像度自体(0.125°への変更)は本機のメモリ制約により対象外(既存の判断を維持)
- 点源処理方式(spectral subtraction vs NaN mask)の切り替えは既に別タスクで検証済みのため対象外
- ICS-halo縮退問題への対応は別タスク
