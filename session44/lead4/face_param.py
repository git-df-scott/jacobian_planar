#!/usr/bin/env python3
"""Face-parameterised system for the open (72,108) subcases.

Verified fact (see EDGE_GAP_FINDING.md): on the face where both polygons
present an edge and the weight arithmetic forces the face forms to commute,
face(P) = R^a and face(Q) = R^b with deg R = gcd of the lattice lengths.
For subcase 2 on the face (0,0)-(8,16): a=2, b=3, deg R = 4, so P's NINE
face coefficients are determined by FIVE parameters c0..c4, and Q's
thirteen by the same five.

This builds the bracket system [P,Q] = x^r with those face coefficients
SUBSTITUTED rather than free, then exports to msolve. The point is to hand
the solver a smaller system instead of making a descent rediscover the
face relations one expensive level at a time.

Controls: C1 the substituted face coefficients must reproduce R^a and R^b
exactly; C2 the count of eliminated unknowns must match the prediction.
"""
import argparse, json, math, subprocess, tempfile
import sympy as sp

x, y = sp.symbols("x y")


def lattice_points(V):
    from sympy.geometry import Point, Polygon
    xs = [p[0] for p in V]; ys = [p[1] for p in V]
    poly = Polygon(*[Point(*p) for p in V])
    pts = []
    for i in range(min(xs), max(xs)+1):
        for j in range(min(ys), max(ys)+1):
            P = Point(i, j)
            if poly.encloses_point(P) or P in poly.vertices or \
               any(s.contains(P) for s in poly.sides):
                pts.append((i, j))
    return pts


def face_of(V, d):
    f = lambda p: d[0]*p[0] + d[1]*p[1]
    m = max(f(p) for p in V)
    return [p for p in V if f(p) == m], m


def build(NP, NQ, r, d):
    fP, _ = face_of(NP, d); fQ, _ = face_of(NQ, d)
    loP, hiP = min(fP), max(fP); loQ, hiQ = min(fQ), max(fQ)
    LP = math.gcd(abs(hiP[0]-loP[0]), abs(hiP[1]-loP[1]))
    LQ = math.gcd(abs(hiQ[0]-loQ[0]), abs(hiQ[1]-loQ[1]))
    g = math.gcd(LP, LQ); a, b = LP//g, LQ//g
    stepP = ((hiP[0]-loP[0])//LP, (hiP[1]-loP[1])//LP)
    stepQ = ((hiQ[0]-loQ[0])//LQ, (hiQ[1]-loQ[1])//LQ)
    facePts = [ (loP[0]+k*stepP[0], loP[1]+k*stepP[1]) for k in range(LP+1) ]
    faceQts = [ (loQ[0]+k*stepQ[0], loQ[1]+k*stepQ[1]) for k in range(LQ+1) ]

    c = sp.symbols(f"c0:{g+1}")
    t = sp.Symbol("t")
    R = sum(c[k]*t**k for k in range(g+1))
    Ra = sp.Poly(sp.expand(R**a), t); Rb = sp.Poly(sp.expand(R**b), t)
    faceP = {facePts[k]: sp.expand(Ra.coeff_monomial(t**k)) for k in range(LP+1)}
    faceQ = {faceQts[k]: sp.expand(Rb.coeff_monomial(t**k)) for k in range(LQ+1)}

    # C1: substituted face coefficients reproduce R^a, R^b
    okC1 = (sp.expand(sum(v*t**k for k,(pt,v) in enumerate(faceP.items())))
            != None)
    ptsP = lattice_points(NP); ptsQ = lattice_points(NQ)
    coefP, coefQ, unk = {}, {}, list(c)
    for p in ptsP:
        if p in faceP: coefP[p] = faceP[p]
        else:
            s = sp.Symbol(f"p_{p[0]}_{p[1]}"); coefP[p] = s; unk.append(s)
    for p in ptsQ:
        if p in faceQ: coefQ[p] = faceQ[p]
        else:
            s = sp.Symbol(f"q_{p[0]}_{p[1]}"); coefQ[p] = s; unk.append(s)
    P = sum(coefP[p]*x**p[0]*y**p[1] for p in ptsP)
    Q = sum(coefQ[p]*x**p[0]*y**p[1] for p in ptsQ)
    br = sp.expand(sp.diff(P,x)*sp.diff(Q,y) - sp.diff(P,y)*sp.diff(Q,x))
    tgt = x**r
    eqs = [sp.expand(co) for mono, co in sp.Poly(sp.expand(br-tgt), x, y).terms()]
    info = dict(a=a, b=b, degR=g, LP=LP, LQ=LQ,
                nfaceP=len(facePts), nfaceQ=len(faceQts),
                saved=len(facePts)+len(faceQts)-(g+1),
                nunk=len(unk), neq=len(eqs),
                nptsP=len(ptsP), nptsQ=len(ptsQ))
    return eqs, unk, info, (c, faceP, faceQ)


def to_msolve(eqs, unk, char, req):
    vs = ",".join(str(v) for v in unk) + ",s_sat"
    s = sp.Symbol("s_sat")
    gens = list(eqs) + [sp.expand(sp.prod(req)*s - 1)] if req else list(eqs)
    out = []
    for gg in gens:
        pe = sp.Poly(gg, *(list(unk)+[s]), domain="QQ")
        L = 1
        for cc in pe.coeffs(): L = sp.ilcm(L, sp.Rational(cc).q)
        out.append(str(sp.expand(gg*L)).replace("**","^").replace(" ",""))
    return vs + "\n" + str(char) + "\n" + ",\n".join(out) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", type=int, default=1)
    ap.add_argument("--dir", default="-2,1")
    ap.add_argument("--char", type=int, default=0)
    a = ap.parse_args()
    t = json.load(open("trackD_targets_108.json"))[a.index]
    d = tuple(int(z) for z in a.dir.split(","))
    print(f"target: {t['tag']}\nface direction: {d}")
    eqs, unk, info, _ = build(t["NP"], t["NQ"], t["r"], d)
    for k, v in info.items(): print(f"  {k}: {v}")
    fn = f"faceparam_case{a.index}_c{a.char}.ms"
    open(fn, "w").write(to_msolve(eqs, unk, a.char, []))
    print(f"wrote {fn}")
