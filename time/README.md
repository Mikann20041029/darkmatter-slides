# 作業時間記録

このディレクトリには、`2026-04-01` から `2027-03-31` までの研究従事時間を記録します。

## ファイル構成

- `research_hours_2026.csv`
  - 日次の入力ファイルです。
  - 1日につき1行あります。
  - 研究従事時間は `on_campus_hours` 列と `off_campus_hours` 列に分けて入力します。
  - `note` 列は任意のメモ欄です。
- `summarize_research_hours.py`
  - CSV の内容を検証します。
  - 月別合計と全期間合計を出力します。

## CSV 形式

ヘッダ:

```csv
date,on_campus_hours,off_campus_hours,note
```

記入例:

```csv
2026-04-01,3,0.5,experiment
2026-04-02,0,1,reading
2026-04-03,0,0,
```

記入ルール:

- `date` 列は変更しないでください。
- `on_campus_hours` には学内での研究時間を、`off_campus_hours` には学外での研究時間を入力してください。
- 各時間列には `0`, `1`, `2.5` のような 0 以上の数値を入力してください。
- まだ記録していない日は、両方の時間列を空欄のままにできます。
- `2026-04-01` から `2027-03-31` までの全日付を残してください。
- 同じ日付を重複して追加しないでください。

## 使い方

リポジトリのルートで次のコマンドを実行してください。

```bash
python3 time/summarize_research_hours.py
```

出力例:

```text
file: /path/to/research_hours_2026.csv

monthly research hours
month,on_campus_hours,off_campus_hours,total_hours
2026-04,8.5,4,12.5
2026-05,10,8,18

total,18.5,12,30.5
```

## GitHub での運用

- GitHub の Web 画面で `time/research_hours_2026.csv` を開きます。
- 編集ボタンからファイルを更新します。
- `on_campus_hours`、`off_campus_hours` と必要に応じて `note` のみを編集します。
- GitHub Web からそのままコミットできます。

CSV は差分が見やすく、GitHub 上で編集しやすいため、後からスクリプトや表計算ソフトで集計しやすい形式です。
