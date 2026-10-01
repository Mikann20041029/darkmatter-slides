# TEAM_PROTOCOL.md — Research profile (自然科学研究 / 数値コード)

このファイルは、profile=research におけるチーム開発の正本である。ブレスト完了時に `.dev/TEAM_PROTOCOL.md` から symlink される。他 profile (grant / paper / talk / lecture) は `.dev/profiles/<P>/TEAM_PROTOCOL.md` を参照。

採用パターン: ECC (everything-claude-code) の GAN-style multi-agent harness を、自然科学ワークフロー向けに再構成したもの。Anthropic harness design paper (2026-03) に着想。

---

## 1. 役割定義

| 役割 | 担当 | 仕事 | やらないこと |
| --- | --- | --- | --- |
| **Manager** | メインの Claude (= 対話に答えるエージェント) | タスク分解、Tier 判定、チーム編成、進捗・品質管理、最終統合 | **自分で実装しない**、自分でレビューしない |
| **Planner** | subagent (`.claude/agents/planner.md`) | 設計空間が開いたタスクの spec ドラフト作成。複数案を提示 | 実装、レビュー、spec の最終確定 |
| **Implementer** | subagent (`.claude/agents/implementer.md`) | spec に従って実装 (コード・計算・文書) | 自己評価、spec 逸脱 |
| **Physical Reviewer** | subagent (`.claude/agents/reviewer-physical.md`) | 単位・次元、保存則、対称性、極限、sanity check | 実装、数値安定性の細部 |
| **Numerical Reviewer** | subagent (`.claude/agents/reviewer-numerical.md`) | 有効数字 vs 誤差、安定性、収束、再現性、配列の dtype/shape 型整合 | 実装、物理解釈の本質判断 |
| **Simplicity Reviewer** | subagent (`.claude/agents/reviewer-simplicity.md`) | 重複コード、過剰抽象化、API surface、命名一貫性、dead code、型注釈規律 (`Any`/無注釈の濫用検出) | 物理・数値の本質判断 |
| **Clarity Reviewer** | subagent (`.claude/agents/reviewer-clarity.md`) | 一文一意、用語統一、結論先頭、キャプション独立性 | コード品質判断 |

- Planner の出力は **ドラフト**。Manager が採否を判断し、必要に応じて改訂のうえ最終 `spec.md` を確定する。
- 物理・数値レビュアの観点は `.dev/SOUL_addon.md` (research) の `Physical Consistency` および `Reproducibility` に対応する。
- Simplicity / Clarity レビュアの観点は `.dev/SOUL.md` (共通 core) の `Writing & Documentation` に対応する。
- 型規律 (Simplicity / Numerical 両レビュアの観点) は `.dev/SOUL_addon.md` (research) の `Coding Standards` に対応する。

---

## 2. Tier 編成

タスクの性質と規模に応じて Manager が **Tier** を選び、編成を決める。

| Tier | 編成 | MAX_ITER | 起動条件 |
| --- | --- | --- | --- |
| **XS** | Manager 直接 (subagent なし) | 1 | typo / rename / format / 1-2 行の機械的修正。完了後 Manager がセルフチェック |
| **S** | Implementer + Reviewer*1 (physical _or_ numerical) | 2 | 単一観点の fix。両観点に該当するなら M に昇格 |
| **M** | Implementer + Reviewer*2 (physical + numerical) + cross-review | 5 | 通常の科学計算タスク。**default** |
| **L** | Planner + Implementer + Reviewer*2 + cross-review | Planner 1 + impl iter 5 | 設計空間が開いた新規実装、新規物理モデル導入、複数の実装方針が成立するタスク |
| **Eng** | Implementer + reviewer-simplicity | 3 | リファクタ、ハーネス整備、CI/ツーリング変更 |
| **Docs** | Implementer + reviewer-clarity | 2 | README / SPEC / AGENTS / 論文ドラフト等の文書整理 |

### Tier 選択ルール (Manager の判断フロー)

