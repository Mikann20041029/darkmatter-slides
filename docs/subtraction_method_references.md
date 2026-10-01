# 引く手法(背景差し引き手法)の各論文リスト表

教授指摘(2026-07-03、`PPT/interim/README.md` 参照)「重要✨ 引く手法の各論文リスト表をつくる」への対応。

本解析(および Totani 2025)が採用している6成分モデルの各背景成分について、その差し引き手法・テンプレートの**出典論文**を一次資料ベースで整理する。各エントリの書誌情報は WebSearch で個別に検証済み(タイトル・著者・巻号・arXiv IDを一次情報源で確認、記憶からの記述はしていない)。

---

## 対応表

| # | 成分 | 手法の出典論文 | 出典が定義する手法 | 本解析(nakamura-darkmatter)での採用状況 |
|---|---|---|---|---|
| ① | 点源 (Point sources) | 4FGL-DR4: Fermi-LAT Collaboration, *"Fermi Large Area Telescope Fourth Source Catalog Data Release 4"*, arXiv:2307.12546 | 14年分データによる点源カタログ(`gll_psc_v35.fit`)。位置・フラックス・スペクトル形状 | 本解析は当初 4FGL-DR2(12年)使用。本セッションで DR4(`ref/gll_psc_v35_dr4.fit`)を取得済み、コード側の切替は別TODO |
| ② | GALPROP銀河拡散放射 | Acero, F. et al. 2016, *"Development of the Model of Galactic Interstellar Emission for Standard Point-Source Analysis of Fermi Large Area Telescope Data"*, ApJS 223, 26, arXiv:1602.07246 | GALPROPによる π0崩壊+制動放射+IC放射のテンプレートフィット(ガス柱密度マップ+CR伝播モデル)を合成した `gll_iem_v0X` シリーズの構築法 | Totaniと同じ `gll_iem_v07.fits`(本セッションで `ref/` に再取得済み)を参照するが、実際の差し引きは指数関数近似 `A*exp(-|b|/b0)` で代替(§6成分比較表で偏差 +3.2%〜+21.9% と定量化済み) |
| ③ | 等方背景放射 (Isotropic / EGB) | Ackermann, M. et al. 2015, *"The Spectrum of Isotropic Diffuse Gamma-Ray Emission Between 100 MeV and 820 GeV"*, ApJ 799, 86, arXiv:1410.3696 | 未分解点源+真の河外拡散放射(EGB)を合わせた「等方成分」のスペクトルテンプレート。Totani は本論文の初期値(E²dN/dE≈1e-4 MeV cm⁻²s⁻¹sr⁻¹)を出発点にMCMCフィット | 本解析は `|b|≥50°` 平均カウント密度を定数フロアとして差し引く(物理テンプレートではなくデータ駆動の経験値)。露出マップ未取得のため物理単位変換ができず、Totaniとの%比較は不可 |
| ④ | Loop I (North Polar Spur) | Wolleben, M. 2007, *"A New Model for the Loop I (North Polar Spur) Region"*, ApJ 664, 349, arXiv:0704.0276 | 2つのシンクロトロン輝面シェル(半径50-100pc)による幾何モデル。偏光サーベイから輝面形状を再構成 | 本解析はWollebenの幾何形状を採用せず、画像残差への経験的2成分(内側/外側)独立フィット。物理シェル形状の仮定なし(手法上の相違として比較表に明記済み) |
| ⑤ | フェルミバブル | Su, M., Slatyer, T. R., & Finkbeiner, D. P. 2010, *"Giant Gamma-ray Bubbles from Fermi-LAT: Active Galactic Nucleus Activity or Bipolar Galactic Wind?"*, ApJ 724, 1044, arXiv:1005.5480 | Fermi-LAT全天マップから最初に発見された、銀河中心から南北に伸びる巨大ガンマ線構造。ハードスペクトル(dN/dE∝E⁻²)を持つ領域として同定 | Totani・本解析とも、4.3 GeV残差マップの正領域をテンプレート化する手法は Su+2010 の発見的手法を踏襲。本解析は境界固定・smoothingなしの簡略版(§5参照) |
| ⑥ | NFWハロー (DM) | Navarro, J. F., Frenk, C. S., & White, S. D. M. 1997 *"A Universal Density Profile from Hierarchical Clustering"*, ApJ 490, 493 (NFWプロファイル定義); パラメータは Diemand, J. et al. 2008, *"Clumps and streams in the local dark matter distribution"*, Nature 454, 735 (Via Lactea II シミュレーション、rs=21kpc, ρs=8.1×10⁶ M☉/kpc³) | ダークマター密度プロファイル ρ(r)=ρs·x⁻¹(1+x)⁻² の関数形とパラメータの物理的根拠 | 本解析・Totaniともパラメータ完全一致(§6成分比較表で確認済み)。J-factor計算方法は視線積分∫ρ²dsで共通 |

---

## 参考: 本解析手法と直接比較すべき関連解析論文

上記は各成分の「一次定義論文」だが、Totani(2025)や本解析と同種の**背景差し引き手法そのもの**を扱う関連解析として、以下も参照価値が高い(教授の「引く手法」という言葉が指す可能性がある、方法論の比較対象):

| 論文 | 内容 | 本解析との関係 |
|---|---|---|
| Calore, F., Cholis, I., & Weniger, C. 2015, *"Background Model Systematics for the Fermi GeV Excess"*, JCAP03(2015)038, arXiv:1409.0042 | 銀河中心領域における拡散モデルの系統誤差を、複数のGALPROPモデルバリエーション+残差の主成分分析で定量化 | 本解析が未実施の「GALPROPモデル不確かさの系統誤差評価」(`.dev/TODO.md` 既存項目)の手法的模範 |
| Daylan, T. et al. 2016, *"The Characterization of the Gamma-Ray Signal from the Central Milky Way: A Case for Annihilating Dark Matter"*, Physics of the Dark Universe 12, 1, arXiv:1402.6703 | 銀河中心超過(GCE)をテンプレートフィット(点源+等方+GALPROP+ハロー)で解析する方法論。本解析の6成分同時フィットと同型のアプローチ | 同時フィット・テンプレート法の先行例として方法論を比較可能 |
| Ackermann, M. et al. (Fermi-LAT Collaboration) 2015, *"Searching for Dark Matter Annihilation from Milky Way Dwarf Spheroidal Galaxies with Six Years of Fermi Large Area Telescope Data"*, PRL 115, 231301, arXiv:1503.02641 | 矮小銀河でのダークマター探索の標準的解析手法(ON/OFF領域、J-factor、複数天体の結合尤度) | 本解析の矮小銀河5天体パイプライン(`code/plot_dwarf_pipeline.py` 等)の比較対象。結合尤度(joint likelihood)を使うか単純な複数天体独立解析にとどめるかの判断材料 |

---

## 書誌情報の検証について

上表の全エントリはタイトル・著者・巻号・arXiv IDをWebSearch経由で個別に確認した一次情報源に基づく(2026-07-10実施)。「〜と言われている」式の未検証記述は含まない([[.dev/SOUL.md]] Scientific Integrity 準拠)。ただし内容要約(「手法」列)は各論文アブストラクト等からの要約であり、詳細な数式・図番号の対応は原論文PDFの取得後に個別確認が必要(現時点で ref/ にPDFがあるのは Totani(2025)と Alemanno+2026のみ)。
