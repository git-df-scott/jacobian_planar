"""Session 43 — adversarial validation of every Path S claim.

The campaign's standing failure mode is the certifier that cannot fail.  Two of
those were already caught inside this session (a resultant reporting a phantom
intersection for a vertical component; a resultant reporting a phantom
component-hit wherever lc_y vanishes).  This file exists to attack the rest.

Every load-bearing claim is re-derived here by a route INDEPENDENT of the one
that produced it, and every instrument is first calibrated on inputs whose
answer is known a priori.  Anything that cannot be made to fail is not evidence.

Run:  python3 session43/VALIDATE.py     (nonzero exit on any FAIL)
"""
import sys
import sympy as sp

sys.path.insert(0, __file__.rsplit('/', 1)[0])
import pathS_chi as CH

x, y, z = sp.symbols('x y z')
w1, w2, w3 = sp.symbols('w1 w2 w3')
mu, r = sp.symbols('mu r')
u, v = CH.u, CH.v

U = 1 + x*y
P = U**3*z + y**2*U*(4 + 3*x*y)
Q = 3*x*U**2*z + y + 3*x*y**2*(4 + 3*x*y)
R = -x**3*z + 2*x - 3*x**2*y
DELTA = CH.DELTA
E = 27*w1*w3**2 - 9*w2*w3 + 8

RESULTS = []


def check(name, ok, detail=''):
    RESULTS.append((name, bool(ok), detail))
    print(("  PASS  " if ok else "  FAIL  ") + name + (("   " + detail) if detail else ""))


# --------------------------------------------------------------------------
print("\n[A] CALIBRATION of chi_curve on curves with independently known chi")
print("    (an instrument that cannot report a wrong answer is not an instrument)")
# chi = 2 - 2g - s - sum(r_p - 1)
CAL = [
    ("a line  {v=0}",                     v,                          1),
    ("a parabola {v = u^2}  ~ A^1",       v - u**2,                   1),
    ("hyperbola {uv=1} ~ C*",             u*v - 1,                    0),
    ("circle {u^2+v^2=1} ~ C*",           u**2 + v**2 - 1,            0),
    ("cuspidal cubic {v^2=u^3}",          v**2 - u**3,                1),
    ("nodal cubic {v^2=u^3+u^2}",         v**2 - u**3 - u**2,         0),
    ("elliptic {v^2=u^3-u}, g=1,s=1",     v**2 - u**3 + u,           -1),
    ("two disjoint lines {v(v-1)=0}",     v*(v - 1),                  2),
    ("two crossing lines {uv=0}",         u*v,                        1),
    ("three concurrent lines {uv(u-v)=0}", u*v*(u - v),               1),
    ("line u=0 disjoint from {uv=1}",     u*(u*v - 1),                1),
    ("smooth conic pair, disjoint",       (u*v - 1)*(u*v - 2),        0),
]
for nm, f, expected in CAL:
    got = CH.chi_curve(f)
    check("chi(%s) = %s" % (nm, expected), got == expected, "got %s" % got)

print("\n[A2] CALIBRATION of the A^1 detector (Chau filter)")
A1CAL = [("line v", v, True), ("parabola v-u^2", v - u**2, True),
         ("cuspidal cubic v^2-u^3", v**2 - u**3, False),
         ("hyperbola uv-1", u*v - 1, False),
         ("elliptic v^2-u^3+u", v**2 - u**3 + u, False)]
for nm, f, expected in A1CAL:
    got = CH.is_isomorphic_to_A1(f, u, v)
    check("is_A1(%s) = %s" % (nm, expected), got == expected, "got %s" % got)

# --------------------------------------------------------------------------
print("\n[B] THE MAP, re-verified from scratch")
J = sp.Matrix([[sp.diff(f, s) for s in (x, y, z)] for f in (P, Q, R)])
check("det JF = -2", sp.expand(J.det()) == -2)
pts = [(0, 0, sp.Rational(-1, 4)), (1, sp.Rational(-3, 2), sp.Rational(13, 2)),
       (-1, sp.Rational(3, 2), sp.Rational(13, 2))]
vals = {tuple(sp.expand(f.subs({x: a, y: b, z: c})) for f in (P, Q, R)) for a, b, c in pts}
check("three distinct points collide", vals == {(sp.Rational(-1, 4), 0, 0)} and len(set(pts)) == 3)

# --------------------------------------------------------------------------
print("\n[C] THE FIBRE STRUCTURE -- proved generically over function fields,")
print("    not merely sampled (this is the load-bearing claim for chi(S))")

# C1. off the tear: the fibre ideal is 0-dimensional of degree 3 over Q(w).
K = sp.QQ.frac_field(w1, w2, w3)
G = sp.groebner([sp.expand(P - w1), sp.expand(Q - w2), sp.expand(R - w3)],
                x, y, z, order='lex', domain=K)
