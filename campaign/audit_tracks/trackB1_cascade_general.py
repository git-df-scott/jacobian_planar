#!/usr/bin/env python3
"""Cascade solver on ANY admissible S -- both components of the bottom criterion.

The bottom criterion (C4) is solvable exactly on two 3-dimensional components
(trackB1_star_full.py, trackB1_elliptic_locus.py):

  COMPONENT I   S = c A^2, deg A = 2                      (perfect squares)
  COMPONENT II  S = c A^2 B, B = z^2 + u z + v squarefree,
                A = 2(5u^2 - 4v) z + u(7u^2 - 12v)        (NEW, never searched)

Level 2 of the ladder is  S | P_7^2, i.e.  H(S) | P_7  with the HALF-RADICAL
H(S) = prod pi_i^ceil(e_i/2).  deg H = 2 on component I and 3 on component II
(A^3 C members included: H = A^2 C).  P_7 = H * M is imposed by parametrization,
never by an affine solve -- level 2 is the one quadratic level.

Levels >= 3 are linear in the newest slice and are solved exactly as in
trackB1_cascade_solve.py (which this reproduces when H = A).
"""
import random, sys
from collections import Counter
from trackB1_sqrt import (pmul, padd, pscal, pderiv, ptrim, pdiv_exact,
                          prange, qrange, slice_bracket)

# --------------------------------------------------------------- polynomials
def prem(f, g, p):
    f = list(f)
    if len(f) < len(g):
        return ptrim(f)
    inv = pow(g[-1], p - 2, p)
    for k in range(len(f) - len(g), -1, -1):
        c = (f[k + len(g) - 1] * inv) % p
        if c:
            for i, gi in enumerate(g):
                f[k + i] = (f[k + i] - c * gi) % p
    return ptrim(f[:len(g) - 1])

def pgcd(f, g, p):
    f, g = ptrim(list(f)), ptrim(list(g))
    while g:
        f, g = g, prem(f, g, p)
    if f:
        inv = pow(f[-1], p - 2, p)
        f = [(c * inv) % p for c in f]
    return f

