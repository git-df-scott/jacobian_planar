#!/bin/bash
# Serialized engine queue: G2 chart A, then the G1 ladder.  Exactly one engine
# process runs at any moment -- the stages are sequential by construction, not
# by convention.  Both stages resume, so re-running this script never repeats
# completed work.
cd /home/user/jacobian_planar
echo "=== QUEUE: G2 chart A d=3..8 (300 s elimination deadline) ==="
GGV_ETIMEOUT=300 python3 ggv/g23_eliminants.py A 3 4 5 6 7 8 >> ggv/logs/G2b.log 2>&1
echo "=== QUEUE: G1 ladder d=8..12 (900 s deadline) ==="
GGV_TIMEOUT=900 python3 ggv/g1_ladder.py 8 9 10 11 12 >> ggv/logs/G1_ladder.log 2>&1
echo "=== QUEUE COMPLETE ==="
