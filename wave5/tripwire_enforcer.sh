#!/bin/bash
# Tripwire ENFORCER v2 -- watches the BINDING constraint: the container memcg
# (dmesg 22:20Z proved kills are CONSTRAINT_MEMCG, not host swap; the OOM
# killer picks the largest RSS, i.e. the twin). SIGSTOP does not un-charge
# memcg pages, so on pressure the enforcer KILLS non-twin heavies instead.
# Exits when the twin's msolve is gone.
LOG=/home/user/jacobian_planar/wave5/tripwire.log
MC=/sys/fs/cgroup/memory/process_api/01a02089-1187-7310-8c13-8ca8a73c259d/claude-code-bash
MAX=$(cat $MC/memory.limit_in_bytes 2>/dev/null); [ -z "$MAX" ] && MAX=14327656448
echo "$(date -u +%H:%M:%S) enforcer v2 armed (memcg max=$MAX, kill non-twin heavies at headroom<1.5G)" >> "$LOG"
while true; do
  TWIN=""
  for p in $(pgrep -x msolve); do
    grep -q b16r12seed_N_p1000033 /proc/$p/cmdline 2>/dev/null && TWIN=$p && break
  done
  [ -z "$TWIN" ] && { echo "$(date -u +%H:%M:%S) twin gone -> enforcer exit" >> "$LOG"; exit 0; }
  CUR=$(cat $MC/memory.usage_in_bytes 2>/dev/null)
  if [ -z "$CUR" ] || [ "$CUR" = 0 ]; then
    echo "$(date -u +%H:%M:%S) WARN memcg read failed -- metric blind, not silently green" >> "$LOG"
    CUR=$MAX
  fi
  HEAD=$(( (MAX - CUR) / 1048576 ))
  RSS=$(awk '/VmRSS/{print $2}' /proc/$TWIN/status 2>/dev/null)
  echo "$(date -u +%H:%M:%S) memcg_headroom=${HEAD}MB twin_rss=${RSS}kB" >> "$LOG"
  if [ "$HEAD" -lt 1536 ]; then
    for p in $(pgrep -x msolve; pgrep -x Singular); do
      [ "$p" = "$TWIN" ] && continue
      R=$(awk '/VmRSS/{print $2}' /proc/$p/status 2>/dev/null); [ -z "$R" ] && continue
      if [ "$R" -gt 1048576 ]; then
        kill -KILL "$p" && echo "$(date -u +%H:%M:%S) TRIPWIRE v2: KILLED pid $p (rss ${R}kB) to protect twin" >> "$LOG"
      fi
    done
  fi
  sleep 60
done