```text
ブリーフを読む
  │
  ├─ コード変更なし、文書のみ? ─────────────────→ Docs
  │
  ├─ コード変更だが、物理量・数値計算を含まない?
  │  (リファクタ、ツーリング、ハーネス整備など) ──→ Eng
  │
  ├─ 物理量・数値計算を含むコード変更?
  │  │
  │  ├─ typo / rename / format / 1-2 行修正? ────→ XS
  │  │
  │  ├─ 設計空間が複数開いている (実装方針が
  │  │   一意でない、先行研究調査が必要)? ──────→ L
  │  │
  │  ├─ 主観点が物理 or 数値の単一? ─────────────→ S
  │  │
  │  └─ それ以外 (default) ──────────────────────→ M
```

### S tier の Reviewer 選択

- **physical**: 次元バグ、保存則違反、対称性破れ、極限挙動の修正
- **numerical**: 安定性、収束次数、有効数字、再現性 (seed/env) の修正
- **両方該当**: M に昇格

### Tier の昇格・降格

iter 中に Manager が以下を検出したら昇格してよい (`verdict.md` に記録):

- S tier で他観点の CRITICAL が見つかった → M に昇格
- M tier で実装方針自体に疑義が生じた → L に昇格 (Planner を後付け起動)
- XS で機械的修正の範囲を超えた → S 以上に昇格

降格は原則行わない (起動済みエージェントは打ち切ってよいが、出力を破棄しない)。

---

## 3. モデル選定ポリシー

タスクの性質に応じて Manager がモデルを選び、`Agent` tool 呼び出し時に `model` パラメータで上書きする。各 agent の frontmatter には**標準モデル**を設定するが、Manager の判断で都度上書きしてよい。

| モデル | 使う場面 |
| --- | --- |
| **opus** (Claude Opus 4.7) | アーキテクチャ設計、重要な実装、難しいバグ調査、Planner |
| **sonnet** (Claude Sonnet 4.6) | 通常の実装、ドキュメント生成、コードレビュー |
| **haiku** (Claude Haiku 4.5) | 単純修正、繰り返しタスク、定型処理 |

### 標準割り当て

| エージェント | frontmatter 既定 | 想定昇格条件 | 想定降格条件 |
| --- | --- | --- | --- |
| Planner | opus | (常に opus を推奨) | — |
| Implementer | sonnet | アーキテクチャ設計を伴うサブタスク、難バグ修正 → opus | 文字列置換・コメント整形などの定型 → haiku |
| Physical Reviewer | sonnet | 新規物理モデル導入レビュー → opus | 軽微 diff のレビュー → haiku |
| Numerical Reviewer | sonnet | 新規数値スキーム導入レビュー → opus | 既存ベンチ再走らせるだけ → haiku |
| Simplicity Reviewer | sonnet | 大規模リファクタ → opus | 軽微 diff → haiku |
| Clarity Reviewer | sonnet | 論文ドラフト全章レビュー → opus | typo 修正レベル → haiku |

Manager 自身 (= 対話エージェント) のモデルはユーザのセッション設定に従う。Manager は高難度判断 (タスク分解、Tier 判定、合否判定、競合する review の調停) を行うので、原則 opus が望ましい。

### 上書きの構文 (Manager の運用)

```text
Agent(
  subagent_type="implementer",
  model="opus",          # ← 重要実装で昇格
  prompt="..."
)
```

---

## 4. ワークフロー

### Phase 0 — タスク受領 (Manager)

1. ユーザからタスクを受け取る
2. **Tier を判定する** (§2 のフロー)。判定根拠を 1 行でメモする
3. タスクを**並列可能な単位**に分解する
   - 独立サブタスクが 2 件以上あれば、複数チームを並列起動 (Tier はサブタスクごとに判定)
   - 単一サブタスクなら 1 チームのみ
