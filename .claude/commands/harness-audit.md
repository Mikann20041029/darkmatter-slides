---
description: プロジェクトの規律健全性を 7 軸でセルフ監査しスコアと指摘を返す。自然科学ワークフロー向けに ECC /harness-audit を再定義したもの
---

# /harness-audit — 規律セルフ監査

## 使い方

```text
/harness-audit [--scope all|core|team|results]
```

- `--scope all` (既定): 全 7 軸
- `--scope core`: 軸 1〜3 のみ (SOUL/SPEC/TODO 周り)
- `--scope team`: 軸 4〜5 のみ (チーム運用)
- `--scope results`: 軸 6〜7 のみ (再現性・成果物)

## 7 つの監査軸

各軸を 0〜10 で採点する。Node script は使わず、LLM (= あなた) がルールベースで判定する。

### 軸 1: SOUL.md 遵守度

確認項目:
- [.dev/SOUL.md](../../.dev/SOUL.md) の `Scientific Integrity` `Physical Consistency` `Reproducibility` 各セクションに反する記述・実装が直近 1 ヶ月のコミットに混入していないか
- 数値・式・結果に単位、誤差、seed/hash の併記があるか
- 検証不能表現 (「だいたい」「ほぼ」「速い」「ほぼゼロ」) が文書・コード comment に残っていないか

### 軸 2: SPEC.md ↔ 実装の整合性

- [.dev/SPEC.md](../../.dev/SPEC.md) の各節と実装ファイルの対応がとれているか
- spec に書かれた合格条件のうち、テストでカバーされていないものはいくつあるか
- spec から逸脱した実装 (commit 履歴と spec の改訂履歴を突き合わせ) が放置されていないか

### 軸 3: TODO ↔ CHANGELOG 同期

- [.dev/TODO.md](../../.dev/TODO.md) の `[x]` には `*(YYYY-MM-DD, {hash})*` が必ず付いているか
- 直近 10 コミットそれぞれに対し [.dev/CHANGELOG.md](../../.dev/CHANGELOG.md) のエントリが対応しているか
- 完了済みタスクが各セクション末尾に正しく残されているか

### 軸 4: チーム運用の健全性

- [.dev/teams/](../../.dev/teams/) が存在するなら、PASS した task-slug に `verdict.md` があるか
- 完了せず放置された task-slug (`MAX_ITER` 到達後のまま) が無いか
- レビュア report がクロスレビュー付きで残っているか

### 軸 5: HANDOFF.md 鮮度

- [.dev/HANDOFF.md](../../.dev/HANDOFF.md) の `TL;DR` 最終更新日が**直近 7 日**以内か
- 「現在のブランチ」「working tree」「直近の重要コミット」が実際の `git status` と一致するか
- 不変条件セクションが空でないか

### 軸 6: 再現性記録

- `results/` に置かれた数値結果に seed / commit hash / 環境メモが添付されているか
- ベンチマークが基準値 (baseline) との比較を含んでいるか
- ランダム要素を含む再現実験で、`reproducibility-stamp` skill 由来のスタンプが付いているか

### 軸 7: repo_guard 健全性

- [.dev/repo_guard/check_repo_size.sh](../../.dev/repo_guard/check_repo_size.sh) が直近の commit で発火していないか (= サイズ警告が出ていないか)
- `du -sh ./*` の top 5 を確認し、想定外に肥大した大物が無いか
- `.gitignore` で除外すべきものが漏れていないか

## 出力フォーマット

```markdown
## 📊 Harness Audit Report

- **日時**: YYYY-MM-DD HH:MM
- **commit**: {hash}
- **scope**: all / core / team / results

| 軸 | スコア | 状態 |
|---|---|---|
| 1. SOUL.md 遵守度       | X/10 | ✓ / ⚠ / ✗ |
| 2. SPEC.md 整合性        | X/10 | ... |
| 3. TODO ↔ CHANGELOG     | X/10 | ... |
| 4. チーム運用             | X/10 | ... |
| 5. HANDOFF.md 鮮度        | X/10 | ... |
| 6. 再現性記録             | X/10 | ... |
| 7. repo_guard            | X/10 | ... |
| **総合**                | **X.X/10** |   |

### 🔴 要対応 (CRITICAL)
- [軸N] 具体的な指摘と対処案

### 🟡 推奨 (IMPORTANT)
- ...

### 🟢 改善余地 (SUGGEST)
- ...

### ✓ 通過した検証 (記録)
- ...
```

## 採点の指針

- 0〜3: 機能していない or 重大な逸脱
- 4〜6: 部分的に機能。要改善
- 7〜8: 良好。小さな改善余地
- 9〜10: 規律として確立

主観を避け、**ファイルの実在・日付・実数値**で判定する。「印象」での減点はしない。
