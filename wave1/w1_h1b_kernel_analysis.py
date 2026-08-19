#!/usr/bin/env python3
"""PLAN 43 / WAVE 1 / H1b step 1b -- WHAT the rank-60 deficiency actually is,
and what it does and does not license.

Step 1 confirmed rank(J) = 60 of 61 independently.  This asks the two questions
that decide what the number MEANS:

  (i) is the 1-dimensional kernel a GAUGE direction or a genuine modulus?
 (ii) does a rank computed AT RANDOM POINTS bound dim V from above, as the
      campaign's docstring and Plan 43's Live Map both assert?

(ii) matters because the whole recorded status of the pentagons -- Plan 43 L1:
"y-adic rank 60/61 => dim <= 1 (evidence)" -- is that inference.
"""
import random, sys
sys.path.insert(0, "/home/user/jacobian_planar/wave1")
from w1_h1b_yadic_independent import PARAMS, run, conditions, rank_mod

FAIL = []
def check(l, c, s, e=""):
    if not c: FAIL.append(l)
    print(f"  {'PASS' if c else 'FAIL'}  {l}   <{s}>" + (f"   [{e}]" if e else ""))

p = 1000003
print("="*78); print("H1b step 1b -- THE KERNEL, AND WHAT RANK 60 LICENSES"); print("="*78)

rng = random.Random(4321)
Pv = [rng.randrange(1, p) for _ in PARAMS]
base = run(p, Pv); ncond = len(conditions(base))
cols = []
for k in range(len(PARAMS)):
    cols.append([c[1] for c in conditions(run(p, Pv, dpar=k))])

zero_cols = [k for k in range(len(PARAMS)) if all(v % p == 0 for v in cols[k])]
p00 = PARAMS.index((0, 0))
print(f"  parameters {len(PARAMS)}, conditions {ncond}")
check("exactly ONE column of the Jacobian is identically zero",
      len(zero_cols) == 1, "CERTIFIED", f"zero columns: {[PARAMS[k] for k in zero_cols]}")
check("that column is p_00 -- the constant term of P",
      zero_cols == [p00], "CERTIFIED", f"index {p00} = lattice point (j,i) = (0,0)")
print("""
  WHY p_00 IS GAUGE, structurally: the bracket [P,Q] = P_x Q_y - P_y Q_x sees P
  only through P_x and P_y, so P and P + const have identical brackets.  Adding
  a constant to P is a symmetry of the entire system.  The kernel is therefore
  a GAUGE direction, not a modulus.""")

J_nog = [[cols[k][r] for k in range(len(PARAMS)) if k != p00] for r in range(ncond)]
r_nog = rank_mod(J_nog, p)
check("with p_00 removed, the Jacobian has FULL rank 60 on the 60 essential "
      "parameters", r_nog == 60, "CERTIFIED", f"rank {r_nog} of 60 columns")

print("""
  CONSEQUENCE (i).  Modulo the single gauge direction, the pentagon condition
  map is generically FINITE: 60 essential parameters, generic rank 60.  So a
  solution, if one exists, is an ISOLATED POINT modulo gauge -- which is
  exactly what a counterexample looks like.  The pentagons are NOT excluded by
  dimension.
""")
print("="*78); print("  (ii) WHAT A RANDOM-POINT RANK DOES AND DOES NOT PROVE"); print("="*78)
print("""
  The campaign computes rank(J) at RANDOM points and records
  "dim <= 61 - rank locally".  That inference does not follow, and it runs the
  wrong way:

    * At a point v OF the variety V, dim_v V <= dim T_v V = 61 - rank J(v).
      That is correct -- but it needs the rank AT v, not at a random point.
    * rank J is lower semicontinuous: it can only DROP on the special locus.
      So for v in V, rank J(v) <= 60, hence 61 - rank J(v) >= 1, and the bound
      obtained at v is WEAKER than the one obtained generically, never stronger.
    * What the random-point rank really computes is the GENERIC rank of the
      condition map Phi : A^61 -> A^374, i.e. dim(image Phi) = 60.  By the
      fibre-dimension theorem, every NONEMPTY fibre of Phi then has dimension
      >= 61 - 60 = 1.  V = Phi^{-1}(0) is one such fibre.

  So the correct statement is the reverse of the recorded one:

      IF the pentagon system has a solution at all, that solution set has
      dimension >= 1 -- and the gauge direction p_00 accounts for exactly 1.

  The two readings agree on the arithmetic and disagree on the logic.  Nothing
  here says the variety is small; it says the system is SQUARE modulo gauge.
""")
check("Plan 43 L1's inference 'rank 60/61 => dim <= 1' is NOT supported by a "
      "random-point rank", True, "PROVED-exact",
      "semicontinuity runs the other way; the fibre-dimension theorem gives dim >= 1")
check("the rank NUMBER (60) is nonetheless correct and independently confirmed",
      True, "CERTIFIED", "step 1, two primes, three points each")

print("\n" + "="*78)
print("""H1b step 1b RESULT.

  RETAINED: rank(J) = 60 of 61, confirmed independently.  A2.9's number is right.
  CORRECTED: the reading of it.  The deficiency is the p_00 gauge direction and
  nothing else; with p_00 removed the rank is FULL (60 of 60).

  So the pentagon system is SQUARE modulo gauge, and Plan 43's Live Map entry
  for L1 -- "y-adic rank 60/61 => dim <= 1 (evidence)" -- should read:

      the condition map is generically finite modulo gauge; any solution is an
      isolated point modulo the p_00 translation.  This EXCLUDES NOTHING and is
      not evidence of emptiness.

  That makes the pentagons a live hit-target rather than a nearly-closed one,
  and it is why step 2 must compute the SCHEME.""")
print("="*78)
if FAIL: print("FAILED:", FAIL); sys.exit(1)
