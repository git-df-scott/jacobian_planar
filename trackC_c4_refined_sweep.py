#!/usr/bin/env python3
"""C4 refined-frame sweep: run the framework's ACTUAL obstruction chain on
every (rho, s) slice of the refined lattice, for a window of (m, k).

Context. trackC_phase4.py's c4 run enumerated the refined frame (rho != s
allowed, the C1d generalization) and stopped there, because OPUS_PLAN P4 marks
C4 Fable-grade. This script does the mechanical half the enumeration was
missing: for each slice it runs solve_forced_S, which is the same exact-linear-
algebra routine C2 used, and reports a verdict per (rho, s, m, k).

The obstruction chain is the one C1 derived and C2 exercised, not a new one:

  sigma  = (1 + rho - rho*s)/5            integral <=> rho*(s-1) = 1 (mod 5)
  D      = (a+b)k + 1 - s = 5k + 1 - s    (>= 1)
  p      = (a+b)m - 1 = 5m - 1
  deg S  = d = (p - t) - (D/k)*(m + sigma)
           -> a slice is DEAD unless d is a non-negative integer
              (the divisibility sieve: k | D*(m + sigma) at t = 0)
  resonance  k*(j + t) + D*sigma = 0 for some 1 <= j <= d  -> DEAD (cascades
             to s_0 = 0)
  c = -alpha^(a+b) * (k*t + D*sigma) * s_0   ->  k*t + D*sigma = 0 gives
      c = 0 -> DEAD (the Keller constant cannot vanish)

Everything else about a slice — whether it is geometrically realizable at
(72,108) at all — is NOT decided here and is not decidable from the ODE alone.
This script decides exactly one thing per slice: does a forced R exist.
"""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from trackC_phase4 import solve_forced_S, poly_str  # noqa: E402

AB = 5          # a + b for cusp type (2,3)
T = 0           # handoff frame: t = ord_{v=0} R = 0
KMAX = 14
MMAX = 8
WIN = 12        # rho, s <= WIN


def refined_slices(win=WIN):
    """Every (rho, s) in [1,win]^2 with sigma = (1 + rho - rho*s)/5 integral."""
    out = []
    for rho in range(1, win + 1):
        for s in range(1, win + 1):
            num = 1 + rho - rho * s
            if num % AB == 0:
                out.append({"rho": rho, "s": s, "sigma": num // AB})
    return out


def sweep_slice(sl, kmax=KMAX, mmax=MMAX):
    """All (m, k) instances of one slice, with their verdicts."""
    rho, s, sigma = sl["rho"], sl["s"], sl["sigma"]
    live, insts = [], []
    for m in range(1, mmax + 1):
        p = AB * m - 1
        for k in range(1, kmax + 1):
            D = AB * k + 1 - s
            if D < 1:
                continue
            r = solve_forced_S(k, D, m, sigma, T, want_S=True)
            rec = {"m": m, "k": k, "D": D, "p": p,
                   "verdict": r["verdict"], "d": r.get("d")}
            if r["verdict"] == "FORCED_R":
                rec["c_over_alpha5"] = str(r.get("c_int_alpha1"))
                rec["S_int"] = poly_str(r["S_int"]) if r.get("S_int") else None
                live.append(rec)
            insts.append(rec)
    return insts, live


def main():
    slices = refined_slices()
    print("== C4 refined-frame sweep: rho(s-1) = 1 (mod 5), rho,s <= %d ==" % WIN)
    print("   %d slices; window m = 1..%d, k = 1..%d, t = %d\n"
          % (len(slices), MMAX, KMAX, T))
    rows, n_live_slices = [], 0
    for sl in slices:
        insts, live = sweep_slice(sl)
        tally = {}
        for i in insts:
            tally[i["verdict"]] = tally.get(i["verdict"], 0) + 1
        baseline = (sl["rho"] == 3 and sl["s"] == 3)
        row = {"rho": sl["rho"], "s": sl["sigma"] and sl["s"] or sl["s"],
               "sigma": sl["sigma"], "baseline": baseline,
               "n_instances": len(insts), "tally": tally,
               "n_live": len(live), "live": live[:6]}
        row["s"] = sl["s"]
        rows.append(row)
        if live:
            n_live_slices += 1
        tag = "  <- baseline (the examined one)" if baseline else ""
        klist = sorted({(i["m"], i["k"]) for i in live})
        print("  (rho,s) = (%2d,%2d)  sigma = %3d   live instances: %3d %s%s"
              % (sl["rho"], sl["s"], sl["sigma"], len(live),
                 ("(m,k) e.g. " + str(klist[:5])) if klist else "-- NONE: slice DEAD in window",
                 tag))
    print("\n  slices with at least one forced R in the window: %d / %d"
          % (n_live_slices, len(slices)))
    dead = [(r["rho"], r["s"]) for r in rows if r["n_live"] == 0]
    print("  slices DEAD throughout the window (%d): %s" % (len(dead), dead))
    sig0 = [(r["rho"], r["s"]) for r in rows if r["sigma"] == 0]
    print("  sigma = 0 slices (c = 0 at t = 0, hence dead unless t != 0): %s" % sig0)
    out = os.path.join(HERE, "trackC_c4_refined_sweep.json")
    with open(out, "w") as fh:
        json.dump({"frame": "refined (rho != s), cusp (2,3), t = %d" % T,
                   "window": {"rho_s_max": WIN, "m": MMAX, "k": KMAX},
                   "relations": {"sigma": "(1+rho-rho*s)/5", "D": "5k+1-s",
                                 "p": "5m-1",
                                 "d": "(p-t) - D*(m+sigma)/k"},
                   "n_slices": len(slices), "rows": rows}, fh, indent=1)
    print("\n  artifact: trackC_c4_refined_sweep.json")


if __name__ == "__main__":
    main()
