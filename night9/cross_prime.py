"""night9 — the cross-prime experiment.

Twelve distinguished supports, each run at EVERY prime in
{2, 3, 5, 7, 11, 13, 17, 19, 23}, with the same standards as the sweep:

  * verdict NONEMPTY / EMPTY by the complete exhaustive-bilinear method when
    p^nfree <= BUDGET, otherwise by Groebner over GF(p) together with the
    field equations z^p - z (so the variety is exactly the F_p-rational
    points); a Groebner timeout is recorded as TIMEOUT, never as EMPTY;
  * on NONEMPTY: the COMPLETE solution set (when the exact count is at most
    CAP), split by the additive-type degeneracy screen into DEGENERATE and
    NON-DEGENERATE;
  * for up to SAMPLE non-degenerate solutions: direct-substitution
    verification, the tear class mod p (or TEAR-NOT-COMPUTED per the caps in
    tear.py), and the Hensel steps to Z/p^2 and then Z/p^3, TEAR-NONEMPTY
    first.

The quantity of interest, recorded without interpretation: whether any single
support is non-degenerate NONEMPTY at three or more distinct primes.

Outputs: night9/cross_prime.csv, night9/cross_prime/<hash>_p<p>.json.
"""
import csv, json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from keller_solver import (exhaustive, verify_solution, hensel_step,
                           degenerate_screen)
from tear import tear_data
from survey import groebner_cell, sampling_cell, shash
from census import all_solutions

BUDGET = 10 ** 7
CAP = 60000
SAMPLE = 8
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23]

# (a) the four supports whose solutions climbed to Z/p^2 in the sweep
CLIMBERS = ["3ee4c514dba8", "c764f008a1a1", "cf8c7ed97c0c", "e3ff048903ae"]
# (b) eight further TEAR-NONEMPTY cells that carry non-degenerate solutions,
#     chosen for enumerability: small min(|S_P|,|S_Q|) and low total degree,
#     spread over families F1/F2 and over the primes at which they were found.
CHOSEN = ["4ed4abb6f5df", "9fad1aac9556", "1c4afff29879", "184a36732588",
          "2b796756e70e", "252ffcaec0dc", "36b363c5d338", "6c5a7dd8e3e9"]

FIELDS = ["hash", "p", "origin", "nP", "nQ", "n", "method", "n_enum",
          "verdict", "count", "enumerated", "truncated", "n_degenerate",
          "n_nondegenerate", "n_sampled", "n_verify_fail", "tear_nonempty",
          "tear_empty", "tear_other", "climb_p2", "climb_p3", "wall_s",
          "note"]


