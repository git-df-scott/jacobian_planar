#!/bin/bash
# Watcher for the two pentagon Groebner runs.
#
# Designed against the failure recorded in CATCHES.md ("WATCHER WAS A FALSE-ALARM
# MACHINE"): that one used a loose regex and fired on the apostrophe in "'contra': 0".
# Rules here:
#   * a VERDICT is only ever read from a NON-EMPTY output file;
#   * an empty file with a dead process is a TIMEOUT/CRASH, never a verdict
#     (msolve exits 0 even on a parse error, so exit codes are ignored);
#   * the verdict string is matched EXACTLY against msolve's documented outputs:
#         "[-1]:"        -> EMPTY (no solution in the algebraic closure)
#         "[1, n, -1,[]]"-> POSITIVE-DIMENSIONAL
#         "[0, ..."      -> ZERO-DIMENSIONAL, solutions exist  <-- the hit case
#   * anything else is reported verbatim as UNRECOGNISED, not interpreted.
D=/home/user/jacobian_planar/wave6/pentseed
declare -A ST
classify () {   # $1 = output file
  local f=$1
  if [ ! -s "$f" ]; then echo "NO-VERDICT(empty file)"; return; fi
  local h; h=$(head -c 12 "$f")
  case "$h" in
    '[-1]:'*)  echo "EMPTY" ;;
    '[1,'*)    echo "POSITIVE-DIMENSIONAL" ;;
    '[0,'*)    echo "ZERO-DIM-SOLUTIONS-EXIST  *** HIT ***" ;;
    *)         echo "UNRECOGNISED: $(head -c 60 "$f")" ;;
  esac
}
while true; do
  for job in "1:24828:$D/seed0_p1000003.out:267eq/148unk" \
             "2:$(pgrep -f 'seed0_p1000003_lin[.]ms'|tail -1):$D/seed0_lin.out:241eq/123unk"; do
    IFS=: read -r n pid out tag <<< "$job"
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
      cur="RUNNING $(ps -o rss= -p $pid | awk '{printf "%.2fGB",$1/1048576}') $(ps -o etime= -p $pid|tr -d ' ')"
    else
      cur="ENDED -> $(classify "$out")"
    fi
    key="j$n"
    if [ "${ST[$key]}" != "${cur%% *}" ]; then
      echo "$(date +%T) job$n($tag): $cur"
      ST[$key]="${cur%% *}"
      case "$cur" in *ENDED*) echo "$(date +%T) job$n FINAL: $(classify "$out")" ;; esac
    fi
  done
  if ! kill -0 24828 2>/dev/null && ! pgrep -f 'seed0_p1000003_lin[.]ms' >/dev/null; then
    echo "$(date +%T) both jobs ended; watcher exiting"; break
  fi
  sleep 30
done
