#!/usr/bin/env python3
"""Level 4, done correctly: it is a QUADRATIC OVER THE RING R = F_p[z]/(S).

The cascade solvers solved level m for the slice P_{9-m}. That pairing is off
by one: the terms of (P^3)_{24-m} carrying P_{8-m} and P_{9-m} are

    3 P_8^2 P_{8-m}   = 3a^2 S^4 P_{8-m}            (S^3 | it, drops)
    6 P_8 P_7 P_{9-m} = 6a S^2 P_7 P_{9-m}          (S | P_7, so S^3 | it, drops)

so level m's newest variable is P_{10-m}. Measured confirmation: the level-m
matrix built against P_{9-m} has RANK ZERO at every level (KDIM free == nun).

For m = 4 the newest variable is P_6, and it enters QUADRATICALLY
((P^3)_20 = 3P_8^2P_4 + 6P_8P_7P_5 + 3P_8P_6^2 + 3P_7^2P_6). Extracting the
condition rem(N_4, S^3) by finite differences shows, on every sample tested:

  * the whole condition lives in S-adic digit 2 (so there is NO P_6-independent
    obstruction at level 4 -- the old "OBSTRUCTED level 4" was the artifact of
    fixing P_6 one level early);
  * the quadratic part is exactly (3/4) * (X^2 mod S);
  * the linear part is multiplication by a fixed beta in R.

So level 4 reads, with X := P_6 mod S,

    (3/4) X^2 + beta X + gamma = 0   in   R = F_p[z]/(S),

i.e. completing the square, (X + (2/3)beta)^2 = D with

    D := (4/9) beta^2 - (4/3) gamma .

**Level 4 is solvable iff D is a SQUARE in R**, and then P_6 = X + S*Y with
Y free of degree <= 4 (5 free parameters). By Hensel (p odd), a unit of
F_p[z]/(pi^e) is a square iff its image in the residue field F_p[z]/(pi) is, so
squareness in R is decided factor by factor on the RESIDUE FIELDS of S.
"""
import random, sys
from collections import Counter
from trackB1_sqrt import pmul, padd, pscal, ptrim, pderiv
from trackB1_cascade_general import (prem, pgcd, component1_S, component2_S)
from trackB1_offbyone_check import level_condition, ppow

p = 65521

def pmod_pow(f, e, mod, p):
    """f^e mod `mod` in F_p[z]."""
    r, b = [1], prem(list(f), mod, p)
    while e:
        if e & 1:
            r = prem(pmul(r, b, p), mod, p)
        b = prem(pmul(b, b, p), mod, p)
        e >>= 1
    return ptrim(r)

def factor_deg4(S, p):
    """Distinct irreducible factors of a degree-<=4 S over F_p.
    Returns a list of monic irreducibles (each distinct)."""
    S = ptrim(list(S))
    inv = pow(S[-1], p - 2, p)
    S = [(c * inv) % p for c in S]
    # radical first
    g = pgcd(S, pderiv(S, p), p)
    rad = S
    if len(g) > 1:
        from trackB1_sqrt import pdiv_exact
        rad = pdiv_exact(S, g, p)
        rad = ptrim(rad)
    # split off linear factors: gcd(z^p - z, rad)
    zp = pmod_pow([0, 1], p, rad, p)
    lin = pgcd(padd(zp, pscal([0, 1], -1, p), p), rad, p)
    facs = []
    from trackB1_sqrt import pdiv_exact
    # roots of `lin` by trial: lin has degree <= 4, find roots via gcd with (z-r)
    # use Cantor-Zassenhaus style random splitting
    def roots(f):
        f = ptrim(list(f))
        if len(f) <= 1:
            return []
        if len(f) == 2:
            return [(-f[0] * pow(f[1], p - 2, p)) % p]
        for _ in range(200):
            a = random.randrange(p)
            h = pmod_pow([a, 1], (p - 1) // 2, f, p)
            g2 = pgcd(padd(h, [p - 1], p), f, p)
            if 1 < len(g2) < len(f):
                return roots(g2) + roots(ptrim(pdiv_exact(f, g2, p)))
        return []
    for r in roots(lin):
        facs.append([(-r) % p, 1])
    rest = rad
    for f in facs:
        rest = ptrim(pdiv_exact(rest, f, p))
    if len(rest) > 1:
        facs.append(rest)          # deg 2 irreducible (or deg 3/4 irreducible)
    return facs

def is_square_mod_irr(D, pi, p):
    """Is D a square in the field F_p[z]/(pi)?  None if D == 0 there."""
    d = prem(list(D), pi, p)
    if not ptrim(list(d)):
        return None
    q_minus_1 = p ** (len(pi) - 1) - 1
    r = pmod_pow(d, q_minus_1 // 2, pi, p)
    return ptrim(list(r)) == [1]

def level4_data(S, P7, a=1, b=1):
    """Return (beta, gamma, D) for the level-4 ring quadratic."""
    P_base = {8: pscal(pmul(S, S, p), a, p), 7: P7}
    for w in range(6, -2, -1):
        P_base[w] = []
    got = level_condition(S, P_base, 4, 6, a, b)
    if got is None:
        return None
    c0, lin, quad, n = got
    S2 = pmul(S, S, p)

    def dig2(f):
        from trackB1_sqrt import pdiv_exact
        r, q = list(f), [0] * (max(0, len(f) - len(S2)) + 1)
        if len(r) >= len(S2):
            iv = pow(S2[-1], p - 2, p)
            for k in range(len(r) - len(S2), -1, -1):
                c = (r[k + len(S2) - 1] * iv) % p
                q[k] = c
                if c:
                    for i, gi in enumerate(S2):
                        r[k + i] = (r[k + i] - c * gi) % p
        return ptrim(q)

    # digits 0 and 1 must vanish identically (no P_6 there) -- verify
    low = padd(c0, pscal(pmul(dig2(c0), S2, p), -1, p), p)
    if ptrim(list(low)):
        return ("LOW_DIGIT_OBSTRUCTION", None, None)
    inv2 = pow(2, p - 2, p)
    qii = pscal(quad.get((0, 0), []), inv2, p)
    beta = dig2(padd(lin[0], pscal(qii, -1, p), p))
    gamma = dig2(c0)
    inv9 = pow(9, p - 2, p)
    inv3 = pow(3, p - 2, p)
    D = padd(pscal(prem(pmul(beta, beta, p), S, p), (4 * inv9) % p, p),
             pscal(gamma, (-4 * inv3) % p, p), p)
    return (prem(D, S, p), beta, gamma)

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    random.seed(seed)
    print("Is level 4 solvable for P_6?  (D a square in R = F_p[z]/(S))\n")
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
            res = level4_data(S, P7)
            if res is None or res[0] == "LOW_DIGIT_OBSTRUCTION":
                tally["low-digit obstruction"] += 1
                continue
            Dq, beta, gamma = res
            facs = factor_deg4(S, p)
            verdicts = [is_square_mod_irr(Dq, pi, p) for pi in facs]
            if any(v is None for v in verdicts):
                tally["D degenerate at a factor"] += 1
            elif all(verdicts):
                tally["SOLVABLE (D is a square)"] += 1
            else:
                tally["obstructed (D a non-square)"] += 1
        tot = sum(tally.values())
        print(f"  component {tag}:  ({tot} samples, factor shapes vary)")
        for k, c in sorted(tally.items(), key=lambda t: -t[1]):
            print(f"     {k:<32} {c}/{tot}  ({100*c/tot:.0f}%)")
        print()
