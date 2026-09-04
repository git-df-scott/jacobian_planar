#!/usr/bin/env python3
"""The y-adic engine: Q is determined by P, and Q_1 = x^2 / p_10 exactly.

Expand in powers of y:  P = sum_j P_j(x) y^j,  Q = sum_j Q_j(x) y^j.
Then [P,Q] = P_x Q_y - P_y Q_x = x^2 reads, coefficient of y^k,

    sum_{a+b=k} P_a' (b+1) Q_{b+1}  -  sum_{a+b=k} (a+1) P_{a+1} Q_b'
        = x^2 * [k == 0].

From N(P) the j = 0 row is {(0,0),(1,0)}, so P_0 = p_00 + p_10 x with
p_10 != 0 (vertex).  From N(Q) the j = 0 row is {(0,0)} alone (its lower edge
runs (0,0)-(2,1), so j = 0 forces i <= 0), so Q_0 = q_00 is a CONSTANT and
Q_0' = 0.  The k = 0 equation is therefore

        p_10 * Q_1 = x^2      =>      ***  Q_1 = x^2 / p_10  ***

exactly -- no freedom at all.  N(Q)'s j = 1 row is {(0,1),(1,1),(2,1)}, so this
forces q_01 = q_11 = 0 and q_21 = 1/p_10, reproducing v'(0) = 0 and V'(0) = 0
(derived independently in trackB1_x0_theorem.py) and the normalization
p_10 q_21 = 1.

For k >= 1 the equation solves for Q_{k+1} because P_0' = p_10 is a nonzero
constant:

    (k+1) p_10 Q_{k+1} = x^2-free rearrangement of the lower terms,

so **Q is entirely determined by P** (given p_10 and q_00) -- the y-adic
analogue of "Q is not an unknown", but with no square roots, no S-denominators
and no formal series.  The degree bound deg Q_j <= (j+3)/2 propagates
automatically, so N(Q)'s lower-right edge costs nothing; the real conditions are
N(Q)'s UPPER edge (i >= j - 12 for j > 12) and TERMINATION (Q_j = 0 for j > 24).
"""
import sys
from fractions import Fraction

def polmul(a, b):
    if not a or not b:
        return []
    o = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    o[i + j] += x * y
    return trim(o)

def poladd(a, b):
    n = max(len(a), len(b))
    return trim([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
                 for i in range(n)])

def polscal(a, c):
    return trim([x * c for x in a]) if c else []

def trim(a):
    while a and a[-1] == 0:
        a.pop()
    return a

def deriv(a):
    return trim([i * a[i] for i in range(1, len(a))]) if len(a) > 1 else []

def yadic_Q(P, N, p10, q00):
    """P: dict j -> coeff list in x.  Returns Q: dict j -> coeff list."""
    Q = {0: [q00]}
    inv10 = Fraction(1, 1) / p10
    Q[1] = [0, 0, inv10]                       # x^2 / p_10
    for k in range(1, N):
        # (k+1) p_10 Q_{k+1} = -sum_{a+b=k, a>=1} P_a'(b+1)Q_{b+1}
        #                      + sum_{a+b=k} (a+1) P_{a+1} Q_b'
        acc = []
        for a in range(1, k + 1):
            b = k - a
            if a in P and (b + 1) in Q:
                acc = poladd(acc, polscal(polmul(deriv(P[a]), Q[b + 1]),
                                          -(b + 1)))
        for a in range(0, k + 1):
            b = k - a
            if (a + 1) in P and b in Q:
                acc = poladd(acc, polscal(polmul(P[a + 1], deriv(Q[b])),
                                          (a + 1)))
        Q[k + 1] = polscal(acc, Fraction(1, (k + 1)) / p10)
    return Q

