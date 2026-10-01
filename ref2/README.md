# ref2 — 「散漫放射か、未分解点源か」論争の一次資料 (全22本)

作成: 2026-08-17 / 用途: 青学大学院 出願書類・面接、および卒論の議論部
関連: [../aogaku/KENKYU_KEIKAKU_DRAFT.md](../aogaku/KENKYU_KEIKAKU_DRAFT.md) /
[../aogaku/SAKAMOTO_DOSSIER.md](../aogaku/SAKAMOTO_DOSSIER.md)

`ref/` = 本研究のパイプラインが直接使う資料 (Totani 原論文、GALPROP 出力、カタログ)。
`ref2/` = **「超過の起源は何か」という論争の文脈**。

**全 PDF は arXiv から取得し、1本ずつ PDF を開いて書誌情報を検証済み** (2026-08-17)。

---

## 0. この論争の本当の問い

坂本先生に承認された研究の軸は**これ**である。

> ### ガンマ線過剰は「滑らかな散漫放射」か、「未分解の暗い点源の集団」か。

- **滑らかなら** → 暗黒物質対消滅と整合的
- **塊状 (clumpy) なら** → ミリ秒パルサー (MSP) など天体起源

つまり **「暗黒物質か否か」は、突き詰めると "源の検出" の問題**である。
暗黒物質の理論的専門性ではなく、**ガンマ線データから暗い源を検出し散漫成分と分離する
観測技術**が要る。ここが坂本研究室の土俵と噛み合う。

**どちらに転んでも成果になる**: MSP 説を潰せば暗黒物質が残り、
MSP だと分かればそれ自体が高エネルギー天体物理の成果。

### 判別が原理的に難しい理由 (面接で必ず聞かれる)

点源は**極端に暗い極限で、滑らかなポアソン放射と統計的に縮退する**。
「点源的か滑らかか」という問いそのものが、暗い側で曖昧になる。
だから「何個の点源か」を言うには**光度関数の仮定**が要り、そこに系統誤差が入る。

---

## 🔴 1. 混同厳禁 — 2つの別の信号

| | **銀河中心 GeV 超過 (GCE)** | **20 GeV ハロー超過 (卒論の対象)** |
|---|---|---|
| ピーク | **1–3 GeV** | **約 20 GeV** |
| 広がり | 中心から約 10°、~1.5 kpc | **\|b\| = 10°–60° のハロー全体** |
| 歴史 | 2009年頃〜、**十数年の論争** | **2025年7月〜、まだ1年** |
| 二大仮説 | **暗黒物質 vs 未分解 MSP** | 拡散モデルの系統誤差 / 未分解の**系外**天体 |
| 暗黒物質なら | mχ ≈ 50 GeV | **mχ ≈ 0.5–0.8 TeV** (bb̄) |
| 「点源」の正体 | **銀河バルジの MSP** | **系外ブレーザー (= IGRB の実体)** |

- **「二大巨頭 = 暗黒物質 vs ミリ秒パルサー」は GCE については正しい。**
  Gordon & Macias (1306.5725) が 2013年に「**約 10³ 個の未分解 MSP**」で定式化した
- ⚠️ **ハロー超過に MSP 説をそのまま持ち込んではいけない。**
  バルジの MSP は銀河中心から 10–20° 程度に集中するので、\|b\|=60° まで広がる信号は作れない
- ✅ **ただし「散漫か点源か」という問いの構造は両方に共通する。**
  ハロー超過での「点源」は**系外ブレーザー**であり、その総和が IGRB (等方ガンマ線背景) である。
  **卒論で見つけた「IGRB が ICS に食われて潰れる」問題は、まさにこの分離の失敗**である

---

## 2. 収録論文 — 論争の時系列

### 第0幕 (2013–2015) 二大仮説の定式化と、独立な制約

