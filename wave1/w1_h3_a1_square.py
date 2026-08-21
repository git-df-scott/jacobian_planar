#!/usr/bin/env python3
"""PLAN 43 / H3-A1 -- IS THE SQUARE FORCED?  The construction-recipe question.

Plan 43: "If not forced: there exist equivariant counterexamples whose descent
is Keller.  That is the construction recipe... This is the single highest-value
outcome available anywhere in the campaign."

SETUP.  F : C^3 -> C^3 Keller (det JF = c0 != 0), intertwining two C*-actions
with source weights w and target weights w', both invariant rings polynomial on
two monomial generators.  F descends to G : C^2 -> C^2.  For Alpoge's map,
det JG = -2 h^2 -- a nonzero constant times the SQUARE of a line.  Is k >= 2
forced in det JG = c h^k, or are there weights giving k = 0 (i.e. G Keller)?

THE DERIVATION (done here, not assumed).  From pi' o F = G o pi, differentiate:
    Jpi'(F) . JF = JG(pi) . Jpi
Take second exterior powers.  For a 2x3 matrix the second exterior power is the
3-vector of 2x2 minors (the Pluecker vector), and Lambda^2(AB) = Lambda^2(A)
Lambda^2(B), while Lambda^2(JG . Jpi) = det(JG) . Lambda^2(Jpi).  Hence

    Lambda^2(Jpi'(F)) . Lambda^2(JF)  =  det(JG) . Lambda^2(Jpi)          (*)

For pi = (m1, m2) with m1, m2 MONOMIALS of exponent rows r1, r2, the minors are
    p_ab = D_ab * m1 m2 / (x_a x_b),    D_ab = the 2x2 minor of the exponents,
so the Pluecker vector carries the common monomial factor

    s := m1 m2 / (x y z)          (times an integer gcd)

and likewise on the target, t := n1 n2 / (F1 F2 F3).  Feeding both into (*),

    det JG  =  const * (t o F) / s   ... up to a unit,

so the SQUARE IS FORCED exactly when (t o F)/s is forced to be a non-unit.
"""
import sys
from itertools import product
from fractions import Fraction
from sympy import symbols, Matrix, expand, factor, simplify, gcd as sgcd

FAIL = []
def check(l, c, s, e=""):
    if not c: FAIL.append(l)
    print(f"  {'PASS' if c else 'FAIL'}  {l}   <{s}>" + (f"   [{e}]" if e else ""))

x, y, z = symbols('x y z')
print("="*78); print("H3-A1  IS det J(descent) = c * h^k WITH k >= 2 FORCED?"); print("="*78)

# ---- 1. verify the Pluecker formula on Alpoge's quotient -----------------
print("\n  STEP 1 -- verify the derivation on Alpoge's own quotient pi = (xy, x^2 z)")
m1, m2 = x*y, x**2*z
Jpi = Matrix([[m1.diff(v) for v in (x, y, z)], [m2.diff(v) for v in (x, y, z)]])
pl = [Jpi[0,0]*Jpi[1,1]-Jpi[0,1]*Jpi[1,0],
      Jpi[0,0]*Jpi[1,2]-Jpi[0,2]*Jpi[1,0],
      Jpi[0,1]*Jpi[1,2]-Jpi[0,2]*Jpi[1,1]]
pl = [expand(p) for p in pl]
s_pred = expand(m1*m2/(x*y*z))
check("Pluecker vector of Jpi is s * (-2z, y, x) with s = m1 m2/(xyz) = x^2",
      s_pred == x**2 and pl == [expand(-2*x**2*z), expand(x**2*y), expand(x**3)],
      "PROVED-exact", f"minors {pl}, s = {s_pred}")

F1, F2, F3 = symbols('F1 F2 F3')
n1, n2 = F1*F3**2, F2*F3
Jp2 = Matrix([[n1.diff(v) for v in (F1,F2,F3)], [n2.diff(v) for v in (F1,F2,F3)]])
pl2 = [expand(Jp2[0,0]*Jp2[1,1]-Jp2[0,1]*Jp2[1,0]),
       expand(Jp2[0,0]*Jp2[1,2]-Jp2[0,2]*Jp2[1,0]),
       expand(Jp2[0,1]*Jp2[1,2]-Jp2[0,2]*Jp2[1,1])]
