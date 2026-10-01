---
name: forbidden-list-check
description: 応急処置・workaround・一時対応・暫定対応・hotfix を新しく入れようとしている、または新規実装に着手する場面で必ず発火する。`.dev/FORBIDDEN.md` の廃止済み実装と照合し、再導入を防ぐ
origin: ai-project-kickstart-template
tools: Read, Grep, Edit
---

# Forbidden List Check Skill

`.dev/FORBIDDEN.md` は、過去にプロジェクトへ追加して**廃止された応急処置**の記録である。再導入を防ぐためのリストとして運用する。

## When to Activate

以下のいずれかに該当するとき**必ず発火**する:

- 「応急処置」「workaround」「一時対応」「暫定対応」「hotfix」「とりあえず」と発想したとき
- 新しい機能の実装に着手するとき
- 過去にあった不具合の修正方法を検討するとき
- 「症状を消すだけ」の対処を入れたい誘惑が生じたとき

## Procedure

### Step 1: FORBIDDEN.md と照合

```bash
# 必ず実行
cat .dev/FORBIDDEN.md
```

「廃止済み実装一覧」を読み、これから入れようとしている対処が**過去に廃止されたものと同型**でないか確認する。

### Step 2: 同型なら入れない

過去に同じ対処が廃止されている場合、**再導入してはならない**。`FORBIDDEN.md` に書かれた廃止理由・代替案を読み、根本原因に基づく解決策を検討する。

### Step 3: 同型でなければ慎重に判断

別物の対処であっても、まず根本原因の調査を優先する。「症状を消すだけの対処」は技術的負債を再生産する。

### Step 4: やむなく一時対処を入れる場合

次の 2 点を必ず明記する:

- **撤去条件** (何が満たされたら撤去するか)
- **期限** (いつまでに撤去するか)

記載先: `.dev/SPEC.md` または `.dev/HANDOFF.md`。書かない場合、後でこの一時対処が永続化する。

### Step 5: 応急処置を撤去できたら FORBIDDEN.md に追記

経緯と再発防止の教訓を `.dev/FORBIDDEN.md` に追記する。形式は既存エントリに従う。

## NG パターン

- FORBIDDEN.md を**読まずに**応急処置を入れる
- 「今回は別物だから大丈夫」と FORBIDDEN.md を**スキップ**する
- 撤去条件・期限を**書かない**一時対処
- 撤去できた応急処置を FORBIDDEN.md に**記録しない**

## Output (使用後の記録)

応急処置を入れた場合、commit message または PR description に以下を含める:

```text
[forbidden-list-check] FORBIDDEN.md 照合済み (同型なし)
撤去条件: <条件>
撤去期限: <YYYY-MM-DD>
記録先: .dev/HANDOFF.md / .dev/SPEC.md
```
