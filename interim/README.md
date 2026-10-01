# interim/ — 中間発表グラフを自分のコードで書き直すための作業場所

## フォルダ構成

```
interim/
  interim_report.pptx      ← 中間発表スライド本体(2026-07-16以降、AIは直接編集しない)
  reference_code/           ← 【答えコード】1行ずつコメント付き。まずこれを読む
  my_code_data/              ← 02番用の事前計算済み.npyデータ(重い計算を分離)
  my_code/
    01_halo_spectrum/halo_spectrum.py             ← あなたが穴埋めするファイル(既に用意済み)
    02_bin6_before_after/bin6_before_after.py       (Bin6の差引前/完全差引後スカイマップ2枚)
    03_ics_naturalness/ics_naturalness.py
    04_dwarf_summary/dwarf_summary.py
    05_dwarf_psmask_coma/dwarf_psmask_coma.py
```

**[2026-07-16] 02番は「バブル内外(A/C)ロバスト性検証」から「Bin6差引前/後スカイマップ」に差し替えた。**
A/C検証はユーザー判断でスコープ外(理解の負荷が高すぎる)としたため、`my_code`には含めない。

**[2026-07-16 22時ごろ、方針を再変更] 「穴埋め式」をやめ、`my_code/NN_xxx/`の中の
`.py`ファイルは全て最初から完成した動くコードにした。** プログラミング未経験者に
「ここだけ自分で書いて」という穴埋めを求めるのは、そもそも書き方を知らない人には
無理があるという指摘を受けたための変更。今のファイルは:
- 何も変えずに実行すればそのまま動く(まず動かして達成感を得る)
- コードの意味は全行に日本語コメントで説明済み
- `# 🔧 ここを変えてみよう`という場所の数字や文字列を書き換えて再実行すると、
  グラフがどう変わるかを見比べられる(「読んで理解する」→「変えて確かめる」という、
  ゼロから書くよりハードルの低い学習方法)

## 進め方

1. `my_code/01_halo_spectrum/halo_spectrum.py` を開き、まず何も変えずに実行する:
   ```
   cd /home/arsei/univ/nakamura-darkmatter
   /tmp/darkmatter_venv/bin/python3 interim/my_code/01_halo_spectrum/halo_spectrum.py
   ```
   (必ずリポジトリのルートから実行すること。JSONファイルの読み込みパスが
   リポジトリ直下からの相対パスになっているため、`my_code`フォルダの中で
   直接実行するとエラーになる)
2. `my_code/01_halo_spectrum/` に`my_halo_spectrum.png`が出力されれば成功
3. コード中の`# 🔧 ここを変えてみよう`の指示に従って、数字や文字列を書き換えて
   再実行し、グラフの変化を確認する。これを何箇所かやって「このコードとこの
   見た目が対応している」という感覚をつかむ
4. 02〜05番も同じ手順で進める
5. 分からない行があれば、遠慮なく質問する
6. `reference_code/`は`my_code/`とほぼ同内容だが、02番のみ配色(totani_div)の
   詳しい説明コメントが多い版として残してある

## 各グラフの元データ(JSON)の場所

| 番号 | グラフ | 元データ |
|---|---|---|
| 01 | 全13ビン有意度スペクトル | `results/mcmc_allbins_gasICS_v1/halo_spectrum.json` |
| 02 | Bin6 差引前/完全差引後スカイマップ | `interim/my_code_data/bin6_raw_counts.npy`, `bin6_residual.npy`(`results/mcmc_allbins_gasICS_v1/_precompute_bin6_skymaps.py`で事前計算済み) |
| 03 | ICSスペクトル自然性チェック | `results/mcmc_allbins_gasICS_v1/iter004_ics_naturalness_check.json` |
| 04 | 矮小銀河5天体 Bin6有意度 | `results/dwarf_pipeline_results.json` |
| 05 | Coma Berenices 点源マスク前後 | `results/dwarf_pipeline_results.json`(同上) |

## 大事な注意

- ここにあるのは**グラフを描く部分だけ**です。JSONファイルを作るまでの計算
  (MCMCフィット・GALPROP読み込み等)は`code/`以下の別スクリプトが担当しており、
  それ自体は複数回のレビューを経た本実装です。「グラフの作り方」を自分の力に
  することが今回の目的です。
- ファインマン図(スライド3)はコードではなくPowerPoint上での作図に置き換える
  方針と伺っているので、ここには含めていません。
- 生成AI利用の開示ルールは大学に確認中とのことなので、確認が取れ次第、
  本ファイルとスライドノートに開示の要否を反映してください。

## 【2026-07-16】interim_report.pptxはAIが直接編集しない

ユーザーがPowerPoint上で直接スライドを編集する運用に切り替えた。
`code/build_interim_ppt.py`を実行すると全スライドがゼロから再生成され、
ユーザーの手動編集が消えるため、**ユーザーの明示的な許可なしにこのスクリプトを
実行してはいけない**。スライド内容の変更提案はテキストで伝え、実際の編集は
ユーザーが手作業で行う。

## 【2026-07-16 方針変更】配色はあえてシンプルにしている

教授から「学部生は色を作り込まない・そっけなさがある」という指摘があったため、
`reference_code/`・`my_code/`とも濃紺背景や凝ったhexカラーコードはやめ、
matplotlibの初期設定(白背景・デフォルト配色)に統一した。区別に意味がある
色分け(A/C、マスク前後等)だけ`red`/`blue`/`gray`のような標準色名を使う。

**例外: スカイマップ(imshow/pcolormesh)は`totani_div`カラーマップ必須。**
線グラフ・棒グラフは上記の通りシンプルでよいが、l/b平面のスカイマップ
(02番のようなimshow図)だけは、このプロジェクト全体(`code/mcmc_fit.py`他)で
統一して使われている専用カラーマップ`totani_div`(シアン→黒→黄、0中心対称、
戸谷論文Fig.11-13準拠)を必ず使うこと。02_bin6_before_afterのreference_codeに
定義をコピーしてあるので、それを再利用する。理由: 汎用カラーマップ(inferno等)を
使うと他の図と見た目が不統一になり、2026-07-16に実際にこの不統一が指摘された。
本編のPPT(`interim_report.pptx`)側は既存のダークテーマのままなので、
自分で書いたグラフをスライドに差し込む際は見た目のギャップが出る点に注意
(むしろ「自分で作った部分だけ地味」という状態は不自然ではないので気にしなくてよい)。
