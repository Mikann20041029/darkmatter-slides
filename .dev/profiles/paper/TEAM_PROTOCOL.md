# TEAM_PROTOCOL.md — Paper profile (論文執筆)

このファイルは、profile=paper におけるチーム開発の正本である。ブレスト完了時に `.dev/TEAM_PROTOCOL.md` から symlink される。

共通部 (§3 モデル選定、§5 クロスレビュー定義、§6 並列性、§7 出力規律、§8 アーティファクト管理、§9 完了判定、§10 ESCALATE、§11 起動方法) は research profile と同一。詳細は [.dev/profiles/research/TEAM_PROTOCOL.md](../research/TEAM_PROTOCOL.md) を参照。本ファイルは **§1 役割定義** と **§2 Tier 編成** の profile 固有部分のみを定義する。

---

## 1. 役割定義

| 役割 | 担当 | 仕事 | やらないこと |
| --- | --- | --- | --- |
| **Manager** | メインの Claude | タスク分解、Tier 判定、チーム編成、進捗・品質管理、最終統合 | 実装・レビューは自分でしない |
| **Planner** | subagent (`.claude/agents/planner.md`) | 章構成、Introduction の論理階段設計、figure first の骨組み提案 | 実装、最終確定 |
| **Implementer** | subagent (`.claude/agents/implementer.md`) | 本文・図キャプション・式・引用を書く | 自己評価、spec 逸脱 |
| **Physical Reviewer** | subagent (`.claude/agents/reviewer-physical.md`) | 単位・次元、保存則、対称性、極限、sanity check (内容の物理的正当性) | 文章の物語構造 |
| **Numerical Reviewer** | subagent (`.claude/agents/reviewer-numerical.md`) | 有効数字 vs 誤差、安定性、収束、再現性 (seed/hash/env)、配列型整合 | 文章の物語構造 |
| **Narrative Reviewer** | subagent (`.claude/agents/reviewer-narrative.md`) | 結論先頭の徹底、章の論理階段、abstract と本文の整合、Discussion の主張一貫性 | 物理・数値の本質判断 |
| **Prior Art Reviewer** | subagent (`.claude/agents/reviewer-priorart.md`) | 先行研究の網羅、引用漏れ、競合手法との差別化、比較表の評価軸妥当性 | 文章表現 |
| **Clarity Reviewer** | subagent (`.claude/agents/reviewer-clarity.md`) | 一文一意、用語統一、図キャプションの独立性、Notation 統一、略語ルール | コード品質判断 |
| **Simplicity Reviewer** | subagent (`.claude/agents/reviewer-simplicity.md`) | 冗長表現削減、字数制約 (投稿先の文字数制限) への適合 | 内容判断 |

参照: `.dev/SOUL_addon.md` (paper) の `結論先頭の徹底`, `Figure first`, `Assumption / Approximation の明示`, `再現性` 各項。

---

## 2. Tier 編成

| Tier | 編成 | MAX_ITER | 起動条件 |
| --- | --- | --- | --- |
| **PaperPlan** (L 相当) | Planner + Implementer + narrative + priorart + cross-review (narrative ↔ priorart) | Planner 1 + impl 5 | 論文全体構成、Introduction の論理階段設計、新規論文の骨組み |
| **PaperSection** (M, default) | Implementer + physical + numerical + narrative + clarity (並列) + cross-review (physical ↔ numerical, narrative ↔ priorart は必要に応じて) | 5 | 本文章節 (Methods, Results, Discussion 等) の執筆 |
| **PaperPriorArt** (S 相当) | Implementer + priorart | 2 | 先行研究セクション・引用網羅 |
| **PaperFigure** (S 相当) | Implementer + clarity + (physical or numerical) | 2 | 図・表の追加・改訂。caption 独立性と内容の正しさを検証 |
| **PaperRevise** (M 相当) | Implementer + (査読指摘の担当 reviewer を選択して並列起動) + clarity | 5 | 査読 report への対応稿・改訂稿 |
| **PaperTrim** (Eng 相当) | Implementer + simplicity + clarity | 3 | 字数超過削減 (投稿規定の文字数制限) |
| **PaperDocs** (Docs 相当) | Implementer + clarity | 2 | abstract, cover letter, supplementary text 等の整形 |
| **XS** | Manager 直接 | 1 | typo / 数式記号の表記揺れ修正 |

### Tier 選択ルール

```text
ブリーフを読む
  │
  ├─ typo / 1-2 行修正? ────────────────────────→ XS
  │
  ├─ 字数超過の圧縮? ───────────────────────────→ PaperTrim
  │
  ├─ abstract / cover letter / supp text 整形? ─→ PaperDocs
  │
  ├─ 図・表のみの追加・改訂? ───────────────────→ PaperFigure
  │
  ├─ 先行研究セクション・引用網羅? ─────────────→ PaperPriorArt
  │
  ├─ 査読 report への対応稿? ───────────────────→ PaperRevise
  │
  ├─ 論文全体構成・新規論文の骨組み? ───────────→ PaperPlan
  │
  └─ それ以外 (本文章節執筆、default) ────────────→ PaperSection
```

### クロスレビュー

- physical ↔ numerical: research profile と同じ (両者の指摘を相互検証)
- narrative ↔ priorart: PaperPlan で必須、PaperSection で Introduction / Discussion を扱うときは推奨

### 昇格・降格

- PaperRevise で査読指摘が広範に渡る → PaperSection または PaperPlan に昇格
- PaperFigure で物理・数値の重大誤りが発覚 → PaperSection に昇格
- 査読指摘がそもそも論文の骨格 (主張、新規性) に及ぶ → PaperPlan に昇格

---

## 3〜11. 共通部

`.dev/profiles/research/TEAM_PROTOCOL.md` §3〜§11 と同一。読み替え:

- §1 で定義した役割・Tier に置き換える
- §8 アーティファクト管理に `review-narrative.md` / `review-priorart.md` / `cross-narrative-on-priorart.md` / `cross-priorart-on-narrative.md` を加える
- §7 出力規律: 図ファイルは `figures/` (commit) 又は `results/<run-id>/figures/` (出力場所) に置く。論文本体は `manuscript.tex` または `manuscript.md` を正本とする
