"""night12 v1 -- independent re-verification of every certificate emitted.

This file trusts nothing in the records except the raw data: the `P` (as its
hash into the pools), the stage name, the stored lambda vector, and the stored
`Q`.  It rebuilds the carrier and the Keller system from scratch and re-checks
each certificate over `Q` with `Fraction` arithmetic, without calling
`exact.decide`.  Its purpose is to catch a certificate that was recorded but
does not actually hold.

What is re-checked, per certificate type:

  E1 `lambda_exact`      rebuild the carrier for that stage and the row
                         dictionary of the Keller system, then check
                         `lambda^T A = 0` on EVERY column and
                         `lambda^T e_00 = 1`, over Q.

  E3 `exact_solution`    expand `P_x Q_y - P_y Q_x - 1` coefficientwise from
                         the stored rational Q and check every coefficient is
                         zero, over Q.

  E2 `rank_full_column_exact`
                         not re-derivable from the record alone (it is a rank
                         statement at the scheduling prime, whose validity is
                         the lower-bound argument in MATE_V1.md section E2).
                         Counted and reported, not re-checked here.
"""

import collections
import json
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import matekit as M
import v1
import pool as poolmod

ARMS = [("pipeline", "v1_records.json"),
        ("M1 override", "m1_records.json"),
        ("undecided override", "undecided_records.json")]


def build_index():
    items = (poolmod.pool_M1(30) + poolmod.pool_M1L(20)
             + poolmod.pool_HDC() + poolmod.pool_V0())
    by = {}
    for it in items:
        by.setdefault(v1.phash(it["P"]), it)
    return by


def unpack_P(rec):
    return {tuple(int(t) for t in k.split(",")): int(v)
            for k, v in rec["P"].items()}


def unpack_Q(rec):
    return {tuple(int(t) for t in k.split(",")): Fraction(v[0], v[1])
            for k, v in rec["Q"].items()}


def check_lambda(item, stage, lamvec):
    """rebuild carrier + system, re-check lambda^T A = 0 and lambda^T e = 1."""
    S, info = v1.carrier_for(item, stage)
    if not S:
        return False, "empty carrier"
    rows, _ = M.build_system(item["P"], S)
    lam = {(int(k[0]), int(k[1])): Fraction(int(v[0]), int(v[1]))
           for k, v in lamvec}
    acc = {}
    for key, wt in lam.items():
        for j, val in rows.get(key, {}).items():
            acc[j] = acc.get(j, Fraction(0)) + wt * Fraction(val)
    nz = [j for j, v in acc.items() if v != 0]
    if nz:
        return False, "lambda^T A nonzero on %d columns" % len(nz)
    if lam.get((0, 0), Fraction(0)) != 1:
        return False, "lambda^T e_00 = %s, not 1" % lam.get((0, 0))
    return True, "ok (%d columns checked)" % len(S)


def main():
    by = build_index()
    tally = collections.Counter()
    fails = []

    for armname, fn in ARMS:
        path = os.path.join(HERE, fn)
        if not os.path.exists(path):
            continue
        recs = json.load(open(path))
        for r in recs:
            item = by.get(r["hash"])
            # E3
            if r["outcome"] == "MATE":
                P, Q = unpack_P(r), unpack_Q(r)
                ok = M.is_one(M.bracket(P, Q))
                tally[(armname, "exact_solution", ok)] += 1
                if not ok:
                    fails.append((armname, r["hash"], "MATE", "bracket != 1"))
            # E1 / E2
            for st in r["stages"]:
                c = st.get("certificate")
                if c == "lambda_exact":
                    lv = st.get("lambda_vector")
                    if lv is None:
                        tally[(armname, "lambda_exact", "NOT_RECORDED")] += 1
                        continue
                    if item is None:
                        tally[(armname, "lambda_exact", "NO_ITEM")] += 1
                        continue
                    ok, why = check_lambda(item, st["stage"], lv)
                    tally[(armname, "lambda_exact", ok)] += 1
                    if not ok:
                        fails.append((armname, r["hash"], st["stage"], why))
                elif c == "rank_full_column_exact":
                    tally[(armname, "rank_full_column_exact", "not_recheckable")] += 1

    print("independent re-verification of emitted certificates")
    print("(carriers and Keller systems rebuilt from scratch; exact.decide not used)\n")
    for k in sorted(tally, key=str):
        print("  %-22s %-26s %-16s %d" % (k[0], k[1], str(k[2]), tally[k]))
    print("\nFAILURES: %d" % len(fails))
    for f in fails:
        print("  ", f)
    json.dump({"tally": {" | ".join(str(x) for x in k): v
                         for k, v in tally.items()},
               "failures": fails},
              open(os.path.join(HERE, "verify_certs.json"), "w"), indent=1)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
