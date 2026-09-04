#!/usr/bin/env python3
"""Exact target/source compatibility checks for the ASTRA strike.

This module deliberately does not search polynomial coefficients.  It joins
generic target meridian cycles to source boundary data, then solves the exact
intersection/complementarity problem for the coordinate pole divisors.

The bounded H3 run uses precisely the boundary-tree generator archived in
``docs/plans/audit/trees/trees.py``.  Its conclusion therefore applies to that
generated list only; it is not an unbounded compactification theorem.
"""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import sys
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
TREE_TOOL = ROOT / "docs/plans/audit/trees/trees.py"
sys.dont_write_bytecode = True


def load_tree_tool():
    spec = importlib.util.spec_from_file_location("astra_archived_trees", TREE_TOOL)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {TREE_TOOL}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


TREES = load_tree_tool()


@dataclass(frozen=True)
class EscapeComponent:
    """One source dicritical component above one target component.

    ``degree`` is its tangential degree over the normalization of the target
    curve. ``ramification`` is its generic transverse ramification index.
    """

    degree: int
    ramification: int

    @property
    def discrepancy(self) -> int:
        # ord_E(dP wedge dQ) = ramification - 1 = -k_E.
        return 1 - self.ramification


@dataclass(frozen=True)
class TargetComponent:
    alpha: int
    beta: int
    moved_sheets: int
    moved_cycles: int


@dataclass
class SearchSummary:
    target_bidegree: list[int]
    geometric_degree: int
    max_blowups: int
    generated_tree_records: int
    relevant_tree_records: int
    escape_placements: int
    p_coordinate_solutions: int
    q_coordinate_solutions: int
    paired_coordinate_solutions: int
    joint_survivors: int
    higher_dimensional_kernel_walls: int
    expected_p_fibre_euler: int
    expected_q_fibre_euler: int


def bridge_counts(components: Sequence[EscapeComponent]) -> tuple[int, int]:
    """Return (moved cycles, moved sheets) forced by source dicriticals."""

    cycles = sum(component.degree for component in components)
    sheets = sum(component.degree * component.ramification for component in components)
    return cycles, sheets


def bridge_matches(
    target: TargetComponent, components: Sequence[EscapeComponent]
) -> bool:
    return bridge_counts(components) == (target.moved_cycles, target.moved_sheets)


def mat_vec(matrix: Sequence[Sequence[int]], vector: Sequence[Fraction]) -> list[Fraction]:
    return [
        sum(Fraction(matrix[i][j]) * vector[j] for j in range(len(vector)))
        for i in range(len(vector))
    ]


def coordinate_solutions(tree, mandatory_degrees: dict[int, int]):
    """Solve M m = d, m,d >= 0, and m_i d_i = 0 exactly.

    Here m is a coordinate pole divisor and d its horizontal-degree vector.
    The complementarity equation says a boundary component cannot
    simultaneously be a pole component and carry a finite nonconstant value of
    that coordinate.  The requested horizontal degrees are fixed on the
    target-side escape components.

    Enumerating the zero set of m converts the problem to kernels of principal
    submatrices.  Principal kernels of dimension above one are reported rather
    than silently discarded.
    """

    size = len(tree.k)
    raw = tree.matrix()
    matrix = [[int(raw[i, j]) for j in range(size)] for i in range(size)]
    forced_zero = set(mandatory_degrees)
    optional_zero = [i for i in range(size) if i not in forced_zero]
    solutions: set[tuple[tuple[int, ...], tuple[int, ...]]] = set()
    kernel_walls = 0

    for mask in range(1 << len(optional_zero)):
        zero_set = forced_zero | {
            optional_zero[j]
            for j in range(len(optional_zero))
            if (mask >> j) & 1
        }
        pole_set = [i for i in range(size) if i not in zero_set]
        if not pole_set:
            continue

        principal = sp.Matrix(
            [[matrix[i][j] for j in pole_set] for i in pole_set]
        )
        kernel = principal.nullspace()
        if len(kernel) > 1:
            kernel_walls += 1
            continue
        if len(kernel) != 1:
            continue

        generator = [Fraction(int(x.p), int(x.q)) for x in kernel[0]]
        if all(x < 0 for x in generator):
            generator = [-x for x in generator]
        if any(x <= 0 for x in generator):
            continue

        base_poles = [Fraction(0) for _ in range(size)]
        for index, value in zip(pole_set, generator):
            base_poles[index] = value
        base_degrees = mat_vec(matrix, base_poles)

        if any(base_degrees[i] != 0 for i in pole_set):
            raise AssertionError("principal-kernel construction failed")
        if any(base_degrees[i] < 0 for i in zero_set):
            continue

        scale = None
        compatible = True
        for index, required in mandatory_degrees.items():
            if base_degrees[index] <= 0:
                compatible = False
                break
            this_scale = Fraction(required) / base_degrees[index]
            if scale is None:
                scale = this_scale
            elif scale != this_scale:
                compatible = False
                break
        if not compatible or scale is None or scale <= 0:
            continue

        poles = [x * scale for x in base_poles]
        degrees = [x * scale for x in base_degrees]
        if any(x.denominator != 1 for x in poles + degrees):
            continue
        int_poles = tuple(int(x) for x in poles)
        int_degrees = tuple(int(x) for x in degrees)
        if any(int_poles[i] * int_degrees[i] != 0 for i in range(size)):
            raise AssertionError("complementarity failed")
        solutions.add((int_poles, int_degrees))

    return sorted(solutions), kernel_walls


