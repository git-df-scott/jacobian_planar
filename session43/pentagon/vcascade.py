#!/usr/bin/env python3
"""THE v-CASCADE: a second, dual complete cascade.

v(x^i y^j) = 2i - j.  A v-homogeneous piece of degree d is y^-d F_d(r), r = xy^2,
since x^i y^(2i-d) = y^-d (xy^2)^i.  With

    { y^a F(r), y^b G(r) } = y^(a+b+1) ( b F' G - a F G' )   [controlled]

and a = -d, b = -e, the bracket lands on v-level d+e-1, so {P,Q} = x^2 = y^-4 r^2
becomes

    **sum_{d+e = V+1} [ d F_d G_e' - e F_d' G_e ] = delta_{V,4} r^2**

v ranges: N(P) -> [-8, 2], N(Q) -> [-12, 3].  Levels V = 4 down to -21: 25 of
them, against the w-cascade's 22.  The TOP level V=4 is (d,e)=(2,3), i.e. the
inhomogeneous lower-edge relation already decided NONEMPTY (LOWER_EDGE.md).
"""
import sympy as sp
r = sp.Symbol('r')
def P_ok(j, i): return 0 <= i <= 8 and 0 <= j <= 16 and max(0, j-8) <= i <= min(8, j//2+1)
def Q_ok(j, k):
    if not (0 <= k <= 12): return False
    lo = (k+1)//2 if k <= 2 else 2*k-3
    return lo <= j <= 12+k

F, G = {}, {}
for d in range(-8, 3):
    t = 0
    for i in range(0, 9):
        j = 2*i - d
        if j >= 0 and P_ok(j, i):
            c = sp.Integer(0) if (j,i)==(0,0) else sp.Integer(1) if (j,i)==(0,1) else sp.Symbol(f'p_{j}_{i}')
            t += c*r**i
    F[d] = sp.expand(t)
for e in range(-12, 4):
    t = 0
    for k in range(0, 13):
        j = 2*k - e
        if j >= 0 and Q_ok(j, k):
            c = sp.Integer(0) if (j,k)==(0,0) else sp.Integer(1) if (j,k)==(1,2) else sp.Symbol(f'q_{j}_{k}')
            t += c*r**k
    G[e] = sp.expand(t)

def lev(V):
    out = 0
    for d in range(-8, 3):
        e = V+1-d
        if -12 <= e <= 3:
            out += d*F[d]*sp.diff(G[e], r) - e*sp.diff(F[d], r)*G[e]
    return sp.expand(out - (r**2 if V == 4 else 0))

print("v-graded pieces (nonzero):")
for d in range(2, -9, -1):
    if F[d] != 0: print(f"  F_{d:3d}: deg {sp.degree(F[d],r)}, {sp.Poly(F[d],r).length()} terms")
print()
for e in range(3, -13, -1):
    if G[e] != 0 and e >= -1: print(f"  G_{e:3d}: deg {sp.degree(G[e],r)}, {sp.Poly(G[e],r).length()} terms")

print("\nCONTROL: top level V=4 must be the lower-edge relation 2 F_2 G_3' - 3 F_2' G_3 = r^2")
top = sp.expand(2*F[2]*sp.diff(G[3],r) - 3*sp.diff(F[2],r)*G[3] - r**2)
print("   level(4) - that expression =", sp.simplify(lev(4) - top), "-> ",
      "PASS" if sp.simplify(lev(4)-top) == 0 else "FAIL")
print("   F_2 =", F[2])
print("   G_3 =", G[3])

print("\nlevel equation counts:")
tot = 0
for V in range(4, -22, -1):
    e_ = lev(V)
    n = len([c for c in (sp.Poly(e_, r).all_coeffs() if e_ != 0 else []) if c != 0])
    tot += n
    if n: print(f"  V={V:3d}: {n:3d} equations")
print(f"  TOTAL {tot} equations across the v-cascade (w-cascade had 301)")
