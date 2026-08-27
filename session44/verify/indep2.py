#!/usr/bin/env python3
"""INDEPENDENT check of the subcase-2 verdict.

Built from scratch in the original (x,y) coordinates -- no (u,z) change of
variables, no reuse of the agent's system builder -- so that agreement is
evidence and not an echo.

GGHV arXiv:2204.14178 Prop 4.3 subcase 2 (quadrilaterals), reduced Laurent
coordinates:   N(P) = conv{(0,0),(1,0),(8,14),(8,16)}
               N(Q) = conv{(0,0),(2,1),(12,21),(12,24)}
               [P,Q] = P_x Q_y - P_y Q_x = x^2.

The reported verdict to be checked is that the vertex (8,16) of N(P) is
forced to vanish, i.e. no pair with THIS Newton polygon exists.  Here that
is asked as a single Rabinowitsch question:

        < bracket equations >  +  < W * P_{8,16} - 1 >   =   (1) ?

A unit ideal means (8,16) can never be a vertex, i.e. the subcase is empty.
"""
import itertools, sys
from fractions import Fraction

# ---------- lattice points of a convex polygon, computed here from scratch
def poly_points(verts):
    """Integer points of conv(verts).  Half-plane test with exact rationals."""
    n = len(verts)
    cx = Fraction(sum(v[0] for v in verts), n)
    cy = Fraction(sum(v[1] for v in verts), n)
    edges = []
    for k in range(n):
        (x1, y1), (x2, y2) = verts[k], verts[(k + 1) % n]
        a, b = y2 - y1, x1 - x2          # inward/outward normal
        c = a * x1 + b * y1
        if a * cx + b * cy < c:          # orient so interior gives >= c
            a, b, c = -a, -b, -c
        edges.append((a, b, c))
    xs = [v[0] for v in verts]; ys = [v[1] for v in verts]
    pts = []
    for i in range(min(xs), max(xs) + 1):
        for j in range(min(ys), max(ys) + 1):
            if all(a * i + b * j >= c for a, b, c in edges):
                pts.append((i, j))
    return sorted(pts)

NP = [(0, 0), (1, 0), (8, 14), (8, 16)]
NQ = [(0, 0), (2, 1), (12, 21), (12, 24)]
ptsP, ptsQ = poly_points(NP), poly_points(NQ)

# ---------- the bracket, expanded by hand on monomials
# [x^a y^b , x^c y^d] = (a d - b c) x^(a+c-1) y^(b+d-1)
# so the coefficient of x^m y^n in [P,Q] is
#     sum over (a,b) in N(P), (c,d) in N(Q) with a+c-1=m, b+d-1=n
#         (a d - b c) * A_{a,b} * B_{c,d}
def build():
    terms = {}                      # (m,n) -> list of (coef, ivar, jvar)
    for (a, b) in ptsP:
        for (c, d) in ptsQ:
            k = a * d - b * c
            if k == 0:
                continue
            terms.setdefault((a + c - 1, b + d - 1), []).append(
                (k, (a, b), (c, d)))
    return terms

def main():
    prime = int(sys.argv[1]) if len(sys.argv) > 1 else 65521
    terms = build()
    print(f"N(P) lattice points: {len(ptsP)}   N(Q): {len(ptsQ)}")
    w = lambda q: q[1] - 2 * q[0]
    print("P weights j-2i:", sorted({w(q) for q in ptsP}),
          "  Q weights:", sorted({w(q) for q in ptsQ}))
    # which coefficients actually occur in the bracket?
    usedP, usedQ = set(), set()
    for lst in terms.values():
        for _, i, j in lst:
            usedP.add(i); usedQ.add(j)
    print(f"coefficients appearing in the bracket: P {len(usedP)}, "
          f"Q {len(usedQ)}  (constant terms drop out, as they must)")
    eqs = []
    for (m, n), lst in sorted(terms.items()):
        rhs = 1 if (m, n) == (2, 0) else 0
        eqs.append(((m, n), lst, rhs))
    print(f"bracket equations: {len(eqs)}")
    byw = {}
    for (m, n), lst, rhs in eqs:
        byw.setdefault(w((m, n)), []).append(((m, n), lst, rhs))
    for lev in sorted(byw):
        print(f"   bracket weight {lev:3d}: {len(byw[lev]):3d} equations")
    tgt = w((2, 0))
    print(f"target x^2 sits at weight {tgt}  "
          f"(= deepest level: {tgt == min(byw)})")

    # ---------- emit Singular
    names = {}
    for q in sorted(usedP): names[('P', q)] = f"A{q[0]}_{q[1]}"
    for q in sorted(usedQ): names[('Q', q)] = f"B{q[0]}_{q[1]}"
    varlist = sorted(names.values())
    def poly(lst, rhs):
        s = " + ".join(f"{k}*{names[('P',i)]}*{names[('Q',j)]}"
                       for k, i, j in lst)
        return s + (f" - {rhs}" if rhs else "")
    lines = [f"ring R = {prime}, ({','.join(varlist)},W), dp;"]
    lines.append("ideal I = " + ",\n  ".join(poly(l, r) for _, l, r in eqs)
                 + ";")
    # the decisive condition: the vertex (8,16) of N(P) is genuinely present
    lines.append("I = I + ideal(W*A8_16 - 1);")
    lines.append('"variables: ' + str(len(varlist) + 1) + '";')
    lines.append("int t0 = timer;")
    lines.append("ideal G = std(I);")
    lines.append('"seconds: " + string(timer - t0);')
    lines.append('if (size(G)==1 && G[1]==1) { "VERDICT: UNIT IDEAL -- '
                 'vertex (8,16) is FORCED TO VANISH => subcase 2 EMPTY"; } '
                 'else { "VERDICT: nonempty, dim = " + string(dim(G)); }')
    lines.append("quit;")
    fn = f"indep2_v816_p{prime}.sing"
    open(fn, "w").write("\n".join(lines) + "\n")
    print(f"wrote {fn}   ({len(varlist)+1} variables, {len(eqs)+1} generators)")

if __name__ == "__main__":
    main()
