#!/usr/bin/env python3
"""Is the cascade solver's level <-> variable pairing off by one?

trackB1_cascade_solve.py / trackB1_cascade_general.py solve level m for the
slice P_{9-m}.  But the measured kernel dimension equals the number of unknowns
at EVERY level (free == nun in the KDIM profile), i.e. the level-m matrix has
RANK ZERO: P_{9-m} does not appear in level m's condition at all.

Hand derivation agrees.  At level m the condition is S^3 | N_m, and the terms
of (P^3)_{24-m} containing P_{9-m} or P_{8-m} are

    3 P_8^2 P_{8-m}  = 3a^2 S^4 P_{8-m}        -> divisible by S^3, drops
    6 P_8 P_7 P_{9-m} = 6a S^2 P_7 P_{9-m}     -> S | P_7 (level 3), so S^3 | it

so BOTH drop out.  The newest slice that actually appears is P_{10-m}:

    (P^3)_20 = 3P_8^2 P_4 + 6P_8 P_7 P_5 + 3 P_8 P_6^2 + 3 P_7^2 P_6

at m = 4 involves P_6 (quadratically!) while P_5 and P_4 drop.  So

    ***  level m constrains P_{10-m}, and level 4 is QUADRATIC in P_6.  ***

The solver fixes P_{9-m} (to 0, or at random) at level m -- i.e. it fixes the
variable one level BEFORE the level that constrains it, then reports the next
level as OBSTRUCTED.  If so, the published spiral table (OBSTRUCTED 4 / 7 and
the "forced" P_7 = c S^2 endgame) is an artifact.

DECISIVE TEST: take a sample the old solver calls OBSTRUCTED at level 4 and
search for ANY P_6 satisfying level 4.  If one exists, the pairing is the bug.
The level-4 condition is extracted by finite differences (it is quadratic, so
N(0), N(e_i), N(e_i+e_j) determine it exactly) -- no symbolic algebra, no
reliance on the derivation above.
"""
import random, sys, itertools
import trackB1_cascade_general as CG
from trackB1_cascade_general import component1_S, component2_S, prem
from trackB1_sqrt import (pmul, padd, pscal, ptrim, pdiv_exact, prange,
                          pderiv)

p = 65521

def ppow(f, k):
    o = [1]
    for _ in range(k):
        o = pmul(o, f, p)
    return o

def build_N(S, P, m, a=1, b=1):
    """N_m for the given full dict of P slices (weights 8..-1)."""
    gamma = (b * b % p) * pow(pow(a, 3, p), p - 2, p) % p
    s3 = pmul(pmul(S, S, p), S, p)
    F = {12: pscal(s3, b, p)}
    twoF12 = pscal(s3, 2 * b, p)

    def p3(W):
        out = []
        ws = sorted(P)
        for w1 in ws:
            for w2 in ws:
                for w3 in ws:
                    if w1 + w2 + w3 == W:
                        out = padd(out, pmul(pmul(P[w1], P[w2], p), P[w3], p), p)
        return out

    for k in range(1, m + 1):
        W = 24 - k
        N = pscal(p3(W), gamma, p)
        for q_ in list(F):
            if W - q_ in F and q_ <= 11 and W - q_ <= 11:
                N = padd(N, pscal(pmul(F[W - q_], F[q_], p), -1, p), p)
        if k == m:
            return N
        q = pdiv_exact(N, twoF12, p)
        if q is None:
            return None
        F[12 - k] = q
    return None

def level_condition(S, P_base, m, wvar, a=1, b=1):
    """Return the condition rem(N_m, S^3) as a quadratic map in the
    coefficients of P_wvar, extracted by finite differences."""
    S3 = pmul(pmul(S, S, p), S, p)
    lo, hi = prange(wvar)
    n = hi - lo + 1

    def cond(vec):
        P = dict(P_base)
        P[wvar] = ptrim([0] * lo + list(vec))
        N = build_N(S, P, m, a, b)
        if N is None:
            return None
        return prem(N, S3, p)

    c0 = cond([0] * n)
    if c0 is None:
        return None
    lin = []
    for i in range(n):
        e = [0] * n
        e[i] = 1
        ci = cond(e)
        if ci is None:
            return None
        lin.append(padd(ci, pscal(c0, -1, p), p))
    quad = {}
    for i in range(n):
        for j in range(i, n):
            e = [0] * n
            e[i] = (e[i] + 1) % p
            e[j] = (e[j] + 1) % p
            cij = cond(e)
            if cij is None:
                return None
            # c(ei+ej) = c0 + lin_i + lin_j + Q_ij  (Q_ii counted once)
            t = padd(cij, pscal(c0, -1, p), p)
            t = padd(t, pscal(lin[i], -1, p), p)
            t = padd(t, pscal(lin[j], -1, p), p)
            if ptrim(list(t)):
                quad[(i, j)] = t
    return c0, lin, quad, n

