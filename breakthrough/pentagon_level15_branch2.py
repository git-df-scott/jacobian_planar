#!/usr/bin/env python3
"""Exact level-15 equations on the lambda=0 branch of level 16."""

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

    # Thus divisibility by z^7 is equivalent (set-theoretically, in the
    # c0*c1 != 0 chart) to F0=F1=a0^3*lambda=0.
    conditions = {**matched, lam: 0}
    assert all(sp.simplify(value.subs(conditions)) == 0 for value in low)
    alternative = {b[0]: 0, b[1]: 0, a[0]: 0}
    assert all(sp.simplify(value.subs(alternative)) == 0 for value in low)

    # There is no hidden D8 image obstruction.  The new h4 and g8 occur only
    # through W8=g8-(3c1/2c0)z^4 h4, and the resonant coefficient vanishes on
    # the exact condition.  Reconstruct W8 on each irreducible branch.
    for branch in (conditions, alternative):
        specialized = sp.expand(carried16.subs(branch))
        rhs8 = sp.cancel(-specialized / (8 * c0 * z**7))
        assert coefficient(rhs8, 8) == 0
        invert_diagonal(8, rhs8, sp.Symbol("theta"))

    # Branch 2 continuation to level 15.
    h4c = sp.symbols("e0:7")
    h4 = sum(h4c[i]*z**i for i in range(7))
    branch2_carried16 = sp.expand(carried16.subs(conditions))
    branch2_rhs8 = sp.cancel(-branch2_carried16/(8*c0*z**7))
    theta=sp.symbols("theta")
    W8=invert_diagonal(8,branch2_rhs8,theta)
    g8=sp.expand(W8+3*c1*z**4*h4/(2*c0))
    carried15=sp.expand(pairing(7,h7,8,g8)+pairing(6,h6.subs(conditions),9,g9.subs(conditions))+pairing(5,h5,10,g10.subs(conditions))+pairing(4,h4,11,g11.subs(conditions)))
    low15=[sp.factor(coefficient(carried15,i)) for i in range(7)]
    # The new h3,g7 pair occurs through W7 and contributes 8*c0*z^7*D7(W7).
    # Hence low coefficients are the full obstruction; D7 has no extra resonance.
    assert coefficient(carried15, 14) == 0
    C = tuple(sp.factor(coefficient(carried15, i)) for i in range(3, 7))
    assert all(coefficient(carried15, i) == 0 for i in range(3))

    F2 = 2*a[0]*a[2] + a[1]**2 - 4*c0*b[2]
    F3 = a[0]*a[3] + a[1]*a[2] - 2*c0*b[3]
    assert sp.factor(C[0] - 33*a[0]*c1*F2**2/(32*c0**4)) == 0
    assert sp.factor(C[1].subs(a[0], 0) - 15*a[1]*c1*F2.subs(a[0],0)**2/(16*c0**4)) == 0

    # On the generic open chart a0*F3 != 0, C3 forces F2; after that C5
    # determines kappa and C6 determines d0. Verify both coefficients are units
    # on that chart and reconstruct the complete D7 solution formally.
    matched2 = {b[2]:(2*a[0]*a[2]+a[1]**2)/(4*c0)}
    C5 = sp.factor(C[2].subs(matched2))
    kappa_coeff = sp.factor(sp.diff(C5, kappa))
    assert kappa_coeff == -45*a[0]**3/(16*c0**2)
    kappa_solution = sp.solve(C5, kappa)[0]
    C6 = sp.factor(C[3].subs(matched2).subs(kappa, kappa_solution))
    d0_coeff = sp.factor(sp.diff(C6, d[0]))
    assert sp.factor(d0_coeff - 24*c1*F3/c0**2) == 0
    d0_solution = sp.solve(C6, d[0])[0]
    generic = {**matched2, kappa:kappa_solution, d[0]:d0_solution}
    specialized = sp.cancel(carried15.subs(generic))
    rhs7 = sp.cancel(-specialized/(8*c0*z**7))
    assert coefficient(rhs7,7) == 0
    invert_diagonal(7,rhs7,sp.Symbol("iota"))

    print("PASS: level 15 iff C3=C4=C5=C6=0; generic branch reconstructed")

if __name__ == "__main__":
    main()
