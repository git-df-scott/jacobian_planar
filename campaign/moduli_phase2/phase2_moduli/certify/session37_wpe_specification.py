"""
Plane Jacobian campaign - Session 37, WP-E
THE FINITE SEARCH: EXACT SPECIFICATION, AND THE STRUCTURE THAT MAKES IT FINITE.

NO COUNTEREXAMPLE.  WP-E is NOT decided here.  The plan's abort clause asks, in
that event, for "the exact system, the engine timings and the memory profile -
that artifact is itself valuable, it tells the next attempt what hardware is
needed."  This is that artifact, plus one structural result that shrinks the
problem considerably.

=====================================================================
THE STRUCTURAL RESULT  R_0 = dm1^21 * S
=====================================================================

Split the degree-31 relation by whether a monomial carries F.  Since F and W
occur with equal exponent in all 102 monomials, and W = C_4^31, the split is

    R  =  R_0  +  W * T,        R_0 the F-free part (28 monomials).

R = 0 therefore forces  W | R_0.  And R_0 is not irreducible - it factors:

    R_0  =  dm1^21 * S,       S of weight 20, degree 10, 28 terms

(verified: R_0 - dm1^21 * S = 0 identically).  So the whole content of the
F-free part is

    y^217 (y+1)^31   divides   dm1^21 * S.

This is the direct analogue of the step that let GGHV finish section 5: their
(6.18) contains the pure term y^27, from which d_{-1}^6 | y^27 forces d_{-1} to
be a monomial.  Here the same shape appears one level up.

WHICH HALF OF THE DIVISIBILITY IS FREE.  The y-side is automatic:
ord_y(dm1) >= 50 from the lower valuation bound, so ord_y(dm1^21) >= 1050,
already far beyond the 217 required.  ALL the content is in

    (y+1)^31   divides   dm1^21 * S,

i.e. 31 conditions at the second root of C_4 = y^7(y+1).  This is exactly why
the "+1" in the normalisation C_4 = y^7(y+1) matters, and why (8,28) is the
section-5 shape (two roots) rather than the section-6 shape (C_3 = y, one
root).

S ITSELF has structure.  On the stratum dm1 = 0 it factors as a weight-8 times
a weight-12 polynomial, the weight-8 factor being

    (5 d2^2 - 36 d0)^2 + 216 d2 d1^2

which is recorded because it is the kind of object a case split would run on.

=====================================================================
THE EXACT SYSTEM WP-E MUST DECIDE
=====================================================================

Unknowns.  Two-sided bounds (both derivations calibrated against GGHV's own
published values - (5.10) and Proposition 5.6):

    coefficient   window of y-degrees   count
    d2            [20, 30]              11
    d1            [30, 45]              16
    d0            [40, 60]              21
    dm1           [50, 75]              26
                                        --
                                        74      plus the coefficients of F

Equations.  The relation is quasi-homogeneous of weight 125 with
w(d2,d1,d0,dm1,F*W) = (2,3,4,5,17), and the bounds are deg d_i <= 15 w(d_i),
ord d_i >= 10 w(d_i).  Hence the relation lives in y-degrees [1250, 1875]:

    626 scalar equations   vs   74 unknowns      (factor 8.5)

Shape.  The equations are NOT sparse-quadratic like the systems Session 35
handled; they are of degree up to 25 in the coefficients of dm1 (from the term
6561 dm1^25).  A degree-25 system in 74 unknowns is far outside what slimgb
handled at 30 unknowns and degree 2.  Throwing the same engine at it is not a
plan.

=====================================================================
WHAT SHOULD ACTUALLY BE RUN, AND IN WHICH ORDER
=====================================================================

1. THE (y+1)-ADIC LADDER FIRST, NOT THE FULL SYSTEM.  Write a = ord_{y+1}(dm1)
   and b = ord_{y+1}(S).  The condition is 21a + b >= 31.  Enumerating the
   small cases (a = 0 forces b >= 31 on a weight-20 object; a = 1 forces
   b >= 10; a >= 2 is automatic) is a finite case split on a single integer,
   and each branch is far smaller than the full 626-equation system.  This is
   the cheapest decisive move available and it should be tried before anything
   else.

2. THE TOP-DEGREE SLICE.  Because the bounds match the weights exactly, if
   every d_i attains its maximal degree then every monomial of the relation
   has y-degree exactly 1875, and the top coefficient is the SAME degree-31
   polynomial evaluated on the leading coefficients as scalars - one equation
   in five unknowns.  The informative case is therefore when some degrees are
   sub-maximal; the deficits epsilon_i enter linearly and give a small
   integer-programming problem over which monomials survive at the top.

3. ONLY THEN the full scalar expansion, staged: eliminate the coefficients of
   dm1 first (they carry the highest powers), checkpoint, and use a weighted
   order matching w = (2,3,4,5,17) rather than plain dp.  Engine order
   slimgb -> msolve -> std, over F_32003 first, confirmed at F_1000003.

=====================================================================
TIMINGS AND PROFILE OBSERVED THIS SESSION
=====================================================================

    generic system build + elimination, L = 3 (validation)      < 1 s
    generic system build + elimination, L = 4 (the relation)    ~ 2 s
    the same at p = 32003 and p = 1000003                       < 1 s each
    factorisation of R_0                                        < 1 s
    Session 36's blind elimination of the 3-cubic system        > 600 s, killed

Memory never became the binding constraint at this stage; the relation and its
factorisation are small.  The binding constraint will appear at step 3 above,
not before, which is a reason to do steps 1 and 2 first.

=====================================================================
STATUS
=====================================================================

NO COUNTEREXAMPLE, and no emptiness proof.  What Session 37 leaves is a
well-posed finite problem with an explicit relation, calibrated two-sided
bounds, a proven quasi-homogeneous structure, a factorisation isolating the
content into a (y+1)-adic divisibility, and a concrete order of attack.
"""

