#!/bin/bash
cd "$(dirname "$0")"
while pgrep -x python3 >/dev/null; do sleep 20; done
echo "=== retry pass done; re-labelling UNKNOWNs with the repaired engine ===" >> twoprime.log
RELABEL_BUDGET=420 python3 relabel_oom.py >> twoprime.log 2>&1
echo "=== relabel complete ===" >> twoprime.log
