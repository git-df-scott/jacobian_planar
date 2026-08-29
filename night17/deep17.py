"""night17 -- deeper mate escalation on the small survivors.

The brief's floor is deg Q <= 2 deg P.  For the survivors of degree <= 7 the
carrier is small enough to push to 3 deg P and 4 deg P, so that is done here;
every EMPTY is a lambda certificate solved and verified exactly over Q.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from fractions import Fraction as F                        # noqa: E402
import pk17 as pk                                          # noqa: E402
import mate17 as MT                                        # noqa: E402

import sweep17 as SW                                       # noqa: E402


INSTANCES = [
    ("H3", SW.he_instance(1, 0, [1, 1], 2)[0]),
    ("H4", SW.he_instance(1, 1, [1, 1, 1], 1)[0]),
    ("H5", SW.he_instance(2, 0, [1, 0, 1, 1], 3)[0]),
    ("E1a", SW.se_instance(1, 0, 1, [(0, 3)], 2)),
    ("E1b", SW.se_instance(2, 1, 3, [(1, 3)], 2)),
    ("E4", SW.se_instance(1, 0, 1, [(0, 5)], 2)),
    ("E7", SW.se_instance(1, 0, 1, [(0, 4)], 3)),
    ("V1", SW.se_instance(1, 0, 1, [(0, 2)], 1, swap=True)),
    ("V2", SW.se_instance(1, 0, 1, [(0, 3)], 2, swap=True)),
    ("V3", SW.se_instance(1, 0, 1, [(0, 5)], 2, swap=True)),
    ("V4", SW.se_instance(1, 0, 1, [(0, 4)], 3, swap=True)),
    ("M1", SW.shear(SW.he_instance(1, 0, [1, 1], 2)[0], [0, 1, 1], None)),
    ("M3", SW.shear(SW.se_instance(1, 0, 1, [(0, 3)], 2), None, [0, 1])),
]

res = []
for sid, P in INSTANCES:
    d = pk.tdeg(P)
    if d > 7:
        continue
    degs = tuple(sorted({2 * d, 3 * d, 4 * d}))
    r = MT.solve(P, max_cols=2200, degs=degs)
    hit = r["verdict"] == "MATE_over_Q"
    print("%-4s deg %-2d  %-28s  %s" % (sid, d, r["verdict"],
                                        ";".join("D=%s:%s" % (s.get("deg_Q_bound"),
                                                              s.get("verdict"))
                                                 for s in r["stages"])))
    sys.stdout.flush()
    if hit:
        print("*** A MATE SYSTEM WAS CONSISTENT: %s ***" % sid)
    res.append({"instance": sid, "hash": SW.phash(P), "deg": d,
                "P": pk.to_str(P), "degs": list(degs), "result": r})

json.dump(res, open(os.path.join(HERE, "deep17.json"), "w"), indent=1, default=str)
print("deep escalation done: %d instances, mates found: %d"
      % (len(res), sum(1 for r in res if r["result"]["verdict"] == "MATE_over_Q")))
