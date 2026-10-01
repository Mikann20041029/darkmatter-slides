#!/bin/bash
# 負のl（l=-60〜0°）のデータをFITSから抽出してCSVに追記する
# 1ファイルずつDL→処理→即削除するのでディスクを圧迫しない
#
# 実行方法: bash code/append_negative_l.sh

BASE_URL="https://heasarc.gsfc.nasa.gov/FTP/fermi/data/lat/weekly/photon"
OUTPUT_CSV="data/CSV/filtered_events_negative_l.csv"
LOG="code/append_negative_l.log"

echo "開始: $(date)" | tee "$LOG"

# ヘッダー書き込み
echo "energy_GeV,l_deg,b_deg,ra_deg,dec_deg,zenith_angle_deg,time_met_s" > "$OUTPUT_CSV"

SUCCESS=0; FAIL=0

for w in $(seq 9 549); do
    # w187はスキップ（破損ファイル）
    [ "$w" -eq 187 ] && continue

    fname="lat_photon_weekly_w$(printf '%03d' $w)_p305_v001.fits"
    fpath="fits/$fname"

    echo -n "  w$(printf '%03d' $w): DL中..." | tee -a "$LOG"

    wget -q --tries=3 --timeout=60 -O "$fpath" "$BASE_URL/$fname"
    if [ $? -ne 0 ] || [ ! -s "$fpath" ]; then
        echo "FAIL" | tee -a "$LOG"
        rm -f "$fpath"; FAIL=$((FAIL+1)); continue
    fi

    # Pythonで負のl側だけ抽出してCSVに追記
    python3 - "$fpath" "$OUTPUT_CSV" <<'EOF'
import sys, numpy as np
from astropy.io import fits
import csv

fpath, out_csv = sys.argv[1], sys.argv[2]
try:
    with fits.open(fpath) as hdul:
        ev     = hdul["EVENTS"].data
        energy = ev["ENERGY"].astype(float) / 1000.0
        l_raw  = ev["L"].astype(float)
        l      = np.where(l_raw > 180, l_raw - 360, l_raw)
        b      = ev["B"].astype(float)
        ra     = ev["RA"].astype(float)
        dec    = ev["DEC"].astype(float)
        zenith = ev["ZENITH_ANGLE"].astype(float)
        t      = ev["TIME"].astype(float)

    mask = (
        (energy >= 1.0) &
        (zenith < 100.0) &
        (l >= -60.0) & (l < 0.0) &   # 負のlのみ
        (np.abs(b) >= 10.0) &
        (np.abs(b) <= 60.0)
    )

    n = mask.sum()
    with open(out_csv, "a", newline="") as f:
        w = csv.writer(f)
        for i in np.where(mask)[0]:
            w.writerow([f"{energy[i]:.5f}", f"{l[i]:.5f}", f"{b[i]:.5f}",
                        f"{ra[i]:.5f}", f"{dec[i]:.5f}", f"{zenith[i]:.3f}",
                        f"{t[i]:.2f}"])
    print(n)
except Exception as e:
    print(f"0 ({e})")
EOF

    rm -f "$fpath"
    SUCCESS=$((SUCCESS+1))
    echo "OK ($SUCCESS/539)" | tee -a "$LOG"
done

echo "" | tee -a "$LOG"
echo "完了: $(date)  成功=$SUCCESS 失敗=$FAIL" | tee -a "$LOG"
echo "出力: $OUTPUT_CSV"
wc -l "$OUTPUT_CSV"
EOF
chmod +x code/append_negative_l.sh