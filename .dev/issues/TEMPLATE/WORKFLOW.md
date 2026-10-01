# Issue #N — 開発ワークフロー

このファイルは、issue 単位で長期化する作業のための運用ルール雛形である。
新しい issue を立てるときは、このディレクトリ全体を `.dev/issues/issue-N/` にコピーして使う。

---

## 1. ブランチ

| Branch | 役割 |
| --- | --- |
| `main` | 現行コード。本 issue の作業は流入させない |
| `feature/issue-N-<topic>` | 本 issue の long-lived 統合ブランチ |
| `feature/issue-N-<topic>/<sub>` | サブタスク作業ブランチ |

サブブランチ → 統合ブランチへ PR (squash merge)。完了後に統合ブランチ → `main` へ。

`main` の更新は適宜統合ブランチへ merge して同期する。

---

## 2. Issue 運用

- 本 issue (#N) をアンブレラとし、不要に新規 issue を切らない
- サブタスクは本ディレクトリの [TODO.md](TODO.md) のチェックリスト ID (`T-N.x`) で管理する
- commit / PR タイトルに ID を含める
  - 例: `feat(T-N.3): add new analyzer`
- 独立化したい論点は `decisions/NNN-<title>.md` に「issue 化見送り理由」を残してインライン処理する

---

## 3. ディレクトリ構成

```text
.dev/issues/issue-N/
  WORKFLOW.md       ← このファイル
  SPEC.md           ← 本 issue 範囲の設計
  TODO.md           ← 本 issue 範囲のタスク
  HANDOFF.md        ← 本 issue 範囲のセッション間引き継ぎ
  CHANGELOG.md      ← 本 issue 範囲の変更履歴
  decisions/        ← ADR (アーキテクチャ決定記録)
    000-template.md
  bench/            ← (任意) 性能計測の plan / measurements
  survey/           ← (任意) 調査メモ
  archive/          ← (任意) 退避済みコード・廃案の記録
```

下位ディレクトリは必要になったときだけ作る。

---

## 4. リポジトリ直下の管理ファイルとの関係

- `.dev/SPEC.md` は**プロジェクト全体**の設計の正本
- `.dev/TODO.md` は**プロジェクト全体**のタスクの正本
- 本 issue 範囲に閉じる議論は本ディレクトリ内で完結させる
- 本 issue で確定した仕様変更は `.dev/SPEC.md` にも反映する

---

## 5. issue クローズ時

- `decisions/` に最終的な合意事項が揃っていることを確認
- 本 issue 範囲の `CHANGELOG.md` をプロジェクト直下の `.dev/CHANGELOG.md` に巻き取る (任意)
- `.dev/issues/closed/issue-N/` へ移動するか、ディレクトリをそのまま残す
