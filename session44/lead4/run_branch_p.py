import json, sys
import walk_branch as WB
p = int(sys.argv[1]); idx = int(sys.argv[2])
WB.MODP = p
t = json.load(open("trackD_targets_108.json"))[idx]
print(f"MOD-P DESCENT p={p}: {t['tag']}", flush=True)
res, info = WB.analyse(t["NP"], t["NQ"], t["r"])
from collections import Counter
print("branches:", Counter(r[0] for r in res))
for kind, data, hist in res:
    if kind.startswith("CANDIDATE"):
        print("*** CANDIDATE (mod p only -- must be lifted and verified "
              "exactly before it means anything) ***")
        print("  history:", hist[:8])
