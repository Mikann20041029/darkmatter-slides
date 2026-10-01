---
name: issue-tracking
description: 複数日にわたる作業、設計議論 + 性能計測を伴うタスク、複数タスクが束になる長期作業を開始する場面で発火。`.dev/issues/issue-N/` ディレクトリを TEMPLATE から複製してセットアップする
origin: ai-project-kickstart-template
tools: Read, Write, Edit, Bash
---

# Issue Tracking Skill

長期化・複雑化する作業のための issue 単位記録運用。`.dev/TODO.md` 直接記入では収まらない作業を扱う。

## When to Activate

以下のいずれかに該当する**新しい作業を始めるとき**:

- 複数日にわたる作業の見込み
- 設計議論 (ADR 含む) と実装の両方を要する
- 性能計測・ベンチマークが必要
- 複数タスクが束になる (5+ サブタスク)
- 並列ブランチでの作業

逆に、**軽い作業 (1-2 コミットで終わるもの) は `.dev/TODO.md` に直接書く**。issue ディレクトリは作らない。

## Procedure

### Step 1: 次の issue 番号を決める

```bash
ls .dev/issues/ 2>/dev/null | grep -E '^issue-[0-9]+$' | sort -V | tail -1
```

最後の番号 + 1 を新しい issue 番号 N とする。

### Step 2: TEMPLATE を複製

```bash
cp -r .dev/issues/TEMPLATE .dev/issues/issue-N
```

### Step 3: 構成と用途

| ファイル | 用途 |
| --- | --- |
| `WORKFLOW.md` | ブランチ運用、サブタスク ID (`T-N.x`) ルール、PR 規約 |
| `SPEC.md` | この issue の仕様 (プロジェクト全体の `.dev/SPEC.md` のサブセット) |
| `TODO.md` | この issue 内のタスク管理 |
| `HANDOFF.md` | この issue 専用の引き継ぎ (直下の HANDOFF.md は全体最新状況に専念) |
| `CHANGELOG.md` | この issue 内の変更履歴 (直下と独立) |
| `decisions/` | アーキテクチャ決定 (ADR、`NNN-<title>.md`) |

### Step 4: 直下ファイルとの関係

- 直下の `.dev/HANDOFF.md` は**プロジェクト全体の最新状況のみ**を保持する。issue 単位の細部は `.dev/issues/issue-N/HANDOFF.md` に書く
- 直下の `.dev/TODO.md` には issue へのリンクのみ残し、サブタスクは `issue-N/TODO.md` に
- 直下の `.dev/CHANGELOG.md` には issue クローズ時にサマリを 1 エントリ書く

### Step 5: issue クローズ時

issue が完了したら、`.dev/issues/closed/issue-N/` に移動する (必要なら)。

```bash
mkdir -p .dev/issues/closed
mv .dev/issues/issue-N .dev/issues/closed/
```

ただし参照頻度が高ければ `.dev/issues/issue-N/` のまま残してよい。

## ADR (Architecture Decision Record) 運用

設計議論は `.dev/issues/issue-N/decisions/NNN-<title>.md` に分離する。ファイル名は番号 + kebab-case。雛形は `.dev/issues/TEMPLATE/decisions/000-template.md`。

## Output (発火後の記録)

issue ディレクトリを作成したら、`.dev/TODO.md` の「進行中」セクションに 1 行追加:

```md
- [ ] [issue-N: タイトル](.dev/issues/issue-N/) — 1 行サマリ 🔴 🟣
```
