#!/usr/bin/env python3
"""Session 44, Lead 5 — cross-prime Mondello-shape transfer sweep.

Question (the invariant charp_ladder did not measure): do planar Keller pairs
over F_p exist with generic fibre size g >= 2 and p NOT dividing g, at shapes
STABLE across primes?  Artin-Schreier/Frobenius artefacts always have p | g;
Mondello's char-2 counterexample has g = 3.  A shape alive at two or more
primes is a bounded-degree family across primes — the certified road to
characteristic zero (an emptiness certificate has finitely many bad primes).

Family swept (u = 1 + x*y):

    P = x^a u^b + C x^m u^n,      Q = y u^e + D x^r u^s,   C, D in F_p^*.

It contains Mondello's counterexample (a,b,C,m,n)=(1,1,1,4,2),
(e,D,r,s)=(0,1,5,3) at p=2 — the positive control the sweep MUST find.
Injective-automorphism control: P=x, Q=y+x^2 must classify as g=1.

Verdicts per Keller hit: collision counts and fibre statistics over F_p^2,
F_{p^2}^2 (and F_{p^3}^2 for p=2,3), generic fibre size g = the maximum
fibre size seen (lower bound for geometric degree), and whether p | g.
Nothing here is a counterexample claim; cross-prime shape hits go to the
Hensel/exact pipeline.
"""
import argparse
import itertools
from collections import Counter, defaultdict


def bracket(P, Q, p):
    """[P,Q] = P_x Q_y - P_y Q_x for dicts {(i,j): coeff} over F_p."""
    out = {}
    for (i1, j1), c1 in P.items():
        for (i2, j2), c2 in Q.items():
            v = (c1 * c2) % p
            if not v:
                continue
            if i1 and j2:
                k = (i1 + i2 - 1, j1 + j2 - 1)
                out[k] = (out.get(k, 0) + i1 * j2 * v) % p
            if j1 and i2:
                k = (i1 + i2 - 1, j1 + j2 - 1)
                out[k] = (out.get(k, 0) - j1 * i2 * v) % p
    return {k: v for k, v in out.items() if v}


def xaub(a, b, p, coeff=1):
    """x^a * (1+xy)^b as a dict over F_p."""
    from math import comb
    out = {}
    for t in range(b + 1):
        c = (comb(b, t) * coeff) % p
        if c:
            out[(a + t, t)] = c
    return out


def padd(A, B, p):
    out = dict(A)
    for k, v in B.items():
        out[k] = (out.get(k, 0) + v) % p
        if not out[k]:
            del out[k]
    return out


def pmul_y(e, p):
    """y * (1+xy)^e as a dict."""
    from math import comb
    out = {}
    for t in range(e + 1):
        c = comb(e, t) % p
        if c:
            out[(t, t + 1)] = c
    return out


class Fq:
    """F_{p^k} as tuples, via a fixed irreducible polynomial."""

    IRRED = {  # coefficients of monic irreducible, low to high, excluding top
        (2, 2): (1, 1), (2, 3): (1, 1, 0), (2, 4): (1, 1, 0, 0),
        (3, 2): (1, 0), (3, 3): (1, 2, 0),
        (5, 2): (2, 0), (5, 3): (1, 1, 0),
        (7, 2): (3, 0), (7, 3): (2, 0, 0),
        (11, 2): (7, 0), (13, 2): (2, 0),
    }

    def __init__(self, p, k):
        self.p, self.k = p, k
        self.red = self.IRRED[(p, k)]
        self.elems = list(itertools.product(range(p), repeat=k))

    def mul(self, A, B):
        p, k, red = self.p, self.k, self.red
        prod = [0] * (2 * k - 1)
        for i, a_ in enumerate(A):
            if a_:
                for j, b_ in enumerate(B):
                    prod[i + j] = (prod[i + j] + a_ * b_) % p
        for d in range(2 * k - 2, k - 1, -1):
            c = prod[d]
            if c:
                prod[d] = 0
                for t in range(k):
                    prod[d - k + t] = (prod[d - k + t] - c * red[t]) % p
        return tuple(prod[:k])

    def add(self, A, B):
        return tuple((a_ + b_) % self.p for a_, b_ in zip(A, B))

    def scalar(self, c):
        return tuple([c % self.p] + [0] * (self.k - 1))


