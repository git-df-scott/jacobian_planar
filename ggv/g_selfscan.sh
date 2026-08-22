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

# A 0-byte artifact under ggv/ is a FAILED RUN, never a verdict.  Committing one
# lets a reader mistake an empty file for an empty variety, so refuse outright.
ZERO=$(cd "$REPO" && find ggv -type f -size 0 -not -path "ggv/__pycache__/*" | sort)
if [ -n "$ZERO" ]; then
  echo "ZERO-BYTE ARTIFACT(S) under ggv/ -- a failed run is not a verdict, REFUSING:"
  echo "$ZERO"
  exit 1
fi
echo "ZEROBYTE: 0 zero-byte artifacts under ggv/"
exit 0
