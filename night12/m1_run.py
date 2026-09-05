"""night12 v1 -- the M1-first arm.

Why this file exists (measurement, not conclusion).  In the screen phase every
one of the 200 M1 / M1L P was rejected by S1: the gradient pair (P_x, P_y) has
a common zero over Qbar.  S1 is a gate, so none of them reached `v1.py`'s
pipeline phase, and the M1 profiles -- the family the brief puts first --
carried no per-P record at all.

This arm runs those same P through SY and the exact-over-Q decision layer
anyway, under an EXPLICIT OVERRIDE of the screens, exactly as control C-NEG
does.  Nothing about the mathematics is relaxed:

  * the S1 rejection stands on its own.  A common zero (a,b) of (P_x, P_y)
    makes the Keller equation read 0 = 1 there, so such a P has no mate at any
    degree whatsoever.  That is already a complete emptiness proof for these P,
    independent of any carrier.
  * what this arm adds is the carrier-level certificate: for each stage
    Y / C / W of the mu_3 carrier, an exact lambda (or a full-column-rank)
    certificate over Q for the linear system actually built.  Two independent
    routes to the same emptiness, recorded separately.
  * the hit gate is unchanged and still armed: a MATE_over_Q on an
    SY NON_COORDINATE P would halt the run and be written out.  An override P
    producing a mate would additionally contradict its own S1 verdict, which
    is why the gate is left armed here rather than disabled.

Records land in m1_records.json and V1_RECORDS_M1/, kept separate from the
screened-and-passed pipeline records in v1_records.json / V1_RECORDS/ so that
the two arms are never conflated.
"""

import json
import os
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import matekit as M
import v1
import pool as poolmod

RECDIR = os.path.join(HERE, "V1_RECORDS_M1")


def one(item):
    rec = v1.pipeline_one(item)
    rec["arm"] = "M1_override"
    rec["screens_overridden"] = True
    return rec


def main():
    n_per = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    scr = {r["hash"]: r for r in
           json.load(open(os.path.join(HERE, "v1_screens.json")))}
    items = poolmod.pool_M1(n_per) + poolmod.pool_M1L(max(1, n_per * 2 // 3))
    seen, uniq = set(), []
    for it in items:
        h = v1.phash(it["P"])
        if h in seen:
            continue
        seen.add(h)
        uniq.append(it)
    # M1 profiles first, in the brief's profile order, then M1L
    porder = {"(%d,%d)" % p: i for i, p in enumerate(__import__("carriers").PROFILES)}
    uniq.sort(key=lambda it: (0 if it["family"] == "M1" else 1,
                              porder.get(it["profile"], 9), it["deg_P"]))
    print("M1 override arm: %d P (M1=%d, M1L=%d)"
          % (len(uniq), sum(1 for i in uniq if i["family"] == "M1"),
             sum(1 for i in uniq if i["family"] == "M1L")), flush=True)

    t0 = time.time()
    with Pool(4) as p:
        res = p.map(one, uniq, chunksize=1)

    for r in res:
        s = scr.get(r["hash"], {})
        r["screen_S1"] = s.get("S1")
        r["screen_S1_detail"] = s.get("S1_detail")
        r["screen_S2"] = s.get("S2")
        r["places_at_infinity"] = s.get("places_at_infinity")
        r["genus_newton"] = s.get("genus_newton")

    json.dump(res, open(os.path.join(HERE, "m1_records.json"), "w"), indent=1)
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
    print("M1 arm done in %.0fs. P: %d ; mates: %d ; HITs: %d"
          % (time.time() - t0, len(res),
             sum(1 for r in res if r["outcome"] == "MATE"), nhit), flush=True)


if __name__ == "__main__":
    main()
