#!/bin/bash
# Recovery for leaf 1's p=65539 terminal branch.
#
# r0b_f0_f0_f0_f0 is running against a 2400s stage-2 budget on an
# oversubscribed box, where the same branch took ~10 min on leaf 2. If it
# exceeds the budget, trackB_staged.sing() raises TimeoutExpired, nothing
# catches it, the sweep dies, and trackB_leaf1_chain.sh moves straight on to
# p=65599 — leaving that branch with NO verdict while every surrounding log
# line reads EMPTY. That is a silent branch drop, which the campaign's first
# mandate exists to prevent.
#
# So: wait for the chain to finish its queue, then re-run p=65539 with a 2.5h
# stage budget. Markers skip every branch already closed, so this re-runs
# exactly the outstanding one. Then re-run the leaf-1 exact-Q pass, which the
# chain may also have skipped if the sweep crash propagated.
cd /home/user/jacobian_planar || exit 1

while pgrep -f "trackB_leaf1_chain.sh" > /dev/null; do sleep 60; done
echo "$(date +%H:%M:%S) recover: chain done, re-running p65539 with a long budget" >> trackB_leaf1_recover.log

JCP=65539 JC_ST2_TIMEOUT=9000 taskset -c 0,1 python3 trackB_leaf1_sweep.py \
    >> trackB_leaf1_recover.log 2>&1
rc=$?
echo "$(date +%H:%M:%S) recover: p65539 rerun exit=$rc" >> trackB_leaf1_recover.log

# p65599 may itself have hit the same wall; re-run it with the long budget too.
JCP=65599 JC_ST2_TIMEOUT=9000 taskset -c 0,1 python3 trackB_leaf1_sweep.py \
    >> trackB_leaf1_recover.log 2>&1
rc=$?
echo "$(date +%H:%M:%S) recover: p65599 rerun exit=$rc" >> trackB_leaf1_recover.log

JCLEAF=1 taskset -c 0,1 python3 trackB_exactQ.py >> trackB_leaf1_recover.log 2>&1
rc=$?
echo "$(date +%H:%M:%S) recover: leaf-1 exact-Q exit=$rc" >> trackB_leaf1_recover.log
echo "$(date +%H:%M:%S) recover: COMPLETE" >> trackB_leaf1_recover.log
