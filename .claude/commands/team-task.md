---
description: profile (grant/research/paper/talk/lecture) に応じた Tier 編成でマルチエージェントチームを起動する。Tier 一覧と編成は .dev/TEAM_PROTOCOL.md (現 profile) を参照
---

# /team-task — マルチエージェントチーム起動

## 使い方

```text
/team-task <ブリーフ> [--profile P] [--tier T] [--max-iter N] [--teams M] [--lightweight]
```

- `<ブリーフ>`: 何をしたいか (1〜3 行で十分)
- `--profile P`: profile 明示指定 (省略時は `.dev/SPEC.md` 冒頭の `Profile:` 行を正本とする)
- `--tier T`: Tier 明示指定 (省略時は Manager が自動判定。Tier 名は profile に依存)
- `--max-iter N`: 反復上限 (省略時は Tier 既定値)
- `--teams M`: 編成するチーム数 (既定: Manager が自動分解)
- `--lightweight`: `.dev/teams/<slug>/` を作らず chat 内応答のみで完結

## Profile の解決順

1. `--profile` オプション (明示上書き)
2. `.dev/SPEC.md` 冒頭の `Profile:` 行 (正本)
3. `.dev/TEAM_PROTOCOL.md` (symlink 先) の profile 名 (フォールバック)

いずれでも特定できない場合、Manager はユーザに 1 度だけ profile を確認する。

## Manager (= あなた) の手順

### Phase 0 — Profile 確認・タスク受領・Tier 判定

1. **Profile を解決**: `--profile` 引数 → `.dev/SPEC.md` 冒頭の `Profile:` → `.dev/TEAM_PROTOCOL.md` の symlink 先、の順に確認
2. ブリーフを熟読する
3. 不明点があればこの時点でユーザに 1 問だけ確認 (ブレストではないので深掘りしない)
4. **Tier を判定する**: 解決した profile に応じて、対応する `.dev/profiles/<profile>/TEAM_PROTOCOL.md` の §2 (Tier 選択ルール) を参照する。Tier 名は profile に依存する:
   - `grant`: GrantPlan / GrantDraft / GrantRevise / CV / Trim / XS
   - `research`: XS / S / M / L / Eng / Docs (既存)
   - `paper`: PaperPlan / PaperSection / PaperPriorArt / PaperFigure / PaperRevise / PaperTrim / PaperDocs / XS
   - `talk`: TalkPlan / TalkDeck / TalkSlide / TalkRehearsal / TalkFactCheck / XS
   - `lecture`: LecPlan / LecSection / LecSlide / LecExam / LecExercise / LecRefactor / LecDocs / XS

   判定根拠を 1 行でメモして以後の進行に使う。
5. タスクを並列可能な単位に分解する (Tier はサブタスクごとに判定し直してよい)
6. 各サブタスクに **task-slug** を割り当て (kebab-case)
7. **モデル選定** (全 profile 共通、`.dev/profiles/research/TEAM_PROTOCOL.md` §3):
   - アーキテクチャ設計・重要実装・難バグ・Planner → opus
   - 通常実装・文書・レビュー → sonnet
   - 単純修正・反復・定型 → haiku
8. `--lightweight` 指定が無く、Tier が XS でないなら:
   - `.dev/teams/<slug>/spec.md` を Manager が書く (合格条件込み)
   - Planner を起動する Tier (各 profile の L 相当: GrantPlan / PaperPlan / TalkPlan / LecPlan / research L) の場合は先に Planner を起動して `spec-draft.md` を出させ、Manager が改訂して `spec.md` を確定
   - `.dev/teams/<slug>/iter-001/` を作成
   - grant profile で公募要項を扱う場合は `call.pdf` を `.dev/teams/<slug>/` または `.dev/proposals/<grant>/` に配置済みであることを確認

### Phase 1 — Tier 別の編成と反復ループ

Tier 別の編成 (どの reviewer を並列起動するか、クロスレビューの有無、MAX_ITER) は **profile 固有**。`.dev/TEAM_PROTOCOL.md` (現 profile, symlink) の §1〜§2 を参照して編成を決める。

共通骨格:

```text
iter = 1
while iter <= MAX_ITER(Tier):

  # Step A: Implementer
  Agent(subagent_type="implementer", model=<選定>,
        prompt="<spec> + iter=N + アーティファクト先 + (N>=2なら) 前回consolidated-feedback")

  # Step B: profile・Tier に対応する Reviewer 群を並列起動
  並列に:
    Agent(subagent_type="<reviewer-1>", model=<選定>, prompt="<spec> + 実装アーティファクト")
    Agent(subagent_type="<reviewer-2>", ...)
    ...

  # Step C: クロスレビュー (Tier が cross-review を要求する場合のみ、並列)
  並列に:
    Agent(subagent_type="<reviewer-A>", prompt="review-<B>-NNN.md を <A 観点> で検証")
    Agent(subagent_type="<reviewer-B>", prompt="review-<A>-NNN.md を <B 観点> で検証")

  # Step D: Manager 判定
  Manager が全 report を読み consolidated-feedback-NNN.md を書く
  CRITICAL 0 → PASS / それ以外 → FAIL, iter += 1
```

