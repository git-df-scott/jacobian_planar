"""night15 -- exact mate solve on the survivors of the period screen.

Reads screen15_records.json, takes every P whose period verdict is VANISHING
(and, for completeness, the UNRESOLVED / NOT_SCREENED ones, which are NOT
survivors but are reported separately), and runs mate15.solve on them.

HIT GATE.  If any stage returns MATE_over_Q the reconstructed Q is verified by
expanding [P,Q] - 1 coefficientwise over Q, BOTH non-coordinate witnesses are
re-run on P, and everything is written to night15/HIT_<hash>/.
"""

import json
import os
import sys
import time
from fractions import Fraction as F

import pk15 as P14
import sy15
import fib15
import cert15
import mate15

HERE = os.path.dirname(os.path.abspath(__file__))


def load(path="screen15_records.json"):
    with open(os.path.join(HERE, path)) as fh:
        return json.load(fh)


def P_of(rec):
    return P14.clean({tuple(int(t) for t in k.split(",")): F(v[0], v[1])
                      for k, v in rec["P"].items()})


def main():
    recs = load()
    surv = [r for r in recs if r.get("period_verdict") == "VANISHING"]
    other = [r for r in recs if r.get("period_verdict") in ("UNRESOLVED", "NOT_SCREENED")]
    print("survivors (PERIODS-VANISHING): %d ; not decided by the screen: %d"
          % (len(surv), len(other)))
    out = []
    for i, r in enumerate(sorted(surv, key=lambda z: z["deg_P"])):
        P = P_of(r)
        print("\n[%d/%d] %s deg=%d dy=%d  %s" % (i + 1, len(surv), r["hash"],
                                                 r["deg_P"], r["deg_y"], r["label"]))
        sys.stdout.flush()
        t = time.time()
        res = mate15.solve(P)
        res["hash"] = r["hash"]
        res["label"] = r["label"]
        res["deg_P"] = r["deg_P"]
        res["secs"] = round(time.time() - t, 1)
        out.append(res)
        print("    => %s (%.0fs)" % (res["verdict"], res["secs"]))
        sys.stdout.flush()
        if res["verdict"] == "MATE_over_Q":
            d = os.path.join(HERE, "HIT_" + r["hash"])
            os.makedirs(d, exist_ok=True)
            sy, st = sy15.certify(P, node_budget=400000)
            fv, fres = fib15.screen(P, lams=(0, 1, -1), timeout=180)
            u = cert15.bezout_unimodular(P)
            json.dump({"screen_record": r, "mate": res,
                       "recheck": {"SY": sy, "SY_stats": st,
                                   "FIB": fv, "FIB_detail": fres,
                                   "U_bezout": u},
                       "P_str": P14.to_str(P)},
                      open(os.path.join(d, "hit.json"), "w"), indent=1, default=str)
            print("HIT written to", d)
            with open(os.path.join(HERE, "survivors15.json"), "w") as fh:
                json.dump(out, fh, indent=1, default=str)
            return
        with open(os.path.join(HERE, "survivors15.json"), "w") as fh:
            json.dump(out, fh, indent=1, default=str)
    with open(os.path.join(HERE, "survivors15.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    from collections import Counter
    print("\nMATE VERDICTS:", Counter(o["verdict"] for o in out))


if __name__ == "__main__":
    main()
