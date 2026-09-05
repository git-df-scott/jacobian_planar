"""night9 — PRIME EXTENSION of the altitude sweep to p = 5 and p = 7.

Measurements only.  Every result is labelled with its characteristic.  No
assessment of what any of these numbers mean is offered.

INPUT: the supports of night9/altitude.csv that are NONEMPTY at BOTH p = 2 and
p = 3 (38 of the 60).

METHOD.
  * p = 5: complete `exhaustive-bilinear`.  The enumerated side has at most 8
    coefficients, so at most 5^8 = 390625 outer points.  A support whose
    enumerated side exceeds 8 coefficients would be SKIPPED and recorded as
    SKIPPED-nP-too-large; none occurs.
  * p = 7: complete `exhaustive-bilinear` when 7^nfree <= 8 * 10^6, otherwise
    Groebner over GF(p) together with the field equations z^p - z (so the
    variety is exactly the F_p-rational points), 300 s timeout, a timeout
    recorded as TIMEOUT and never as EMPTY.

For every NONEMPTY cell: the solution set (cap 50000, truncation recorded),
the additive degeneracy screen, direct-substitution verification of a sample,
and the tear class mod p (TEAR-NOT-COMPUTED where tear.py's caps bite).

ACCUMULATOR.  A support is counted at a prime when it has at least one
NON-DEGENERATE solution there.  Any support reaching FOUR OR MORE primes is
handed to night9/interp/interp.py for the full CRT / rational-reconstruction /
exact-verification-over-Q treatment, with outputs in night9/interp2/.

Outputs: night9/altitude2.csv, night9/altitude2/<hash>.json, ALTITUDE2.md.
"""
import csv
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from keller_solver import exhaustive, verify_solution, degenerate_screen  # noqa: E402
from tear import tear_data                                               # noqa: E402
from census import all_solutions                                         # noqa: E402
from survey import groebner_cell                                         # noqa: E402
import altitude as ALT                                                   # noqa: E402

PRIMES = [5, 7]
BUDGET7 = 8 * 10 ** 6
BUDGET5 = 10 ** 7
CAP = 50000
SAMPLE = 8
MAX_ENUM_SIDE = 8          # "nP <= 8" rule for p = 5

FIELDS = ["hash", "p", "nP", "nQ", "n", "max_total_degree", "method",
          "n_enum", "verdict", "count", "truncated", "n_degenerate",
          "n_nondegenerate", "n_sampled", "n_verify_fail", "tear_nonempty",
          "tear_empty", "tear_other", "wall_s", "note"]


