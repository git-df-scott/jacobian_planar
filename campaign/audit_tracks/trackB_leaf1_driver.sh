#!/bin/bash
# Single driver for the remaining leaf-1 work, replacing the earlier
# chain + recover pair.
#
# Why a replacement: those two were edited in place while bash was executing
# them. Bash reads a script incrementally by byte offset, so inserting lines
# into a running script can make it resume mid-command. Both were therefore
# retired and their remaining work folded in here.
#
# Everything below is marker-resumable, so re-running finished branches is
# nearly free and nothing is recomputed that already has a verdict.
#
# Stage budget: JC_ST2_TIMEOUT=9000 (2.5h) rather than the 2400s default.
# p=65539's terminal branch r0b_f0_f0_f0_f0 blew through 2400s on this
# oversubscribed box against a ~10min precedent on leaf 2, and the resulting
# TimeoutExpired killed that sweep with the branch unverified.
cd /home/user/jacobian_planar || exit 1
LOG=trackB_leaf1_driver.log

# Let any sweep already in flight finish on its own terms.
while pgrep -f "python3 trackB_leaf1_sweep.py" > /dev/null; do sleep 45; done
echo "$(date +%H:%M:%S) driver: start" >> $LOG

for p in 65539 65599; do
  JCP=$p JC_ST2_TIMEOUT=9000 taskset -c 0,1 python3 trackB_leaf1_sweep.py >> $LOG 2>&1
  rc=$?   # captured BEFORE any command substitution, which resets $?
  echo "$(date +%H:%M:%S) driver: p$p exit=$rc" >> $LOG
done

# Exact Q for leaf 1 — the proof standard. Artifacts carry the L1_ prefix.
JCLEAF=1 taskset -c 0,1 python3 trackB_exactQ.py >> $LOG 2>&1
rc=$?
echo "$(date +%H:%M:%S) driver: leaf-1 exact-Q exit=$rc" >> $LOG
echo "$(date +%H:%M:%S) driver: COMPLETE" >> $LOG
