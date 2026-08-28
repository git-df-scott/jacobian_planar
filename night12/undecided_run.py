"""night12 v1 -- the undecided arm.

The screen phase ran S1 with a 90 s budget under 4-way parallelism.  22 P came
back `timeout`, which is UNDECIDED: neither passed nor rejected.  `v1.py`
selects its pipeline by the `passed` flag, so all 22 fell out of the run with
no recorded verdict of any kind.

9 of the 22 are M1 and are covered by `m1_run.py`.  This file covers the
remaining 13 (V0 families), by the same route: SY plus the exact-over-Q
decision layer at stages Y / C / W, under an explicit override of the screens.

What the resulting verdict does and does not say.  The certificate is
carrier-level and exact over Q: it decides the mate system on the carrier that
stage actually built, and nothing beyond it.  It is INDEPENDENT of S1 -- it
neither assumes nor establishes that the gradient pair is unimodular -- so it
stands whichever way S1 would have gone had it been given more time.  S1
itself is separately re-run by `s1_retry.py`.

The hit gate stays armed.  Records go to `undecided_records.json` and
`V1_RECORDS_UNDECIDED/`, kept apart from both other arms.
"""

import json
import os
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import v1
import pool as poolmod

RECDIR = os.path.join(HERE, "V1_RECORDS_UNDECIDED")


def one(item):
    rec = v1.pipeline_one(item)
    rec["arm"] = "undecided_override"
    rec["screens_overridden"] = True
    return rec


def main():
    scr = {r["hash"]: r for r in
           json.load(open(os.path.join(HERE, "v1_screens.json")))}
    todo = {h for h, r in scr.items()
            if r["S1"] == "timeout" and not r["family"].startswith("M1")}
    items = (poolmod.pool_M1(30) + poolmod.pool_M1L(20)
             + poolmod.pool_HDC() + poolmod.pool_V0())
    by = {}
    for it in items:
        by.setdefault(v1.phash(it["P"]), it)
    uniq = [by[h] for h in sorted(todo) if h in by]
    uniq.sort(key=lambda it: -it["deg_P"])
    print("undecided arm: %d P (non-M1 S1 timeouts)" % len(uniq), flush=True)

    t0 = time.time()
    with Pool(4) as p:
        res = p.map(one, uniq, chunksize=1)

    for r in res:
        s = scr.get(r["hash"], {})
        r["screen_S1"] = s.get("S1")
        r["screen_S2"] = s.get("S2")
        r["places_at_infinity"] = s.get("places_at_infinity")
        r["genus_newton"] = s.get("genus_newton")

    json.dump(res, open(os.path.join(HERE, "undecided_records.json"), "w"), indent=1)
    os.makedirs(RECDIR, exist_ok=True)
    for r in res:
        json.dump(r, open(os.path.join(RECDIR, r["hash"] + ".json"), "w"), indent=1)

    nhit = 0
    for r in res:
        if r["hit"]:
            d = os.path.join(HERE, "HIT_" + r["hash"])
            os.makedirs(d, exist_ok=True)
            json.dump(r, open(os.path.join(d, "record.json"), "w"), indent=1)
            nhit += 1
    print("undecided arm done in %.0fs. P: %d ; mates: %d ; HITs: %d"
          % (time.time() - t0, len(res),
             sum(1 for r in res if r["outcome"] == "MATE"), nhit), flush=True)


if __name__ == "__main__":
    main()
