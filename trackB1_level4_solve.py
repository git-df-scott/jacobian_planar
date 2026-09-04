#!/usr/bin/env python3
"""CONSTRUCTIVE proof that level 4 never obstructs — the spiral was an artifact.

Level 4 is the ring quadratic (3/4) X^2 + beta X + gamma = 0 in R = F_p[z]/(S),
X := P_6 mod S.  Completing the square gives (X + (2/3)beta)^2 = D with
D = (4/9)beta^2 - (4/3)gamma, and MEASUREMENT SAYS D == 0 IN R, always.
So level 4 is the PERFECT SQUARE condition

        ( X + (2/3) beta )^2  ==  0     in    R = F_p[z]/(S),

which is always solvable.  Its solution set: Y := X + (2/3)beta must satisfy
S | Y^2, i.e. H(S) | Y with H the half-radical, so with deg Y <= 3

    component I   S ~ A^2 (A squarefree quadratic):  Y = A * (linear)   [2 free]
    component II  S ~ A^2 B:                          Y = c * A B        [1 free]

and then P_6 = X + S*Z with deg Z <= 4 [5 more free].  This script CONSTRUCTS
such a P_6 and verifies rem(N_4, S^3) == 0 directly from build_N -- i.e. it
does not trust the beta/gamma extraction at all.
"""
import random, sys
from collections import Counter
from trackB1_sqrt import pmul, padd, pscal, ptrim, pdiv_exact
from trackB1_cascade_general import (prem, component1_S, component2_S,
                                     half_radical)
from trackB1_offbyone_check import build_N, ppow
from trackB1_level4 import level4_data

p = 65521

def solve_level4(S, P7, rng, a=1, b=1):
    """Return a P_6 satisfying level 4 exactly, or None."""
    res = level4_data(S, P7, a, b)
    if res is None or res[0] == "LOW_DIGIT_OBSTRUCTION":
        return None, "low-digit obstruction"
    D, beta, gamma = res
    if ptrim(list(D)):
        return None, "D nonzero (would need a square root in R)"
    inv3 = pow(3, p - 2, p)
    X0 = prem(pscal(beta, (-2 * inv3) % p, p), S, p)      # -(2/3) beta
    H = half_radical(S, p)                                 # Y must be H * (...)
    dY = 3 - (len(H) - 1)
    if dY < 0:
        Y = []
    else:
        Y = pmul(H, [rng.randrange(p) for _ in range(dY + 1)], p)
    Z = [rng.randrange(p) for _ in range(5)]               # deg Z <= 4
    P6 = padd(padd(X0, Y, p), pmul(S, Z, p), p)
    lo, hi = 0, 8
    if len(P6) - 1 > hi:
        P6 = ptrim(P6[:hi + 1])
    return P6, "ok"

def check(S, P7, P6, a=1, b=1):
    P = {8: pscal(pmul(S, S, p), a, p), 7: P7, 6: P6}
    for w in range(5, -2, -1):
        P[w] = []
    N = build_N(S, P, 4, a, b)
    if N is None:
        return None
    S3 = pmul(pmul(S, S, p), S, p)
    return not ptrim(list(prem(N, S3, p)))

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    random.seed(seed)
    rng = random.Random(seed + 1000)
    print("CONSTRUCTIVE level-4 solve, verified against build_N directly\n")
    for tag in ("I", "II"):
        tally = Counter()
        for _ in range(n):
            if tag == "I":
                A = [1, random.randrange(p), random.randrange(1, p)]
                S = component1_S(A, 1, p)
                Dv = ppow(A, 2)
            else:
                S = None
                for _ in range(400):
                    u, v = random.randrange(1, p), random.randrange(1, p)
                    S = component2_S(u, v, 1, p)
                    if S:
                        break
                if S is None:
                    continue
                a1 = (2 * (5 * u * u - 4 * v)) % p
                a0 = (u * (7 * u * u - 12 * v)) % p
                Dv = pmul(ppow(ptrim([a0, a1]), 2), ptrim([v % p, u % p, 1]), p)
            if S is None:
                continue
            dM = 8 - (len(Dv) - 1)
            M = [random.randrange(p) for _ in range(dM + 1)]
            P7 = pmul(Dv, M, p)
            P6, why = solve_level4(S, P7, rng)
            if P6 is None:
                tally[why] += 1
                continue
            ok = check(S, P7, P6)
            tally["LEVEL 4 SATISFIED" if ok else "constructed P_6 FAILS"] += 1
        tot = sum(tally.values())
        print(f"  component {tag}: ({tot} samples)")
        for k, c in sorted(tally.items(), key=lambda t: -t[1]):
            print(f"     {k:<40} {c}/{tot}")
        print()
