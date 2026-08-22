#!/usr/bin/env python3
"""Exact controls for the generic residual-edge derivation (SymPy only)."""

from math import gcd

import sympy as sp


x, y, t, rho = sp.symbols("x y t rho")


def bracket(f, h):
    return sp.expand(sp.diff(f, x) * sp.diff(h, y) - sp.diff(f, y) * sp.diff(h, x))


def edge_control(m, n):
    """Check the claimed edge ODEs on the predicted nonzero solution family."""
    alpha, beta, delta = sp.symbols("alpha beta delta", nonzero=True)
    A = alpha * (t - rho) ** m
    B = beta * (t - rho) ** n
    H = delta * (t - rho) ** (m - 1)
    assert sp.expand(m * A * sp.diff(B, t) - n * sp.diff(A, t) * B) == 0
    assert sp.expand((m - 1) * sp.diff(A, t) * H - m * A * sp.diff(H, t)) == 0
    assert sp.degree(A, t) == m and sp.degree(B, t) == n
    return m // gcd(m, n)


def tame_control(m, k):
    """A degree-(m,km) Keller map known in advance."""
    P = x + y**m
    Q = y + P**k
    assert bracket(P, Q) == 1
    assert sp.Poly(P, x, y).total_degree() == m
    assert sp.Poly(Q, x, y).total_degree() == m * k


def poisson_residual_control(a, b):
    """Check {P,Q^a-lambda P^b}=a Q^(a-1){P,Q} generically."""
    lam = sp.symbols("lambda")
    P = x**2 + x * y + y
    Q = x**3 - y**2 + x
    R = Q**a - lam * P**b
    assert sp.expand(bracket(P, R) - a * Q ** (a - 1) * bracket(P, Q)) == 0


def main():
    # Pentagon: a=2, b=3, and the second relation is H^8 ~ A^7.
    assert edge_control(8, 12) == 2
    poisson_residual_control(2, 3)

    # Requested divisible-ratio controls: m/gcd(m,n)=1, no exclusion.
    for m, n in ((1, 2), (2, 4), (2, 6)):
        assert edge_control(m, n) == 1
        tame_control(m, n // m)

    print("PASS: generic residual edge, pentagon specialization, and tame controls")


if __name__ == "__main__":
    main()
