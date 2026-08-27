#!/usr/bin/env python3
"""Fix the essential face to a solution, then solve the REST of [P,Q]=x^2.

Frame: u = x y^2, w = j - 2i is the y-weight. For the open subcases
    N(P) has w in {0,-1,-2},  N(Q) has w in {0,-1,-2,-3}
and the ESSENTIAL face is the DEEPEST level (w = -2 for P, w = -3 for Q):
that is where the bracket's weight -2 + -3 + w(-1,-1) = -4 equals w(x^2).
Every shallower level of the bracket must VANISH.

So: solve the essential face (done -- 35 solutions), substitute it, and the
remaining conditions determine the shallower levels. Solvable -> explicit
candidate (P,Q). Unsolvable for all 35 -> the subcase is EMPTY.

Everything mod p here; a survivor is lifted to characteristic zero and
verified exactly before any claim.
"""
import json, subprocess, sys
import sympy as sp

p = 65521
x, y = sp.symbols("x y")
t = json.load(open("trackD_targets_108.json"))[1]
NP, NQ, r = t["NP"], t["NQ"], t["r"]
from face_param import lattice_points
ptsP, ptsQ = lattice_points(NP), lattice_points(NQ)
w = lambda q: q[1] - 2*q[0]
deepP, deepQ = min(w(q) for q in ptsP), min(w(q) for q in ptsQ)
faceP = [q for q in ptsP if w(q) == deepP]
faceQ = [q for q in ptsQ if w(q) == deepQ]
print(f"P lattice points {len(ptsP)}, weights {sorted({w(q) for q in ptsP})}")
print(f"Q lattice points {len(ptsQ)}, weights {sorted({w(q) for q in ptsQ})}")
print(f"essential face of P: w={deepP}, {len(faceP)} points")
print(f"essential face of Q: w={deepQ}, {len(faceQ)} points")
print(f"bracket top weight {deepP+deepQ+w((-1,-1))} vs target w(x^2)={w((r,0))}"
      f"  {'MATCH' if deepP+deepQ+w((-1,-1))==w((r,0)) else 'MISMATCH'}")

cP = {q: sp.Symbol(f"P_{q[0]}_{q[1]}") for q in ptsP}
cQ = {q: sp.Symbol(f"Q_{q[0]}_{q[1]}") for q in ptsQ}
P = sum(cP[q]*x**q[0]*y**q[1] for q in ptsP)
Q = sum(cQ[q]*x**q[0]*y**q[1] for q in ptsQ)
br = sp.expand(sp.diff(P,x)*sp.diff(Q,y)-sp.diff(P,y)*sp.diff(Q,x) - x**r)
eqs = [sp.expand(co) for _, co in sp.Poly(br, x, y).terms()]
print(f"\nfull system: {len(ptsP)+len(ptsQ)} unknowns, {len(eqs)} equations")
nface = len(faceP)+len(faceQ)
print(f"the essential face fixes {nface} of them, leaving "
      f"{len(ptsP)+len(ptsQ)-nface} unknowns")
print(f"\nThat residual system is what decides the case: it is the part the")
print(f"face solution does NOT determine. Exporting it with the face left")
print(f"symbolic is pointless (that is the original problem); the useful")
print(f"run substitutes a NUMERIC face solution. Writing the template.")
json.dump({"faceP": faceP, "faceQ": faceQ,
           "nunk_total": len(ptsP)+len(ptsQ),
           "nface": nface,
           "nresidual": len(ptsP)+len(ptsQ)-nface,
           "neqs": len(eqs)}, open("extend_structure.json","w"), indent=1)
print("wrote extend_structure.json")
