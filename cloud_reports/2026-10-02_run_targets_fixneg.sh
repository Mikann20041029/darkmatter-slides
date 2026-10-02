#!/bin/bash
# 予測光子数が負になる組を除外する修正 (2026-10-02 本人了承) 後に、79 天体すべてを計算し直す。
# 出力 /tmp/targets_t2 (修正前の /tmp/targets_t は比較用に残す)。終わった天体は飛ばすので、止まっても続きから
cd /home/user/dm-main
export HOME=/home/arsei
mkdir -p /tmp/targets_t2
/root/venv312/bin/python - <<'PY' > /tmp/targets_groups2.txt
import sys, os; sys.path.insert(0,'code'); import target_geometry as tg
done={f.replace('_spectrum.json','') for f in os.listdir('/tmp/targets_t2')}
rest=[t.key for t in tg.load_targets(n_control=23, control_seed=20260731) if t.key not in done]
for g in range(3): print(','.join(rest[g::3]))
PY
echo "targets2 start $(date -u +%T) remaining=$(tr ',' '\n' < /tmp/targets_groups2.txt | grep -c .)"
g=0
while read keys; do
  [ -z "$keys" ] && continue
  /root/venv312/bin/python code/apply_v20_method_targets.py --targets "$keys" --n-control 23 --cell-deg 1 --out /tmp/targets_t2 > /tmp/targets2_g$g.log 2>&1 &
  g=$((g+1))
done < /tmp/targets_groups2.txt
wait
echo "targets2 done $(date -u +%T) n=$(ls /tmp/targets_t2 | wc -l)"
