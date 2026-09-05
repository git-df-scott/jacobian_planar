"""night20 -- the generator: Newton-polygon supports that can carry a
critical-point-free polynomial with a positive-genus generic fibre.

Design reasoning (recorded as part of the measurement):

 * genus >= 1 is required of the target because of Neumann-Norbury: a
   nontrivial rational polynomial in two variables has a reducible fibre, so
   "all fibres irreducible + generic fibre rational" leaves only coordinates.
   Baker's bound gives genus <= #interior lattice points of the Newton polygon
   of the generic fibre P - c = conv(supp P u {(0,0)}).  So a support with NO
   interior lattice point can never carry a target: it is discarded for free.

 * no critical points.  By Bernstein's theorem the number of solutions of
   P_x = P_y = 0 in the torus (C*)^2 is at most the mixed volume
   MV(Newton(P_x), Newton(P_y)); MV = 0 therefore *forces* the torus part of
   the critical locus to be empty, for EVERY choice of coefficients on that
   support.  MV = 0 in the plane means the two polygons are points or parallel
   segments.  Supports with MV = 0 are enumerated exhaustively; what is left to
   check is then only the two axes x = 0 and y = 0, a one-variable gcd.
   (MV > 0 does not imply a critical point exists -- only that generic
   coefficients on that support have one -- so a separate degenerate-coefficient
   sweep is run alongside, see search20.py.)

 * monomial content.  If every monomial of P is divisible by x then P - 0 = P
   is divisible by x, hence reducible; same for y.  Such supports are discarded.
"""
import itertools


def hull(pts):
    pts = sorted(set(pts))
    if len(pts) <= 2:
        return pts
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


def area2(h):
    if len(h) < 3:
        return 0
    s = 0
    for i in range(len(h)):
        a, b = h[i], h[(i+1) % len(h)]
        s += a[0]*b[1] - b[0]*a[1]
    return abs(s)


def mv2(A, B):
    """twice the mixed volume of conv(A), conv(B)."""
    if not A or not B:
        return 0
    S = [(a[0]+b[0], a[1]+b[1]) for a in A for b in B]
    return area2(hull(S)) - area2(hull(A)) - area2(hull(B))


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def interior(pts):
    """#interior lattice points of conv(pts u {(0,0)}) = Baker bound."""
    h = hull(list(set(pts)) + [(0, 0)])
    if len(h) < 3:
        return 0
    A2 = area2(h)
    B = 0
    for i in range(len(h)):
        a, b = h[i], h[(i+1) % len(h)]
        B += _gcd(abs(a[0]-b[0]), abs(a[1]-b[1]))
    return (A2 - B + 2) // 2


def supports(D, size, require_mv0=True):
    mons = [(i, j) for d in range(D+1) for i in range(d+1) for j in [d-i]]
    out = []
    for S in itertools.combinations(mons, size):
        if all(m[0] > 0 for m in S):
            continue
        if all(m[1] > 0 for m in S):
            continue
        if max(i+j for (i, j) in S) < 3:
            continue
        if interior(S) < 1:
            continue
        A = [(i-1, j) for (i, j) in S if i >= 1]
        B = [(i, j-1) for (i, j) in S if j >= 1]
        if not A or not B:
            continue
        if require_mv0 and mv2(A, B) != 0:
            continue
        out.append(S)
    return out


# ------------------------------------------- Bernstein degeneracy of P_x,P_y
def _edges(h):
    return [(h[i], h[(i+1) % len(h)]) for i in range(len(h))] if len(h) >= 2 else []


def _normals(pts):
    h = hull(pts)
    out = []
    for (p, q) in _edges(h):
        d = (q[0]-p[0], q[1]-p[1])
        out.append((-d[1], d[0]))
        out.append((d[1], -d[0]))
    if len(h) == 2:
        pass
    return out


def _face(terms, w):
    """terms: list ((i,j), coeff).  Return the subset minimising <w, (i,j)>."""
    vals = [w[0]*i + w[1]*j for ((i, j), _) in terms]
    m = min(vals)
    return [t for t, v in zip(terms, vals) if v == m]


