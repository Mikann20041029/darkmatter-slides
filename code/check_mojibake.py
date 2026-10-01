#!/usr/bin/env python3
"""文字化け (□ tofu) 防止チェッカー。

経緯:
  matplotlib で日本語フォントとして "Noto Sans CJK JP" を使う本リポジトリでは、
  以下の2種類の □ 化事故が過去に発生した:
    1. (2026-06-10) DejaVu Sans のままで日本語を描画 → 全CJK文字が □
    2. (2026-06-11) Noto Sans CJK JP に切り替えたが、Unicode 上付き/下付き
       数字 (U+2070, U+2074-2079, U+2080-2089, U+207A/B 等) は同フォントにも
       無く □ のまま

このスクリプトは、matplotlib の通常テキスト (font.family = Noto Sans CJK JP)
と mathtext (`$...$`, デフォルト mathtext.fontset = "dejavusans" → DejaVu Sans
で描画される) のそれぞれについて、実際に matplotlib の描画 API へ渡される
文字列がフォントの cmap に存在するかをチェックする。cmap に無い文字は描画時
に □ になる。

AST ベースでチェック対象を絞る理由:
  単純な「ファイル全体の文字」走査では、コメントや docstring 中の説明文
  (実際には描画されない) を誤検出する (例: 単位を示すコメント
  "# cm⁻²s⁻¹" や、本モジュール自身の jp_font.py docstring の NG 例)。
  これらは matplotlib に渡らないため □ にならない。
  → ast を使い、以下に渡される文字列リテラルのみを検査する:
    - テキスト描画 API (set_xlabel/set_title/text/annotate/legend 等。
      TEXT_METHODS を参照) の引数・キーワード引数
    - 任意の呼び出しの `label=` キーワード引数 (legend() に表示されるため)
  簡単な `x = "..."` 代入で作った変数をそのまま上記に渡すケースも
  ヒューリスティックに解決する (スコープは無視した簡易解析)。

判定ロジック (文字列の値ごと):
  - 文字列を `$` で分割し、奇数番目のセグメント(0-indexed)を mathtext 領域、
    偶数番目を通常テキスト領域とみなす (簡易パーサ。複数行 mathtext や
    エスケープされた `\\$` は非対応 — 本リポジトリのスクリプトでは未使用)。
  - 通常テキスト領域: Noto Sans CJK JP の cmap でチェック
  - mathtext 領域: DejaVu Sans の cmap でチェック (matplotlib mathtext の
    デフォルトフォント)
  - ASCII (U+0000-007F) は両方のフォントで描画可能なため常に許可

対象範囲:
  matplotlib を import しているスクリプトのみを対象にする
  (`import matplotlib` / `from matplotlib` を含むファイル)。
  write_all_notes.py 等の pptx ノート生成スクリプトは PowerPoint 側の
  フォントで描画されるため対象外 (上付き/下付き文字も問題なく表示される)。

使い方:
  python3 code/check_mojibake.py [files...]
  (引数なしの場合 code/*.py 全体をスキャン)

終了コード:
  0: 問題なし
  1: □ になる文字を検出 (修正が必要)
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

from fontTools.ttLib import TTCollection, TTFont

NOTO_PATH = "/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf"
NOTO_INDEX = 0  # "Noto Sans CJK JP" (collection内の0番目)
DEJAVU_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

ASCII_MAX = 0x7F

# matplotlib のテキスト描画 API: 文字列を描画として渡すメソッド/関数名
TEXT_METHODS = {
    "set_xlabel", "set_ylabel", "set_zlabel", "set_title", "suptitle",
    "set_xticklabels", "set_yticklabels", "set_label",
    "text", "annotate", "figtext", "xlabel", "ylabel", "title",
}

Issue = tuple[int, int, str, int, str]  # (行番号, 列番号, 文字, codepoint, 領域種別)


def _load_cmaps() -> tuple[set[int], set[int]]:
    noto = TTCollection(NOTO_PATH).fonts[NOTO_INDEX].getBestCmap()
    dejavu = TTFont(DEJAVU_PATH).getBestCmap()
    return set(noto), set(dejavu)


def _uses_matplotlib(text: str) -> bool:
    return any(
        line.startswith(("import matplotlib", "from matplotlib"))
        for line in text.splitlines()
    )


def _string_parts(node: ast.AST, consts: dict[str, str]) -> list[tuple[str, int, int]]:
    """node から文字列リテラル断片を (値, 行, 列) で列挙する。"""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [(node.value, node.lineno, node.col_offset)]
    if isinstance(node, ast.JoinedStr):  # f-string
        out: list[tuple[str, int, int]] = []
        for v in node.values:
            if isinstance(v, ast.Constant) and isinstance(v.value, str):
                out.append((v.value, v.lineno, v.col_offset))
        return out
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        out = []
        for elt in node.elts:
            out.extend(_string_parts(elt, consts))
        return out
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return _string_parts(node.left, consts) + _string_parts(node.right, consts)
    if isinstance(node, ast.Name) and node.id in consts:
        return [(consts[node.id], node.lineno, node.col_offset)]
    return []


def _check_segments(text: str, lineno: int, col: int, noto: set[int], dejavu: set[int]) -> list[Issue]:
    issues: list[Issue] = []
    for seg_idx, seg in enumerate(text.split("$")):
        in_math = seg_idx % 2 == 1
        cmap = dejavu if in_math else noto
        kind = "mathtext" if in_math else "text"
        for ch in seg:
            cp = ord(ch)
            if cp > ASCII_MAX and cp not in cmap:
                issues.append((lineno, col, ch, cp, kind))
    return issues


def scan_file(path: Path, noto: set[int], dejavu: set[int]) -> list[Issue]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    # 単純な `name = "..."` 代入を解決用に収集 (スコープ無視のヒューリスティック)
    consts: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            parts = _string_parts(node.value, {})
            if len(parts) == 1:
                consts[node.targets[0].id] = parts[0][0]

    issues: list[Issue] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Attribute):
            name = func.attr
        elif isinstance(func, ast.Name):
            name = func.id
        else:
            name = None

        targets: list[ast.AST] = []
        if name in TEXT_METHODS:
            targets.extend(node.args)
            targets.extend(kw.value for kw in node.keywords if kw.arg is not None)
        else:
            targets.extend(kw.value for kw in node.keywords if kw.arg == "label")

        for t in targets:
            for text, lineno, col in _string_parts(t, consts):
                issues.extend(_check_segments(text, lineno, col, noto, dejavu))

    return issues


def main(argv: list[str]) -> int:
    noto_cmap, dejavu_cmap = _load_cmaps()

    if len(argv) > 1:
        files = [Path(p) for p in argv[1:]]
    else:
        files = sorted(Path("code").glob("*.py"))

    n_issues = 0
    for path in files:
        if not path.exists() or path.suffix != ".py":
            continue
        if not _uses_matplotlib(path.read_text(encoding="utf-8")):
            continue
        for lineno, col, ch, cp, kind in scan_file(path, noto_cmap, dejavu_cmap):
            font = "DejaVu Sans (mathtext)" if kind == "mathtext" else "Noto Sans CJK JP"
            print(
                f"{path}:{lineno}:{col}: 文字 {ch!r} (U+{cp:04X}) は "
                f"{font} に存在せず □ として表示されます"
            )
            n_issues += 1

    if n_issues:
        print(
            f"\n{n_issues} 件の文字化けリスクを検出しました。"
            " 上付き/下付き数字は matplotlib mathtext "
            "(例: r'b$_0$', r'$10^{-3}$') に置換してください。"
            " 詳細: code/jp_font.py"
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