| ファイル | 論文 |
|---|---|
| `1306.5725.pdf` | **Gordon & Macias (2013), PRD** — "Dark Matter and Pulsar Model Constraints from Galactic Center Fermi-LAT Gamma Ray Observations" |
| `1503.02641.pdf` | **Ackermann et al. / Fermi-LAT (2015), PRL** — "Searching for Dark Matter Annihilation from Milky Way Dwarf Spheroidal Galaxies with Six Years of Fermi-LAT Data" |

- Gordon & Macias: 「**暗黒物質対消滅、あるいは約 10³ 個の未分解 MSP**、どちらも十分動機づけられた
  説明」と定式化した論文。**「1000個規模の MSP」の出典はここ**。
  ただし銀河中心の拡散背景に大きな不定性があることも同時に指摘している
- Ackermann+: 矮小楕円銀河 15 個を**結合尤度でスタッキング**し、どれにも有意な超過が無いことから
  対消滅断面積に上限。100 GeV 以下でクォーク・τ チャンネルの熱的レリック断面積を排除。
  🔑 **卒論の「79 領域への拡張」の手法のお手本**。J-factor、結合尤度、上限の出し方が全部ある

### 第1幕 (2015–2016) 点源説が優勢に — 同時投稿の2本

| ファイル | 論文 |
|---|---|
| `1506.05124.pdf` | **Lee, Lisanti, Safdi, Slatyer & Xue (2016), PRL** — "Evidence for Unresolved Gamma-Ray Point Sources in the Inner Galaxy" |
| `1506.05104.pdf` | **Bartels, Krishnamurthy & Weniger (2016), PRL** — "Strong Support for the Millisecond Pulsar Origin of the Galactic Center GeV Excess" |

- Lee+: **非ポアソン型テンプレートフィット (NPTF)** を新規開発。
  「同じ平均光子数でも、点源集団は明るい画素と暗い画素の差が大きい」という**光子統計の違い**を測る。
  内側 10° の flux の 5–10% が未分解点源で、**超過は点源に完全に吸収され暗黒物質より好まれる**
- Bartels+: **ウェーブレット分解**で空の「粒々」を検出。**10.0σ**。
  もっともらしい光度関数なら超過の **100%** を説明
- **この2本で「暗黒物質説は死んだ」空気になった**

### 第2幕 (2016–2018) 「形」も星の分布をなぞる

| ファイル | 論文 |
|---|---|
| `1611.06644.pdf` | **Macias, Gordon, Crocker, Coleman, Paterson, Horiuchi & Pohl (2018), Nature Astronomy** — "Galactic Bulge Preferred Over Dark Matter for the Galactic Center Gamma-Ray Excess" |
| `1711.04778.pdf` | **Bartels, Storm, Weniger & Calore (2018), Nature Astronomy** — "The Fermi-LAT GeV Excess Traces Stellar Mass in the Galactic Bulge" |

- 光子統計 (粒々) だけでなく、**超過の空間的な"形"が球対称 (NFW) より
  銀河バルジ/バーの星の分布に合う**という主張。SkyFACT というツールを開発
- 🔴 **Oscar Macias はこの「バルジ MSP 派」の中心人物**。名前を覚えておくこと
  (後述の CTAO 論文 `2607.05245` の共著者でもある)

### 第3幕 (2019–2020) 反撃と再反論 — 🔑 この分野で一番大事な教訓

| ファイル | 論文 |
|---|---|
| `1904.08430.pdf` | **Leane & Slatyer (2019), PRL** — "Dark Matter Strikes Back at the Galactic Center" |
| `2002.12370.pdf` | **Leane & Slatyer (2020), PRL** — "Spurious Point Source Signals in the Galactic Center Excess" |
| `2002.12371.pdf` | **Leane & Slatyer (2020), PRD** — "The Enigmatic Galactic Center Excess: Spurious Point Sources and Signal Mismodeling" (上の詳細版・47ページ) |
| `1908.10874.pdf` | **Chang, Mishra-Sharma, Lisanti, Buschmann, Rodd & Safdi (2020), PRD** — "Characterizing the Nature of the Unresolved Point Sources in the Galactic Center: An Assessment of Systematic Uncertainties" |
| `2002.12373.pdf` | **Buschmann, Rodd, Safdi, Chang, Mishra-Sharma, Lisanti & Macias (2020), PRD** — "Foreground Mismodeling and the Point Source Explanation of the Fermi Galactic Center Excess" |

