"""Graded descent on the VALIDATION target (Singular pipeline: EMPTY)."""
import json, time, pickle, sympy as sp
import wgrade as W
T = json.load(open("trackD_targets_validate.json"))[0]
NP=[tuple(p) for p in T["NP"]]; NQ=[tuple(p) for p in T["NQ"]]
print("VALIDATION target:", T["tag"])
print("  independent instrument (Singular/facstd, mod 65521 and 65539): EMPTY")
print("  cands:", W.weight_candidates(NP,NQ), flush=True)
wk = W.Walk(NP, NQ, T["r"], (1,-2), gauge=[("P",(24,9),1), ("Q",(32,12),1)])
t0=time.time()
conds = wk.run(order="down", dump="val_walk_partial.pkl")
print(f"\nwalk done in {time.time()-t0:.0f}s: {len(conds)} conditions, "
      f"{len(wk.unassigned())} unknowns left", flush=True)
pickle.dump({"conds":[sp.srepr(c) for c in conds],
             "unassigned":[str(s) for s in wk.unassigned()],
             "assign":{str(k):sp.srepr(v) for k,v in wk.assign.items()}},
            open("val_walk2.pkl","wb"))
