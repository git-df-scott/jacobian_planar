#!/usr/bin/env python3
"""Order-by-order formal-arc reconnaissance from the degenerate solution.

This is not a point finder and cannot produce NONEMPTY.  It follows one greedy
particular correction for a prescribed square/cube top edge.  Because each
correction is defined modulo a large Jacobian kernel, failure of this greedy
path excludes no formal arc and is NO VERDICT.
"""

from bilinear_full import P_VARIABLES, Q_VARIABLES, build_bracket_equations
from bilinear_tangent import derivative
from pentagon_core import solve_affine


def coefficient_at(poly, series, order, prime):
    total = 0
    for monomial, coefficient in poly.items():
        if not monomial:
            if order == 0:
                total += coefficient
        elif len(monomial) == 1:
            total += coefficient * series[monomial[0]][order]
        elif len(monomial) == 2:
            left, right = monomial
            total += coefficient * sum(
                series[left][k] * series[right][order - k]
                for k in range(order + 1))
        else:
            raise AssertionError(f"unexpected degree {len(monomial)}")
    return total % prime


def required_coefficients(order, p14_order, q21_order, top_edge=True):
    required = {"p_1_0": 0}
    for i in range(9):
        required[f"p_{8+i}_{i}"] = 0
    for i in range(13):
        required[f"q_{12+i}_{i}"] = 0

    if top_edge:
        # P_top = t*(1+t*u^4)^2.
        if order == 1:
            required["p_8_0"] = 1
        elif order == 2:
            required["p_12_4"] = 2
        elif order == 3:
            required["p_16_8"] = 1

        # Q_top = t*(1+t*u^4)^3.
        if order == 1:
            required["q_12_0"] = 1
        elif order == 2:
            required["q_16_4"] = 3
        elif order == 3:
            required["q_20_8"] = 3
        elif order == 4:
            required["q_24_12"] = 1

    required["p_14_8"] = int(order == p14_order)
    required["q_21_12"] = int(order == q21_order)
    return required


def lift(prime, max_order, p14_order, q21_order, jacobian, variables,
         equations, base, top_edge=True):
    series = {variable: [base.get(variable, 0)] + [0] * max_order
              for variable in variables}
    for order in range(1, max_order + 1):
        residual = [coefficient_at(poly, series, order, prime)
                    for _, poly in equations]
        matrix = [row[:] for row in jacobian]
        rhs = [(-value) % prime for value in residual]
        required = required_coefficients(
            order, p14_order, q21_order, top_edge=top_edge)
        for variable, value in required.items():
            row = [0] * len(variables)
            row[variables.index(variable)] = 1
            matrix.append(row)
            rhs.append(value % prime)

        # solve_affine solves M*x=-v, so pass v=-rhs.
        rank_m, rank_aug, consistent, solution = solve_affine(
            matrix, [(-value) % prime for value in rhs], prime)
        if not consistent:
            return series, order - 1, (rank_m, rank_aug)
        for variable, value in zip(variables, solution):
            series[variable][order] = value
        check = [coefficient_at(poly, series, order, prime)
                 for _, poly in equations]
        assert not any(check)
    return series, max_order, (rank_m, rank_aug)


def main(prime=43, max_order=5):
    variables = P_VARIABLES + Q_VARIABLES
    equations = build_bracket_equations()
    base = {variable: 0 for variable in variables}
    base.update({
        "p_1_0": 1,
        "q_2_1": 1,
        "q_3_0": pow(3, prime - 2, prime),
    })
    jacobian = [[derivative(poly, variable, base, prime)
                 for variable in variables] for _, poly in equations]

    # Positive control 1: the constant degenerate solution must lift with every
    # higher coefficient zero.
    _, control_reached, _ = lift(
        prime, max_order, max_order + 1, max_order + 1,
        jacobian, variables, equations, base, top_edge=False)
    assert control_reached == max_order
    print(f"PASS planted constant arc lifts through t^{max_order}")

    # Positive control 2 exercises the quadratic convolution.  It is the exact
    # family P=x+y+t*y^2 and
    # Q=1+x^2*y+x*y^2+y^3/3+(4t/3)*x*y^3+(5t/6)*y^4
    #   +(8t^2/15)*y^5.
    known = {variable: [base.get(variable, 0)] + [0] * max_order
             for variable in variables}
    known["p_2_0"][1] = 1
    known["q_3_1"][1] = 4 * pow(3, prime - 2, prime) % prime
    known["q_4_0"][1] = 5 * pow(6, prime - 2, prime) % prime
    known["q_5_0"][2] = 8 * pow(15, prime - 2, prime) % prime
    for order in range(max_order + 1):
        assert not any(coefficient_at(poly, known, order, prime)
                       for _, poly in equations)
    print(f"PASS known nonconstant family arc through t^{max_order}")

    # Negative control: p_16_8 cannot be forced at first order, as independently
    # predicted by the tangent calculation.
    row = [0] * len(variables)
    row[variables.index("p_16_8")] = 1
    rank_m, rank_aug, consistent, _ = solve_affine(
        jacobian + [row], [0] * len(jacobian) + [-1 % prime], prime)
    assert not consistent and rank_aug == rank_m + 1
    print("PASS negative control rejects first-order p_16_8")

    successes = []
    for p14_order in range(1, 5):
        for q21_order in range(1, 6):
            series, reached, ranks = lift(
                prime, max_order, p14_order, q21_order,
                jacobian, variables, equations, base)
            print(f"p14@t^{p14_order} q21@t^{q21_order}: "
                  f"greedy_reached={reached}/{max_order} "
                  f"ranks={ranks[0]}/{ranks[1]}")
            if reached == max_order:
                successes.append((p14_order, q21_order, series))

    print(f"greedy paths reaching order {max_order}: {len(successes)}")
    if successes:
        p14_order, q21_order, series = successes[0]
        print(f"FIRST LEAD p14@t^{p14_order} q21@t^{q21_order}")
        for vertex in ("p_8_0", "p_14_8", "p_16_8",
                       "q_12_0", "q_21_12", "q_24_12"):
            print(f"  {vertex}: {series[vertex]}")
    print("VERDICT: NO VERDICT")


if __name__ == "__main__":
    main()
