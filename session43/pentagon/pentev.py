#!/usr/bin/env python3
"""Fast numeric evaluator for the pentagon conditions over F_p.

The exported system pent_L23.ms has degree 22 and 1.08M terms because every
intermediate Q level is substituted away.  The underlying object is a
straight-line recursion, so at a NUMERIC point the same conditions cost a few
milliseconds.  This turns a Groebner problem into point evaluation.

Recursion (from wave1/w1_h1b_sparsity.py, gauges p_0_0 = 0, p_0_1 = 1):
    Q[0] = 1 ; Q[1] = x^2
    Q[k+1] = (1/(k+1)) * sum_{a=1..k} [ a*P[a]*Q[b]' - (k+1-a)*P[a]'*Q[b] ],
             b = k+1-a
Conditions: Q[j][i] = 0 for j = 13..23, i = 0..j-13   (66 of them).
"""
p = 1000003

def P_rows(jmax=16):
    r = {}
    for j in range(jmax + 1):
        lo, hi = max(0, j - 8), min(8, j // 2 + 1)
        if lo <= hi:
            r[j] = (lo, hi)
    return r

PR = P_rows()
PARAMS = [(j, i) for j in sorted(PR) for i in range(PR[j][0], PR[j][1] + 1)]
VARS = [f"p_{j}_{i}" for (j, i) in PARAMS if (j, i) not in ((0, 0), (0, 1))]
VIDX = {v: k for k, v in enumerate(VARS)}
NV = len(VARS)

def xmul(A, B):
    if not A or not B:
        return []
    out = [0] * (len(A) + len(B) - 1)
    for i, a in enumerate(A):
        if not a:
            continue
        for j, b in enumerate(B):
            if b:
                out[i + j] = (out[i + j] + a * b) % p
    return out

def xadd(A, B):
    n = max(len(A), len(B))
    return [((A[i] if i < len(A) else 0) + (B[i] if i < len(B) else 0)) % p
            for i in range(n)]

def xscal(A, c):
    c %= p
    return [(a * c) % p for a in A] if c else []

def xderiv(A):
    return [(A[i] * i) % p for i in range(1, len(A))] if len(A) > 1 else []

def conditions(vals, jtop=23):
    """vals: dict name->int or list of length NV.  Returns list of 66 residues."""
    if not isinstance(vals, dict):
        vals = {VARS[k]: vals[k] for k in range(NV)}
    P = []
    for j in range(jtop + 2):
        if j not in PR:
            P.append([])
            continue
        lo, hi = PR[j]
        row = [0] * (hi + 1)
        for i in range(lo, hi + 1):
            if (j, i) == (0, 0):
                row[i] = 0
            elif (j, i) == (0, 1):
                row[i] = 1
            else:
                row[i] = vals.get(f"p_{j}_{i}", 0) % p
        P.append(row)
    Q = [[] for _ in range(jtop + 2)]
    Q[0] = [1]
    Q[1] = [0, 0, 1]
    for k in range(1, jtop + 1):
        acc = []
        for a in range(1, k + 1):
            b = k + 1 - a
            if b < 0 or a >= len(P) or not P[a] or not Q[b]:
                continue
            acc = xadd(acc, xscal(xmul(P[a], xderiv(Q[b])), a))
            acc = xadd(acc, xscal(xmul(xderiv(P[a]), Q[b]), -(k + 1 - a)))
        Q[k + 1] = xscal(acc, pow(k + 1, p - 2, p))
    out = []
    for j in range(13, jtop + 1):
        for i in range(0, j - 12):
            out.append(Q[j][i] % p if i < len(Q[j]) else 0)
    return out

LATE = [v for v in VARS if int(v.split("_")[1]) >= 12]
EARLY = [v for v in VARS if int(v.split("_")[1]) < 12]
