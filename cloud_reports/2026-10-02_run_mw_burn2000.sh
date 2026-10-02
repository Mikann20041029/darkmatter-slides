#!/bin/bash
# 矮小銀河の計算が終わってから、天の川 13 ビンを「捨てる歩数 2000」で計算し直す (出力に 400・5000 の誤差も残る)。
# 種 42 は前回と同じなので、最良値と有意度は前回 (/tmp/v20t) と同じになるはず。変わるのは誤差だけ
while pgrep -f apply_v20_method_targets > /dev/null; do sleep 60; done
cd /home/user/dm-main
echo "mw start $(date -u +%T)"
HOME=/home/arsei MCMC_ALLBINS_OUTDIR=/tmp/v20t_b2000 MCMC_CELL_LIKELIHOOD=1 MCMC_DISK_BUBBLE=1 MCMC_PIXEL_DEG=0.125 \
  MCMC_SIGNFREE_HALO=1 MCMC_ULTRACLEAN=1 MCMC_TOTANI_BESTFIT=1 MCMC_TOTANI_N_BURN=2000 \
  /root/venv312/bin/python code/mcmc_fit_all_bins.py > /tmp/v20t_b2000.log 2>&1
echo "mw done $(date -u +%T) exit=$?"
