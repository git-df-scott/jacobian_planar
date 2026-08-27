"""Decide a walk's condition ideal (saturated by the Newton-polygon vertex
non-degeneracies).  Usage: verdict.py <pkl> <NPjson> <NQjson> [char] [ncond]"""
import json, pickle, sys, sympy as sp
import wgrade as W

def load(pkl, NP, NQ, ncond=None, qverts=True):
    d = pickle.load(open(pkl, "rb"))
    conds = [sp.sympify(c) for c in d["conds"]]
    if ncond: conds = conds[:ncond]
    assign = {sp.Symbol(k): sp.sympify(v) for k, v in d["assign"].items()}
    free = [sp.Symbol(s) for s in d["unassigned"]]
    nd = []
    for which, V in (("a", NP),) + ((("b", NQ),) if qverts else ()):
        for p in W.hull_vertices([tuple(q) for q in V]):
            if p == (0, 0): continue
            s = sp.Symbol(f"{which}_{p[0]}_{p[1]}")
            nd.append(sp.expand(assign.get(s, s)))
    return conds, free, nd

if __name__ == "__main__":
    pkl = sys.argv[1]
    T = json.load(open(sys.argv[2]))[int(sys.argv[3])]
    char = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    ncond = int(sys.argv[5]) if len(sys.argv) > 5 else None
    qv = (len(sys.argv) <= 6) or sys.argv[6] != "noq"
    conds, free, nd = load(pkl, T["NP"], T["NQ"], ncond, qverts=qv)
    gg = [g for g in (sys.argv[8].split(",") if len(sys.argv) > 8 else []) if g]
    for g in gg:                       # extra gauge slice, e.g. "a_8_14=1"
        v, val = g.split("=")
        conds = conds + [sp.Symbol(v) - sp.Integer(val)]
    if gg: print("  extra gauge:", gg)
    print(f"{T['tag']}\n  conditions {len(conds)}  free {len(free)}  "
          f"nondeg factors {len(nd)}  char {char}  Qvertices {qv}", flush=True)
    out, fn = W.singular_verdict(conds, free, nd, char=char,
                                 tag=pkl.split('.')[0] + f"_{ncond}_{qv}",
                                 timeout=int(sys.argv[7]) if len(sys.argv)>7 else 1800)
    print(out)
    print("[script]", fn)
