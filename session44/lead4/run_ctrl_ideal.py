"""Control for walk_ideal: the (9,27) shape GGHV PROVED impossible.

The instrument must return EMPTY here (ideal contains 1). Anything else
invalidates every verdict walk_ideal gives on the open case.
"""
import json
import walk_ideal as WI
t = json.load(open("trackD_targets_ctrl927.json"))[0]
print("CONTROL:", t["tag"], flush=True)
v, rels, assign = WI.analyse(t["NP"], t["NQ"], t["r"])
print(f"\nverdict: {v}   relations: {len(rels)}")
if v == "EMPTY":
    print("*** CONTROL PASS: reproduces GGHV Cor 5.7 (EMPTY) ***")
else:
    print("*** CONTROL INCONCLUSIVE/FAIL: got", v, "on a case the literature")
    print("    proved impossible. Verdicts on the open case are NOT")
    print("    trustworthy unless this returns EMPTY. ***")
