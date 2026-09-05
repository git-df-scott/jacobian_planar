#!/bin/bash
# Lead 1 night battery — direct (transcription-free) B=16 ladder.
cd "$(dirname "$0")"
ulimit -v 12000000   # 12 GB guard: die cleanly instead of taking the box
run() { echo "### $*"; timeout "$1" python3 b16_direct.py "${@:2}" --skipcal 2>&1 | grep -E "j=|Traceback|MemoryError" ; }
run 900  1 --gauge 0
run 1800 2 --gauge 1
run 1800 2 --gauge 0
run 1800 2 --gauge 1 --satvar mu1
run 1800 2 --gauge 1 --satvar mu2
run 2400 3 --gauge 1
run 2400 3 --gauge 0
run 2400 3 --gauge 1 --satvar mu1
run 3000 4 --gauge 1
run 3000 4 --gauge 1 --satvar mu1
run 3600 5 --gauge 1
run 3600 6 --gauge 1
run 3600 7 --gauge 1
run 3600 7 --gauge 1 --satvar mu1   # THE crack test, transcription-free
echo BATTERY1-DONE
