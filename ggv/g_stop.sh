#!/bin/bash
# Stop the campaign cleanly.
#
# ORDER MATTERS.  Killing the engines first leaves the driver alive, and the
# driver immediately launches the NEXT engine -- which then survives the stop
# and keeps burning a core.  That happened once in this campaign: a Singular
# process on chartA_d6_sat outlived the stop by 22 minutes at 1 GiB because the
# engines were killed before the drivers.  Drivers die first here.
#
# Never `pgrep -f` a pattern that this script's own command line contains: the
# pattern matches this shell and the kill takes out the caller.  That trap has
# now fired five times across the campaign, once in this session.  Match binary
# names with `pgrep -x`, and drivers by their exact script path.
cd "$(dirname "$0")/.." || exit 1

for pid in $(ps -eo pid,args | awk '/[g]gv\/(g23_eliminants|g1_ladder|g4_recursion|g5_reproduce)\.py|[g]gv\/g_queue\.sh/ {print $1}'); do
    kill "$pid" 2>/dev/null
done
sleep 2

for sig in TERM KILL; do
    for pid in $(pgrep -x msolve) $(pgrep -x Singular); do
        kill "-$sig" "$pid" 2>/dev/null
    done
    sleep 2
done

# Verify, do not assume.  Report non-zero if anything survived.
left=""
for pid in $(pgrep -x msolve) $(pgrep -x Singular); do left="$left $pid"; done
for pid in $(ps -eo pid,args | awk '/[g]gv\/(g23_eliminants|g1_ladder)\.py|[g]gv\/g_queue\.sh/ {print $1}'); do left="$left $pid"; done
if [ -n "$left" ]; then
    echo "STOP INCOMPLETE -- still running:$left"
    ps -o pid,etime,rss,args -p ${left// /,} 2>/dev/null
    exit 1
fi
echo "STOP COMPLETE: no msolve, no Singular, no campaign driver running"
exit 0
