#!/usr/bin/env python3
"""INDEPENDENT instrument: Hurwitz existence for the essential face.

The essential-face equation  W = f g + 2 u f g' - 3 u f' g = 1
(deg f = m = 2k+1, deg g = n = 3k+1) is equivalent to the existence of a
rational map of P^1 with prescribed ramification.  Derivation:

  psi := f^3 / (u g^2)      (the unique weight-0 combination:
                             deg num = 3m = 6k+3 = 1 + 2n = deg den)
  psi' = -f^2 W / (u^2 g^3) = -f^2/(u^2 g^3)      once W == 1.

W == 1 forces f, g to have only simple roots, none at 0, and no common root
(at a multiple root of f or g both f,f' -- resp. g,g' -- vanish, making
W = 0 there, not 1).  So:

  deg psi = 6k+3
  psi^{-1}(0)    = m simple roots of f, each of multiplicity 3   -> [3^(2k+1)]
  psi^{-1}(inf)  = n roots of g (multiplicity 2) and u=0 (mult 1)
                                                                 -> [2^(3k+1),1]
  psi^{-1}(psi(inf)) : psi' ~ u^(2m - 2 - 3n) = u^-(5k+3) at infinity, so in
                   v = 1/u,  d psi/dv ~ v^(5k+1), psi - c ~ v^(5k+2)
                                                        -> [5k+2, 1^(k+1)]
  Riemann-Hurwitz: (4k+2)+(3k+1)+(5k+1) = 12k+4 = 2(6k+3)-2   [consistent]

and conversely a map with that data, normalised so that the simple point of
psi^{-1}(inf) sits at 0 and the (5k+2)-fold point at infinity, has
psi' = -A f^2 W /(u^2 g^3) with W forced to be a nonzero CONSTANT (no other
critical points allowed, and W cannot vanish at 0 or at a root of g without
lowering the pole order there), rescalable to W = 1.

So the face system is solvable  <=>  such a cover exists.  Existence is
counted by Frobenius:

  N = (|C1||C2||C3| / d!) * sum_lambda chi(c1)chi(c2)chi(c3)/chi(1)

over irreducible characters of S_d.  chi computed by Murnaghan-Nakayama.
Transitivity is automatic here (proved in the module docstring of
case1_transitivity below).
"""
import sys
from functools import lru_cache
from itertools import permutations
from math import factorial
from fractions import Fraction


# ---------- partitions ----------
def partitions(n, maxpart=None):
    if maxpart is None:
        maxpart = n
    if n == 0:
        yield ()
        return
    for p in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - p, p):
            yield (p,) + rest


# ---------- Murnaghan-Nakayama ----------
def rim_hooks(lam, r):
    """yield (sign, mu) for each rim hook of size r removable from lam."""
    lam = list(lam)
    L = len(lam)
    # beta numbers: lam_i + (L - 1 - i)
    beta = [lam[i] + (L - 1 - i) for i in range(L)]
    bset = set(beta)
    for i in range(L):
        b = beta[i]
        if b - r >= 0 and (b - r) not in bset:
            nb = sorted([x for x in beta if x != b] + [b - r], reverse=True)
            # height = number of beta values strictly between b-r and b
            ht = sum(1 for x in beta if b - r < x < b)
            mu = [nb[j] - (L - 1 - j) for j in range(L)]
            mu = tuple(x for x in mu if x > 0)
            yield ((-1) ** ht, mu)


@lru_cache(maxsize=None)
def chi(lam, mu):
    """irreducible character chi_lam evaluated on class of cycle type mu."""
    if not mu:
        return 1 if not lam else 0
    r = mu[0]
    rest = mu[1:]
    tot = 0
    for sgn, nu in rim_hooks(lam, r):
        tot += sgn * chi(nu, rest)
    return tot


def hook_dim(lam):
    n = sum(lam)
    lamc = []
    if lam:
        for j in range(lam[0]):
            lamc.append(sum(1 for x in lam if x > j))
    prod = 1
    for i, li in enumerate(lam):
        for j in range(li):
            prod *= (li - j) + (lamc[j] - i) - 1
    return factorial(n) // prod


def class_size(mu, n):
    from collections import Counter
    c = Counter(mu)
    z = 1
    for k, v in c.items():
        z *= (k ** v) * factorial(v)
    return factorial(n) // z


