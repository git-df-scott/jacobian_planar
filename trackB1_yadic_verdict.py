#!/usr/bin/env python3
"""A COMPLETE, INDEPENDENT verdict engine for GGHV Prop 4.3 case (1).

Nothing here uses the weight grading, the square root T = P^{1/2}, the cusp
parametrization P_8 = a S^2, the S-classification, or the cascade.  It uses only

    [P,Q] = x^2,   N(P) and N(Q) exactly the two pentagons,

expanded in powers of y.  Since N(Q)'s j = 0 row is {(0,0)} alone, Q_0 is a
constant and Q_0' = 0; with P_0 = p_00 + p_10 x (N(P)'s j = 0 row) the order-y^0
equation is p_10 Q_1 = x^2.  Every higher order then solves for Q_{k+1} because
P_0' = p_10 is a nonzero constant:

    (k+1) p_10 Q_{k+1} = sum_{a+b=k} (a+1) P_{a+1} Q_b'
                       - sum_{a+b=k, a>=1} (b+1) P_a' Q_{b+1}

so **Q is a function of P**.  Note Q_{k+1} does NOT involve P_{k+1} (that term
carries Q_0' = 0), so the condition at order j involves P_0..P_{j-1} only, and
is LINEAR in the newest slice P_{j-1} (which enters solely through
P_{j-1}' Q_1 = P_{j-1}' x^2 / p_10).

The verdict conditions are exactly N(Q):

    j <= 12       i <= min(12, 2j, (j+3)/2)     -- propagates automatically
    13 <= j <= 24 additionally i >= j - 12      -- REAL conditions
    j > 24        Q_j = 0                       -- REAL conditions

Counting: the low-i conditions contribute 1+2+...+9 = 45 by j = 21, then 10, 12,
13 at j = 22, 23, 24, against P's 61 lattice-point coefficients.  The system is
already overdetermined at j = 23 -- before the termination conditions.
"""
import random, sys
from collections import Counter

p = 65521

# ------------------------------------------------------------------ polynomials
def pmul(a, b):
    if not a or not b:
        return []
    o = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    o[i + j] = (o[i + j] + x * y) % p
    return trim(o)

