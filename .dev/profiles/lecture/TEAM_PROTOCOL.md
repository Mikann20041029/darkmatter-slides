# TEAM_PROTOCOL.md — Lecture profile (講義資料 / スライド・演習・試験問題)

このファイルは、profile=lecture におけるチーム開発の正本である。ブレスト完了時に `.dev/TEAM_PROTOCOL.md` から symlink される。

共通部 (§3 モデル選定、§5 クロスレビュー定義、§6 並列性、§7 出力規律、§8 アーティファクト管理、§9 完了判定、§10 ESCALATE、§11 起動方法) は research profile と同一。詳細は [.dev/profiles/research/TEAM_PROTOCOL.md](../research/TEAM_PROTOCOL.md) を参照。本ファイルは **§1 役割定義** と **§2 Tier 編成** の profile 固有部分のみを定義する。

---

## 1. 役割定義

| 役割 | 担当 | 仕事 | やらないこと |
| --- | --- | --- | --- |
| **Manager** | メインの Claude | タスク分解、Tier 判定、チーム編成、進捗・品質管理、最終統合 | 実装・レビューは自分でしない |
| **Planner** | subagent (`.claude/agents/planner.md`) | syllabus 全体設計、学習目標 (learning objectives) 策定、prerequisite chain | 実装、最終確定 |
| **Implementer** | subagent (`.claude/agents/implementer.md`) | スライド・演習問題・試験問題・解答・解説を書く | 自己評価、spec 逸脱 |
| **Pedagogy Reviewer** | subagent (`.claude/agents/reviewer-pedagogy.md`) | scaffolding (段階性)、prerequisite の妥当性、cognitive load、misconception 予防 | 内容の物理的正しさ |
| **Examples Reviewer** | subagent (`.claude/agents/reviewer-examples.md`) | 例題の representative 性、図の messaging、典型的つまずきを突くか、キャプション独立性 | 双方向性 |
| **Engagement Reviewer** | subagent (`.claude/agents/reviewer-engagement.md`) | clicker / peer instruction / concept question への置換可否、双方向化余地 | 内容の正しさ |
| **Clarity Reviewer** | subagent (`.claude/agents/reviewer-clarity.md`) | 一文一意、用語統一、記号統一、初学者向けの分かりやすさ | コード判断 |
| **Physical Reviewer** | subagent (`.claude/agents/reviewer-physical.md`) | **内容の事実誤りチェック** (次元、保存則、極限)。既知内容でも誤植は起きる前提 | 教育設計 |
| **Numerical Reviewer** | subagent (`.claude/agents/reviewer-numerical.md`) | **演習・試験問題の解答妥当性**、数値の誤植、有効数字 | 教育設計 |
| **Simplicity Reviewer** | subagent (`.claude/agents/reviewer-simplicity.md`) | 重複説明、冗長な例題、削れる項 | 教育設計 |

参照: `.dev/SOUL_addon.md` (lecture) の `Scaffolding`, `Misconception の予防`, `双方向化`, `例題・演習問題` 各項。

---

## 2. Tier 編成

| Tier | 編成 | MAX_ITER | 起動条件 |
| --- | --- | --- | --- |
| **LecPlan** (L 相当) | Planner + Implementer + pedagogy + examples + cross-review (pedagogy ↔ examples) | Planner 1 + impl 5 | syllabus 全体設計、prerequisite chain、新規科目の骨組み |
| **LecSection** (M, default) | Implementer + pedagogy + examples + engagement + clarity + (physical or numerical, 事実誤りチェック) | 5 | 章/節を新規作成 |
| **LecSlide** (S 相当) | Implementer + Reviewer 1 (pedagogy or examples or clarity) | 2 | 1 スライド・1 問題の追加 |
| **LecExam** (M 専用) | Implementer + pedagogy + examples + numerical (解答妥当性) | 3 | 試験問題作成。難易度配分・解答の正しさ・採点基準を検証 |
| **LecExercise** (S 相当) | Implementer + examples + numerical | 2 | 演習問題の追加・改訂 (試験ではない) |
| **LecRefactor** (Eng 相当) | Implementer + simplicity + clarity | 3 | 既存講義の構成見直し、冗長削減 |
| **LecDocs** (Docs 相当) | Implementer + clarity | 2 | syllabus, 評価基準ドキュメント等の整形 |
| **XS** | Manager 直接 | 1 | typo / 記号統一 / 1-2 行修正 |

### Tier 選択ルール

```text
ブリーフを読む
  │
  ├─ typo / 記号統一 / 1-2 行修正? ────────────→ XS
  │
  ├─ syllabus / 評価基準 等の整形のみ? ────────→ LecDocs
  │
  ├─ 既存講義の構成見直し? ───────────────────→ LecRefactor
  │
  ├─ 試験問題作成? ───────────────────────────→ LecExam
  │
  ├─ 演習問題の追加・改訂 (試験以外)? ─────────→ LecExercise
  │
  ├─ 1 スライド・1 問題の追加? ────────────────→ LecSlide
  │
  ├─ syllabus 全体設計・新規科目? ─────────────→ LecPlan
  │
  └─ それ以外 (章/節を新規作成、default) ────────→ LecSection
```

### クロスレビュー

- pedagogy ↔ examples: LecPlan, LecSection, LecExam で推奨。Manager 判断で起動。
  - pedagogy-on-examples: 教育設計レビュアが「例題が段階性を破っていないか」を検証
  - examples-on-pedagogy: 例示レビュアが「段階性指摘で削った例題が representative 性を損なっていないか」を検証

### 昇格・降格

- LecSlide で複数 reviewer の CRITICAL → LecSection に昇格
- LecExam で解答妥当性 (numerical) と段階性 (pedagogy) が対立 → ユーザに ESCALATE
- LecRefactor で内容自体の問題が発覚 → LecSection に昇格

---

## 3〜11. 共通部

`.dev/profiles/research/TEAM_PROTOCOL.md` §3〜§11 と同一。読み替え:

- §1 で定義した役割・Tier に置き換える
- §8 アーティファクト管理に `review-pedagogy.md` / `review-examples.md` / `review-engagement.md` / `cross-pedagogy-on-examples.md` / `cross-examples-on-pedagogy.md` を加える
- §7 出力規律: スライドソース (Beamer `.tex`, Quarto `.qmd`, Reveal `.md` 等) と PDF を分ける。試験問題は `exams/<year>/<id>.tex` 等で問題と解答を分離
