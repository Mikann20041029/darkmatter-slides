# HANDBOOK — 開発フェーズ用ハンドブック

このファイルは、初期ブレストから本実装フェーズへ移行した直後のユーザに**選択肢と参考情報**を提示する、長寿のハンドブックである。

構成:

1. 移行直後のオプション設定 (Manager がユーザに提示し、採否を記録する)
2. よく使うプロンプト集
3. コマンド・スキル・エージェント cheat sheet
4. 移行記録 (migration 時に Manager が記入)

---

## 1. 移行直後のオプション設定

このセクションは、本実装フェーズ移行直後に Manager が**ユーザに提示**し、採否を確認する。採用したものは §4 移行記録に記入する。

### 1.1. rtk (Rust Token Killer) — token 圧縮 proxy

**機能**: Bash 経由のコマンド出力 (git / test / lint / grep / cat 等) を圧縮し、LLM コンテキストへ流すトークン数を 60-90% 削減する。

**前提・本テンプレートとの整合**:

- 本テンプレは `output-discipline` skill で「数値・テスト・診断の出力は必ずファイル化」を規約化済み。レビュアは `Read` tool で正本ファイルを読むため、rtk 圧縮の影響を受けない設計
- レビュー品質への懸念は規律で排除済み

**前提・懸念事項**:

- License 不整合: rtk README は MIT バッジ、実 LICENSE は Apache-2.0
- スター数 45,908 (5 ヶ月の Rust CLI として不自然に高い) — 信頼性評価は別途必要
- crate 名衝突: `cargo install rtk` だと別プロジェクト (Rust Type Kit) が入る可能性。**必ず** `--git` で source 指定する

**導入手順 (採用する場合)**:

```bash
# 1. install.sh を先に審査
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh | less

# 2. cargo from source でビルド (より監査しやすい)
cargo install --git https://github.com/rtk-ai/rtk

# 3. インストール検証 (Token Killer であることを確認)
rtk --version
rtk gain   # これが動かない場合、別の rtk が入っている

# 4. 本プロジェクト限定で hook-only セットアップ
rtk init --hook-only

# 5. 書き込み内容を審査してから commit
git diff .claude/settings.json
```

**スコープ選択肢**:

| スコープ | コマンド | 影響範囲 |
| --- | --- | --- |
| 本プロジェクト限定 hook-only (推奨) | `rtk init --hook-only` | このリポジトリの `.claude/settings.json` のみ |
| binary のみ (手動起動) | binary install のみ | 自動圧縮無し、必要時に `rtk grep` 等を手動で叩く |
| グローバル | `rtk init -g` | 全 Claude Code セッション (他プロジェクトのレビュー品質にも影響) |

**採否を §4 に記録する**。

### 1.2. 静的型 checker のセットアップ

**背景**: [.dev/SOUL.md](SOUL.md) `Coding Standards` で「静的型を優先する」を規約化している。本テンプレは言語非依存なので、子プロジェクトが採用言語を決めた時点で対応する type checker を CI / pre-commit に組み込む。

**Manager がユーザに尋ねる項目**: 採用言語と type checker を確認し、対応する設定ファイルを生成する。

#### Python の場合

選択肢: `mypy --strict` または `pyright` strict mode (どちらかを採用)。

`pyproject.toml` に以下を追加:

```toml
# mypy を使う場合
[tool.mypy]
strict = true
python_version = "3.12"
warn_return_any = true
warn_unused_ignores = true

# pyright を使う場合
[tool.pyright]
typeCheckingMode = "strict"
pythonVersion = "3.12"
```

`.pre-commit-config.yaml` の例 (mypy):

```yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.11.0
    hooks:
      - id: mypy
        args: [--strict]
        additional_dependencies: [numpy, types-requests]
```

数値配列の型は `numpy.typing.NDArray[np.float64]` または `jaxtyping` (PyTorch/JAX 利用時) を用いる。

#### TypeScript の場合

`tsconfig.json`:

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUncheckedIndexedAccess": true
  }
}
```

`.pre-commit-config.yaml` の例:

```yaml
repos:
  - repo: local
    hooks:
      - id: tsc
        name: TypeScript type check
        entry: npx tsc --noEmit
        language: system
        types: [ts]
        pass_filenames: false
