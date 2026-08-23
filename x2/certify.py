"""Certifier for a candidate pair (P,Q) with {P,Q} = x^k.

Every check is exact (sympy over Q); no floating point, no division.
  1. bracket   : expand(P_x Q_y - P_y Q_x) == x^k, term by term
  2. support   : Newton support of P and Q, and their convex hulls
  3. vertices  : each named vertex coefficient is nonzero
  4. integrality: P, Q have no denominators in x,y (are polynomials)
"""
import sympy as sp

x, y = sp.symbols('x y')


def support(F):
    F = sp.expand(F)
    if F == 0:
        return {}
    return {k: v for k, v in sp.Poly(F, x, y).as_dict().items() if v != 0}


def hull(pts):
    pts = sorted(set(pts))
    if len(pts) <= 2:
        return list(pts)
    def cr(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    lo = []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    up = []
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def certify(P, Q, k=2, want_vertices=None, verbose=True):
    checks = []
    P, Q = sp.expand(P), sp.expand(Q)
    checks.append(("P is a polynomial in x,y", P.is_polynomial(x, y)))
    checks.append(("Q is a polynomial in x,y", Q.is_polynomial(x, y)))
    br = sp.expand(sp.diff(P, x)*sp.diff(Q, y) - sp.diff(P, y)*sp.diff(Q, x))
    checks.append((f"{{P,Q}} == x^{k}", sp.expand(br - x**k) == 0))
    sP, sQ = support(P), support(Q)
    hP, hQ = hull(list(sP)), hull(list(sQ))
    if want_vertices is not None:
        for v in want_vertices:
            checks.append((f"vertex {v} of P nonzero", sP.get(tuple(v), 0) != 0))
    if verbose:
        print(f"  P = {sp.factor(P)}")
        print(f"  Q = {sp.factor(Q)}")
        print(f"  bracket   = {sp.expand(br)}")
        print(f"  supp P    = {sorted(sP)}")
        print(f"  hull P    = {hP}")
        print(f"  supp Q    = {sorted(sQ)}")
        print(f"  hull Q    = {hQ}")
        print(f"  deg P, deg Q = {sp.total_degree(P)}, {sp.total_degree(Q)}")
        for name, ok in checks:
            print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    return all(ok for _, ok in checks), dict(suppP=sP, suppQ=sQ, hullP=hP, hullQ=hQ)