def escape_partitions() -> list[tuple[EscapeComponent, ...]]:
    """Partitions of the H3 cycle data into irreducible source components."""

    return [
        (EscapeComponent(degree=2, ramification=2),),
        (
            EscapeComponent(degree=1, ramification=2),
            EscapeComponent(degree=1, ramification=2),
        ),
    ]


def keller_delta(tree, p_poles: Sequence[int], q_poles: Sequence[int]) -> list[int]:
    return [
        p_poles[i] + q_poles[i] + 1 - tree.k[i]
        for i in range(len(tree.k))
    ]


def fibre_euler(tree, horizontal_degrees: Sequence[int]) -> int:
    """Euler characteristic of a smooth generic affine coordinate fibre.

    Adjunction gives 2g-2=-sum(k_E*d_E), while the number of punctures is
    sum(d_E), hence chi=sum((k_E-1)*d_E).
    """

    return sum(
        (tree.k[i] - 1) * horizontal_degrees[i]
        for i in range(len(tree.k))
    )


def search_h3(beta: int, max_blowups: int = 6) -> SearchSummary:
    if beta not in (5, 6):
        raise ValueError("the audited H3 target has beta 5 or 6")
    target = TargetComponent(alpha=3, beta=beta, moved_sheets=4, moved_cycles=2)
    partitions = escape_partitions()
    assert all(bridge_matches(target, partition) for partition in partitions)

    trees = TREES.gen_trees(max_blowups)
    relevant = placements = p_count = q_count = pairs = survivors = walls = 0

    for tree in trees:
        compatible_indices = {
            component.discrepancy: [
                i for i, discrepancy in enumerate(tree.k) if discrepancy == component.discrepancy
            ]
            for partition in partitions
            for component in partition
        }
        if not compatible_indices.get(-1):
            continue
        relevant += 1

        for partition in partitions:
            index_pool = compatible_indices[partition[0].discrepancy]
            for indices in itertools.combinations(index_pool, len(partition)):
                placements += 1
                p_required = {
                    index: target.alpha * component.degree
                    for index, component in zip(indices, partition)
                }
                q_required = {
                    index: target.beta * component.degree
                    for index, component in zip(indices, partition)
                }
                p_solutions, p_walls = coordinate_solutions(tree, p_required)
                q_solutions, q_walls = coordinate_solutions(tree, q_required)
                walls += p_walls + q_walls
                p_count += len(p_solutions)
                q_count += len(q_solutions)

                for p_poles, p_degrees in p_solutions:
                    for q_poles, q_degrees in q_solutions:
                        pairs += 1
                        degree_pq = sum(
                            p_poles[i] * q_degrees[i]
                            for i in range(len(tree.k))
                        )
                        degree_qp = sum(
                            q_poles[i] * p_degrees[i]
                            for i in range(len(tree.k))
                        )
                        if degree_pq != 6 or degree_qp != 6:
                            continue
                        if min(keller_delta(tree, p_poles, q_poles)) < 0:
                            continue
                        if fibre_euler(tree, p_degrees) != 6 - target.alpha * target.moved_sheets:
                            continue
                        if fibre_euler(tree, q_degrees) != 6 - target.beta * target.moved_sheets:
                            continue
                        survivors += 1

    return SearchSummary(
        target_bidegree=[target.alpha, target.beta],
        geometric_degree=6,
        max_blowups=max_blowups,
        generated_tree_records=len(trees),
        relevant_tree_records=relevant,
        escape_placements=placements,
        p_coordinate_solutions=p_count,
        q_coordinate_solutions=q_count,
        paired_coordinate_solutions=pairs,
        joint_survivors=survivors,
        higher_dimensional_kernel_walls=walls,
        expected_p_fibre_euler=6 - target.alpha * target.moved_sheets,
        expected_q_fibre_euler=6 - target.beta * target.moved_sheets,
    )


