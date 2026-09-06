#!/usr/bin/env python3
"""End-to-end graded-cascade controls on explicit tame Keller maps.

Unlike ``verify_generic_residual_edge.py``, this does not merely substitute the
predicted edge forms.  It constructs each complete map, grades every term,
reassembles every bracket level independently, and checks the terminal Keller
level.  Thus an accidental dropped or manufactured level is detected.
"""

from collections import defaultdict

import sympy as sp


x, y = sp.symbols("x y")


def bracket(f, g):
    return sp.Poly(
        sp.expand(sp.diff(f, x) * sp.diff(g, y) - sp.diff(f, y) * sp.diff(g, x)),
        x,
        y,
    )


def total_degree_blocks(poly):
    """Return the total-degree homogeneous blocks of ``poly``."""
    blocks = defaultdict(lambda: sp.Integer(0))
    for (i, j), coeff in sp.Poly(poly, x, y).terms():
        blocks[i + j] += coeff * x**i * y**j
    return dict(blocks)


def cascade(P, Q, expected=1):
    """Audit all graded bracket levels, top-down, without cancellation shortcuts."""
    pblocks = total_degree_blocks(P)
    qblocks = total_degree_blocks(Q)
    contributions = defaultdict(lambda: sp.Integer(0))

    # A bracket of total degrees i and j has total degree i+j-2.
    for i, Pi in pblocks.items():
        for j, Qj in qblocks.items():
            contributions[i + j - 2] += bracket(Pi, Qj).as_expr()

    full = bracket(P, Q).as_expr()
    rebuilt = sp.expand(sum(contributions.values(), sp.Integer(0)))
    assert sp.expand(rebuilt - full) == 0

    for level, value in contributions.items():
        target = expected if level == 0 else 0
        assert sp.expand(value - target) == 0, (level, sp.factor(value - target))
    assert full == expected
    return tuple(sorted(contributions, reverse=True))


def control(m, n):
    assert n % m == 0
    k = n // m
    P = x + y**m
    Q = y + P**k

    # Confirm the input degree pair and its common leading generator.  For
    # m=1 the generator is x+y; for m>1 it is y^m (itself a power of y).
    assert sp.Poly(P, x, y).total_degree() == m
    assert sp.Poly(Q, x, y).total_degree() == n
    Ptop = total_degree_blocks(P)[m]
    assert sp.expand(total_degree_blocks(Q)[n] - Ptop**k) == 0
    return cascade(P, Q)


def main():
    results = {(m, n): control(m, n) for m, n in ((1, 2), (2, 4), (2, 6))}
    for pair, levels in results.items():
        print(f"NONEMPTY control {pair}: all bracket levels {levels} pass")


if __name__ == "__main__":
    main()
