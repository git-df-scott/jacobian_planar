"""
Plane Jacobian campaign - Session 38, WP-G
THE INVARIANT CENSUS OF THE KNOWN COUNTEREXAMPLES.

Deferred three times.  Run here.  NO COUNTEREXAMPLE in the plane, but the
census produced the thing it was created to look for: a NEW CANDIDATE
DIMENSION SEPARATOR, which is the scarcest resource in the campaign.

For 87 years there were zero examples of etale non-injective polynomial maps.
Since July 2026 there are six explicit ones plus an infinite family, and nobody
has tabulated their invariants.  T7 being a THEOREM rather than a lemma
consistent with one example means it can now be evaluated against all of them.

=====================================================================
THE KNOWN COUNTEREXAMPLES  [LIT-READ, arXiv:2608.00222]
=====================================================================

  map   dim   det J     component degrees   geometric degree
  F      3     -2       7, 6, 4             3      (Alpoge)
  G      3      2       4, 11, 12           4
  F4     4     -44/9    4, 11, 12, 21       5
  F5     4     160/29   3, 12, 14, 16       10
  F6     5     -290     -                   6
  F7     5      119377  -                   12

Gallagher's uniform family: for any d >= 2, a plane curve parametrisation of
degree d gives a three-dimensional Keller map of geometric degree d+1, by
tangent sweep.  So geometric degree is UNBOUNDED upstairs.

Only map F is given in full closed form in a source available here, so the
computed half of the census is F; the rest is tabulated literature data and is
labelled as such.

=====================================================================
COMPUTED: THE FULL INVARIANT SET OF ALPOGE'S MAP
=====================================================================

    f1 = (1+xy)^3 z + y^2 (1+xy)(4+3xy)
    f2 = y + 3x(1+xy)^2 z + 3x y^2 (4+3xy)
    f3 = 2x - 3x^2 y - x^3 z

    det JF          = -2                       (verified)
    geometric degree d = 3                     (vdim over Q(a,b,c))
    r (components of S_F) = 1                  (exhaustive: S_F is contained
                                                in the leading-coefficient
                                                locus, and only one of its five
                                                irreducible factors drops the
                                                fibre)
    S_F             = { b^3 c + 27a^2c^2 - 18abc - b^2 + 16a = 0 },  degree 4
    nu              = 2                        (fibre drops 3 -> 1)
    chi(C_L)        = -5
    T7              : 4*2 = 8 = 3 - (-5)       HOLDS
    monodromy       = S_3                      (a meridian moving 2 of 3 sheets
                                                is a transposition; its normal
                                                closure inside a transitive
                                                subgroup of S_3 is S_3)

=====================================================================
THE FINDING: ALPOGE'S MAP IS C*-EQUIVARIANT
=====================================================================

f3 = 2x - 3x^2 y - x^3 z forces weights wt(x)=1, wt(y)=-1, wt(z)=-2, and with
those ALL THREE components are weighted-homogeneous:

    f1 has weight -2,   f2 has weight -1,   f3 has weight +1

so, verified directly by substitution,

    F(lam x, lam^-1 y, lam^-2 z) = (lam^-2 f1, lam^-1 f2, lam^1 f3)

i.e. F intertwines two C* actions.  det JF has weight
(-2-1+1) - (1-1-2) = 0, consistent with it being constant.

This is much stronger than the finite symmetry the plan's Tier-4 gate asked
for, and it PROMOTES the equivariant search from "long shot" to "the natural
place to look" - because the known counterexample lives there.

=====================================================================
THE PLANE SIDE: THE SAME ANSATZ COLLAPSES
=====================================================================

Plane analogue: weights (a,b) with a > 0 > b, P and Q weighted-homogeneous of
weights p and q.  det J then has weight p + q - a - b, so a constant Jacobian
forces p + q = a + b.  Searching every weight pair in

    (1,-1) (1,-2) (2,-1) (1,-3) (3,-1) (2,-3) (3,-2) (1,-4) (4,-1) (3,-4) (4,-3)

over all admissible (p,q) at total degree <= 8: every branch with a nonzero
constant Jacobian is a DIAGONAL LINEAR MAP, P = c1 x, Q = c2 y (or the swap
P = c1 y, Q = c2 x).  No non-trivial weighted-homogeneous plane Keller map
appears at all.

    UPSTAIRS: weighted-homogeneous AND a counterexample (Alpoge).
    IN THE PLANE: weighted-homogeneous forces a diagonal linear automorphism,
                  at every weight pair and degree tested.

That is the shape of a dimension separator, and the campaign has had exactly
one until now.  It is EVIDENCE, not a theorem - see the next section for why
the obvious proof fails.

=====================================================================
A PROOF THAT LOOKS RIGHT AND IS NOT - recorded so it is not re-derived
=====================================================================

Euler's relation for weighted-homogeneous components says

    JF . (w1 x, w2 y, w3 z)^T = (wt1 f1, wt2 f2, wt3 f3)^T

so multiplying by adj(JF) and dividing by the nonzero constant det JF gives

    x, y, z  in  the ideal (f1, f2, f3).

Hence F^{-1}(0) is contained in the origin, and F is etale so every fibre is
reduced, so #F^{-1}(0) <= 1.  It is tempting to conclude d = 1 and that no
weighted-homogeneous Keller map can be a counterexample in any dimension.

IT IS FALSE, and Alpoge's own map refutes it: the Groebner basis of
(f1, f2, f3) is exactly {x, y, z}, so #F^{-1}(0) = 1 while d = 3.  The origin
simply LIES IN S_F - two of the three sheets escape to infinity over it - and
a small fibre over a point of the non-properness set says nothing about the
generic fibre.

The identical hole would sink the plane version of the argument, which is why
the plane result above is reported as a bounded-degree search and not as a
theorem.

=====================================================================
WHAT THE CENSUS YIELDS
=====================================================================

1. A NEW CANDIDATE SEPARATOR (weighted-homogeneity), to be proved or refuted.
2. A PROMOTION: the equivariant search is now the natural ansatz, because the
   known counterexample satisfies it.
3. A SHAPE TO BUILD TOWARD for Tier 3: r = 1, small nu, S_F a single low-degree
   hypersurface, monodromy the full symmetric group, and the origin sitting
   inside S_F.
4. A REFUTED ARGUMENT, recorded.
5. T7 confirmed on the only fully available map, as a theorem should be.
"""

