#!/usr/bin/env python3
"""STEP 2-4: exhaustive F_p sweep of the u != 0 chart of the (4,6) frontier.

Every point (u,v,w) in F_p^* x F_p x F_p is a complete initial condition for
the kernel-retaining recurrence (validated in lane6_validate.py).  Imposing
the degree caps deg p3 <= 21, deg p2 <= 42, deg p1 <= 63 turns each rung
n >= 22 into a *condition* rather than a solve.  A Keller-pair candidate must
satisfy all of them.

Modular rigour limit
--------------------
The recurrence divides by n (integrating q_j' -> q_j) and by n+1 (solving
p1[n+1], p2[n+1]).  Mod p those fail at n = p and n = p-1.  The last fully
rigorous rung is therefore N_limit = p-2, unless a cap has already removed the
division.  For p = 41 that is rung 39, for p = 43 rung 41, for p = 67 rung 60.
The engine raises rather than silently producing garbage.
"""
import argparse
import sys
import time

import numpy as np

from lane6_core import FpRing, run

CAPS = {"p3": 22, "p2": 43, "p1": 64}


def rigour_limit(p):
    n = 1
    last = 1
    while True:
        n += 1
        if n >= 83:
            return 82
        # chain(n) divides by n
        if n % p == 0:
            return last
        # p1[n+1] solve divides by n+1 unless capped
        if (n + 1) < CAPS["p1"] and (n + 1) % p == 0:
            return last
        # p2[n+1] solve divides by n+1 unless capped
        if (n + 1) < CAPS["p2"] and (n + 1) % p == 0:
            return last
        # p3[n] solve divides by n+1 unless capped
        if n < CAPS["p3"] and (n + 1) % p == 0:
            return last
        last = n


def sweep_points(p):
    u = np.arange(1, p, dtype=np.int64)
    v = np.arange(0, p, dtype=np.int64)
    w = np.arange(0, p, dtype=np.int64)
    U, V, W = np.meshgrid(u, v, w, indexing="ij")
    return U.ravel(), V.ravel(), W.ravel()


def stage(p, U, V, W, N, chunk):
    """Return dict (row,index) -> concatenated residual array over the points."""
    npts = U.size
    out = {}
    for start in range(0, npts, chunk):
        stop = min(start + chunk, npts)
        R = FpRing(p, stop - start)
        res = run(R, U[start:stop].copy(), V[start:stop].copy(),
                  W[start:stop].copy(), N, caps=CAPS, selfcheck=False)
        for key, val in res["cond"].items():
            out.setdefault(key, []).append(val % p)
    return {k: np.concatenate(v) for k, v in out.items()}


def nested_counts(cond, p, nmax):
    keys = sorted([k for k in cond if k[0] == "p3"], key=lambda k: k[1])
    keys = [k for k in keys if k[1] <= nmax]
    alive = None
    hist = []
    for k in keys:
        z = cond[k] == 0
        alive = z if alive is None else (alive & z)
        hist.append((k[1], int(z.sum()), int(alive.sum())))
    return hist, alive


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--primes", type=int, nargs="+", default=[41, 43])
    ap.add_argument("--stage1", type=int, default=30)
    ap.add_argument("--chunk", type=int, default=16384)
    ap.add_argument("--nmax", type=int, default=60)
    args = ap.parse_args()

    summary = {}
    for p in args.primes:
        lim = min(rigour_limit(p), args.nmax)
        n1 = lim if args.stage1 <= 0 else min(args.stage1, lim)
        U, V, W = sweep_points(p)
        npts = U.size
        print("=" * 74)
        print("PRIME p = %d   points with u != 0 : %d   rigorous rung limit %d"
              % (p, npts, lim))
        print("=" * 74)

        t0 = time.time()
        cond = stage(p, U, V, W, n1, args.chunk)
        t1 = time.time()
        print("stage 1: rungs 0..%d over all %d points in %.1f s"
              % (n1, npts, t1 - t0))

        hist, alive = nested_counts(cond, p, n1)
        print()
        print("  SURVIVAL HISTOGRAM (condition k is E0[n]=0 with p3[22..n]:=0)")
        print("   rung n   #{this condition alone}   #{all of 22..n}"
              "   expected ~ (p-1)p^2/p^(n-21)")
        for n, single, cum in hist:
            exp = (p - 1) * p * p / float(p ** (n - 21))
            print("    %3d      %10d              %10d          %12.2f"
                  % (n, single, cum, exp))

        # also the p2 cap conditions that were reached in stage 1
        p2keys = sorted([k for k in cond if k[0] == "p2"], key=lambda k: k[1])
        if p2keys:
            print("  p2 cap conditions reached in stage 1:",
                  [k[1] for k in p2keys])

        alive_idx = np.nonzero(alive)[0]
        print()
        print("  survivors of ALL rungs 22..%d : %d" % (n1, alive_idx.size))

        stage2 = None
        if alive_idx.size:
            print("  survivor parameter points (u,v,w):")
            for i in alive_idx[:50]:
                print("     (%d, %d, %d)" % (U[i], V[i], W[i]))
            if lim > n1:
                cond2 = stage(p, U[alive_idx], V[alive_idx], W[alive_idx],
                              lim, min(args.chunk, alive_idx.size))
                hist2, alive2 = nested_counts(cond2, p, lim)
                print("  stage 2 (rungs to %d) on the %d survivors:"
                      % (lim, alive_idx.size))
                for n, single, cum in hist2:
                    if n > n1:
                        print("    rung %3d : cumulative survivors %d"
                              % (n, cum))
                p2bad = {k: int((cond2[k] != 0).sum())
                         for k in cond2 if k[0] == "p2"}
                print("    p2-cap violations by rung:", p2bad)
                final = np.nonzero(alive2)[0]
                allp2 = np.ones(alive_idx.size, dtype=bool)
                for k in cond2:
                    if k[0] in ("p2", "p1"):
                        allp2 &= (cond2[k] == 0)
                final_all = np.nonzero(alive2 & allp2)[0]
                stage2 = [(int(U[alive_idx[i]]), int(V[alive_idx[i]]),
                           int(W[alive_idx[i]])) for i in final_all]
                print("    survivors of EVERY condition through rung %d : %d"
                      % (lim, len(stage2)))
                for t in stage2:
                    print("      *** CANDIDATE (u,v,w) =", t)
        summary[p] = dict(npts=npts, limit=lim, stage1=n1,
                          hist=hist,
                          alive=[(int(U[i]), int(V[i]), int(W[i]))
                                 for i in alive_idx],
                          stage2=stage2,
                          seconds=t1 - t0)
        print()

    print("=" * 74)
    print("CROSS-PRIME SUMMARY")
    print("=" * 74)
    for p, s in summary.items():
        print("p=%d: %d points, rigorous to rung %d, survivors of 22..%d = %d"
              % (p, s["npts"], s["limit"], s["stage1"], len(s["alive"])))
        if s["stage2"] is not None:
            print("      survivors of every condition to rung %d: %s"
                  % (s["limit"], s["stage2"]))
    import json
    with open("lane6_sweep_result.json", "w") as fh:
        json.dump({str(k): v for k, v in summary.items()}, fh, indent=1)
    print("wrote lane6_sweep_result.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
