# Physical Review (iter 004)

## 判断（結論先頭）

**依然として採用不可。** 4 iter を通じて「機構の正しさ」(f_halo 非負性 / バブル ROI 制限 / N-1 勾配) は着実に修正されたが、**DM 解釈の成立に必要な物理的分離は一つも達成されていない**。決定的なのは今回追加された ICS 自然性チェックである。これは Totani §4.1 が「ICS-halo 縮退は無害」と主張する根拠そのものだが、**本パイプラインではその検定に不合格**する。すなわち Totani が「良性」と示した縮退が、本実装では「悪性」(ICS 形状変化が偽の halo と混同されている) 側に振れている。25σ の超過も、この悪性縮退 (gas/ICS mismodeling の肩代わり) の帰結として物理的に説明できる。

---

## 🔴 CRITICAL

### C-1. ICS 自然性チェック不合格 — with-halo の ICS SED は物理的に不自然 (Totani §4.1 の警告シナリオに該当)

正本: `results/mcmc_allbins_gasICS_v1/iter004_ics_naturalness_check.json`

これが本 iter の最重要所見です。依頼観点 1 への回答。

**(a) with-halo の ICS SED は Bin8(59 GeV) で dip-and-recover の V 字を示し、これは真の ICS 成分としてありえない形状である。**
- SED (MeV cm⁻² s⁻¹ sr⁻¹): Bin7=9.3e-5 → **Bin8=2.18e-5 (4.3倍減)** → Bin9=5.4e-5 (**2.5倍増**)。局所べき指数は 7-8 ペア=-2.76、8-9 ペア=+1.73。
- ICS は「滑らかな ISRF に対する滑らかな CR 電子分布の逆コンプトン散乱」であり、**単一エネルギービンで急落してから反発する構造を物理的に持てない**。ICS SED は必ず滑らか (単調〜緩い曲率) でなければならない。
- 対して **no-halo の ICS SED は滑らかに単調減少** (index 7-8=-0.99、8-9=-0.16)。これは物理的に自然。

→ **halo を加えた瞬間に ICS スペクトルが非物理的になる。** これは「ICS 形状変化が偽の halo と混同される」という Totani 自身が §4.1 で警告するシナリオそのものである。

**(b) f_ics が halo 有意ビンで系統的に 2〜7 倍抑圧される (halo が ICS 振幅を直接横取りしている)。**

| Bin | E(GeV) | f_ics no-halo | f_ics with-halo | 抑圧率 |
|---|---|---|---|---|
| 4 | 7.28 | 1.59 | 0.95 | 1.7× |
| 6 | 20.76 | 1.71 | 0.60 | 2.8× |
| 8 | 59.22 | 1.69 | 0.24 | **7.0×** |

- GALPROP ICS 振幅は物理計算済みテンプレートの規格化であり、halo の有無で O(1) 程度しか動かないべき (Totani の良性縮退の定義)。実測は factor 2〜7 の系統的抑圧で、しかも抑圧が **halo が効くエネルギー帯 (7-59 GeV) に集中**している。halo と ICS が同一の flux を奪い合っている決定的証拠。

**(c) 定量指標も全て「歪みは無視できない」側:** global power-law 残差 RMS は with-halo=0.472 vs no-halo=0.239 (約 2 倍)、隣接指数差 RMS=0.843、最大差 1.888 (8-9 ペア)。

**判定:** Implementer は「定性的特徴 (Bin8 dip 存在、Bin6 dip 不在) は再現、定量は無視できない」と両論併記したが、**物理的には両論併記にならない**。Bin8 の dip-recover V 字 (index -2.76→+1.73) は誤差やスペクトル微調整の問題ではなく、**ICS として存在しえない形状**である。Totani の ICS は power-law を保つ (彼の良性の根拠)。本実装の ICS は保たない。**縮退は良性ではなく悪性。** これは spec の合格条件「歪みが小さい/大きい両方を排除せず報告」を超えて、物理的に片側 (悪性) に確定できる。

### C-2. halo-ICS/gas 空間縮退の本体は未解決のまま (iter-002 C-1/C-2 が iter-003/004 で放置された)

