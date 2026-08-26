#!/usr/bin/env python3
"""Construct the exact (lambda_2,lambda_4)=(1,1) degree-144 line.

This script keeps lambda_3=t symbolic, computes both complete reverse-lift
kernels over Q(t), imposes the two independent driver gauges, and writes the
cleared full bracket system to JSON.  Although ungauged shears admit a diagonal
scaling normalization, the second driver gauge consumes that scaling freedom;
this gauged line is therefore only a genuine slice of the two-parameter chart.
The output is an elimination input, not by itself a verdict.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp

from degree144_numeric import CASES, Search
from degree144_lift_continuation import FastLift


t = sp.Symbol("t")
ds = sp.symbols("d0:9")
os = sp.symbols("o0:7")


def symbolic_lift_matrix(fast):
    matrix = sp.zeros(len(fast.rows), len(fast.supp))
    for row_index, row in enumerate(fast.rows):
        for column, lambda2_power, lambda3_power, coefficient in row:
            # lambda_2=lambda_4=1 and lambda_3=t.
            matrix[row_index, column] += coefficient*t**lambda3_power
    return matrix


def kernel(matrix, expected):
    rr, pivots = matrix.rref(simplify=False)
    free = [column for column in range(matrix.cols) if column not in pivots]
    if len(free) != expected:
        raise ArithmeticError(f"kernel dimension {len(free)} != {expected}")
    result = sp.zeros(matrix.cols, len(free))
    for j, column in enumerate(free):
        result[column, j] = 1
        for row, pivot in enumerate(pivots):
            result[pivot, j] = -rr[row, column]
    return result


def gauge_driver(driver_kernel, shape):
    rows = [shape.Dsupp.index(v) for v in ((1, 0), (16, 12))]
    gauge = driver_kernel[rows, :]
    _, pivots = gauge.rref(simplify=False)
    pivots = pivots[:2]
    free = [column for column in range(11) if column not in pivots]
    if len(pivots) != 2 or len(free) != 9:
        raise ArithmeticError("driver gauge rank is not exactly two")
    coordinates = [None]*11
    for value, column in zip(ds, free):
        coordinates[column] = value
    z = sp.symbols("z0:2")
    equations = [
        sum(gauge[row, column]*coordinates[column] for column in free)
        + sum(gauge[row, column]*z[j] for j, column in enumerate(pivots))-1
        for row in range(2)
    ]
    solution = sp.solve(equations, z, dict=True, simplify=False)[0]
    for j, column in enumerate(pivots):
        coordinates[column] = solution[z[j]]
    return driver_kernel*sp.Matrix(coordinates)


def construct():
    data = next(case for case in CASES if case[0] == "Q-drives")
    shape = Search(*data, pin_other=False, lift_chart=None)
    driver_kernel = kernel(symbolic_lift_matrix(FastLift(shape.Dsupp)), 11)
    other_kernel = kernel(symbolic_lift_matrix(FastLift(shape.Osupp)), 7)
    driver = gauge_driver(driver_kernel, shape)
    other = other_kernel*sp.Matrix(os)
    bracket = {}
    for ai, (i, j) in enumerate(shape.Dsupp):
        for bi, (k, ell) in enumerate(shape.Osupp):
            multiplier = i*ell-j*k
            if multiplier:
                target = (i+k-1, j+ell-1)
                bracket[target] = bracket.get(target, 0) + multiplier*driver[ai]*other[bi]
    bracket[(2, 0)] = bracket.get((2, 0), 0)-1
    equations = []
    for target, expression in sorted(bracket.items()):
        numerator, denominator = sp.cancel(expression).as_numer_denom()
        numerator = sp.primitive(sp.Poly(numerator, *(ds+os+(t,)), domain=sp.QQ))[1].as_expr()
        if numerator != 0:
            equations.append((target, sp.factor(numerator), sp.factor(denominator)))
    return equations


def coefficient_reduce(equations):
    """Eliminate the six forced coefficient coordinates over Q[t]."""
    variables = ds+os
    polys = [numerator for _, numerator, _ in equations]

    def normalize(expression):
        numerator, denominator = sp.cancel(expression).as_numer_denom()
        if denominator.free_symbols:
            raise ArithmeticError(f"non-polynomial forced substitution: {denominator}")
        polynomial = sp.Poly(numerator/denominator, *(variables+(t,)), domain=sp.QQ)
        return sp.primitive(polynomial)[1].as_expr()

    def substitute_all(expressions, substitution):
        result = []
        for expression in expressions:
            value = normalize(expression.subs(substitution))
            if value != 0:
                result.append(value)
        return result

    linear = [f for f in polys if sp.Poly(f, *variables).total_degree() <= 1]
    substitutions = sp.solve(linear, os[1:4], dict=True, simplify=False)[0]
    polys = substitute_all(polys, substitutions)

    # These three pivots are constant after the preceding substitutions.  The
    # apparent factor t in the final d1 equation cancels exactly in its RHS,
    # so the result remains valid at t=0 rather than silently deleting it.
    for variable in (ds[2], ds[4], ds[1]):
        active = tuple(v for v in variables if v not in substitutions)
        linear = [f for f in polys if sp.Poly(f, *active).total_degree() <= 1]
        candidates = [f for f in linear if sp.diff(f, variable) != 0]
        candidates.sort(key=lambda f: (sp.degree(sp.diff(f, variable), t), len(str(f))))
        equation = candidates[0]
        coefficient = sp.diff(equation, variable)
        rhs = sp.cancel(-(equation-coefficient*variable)/coefficient)
        if sp.denom(rhs) != 1:
            raise ArithmeticError(f"pivot for {variable} loses a parameter fibre")
        substitutions[variable] = sp.expand(rhs)
        polys = substitute_all(polys, {variable: rhs})

    active = tuple(v for v in variables if v not in substitutions)
    if active != (ds[0], ds[3], ds[5], ds[6], ds[7], ds[8],
                  os[0], os[4], os[5], os[6]):
        raise AssertionError(active)

    # The bracket dictionary contains repeated edge equations and parameter
    # multiples of equations that also occur primitively.  Retain one monic
    # representative of each Q[t]-primitive class, but only after checking
    # that the primitive representative itself occurs in the original list;
    # this prevents accidental division by a parameter factor at its roots.
    classes = {}
    exact = set()
    for expression in polys:
        monic = sp.Poly(expression, *(active+(t,)), domain=sp.QQ).monic().as_expr()
        exact.add(monic)
        coefficients = [sp.Poly(c, t, domain=sp.QQ)
                        for c in sp.Poly(expression, *active).coeffs()]
        content = coefficients[0]
        for coefficient in coefficients[1:]:
            content = sp.gcd(content, coefficient)
        primitive = sp.Poly(sp.cancel(expression/content.as_expr()),
                            *(active+(t,)), domain=sp.QQ).monic().as_expr()
        classes.setdefault(primitive, []).append((monic, sp.degree(content, t)))
    reduced_classes = set()
    for primitive, members in classes.items():
        if primitive in exact:
            reduced_classes.add(primitive)
        else:
            # No primitive equation is present, so retain each parameter
            # multiple; dividing it would strengthen the exceptional fibres.
            reduced_classes.update(monic for monic, _ in members)
    polys = sorted(reduced_classes, key=str)
    return polys, active, substitutions


def fixed_fibre_control(reduced, active, prime=101, value=1):
    """Compare a specialization with the independent modular constructor."""
    from degree144_fixed_fiber_certificate import linear_reduce
    from degree144_lift_modp import build

    all_variables = ds+os
    fixed, *_ = build(prime, 1, value)
    fixed, fixed_active, _ = linear_reduce(fixed, all_variables, prime)
    if tuple(fixed_active) != active:
        raise AssertionError("fixed-fibre reduction chose different variables")

    def modular_polynomial(expression):
        rational = sp.Poly(expression, *active, domain=sp.QQ)
        denominator = sp.ilcm(*[int(c.q) for c in rational.coeffs()])
        return sp.Poly(sp.expand(expression*denominator), *active, modulus=prime)

    def key(polynomial):
        leading = int(polynomial.LC()) % prime
        monic = sp.Poly(polynomial.as_expr()*pow(leading, prime-2, prime),
                        *active, modulus=prime)
        return tuple(monic.terms())

    symbolic = [modular_polynomial(f.subs(t, value)) for f in reduced]
    symbolic = {key(f) for f in symbolic if f.as_expr() != 0}
    independent = {key(sp.Poly(f, *active, modulus=prime))
                   for f in fixed if f != 0}
    if symbolic != independent:
        raise AssertionError("symbolic line disagrees with fixed-fibre builder")
    return len(symbolic)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="sol3/degree144_normalized_line.json")
    parser.add_argument("--skip-control", action="store_true")
    ns = parser.parse_args()
    equations = construct()
    reduced, active, substitutions = coefficient_reduce(equations)
    variables = ds+os+(t,)
    artifact = {
        "normalization": ["lambda2=1", "lambda3=t", "lambda4=1"],
        "variables": [str(v) for v in variables],
        "equations": [
            {"target": list(target), "numerator": str(numerator),
             "denominator": str(denominator)}
            for target, numerator, denominator in equations
        ],
        "reduced_variables": [str(v) for v in active]+["t"],
        "forced_substitutions": {str(k): str(v) for k, v in substitutions.items()},
        "reduced_equations": [str(f) for f in reduced],
    }
    Path(ns.output).write_text(json.dumps(artifact, indent=2)+"\n")
    degrees = [sp.Poly(numerator, *variables).total_degree()
               for _, numerator, _ in equations]
    t_degrees = [sp.degree(numerator, t) for _, numerator, _ in equations]
    denominators = sorted({str(denominator) for _, _, denominator in equations})
    print("NORMALIZED LINE CONSTRUCTION: PASS")
    print(f"equations={len(equations)} variables={len(variables)}")
    print(f"total degree max={max(degrees)} t-degree max={max(t_degrees)}")
    print(f"distinct denominators={len(denominators)}")
    print(f"coefficient reduction={len(reduced)} equations/{len(active)} coefficient variables + t")
    if not ns.skip_control:
        count = fixed_fibre_control(reduced, active)
        print(f"FIXED-FIBRE MOD-101 CONTROL AT t=1: PASS ({count} distinct equations)")
    print(f"wrote {ns.output}")


if __name__ == "__main__":
    main()
