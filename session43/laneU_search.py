"""Session 43, LANE U — the search.

From laneU_xu.py (all identities verified there):

    P = P(x,u),  Q = y + g(x,u),  u = 1 + xy
    [P,Q] = P_x + y P_u + x {P,g}                                    (identity)
    Keller  <=>  x P_x + (u-1) P_u + x^2 {P,g} = x                        (*)

(*) forces P(0,u) = const (normalise to 0), then P = x P~, and at x = 0 forces

    p + (u-1) p' = 1,   p(u) := P~(0,u)   =>   p = 1  in characteristic zero

so P = x + x^2 Psi(x,u) is FORCED.  Substituting and dividing by x^2 turns (*)
into a single equation which is LINEAR in g:

    2 Psi + (u-1) Psi_u + x Psi_x + P_x * g_u - x^2 Psi_u * g_x = 0        (**)
        with  P_x = 1 + 2 x Psi + x^2 Psi_x.

TWO STRUCTURAL FACTS, proved here rather than assumed:
  * Psi_u = 0 forces Psi = 0.  Indeed then g_u = -(P_x - 1)/(x P_x), and
    polynomiality needs x P_x | P_x - 1, impossible by degree unless P_x = 1.
    So every member with Psi independent of u is the triangular automorphism
    (x, y + h(x)).  A counterexample here MUST have Psi_u != 0.
  * Mondello's char-2 map has p(u) = u, and p + (u-1)p' - 1 = 2(u-1), which
    vanishes ONLY in characteristic 2.  That is exactly why his counterexample
    is a characteristic-2 phenomenon and has no naive char-0 analogue.

THE SEARCH.  Sweep Psi over a support; (**) is a LINEAR system in the
coefficients of g; solve it exactly over Q.  Every consistent solution is a
genuine Keller pair in characteristic zero -- and then the ONLY thing that
matters is its geometric degree, computed exactly.  Degree 1 = automorphism
(expected, and used here as the positive control that the pipeline can produce
solutions at all).  Degrees 2,3,4,5 are excluded by Campbell / Orevkov /
Domrina-Orevkov / Domrina / Zoladek, so any such hit would signal a BUG.
Degree >= 6 would be a counterexample candidate and goes to the full gate.
"""
import sys
import sympy as sp
from itertools import product

x, y, u = sp.symbols('x y u')
a, b = sp.symbols('a b')


def keller_eq(Psi, g):
    """The left side of (**).  Vanishes identically iff (P,Q) is Keller."""
    Px = sp.expand(1 + 2*x*Psi + x**2*sp.diff(Psi, x))
    return sp.expand(2*Psi + (u - 1)*sp.diff(Psi, u) + x*sp.diff(Psi, x)
                     + Px*sp.diff(g, u) - x**2*sp.diff(Psi, u)*sp.diff(g, x))


def to_xy(e):
    return sp.expand(e.subs(u, 1 + x*y))


def bracket(Pxy, Qxy):
    return sp.expand(sp.diff(Pxy, x)*sp.diff(Qxy, y) - sp.diff(Pxy, y)*sp.diff(Qxy, x))


def geometric_degree(Pxy, Qxy):
    K = sp.QQ.frac_field(a, b)
    try:
        G = sp.groebner([sp.expand(Pxy - a), sp.expand(Qxy - b)], x, y,
                        order='lex', domain=K)
    except Exception:
        return None
    for gg in G.exprs:
        fs = gg.free_symbols
        if x in fs and y not in fs:
            return sp.Poly(gg, x).degree()
        if y in fs and x not in fs:
            return sp.Poly(gg, y).degree()
    return None


