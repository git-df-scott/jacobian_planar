#!/usr/bin/env python3
"""Gauge-free sweep: c and the p0 scale a are swept, not assumed.

The prior collision-first scripts fix the leading y^6 coefficient c = 1 and
p0 = x^84 - x.  Here p0 = a(x^84 - x) with a != 0 and c != 0 are extra sweep
coordinates, so the whole u != 0 chart is covered without any gauge choice.
"""
import argparse
import json
import sys
import time

import numpy as np

from lane6_core import FpRing, run
from lane6_sweep import CAPS, rigour_limit


def grid(p, sweep_a):
    u = np.arange(1, p, dtype=np.int64)
    vw = np.arange(0, p, dtype=np.int64)
    c = np.arange(1, p, dtype=np.int64)
    a = np.arange(1, p, dtype=np.int64) if sweep_a else np.array([1], np.int64)
    U, V, W, C, A = np.meshgrid(u, vw, vw, c, a, indexing="ij")
    return (U.ravel(), V.ravel(), W.ravel(), C.ravel(), A.ravel())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--primes", type=int, nargs="+", required=True)
    ap.add_argument("--levels", type=int, default=3)
    ap.add_argument("--chunk", type=int, default=8192)
    ap.add_argument("--sweep-a", action="store_true")
    ap.add_argument("--out", default="lane6_gauge.json")
    args = ap.parse_args()

    nr = 21 + args.levels
    rows = []
    print("sweeping c%s ; conditions to rung %d"
          % (" and a" if args.sweep_a else " (a = 1 pinned by the problem)", nr))
    print("  p     points        N1       N2      N3   first-fail of the N3 "
          "points")
    for p in args.primes:
        assert rigour_limit(p) >= nr
        U, V, W, C, A = grid(p, args.sweep_a)
        npts = U.size
        t0 = time.time()
        counts = [0] * args.levels
        alive = []
        for start in range(0, npts, args.chunk):
            stop = min(start + args.chunk, npts)
            R = FpRing(p, stop - start)
            res = run(R, U[start:stop].copy(), V[start:stop].copy(),
                      W[start:stop].copy(), nr, caps=CAPS,
                      cval=C[start:stop].copy(), aval=A[start:stop].copy())
            ok = np.ones(stop - start, dtype=bool)
            for i, n in enumerate(range(22, nr + 1)):
                ok = ok & (res["cond"][("p3", n)] % p == 0)
                counts[i] += int(ok.sum())
            alive.append(np.nonzero(ok)[0] + start)
        alive = np.concatenate(alive)
        dt = time.time() - t0

        deeper = []
        if alive.size:
            deep = min(rigour_limit(p), 40)
            R = FpRing(p, alive.size)
            res = run(R, U[alive].copy(), V[alive].copy(), W[alive].copy(),
                      deep, caps=CAPS, cval=C[alive].copy(),
                      aval=A[alive].copy())
            for i in range(alive.size):
                first = None
                for key in sorted(res["cond"], key=lambda k: (k[1], k[0])):
                    if res["cond"][key][i] % p != 0:
                        first = key
                        break
                deeper.append(dict(u=int(U[alive[i]]), v=int(V[alive[i]]),
                                   w=int(W[alive[i]]), c=int(C[alive[i]]),
                                   a=int(A[alive[i]]),
                                   first_fail=list(first) if first else None))
        fails = sorted({tuple(d["first_fail"]) for d in deeper if
                        d["first_fail"]})
        print("%4d %10d %9d %8d %7d   %s   [%.1fs]"
              % (p, npts, counts[0], counts[1], counts[2], fails or "-", dt))
        rows.append(dict(p=p, npts=npts, counts=counts, deeper=deeper,
                         seconds=dt, sweep_a=args.sweep_a))

    survived = [d for r in rows for d in r["deeper"]
                if d["first_fail"] is None]
    print()
    print("points surviving EVERY condition to rung 40: %s" % (survived or
                                                               "NONE"))
    with open(args.out, "w") as fh:
        json.dump(rows, fh, indent=1)
    print("wrote", args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