```

#### Rust の場合

標準で型強制。`clippy` を pre-commit に組み込む:

```yaml
repos:
  - repo: local
    hooks:
      - id: clippy
        name: cargo clippy
        entry: cargo clippy -- -D warnings
        language: system
        types: [rust]
        pass_filenames: false
```

#### Julia の場合

Julia は型 annotation がオプショナル (multiple dispatch が本質)。型強制を目的とするより、`@assert` と test suite で型契約を検証する運用が現実的。`JET.jl` で静的解析を回せる:

```julia
# test/runtests.jl
using JET
@test_opt my_function(args...)  # 型推論の不安定性を検出
```

#### C++ の場合

`-Wall -Wextra -Wpedantic -Werror` をビルドフラグに、`clang-tidy` を pre-commit に組み込む。`auto` の濫用を避け、関数 signature では明示型を使う。

#### Fortran の場合

`implicit none` を全モジュールで宣言。コンパイラフラグ `-fimplicit-none -Wall -Wextra` を使う (gfortran)。

**採否を §4 に記録する** (採用した言語と checker、設定ファイルのパス)。

### 1.3. markdownlint 設定 (任意採用)

**背景**: テンプレ既定の Markdown 書式 (CLAUDE.md の `@import` 冒頭、CHANGELOG の h2/h3 構造、テーブル `| --- | --- |` 形式、コードブロック言語タグ必須、プレースホルダ `` `<name>` ``) を強制するため、`.markdownlint.json` を repo 直下に同梱している。content:

```json
{
  "default": true,
  "MD013": false,
  "MD024": { "siblings_only": true }
}
```

- `MD013` (line-length): 日本語混在文書では実用不能のため disable
- `MD024` (no-duplicate-heading): CHANGELOG の各エントリで `### 追加 / ### 変更 / ### 判断・後回し事項` が再帰的に出現するため、`siblings_only: true` で同一 h2 セクション内の重複のみ検査
- 除外パス: `.markdownlintignore` で `.template/`, `.dev/teams/`, `.dev/issues/issue-*/`, `results/`, `node_modules/` を指定

**Manager がユーザに尋ねる項目**:

- (a) **エディタの markdownlint 拡張** (VSCode 等) を有効化するか
- (b) **pre-commit hook** で `markdownlint-cli2` を強制実行するか (推奨だが任意)

**(a) エディタ拡張**: VSCode の `DavidAnson.vscode-markdownlint` 拡張を入れれば、repo の `.markdownlint.json` を自動認識する。追加設定不要。

**(b) pre-commit hook** 採用時の手順:

```bash
# 1. markdownlint-cli2 をインストール
npm install -g markdownlint-cli2

# 2. .pre-commit-config.yaml に追加
cat >> .pre-commit-config.yaml <<'EOF'
repos:
  - repo: https://github.com/DavidAnson/markdownlint-cli2
    rev: v0.13.0
    hooks:
      - id: markdownlint-cli2
        files: \.md$
EOF

# 3. 有効化
pre-commit install
```

利用者プロジェクトで rule を追加無効化したい場合は、`.markdownlint.json` を編集する。

**採否を §4 に記録する** (採用した場合、エディタ拡張のみ / pre-commit hook も / 不採用)。

---

## 2. よく使うプロンプト集

### 2.1. セッション開始時

Claude Code は `CLAUDE.md` を自動ロードし、これが `@AGENTS.md` を import するため、AI は AGENTS.md を**既に読んだ状態でセッションを始める**。AGENTS.md §0 の他ファイル (SOUL / SPEC / TODO / HANDOFF / FORBIDDEN / TEAM_PROTOCOL) は AI が §0 指示に従って自主的に読みに行く想定。

**最初のプロンプト例**:

- 「現状を 3 行で要約してください (`HANDOFF.md` TL;DR + `TODO.md` 進行中最上位)」
- 「`.dev/TODO.md` の『進行中』最上位を確認し、続きから着手してください」
- 「直近 3 コミットの主旨を `.dev/CHANGELOG.md` から要約してください」