def run_controls() -> dict:
    """Positive and negative exact controls run before the research search."""

    # Resolve the identity map on P^2 by blowing up the two distinct coordinate
    # base points on the line at infinity.
    identity_tree = TREES.Tree().blowup_free(0).blowup_free(0)
    p_solutions, p_walls = coordinate_solutions(identity_tree, {1: 1})
    q_solutions, q_walls = coordinate_solutions(identity_tree, {2: 1})
    expected_p = ((1, 0, 1), (0, 1, 0))
    expected_q = ((1, 1, 0), (0, 0, 1))
    if expected_p not in p_solutions or expected_q not in q_solutions:
        raise AssertionError("identity-map positive control was not recovered")
    delta = keller_delta(identity_tree, expected_p[0], expected_q[0])
    degree_pq = sum(a * b for a, b in zip(expected_p[0], expected_q[1]))
    degree_qp = sum(a * b for a, b in zip(expected_q[0], expected_p[1]))
    p_euler = fibre_euler(identity_tree, expected_p[1])
    q_euler = fibre_euler(identity_tree, expected_q[1])
    if (
        delta != [0, 0, 0]
        or degree_pq != 1
        or degree_qp != 1
        or p_euler != 1
        or q_euler != 1
    ):
        raise AssertionError("identity-map intersection invariants are wrong")

    h3_source = (EscapeComponent(2, 2),)
    target = TargetComponent(3, 5, 4, 2)
    bad_target = TargetComponent(3, 5, 5, 2)
    if not bridge_matches(target, h3_source) or bridge_matches(bad_target, h3_source):
        raise AssertionError("target/source bridge controls failed")

    return {
        "identity_automorphism": {
            "self_intersections": identity_tree.selfint,
            "discrepancies": identity_tree.k,
            "p_poles": list(expected_p[0]),
            "p_horizontal_degrees": list(expected_p[1]),
            "q_poles": list(expected_q[0]),
            "q_horizontal_degrees": list(expected_q[1]),
            "geometric_degree": degree_pq,
            "keller_delta": delta,
            "generic_fibre_euler": [p_euler, q_euler],
        },
        "bridge_positive": {
            "source": [asdict(x) | {"discrepancy": x.discrepancy} for x in h3_source],
            "target_moved_cycles_and_sheets": list(bridge_counts(h3_source)),
        },
        "bridge_negative_rejected": True,
        "kernel_walls": p_walls + q_walls,
        "status": "PASS",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-blowups", type=int, default=6)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = {
        "evidence_label": "EXACT-Q",
        "scope": "archived boundary-tree records through the stated blowup bound",
        "controls": run_controls(),
        "h3_3_5": asdict(search_h3(5, args.max_blowups)),
        "h3_3_6": asdict(search_h3(6, args.max_blowups)),
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