def npoly_P_rows():
    """i-range of N(P) at each j (0..16)."""
    rows = {}
    for j in range(17):
        lo = max(0, j - 8)
        hi = min(8, j // 2 + 1)
        if lo <= hi:
            rows[j] = (lo, hi)
    return rows

def npoly_Q_rows():
    """N(Q) has TWO lower edges: (0,0)-(2,1) gives j >= i/2, i.e. i <= 2j, and
    (2,1)-(12,21) gives j >= 2i-3, i.e. i <= (j+3)/2.  Both bind (the first for
    j <= 1, the second for j >= 2); omitting i <= 2j wrongly admits (1,0)."""
    rows = {}
    for j in range(25):
        lo = max(0, j - 12)
        hi = min(12, 2 * j, (j + 3) // 2)
        if lo <= hi:
            rows[j] = (lo, hi)
    return rows

def witness_check():
    """P = T^2, Q = T^3 with T = y^4 + x^4 y^8 + t x^4 y^7 has [P,Q] = 0, so it
    is NOT a Keller pair; instead validate the recursion on a genuine pair."""
    # Genuine simple pair: P = x, Q = x^2 y / 1  ->  [P,Q] = P_x Q_y - P_y Q_x
    #                                             = 1*x^2 - 0 = x^2. Good anchor.
    P = {0: [0, 1]}                    # P = x, so p_10 = 1, p_00 = 0
    Q = yadic_Q(P, 6, Fraction(1), Fraction(0))
    ok = (Q[1] == [0, 0, 1]) and all(not Q[j] for j in range(2, 7))
    return ok, Q

def bracket_check(P, Q, N):
    """Verify [P,Q] = x^2 through y^{N-2}: returns list of offending k."""
    bad = []
    for k in range(N - 1):
        acc = []
        for a in range(0, k + 1):
            b = k - a
            if a in P and (b + 1) in Q:
                acc = poladd(acc, polscal(polmul(deriv(P[a]), Q[b + 1]), b + 1))
            if (a + 1) in P and b in Q:
                acc = poladd(acc, polscal(polmul(P[a + 1], deriv(Q[b])),
                                          -(a + 1)))
        want = [0, 0, Fraction(1)] if k == 0 else []
        if trim(list(acc)) != trim(list(want)):
            bad.append(k)
    return bad

def selfcheck(trials=5, N=9, seed=3):
    """Random P with p_10 != 0: the recursion must reproduce [P,Q] = x^2."""
    import random
    rng = random.Random(seed)
    rows = npoly_P_rows()
    ok = 0
    for _ in range(trials):
        P = {}
        for j, (lo, hi) in rows.items():
            if j > N:
                continue
            P[j] = trim([0] * lo + [Fraction(rng.randint(-5, 5))
                                    for _ in range(hi - lo + 1)])
        P[0] = [Fraction(rng.randint(-5, 5)), Fraction(rng.randint(1, 5))]
        Q = yadic_Q(P, N, P[0][1], Fraction(rng.randint(-5, 5)))
        ok += not bracket_check(P, Q, N)
    return ok, trials

if __name__ == "__main__":
    a, b = selfcheck()
    print(f"SELFCHECK  random P -> recursion Q reproduces [P,Q] = x^2: {a}/{b}")
    ok, Q = witness_check()
    print("ANCHOR  P = x, Q = x^2 y  ([P,Q] = x^2):")
    print(f"   recursion gives Q_1 = {Q[1]} (expect [0,0,1]) and "
          f"Q_j = 0 for 2 <= j <= 6: {ok}")
    print("\nN(P) rows (j: i-range):")
    rp = npoly_P_rows()
    print("   " + "  ".join(f"{j}:{lo}-{hi}" for j, (lo, hi) in rp.items()))
    print(f"   total lattice points (free coefficients of P): "
          f"{sum(hi-lo+1 for lo,hi in rp.values())}")
    rq = npoly_Q_rows()
    print("\nN(Q) rows (j: i-range):")
    print("   " + "  ".join(f"{j}:{lo}-{hi}" for j, (lo, hi) in rq.items()))
    print("\nj = 0 row of N(Q):", rq[0], " -> Q_0 is a CONSTANT, so Q_0' = 0")
    print("j = 1 row of N(Q):", rq[1],
          " -> Q_1 = x^2/p_10 forces q_01 = q_11 = 0, q_21 = 1/p_10")
    print("\nSo Q is determined by P; the live conditions are N(Q)'s upper edge")
    print("(i >= j-12 for j > 12) and TERMINATION Q_j = 0 for j > 24.")
