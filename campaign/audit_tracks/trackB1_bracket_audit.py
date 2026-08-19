#!/usr/bin/env python3
"""AUDIT: is the cascade's C4 test too strict?

cascade() in trackB1_sqrt.py declares INHOM_FAIL unless [P_8, F_-10] equals
-z^2 EXACTLY.  But [P,Q] = kappa x^2 with kappa != 0 is an equally good Keller
pair (replace Q by Q/kappa; the Newton polygon is unchanged).  So the
scale-invariant content of (C4) is

        [P_8, F_-10]  PROPORTIONAL to z^2,  with nonzero constant.

This script re-runs the cascade on both components and classifies the actual
bracket instead of testing equality:

    ZERO          br = 0                       -> genuine failure (witness-like)
    PROPORTIONAL  br = kappa z^2, kappa != 0    -> *** SURVIVOR ***
    OFF_SUPPORT   br has a monomial != z^2      -> genuine failure

If any sample lands in PROPORTIONAL, every INHOM_FAIL verdict in the campaign
needs re-reading.
"""
import random, sys
from collections import Counter
from trackB1_sqrt import (pmul, padd, pscal, ptrim, pdiv_exact, prange,
                          qrange, slice_bracket)
from trackB1_cascade_general import (run, half_radical, component1_S,
                                     component2_S, KDIM)
import trackB1_cascade_general as CG

def cascade_bracket(s, a, b, plow, p, wmin=-10):
    """Same as trackB1_sqrt.cascade but RETURNS the raw bracket + condition log."""
    ginv = pow(a, p - 2, p)
    gamma = (b * b % p) * pow(ginv, 3, p) % p
    P = {8: pscal(pmul(s, s, p), a, p)}
    for w in range(7, -2, -1):
        P[w] = ptrim(list(plow.get(w, [])))
    P2 = {}
    for w1 in P:
        for w2 in P:
            P2[w1 + w2] = padd(P2.get(w1 + w2, []), pmul(P[w1], P[w2], p), p)
    P3 = {}
    for W2 in P2:
        for w3 in P:
            P3[W2 + w3] = padd(P3.get(W2 + w3, []), pmul(P2[W2], P[w3], p), p)
    s3 = pmul(pmul(s, s, p), s, p)
    F = {12: pscal(s3, b, p)}
    twoF12 = pscal(s3, 2 * b, p)
    for m in range(1, 12 - wmin + 1):
        W = 24 - m
        N = pscal(P3.get(W, []), gamma, p)
        for q_ in list(F):
            pq = W - q_
            if pq in F and pq <= 11 and q_ <= 11:
                N = padd(N, pscal(pmul(F[pq], F[q_], p), -1, p), p)
        Fw = pdiv_exact(N, twoF12, p)
        if Fw is None:
            return {"verdict": "LADDER_FAIL", "level": 12 - m}
        F[12 - m] = Fw
    for w in range(12, -2, -1):
        r = qrange(w)
        fw = F.get(w, [])
        if not fw:
            continue
        if r is None:
            return {"verdict": "SUPPORT_FAIL", "level": w}
        lo, hi = r
        for i, c in enumerate(fw):
            if c and not (lo <= i <= hi):
                return {"verdict": "SUPPORT_FAIL", "level": w, "i": i}
    for w in range(-2, -10, -1):
        if F.get(w, []):
            return {"verdict": "VANISH_FAIL", "level": w}
    br = ptrim(list(slice_bracket(P[8], 8, F.get(-10, []), -10, p)))
    if not br:
        cls = "ZERO"
    elif len(br) == 3 and br[0] == 0 and br[1] == 0 and br[2] != 0:
        cls = "PROPORTIONAL"
    else:
        cls = "OFF_SUPPORT"
    return {"verdict": cls, "bracket": br,
            "kappa": br[2] if cls == "PROPORTIONAL" else None}

def sweep(name, gen, n, p, randfree):
    tally = Counter()
    examples = []
    tried = 0
    while sum(tally.values()) < n and tried < 60 * n:
        tried += 1
        got = gen()
        if got is None:
            continue
        S, M = got
        v, lvl, P = run(S, M, p, rand_free=randfree)
        if v != "SURVIVED_LADDER":
            tally[(v, lvl)] += 1
            continue
        plow = {w: P[w] for w in range(7, -2, -1) if w in P}
        res = cascade_bracket(S, 1, 1, plow, p)
        key = (res["verdict"], res.get("level"))
        tally[key] += 1
        if res["verdict"] == "PROPORTIONAL":
            examples.append((S, M, res["kappa"]))
    print(f"\n=== {name} (n={sum(tally.values())}, "
          f"free-dirs={'random' if randfree else 'zero'}) ===")
    for k, c in sorted(tally.items(), key=lambda t: (-t[1], str(t[0]))):
        print(f"   {str(k):>30} : {c}")
    if examples:
        print(f"   *** {len(examples)} PROPORTIONAL survivors ***")
        for S, M, k in examples[:3]:
            print(f"       S={S}  M={M}  kappa={k}")
    return tally, examples

if __name__ == "__main__":
    p = 65521
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    randfree = len(sys.argv) > 3 and sys.argv[3] == "rand"
    random.seed(seed)

    def gen1():
        A = [1, random.randrange(p), random.randrange(1, p)]
        S = component1_S(A, 1, p)
        if S is None:
            return None
        H = half_radical(S, p)
        return S, [random.randrange(p) for _ in range(8 - (len(H) - 1) + 1)]

    def gen2():
        u, v = random.randrange(1, p), random.randrange(1, p)
        S = component2_S(u, v, 1, p)
        if S is None:
            return None
        H = half_radical(S, p)
        return S, [random.randrange(p) for _ in range(8 - (len(H) - 1) + 1)]

    sweep("COMPONENT I (perfect squares)", gen1, n, p, randfree)
    sweep("COMPONENT II (new locus)", gen2, n, p, randfree)
