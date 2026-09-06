#!/usr/bin/env python3
"""Exact level-17 s-ladder obstruction for the pentagon target."""

import sympy as sp


z = sp.symbols("z")
c0, c1 = sp.symbols("c0 c1", nonzero=True)
lam, kappa = sp.symbols("lambda kappa")
a = sp.symbols("a0:7")
b = sp.symbols("b0:9")


def pairing(weight_f, f, weight_g, g):
    return sp.expand(weight_g * sp.diff(f, z) * g - weight_f * f * sp.diff(g, z))


def D(weight, f):
    return sp.expand(weight * f - z * sp.diff(f, z))


def coefficient(poly, degree):
    return sp.expand(poly).coeff(z, degree)


def main():
    h7 = z**2 * sum(a[i] * z**i for i in range(7))
    h6 = sum(b[i] * z**i for i in range(9))
    g12 = c1 * z**12
    g11 = 3 * c1 * z**4 * h7 / (2 * c0) + lam * z**11 / (8 * c0)

    carried18 = pairing(7, h7, 11, g11) + pairing(6, h6, 12, g12)
    quotient18 = sp.cancel(-carried18 / (8 * c0 * z**7))
    assert sp.rem(sp.together(carried18).as_numer_denom()[0], z**7, z) == 0
    assert coefficient(quotient18, 10) == 0  # the sole D_10 image obstruction

    # Invert D_10 diagonally and retain its complete one-dimensional kernel.
    g10 = kappa * z**10
    for (degree,), coeff in sp.Poly(quotient18, z).terms():
        if degree != 10:
            g10 += coeff * z**degree / (10 - degree)
    g10 = sp.expand(g10)
    assert sp.simplify(D(10, g10) - quotient18) == 0

    carried17 = sp.expand(pairing(7, h7, 10, g10) + pairing(6, h6, 11, g11))
    low = [sp.factor(coefficient(carried17, degree)) for degree in range(7)]

    assert low[1] == 15 * c1 * a[0] ** 3 / (2 * c0**2)
    assert sp.factor(low[4].subs(a[0], 0)) == 6 * c1 * a[1] ** 3 / c0**2
    assert all(sp.simplify(value.subs({a[0]: 0, a[1]: 0})) == 0 for value in low)

    # The remaining level-17 equation is D_9(W_9) = quotient17.  Its only
    # image obstruction is the z^9 coefficient, which vanishes identically;
    # thus fourfold divisibility is sufficient for the complete level.
    quotient17 = sp.cancel(-carried17.subs({a[0]: 0, a[1]: 0}) / (8 * c0 * z**7))
    assert coefficient(quotient17, 9) == 0
    W9 = sp.Integer(0)
    for (degree,), coeff in sp.Poly(quotient17, z).terms():
        if degree != 9:
            W9 += coeff * z**degree / (9 - degree)
    assert sp.simplify(D(9, W9) - quotient17) == 0

    print("PASS: level 17 is solvable iff (s-tau)^4 divides h_7")


if __name__ == "__main__":
    main()
