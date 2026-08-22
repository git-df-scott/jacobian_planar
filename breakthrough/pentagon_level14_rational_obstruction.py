#!/usr/bin/env python3
"""Certify a rational obstruction below the generic level-15 branch."""

import sympy as sp

from pentagon_level15_branch2 import (
    a, b, build_generic_branch, c0, c1, coefficient, d, eta,
    invert_diagonal, pairing, z,
)
from pentagon_vbottom_branch2 import check_regrading_identity, vbottom_conditions


def evaluate_sparse(terms, h, g):
    """Evaluate a sparse p/q equation from its polynomial rows."""
    total = 0
    for (p_name, q_name), scalar in terms.items():
        _, jp, i = p_name.split("_")
        _, jq, k = q_name.split("_")
        jp, i, jq, k = map(int, (jp, i, jq, k))
        hp = h.get(jp - i, sp.Integer(0))
        gq = g.get(jq - k, sp.Integer(0))
        total += scalar * coefficient(hp, i) * coefficient(gq, k)
    return sp.factor(total)


def build_obstructed_point():
    branch = build_generic_branch()
    # Here a0=F3=1. Unlisted free coefficients are zero; b0,b1,b2,b8,
    # kappa,d0 are already determined by the generic branch substitutions.
    point = {
        c0: 1, c1: 1,
        a[0]: 1, a[1]: 0, a[2]: 0, a[3]: 1, a[4]: 0,
        b[3]: 0, b[4]: 0, b[5]: 0, b[6]: 0, b[7]: 0,
        d[1]: 0, d[2]: 0, d[3]: 0, d[4]: 0, d[5]: 0, d[6]: 0, d[7]: 0,
        eta: 0, sp.Symbol("theta"): 0,
    }
    rows = list(branch["h"].values()) + list(branch["g"].values())
    for symbol in set().union(*(row.free_symbols for row in rows)):
        if symbol.name.startswith("e"):
            point[symbol] = 0
    assert sp.factor(branch["F3"].subs(point)) == 1
    h = {weight: sp.cancel(row.subs(point)) for weight, row in branch["h"].items()}
    g = {weight: sp.cancel(row.subs(point)) for weight, row in branch["g"].items()}

    # Retain the entire new h3 row and D7 kernel while reconstructing level 15.
    x = sp.symbols("x0:6")
    iota = sp.Symbol("iota")
    h[3] = sum(x[index] * z**index for index in range(6))
    carried15 = sum(pairing(i, h[i], 15 - i, g[15 - i]) for i in range(4, 8))
    rhs7 = sp.cancel(-carried15 / (8 * z**7))
    assert coefficient(rhs7, 7) == 0
    W7 = invert_diagonal(7, rhs7, iota)
    g[7] = sp.expand(W7 + sp.Rational(3, 2) * z**4 * h[3])

    # Check complete levels rather than only the selected coefficient.
    for level in range(15, 21):
        equation = sum(
            pairing(i, h[i], level - i, g[level - i])
            for i in h if level - i in g
        )
        assert sp.expand(equation) == 0

    level14 = sp.expand(
        sum(pairing(i, h[i], 14 - i, g[14 - i]) for i in range(3, 8))
    )
    obstruction = sp.factor(coefficient(level14, 1))
    assert obstruction == -sp.Rational(63, 32)
    assert not obstruction.free_symbols

    # Cross-check it against the independently generated pending v-equation.
    target = next(eq for eq in vbottom_conditions() if eq[:2] == (-13, 1))
    assert check_regrading_identity(*target) == 14
    assert evaluate_sparse(target[2], h, g) == obstruction
    return obstruction


def main():
    obstruction = build_obstructed_point()
    print("PASS: levels 20..15 vanish on the rational generic point")
    print(f"PASS: pending (V=-13,r^1) = [z]w14 = {obstruction}")
    print("CERTIFICATE: 32*[z]w14 + 63 = 0, hence level 14 is impossible")


if __name__ == "__main__":
    main()
