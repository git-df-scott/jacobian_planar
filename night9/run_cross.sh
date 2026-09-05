#!/bin/sh
cd /home/user/jacobian_planar
for i in 1 2 3 4 5 6 7 8 9 10 11 12; do
  n=$(wc -l < night9/cross_prime.csv 2>/dev/null || echo 0)
  if [ "$n" -ge 109 ]; then echo "COMPLETE $n"; exit 0; fi
  python3 -u night9/cross_prime.py >> night9/cross_prime_log.txt 2>&1
done
echo "STOPPED $(wc -l < night9/cross_prime.csv)"