def run_cell(SP, SQ, p, h, D):
    t0 = time.time()
    rec = {"hash": h, "p": p, "nP": len(SP), "nQ": len(SQ),
           "n": len(SP) + len(SQ), "max_total_degree": D, "truncated": False}
    budget = BUDGET5 if p == 5 else BUDGET7
    ex = exhaustive(SP, SQ, p, budget=budget, max_solutions=SAMPLE)
    rec["n_enum"] = ex["n_enum"]
    enum_side_size = len(SP) if ex.get("enum_side") == "P" else len(SQ)
    if p == 5 and enum_side_size > MAX_ENUM_SIDE:
        rec["method"] = "skipped"
        rec["verdict"] = "SKIPPED-nP-too-large"
        rec["note"] = "enumerated side has %d coefficients > %d" % (
            enum_side_size, MAX_ENUM_SIDE)
        rec["wall_s"] = round(time.time() - t0, 2)
        return rec, []
    if ex["feasible"]:
        rec["method"] = "exhaustive-bilinear"
        rec["count"] = ex["count"]
        rec["verdict"] = "NONEMPTY" if ex["count"] > 0 else "EMPTY"
    else:
        gb = groebner_cell(SP, SQ, p)
        rec["method"] = "groebner-gfp-field"
        rec["count"] = ""
        if gb["status"] == "OK":
            rec["verdict"] = "EMPTY" if gb["empty"] else "NONEMPTY"
        else:
            rec["verdict"] = "TIMEOUT"
            rec["note"] = "groebner " + gb["status"]

    nd = []
    if rec["verdict"] == "NONEMPTY":
        if ex["feasible"]:
            sols, trunc = all_solutions(SP, SQ, p, cap=CAP)
        else:
            sols, trunc = ex.get("solutions", []), True
        rec["truncated"] = trunc
        nd = [s for s in sols if not degenerate_screen(SP, SQ, s[0], s[1])[0]]
        rec["n_degenerate"] = len(sols) - len(nd)
        rec["n_nondegenerate"] = len(nd)
        tc = {"TEAR-NONEMPTY": 0, "TEAR-EMPTY": 0}
        other = nfail = nsamp = 0
        for (a, b) in nd[:SAMPLE]:
            chk = verify_solution(SP, SQ, a, b, p)
            if not (chk["det_ok"] and chk["coll_ok"]):
                nfail += 1
                continue
            nsamp += 1
            k = tear_data(SP, SQ, a, b, p)["tear"]
            if k in tc:
                tc[k] += 1
            else:
                other += 1
        rec.update({"n_sampled": nsamp, "n_verify_fail": nfail,
                    "tear_nonempty": tc["TEAR-NONEMPTY"],
                    "tear_empty": tc["TEAR-EMPTY"], "tear_other": other})
    rec["wall_s"] = round(time.time() - t0, 2)
    return rec, nd


def main():
    outdir = os.path.join(HERE, "altitude2")
    os.makedirs(outdir, exist_ok=True)

    prev = {}
    for r in csv.DictReader(open(os.path.join(HERE, "altitude.csv"))):
        prev.setdefault(r["hash"], {})[int(r["p"])] = r
    duals = [h for h, v in prev.items()
             if v[2]["verdict"] == "NONEMPTY" and v[3]["verdict"] == "NONEMPTY"]
    print("dual-prime supports carried forward: %d" % len(duals), flush=True)

    sup = {}
    for f in os.listdir(os.path.join(HERE, "altitude")):
        d = json.load(open(os.path.join(HERE, "altitude", f)))
        sup[d["hash"]] = d

    cpath = os.path.join(HERE, "altitude2.csv")
    done = set()
    if os.path.exists(cpath):
        for r in csv.DictReader(open(cpath)):
            done.add((r["hash"], int(r["p"])))
    newf = not os.path.exists(cpath)
    fh = open(cpath, "a", newline="")
    w = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
    if newf:
        w.writeheader()

    for i, h in enumerate(sorted(duals)):
        d = sup[h]
        SP = [tuple(m) for m in d["support_P"]]
        SQ = [tuple(m) for m in d["support_Q"]]
        D = d["max_total_degree"]
        recs = {}
        for p in PRIMES:
            if (h, p) in done and os.path.exists(
                    os.path.join(outdir, "%s.json" % h)):
                continue
            rec, nd = run_cell(SP, SQ, p, h, D)
            recs[p] = (rec, nd)
            w.writerow(rec)
            fh.flush()
            print("[%2d/%d] %s D=%3d p=%d %-22s cnt=%-8s nondeg=%-7s %.1fs"
                  % (i + 1, len(duals), h, D, p, rec["verdict"],
                     str(rec.get("count", "")),
                     str(rec.get("n_nondegenerate", "")), rec["wall_s"]),
                  flush=True)
        if recs:
            with open(os.path.join(outdir, "%s.json" % h), "w") as g:
                json.dump({"hash": h, "max_total_degree": D,
                           "support_P": [list(m) for m in SP],
                           "support_Q": [list(m) for m in SQ],
                           "per_prime": {str(p): recs[p][0] for p in recs}},
                          g, indent=1)
    fh.close()


if __name__ == "__main__":
    main()