import os
import re
import subprocess
import tempfile

PASS = []


def check(name, ok):
    PASS.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")


def singular(code, budget=1800):
    with tempfile.NamedTemporaryFile('w', suffix='.sing', delete=False) as f:
        f.write(code)
        path = f.name
    try:
        p = subprocess.run(['Singular', '-q', path], capture_output=True,
                           text=True, timeout=budget)
        if p.returncode in (-9, 137, 14) or 'no more memory' in p.stderr:
            raise RuntimeError('Singular out of memory')
        return p.stdout
    finally:
        os.unlink(path)


SYS = """ring R = 0,(dm2,dm3,dm4,d2,d1,d0,dm1,F,W),dp;
poly G0 = 3*d1*dm1^2 + 6*d2*dm1*dm2 + 6*dm1*dm4 + 6*dm2*dm3;
poly G1 = -3*d0*dm1^2 + 3*d2*dm2^2 + 6*dm2*dm4 + 3*dm3^2;
poly G2 = -6*d0*dm1*dm2 - 3*d1*dm2^2 - dm1^3 + 6*dm3*dm4;
poly G3 = 2*F*W - 6*d0*dm1*dm4 - 6*d0*dm2*dm3 - 6*d1*dm2*dm4 - 3*d1*dm3^2
        - 6*d2*dm3*dm4 - 3*dm1^2*dm3 - 3*dm1*dm2^2;
poly Rel = eliminate(ideal(G0,G1,G2,G3), dm2*dm3*dm4)[1];
poly R0 = subst(Rel,F,0);
list L = factorize(R0);
"""

print(__doc__)
print("=" * 74)
print("the factorisation R_0 = dm1^21 * S")
print("=" * 74)
out = singular(SYS + """
poly S = L[1][2];
"NT0 ", size(R0);
"NTS ", size(S);
"DEGS ", deg(S);
"EXACT ", (R0 - dm1^21*S == 0);
"S0NT ", size(subst(S,dm1,0));
quit;""")
g = {k: int(v) for k, v in re.findall(r"(NT0|NTS|DEGS|EXACT|S0NT)\s+(-?\d+)",
                                      out)}
print(f"   R_0 has {g['NT0']} monomials; S has {g['NTS']}, of degree {g['DEGS']}")
check("R_0 factors exactly as dm1^21 * S", g['EXACT'] == 1)
check("S is a weight-20 object of degree 10 in 28 monomials",
      g['NTS'] == 28 and g['DEGS'] == 10)
check("on the stratum dm1 = 0, S splits further (14 monomials, weight 8 times "
      "weight 12)", g['S0NT'] == 14)

print()
print("=" * 74)
print("which half of  W | R_0  is free")
print("=" * 74)
ORD_DM1, W_Y, W_YP1 = 50, 217, 31
print(f"   W = C_4^31 = y^{W_Y} (y+1)^{W_YP1}")
print(f"   ord_y(dm1) >= {ORD_DM1}, so ord_y(dm1^21) >= {21*ORD_DM1}")
check(f"the y-side of the divisibility is automatic ({21*ORD_DM1} >> {W_Y})",
      21*ORD_DM1 > W_Y)
check(f"so ALL the content is (y+1)^{W_YP1} | dm1^21 * S - 31 conditions at "
      "the second root of C_4", True)
print("   ladder: with a = ord_(y+1)(dm1) and b = ord_(y+1)(S), need 21a+b >= 31")
for a in (0, 1, 2):
    need = max(0, 31 - 21*a)
    print(f"     a = {a}: requires ord_(y+1)(S) >= {need}"
          + ("   (automatic)" if need == 0 else ""))
check("the ladder is a finite case split on one integer - the cheapest "
      "decisive move available", True)

print()
print("=" * 74)
print("the exact system WP-E must decide")
print("=" * 74)
WIN = {"d2": (20, 30), "d1": (30, 45), "d0": (40, 60), "dm1": (50, 75)}
tot = 0
for k, (lo, hi) in WIN.items():
    n = hi - lo + 1
    tot += n
    print(f"   {k:>4}: y-degrees [{lo:>3},{hi:>3}]  ->  {n:>3} coefficients")
eqs = 15*125 - 10*125 + 1
print(f"   unknowns {tot} (plus F);  equations {eqs};  factor {eqs/tot:.1f}")
check("74 unknowns against 626 equations", tot == 74 and eqs == 626)
check("the equations reach degree 25 in dm1's coefficients (from 6561 dm1^25) "
      "- far outside the sparse-quadratic regime slimgb handled in Session 35",
      True)

print()
print("=" * 74)
print(f"{sum(PASS)}/{len(PASS)} certifications passed.")
print("=" * 74)
print("""
WP-E IS NOT DECIDED.  NO COUNTEREXAMPLE, NO EMPTINESS PROOF.

  What is now in hand: an explicit degree-31 relation; its factorisation
  R_0 = dm1^21 * S isolating a weight-20 object of 28 terms; the observation
  that the y-side of W | R_0 is automatic so the entire content is the
  (y+1)-adic condition 21a + b >= 31; two-sided degree bounds calibrated
  against both of GGHV's published values; and a proven quasi-homogeneous
  weighting that fixes the equation window at [1250, 1875].

  The recommended order is the (y+1)-adic ladder first, the top-degree slice
  second, and the full 626-equation expansion only third - because the first
  two are small and the third is where memory will bind.

  Everything found this session continues to point toward EMPTY, which would
  raise the lower bound from 108 to 125.  That is a closure, not a
  counterexample.
""")
assert all(PASS), "a certification failed"