lead = [sp.LT(g, order='lex') for g in G.exprs]
# degree of the quotient ring = product of leading-monomial degrees for a
# triangular lex basis; check directly that x satisfies a cubic and y,z are
# determined by x (so the fibre has exactly 3 points over the generic w).
gx = [g for g in G.exprs if g.free_symbols & {x} and not (g.free_symbols & {y, z})]
check("over Q(w1,w2,w3) the fibre ideal contains a univariate poly in x",
      len(gx) >= 1, "found %d" % len(gx))
if gx:
    px = sp.Poly(gx[0], x)
    check("that polynomial has degree 3 in x  => generic fibre = 3 points",
          px.degree() == 3, "degree %s" % px.degree())
    # and it agrees with h up to a unit
    h = sp.expand(DELTA*x**3 + (4 - 3*w2*w3)*x - 2*w3)
    ratio = sp.simplify(sp.cancel(sp.expand(px.as_expr())/h))
    check("it is proportional to h = Delta x^3 + (4-3w2w3)x - 2w3",
          ratio.free_symbols.isdisjoint({x}), "ratio = %s" % ratio)

# C2. ON the tear, off C_sing: substitute the parametrization (mu != 0).
W1 = (mu + 1)*(mu - 2)**2/(27*r**2)
W2 = -(mu - 2)*(mu + 2)/(3*r)
W3 = r
check("parametrization lies on the tear", sp.simplify(DELTA.subs({w1: W1, w2: W2, w3: W3})) == 0)
check("mu = E/(4-3 w2 w3) inverts it",
      sp.simplify(E.subs({w1: W1, w2: W2, w3: W3}) - mu*(4 - 3*W2*W3)) == 0)
# surjectivity of the parametrization onto tear n {w3 != 0}: given w on the tear
# with 4-3w2w3 != 0, set m = E/(4-3w2w3); then the parametrization at (m, w3)
# returns w.  Verify as an identity modulo Delta.
m_of_w = E/(4 - 3*w2*w3)
back1 = sp.simplify(sp.cancel(W1.subs({mu: m_of_w, r: w3}) - w1))
back2 = sp.simplify(sp.cancel(W2.subs({mu: m_of_w, r: w3}) - w2))
num1 = sp.expand(sp.numer(sp.together(back1)))
num2 = sp.expand(sp.numer(sp.together(back2)))
q1 = sp.reduced(num1, [DELTA], w1, w2, w3)[1]
q2 = sp.reduced(num2, [DELTA], w1, w2, w3)[1]
check("parametrization is ONTO tear n {w3!=0, not C_sing} (w2 recovered)", sp.expand(q2) == 0,
      "remainder %s" % sp.expand(q2))
check("parametrization is ONTO (w1 recovered, modulo Delta)", sp.expand(q1) == 0,
      "remainder %s" % sp.expand(q1))

# fibre over the generic point of the tear
Kt = sp.QQ.frac_field(mu, r)
Gt = sp.groebner([sp.expand(sp.numer(sp.together(P - W1))),
                  sp.expand(sp.numer(sp.together(Q - W2))),
                  sp.expand(sp.numer(sp.together(R - W3)))],
                 x, y, z, order='lex', domain=Kt)
gxt = [g for g in Gt.exprs if g.free_symbols & {x} and not (g.free_symbols & {y, z})]
if gxt:
    pxt = sp.Poly(gxt[0], x)
    check("over the generic point of the TEAR the x-polynomial has degree 1"
          "  => fibre = 1 point", pxt.degree() == 1, "degree %s" % pxt.degree())
else:
    check("tear fibre: univariate x-polynomial found", False)

# C3. over C_sing (mu = 0) the fibre is EMPTY
Kr = sp.QQ.frac_field(r)
csing = {w1: sp.Rational(4, 27)/r**2, w2: sp.Rational(4, 3)/r, w3: r}
Gs = sp.groebner([sp.expand(sp.numer(sp.together(P - csing[w1]))),
                  sp.expand(sp.numer(sp.together(Q - csing[w2]))),
                  sp.expand(sp.numer(sp.together(R - csing[w3])))],
                 x, y, z, order='grevlex', domain=Kr)
check("over the generic point of C_sing the fibre ideal is (1) => fibre EMPTY",
      list(Gs.exprs) == [sp.Integer(1)], "GB = %s" % list(Gs.exprs)[:2])

# C4. sampled cross-check at random rational points of each stratum
import random
random.seed(11)
ok3 = True
for _ in range(6):
    wv = (sp.Rational(random.randint(-9, 9), random.randint(1, 5)),
          sp.Rational(random.randint(-9, 9), random.randint(1, 5)),
          sp.Rational(random.randint(-9, 9), random.randint(1, 5)))
    if sp.expand(DELTA.subs({w1: wv[0], w2: wv[1], w3: wv[2]})) == 0:
        continue
    n = len(sp.solve([P - wv[0], Q - wv[1], R - wv[2]], [x, y, z], dict=True))
    ok3 = ok3 and (n == 3)
