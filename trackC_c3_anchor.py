#!/usr/bin/env python3
"""C3 anchor — check the re-derived sqrt-reduction against CERTIFIED data.

trackC_c3_ladder.py proves its identities generically, which makes them
internally consistent but not yet tied to anything the campaign has certified.
This module ties them down: it reruns the re-derivation on the Session-7/10
near-miss Belyi data — which Track F reproduces with zero divergences — and
checks that it recovers the numbers Sessions 12-14 assert in prose.

The claims under test (Sessions 12-14, THEOREM 1, prose, engines lost):
    y2 = q^-6 v^-18 g^2 (1 + T),   T = sum_{m>=1} q^m v^{3m} B~_{-6+m}/g^2
    chain + ladder  <=>  A~_{-9+m} = g^3 S_m   for m = 0..12
    where (sum S_m x^m)^2 = (1 + T)^3
    near-miss: S_m = p_{8-m} v^{-3m} for m <= 8, S_9..12 = 0,
               S_13 = -n3 v^{-39}/2, recovering R = n3.

If the re-derivation is right, S_m computed by frac_root from the near-miss
B-tower must equal A~_{-9+m}/g^3 on the nose, for every m in range. That is a
cross-epoch check: the S-side comes from this session's generic engine, the
A-side from Session 10's certified expansion of the Belyi p-tower. They were
built by completely different code paths.

Exact throughout over Q(sqrt(-3)). No floats.

Run:  python3 trackC_c3_anchor.py
"""
import os, sys
from math import comb

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from trackC_c3_ladder import frac_root  # the generic engine under test

PASS = FAIL = 0
S3 = sp.sqrt(-3)


def report(name, ok, extra=""):
    global PASS, FAIL
    if ok:
        PASS += 1
    else:
        FAIL += 1
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name,
                           ("   " + extra) if extra else ""))
    return ok


def q2(a, b=0, den=1):
    """a/den + (b/den)*sqrt(-3), matching Session 10's tuple convention."""
    return sp.Rational(a, den) + sp.Rational(b, den) * S3


# ---- CERTIFIED INPUT: Session 7 Belyi data, verbatim from Session 10's run --
p_coef = {8: q2(1), 7: q2(2, 8), 6: q2(-233, 50, 3),
          5: sp.Rational(-4600, 27) + sp.Rational(-376, 3) * S3,
          4: q2(835, -890, 3), 3: q2(2420, 22, 3),
          2: sp.Rational(1043, 3) + sp.Integer(336) * S3,
          1: q2(-118, 158), 0: q2(-28, 4)}
r_coef = {5: q2(1), 4: q2(4, 16, 3), 3: q2(-278, 68, 9),
          2: sp.Rational(-140, 3) + sp.Integer(-24) * S3,
          1: q2(35, -112, 3), 0: q2(68, -20, 3)}


def expand_nm(poly, i0, j0, ev):
    """Session 10's expansion, ported to sympy coefficients."""
    out = {}
    for k, pk in poly.items():
        N = 3 * k + ev
        for u in range(N + 1):
            key = (i0 + u, j0 - k + 3 * u)
            out[key] = out.get(key, 0) + sp.Integer(comb(N, u)) * (-1)**(N - u) * pk
    return {k: sp.expand(v) for k, v in out.items() if sp.expand(v) != 0}


def blocks(vec):
    """Group by weight n = j - 3i; each block is a dict i -> coeff (poly in U)."""
    B = {}
    for (i, j), c in vec.items():
        B.setdefault(j - 3 * i, {})
        B[j - 3 * i][i] = sp.expand(B[j - 3 * i].get(i, 0) + c)
    return {n: {i: c for i, c in P.items() if c != 0} for n, P in B.items()}


def to_poly(block, U):
    """block dict {i: coeff} -> sympy polynomial sum coeff * U^i."""
    return sp.expand(sum(c * U**i for i, c in block.items()))


