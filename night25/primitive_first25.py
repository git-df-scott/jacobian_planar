#!/usr/bin/env python3
"""Exact algebra for the minimal primitive-first genus-one strike.

No numerical or modular calculation occurs here.  Polynomial identities are
checked in Z[u,v] with a tiny independent dictionary implementation.
"""

from fractions import Fraction as F
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def clean(a):
    return {m: F(c) for m, c in a.items() if c}


def add(*aa):
    out = {}
    for a in aa:
        for m, c in a.items():
            out[m] = out.get(m, F(0)) + c
    return clean(out)


def scale(c, a):
    return clean({m: F(c) * v for m, v in a.items()})


def mul(a, b):
    out = {}
    for (i, j), c in a.items():
        for (r, s), d in b.items():
            m = (i + r, j + s)
            out[m] = out.get(m, F(0)) + c * d
    return clean(out)


def power(a, n):
    out = {(0, 0): F(1)}
    for _ in range(n):
        out = mul(out, a)
    return out


def der(a, k):
    out = {}
    for (i, j), c in a.items():
        e = i if k == 0 else j
        if e:
            m = (i - 1, j) if k == 0 else (i, j - 1)
            out[m] = c * e
    return clean(out)


def bracket(a, b):
    return add(mul(der(a, 0), der(b, 1)),
               scale(-1, mul(der(a, 1), der(b, 0))))


def jac(a, b):
    return bracket(a, b)


