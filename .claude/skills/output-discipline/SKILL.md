---
name: output-discipline
description: コマンド出力 (テスト・ビルド・lint・診断・数値計算・git diff など) を Claude のコンテキストに直接流さず、ファイルに保存してから Read tool で必要分だけ読む規律。レビュー品質の保全とコンテキスト節約の両立、および外部 token 削減ツールへの耐性を確保する
origin: ai-project-kickstart-template
tools: Read, Write, Edit, Bash
---

# Output Discipline Skill

コマンド出力の取り扱い規律。**stdout に大量出力を流さず、ファイルに保存してから読む**ことを徹底する。

## Why

1. **レビュー品質の保全**: 物理・数値レビュアが必要とする情報 (seed, hash, stack trace, 全 diff) が、stdout 圧縮や中間ツールに影響されず常にファイルとして再現参照できる
2. **コンテキスト節約**: Claude のコンテキストには Read で**必要分のみ**を取り込める
3. **外部 token 削減ツールへの耐性**: Bash 出力を圧縮する proxy ツール (rtk 等) を併用しても、正本がファイルに残るためレビュー品質が保たれる
4. **再現性**: ファイル化された結果は時間が経っても見直せる

## When to Activate

以下のいずれかに該当するとき:

- 数値計算・シミュレーションを実行する
- テスト (`pytest`, `cargo test`, `npm test`, ...) を実行する
- ビルド・型チェック・lint を実行する
- 大きい diff / git log / log ファイルを参照する
- レビュア (Physical / Numerical) が詳細出力を必要とする

## Rules

### Rule 1: 数値計算結果は `results/<run-id>/` に保存

`run-id` は ISO timestamp ベース推奨 (例: `20260511T134211Z-solver` または `0042`)。

```text
results/
  20260511T134211Z-solver/
    result.npy              # 主要数値結果
    meta.json               # 再現性メタ (reproducibility-stamp 出力)
    summary.txt             # 1〜3 行の人間向け要約
    log.txt                 # stdout/stderr 全文 (必要に応じて)
```

stdout には **1〜2 行のサマリのみ**流す:

```text
[run 20260511T134211Z-solver] OK. result.npy (1.2 MiB), see meta.json
```

### Rule 2: テストランナーは結果ファイルを必ず出力

| Runner | ファイル化オプション例 |
| --- | --- |
| pytest | `pytest --tb=long --junit-xml=results/tests/<id>.xml --log-file=results/tests/<id>.log` |
| cargo test | `cargo test 2>&1 \| tee results/tests/<id>.log` |
| go test | `go test -json ./... > results/tests/<id>.ndjson` |
| jest | `jest --json --outputFile=results/tests/<id>.json` |

stdout 圧縮の有無に関わらず、**失敗詳細はログファイルに残る**。

### Rule 3: 大きい diff / log は一時ファイル経由で読む

```bash
git diff --no-color > /tmp/diff-$(date +%s).txt
# 続いて Read tool で /tmp/diff-XXX.txt を読む
```

```bash
docker logs <container> > /tmp/dockerlog-$(date +%s).txt
# Read で必要部分のみ取得
```

### Rule 4: レビュアは Read を優先 (`Bash cat` を使わない)

Claude Code の `Read` / `Grep` / `Glob` tools はファイルを直接読むため、Bash 経由の出力圧縮の影響を受けない。レビュアは:

- コード閲覧 → `Read`
- パターン検索 → `Grep`
- ファイル列挙 → `Glob`
- 結果ファイル閲覧 → `Read`

`cat file.py`, `grep "pat" -r .` を Bash で呼ぶのは、上記 tool が使えない特殊状況に限る。

### Rule 5: stdout 圧縮を許容するコマンド

以下は「結果のみ」が分かれば足りるので、stdout が圧縮されても問題ない:

- `git status`, `git log --oneline`
- `ls`, `tree`, `find`, `which`, `pwd`
- ビルド成否 (`cargo build`, `tsc`, `next build` の OK/error)
- リント要約 (`ruff check`, `eslint` の件数・分類)

これらの**詳細**が必要になった場合のみ、Rule 1〜3 のファイル化迂回路を取る。

## Output (発火後の記録)

数値結果を生成したら commit message または `.dev/CHANGELOG.md` に:

```text
results/<run-id>/ に出力。meta.json に再現情報併記。
```

## NG パターン

- 数値結果を**stdout のみ**で確認し、ファイルに残さない
- テスト出力を**stdout だけ**でレビューさせる (失敗詳細が圧縮で欠落する)
- 大きい diff/log を**stdout で全文流す** (コンテキスト浪費)
- レビュアが `Bash cat` で 1000 行のソースを読もうとする (Read を使え)

## References

- 数値結果のメタデータ仕様: `reproducibility-stamp` skill
- レビュアの参照規約: `.dev/TEAM_PROTOCOL.md` §3
- ローカル出力置き場: `results/` (Git 追跡対象外、`.gitignore` 済み)
