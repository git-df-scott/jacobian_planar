"""night12 v1 -- driver.

Order of operations per P (nothing is skipped, nothing is reordered):

  screens  S2 (cheap gcd composition screen) -> S1 (unimodular gradient,
           Groebner) -> S3 diagnostics.  A P failing S1 or S2 never reaches a
           mate matrix.
  SY       Shpilrain-Yu gradient-row reduction: COORDINATE / NON_COORDINATE.
  stages   Q-degree escalation Y -> C -> W, each decided EXACTLY over Q by
           exact.decide.  Escalation stops at the first stage that yields a
           mate.  Emptiness is never claimed beyond the stage actually tried:
           each stage records its own carrier and its own certificate.
  gate     a mate certified over Q whose P is SY-certified NON_COORDINATE is
           written to night12/HIT_<hash>/ and the run stops.
"""

import json
import os
import sys
import time
import hashlib
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import matekit as M
import carriers
import screens
import sy
import exact
import pool as poolmod

CAP = {"Y": 1500, "C": 1500, "W": 1500}
STAGES = ["Y", "C", "W"]


def phash(P):
    s = json.dumps(sorted((list(k), int(v)) for k, v in P.items()))
    return hashlib.sha256(s.encode()).hexdigest()[:12]


def pstr(P):
    return {("%d,%d" % k): int(v) for k, v in sorted(P.items())}


