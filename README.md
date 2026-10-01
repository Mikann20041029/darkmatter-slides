# darkmatter-slides

卒業研究 (天の川ハローからの 20 GeV ガンマ線超過の再現検証) の**スライド作り専用**の作業場。

研究の本体は研究室のリポジトリ `astro-sim-lab/nakamura-darkmatter` にあり、ここはその抜粋コピー
(コピー元コミット `bceb006`、2026-10-01)。**解析コードとイベントデータは入っていない**ので、
ここで計算はできない。数値を新しく出す必要があれば本体で行う。

## 中身

| フォルダ | 中身 |
|---|---|
| `papers/` | Bertólez-Martínez, Hooper & Khatee Zathul (2026) arXiv:2609.20944 / Totani (2025) arXiv:2507.07209 |
| `slides/` | 作りかけのスライド |
| `docs/` | 研究の現状 (`HANDOFF.md`)、手法と Totani 論文の対応 (`TOTANI_SPEC.md`)、本体の README |
| `docs/verification/` | 2026-09-28 の検証 (バブル依存性・矮小銀河) の仕様・レビュー・**判定 (`verdict.md`)** |
| `figures/` | 中間発表と検証の図 |
| `results/` | 図の元になった数値 (v20 の成分スペクトル・ハロースペクトル、対照実験のログ、矮小銀河の予測) |

教授から受け取った GALPROP の出力など、外部から提供されたデータは意図的に入れていない。
