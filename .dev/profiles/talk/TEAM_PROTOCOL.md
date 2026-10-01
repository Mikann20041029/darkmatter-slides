# TEAM_PROTOCOL.md — Talk profile (学会発表)

このファイルは、profile=talk におけるチーム開発の正本である。ブレスト完了時に `.dev/TEAM_PROTOCOL.md` から symlink される。

共通部 (§3 モデル選定、§5 クロスレビュー定義、§6 並列性、§7 出力規律、§8 アーティファクト管理、§9 完了判定、§10 ESCALATE、§11 起動方法) は research profile と同一。詳細は [.dev/profiles/research/TEAM_PROTOCOL.md](../research/TEAM_PROTOCOL.md) を参照。本ファイルは **§1 役割定義** と **§2 Tier 編成** の profile 固有部分のみを定義する。

---

## 1. 役割定義

| 役割 | 担当 | 仕事 | やらないこと |
| --- | --- | --- | --- |
| **Manager** | メインの Claude | タスク分解、Tier 判定、チーム編成、進捗・品質管理、最終統合 | 実装・レビューは自分でしない |
| **Planner** | subagent (`.claude/agents/planner.md`) | スライド全体構成、time budget 設計、結論先頭スライドの位置決め | 実装、最終確定 |
| **Implementer** | subagent (`.claude/agents/implementer.md`) | スライド・スピーカーノートを書く (Beamer, Keynote, Reveal.js 等) | 自己評価、spec 逸脱 |
| **Engagement Reviewer** | subagent (`.claude/agents/reviewer-engagement.md`) | 概念質問 / clicker / peer instruction / Q&A への置換可否、聴衆との双方向化余地 | 時間配分の細部 |
| **Examples Reviewer** | subagent (`.claude/agents/reviewer-examples.md`) | 図の messaging、example の representative 性、軸ラベル可読性、annotation の有無 | 時間配分 |
| **Timing Reviewer** | subagent (`.claude/agents/reviewer-timing.md`) | スライド枚数 × 所要時間 vs 持ち時間、削れるスライドの特定、リハーサル結果との照合 | 内容の本質判断 |
| **Clarity Reviewer** | subagent (`.claude/agents/reviewer-clarity.md`) | 1 スライド 1 メッセージ、タイトルが主張になっているか、用語統一 | コード品質判断 |
| **Physical / Numerical Reviewer** | 既存 (任意起動) | 発表内容の事実誤り・次元エラー・数値の誤植チェック | 物語・engagement |
| **Simplicity Reviewer** | subagent (`.claude/agents/reviewer-simplicity.md`) | スライド上の冗長文字、不要な装飾、減らせる項目数 | 内容判断 |

参照: `.dev/SOUL_addon.md` (talk) の `1 スライド 1 メッセージ`, `時間制約は絶対`, `結論先頭` 各項。

### 持ち時間の事前確認

Manager は起動時にユーザから**持ち時間 (分)** と**質疑時間** を必ず確認する。Timing Reviewer は持ち時間が不明な場合はレビュー不能を CRITICAL で返す。

---

## 2. Tier 編成

| Tier | 編成 | MAX_ITER | 起動条件 |
| --- | --- | --- | --- |
| **TalkPlan** (L 相当) | Planner + Implementer + narrative-replacement (clarity) + engagement + timing | Planner 1 + impl 3 | スライド全体構成、time budget 設計、新規発表の骨組み |
| **TalkDeck** (M, default) | Implementer + engagement + examples + clarity + timing (並列) | 3 | スライド本体作成・改訂 |
| **TalkSlide** (S 相当) | Implementer + Reviewer 1 (clarity or examples or engagement) | 2 | 1〜数枚のスライド修正 |
| **TalkRehearsal** (Eng 相当) | Implementer + timing + simplicity | 2 | リハーサル後の時間圧縮、削るスライドの選定 |
| **TalkFactCheck** (S 相当) | Implementer + physical or numerical | 2 | 発表内容の事実誤りチェック (内容変更時、引用追加時) |
| **XS** | Manager 直接 | 1 | typo / レイアウト微調整 |

### Tier 選択ルール

```text
ブリーフを読む
  │
  ├─ typo / レイアウト微調整? ─────────────────→ XS
  │
  ├─ リハーサル後の時間圧縮? ──────────────────→ TalkRehearsal
  │
  ├─ 内容の事実誤り・引用チェック? ────────────→ TalkFactCheck
  │
  ├─ 1〜数枚のスライド修正? ───────────────────→ TalkSlide
  │
  ├─ 新規発表・全体構成? ──────────────────────→ TalkPlan
  │
  └─ それ以外 (スライド本体作成・改訂、default) → TalkDeck
```

### クロスレビュー

talk profile では原則クロスレビューを行わない (各 reviewer の観点が直交的)。代わりに Manager が consolidated-feedback で調停。

例外: TalkPlan で engagement と timing が対立する (双方向化を入れたいが時間がない等) 場合、Manager がユーザに ESCALATE して持ち時間配分の判断を仰ぐ。

### 昇格・降格

- TalkSlide で複数 reviewer の CRITICAL → TalkDeck に昇格
- TalkRehearsal で内容自体の問題が発覚 → TalkDeck に昇格

---

## 3〜11. 共通部

`.dev/profiles/research/TEAM_PROTOCOL.md` §3〜§11 と同一。読み替え:

- §1 で定義した役割・Tier に置き換える
- §8 アーティファクト管理に `review-engagement.md` / `review-examples.md` / `review-timing.md` を加える
- §7 出力規律: スライドソース (Beamer `.tex`, Keynote, Reveal `.md` 等) と PDF 出力を分ける。PDF は `results/talks/<id>/` または `dist/` に
