#!/usr/bin/env python3
"""Structured exact search in both live degree-144 quadrilateral orientations.

For driver degree m and vertical-edge width w, pin the common-base power and
the full required vertical edge at once:

 D = alpha*(x*y-tau)^m
     + alpha*x^m*y^(m-w)*((y-rho)^w-y^w) + a*x.

The two derived c'=0 shapes have (m,w)=(12,3) and (16,4).  For every slice,
solve linearly for every coefficient of the opposite polygon.  The second
orientation uses [Q,P]=-x^2.  Modular hits are CANDIDATE-UNVERIFIED.
"""
import argparse
from math import comb
from degree8_jet import lattice, system, ranks, positive_control


CASES = [
    ("P-drives", 12, 3,
     [(0, 0), (2, 1), (16, 12), (16, 16)], 1),
    ("Q-drives", 16, 4,
     [(0, 0), (2, 1), (12, 9), (12, 12)], -1),
]


def driver(m, w, alpha, tau, rho, p):
    out = {(1, 0): 1}
    for i in range(m+1):
        out[(i, i)] = (out.get((i, i), 0)
                       + alpha*comb(m, i)*pow(-tau, m-i, p)) % p
    # alpha*x^m*y^(m-w)*((y-rho)^w-y^w)
    for j in range(w):
        e = m-w+j
        c = alpha*comb(w, j)*pow(-rho, w-j, p)
        out[(m, e)] = (out.get((m, e), 0)+c) % p
    return {z: c for z, c in out.items() if c % p}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bound", type=int, default=3)
    ap.add_argument("--primes", default="101,103")
    ap.add_argument("--projective", action="store_true",
                    help="normalize tau=rho=1 and exhaust every nonzero alpha")
    ns = ap.parse_args()
    vals = [z for z in range(-ns.bound, ns.bound+1) if z]
    grand = 0
    for label, m, w, other_poly, sign in CASES:
        mons = lattice(other_poly)
        print(f"{label}: driver m={m}, other coefficients={len(mons)}")
        for p in map(int, ns.primes.split(',')):
            print(f"  F_{p} planted matrix control:",
                  "PASS" if positive_control(p) else "FAIL")
            hits = 0
            grid = ((alpha, 1, 1) for alpha in range(1, p)) if ns.projective else (
                (alpha, tau, rho) for alpha in vals for tau in vals for rho in vals)
            tried = 0
            for alpha, tau, rho in grid:
                        tried += 1
                        M = system(driver(m, w, alpha, tau, rho, p), mons,
                                   p, rhs=sign)
                        ra, rg = ranks(M, len(mons), p)
                        if ra == rg:
                            hits += 1; grand += 1
                            print("CANDIDATE-UNVERIFIED", label, p,
                                  alpha, tau, rho, "rank", ra,
                                  "nullity", len(mons)-ra)
            print(f"  F_{p}: {hits}/{tried} consistent slices")
    print("VERDICT:", grand, "modularly consistent slices")


if __name__ == "__main__":
    main()
