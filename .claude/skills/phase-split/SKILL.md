---
name: phase-split
description: プロジェクトが性質の異なる段階 (プロトタイプ→本実装、Fortran→C++ 移植、検証→本番など) に分かれる境界に達したと判断したときに発火。`.dev/phaseN/` 構造への移行手順を提供する
origin: ai-project-kickstart-template
tools: Read, Write, Edit, Bash
---

# Phase Split Skill

プロジェクトを `.dev/phase1/`, `.dev/phase2/` ... のように**フェーズ分割管理**する運用への移行手順。

## When to Activate

以下のいずれかに該当する**性質的に異なる段階の境界**に達したとき:

- プロトタイプ → 本実装の移行
- 言語移植 (例: Fortran → C++, Python → Rust)
- 検証 / 校正 → 本番運用
- アルゴリズム抜本変更 (旧アルゴリズム保持しつつ新アルゴリズムを並走)
- アーキテクチャ抜本変更

逆に、単一フェーズで完結するなら**導入しなくてよい**。直下の `.dev/SPEC.md` 等だけで十分。

## When NOT to Apply

- 小規模なリファクタや機能追加 (issue 単位で十分)
- フェーズと呼ぶには軽い変更
- 「念のため」の予防的フェーズ分割 (YAGNI)

## Procedure

### Step 1: 現状を `.dev/phase1/` に固定

```bash
mkdir -p .dev/phase1
cp .dev/SPEC.md .dev/TODO.md .dev/CHANGELOG.md .dev/HANDOFF.md .dev/phase1/
# 移動でも可:
# mv .dev/SPEC.md .dev/TODO.md .dev/CHANGELOG.md .dev/HANDOFF.md .dev/phase1/
```

### Step 2: 直下ファイルを「全フェーズ共通仕様 + 各フェーズへのリンク」に書き換える

例: `.dev/SPEC.md`

```md
# SPEC

全フェーズ共通の不変仕様と、各フェーズ固有仕様へのリンクを保持する。

## 不変条件 (全フェーズ共通)
- ...

## フェーズ別仕様
- [phase1](phase1/SPEC.md) — プロトタイプ (frozen)
- [phase2](phase2/SPEC.md) — 本実装 (active)
```

### Step 3: 新フェーズの作成

```bash
mkdir -p .dev/phase2
# phase1 から複製するか、新規作成する
cp .dev/phase1/SPEC.md .dev/phase2/SPEC.md  # 必要に応じて
# TODO/CHANGELOG/HANDOFF は新規でよいことが多い
```

### Step 4: 旧フェーズの freeze

`.dev/phase1/README.md` (作成) に以下を記載:

```md
# Phase 1 — <名称> (frozen as of YYYY-MM-DD)

このフェーズは凍結済み。以下を除き新規変更は加えない:

- バグ修正 (再現性を保つため必要な場合のみ)
- ドキュメント誤記の修正

新規開発は phase2 で行う。
```

### Step 5: AGENTS.md の必須読み込みを更新

セッション開始時にどのフェーズを active として読むかを明示する。`AGENTS.md §0` を編集:

```md
## 0. セッション開始時の必須読み込み
...
4. `.dev/SPEC.md` (全フェーズ共通仕様 + リンク)
5. `.dev/phase2/SPEC.md` (現フェーズ)
6. `.dev/phase2/TODO.md`
7. `.dev/phase2/HANDOFF.md`
...
```

### Step 6: TEAM_PROTOCOL.md と整合

チーム開発を併用する場合、`.dev/teams/<task-slug>/` はフェーズ非依存のままでよい。チームタスクは現フェーズの SPEC を参照する。

## 重要な不変条件

- 旧フェーズは frozen。バグ修正以外は触らない
- 直下の `.dev/SPEC.md` 等は**ナビゲーションファイル**として機能させ、実体は `phaseN/` に置く
- `git log` の連続性は維持される (ファイル移動は git mv)

## NG パターン

- 旧フェーズに新機能を継ぎ足す (frozen 違反)
- 直下の `.dev/SPEC.md` を空にする (ナビゲーションを残す)
- フェーズ移行を `.dev/CHANGELOG.md` に記録しない
