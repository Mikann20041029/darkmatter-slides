#!/bin/bash
# 重い計算を順番に。矮小銀河は 3 本に分けて同時に (終わった天体は飛ばす = 止まっても続きから)
cd /home/user/dm-main
export HOME=/home/arsei
if [ ! -f /home/user/darkmatter-slides/cloud_reports/2026-10-02_mcmc_settings_check.json ]; then
  echo "settings start $(date -u +%T)"
  /root/venv312/bin/python /home/user/darkmatter-slides/cloud_reports/2026-10-02_mcmc_settings_check.py /home/user/darkmatter-slides/cloud_reports/2026-10-02_mcmc_settings_check.json > /tmp/mcmc_settings.log 2>&1
  echo "settings done $(date -u +%T) exit=$?"
fi
/root/venv312/bin/python - <<'PY' > /tmp/targets_groups.txt
import sys, os; sys.path.insert(0,'code'); import target_geometry as tg
done={f.replace('_spectrum.json','') for f in os.listdir('/tmp/targets_t')}
rest=[t.key for t in tg.load_targets(n_control=23, control_seed=20260731) if t.key not in done]
for g in range(3): print(','.join(rest[g::3]))
PY
echo "targets start $(date -u +%T) remaining=$(tr ',' '\n' < /tmp/targets_groups.txt | grep -c .)"
g=0
while read keys; do
  [ -z "$keys" ] && continue
  /root/venv312/bin/python code/apply_v20_method_targets.py --targets "$keys" --n-control 23 --cell-deg 1 --out /tmp/targets_t > /tmp/targets_g$g.log 2>&1 &
  g=$((g+1))
done < /tmp/targets_groups.txt
wait
echo "targets done $(date -u +%T)"
echo ALLDONE
