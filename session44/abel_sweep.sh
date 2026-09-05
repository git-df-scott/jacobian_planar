#!/bin/bash
cd "$(dirname "$0")"
for k in 4 5 6 7; do
  for chart in 1 0; do
    echo "### deg(q1)=$k chart mu3=$chart p=32003"
    timeout 1500 python3 abel_empty.py $k --p 32003 --chart $chart --skipcal 2>&1 | grep -E "deg\(q1\)|LIVE|GB-ERROR|Terminated"
  done
done
echo ABEL-SWEEP-DONE
