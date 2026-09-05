"""night12 -- mate search driver.

Per P: build the exact linear system for Q on a bounded support, decide
consistency over F_999983 and F_1000003, and on dual-prime consistency
attempt an exact rational solve followed by an exact bracket verification.

Nothing here is a conclusion; every field is a measurement and carries the
ring it was measured in.
"""

import json
import os
import sys
import time
import hashlib
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matekit as M
import ansatz

HERE = os.path.dirname(os.path.abspath(__file__))
CAP_FULL = 4000     # the design cap on the similarity support
CAP_WORK = 1200     # further computational cap (recorded separately)


def parse_P(d):
    return {tuple(int(t) for t in k.split(",")): v for k, v in d["P"].items()}


def phash(P):
    s = json.dumps(sorted((list(k), int(v)) for k, v in P.items()))
    return hashlib.sha256(s.encode()).hexdigest()[:12]


def run_one(rec):
    Praw = rec["P"]
    P = Praw if all(isinstance(k, tuple) for k in Praw) else parse_P(rec)
    rec = {k: v for k, v in rec.items() if k != "P"}
    rec["P"] = {("%d,%d" % k): int(v) for k, v in sorted(P.items())}
    t0 = time.time()
    S, info = M.q_support(P, cap_full=CAP_FULL, cap_work=CAP_WORK)
    rows, _ = M.build_system(P, S)
    n = len(S)
    out = dict(rec)
    out["hash"] = phash(P)
    out["n_supp_P"] = len(P)
    out["has_linear_term"] = int(((1, 0) in P) or ((0, 1) in P))
    out.update({
        "n_full_support": info["n_full"],
        "thin_k": info["thin_k"],
        "n_unknowns": n,
        "cap_full": CAP_FULL,
        "cap_work": CAP_WORK,
        "deg_Q_max": info["deg_Q_max"],
        "n_rows_nonzero": len(rows),
    })
    verdicts = {}
    for p in M.PRIMES:
        r = M.consistency_mod_p(rows, n, p, seed=20260831)
        verdicts[p] = r
        out["rank_A_p%d" % p] = r["rank_A"]
        out["rank_Ae_p%d" % p] = r["rank_Ae"]
        out["consistent_p%d" % p] = int(r["consistent"])
        out["nullity_p%d" % p] = n - r["rank_A"]
    dual = all(verdicts[p]["consistent"] for p in M.PRIMES)
    out["dual_prime_consistent"] = int(dual)
    out["exact_status"] = "not_attempted"
    out["deg_Q"] = -1
    out["div_ordered"] = ""
    out["Q"] = None
    if dual:
        piv = verdicts[M.P1]["pivcols"]
        cols = list(range(n)) if n <= 500 else piv
        Qd, st = M.exact_solve(rows, n, S, cols)
        if Qd is None and cols is not piv:
            out["exact_status"] = st
        elif Qd is None:
            Qd, st = M.exact_solve(rows, n, S, list(range(n)))
            out["exact_status"] = st
        if Qd is not None:
            B = M.bracket(P, Qd)
            ok = M.is_one(B)
            out["exact_status"] = "verified_bracket_eq_1" if ok else "solve_did_not_verify"
            if ok:
                dq = M.pdeg(Qd)
                out["deg_Q"] = dq
                do = M.divisibility_ordered(M.pdeg(P), dq)
                out["div_ordered"] = str(do)
                out["Q"] = {("%d,%d" % k): [int(v.numerator), int(v.denominator)]
                            for k, v in sorted(Qd.items())}
    out["secs"] = round(time.time() - t0, 2)
    return out


def main():
    recs = ansatz.build_all()
    with Pool(4) as pool:
        res = pool.map(run_one, recs, chunksize=1)
    with open(os.path.join(HERE, "mate_search.json"), "w") as f:
        json.dump(res, f, indent=1)
    cols = ["hash", "arm", "tag", "deg", "n_supp_P", "has_linear_term",
            "n_full_support", "thin_k", "n_unknowns", "deg_Q_max",
            "n_rows_nonzero", "rank_A_p999983", "rank_Ae_p999983",
            "nullity_p999983", "consistent_p999983", "rank_A_p1000003",
            "rank_Ae_p1000003", "nullity_p1000003", "consistent_p1000003",
            "dual_prime_consistent", "exact_status", "deg_Q", "div_ordered",
            "secs"]
    with open(os.path.join(HERE, "mate_search.csv"), "w") as f:
        f.write(",".join(cols) + "\n")
        for r in res:
            f.write(",".join(str(r.get(c, "")) for c in cols) + "\n")

    # halt-and-commit: any main-arm P with an exactly verified mate whose
    # degree pair is not divisibility-ordered
    nhits = 0
    for r in res:
        if r["exact_status"] != "verified_bracket_eq_1":
            continue
        flag = (r["arm"] == "main" and r["div_ordered"] == "False")
        d = os.path.join(HERE, ("HIT_%s" % r["hash"]) if flag else "VERIFIED")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "%s.json" % r["hash"]), "w") as f:
            json.dump(r, f, indent=1)
        nhits += 1 if flag else 0
    print("P swept: %d ; exactly verified mates: %d ; main-arm non-divisibility-ordered: %d"
          % (len(res), sum(1 for r in res if r["exact_status"] == "verified_bracket_eq_1"), nhits))


if __name__ == "__main__":
    main()
