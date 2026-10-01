#!/usr/bin/env python3
# =============================================================
# 解析 01: FITS → CSV 変換
# 元ファイル: code/fits_to_csv.py
# 対応レベル: Lv 5〜15
# =============================================================

# ---- 新しく出てくる概念（Level 0 の人へ）----
# sys.argv : コマンドライン引数（実行時に渡す値）
# with文   : ファイルを安全に開いて、自動で閉じてくれる仕組み
# .astype(): 配列の型を変換するメソッド

import sys          # sys.argv でコマンドライン引数を受け取るため
from pathlib import Path   # ファイルパスを扱うクラス（Level 5で覚える）
import numpy as np  # 数値計算（ここではデータ型変換に使う）
from astropy.io import fits  # FITS ファイルを読む天文ライブラリ
import csv          # CSV ファイルに書き出すための標準ライブラリ


# ---- 定数: 出力する列の名前と説明 ----
# これは「辞書のリスト」ではなく「タプルのリスト」
# タプル(tuple) = () で囲んだ、変更できないリスト
COLUMN_DESCRIPTIONS = [
    ("energy_GeV",  "光子エネルギー [GeV]"),
    ("ra_deg",      "赤経 J2000 [度]"),
    ("dec_deg",     "赤緯 J2000 [度]"),
    ("l_deg",       "銀経 [度]"),
    ("b_deg",       "銀緯 [度]"),
    ("theta_deg",   "衛星視野中心からの角度 [度]"),
    ("zenith_angle_deg", "天頂角 [度]"),
    ("time_met_s",  "観測時刻 MET [秒]"),
    ("event_class", "イベントクラス"),
    ("event_type",  "イベントタイプ"),
]


def fits_to_csv(fits_path, csv_path):
    """FITS ファイルを読み込んで CSV に書き出す関数。

    引数:
        fits_path: 入力 FITS ファイルのパス（文字列）
        csv_path : 出力 CSV ファイルのパス（文字列）
    """

    print(f"読み込み: {fits_path}")

    # ---- with文の使い方 ----
    # with A as B: → A を開いて B という名前で使う。ブロックを抜けたら自動でクローズ
    # fits.open() で FITS ファイルを開く（astropy ライブラリの関数）
    with fits.open(fits_path) as hdul:
        # hdul = HDU List（Header Data Unit の集まり）
        # FITS ファイルは複数の「テーブル」から成る（Excel のシートに似ている）
        # "EVENTS" という名前のテーブルが γ線光子データ

        hdul.info()          # どんなテーブルがあるか表示（デバッグ用）
        ev = hdul["EVENTS"].data  # EVENTS テーブルのデータ部分を取り出す

        # ---- 各列のデータを取り出す ----
        # ev["列名"] で特定の列を NumPy 配列として取り出せる
        # .astype(float) = データ型を float（小数）に変換

        energy_gev = ev["ENERGY"].astype(float) / 1000.0
        # ↑ Fermi-LAT のエネルギー単位は MeV。GeV に変換するため 1000 で割る
        # 1 GeV = 1000 MeV（ギガ = 10億、メガ = 100万）

        ra    = ev["RA"].astype(float)   # 赤経（天球上の座標）
        dec   = ev["DEC"].astype(float)  # 赤緯（天球上の座標）
        l     = ev["L"].astype(float)    # 銀経（銀河系の座標）
        b     = ev["B"].astype(float)    # 銀緯（銀河系の座標）
        theta = ev["THETA"].astype(float)
        zenith = ev["ZENITH_ANGLE"].astype(float)
        time_met = ev["TIME"].astype(float)
        event_class_bits = ev["EVENT_CLASS"]
        event_type_bits  = ev["EVENT_TYPE"]

        # ビットフラグ（0と1の組み合わせ）を整数に変換する内部関数
        # def を def の中に書くこともできる（ローカル関数 / Level 15 の概念）
        def bits_to_int(arr):
            if arr.ndim == 1:          # 1次元配列の場合はそのまま変換
                return arr.astype(int)
            result = np.zeros(len(arr), dtype=np.int64)
            for bit_idx in range(arr.shape[1]):
                # << はビットシフト演算子（2^bit_idx を掛けるのと同じ）
                result += arr[:, bit_idx].astype(np.int64) << bit_idx
            return result

        ec_int = bits_to_int(event_class_bits)
        et_int = bits_to_int(event_type_bits)

    # with ブロックを抜けると、FITS ファイルは自動でクローズされる ←ここがポイント！

    n_events = len(energy_gev)
    print(f"総イベント数: {n_events:,}")  # :, = 3桁区切りで表示（1,234,567 のように）
    print(f"エネルギー範囲: {energy_gev.min():.4f} 〜 {energy_gev.max():.1f} GeV")
    # .min() = 最小値、.max() = 最大値（NumPy 配列のメソッド）

    # ---- CSV に書き出す ----
    # ヘッダーコメント行を作る（"# 列名: 説明 | ..." の形式）
    header_comment = "# " + " | ".join(f"{name}: {desc}" for name, desc in COLUMN_DESCRIPTIONS)
    # str.join(リスト) = リストの要素を指定した文字列で繋ぐ
    # " | ".join(["A", "B", "C"]) → "A | B | C"

    col_names = [name for name, _ in COLUMN_DESCRIPTIONS]
    # name, _ の _ は「使わない変数」を捨てるときの慣習

    print(f"書き出し: {csv_path}")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        # open(パス, "w") = 書き込みモードで開く（w = write）
        # newline="" = Windows での改行コード問題を防ぐ
        # encoding="utf-8" = 日本語が文字化けしないように

        f.write(header_comment + "\n")  # コメント行を書く
        writer = csv.writer(f)          # CSV 書き込みオブジェクトを作成
        writer.writerow(col_names)      # ヘッダー行（列名）を書く

        for i in range(n_events):
            writer.writerow([
                f"{energy_gev[i]:.6f}",  # 小数点6桁
                f"{ra[i]:.6f}",
                f"{dec[i]:.6f}",
                f"{l[i]:.6f}",
                f"{b[i]:.6f}",
                f"{theta[i]:.4f}",
                f"{zenith[i]:.4f}",
                f"{time_met[i]:.3f}",
                int(ec_int[i]),
                int(et_int[i]),
            ])

    print(f"完了: {n_events:,} 行を書き出しました。")


def main():
    """コマンドライン引数を受け取ってメイン処理を呼ぶ。"""

    # sys.argv = コマンドライン引数のリスト
    # python fits_to_csv.py input.fits output.csv
    # sys.argv[0] = "fits_to_csv.py"（スクリプト名自身）
    # sys.argv[1] = "input.fits"
    # sys.argv[2] = "output.csv"

    if len(sys.argv) < 2:  # 引数が足りなければ使い方を表示して終了
        print("使い方: python fits_to_csv.py <input.fits> [<output.csv>]")
        sys.exit(1)  # sys.exit(1) = エラーとして終了（0 = 正常終了）

    fits_path = sys.argv[1]

    if len(sys.argv) >= 3:
        csv_path = sys.argv[2]
    else:
        # 出力ファイル名の指定がない場合: 拡張子を .csv に変換して使う
        csv_path = str(Path(fits_path).with_suffix(".csv"))
        # Path("data.fits").with_suffix(".csv") → Path("data.csv")

    fits_to_csv(fits_path, csv_path)


if __name__ == "__main__":
    main()
