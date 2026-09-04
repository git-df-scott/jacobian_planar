#!/usr/bin/env python3
"""Deterministic replay of the PR #24 abstract target pre-screen.

The output is only ADMISSIBLE-SHAPE data.  It does not assert that a
transitive group or polynomial curve realizes any row.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path


def cusp_decompositions(degree: int, moved: int, cusp_order: int):
    result = set()
    half = (cusp_order - 1) // 2
    for regular in range(degree // (2 * cusp_order) + 1):
        for polygon in range(degree // cusp_order + 1):
            for pair in range(degree // 2 + 1):
                points = 2 * cusp_order * regular + cusp_order * polygon + 2 * pair
                transpositions = cusp_order * regular + half * polygon + pair
                if points <= degree and transpositions == moved // 2:
                    result.add((degree - points, regular + polygon + pair))
    return result


def node_decompositions(degree: int, moved: int):
    result = set()
    for regular in range(degree // 4 + 1):
        for both in range(degree // 2 + 1):
            for first in range(degree // 2 + 1):
                for second in range(degree // 2 + 1):
                    points = 4 * regular + 2 * (both + first + second)
                    if points > degree:
                        continue
                    moved_first = 2 * regular + both + first
                    moved_second = 2 * regular + both + second
                    if moved_first == moved // 2 and moved_second == moved // 2:
                        result.add((degree - points, regular + both + first + second))
    return result


def enumerate_shapes():
    rows = []
    for degree in range(4, 13):
        for moved in range(2, degree, 2):
            fixed = degree - moved
            for cusp_count in range(1, 5):
                for types in itertools.combinations_with_replacement((3, 5, 7, 9), cusp_count):
                    for nodes in range(1, 5):
                        branch_count = cusp_count + 2 * nodes
                        required_fixed = 1 - degree * nodes - fixed * (1 - branch_count)
                        if required_fixed < 0:
                            continue
                        base_chi_r = (moved // 2) * (1 - branch_count)
                        cusp_options = [cusp_decompositions(degree, moved, order) for order in types]
                        node_options = node_decompositions(degree, moved)
                        if not all(cusp_options) or not node_options:
                            continue
                        for choice in itertools.product(*cusp_options, *([node_options] * nodes)):
                            fixed_sum = sum(item[0] for item in choice)
                            orbit_sum = sum(item[1] for item in choice)
                            chi_r = base_chi_r + orbit_sum
                            if fixed_sum == required_fixed and chi_r >= 1:
                                rows.append((degree, moved, fixed, types, nodes, fixed_sum, chi_r, choice))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rows = enumerate_shapes()
    if len(rows) != 5261:
        raise AssertionError(f"PR #24 count changed: {len(rows)}")
    keys = {(row[0], row[1], row[2], row[3], row[4]) for row in rows}
    report = {
        "evidence_label": "ADMISSIBLE-SHAPE",
        "raw_feasible_configurations": len(rows),
        "unique_basic_signatures": len(keys),
        "counts_by_degree": dict(sorted(Counter(row[0] for row in rows).items())),
        "scope": {
            "degree": [4, 12],
            "even_moved_sheets": True,
            "cusp_orders": [3, 5, 7, 9],
            "cusp_count": [1, 4],
            "node_count": [1, 4],
        },
        "realizability": "UNKNOWN: no group, peripheral system, or polynomial curve is constructed",
        "status": "PASS",
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
