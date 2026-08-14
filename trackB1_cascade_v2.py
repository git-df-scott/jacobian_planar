#!/usr/bin/env python3
"""CORRECTED cascade for GGHV Prop 4.3 case (1) — right level<->variable pairing.

Level m constrains P_{10-m}, not P_{9-m} (see trackB1_offbyone_check.py):

    m = 2   H(S) | P_7       (quadratic; imposed by parametrization)
    m = 3   S | P_7          (pure condition on P_7)
    m = 4   quadratic in P_6; ALWAYS solvable, (X + (2/3)beta)^2 = 0 in R
    m = 5..11  LINEAR in P_{10-m} = P_5, P_4, P_3, P_2, P_1, P_0, P_-1
    m = 12..22 pure obstructions (no new variable)

then N(Q)-support, the vanishing conditions, and the bottom equation (C4),
all via cascade_bracket() with the SCALE-INVARIANT C4 test.

Free data: S (3 params on either component), P_7 = S*M with deg M <= 4
(5 params), plus the kernel directions of the per-level solves.  Those free
directions are the search space -- randomizing them is a weak search, so this
module exposes them so they can be swept or carried symbolically.

Every level asserts that its condition is independent of the slices BELOW the
one it solves for; if that ever fails the run aborts rather than reporting a
verdict (the failure mode that produced the retracted spiral).
"""
import random, sys
from collections import Counter
from trackB1_sqrt import pmul, padd, pscal, ptrim, pdiv_exact, prange
from trackB1_cascade_general import (prem, component1_S, component2_S,
                                     half_radical)
from trackB1_offbyone_check import build_N, ppow
from trackB1_level4 import level4_data
from trackB1_bracket_audit import cascade_bracket

p = 65521

def _cond(S, P, m, wvar, val, a, b):
    Q = dict(P)
    Q[wvar] = ptrim(list(val))
    N = build_N(S, Q, m, a, b)
    if N is None:
        return None
    S3 = pmul(pmul(S, S, p), S, p)
    return prem(N, S3, p)

def solve_linear_level(S, P, m, wvar, rng, randfree, a=1, b=1):
    """Solve level m for P_wvar (linear).  Returns (P_wvar, nfree) or None."""
    lo, hi = prange(wvar)
    n = hi - lo + 1
    base = _cond(S, P, m, wvar, [], a, b)
    if base is None:
        return None, None, "LADDER_BREAK"
    cols = []
    for i in range(n):
        ci = _cond(S, P, m, wvar, [0] * (lo + i) + [1], a, b)
        if ci is None:
            return None, None, "LADDER_BREAK"
        cols.append(padd(ci, pscal(base, -1, p), p))
        # linearity check: value at 2*e_i must be base + 2*col_i
        c2 = _cond(S, P, m, wvar, [0] * (lo + i) + [2], a, b)
        if c2 is None or ptrim(list(padd(c2, pscal(padd(base,
                pscal(cols[-1], 2, p), p), -1, p), p))):
            return None, None, "NONLINEAR_LEVEL"
    rows = max([len(c) for c in cols] + [len(base), 1])
    Mx = [[(cols[k][r] if r < len(cols[k]) else 0) for k in range(n)]
          + [(-base[r]) % p if r < len(base) else 0] for r in range(rows)]
    row, piv_of = 0, {}
    for col in range(n):
        piv = next((r for r in range(row, rows) if Mx[r][col]), None)
        if piv is None:
            continue
        Mx[row], Mx[piv] = Mx[piv], Mx[row]
        inv = pow(Mx[row][col], p - 2, p)
        Mx[row] = [(v * inv) % p for v in Mx[row]]
        for r in range(rows):
            if r != row and Mx[r][col]:
                f = Mx[r][col]
                Mx[r] = [(Mx[r][c] - f * Mx[row][c]) % p for c in range(n + 1)]
        piv_of[col] = row
        row += 1
    if any(all(Mx[r][c] == 0 for c in range(n)) and Mx[r][n]
           for r in range(rows)):
        return None, None, "OBSTRUCTED"
    free = [c for c in range(n) if c not in piv_of]
    fv = {c: (rng.randrange(p) if randfree else 0) for c in free}
    sol = [0] * (hi + 1)
    for c, v in fv.items():
        sol[lo + c] = v
    for col in range(n):
        if col in piv_of:
            r = piv_of[col]
            v = Mx[r][n]
            for c2 in free:
                v = (v - Mx[r][c2] * fv[c2]) % p
            sol[lo + col] = v
    return ptrim(sol), len(free), "ok"

