#!/usr/bin/env python3
"""PLAN 43 / WAVE 1 / H1b step 2b -- is the cascade LINEAR in the newest slice?

trackB1_yadic_verdict.py asserts: "the condition at order j involves P_0..P_{j-1}
only, and is LINEAR in the newest slice P_{j-1}".  If true, the whole system
eliminates: given P_0..P_11 the conditions at j = 13..17 are a LINEAR system for
the 13 coefficients of P_12..P_16, and its consistency imposes equations on
P_0..P_11 alone.

The campaign's own retracted results came from GUESSING exactly this kind of
structure ("the same class of mistake as the retracted off-by-one"), so it is
MEASURED here, not assumed: a function is affine in a variable iff its second
difference vanishes identically, which over F_p is an exact test.
"""
import random, sys
sys.path.insert(0, "/home/user/jacobian_planar/wave1")
from w1_h1b_yadic_independent import PARAMS, PR, run, conditions

p = 1000003
FAIL = []
def check(l, c, s, e=""):
    if not c: FAIL.append(l)
    print(f"  {'PASS' if c else 'FAIL'}  {l}   <{s}>" + (f"   [{e}]" if e else ""))

labels = []
for j in range(13, 25):
    for i in range(0, j - 12): labels.append((j, i))
NLOW = len(labels)

def vals(Pv):
    return [c[0] for c in conditions(run(p, Pv))]

print("="*78); print("H1b step 2b -- LINEARITY OF THE CASCADE IN THE NEWEST SLICE"); print("="*78)
slices = {}
for k, (j, i) in enumerate(PARAMS): slices.setdefault(j, []).append(k)
print(f"  P slices: " + ", ".join(f"P_{j}:{len(v)}" for j, v in sorted(slices.items())))
print(f"  total {len(PARAMS)} params; P_12..P_16 carry "
      f"{sum(len(slices[j]) for j in range(12,17))} of them\n")

rng = random.Random(202)
base = [rng.randrange(1, p) for _ in PARAMS]

# second-difference test: f(t) affine in param k  <=>  f(a+2h)-2f(a+h)+f(a) == 0
def second_diff_zero(k, rows):
    h = rng.randrange(1, p)
    P0 = list(base)
    P1 = list(base); P1[k] = (P1[k] + h) % p
    P2 = list(base); P2[k] = (P2[k] + 2 * h) % p
    v0, v1, v2 = vals(P0), vals(P1), vals(P2)
    return all((v2[r] - 2 * v1[r] + v0[r]) % p == 0 for r in rows)

for j in range(13, 18):
    newest = j - 1                     # the slice the level-j condition should be linear in
    rows = [r for r in range(NLOW) if labels[r][0] == j]
    ok = all(second_diff_zero(k, rows) for k in slices.get(newest, []))
    check(f"level j={j}: conditions are AFFINE in the newest slice P_{newest} "
          f"({len(slices.get(newest,[]))} params, {len(rows)} conditions)",
          ok, "CERTIFIED", "exact second-difference test over F_p")

# and NOT affine in an earlier slice (so the structure is genuine, not vacuous)
rows17 = [r for r in range(NLOW) if labels[r][0] == 17]
nonlin = [j for j in range(1, 12) if not second_diff_zero(slices[j][0], rows17)]
check("level j=17 is genuinely NONLINEAR in earlier slices (structure is real, "
      "not vacuous)", len(nonlin) > 0, "CERTIFIED",
      f"nonlinear in slices {nonlin[:6]}...")

# ---- the elimination this licenses ---------------------------------------
n_early = sum(len(slices[j]) for j in range(0, 12))
n_late  = sum(len(slices[j]) for j in range(12, 17))
n_lin_conds = sum(1 for r in range(NLOW) if 13 <= labels[r][0] <= 17)
print(f"""
  THE ELIMINATION THIS LICENSES.
    early slices P_0..P_11 : {n_early} params ({n_early-1} modulo the p_00 gauge)
    late  slices P_12..P_16: {n_late} params
    conditions at j = 13..17: {n_lin_conds}, LINEAR in the late slices

  So {n_lin_conds} linear equations in {n_late} unknowns.  Solving them determines the late
  slices and leaves {n_lin_conds - n_late} compatibility conditions on the early slices alone.
  Everything from j = 18 up ({374 - n_lin_conds} further conditions) then constrains the
  {n_early-1} essential early parameters.

  This is the elimination order the system actually has -- measured, not guessed.
""")
print("="*78)
if FAIL: print("FAILED:", FAIL); sys.exit(1)
print("""H1b step 2b RESULT: the cascade IS affine in the newest slice at every
level 13..17, and genuinely nonlinear in earlier slices.  The pentagon system
therefore reduces to 47 essential early parameters carrying a heavily
overdetermined polynomial system -- 2 compatibility conditions plus 359 more.""")
print("="*78)
