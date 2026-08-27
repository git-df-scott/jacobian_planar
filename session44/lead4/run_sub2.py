"""Graded descent on the open (72,108) subcase 2."""
import json, time, sympy as sp
import wgrade as W
T = json.load(open("trackD_targets_108.json"))[1]
NP = [tuple(p) for p in T["NP"]]; NQ = [tuple(p) for p in T["NQ"]]
print("target:", T["tag"])
print("cands:", W.weight_candidates(NP, NQ))
wk = Walk = W.Walk(NP, NQ, T["r"], (-2, 1), gauge=[((1, 0), 1)])
t0 = time.time()
conds = wk.run()
print(f"\nwalk done in {time.time()-t0:.0f}s: {len(conds)} conditions, "
      f"{len(wk.unassigned())} unknowns left")
print("unknowns:", [str(s) for s in wk.unassigned()])
import pickle
pickle.dump({"conds": [sp.srepr(c) for c in conds],
             "assign": {str(k): sp.srepr(v) for k, v in wk.assign.items()},
             "unassigned": [str(s) for s in wk.unassigned()]},
            open("sub2_walk.pkl", "wb"))