def search_P6(S, P_base, m, wvar, tries=4000, seed=0):
    """Search for a vector satisfying the (quadratic) level condition."""
    got = level_condition(S, P_base, m, wvar)
    if got is None:
        return None, None
    c0, lin, quad, n = got
    deg = "QUADRATIC" if quad else "LINEAR"
    rng = random.Random(seed)

    def evalc(v):
        out = list(c0)
        for i in range(n):
            if v[i]:
                out = padd(out, pscal(lin[i], v[i], p), p)
        for (i, j), t in quad.items():
            c = (v[i] * v[j]) % p
            if c:
                out = padd(out, pscal(t, c, p), p)
        return ptrim(out)

    # strategy: random affine line, solve the resulting quadratics in 1 var
    for _ in range(tries):
        base = [rng.randrange(p) for _ in range(n)]
        d = [rng.randrange(p) for _ in range(n)]
        # c(base + t d) = alpha t^2 + beta t + gamma  (coefficientwise)
        g = evalc(base)
        c1 = evalc([(base[i] + d[i]) % p for i in range(n)])
        c2 = evalc([(base[i] + 2 * d[i]) % p for i in range(n)])
        L = max(len(g), len(c1), len(c2))
        def at(v, k):
            return v[k] if k < len(v) else 0
        roots = None
        for k in range(L):
            g0, g1, g2 = at(g, k), at(c1, k), at(c2, k)
            # alpha + beta + gamma = g1 ; 4alpha + 2beta + gamma = g2
            alpha = ((g2 - 2 * g1 + g0) * pow(2, p - 2, p)) % p
            beta = (g1 - g0 - alpha) % p
            gam = g0 % p
            rk = set()
            if alpha == 0 and beta == 0:
                if gam == 0:
                    continue          # identically zero in t
                rk = set()
            elif alpha == 0:
                rk = {((-gam) * pow(beta, p - 2, p)) % p}
            else:
                disc = (beta * beta - 4 * alpha * gam) % p
                sq = pow(disc, (p - 1) // 2, p)
                if disc == 0:
                    rk = {((-beta) * pow(2 * alpha, p - 2, p)) % p}
                elif sq == 1:
                    r = tonelli(disc, p)
                    inv = pow(2 * alpha, p - 2, p)
                    rk = {((-beta + r) * inv) % p, ((-beta - r) * inv) % p}
                else:
                    rk = set()
            roots = rk if roots is None else (roots & rk)
            if not roots:
                break
        if roots:
            t = roots.pop()
            v = [(base[i] + t * d[i]) % p for i in range(n)]
            assert not evalc(v)
            return v, deg
    return None, deg

def tonelli(a, p):
    a %= p
    if a == 0:
        return 0
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    q, s = p - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    m_, c, t, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q + 1) // 2, p)
    while t != 1:
        i, t2 = 0, t
        while t2 != 1:
            t2 = t2 * t2 % p
            i += 1
        b = pow(c, 1 << (m_ - i - 1), p)
        m_, c = i, b * b % p
        t = t * c % p
        r = r * b % p
    return r

if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    random.seed(seed)
    print("Samples the OLD solver reports as OBSTRUCTED at level 4.")
    print("Question: does a valid P_6 exist (i.e. was level 4 mis-assigned)?\n")
    for name, mk in (("COMPONENT I ", "I"), ("COMPONENT II", "II")):
        found = tried = 0
        for _ in range(6):
            if mk == "I":
                A = [1, random.randrange(p), random.randrange(1, p)]
                S = component1_S(A, 1, p)
                D = ppow(A, 2)
            else:
                S = None
                while S is None:
                    u, v = random.randrange(1, p), random.randrange(1, p)
                    S = component2_S(u, v, 1, p)
                a1 = (2 * (5 * u * u - 4 * v)) % p
                a0 = (u * (7 * u * u - 12 * v)) % p
                Aa, Bb = ptrim([a0, a1]), ptrim([v % p, u % p, 1])
                D = pmul(ppow(Aa, 2), Bb, p)
            if S is None:
                continue
            dM = 8 - (len(D) - 1)
            M = [random.randrange(p) for _ in range(dM + 1)]
            P7 = pmul(D, M, p)
            # old solver's verdict
            real = CG.half_radical
            CG.half_radical = lambda S_, p_: [1]
            try:
                v_old, lvl_old, _ = CG.run(S, P7, p)
            finally:
                CG.half_radical = real
            P_base = {8: pmul(S, S, p), 7: P7}
            for w in range(6, -2, -1):
                P_base[w] = []
            sol, deg = search_P6(S, P_base, 4, 6, tries=300, seed=seed)
            tried += 1
            found += sol is not None
            print(f"  {name}: old verdict=({v_old},{lvl_old})  "
                  f"level-4 condition is {deg} in P_6  -> "
                  f"{'SOLVED: P_6 EXISTS' if sol else 'no P_6 found'}")
        print(f"  --> {found}/{tried} samples admit a valid P_6\n")
