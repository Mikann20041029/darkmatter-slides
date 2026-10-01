#!/usr/bin/env python3
"""
全FITSファイルを読み込み、Totaniの解析条件でフィルタリングしてCSVに結合する

フィルタ条件（Totani 2025 Section 2.1より）:
  - エネルギー  : E > 1 GeV
  - 天頂角     : zenith_angle < 100°
  - ROI 銀経   : |l| <= 60°
  - ROI 銀緯   : |b| >= 10°  （銀河面を除外）
  - ROI 銀緯   : |b| <= 60°
"""

import sys
from pathlib import Path
import numpy as np
from astropy.io import fits
import csv

FITS_DIR = Path(__file__).resolve().parent.parent / "fits"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUTPUT_CSV = DATA_DIR / "CSV" / "filtered_events.csv"

COLUMN_DESCRIPTIONS = [
    ("energy_GeV",       "光子エネルギー [GeV]"),
    ("l_deg",            "銀経 [度]  |l|<=60 でフィルタ済み"),
    ("b_deg",            "銀緯 [度]  10<=|b|<=60 でフィルタ済み（銀河面除外）"),
    ("ra_deg",           "赤経 J2000 [度]"),
    ("dec_deg",          "赤緯 J2000 [度]"),
    ("zenith_angle_deg", "天頂角 [度]  <100° でフィルタ済み"),
    ("time_met_s",       "観測時刻 MET [秒]（基準=2001-01-01）"),
]

# フィルタ条件
E_MIN_GEV   = 1.0
ZENITH_MAX  = 100.0
L_MAX       = 60.0
B_MIN       = 10.0
B_MAX       = 60.0


def process_fits(fits_path: Path, writer: csv.writer) -> int:
    with fits.open(fits_path) as hdul:
        ev = hdul["EVENTS"].data
        energy_gev = ev["ENERGY"].astype(float) / 1000.0
        l_raw      = ev["L"].astype(float)
        l          = np.where(l_raw > 180, l_raw - 360, l_raw)  # 0-360 → -180-180
        b          = ev["B"].astype(float)
        ra         = ev["RA"].astype(float)
        dec        = ev["DEC"].astype(float)
        zenith     = ev["ZENITH_ANGLE"].astype(float)
        time_met   = ev["TIME"].astype(float)

    mask = (
        (energy_gev >= E_MIN_GEV) &
        (zenith     <  ZENITH_MAX) &
        (np.abs(l)  <= L_MAX) &
        (np.abs(b)  >= B_MIN) &
        (np.abs(b)  <= B_MAX)
    )

    n_pass = mask.sum()
    for i in np.where(mask)[0]:
        writer.writerow([
            f"{energy_gev[i]:.5f}",
            f"{l[i]:.5f}",
            f"{b[i]:.5f}",
            f"{ra[i]:.5f}",
            f"{dec[i]:.5f}",
            f"{zenith[i]:.3f}",
            f"{time_met[i]:.2f}",
        ])
    return n_pass


def main():
    fits_files = sorted(FITS_DIR.glob("*.fits"))
    if not fits_files:
        sys.exit(f"FITSファイルが見つかりません: {FITS_DIR}")

    print(f"対象ファイル: {len(fits_files)} 個")
    for f in fits_files:
        print(f"  {f.name}")

    (DATA_DIR / "CSV").mkdir(exist_ok=True)
    header_comment = "# " + " | ".join(f"{n}: {d}" for n, d in COLUMN_DESCRIPTIONS)
    col_names = [n for n, _ in COLUMN_DESCRIPTIONS]

    total = 0
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        f.write(header_comment + "\n")
        writer = csv.writer(f)
        writer.writerow(col_names)

        for fits_path in fits_files:
            try:
                n = process_fits(fits_path, writer)
                total += n
                print(f"  {fits_path.name}: {n:,} イベント通過")
            except Exception as e:
                print(f"  SKIP {fits_path.name}: {e}")

    print(f"\n完了: 合計 {total:,} イベント → {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
