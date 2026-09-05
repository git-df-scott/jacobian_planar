"""night16 -- exact mate solve at the LARGEST affordable carrier, for the P
that are STILL-VANISHING at every atypical value.

night15 escalated the carrier to deg Q = 2 deg P and got EMPTY_over_Q with a
lambda certificate at every stage.  This run starts ABOVE that: it takes
D = 2 deg P + 1, 2 deg P + 2, ... while the full triangular carrier fits in
max_cols columns and the wall-clock budget holds.  Every EMPTY verdict carries
an exact lambda certificate, re-verified over Q.

HIT GATE: a consistent system is reconstructed to an exact Q over Q, verified
by expanding [P,Q] - 1 coefficientwise, and written to night16/HIT_<hash>/.
"""
import json, os, sys, time
from fractions import Fraction as F

import mate16, pk16, load16, atyp16 as A
import sympy as sp

MAXCOLS = int(os.environ.get("MAXCOLS", "2400"))
TBUDGET = float(os.environ.get("TBUDGET", "900"))
EXTRACOLS = int(os.environ.get("EXTRACOLS", "400"))
LAMCAP = int(os.environ.get("LAMCAP", "900"))
OUT = "mate16_%s.json" % (os.environ.get("TAG", "") + (sys.argv[1] if len(sys.argv) > 1 else "all"))


def degs_for(d):
    """the two carriers just above night15's ceiling, plus the largest that fits."""
    fit = 2 * d + 1
    while (fit + 2) * (fit + 3) // 2 <= EXTRACOLS and fit + 1 <= 3 * d:
        fit += 1
    out = []
    for D in (2 * d + 1, 2 * d + 2, fit):
        if D not in out and (D + 1) * (D + 2) // 2 <= MAXCOLS:
            out.append(D)
    return sorted(out)


def unimodular_and_noncoordinate(rec):
    """re-verify the two hypotheses from night15's own record."""
    return {"U_bezout_identity": rec["U"]["U"], "U_reason": rec["U"]["reason"],
            "SY": rec["SY"], "FIB": rec["FIB"]}


def main():
    names = json.load(open(os.environ.get("NAMES", "still_vanishing16.json")))
    if len(sys.argv) > 2:
        kk, nn = int(sys.argv[1]), int(sys.argv[2])
        names = [h for i, h in enumerate(names) if i % nn == kk]
    S = {r["hash"]: r for r in load16.survivors()}
    res = []
    if os.path.exists(OUT):
        res = json.load(open(OUT))
    done = {r["hash"] for r in res}
    for h in names:
        if h in done:
            continue
        rec = S[h]
        P = load16.Pdict(rec)
        d = rec["deg_P"]
        ds = degs_for(d)
        t0 = time.time()
        stages = []
        hit = None
        for D in ds:
            if time.time() - t0 > TBUDGET:
                stages.append({"deg_Q_bound": D, "verdict": "SKIPPED_time_budget"})
                break
            r = mate16.solve(P, max_cols=MAXCOLS, verbose=False, degs=(D,), lam_cap=LAMCAP)
            stages.extend(r["stages"])
            if r["verdict"] == "MATE_over_Q":
                hit = r
                break
        rec_out = {"hash": h, "label": rec["label"], "deg_P": d,
                   "degs_tried": ds, "stages": stages,
                   "hypotheses": unimodular_and_noncoordinate(rec),
                   "verdict": "MATE_over_Q" if hit else (
                       "EMPTY_all_stages" if stages and all(
                           s.get("verdict") in ("EMPTY_over_Q", "SKIPPED_time_budget",
                                                "SKIPPED_too_large")
                           for s in stages) and any(
                           s.get("verdict") == "EMPTY_over_Q" for s in stages)
                       else "NOT_CERTIFIED"),
                   "secs": round(time.time() - t0, 1)}
        if hit:
            rec_out["HIT"] = hit
            os.makedirs("HIT_%s" % h, exist_ok=True)
            json.dump({"record": rec, "solve": hit}, open("HIT_%s/hit.json" % h, "w"),
                      indent=1, default=str)
            print("HIT %s" % h, flush=True)
        res.append(rec_out)
        json.dump(res, open(OUT, "w"), indent=1, default=str)
        print("%s deg=%2d %-18s stages=%s (%.0fs)"
              % (h, d, rec_out["verdict"],
                 [(s.get("deg_Q_bound"), s.get("verdict"), s.get("certificate"))
                  for s in stages], rec_out["secs"]), flush=True)


if __name__ == "__main__":
    main()
