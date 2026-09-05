#!/usr/bin/env python3
"""INDEPENDENT falsification test of the prediction a_10_5 = 0.

The face analysis (EDGE_GAP_FINDING.md) claims that for open subcase 2 the
face root has a gap, R = c0 + c3 t^3 + c4 t^4, which makes the face
coefficients of P vanish at positions k = 1, 2 AND 5. The descent found
k=1 (lattice point (1,2)) and k=2 (point (2,4)) on its own. Position k=5,
lattice point (5,10), is the PREDICTION.

This test assumes NOTHING about the face structure. It builds the raw
bracket system [P,Q] = x^2 with all coefficients free, imposes only the
two zeros the descent actually found, and asks whether the coefficient at
(5,10) is then forced to vanish -- by saturating with it and testing
emptiness:

    ideal( bracket equations, p_{1,2}, p_{2,4}, p_{5,10}*s - 1 )

  EMPTY    -> no solution has p_{5,10} != 0, so p_{5,10} = 0 IS forced:
              the prediction is CONFIRMED by an independent route.
  NONEMPTY -> a solution exists with p_{5,10} != 0: the prediction is
              REFUTED and the face analysis must be retracted.
"""
import json, math, sys
import sympy as sp
from face_param import lattice_points

x, y = sp.symbols("x y")
t = json.load(open("trackD_targets_108.json"))[1]
NP, NQ, r = t["NP"], t["NQ"], t["r"]
ptsP, ptsQ = lattice_points(NP), lattice_points(NQ)
cP = {p: sp.Symbol(f"p_{p[0]}_{p[1]}") for p in ptsP}
cQ = {p: sp.Symbol(f"q_{p[0]}_{p[1]}") for p in ptsQ}
P = sum(cP[p]*x**p[0]*y**p[1] for p in ptsP)
Q = sum(cQ[p]*x**p[0]*y**p[1] for p in ptsQ)
br = sp.expand(sp.diff(P,x)*sp.diff(Q,y) - sp.diff(P,y)*sp.diff(Q,x) - x**r)
eqs = [sp.expand(co) for _, co in sp.Poly(br, x, y).terms()]

found = [(1,2), (2,4)]          # the zeros the descent actually established
pred  = (5,10)                  # the predicted zero
for f in found + [pred]:
    if f not in cP:
        sys.exit(f"lattice point {f} is not in N(P) -- test invalid")
sub = {cP[f]: 0 for f in found}
eqs = [sp.expand(e.subs(sub)) for e in eqs]
eqs = [e for e in eqs if e != 0]
unk = [v for v in (list(cP.values())+list(cQ.values())) if v not in sub]
s = sp.Symbol("s_sat")
eqs.append(sp.expand(cP[pred]*s - 1))
unk.append(s)
print(f"raw system: {len(unk)} unknowns, {len(eqs)} equations")
print(f"imposed zeros: {found};  saturating by the predicted zero {pred}")

def export(char, fn):
    out = []
    for g in eqs:
        pe = sp.Poly(g, *unk, domain="QQ")
        L = 1
        for c in pe.coeffs(): L = sp.ilcm(L, sp.Rational(c).q)
        out.append(str(sp.expand(g*L)).replace("**","^").replace(" ",""))
    open(fn,"w").write(",".join(str(v) for v in unk) + f"\n{char}\n"
                       + ",\n".join(out) + "\n")
    print("wrote", fn)

export(65521, "test_a5_p65521.ms")
export(0, "test_a5_char0.ms")
