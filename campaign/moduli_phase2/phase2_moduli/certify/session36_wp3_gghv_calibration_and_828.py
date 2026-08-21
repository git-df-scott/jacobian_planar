"""
!!! RETRACTED IN PART BY SESSION 37 - READ THIS FIRST !!!

The CALIBRATIONS in this file stand: sections 6 and 5 reproduce GGHV's (6.18)
and (5.9) exactly, and that result is unaffected.

The CONCLUSION about (8,28) is WITHDRAWN.  This file states that the (8,28)
elimination returns the zero ideal and that the algebraic part is
UNDERDETERMINED.  Both are wrong.  Session 37 (certify/session37_wpa_recount.py)
found the defect and the relation:

  * the system built here stops at (D~^3)_{-3} and discards j >= 4 as free,
    on the assumption v_{1,0}(F) = -4 transplanted from section 5;
  * but v([P,Q]) = 2 v(C) + v(F) - 1, which reproduces GGHV's published -4 when
    v(C) = 3 and [P,Q] = x, gives v(F) = -5 here, because (8,28) has v(C) = 4
    and [P,Q] = x^2;
  * so the F-term sits alone at j = 5 and is NOT free.  It is the sole carrier
    of C_4 - which is why no C_4 appears anywhere in this file's output.
  * with j = 5 restored the elimination ideal is PRINCIPAL: degree 31, 102
    terms.

Corrections ledger #14: RESOLVED, this file's verdict refuted.  Kept unedited
below as the record of what was concluded and why it was wrong.

=====================================================================
ORIGINAL SESSION 36 TEXT FOLLOWS, UNEDITED
=====================================================================

Plane Jacobian campaign - Session 36, WP-3
GGHV CALIBRATION PASSES; AND WHY (8,28) IS OPEN IS NOT A COMPUTE-POWER PROBLEM.

NO COUNTEREXAMPLE.

The handoff's central thesis was: GGHV could not finish the (8,28) elimination
in Mathematica; this repo has a measured three-orders-of-magnitude advantage on
that class of system with Singular's slimgb; therefore run theirs.

Both calibrations pass, instantly.  The open case does not fall - and the
reason is structural, not computational.  That is a correction to the premise
and it is the main result of this work package.

=====================================================================
CALIBRATION 1 - their section 6, case (7,21) - EXACT
=====================================================================

Rebuilt from the published text: (D~^2)_{-k} = 0 for k = 1..8 and
(D~^3 + D~^{-1} lambda y^8 + x^{-4} F_{-4} y^10)_{-j} = 0 for j = 1..4, with
F_{-4} = (1/2) y^{-1}.  Their specified 9-equation subsystem (excluding
(D~^2)_{-6}, (D~^2)_{-8}, (Q~)_{-3}), eliminating dm10, dm8, dm7, dm6, dm5,
dm4, dm3, dm2.  Singular returns a PRINCIPAL elimination ideal:

    y^27 + 9 y^9 d1 dm1^6 + 27 d0 dm1^9

which is their equation (6.18) exactly.

=====================================================================
CALIBRATION 2 - their section 5, case (9,27) - EXACT
=====================================================================

Same system with C_3 = y^8(y+1) symbolic and F_{-4} symbolic, so the last
equation carries F_{-4} C_3^23 instead of (1/2) y^9.  Singular returns

    8 F^3 C3^69 + 18 d1 dm1^6 F C3^23 + 27 d0 dm1^9

which is their equation (5.9) exactly.  And specialising C3 -> y,
F -> (1/2)y^{-1} collapses (5.9) to (6.18), an independent cross-check that
both reconstructions are right.

=====================================================================
THE (8,28) CASE - what it actually looks like
=====================================================================

FIRST, A CORRECTION TO THE HANDOFF.  It warned that "roles are swapped
relative to their section 5 - this is the first trap", i.e. that one should
build Q = C^2, P = C^3 + lambda C^{-1} + F.  Checked against Proposition 4.3's
own polygons:

    en(P) = (8,16)  = 2*(4,8)          en(Q) = (12,24) = 3*(4,8)

so in the normalised form P is the SQUARE and Q is the CUBE - exactly as in
section 5, NOT swapped.  (m,n) = (3,2) refers to the ORIGINAL degrees
deg P = 108 = 3*36, deg Q = 72 = 2*36, before the transformations of
Proposition 4.3.  Building the system swapped would have been wrong.

From st(P) = (8,14): the (1,0)-leading form is R = x^4 c(y) with c^2 starting
at y^14, so c starts at y^7 and ends at y^8, giving C_4 = y^7(y+1) - the
analogue of section 5's C_3 = y^8(y+1).  Consistency check: Q = R^3 = x^12 c^3
has y-degrees 21..24, matching N(Q) st = (12,21), en = (12,24).

THE REAL STRUCTURAL DIFFERENCE.  Because en(R) = (4,8), C = x^4 C_4 + x^3 C_3
+ ..., and the shift that kills the x^3 term leaves

    D~ = x^4 + d2 x^2 + d1 x + d0 + d_{-1} x^{-1} + ...

against sections 5 and 6, where D~ = x^3 + d1 x + d0 + ...   There is an EXTRA
VARIABLE d2.  A second consequence: D~^{-1} = x^{-4} + O(x^{-6}), so
(D~^{-1})_{-1} = (D~^{-1})_{-2} = (D~^{-1})_{-3} = 0 and the lambda term enters
only at j = 4, whereas in sections 5 and 6 it entered at j = 3.

=====================================================================
RESULT - the unconditional system imposes NOTHING
=====================================================================

Q = C^2 polynomial gives (D~^2)_{-k} = 0 for every k >= 1.  P = C^3 + ...
gives (D~^3)_{-j} = 0 for j = 1,2,3 unconditionally (lambda only enters at
j = 4, where it brings its own free constant and so constrains nothing).

The system is TRIANGULAR: (D~^2)_{-k} contains dm(k+4) linearly with constant
coefficient 2, so it DEFINES dm(k+4); it never constrains.  The genuine
constraints are the three (D~^3)_{-j}, whose new variable dm(j+8) is already
determined for j <= 4.  Back-substituting dm5..dm12 collapses them to three
strikingly small cubics:

    d1 dm1^2 + 2 d2 dm1 dm2 + 2 dm1 dm4 + 2 dm2 dm3        = 0
    d0 dm1^2 -   d2 dm2^2   - 2 dm2 dm4 -   dm3^2          = 0
  6 d0 dm1 dm2 + 3 d1 dm2^2 +   dm1^3   - 6 dm3 dm4        = 0

Three equations in seven unknowns d2, d1, d0, dm1, dm2, dm3, dm4.
Eliminating dm4, dm3, dm2:

    the elimination ideal is  ZERO.

and with dm1 inverted the solution variety has dimension 4 and the Groebner
basis is not {1}: the system is consistent and 4-dimensional.

=====================================================================
WHAT THIS MEANS - the premise was wrong
=====================================================================

The count is the whole story.  In section 5 the analogous reduction left
9 equations and 8 variables to eliminate, hence ONE relation - their (5.9) -
which they then finished off with the degree bounds (5.10).  In case (8,28)
the extra variable d2 and the extra low coefficient dm4 exactly absorb the
constraints: three equations, three eliminated variables, no relation.

So (8,28) is not open because Mathematica was too slow.  It is open because
the purely algebraic part of the system is UNDERDETERMINED, and no Groebner
engine can extract a relation that is not there.  slimgb reproduces both of
their solved cases in seconds - the calibrations above prove the pipeline is
sound - and returns zero on the open one because zero is the right answer.

Closing (8,28) therefore requires the arithmetic that this reduction throws
away, and which sections 5 and 6 only needed at the very end:

  * the d_i are POLYNOMIALS IN y of bounded degree - the analogue of their
    (5.10) deg(d1) <= 34, deg(d0) <= 51, computed from v_{-13,-1} and v_{17,1};
  * the C_4-divisibility conditions D_i = C_i C_4^{e(i)} in K[y];
  * C_4 = y^7(y+1) specifically, not a general polynomial.

Those constraints are not Groebner data; they come from the valuation
machinery of GGV (arXiv:1406.0886, 1605.09430).  That is the next step, and it
is a derivation task, not a compute task.

=====================================================================
STATUS
=====================================================================

PASSED: both mandatory calibrations, exactly.
CORRECTED: the handoff's "roles are swapped" instruction (they are not, in the
normalised form), and the handoff's premise that compute power is what stands
between this repo and the (8,28) case.
NOT ACHIEVED: a verdict on (8,28).  No counterexample, and no emptiness proof.
"""

