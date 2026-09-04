#!/usr/bin/env python3
"""Independent group-first replay of the six-sheet H3 near-miss.

No GAP database or curve equation is used.  The script enumerates the relevant
conjugacy class in S_6, imposes the H3 Coxeter relations, quotients by
simultaneous conjugacy, and computes the Euler and coarse escaping-curve data.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
from typing import Iterable


Permutation = tuple[int, ...]


def identity(n: int) -> Permutation:
    return tuple(range(n))


def compose(left: Permutation, right: Permutation) -> Permutation:
    return tuple(left[right[i]] for i in range(len(left)))


def inverse(permutation: Permutation) -> Permutation:
    result = [0] * len(permutation)
    for i, image in enumerate(permutation):
        result[image] = i
    return tuple(result)


def power(permutation: Permutation, exponent: int) -> Permutation:
    result = identity(len(permutation))
    base = permutation
    while exponent:
        if exponent & 1:
            result = compose(result, base)
        base = compose(base, base)
        exponent //= 2
    return result


def cycle_type(permutation: Permutation) -> tuple[int, ...]:
    seen: set[int] = set()
    lengths: list[int] = []
    for start in range(len(permutation)):
        if start in seen:
            continue
        point = start
        length = 0
        while point not in seen:
            seen.add(point)
            point = permutation[point]
            length += 1
        if length > 1:
            lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


def group_closure(generators: Iterable[Permutation]) -> set[Permutation]:
    generators = tuple(generators)
    result = {identity(len(generators[0]))}
    frontier = list(result)
    while frontier:
        element = frontier.pop()
        for generator in generators:
            product = compose(element, generator)
            if product not in result:
                result.add(product)
                frontier.append(product)
    return result


def common_fixed_points(generators: Iterable[Permutation]) -> int:
    group = group_closure(generators)
    return sum(
        all(element[point] == point for element in group)
        for point in range(len(next(iter(group))))
    )


def nontrivial_orbit_count(generators: Iterable[Permutation]) -> int:
    group = group_closure(generators)
    degree = len(next(iter(group)))
    remaining = set(range(degree))
    count = 0
    while remaining:
        point = min(remaining)
        orbit = {element[point] for element in group}
        if len(orbit) > 1:
            count += 1
        remaining -= orbit
    return count


def conjugate(conjugator: Permutation, element: Permutation) -> Permutation:
    return compose(compose(conjugator, element), inverse(conjugator))


def transitive(group: Iterable[Permutation]) -> bool:
    group = tuple(group)
    return len({element[0] for element in group}) == len(group[0])


def positive_control() -> dict:
    # Two adjacent transpositions generate the natural transitive S3.
    a = (1, 0, 2)
    b = (0, 2, 1)
    group = group_closure((a, b))
    if len(group) != 6 or not transitive(group):
        raise AssertionError("S3 closure/transitivity control failed")
    if power(compose(a, b), 3) != identity(3):
        raise AssertionError("A2 Coxeter relation control failed")
    return {"group": "S3", "degree": 3, "order": 6, "status": "PASS"}


def enumerate_h3() -> dict:
    degree = 6
    symmetric = list(itertools.permutations(range(degree)))
    double_transpositions = [
        permutation for permutation in symmetric if cycle_type(permutation) == (2, 2)
    ]
    a = double_transpositions[0]
    triples = []
    one = identity(degree)

    for b in double_transpositions:
        if power(compose(a, b), 3) != one:
            continue
        for c in double_transpositions:
            if power(compose(b, c), 5) != one:
                continue
            if power(compose(a, c), 2) != one:
                continue
            group = group_closure((a, b, c))
            if not transitive(group):
                continue
            staying = (
                common_fixed_points((a, b)),       # ordinary cusp
                common_fixed_points((b, c)),       # (2,5)-cusp
                common_fixed_points((a, c)),       # node
            )
            escaping_orbits = (
                nontrivial_orbit_count((a, b)),
                nontrivial_orbit_count((b, c)),
                nontrivial_orbit_count((a, c)),
            )
            triples.append((b, c, len(group), staying, escaping_orbits))

    centralizer = [
        z for z in symmetric if compose(z, a) == compose(a, z)
    ]
    remaining = {(b, c) for b, c, _, _, _ in triples}
    simultaneous_orbits = []
    while remaining:
        representative = min(remaining)
        orbit = {
            (conjugate(z, representative[0]), conjugate(z, representative[1]))
            for z in centralizer
        } & remaining
        simultaneous_orbits.append(orbit)
        remaining -= orbit

    records = {
        (order, staying, escaping)
        for _, _, order, staying, escaping in triples
    }
    if records != {(60, (0, 1, 0), (2, 1, 3))}:
        raise AssertionError(f"unexpected H3 records: {records}")
    if len(simultaneous_orbits) != 1:
        raise AssertionError("H3 representation is not unique up to conjugacy")

    # Irreducible target: two cusps plus one node, so k=4 and nu=1.
    fixed_per_meridian = 2
    branches_over_singularities = 4
    branch_excess = 1
    staying = next(iter(records))[1]
    escaping = next(iter(records))[2]
    euler_source = (
        degree * branch_excess
        + fixed_per_meridian * (1 - branches_over_singularities)
        + sum(staying)
    )
    moved_cycles_per_meridian = 2
    chi_r_coarse = (
        moved_cycles_per_meridian * (1 - branches_over_singularities)
        + sum(escaping)
    )
    if euler_source != 1 or chi_r_coarse != 0:
        raise AssertionError("H3 Euler replay failed")

    return {
        "degree": degree,
        "meridian_cycle_type": [2, 2, 1, 1],
        "conjugacy_class_size": len(double_transpositions),
        "labeled_triples_after_fixing_a": len(triples),
        "centralizer_size": len(centralizer),
        "simultaneous_conjugacy_orbits": len(simultaneous_orbits),
        "orbit_sizes": [len(orbit) for orbit in simultaneous_orbits],
        "generated_group_order": 60,
        "generated_group_identification": "A5 (order 60; inherited identification checked independently in GAP archive)",
        "staying_counts": {
            "ordinary_cusp": staying[0],
            "2_5_cusp": staying[1],
            "node": staying[2],
        },
        "escaping_local_orbit_counts": {
            "ordinary_cusp": escaping[0],
            "2_5_cusp": escaping[1],
            "node": escaping[2],
        },
        "source_euler": euler_source,
        "coarse_chi_R": chi_r_coarse,
        "verdict": "BLUEPRINT near-miss: Euler passes, R-line condition fails",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = {
        "evidence_label": "EXACT-Q",
        "positive_control": positive_control(),
        "h3": enumerate_h3(),
        "status": "PASS",
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