def main():
    print("== C3 anchor: re-derived sqrt-reduction vs CERTIFIED near-miss ==")
    U = sp.Symbol("U")
    A = blocks(expand_nm(p_coef, 3, 8, 0))     # y1-side blocks A~_n
    Bb = blocks(expand_nm(r_coef, 2, 5, 1))    # y2-side blocks B~_n
    print("   A-blocks present:", sorted(A))
    print("   B-blocks present:", sorted(Bb))

    # g^2 = B~_-6, and Sessions 12-14 claim g = alpha U (U-1)^8 (deg 9).
    g2 = to_poly(Bb[-6], U)
    gsq = sp.factor(g2)
    print("   B~_-6 = g^2 factored:", gsq)
    # extract g as an exact polynomial square root of g^2, by halving the
    # exponents of the factorization (and checking every exponent is even —
    # if one were odd, g^2 would not be a square and the whole sqrt-reduction
    # picture would be wrong here)
    const, facs = sp.factor_list(g2)
    odd = [(f, e) for f, e in facs if e % 2]
    report("every factor of B~_-6 occurs to an even power (so g exists in "
           "the polynomial ring)", odd == [], "odd-power factors: %s" % odd)
    g = sp.sqrt(const)
    for f, e in facs:
        g *= f**(e // 2)
    g = sp.expand(g)
    ok = sp.simplify(sp.expand(g**2 - g2)) == 0
    report("g^2 == B~_-6 exactly", ok, "g = %s" % sp.factor(g))
    dg = sp.degree(g, U)
    report("deg g = 9, shape alpha*U*(U-1)^8 — Sessions 12-14 THEOREM 2's "
           "boundary form, here DERIVED not assumed",
           dg == 9 and sp.simplify(sp.expand(g - U * (U - 1)**8)) == 0,
           "deg = %s, g = %s" % (dg, sp.factor(g)))

    # T_m := B~_{-6+m} / g^2   (the q^m v^{3m} factors are uniform bookkeeping)
    NT = 13
    T = [sp.Integer(0)]
    for m in range(1, NT + 1):
        blk = Bb.get(-6 + m)
        T.append(sp.cancel(to_poly(blk, U) / g2) if blk else sp.Integer(0))
    nz = [m for m in range(1, NT + 1) if T[m] != 0]
    print("   nonzero T_m at m =", nz)

    # S from the GENERIC engine under test
    S = frac_root(T, 2, 3, NT)

    # Claim: A~_{-9+m} == g^3 * S_m
    g3 = sp.expand(g**3)
    agree, disagree = [], []
    for m in range(0, NT):
        lhs = to_poly(A[-9 + m], U) if (-9 + m) in A else sp.Integer(0)
        rhs = sp.cancel(sp.together(g3 * S[m]))
        if sp.simplify(sp.expand(sp.cancel(lhs - rhs))) == 0:
            agree.append(m)
        else:
            disagree.append(m)
    report("A~_{-9+m} == g^3 * S_m for m = 0..12 "
           "(cross-epoch: generic engine vs certified Belyi expansion)",
           disagree == [], "agree at m = %s; disagree at %s" % (agree, disagree))

    # The first level is claimed condition-free: A~_-9 = ... and A~_-8 = (3/2) g B~_-5
    if -8 in A and -5 in Bb:
        lhs = to_poly(A[-8], U)
        rhs = sp.cancel(sp.Rational(3, 2) * g * to_poly(Bb[-5], U) / g2 * g2 / g2)
        rhs = sp.cancel(sp.Rational(3, 2) * to_poly(Bb[-5], U) * g / g2 * g2 / g2)
        # A~_-8 = g^3 S_1 = g^3 (3/2) T_1 = (3/2) g^3 B~_-5/g^2 = (3/2) g B~_-5
        rhs = sp.cancel(sp.Rational(3, 2) * g * to_poly(Bb[-5], U))
        report("condition-free first level: A~_-8 == (3/2) g B~_-5",
               sp.simplify(sp.expand(lhs - rhs)) == 0)

    print("\nTOTAL: %d PASS, %d FAIL" % (PASS, FAIL))
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
