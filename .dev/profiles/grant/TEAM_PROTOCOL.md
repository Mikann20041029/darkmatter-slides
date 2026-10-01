# TEAM_PROTOCOL.md — Grant profile (研究企画書 / 公募・助成申請)

このファイルは、profile=grant におけるチーム開発の正本である。ブレスト完了時に `.dev/TEAM_PROTOCOL.md` から symlink される。

共通部 (§3 モデル選定、§5 クロスレビュー定義、§6 並列性、§7 出力規律、§8 アーティファクト管理、§9 完了判定、§10 ESCALATE、§11 起動方法) は research profile と同一。詳細は [.dev/profiles/research/TEAM_PROTOCOL.md](../research/TEAM_PROTOCOL.md) を参照。本ファイルは **§1 役割定義** と **§2 Tier 編成** の profile 固有部分のみを定義する。

---

## 1. 役割定義

| 役割 | 担当 | 仕事 | やらないこと |
| --- | --- | --- | --- |
| **Manager** | メインの Claude | タスク分解、Tier 判定、チーム編成、進捗・品質管理、最終統合 | 実装・レビューは自分でしない |
| **Planner** | subagent (`.claude/agents/planner.md`) | 公募要項を読み、応募者の業績・計画から narrative angle を 2-3 案起案。spec ドラフト作成 | 実装、最終確定 |
| **Implementer** | subagent (`.claude/agents/implementer.md`) | spec に従って文章を書く (申請書本体、業績欄、研究計画等) | 自己評価、spec 逸脱 |
| **Narrative Reviewer** | subagent (`.claude/agents/reviewer-narrative.md`) | why-now / why-me / why-this の論理階段、起承転結、ストーリーの一貫性 | 公募要項適合性の細部 |
| **Fit Reviewer** | subagent (`.claude/agents/reviewer-fit.md`) | 公募要項 (call.pdf) の必須要件・評価基準・字数/様式制約への適合 | 文章の表現品質 |
| **Feasibility Reviewer** | subagent (`.claude/agents/reviewer-feasibility.md`) | 予算・期間・体制・リスクの現実性、マイルストーン整合、過剰約束の検出 | 文章の論理構造 |
| **Clarity Reviewer** | subagent (`.claude/agents/reviewer-clarity.md`) | 一文一意、用語統一、結論先頭、専門用語のレイヤ管理 | 公募適合性の判断 |
| **Simplicity Reviewer** | subagent (`.claude/agents/reviewer-simplicity.md`) | 冗長表現削減、字数制約への適合 (Trim 用途) | 内容判断 |

参照: `.dev/SOUL_addon.md` (grant) の `Narrative の三本柱`, `公募適合性`, `過剰約束の禁止` 各項。

### 公募要項の配置

公募要項 (call for proposals) を `.dev/teams/<slug>/call.pdf` または `.dev/proposals/<grant-name>/call.pdf` に配置する。Planner と Fit Reviewer は `Read` で必ず開く。要項が存在しない場合は Manager がユーザに確認する。

---

## 2. Tier 編成

| Tier | 編成 | MAX_ITER | 起動条件 |
| --- | --- | --- | --- |
| **GrantPlan** (L 相当) | Planner + Implementer + narrative + fit + feasibility + cross-review (narrative ↔ fit) | Planner 1 + impl 5 | 企画全体構想。narrative angle を複数比較。新規申請の初稿 |
| **GrantDraft** (M, default) | Implementer + narrative + fit + clarity (並列) + cross-review (narrative ↔ fit) | 5 | 章単位の新規執筆 (研究目的、方法、計画、業績 等) |
| **GrantRevise** (S 相当) | Implementer + Reviewer 1 (narrative or fit or feasibility) | 2 | レビュー指摘の反映、改訂稿。主観点 1 つの場合 |
| **CV / 業績** (Docs 相当) | Implementer + clarity | 2 | 業績リスト整形、研究履歴整理、字数調整 |
| **Trim** (Eng 相当) | Implementer + simplicity + clarity | 2 | 字数超過の圧縮、冗長削減 |
| **XS** | Manager 直接 | 1 | typo / 表記揺れ / 数値 1 点の修正 |

### Tier 選択ルール

```text
ブリーフを読む
  │
  ├─ typo / 表記揺れ / 1-2 行修正? ──────────────→ XS
  │
  ├─ 字数超過の圧縮のみ? ────────────────────────→ Trim
  │
  ├─ 業績リスト・CV の整形? ─────────────────────→ CV
  │
  ├─ 企画全体の構想・narrative angle 決定?
  │   (新規申請の初稿、再応募の戦略練り直し) ──→ GrantPlan
  │
  ├─ 既稿の改訂・指摘反映?
  │   (主観点 1 つ) ─────────────────────────────→ GrantRevise
  │
  └─ それ以外 (新規章執筆、default) ──────────────→ GrantDraft
```

### クロスレビュー (Tier=GrantPlan, GrantDraft のみ)

- narrative-on-fit: 物語性レビュアが「適合性指摘の物語構造への影響」を検証
- fit-on-narrative: 適合性レビュアが「物語構造変更による要項違反リスク」を検証

feasibility は単独で動く (cross-review は narrative↔fit のみ)。

### 昇格・降格

- GrantRevise で複数観点の CRITICAL が出た → GrantDraft に昇格
- GrantDraft で実装方針 (narrative angle) 自体に疑義が生じた → GrantPlan に昇格 (Planner 再起動)
- 字数制約違反が複数 reviewer から出た → Trim を別チームで並行起動

---

## 3〜11. 共通部

`.dev/profiles/research/TEAM_PROTOCOL.md` §3〜§11 と同一。読み替え:

- §1 で定義した役割・Tier に置き換える
- §8 アーティファクト管理の命名規約は `.dev/teams/<task-slug>/` 配下に `review-narrative.md` / `review-fit.md` / `review-feasibility.md` / `cross-narrative-on-fit.md` / `cross-fit-on-narrative.md` を加える
