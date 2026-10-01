#!/bin/bash
LOG=/home/arsei/univ/nakamura-darkmatter/results/ultraclean_watchdog.log
while true; do
  CFREE=$(df -BG --output=avail /mnt/c 2>/dev/null | tail -1 | tr -dc '0-9')
  echo "$(date) C:空き=${CFREE}GB" >> "$LOG"
  if [ -n "$CFREE" ] && [ "$CFREE" -lt 8 ]; then
    echo "$(date) !!! C:${CFREE}GB<8 緊急停止 !!!" >> "$LOG"
    pkill -f rebuild_ultraclean_week780.py; break
  fi
  sleep 60
done
