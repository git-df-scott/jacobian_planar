#!/usr/bin/env python3
"""Derive, from the polygons alone, every face condition for a target.

For each primitive direction (rho,sigma) the top (rho,sigma)-weighted
component of [P,Q] is [face(P), face(Q)].  Its weight is
    w(P) + w(Q) - w(1,1)
because [x^a y^b, x^c y^d] = (ad-bc) x^(a+c-1) y^(b+d-1).
Compare with w of the target monomial x^r:
    strictly greater -> the top component must VANISH  -> faces commute
    equal            -> the top component must EQUAL the target
    smaller          -> impossible (would leave the target unmatched)

This script does that bookkeeping and then, for the "equal" direction,
writes out the resulting one-variable polynomial identity explicitly with
sympy, symbolically, so nothing is taken on trust.
"""
import json, sys
from math import gcd
import sympy as sp

x, y, u = sp.symbols("x y u")


def hull_points(verts):
    """all lattice points of the convex hull, via row ranges"""
    from trackB1_polygon import hull_rows
    R = hull_rows(verts)
    return [(i, j) for j in sorted(R) for i in range(R[j][0], R[j][1] + 1)]


def edges_and_faces(NP, NQ, r):
    P = [tuple(v) for v in NP]
    Q = [tuple(v) for v in NQ]
    dirs = set()
    for S in (P, Q):
        for a in range(len(S)):
            for b in range(len(S)):
                if a == b:
                    continue
                di, dj = S[b][0]-S[a][0], S[b][1]-S[a][1]
                g = gcd(abs(di), abs(dj)) or 1
                di, dj = di//g, dj//g
                # outward normals candidates: rotate +-90
                for (rho, sig) in ((dj, -di), (-dj, di)):
                    if (rho, sig) != (0, 0):
                        g2 = gcd(abs(rho), abs(sig)) or 1
                        dirs.add((rho//g2, sig//g2))
    out = []
    for (rho, sig) in sorted(dirs):
        wP = max(rho*i + sig*j for (i, j) in P)
        wQ = max(rho*i + sig*j for (i, j) in Q)
        fP = [(i, j) for (i, j) in hull_points(P) if rho*i+sig*j == wP]
        fQ = [(i, j) for (i, j) in hull_points(Q) if rho*i+sig*j == wQ]
        wtop = wP + wQ - (rho + sig)
        wtarget = rho * r          # x^r = x^r y^0
        out.append(dict(dirn=(rho, sig), wP=wP, wQ=wQ, faceP=fP, faceQ=fQ,
                        wtop=wtop, wtarget=wtarget,
                        verdict=("MUST EQUAL TARGET" if wtop == wtarget
                                 else ("commute (top vanishes)" if wtop > wtarget
                                       else "IMPOSSIBLE: target above top")))
                   )
    return out


def symbolic_face_identity(faceP, faceQ, r, dirn):
    """Write [F,G] for the two face forms explicitly and reduce it."""
    a = sp.symbols(f"a0:{len(faceP)}")
    b = sp.symbols(f"b0:{len(faceQ)}")
    F = sum(a[k]*x**i*y**j for k, (i, j) in enumerate(faceP))
    G = sum(b[k]*x**i*y**j for k, (i, j) in enumerate(faceQ))
    br = sp.expand(sp.diff(F, x)*sp.diff(G, y) - sp.diff(F, y)*sp.diff(G, x))
    return F, G, br, a, b


if __name__ == "__main__":
    idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    t = json.load(open("trackD_targets_108.json"))[idx]
    print("target:", t["tag"])
    print("N(P) =", t["NP"])
    print("N(Q) =", t["NQ"], "   [P,Q] = x^%d\n" % t["r"])
    for e in edges_and_faces(t["NP"], t["NQ"], t["r"]):
        if len(e["faceP"]) < 2 and len(e["faceQ"]) < 2:
            continue
        print(f"dir {e['dirn']}: wP={e['wP']} wQ={e['wQ']} "
              f"wtop={e['wtop']} wtarget={e['wtarget']}  -> {e['verdict']}")
        print(f"    faceP {e['faceP']}")
        print(f"    faceQ {e['faceQ']}")
    print()
    # the essential face
    ess = [e for e in edges_and_faces(t["NP"], t["NQ"], t["r"])
           if e["verdict"] == "MUST EQUAL TARGET"]
    for e in ess:
        print("=== ESSENTIAL FACE", e["dirn"], "===")
        F, G, br, a, b = symbolic_face_identity(e["faceP"], e["faceQ"],
                                                t["r"], e["dirn"])
        print("F =", F)
        print("G =", G)
        pol = sp.Poly(br, x, y)
        # target
        tgt = x**t["r"]
        diff = sp.expand(br - tgt)
        print("bracket monomials:", sorted(pol.monoms())[:5], "...",
              sorted(pol.monoms())[-3:])
        # factor out x^r: check br = x^r * (poly in u=x y^2)?
        q, rem = sp.div(sp.expand(br), x**t["r"], x)
        print("bracket / x^%d exact?" % t["r"], sp.simplify(rem) == 0)
        qq = sp.expand(q)
        # substitute y^2 x = u  : check every monomial is a power of u
        pq = sp.Poly(qq, x, y)
        ok = all(2*ix == jy for (ix, jy) in pq.monoms())
        print("quotient is a polynomial in u = x*y^2 ?", ok)
        if ok:
            W = 0
            for (ix, jy), c in zip(pq.monoms(), pq.coeffs()):
                W += c * u**ix
            W = sp.expand(W)
            print("W(u) =", sp.Poly(W, u).all_coeffs()[::-1][:4], "...")
            print("deg W =", sp.degree(W, u))
            print("\nCONDITION:  W(u) == 1")
            for n in range(sp.degree(W, u)+1):
                print("  n=%2d : %s" % (n, sp.Poly(W, u).coeff_monomial(u**n)))
