# v20r の成分比 (本研究 / Totani) の計算し直し (2026-10-01、クラウド)

## 結論

1. **v20r の成分比 (59 GeV 未満の中央値)**: ガス 0.91 / ICS 1.15 / IGRB 0.37 / Loop I 0.73 / ハロー 1.16 / 合計 0.95。
   中間発表 (v20) のガス 0.68 / ICS 1.41 / Loop I 1.03 から変わった。ハロー・IGRB・合計はほぼ同じ。1 からの偏差の総和は 1.52 → 1.31 で、v20r のほうが Totani に近い
2. **この 6 つの値は、HANDOFF の 2026-07-24 の節に「v20 の成分比」として書かれた値と完全に一致する** (`.dev/HANDOFF.md:163-164`)。
   7/31 の節の値 (0.68 / 1.41 …、`.dev/HANDOFF.md:93`) は、今 `results/mcmc_allbins_gasICS_v20_constructsplit/` にある結果ファイルと一致する
3. ⇒ **v20 のフォルダの結果ファイルは、7/24 から 7/31 の間に別の状態で作り直された可能性が高い**。
   「v20 が再現できない」は、計算が毎回ぶれるからではなく、このファイルの入れ替わりで説明できそう (推測。本体の git 履歴で確認できる)

## 根拠

### 計算 (確認済み)

- `code/plot_component_overlay_vN.py` を v20r の結果 (`results/mcmc_allbins_gasICS_v20r_rerun/`) のコピーに対して実行。
  写しの `results/` は上書きしないよう、`/tmp/v20r` にコピーしてから実行した
- 環境: クラウド (x86_64)、Python 3.12.11、numpy 2.5.1 ほか `cloud_setup/requirements.txt` の固定版。v20 と同じ環境変数
  (`MCMC_ULTRACLEAN=1 MCMC_PIXEL_DEG=0.125 MCMC_DISK_BUBBLE=1 MCMC_CELL_LIKELIHOOD=1 MCMC_SIGNFREE_HALO=1`)
- 中央値は `code/plot_component_overlay_vN.py:163` のとおり 59 GeV 未満のビンだけでとる (7/24 と同じ定義)
- 成果物: 図 `cloud_reports/2026-10-01_v20r_component_overlay_totani.png`、数値 `cloud_reports/2026-10-01_v20r_component_spectra.json`

| | ガス | ICS | IGRB | Loop I | ハロー | 合計 |
|---|---|---|---|---|---|---|
| v20 (今ある結果ファイル = 中間発表) | 0.68 | 1.41 | 0.38 | 1.03 | 1.15 | 0.96 |
| **v20r (今日の再計算)** | **0.91** | **1.15** | **0.37** | **0.73** | **1.16** | **0.95** |
| HANDOFF 7/24 に書かれた「v20」 | 0.91 | 1.15 | 0.37 | 0.73 | 1.16 | 0.96 |

ビンごとの明るさ (v20r ÷ v20): ガス 1.22–1.66 倍、ICS 0.40–0.84 倍、ハロー 0.92–1.06 倍 (1.5–285 GeV)。
ガスと ICS の分け方だけが変わり、ハローはほぼ不変。

### 注意 (確認済み)

- このスクリプトはテンプレートをその場で作り直す。ガス・ICS・等方・Loop I・ハローのテンプレートは入力から一意に決まるので、
  クラウドで作っても本人 PC と同じはず。**バブル正負のテンプレートだけはクラウドと本人 PC で少し違う** (Bin6 で 19.46σ vs 19.00σ の原因)。
  図のバブル成分の値は参考扱い。上の表の成分比 (ガス・ICS・IGRB・Loop I・ハロー) にはバブルは入っていない
- 「合計」にはバブルが入るので、小数第 2 位は環境でずれうる

### 7/24 と 7/31 の食い違い (推測)

- 7/24 の HANDOFF は v20 を「現 baseline」とし、上の表の 3 行目の値を記録している
- 7/31 の HANDOFF は同じ v20 について 0.68 / 1.41 … を記録し、中間発表の図もこちら
- 今日の v20r (記録付き、決定性確認済み) は 7/24 側と一致する。したがって 7/24 以降に v20 のフォルダが上書きされたと考えるのが最も素直
- 一方 7/24 の HANDOFF の Bin6 有意度は 19.11σ で、これは今の v20 の結果ファイルと同じ値 (v20r は 19.00σ)。完全には整合しないので断定はしない

## 本人 PC (ローカル) でやってほしいこと

研究室のリポジトリ (本体) でだけ確認できる (写しには git 履歴が無い)。数秒で終わる:

```
cd ~/univ/nakamura-darkmatter
git log --format='%h %ad %s' --date=iso -- results/mcmc_allbins_gasICS_v20_constructsplit/mcmc_bin06.json
git log --format='%h %ad %s' --date=iso -- results/mcmc_allbins_gasICS_v20_constructsplit/component_spectra.json
```

- コミットが 2 つ以上あれば、v20 のフォルダは途中で上書きされている。そのコミットのメッセージで、何の計算で上書きしたかが分かる
- 結果ファイルが git 管理外なら、`ls -l --time-style=full-iso` で更新日時を見る

## 本体の TODO に足すべき項目

- [ ] 卒論・スライドの成分比を v20r の値 (ガス 0.91 / ICS 1.15 / IGRB 0.37 / Loop I 0.73 / ハロー 1.16 / 合計 0.95) に差し替える。図は `cloud_reports/2026-10-01_v20r_component_overlay_totani.png` (タイトルなし版が要るなら言ってください)
- [ ] 中間発表スライド・`.dev/INTERIM_SLIDES_2026-07-31.md` の「gas と ICS は補い合ってズレる (0.68 / 1.41)」の説明は、v20r では差が小さくなった (0.91 / 1.15) ので書き直す
- [ ] 上の git log で v20 のフォルダの上書きの有無を確かめ、判定記録に書く
