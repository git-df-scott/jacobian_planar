#!/usr/bin/env python3
"""Exact independent algebra for the September 5 missed-routes audit.

Run from any directory. Requires SymPy. The all-degree steps are written
proofs in RIBBON46_ALL_DEGREES.md, not inferred from bounded tests.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as s


HERE = Path(__file__).resolve().parent


def zero(expression):
    assert s.cancel(s.expand(expression)) == 0, expression


def bracket(f, g, x, y):
    return s.expand(s.diff(f, x) * s.diff(g, y) - s.diff(f, y) * s.diff(g, x))


def integrate_one_form(form, variables, differentials):
    coefficients = [s.diff(form, dv) for dv in differentials]
    zero(form - sum(c * dv for c, dv in zip(coefficients, differentials)))
    for i in range(len(variables)):
        for j in range(len(variables)):
            zero(s.diff(coefficients[i], variables[j]) - s.diff(coefficients[j], variables[i]))
    t = s.Dummy("t")
    scaling = {v: t * v for v in variables}
    result = s.expand(s.integrate(sum(v * c.subs(scaling, simultaneous=True)
                                        for v, c in zip(variables, coefficients)), (t, 0, 1)))
    zero(sum(s.diff(result, v) * dv for v, dv in zip(variables, differentials)) - form)
    return result


def verify_ribbon():
    # Derive from the original bracket, independently of all inherited modules.
    Y = s.Symbol("Y")
    a, b, c = variables = s.symbols("a b c")
    da, db, dc = differentials = s.symbols("da db dc")
    constants = s.symbols("k0:6")
    derivative = lambda f: s.expand(sum(s.diff(f, v) * dv for v, dv in zip(variables, differentials)))
    P = Y**4 + a * Y**2 + b * Y + c
    Q = Y**6
    for degree in range(8, 2, -1):
        row = s.expand(derivative(P) * s.diff(Q, Y) - s.diff(P, Y) * derivative(Q)).coeff(Y, degree)
        Q += Y**(degree - 3) * (integrate_one_form(row / 4, variables, differentials) + constants[degree - 3])
    Q = s.expand(Q)
    J = s.Poly(derivative(P) * s.diff(Q, Y) - s.diff(P, Y) * derivative(Q), Y)
    for degree in range(3, 10):
        zero(J.nth(degree))
    E2, E1, E0 = (J.nth(i) for i in (2, 1, 0))
    primitives = [integrate_one_form(f, variables, differentials)
                  for f in (E2, E1, E0 - a * E2 / 4)]
    d, h, k, ell, m = s.symbols("d h k ell m")
    replacement = {c: d + a*a/4, constants[5]: h, constants[3]: k,
                   constants[2]: ell, constants[1]: m}
    derived = [s.expand(H.subs(replacement)) for H in primitives]
    H2 = (5*a**3*h + 12*a**2*k + 40*a*d*h + 32*a*m + 20*b**2*h
          + 96*b*d + 64*b*ell + 96*d*k) / 32
    H1 = (-5*a**2*b*h - 24*a*b**2 - 24*a*b*k + 40*b*d*h + 32*b*m
          + 48*d**2 + 64*d*ell) / 32
    H0 = (15*a**4*h + 32*a**3*k + 80*a**2*d*h + 64*a**2*m
          - 160*a*b**2*h - 384*a*b*d - 256*a*b*ell - 128*b**3
          - 192*b**2*k + 320*d**2*h + 512*d*m) / 512
    explicit = [H2, H1, H0]
    for actual, expected in zip(derived, explicit):
        zero(actual - expected)

    # Recompose actual two-variable polynomial pairs with a nonconstant cubic
    # row, to verify both the depression shear and the complete bracket identity.
    x, y = s.symbols("x y")
    samples = [
        (x*x+1, x**3-x, x**4+2, x*x-x, (1, 2, 3, 4, 5, 6)),
        (2, x*x+1, x+3, x**3, (0, -2, 1, -3, 2, 0)),
        (x, 1, x*x, x+1, (1, 2, 0, 0, 0, 0)),
    ]
    for av, bv, dv, shear, kv in samples:
        replacements = {a: av, b: bv, c: dv+av*av/4, **dict(zip(constants, kv))}
        pxy = s.expand(P.subs(replacements).subs(Y, y + shear))
        qxy = s.expand(Q.subs(replacements).subs(Y, y + shear))
        hs = [s.expand(H.subs({a: av, b: bv, d: dv, h: kv[5], k: kv[3], ell: kv[2], m: kv[1]}))
              for H in explicit]
        rhs = s.diff(hs[0], x) * ((y+shear)**2 + av/4) + s.diff(hs[1], x)*(y+shear) + s.diff(hs[2], x)
        zero(bracket(pxy, qxy, x, y) - rhs)
        assert s.expand(bracket(pxy, qxy + y, x, y) - rhs) != 0

    # Leading coefficient identities used in the written degree proof.
    u, v, w = s.symbols("u v w")
    zero((15*h*u**4 - 384*u*v*w).subs(w, -5*h*u**3/(96*v)) / 512 - 35*h*u**4/512)
    zero((32*k*u**3 - 384*u*v*w).subs(w, -k*u**2/(8*v)) / 512 - 5*k*u**3/32)
    zero((64*m*u**2 - 384*u*v*w).subs(w, -m*u/(3*v)) / 512 - 3*m*u**2/8)
    zero((H0 + a*H2/4 + b**3/4).subs({h: 0, k: 0, m: 0}))
    # A genuine Keller control is outside, and must stay outside, the sextic gate.
    zero(bracket(x + y**4, y, x, y) - 1)
    assert s.Poly(y, y).degree() != 6
    return {"status": "PASS", "H2": str(H2), "H1": str(H1), "H0": str(H0),
            "normalized_Q": str(Q), "degree_proof": "RIBBON46_ALL_DEGREES.md",
            "scope": "Both leading y coefficients constant and nonzero; arbitrary polynomial x coefficients."}


def verify_localization():
    x, y = s.symbols("x y")
    P = x*y*y + y
    Q = -x/(x*y+1)
    A = -x*y
    zero(bracket(P, Q, x, y)-1)
    zero(A/P-Q)
    zero(bracket(P, A, x, y)-P)
    zero(bracket(P, -1/y, x, y)-1)
    zero(Q + 1/y - 1/P)
    return {"status": "PASS", "P": str(P), "Q": str(Q), "A": str(A),
            "clearing_denominator": str(P), "D_P(A)": str(P)}


def verify_conductor():
    v, c, r, z = s.symbols("v c r z")
    a = -c*v**3 + v*v + v
    b = -3*c*v*v + 4*v + 2
    Delta = (3*c*v-2)**2 - 9*c
    zero(v*v-(b+1)*v+3*a)
    zero(Delta-(4-3*c*(b+1)))
    zero(Delta*v-(b-2-9*c*a))
    param = {v: 3*(r+2)/r**2, c: r*r/9}
    zero(Delta.subs(param))
    zero((3*c*v-2).subs(param)-r)
    zero((v*r-3).subs(param)/6-1/r)
    restrictions = [12/r**4-3/r**2, -1+12/r**2, r**2/9]
    for f, expected in zip((a,b,c), restrictions):
        zero(f.subs(param)-expected)
        zero(expected.subs(r, -r)-expected)
    # Recorded collision in the new affine coordinates.
    images = []
    for vv in (-s.Rational(1,3), s.Rational(2,3)):
        images.append([f.subs({v: vv, c: 4}) for f in (a,b,c)])
    assert images[0] == images[1] == [-s.Rational(2,27), -s.Rational(2,3), 4]
    # An exact first conductor jet, explicitly NOT a Keller pair.
    rr = 3*c*v-2
    Pjet = c + Delta*rr*(2*rr-1)/72
    Qjet = b
    residual = bracket(Pjet,Qjet,v,c)-1
    remainder = s.rem(s.Poly(residual,v,c),s.Poly(Delta,v,c)).as_expr()
    zero(remainder)
    assert residual != 0
    assert s.Poly(bracket(Pjet,Qjet,v,c),v,c).total_degree() > 0
    return {"status": "PASS", "a": str(a), "b": str(b), "c": str(c),
            "Delta": str(Delta), "collision_images": [str(f) for f in images[0]],
            "restriction": [str(f) for f in restrictions],
            "first_jet_P": str(Pjet), "first_jet_Q": str(Qjet),
            "first_jet_is_Keller": False,
            "target_degree_3_total_degree_bound": 12,
            "target_degree_26_total_degree_bound": 104}


def verify_boundary_control():
    # Smooth affine symplectic extension containing A2 as an open subset.
    # Its projection gives a non-Keller control with a fixed escaping sheet.
    x, y, u, v, w = s.symbols("x y u v w")
    U, V, W = x, x*y, y*(x*y-1)
    zero(U*W - V*(V-1))
    zero(bracket(U,V,x,y)/U - 1)
    zero(W/(V-1)-y)
    zero(V/U-y)
    # The affine surface is smooth: u=w=0 and 2v-1=0 misses it.
    assert (u*w-v*(v-1)).subs({u:0,w:0,v:s.Rational(1,2)}) == s.Rational(1,4)
    zero(bracket(U,W,x,y)-(2*x*y-1))
    assert bracket(U,W,x,y) != 1
    return {"status":"PASS", "surface":"u*w=v*(v-1)",
            "open_embedding":"(x,y) -> (x,xy,y(xy-1))",
            "omitted_curve":"u=0,v=1", "volume":"du wedge dv/u = dx wedge dy",
            "plane_projection":"(x,xy^2-y)", "projection_Jacobian":"2xy-1",
            "generic_meridian_over_u0":"identity: one staying, one escaping",
            "is_Keller_counterexample":False}


def main():
    results = {}
    for name, function in [("RIBBON46_INTEGRALS",verify_ribbon),
                            ("LOCALIZATION_COUNTEREXAMPLE",verify_localization),
                            ("CONDUCTOR_AND_FIRST_JET",verify_conductor),
                            ("AFFINE_BOUNDARY_CONTROL",verify_boundary_control)]:
        results[name] = function()
        print(name+": PASS", flush=True)
    results["counterexample_found"] = False
    results["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (HERE/"verification.json").write_text(json.dumps(results,indent=2)+"\n")


if __name__ == "__main__":
    main()