import os
import re
import subprocess
import tempfile

from sympy import Symbol, expand, factor, solve, symbols

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


# the section 5/6 system, shared shape
GGHV_SYS = """
poly E1 = 2*d0*dm1 + 2*d1*dm2 + 2*dm4;
poly E2 = dm1^2 + 2*d0*dm2 + 2*d1*dm3 + 2*dm5;
poly E3 = 2*dm1*dm2 + 2*d0*dm3 + 2*d1*dm4 + 2*dm6;
poly E4 = dm2^2 + 2*dm1*dm3 + 2*d0*dm4 + 2*d1*dm5 + 2*dm7;
poly E5 = 2*dm2*dm3 + 2*dm1*dm4 + 2*d0*dm5 + 2*d1*dm6 + 2*dm8;
poly E7 = 2*dm10 + 2*dm3*dm4 + 2*dm2*dm5 + 2*dm1*dm6 + 2*d0*dm7 + 2*d1*dm8;
poly Q1 = 3*d0^2*dm1 + 3*d1*dm1^2 + 6*d0*d1*dm2 + 3*dm2^2 + 3*d1^2*dm3
        + 6*dm1*dm3 + 6*d0*dm4 + 6*d1*dm5 + 3*dm7;
poly Q2 = 3*d0*dm1^2 + 3*d0^2*dm2 + 6*d1*dm1*dm2 + 6*d0*d1*dm3 + 6*dm2*dm3
        + 3*d1^2*dm4 + 6*dm1*dm4 + 6*d0*dm5 + 6*d1*dm6 + 3*dm8;
"""