def solve_level4(S, P, rng, randfree, a=1, b=1):
    P7 = P[7]
    res = level4_data(S, P7, a, b)
    if res is None or res[0] == "LOW_DIGIT_OBSTRUCTION":
        return None, None, "L4_LOW_DIGIT"
    D, beta, gamma = res
    if ptrim(list(D)):
        return None, None, "L4_D_NONZERO"
    inv3 = pow(3, p - 2, p)
    X0 = prem(pscal(beta, (-2 * inv3) % p, p), S, p)
    H = half_radical(S, p)
    dY = 3 - (len(H) - 1)
    Y = pmul(H, [(rng.randrange(p) if randfree else 0)
                 for _ in range(dY + 1)], p) if dY >= 0 else []
    Z = [(rng.randrange(p) if randfree else 0) for _ in range(5)]
    P6 = padd(padd(X0, Y, p), pmul(S, Z, p), p)
    lo, hi = prange(6)
    if len(P6) - 1 > hi:
        return None, None, "L4_DEGREE"
    nfree = (dY + 1 if dY >= 0 else 0) + 5
    return ptrim(P6), nfree, "ok"

def run_v2(S, M, rng, randfree=True, a=1, b=1, indep_check=True):
    """P_7 = S*M.  Returns (verdict, level, freedims)."""
    P7 = pmul(S, M, p)
    lo7, hi7 = prange(7)
    if len(P7) - 1 > hi7:
        return ("P7_DEGREE", None, [])
    P = {8: pscal(pmul(S, S, p), a, p), 7: P7}
    for w in range(6, -2, -1):
        P[w] = []
    S3 = pmul(pmul(S, S, p), S, p)
    # level 3: pure condition on P_7
    N3 = build_N(S, P, 3, a, b)
    if N3 is None:
        return ("LADDER_BREAK", 3, [])
    if ptrim(list(prem(N3, S3, p))):
        return ("OBSTRUCTED", 3, [])
    freedims = []
    # level 4 (quadratic)
    P6, nf, why = solve_level4(S, P, rng, randfree, a, b)
    if P6 is None:
        return (why, 4, freedims)
    P[6] = P6
    freedims.append((4, 6, nf))
    # levels 5..11 (linear)
    for m in range(5, 12):
        wvar = 10 - m
        if indep_check:
            # the level must not depend on slices below wvar
            probe = dict(P)
            probe[wvar] = []
            c_a = _cond(S, probe, m, wvar - 1 if wvar - 1 >= -1 else wvar,
                        [], a, b)
            if wvar - 1 >= -1:
                c_b = _cond(S, probe, m, wvar - 1,
                            [rng.randrange(p) for _ in range(4)], a, b)
                if c_a is not None and c_b is not None and \
                   ptrim(list(padd(c_a, pscal(c_b, -1, p), p))):
                    return ("DEPENDS_ON_LOWER_SLICE", m, freedims)
        sol, nf, why = solve_linear_level(S, P, m, wvar, rng, randfree, a, b)
        if sol is None:
            return (why, m, freedims)
        P[wvar] = sol
        freedims.append((m, wvar, nf))
    plow = {w: P[w] for w in range(7, -2, -1)}
    res = cascade_bracket(S, a, b, plow, p)
    return (res["verdict"], res.get("level"), freedims)

def gen_component(tag, rng):
    if tag == "I":
        A = [1, rng.randrange(p), rng.randrange(1, p)]
        S = component1_S(A, 1, p)
    else:
        S = None
        for _ in range(400):
            u, v = rng.randrange(1, p), rng.randrange(1, p)
            S = component2_S(u, v, 1, p)
            if S:
                break
    return S

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    randfree = not (len(sys.argv) > 3 and sys.argv[3] == "zero")
    rng = random.Random(seed)
    print(f"CORRECTED CASCADE  (p={p}, seed={seed}, "
          f"free-dirs={'random' if randfree else 'zero'})\n")
    survivors = []
    for tag in ("I", "II"):
        tally = Counter()
        fd = None
        for _ in range(n):
            S = gen_component(tag, rng)
            if S is None:
                continue
            M = [rng.randrange(p) for _ in range(5)]   # P_7 = S*M, deg M <= 4
            v, lvl, freedims = run_v2(S, M, rng, randfree)
            tally[(v, lvl)] += 1
            if freedims and fd is None:
                fd = freedims
            if v == "PROPORTIONAL":
                survivors.append((S, M))
        tot = sum(tally.values())
        print(f"  component {tag}: ({tot} samples)")
        for k, c in sorted(tally.items(), key=lambda t: -t[1]):
            print(f"     {str(k):<34} {c}/{tot}")
        if fd:
            print(f"     free dims (level, weight, n): {fd}")
        print()
    print(f"SURVIVORS: {len(survivors)}")
