#!/bin/bash
cd "$(dirname "$0")"
echo "### GAUGE CHECK deg5 free-mu3 saturated"
timeout 2400 python3 abel_msolve.py 5 --free --skipcal 2>&1 | grep -E "deg\(q1\)|raw:"
for k in 9 10 11 12; do
  echo "### deg(q1)=$k mu3=1 saturated (mu0!=0)"
  timeout 3000 python3 abel_msolve.py $k --skipcal 2>&1 | grep -E "deg\(q1\)|raw:"
done
echo ABEL-EXT-DONE
