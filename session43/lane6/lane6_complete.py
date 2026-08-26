#!/usr/bin/env python3
"""DEFINITIVE sweep on a complete, gauge-free slice of the u != 0 chart.

Two exact symmetries of the whole cap-condition tower were measured (not
assumed) and are re-verified here at every prime:

  T1 (exact quasi-homogeneity, weights wt(u,v,w,c) = (1,2,3,5), wt(x) = -4,
      wt(A_j) = j-1, so the reduced row E_d has weight d and
            E_d[n]  ->  L^(d+4n) E_d[n] ):
        (u, v, w, c)  ->  (L u, L^2 v, L^3 w, L^5 c),      L in F_p^*
  T2 (rescaling x, from p0 = a(x^84 - x), locally p0 = -a x):
        (a, c, u, v, w) -> (1, a c, u/a, v/a, w/a),        a in F_p^*

T2 normalises a = 1, then T1 normalises u = 1.  Both stabilisers are trivial,
so

        { a = 1, u = 1, (v, w, c) in F_p x F_p x F_p^* }

meets every T1xT2-orbit of the u != 0 chart exactly once.  It has p^2(p-1)
points -- the same cost as the naive (u,v,w) grid at c = 1, but unlike that
grid it is COMPLETE.  (The c = 1 slice is provably incomplete over F_p: at
p = 41 it contains none of the 40 three-condition solutions, because their
c-coordinate is not a fifth power mod 41.)
"""
import argparse
import json
import sys
import time

import numpy as np

from lane6_core import FpRing, run
from lane6_sweep import CAPS, rigour_limit


def verify_symmetries(p, depth, M=200, seed=5):
    rng = np.random.default_rng(seed)
    pw = lambda arr, k: np.array([pow(int(z), k, p) for z in arr], np.int64)
    u = rng.integers(1, p, M)
    v = rng.integers(0, p, M)
    w = rng.integers(0, p, M)
    c = rng.integers(1, p, M)
    a = rng.integers(1, p, M)
    L = rng.integers(1, p, M)
    R = FpRing(p, M)
    d = depth
    base = run(R, u, v, w, d, caps=CAPS, cval=c, aval=a)
    t1 = run(R, (L * u) % p, (pw(L, 2) * v) % p, (pw(L, 3) * w) % p, d,
             caps=CAPS, cval=(pw(L, 5) * c) % p, aval=a)
    ai = pw(a, p - 2)
    t2 = run(R, (u * ai) % p, (v * ai) % p, (w * ai) % p, d, caps=CAPS,
             cval=(a * c) % p, aval=np.ones(M, np.int64))
    wt = {"p3": lambda n: 4 * n,          # [x^n] E0
          "p1": lambda m: 4 * m - 3,      # [x^(m-1)] E1
          "p2": lambda m: 4 * m - 2}      # [x^(m-1)] E2
    ok1 = all(np.array_equal(
        (pw(L, wt[k[0]](k[1]) % (p - 1)) * base["cond"][k]) % p,
        t1["cond"][k] % p) for k in base["cond"])
    ok2 = all(np.array_equal((base["cond"][k] % p) == 0,
                             (t2["cond"][k] % p) == 0) for k in base["cond"])
    return ok1, ok2