def half_radical(S, p):
    """prod pi^ceil(e/2) for S = prod pi^e, via repeated gcd with derivative."""
    # squarefree decomposition (char p large): S = prod_k A_k^k
    out = [1]
    rem = ptrim(list(S))
    d = pderiv(rem, p)
    g = pgcd(rem, d, p)
    k = 1
    w = pdiv_exact(rem, g, p)
    while len(w) > 1:
        gg = pgcd(w, g, p)          # A_k = w / gg
        Ak = pdiv_exact(w, gg, p)
        if len(Ak) > 1:
            for _ in range((k + 1) // 2):
                out = pmul(out, Ak, p)
        g = pdiv_exact(g, gg, p) if gg else g
        w = gg
        k += 1
    return ptrim(out)

# ----------------------------------------------------------------- component II
def component2_S(u, v, c, p):
    """S = c*A^2*B over F_p, B = z^2+u z+v, A = 2(5u^2-4v)z + u(7u^2-12v)."""
    a1 = (2 * (5 * u * u - 4 * v)) % p
    a0 = (u * (7 * u * u - 12 * v)) % p
    if a1 == 0:
        return None
    A = ptrim([a0, a1])
    B = ptrim([v % p, u % p, 1])
    S = pscal(pmul(pmul(A, A, p), B, p), c, p)
    if len(S) != 5 or S[0] == 0:
        return None
    disc_B = (u * u - 4 * v) % p
    if disc_B == 0:
        return None                     # then S is a perfect square (comp I)
    return S

def component1_S(A, c, p):
    S = pscal(pmul(A, A, p), c, p)
    return S if len(S) == 5 and S[0] else None

# ---------------------------------------------------------------- the cascade
KDIM = []
def run(S, M, p, a=1, b=1, rand_free=False, seed=None):
    """P_7 = H(S)*M; solve levels 3.. by linear algebra; report verdict."""
    global KDIM
    KDIM = []
    if seed is not None:
        random.seed(seed)
    H = half_radical(S, p)
    S3 = pmul(pmul(S, S, p), S, p)
    gamma = (b * b % p) * pow(pow(a, 3, p), p - 2, p) % p
    P7 = pmul(H, M, p)
    lo7, hi7 = prange(7)
    if len(P7) - 1 > hi7:
        return ("P7_DEGREE", None, None)
    P = {8: pscal(pmul(S, S, p), a, p), 7: P7}
    F12 = pscal(pmul(pmul(S, S, p), S, p), b, p)
    twoF12 = pscal(F12, 2, p)

    def p3(Pd, W):
        out = []
        ws = sorted(Pd)
        for w1 in ws:
            for w2 in ws:
                if w1 + w2 > W + 1:
                    continue
                for w3 in ws:
                    if w1 + w2 + w3 == W:
                        out = padd(out, pmul(pmul(Pd[w1], Pd[w2], p),
                                             Pd[w3], p), p)
        return out

    def build(m, trial):
        Pl = dict(P)
        Fl = {12: F12}
        w_new = 9 - m
        if trial is not None and w_new >= -1:
            Pl[w_new] = trial
        for k in range(1, m):
            W2 = 24 - k
            N = pscal(p3(Pl, W2), gamma, p)
            for q_ in list(Fl):
                if W2 - q_ in Fl and q_ <= 11 and W2 - q_ <= 11:
                    N = padd(N, pscal(pmul(Fl[W2 - q_], Fl[q_], p), -1, p), p)
            qq = pdiv_exact(N, twoF12, p)
            if qq is None:
                return None
            Fl[12 - k] = qq
        W = 24 - m
        N = pscal(p3(Pl, W), gamma, p)
        for q_ in list(Fl):
            if W - q_ in Fl and q_ <= 11 and W - q_ <= 11:
                N = padd(N, pscal(pmul(Fl[W - q_], Fl[q_], p), -1, p), p)
        return N

    for m in range(3, 23):
        w_new = 9 - m
        rng = prange(w_new) if w_new >= -1 else None
        if rng is None:
            N = build(m, None)
            if N is None:
                return ("LADDER_BREAK", m, None)
            if prem(N, S3, p):
                return ("OBSTRUCTED", m, None)
        else:
            lo, hi = rng
            nun = hi - lo + 1
            base = build(m, [0] * (hi + 1))
            if base is None:
                return ("LADDER_BREAK", m, None)
            r0 = prem(base, S3, p)
            cols = []
            for i in range(lo, hi + 1):
                Ni = build(m, [0] * i + [1])
                if Ni is None:
                    return ("LADDER_BREAK", m, None)
                cols.append(padd(prem(Ni, S3, p), pscal(r0, -1, p), p))
            n = max([len(c) for c in cols] + [len(r0), 1])
            Mx = [[(cols[k][r] if r < len(cols[k]) else 0) for k in range(nun)]
                  + [(-r0[r]) % p if r < len(r0) else 0] for r in range(n)]
            row = 0
            piv_of = {}
            for col in range(nun):
                piv = next((r for r in range(row, n) if Mx[r][col]), None)
                if piv is None:
                    continue
                Mx[row], Mx[piv] = Mx[piv], Mx[row]
                inv = pow(Mx[row][col], p - 2, p)
                Mx[row] = [(x * inv) % p for x in Mx[row]]
                for r in range(n):
                    if r != row and Mx[r][col]:
                        f = Mx[r][col]
                        Mx[r] = [(Mx[r][c] - f * Mx[row][c]) % p
                                 for c in range(nun + 1)]
                piv_of[col] = row
                row += 1
            if any(all(Mx[r][c] == 0 for c in range(nun)) and Mx[r][nun]
                   for r in range(n)):
                return ("OBSTRUCTED", m, None)
            free_cols = [c for c in range(nun) if c not in piv_of]
            KDIM.append((m, w_new, nun, len(free_cols)))
            fv = {c: (random.randrange(p) if rand_free else 0)
                  for c in free_cols}
            sol = [0] * (hi + 1)
            for c, val in fv.items():
                sol[lo + c] = val
            for col in range(nun):
                if col in piv_of:
                    r = piv_of[col]
                    val = Mx[r][nun]
                    for c2 in free_cols:
                        val = (val - Mx[r][c2] * fv[c2]) % p
                    sol[lo + col] = val
            P[w_new] = ptrim(sol)
    return ("SURVIVED_LADDER", None, P)

# --------------------------------------------------------------- full verdict
def full_verdict(S, M, p, a=1, b=1, rand_free=False):
    v, lvl, P = run(S, M, p, a, b, rand_free)
    if v != "SURVIVED_LADDER":
        return (v, lvl)
    plow = {w: P[w] for w in range(7, -2, -1) if w in P}
    from trackB1_sqrt import cascade
    res = cascade(S if False else _s_of(S), a, b, plow, p)
    return (res["verdict"], res.get("level"))

def _s_of(S):
    return S

if __name__ == "__main__":
    p = 65521
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    randfree = len(sys.argv) > 4 and sys.argv[4] == "rand"
    random.seed(seed)

    def sweep(name, gen):
        tally = Counter()
        kdims = Counter()
        tried = 0
        while sum(tally.values()) < n and tried < 40 * n:
            tried += 1
            got = gen()
            if got is None:
                continue
            S, M = got
            v = full_verdict(S, M, p, rand_free=randfree)
            tally[v] += 1
            if KDIM:
                kdims[tuple(k[3] for k in KDIM)] += 1
        print(f"\n=== {name}  (p={p}, seed={seed}, "
              f"free-dirs={'random' if randfree else 'zero'}) ===")
        for k, c in sorted(tally.items(), key=lambda t: (-t[1], str(t[0]))):
            print(f"   {str(k):>28} : {c}/{sum(tally.values())}")
        for k, c in sorted(kdims.items(), key=lambda t: -t[1])[:3]:
            print(f"   kernel-dim profile {k}: {c}")

    def gen1():
        A = [1, random.randrange(p), random.randrange(1, p)]
        S = component1_S(A, 1, p)
        if S is None:
            return None
        H = half_radical(S, p)
        dM = 8 - (len(H) - 1)
        return S, [random.randrange(p) for _ in range(dM + 1)]

    def gen2():
        u = random.randrange(1, p)
        v = random.randrange(1, p)
        S = component2_S(u, v, 1, p)
        if S is None:
            return None
        H = half_radical(S, p)
        dM = 8 - (len(H) - 1)
        return S, [random.randrange(p) for _ in range(dM + 1)]

    if which in ("both", "1"):
        sweep("COMPONENT I  (perfect squares) -- regression", gen1)
    if which in ("both", "2"):
        sweep("COMPONENT II (new locus) -- FIRST SEARCH EVER", gen2)