def fibre_stats(P, Q, p, k):
    """Evaluate the map on F_{p^k}^2; return (n_colliding_pairs_exists,
    fibre-size histogram over image points)."""
    if k == 1:
        elems = [(i,) for i in range(p)]

        class F1:
            @staticmethod
            def mul(A, B):
                return ((A[0] * B[0]) % p,)

            @staticmethod
            def add(A, B):
                return ((A[0] + B[0]) % p,)

            @staticmethod
            def scalar(c):
                return (c % p,)
        fld = F1
    else:
        fq = Fq(p, k)
        elems, fld = fq.elems, fq
    # precompute powers needed
    max_i = max(max(i for i, _ in P), max(i for i, _ in Q))
    max_j = max(max(j for _, j in P), max(j for _, j in Q))
    images = {}
    for xv in elems:
        xpow = [fld.scalar(1)]
        for _ in range(max_i):
            xpow.append(fld.mul(xpow[-1], xv))
        for yv in elems:
            ypow = [fld.scalar(1)]
            for _ in range(max_j):
                ypow.append(fld.mul(ypow[-1], yv))
            pv = fld.scalar(0)
            for (i, j), c in P.items():
                pv = fld.add(pv, fld.mul(fld.scalar(c),
                                         fld.mul(xpow[i], ypow[j])))
            qv = fld.scalar(0)
            for (i, j), c in Q.items():
                qv = fld.add(qv, fld.mul(fld.scalar(c),
                                         fld.mul(xpow[i], ypow[j])))
            images.setdefault((pv, qv), 0)
            images[(pv, qv)] += 1
    hist = Counter(images.values())
    return hist


def classify(P, Q, p, deep):
    """Return (max fibre size over tested fields, histogram summaries)."""
    out = {}
    gmax = 0
    for k in (1, 2, 3) if deep else (1, 2):
        if k == 3 and (p, 3) not in Fq.IRRED:
            continue
        if p ** (2 * k) > 1_200_000:
            break
        hist = fibre_stats(P, Q, p, k)
        out[k] = dict(hist)
        gmax = max(gmax, max(hist))
    return gmax, out


def controls():
    # Mondello, p=2: P = x u + x^4 u^2, Q = y + x^5 u^3
    p = 2
    P = padd(xaub(1, 1, p), xaub(4, 2, p), p)
    Q = padd({(0, 1): 1}, xaub(5, 3, p), p)
    br = bracket(P, Q, p)
    assert br == {(0, 0): 1}, f"Mondello bracket failed: {br}"
    g, hists = classify(P, Q, p, deep=True)
    assert g >= 3, f"Mondello generic fibre came out {g}"
    print(f"CONTROL Mondello p=2: Keller OK, max fibre {g} (expect >=3), "
          f"p|g: {g % p == 0} (expect False)")
    # automorphism control: P=x, Q=y+x^2 -> injective
    P2 = {(1, 0): 1}
    Q2 = {(0, 1): 1, (2, 0): 1}
    br2 = bracket(P2, Q2, 3)
    assert br2 == {(0, 0): 1}
    g2, _ = classify(P2, Q2, 3, deep=False)
    assert g2 == 1, f"automorphism misclassified: {g2}"
    print("CONTROL automorphism p=3: Keller OK, max fibre 1  OK")


def sweep(p, deep=False):
    """Sweep the family; print every Keller hit with fibre verdicts."""
    hits = []
    n_keller = 0
    tried = 0
    RA, RB = 5, 4       # a<=4, b<=3
    RM, RN = 9, 5       # m<=8, n<=4
    RE = 4              # e<=3
    RR, RS = 10, 5      # r<=9, s<=4
    for a, b, m, n in itertools.product(range(RA), range(RB),
                                        range(RM), range(RN)):
        if (a, b) >= (m, n):
            continue
        if a == 0 and b == 0:
            continue
        for C in range(1, p):
            P = padd(xaub(a, b, p), xaub(m, n, p, C), p)
            if not P:
                continue
            for e, r, s in itertools.product(range(RE), range(RR), range(RS)):
                for D in range(0, p):
                    tried += 1
                    Q = pmul_y(e, p)
                    if D:
                        Q = padd(Q, xaub(r, s, p, D), p)
                    elif (r, s) != (0, 0):
                        continue
                    br = bracket(P, Q, p)
                    if br != {(0, 0): 1}:
                        continue
                    n_keller += 1
                    g, hists = classify(P, Q, p, deep)
                    tag = (a, b, m, n, e, r, s)
                    if g >= 2 and g % p != 0:
                        hits.append((tag, C, D, g))
                        print(f"PRIME-TO-p HIT p={p} shape={tag} C={C} D={D} "
                              f"maxfibre={g} hists={hists}", flush=True)
    print(f"p={p}: tried {tried}, Keller {n_keller}, prime-to-p hits "
          f"{len(hits)}")
    shapes = defaultdict(list)
    for tag, C, D, g in hits:
        shapes[tag].append((C, D, g))
    return shapes


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("primes", nargs="*", type=int, default=[2, 3, 5])
    ap.add_argument("--deep", action="store_true")
    a = ap.parse_args()
    controls()
    per_prime = {}
    for p in (a.primes or [2, 3, 5]):
        per_prime[p] = sweep(p, a.deep)
    if len(per_prime) > 1:
        all_shapes = set().union(*[set(s) for s in per_prime.values()])
        cross = [t for t in all_shapes
                 if sum(1 for s in per_prime.values() if t in s) >= 2]
        print("CROSS-PRIME SHAPES (alive at >=2 primes):", sorted(cross))
