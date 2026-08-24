#!/usr/bin/env python3
"""Exact finite-field sweep of a degree-8 jet inside the open pentagon.

The ansatz pins both proved edge structures of P simultaneously:

 P = alpha*y^8*(x*y-tau)^8
     + alpha*x^8*y^14*((y-rho)^2-y^2) + a*x.

Thus the upper edge is an eighth power, the x^8 lower-edge row is
alpha*y^14*(y-rho)^2, and all five required P vertices are nonzero when
alpha*a*tau*rho != 0.  For each parameter slice we solve the FULL linear
equation [P,Q]=x^2 for every Q coefficient in the pentagon
conv{(0,0),(2,1),(12,21),(12,24),(0,12)}.

A modularly consistent slice is only CANDIDATE-UNVERIFIED until replayed over
Q and then lifted back to an original constant-Jacobian pair.
"""
import argparse
from math import comb


NPQ = [(0, 0), (2, 1), (12, 21), (12, 24), (0, 12)]
QVERT = set(NPQ) - {(0, 0)}


def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])


def hull(points):
    pts = sorted(set(points))
    lo, hi = [], []
    for pt in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], pt) <= 0:
            lo.pop()
        lo.append(pt)
    for pt in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], pt) <= 0:
            hi.pop()
        hi.append(pt)
    return lo[:-1] + hi[:-1]


def inside(poly, pt):
    signs = [cross(poly[i], poly[(i+1) % len(poly)], pt)
             for i in range(len(poly))]
    return all(s >= 0 for s in signs) or all(s <= 0 for s in signs)


def lattice(poly):
    H = hull(poly)
    return [(i, j) for i in range(max(x for x, _ in H)+1)
            for j in range(max(y for _, y in H)+1) if inside(H, (i, j))]


def p_terms(alpha, a, tau, rho, p):
    out = {(1, 0): a % p}
    # alpha*y^8*(xy-tau)^8
    for i in range(9):
        out[(i, i+8)] = (out.get((i, i+8), 0)
                         + alpha*comb(8, i)*pow(-tau, 8-i, p)) % p
    # replace the x^8 top contribution alpha*y^16 by
    # alpha*y^14*(y-rho)^2.
    out[(8, 15)] = (out.get((8, 15), 0)-2*alpha*rho) % p
    out[(8, 14)] = (out.get((8, 14), 0)+alpha*rho*rho) % p
    return {m: c for m, c in out.items() if c % p}


def system(P, mons, p, rhs=1):
    rows = {}
    for col, (i, j) in enumerate(mons):
        for (a, b), pc in P.items():
            c = (a*j-b*i)*pc % p
            if c:
                e = (a+i-1, b+j-1)
                rows.setdefault(e, {})[col] = (rows.setdefault(e, {}).get(col, 0)+c) % p
    rows.setdefault((2, 0), {})
    dense = []
    for e, rr in rows.items():
        dense.append([rr.get(i, 0) for i in range(len(mons))]
                     + [rhs % p if e == (2, 0) else 0])
    return dense


def ranks(mat, n, p):
    A = [r[:] for r in mat]
    rank_a = rank_aug = 0
    row = 0
    for col in range(n+1):
        piv = next((u for u in range(row, len(A)) if A[u][col] % p), None)
        if piv is None:
            continue
        A[row], A[piv] = A[piv], A[row]
        inv = pow(A[row][col] % p, p-2, p)
        A[row] = [(z*inv) % p for z in A[row]]
        for u in range(len(A)):
            if u != row and A[u][col] % p:
                f = A[u][col] % p
                A[u] = [(A[u][v]-f*A[row][v]) % p for v in range(n+1)]
        row += 1
        if col < n:
            rank_a += 1
        rank_aug += 1
        if row == len(A):
            break
    return rank_a, rank_aug


def positive_control(p):
    """Plant P=x+y, Q=(x+y)^3-x^3/3, whose bracket is x^2."""
    mons = [(0, 3), (1, 2), (2, 1), (3, 0)]
    coeff = [1, 3, 3, (1-pow(3, p-2, p)) % p]
    M = system({(1, 0): 1, (0, 1): 1}, mons, p)
    return all(sum(r[i]*coeff[i] for i in range(len(mons))) % p == r[-1] % p
               for r in M)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bound", type=int, default=3)
    ap.add_argument("--primes", default="101,103")
    ap.add_argument("--projective", action="store_true",
                    help="normalize tau=rho=1 and exhaust every nonzero alpha")
    ns = ap.parse_args()
    vals = [z for z in range(-ns.bound, ns.bound+1) if z]
    mons = lattice(NPQ)
    mode = "all nonzero alpha after tau=rho=1 normalization" if ns.projective else f"{len(vals)**3} grid slices"
    print(f"Q coefficients: {len(mons)}; mode: {mode}")
    total = hits = 0
    for p in map(int, ns.primes.split(',')):
        print(f"F_{p} planted-solution control:",
              "PASS" if positive_control(p) else "FAIL")
        phit = 0
        grid = ((alpha, 1, 1) for alpha in range(1, p)) if ns.projective else (
            (alpha, tau, rho) for alpha in vals for tau in vals for rho in vals)
        tried = 0
        for alpha, tau, rho in grid:
                    tried += 1
                    total += 1
                    M = system(p_terms(alpha, 1, tau, rho, p), mons, p)
                    ra, rg = ranks(M, len(mons), p)
                    if ra == rg:
                        hits += 1; phit += 1
                        print("CANDIDATE-UNVERIFIED", p, alpha, tau, rho,
                              "rank", ra, "nullity", len(mons)-ra)
        print(f"F_{p}: {phit}/{tried} consistent slices")
    print(f"VERDICT: {hits}/{total} modular slices consistent")
    if hits == 0:
        print("No counterexample in this normalized degree-8 two-edge jet grid.")


if __name__ == "__main__":
    main()