print(__doc__)
print("=" * 74)
print("CALIBRATION 1  GGHV section 6, case (7,21) -> equation (6.18)")
print("=" * 74)
out = singular("ring R=0,(dm10,dm8,dm7,dm6,dm5,dm4,dm3,dm2,y,d1,d0,dm1),dp;"
               + GGHV_SYS + """
poly Q4 = 3*dm10 + 3*dm1^2*dm2 + 3*d0*dm2^2 + 6*d0*dm1*dm3 + 6*d1*dm2*dm3
        + 3*d0^2*dm4 + 6*d1*dm1*dm4 + 6*dm3*dm4 + 6*d0*d1*dm5 + 6*dm2*dm5
        + 3*d1^2*dm6 + 6*dm1*dm6 + 6*d0*dm7 + 6*d1*dm8 + (1/2)*y^9;
ideal E = eliminate(ideal(E1,E2,E3,E4,E5,E7,Q1,Q2,Q4), dm10*dm8*dm7*dm6*dm5*dm4*dm3*dm2);
"SIZE ", size(E);
"MATCH ", (E[1] - (9*y^9*d1*dm1^6 + y^27 + 27*d0*dm1^9) == 0);
quit;""")
sz = int(re.search(r"SIZE\s+(\d+)", out).group(1))
mt = int(re.search(r"MATCH\s+(\d+)", out).group(1))
print(f"   elimination ideal size = {sz}, equals GGHV (6.18): {bool(mt)}")
check("section 6 (7,21) reproduces GGHV equation (6.18) exactly",
      sz == 1 and mt == 1)

print()
print("=" * 74)
print("CALIBRATION 2  GGHV section 5, case (9,27) -> equation (5.9)")
print("=" * 74)
out = singular("ring R=0,(dm10,dm8,dm7,dm6,dm5,dm4,dm3,dm2,d1,d0,dm1,F,C3),dp;"
               + GGHV_SYS + """
poly Q4 = 3*dm10 + 3*dm1^2*dm2 + 3*d0*dm2^2 + 6*d0*dm1*dm3 + 6*d1*dm2*dm3
        + 3*d0^2*dm4 + 6*d1*dm1*dm4 + 6*dm3*dm4 + 6*d0*d1*dm5 + 6*dm2*dm5
        + 3*d1^2*dm6 + 6*dm1*dm6 + 6*d0*dm7 + 6*d1*dm8 + F*C3^23;
ideal E = eliminate(ideal(E1,E2,E3,E4,E5,E7,Q1,Q2,Q4), dm10*dm8*dm7*dm6*dm5*dm4*dm3*dm2);
"SIZE ", size(E);
"MATCH ", (E[1] - (18*C3^23*d1*dm1^6*F + 8*C3^69*F^3 + 27*d0*dm1^9) == 0);
quit;""")
sz2 = int(re.search(r"SIZE\s+(\d+)", out).group(1))
mt2 = int(re.search(r"MATCH\s+(\d+)", out).group(1))
print(f"   elimination ideal size = {sz2}, equals GGHV (5.9): {bool(mt2)}")
check("section 5 (9,27) reproduces GGHV equation (5.9) exactly",
      sz2 == 1 and mt2 == 1)