#### Profile 別の Tier↔編成 早見

profile に応じた reviewer 集合とクロスレビューの組合せ:

- **grant**:
  - GrantPlan: planner + implementer + narrative + fit + feasibility, cross: narrative ↔ fit
  - GrantDraft (default): implementer + narrative + fit + clarity, cross: narrative ↔ fit
  - GrantRevise: implementer + reviewer 1 (narrative/fit/feasibility)
  - CV: implementer + clarity
  - Trim: implementer + simplicity + clarity
  - XS: Manager 直接

- **research**: 既存 (`.dev/profiles/research/TEAM_PROTOCOL.md` §2)
  - XS / S / M (physical+numerical+cross) / L (planner+M) / Eng (simplicity) / Docs (clarity)

- **paper**:
  - PaperPlan: planner + implementer + narrative + priorart, cross: narrative ↔ priorart
  - PaperSection (default): implementer + physical + numerical + narrative + clarity, cross: physical ↔ numerical (narrative ↔ priorart は Intro/Discussion で)
  - PaperPriorArt: implementer + priorart
  - PaperFigure: implementer + clarity + (physical or numerical)
  - PaperRevise: implementer + 査読指摘の担当 reviewer + clarity
  - PaperTrim: implementer + simplicity + clarity
  - PaperDocs: implementer + clarity
  - XS: Manager 直接

- **talk**:
  - TalkPlan: planner + implementer + clarity + engagement + timing
  - TalkDeck (default): implementer + engagement + examples + clarity + timing
  - TalkSlide: implementer + reviewer 1 (clarity/examples/engagement)
  - TalkRehearsal: implementer + timing + simplicity
  - TalkFactCheck: implementer + (physical or numerical)
  - XS: Manager 直接

- **lecture**:
  - LecPlan: planner + implementer + pedagogy + examples, cross: pedagogy ↔ examples
  - LecSection (default): implementer + pedagogy + examples + engagement + clarity + (physical or numerical 任意)
  - LecSlide: implementer + reviewer 1 (pedagogy/examples/clarity)
  - LecExam: implementer + pedagogy + examples + numerical
  - LecExercise: implementer + examples + numerical
  - LecRefactor: implementer + simplicity + clarity
  - LecDocs: implementer + clarity
  - XS: Manager 直接

MAX_ITER はそれぞれの profile の TEAM_PROTOCOL.md §2 を正本とする (research の M=5 を基準に、軽量 Tier は 2-3)。

#### XS tier (全 profile 共通)

Phase 1 を agent に委譲しない。Manager が直接 Edit/Write し、完了後セルフチェック。必要なら `/harness-audit` を 1 回回す。verdict は chat 内で口頭報告。

#### L 相当 tier (Planner 必須)

Planner を **1 回起動** してから default tier (M / GrantDraft / PaperSection / TalkDeck / LecSection) と同じループに入る:

```text
# Phase 0.5: Planner
Agent(subagent_type="planner", model="opus",
      prompt="<ブリーフ> + task-slug + アーティファクト先 + profile")
出力: .dev/teams/<slug>/spec-draft.md

# Manager が spec-draft.md を読み、採否判断のうえ spec.md を確定

# Phase 1: default tier と同じループ
```

Planner を再起動するのは spec 自体の不備で iter が回らない場合のみ (ESCALATE 検討と並行)。

### Phase 2 — 統合

1. 全チームの成果を統合
2. チーム間の整合性 (API, 命名, 依存) を確認
3. 必要に応じて `/harness-audit` を走らせる
4. [.dev/CHANGELOG.md](../../.dev/CHANGELOG.md) に記録
5. [.dev/TODO.md](../../.dev/TODO.md) を更新

## 並列実行の作法

`Agent` tool 呼び出しは**独立なものを 1 メッセージで複数発火**する。default tier (M / GrantDraft / PaperSection / TalkDeck / LecSection) と L 相当 tier の Step B (一次レビュー) と Step C (クロスレビュー) は必ず並列。複数チームの Phase 1 も依存が無ければ並列。

## 出力例 (ユーザへのレポート)

```markdown
## /team-task レポート

**Profile**: <grant|research|paper|talk|lecture>
**ブリーフ**: ...
**Tier 判定**: <Tier name> (default または明示理由)
**結果**: PASS (チーム K/K, 平均 N iter)

### チーム a: <task-slug> (Tier=<T>)
- iter 1 → 2 で PASS。<reviewer-X> CRITICAL N 件、<reviewer-Y> CRITICAL M 件を解消
- 主要変更: <path:line>, <path>

### チーム b: <task-slug> (Tier=<T>)
- iter 1 で PASS

### 残課題 (SUGGEST レベル、後回し)
- ...
```

## 起動しない場面

- ブレスト中 (profile 未確定。`.dev/TEAM_PROTOCOL.md` が stub のまま)
- 単純な質問への回答 (チーム起動は過剰)
- 1-2 行の機械的修正 (XS tier 相当、Manager 直接編集で十分)
- ファイル 1〜2 行の修正 (XS tier 相当、Manager 直接編集で十分)
