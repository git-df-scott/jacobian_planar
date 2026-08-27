#!/bin/bash
cd "$(dirname "$0")"
p=10007
for i in $(seq 1 40); do
  v=$((RANDOM % p)); w=$((RANDOM % p))
  python3 generic_exact.py $p $v $w --horizon 25 2>/dev/null | grep -E "gcd_u|NONTRIVIAL"
done
echo SLICES-DONE
