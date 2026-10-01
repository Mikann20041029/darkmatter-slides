#!/bin/bash
# W1 対照実験: 除外矩形の中心経度を振って Bin6 の有意度を測る。
# 目的: 19.11σ→4.96σ の低下が「バブル固有」か「NFW が明るい領域を削っただけ」かの切り分け。
set -u
cd /home/arsei/univ/nakamura-darkmatter

export MCMC_ULTRACLEAN=1
export MCMC_PIXEL_DEG=0.125
export MCMC_DISK_BUBBLE=1
export MCMC_CELL_LIKELIHOOD=1
export MCMC_SIGNFREE_HALO=1
export MCMC_SKIP_MCMC=1
export MCMC_BINS=6

PY=/home/arsei/darkmatter_venv/bin/python
OUT=/home/arsei/ctrl_sweep.txt
: > "$OUT"

# 除外なし (v20 相当、既知 19.11σ)
echo "### no_exclusion" >> "$OUT"
MCMC_ALLBINS_OUTDIR=/home/arsei/ctrl_none \
  "$PY" -u code/mcmc_fit_all_bins.py 2>&1 | grep -E '有意度' >> "$OUT"

for L0 in 0 20 -20 30 -30 38 -38; do
  echo "### l0=${L0}" >> "$OUT"
  MCMC_EXCLUDE_BUBBLE=1 \
  MCMC_EXCLUDE_RECT_L0="$L0" \
  MCMC_ALLBINS_OUTDIR="/home/arsei/ctrl_l0_${L0}" \
    "$PY" -u code/mcmc_fit_all_bins.py 2>&1 | grep -E '除外矩形|有意度' >> "$OUT"
done

echo "### done" >> "$OUT"
cat "$OUT"
