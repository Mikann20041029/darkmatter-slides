#!/bin/bash
# 本体の git 管理外データ (イベント CSV・GALPROP 出力・HI4PI・GIEM など) をこの写しに入れる。
# ローカル PC で実行する。
#
# GitHub は 1 ファイル 100 MB まで。そこで
#   95 MB 未満のファイル → 本体と同じパスにそのまま置く
#   それ以上             → gzip して 95 MB ずつに分割し data_bundle/ に置く (元が .gz なら分割のみ)
# クラウド側は restore_data.sh で元のパスに戻し、SHA256 で完全一致を確認する。
#
# 使い方: ./bundle_data.sh <グループ名>   (グループごとに別コミットにして 2 GB/push 制限を避ける)
#   galprop | events_main | events_allsky | maps | misc
set -eu
MAIN=/home/arsei/univ/nakamura-darkmatter
HERE=$(cd "$(dirname "$0")" && pwd)
LIMIT=$((95 * 1024 * 1024))
MANIFEST="$HERE/data_bundle/MANIFEST.tsv"
mkdir -p "$HERE/data_bundle"
touch "$MANIFEST"

group=${1:?group required}
case "$group" in
  galprop)       files=$(cd "$MAIN" && ls ref/galprop_webrun_10050003/*) ;;
  events_main)   files=$(cd "$MAIN" && ls data/CSV/filtered_events_week780_ultraclean.csv \
                                         data/CSV/disk_bl10_week780_ultraclean.csv \
                                         data/CSV/dwarfs/* \
                                         data/fermi_exposure/*) ;;
  events_allsky) files="data/CSV/allsky_events_ultraclean.csv" ;;
  maps)          files=$(cd "$MAIN" && ls data/CSV/allsky_events.csv ref/hi4pi/* ref/gll_iem_v07.fits) ;;
  # 院試・就活は文章 (md/txt/tsv) だけ。PDF・画像・スライド・履歴書のデータは渡さない (2026-10-02 本人の指示)
  aogaku_text)   files=$(cd "$MAIN" && find aogaku -type f \( -name '*.md' -o -name '*.txt' -o -name '*.tsv' \)) ;;
  misc)          files="" ;;
  *) echo "unknown group $group"; exit 1 ;;
esac

process() {
  local rel="$1" src="$MAIN/$1"
  [ -f "$src" ] || return 0
  # 本体で git 管理済みのものは sync_from_main.sh が写すので飛ばす
  if git -C "$MAIN" ls-files --error-unmatch "$rel" >/dev/null 2>&1; then return 0; fi
  local size sha
  size=$(stat -c %s "$src")
  sha=$(sha256sum "$src" | cut -d' ' -f1)
  local key=${rel//\//__}
  if [ "$size" -lt "$LIMIT" ]; then
    mkdir -p "$HERE/$(dirname "$rel")"
    cp -p "$src" "$HERE/$rel"
    method=copy
  else
    rm -f "$HERE/data_bundle/$key".part_*
    if [[ "$rel" == *.gz ]]; then
      split -b 95M -d -a 3 "$src" "$HERE/data_bundle/$key.part_"
      method=split
    else
      gzip -6 -c "$src" | split -b 95M -d -a 3 - "$HERE/data_bundle/$key.part_"
      method=gzsplit
    fi
  fi
  # 同じパスの古い行を消してから追記
  grep -v -P "^\Q$rel\E\t" "$MANIFEST" > "$MANIFEST.tmp" || true
  mv "$MANIFEST.tmp" "$MANIFEST"
  printf '%s\t%s\t%s\t%s\t%s\n' "$rel" "$method" "$size" "$sha" "$key" >> "$MANIFEST"
  echo "$method  $(numfmt --to=iec "$size")  $rel"
}

# 1 行 1 ファイルで読む (日本語・空白を含むファイル名でも分割されないように)
while IFS= read -r f; do [ -n "$f" ] && process "$f"; done <<< "$files"
sort -o "$MANIFEST" "$MANIFEST"
echo "--- data_bundle now: $(du -sh "$HERE/data_bundle" | cut -f1)"
