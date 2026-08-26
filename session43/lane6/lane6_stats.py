#!/usr/bin/env python3
"""STEP 4: multi-prime structure statistics for the cap-condition tower.

For each prime p, exhaustively sweeps every (u,v,w) in F_p^* x F_p x F_p and
counts, nested,

    N1 = #{ E0[22] = 0 }                       (a surface)
    N2 = #{ E0[22] = E0[23] = 0 }              (a curve)
    N3 = #{ E0[22] = E0[23] = E0[24] = 0 }     (finite)
    N4, N5, ...                                (should be empty)

all with p3[22..n] pinned to 0 by the degree cap deg p3 <= 21.

Lang-Weil / Chebotarev reading:
    N1/p^2  -> number of absolutely irreducible components of the surface
    N2/p    -> number of absolutely irreducible components of the curve
    mean N3 -> number of Galois orbits of the finite intersection scheme
    mean N4 -> 0 if the 4-condition system is empty over Qbar
"""
import argparse
import json
import sys
import time

import numpy as np

from lane6_core import FpRing, run
from lane6_sweep import CAPS, rigour_limit, sweep_points

DEEP = 40


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--primes", type=int, nargs="+", required=True)
    ap.add_argument("--levels", type=int, default=3)
    ap.add_argument("--chunk", type=int, default=8192)
    ap.add_argument("--out", default="lane6_stats.json")
    args = ap.parse_args()

    n1rung = 21 + args.levels
    rows = []
    print("  p    points     N1      N1/p^2    N2    N2/p    N3   deeper "
          "(first failing rung of the N3 points)")
    for p in args.primes:
        lim = rigour_limit(p)
        assert lim >= n1rung, "prime %d too small for rung %d" % (p, n1rung)
        U, V, W = sweep_points(p)
        npts = U.size
        t0 = time.time()
        counts = None
        alive = None
        for start in range(0, npts, args.chunk):
            stop = min(start + args.chunk, npts)
            R = FpRing(p, stop - start)
            res = run(R, U[start:stop].copy(), V[start:stop].copy(),
                      W[start:stop].copy(), n1rung, caps=CAPS)
            a = np.ones(stop - start, dtype=bool)
            cs = []
            for n in range(22, n1rung + 1):
                a = a & (res["cond"][("p3", n)] % p == 0)
                cs.append(int(a.sum()))
            counts = cs if counts is None else [x + y
                                               for x, y in zip(counts, cs)]
            idx = np.nonzero(a)[0] + start
            alive = idx if alive is None else np.concatenate([alive, idx])
        dt = time.time() - t0

        # follow the survivors deeper
        deeper = []
        if alive.size:
            deep = min(rigour_limit(p), DEEP)
            R = FpRing(p, alive.size)
            res = run(R, U[alive].copy(), V[alive].copy(), W[alive].copy(),
                      deep, caps=CAPS)
            for i in range(alive.size):
                first = None
                for key in sorted(res["cond"], key=lambda k: (k[1], k[0])):
                    if res["cond"][key][i] % p != 0:
                        first = key
                        break
                deeper.append(dict(u=int(U[alive[i]]), v=int(V[alive[i]]),
                                   w=int(W[alive[i]]),
                                   first_fail=list(first) if first else None,
                                   deep=deep))
        print("%4d %9d %7d %8.4f %6d %7.3f %5d   %s   [%.1fs]"
              % (p, npts, counts[0], counts[0] / float(p * p), counts[1],
                 counts[1] / float(p), counts[2],
                 ";".join("(%d,%d,%d)->%s" % (d["u"], d["v"], d["w"],
                                              d["first_fail"])
                          for d in deeper) or "-", dt))
        rows.append(dict(p=p, npts=npts, counts=counts, deeper=deeper,
                         seconds=dt))

    n1 = [r["counts"][0] / float(r["p"] ** 2) for r in rows]
    n2 = [r["counts"][1] / float(r["p"]) for r in rows]
    n3 = [r["counts"][2] for r in rows]
    print()
    print("mean N1/p^2 = %.4f   (Lang-Weil: # abs. irred. components of the "
          "surface)" % (sum(n1) / len(n1)))
    print("mean N2/p   = %.4f   (Lang-Weil: # abs. irred. components of the "
          "curve)" % (sum(n2) / len(n2)))
    print("mean N3     = %.4f   over %d primes (Chebotarev: # Galois orbits "
          "of the finite scheme)" % (sum(n3) / len(n3), len(n3)))
    nonzero = [r for r in rows if r["counts"][2]]
    print("primes with an N3 point: %s"
          % ([(r["p"], r["counts"][2]) for r in nonzero] or "none"))
    survived4 = [d for r in rows for d in r["deeper"]
                 if d["first_fail"] is None]
    print("N3 points that ALSO survive every deeper condition: %s"
          % (survived4 or "NONE"))

    with open(args.out, "w") as fh:
        json.dump(rows, fh, indent=1)
    print("wrote", args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