def general_carrier(P, stage, cap):
    """carrier for a P with no H (non-M1 pools): the stage-scaled Newton
    polygon of P, with the trivial directions Q -> Q + h(P) deflated by
    deleting the column at lead(P)^k for every power P^k that fits."""
    d = M.pdeg(P)
    D = {"Y": d - 1, "C": (3 * d) // 2, "W": 2 * d - 1}[stage]
    if D < 1:
        return [], {"stage": stage, "deg_Q_bound": D, "n_raw": 0,
                    "thin_t": 1, "n_used": 0, "deflated_kernel_dim": 0}
    base = list(P.keys()) + M.BASE
    verts = M._hull(sorted(set((p[0] * D, p[1] * D) for p in base)))
    S = []
    for a in range(D + 1):
        for b in range(D + 1 - a):
            if M._inside(verts, (a * d, b * d)):
                S.append((a, b))
    info = {"stage": stage, "deg_Q_bound": D, "n_raw": len(S), "thin_t": 1}
    t = 1
    keep = set(M.BASE)
    while len(S) > cap:
        t += 1
        S = sorted(set(p for p in S if p[0] % t == 0 and p[1] % t == 0) |
                   (keep & set(S)))
        info["thin_t"] = t
        if t > 40:
            break
    # Kernel deflation.  S2 (gcd(P_x,P_y) = 1) has already rejected every
    # proper composition P = h(R), so for a screened P the exact kernel
    # {Q : [P,Q] = 0} is Q[P].  Its part living on the carrier is spanned by
    # the powers P^k with supp(P^k) contained in S, and deleting the column at
    # lead(P)^k for exactly those k is a genuine quotient (the coefficients of
    # Q at those monomials are triangular in the c_k, so each Q on the carrier
    # has a unique representative with them zeroed).  A P^k that does NOT fit
    # the carrier contributes no kernel and must NOT be deflated -- deleting
    # its column would shrink the search space rather than quotient it.
    Sset = set(S)
    lead = max(P, key=lambda m: (m[0] + m[1], m[0]))
    drop = set()
    Pk = {(0, 0): 1}
    k = 0
    while k * d <= D:
        if not set(Pk).issubset(Sset):
            break
        drop.add((lead[0] * k, lead[1] * k))
        Pk = M.pmul(Pk, P)
        k += 1
    S = sorted(Sset - drop)
    info["n_used"] = len(S)
    info["deflated_kernel_dim"] = len(drop)
    return S, info


def carrier_for(item, stage):
    if item.get("H"):
        return carriers.carrier(item["H"], item["m"], stage, CAP[stage])
    return general_carrier(item["P"], stage, CAP[stage])


def screen_one(item):
    P = item["P"]
    t0 = time.time()
    r = screens.screen(P, t2=60, t1=90)
    return {"hash": phash(P), "family": item["family"], "profile": item["profile"],
            "deg_P": item["deg_P"], "n_supp_P": len(P),
            "screen_secs": round(time.time() - t0, 1), **r}


def pipeline_one(item):
    P = item["P"]
    h = phash(P)
    rec = {"hash": h, "family": item["family"], "profile": item["profile"],
           "deg_P": item["deg_P"], "n_supp_P": len(P), "P": pstr(P)}
    t0 = time.time()
    v, st = sy.certify(P)
    rec["SY_verdict"] = v
    rec["SY_nodes"] = st["nodes"]
    rec["SY_leaves"] = st["leaves"]
    rec["stages"] = []
    rec["outcome"] = "EMPTY_all_stages_tried"
    for stage in STAGES:
        S, info = carrier_for(item, stage)
        if not S:
            rec["stages"].append({**info, "verdict": "EMPTY_trivial_carrier"})
            continue
        ts = time.time()
        out, rows, Qd = exact.decide(P, S, want_lambda=True)
        out.update(info)
        out["secs"] = round(time.time() - ts, 1)
        rec["stages"].append(out)
        if out["verdict"] == "MATE_over_Q":
            rec["outcome"] = "MATE"
            rec["deg_Q"] = M.pdeg(Qd)
            rec["div_ordered"] = str(M.divisibility_ordered(M.pdeg(P), M.pdeg(Qd)))
            rec["Q"] = {("%d,%d" % k): [int(x.numerator), int(x.denominator)]
                        for k, x in sorted(Qd.items())}
            rec["bracket_is_one"] = bool(M.is_one(M.bracket(P, Qd)))
            break
        if out["verdict"] == "NOT_CERTIFIED":
            rec["outcome"] = "NOT_CERTIFIED_at_" + stage
    rec["hit"] = bool(rec["outcome"] == "MATE" and rec["SY_verdict"] == "NON_COORDINATE")
    rec["secs"] = round(time.time() - t0, 1)
    return rec


def main():
    phase = sys.argv[1] if len(sys.argv) > 1 else "all"

    if phase in ("all", "screen"):
        items = (poolmod.pool_M1(30) + poolmod.pool_M1L(20)
                 + poolmod.pool_HDC() + poolmod.pool_V0())
        print("screening %d P" % len(items), flush=True)
        with Pool(4) as p:
            res = p.map(screen_one, items, chunksize=1)
        json.dump(res, open(os.path.join(HERE, "v1_screens.json"), "w"), indent=1)
        cols = ["hash", "family", "profile", "deg_P", "n_supp_P", "S2", "S1",
                "places_at_infinity", "genus_newton", "lead_terms", "passed",
                "screen_secs", "S1_detail"]
        with open(os.path.join(HERE, "v1_screens.csv"), "w") as f:
            f.write(",".join(cols) + "\n")
            for r in res:
                f.write(",".join('"%s"' % str(r.get(c, "")).replace('"', "'")
                                 for c in cols) + "\n")
        print("screened. passed:", sum(1 for r in res if r["passed"]), flush=True)

    if phase in ("all", "pipe"):
        scr = {r["hash"]: r for r in
               json.load(open(os.path.join(HERE, "v1_screens.json")))}
        items = (poolmod.pool_M1(30) + poolmod.pool_M1L(20)
                 + poolmod.pool_HDC() + poolmod.pool_V0())
        order = {"M1": 0, "M1L": 1, "HDC": 2}
        passers = [it for it in items
                   if scr.get(phash(it["P"]), {}).get("passed")]
        seen = set()
        uniq = []
        for it in passers:
            hh = phash(it["P"])
            if hh in seen:
                continue
            seen.add(hh)
            uniq.append(it)
        uniq.sort(key=lambda it: (order.get(it["family"], 3), -it["deg_P"]))
        print("pipeline on %d screened-and-passed P" % len(uniq), flush=True)
        with Pool(4) as p:
            res = p.map(pipeline_one, uniq, chunksize=1)
        json.dump(res, open(os.path.join(HERE, "v1_records.json"), "w"), indent=1)
        os.makedirs(os.path.join(HERE, "V1_RECORDS"), exist_ok=True)
        for r in res:
            json.dump(r, open(os.path.join(HERE, "V1_RECORDS",
                                           r["hash"] + ".json"), "w"), indent=1)
        nhit = 0
        for r in res:
            if r["hit"]:
                d = os.path.join(HERE, "HIT_" + r["hash"])
                os.makedirs(d, exist_ok=True)
                json.dump(r, open(os.path.join(d, "record.json"), "w"), indent=1)
                nhit += 1
        print("pipeline done. P through pipeline: %d ; mates: %d ; HITs: %d"
              % (len(res), sum(1 for r in res if r["outcome"] == "MATE"), nhit),
              flush=True)


if __name__ == "__main__":
    main()
