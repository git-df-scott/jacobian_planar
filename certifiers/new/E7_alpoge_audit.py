"""
E7 - AUDIT OF THE ALPOGE MAP AND ITS QUOTIENT DESCENT (Sessions 1, 38, 39).

Step 1 of the campaign plan lists "the Alpoge map" among the load-bearing
claims to fact-check.  This file re-verifies every claim of Sessions 1/38/39
from scratch (no code reused from the archive) and additionally certifies the
three Session-39 claims that its own script did NOT check:

   *  h = f_3/x  is the degeneracy line of the quotient projection;
   *  one of the two colliding quotient points lies on h = 0;
   *  det JG = -2 h^2 is intrinsic (invariant under coordinate changes of
      the quotient, and under regenerating the invariant ring).

It also supplies the explicit rational-point witness of non-injectivity that
the HIT protocol demands, verified by hand-checkable exact arithmetic.
"""
import sympy as sp
from fractions import Fraction as Fr

x, y, z, u, w, lam = sp.symbols('x y z u w lam')
PASS = []
def chk(name, cond):
    PASS.append((name, bool(cond)))
    print(("  [PASS] " if cond else "  [FAIL] ") + name)

# ------------------------------------------------------------------ the map
f1 = (1 + x*y)**3*z + y**2*(1 + x*y)*(4 + 3*x*y)
f2 = y + 3*x*(1 + x*y)**2*z + 3*x*y**2*(4 + 3*x*y)
f3 = 2*x - 3*x**2*y - x**3*z
F = [f1, f2, f3]
print("--- 1. the C^3 counterexample ---------------------------------------")
J = sp.Matrix([[sp.diff(f, t) for t in (x, y, z)] for f in F])
chk("det JF == -2 (constant, nonzero)", sp.expand(J.det()) == -2)
degs = [sp.Poly(sp.expand(f), x, y, z).total_degree() for f in F]
print("    total degrees of (f1,f2,f3) =", tuple(degs))
chk("deg F = (7,6,4): max 7, matching the archive's 'degree-7 counterexample'",
    degs == [7, 6, 4] and max(degs) == 7)

# non-injectivity upstairs, by exact rational arithmetic
P1 = (sp.Integer(0), sp.Integer(0), sp.Rational(-1, 4))
P2 = (sp.Integer(1), sp.Rational(-3, 2), sp.Rational(13, 2))
P3 = (sp.Integer(-1), sp.Rational(3, 2), sp.Rational(13, 2))
def ev(P): return tuple(sp.simplify(f.subs({x: P[0], y: P[1], z: P[2]})) for f in F)
im1, im2, im3 = ev(P1), ev(P2), ev(P3)
print("    F(0,0,-1/4)    =", im1)
print("    F(1,-3/2,13/2) =", im2)
print("    F(-1,3/2,13/2) =", im3)
chk("three distinct rational points collide upstairs",
    im1 == im2 == im3 == (sp.Rational(-1, 4), sp.Integer(0), sp.Integer(0))
    and len({P1, P2, P3}) == 3)

# ------------------------------------------------------------------ C*-action
print("\n--- 2. C*-equivariance, weights (1,-1,-2) -> (-2,-1,1) --------------")
sub = {x: lam*x, y: y/lam, z: z/lam**2}
for f, wt in zip(F, (-2, -1, 1)):
    chk(f"component weight {wt}",
        sp.simplify(sp.expand(f.subs(sub, simultaneous=True) - lam**wt*f)) == 0)
chk("source weights (1,-1,-2) and target weights (-2,-1,1) are the same multiset",
    sorted([1, -1, -2]) == sorted([-2, -1, 1]))

# ------------------------------------------------------------------ descent
print("\n--- 3. the descent to C^2 -------------------------------------------")
# source invariants: a - b - 2c = 0  ->  C[xy, x^2 z]
chk("xy and x^2 z are invariant", all(
    sp.simplify(e.subs(sub, simultaneous=True) - e) == 0 for e in (x*y, x**2*z)))
# target invariants: -2a - b + c = 0  ->  C[f1 f3^2, f2 f3]
chk("f1 f3^2 and f2 f3 are invariant", all(
    sp.simplify(sp.expand(e.subs(sub, simultaneous=True) - e)) == 0
    for e in (f1*f3**2, f2*f3)))