- iter-002 review-physical C-1 が要求した決定的テスト (**バブル外領域 C 単独での全ビン halo フィット**、あるいは **A/C 共有 f_halo の LRT**) は iter-003/004 のいずれでも実行されていない。iter-002 で確定した事実「halo 信号はバブル領域 A に限局 (Bin6: A=3.5 vs C=0.03、約 116 倍)」は反証も再検証もされていない。
- `iter003_template_correlation.json` は halo の空間パターンが gas+ICS で **R²=0.53-0.56** 説明されること (ics-halo 相関 0.71-0.74、gas-halo 0.57) を示す。これは C-1 の ICS 抑圧と同じ物理の空間側の顔である。**halo テンプレートの過半は gas/ICS の線形結合で再現できてしまう** → 独立な物理成分として測れていない。
- 球対称・全天 NFW ハローは単一 f_halo で全 ROI を満たさねばならない。A 限局 (C≈0) はこの物理的要請を満たさない。**この空間非整合が解けない限り、25σ が DM である証拠にはならない。**

---

## 🟡 IMPORTANT

### I-1. 25σ 超過の機構は「gas/ICS mismodeling の肩代わり」で物理的に説明できる (依頼観点 2 への回答)

Implementer の機構分析 (OLD 矩形→NEW ROI 全域で no-halo/with-halo 両方の lnL が改善、with-halo の改善幅が常に大) を物理的に解釈すると、DM ではなく縮退側が支持される。

**機構の物理:** OLD では fb_neg が矩形外 (高緯度領域 C) でゼロだったため、領域 C の負残差 (data &lt; GALPROP) を吸収する手段が gas/ICS の押し下げしかなかった。ROI 全域 fb_neg 化でこの負残差が fb_neg に移り、gas/ICS が領域 C からの押し下げ圧力から解放される。その結果、**領域 A に残る正の NFW 状残差がよりクリーンに halo へ帰属され、有意度が上昇する**。fb_neg の ROI 拡大は Totani 原文に忠実だが、それが「あぶり出した」領域 A の正残差の正体は DM とは限らない。

**DM でなく縮退である根拠:**
1. C-1 の f_ics 抑圧 (2〜7 倍) — halo は ICS 振幅を直接奪っている。
2. no-halo でも **f_ics = 1.5〜3 (&gt;&gt;1)** — GALPROP ICS が data を 50〜200% 過小予測。これは大きな mismodeling で、fb_neg でも吸収しきれない残差の貯水池を作る。halo はここから食べている。
3. fb_neg-halo 直接相関は full_roi で **+0.145 (弱)**、R²_halo_on_fbneg_only=0.02。つまり **超過の主因は fb_neg ではなく gas/ICS** (R²_halo_on_gas_ics=0.53-0.55)。Totani (15σ) より 10σ 多い分は、本 webrun (SLZ6R30T150C2) の gas/ICS mismodeling が Totani 自身の GALPROP tuning より大きいためと整合する (f_ics≫1 がその指標)。

→ 「真の DM ハローが GALPROP 不一致構造を正しく説明している」より「**NFW の柔軟性が fb_neg で吸収しきれない gas/ICS 残差を肩代わりしている**」が物理的に優勢。C-1 の ICS 非自然性がこれを裏付ける。

### I-2. f_ics ≫ 1 (GALPROP ICS の系統的過小予測) 自体が独立の系統誤差フラグ

- no-halo でも f_ics=1.5〜3 (Bin13 で 12.4)。ICS 規格化が合っていれば f_ics≈1 のはず。50〜200% のずれは ISRF モデル or CR 電子スペクトルの mismodeling を示唆する。
- これは C-1/I-1 の貯水池であり、**Totani 再現の前提条件 (GALPROP が data を良く合わせること) が満たされていない**ことを意味する。ISRF データ (教授提供見込み、commit f5950ed 参照) を用いた再計算後に f_ics が 1 近傍に落ちるかを確認するまで、halo 有意度の物理的意味は確定しない。

### I-3. N-1 修正は物理的に正しい (勾配・次元・極限すべて通過)

- `neg_log_likelihood_and_grad:368-369` の `factor = np.where(clipped, 0.0, 1.0 - c/mu)` は正しい。raw_mu&lt;1e-10 でクリップされた画素では μ が定数 1e-10 に固定され d(μ)/d(f_k)=0 なので、その画素の勾配寄与は 0 が正解。無クリップ極限では factor=1-c/μ で標準 Poisson 勾配に帰着。次元も factor(無次元)×T_k(counts) で整合。
- ただし物理的には、iso&gt;0 かつ全テンプレート≥0 なら μ&gt;0 が保証され、クリップは発火しないはずである。クリップが発火するのは **fb_neg が符号自由 (index 5)** で `f_fb_neg·fb_neg` が大きな負値を取り μ を 0 近傍へ押すため (`build_templates_for_bin:272` fb_neg_tmpl)。これは物理的に「モデルが負の counts を予測しかけている」状態で、Bin13 で露呈した副次的停留点 (impl-state 懸念) の根であり得る。**headline 結果 (Bin1-11) は不変**で汚染なしという Implementer の主張は本 iter データで裏付けられる (機構分析の sig OLD が iter-003 と一致)。

