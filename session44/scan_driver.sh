#!/bin/bash
# Full F_p^3 scans at p=29 and p=31, horizon 27, 4-way parallel over u-slices.
cd "$(dirname "$0")"
for p in 29 31; do
  seq 0 $((p-1)) | xargs -P4 -I{} sh -c \
    "python3 uvw_hunt.py scan $p {} \$(({}+1)) --horizon 27 > scanlogs/p${p}_u{}.log 2>&1"
done
grep -l SURVIVOR scanlogs/*.log > scanlogs/SURVIVOR_FILES.txt || true
echo DONE > scanlogs/STATUS.txt
