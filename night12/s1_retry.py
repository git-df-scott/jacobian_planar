"""night12 v1 -- gap fill: re-decide the P whose S1 timed out in the screen phase.

The screen phase ran S1 with t1 = 90s under 4-way parallelism.  Every P that
returned S1 = timeout is UNDECIDED, not rejected: it is neither in the pool
that reached the pipeline nor certified as screened out.  This script re-runs
S1 alone on exactly those P with a long serial budget, so that no P is left
undecided by the screens.  Nothing else changes: same S1 predicate, same
Singular ring, same code path (screens.S1_unimodular).
"""

import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import screens, v1
import pool as poolmod

T1 = int(sys.argv[1]) if len(sys.argv) > 1 else 3600


def main():
    scr = json.load(open(os.path.join(HERE, "v1_screens.json")))
    todo = {r["hash"] for r in scr if r["S1"] == "timeout"}
    items = (poolmod.pool_M1(30) + poolmod.pool_M1L(20)
             + poolmod.pool_HDC() + poolmod.pool_V0())
    by = {}
    for it in items:
        by.setdefault(v1.phash(it["P"]), it)
    print("S1 timeouts to re-decide: %d (budget %ds each)" % (len(todo), T1), flush=True)
    out = []
    for h in sorted(todo):
        it = by[h]
        t0 = time.time()
        v, d = screens.S1_unimodular(it["P"], T1)
        dt = round(time.time() - t0, 1)
        print("  %s %-24s deg=%-4d -> S1=%-8s %-55s (%.1fs)"
              % (h, it["family"], it["deg_P"], v, d, dt), flush=True)
        out.append({"hash": h, "family": it["family"], "profile": it["profile"],
                    "deg_P": it["deg_P"], "S1_retry": v, "S1_retry_detail": d,
                    "S1_retry_secs": dt, "budget_secs": T1})
    json.dump(out, open(os.path.join(HERE, "s1_retry.json"), "w"), indent=1)
    # fold the resolved verdicts back into the screen table
    res = {r["hash"]: r for r in out}
    nch = 0
    for r in scr:
        q = res.get(r["hash"])
        if q and q["S1_retry"] != "timeout":
            r["S1"] = q["S1_retry"]
            r["S1_detail"] = q["S1_retry_detail"] + "  [re-decided, budget %ds]" % T1
            r["passed"] = (r["S1"] == "pass" and r["S2"] == "pass")
            nch += 1
    json.dump(scr, open(os.path.join(HERE, "v1_screens.json"), "w"), indent=1)
    print("re-decided %d of %d; screen table updated. passed now: %d"
          % (nch, len(todo), sum(1 for r in scr if r["passed"])), flush=True)


if __name__ == "__main__":
    main()
