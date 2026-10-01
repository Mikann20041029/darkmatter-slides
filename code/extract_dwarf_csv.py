#!/usr/bin/env python3
"""
全天球CSV（allsky_events.csv）から矮小銀河周辺の光子を抽出してCSVを作る

天体リスト（Ackermann et al. 2015 PRL 115, 231301 採用天体）:
  - Draco      : 最有力。DM支配的な矮小球状銀河
  - Sculptor   : 光子数が多く統計が取りやすい
  - Ursa Minor : J-factorが高い
  - Segue 1    : 最高J-factor候補（ただし不確かさ大）
  - Coma Ber.  : Fermi公式解析で使われた天体

抽出方法:
  各天体の中心座標（RA, Dec）から角距離 r_deg 以内の光子を全天球CSVから切り出す
  → 各天体ごとに data/CSV/dwarf_<name>.csv を作成

なぜこれらの天体か:
  矮小銀河はDMが支配的（M/L比が非常に大きい）で、ガス・星が少ない
  → DMシグナル以外のγ線放射源が少なく、クリーンなDM探索に最適
  → Fermiバブル・ループIなど天の川固有の成分が不要
  → Ackermann et al. (2015)で上限値が設定された標準的なターゲット天体
"""

from pathlib import Path
import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CSV_IN   = DATA_DIR / "CSV" / "allsky_events.csv"
OUT_DIR  = DATA_DIR / "CSV" / "dwarfs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# 天体リスト: (名前, RA[deg], Dec[deg], 抽出半径[deg], 説明)
TARGETS = [
    ("draco",       260.052,  57.915, 5.0,
     "Draco dwarf spheroidal. DM-dominated, high J-factor. "
     "One of the best DM targets. Used in Ackermann+2015."),
    ("sculptor",     15.039, -33.709, 5.0,
     "Sculptor dwarf spheroidal. Large angular size, good photon statistics. "
     "Used in Ackermann+2015."),
    ("ursa_minor",  227.285,  67.222, 5.0,
     "Ursa Minor dwarf spheroidal. High J-factor, well-studied. "
     "Used in Ackermann+2015."),
    ("segue1",      151.767,  16.082, 5.0,
     "Segue 1 ultra-faint dwarf. Highest J-factor candidate among known dwarfs. "
     "Large uncertainty but best sensitivity target. Used in Ackermann+2015."),
    ("coma_ber",    186.746,  23.904, 5.0,
     "Coma Berenices ultra-faint dwarf. Used in Ackermann+2015 DM search."),
]


def angular_distance(ra1, dec1, ra2_arr, dec2_arr):
    """2点間の角距離[deg]を返す（小角度近似なし）"""
    ra1r  = np.radians(ra1);  dec1r = np.radians(dec1)
    ra2r  = np.radians(ra2_arr); dec2r = np.radians(dec2_arr)
    cos_d = (np.sin(dec1r)*np.sin(dec2r) +
             np.cos(dec1r)*np.cos(dec2r)*np.cos(ra1r - ra2r))
    return np.degrees(np.arccos(np.clip(cos_d, -1, 1)))


def main():
    print(f"全天球CSV読み込み中: {CSV_IN}")
    df = pd.read_csv(CSV_IN, comment="#")
    print(f"  総イベント数: {len(df):,}")

    for name, ra, dec, radius, description in TARGETS:
        print(f"\n>>> {name} (RA={ra}, Dec={dec}, r<{radius}deg)")
        print(f"    {description[:80]}")

        dist = angular_distance(ra, dec, df["ra_deg"].values, df["dec_deg"].values)
        mask = dist < radius
        df_out = df[mask].copy()
        df_out["ang_dist_deg"] = dist[mask]

        out = OUT_DIR / f"dwarf_{name}_780w.csv"
        df_out.to_csv(out, index=False)
        print(f"    → {len(df_out):,}イベント → {out.name}")

    print("\n完了")


if __name__ == "__main__":
    main()
