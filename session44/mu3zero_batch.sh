#!/bin/bash
# mu3=0 stratum ladder: the gauge-uncovered branch of the B=16 F-system.
cd "$(dirname "$0")"
echo "=== j=2 mu0 gauge 0 (with calibration) ==="
nice -n 8 python3 f_system.py 2 --satvar mu0 --gauge 0 --timeout 3000
echo "=== j=2 mu1 gauge 0 ==="
nice -n 8 python3 f_system.py 2 --satvar mu1 --gauge 0 --timeout 3000 --skipcal
echo "=== j=3 mu0 gauge 0 ==="
nice -n 8 python3 f_system.py 3 --satvar mu0 --gauge 0 --timeout 4000 --skipcal
echo "=== j=3 mu1 gauge 0 ==="
nice -n 8 python3 f_system.py 3 --satvar mu1 --gauge 0 --timeout 4000 --skipcal
echo "=== j=7 mu1 gauge 0 mod 65521 (the crack companion, direct shot) ==="
nice -n 8 timeout 14400 msolve -g 2 -f lead4/j7mu1_mu3zero_p65521.ms -o lead4/j7mu1_mu3zero_p65521.gb
echo "msolve exit: $?"
ls -la lead4/j7mu1_mu3zero_p65521.gb && head -c 200 lead4/j7mu1_mu3zero_p65521.gb
echo; echo "=== BATCH DONE ==="
