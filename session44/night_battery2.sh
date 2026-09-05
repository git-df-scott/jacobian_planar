#!/bin/bash
cd "$(dirname "$0")"
ulimit -v 12000000
run() { echo "### $*"; timeout "$1" python3 b16_direct.py "${@:2}" --skipcal 2>&1 | grep -E "j=|Error" || echo "STEP-TIMEOUT-OR-EMPTY $*"; pkill -9 msolve 2>/dev/null; }
run 1800 2 --gauge 1 --satvar mu2
run 2400 3 --gauge 1
run 2400 3 --gauge 0
run 2400 3 --gauge 1 --satvar mu1
run 3000 4 --gauge 1
run 3000 4 --gauge 1 --satvar mu1
run 3600 5 --gauge 1
run 3600 6 --gauge 1
run 3600 7 --gauge 1
run 3600 7 --gauge 1 --satvar mu1
echo BATTERY2-DONE
