#!/usr/bin/env bash
# wave3 adjudication suite. Nonzero exit if any certifier fails.
set -u; cd "$(dirname "$0")/.."; F=0
for f in wave3/w3_*.py; do
  b=$(basename "$f" .py)
  out=$(timeout 3600 python3 "$f" 2>&1); rc=$?
  echo "  $([ $rc -eq 0 ] && echo ok || echo FAIL)  $b  :: $(echo "$out" | tail -1)"
  [ $rc -ne 0 ] && F=1
done
for f in wave3/w3_*.gp; do
  b=$(basename "$f" .gp)
  out=$(timeout 3600 gp -q -f "$f" 2>&1); rc=$?
  echo "  $([ $rc -eq 0 ] && echo ok || echo FAIL)  $b  :: $(echo "$out" | grep -E '^w3_' | tail -1)"
  [ $rc -ne 0 ] && F=1
done
[ $F -eq 0 ] && echo "WAVE3: ALL PASS" || echo "WAVE3: FAILURES"
exit $F