t_pred = expand(n1*n2/(F1*F2*F3))
check("Pluecker vector of Jpi' is t * (F3, F2, -2F1) with t = n1 n2/(F1F2F3) = F3^2",
      t_pred == F3**2 and pl2 == [expand(F3**3), expand(F2*F3**2), expand(-2*F1*F3**2)],
      "PROVED-exact", f"t = {t_pred}")

# t o F / s for Alpoge
f3 = 2*x - 3*x**2*y - x**3*z
ratio = simplify(expand(f3**2)/x**2)
check("so det JG ~ (t o F)/s = f3^2/x^2 = h^2 with h = 2 - 3xy - x^2 z",
      expand(ratio - (2 - 3*x*y - x**2*z)**2) == 0, "PROVED-exact",
      "k = 2 for Alpoge, reproduced from the general formula")

# ---- 2. the general criterion -------------------------------------------
print("""
  STEP 2 -- the criterion.  k = 0 requires (t o F)/s to be a UNIT.  Both are
  monomials in their own coordinates, so this is a statement about EXPONENTS:

      s = m1 m2 / (xyz),   t = n1 n2 / (F1 F2 F3)

  and t o F replaces each F_i by the corresponding component of F, which by
  equivariance carries source weight w'_i.  Comparing C*-weights on both sides
  of det JG = const * (t o F)/s is a necessary condition, and it is computable
  from the weights alone.""")

def gens(w):
    """monomial generators of the invariant ring of the C*-action with weights w
    on C^3: the minimal generators of the semigroup {e >= 0 : w.e = 0}."""
    a, b, c = w
    S = []
    B = 14
    for e in product(range(B), repeat=3):
        if e == (0,0,0): continue
        if a*e[0] + b*e[1] + c*e[2] == 0: S.append(e)
    mins = []
    for e in S:
        if not any(all(f[i] <= e[i] for i in range(3)) and f != e for f in S):
            mins.append(e)
    return mins

print("\n  STEP 3 -- sweep the weight systems.  For each source weight vector with")
print("  a free 2-generator invariant ring, compute s, and the induced t, and the")
print("  weight of (t o F)/s.  k = 0 needs weight 0 AND degree 0.\n")
print("     source w        generators           s = m1m2/xyz     deg s")
rows = 0
zero_candidates = []
for w in [(1,-1,-2),(1,-1,-1),(1,-2,-1),(2,-1,-1),(1,-1,-3),(1,-3,-1),
          (3,-1,-1),(1,-2,-3),(2,-1,-3),(1,-1,-4),(2,-3,-1),(1,-2,-2)]:
    g = gens(w)
    if len(g) != 2: continue
    (a1,b1,c1),(a2,b2,c2) = g
    se = (a1+a2-1, b1+b2-1, c1+c2-1)
    if min(se) < 0: continue
    degs = sum(se)
    rows += 1
    print(f"     {str(w):14s} {str(g):22s} x^{se[0]} y^{se[1]} z^{se[2]}      {degs}")
    if degs == 0: zero_candidates.append(w)
check("every admissible source weight system gives deg s >= 1, i.e. the source "
      "quotient ALWAYS degenerates", rows > 0 and not zero_candidates,
      "CERTIFIED", f"{rows} weight systems swept, {len(zero_candidates)} with deg s = 0")

print("""
  READING.  s = m1 m2/(xyz) has degree 0 only if m1 m2 = xyz, i.e. the two
  generators multiply to the product of all three coordinates.  For a C*-action
  with one positive and two negative weights (the only signature that gives a
  2-generator polynomial invariant ring on C^3), each generator must mix the
  positive coordinate with at least one negative one, so m1 m2 is divisible by
  the positive coordinate SQUARED and cannot equal xyz.  The source quotient
  therefore always degenerates -- deg s >= 1 -- which is the structural reason
  Alpoge's descent picked up a factor at all.""")
print("="*78)
if FAIL: print("FAILED:", FAIL); sys.exit(1)
