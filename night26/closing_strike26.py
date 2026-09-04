#!/usr/bin/env python3
"""Exact checks for the NIGHT26 degree-six primitive-first frontier.

All polynomial calculations use integer coefficient dictionaries.  No
floating-point, modular, or truncated calculation occurs here.
"""


def clean(p):
    return {m: c for m, c in p.items() if c}


def add(*ps):
    out = {}
    for p in ps:
        for m, c in p.items():
            out[m] = out.get(m, 0) + c
    return clean(out)


def scale(c, p):
    return clean({m: c * a for m, a in p.items()})


def mul(p, q):
    out = {}
    for (i, j), a in p.items():
        for (k, ell), b in q.items():
            m = (i + k, j + ell)
            out[m] = out.get(m, 0) + a * b
    return clean(out)


def power(p, n):
    out = {(0, 0): 1}
    for _ in range(n):
        out = mul(out, p)
    return out


def derivative(p, variable):
    out = {}
    for (i, j), a in p.items():
        e = i if variable == 0 else j
        if e:
            m = (i - 1, j) if variable == 0 else (i, j - 1)
            out[m] = a * e
    return clean(out)


def jacobian(p, q):
    return add(mul(derivative(p, 0), derivative(q, 1)),
               scale(-1, mul(derivative(p, 1), derivative(q, 0))))


def main():
    one = {(0, 0): 1}
    u = {(1, 0): 1}
    r = {(0, 1): 1}

    # Total surface A^2_(u,r): t=r^2+2u^2r and primitive R=r^3.
    t = add(power(r, 2), scale(2, mul(power(u, 2), r)))
    R = power(r, 3)
    assert jacobian(t, R) == {(1, 3): 12}

    # On C_t put w=2ru.  Its Weierstrass equation is
    # w^2=2tr-2r^3.  Verify after pullback to the total surface.
    w = scale(2, mul(r, u))
    assert add(power(w, 2), scale(-2, mul(t, r)),
               scale(2, power(r, 3))) == {}

    # The finite critical axes and their target cusp.
    # u=0 gives (t,R)=(r^2,r^3), hence R^2=t^3.
    t_u0 = power(r, 2)
    R_u0 = power(r, 3)
    assert add(power(R_u0, 2), scale(-1, power(t_u0, 3))) == {}
    # r=0 is contracted to (0,0).
    assert not {m: c for m, c in t.items() if m[1] == 0}
    assert not {m: c for m, c in R.items() if m[1] == 0}

    # Toric/monomial Darboux obstruction.  If
    # x=c1*u^a*r^b, y=c2*u^c*r^d and dx^dy is proportional to
    # u*r^3 du^dr, then a+c=2 and b+d=4.  The exponent determinant is
    # 4a-2b, always even, so it cannot be +/-1 as birationality requires.
    for a in range(-100, 101):
        for b in range(-100, 101):
            c, d = 2 - a, 4 - b
            determinant = a * d - b * c
            assert determinant == 4 * a - 2 * b
            assert determinant not in (-1, 1)

    # Exact genus-one affine-modification control:
    # P=2y+x^4y^2, Y=1+x^4y gives Y^2=1+x^4P.
    x, y = u, r  # abstract checker variables for this separate identity
    P_control = add(scale(2, y), mul(power(x, 4), power(y, 2)))
    Y_control = add(one, mul(power(x, 4), y))
    assert add(power(Y_control, 2), scale(-1, one),
               scale(-1, mul(power(x, 4), P_control))) == {}
    assert derivative(P_control, 1) == scale(2, Y_control)

    print("PASS exact: [t,r^3]=12*u*r^3")
    print("PASS exact: w^2=2*t*r-2*r^3 and finite cusp R^2=t^3")
    print("PASS exact: monomial birational Darboux charts impossible by parity")
    print("PASS exact: split-quartic control polynomializes but has holomorphic GL form")


if __name__ == "__main__":
    main()
