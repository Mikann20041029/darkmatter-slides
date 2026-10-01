# AGENTS_project.md — 本実装担当

このファイルは、**本実装フェーズで `AGENTS.md` に昇格する AI エージェント向け指示書テンプレート**である。

---

## 0. セッション開始時に読むファイル

毎セッション最初に読む (動的に変化するため):

1. `.dev/SPEC.md` — 仕様の正本 (冒頭の `Profile:` 行で profile を確認)
2. `.dev/TODO.md` — タスクの正本
3. `.dev/HANDOFF.md` — 現況スナップショット

> `CLAUDE.md` が `@.dev/SOUL.md` / `@.dev/SOUL_addon.md` / `@AGENTS.md` / `@.dev/TEAM_PROTOCOL.md` を auto-load するため、SOUL / SOUL_addon / AGENTS / TEAM_PROTOCOL は毎回明示的に読む必要はない。`SOUL_addon.md` と `TEAM_PROTOCOL.md` はブレスト完了時に選択 profile (`grant` / `research` / `paper` / `talk` / `lecture`) から symlink (または cp) された profile 固有の正本である。`README.md` は初回または不明点があるときに参照。`.dev/FORBIDDEN.md` は `forbidden-list-check` skill が必要時に読み込む。

---

## 1. 役割と進め方

あなたは**本実装担当**である。設計済みの SPEC と TODO に従って実装・修正・検証・文書更新を進める。

- 正本: 仕様は `.dev/SPEC.md`、タスクは `.dev/TODO.md`、変更履歴は `.dev/CHANGELOG.md`
- 仕様変更があれば SPEC を、タスクの完了・追加があれば TODO を、意味のある変更をしたら CHANGELOG を更新する
- 標準フロー: TODO 選定 → SPEC 確認 → 実装 → README/docs 更新 → TODO/CHANGELOG 更新 → コミット

複数エージェントで進める場合は Manager として `/team-task` を使う。原則: **Manager は自分で実装・レビューしない**。詳細は `.dev/TEAM_PROTOCOL.md`。

---

## 2. コミット後の必須作業

コミットを作成したら、**同じコミットまたは直後のコミット**で以下を反映する。

1. `.dev/TODO.md` の完了タスクを `[ ]` → `[x]` に更新し、`*(YYYY-MM-DD, {hash})*` を付ける
2. `.dev/CHANGELOG.md` の上部にそのコミットの変更内容を追記する

`PostToolUse` hook (`.claude/hooks/check_post_commit.sh`) が `git commit` 実行後に上記の漏れを警告する。

---

## 3. 自動発火スキル一覧

以下のスキルは context に応じて Claude Code が**自動発火**する。Manager が直接呼ぶ必要はないが、概念は知っておく。

| スキル | 発火タイミング |
| --- | --- |
| `dimensional-check` | 物理量を含む式・コードを書く / 物理レビュー時 |
| `reproducibility-stamp` | 数値結果出力 / ベンチマーク実行 / ランダム要素を含む実験 |
| `output-discipline` | 数値・テスト・診断の出力を扱う / 大きい diff・log を参照する |
| `forbidden-list-check` | 応急処置・workaround を入れようとしているとき / 新規実装着手時 |
| `issue-tracking` | 複数日にわたる長期作業を始めるとき |
| `phase-split` | プロジェクトが性質の異なる段階に分かれるとき |
| `repo-guard-response` | repo_guard が容量警告を出したとき |

スキル本体は `.claude/skills/<name>/SKILL.md`。`.dev/HANDBOOK.md` にコマンド・cheat sheet あり (迷ったら開く)。

---

## 4. CHANGELOG の記述ルール

- 新しいエントリは**ファイル上部**に追記する (過去のエントリは編集しない)
- エントリはコミット単位で記述する
- ファイルの最上位 h1 (`# CHANGELOG`) は 1 つ。各エントリは h2 で始まり、サブ見出し (追加/変更/判断・後回し事項) は h3

```markdown
## {hash} — {タイトル}

### 追加

- ...

### 変更

- ...

### 判断・後回し事項

- ...
```

旧書式 (h3 から開始 + `**追加**` を見出し代用) は markdownlint MD001/MD036 と衝突するため廃止。新規エントリは上記新書式を用いる。
