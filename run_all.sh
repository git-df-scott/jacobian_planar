#!/usr/bin/env bash
# Runs every certifier in the repository and records PASS/FAIL per file.
# Exit status is nonzero if any certifier fails.
set -u
cd "$(dirname "$0")"
mkdir -p logs
FAILED=0
echo "=============================================================="
echo " A. ARCHIVE RE-RUNS  (certifiers/rerun) - sessions 1-18, 39"
echo "=============================================================="
for f in certifiers/rerun/S*.py; do
  b=$(basename "$f" .py)
  timeout 1800 python3 "$f" > "logs/$b.log" 2>&1
  rc=$?
  n=$(grep -c "PASS" "logs/$b.log" || true)
  if [ $rc -eq 0 ]; then echo "  ok    $b   (rc=0, PASS lines: $n)";
  else echo "  FAIL  $b   (rc=$rc)"; FAILED=1; fi
done
echo
echo "=============================================================="
echo " B. NEW CERTIFIERS  (certifiers/new) - this session"
echo "=============================================================="
for f in certifiers/new/E*.py; do
  b=$(basename "$f" .py)
  timeout 3600 python3 "$f" > "logs/$b.log" 2>&1
  rc=$?
  s=$(tail -1 "logs/$b.log")
  if [ $rc -eq 0 ]; then echo "  ok    $b   $s";
  else echo "  FAIL  $b   (rc=$rc)"; FAILED=1; fi
done
for f in certifiers/new/E*.gp; do
  b=$(basename "$f" .gp)
  timeout 3600 gp -q -f "$f" > "logs/$b.log" 2>&1
  rc=$?
  s=$(grep -E "^E[0-9]+: PASS" "logs/$b.log" | tail -1)
  if [ $rc -eq 0 ]; then echo "  ok    $b   $s";
  else echo "  FAIL  $b   (rc=$rc)"; FAILED=1; fi
done
echo
if [ $FAILED -eq 0 ]; then echo "ALL CERTIFIERS PASS"; else echo "SOME CERTIFIERS FAILED"; fi
exit $FAILED
