# 01: FITS → CSV 変換

## 今回の最終目標

Fermi-LAT 衛星が検出したγ線光子のデータ（FITS形式）を、
Python で読める CSV ファイルに変換すること。

## 入力と出力

```
入力: L241120141937.fits  ← NASAから取得した生データ（1億光子級）

出力: events.csv
 energy_GeV, ra_deg, dec_deg, l_deg, b_deg, ...
 1.532,       83.81,  22.01,  184.5, -5.8, ...
 2.007,       266.5,  -28.9,  0.12,  -0.3, ...
 ...（数十万〜数百万行）
```

## なぜ CSV に変換するのか？

FITS = 天文専用バイナリ形式（NASAが標準として使う）
→ そのままでは pandas/Excel で読めない

CSV = 普通のテキスト形式（どんなツールでも読める）
→ 変換後は `pd.read_csv("events.csv")` の1行で読める！

## このフォルダで学ぶこと（Level 5〜15）

- `sys.argv` でコマンドライン引数を受け取る方法
- `with` 文（自動クローズ）
- `astropy.io.fits` で FITS ファイルを開く
- 配列のデータ型変換（MeV → GeV に単位変換）
- CSV への書き出し

## コード

→ `fits_to_csv_explained.py` を参照
