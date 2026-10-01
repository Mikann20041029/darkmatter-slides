#!/usr/bin/env bash
# check_repo_size.sh — リポジトリサイズガード (.git は除外)
#
# 上限超過時に warning を stderr に出す (warn_only=1) か、exit 1 でフックを
# 失敗させる (warn_only=0)。`.githooks/pre-commit` から呼び出すことを想定。
#
# 設定: .dev/repo_guard/repo_size_limit (limit_bytes / limit_label / warn_only)
# macOS / Linux 両対応 (du -sk を使用、GNU 専用の -sb は不使用)

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
config_file="${repo_root}/.dev/repo_guard/repo_size_limit"

# デフォルト値 (config 上書き可)
limit_bytes=$((2 * 1024 * 1024 * 1024))
limit_label="2 GiB"
warn_only=1

if [[ -f "${config_file}" ]]; then
  # shellcheck disable=SC1090
  source "${config_file}"
fi

# du -sk は macOS / Linux 共通で 1024-byte block 数を返す
current_kb="$(du -sk "${repo_root}" 2>/dev/null | awk '{print $1}')"
git_kb=0
if [[ -d "${repo_root}/.git" ]]; then
  git_kb="$(du -sk "${repo_root}/.git" 2>/dev/null | awk '{print $1}')"
fi
current_bytes=$(( (current_kb - git_kb) * 1024 ))

human_size() {
  python3 - "$1" <<'PY'
import sys
n = int(sys.argv[1])
units = ["B", "KiB", "MiB", "GiB", "TiB"]
v = float(n)
for u in units:
    if v < 1024.0 or u == units[-1]:
        print(f"{v:.1f} {u}")
        break
    v /= 1024.0
PY
}

if (( current_bytes > limit_bytes )); then
  current_label="$(human_size "${current_bytes}")"
  {
    echo "[repo-size] WARNING: repository size ${current_label} exceeded limit ${limit_label}."
    echo "[repo-size] path: ${repo_root}"
    echo "[repo-size] largest top-level entries:"
    du -sh "${repo_root}"/* 2>/dev/null | sort -h | tail -n 10
  } >&2
  if [[ "${warn_only}" != "1" ]]; then
    exit 1
  fi
fi