def padd(a, b):
    n = max(len(a), len(b))
    return trim([((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % p
                 for i in range(n)])

def pscal(a, c):
    c %= p
    return trim([x * c % p for x in a]) if c else []

def trim(a):
    while a and a[-1] == 0:
        a.pop()
    return a

def pderiv(a):
    return trim([i * a[i] % p for i in range(1, len(a))]) if len(a) > 1 else []

# ------------------------------------------------------------------- polygons
def P_rows(jmax=16):
    """i-range of N(P) at each j.  Lower edges: j >= 0 and j >= 2(i-1)."""
    r = {}
    for j in range(jmax + 1):
        lo, hi = max(0, j - 8), min(8, j // 2 + 1)
        if lo <= hi:
            r[j] = (lo, hi)
    return r

def Q_rows(jmax=24):
    """i-range of N(Q).  Lower edges: j >= i/2 (i.e. i <= 2j) and j >= 2i-3."""
    r = {}
    for j in range(jmax + 1):
        lo, hi = max(0, j - 12), min(12, 2 * j, (j + 3) // 2)
        if lo <= hi:
            r[j] = (lo, hi)
    return r

PR, QR = P_rows(), Q_rows()

# ------------------------------------------------------------------- recursion
def yadic_Q(P, N):
    """P: dict j -> coeff list (mod p), P[0] = [p_00, p_10] with p_10 != 0."""
    p10 = P[0][1]
    inv10 = pow(p10, p - 2, p)
    Q = {0: [0], 1: [0, 0, inv10]}          # Q_0 constant (set 0: gauge), Q_1
    for k in range(1, N):
        acc = []
        for a in range(0, k + 1):
            b = k - a
            if (a + 1) in P and b in Q:
                acc = padd(acc, pscal(pmul(P[a + 1], pderiv(Q[b])), a + 1))
            if a >= 1 and a in P and (b + 1) in Q:
                acc = padd(acc, pscal(pmul(pderiv(P[a]), Q[b + 1]), -(b + 1)))
        Q[k + 1] = pscal(acc, inv10 * pow(k + 1, p - 2, p) % p)
    return Q

def violations(Q, jmax):
    """Return the list of (j, kind, count) violations of N(Q)."""
    out = []
    for j in range(2, jmax + 1):
        q = Q.get(j, [])
        if not q:
            continue
        if j in QR:
            lo, hi = QR[j]
            low = [i for i, c in enumerate(q) if c and i < lo]
            high = [i for i, c in enumerate(q) if c and i > hi]
            if low:
                out.append((j, "below N(Q)", len(low)))
            if high:
                out.append((j, "above N(Q)", len(high)))
        else:
            out.append((j, "Q_j must vanish", len([c for c in q if c])))
    return out

def first_violation(P, jmax):
    Q = yadic_Q(P, jmax)
    v = violations(Q, jmax)
    return (v[0] if v else None), Q

# ------------------------------------------------------------------- generators
def random_P(rng, jmax=16):
    P = {}
    for j, (lo, hi) in PR.items():
        if j > jmax:
            continue
        P[j] = trim([0] * lo + [rng.randrange(p) for _ in range(hi - lo + 1)])
    P[0] = [rng.randrange(p), rng.randrange(1, p)]      # p_10 != 0
    return P

def solve_newest(P, j, rng):
    """The order-j condition is linear in P_{j-1}; solve it for P_{j-1}.
    Returns True if solvable (P is updated), False if inconsistent."""
    w = j - 1
    if w not in PR:
        return None
    lo, hi = PR[w]
    n = hi - lo + 1
    lo_q, hi_q = QR[j]

    def resid(vec):
        P2 = dict(P)
        P2[w] = trim([0] * lo + list(vec))
        Q = yadic_Q(P2, j)
        q = Q.get(j, [])
        return [q[i] if i < len(q) else 0 for i in range(lo_q)]

    base = resid([0] * n)
    cols = []
    for i in range(n):
        e = [0] * n
        e[i] = 1
        cols.append([(resid(e)[r] - base[r]) % p for r in range(len(base))])
    rows = len(base)
    M = [[cols[c][r] for c in range(n)] + [(-base[r]) % p] for r in range(rows)]
    piv, row = {}, 0
    for c in range(n):
        pr = next((r for r in range(row, rows) if M[r][c]), None)
        if pr is None:
            continue
        M[row], M[pr] = M[pr], M[row]
        iv = pow(M[row][c], p - 2, p)
        M[row] = [x * iv % p for x in M[row]]
        for r in range(rows):
            if r != row and M[r][c]:
                f = M[r][c]
                M[r] = [(M[r][k] - f * M[row][k]) % p for k in range(n + 1)]
        piv[c] = row
        row += 1
    if any(all(M[r][c] == 0 for c in range(n)) and M[r][n] for r in range(rows)):
        return False
    sol = [0] * n
    for c, r in piv.items():
        sol[c] = M[r][n]
    for c in range(n):
        if c not in piv:
            sol[c] = rng.randrange(p)
    # re-solve pivots against the random free choices
    sol2 = [0] * n
    free = {c: sol[c] for c in range(n) if c not in piv}
    for c, r in piv.items():
        val = M[r][n]
        for c2, fv in free.items():
            val = (val - M[r][c2] * fv) % p
        sol2[c] = val
    for c, fv in free.items():
        sol2[c] = fv
    P[w] = trim([0] * lo + sol2)
    return True

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "scan"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    jmax = int(sys.argv[4]) if len(sys.argv) > 4 else 26
    rng = random.Random(seed)

    print(f"N(P): {sum(hi-lo+1 for lo,hi in PR.values())} lattice points")
    print(f"low-i conditions by j=21: "
          f"{sum(max(0, j-12) for j in range(13,22))}; "
          f"through j=24: {sum(max(0,j-12) for j in range(13,25))}\n")

    if mode == "scan":
        tally = Counter()
        for _ in range(n):
            P = random_P(rng)
            v, _ = first_violation(P, jmax)
            tally[v[:2] if v else "SURVIVOR"] += 1
        print(f"RANDOM P (no conditions imposed), {n} samples:")
        for k, c in sorted(tally.items(), key=lambda t: -t[1])[:6]:
            print(f"   first violation {str(k):<34} {c}/{n}")
    elif mode == "solve":
        tally = Counter()
        for _ in range(n):
            P = random_P(rng)
            ok = True
            for j in range(13, 18):            # solve using P_12..P_16
                r = solve_newest(P, j, rng)
                if r is False:
                    tally[f"inconsistent at j={j}"] += 1
                    ok = False
                    break
            if not ok:
                continue
            v, _ = first_violation(P, jmax)
            tally[v[:2] if v else "SURVIVOR"] += 1
        print(f"P with orders j=13..17 SOLVED for P_12..P_16, {n} samples:")
        for k, c in sorted(tally.items(), key=lambda t: -t[1])[:8]:
            print(f"   {str(k):<40} {c}")