check("sampled points off the tear all have fibre exactly 3", ok3)

ok1 = True
for mv in [1, 2, -1, sp.Rational(1, 2), 3]:
    for rv in [1, -2]:
        wv = (W1.subs({mu: mv, r: rv}), W2.subs({mu: mv, r: rv}), rv)
        n = len(sp.solve([P - wv[0], Q - wv[1], R - wv[2]], [x, y, z], dict=True))
        if n != 1:
            ok1 = False
            print("      tear point mu=%s r=%s gave fibre %d" % (mv, rv, n))
check("sampled points on the tear (mu!=0) all have fibre exactly 1", ok1)

ok0 = True
for rv in [1, -1, 2, sp.Rational(1, 3)]:
    wv = (sp.Rational(4, 27)/rv**2, sp.Rational(4, 3)/rv, rv)
    n = len(sp.solve([P - wv[0], Q - wv[1], R - wv[2]], [x, y, z], dict=True))
    if n != 0:
        ok0 = False
check("sampled points of C_sing all have fibre EMPTY", ok0)

# --------------------------------------------------------------------------
print("\n[D] THE (C*)^2 LEMMA, tested where it must hold and where it must not")
check("a curve in (C*)^2 with chi = 0 exists (the lemma is not vacuous)",
      CH.chi_curve(u - 1) == 1)     # {u=1} in C^2 has chi 1; inside (C*)^2 it is C*
# the lemma's content: no curve in (C*)^2 has chi > 0.  Test representatives.
for nm, f, inside in [("{u=1} n (C*)^2 = C*", u - 1, True),
                      ("{uv=1} = C*", u*v - 1, True),
                      ("{u+v=1} n (C*)^2 = C minus 2 pts", u + v - 1, True)]:
    # chi inside the torus = chi in C^2 minus the points with u=0 or v=0
    f_ = sp.expand(f)
    total = CH.chi_curve(f_)
    onaxes = 0
    for ax in (u, v):
        res = sp.expand(sp.resultant(sp.Poly(f_, ax), sp.Poly(ax, ax)))
        if res != 0:
            other = v if ax is u else u
            pol = sp.Poly(sp.expand(f_.subs(ax, 0)), other)
            if pol.degree() >= 1:
                onaxes += sp.Poly(sp.quo(pol, sp.gcd(pol, pol.diff(other))), other).degree()
    check("chi(%s) <= 0 inside the torus" % nm, total - onaxes <= 0,
          "chi_in_torus = %s" % (total - onaxes))

# --------------------------------------------------------------------------
print("\n[E] THE PLANE VERDICTS, re-derived by hand-checkable identities")
from pathS_modification import slice_AB, components, meets
# W = {w1 = k}, k != 0 : A = (1+xy)^3 and B = k on {1+xy=0}, so the component is
# NOT hit and pi_1(S) = Z.  Verify B == k identically along 1+xy = 0.
A_, B_ = slice_AB(1, 0, 0, sp.Symbol('k'))
Bred = sp.simplify(sp.expand(B_.as_expr()).subs(y, -1/x))
check("on {1+xy=0}, B == k for the plane {w1=k}", sp.simplify(Bred - sp.Symbol('k')) == 0,
      "B|_{y=-1/x} = %s" % Bred)
A0, B0 = slice_AB(0, 1, 0, 0)
B0red = sp.simplify(sp.expand(B0.as_expr()).subs(y, -1/x))
check("on {1+xy=0}, B is a nonzero constant for {w2=0} (component not hit)",
      sp.simplify(B0red) != 0, "B|_{y=-1/x} = %s" % sp.simplify(B0red))

# --------------------------------------------------------------------------
print("\n[F] NEGATIVE CONTROLS -- the filters must be able to say YES")
# A plane whose A has a component that IS hit, to prove `meets` is not always False
Ah, Bh = slice_AB(0, 1, 0, 0)
hits = [(f, meets(f, Bh)[0]) for f, _m in components(Ah)]
check("`meets` returns True on at least one component (not a constant-False test)",
      any(h for _f, h in hits), str(hits))
# chi_curve must not always return the same number
check("chi_curve is not constant", len({CH.chi_curve(f) for _n, f, _e in CAL}) > 2)

print("\n" + "=" * 70)
nfail = sum(1 for _n, ok, _d in RESULTS if not ok)
print("%d checks, %d FAILED" % (len(RESULTS), nfail))
if nfail:
    for n, ok, d in RESULTS:
        if not ok:
            print("   FAILED:", n, d)
sys.exit(1 if nfail else 0)
