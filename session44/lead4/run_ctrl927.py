import json
import walk_branch as WB
t = json.load(open("trackD_targets_ctrl927.json"))[0]
print("CONTROL:", t["tag"], flush=True)
res, info = WB.analyse(t["NP"], t["NQ"], t["r"])
from collections import Counter
print("branches:", Counter(r[0] for r in res))
kinds = {r[0] for r in res}
if kinds and kinds <= {"EMPTY"}:
    print("*** CONTROL PASS: instrument reproduces GGHV Cor 5.7 (EMPTY) ***")
else:
    print("*** CONTROL FAIL: instrument reports", kinds, "on a case the",
          "literature proved impossible -- verdicts on the open case are",
          "NOT trustworthy until this is fixed ***")
