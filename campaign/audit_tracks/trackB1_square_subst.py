#!/usr/bin/env python3
"""Substitute the PERFECT-SQUARE theorem S = A^2 into the pentagon system.

trackB1_THEOREM_S_square.md proves S must be a perfect square. With the system's
normalization S(0) = 1 we may take A = 1 + al1 z + al2 z^2, giving
  s_1_5 = 2 al1,  s_2_6 = al1^2 + 2 al2,  s_3_7 = 2 al1 al2,  s_4_8 = al2^2.
That is a codimension-2 cut on the top-edge data, applied BEFORE elimination.
"""
import json, hashlib
from fractions import Fraction

SRC = "trackB1_param_system.json"
OUT = "trackB1_square_system.json"

def mono_mul(m1, m2):
    d = dict(m1)
    for v, e in m2:
        d[v] = d.get(v, 0) + e
    return tuple(sorted(d.items()))

def padd(P, Q):
    for m, c in Q.items():
        P[m] = P.get(m, Fraction(0)) + c
        if P[m] == 0:
            del P[m]
    return P

def pmul(P, Q):
    out = {}
    for m1, c1 in P.items():
        for m2, c2 in Q.items():
            m = mono_mul(m1, m2)
            out[m] = out.get(m, Fraction(0)) + c1 * c2
            if out[m] == 0:
                del out[m]
    return out

AL1 = (("al_1", 1),)
AL2 = (("al_2", 1),)
SUB = {
    "s_1_5": {AL1: Fraction(2)},
    "s_2_6": {mono_mul(AL1, AL1): Fraction(1), AL2: Fraction(2)},
    "s_3_7": {mono_mul(AL1, AL2): Fraction(2)},
    "s_4_8": {mono_mul(AL2, AL2): Fraction(1)},
}

data = json.load(open(SRC))
new_eqs = []
for ser in data["equations"]:
    acc = {}
    for mono, (num, den) in ser["terms"]:
        term = {(): Fraction(num, den)}
        for v, e in mono:
            factor = SUB.get(v, {((v, 1),): Fraction(1)})
            for _ in range(e):
                term = pmul(term, factor)
        padd(acc, term)
    if acc:
        new_eqs.append({"bracket_point": ser["bracket_point"],
                        "terms": [[list(m), [c.numerator, c.denominator]]
                                  for m, c in sorted(acc.items())]})
newvars = sorted({v for e in new_eqs for t in e["terms"] for v, _ in t[0]})
nz = [x for x in data["nonzero"] if not x.startswith("s_")] + ["al_2"]
out = {"meta": {"source": "Track B1 + PERFECT-SQUARE theorem: S = A^2, A = 1+al_1 z+al_2 z^2",
                "input_system": SRC, "input_hash": data["content_hash"],
                "theorem": "trackB1_THEOREM_S_square.md"},
       "variables": newvars, "nonzero": nz, "equations": new_eqs}
blob = json.dumps({k: out[k] for k in ("variables", "nonzero", "equations")},
                  sort_keys=True).encode()
out["content_hash"] = hashlib.sha256(blob).hexdigest()
json.dump(out, open(OUT, "w"))
print(f"{SRC}: {len(data['variables'])} vars / {len(data['equations'])} eqs")
print(f"{OUT}: {len(newvars)} vars / {len(new_eqs)} eqs   hash {out['content_hash'][:16]}")
print("nonzero:", nz)
