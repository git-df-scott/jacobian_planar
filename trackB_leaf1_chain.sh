#!/bin/bash
# P2 continuation: leaf 1 at the two remaining primes, then the exact-Q pass.
#
# Sequential on purpose — one Singular at a time for this track, so it shares
# the box with the P1 exact-Q run and whatever P0 work is in flight. Every
# stage is marker-resumable, so a container restart costs only the stage in
# progress. Verdicts land in trackB_staged_verdicts.log (the log of record).
cd /home/user/jacobian_planar || exit 1

# Wait for the p=65521 leaf-1 sweep, if it is still running.
while pgrep -f "python3 trackB_leaf1_sweep.py" > /dev/null; do sleep 30; done
echo "$(date +%H:%M:%S) chain: p65521 sweep done, starting p65539" >> trackB_leaf1_chain.log

JCP=65539 python3 trackB_leaf1_sweep.py >> trackB_leaf1_chain.log 2>&1
echo "$(date +%H:%M:%S) chain: p65539 exit=$?" >> trackB_leaf1_chain.log

JCP=65599 python3 trackB_leaf1_sweep.py >> trackB_leaf1_chain.log 2>&1
echo "$(date +%H:%M:%S) chain: p65599 exit=$?" >> trackB_leaf1_chain.log

# Exact Q for leaf 1 — the proof standard. Artifacts carry the L1_ prefix.
JCLEAF=1 python3 trackB_exactQ.py >> trackB_leaf1_chain.log 2>&1
echo "$(date +%H:%M:%S) chain: leaf-1 exact-Q exit=$?" >> trackB_leaf1_chain.log
echo "$(date +%H:%M:%S) chain: COMPLETE" >> trackB_leaf1_chain.log
