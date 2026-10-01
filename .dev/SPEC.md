# SPEC.md — 実装で使う設計書

このファイルは、初期ブレストで固めた内容を、本実装フェーズでも参照し続けるための設計書である。

仕様変更があれば、このファイルを更新する。

---

## 0. Profile

Profile: `research`

---

## 1. 目的・背景

Fermi-LAT 衛星の Pass 8 Release 3 データ（15年分、w009〜w789、780週）を解析し、
Totani (2025) が報告した**銀河系ハローからの 20 GeV ダークマター対消滅過剰信号**を再現・検証する。

- 先行研究: Totani T. (2025), "Evidence of 20 GeV dark matter annihilation in the inner Milky Way halo"
- 手法: 5成分逐次差引 → NFW ハロー形状マッチング → 有意性検定（OLS、将来は MCMC）
- 現状: 780週フルデータで Bin06（20.76 GeV）に **31σ の過剰検出**（Totani 報告の 13–19σ と比較中）

---

## 2. スコープ

### やること

- Fermi-LAT FITS → フィルタ済み CSV 変換（`make_filtered_csv.py`）
- 13 ビンエネルギースペクトル解析（Totani Section 2.1 準拠）
- 全天スカイマップ生成（各ビン、1°×1° ピクセル）
- 5 成分逐次差引（等方背景・銀河拡散・既知点源・フェルミバブル・ループ I）
- NFW ハロー形状マッチング（`plot_nfw_halo_fit.py`、OLS）
- 矮小銀河解析（5 天体、Li&Ma 統計）

### やらないこと

- FITS ダウンロード自動化の新規実装（手動取得 or SSD 受け渡し）
- リアルタイムデータ更新
- MCMC / Bayesian 解析（将来課題）
- 検出器応答関数（IRF）の本格的な畳み込み（1° ピクセルで近似済み）

---

## 3. ユーザ・利用シーン

- **主担当**: 中村誠一（卒業研究生）
- **利用シーン**: 卒業論文執筆・発表用の図表生成と数値検証

---

## 4. 機能要件

### 必須機能

| スクリプト | 役割 |
|---|---|
| `make_filtered_csv.py` | 全 FITS → フィルタ済み CSV（1 回のみ実行） |
| `plot_raw_skymap.py` | 生ガンマ線カウントマップ |
| `plot_energy_spectrum.py` | 13 ビンエネルギースペクトル |
| `plot_skymap_13bins.py` | 各ビン個別スカイマップ |
| `plot_skymap_minus_isotropic.py` | 等方背景差引後マップ |
| `plot_skymap_all_subtracted.py` | 全 5 成分差引マップ（最重要） |
| `plot_nfw_halo_fit.py` | NFW ハロー形状マッチング |
| `extract_dwarf_csv.py` | 矮小銀河周辺光子抽出 |
| `analyze_dwarfs.py` | 矮小銀河スペクトル + 有意性計算 |

### あれば良い機能

- 4FGL-DR4 への更新（現在 DR2）
- MCMC による NFW 振幅フィット
- Cirelli PPPC 4 DM ID テーブルによるスペクトル形状フィット
- 系統誤差評価（GALPROP 不確かさ伝播）

---

## 5. 非機能要件

- Python 3 で動作
- 外部依存: `astropy`, `numpy`, `pandas`, `matplotlib`, `scipy`
- 全スクリプトは CSV を入力とし、FITS を読むのは `make_filtered_csv.py` のみ
- 出力先: `data/figure-*/`（Git 除外）

---

## 6. 技術スタック

| 項目 | 内容 |
|---|---|
| 言語 | Python 3 |
| 主要ライブラリ | astropy, numpy, pandas, matplotlib, scipy |
| データ形式 | Fermi-LAT FITS (Pass 8 R3), CSV（中間処理済み） |
| 参照カタログ | 4FGL-DR2（`ref/4fgl_dr2.fit`、6.7 MB、Git 除外） |
| 銀河拡散モデル | GALPROP `gll_iem_v07.fits`（887 MB、ローカル or 自動 DL、Git 除外） |

---

## 7. ベンチマーク・合格条件

| 条件 | 目標値 | 現状 |
|---|---|---|
| Bin06（20.76 GeV）S/N | ≥ 5σ | **31σ**（780週） |
| Totani との比較 | 定性的に一致 | 過剰検出の存在は再現済み、絶対値は Totani より大 |
| 矮小銀河 Coma Berenices | > 3σ @ 20 GeV | **4.54σ** |
| NFW 形状マッチング | A > 0 | 達成 |

> **注意**: 現在の 31σ は統計的下限。GALPROP 近似による系統誤差および OLS の過大評価を含む。

---

## 8. ディレクトリ構造案

```text
nakamura-darkmatter/
├── code/               ← 解析・可視化スクリプト（Python）
├── docs/               ← 研究記録・発表資料（markdown + PDF + PPTX）
├── data/               ← 出力データ（図表・CSV、Git 除外）
│   ├── CSV/            ← フィルタ済みイベントテーブル
│   └── figure-*/       ← 各フェーズの出力図表
├── ref/                ← 参照データ・論文 PDF（FITS は Git 除外）
├── fits/               ← Fermi-LAT 生 FITS（外付け SSD or ローカル、Git 除外）
├── time/               ← 研究時間記録
├── results/            ← ローカル出力置き場（Git 除外）
└── .dev/               ← 管理ファイル（SPEC/TODO/CHANGELOG/HANDOFF）
```

---

## 9. 実装メモ

### 重要な定数

```python
# エネルギービン（Totani 13 ビン）
BIN_CENTERS = [1.51, 2.55, 4.31, 7.28, 12.29, 20.76, 35.06,
               59.22, 100.02, 168.93, 285.33, 481.93, 814.00]  # GeV

# 空間解像度
PIXEL_DEG = 1.0        # 度
L_RANGE = [-60, 60]    # 銀経範囲（度）
B_RANGE = [-60, 60]    # 銀緯範囲（度）

# フィルタ条件
E_MIN = 1.0            # GeV
ZENITH_MAX = 100.0     # 度
B_MIN = 10.0           # |b| の最小値（銀河面除外）
B_MAX = 60.0           # |b| の最大値

# NFW パラメータ（Via Lactea II）
RS     = 21.0          # kpc（スケール半径）
RHO_S  = 8.1e6         # M_sun/kpc³（スケール密度）
D_SUN  = 8.0           # kpc（太陽–銀河中心距離）

# 矮小銀河解析
ON_RADIUS  = 2.0       # 度
OFF_RADIUS = 5.0       # 度
ALPHA = ON_RADIUS**2 / (OFF_RADIUS**2 - ON_RADIUS**2)
```

### データ準備手順

1. `fits/` に w009〜w789 の FITS を配置（外付け SSD から）
2. `ref/4fgl_dr2.fit` を配置（Git 管理外）
3. `ref/gll_iem_v07.fits` を配置（887 MB、自動 DL 可）
4. `python code/make_filtered_csv.py` → `data/CSV/filtered_events.csv`
5. 以降のスクリプトは CSV のみ参照

### 既知の制限事項

- 現在の NFW フィットは OLS のみ → 31σ は統計的過大評価
- GALPROP 成分の空間テンプレートは指数関数近似（本来は FITS モデルで引くべき）
- 点源 PSF 畳み込みは 1° ピクセルで近似（影響は小さいと推定）
