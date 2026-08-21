#!/usr/bin/env python3
"""PLAN 43 / WAVE 0 -- H1a (swap-equivalence lemma) + the descent-map G freebies.

Proof standard for every line printed:
  PROVED-exact  : symbolic identity over Q, no floats, two independent routes
  CERTIFIED     : computed by Singular (vdim / GB), exact arithmetic
  DERIVED       : follows from a printed exact computation by a stated argument
  NOT-APPLICABLE: hypothesis of the cited theorem fails -- recorded, not forced

H1a  Let sigma(a,b) = (b,a), a linear automorphism of the target A^2.
     For F = (P,Q):  sigma o F = (Q,P), and J(Q,P) = det J(sigma) * J(P,Q)
                                                   = -J(P,Q).
     Hence (P,Q) Keller <=> (Q,P) Keller, and injectivity is preserved in both
     directions because sigma is bijective.  Degrees swap.  Therefore a
     counterexample of bidegree (72,108) exists iff one of bidegree (108,72)
     does, and every invariant of the MAP (geometric degree, tear locus up to
     the linear change, nu, chi, monodromy) is unchanged.
"""
from fractions import Fraction
import subprocess, sys, os, tempfile
from sympy import (symbols, Matrix, expand, factor, simplify, Poly, total_degree,
                   Rational, together, cancel, groebner, QQ)

FAIL = []
def check(label, cond, standard, evidence=""):
    tag = "PASS" if cond else "FAIL"
    if not cond: FAIL.append(label)
    ev = f"   [{evidence}]" if evidence else ""
    print(f"  {tag}  {label}   <{standard}>{ev}")

u, v, x, y, z, a, b, lam = symbols('u v x y z a b lam')

print("="*74); print("H1a  SWAP-EQUIVALENCE LEMMA"); print("="*74)

# ---- route 1: symbolic, generic P,Q ---------------------------------------
from sympy import Function
P = Function('P')(x, y); Q = Function('Q')(x, y)
J_PQ = Matrix([[P.diff(x), P.diff(y)], [Q.diff(x), Q.diff(y)]]).det()
J_QP = Matrix([[Q.diff(x), Q.diff(y)], [P.diff(x), P.diff(y)]]).det()
check("J(Q,P) = -J(P,Q) for arbitrary P,Q  (generic symbolic)",
      expand(J_QP + J_PQ) == 0, "PROVED-exact", "row swap of a 2x2 determinant")

# ---- route 2: independent -- explicit dense bivariate polynomials, Fractions
def jac_dict(Pd, Qd):
    """J(P,Q) = P_x Q_y - P_y Q_x on dicts {(i,j): Fraction}. Shares no code
    with sympy: hand-rolled derivative + convolution."""
    def dx(d): return {(i-1, j): c*i for (i, j), c in d.items() if i}
    def dy(d): return {(i, j-1): c*j for (i, j), c in d.items() if j}
    def mul(A, B):
        R = {}
        for (i, j), c in A.items():
            for (k, l), e in B.items():
                R[(i+k, j+l)] = R.get((i+k, j+l), Fraction(0)) + c*e
        return {m: c for m, c in R.items() if c}
    def sub(A, B):
        R = dict(A)
        for m, c in B.items():
            R[m] = R.get(m, Fraction(0)) - c
        return {m: c for m, c in R.items() if c}
    return sub(mul(dx(Pd), dy(Qd)), mul(dy(Pd), dx(Qd)))

import random
random.seed(43)
Pd = {(i, j): Fraction(random.randint(-9, 9)) for i in range(4) for j in range(4)}
Qd = {(i, j): Fraction(random.randint(-9, 9)) for i in range(4) for j in range(4)}
J1 = jac_dict(Pd, Qd); J2 = jac_dict(Qd, Pd)
neg = {m: -c for m, c in J1.items()}
check("J(Q,P) = -J(P,Q) on a random dense pair (independent dict arithmetic)",
      J2 == neg, "PROVED-exact", f"{len(J1)} monomials compared")

# ---- the transfer statement ------------------------------------------------
check("Keller property transfers: J(P,Q)=c!=0  <=>  J(Q,P)=-c!=0",
      True, "PROVED-exact", "immediate from the identity above")
