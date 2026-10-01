# ref/

参考文献メモ、文献リスト、BibTeX などを置きます。  
ダウンロードした論文 PDF は原則コミットしない運用を想定しています。

## 文献を探すときの入口

天文・宇宙物理では、まず `NASA ADS` を使うと文献を探しやすいです。  
著者名、キーワード、年、引用関係などから論文を検索できます。

`arXiv` はプレプリントを探すのに便利です。  
新しい論文や、公開された原稿を早く確認したいときに使います。

`alphaxiv` は、論文の概要をつかむ補助として使えます。  
ただし、最終的な確認は必ず元の論文本文で行ってください。

見つけた論文については、この `ref/` にメモ、BibTeX、文献リストなどを整理して残してください。

## データファイル（gitignore対象・手動DLが必要）

### 4FGL-DR2 点源カタログ（`4fgl_dr2.fit`、6.7MB）

`plot_skymap_all_subtracted.py` のStep 3（点源マスク）で使用。

```bash
cd ref/
wget https://fermi.gsfc.nasa.gov/ssc/data/access/lat/12yr_catalog/gll_psc_v28.fit -O 4fgl_dr2.fit
```

収録内容：Fermi-LAT 12年分の既知γ線点源6,659個の座標・スペクトル情報。
