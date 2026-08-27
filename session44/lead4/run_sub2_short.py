"""Subcase 2: conditions from the four lowest w-levels only (a SUBSET of the
full system -- an EMPTY verdict from a subset is still EMPTY)."""
import json, time, sympy as sp
import wgrade as W
T=json.load(open("trackD_targets_108.json"))[1]
NP=[tuple(p) for p in T["NP"]]; NQ=[tuple(p) for p in T["NQ"]]
wk=W.Walk(NP,NQ,T["r"],(-2,1),gauge=[("P",(1,0),1)],tdir=(1,2))
t0=time.time()
wk.run(nlevels=4, dump="sub2_short.pkl")
print(f"done {time.time()-t0:.0f}s  conds={len(wk.conds)} "
      f"free={len(wk.unassigned())}", flush=True)
print("free:", [str(s) for s in wk.unassigned()])
