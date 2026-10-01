# フェーズ2 作業記録：解析パイプラインと保存容量の整理

作成日：2026-04-21
担当：Seiichi Nakamura

---

## 1. 教授への回答：「45GBのFITSデータは解析に常に必要か？」

### 結論：**FITSファイルは最初の1回だけ必要。以降の解析はCSVのみ。**

| フェーズ | 使うファイル | 容量 |
|---|---|---|
| ① FITSをCSVに変換（1回だけ） | `fits/*.fits` | 約42GB（780週分） |
| ② 以降の全解析 | `data/CSV/filtered_events.csv` | 約195MB（推定） |

### 根拠

`make_filtered_csv.py` だけがFITSを読む。残り5本のスクリプトは全てCSVのみを入力とする。

```
fits/*.fits
    ↓ make_filtered_csv.py（1回実行）
data/CSV/filtered_events.csv   ← ここから先はこれだけ
    ↓ plot_raw_skymap.py
    ↓ plot_energy_spectrum.py
    ↓ plot_skymap_13bins.py
    ↓ plot_skymap_minus_isotropic.py
    ↓ plot_skymap_all_subtracted.py
```

### 推奨運用案

- **方法A（先生案）**：大学デスクトップで全780週のFITSをDL → `make_filtered_csv.py` を1回実行 → 生成されたCSV（〜195MB）を外付けSSDで受け取る → 以降はSSDなしで解析可能
- **方法B**：外付けSSD（42GB）を毎回接続してFITSを保持する → 再フィルタが必要になった場合に対応できる

**卒論の方針（データに加工した後は元データを触らない）であれば方法Aで十分。**

---

## 2. フェーズ0〜2 の作業全記録

### 全体の流れ

```
[フェーズ0]  FITSダウンロード → CSV変換 → 生マップ作成
[フェーズ1]  等方背景のみ差し引き
[フェーズ2]  全5成分差し引き（Totani手法の近似再現）
```

---

### フェーズ0：生データの取得と可視化

#### Step 0-1：FITSダウンロード

- HEASARCサーバーからwgetで取得
- 取得範囲：w009〜w018（10週分、2008年8月〜10月）
- 合計容量：537MB

```bash
cd fits/
for w in $(seq -f "%03g" 9 18); do
  wget "https://heasarc.gsfc.nasa.gov/FTP/fermi/data/lat/weekly/photon/lat_photon_weekly_w${w}_p305_v001.fits"
done
```

#### Step 0-2：FITSをCSVに変換（`make_filtered_csv.py`）

Totani (2025) Section 2.1 のフィルタ条件を適用：

| 条件 | 値 | 理由 |
|---|---|---|
| エネルギー | E ≥ 1 GeV | 低エネルギーは角度分解能が悪い |
| 天頂角 | θ < 100° | 地球大気由来のγ線を除去 |
| 銀経 | \|l\| ≤ 60° | 解析領域（ROI） |
| 銀緯 | 10° ≤ \|b\| ≤ 60° | 銀河面除外 |

出力：`data/CSV/filtered_events.csv`（38,671光子、2.5MB）

#### Step 0-3：生γ線マップ（`plot_raw_skymap.py`）

出力フォルダ：`data/figure-week9-phase0/`

- `skymap_raw_1-100GeV.png` など3枚（全エネルギー帯）
- Totaniの13ビンに合わせた13枚の個別マップ（`plot_skymap_13bins.py`）
- 13枚をPPTサイズ（1999×1125px）にまとめたグリッド画像（`make_grid_image.py`）

---

### フェーズ1：等方背景差し引き（`plot_skymap_minus_isotropic.py`）

出力フォルダ：`data/figure-week9-isotropic/`

- 引いたもの：**等方背景放射**（Totani成分④）
- 方法：銀緯50°〜60°（銀河から最も遠い帯）の平均カウント/ピクセルを各ビンで計算し全ピクセルから引く
- グレーピクセル = 差し引き後ゼロ以下（統計的に信号なし）

---

### フェーズ2：全成分差し引き（`plot_skymap_all_subtracted.py`）

出力フォルダ：`data/figure-week9-all-subtracted/`

Totaniの5成分をデータ駆動で近似差し引き：

| 順序 | 成分 | 実装方法 |
|---|---|---|
| Step 1 | ④ 等方背景 | \|b\|>50° の平均を全ピクセルから引く |
| Step 2 | ②③ GALPROP proxy | b方向の指数プロファイル（A×exp(-\|b\|/b0)）をフィットして引く |
| Step 3 | ① 点源マスク | 局所平均+4σ超えのピクセルをNaNに |
| Step 4 | ⑥ フェルミバブル proxy | 幾何テンプレート（\|l\|<22°, 15°<\|b\|<50°）の平均を引く |
| Step 5 | ⑤ ループI proxy | 幾何弧テンプレート（中心l=-31°,b=18°, 角半径40-70°）の平均を引く |

**注意**：本来はGALPROPモデルFITSファイル（3GB）と露出マップが必要。
現状はデータ駆動の近似であり、教育的再現の位置づけ。

---

### Bin 6（20.76 GeV）の解釈

- 光子数：398個（10週分）
- 全差し引き後：ポアソンノイズが支配的、球対称構造は見えない
- **理由**：Totaniは780週（15年）のデータで13〜19σ検出。10週は1/78のため有意性が〜1.5σ程度に希薄化される。
- **解釈**：パイプラインは正しく動作している。データ増量（w019以降）が次の課題。

---

## 3. 現在のフォルダ構成

```
grad-nakamura/
├── fits/           ← FITSファイル（w009〜w018、537MB）※gitignore済み
├── data/
│   ├── CSV/
│   │   └── filtered_events.csv      （38,671光子、2.5MB）
│   ├── figure-week9-phase0/         （生マップ 13枚 + グリッド）
│   ├── figure-week9-isotropic/      （等方差し引き 13枚 + グリッド）
│   └── figure-week9-all-subtracted/ （全成分差し引き 13枚 + グリッド）
├── code/
│   ├── make_filtered_csv.py         FITSをCSVに変換（フィルタあり）
│   ├── plot_raw_skymap.py           生マップ（3エネルギー帯）
│   ├── plot_energy_spectrum.py      13ビンエネルギースペクトル
│   ├── plot_skymap_13bins.py        13ビン個別マップ
│   ├── plot_skymap_minus_isotropic.py  等方差し引きマップ
│   ├── plot_skymap_all_subtracted.py   全成分差し引きマップ
│   ├── make_grid_image.py           グリッド画像生成（引数でフォルダ指定）
│   └── README.md
├── doc/
│   ├── phase1_what_we_did.md
│   ├── phase2_totani_subtraction_table.md
│   └── phase2_pipeline_and_storage.md  ← このファイル
├── ref/
│   └── 20Gev_gamma_ray.paper.2025-Nov-23.pdf
└── time/
    └── research_hours_2026.csv
```

---

## 4. 次のステップ

1. **データ増量**：w019以降をDLして780週分に近づける（先生と相談）
2. **GALPROP本体の導入**：proper な diffuse model テンプレートを使う
3. **点源カタログの導入**：4FGL-DR4（10MB）をダウンロードして正確な点源差し引き
4. **ハロー成分の検出**：差し引き後の残差をNFWプロファイルでフィット
