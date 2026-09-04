#!/usr/bin/env python3
"""Exact positive controls for the Poisson-graded Newton-polygon machinery.

This is intentionally small and solver-independent.  It verifies the general
grading identity and five explicit polynomial witnesses before any negative
graded-chain record is trusted.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


x, y, T = sp.symbols("x y T")


def bracket(p, q):
    return sp.expand(sp.diff(p, x) * sp.diff(q, y) - sp.diff(p, y) * sp.diff(q, x))


def grading_identity_control() -> dict:
    mu, rho, sigma = 2, 2, 3
    aa = sp.symbols("a0:4")
    bb = sp.symbols("b0:5")
    f = sum(aa[i] * T**i for i in range(len(aa)))
    g = sum(bb[i] * T**i for i in range(len(bb)))
    txy = x * y**mu
    p = y ** (-rho) * f.subs(T, txy)
    q = y ** (-sigma) * g.subs(T, txy)
    expected = y ** (mu - 1 - rho - sigma) * (
        rho * f * sp.diff(g, T) - sigma * sp.diff(f, T) * g
    ).subs(T, txy)
    if sp.expand(bracket(p, q) - expected) != 0:
        raise AssertionError("Poisson grading identity failed")
    return {
        "mu": mu,
        "rho": rho,
        "sigma": sigma,
        "identity": "{y^-rho f(T),y^-sigma g(T)}=y^(mu-1-rho-sigma)(rho*f*g'-sigma*f'*g)",
        "status": "PASS",
    }


def witnesses():
    return [
        (
            "W1",
            x * (y + 1),
            sp.Rational(1, 2) * x**2 * y * (y + 2),
        ),
        (
            "W2",
            sp.Rational(1, 4) * x * (x**3 * y**4 + 4),
            sp.Rational(1, 5) * x**2 * y * (x**3 * y**4 + 5),
        ),
        (
            "W3",
            sp.Rational(1, 12)
            * x
            * (3 * x**3 * y**4 - 4 * x**2 * y**3 + 12 * x * y - 12),
            -sp.Rational(1, 3) * x * (x**2 * y**3 + 3),
        ),
        (
            "W4",
            sp.Rational(1, 30)
            * x
            * (
                5 * x**5 * y**6
                - 6 * x**4 * y**5
                - 10 * x**2 * y**3
                + 15 * x * y**2
                + 30 * x * y
                - 30
            ),
            sp.Rational(1, 30)
            * x
            * (
                10 * x**5 * y**6
                - 18 * x**4 * y**5
                - 20 * x**2 * y**3
                + 45 * x * y**2
                + 60 * x * y
                - 90
            ),
        ),
        (
            "W5",
            sp.Rational(1, 6)
            * x
            * (3 * x**3 * y**4 + 10 * x**2 * y**3 + 12 * x * y + 30),
            sp.Rational(1, 12)
            * x
            * (3 * x**3 * y**4 + 8 * x**2 * y**3 + 12 * x * y + 24),
        ),
    ]


def witness_controls() -> list[dict]:
    results = []
    for name, p, q in witnesses():
        residual = sp.expand(bracket(p, q) - x**2)
        if residual != 0:
            raise AssertionError(f"{name}: exact bracket control failed")
        results.append(
            {
                "name": name,
                "P": str(sp.expand(p)),
                "Q": str(sp.expand(q)),
                "degree_P": int(sp.Poly(p, x, y).total_degree()),
                "degree_Q": int(sp.Poly(q, x, y).total_degree()),
                "bracket": "x^2",
                "status": "PASS",
            }
        )
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = {
        "evidence_label": "EXACT-Q",
        "grading_identity": grading_identity_control(),
        "positive_witnesses": witness_controls(),
        "status": "PASS",
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
