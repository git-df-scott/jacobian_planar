#!/usr/bin/env python3
"""PLAN 43 / WAVE 1 / H1b step 4b -- degree of ALL 374 conditions in the LATE
block, and what elimination that licenses.

Step 4 probed only levels 13..20 and found degrees 0 and 1 -- including at
levels 18..20, which the probe had expected to be nonlinear.  If the WHOLE
system is jointly affine in the 13 late parameters, then

      M(P_early) . P_late  =  b(P_early)

with M (374 x 13) and b polynomial in the early parameters, and the late
parameters can be eliminated by EXACT LINEAR ALGEBRA with no monomial
expansion anywhere.  That is the only lever that removes variables without
paying the degree-12..23 expansion cost.

Also corrects step 2b's wording: at levels 13..15 the conditions are not merely
affine in the newest slice, they are INDEPENDENT of it (degree 0) -- exactly
what trackB1_yadic_rank.py warned about ("the i = 0 condition at j = 13 is
untouched by P_12, because N(P) forces P_12 to have i >= 4").
"""
import random, sys
sys.path.insert(0, "/home/user/jacobian_planar/wave1")
from w1_h1b_yadic_independent import PARAMS, run, conditions

p = 1000003
FAIL = []
def check(l, c, s, e=""):
    if not c: FAIL.append(l)
    print(f"  {'PASS' if c else 'FAIL'}  {l}   <{s}>" + (f"   [{e}]" if e else ""))

slices = {}
for k, (j, i) in enumerate(PARAMS): slices.setdefault(j, []).append(k)
LATE  = [k for j in range(12, 17) for k in slices[j]]
EARLY = [k for j in range(0, 12) for k in slices[j]]
P10 = PARAMS.index((0, 1))

labels = []
for j in range(13, 25):
    for i in range(0, j - 12): labels.append((j, i))
rng = random.Random(5150)
A = [rng.randrange(1, p) for _ in PARAMS]
base = run(p, A)
for j in range(25, 41):
    for i in range(len(base[j])): labels.append((j, i))
NC = len(labels)

def degrees_along(idx, maxd, hold_p10=True):
    B = [0]*len(PARAMS)
    for k in idx:
        if hold_p10 and k == P10: continue      # p_10 must stay fixed: the
        B[k] = rng.randrange(1, p)              # recursion divides by it
    vals = []
    for s in range(maxd + 2):
        Pv = [(A[k] + (s+1)*B[k]) % p for k in range(len(PARAMS))]
        vals.append([c[0] for c in conditions(run(p, Pv))])
    out = []
    for r in range(NC):
        d = [vals[s][r] for s in range(len(vals))]; deg = None
        for order in range(len(d)-1):
            d = [(d[i+1]-d[i]) % p for i in range(len(d)-1)]
            if all(v == 0 for v in d): deg = order; break
        out.append(deg)
    return out

print("="*78); print("H1b step 4b -- DEGREE IN THE LATE BLOCK, ALL 374 CONDITIONS"); print("="*78)
dl = degrees_along(LATE, maxd=8)
known = [d for d in dl if d is not None]
unknown = sum(1 for d in dl if d is None)
print(f"  conditions probed : {NC}")
print(f"  degrees observed  : {sorted(set(known))}   ({unknown} above the probe bound)")
per = {}
for r, d in enumerate(dl): per.setdefault(labels[r][0], set()).add(d)
print("  by level: " + "  ".join(f"j{j}:{sorted(x, key=lambda v:(v is None, v))}"
                                  for j, x in sorted(per.items()) if j <= 26))
check("EVERY condition is at most AFFINE in the 13 late parameters",
      unknown == 0 and max(known) <= 1, "CERTIFIED",
      f"max degree {max(known) if known else '?'}, {unknown} unresolved")
check("levels 13..15 are INDEPENDENT of the late block (degree 0), correcting "
      "step 2b's wording from 'affine' to 'does not appear'",
      all(0 in per[j] and per[j] <= {0} for j in (13, 14, 15)), "CERTIFIED",
      f"j13 {sorted(per[13])}, j14 {sorted(per[14])}, j15 {sorted(per[15])}")

print("\n--- and the degree in the EARLY parameters, for comparison ---")
de = degrees_along(EARLY, maxd=30)
kn = [d for d in de if d is not None]
print(f"  degrees in the 48 early parameters: {sorted(set(kn))[:12]}"
      f"{' ...' if len(set(kn))>12 else ''}   ({sum(1 for d in de if d is None)} above bound)")

print(f"""
  THE ELIMINATION THIS LICENSES.
    The whole system is  M(P_early) . P_late = b(P_early),  M of size {NC} x 13.
    Solving 13 of those equations for P_late is EXACT LINEAR ALGEBRA over the
    field of fractions in the early parameters -- no monomial expansion.
    What remains is {NC} - 13 = {NC-13} compatibility conditions on the 48 early
    parameters (45 essential after the three gauges).

  BUT the remaining conditions inherit the early-parameter degree above, plus
  the degree of Cramer determinants of M.  Whether THAT is exportable is the
  next measurement -- and it is the whole question for approach (b).""")
print("="*78)
if FAIL: print("FAILED:", FAIL); sys.exit(1)
