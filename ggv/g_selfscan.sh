#!/bin/sh
# Run the campaign's can't-fail scanner and require ZERO findings in ggv/.
# (The scanner reports the whole tree; pre-existing findings in other waves are
# outside this campaign's remit.  Findings under ggv/ are a hard stop.)
set -u
REPO=$(cd "$(dirname "$0")/.." && pwd)
OUT=$(python3 "$REPO/wave5/tools_cantfail.py" 2>&1)
echo "$OUT" | grep -E '^\s+ggv/' && { echo "CANTFAIL: rigged check(s) under ggv/ -- REFUSING"; exit 1; }
echo "$OUT" | grep -E 'scanner self-test'
echo "CANTFAIL: 0 findings under ggv/"
exit 0
