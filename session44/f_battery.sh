#!/bin/bash
cd "$(dirname "$0")"
run() { echo "### F $*"; timeout "$1" python3 f_system.py "${@:2}" --skipcal 2>&1 | grep -E "F-system|FAIL" || echo "F-STEP-TIMEOUT $*"; pkill -9 msolve 2>/dev/null; }
run 1800 4 --satvar mu0
run 1800 5 --satvar mu0
run 2400 6 --satvar mu0
run 2400 7 --satvar mu0
run 1800 2 --satvar mu1
run 1800 3 --satvar mu1
run 1800 4 --satvar mu1
run 2400 5 --satvar mu1
run 2400 6 --satvar mu1
run 3000 7 --satvar mu1
run 1800 7 --satvar mu2
run 3000 8 --satvar mu0
run 3000 9 --satvar mu0
echo F-BATTERY-DONE