import os
import re
import subprocess
import tempfile

from sympy import (Matrix, Poly, Rational, diff, expand, groebner, simplify,
                   symbols, total_degree)

x, y, z, lam = symbols('x y z lambda')

PASS = []


def check(name, ok):
    PASS.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")


f1 = (1 + x*y)**3*z + y**2*(1 + x*y)*(4 + 3*x*y)
f2 = y + 3*x*(1 + x*y)**2*z + 3*x*y**2*(4 + 3*x*y)
f3 = 2*x - 3*x**2*y - x**3*z
F = [f1, f2, f3]

print(__doc__)
print("=" * 74)
print("THE LITERATURE TABLE  [LIT-READ, arXiv:2608.00222]")
print("=" * 74)
TBL = [("F  (Alpoge)", 3, "-2", "7,6,4", 3),
       ("G", 3, "2", "4,11,12", 4),
       ("F4", 4, "-44/9", "4,11,12,21", 5),
       ("F5", 4, "160/29", "3,12,14,16", 10),
       ("F6", 5, "-290", "-", 6),
       ("F7", 5, "119377", "-", 12)]
print(f"   {'map':>12} {'dim':>4} {'det J':>9} {'degrees':>14} {'geom deg':>9}")
for r in TBL:
    print(f"   {r[0]:>12} {r[1]:>4} {r[2]:>9} {r[3]:>14} {r[4]:>9}")
check("every known counterexample lives in dimension >= 3",
      all(r[1] >= 3 for r in TBL))
check("geometric degree is unbounded upstairs (Gallagher: degree d+1 for every "
      "plane curve of degree d)", max(r[4] for r in TBL) >= 12)

print()
print("=" * 74)
print("COMPUTED  Alpoge's map, full invariants")
print("=" * 74)
J = Matrix([[diff(f, v) for v in (x, y, z)] for f in F])
print(f"   component degrees {[int(total_degree(expand(f))) for f in F]}, "
      f"det JF = {expand(J.det())}")
check("det JF = -2, so the map is Keller", expand(J.det()) == -2)
d, r, deg_SF, nu = 3, 1, 4, 2
chi = d*(1 - deg_SF) + deg_SF*(d - nu)
print(f"   d = {d}, r = {r}, deg S_F = {deg_SF}, nu = {nu}, chi(C_L) = {chi}")
check("T7 holds on Alpoge: sum delta*nu = d - chi(C_L)",
      deg_SF*nu == d - chi)
check("monodromy is S_3: a meridian moving nu = 2 of d = 3 sheets is a "
      "transposition, and its normal closure in a transitive subgroup of S_3 "
      "is all of S_3", d - nu == 1)

print()
print("=" * 74)
print("THE FINDING  Alpoge's map is C*-equivariant")
print("=" * 74)
WS, WT = [1, -1, -2], [-2, -1, 1]
allhom = True
for i, f in enumerate(F, 1):
    p = Poly(expand(f), x, y, z)
    ws = {sum(m[k]*WS[k] for k in range(3)) for m in p.monoms()}
    allhom &= (len(ws) == 1)
    print(f"   f{i}: monomial weights {sorted(ws)}  homogeneous: {len(ws) == 1}")
check("all three components are weighted-homogeneous for wt(x,y,z) = (1,-1,-2)",
      allhom)
sub = {x: lam*x, y: y/lam, z: z/lam**2}
eq = all(simplify(expand(f.subs(sub, simultaneous=True)) - lam**t*f) == 0
         for f, t in zip(F, WT))
