# code/ — Fermi-LAT 解析スクリプト

## 必要なライブラリ（初回のみ）

```bash
sudo apt-get install -y python3-astropy python3-pandas python3-matplotlib python3-numpy
```

---

## スクリプト一覧

### 1. `fits_to_csv.py` — FITSを1ファイルずつCSVに変換

```bash
python3 code/fits_to_csv.py fits/lat_photon_weekly_w009_p305_v001.fits
# → fits/lat_photon_weekly_w009_p305_v001.csv が生成される
```

**出力列:**

| 列名 | 意味 | 単位 |
|---|---|---|
| `energy_GeV` | 光子エネルギー | GeV |
| `ra_deg` | 赤経 (J2000) | 度 |
| `dec_deg` | 赤緯 (J2000) | 度 |
| `l_deg` | 銀経 | 度 |
| `b_deg` | 銀緯（銀河面からの角度） | 度 |
| `theta_deg` | 衛星視野中心からの角度 | 度 |
| `zenith_angle_deg` | 天頂角 | 度 |
| `time_met_s` | 観測時刻 MET（基準=2001-01-01） | 秒 |
| `event_class` | イベントクラス（Pass 8 品質フラグ） | ビット整数 |
| `event_type` | イベントタイプ | ビット整数 |

---

### 2. `make_filtered_csv.py` — 全FITSをまとめてフィルタリングしCSVに結合

Totani (2025) の解析条件でフィルタリングして `data/filtered_events.csv` を生成する。

```bash
python3 code/make_filtered_csv.py
```

**フィルタ条件（Totani 2025 Section 2.1）:**

| 条件 | 値 | 理由 |
|---|---|---|
| エネルギー | E ≥ 1 GeV | 低エネルギーは角度分解能が悪い |
| 天頂角 | θ < 100° | 地球大気由来のγ線を除去 |
| ROI 銀経 | \|l\| ≤ 60° | 解析領域 |
| ROI 銀緯 | 10° ≤ \|b\| ≤ 60° | 銀河面（\|b\|<10°）を除外 |

FITSファイルは `fits/` フォルダに置いておくこと。

---

### 3. `plot_raw_skymap.py` — 生のγ線カウントマップをプロット

何も差し引かない生の光子分布を銀河座標でプロットする（卒論フェーズ1）。

```bash
python3 code/plot_raw_skymap.py
```

- 入力: `data/filtered_events.csv`（`make_filtered_csv.py` の出力）
- 出力: `data/skymap_raw_1-100GeV.png` ほか3枚

---

## データの準備（FITSファイルのダウンロード）

Fermi-LAT 週次全天ファイルを HEASARC から取得する。
以下は w009〜w018（10週分、テスト用）の例：

```bash
cd fits/
for w in $(seq -f "%03g" 9 18); do
  wget "https://heasarc.gsfc.nasa.gov/FTP/fermi/data/lat/weekly/photon/lat_photon_weekly_w${w}_p305_v001.fits"
done
```

Totani論文と同条件（15年分）は w009〜w789 を取得する（約12GB）。

---

## 解析の流れ

```
fits/*.fits
    ↓  make_filtered_csv.py
data/filtered_events.csv
    ↓  plot_raw_skymap.py
data/skymap_raw_*.png
```
