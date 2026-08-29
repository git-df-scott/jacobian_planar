#!/bin/bash
# Classify the L23 msolve run per the campaign engine contract (tools/README.md):
# every invocation must land in exactly one of EMPTY | NONEMPTY | TIMEOUT | OOM.
# Memory exhaustion arrives TWO ways and both must be caught, or a memory failure
# is silently reported as "no verdict".
cd /home/user/jacobian_planar
while pgrep -x msolve > /dev/null; do sleep 20; done
LOG=wave1/msolve_L23.log; OUT=wave1/pent_L23.out; V=wave1/L23_VERDICT.txt
EXIT=$(grep -o 'EXIT=[0-9]*' "$LOG" 2>/dev/null | tail -1 | cut -d= -f2)
PEAK=$(grep -o 'RSS[^ ]*' "$LOG" 2>/dev/null | tail -1)
SIZE=$(stat -c%s "$OUT" 2>/dev/null || echo 0)
HEAD=$(head -c 200 "$OUT" 2>/dev/null)
{
echo "L23 msolve verdict  ($(date -u +%Y-%m-%dT%H:%M:%SZ))"
echo "system : pent_L23.ms  -- 66 conditions, 1,080,147 monomials, 59 variables"
echo "         (levels 13..23 of the pentagon y-adic conditions; gauges p_00=0, p_10=1)"
echo "exit   : ${EXIT:-unknown}   output bytes: $SIZE"
if   [ "$SIZE" -gt 0 ] && printf '%s' "$HEAD" | grep -q '^\[-1'; then
  echo "VERDICT: EMPTY  -- no common zero over F_p for levels 13..23"
  echo "         => the pentagon system is EMPTY on the p_10 != 0 chart at this prime."
  echo "         NOT promoted: needs a second good prime = 1 mod 3, and the"
  echo "         p_10 = 0 branch closed separately, before any closure claim."
elif [ "$SIZE" -gt 0 ]; then
  echo "VERDICT: NONEMPTY -- solutions reported; ESCALATE to HIT protocol 6.1"
  echo "         (reconstruct in ungauged coordinates FIRST; a lifted point can"
  echo "          satisfy only the gauge-fixed system)"
elif [ "$EXIT" = "124" ]; then
  echo "VERDICT: TIMEOUT -- STALLED"
  echo "         stall point: msolve F4 on 66 polynomials of degree <= 23 in 59"
  echo "         variables did not finish within 3300s."
elif [ "$EXIT" = "137" ] || [ "$EXIT" = "139" ] || grep -qi 'no more memory\|hash table' "$LOG" 2>/dev/null; then
  echo "VERDICT: OOM -- STALLED"
  echo "         stall point: msolve exhausted memory (15 GB box). Same failure"
  echo "         class as the recorded 166-variable run, at 59 variables and"
  echo "         degree <= 23 rather than 166 variables at degree 2."
else
  echo "VERDICT: STALLED -- unclassified exit ${EXIT:-none}; see $LOG"
fi
echo
echo "NEXT (per 6.4 escalation ladder, capped): staged eliminator on the"
echo "smaller exports (L17/L18) -> case-derived weighted ordering -> Singular"
echo "slimgb as the second engine -> STALLED-with-named-stall-point."
} > "$V"
cat "$V"
