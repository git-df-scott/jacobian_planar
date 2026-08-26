#!/usr/bin/env python3
"""Exhaust the rational points of the normalized shear line over F_p.

Each fibre is rebuilt from the exact lift matrices, linearly reduced, and
given a degree-bounded Macaulay unit certificate.  This closes F_p-rational
parameters only; it does not claim closure over the algebraic closure.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import sympy as sp

from degree144_fixed_fiber_certificate import (
    linear_reduce, monomials_leq, polynomial_dicts, row_basis_with_sources,
    solve_full_column_rank,
)
from degree144_lift_modp import build


def certify(prime, lambda3, degree):
    equations, *_ = build(prime, 1, lambda3)
    all_variables = sp.symbols("d0:9")+sp.symbols("o0:7")
    polys, variables, _ = linear_reduce(equations, all_variables, prime)
    dictionaries = polynomial_dicts(polys, variables, prime)
    max_degree = max(max(sum(m) for m in f) for f in dictionaries)
    columns = monomials_leq(len(variables), degree)
    column_index = {monomial: i for i, monomial in enumerate(columns)}
    multipliers = monomials_leq(len(variables), degree-max_degree)
    rows = []
    for polynomial in dictionaries:
        for multiplier in multipliers:
            row = np.zeros(len(columns), dtype=np.int64)
            for monomial, coefficient in polynomial.items():
                product = tuple(a+b for a, b in zip(monomial, multiplier))
                row[column_index[product]] = coefficient
            rows.append(row)
    matrix = np.asarray(rows, dtype=np.int64)
    pivots, selected = row_basis_with_sources(matrix, prime)
    target = np.zeros(len(columns), dtype=np.int64)
    target[column_index[(0,)*len(variables)]] = 1
    coefficients = solve_full_column_rank(matrix[selected].T, target, prime)
    replay = sum((int(c)*matrix[r] for c, r in zip(coefficients, selected)),
                 np.zeros(len(columns), dtype=np.int64)) % prime
    if not np.array_equal(replay, target):
        raise AssertionError("certificate replay failed")
    first = next(i for i, coefficient in enumerate(coefficients) if coefficient)
    broken = (replay-matrix[selected[first]]) % prime
    if np.array_equal(broken, target):
        raise AssertionError("negative control failed")
    terms = int(np.count_nonzero(coefficients))
    return {
        "lambda3": lambda3, "original_equations": len(equations),
        "reduced_equations": len(polys), "variables": len(variables),
        "macaulay_shape": list(matrix.shape), "rank": len(pivots),
        "certificate_terms": terms, "replay": "PASS",
        "negative_control": "PASS",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, default=11)
    parser.add_argument("--degree", type=int, default=4)
    parser.add_argument("--output", default="sol3/degree144_normalized_line_F11.json")
    ns = parser.parse_args()
    results = []
    for lambda3 in range(ns.prime):
        result = certify(ns.prime, lambda3, ns.degree)
        results.append(result)
        print(f"t={lambda3}: rank={result['rank']} terms={result['certificate_terms']} PASS",
              flush=True)
    artifact = {
        "prime": ns.prime, "lambda2": 1, "lambda4": 1,
        "degree": ns.degree, "scope": "all F_p-rational lambda3 values",
        "warning": "not a certificate over the algebraic closure",
        "fibres": results,
    }
    Path(ns.output).write_text(json.dumps(artifact, indent=2)+"\n")
    print(f"NORMALIZED F_{ns.prime} RATIONAL-LINE SWEEP: PASS")
    print(f"wrote {ns.output}")


if __name__ == "__main__":
    main()