- **Leane & Slatyer 2019**: 実データに**わざと人工の暗黒物質信号を注入**したら、
  NPTF がそれを**丸ごと「点源」と誤判定した**。原因はフェルミバブル内などの未モデル化成分
- **Leane & Slatyer 2020 (PRL)**: NPTF が点源を支持したのは、
  **超過の南北非対称性をモデルに入れていなかったアーティファクト**。
  非対称性を許すと**点源への選好が有意でなくなる**
- **Chang+ / Buschmann+**: NPTF 側 (Lee+ の系譜) からの応答。系統誤差を精査し、
  前景モデルの誤りが結論をどう変えるかを定量化
- 🔑 **教訓: 「点源だ！」にも「暗黒物質だ！」にも簡単に飛びついてはいけない。**
  背景モデルの誤りが、そのまま別成分に付け替わる。
  **これは卒論で実測した「GALPROP のずれが ICS に化け、IGRB を潰す」と同じ病理**である

### 第4幕 (2020–2022) 機械学習の参入 ← 坂本研との直結点

| ファイル | 論文 |
|---|---|
| `2006.12504.pdf` | **List, Rodd, Lewis & Bhat (2020), PRL 125, 241102** — "The GCE in a New Light: Disentangling the γ-ray Sky with Bayesian Graph Convolutional Neural Networks" |
| `2107.09070.pdf` | **List, Rodd & Lewis (2021), PRD 104, 123022** — "Dim but not entirely dark: Extracting the Galactic Center Excess' source-count distribution with neural nets" |
| `2110.06931.pdf` | **Mishra-Sharma & Cranmer (2022), PRD 105, 063017** — "A neural simulation-based inference approach for characterizing the Galactic Center γ-ray excess" |
| `2209.14370.pdf` | **Hooper (2022), SciPost Phys. Proc.** — "The Status of the Galactic Center Gamma-Ray Excess" |

- List+ 2020: **ベイジアン・グラフ畳み込みニューラルネット**で、球面上のガンマ線マップを
  「滑らか成分 vs 点源成分」に切り分ける。HEALPix の球面データを直接扱うのが技術的な肝
- List+ 2021: 発展版。**点源の光度分布 (source-count distribution) そのもの**を NN で抽出
- Mishra-Sharma & Cranmer: **正規化フローによるシミュレーションベース推論 (SBI)**。
  従来の光子統計手法より**画像の空間相関を活かせ、モデル誤指定に強い**。
  ベースライン解析で超過の**約 38% 以上**を未分解点源に帰属
- Hooper: 9ページの総説。**全体像を最短で掴むならこれ**。
  ⚠️ ただし Hooper は暗黒物質説の代表的推進者で**中立ではない**

### 第5幕 (2024–2026) 現在地

| ファイル | 論文 |
|---|---|
| `2401.04565.pdf` | **Malyshev (2025), PRD 111, 043033** — "Towards resolving the Galactic center GeV excess with millisecond-pulsar-like sources using machine learning" |
| `2507.17804.pdf` | 🔥 **List, Park, Rodd, Schoen & Wolf (2026), PRL** — "On the Energy Distribution of the Galactic Center Excess' Sources" |
| `2509.20614.pdf` | **Sengar, Anumarlapudi, Kaplan, Frail, Hyman & Polisensky (2026), ApJ 1001, 119** — "Discovery of Millisecond Pulsars toward the Galactic Bulge in an Image-based Survey with MeerKAT" |
| `2512.16699.pdf` | **Berteaud et al. (2026), A&A** — "Discovery of two new millisecond pulsars towards the Galactic bulge" |
| `2511.15793.pdf` | **Lei, Zhou & Huang (2026)** — "How Bright in Gravitational Waves are Millisecond Pulsars for the Galactic Center GeV Gamma-Ray Excess?" |

