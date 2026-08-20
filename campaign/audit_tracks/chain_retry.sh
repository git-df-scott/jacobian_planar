#!/bin/bash
# Wait for the 90s-budget pass to finish, then retry the TIMEOUTs at 300s.
# The driver only re-queues a TIMEOUT when the new budget exceeds the recorded
# one, so this is a strict improvement pass and never redoes terminal verdicts.
cd "$(dirname "$0")"
while pgrep -x python3 >/dev/null; do sleep 20; done
echo "=== pass 1 (90s) complete; starting retry pass at 300s ===" >> twoprime.log
python3 trackD_twoprime.py 300 60 >> twoprime.log 2>&1
echo "=== retry pass complete ===" >> twoprime.log
