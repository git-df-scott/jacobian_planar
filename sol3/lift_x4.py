#!/usr/bin/env python3
"""Correct reverse-Laurent lift for GGHV Proposition 4.3, case (8,28).

The final map in the (8,28) proof is

    phi_4(x) = x^-1,  phi_4(y) = x^4 y,

not the x^3 y map used for (9,27).  The map is an involution.  Before it,
the proof uses Laurent triangular translations y -> y + lambda*x^-k with
k in {2,3,4}, depending on the branch, and initially swaps x and y.

This file implements those maps on sparse Laurent polynomials exactly.  It
also constructs the LINEAR polynomiality filter: for fixed shear parameters,
which reduced-pair coefficient vectors lift back to K[x,y] after reversing
the whole chain?  That filter is necessary before a reduced [P,Q]=x^2 point
can be called a plane Keller candidate.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from math import comb, ceil, floor
import argparse
import random

NP = [(0, 0), (1, 0), (8, 14), (8, 16), (0, 8)]
NQ = [(0, 0), (2, 1), (12, 21), (12, 24), (0, 12)]


def support(vertices, xmax):
    out = []
    for i in range(xmax + 1):
        ys = []
        for a, b in zip(vertices, vertices[1:] + vertices[:1]):
            (x1, y1), (x2, y2) = a, b
            if x1 == x2 == i:
                ys.extend([Fraction(y1), Fraction(y2)])
            elif x1 != x2 and (x1 - i) * (x2 - i) <= 0:
                ys.append(Fraction(y1) + Fraction(y2 - y1, x2 - x1) * (i - x1))
        if ys:
            out.extend((i, j) for j in range(ceil(min(ys)), floor(max(ys)) + 1))
    return out


SP = support(NP, 8)
SQ = support(NQ, 12)


def add_term(poly, exp, value, modulus=None):
    if modulus:
        value %= modulus
    if value:
        poly[exp] = (poly.get(exp, 0) + value) % modulus if modulus else poly.get(exp, 0) + value
        if poly[exp] == 0:
            del poly[exp]


def phi4(poly, modulus=None):
    """Apply the involution x->x^-1, y->x^4*y."""
    out = {}
    for (i, j), c in poly.items():
        add_term(out, (4 * j - i, j), c, modulus)
    return out


def shear(poly, k, lam, modulus=None):
    """Substitute y -> y + lam*x^-k in a sparse Laurent polynomial."""
    out = {}
    for (i, j), c in poly.items():
        for r in range(j + 1):
            cc = c * comb(j, r) * pow(lam, j - r)
            add_term(out, (i - k * (j - r), r), cc, modulus)
    return out


def swap(poly):
    return {(j, i): c for (i, j), c in poly.items()}


def bracket(a, b, modulus=None):
    out = {}
    for (i, j), u in a.items():
        for (k, l), v in b.items():
            add_term(out, (i+k-1, j+l-1), (i*l-j*k)*u*v, modulus)
    return out


def forward(poly, l2, l3, l4, modulus=None):
    """Over-complete forward chain containing every Prop. 4.3 branch."""
    p = swap(poly)
    p = shear(p, 2, l2, modulus)
    p = shear(p, 3, l3, modulus)
    p = shear(p, 4, l4, modulus)
    return phi4(p, modulus)


def reverse(poly, l2, l3, l4, modulus=None):
    p = phi4(poly, modulus)
    p = shear(p, 4, -l4, modulus)
    p = shear(p, 3, -l3, modulus)
    p = shear(p, 2, -l2, modulus)
    return swap(p)


def rref_rank(rows, ncols, modulus):
    A = [dict(r) for r in rows if r]
    rank = 0
    for col in range(ncols):
        pivot = next((r for r in range(rank, len(A)) if A[r].get(col, 0) % modulus), None)
        if pivot is None:
            continue
        A[rank], A[pivot] = A[pivot], A[rank]
        inv = pow(A[rank][col] % modulus, modulus - 2, modulus)
        A[rank] = {c: v * inv % modulus for c, v in A[rank].items() if v % modulus}
        for r in range(len(A)):
            if r == rank:
                continue
            f = A[r].get(col, 0) % modulus
            if not f:
                continue
            for c, v in A[rank].items():
                A[r][c] = (A[r].get(c, 0) - f * v) % modulus
                if A[r][c] == 0:
                    A[r].pop(c, None)
        rank += 1
        if rank == len(A):
            break
    return rank


def lift_matrix(supp, l2, l3, l4, modulus):
    """Rows are negative-exponent coefficients after reverse lifting."""
    by_exp = defaultdict(dict)
    for col, exp in enumerate(supp):
        image = reverse({exp: 1}, l2, l3, l4, modulus)
        for target, value in image.items():
            if min(target) < 0:
                by_exp[target][col] = value % modulus
    rows = list(by_exp.values())
    return rows, sorted(by_exp)


def control():
    p = 2147483647
    rng = random.Random(41)
    original = {(i, j): rng.randrange(1, p) for i, j in [(0, 0), (2, 0), (0, 3), (2, 2), (4, 1)]}
    lifted = forward(original, 7, 11, 13, p)
    recovered = reverse(lifted, 7, 11, 13, p)
    assert recovered == original
    # Swap and phi4 each reverse orientation; together they send bracket 1
    # to bracket x^2.  This guards both the exponent 4 and the signs.
    fx = forward({(1, 0): 1}, 7, 11, 13, p)
    fy = forward({(0, 1): 1}, 7, 11, 13, p)
    assert bracket(fx, fy, p) == {(2, 0): 1}
    # phi_4 maps the pre-final vertices in Prop. 4.3 to the reduced pentagon.
    preP = {(-1, 0), (0, 0), (56, 16), (48, 14), (32, 8)}
    assert {next(iter(phi4({e: 1}))) for e in preP} == set(NP)
    return len(lifted)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prime", type=int, default=2147483647)
    ap.add_argument("--samples", type=int, default=12)
    args = ap.parse_args()
    print(f"CONTROL PASS: forward/reverse exact; transformed control has {control()} terms")
    print("PHI4 PASS: pre-final Prop. 4.3 vertices map exactly to the reduced pentagon")
    rng = random.Random(83023)
    # Every zero/nonzero incidence stratum of the three shear parameters,
    # followed by generic nonzero samples.  This includes the omitted
    # lower-dimensional divisors, not only the all-nonzero chart.
    charts = [(i, j, k) for i in (0, 1) for j in (0, 1) for k in (0, 1)]
    charts += [tuple(rng.randrange(1, args.prime) for _ in range(3)) for _ in range(args.samples)]
    for name, supp in [("P", SP), ("Q", SQ)]:
        print(f"\n{name}: {len(supp)} reduced coefficients")
        for ls in charts:
            rows, exps = lift_matrix(supp, *ls, args.prime)
            rank = rref_rank(rows, len(supp), args.prime)
            vertices = NP if name == "P" else NQ
            live = []
            for vertex in vertices:
                row = {supp.index(vertex): 1}
                # If rank increases, this coordinate is not identically zero
                # on the polynomial-lift kernel.
                live.append(rref_rank(rows + [row], len(supp), args.prime) > rank)
            print(f"  lambdas={ls}: negative monomials={len(exps):3d}, rank={rank:3d}, "
                  f"lift-nullity={len(supp)-rank:3d}, vertices-live={all(live)}")


if __name__ == "__main__":
    main()