def slice_grid(p):
    v = np.arange(0, p, dtype=np.int64)
    w = np.arange(0, p, dtype=np.int64)
    c = np.arange(1, p, dtype=np.int64)
    V, W, C = np.meshgrid(v, w, c, indexing="ij")
    return V.ravel(), W.ravel(), C.ravel()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--primes", type=int, nargs="+", required=True)
    ap.add_argument("--nmax", type=int, default=60)
    ap.add_argument("--chunk", type=int, default=8192)
    ap.add_argument("--out", default="lane6_complete.json")
    args = ap.parse_args()

    rows = []
    for p in args.primes:
        depth = min(rigour_limit(p), args.nmax)
        ok1, ok2 = verify_symmetries(p, depth)
        V, W, C = slice_grid(p)
        npts = V.size
        one = np.ones(1, np.int64)
        print("=" * 74)
        print("p = %d   complete slice {a=1,u=1} x (v,w,c): %d points   "
              "depth %d" % (p, npts, depth))
        print("   symmetry re-verification: T1 invariance %s, T2 invariance %s"
              % (ok1, ok2))
        assert ok1 and ok2, "symmetry verification failed at p=%d" % p

        t0 = time.time()
        keys = None
        acc = {}
        alive = []
        for start in range(0, npts, args.chunk):
            stop = min(start + args.chunk, npts)
            R = FpRing(p, stop - start)
            res = run(R, np.full(stop - start, 1, np.int64),
                      V[start:stop].copy(), W[start:stop].copy(), depth,
                      caps=CAPS, cval=C[start:stop].copy(),
                      aval=np.full(stop - start, 1, np.int64))
            if keys is None:
                keys = sorted(res["cond"], key=lambda k: (k[1], k[0]))
            ok = np.ones(stop - start, dtype=bool)
            for i, k in enumerate(keys):
                ok = ok & (res["cond"][k] % p == 0)
                acc[k] = acc.get(k, 0) + int(ok.sum())
            alive.append(np.nonzero(ok)[0] + start)
        alive = np.concatenate(alive)
        dt = time.time() - t0

        print("   nested survival (cumulative through each condition):")
        run_out = []
        for k in keys:
            run_out.append((k, acc[k]))
        shown = [x for x in run_out if x[1] > 0 or x[0][1] <= 27]
        for k, n in shown[:12]:
            print("      after %s[%d] : %d" % (k[0], k[1], n))
        if len(shown) > 12:
            print("      ... (all remaining conditions: 0 survivors)")
        print("   survivors of EVERY condition to rung %d : %d"
              % (depth, alive.size))
        for i in alive[:20]:
            print("      *** CANDIDATE (a,u,v,w,c) = (1,1,%d,%d,%d)"
                  % (V[i], W[i], C[i]))

        # follow the three-condition survivors
        n3key = ("p3", 24)
        R = FpRing(p, npts)
        deeper = []
        # recompute cheaply only for the level-3 set
        lvl = None
        for start in range(0, npts, args.chunk):
            stop = min(start + args.chunk, npts)
            Rc = FpRing(p, stop - start)
            res = run(Rc, np.full(stop - start, 1, np.int64),
                      V[start:stop].copy(), W[start:stop].copy(), 24,
                      caps=CAPS, cval=C[start:stop].copy(),
                      aval=np.full(stop - start, 1, np.int64))
            ok = np.ones(stop - start, dtype=bool)
            for n in (22, 23, 24):
                ok = ok & (res["cond"][("p3", n)] % p == 0)
            idx = np.nonzero(ok)[0] + start
            lvl = idx if lvl is None else np.concatenate([lvl, idx])
        if lvl.size:
            Rc = FpRing(p, lvl.size)
            res = run(Rc, np.full(lvl.size, 1, np.int64), V[lvl].copy(),
                      W[lvl].copy(), depth, caps=CAPS, cval=C[lvl].copy(),
                      aval=np.full(lvl.size, 1, np.int64))
            for i in range(lvl.size):
                first = None
                for k in keys:
                    if res["cond"][k][i] % p != 0:
                        first = k
                        break
                deeper.append(dict(v=int(V[lvl[i]]), w=int(W[lvl[i]]),
                                   c=int(C[lvl[i]]),
                                   first_fail=list(first) if first else None))
        print("   three-condition solutions (u=1,a=1): %d  %s   [%.1fs]"
              % (lvl.size,
                 "; ".join("(v,w,c)=(%d,%d,%d) dies at %s"
                           % (d["v"], d["w"], d["c"], d["first_fail"])
                           for d in deeper) or "-", dt))
        rows.append(dict(p=p, npts=npts, depth=depth,
                         cumulative={"%s%d" % k: acc[k] for k in keys},
                         level3=deeper, survivors=int(alive.size),
                         seconds=dt))
        print()

    tot3 = sum(len(r["level3"]) for r in rows)
    print("=" * 74)
    print("TOTAL over %d primes: %d three-condition solutions, %d survivors "
          "of the full tower" % (len(rows), tot3,
                                 sum(r["survivors"] for r in rows)))
    fails = sorted({tuple(d["first_fail"]) for r in rows for d in r["level3"]
                    if d["first_fail"]})
    print("distinct first-failure rungs of those solutions:", fails)
    print("mean number of three-condition solutions per prime: %.3f"
          % (tot3 / float(len(rows))))
    with open(args.out, "w") as fh:
        json.dump(rows, fh, indent=1)
    print("wrote", args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
