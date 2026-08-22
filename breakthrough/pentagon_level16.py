#!/usr/bin/env python3
"""Exact level-16 obstruction after the level-17 fourfold-root condition."""

import sympy as sp


z = sp.symbols("z")
c0, c1 = sp.symbols("c0 c1", nonzero=True)
lam, kappa, eta = sp.symbols("lambda kappa eta")
a = sp.symbols("a0:5")
b = sp.symbols("b0:9")
d = sp.symbols("d0:8")


def pairing(weight_f, f, weight_g, g):
    return sp.expand(weight_g * sp.diff(f, z) * g - weight_f * f * sp.diff(g, z))


def D(weight, f):
    return sp.expand(weight * f - z * sp.diff(f, z))


def coefficient(poly, degree):
    return sp.expand(poly).coeff(z, degree)


def invert_diagonal(weight, rhs, kernel):
    """Invert D_weight coefficientwise and retain its one-dimensional kernel."""
    answer = kernel * z**weight
    for (degree,), coeff in sp.Poly(rhs, z).terms():
        if degree != weight:
            answer += coeff * z**degree / (weight - degree)
    answer = sp.expand(answer)
    assert sp.simplify(D(weight, answer) - rhs) == 0
    return answer


def main():
    # z^4 | h7 is the exact result of the complete level 17.
    h7 = z**4 * sum(a[i] * z**i for i in range(5))
    h6 = sum(b[i] * z**i for i in range(9))
    h5 = sum(d[i] * z**i for i in range(8))
    g12 = c1 * z**12
    g11 = 3 * c1 * z**4 * h7 / (2 * c0) + lam * z**11 / (8 * c0)

    carried18 = pairing(7, h7, 11, g11) + pairing(6, h6, 12, g12)
    rhs10 = sp.cancel(-carried18 / (8 * c0 * z**7))
    assert coefficient(rhs10, 10) == 0
    g10 = invert_diagonal(10, rhs10, kappa)

    carried17 = pairing(7, h7, 10, g10) + pairing(6, h6, 11, g11)
    rhs9 = sp.cancel(-carried17 / (8 * c0 * z**7))
    assert coefficient(rhs9, 9) == 0
    W9 = invert_diagonal(9, rhs9, eta)

    # The complete level-17 unknown is W9 = g9-(3c1/2c0)z^4 h5.
    # Keeping h5 arbitrary here is essential; setting g9=W9 manufactures a
    # false level-16 resonance.
    g9 = sp.expand(W9 + 3 * c1 * z**4 * h5 / (2 * c0))
    carried16 = sp.expand(
        pairing(7, h7, 9, g9)
        + pairing(6, h6, 10, g10)
        + pairing(5, h5, 11, g11)
    )
    low = [sp.factor(coefficient(carried16, degree)) for degree in range(7)]
    assert low[:3] == [0, 0, 0]

    F0 = a[0] ** 2 - 4 * c0 * b[0]
    F1 = a[0] * a[1] - 2 * c0 * b[1]
    assert sp.factor(low[3] + 9 * c1 * F0**2 / (4 * c0**3)) == 0
    assert sp.factor(low[4] + 33 * c1 * F0 * F1 / (4 * c0**3)) == 0

    matched = {b[0]: a[0] ** 2 / (4 * c0), b[1]: a[0] * a[1] / (2 * c0)}
    assert sp.factor(low[5].subs(matched) + 15 * c1 * F1.subs(matched) ** 2 / (2 * c0**3)) == 0
    assert sp.factor(low[6].subs(matched) + 693 * a[0] ** 3 * lam / (1024 * c0**3)) == 0

    # The bounded support of W8 is also essential: g8 has degree at most 11
    # and z^4*h4 has degree at most 10.  Therefore the z^12 term of the formal
    # D8 inverse must vanish, equivalently [z^19]carried16=0.
    F8 = a[4] ** 2 - 4 * c0 * b[8]
    assert sp.factor(coefficient(carried16, 19) - 3 * c1 * F8**2 / (4 * c0**3)) == 0

    # Thus complete solvability is equivalent (set-theoretically, in the
    # c0*c1 != 0 chart) to F0=F1=a0^3*lambda=F8=0.
    top_matched = {b[8]: a[4] ** 2 / (4 * c0)}
    conditions = {**matched, **top_matched, lam: 0}
    assert all(sp.simplify(value.subs(conditions)) == 0 for value in low)
    alternative = {b[0]: 0, b[1]: 0, a[0]: 0, **top_matched}
    assert all(sp.simplify(value.subs(alternative)) == 0 for value in low)

    # There is no hidden D8 image obstruction.  The new h4 and g8 occur only
    # through W8=g8-(3c1/2c0)z^4 h4, and the resonant coefficient vanishes on
    # the exact condition.  Reconstruct W8 on each irreducible branch.
    for branch in (conditions, alternative):
        specialized = sp.expand(carried16.subs(branch))
        rhs8 = sp.cancel(-specialized / (8 * c0 * z**7))
        assert coefficient(rhs8, 8) == 0
        invert_diagonal(8, rhs8, sp.Symbol("theta"))

    # Concrete characteristic-zero witness for the disputed a0=0 branch.
    # All displayed rows retain their exact allowed degree.
    witness = {
        c0: 1, c1: 1, lam: 1, kappa: 0, eta: 0,
        **{value: 0 for value in a + b + d},
        a[4]: 2, b[8]: 1, d[7]: 1,
    }
    h8 = c0 * z**8
    numeric_rhs8 = sp.cancel(-carried16.subs(witness) / (8 * z**7))
    numeric_W8 = invert_diagonal(8, numeric_rhs8, sp.Integer(0))
    numeric_g8 = numeric_W8  # choose h4=0 in W8=g8-(3c1/2c0)z^4h4
    complete_levels = (
        pairing(8, h8, 11, g11) + pairing(7, h7, 12, g12),
        pairing(8, h8, 10, g10) + carried18,
        pairing(8, h8, 9, g9) + carried17 + pairing(5, h5, 12, g12),
        pairing(8, h8, 8, numeric_g8) + carried16,
    )
    assert all(sp.expand(level.subs(witness)) == 0 for level in complete_levels)
    assert sp.degree(h7.subs(witness), z) == 8
    assert sp.degree(h6.subs(witness), z) == 8
    assert sp.degree(h5.subs(witness), z) == 7

    print("PASS: exact level-16 branches and explicit a0=0 witness")


if __name__ == "__main__":
    main()
