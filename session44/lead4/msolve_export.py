"""Export a walk's conditions (saturated) for msolve."""
import json, pickle, sys, sympy as sp
import wgrade as W
from verdict import load
pkl, tj, idx, char = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
out = sys.argv[5]
gg = [g for g in (sys.argv[6].split(",") if len(sys.argv) > 6 else []) if g]
T = json.load(open(tj))[idx]
conds, free, nd = load(pkl, T["NP"], T["NQ"])
for g in gg:
    v, val = g.split("="); conds.append(sp.Symbol(v) - sp.Integer(val))
zz = sp.Symbol("zz")
prod = sp.Integer(1)
for n in nd:
    prod *= n
conds.append(sp.expand(zz*prod - 1))
allv = sorted({s for c in conds for s in c.free_symbols}, key=str)
def cv(e):
    e = sp.expand(e)
    p = sp.Poly(e, *allv)
    den = sp.ilcm(1, *[sp.denom(c) for c in p.coeffs()])
    return str(sp.expand(e*den)).replace("**", "^")
open(out, "w").write(",".join(str(v) for v in allv) + f"\n{char}\n"
                    + ",\n".join(cv(c) for c in conds) + "\n")
print(out, len(allv), "vars", len(conds), "eqs")
