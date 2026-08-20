#!/bin/bash
# Tripwire ENFORCER (was policy-only -- the original chart-N run died with no one acting).
# Every 60s: if swap-free < 8 GiB, SIGSTOP every msolve that is NOT the twin
# (b16r12seed_N_p1000033) and log. If margin recovers above 12 GiB, SIGCONT them.
# Exits on its own when the twin's msolve is gone (verdict or death).
LOG=/home/user/jacobian_planar/wave5/tripwire.log
echo "$(date -u +%H:%M:%S) enforcer armed (stop<8G, resume>12G)" >> "$LOG"
while true; do
  TWIN=""
  for p in $(pgrep -x msolve); do
    grep -q b16r12seed_N_p1000033 /proc/$p/cmdline 2>/dev/null && TWIN=$p && break
  done
  [ -z "$TWIN" ] && { echo "$(date -u +%H:%M:%S) twin gone -> enforcer exit" >> "$LOG"; exit 0; }
  FREE_KB=$(awk '/SwapFree/{print $2}' /proc/meminfo)
  RSS=$(awk '/VmRSS/{print $2}' /proc/$TWIN/status 2>/dev/null)
  echo "$(date -u +%H:%M:%S) swapfree=${FREE_KB}kB twin_rss=${RSS}kB" >> "$LOG"
  OTHERS=$(pgrep -x msolve | grep -v "^$TWIN$")
  if [ "$FREE_KB" -lt 8388608 ]; then
    for p in $OTHERS; do
      S=$(ps -o stat= -p "$p")
      case "$S" in T*) ;; *) kill -STOP "$p" && echo "$(date -u +%H:%M:%S) TRIPWIRE: SIGSTOP msolve $p" >> "$LOG";; esac
    done
  elif [ "$FREE_KB" -gt 12582912 ]; then
    for p in $OTHERS; do
      S=$(ps -o stat= -p "$p")
      case "$S" in T*) kill -CONT "$p" && echo "$(date -u +%H:%M:%S) recovered: SIGCONT msolve $p" >> "$LOG";; esac
    done
  fi
  sleep 60
done
