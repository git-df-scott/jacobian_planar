#!/bin/bash
# Step 1 of the zero-omission directive: run the exact-Q fallback charts to
# completion, in order, one at a time.
#
# Chart A (d_3_3 = 1) is already in flight from an earlier launch; this waits
# for it, then runs B (d_3_3 = 0) and C (d_9_15 = 0). A and B alone cover the
# variety — the complement of "d_3_3 != 0" is exactly "d_3_3 = 0", so no fork
# is dropped. C is a sub-case of them, run because the directive asks for it:
# a redundant CLOSED there is a free consistency check, a SURVIVOR there would
# flag a bug in A or B.
cd /home/user/jacobian_planar || exit 1

while pgrep -f "trackB_exactQ_fallback.py A_d33_1" > /dev/null; do sleep 60; done
echo "$(date +%H:%M:%S) QF chain: chart A finished, starting B" >> trackB_QF_chain.log

python3 trackB_exactQ_fallback.py B_d33_0  >> trackB_QF_chain.log 2>&1
echo "$(date +%H:%M:%S) QF chain: B exit=$?" >> trackB_QF_chain.log

python3 trackB_exactQ_fallback.py C_d915_0 >> trackB_QF_chain.log 2>&1
echo "$(date +%H:%M:%S) QF chain: C exit=$?" >> trackB_QF_chain.log
echo "$(date +%H:%M:%S) QF chain: COMPLETE" >> trackB_QF_chain.log
