#!/bin/bash
cd "$(dirname "$0")"
for k in 4 5 6 7 8; do
  echo "### deg(q1)=$k mu3=1 saturated (mu0!=0)"
  timeout 2400 python3 abel_msolve.py $k --skipcal 2>&1 | grep -E "deg\(q1\)|raw:"
done
echo ABEL-MSOLVE-DONE
