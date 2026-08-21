#!/bin/bash
# Serial ladder queue: one heavy msolve at a time (memcg cap ~13.3GiB).
# Enforces the standing rule: capture stderr; a "[-1]" accompanied by a
# parse/read error is a FAILURE, never a verdict.
Q=/home/user/jacobian_planar/wave5/ms2
LOG=/home/user/jacobian_planar/wave6/ladder_queue.log
cd $Q
# wait for any in-flight msolve to clear
while pgrep -x msolve > /dev/null; do sleep 30; done
for spec in "9 1000033" "10 1000081" "11 1000003"; do
  set -- $spec; d=$1; p=$2
  for k in 0 1; do
    f=b16seedN_d${d}_r${k}_p${p}
    [ -f "$f.ms" ] || { echo "$(date -u +%H:%M) MISSING $f.ms" >> $LOG; continue; }
    cg=$(tail -n +3 $f.ms | tr ',' '\n' | grep -cE '^[0-9-]+$')
    if [ "$cg" != "0" ]; then echo "$(date -u +%H:%M) $f REFUSED: $cg constant generators" >> $LOG; continue; fi
    echo "$(date -u +%H:%M) START $f (vars=$(head -1 $f.ms | tr ',' '\n' | wc -l))" >> $LOG
    timeout 7200 msolve -t 2 -f $f.ms -o $f.out 2> $f.err
    rc=$?
    head=$(head -c 30 $f.out 2>/dev/null)
    if grep -qi "error" $f.err 2>/dev/null; then
      echo "$(date -u +%H:%M) $f FAILURE-PARSE rc=$rc stderr=$(head -c 120 $f.err)" >> $LOG
    elif [ "$rc" = "124" ]; then
      echo "$(date -u +%H:%M) $f TIMEOUT-7200 (failure, not a verdict)" >> $LOG
    elif [ "${head:0:4}" = "[-1]" ]; then
      echo "$(date -u +%H:%M) $f EMPTY (clean stderr)" >> $LOG
    elif [ -s "$f.out" ]; then
      echo "$(date -u +%H:%M) $f *** NONEMPTY *** head=$head" >> $LOG
    else
      echo "$(date -u +%H:%M) $f NO-OUTPUT rc=$rc (failure)" >> $LOG
    fi
  done
done
echo "$(date -u +%H:%M) LADDER-QUEUE-DONE" >> $LOG