def _univ_gcd_nontrivial(fa, fb):
    """fa, fb both supported on a common lattice line with primitive direction
    d; test whether the two univariate polynomials in u = x^d1 y^d2 have a
    common root u != 0."""
    pts = [p for (p, _) in fa] + [p for (p, _) in fb]
    p0 = pts[0]
    dv = None
    for p in pts[1:]:
        v = (p[0]-p0[0], p[1]-p0[1])
        if v != (0, 0):
            g = _gcd(abs(v[0]), abs(v[1]))
            dv = (v[0]//g, v[1]//g)
            break
    if dv is None:
        return False
    def coords(fs):
        d = {}
        for ((i, j), co) in fs:
            k = (i-p0[0])//dv[0] if dv[0] != 0 else (j-p0[1])//dv[1]
            d[k] = d.get(k, 0) + co
        return d
    ca, cb = coords(fa), coords(fb)
    import sympy as sp
    u = sp.Symbol('u')
    kmin = min(min(ca), min(cb))
    A = sum(v * u**(k - kmin) for k, v in ca.items())
    B = sum(v * u**(k - kmin) for k, v in cb.items())
    if A == 0 or B == 0:
        return True
    g = sp.Poly(sp.gcd(sp.Poly(A, u), sp.Poly(B, u)), u)
    g = sp.Poly(sp.quo(g, sp.Poly(u, u)**min(g.monoms(), key=lambda m: m[0])[0]), u) \
        if g.degree() >= 1 else g
    return g.degree() >= 1


def torus_may_be_empty(S, cf):
    """A necessary condition for  V(P_x, P_y) n (C*)^2 = empty.

    By Bernstein's theorem the system has exactly MV(N(P_x), N(P_y)) roots in
    the torus whenever it is non-degenerate (no face system, in any direction
    w, has a torus root).  So an empty torus part forces MV = 0 or degeneracy
    in some edge-normal direction.  Faces that are single monomials never
    vanish in the torus; two faces supported on lattice segments of different
    primitive directions always have a common torus zero; two faces on
    segments of the same direction have one iff the corresponding univariate
    polynomials share a non-zero root."""
    A = [((i-1, j), a*i) for a, (i, j) in zip(cf, S) if i >= 1]
    B = [((i, j-1), a*j) for a, (i, j) in zip(cf, S) if j >= 1]
    if not A or not B:
        return False
    PA = [p for (p, _) in A]
    PB = [p for (p, _) in B]
    if mv2(PA, PB) == 0:
        return True
    for w in _normals(PA) + _normals(PB):
        fa, fb = _face(A, w), _face(B, w)
        if len(fa) < 2 or len(fb) < 2:
            continue
        da = _dir(fa)
        db = _dir(fb)
        if da is None or db is None:
            continue
        if da != db and da != (-db[0], -db[1]):
            return True
        if _univ_gcd_nontrivial(fa, fb):
            return True
    return False


def _dir(fs):
    pts = sorted(set(p for (p, _) in fs))
    if len(pts) < 2:
        return None
    v = (pts[1][0]-pts[0][0], pts[1][1]-pts[0][1])
    g = _gcd(abs(v[0]), abs(v[1]))
    v = (v[0]//g, v[1]//g)
    return v if v > (0, 0) or v[0] > 0 or (v[0] == 0 and v[1] > 0) else (-v[0], -v[1])


# ------------------------------------------ Minkowski (in)decomposability
def edge_vectors(h):
    """edges of the hull as (primitive direction, multiplicity)."""
    out = []
    for i in range(len(h)):
        p, q = h[i], h[(i+1) % len(h)]
        v = (q[0]-p[0], q[1]-p[1])
        m = _gcd(abs(v[0]), abs(v[1]))
        out.append(((v[0]//m, v[1]//m), m))
    return out


def indecomposable(pts):
    """Is conv(pts) Minkowski-indecomposable (as a lattice polygon)?
    A summand corresponds to a choice 0 <= n_i <= m_i of the edge
    multiplicities with sum n_i * d_i = 0, other than all-0 and all-m.
    If conv(pts) is indecomposable and 2-dimensional then every polynomial
    with that Newton polygon and no monomial factor is irreducible, since
    Newton(F*G) = Newton(F) + Newton(G)."""
    h = hull(pts)
    if len(h) < 3:
        return False
    ev = edge_vectors(h)
    ranges = [range(m + 1) for (_, m) in ev]
    import itertools as it
    tot = 1
    for r in ranges:
        tot *= len(r)
    if tot > 200000:
        return None
    for n in it.product(*ranges):
        if all(v == 0 for v in n):
            continue
        if all(n[i] == ev[i][1] for i in range(len(ev))):
            continue
        sx = sum(n[i]*ev[i][0][0] for i in range(len(ev)))
        sy = sum(n[i]*ev[i][0][1] for i in range(len(ev)))
        if sx == 0 and sy == 0:
            return False
    return True


def touches_both_axes(pts):
    return min(p[0] for p in pts) == 0 and min(p[1] for p in pts) == 0


def newton_forces_all_fibres_irreducible(S):
    """The Newton-polygon design test.  For c != P(0,0) the fibre P - c has
    Newton polygon N1 = conv(S u {0}); for c = P(0,0) it is N0 = conv(S\\{0}).
    If BOTH are 2-dimensional, Minkowski-indecomposable, and touch both axes
    (no monomial factor), then EVERY fibre is irreducible, whatever the
    coefficients."""
    S = [tuple(m) for m in S]
    N1 = list(set(S) | {(0, 0)})
    N0 = [m for m in S if m != (0, 0)]
    if not N0:
        return False
    for N in (N1, N0):
        if not touches_both_axes(N):
            return False
        r = indecomposable(N)
        if r is not True:
            return False
    return True