def frobenius(mu1, mu2, mu3):
    """number of triples (a,b,c) in C1 x C2 x C3 with abc = 1."""
    n = sum(mu1)
    assert sum(mu2) == n and sum(mu3) == n
    s = Fraction(0)
    for lam in partitions(n):
        d = hook_dim(lam)
        c1 = chi(lam, tuple(sorted(mu1, reverse=True)))
        if c1 == 0:
            continue
        c2 = chi(lam, tuple(sorted(mu2, reverse=True)))
        if c2 == 0:
            continue
        c3 = chi(lam, tuple(sorted(mu3, reverse=True)))
        if c3 == 0:
            continue
        s += Fraction(c1 * c2 * c3, d)
    N = Fraction(class_size(mu1, n) * class_size(mu2, n) * class_size(mu3, n),
                 factorial(n)) * s
    assert N.denominator == 1, N
    return int(N)


# ---------- brute force validation ----------
def cycle_type(p):
    n = len(p)
    seen = [False] * n
    t = []
    for i in range(n):
        if seen[i]:
            continue
        L = 0
        j = i
        while not seen[j]:
            seen[j] = True
            j = p[j]
            L += 1
        t.append(L)
    return tuple(sorted(t, reverse=True))


def brute(mu1, mu2, mu3):
    n = sum(mu1)
    P = list(permutations(range(n)))
    A = [p for p in P if cycle_type(p) == tuple(sorted(mu1, reverse=True))]
    B = [p for p in P if cycle_type(p) == tuple(sorted(mu2, reverse=True))]
    t3 = tuple(sorted(mu3, reverse=True))
    cnt = 0
    for a in A:
        for b in B:
            # c = (a b)^{-1}; product convention: apply a then b  (abc = 1)
            ab = tuple(b[a[i]] for i in range(n))
            inv = [0] * n
            for i in range(n):
                inv[ab[i]] = i
            if cycle_type(tuple(inv)) == t3:
                cnt += 1
    return cnt


if __name__ == "__main__":
    if sys.argv[1:2] == ["validate"]:
        print("VALIDATION of the Frobenius/Murnaghan-Nakayama counter")
        print("  (brute force over all of S_n vs the character formula)")
        tests = [((3,), (2, 1), (2, 1)),
                 ((2, 1), (2, 1), (2, 1)),
                 ((3,), (3,), (3,)),
                 ((4,), (2, 2), (2, 1, 1)),
                 ((2, 2), (2, 2), (2, 2)),
                 ((3, 1), (2, 2), (4,)),
                 ((5,), (2, 2, 1), (2, 2, 1)),
                 ((3, 2), (2, 1, 1, 1), (5,)),
                 ((3, 3), (2, 2, 2), (4, 2)),
                 ((3, 3), (2, 2, 1, 1), (5, 1))]
        ok = True
        for t in tests:
            bf, fr = brute(*t), frobenius(*t)
            flag = "OK " if bf == fr else "MISMATCH"
            if bf != fr:
                ok = False
            print(f"  {flag} {t}: brute {bf}  frobenius {fr}")
        print("INSTRUMENT VALIDATED" if ok else "*** INSTRUMENT BROKEN ***")
        sys.exit(0)

    ks = [int(v) for v in sys.argv[1:]] or [0, 1, 2, 3]
    for k in ks:
        d = 6 * k + 3
        m, n = 2 * k + 1, 3 * k + 1
        mu0 = tuple([3] * m)
        muI = tuple([2] * n + [1])
        muC = tuple([5 * k + 2] + [1] * (k + 1))
        assert sum(mu0) == d and sum(muI) == d and sum(muC) == d
        rh = (d - len(mu0)) + (d - len(muI)) + (d - len(muC))
        N = frobenius(mu0, muI, muC)
        print(f"k={k}  d={d}  [3^{m}] , [2^{n},1] , [{5*k+2},1^{k+1}]"
              f"   RH: {rh} vs {2*d-2}")
        print(f"    triples with product 1 : {N}")
        print(f"    N/d!  (weighted # of covers) : {Fraction(N, factorial(d))}")
        print(f"    predicted # normalised (f,g) = m * N/d! = "
              f"{Fraction(m * N, factorial(d))}")
