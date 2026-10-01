#!/bin/bash
# PostToolUse hook for Bash: after a successful `git commit`, warn if
# .dev/TODO.md and/or .dev/CHANGELOG.md were not included in the commit.
#
# Externalizes the "コミット後の必須作業" discipline from AGENTS.md so the
# rule is enforced by the harness rather than relying on memory.
#
# Triggers only when the Bash command line contains "git commit" and the
# HEAD commit object exists. Emits a reminder to stderr and exits 2 so
# Claude Code surfaces the message back to the assistant as feedback.
#
# Template-meta carve-out: if the commit touches `.template/CHANGELOG.md`,
# it is treated as a change to the template harness itself (not a user
# project commit) and the `.dev/*` checks are skipped. Users who adopt the
# template delete `.template/` per AGENTS.md §5, so this branch is inert
# in adopter repos.

set -u

INPUT=$(cat)

# Extract the command string from the PostToolUse JSON payload. We avoid
# requiring jq by using a small python fallback chain.
extract_command() {
  if command -v jq >/dev/null 2>&1; then
    printf '%s' "$INPUT" | jq -r '.tool_input.command // ""'
  else
    printf '%s' "$INPUT" | python3 -c 'import json,sys; d=json.load(sys.stdin); print((d.get("tool_input") or {}).get("command",""))' 2>/dev/null || printf ''
  fi
}

CMD=$(extract_command)

# Bail out unless this was a git commit invocation at command position.
# We accept the command if a `git commit` token appears at the start, or
# right after a shell separator (;, &&, ||, |, newline). This avoids
# false positives when "git commit" appears inside a string literal
# (e.g. `echo "run git commit"` or test fixtures).
if ! printf '%s' "$CMD" | grep -Eq '(^|[;\|&]|&&|\|\||\n)[[:space:]]*git[[:space:]]+commit\b'; then
  exit 0
fi

# Resolve the project root via $CLAUDE_PROJECT_DIR if set, else fall back
# to the current working directory.
ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
cd "$ROOT" 2>/dev/null || exit 0

# Skip if HEAD is not a commit (e.g. commit failed, empty repo).
git rev-parse --verify HEAD >/dev/null 2>&1 || exit 0

FILES=$(git diff-tree --no-commit-id --name-only -r HEAD 2>/dev/null)

# Template-meta carve-out: commits that update `.template/CHANGELOG.md` are
# changes to the template harness itself. Skip the `.dev/*` discipline check
# (the template repo uses `.template/CHANGELOG.md` as its own changelog).
if echo "$FILES" | grep -qx ".template/CHANGELOG.md"; then
  exit 0
fi

missing=()
echo "$FILES" | grep -qx ".dev/TODO.md" || missing+=(".dev/TODO.md")
echo "$FILES" | grep -qx ".dev/CHANGELOG.md" || missing+=(".dev/CHANGELOG.md")

# Silently exit if both files were updated in this commit.
if [ ${#missing[@]} -eq 0 ]; then
  exit 0
fi

SHORT=$(git rev-parse --short HEAD)

{
  echo "[post-commit reminder] 直前のコミット (${SHORT}) で以下が更新されていません:"
  for f in "${missing[@]}"; do
    echo "  - ${f}"
  done
  echo
  echo "AGENTS.md §2「コミット後の必須作業」に従い、フォローアップコミットで反映してください。"
} >&2

exit 2