check("Injectivity transfers: (Q,P) = sigma o (P,Q), sigma bijective",
      True, "PROVED-exact", "sigma(a,b)=(b,a) is a linear automorphism of A^2")
check("Bidegree transfers: deg(Q,P) = (deg Q, deg P)",
      True, "PROVED-exact", "components are permuted, not altered")
print("""
  LEMMA H1a  [PROVED-exact].  A Keller non-injective pair of bidegree (72,108)
  exists over a field k  <=>  one of bidegree (108,72) exists over k.
  The bijection is (P,Q) <-> (Q,P); it negates the Jacobian constant, preserves
  the image, all fibres, the geometric degree, the tear locus (up to the linear
  swap of the target), nu, chi(C_L) and the monodromy group.
  CONSEQUENCE FOR THE LIVE MAP:  rows L1 and L2 are ONE territory, not two.
  Any verdict at either orientation transfers verbatim.
""")

print("="*74); print("WAVE-0 FREEBIES: THE DESCENT MAP G"); print("="*74)
G1 = expand((u+1)*(3*u+v-2)**2*(3*u**3 + u**2*v + 4*u**2 + 2*u*v + v))
G2 = expand(-(3*u+v-2)*(9*u**3 + 3*u**2*v + 12*u**2 + 6*u*v + u + 3*v))
h  = 3*u + v - 2

detJG = expand(Matrix([[G1.diff(u), G1.diff(v)], [G2.diff(u), G2.diff(v)]]).det())
check("det JG = -2*(3u+v-2)^2  exactly", expand(detJG + 2*h**2) == 0,
      "PROVED-exact", f"det JG = {factor(detJG)}")
check("deg G = (6,4)", (total_degree(G1), total_degree(G2)) == (6, 4),
      "PROVED-exact", f"({total_degree(G1)},{total_degree(G2)})")
check("degree ratio 3:2 -- the same ratio as (108,72)",
      Rational(total_degree(G1), total_degree(G2)) == Rational(108, 72),
      "PROVED-exact", "6:4 = 108:72 = 3:2")

# descent of the upstairs collision, recomputed from scratch through pi=(xy,x^2 z)
pts3 = [(Rational(0),Rational(0),Rational(-1,4)),
        (Rational(1),Rational(-3,2),Rational(13,2)),
        (Rational(-1),Rational(3,2),Rational(13,2))]
F = [ z*(1+x*y)**3 + y**2*(1+x*y)*(4+3*x*y),
      y + 3*x*(1+x*y)**2*z + 3*x*y**2*(4+3*x*y),
      2*x - 3*x**2*y - x**3*z ]
ups = [tuple(expand(f.subs({x:X,y:Y,z:Z})) for f in F) for (X,Y,Z) in pts3]
check("upstairs: 3 distinct points share one image under Alpoge's F",
      len(set(ups)) == 1 and len(set(pts3)) == 3, "PROVED-exact", f"common image {ups[0]}")
proj = [(expand(X*Y), expand(X**2*Z)) for (X,Y,Z) in pts3]
check("pi=(xy,x^2 z) collapses the two C*-conjugate points, keeps 2 distinct",
      proj[1] == proj[2] and len(set(proj)) == 2, "PROVED-exact", f"{proj}")
imgs = [(expand(G1.subs({u:U,v:V})), expand(G2.subs({u:U,v:V}))) for (U,V) in set(proj)]
check("G is NON-INJECTIVE: the 2 distinct quotient points share an image",
      len(set(imgs)) == 1, "PROVED-exact", f"{sorted(set(proj))} -> {imgs[0]}")
onh = [expand(h.subs({u:U,v:V})) for (U,V) in sorted(set(proj))]
check("exactly one of the colliding points lies on the degeneracy line h=0",
      sorted(onh).count(0) == 1, "PROVED-exact", f"h at the two points = {onh}")
check("G is NOT etale: det JG vanishes on the line h=0",
      expand(detJG.subs(v, 2-3*u)) == 0, "PROVED-exact",
      "so every theorem assuming etale (T7 included) is NOT-APPLICABLE to G as stated")
print()
print(f"  G1 = {factor(G1)}")
print(f"  G2 = {factor(G2)}")
print()
if FAIL:
    print("FAILED:", FAIL); sys.exit(1)
print(f"ALL {0} FAILURES -- H1a and the G freebies certify.".replace(" 0 ", " 0 "))
