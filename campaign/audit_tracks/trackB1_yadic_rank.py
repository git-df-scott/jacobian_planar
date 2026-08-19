#!/usr/bin/env python3
"""How much do N(Q)'s conditions actually constrain P?  Measure the Jacobian.

The y-adic engine (trackB1_yadic_verdict.py) makes Q a function of P alone.
The live conditions are N(Q)'s upper edge,

    coefficient of x^i in Q_j must vanish for i < j - 12   (13 <= j <= 24),

which is 1+2+...+9 = 45 conditions by j = 21 and 78 through j = 24, against P's
61 lattice-point coefficients — plus termination (Q_j = 0 for j > 24) on top.

A naive "solve the order-j condition for the newest slice P_{j-1}" is WRONG and
reports spurious inconsistency: the i = 0 condition at j = 13 is untouched by
P_12, because N(P) forces P_12 to have i >= 4, so P_12 contributes to Q_13 only
at i >= 5.  The low-i conditions are driven by the low-i COLUMNS of P.  (This is
the same class of mistake as the retracted off-by-one: guessing which unknown a
condition constrains instead of measuring it.)

So measure: the Jacobian of the conditions with respect to all 61 coefficients
of P, at random points.  Its rank bounds the dimension of the solution variety
from above (dim <= 61 - rank locally), and the per-condition-block ranks show
which conditions are independent and which are consequences.
"""
import random, sys
from trackB1_yadic_verdict import (p, PR, QR, yadic_Q, random_P, trim)

def param_index():
    """Flat list of (j, i) for every lattice point of N(P)."""
    idx = []
    for j in sorted(PR):
        lo, hi = PR[j]
        for i in range(lo, hi + 1):
            idx.append((j, i))
    return idx

IDX = param_index()

def P_from_vec(vec):
    P = {}
    for (j, i), val in zip(IDX, vec):
        P.setdefault(j, [])
        while len(P[j]) <= i:
            P[j].append(0)
        P[j][i] = val % p
    for j in list(P):
        P[j] = trim(P[j])
    return P

def vec_from_P(P):
    return [(P.get(j, [])[i] if i < len(P.get(j, [])) else 0) for (j, i) in IDX]

def conditions(vec, jlo=13, jhi=24):
    """All low-i conditions as a flat list of F_p values."""
    P = P_from_vec(vec)
    if not P.get(0) or len(P[0]) < 2 or P[0][1] == 0:
        return None
    Q = yadic_Q(P, jhi + 1)
    out = []
    for j in range(jlo, jhi + 1):
        lo = max(0, j - 12)
        q = Q.get(j, [])
        for i in range(lo):
            out.append(q[i] if i < len(q) else 0)
    return out

def rank_mod_p(M):
    if not M or not M[0]:
        return 0
    M = [row[:] for row in M]
    rows, cols = len(M), len(M[0])
    r = 0
    for c in range(cols):
        pr = next((i for i in range(r, rows) if M[i][c] % p), None)
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        iv = pow(M[r][c], p - 2, p)
        M[r] = [x * iv % p for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c] % p:
                f = M[i][c]
                M[i] = [(M[i][k] - f * M[r][k]) % p for k in range(cols)]
        r += 1
        if r == rows:
            break
    return r

def jacobian(vec, jlo=13, jhi=24, h=1):
    base = conditions(vec, jlo, jhi)
    if base is None:
        return None, None
    J = []
    for k in range(len(IDX)):
        v2 = list(vec)
        v2[k] = (v2[k] + h) % p
        c2 = conditions(v2, jlo, jhi)
        if c2 is None:
            return None, None
        J.append([(c2[r] - base[r]) % p for r in range(len(base))])
    # J is params x conditions; transpose to conditions x params
    JT = [[J[c][r] for c in range(len(IDX))] for r in range(len(base))]
    return JT, base

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    rng = random.Random(seed)
    print(f"P has {len(IDX)} coefficients (lattice points of N(P))\n")
    print(f"{'j-range':<12}{'#conditions':>12}{'Jacobian rank':>16}"
          f"{'dim bound':>12}")
    for jhi in (13, 14, 16, 18, 20, 21, 22, 23, 24):
        ranks, ncond = [], None
        for _ in range(n):
            vec = vec_from_P(random_P(rng))
            JT, base = jacobian(vec, 13, jhi)
            if JT is None:
                continue
            ncond = len(JT)
            ranks.append(rank_mod_p(JT))
        if ranks:
            r = max(ranks)
            print(f"{'13..'+str(jhi):<12}{ncond:>12}{r:>16}"
                  f"{max(0, len(IDX)-r):>12}")
