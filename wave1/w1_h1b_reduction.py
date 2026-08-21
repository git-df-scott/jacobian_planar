#!/usr/bin/env python3
"""PLAN 43 / WAVE 1 / H1b step 4 -- can the affine reduction be turned into an
EXPORTABLE system?

THE BLOCKER (measured, step 2c): the conditions have degree 12..23 in 61
variables.  A degree-12 form in 61 variables admits ~1e14 monomials, so the
system cannot be written down and no exact engine can be handed it.

THE LEVER (measured, step 2b): each level j = 13..17 is AFFINE in its own
newest slice P_{j-1}.  If the whole block j = 13..17 is JOINTLY affine in the
13 late parameters P_12..P_16, then those 13 unknowns can be eliminated by an
EXACT LINEAR SOLVE -- no expansion -- leaving a system in the 48 early
parameters (45 essential, after the 3 gauges).

BUT "affine in each variable separately" is NOT "jointly affine": xy is affine
in x and in y and is not affine in (x,y).  Step 2b tested only the separate
statement.  This tests the joint one, which is what elimination needs.

TEST: fix the early parameters, take a random LINE inside the 13-dimensional
late-parameter subspace, and read the degree of every condition along it by
exact interpolation over F_p.  Degree 1 everywhere => jointly affine.
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
LATE = [k for j in range(12, 17) for k in slices[j]]
EARLY = [k for j in range(0, 12) for k in slices[j]]
labels = []
for j in range(13, 25):
    for i in range(0, j - 12): labels.append((j, i))

print("="*78); print("H1b step 4 -- IS THE LATE BLOCK JOINTLY AFFINE?"); print("="*78)
print(f"  early parameters P_0..P_11 : {len(EARLY)}")
print(f"  late  parameters P_12..P_16: {len(LATE)}\n")

rng = random.Random(9090)
A = [rng.randrange(1, p) for _ in PARAMS]

def deg_along(direction_idx, rows_upto=17, maxd=12):
    """degree in t of each condition along P = A + t*B, B supported on
    direction_idx only."""
    B = [0]*len(PARAMS)
    for k in direction_idx: B[k] = rng.randrange(1, p)
    vals = []
    for s in range(maxd + 2):
        t = s + 1
        Pv = [(A[k] + t*B[k]) % p for k in range(len(PARAMS))]
        r = run(p, Pv)
        vals.append([c[0] for c in conditions(r)])
    out = {}
    for r in range(len(vals[0])):
        col = [vals[s][r] for s in range(len(vals))]
        d = list(col)
        deg = None
        for order in range(len(d)-1):
            d = [(d[i+1]-d[i]) % p for i in range(len(d)-1)]
            if all(v == 0 for v in d): deg = order; break
        out[r] = deg
    return out

# --- joint test over the whole late block --------------------------------
res = deg_along(LATE)
by_level = {}
for r, d in res.items():
    if r < len(labels): by_level.setdefault(labels[r][0], []).append(d)
print("  degree along a random line in the FULL 13-dimensional late block:")
for j in sorted(by_level):
    ds = [d for d in by_level[j] if d is not None]
    unk = sum(1 for d in by_level[j] if d is None)
    print(f"    level j = {j:2d}:  degrees {sorted(set(ds)) if ds else '?'}"
          + (f"  ({unk} above the probe bound)" if unk else ""))
    if j >= 20: break

lvl_1317 = [d for j in range(13, 18) for d in by_level.get(j, []) if d is not None]
check("levels 13..17 are JOINTLY AFFINE in the 13 late parameters "
      "(degree 1 along a random line in that whole subspace)",
      bool(lvl_1317) and max(lvl_1317) <= 1, "CERTIFIED",
      f"degrees seen: {sorted(set(lvl_1317))}")

lvl_18p = [d for j in range(18, 21) for d in by_level.get(j, []) if d is not None]
check("levels >= 18 are NOT affine in the late block (so the reduction cannot "
      "be extended past level 17)", bool(lvl_18p) and max(lvl_18p) > 1,
      "CERTIFIED", f"degrees seen at j=18..20: {sorted(set(lvl_18p))}")

print("""
  WHAT THIS DECIDES.
  If levels 13..17 are jointly affine in the late block, the 15 conditions there
  form a LINEAR system  M(P_early) * P_late = b(P_early)  whose 15x13 matrix and
  right-hand side are polynomial in the early parameters.  Eliminating P_late is
  then exact linear algebra -- no monomial expansion at any point -- and what
  remains is:
      * 2 compatibility conditions (15 equations, 13 unknowns), and
      * levels 18..24 plus termination, with P_late substituted.
  The question for an EXPORT path is the degree of those残 conditions in the
  early parameters, which step 5 measures.
""")
print("="*78)
if FAIL: print("FAILED:", FAIL); sys.exit(1)
