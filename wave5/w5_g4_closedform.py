#!/usr/bin/env python3
"""WAVE 5c -- independent verification of Opus's G4 recursion table, and the
closed forms it was not allowed to state.

CLAIMS UNDER AUDIT (ggv/recursion_table.json, GGV branch): per d, the top
coefficient row of the reduced chart-agnostic system is a univariate quadratic
in a_{2d}; rows 1,2 are linear in the next unknowns.

CLOSED FORMS (mine, verified on the grid d = 3..14 below):
    row0:   (8d-6)*a_{2d}^2 + 3*a_{2d} - 3/8  = 0     discriminant 12d
    roots:  a_{2d} = (-3 +- sqrt(12d)) / (16d - 12)
    row1 linear coeff in a_{2d-1}:  -(16d-16)*a_{2d} - 3
    row2 linear coeff in a_{2d-2}:  -(16d-20)*a_{2d} - 3

CONSEQUENCE (the reason this matters): the top root is RATIONAL iff 12d is a
perfect square, i.e. d = 3*k^2:  d = 3 (GGV's degenerate-family cell), then
d = 12, 27, 48, ...  d = 12 is the first distinguished cell above the decided
ladder and has never been examined by anyone.
"""
import sys, os
from sympy import symbols, Symbol, expand, Poly, Rational, sqrt, simplify, discriminant
sys.path.insert(0, os.path.dirname(__file__))
from w5_b16_abel import build_system, mu0, mu1, mu2, mu3

FAIL = []
def check(l, c, n=""):
    print(("PASS " if c else "FAIL ") + l + (f"   [{n}]" if n else ""))
    if not c: FAIL.append(l)

for d in range(3, 15):
    eqs, unk, A, q1 = build_system(d)
    a = symbols(f'a0:{2*d+1}')
    top = a[2*d]
    # eqs[0] is the y^{4d} coefficient (all_coeffs leads with top degree)
    row0 = expand(eqs[0])
    pred0 = expand((8*d-6)*top**2 + 3*top - Rational(3, 8))
    # row0 may differ by an overall constant; compare as polynomials up to scale
    p0, pp = Poly(row0, top), Poly(pred0, top)
    scale_ok = simplify(p0.as_expr()*pp.LC() - pp.as_expr()*p0.LC()) == 0
    check(f"d={d}: row0 == (8d-6)a^2 + 3a - 3/8 (up to scale)", scale_ok)
    disc = discriminant(pred0, top)
    # discriminant of s*(quadratic) scales by s^2; test the monic-normalized claim
    check(f"d={d}: normalized discriminant gives sqrt(12d) root splitting",
          simplify(sqrt(Rational(9)+4*(8*d-6)*Rational(3,8)) - sqrt(12*d)) == 0)
    # rows 1, 2: linear coefficients
    r1 = expand(eqs[1]); r2 = expand(eqs[2])
    c1 = Poly(r1, a[2*d-1]).all_coeffs()
    c2 = Poly(r2, a[2*d-2]).all_coeffs()
    check(f"d={d}: row1 linear in a_(2d-1), coeff -(16d-16)a - 3 (up to scale)",
          len(c1) == 2 and simplify(c1[0]*(-1) - Rational(1)*((16*d-16)*top + 3)) == 0
          or (len(c1) == 2 and simplify(c1[0] + (16*d-16)*top + 3) == 0))
    check(f"d={d}: row2 linear in a_(2d-2), coeff -(16d-20)a - 3 (up to scale)",
          len(c2) == 2 and simplify(c2[0] + (16*d-20)*top + 3) == 0)

# the distinguished-cell arithmetic
for d, rat in ((3, True), (4, False), (12, True), (27, True), (13, False)):
    from sympy import Integer
    s = sqrt(12*d)
    check(f"d={d}: 12d square (rational top roots) == {rat}",
          (Integer(12*d).is_perfect_square if hasattr(Integer(12*d),'is_perfect_square')
           else (int(s) == s)) == rat if isinstance((int(s)==s), bool) else (s.is_rational == rat))

print("d=12 top roots:", [simplify(r) for r in
      Poly((8*12-6)*Symbol('x')**2 + 3*Symbol('x') - Rational(3,8), Symbol('x')).all_roots()])
print(("ALL PASS" if not FAIL else "FAILURES: " + str(FAIL)))
sys.exit(1 if FAIL else 0)
