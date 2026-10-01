# ストレージ管理記録

作成：2026-05-05

---

## 経緯

### データダウンロード

Fermi-LAT週単位FITSファイルをHEASARC FTPから自動DL。
途中でPCがロック画面でスリープ → プロセス強制終了を2回繰り返した。

- 1回目停止：w187（ファイルが破損した状態で残留）
- 2回目停止：w647まで取得した時点で停止

### C:ドライブ危機

WSLの仮想ディスク（ext4.vhdx）はC:ドライブ上に存在する。
FITSのDLにより ext4.vhdx が肥大化し、C:の空きが840MBまで低下。
→ VSCodeのWSL接続が頻繁に切断、PCが不安定になった。

---

## 対処

### 1. w551〜w647を削除

```bash
rm /root/grad-nakamura/fits/lat_photon_weekly_w5[5-9]*.fits \
   /root/grad-nakamura/fits/lat_photon_weekly_w6*.fits
```

### 2. w187（破損ファイル）を削除

ダウンロード中断により途中で切れたファイル。

```bash
rm fits/lat_photon_weekly_w187_p305_v001.fits
```

### 3. make_filtered_csv.py に破損ファイルスキップを追加

```python
try:
    n = process_fits(fits_path, writer)
except Exception as e:
    print(f"  SKIP {fits_path.name}: {e}")
```

### 4. CSV変換 → FITS全削除

```bash
python3 code/make_filtered_csv.py && rm -f fits/*.fits && echo "完了"
```

結果：
- CSV：1,956,778イベント、124MB（w009〜w549、539週分）
- FITSフォルダ：0ファイル（全削除）
- WSLディスク：107GB → 4.9GB

---

## WSL仮想ディスクの圧縮（C:の空きを戻す）

WSL内でファイルを削除してもC:の空きはすぐ増えない。
ext4.vhdx ファイルを圧縮する必要がある。

### 手順

**1. WSL内でゼロ埋め（Ubuntuターミナル）**
```bash
sudo fstrim -v /
```

**2. WSLを完全停止（PowerShell）**
```powershell
wsl --shutdown
wsl --list --running   # 「実行中なし」を確認
```

**3. VSCode・Ubuntuターミナルを全て閉じる**

**4. PCを再起動**（WSLを確実に停止させるため）

**5. diskpartで圧縮（管理者として実行）**
```
select vdisk file="C:\Users\arsei\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu24.04LTS_79rhkp1fndgsc\LocalState\ext4.vhdx"
compact vdisk
exit
```

**注意：** VSCodeやUbuntuが1つでも起動していると  
`The process cannot access the file because it is being used by another process.`  
というエラーが出て失敗する。必ず全部閉じてから実行すること。

---

## 現在の状態（2026-05-05）

| 項目 | 状態 |
|---|---|
| CSV | w009〜w549（539週）、1,956,778イベント、124MB |
| FITSファイル | 全削除済み |
| C:ドライブ空き | 約2GB（圧縮未完了）|
| WSL仮想ディスク使用量 | 4.9GB |

---

## 今後のデータ取得方針

- w550〜w788（残り239週）は教授のPCでDLしてもらいSSDで受け取る
- 受け取り後、`make_filtered_csv.py` を再実行してCSVに統合する
- その後、全スクリプトを780週分フルデータで再実行する

### 教授へのDL依頼内容

```
ダウンロード先：https://heasarc.gsfc.nasa.gov/FTP/fermi/data/lat/weekly/photon/
対象ファイル：lat_photon_weekly_w550_p305_v001.fits 〜 lat_photon_weekly_w788_p305_v001.fits
合計：239ファイル、約13GB
```

スクリプト（`fits/download_all_weeks.sh` を START_WEEK=550, END_WEEK=788 に変更して使用）。
