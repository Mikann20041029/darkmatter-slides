#!/bin/bash
# 重い計算を 1 本ずつ順番に (同時に走らせるとメモリ不足で落ちるため)
cd /home/user/dm-main
export HOME=/home/arsei
echo "settings start $(date -u +%T)"
/root/venv312/bin/python /home/user/darkmatter-slides/cloud_reports/2026-10-02_mcmc_settings_check.py /home/user/darkmatter-slides/cloud_reports/2026-10-02_mcmc_settings_check.json > /tmp/mcmc_settings.log 2>&1
echo "settings done $(date -u +%T) exit=$?"
rest=$(/root/venv312/bin/python -c "
import sys, os; sys.path.insert(0,'code'); import target_geometry as tg
done={f.replace('_spectrum.json','') for f in os.listdir('/tmp/targets_t')}
print(','.join(t.key for t in tg.load_targets(n_control=23, control_seed=20260731) if t.key not in done))")
echo "targets start $(date -u +%T) remaining=$(echo $rest | tr ',' '\n' | wc -l)"
/root/venv312/bin/python code/apply_v20_method_targets.py --targets "$rest" --n-control 23 --cell-deg 1 --out /tmp/targets_t > /tmp/targets_t3.log 2>&1
echo "targets done $(date -u +%T) exit=$?"
echo ALLDONE