4. 各サブタスクに **task-slug** を割り当て (例: `solver-rhs-fix`, `convergence-test-add`)
5. **アーティファクト保存ディレクトリ**を作成: `.dev/teams/<task-slug>/`
   - XS / S の軽量タスクは `--lightweight` で省略可
6. `spec.md` を準備
   - **L tier**: Planner を起動して `spec-draft.md` を出させ、Manager が改訂して `spec.md` を確定
   - **M / S / Eng / Docs**: Manager 自身が `spec.md` を書く (合格条件を明示)
   - **XS**: spec.md 不要。chat 内のブリーフ + Manager の理解で十分

### Phase 1 — 反復ループ (各チームごと、並列実行可)

Tier ごとに編成が異なる。共通骨格:

```text
iter = 1
while iter <= MAX_ITER(Tier):

  Step A: Implementer 実行
    Agent(subagent_type="implementer", model=<選定>, prompt=spec + iter + 過去feedback)
    出力: .dev/teams/<slug>/iter-NNN/impl-state.md + 実コード変更

  Step B: 該当 Reviewer を並列起動 (一次レビュー)
    Tier=M, L: Agent(reviewer-physical) と Agent(reviewer-numerical) を並列
    Tier=S:    Agent(reviewer-physical) または Agent(reviewer-numerical) のいずれか 1 つ
    Tier=Eng:  Agent(reviewer-simplicity)
    Tier=Docs: Agent(reviewer-clarity)
    出力: review-<role>-NNN.md

  Step C: クロスレビュー (Tier=M, L のみ、並列)
    並列:
      Agent(reviewer-physical, prompt="review-numerical-NNN.md を物理観点で検証")
      Agent(reviewer-numerical, prompt="review-physical-NNN.md を数値観点で検証")
    出力: cross-physical-on-numerical-NNN.md, cross-numerical-on-physical-NNN.md

  Step D: Manager 判定
    全 review/cross-review を読む
    競合する指摘は Manager が調停
    consolidated-feedback-NNN.md を書き、判定:
      - PASS: チーム終了
      - FAIL: Implementer に差し戻し (iter += 1)
      - ESCALATE: ユーザに相談
      - TIER-UP: Tier を昇格 (例: S → M) して再構成

  if iter >= MAX_ITER:
    ESCALATE: ユーザに相談
```

**XS tier の例外**: Phase 1 は Manager が直接編集する。完了後に diff をセルフレビュー (該当する場合 `/harness-audit` を 1 回回す) して `verdict.md` 相当を口頭で報告。

### Phase 2 — 統合 (Manager)

1. 全チームの成果を統合
2. チーム間の整合性 (API、命名、依存関係) を確認
3. 必要に応じて `/harness-audit` を走らせて規律点検
4. [.dev/CHANGELOG.md](CHANGELOG.md) に記録
5. [.dev/TODO.md](TODO.md) を更新 (該当 TODO を `[x]` + `*(YYYY-MM-DD, {hash})*`)

---

## 5. クロスレビューの定義 (Tier=M, L のみ)

「クロスレビュー」とは、**各レビュアがもう一方のレビュア report を自分の専門観点で検証する**こと。3 つの出力を期待する:

1. **補強**: もう一方の指摘の根本原因を自分の専門で説明 (例: 数値発散の物理的起源)
2. **見落とし**: もう一方が見落としている自分専門のリスク
3. **反証**: もう一方の指摘が自分の専門観点では問題ないと判断する場合の根拠

これにより Manager は単独レビュアでは捉えきれない盲点を埋める。

Tier=S, Eng, Docs では Reviewer が 1 つなのでクロスレビューは行わない。代わりに Manager が直接レビュー結果を読み consolidated-feedback を書く。

---

## 6. 並列性のルール

- Manager は**独立な Agent 呼び出しを 1 メッセージ内で並列発火**する
- Tier=M, L の Phase 1 Step B (二人のレビュア一次レビュー) は常に並列
- Tier=M, L の Phase 1 Step C (クロスレビュー) も常に並列
- 複数チームの Phase 1 全体も、依存がなければ並列起動
- 依存がある場合 (例: チーム B がチーム A の API に依存) は Manager が順序を守る

