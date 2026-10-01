---
name: repo-guard-response
description: pre-commit hook の repo_guard がリポジトリサイズ警告またはエラーを出したとき、または `du` でリポジトリが想定外に肥大していると判明したときに発火。原因特定と退避手順を提供する
origin: ai-project-kickstart-template
tools: Read, Edit, Bash
---

# Repo Guard Response Skill

`.dev/repo_guard/check_repo_size.sh` が警告またはエラーを出した際の対応手順。`.githooks/pre-commit` から自動的に呼ばれる。

## When to Activate

- pre-commit hook がサイズ警告を出した
- pre-commit hook がサイズ超過でコミットを失敗させた
- `du -sh .` でリポジトリが想定外 (> 1 GiB など) に肥大していると判明した
- 大きいバイナリ・データを commit に含めようとしている

## Configuration

`.dev/repo_guard/repo_size_limit` で閾値とモードを設定する:

```text
# デフォルト
limit_gib=2
warn_only=1
```

- `warn_only=1`: コミットは通る。stderr に警告と top-level の大きい順エントリを出す
- `warn_only=0`: コミットを失敗させる

hook は `.githooks/pre-commit` に置いてあるが、Git は `.git/hooks/` を見るのがデフォルトなので、初回 setup 時に次が必要:

```bash
git config core.hooksPath .githooks
```

## Procedure (警告/エラー発生時)

### Step 1: 原因特定

```bash
du -sh ./* | sort -hr | head -10
du -sh ./*/* 2>/dev/null | sort -hr | head -20
```

最大エントリを top-down で特定する。

### Step 2: 分類

| 種別 | 対応 |
| --- | --- |
| ビルド成果物 (`build/`, `target/`, `dist/`) | `.gitignore` 追加。既存 commit にあるなら `git rm --cached -r` |
| ローカル出力 (`results/`, ログ、中間ファイル) | `results/` に退避 (Git 追跡外) |
| 大きいバイナリデータ | Git LFS の検討 (必要なら) / 外部ストレージに移動 |
| node_modules / venv / __pycache__ | `.gitignore` 追加。既に追跡されているなら `git rm --cached -r` |
| 過去の大きい誤コミット | `git filter-repo` を検討 (ただし**履歴改変のため慎重に**) |

### Step 3: `.gitignore` 更新

必要なら `.gitignore` にエントリ追加:

```bash
# 例
echo "build/" >> .gitignore
echo "*.log" >> .gitignore
git add .gitignore
```

### Step 4: 既に追跡されている場合の除去

```bash
git rm --cached -r path/to/dir
# または特定ファイル
git rm --cached path/to/file
```

これで working tree からは消えず、Git の追跡からのみ外れる。

### Step 5: 再確認

```bash
.dev/repo_guard/check_repo_size.sh
du -sh .
```

警告が解消したことを確認。

## 閾値を上げる前に考えるべきこと

「サイズが大きいから閾値を上げる」は最後の手段。次を先に検討する:

1. **本当にリポジトリに置く必要があるか?** 計算結果なら `results/` で十分
2. **外部ストレージで足りるか?** 大きい入力データなら別途配布
3. **Git LFS で済むか?** バイナリ更新が頻繁なら検討
4. **過去のコミットに残った大物を消せるか?** `git filter-repo` (慎重に)

それでも上げる必要があるなら `.dev/repo_guard/repo_size_limit` を編集する。

## NG パターン

- 警告を**無視して**コミットを続ける (warn_only=1 でも対応すべき)
- 原因特定せずに**閾値を上げる**
- 大きいバイナリを `git filter-repo` せず追加で commit する (履歴に永続化)
- `git rm --cached` の代わりに `git rm` を使う (working tree のファイルまで消える)

## Output (対応後の記録)

`.dev/CHANGELOG.md` に対応内容を 1 エントリ記録:

```md
### コミット {hash} — repo_guard 警告対応

**変更**
- `.gitignore` に build/ と *.log を追加
- `path/to/big_file` を Git 追跡から除外
- リポジトリサイズ: 1.8 GiB → 420 MiB
```