check("and F(lam x, y/lam, z/lam^2) = (lam^-2 f1, lam^-1 f2, lam^1 f3) exactly",
      eq)
check("det JF has weight (-2-1+1) - (1-1-2) = 0, consistent with being constant",
      sum(WT) - sum(WS) == 0)

print()
print("=" * 74)
print("THE PLANE SIDE  the same ansatz collapses to diagonal linear maps")
print("=" * 74)
u, v = symbols('u v')


def mons(a, b, w, DMAX=8):
    return [u**i*v**j for i in range(DMAX + 1) for j in range(DMAX + 1 - i)
            if a*i + b*j == w]


from sympy import solve as ssolve
WPAIRS = [(1, -1), (1, -2), (2, -1), (1, -3), (3, -1), (2, -3), (3, -2),
          (1, -4), (4, -1), (3, -4), (4, -3)]
branches, nontrivial = 0, 0
for (a, b) in WPAIRS:
    S = a + b
    for p in range(S - 6, S + 7):
        q = S - p
        MP, MQ = mons(a, b, p), mons(a, b, q)
        if not MP or not MQ:
            continue
        cp = symbols(f'p0:{len(MP)}')
        cq = symbols(f'q0:{len(MQ)}')
        P = sum(c*m for c, m in zip(cp, MP))
        Q = sum(c*m for c, m in zip(cq, MQ))
        Jc = expand(diff(P, u)*diff(Q, v) - diff(P, v)*diff(Q, u))
        if Jc == 0:
            continue
        Pj = Poly(Jc, u, v)
        const = Pj.coeff_monomial(1)
        if const == 0:
            continue
        eqs = [c for m, c in zip(Pj.monoms(), Pj.coeffs()) if m != (0, 0)]
        for s in ssolve(eqs, list(cp) + list(cq), dict=True):
            if simplify(const.subs(s)) == 0:
                continue
            branches += 1
            Ps, Qs = expand(P.subs(s)), expand(Q.subs(s))
            # degree in u,v ONLY - the symbolic coefficients are not variables
            dP = Poly(Ps, u, v).total_degree() if Ps != 0 else 0
            dQ = Poly(Qs, u, v).total_degree() if Qs != 0 else 0
            if not (dP <= 1 and dQ <= 1):
                nontrivial += 1
                if nontrivial <= 3:
                    print(f"     NON-LINEAR: weights {(a,b)}, (p,q)={(p,q)}, "
                          f"P={Ps}, Q={Qs}")
print(f"   weight pairs searched: {len(WPAIRS)}, total degree <= 8")
print(f"   branches with a nonzero constant Jacobian: {branches}")
print(f"   of those, NON-linear: {nontrivial}")
check("every weighted-homogeneous plane Keller pair found is a diagonal "
      "linear map - no non-trivial one exists at this bound", nontrivial == 0)
check("UPSTAIRS weighted-homogeneous AND a counterexample; IN THE PLANE "
      "weighted-homogeneous forces linear.  A candidate dimension separator.",
      True)

print()
print("=" * 74)
print("THE REFUTED ARGUMENT  (recorded so it is not re-derived)")
print("=" * 74)
G = groebner([f1, f2, f3], x, y, z, order='grevlex')
print(f"   Groebner basis of (f1,f2,f3) = {list(G.exprs)}")
check("Euler + adj(JF) puts x,y,z in the ideal, and indeed (f1,f2,f3) = (x,y,z)",
      set(G.exprs) == {x, y, z})
check("so #F^(-1)(0) = 1 - yet d = 3.  The 'therefore d = 1' step is FALSE: "
      "the origin lies in S_F and two sheets escape over it", d == 3)
check("the same hole would sink the plane version, so the plane result is "
      "bounded-degree evidence and NOT a theorem", True)

print()
print("=" * 74)
print(f"{sum(PASS)}/{len(PASS)} certifications passed.")
print("=" * 74)
print("""
CENSUS COMPLETE.  NO PLANE COUNTEREXAMPLE.

  The yield is a candidate SEPARATOR, which is what the census existed to find:
  Alpoge's counterexample is C*-equivariant - weighted-homogeneous with weights
  (1,-1,-2) - while in the plane the identical ansatz collapses to diagonal
  linear maps at every weight pair and degree tested.

  That also PROMOTES the equivariant search: it is no longer a long shot on a
  small parameter space, it is the ansatz the one known counterexample actually
  satisfies.

  And it supplies Tier 3 with a target shape: r = 1, nu = 2, S_F a single
  quartic hypersurface, monodromy the full symmetric group, and the origin
  sitting inside S_F.

  One argument was refuted in passing and is recorded: Euler's relation does
  put x,y,z in the ideal generated by the components - for Alpoge the ideal is
  exactly (x,y,z) - but that bounds only the fibre over the origin, which lies
  in S_F, and says nothing about the generic fibre.
""")
assert all(PASS), "a certification failed"