---

## 🟢 SUGGEST

### S-1. C-2 の決定的テストを次フェーズの必須項目に

iter-002 C-1 推奨 (領域 C 単独 halo フィット / A-C 共有 f_halo の LRT) を実行しない限り、空間非整合は解けない。ICS 自然性 (C-1) と併せて、この 2 点が Totani 再現可否を最終判定する残タスク。

### S-2. ISRF 再計算後に f_ics→1 近傍を確認 / gas も同様の自然性チェックを

f_ics≫1 が ISRF mismodeling 由来なら、教授提供 ISRF での再計算後に f_ics が 1 近傍へ寄り、halo 有意度が Totani 値へ低下する可能性がある。gas 成分についても with/no-halo で同じ SED 自然性チェックを行い、halo が gas も歪めていないか確認すべき (相関 gas-halo=0.57 は無視できない)。

### S-3. 50τ 未達は物理判定に非依存 (iter-002 S-1 継続)

点推定 (L-BFGS-B, fun_spread~1e-10) は堅牢。採用不可の物理判定は誤差幅精度に依存しない。

---

## ✓ 通過した検証

- **N-1 勾配修正の物理的正しさ**: クリップ発火画素の勾配寄与 0、無クリップ極限で標準 Poisson 勾配へ帰着、次元整合 (I-3)。
- **Bin12/13 の ABNORMAL 解消**: 0.00σ(フォールバック)→真値 (1.33σ, 0.48σ)。境界 MLE でなく真の内点解に収束。物理的に妥当 (微小だが非ゼロの高エネ halo)。
- **有意ビン 1-11 の不変性**: 機構分析の sig OLD が iter-003 impl-state と Bin2-9 まで一致 → 再構築方式が iter-002 相当状態を正しく再現、headline は N-1 修正で汚染されていない。
- **入れ子モデル単調性**: ΔlnL≥0 保証と境界処理は iter-002 から不変で正しい。
- **再現性メタ**: SEED=42、base commit 76710e8+未コミット差分、production_match (pos/neg) True で本番関数と数値一致確認済み。

---

## 4 iter を通じた総括判断

**このタスクは、現時点で「Totani の 20 GeV ハロー超過の再現」として採用できない。**

**解決したこと (機構の正しさ):**
1. iter-001: f_halo 符号自由 → 非負制約で -173σ 非物理値を除去。
2. iter-003: バブルテンプレート ROI 制限バグ → Totani 原文に忠実化、region A/C 符号反転を解消。
3. iter-004: N-1 勾配/クリップ不整合 → 修正、Bin12/13 の偽 0σ を解消。

これらは全て **パイプラインの正しさ**の修正であり、DM 解釈の成立には寄与しない。

**未解決の本質的問題 (DM 解釈を阻む):**
1. **ICS-halo 悪性縮退 (C-1)**: Totani §4.1 の自然性検定に不合格。with-halo の ICS SED は Bin8 で物理的にありえない dip-recover を示し、f_ics が halo 有意ビンで 2〜7 倍抑圧される。Totani が「良性」と示した縮退が本実装では「悪性」。**これが単独で採用不可を確定させる。**
2. **halo の空間非整合 (C-2)**: iter-002 で確定した「halo は領域 A 限局 (C≈0)」が iter-003/004 で未検証のまま。全天 NFW の物理的要請を満たさない。
3. **25σ 超過の物理的解釈 (I-1)**: 機構は「fb_neg ROI 拡大が領域 A の正残差をあぶり出し halo へ帰属」。主因は fb_neg (弱相関 +0.145) ではなく gas/ICS mismodeling (R²=0.55、f_ics≫1)。Totani (15σ) 超過分は本 webrun の GALPROP mismodeling が大きいことの反映。

**結論:** region A/C 符号反転と N-1 バグは解消したが、**ICS-halo 悪性縮退という物理的核心は解消どころか今回定量的に確証された**。25σ は真の DM ではなく gas/ICS mismodeling の肩代わりと解釈するのが物理的に整合的。採用の前提として最低限、(a) C-2 の決定的テスト (領域 C 単独 halo フィット / A-C 共有 f_halo LRT)、(b) 教授提供 ISRF での再計算による f_ics→1 近傍化の確認、が必要。**これは Manager が ESCALATE すべき状態(spec自体が「Totani再現」を目標に据えているが、現GALPROP webrunのmismodelingがそれを阻んでいる)である。**
