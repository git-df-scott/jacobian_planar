"""Validate walk_ideal against a target Singular independently called EMPTY."""
import json, time
import walk_ideal as WI
t = json.load(open("trackD_targets_validate.json"))[0]
print("VALIDATION:", t["tag"])
print("  Singular (independent instrument) verdict: EMPTY")
t0 = time.time()
v, rels, assign = WI.analyse(t["NP"], t["NQ"], t["r"])
print(f"\nwalk_ideal verdict: {v}   ({time.time()-t0:.0f}s, "
      f"{len(rels)} relations)")
if v == "EMPTY":
    print("*** AGREES with Singular -- instrument validated on this case ***")
else:
    print("*** DISAGREES: walk_ideal says", v, "where Singular says EMPTY.")
    print("    Either walk_ideal is incomplete (it only walks driver levels")
    print("    and may not reach the contradiction) or it is WRONG.")
    print("    Its verdicts on the open case cannot be trusted until this")
    print("    is understood. ***")
