#!/usr/bin/env python3
"""The (2,-1)-weight cascade for subcase 1: structure and level-by-level ranks.

Grade by w(i,j) = 2i - j.  Then
    P = sum_{w=-8..2} P_w ,  Q = sum_{w=-12..3} Q_w
with P_w supported on the lattice points of N(P) on the line 2i-j = w, and
similarly for Q.  Writing u = x y^2, every w-slice is
    P_w = x^{a} y^{b} p(u),  2a - b = w,  a = min i on the slice,
and for two such,
    [x^a y^b phi(u), x^c y^d psi(u)]
        = x^{a+c-1} y^{b+d-1} [ (ad-bc) phi psi + (2a-b) u phi psi'
                                                 - (2c-d) u phi' psi ]
(verified against sympy below).  So the whole problem is a system of
UNIVARIATE polynomial identities, one per weight level W:

    sum_{w1+w2 = W+1} u^{shift} Phi_{w1,w2}(u) = delta_{W,4}

whose NEW unknowns are P_{W-2} and Q_{W-1}, entering linearly through
    L_W(p,q) = [face(P), q] + [p, face(Q)].
Everything else in the level is a product of unknowns settled higher up.

Levels W = 3 .. -6   : both P_{W-2} and Q_{W-1} are new
Levels W = -7 .. -11 : only Q_{W-1} is new (P has no slice below w = -8)
Levels W = -12..-21  : NOTHING new -- these are pure obstruction levels.
"""
import sys
from fractions import Fraction

NP = [(0, 0), (1, 0), (8, 14), (8, 16), (0, 8)]
NQ = [(0, 0), (2, 1), (12, 21), (12, 24), (0, 12)]


def inside(pt, verts):
    """point in the convex hull of verts (all our polygons are convex)?"""
    from itertools import combinations
    # half-plane description built from consecutive hull edges
    import math
    cx = sum(v[0] for v in verts) / len(verts)
    cy = sum(v[1] for v in verts) / len(verts)
    order = sorted(verts, key=lambda v: math.atan2(v[1] - cy, v[0] - cx))
    n = len(order)
    x, y = pt
    for t in range(n):
        (x1, y1), (x2, y2) = order[t], order[(t + 1) % n]
        cross = (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)
        if cross < 0:
            return False
    return True


def slices(verts):
    """w -> sorted list of i such that (i, 2i-w) is in the polygon."""
    imax = max(v[0] for v in verts)
    jmax = max(v[1] for v in verts)
    out = {}
    for i in range(0, imax + 1):
        for j in range(0, jmax + 1):
            if inside((i, j), verts):
                out.setdefault(2 * i - j, []).append(i)
    return {w: sorted(v) for w, v in out.items()}


SP = slices(NP)
SQ = slices(NQ)


def base(S, w):
    a = min(S[w])
    return a, 2 * a - w, len(S[w])          # (a, b, #coefficients)


def bracket_slice(w1, w2, degp, degq):
    """degree in u of Phi_{w1,w2} and the x-exponent of the product."""
    a, b, _ = base(SP, w1)
    c, d, _ = base(SQ, w2)
    return a + c - 1, b + d - 1, degp + degq


def verify_formula():
    """Check [x^a y^b phi(u), x^c y^d psi(u)] = x^{a+c-1} y^{b+d-1} *
    [ (ad-bc) phi psi + (2a-b) u phi psi' - (2c-d) u phi' psi ] on explicit
    polynomial phi, psi and several (a,b,c,d)."""
    import sympy as sp
    x, y, u = sp.symbols("x y u")
    U = x * y**2
    ok = True
    tests = [(1, 0, 2, 1), (3, 2, 5, 4), (0, 8, 0, 12), (2, 3, 7, 9),
             (5, 1, 0, 4), (0, 0, 1, 1)]
    phis = [1 + 2 * u + 3 * u**2, 7 * u, 4 + u**3 - 2 * u**5]
    psis = [5 - u + u**3, 2 + u, 1 + 9 * u**2]
    for (a, b, c, d) in tests:
        for ph in phis:
            for ps in psis:
                A = sp.expand(x**a * y**b * ph.subs(u, U))
                B = sp.expand(x**c * y**d * ps.subs(u, U))
                lhs = sp.expand(sp.diff(A, x) * sp.diff(B, y)
                                - sp.diff(A, y) * sp.diff(B, x))
                rhs = sp.expand((x**(a + c - 1) * y**(b + d - 1) * (
                    (a * d - b * c) * ph * ps
                    + (2 * a - b) * u * ph * sp.diff(ps, u)
                    - (2 * c - d) * u * sp.diff(ph, u) * ps)).subs(u, U))
                if sp.simplify(lhs - rhs) != 0:
                    ok = False
                    print("  FORMULA MISMATCH", (a, b, c, d), ph, ps)
    print("bracket formula verified on",
          len(tests) * len(phis) * len(psis), "cases:", ok)
    return ok


def report():
    print("N(P) slices (w : i-range, #coeffs):")
    tp = 0
    for w in sorted(SP, reverse=True):
        a, b, k = base(SP, w)
        tp += k
        print(f"   w={w:3d}  i in [{min(SP[w])},{max(SP[w])}]  n={k}"
              f"   base ({a},{b})")
    print("   total P coefficients:", tp)
    tq = 0
    for w in sorted(SQ, reverse=True):
        a, b, k = base(SQ, w)
        tq += k
    print("   total Q coefficients:", tq)

    print("\nlevel-by-level bookkeeping "
          "(W: #eqs, #new unknowns, cumulative balance):")
    bal = 0
    tot_eq = 0
    for W in range(4, -22, -1):
        pairs = [(w1, W + 1 - w1) for w1 in sorted(SP, reverse=True)
                 if (W + 1 - w1) in SQ]
        if not pairs:
            continue
        xs = []
        for (w1, w2) in pairs:
            a, b, kp = base(SP, w1)
            c, d, kq = base(SQ, w2)
            lo = a + c - 1
            hi = lo + (kp - 1) + (kq - 1)
            xs.append((lo, hi))
        lo = min(v[0] for v in xs); hi = max(v[1] for v in xs)
        neq = hi - lo + 1
        if W == 4:
            neq -= 1          # the x^2 on the right-hand side is allowed
        new = 0
        if (W - 2) in SP and W - 2 <= 1:
            new += len(SP[W - 2])
        if (W - 1) in SQ and W - 1 <= 2:
            new += len(SQ[W - 1])
        tot_eq += neq
        bal += new - neq
        print(f"   W={W:4d}: eqs {neq:3d}  new unknowns {new:3d}   "
              f"running (unknowns - equations) = {bal:5d}")
    print(f"\n   total equations {tot_eq}, total unknowns {tp + tq}, "
          f"final balance {bal}")


if __name__ == "__main__":
    if "verify" in sys.argv:
        verify_formula()
    report()