def run(SP, SQ, p, h, origin, outdir):
    t0 = time.time()
    rec = {"hash": h, "p": p, "origin": origin, "nP": len(SP), "nQ": len(SQ),
           "n": len(SP) + len(SQ), "truncated": False}
    ex = exhaustive(SP, SQ, p, budget=BUDGET, max_solutions=SAMPLE)
    sols = []
    sample_only = False
    if ex["feasible"]:
        rec["method"] = "exhaustive-bilinear"
        rec["n_enum"] = ex["n_enum"]
        rec["count"] = ex["count"]
        rec["verdict"] = "NONEMPTY" if ex["count"] > 0 else "EMPTY"
    else:
        gb = groebner_cell(SP, SQ, p)
        rec["n_enum"] = ex["n_enum"]
        rec["count"] = ""
        if gb["status"] == "OK":
            rec["method"] = "groebner-gfp-field"
            rec["verdict"] = "EMPTY" if gb["empty"] else "NONEMPTY"
        else:
            rec["method"] = "groebner-gfp-field"
            rec["verdict"] = "TIMEOUT"
            rec["note"] = "groebner " + gb["status"]

    if rec["verdict"] == "NONEMPTY":
        if ex["feasible"] and ex["count"] <= CAP:
            sols, trunc = all_solutions(SP, SQ, p, cap=CAP)
            rec["enumerated"] = len(sols)
            rec["truncated"] = trunc
        else:
            sp = sampling_cell(SP, SQ, p, seed=p, max_solutions=SAMPLE)
            sols = sp["solutions"]
            sample_only = True
            rec["enumerated"] = len(sols)
            rec["truncated"] = True
            rec["note"] = ((rec.get("note", "") + "; ") if rec.get("note") else "") + \
                "solution list is a sample, not the complete set"
        nd = [s for s in sols if not degenerate_screen(SP, SQ, s[0], s[1])[0]]
        rec["n_degenerate"] = len(sols) - len(nd)
        rec["n_nondegenerate"] = len(nd)
        staged, nfail = [], 0
        for (a, b) in nd[:SAMPLE]:
            chk = verify_solution(SP, SQ, a, b, p)
            if not (chk["det_ok"] and chk["coll_ok"]):
                nfail += 1
                continue
            staged.append({"a": a, "b": b, "verify": chk,
                           "tear": tear_data(SP, SQ, a, b, p)})
        staged.sort(key=lambda z: 0 if z["tear"]["tear"] == "TEAR-NONEMPTY" else 1)
        tc = {"TEAR-NONEMPTY": 0, "TEAR-EMPTY": 0}
        other = c2 = c3 = 0
        for z in staged:
            k = z["tear"]["tear"]
            if k in tc:
                tc[k] += 1
            else:
                other += 1
            l2 = hensel_step(SP, SQ, z["a"], z["b"], p, 1)
            z["lift_to_p2"] = l2 is not None
            if l2 is not None:
                c2 += 1
                z["p2_point"] = {"a": l2[0], "b": l2[1]}
                l3 = hensel_step(SP, SQ, l2[0], l2[1], p, 2)
                z["lift_to_p3"] = l3 is not None
                if l3 is not None:
                    c3 += 1
                    z["p3_point"] = {"a": l3[0], "b": l3[1]}
        rec.update({"n_sampled": len(staged), "n_verify_fail": nfail,
                    "tear_nonempty": tc["TEAR-NONEMPTY"],
                    "tear_empty": tc["TEAR-EMPTY"], "tear_other": other,
                    "climb_p2": c2, "climb_p3": c3})
        with open(os.path.join(outdir, "%s_p%d.json" % (h, p)), "w") as g:
            json.dump({"hash": h, "p": p, "characteristic": p,
                       "origin": origin,
                       "support_P": [list(m) for m in SP],
                       "support_Q": [list(m) for m in SQ],
                       "method": rec["method"],
                       "exact_count": rec.get("count", ""),
                       "solution_list_is_complete": not rec["truncated"],
                       "n_degenerate": rec["n_degenerate"],
                       "n_nondegenerate": rec["n_nondegenerate"],
                       "solutions": staged}, g, indent=1)
    rec["wall_s"] = round(time.time() - t0, 2)
    return rec


def main():
    outdir = os.path.join(HERE, "cross_prime")
    os.makedirs(outdir, exist_ok=True)
    sup = {}
    for f in os.listdir(os.path.join(HERE, "supports")):
        d = json.load(open(os.path.join(HERE, "supports", f)))
        sup[d["hash"]] = d
    sel = [(h, "climber-to-Z/p^2") for h in CLIMBERS] + \
          [(h, "TEAR-NONEMPTY-nondegenerate") for h in CHOSEN]
    cpath = os.path.join(HERE, "cross_prime.csv")
    done = set()
    if os.path.exists(cpath):
        for r in csv.DictReader(open(cpath)):
            done.add((r["hash"], int(r["p"])))
    newf = not os.path.exists(cpath)
    fh = open(cpath, "a", newline="")
    w = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
    if newf:
        w.writeheader()
    for h, origin in sel:
        d = sup[h]
        SP = [tuple(m) for m in d["support_P"]]
        SQ = [tuple(m) for m in d["support_Q"]]
        for p in PRIMES:
            if (h, p) in done:
                continue
            rec = run(SP, SQ, p, h, origin, outdir)
            w.writerow(rec)
            fh.flush()
            print("%s p=%-3d %-20s %-9s cnt=%-8s nondeg=%-6s tearNE=%-3s c2=%-3s %.1fs"
                  % (h, p, rec["method"], rec["verdict"], str(rec.get("count", "")),
                     str(rec.get("n_nondegenerate", "")),
                     str(rec.get("tear_nonempty", "")),
                     str(rec.get("climb_p2", "")), rec["wall_s"]), flush=True)
    fh.close()


if __name__ == "__main__":
    main()