**明示的に必須読み込みを促したい場合**:

- 「`AGENTS.md` §0 の必須読み込みを完了したら、`HANDOFF.md` の TL;DR を 3 行で要約してください」

> CLAUDE.md 自動ロードが効かないツール (Codex CLI 等) を使う場合は「`AGENTS.md` を読み込んでください」を最初に投げる必要がある。

### 2.2. 作業中

- 「`/team-task <ブリーフ>` でこの作業をマルチエージェントチームで進めてください」
- 「`/aside <短い質問>` — タスク中断せず短答」
- 「`/harness-audit` で現在の規律状況を点検してください」

### 2.3. 仕様変更

- 「仕様変更を入れます。`.dev/SPEC.md` を最新の実装に合わせて更新してください。変更理由も明記」
- 「SPEC の §X を以下に修正: <変更内容>。実装側の整合性も確認してください」

### 2.4. ドキュメント更新

- 「直近 commit を `.dev/CHANGELOG.md` に追記してください (`AGENTS.md` §10 の書式)」
- 「`.dev/TODO.md` の完了タスクに `*(YYYY-MM-DD, {hash})*` を付け、各セクション末尾へ移動してください」

### 2.5. セッション終了時

- 「今日の作業を `.dev/HANDOFF.md` に反映してください。状況サマリ 3 行、不変条件、次セッションの context を更新」
- 「次セッションが最初に開くべきファイル/コマンドを HANDOFF の context セクションに追記してください」

### 2.6. 応急処置を入れたいとき

- 「これは応急処置になります。`forbidden-list-check` skill を踏まえて `.dev/FORBIDDEN.md` と照合してください。撤去条件と期限を SPEC または HANDOFF に明記」

### 2.7. 長期化しそうな作業

- 「これは複数日になりそうなので `issue-tracking` skill で `.dev/issues/issue-N/` を立てて管理してください」

### 2.8. 数値計算実行時

- 「この計算を回します。`reproducibility-stamp` と `output-discipline` skill に従って `results/<run-id>/` 配下に結果・meta・summary を保存」
- 「ベンチマーク baseline と比較し、誤差バー込みで報告してください」

### 2.9. レビュー要請

- 「直近の変更について `reviewer-physical` と `reviewer-numerical` をクロスレビュー付きで起動してください」

### 2.10. フェーズ境界に到達

- 「これでプロトタイプは完了です。`phase-split` skill で `.dev/phase1/` に固定し、phase2 に移ります」

---

## 3. コマンド・スキル・エージェント cheat sheet

### Slash commands

| コマンド | 用途 | 定義 |
| --- | --- | --- |
| `/team-task <ブリーフ>` | マルチエージェントチーム起動 | `.claude/commands/team-task.md` |
| `/harness-audit` | 7 軸セルフ監査 | `.claude/commands/harness-audit.md` |
| `/aside <質問>` | タスク中断せず短答 | `.claude/commands/aside.md` |

### Skills (Claude Code が文脈で自動発火)

| スキル | 発火条件 | 定義 |
| --- | --- | --- |
| `dimensional-check` | 物理量を含む式・コードを書く / 物理レビュー時 | `.claude/skills/dimensional-check/` |
| `reproducibility-stamp` | 数値結果出力 / ベンチマーク実行 / ランダム要素を含む実験 | `.claude/skills/reproducibility-stamp/` |
| `output-discipline` | 数値・テスト・診断の出力 / 大きい diff/log / レビュアが詳細出力を必要 | `.claude/skills/output-discipline/` |
| `forbidden-list-check` | 応急処置・workaround を入れようとしている / 新規実装着手時 | `.claude/skills/forbidden-list-check/` |
| `issue-tracking` | 複数日にわたる長期作業を始めるとき | `.claude/skills/issue-tracking/` |
| `phase-split` | プロジェクトが性質の異なる段階に分かれるとき | `.claude/skills/phase-split/` |
| `repo-guard-response` | repo_guard が容量警告を出した / リポジトリ肥大時 | `.claude/skills/repo-guard-response/` |