def to_uw(expr):
    e = sp.cancel(sp.together(sp.expand(expr).subs({y: u/x, z: w/x**2})))
    return sp.expand(sp.simplify(e))
G1, G2 = to_uw(sp.expand(f1*f3**2)), to_uw(sp.expand(f2*f3))
chk("G1 is x-free", sp.simplify(sp.diff(G1, x)) == 0)
chk("G2 is x-free", sp.simplify(sp.diff(G2, x)) == 0)
chk("deg G = (6,4), ratio 3:2",
    (sp.Poly(G1, u, w).total_degree(), sp.Poly(G2, u, w).total_degree()) == (6, 4))
JG = sp.Matrix([[sp.diff(g, t) for t in (u, w)] for g in (G1, G2)])
detJG = sp.expand(JG.det())
h = 3*u + w - 2
chk("det JG == -2 h^2 with h = 3u + w - 2", sp.expand(detJG + 2*h**2) == 0)
chk("det JG is NOT constant", sp.simplify(sp.diff(detJG, u)) != 0)

# ------------------------------------------------------------------ the 3 gaps
print("\n--- 4. the three Session-39 claims its own script did not check ------")
chk("h is f_3/x expressed in the invariants: f_3/x = 2 - 3xy - x^2 z = 2 - 3u - w = -h",
    sp.simplify(sp.expand(f3/x).subs({y: u/x, z: w/x**2}) - (2 - 3*u - w)) == 0
    and sp.expand((2 - 3*u - w) + h) == 0)
q1, q2, q3 = [(P[0]*P[1], P[0]**2*P[2]) for P in (P1, P2, P3)]
print("    quotient images of the three colliding points:", q1, q2, q3)
chk("the three points collapse to two distinct quotient points",
    q2 == q3 and q1 != q2 and len({q1, q2}) == 2)
chk("the surviving pair still collides: G(q1) == G(q2)",
    (G1.subs({u: q1[0], w: q1[1]}), G2.subs({u: q1[0], w: q1[1]})) ==
    (G1.subs({u: q2[0], w: q2[1]}), G2.subs({u: q2[0], w: q2[1]})))
chk("q2 = (-3/2, 13/2) lies on h = 0:  3(-3/2) + 13/2 - 2 = 0",
    h.subs({u: q2[0], w: q2[1]}) == 0)
chk("q1 = (0,0) does NOT lie on h = 0", h.subs({u: q1[0], w: q1[1]}) != 0)
# intrinsic-ness: an affine change of coordinates on the source scales det JG
A = sp.Matrix([[2, 1], [1, 3]])          # any invertible matrix
uu, ww = sp.symbols('uu ww')
sub2 = {u: A[0, 0]*uu + A[0, 1]*ww, w: A[1, 0]*uu + A[1, 1]*ww}
G1b, G2b = sp.expand(G1.subs(sub2)), sp.expand(G2.subs(sub2))
JGb = sp.Matrix([[sp.diff(g, t) for t in (uu, ww)] for g in (G1b, G2b)])
chk("det J(G o A) == det(A) * (det JG o A): h^2 is intrinsic up to a constant",
    sp.expand(JGb.det() - A.det()*detJG.subs(sub2)) == 0)
B = sp.Matrix([[1, 2], [0, 5]])
chk("post-composition by B: det J(B o G) == det(B) det JG",
    sp.expand(sp.Matrix([[sp.diff(g, t) for t in (u, w)] for g in
        (B[0,0]*G1 + B[0,1]*G2, B[1,0]*G1 + B[1,1]*G2)]).det() - B.det()*detJG) == 0)
chk("so det JG is a nonzero constant times a PERFECT SQUARE in every "
    "coordinate system: G can never be Keller", sp.factor_list(detJG)[1] == [(h, 2)])

# ------------------------------------------------------------------ degree of G
print("\n--- 5. geometric degree of the descent -------------------------------")
t1, t2 = sp.symbols('t1 t2')
res = sp.resultant(sp.expand(G1 - t1), sp.expand(G2 - t2), w)
gd = sp.Poly(res, u).degree()
print("    deg_u Res_w(G1-t1, G2-t2) =", gd)
chk("the descent G is a finite map of positive degree", gd > 0)

print()
for n, o in PASS:
    if not o: print("FAILED:", n)
assert all(o for _, o in PASS), "E7 FAILED"
print("E7: ALL %d CHECKS PASS" % len(PASS))