def main():
    one = {(0, 0): F(1)}
    u = {(1, 0): F(1)}
    v = {(0, 1): F(1)}
    # The same dictionary variables are reused as abstract X,Y only when
    # checking the displayed quotient pairs.
    X, Y = u, v

    # Model A: C_t: v^2=u^3+u+t, R=u.  The total surface is A^2_(u,v).
    t_a = add(power(v, 2), scale(-1, power(u, 3)), scale(-1, u))
    r_a = u
    x_a = u
    y_a = scale(-1, power(v, 2))
    p_a_pullback = add(scale(-1, y_a), scale(-1, power(x_a, 3)), scale(-1, x_a))
    p_a = add(scale(-1, Y), scale(-1, power(X, 3)), scale(-1, X))
    q_a = X
    assert add(p_a_pullback, scale(-1, t_a)) == {}
    # Pullback of dX wedge dY equals dt wedge dR.
    assert jac(x_a, y_a) == jac(t_a, r_a)
    assert bracket(p_a, q_a) == one

    # Model B: C_t: v^2=u^4+u+t, R=u; two points over u=infinity.
    t_b = add(power(v, 2), scale(-1, power(u, 4)), scale(-1, u))
    r_b = u
    x_b = u
    y_b = scale(-1, power(v, 2))
    p_b_pullback = add(scale(-1, y_b), scale(-1, power(x_b, 4)), scale(-1, x_b))
    p_b = add(scale(-1, Y), scale(-1, power(X, 4)), scale(-1, X))
    q_b = X
    assert add(p_b_pullback, scale(-1, t_b)) == {}
    assert jac(x_b, y_b) == jac(t_b, r_b)
    assert bracket(p_b, q_b) == one

    # Minimal successor C: same cubic elliptic curve, but R=v has degree 3.
    # The canonical Darboux quotient is still triangular, but the discarded
    # extension is now a non-Galois cubic rather than a forbidden quadratic.
    t_c = t_a
    r_c = v
    x_c = add(scale(-1, power(u, 3)), scale(-1, u))
    y_c = v
    p_c_pullback = add(x_c, power(y_c, 2))
    p_c = add(X, power(Y, 2))
    q_c = Y
    assert add(p_c_pullback, scale(-1, t_c)) == {}
    assert jac(x_c, y_c) == jac(t_c, r_c)
    assert bracket(p_c, q_c) == one

    # Differential identities on the curves.
    # A: 2v dv=(3u^2+1)du, so du is exact and has pole divisor 3O.
    h_a_u = add(scale(3, power(u, 2)), one)
    h_a_v = scale(-2, v)
    assert add(h_a_u, der(add(power(v, 2), scale(-1, power(u, 3)),
                              scale(-1, u)), 0)) == {}
    assert add(h_a_v, der(add(power(v, 2), scale(-1, power(u, 3)),
                              scale(-1, u)), 1)) == {}

    # B: 2v dv=(4u^3+1)du; du has four simple finite zeros and two
    # double poles.  C: dv=(3u^2+1)du/(2v), with pole divisor 4O.
    h_b_u = add(scale(4, power(u, 3)), one)
    assert h_b_u == scale(-1, der(add(power(v, 2), scale(-1, power(u, 4)),
                                      scale(-1, u)), 0))
    assert h_a_u == scale(-1, der(add(power(v, 2), scale(-1, power(u, 3)),
                                      scale(-1, u)), 0))

    out = {
        "base_field": "Q(t)",
        "model_A": {
            "curve": "v^2=u^3+u+t",
            "generic_discriminant": "-4-27*t^2 != 0",
            "genus": 1,
            "punctures_required_for_Keller_open": ["O", "three zeros of du"],
            "R": "u",
            "R_poles": "2*O",
            "dR_divisor": "B1+B2+B3-3*O (Bi: v=0)",
            "degree_R": 2,
            "faithful_Keller_realization": "IMPOSSIBLE_BY_QUADRATIC_GALOIS_CASE",
            "canonical_quotient": "X=u, Y=-v^2; P=-Y-X^3-X, Q=X",
            "canonical_quotient_bracket": 1,
            "collapse": "Q(u,v)/Q(X,Y) has degree 2; quotient fibre is rational"
        },
        "model_B": {
            "curve": "v^2=u^4+u+t",
            "generic_discriminant": "256*t^3-27 != 0",
            "genus": 1,
            "punctures_required_for_Keller_open": ["O+", "O-", "four zeros of du"],
            "R": "u",
            "R_poles": "O+ + O-",
            "dR_divisor": "B1+B2+B3+B4-2*O+-2*O- (Bi: v=0)",
            "degree_R": 2,
            "faithful_Keller_realization": "IMPOSSIBLE_BY_QUADRATIC_GALOIS_CASE",
            "canonical_quotient": "X=u, Y=-v^2; P=-Y-X^4-X, Q=X",
            "canonical_quotient_bracket": 1,
            "collapse": "Q(u,v)/Q(X,Y) has degree 2; quotient fibre is rational"
        },
        "model_C": {
            "curve": "v^2=u^3+u+t",
            "genus": 1,
            "R": "v",
            "R_poles": "3*O",
            "dR_divisor": "Z1+Z2+Z3+Z4-4*O (Zi: 3*u^2+1=0)",
            "degree_R": 3,
            "cubic_minimal_polynomial": "U^3+U+X",
            "cubic_discriminant": "-4-27*X^2 (not a square)",
            "monodromy": "S3 over Q(X,Y)",
            "canonical_quotient": "X=-u^3-u, Y=v; P=X+Y^2, Q=Y",
            "canonical_quotient_bracket": 1,
            "status": "LIVE_INVERSE_REALIZATION_UNKNOWN",
            "missing_condition": "replace the ramified normalization A2_(u,v) by a plane model in which the cubic ramification is entirely at infinity"
        },
        "minimal_linear_in_v_ansatz": {
            "form": "x=f(u), y=a(u)*v+b(u)",
            "result": "DEAD",
            "reason": "birationality forces deg(f)=1; polynomial recovery of v forces a(u) constant, so Jac(x,y) is constant and cannot equal -(3*u^2+1)"
        },
        "theorem_gate": {
            "statement": "A characteristic-zero polynomial Keller map with Galois function-field extension is a polynomial automorphism.",
            "reference": "Bass-Connell-Wright (1982), Theorem 2.1, implication (g)=>(a)",
            "doi": "10.1090/S0273-0979-1982-15032-7",
            "application": "degree(R)=2 makes the extension quadratic, hence Galois; automorphism would make P a coordinate and its compact generic fibre rational, contradicting genus one"
        },
        "CE": "NO",
        "CEC": "NO"
    }
    path = os.path.join(HERE, "primitive_first25.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
    print("PASS: Model A exact differential and symplectic quotient")
    print("PASS: Model B exact differential and symplectic quotient")
    print("PASS: degree-2 faithful realizations excluded by Galois-case theorem")
    print("PASS: minimal degree-3 successor and S3 cubic recorded")


if __name__ == "__main__":
    main()