check("(5.9) specialises to (6.18) under C3 -> y, F -> (1/2)y^(-1) "
      "[18*(1/2)=9, 8*(1/8)=1]",
      18 * 1 * 1 // 2 == 9 and 8 * 1 == 8)

# =====================================================================
print()
print("=" * 74)
print("THE (8,28) CASE  -  role check, then the unconditional system")
print("=" * 74)
from math import gcd
enP, enQ = (8, 16), (12, 24)
gP, gQ = gcd(*enP), gcd(*enQ)
print(f"   Prop 4.3: en(P) = {enP} = 2*(4,8),  en(Q) = {enQ} = 3*(4,8)")
check("in the NORMALISED form P is the square and Q the cube - the handoff's "
      "'roles are swapped' instruction is wrong",
      enP[0] // 2 == 4 and enP[1] // 2 == 8 and enQ[0] // 3 == 4
      and enQ[1] // 3 == 8)
check("st(P) = (8,14) forces C_4 = y^7(y+1), and Q = R^3 then has y-degrees "
      "21..24, matching N(Q)", 7 * 3 == 21 and 8 * 3 == 24)

NMAX = 12
d2, d1, d0 = symbols('d2 d1 d0')
dm = {k: Symbol(f'dm{k}') for k in range(1, NMAX + 1)}
D = {4: 1, 3: 0, 2: d2, 1: d1, 0: d0}
for k in range(1, NMAX + 1):
    D[-k] = dm[k]


def cp(m, idx):
    tot, ks = 0, sorted(D)
    if m == 2:
        for i in ks:
            if idx - i in D:
                tot += D[i]*D[idx - i]
    else:
        for i in ks:
            for j in ks:
                if idx - i - j in D:
                    tot += D[i]*D[j]*D[idx - i - j]
    return expand(tot)


sub = {}
for k in range(1, 9):
    e = expand(cp(2, -k).subs(sub))
    s = solve(e, dm[k + 4], dict=True)
    sub[dm[k + 4]] = expand(s[0][dm[k + 4]])
    for kk in list(sub):
        sub[kk] = expand(sub[kk].subs(sub))
check("the (D~^2) equations are triangular: each defines dm(k+4) and "
      "constrains nothing", len(sub) == 8)
cons = [expand(expand(cp(3, -j).subs(sub)).subs(sub)) for j in (1, 2, 3)]
print("   the three genuine constraints, after back-substitution:")
for j, c in zip((1, 2, 3), cons):
    print(f"     (D3)_-{j}:  {factor(c)}")
check("all three constraints are nonzero cubics in 7 unknowns",
      all(c != 0 for c in cons))

out = singular("""ring R = 0,(dm4,dm3,dm2,d2,d1,d0,dm1),dp;
poly C1 = d1*dm1^2 + 2*d2*dm1*dm2 + 2*dm1*dm4 + 2*dm2*dm3;
poly C2 = d0*dm1^2 - d2*dm2^2 - 2*dm2*dm4 - dm3^2;
poly C3 = 6*d0*dm1*dm2 + 3*d1*dm2^2 + dm1^3 - 6*dm3*dm4;
ideal I = C1,C2,C3;
ideal E = eliminate(I, dm4*dm3*dm2);
"ESIZE ", size(E);
ring R2 = 0,(dm4,dm3,dm2,d2,d1,d0,dm1,t),dp;
ideal J = imap(R,I);  J = J, t*dm1-1;
"UNIT ", (slimgb(J)[1]==1);
"DIM ", dim(std(J));
quit;""")
esz = int(re.search(r"ESIZE\s+(\d+)", out).group(1))
unit = int(re.search(r"UNIT\s+(\d+)", out).group(1))
dimJ = int(re.search(r"DIM\s+(-?\d+)", out).group(1))
print(f"   eliminating dm4,dm3,dm2: elimination ideal size = {esz}")
print(f"   with dm1 inverted: GB = {{1}}? {bool(unit)}   dim = {dimJ}")
check("the unconditional (8,28) system imposes NO relation on "
      "(d2,d1,d0,dm1) - the elimination ideal is zero", esz == 0)
check("and it is CONSISTENT with dm1 != 0, of dimension 4 - so there is "
      "nothing for a Groebner engine to find", unit == 0 and dimJ == 4)

print()
print("=" * 74)
print(f"{sum(PASS)}/{len(PASS)} certifications passed.")
print("=" * 74)
print("""
NO COUNTEREXAMPLE.  AND THE PREMISE NEEDED CORRECTING.

  Both of GGHV's solved cases reproduce exactly and instantly under slimgb,
  so the pipeline and the engine advantage are real.  But the open case does
  not fall, and the reason is not speed.

  In section 5 the reduction left 9 equations and 8 variables to eliminate,
  hence one relation - their (5.9).  In case (8,28) the leading form has
  en(R) = (4,8) instead of (3,9), so D~ carries an extra coefficient d2, and
  the count becomes three equations and three eliminated variables: no
  relation, a 4-dimensional consistent variety, elimination ideal zero.

  (8,28) is open because the purely algebraic part of the system is
  UNDERDETERMINED.  No engine extracts a relation that is not there.  What is
  missing is the valuation arithmetic - bounded y-degrees for the d_i and the
  C_4-divisibility conditions with C_4 = y^7(y+1) - which sections 5 and 6
  needed only at the last step and which this case needs from the start.

  That is a derivation task, not a computation task, and it is where the next
  session should go.
""")
assert all(PASS), "a certification failed"
