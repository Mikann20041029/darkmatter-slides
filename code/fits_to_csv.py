#!/usr/bin/env python3
"""
Fermi-LAT FITS（光子イベント）を CSV に変換するスクリプト

使い方:
    python fits_to_csv.py <input.fits> [<output.csv>]

出力列（1列目に説明を追記）:
    energy_GeV        : 光子エネルギー [GeV]
    ra_deg            : 赤経 (J2000) [度]
    dec_deg           : 赤緯 (J2000) [度]
    l_deg             : 銀経 [度]  ← 銀河解析の主軸
    b_deg             : 銀緯 [度]  ← 銀河面からの角度
    theta_deg         : 衛星視野中心からの角度 [度]（イベント品質の指標）
    zenith_angle_deg  : 天頂角 [度]（地球再入射光子の除外に使用）
    time_met_s        : 観測時刻 MET [秒]（Fermi Mission Elapsed Time、基準=2001-01-01）
    event_class       : イベントクラス（ビットフラグ）
    event_type        : イベントタイプ（ビットフラグ）
"""

import sys
from pathlib import Path
import numpy as np
from astropy.io import fits
import csv

COLUMN_DESCRIPTIONS = [
    ("energy_GeV",       "光子エネルギー [GeV]"),
    ("ra_deg",           "赤経 J2000 [度]"),
    ("dec_deg",          "赤緯 J2000 [度]"),
    ("l_deg",            "銀経 [度]"),
    ("b_deg",            "銀緯 [度]"),
    ("theta_deg",        "衛星視野中心からの角度 [度]"),
    ("zenith_angle_deg", "天頂角 [度]"),
    ("time_met_s",       "観測時刻 MET [秒]"),
    ("event_class",      "イベントクラス（ビットフラグ）"),
    ("event_type",       "イベントタイプ（ビットフラグ）"),
]


def fits_to_csv(fits_path: str, csv_path: str) -> None:
    print(f"読み込み: {fits_path}")
    with fits.open(fits_path) as hdul:
        hdul.info()
        ev = hdul["EVENTS"].data

        energy_gev       = ev["ENERGY"].astype(float) / 1000.0  # MeV → GeV
        ra               = ev["RA"].astype(float)
        dec              = ev["DEC"].astype(float)
        l                = ev["L"].astype(float)
        b                = ev["B"].astype(float)
        theta            = ev["THETA"].astype(float)
        zenith           = ev["ZENITH_ANGLE"].astype(float)
        time_met         = ev["TIME"].astype(float)
        event_class_bits = ev["EVENT_CLASS"]
        event_type_bits  = ev["EVENT_TYPE"]

        # ビットフラグを整数に変換
        def bits_to_int(arr):
            if arr.ndim == 1:
                return arr.astype(int)
            # 32ビット配列の場合
            result = np.zeros(len(arr), dtype=np.int64)
            for bit_idx in range(arr.shape[1]):
                result += arr[:, bit_idx].astype(np.int64) << bit_idx
            return result

        ec_int = bits_to_int(event_class_bits)
        et_int = bits_to_int(event_type_bits)

    n_events = len(energy_gev)
    print(f"総イベント数: {n_events:,}")
    print(f"エネルギー範囲: {energy_gev.min():.4f} ～ {energy_gev.max():.1f} GeV")

    # ヘッダー行にカラム説明を付ける（"# 列名: 説明" 形式で先頭に）
    header_comment = "# " + " | ".join(f"{name}: {desc}" for name, desc in COLUMN_DESCRIPTIONS)
    col_names = [name for name, _ in COLUMN_DESCRIPTIONS]

    print(f"書き出し: {csv_path}")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        f.write(header_comment + "\n")
        writer = csv.writer(f)
        writer.writerow(col_names)
        for i in range(n_events):
            writer.writerow([
                f"{energy_gev[i]:.6f}",
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

    print(f"完了: {n_events:,} 行を {csv_path} に出力しました。")


def main():
    if len(sys.argv) < 2:
        print("使い方: python fits_to_csv.py <input.fits> [<output.csv>]")
        sys.exit(1)

    fits_path = sys.argv[1]
    if len(sys.argv) >= 3:
        csv_path = sys.argv[2]
    else:
        csv_path = str(Path(fits_path).with_suffix(".csv"))

    fits_to_csv(fits_path, csv_path)


if __name__ == "__main__":
    main()