### Subagents (`Agent` tool の `subagent_type` で呼ぶ)

全 profile の reviewer を `.claude/agents/` に常設している。profile に応じて Manager が起動を選択する。

| エージェント | 役割 | 既定 model | 主な使用 profile |
| --- | --- | --- | --- |
| `planner` | 設計担当 (spec ドラフト・複数方針) | opus | 全 profile の L 相当 tier |
| `implementer` | 実装担当 | sonnet | 全 profile |
| `reviewer-physical` | 物理レビュー (単位/保存則/対称性/極限) | sonnet | research, paper, lecture (事実誤りチェック), talk (任意) |
| `reviewer-numerical` | 数値レビュー (誤差/安定性/収束/再現性) | sonnet | research, paper, lecture (解答妥当性), talk (任意) |
| `reviewer-simplicity` | コード/文書の重複・冗長・型注釈規律 | sonnet | research (Eng), paper (Trim), grant (Trim), 他 |
| `reviewer-clarity` | 一文一意/用語統一/結論先頭/キャプション独立性 | sonnet | 全 profile (Docs / default の一部) |
| `reviewer-narrative` | 物語性 (why-now/me/this, 論理階段) | sonnet | grant, paper |
| `reviewer-fit` | 公募要項適合性 (必須要件/評価基準/字数様式) | sonnet | grant |
| `reviewer-feasibility` | 実現可能性 (予算/期間/体制/リスク/過剰約束) | sonnet | grant |
| `reviewer-priorart` | 先行研究網羅・差別化・引用正確性 | sonnet | paper |
| `reviewer-pedagogy` | scaffolding/prerequisite/cognitive load/misconception | sonnet | lecture |
| `reviewer-examples` | 例題 representative 性/図 messaging/キャプション | sonnet | lecture, talk |
| `reviewer-engagement` | 双方向化 (clicker/peer instruction/concept question) | sonnet | lecture, talk |
| `reviewer-timing` | 時間配分 (スライド枚数 × 所要時間 vs 持ち時間) | sonnet | talk |

モデル上書き (opus / haiku) は `.dev/profiles/research/TEAM_PROTOCOL.md` §3 の基準を全 profile で共通適用。重要 reviewer は opus、軽微 diff は haiku に降ろす。

詳細は `.dev/TEAM_PROTOCOL.md` (現 profile の symlink) と `.dev/profiles/<profile>/TEAM_PROTOCOL.md` を参照。

### モデル選定ポリシー (再掲)

- **opus**: アーキテクチャ設計、重要な実装、難しいバグ調査
- **sonnet**: 通常の実装、ドキュメント生成、コードレビュー
- **haiku**: 単純修正、繰り返しタスク、定型処理

---

## 4. 移行記録 (migration 時に Manager が記入)

- 移行日: 2026-05-25
- 移行 commit: `8ddec70`（Initial commit から移行）
- **採用 profile**: research
  - 副 profile (複数併用時): なし
  - 焼き付け方法: symlink（`.dev/TEAM_PROTOCOL.md` → `profiles/research/TEAM_PROTOCOL.md`、`.dev/SOUL_addon.md` → `profiles/research/SOUL_addon.md`）
- 採用したオプション設定:
  - [x] §1.1 rtk — **不採用**（ライセンス不整合・信頼性懸念のため）
  - [x] §1.2 静的型 checker — **不採用**（研究解析スクリプトへの strict 型付けはオーバースペック）
  - [x] §1.3 markdownlint 設定 — **VSCode 拡張のみ採用**（`DavidAnson.vscode-markdownlint`、`.markdownlint.json` は既存）
- 移行時点のフェーズ管理: 単一フェーズ

---

## 補足: 本ファイルの位置づけ

- このファイルは**長寿の参考資料**である。毎セッションの必須読み込みではない (`AGENTS.md` §0 には含めない)
- §1 (オプション) は初回のみ参照。§2-§3 は開発中いつでも参照
- 新しい slash command / skill / subagent / プロンプト パターンが増えたら、ここを更新する
