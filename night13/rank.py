"""night13 stage 2c -- ranking the characteristic-2 survivors of the screen.

Survivors of the unavoidable-singleton screen exist only in a characteristic
dividing BOTH extreme-ray factors 2*e0 and 3*(m-e1); at m = 42 that is
char 2, and exactly the supports whose largest exponent e1 is even (then
m - e1 is even, so 3*(m-e1) = 0 mod 2, and 2*e0 = 0 mod 2 always).

Ranking, as specified: fewest NEAR-SINGLETON rows, i.e. mandatory bracket rows
with exactly two adjustable routes over the maximal pools, computed in the
characteristic in which the support survives.  Ties: fewest one-route rows,
then lexicographic order on the support.

The census is vectorised: all |P| x |Q| pairs at once, keys packed as
i*(3m+2) + j, leading x leading pairs masked out, routes with factor = 0 mod
char masked out, then a bincount.
"""

import itertools
import json
import math
import os
import time

import numpy as np

import screen

HERE = os.path.dirname(os.path.abspath(__file__))


def census_np(SP, SQ, Plow, Qlow, m, char):
    P = np.array(SP + Plow, dtype=np.int64)
    Q = np.array(SQ + Qlow, dtype=np.int64)
    nSP, nSQ = len(SP), len(SQ)
    W = 3 * m + 2
    key = ((P[:, None, 0] + Q[None, :, 0] - 1) * W
           + (P[:, None, 1] + Q[None, :, 1] - 1))
    fac = P[:, None, 0] * Q[None, :, 1] - P[:, None, 1] * Q[None, :, 0]
    good = (fac % char != 0) if char else (fac != 0)
    adj = np.ones(key.shape, dtype=bool)
    adj[:nSP, :nSQ] = False                      # leading x leading cancels
    mask = good & adj
    k = key[mask]
    cnt = np.bincount(k)
    const_key = (0 - 1 + 1) * W + (0 - 1 + 1)    # row (0,0) packed
    n1 = int(((cnt == 1)).sum())
    n2 = int(((cnt == 2)).sum())
    if const_key < len(cnt):
        if cnt[const_key] == 1:
            n1 -= 1
        elif cnt[const_key] == 2:
            n2 -= 1
    return {"n_rows": int((cnt > 0).sum()), "n_1_route": n1, "n_2_route": n2,
            "constant_row_routes": int(cnt[const_key])
            if const_key < len(cnt) else 0}


def survivors(m, char=2, sizes=(3, 4, 5, 6)):
    exps = screen.exponents(m, 2)
    out = []
    t0 = time.time()
    for s in sizes:
        for E in itertools.combinations(exps, s):
            e0, e1 = min(E), max(E)
            if math.gcd(2 * e0, 3 * (m - e1)) % char:
                continue
            r = screen.analyse(list(E), m, 1, 0, char=char)
            if not r["survives"]:
                continue
            SP, SQ = screen.leading_supports(list(E), m, char)
            hp = screen.K.hull(SP + [(0, 0), (1, 0)])
            hq = screen.K.hull(SQ + [(0, 0), (0, 1)])
            Plow = screen.pool(hp, 1, 2 * m, 2 * m)
            Qlow = screen.pool(hq, 0, 3 * m, 3 * m, drop_origin=True)
            c = census_np(SP, SQ, Plow, Qlow, m, char)
            out.append({"E": list(E), "size": s, "char": char,
                        "n_supp_H2": len(SP), "n_supp_H3": len(SQ),
                        "n_pool_P": len(Plow), "n_pool_Q": len(Qlow),
                        **c})
        print("  size %d done, %d survivors so far (%.1fs)"
              % (s, len(out), time.time() - t0), flush=True)
    out.sort(key=lambda r: (r["n_2_route"], r["n_1_route"], r["E"]))
    return out


if __name__ == "__main__":
    res = {}
    for m in (42,):
        rows = survivors(m)
        res[str(m)] = {"n_survivors": len(rows), "ranked": rows}
        print("m=%d: %d char-2 survivors; top 5:" % (m, len(rows)))
        for r in rows[:5]:
            print("   ", r["E"], "2-route rows", r["n_2_route"],
                  "1-route rows", r["n_1_route"], "rows", r["n_rows"])
    json.dump(res, open(os.path.join(HERE, "rank_char2.json"), "w"), indent=1)
