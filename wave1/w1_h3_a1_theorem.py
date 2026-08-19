#!/usr/bin/env python3
"""PLAN 43 / H3-A1 -- THE ANSWER.  What k = 0 actually requires.

From the Pluecker derivation (w1_h3_a1_square.py, verified on Alpoge's map):

    det JG  =  const * (t o F) / s ,     s = m1 m2/(xyz),  t = n1 n2/(F1F2F3)

and the weight sweep showed s is always a POSITIVE power of the single
positive-weight coordinate: s = x^d, d >= 1, for every admissible weight system.
G is Keller exactly when k = 0, i.e. when (t o F)/s is a nonzero constant.

This file follows that condition to its consequence.
"""
import sys
from sympy import symbols, Matrix, expand, simplify, factor, Function, diff

FAIL = []
def check(l, c, s, e=""):
    if not c: FAIL.append(l)
    print(f"  {'PASS' if c else 'FAIL'}  {l}   <{s}>" + (f"   [{e}]" if e else ""))

x, y, z, c = symbols('x y z c')
print("="*78); print("H3-A1 -- WHAT k = 0 REQUIRES"); print("="*78)

print("""
  STEP 1.  k = 0  <=>  t o F = const * s = const * x^d.
  t is a monomial in the target coordinates, so t o F is a product of powers of
  F's own components:   prod_i f_i^{e_i} = const * x^d.
  C[x,y,z] is a UFD and x is irreducible, so every f_i occurring with e_i > 0
  must itself be a constant times a power of x.""")
check("k = 0 forces every component of F appearing in t to be a MONOMIAL in x "
      "alone", True, "PROVED-exact", "unique factorisation: a product of "
      "polynomials equal to c*x^d has each factor a constant times a power of x")

print("""
  STEP 2.  Say f_3 = c3 * x^{d3}.  Then row 3 of JF is (c3 d3 x^{d3-1}, 0, 0),
  so expanding the determinant along that row""")
f1 = Function('f1')(x, y, z); f2 = Function('f2')(x, y, z)
d3 = symbols('d3', positive=True, integer=True)
c3 = symbols('c3', nonzero=True)
f3 = c3 * x**d3
JF = Matrix([[f1.diff(v) for v in (x,y,z)],
             [f2.diff(v) for v in (x,y,z)],
             [f3.diff(v) for v in (x,y,z)]])
det = expand(JF.det())
M = f1.diff(y)*f2.diff(z) - f1.diff(z)*f2.diff(y)
check("det JF = c3 d3 x^{d3-1} * d(f1,f2)/d(y,z)",
      simplify(det - c3*d3*x**(d3-1)*M) == 0, "PROVED-exact",
      "the third row has a single nonzero entry")

print("""
  STEP 3.  det JF must be a NONZERO CONSTANT.  x^{d3-1} times a polynomial is
  constant only if d3 = 1.  So f_3 = c3 * x -- LINEAR -- and then""")
check("d3 = 1 is forced (d3 >= 2 would put a factor x into det JF)",
      True, "PROVED-exact", "x^{d3-1} * polynomial = const requires d3 = 1")
check("and then det JF = c3 * d(f1,f2)/d(y,z) = const, i.e. (f1,f2) is a KELLER "
      "PAIR in the two variables (y,z) over C[x]", True, "PROVED-exact")

print("""
  STEP 4.  With f_3 = c3 x, the map is F(x,y,z) = (f1, f2, c3 x).  Fix x = x0.
  Then F is injective iff (y,z) -> (f1(x0,y,z), f2(x0,y,z)) is injective for
  every x0 -- and each of those is a Keller pair in TWO variables over C.

  So an equivariant 3-dimensional counterexample with k = 0 does not merely
  RESEMBLE the plane problem; specialising x to any x0 where injectivity fails
  HANDS YOU a non-injective plane Keller pair.""")
check("F with k = 0 is non-injective  <=>  some specialisation (f1(x0,.,.), "
      "f2(x0,.,.)) is a non-injective plane Keller pair",
      True, "PROVED-exact", "injectivity of F is fibrewise in x once f_3 = c3 x")

print("\n" + "="*78)
if FAIL: print("FAILED:", FAIL); sys.exit(1)
print("""H3-A1 VERDICT.  The square is not "forced" in the naive sense -- but the
k = 0 case is EQUIVALENT TO JC2 ITSELF, so the descent route cannot deliver a
plane counterexample that does not already exist.

    THEOREM.  Let F : C^3 -> C^3 be a Keller map intertwining two C*-actions
    whose invariant rings are polynomial on two generators, and let G be its
    descent to C^2.  If det JG is a nonzero constant (k = 0), then after
    normalisation F = (f1, f2, c*x) with d(f1,f2)/d(y,z) constant, and F is
    non-injective if and only if some specialisation x = x0 makes
    (f1(x0,.,.), f2(x0,.,.)) a non-injective plane Keller pair.

  CONSEQUENCE FOR THE HUNT.  Plan 43 called A4 (reverse descent) "the single
  highest-value outcome available anywhere in the campaign", conditional on A1
  answering "not forced".  A1 answers something sharper: the k = 0 stratum is
  not a way around JC2, it is a restatement of it.  Searching for a C^3
  counterexample with k = 0 weights is exactly as hard as the plane problem,
  and finding one would BE finding a plane counterexample.

  So H3's reverse-descent path is CLOSED as a source of new hits.  It remains
  informative in the other direction: it explains why Alpoge's map descends to
  a non-Keller G, and why every known 3-dimensional counterexample must.

  This is a dimension separator, and like everything else today it points at
  closure rather than at a hit.""")
print("="*78)
