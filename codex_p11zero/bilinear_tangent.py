#!/usr/bin/env python3
"""Exact tangent audit of the full sparse polynomial-Q system."""

from bilinear_full import (P_VARIABLES, Q_VARIABLES,
                           build_bracket_equations, evaluate)
from pentagon_core import nullspace_mod, rank_mod, solve_affine


def derivative(poly, variable, point, prime):
    total = 0
    for monomial, coefficient in poly.items():
        multiplicity = monomial.count(variable)
        if not multiplicity:
            continue
        term = coefficient * multiplicity
        removed = False
        for factor in monomial:
            if factor == variable and not removed:
                removed = True
            else:
                term = term * point.get(factor, 0) % prime
        total = (total + term) % prime
    return total


def constrained_tangent(jacobian, variables, requirements, prime):
    matrix = [row[:] for row in jacobian]
    rhs = [0] * len(matrix)
    for variable, value in requirements.items():
        row = [0] * len(variables)
        row[variables.index(variable)] = 1
        matrix.append(row)
        rhs.append(value % prime)
    # solve_affine uses M*x=-v.
    return solve_affine(matrix, [(-value) % prime for value in rhs], prime)


def main(prime=43):
    variables = P_VARIABLES + Q_VARIABLES
    equations = build_bracket_equations()
    point = {variable: 0 for variable in variables}
    point.update({
        "p_1_0": 1,
        "q_2_1": 1,
        "q_3_0": pow(3, prime - 2, prime),
    })
    assert not any(evaluate(poly, point, prime) for _, poly in equations)

    jacobian = [[derivative(poly, variable, point, prime)
                 for variable in variables] for _, poly in equations]
    rank = rank_mod(jacobian, prime)
    kernel = nullspace_mod(jacobian, prime)
    print(f"full-bilinear: equations={len(equations)} variables={len(variables)} "
          f"rank={rank} tangent_dim={len(kernel)}")

    vertices = ("p_8_0", "p_14_8", "p_16_8",
                "q_12_0", "q_21_12", "q_24_12")
    for vertex in vertices:
        index = variables.index(vertex)
        movable = any(vector[index] % prime for vector in kernel)
        print(f"  tangent can turn on {vertex}: {movable}")

    requirements = {
        "p_8_0": 1, "p_14_8": 1, "q_12_0": 1, "q_21_12": 1,
        "p_16_8": 0, "q_24_12": 0,
    }
    rank_m, rank_aug, consistent, _ = constrained_tangent(
        jacobian, variables, requirements, prime)
    print("  joint lower-vertex tangent:",
          f"rank={rank_m}/{rank_aug} consistent={consistent}")
    print("VERDICT: NO VERDICT")


if __name__ == "__main__":
    main()
