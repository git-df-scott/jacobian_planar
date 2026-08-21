#!/bin/bash
# Wait for job #1 (PID 24828) to end, then run the REDUCED seed system with the
# whole machine.  #2 was stopped deliberately at 19:05 rather than left to be
# OOM-killed: it had failed twice on address-space caps (3.5 then 5.0 GiB) and
# was growing at ~0.63 GB/min against 3.7 GB of headroom.
cd /home/user/jacobian_planar/wave6/pentseed
while kill -0 24828 2>/dev/null; do sleep 15; done
echo "$(date +%T) job #1 has ended -- #1 verdict: [$(cat seed0_p1000003.out)] ($(stat -c%s seed0_p1000003.out) bytes)"
free -m | head -2
echo 1000 > /proc/self/oom_score_adj
echo "$(date +%T) launching reduced 241eq/123unk, no cap, full machine"
/usr/bin/time -f "TIME %e s RSS %M KB" timeout 3000 msolve -f seed0_p1000003_lin.ms -o seed0_lin.out 2>&1 | tail -3
echo "$(date +%T) DONE reduced -> [$(head -c 150 seed0_lin.out 2>/dev/null)] ($(stat -c%s seed0_lin.out) bytes)"
