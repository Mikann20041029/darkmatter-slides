#!/usr/bin/env python3
"""matplotlib 用の日本語フォント共通設定モジュール。

経緯:
  - DejaVu Sans (matplotlibのデフォルト) は CJK グリフを含まず、
    日本語テキストが □ (tofu) として表示される事故が発生した (2026-06-10)。
  - Noto Sans CJK JP に切り替えても、Unicode 上付き/下付き数字
    (U+2070, U+2074-2079, U+2080-2089, U+207A/B 等) は同フォントにも
    収録されておらず、再び □ になる事故が発生した (2026-06-11)。

このモジュールは (1) Noto Sans CJK JP の登録を一箇所に集約し、
(2) 上付き/下付きの安全な書き方を docstring で示す。

使い方:
    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from jp_font import setup_jp_font
    setup_jp_font()

上付き/下付き文字の書き方 (□ 回避):
    NG: "b₀", "10⁻³"  (リテラル Unicode 上付き/下付き U+2070-209C 帯)
    OK: r"b$_0$", r"$10^{-3}$"  (matplotlib mathtext)

  ¹ ² ³ (U+00B9, U+00B2, U+00B3) や °, ×, σ, α, ≈ 等は Noto Sans CJK JP に
  含まれるため問題ない。判定に迷う場合は code/check_mojibake.py を実行する
  (Edit/Write 時に自動実行される pre-check と同じロジック)。
"""
from __future__ import annotations

import matplotlib
from matplotlib import font_manager as _fm

FONT_PATH = "/home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf"
FONT_NAME = "Noto Sans CJK JP"

_initialized = False


def setup_jp_font() -> None:
    """Noto Sans CJK JP を matplotlib に登録し、デフォルトフォントに設定する。

    複数回呼んでも安全 (2回目以降は no-op)。
    """
    global _initialized
    if _initialized:
        return
    _fm.fontManager.addfont(FONT_PATH)
    matplotlib.rcParams["font.family"] = FONT_NAME
    _initialized = True


if __name__ == "__main__":
    setup_jp_font()
    print(f"font.family = {matplotlib.rcParams['font.family']}")
