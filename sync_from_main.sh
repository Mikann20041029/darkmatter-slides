#!/bin/bash
# 本体 (astro-sim-lab/nakamura-darkmatter) の git 管理下のファイルを、このリポジトリに同じ構成で写す。
# ローカル PC で実行する。クラウドセッションからは実行できない (本体が無い)。
#
# aogaku/ は文章 (md/txt/tsv) だけ写す。git 管理外の文章は bundle_data.sh aogaku_text で入れる
# 写さないもの:
#   PPT/                         古い発表スライド (計 31 MB)。作業中のスライドは slides/ に別置き
#   tools/galprop/galprop         GALPROP の実行ファイル (27.5 MB、クラウドでは使えない)
#   data/CSV, GALPROP の地図データ  そもそも git 管理外 (計 5 GB 超)
#
# 追加で写すもの:
#   ref/galprop_webrun_10050003/galdef*   教授提供の GALPROP 出力のうち設定ファイル (テキスト) だけ
set -eu
MAIN=/home/arsei/univ/nakamura-darkmatter
HERE=$(cd "$(dirname "$0")" && pwd)

cd "$MAIN"
MAIN_COMMIT=$(git rev-parse --short HEAD)
LIST=$(mktemp)
# core.quotePath=false: 日本語ファイル名を記号化させない (させると除外の判定がすり抜ける)
# 作業ツリーで削除済みのファイル (git 上はまだ管理下) は飛ばす
git -c core.quotePath=false ls-files -z \
  | grep -z -v -E '^(PPT/|tools/galprop/galprop$)' \
  | while IFS= read -r -d '' f; do
      # aogaku/ は文章 (md/txt/tsv) だけ。PDF・画像・スライド・履歴書のデータは渡さない (2026-10-02 本人の指示)
      if [[ "$f" == aogaku/* ]] && [[ ! "$f" =~ \.(md|txt|tsv)$ ]]; then continue; fi
      [ -e "$f" ] && printf '%s\0' "$f"
    done \
  > "$LIST"
for f in ref/galprop_webrun_10050003/galdef*; do
  [ -e "$f" ] && printf '%s\0' "$f" >> "$LIST"
done

# -L: .dev/SOUL_addon.md などの symlink は中身を写す
rsync -a -L --from0 --files-from="$LIST" "$MAIN/" "$HERE/"
rm -f "$LIST"

# 本体の CLAUDE.md は SOUL / AGENTS / TEAM_PROTOCOL を読み込む。そこにクラウド運用の注意を足す
if ! grep -q '@CLOUD.md' "$HERE/CLAUDE.md"; then
  printf '\n@CLOUD.md\n' >> "$HERE/CLAUDE.md"
fi
echo "$MAIN_COMMIT" > "$HERE/.main_commit"
echo "synced from nakamura-darkmatter $MAIN_COMMIT"
