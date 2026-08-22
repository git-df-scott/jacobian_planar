#!/usr/bin/env python3
"""Kernel-aware exact order-two obstruction search on the p_1_1=0 chart.

The anchor is the exact family-A point

    P = x + y,
    Q = 1 + x^2*y + x*y^2 + y^3/3.

At first order the slope-top coefficients are normalized to

    P_top = t + O(t^2),    Q_top = t + O(t^2).

Together with a fixed p_1_0 chart coordinate, these linear conditions cut the
44-dimensional tangent space to an affine space d0 + N*u with all 34 kernel
parameters retained.  At second order we impose the faithful square/cube
continuation

    P_top = t*(1 + t*z^4)^2 + O(t^3),
    Q_top = t*(1 + t*z^4)^3 + O(t^3),

and keep the right-edge vertices p_14_8 and q_21_12 zero.  Their geometrically
compatible shared-L schedule starts only at orders three and four.

For every first jet d, the quadratic coefficient of the bilinear bracket is
projected exactly to the cokernel of the constrained second-order matrix.  A
zero obstruction is only a formal mod-p two-jet lead, never a counterexample.
Failure to find one in the sampled sets is NO VERDICT.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path
from typing import Iterable, Sequence

from bilinear_full import P_VARIABLES, Q_VARIABLES, build_bracket_equations
from bilinear_tangent import derivative
from pentagon_core import nullspace_mod, rank_mod, solve_affine


VARIABLES = P_VARIABLES + Q_VARIABLES
RIGHT_EDGE_EARLY_ZERO = (
    "p_14_8", "p_15_8",
    "q_21_12", "q_22_12", "q_23_12",
)


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    for divisor in range(3, math.isqrt(value) + 1, 2):
        if value % divisor == 0:
            return False
    return True


def anchor(prime: int) -> dict[str, int]:
    point = {variable: 0 for variable in VARIABLES}
    point.update({
        "p_1_0": 1,
        "q_2_1": 1,
        "q_3_0": pow(3, prime - 2, prime),
    })
    return point


def jacobian_at_base(equations, base, prime: int) -> list[list[int]]:
    return [[derivative(poly, variable, base, prime)
             for variable in VARIABLES] for _, poly in equations]


def constraint_matrix(requirements: dict[str, int], prime: int):
    rows = []
    rhs = []
    for variable, value in requirements.items():
        row = [0] * len(VARIABLES)
        row[VARIABLES.index(variable)] = 1
        rows.append(row)
        rhs.append(value % prime)
    return rows, rhs


def first_order_requirements() -> dict[str, int]:
    """The normalized common square/cube slope-top leading direction."""
    required = {"p_1_0": 0}
    for i in range(9):
        required[f"p_{8 + i}_{i}"] = int(i == 0)
    for i in range(13):
        required[f"q_{12 + i}_{i}"] = int(i == 0)
    for variable in RIGHT_EDGE_EARLY_ZERO:
        required[variable] = 0
    return required


def second_order_requirements() -> dict[str, int]:
    """Faithful order-two continuation; right-edge vertices still vanish."""
    required = {"p_1_0": 0}
    for i in range(9):
        required[f"p_{8 + i}_{i}"] = 2 if i == 4 else 0
    for i in range(13):
        required[f"q_{12 + i}_{i}"] = 3 if i == 4 else 0
    for variable in RIGHT_EDGE_EARLY_ZERO:
        required[variable] = 0
    return required


def affine_first_jets(jacobian, prime: int):
    rows, rhs = constraint_matrix(first_order_requirements(), prime)
    matrix = [row[:] for row in jacobian] + rows
    target = [0] * len(jacobian) + rhs
    # solve_affine solves M*x=-v.
    rank_m, rank_aug, consistent, particular = solve_affine(
        matrix, [(-value) % prime for value in target], prime)
    if not consistent or particular is None:
        raise AssertionError("normalized first-order square/cube gate is empty")
    kernel = nullspace_mod(matrix, prime)
    if rank_m != rank_aug or len(kernel) != len(VARIABLES) - rank_m:
        raise AssertionError("first-jet affine-space dimension mismatch")
    return matrix, particular, kernel, rank_m


def quadratic_rhs(equations, direction: Sequence[int], prime: int) -> list[int]:
    """Coefficient of t^2 in f(base+t*direction) for bilinear f."""
    positions = {variable: i for i, variable in enumerate(VARIABLES)}
    out = []
    for _, poly in equations:
        value = 0
        for monomial, coefficient in poly.items():
            if len(monomial) == 2:
                left, right = monomial
                value += (coefficient * direction[positions[left]] *
                          direction[positions[right]])
            elif len(monomial) > 2:
                raise AssertionError(f"unexpected degree {len(monomial)}")
        out.append(value % prime)
    return out


def combine_direction(particular, kernel, parameters, prime: int):
    direction = list(particular)
    for coefficient, basis_vector in zip(parameters, kernel):
        if coefficient % prime:
            direction = [(value + coefficient * delta) % prime
                         for value, delta in zip(direction, basis_vector)]
    return direction


def transpose(rows: Sequence[Sequence[int]]) -> list[list[int]]:
    return [list(column) for column in zip(*rows)]


def dot(left: Sequence[int], right: Sequence[int], prime: int) -> int:
    return sum(a * b for a, b in zip(left, right)) % prime


def coefficient_layout(dimension: int):
    pairs = [(i, j) for i in range(dimension) for j in range(i, dimension)]
    pair_position = {pair: 1 + dimension + k
                     for k, pair in enumerate(pairs)}
    return pairs, pair_position


def quadratic_form(poly, particular, kernel, positions, pair_position,
                   dimension: int, prime: int) -> list[int]:
    """Coefficient vector of q(d0+N*u), ordered 1,u_i,u_i*u_j."""
    size = 1 + dimension + dimension * (dimension + 1) // 2
    form = [0] * size
    for monomial, coefficient in poly.items():
        if len(monomial) != 2:
            continue
        left, right = (positions[monomial[0]], positions[monomial[1]])
        coefficient %= prime
        form[0] += coefficient * particular[left] * particular[right]
        for i in range(dimension):
            form[1 + i] += coefficient * (
                particular[left] * kernel[i][right] +
                kernel[i][left] * particular[right])
        for i in range(dimension):
            for j in range(i, dimension):
                value = kernel[i][left] * kernel[j][right]
                if i != j:
                    value += kernel[j][left] * kernel[i][right]
                form[pair_position[(i, j)]] += coefficient * value
    return [value % prime for value in form]


def rref_nonzero_rows(rows: Sequence[Sequence[int]], prime: int):
    """Return an exact row-space basis in reduced echelon form."""
    matrix = [[value % prime for value in row] for row in rows]
    if not matrix:
        return []
    row = 0
    for column in range(len(matrix[0])):
        pivot = next((r for r in range(row, len(matrix))
                      if matrix[r][column]), None)
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        inverse = pow(matrix[row][column], prime - 2, prime)
        matrix[row] = [(value * inverse) % prime for value in matrix[row]]
        for r in range(len(matrix)):
            if r != row and matrix[r][column]:
                scale = matrix[r][column]
                matrix[r] = [(matrix[r][c] - scale * matrix[row][c]) % prime
                             for c in range(len(matrix[0]))]
        row += 1
        if row == len(matrix):
            break
    return [entry for entry in matrix if any(entry)]


def obstruction_forms(equations, particular, kernel, second_matrix,
                      second_rhs, prime: int):
    """Project [q(d); -second_rhs] to coker([J; constraints])."""
    dimension = len(kernel)
    pairs, pair_position = coefficient_layout(dimension)
    positions = {variable: i for i, variable in enumerate(VARIABLES)}
    qforms = [quadratic_form(poly, particular, kernel, positions,
                            pair_position, dimension, prime)
              for _, poly in equations]

    left_kernel = nullspace_mod(transpose(second_matrix), prime)
    projected = []
    equation_count = len(equations)
    form_size = len(qforms[0])
    for covector in left_kernel:
        form = [0] * form_size
        for equation_index, coefficient in enumerate(
                covector[:equation_count]):
            if coefficient:
                source = qforms[equation_index]
                form = [(a + coefficient * b) % prime
                        for a, b in zip(form, source)]
        constant = sum(
            covector[equation_count + i] * (-value)
            for i, value in enumerate(second_rhs))
        form[0] = (form[0] + constant) % prime
        projected.append(form)
    basis = rref_nonzero_rows(projected, prime)
    return left_kernel, projected, basis, pairs


def linear_obstruction_slice(forms, dimension: int, prime: int):
    """Solve every degree-at-most-one polynomial in the obstruction span."""
    quadratic_offset = 1 + dimension
    quadratic_coefficients = [form[quadratic_offset:] for form in forms]
    annihilators = nullspace_mod(transpose(quadratic_coefficients), prime)
    low_forms = []
    for coefficients in annihilators:
        form = [0] * len(forms[0])
        for coefficient, source in zip(coefficients, forms):
            if coefficient:
                form = [(a + coefficient * b) % prime
                        for a, b in zip(form, source)]
        if any(form[quadratic_offset:]):
            raise AssertionError("failed to cancel quadratic obstruction terms")
        low_forms.append(form[:quadratic_offset])
    low_forms = rref_nonzero_rows(low_forms, prime)
    matrix = [form[1:] for form in low_forms]
    constants = [form[0] for form in low_forms]
    rank_m, rank_aug, consistent, particular = solve_affine(
        matrix, constants, prime)
    if not consistent or particular is None:
        return low_forms, None, [], rank_m, rank_aug
    kernel = nullspace_mod(matrix, prime)
    return low_forms, particular, kernel, rank_m, rank_aug


def substitute_affine_form(form, affine, kernel, old_pairs, prime: int):
    """Substitute u=affine+kernel*w in one affine-quadratic form."""
    old_dimension = len(affine)
    new_dimension = len(kernel)
    new_pairs, new_pair_position = coefficient_layout(new_dimension)
    out = [0] * (1 + new_dimension + len(new_pairs))
    out[0] = form[0]
    for i in range(old_dimension):
        coefficient = form[1 + i]
        out[0] += coefficient * affine[i]
        for k in range(new_dimension):
            out[1 + k] += coefficient * kernel[k][i]
    old_offset = 1 + old_dimension
    for old_index, (i, j) in enumerate(old_pairs):
        coefficient = form[old_offset + old_index]
        if not coefficient:
            continue
        out[0] += coefficient * affine[i] * affine[j]
        for k in range(new_dimension):
            out[1 + k] += coefficient * (
                affine[i] * kernel[k][j] + kernel[k][i] * affine[j])
        for k in range(new_dimension):
            for ell in range(k, new_dimension):
                value = kernel[k][i] * kernel[ell][j]
                if k != ell:
                    value += kernel[ell][i] * kernel[k][j]
                out[new_pair_position[(k, ell)]] += coefficient * value
    return [value % prime for value in out]


def substitute_obstruction_system(forms, affine, kernel, old_pairs,
                                  prime: int):
    transformed = [substitute_affine_form(
        form, affine, kernel, old_pairs, prime) for form in forms]
    transformed = rref_nonzero_rows(transformed, prime)
    new_pairs, _ = coefficient_layout(len(kernel))
    return transformed, new_pairs


def evaluate_form(form, parameters, pairs, prime: int) -> int:
    value = form[0]
    dimension = len(parameters)
    for i in range(dimension):
        value += form[1 + i] * parameters[i]
    offset = 1 + dimension
    for k, (i, j) in enumerate(pairs):
        value += form[offset + k] * parameters[i] * parameters[j]
    return value % prime


def evaluate_sparse_form(form, support, pairs_index, dimension, prime: int):
    value = form[0]
    for i, coefficient in support:
        value += form[1 + i] * coefficient
    for a, (i, left) in enumerate(support):
        for j, right in support[a:]:
            value += form[pairs_index[(i, j)]] * left * right
    return value % prime


def obstruction_zero(forms, parameters, pairs, prime: int) -> bool:
    return all(not evaluate_form(form, parameters, pairs, prime)
               for form in forms)


def sparse_obstruction_zero(forms, support, pairs_index, dimension,
                            prime: int) -> bool:
    return all(not evaluate_sparse_form(form, support, pairs_index,
                                        dimension, prime)
               for form in forms)


def exhaustive_weight_two(forms, pairs, dimension: int, prime: int):
    """Exhaust every kernel-coordinate vector of Hamming weight at most two."""
    pairs_index = {pair: 1 + dimension + k
                   for k, pair in enumerate(pairs)}
    samples = 0
    if sparse_obstruction_zero(forms, [], pairs_index, dimension, prime):
        return [0] * dimension, 1
    samples += 1
    nonzero = range(1, prime)
    for i in range(dimension):
        for left in nonzero:
            samples += 1
            if sparse_obstruction_zero(
                    forms, [(i, left)], pairs_index, dimension, prime):
                parameters = [0] * dimension
                parameters[i] = left
                return parameters, samples
    for i in range(dimension):
        for j in range(i + 1, dimension):
            for left in nonzero:
                for right in nonzero:
                    samples += 1
                    if sparse_obstruction_zero(
                            forms, [(i, left), (j, right)], pairs_index,
                            dimension, prime):
                        parameters = [0] * dimension
                        parameters[i], parameters[j] = left, right
                        return parameters, samples
    return None, samples


def random_reconnaissance(forms, pairs, dimension: int, prime: int,
                          count: int, seed: int):
    rng = random.Random(seed)
    for sample in range(1, count + 1):
        parameters = [rng.randrange(prime) for _ in range(dimension)]
        if obstruction_zero(forms, parameters, pairs, prime):
            return parameters, sample
    return None, count


def check_known_curve(equations, jacobian, prime: int):
    """Positive nonlinear control P=x+y+t*y^2 through exact order two."""
    direction = [0] * len(VARIABLES)
    correction = [0] * len(VARIABLES)
    direction[VARIABLES.index("p_2_0")] = 1
    direction[VARIABLES.index("q_3_1")] = 4 * pow(3, prime - 2, prime) % prime
    direction[VARIABLES.index("q_4_0")] = 5 * pow(6, prime - 2, prime) % prime
    correction[VARIABLES.index("q_5_0")] = 8 * pow(15, prime - 2, prime) % prime
    if any(dot(row, direction, prime) for row in jacobian):
        raise AssertionError("known family direction is not tangent")
    rhs = quadratic_rhs(equations, direction, prime)
    residual = [(dot(row, correction, prime) + value) % prime
                for row, value in zip(jacobian, rhs)]
    if any(residual):
        raise AssertionError("known family has a nonzero order-two obstruction")
    left_kernel = nullspace_mod(transpose(jacobian), prime)
    if any(dot(covector, rhs, prime) for covector in left_kernel):
        raise AssertionError("known family does not project to zero in cokernel")
    return len(left_kernel)


def check_negative_p16(jacobian, prime: int):
    row = [0] * len(VARIABLES)
    row[VARIABLES.index("p_16_8")] = 1
    rank_m, rank_aug, consistent, _ = solve_affine(
        [entry[:] for entry in jacobian] + [row],
        [0] * len(jacobian) + [(-1) % prime], prime)
    if consistent or rank_aug != rank_m + 1:
        raise AssertionError("first-order p_16_8 negative control was accepted")
    return rank_m, rank_aug


def lift_and_freeze(parameters, particular, kernel, equations, second_matrix,
                    second_rhs, prime: int, freeze_path: Path):
    direction = combine_direction(particular, kernel, parameters, prime)
    rhs = quadratic_rhs(equations, direction, prime)
    solve_vector = rhs + [(-value) % prime for value in second_rhs]
    rank_m, rank_aug, consistent, correction = solve_affine(
        second_matrix, solve_vector, prime)
    if not consistent or correction is None or rank_m != rank_aug:
        raise AssertionError("projected-zero lead failed direct lifting")
    equation_residual = [(dot(row, correction, prime) + value) % prime
                         for row, value in zip(second_matrix[:len(equations)],
                                               rhs)]
    if any(equation_residual):
        raise AssertionError("frozen lead fails order-two bracket equations")
    constraint_rows = second_matrix[len(equations):]
    if any((dot(row, correction, prime) - value) % prime
           for row, value in zip(constraint_rows, second_rhs)):
        raise AssertionError("frozen lead fails order-two schedule constraints")

    data = {
        "status": "MOD-p FORMAL ORDER-2 GATE: NONEMPTY",
        "prime": prime,
        "parameters": parameters,
        "first_jet_nonzero": {
            variable: value for variable, value in zip(VARIABLES, direction)
            if value % prime
        },
        "second_jet_nonzero": {
            variable: value for variable, value in zip(VARIABLES, correction)
            if value % prime
        },
        "second_order_requirements": second_order_requirements(),
    }
    freeze_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, default=43)
    parser.add_argument("--random-samples", type=int, default=100_000)
    parser.add_argument("--seed", type=int, default=2026082202)
    parser.add_argument("--skip-weight-two", action="store_true")
    parser.add_argument("--freeze", type=Path)
    args = parser.parse_args()
    prime = args.prime
    if prime <= 5 or not is_prime(prime):
        raise ValueError("--prime must be a prime greater than 5")

    equations = build_bracket_equations()
    base = anchor(prime)
    jacobian = jacobian_at_base(equations, base, prime)
    jacobian_rank = rank_mod(jacobian, prime)
    if jacobian_rank + len(nullspace_mod(jacobian, prime)) != len(VARIABLES):
        raise AssertionError("Jacobian rank/nullity mismatch")

    first_matrix, particular, kernel, first_rank = affine_first_jets(
        jacobian, prime)
    first_rhs = [0] * len(jacobian) + list(first_order_requirements().values())
    if any((dot(row, particular, prime) - value) % prime
           for row, value in zip(first_matrix, first_rhs)):
        raise AssertionError("particular first jet fails its defining system")
    if any(dot(row, vector, prime)
           for vector in kernel for row in first_matrix):
        raise AssertionError("first-jet kernel basis failed exact verification")
    for variable in RIGHT_EDGE_EARLY_ZERO:
        index = VARIABLES.index(variable)
        if particular[index] or any(vector[index] for vector in kernel):
            raise AssertionError(
                f"right-edge coefficient {variable} is not forced at order one")

    known_cokernel = check_known_curve(equations, jacobian, prime)
    negative_ranks = check_negative_p16(jacobian, prime)

    second_constraint_rows, second_rhs = constraint_matrix(
        second_order_requirements(), prime)
    second_matrix = [row[:] for row in jacobian] + second_constraint_rows
    second_rank = rank_mod(second_matrix, prime)
    left_kernel, projected_forms, forms, pairs = obstruction_forms(
        equations, particular, kernel, second_matrix, second_rhs, prime)

    # Independent projector control: every column-space vector must vanish.
    planted = [(17 * i + 5) % prime for i in range(len(VARIABLES))]
    image = [dot(row, planted, prime) for row in second_matrix]
    if any(dot(covector, image, prime) for covector in left_kernel):
        raise AssertionError("cokernel projector rejects a planted image vector")

    # Cross-check the affine-quadratic expansion against direct bilinear
    # evaluation and direct cokernel projection at independent exact jets.
    control_rng = random.Random(2026082299 + prime)
    for _ in range(8):
        parameters = [control_rng.randrange(prime) for _ in kernel]
        direction = combine_direction(particular, kernel, parameters, prime)
        rhs = quadratic_rhs(equations, direction, prime)
        direct_vector = rhs + [(-value) % prime for value in second_rhs]
        direct_projection = [dot(covector, direct_vector, prime)
                             for covector in left_kernel]
        expanded_projection = [evaluate_form(
            form, parameters, pairs, prime) for form in projected_forms]
        if direct_projection != expanded_projection:
            raise AssertionError("symbolic obstruction expansion mismatch")

    low_forms, linear_particular, linear_kernel, linear_rank, linear_aug_rank = (
        linear_obstruction_slice(forms, len(kernel), prime))
    low_degree_span_dimension = len(low_forms)
    without_constant_rank = rank_mod([form[1:] for form in forms], prime)
    constant_certificate = len(forms) > without_constant_rank
    if linear_particular is None:
        reduced_forms, reduced_pairs = [], []
    else:
        reduced_forms, reduced_pairs = substitute_obstruction_system(
            forms, linear_particular, linear_kernel, pairs, prime)

    print(f"FIELD F_{prime}")
    print(f"full-bilinear: equations={len(equations)} variables={len(VARIABLES)} "
          f"jacobian_rank={jacobian_rank} tangent_dim={len(VARIABLES)-jacobian_rank}")
    print(f"first-jet gate: rank={first_rank} affine_kernel_dim={len(kernel)}")
    print("PASS five explicit right-edge coefficients are forced zero at "
          "first order")
    print(f"second-order constrained matrix: rows={len(second_matrix)} "
          f"rank={second_rank} cokernel_dim={len(left_kernel)}")
    print(f"obstruction polynomial span={len(forms)} "
          f"low_degree_span_dim={low_degree_span_dimension} "
          f"constant_certificate={constant_certificate}")
    print(f"linear-obstruction slice: rank={linear_rank}/{linear_aug_rank} "
          f"compatible_dim={len(linear_kernel)} "
          f"restricted_obstruction_span={len(reduced_forms)}")
    print(f"PASS known P=x+y+a*y^2 curve has zero obstruction "
          f"in the {known_cokernel}-dimensional bracket cokernel")
    print("PASS negative control rejects first-order p_16_8 "
          f"(ranks={negative_ranks[0]}/{negative_ranks[1]})")
    print("PASS planted second-order image vector projects to zero")
    print("PASS 8 exact direct-vs-expanded cokernel projection controls")

    lead = None
    reduced_lead = None
    total_samples = 0
    if linear_particular is not None and not args.skip_weight_two:
        reduced_lead, samples = exhaustive_weight_two(
            reduced_forms, reduced_pairs, len(linear_kernel), prime)
        total_samples += samples
        complete = samples == (1 + len(linear_kernel) * (prime - 1) +
                               len(linear_kernel) *
                               (len(linear_kernel) - 1) // 2 *
                               (prime - 1) ** 2)
        print(f"linear-compatible coordinate Hamming-weight<=2: "
              f"samples={samples} complete={complete} "
              f"zero_obstruction={reduced_lead is not None}")

    if (linear_particular is not None and reduced_lead is None and
            args.random_samples):
        reduced_lead, samples = random_reconnaissance(
            reduced_forms, reduced_pairs, len(linear_kernel), prime,
            args.random_samples, args.seed)
        total_samples += samples
        print(f"linear-compatible deterministic-random: samples={samples} "
              f"seed={args.seed} zero_obstruction={reduced_lead is not None}")

    if reduced_lead is not None:
        lead = combine_direction(
            linear_particular, linear_kernel, reduced_lead, prime)
        if not obstruction_zero(forms, lead, pairs, prime):
            raise AssertionError("reduced obstruction lead fails full projection")

    print(f"total exact first jets tested={total_samples}")
    if lead is not None:
        freeze_path = args.freeze or Path(__file__).with_name(
            f"kernel_order2_lead_p{prime}.json")
        data = lift_and_freeze(
            lead, particular, kernel, equations, second_matrix, second_rhs,
            prime, freeze_path)
        print("MOD-p FORMAL ORDER-2 GATE: NONEMPTY")
        print(f"FROZEN {freeze_path}")
        print(f"first-jet nonzeros={len(data['first_jet_nonzero'])} "
              f"second-jet nonzeros={len(data['second_jet_nonzero'])}")
    else:
        print("No obstruction-zero jet was found in the stated finite samples.")
    print("ROOT CE TARGET: NO VERDICT")
    print("VERDICT: NONEMPTY" if lead is not None else "VERDICT: NO VERDICT")


if __name__ == "__main__":
    main()