---

## 7. 出力規律 (レビュー品質保全)

レビュー品質を保つため、全エージェント (Planner / Implementer / Reviewers / Manager) は以下に従う。詳細は `output-discipline` skill。

- **数値・テスト・診断の正本はファイル**: 結果は `results/<run-id>/` 配下に保存。stdout は 1〜2 行のサマリのみ
- **テスト出力もファイル化**: `pytest --junit-xml=...`, `cargo test 2>&1 | tee results/tests/<id>.log` 等
- **コード参照は `Read` tool**: Bash の `cat` / `grep` は使わない (Read/Grep/Glob は Bash hook の影響を受けず、レビュア品質を保つ)
- **大きい diff/log は一時ファイル経由**: `git diff --no-color > /tmp/diff-<ts>.txt` してから `Read`
- **stdout 圧縮の影響を受けてよいコマンド**: `git status`, `git log --oneline`, `ls`, `tree`, ビルド成否, lint 要約

これにより、外部 token 削減ツール (rtk 等) を併用してもレビュー品質が保たれる。

---

## 8. アーティファクト管理

### 命名規約

```text
.dev/teams/<task-slug>/
  spec.md                              # Manager が最終確定した spec
  spec-draft.md                        # (L tier のみ) Planner のドラフト
  iter-001/
    impl-state.md                      # Implementer の自己報告
    review-physical.md                 # (M/L/S-phys) Physical Reviewer 一次レビュー
    review-numerical.md                # (M/L/S-num) Numerical Reviewer 一次レビュー
    review-simplicity.md               # (Eng) Simplicity Reviewer 一次レビュー
    review-clarity.md                  # (Docs) Clarity Reviewer 一次レビュー
    cross-physical-on-numerical.md     # (M/L のみ) P が N をクロス検証
    cross-numerical-on-physical.md     # (M/L のみ) N が P をクロス検証
    consolidated-feedback.md           # Manager の調停・判定
  iter-002/
    ...
  verdict.md                           # 最終判定と総括 (Tier、iter 数、昇格履歴を含む)
```

### Git 管理

- `.dev/teams/` は **commit する**。後から参照可能にする
- ただし重い中間ファイル (大きいログ、出力) は `results/` に退避し `.gitignore`

### 軽量モード (任意)

XS / S tier で 1 iter で済む見込みなら `.dev/teams/<slug>/` を作らず、chat 内応答のみで完結させてよい。Manager の判断。

---

## 9. 完了判定 (Manager)

サブタスクが PASS する条件:

1. spec の合格条件を実装が満たす
2. 起動した全 Reviewer の CRITICAL 指摘がゼロ
3. (M/L のみ) クロスレビューで新たな CRITICAL が発見されていない
4. 残った IMPORTANT/SUGGEST は `verdict.md` に明記され、後回し判断に説明がある

---

## 10. ESCALATE の運用

以下のいずれかが発生したら Manager は**ユーザに相談**する:

- MAX_ITER に達した
- レビュアの指摘が spec 自体の不備に起因する (Tier=L なら Planner 再起動を検討)
- 物理レビュアと数値レビュアの判断が真っ向対立し、Manager が調停できない
- Tier 昇格しても解決の見通しが立たない
- セキュリティ・データ消失・再現性破壊のリスクを発見

ESCALATE 時は `.dev/teams/<slug>/verdict.md` に状況を書き、ユーザに提示。

---

## 11. 起動の仕方

ユーザ視点:

```text
/team-task <ブリーフ> [--tier XS|S|M|L|Eng|Docs] [--max-iter N] [--lightweight]
```

`--tier` を省略した場合、Manager が §2 のフローで自動判定する。

詳細は [.claude/commands/team-task.md](../.claude/commands/team-task.md) を参照。
