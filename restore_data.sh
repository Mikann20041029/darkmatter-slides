#!/bin/bash
# data_bundle/ の分割ファイルを元のパスに戻し、MANIFEST の SHA256 と完全一致することを確認する。
# クラウドセッションで最初に 1 回実行する (cloud_setup.sh から呼ばれる)。
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
cd "$HERE"
MANIFEST=data_bundle/MANIFEST.tsv
[ -f "$MANIFEST" ] || { echo "no $MANIFEST"; exit 1; }

ok=0; bad=0
while IFS=$'\t' read -r rel method size sha key; do
  [ -n "$rel" ] || continue
  if [ "$method" != copy ]; then
    if [ -f "$rel" ] && [ "$(stat -c %s "$rel")" = "$size" ]; then
      :   # 既に復元済み
    else
      mkdir -p "$(dirname "$rel")"
      if [ "$method" = split ]; then
        cat "data_bundle/$key".part_* > "$rel"
      else
        cat "data_bundle/$key".part_* | gzip -dc > "$rel"
      fi
    fi
  fi
  got=$(sha256sum "$rel" | cut -d' ' -f1)
  if [ "$got" = "$sha" ]; then ok=$((ok+1)); else bad=$((bad+1)); echo "MISMATCH $rel"; fi
done < "$MANIFEST"
echo "restore: $ok OK, $bad mismatch"
[ "$bad" -eq 0 ]
