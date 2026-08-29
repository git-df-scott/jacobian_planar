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