- **Malyshev**: タイトルどおり「**機械学習で GCE を MSP 的な源に分解する**」。
  テーマと手法が本計画のど真ん中
- 🔥 **List+ 2026 (最新・最重要)**: 従来の点源解析は技術的制約から**空間情報だけを使い、
  光子のエネルギー情報を捨てていた**。ニューラルネット SBI で**空間とスペクトルを同時に**扱う
  (模擬観測 100 万枚以上で訓練)。結果、**点源は大幅に暗くなり、点源で説明するには
  中央値 10⁵ 個・90% 信頼度で 35,000 個以上**必要 (従来説の「数百個」より 2 桁多い)。
  最良の背景モデルでは**超過は暗黒物質が予言するポアソン放射と本質的に無矛盾**。
  → **2026年6月時点で「暗黒物質は排除できない」が現在地**
  (PRL, DOI 10.1103/dkcq-6y4f。[LBL リリース](https://www.physics.lbl.gov/2026/06/12/machine-learning-reopens-the-case-for-dark-matter-at-the-galactic-center/))
- **Sengar+ (MeerKAT)**: 統計でなく**実物を数えに行く**アプローチ。円偏波源を画像から選び
  Parkes で追観測 → 16 天体中 9 個のパルサー検出、**うち 6 個が新発見、5 個が MSP**。
  ⚠️ **重要な但し書き**: 分散量 (DM) が 18–330 pc cm⁻³ とバルジにしては小さく、
  **これらはバルジ内ではなく手前 (foreground) にある**と結論している。
  「MSP が見つかった = バルジ MSP 説の証拠」と単純に言ってはいけない
- **Berteaud+**: Chandra/VLA/Fermi で候補を絞り MeerKAT・Murriyang・Green Bank で深く探索。
  **バルジ方向に新 MSP を 2 個検出** (PSR J1740−2805、J1740−28。片方は black widow 候補)。
  内側 2° の MSP 数が**倍**に
- 🔑 **Lei+ (重力波)**: MSP が非軸対称に回転すれば**連続重力波**を出す。
  「ガンマ線の正体が MSP なら重力波でも見えるはず」。現行検出器では届かないが、
  **Einstein Telescope / Cosmic Explorer なら一部検出可能**。
  → **ガンマ線の謎を重力波で解く = 坂本研のマルチメッセンジャー哲学と直結**

### 本研究に直結する周辺

| ファイル | 論文 |
|---|---|
| `2311.04982.pdf` | **McDaniel, Ajello, Karwin, Di Mauro, Drlica-Wagner & Sánchez-Conde (2024), PRD 109, 063024** — "Legacy Analysis of Dark Matter Annihilation from the Milky Way Dwarf Spheroidal Galaxies with 14 Years of Fermi-LAT Data" |
| `2607.05245.pdf` | **Li, Macias, Vecchi & Ando (2026), MNRAS** — "Geminga and Monogem in the CTAO Era: Probing TeV Halos and Cosmic-Ray Transport" |

- McDaniel+: `1503.02641` (6年) の 14年版。矮小銀河の数も J-factor も更新。
  🔑 **卒論の 79 領域解析の直接のアップデート先**。
  Totani が「Reticulum II の超過の WIMP 質量がハロー超過と近い」と名指しした元論文
- Li, Macias+: **パルサー周りの TeV ハロー**を CTAO で観測したらどう見えるかを、
  前方畳み込み尤度＋テンプレートフィットで予測。効く理由 3 つ:
  ① パルサーが宇宙線陽電子超過の天体的説明として登場 (「暗黒物質 vs パルサー」の別版)、
  ② **モック観測＋尤度解析という手法が将来ミッション路線と繋がる**、
  ③ 共著の **Oscar Macias はバルジ MSP 派の代表格**

---

## 3. 読む順番 (推奨)

```
【土台】 1306.5725 (二大仮説の定式化) → 2209.14370 (Hooper 総説9ページ)
   ↓
【起点】 1506.05124 (NPTF) → 1506.05104 (ウェーブレット)
   ↓
【教訓】 1904.08430 → 2002.12370 (点源説の落とし穴) → 1908.10874 (系統誤差の精査)
   ↓
【手法】 2006.12504 → 2110.06931 → 2401.04565 (機械学習)
   ↓
【現在地】🔥 2507.17804 (2026 PRL・最新の答え)
   ↓
【実観測】 2509.20614 / 2512.16699 → 【将来】 2511.15793 (重力波)
   ↓
【自分の研究】 1503.02641 → 2311.04982 (矮小銀河) / ref/ の Totani + 2607.08552
```

**読むときの視点**: 「この判定を、坂本研の源検出・機械学習の技術でどう強化できるか」。
これで研究計画に直結する。

---

## 4. 書誌情報の訂正 (検証の結果)

外部の助言に含まれていた誤りを、PDF 実物との照合で修正した。

| 誤 | 正 |
|---|---|
| DOI 10.3847/1538-4357/ae4872 を「Fermi-LAT の統計解析で塊状構造を示した論文」として引用 | 🔴 **誤り**。これは **Sengar+ (2026) の MeerKAT 電波パルサー探査** (`2509.20614`) であり、Fermi-LAT の統計解析ではない。**面接で引くと事故る** |
| 「Leane & Slatyer 2020 (2002.12370 と 2002.12371)」 | 正しいが題名は "Spurious Point Source Signals in the GCE" (PRL) と "The Enigmatic GCE: Spurious Point Sources and Signal Mismodeling" (PRD, companion) |
| 「2002.12373 = 上の反論への再反論」 | 著者は **Buschmann, Rodd, Safdi, Chang, Mishra-Sharma, Lisanti, Macias**。NPTF 側からの系統誤差評価であり、単純な「再反論」ではない |
| "The Fermi-LAT GeV excess **as a tracer of** stellar mass..." | 正題は "The Fermi-LAT GeV Excess **Traces** Stellar Mass in the Galactic Bulge" |
| 「Li, Macias, Ando 2026」 | 正しくは **Li, Macias, Vecchi & Ando** (Vecchi が抜けていた) |
| 助言のリストに 2026年最新の List+ が無い | 🔥 **`2507.17804` (2026 PRL) が抜けていた**。List/Rodd 系列の最新版で、**結論が変わっている** (点源説には 10⁵ 個必要)。**面接で「今」を語るならこれが必須** |

---

## 5. 未取得・追加候補

- [ ] CALET の暗黒物質探索論文 ([arXiv:1702.02546](https://arxiv.org/abs/1702.02546))
      — 坂本研との接点として重要
- [ ] Fermi-LAT 等方ガンマ線背景 (IGRB) 公式測定 (Ackermann+ 2015)
      — 卒論の IGRB 崩壊問題の比較対象
- [ ] Calore, Cholis & Weniger の GCE スペクトル系統誤差論文 (2015)
- [ ] Daylan et al. / Abazajian — 暗黒物質推し陣営の代表 (立場の対比用)

---

## 追加 (2026-08-18) — 「天体候補は MSP だけではない」系 + X線からの検証

欄3 v6 の骨格を支える 3 本。**ガンマ線の問いを X線で検証する**という論旨の出典。

### 1701.02726 — Haggard, Heinke, Hooper & Linden (2017), JCAP 🔥 最重要

**"Low Mass X-Ray Binaries in the Inner Galaxy: Implications for Millisecond Pulsars and the GeV Excess"**

- **論旨**: MSP が GeV 超過の原因なら、同じ領域に**大量の低質量X線連星 (LMXB)** が
  存在するはず。MSP は LMXB から生まれる (リサイクル説) ため
- 球状星団と内部銀河の LMXB カタログ + 球状星団のガンマ線放射から、
  内部銀河の MSP 起源ガンマ線フラックスを推定
- **結論: 超過のうち MSP 起源は最大でも 4-23%**
- **決定的な数値 (原文)**: "If MSPs had been responsible for the entirety of the
  observed excess, **INTEGRAL should have detected ~10^3 LMXBs** from within a
  10° radius around the Galactic Center, whereas **only 42 LMXBs**
  (and 46 additional LMXB candidates) have been observed."
  → **1000個必要なのに42個しかない**
- ⚠️ 「候補」46 個を足すと 88 個。面接では「確定 42、候補込み 88」と言えるように

### 1407.5625 — Cholis, Hooper & Linden (2014), JCAP

**"Challenges in Explaining the Galactic Center Gamma-Ray Excess with Millisecond Pulsars"**

- 上の**先行版**。明るい LMXB の観測個数から内部銀河の MSP 数を推定
- **結論: 超過のうち MSP 起源は 1-5% のみ**。
  局所 MSP の光度関数 + Fermi が分解した点源数から上限も導出し、
  **「超過の大半が MSP」を強く排除**

### 1504.02477 — O'Leary, Kistler, Kerr & Dexter (2015)

**"Young Pulsars and the Galactic Center GeV Gamma-ray Excess"**

- **MSP ではなく「若いパルサー」**による説明。中心の星形成領域で生まれた
  高磁場の若いパルサーが起源という主張
- 非常に若く軟らかいスペクトルのものは銀河面近く、年齢とともにスペクトルが
  硬化したものはより大きな角度に蓄積する。この組み合わせが超過の形と
  スペクトルをなぞる
- → **「天体側の候補 = ミリ秒パルサー」だけではない**ことの出典

### 坂本先生側の対応論文 (ref2 には無し・arXiv ID のみ)

- **astro-ph/0703274** — "Periodicities in X-ray Binaries from Swift/BAT
  Observations" (11 名、**T. Sakamoto** を含む)。
  → **X線連星は坂本先生の守備範囲**であることの出典

### 1506.05119 — Cholis, Evoli, Calore, Linden, Weniger & Hooper (2015), JCAP

**"The Galactic Center GeV Excess from a Series of Leptonic Cosmic-Ray Outbursts"**

- **論旨**: 天体でも暗黒物質でもなく、**銀河中心で過去に起きた宇宙線電子の噴出 (アウトバースト)**
  の名残で超過を説明できるか、を詳しく調べた
- **結論**: **複数回のアウトバースト**なら、もっともらしく超過を作れる。
  中心から 1-2° より外の形は **2 回の噴出**で説明できる —
  1 回目が約 **10^6 年前**、2 回目 (注入エネルギーは 1 回目の約 10%) が約 **10^5 年前**
- → **「天体候補」とも「暗黒物質」とも違う第3の道**。欄3 で挙げた
  「宇宙線のアウトバースト」の出典はこれ

---

## 🔑 欄3「天体起源にも複数の候補がある」の出典対応表

**面接で「どの論文で知ったのか」と必ず聞かれるので、この 3 本は紐付けて覚えること。**

| 欄3 の記述 | 出典論文 | ファイル |
|---|---|---|
| **ミリ秒パルサー** | Bartels, Krishnamurthy & Weniger (2016) / Lee, Lisanti, Safdi, Slatyer & Xue (2016) | `1506.05104.pdf` / `1506.05124.pdf` |
| **若いパルサー** | O'Leary, Kistler, Kerr & Dexter (2015) | `1504.02477.pdf` |
| **宇宙線のアウトバースト** | Cholis, Evoli, Calore, Linden, Weniger & Hooper (2015) | `1506.05119.pdf` |

⚠️ **1506.05104 / 1506.05119 / 1506.05124 は arXiv 番号が近い = 2015年6月に相次いで投稿された。**
「ミリ秒パルサー」「宇宙線アウトバースト」「未分解点源」という**3 つの競合説が
ほぼ同時に出た**という事実自体が、当時この問題が最も熱かったことを示す。
面接で言えると「文献の流れを把握している」証拠になる。