def solve_for_g(Psi, gsupport):
    """Solve (**) for g on the given support.  Returns a list of solutions."""
    gam = sp.symbols('G0:%d' % len(gsupport))
    g = sum(gam[i]*x**m[0]*u**m[1] for i, m in enumerate(gsupport))
    eq = keller_eq(Psi, g)
    if eq == 0:
        return [g]
    poly = sp.Poly(eq, x, u)
    eqs = list(poly.coeffs())
    sol = sp.solve(eqs, gam, dict=True)
    out = []
    for s in sol:
        gg = sp.expand(g.subs(s))
        free = [v for v in gam if v not in s]
        # pin remaining free parameters to 0 and to 1 (two representatives)
        for val in (0, 1):
            out.append(sp.expand(gg.subs({v: val for v in free})))
    return out


def run(psi_support, gsupport, coeff_pool, label, verbose=True):
    print("\n=== %s" % label)
    print("    Psi support:", psi_support, "  g support size:", len(gsupport))
    hits, n_keller, n_aut, degs = [], 0, 0, {}
    for coeffs in product(coeff_pool, repeat=len(psi_support)):
        if all(c == 0 for c in coeffs):
            continue
        Psi = sum(c*x**m[0]*u**m[1] for c, m in zip(coeffs, psi_support))
        if sp.expand(sp.diff(Psi, u)) == 0:
            continue                                   # proved: forces Psi = 0
        for g in solve_for_g(Psi, gsupport):
            if sp.expand(keller_eq(Psi, g)) != 0:
                continue
            P = sp.expand(x + x**2*Psi)
            Pxy, Qxy = to_xy(P), sp.expand(y + to_xy(g))
            J = bracket(Pxy, Qxy)
            if sp.expand(J - 1) != 0:                  # independent replay of Keller
                continue
            n_keller += 1
            d = geometric_degree(Pxy, Qxy)
            degs[d] = degs.get(d, 0) + 1
            if d == 1:
                n_aut += 1
            elif d is not None and d >= 2:
                hits.append((Psi, g, d, Pxy, Qxy))
                print("   *** geometric degree %s  Psi=%s  g=%s" % (d, Psi, g))
    print("    Keller pairs found: %d   (degree-1 automorphisms: %d)" % (n_keller, n_aut))
    print("    geometric-degree histogram:", degs)
    return hits


if __name__ == '__main__':
    print("[0] structural facts, verified")
    # Psi_u = 0 => Psi = 0 : check on a family
    ok = True
    for Psi in [sp.Integer(1), x, x**2, 1 + x]:
        gsup = [(i, j) for i in range(4) for j in range(3)]
        if solve_for_g(Psi, gsup):
            for g in solve_for_g(Psi, gsup):
                if sp.expand(keller_eq(Psi, g)) == 0:
                    ok = False
    print("   PASS  Psi independent of u admits no solution g" if ok
          else "   FAIL  a u-independent Psi solved (**)")
    # positive control: Psi = 0 must reproduce the triangular automorphisms
    ctl = [g for g in solve_for_g(sp.Integer(0), [(i, 0) for i in range(4)])
           if sp.expand(keller_eq(sp.Integer(0), g)) == 0]
    print("   PASS  Psi = 0 gives triangular automorphisms (%d found)" % len(ctl)
          if ctl else "   FAIL  positive control produced nothing")

    POOL = [0, 1, -1, 2, -2, sp.Rational(1, 2), 3]
    GSUP = [(i, j) for i in range(5) for j in range(4)]

    allhits = []
    allhits += run([(0, 1)], GSUP, POOL, "Psi = c*u                     (smallest u-dependent)")
    allhits += run([(0, 1), (0, 2)], GSUP, POOL, "Psi = c1*u + c2*u^2")
    allhits += run([(0, 1), (1, 1)], GSUP, POOL, "Psi = c1*u + c2*x*u")
    allhits += run([(0, 1), (1, 0)], GSUP, POOL, "Psi = c1*u + c2*x")
    allhits += run([(0, 1), (2, 2)], GSUP, POOL, "Psi = c1*u + c2*x^2u^2  (Mondello-shaped)")

    print("\n" + "=" * 68)
    print("TOTAL hits with geometric degree >= 2:", len(allhits))
    for h in allhits:
        print("   deg %s :  P = x + x^2*(%s),  g = %s" % (h[2], h[0], h[1]))
