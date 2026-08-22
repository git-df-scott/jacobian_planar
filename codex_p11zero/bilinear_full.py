#!/usr/bin/env python3
"""Build the full polynomial-Q pentagon target as a sparse bilinear system.

Unlike the 66-condition L23 export, this system keeps every supported Q
coefficient as an unknown and imposes the complete identity

    P_x Q_y - P_y Q_x = x^2.

The p_1_1=0 chart is substituted exactly.  Seven necessary nonzero quantities
are encoded by separate Rabinowitsch equations so the maximum degree remains
two.  A returned point is still a modular lead until independently verified and
lifted to characteristic zero.
"""

from __future__ import annotations

import argparse
import json
import random
from fractions import Fraction
from pathlib import Path

from pentagon_core import P_PARAMS, P_ROWS, Q_ROWS


Monomial = tuple[str, ...]
Polynomial = dict[Monomial, int]

P_FIXED = {(0, 0): 0, (0, 1): 1, (1, 1): 0}
Q_FIXED = {(0, 0): 1, (1, 0): 0, (1, 1): 0, (1, 2): 1}

P_VARIABLES = [f"p_{j}_{i}" for j, i in P_PARAMS if (j, i) not in P_FIXED]
Q_PARAMS = [(j, i) for j in sorted(Q_ROWS)
            for i in range(Q_ROWS[j][0], Q_ROWS[j][1] + 1)]
Q_VARIABLES = [f"q_{j}_{i}" for j, i in Q_PARAMS if (j, i) not in Q_FIXED]

NONZERO_TARGETS = (
    "p_1_0",                    # chart condition
    "p_8_0", "p_14_8", "p_16_8",
    "q_12_0", "q_21_12", "q_24_12",
)
SAT_VARIABLES = [f"sat_{name}" for name in NONZERO_TARGETS]
VARIABLES = P_VARIABLES + Q_VARIABLES + SAT_VARIABLES


def coefficient(prefix: str, key: tuple[int, int], fixed):
    if key in fixed:
        value = fixed[key]
        return {} if value == 0 else {(): value}
    j, i = key
    return {(f"{prefix}_{j}_{i}",): 1}


def add_term(poly: Polynomial, monomial: Monomial, value: int):
    monomial = tuple(sorted(monomial))
    poly[monomial] = poly.get(monomial, 0) + value
    if poly[monomial] == 0:
        del poly[monomial]


def multiply(a: Polynomial, b: Polynomial, scale: int = 1) -> Polynomial:
    out: Polynomial = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            add_term(out, ma + mb, scale * ca * cb)
    return out


def build_bracket_equations():
    """Return labelled coefficient equations for [P,Q]-x^2."""
    by_coordinate: dict[tuple[int, int], Polynomial] = {}
    for pj, pi in P_PARAMS:
        pc = coefficient("p", (pj, pi), P_FIXED)
        if not pc:
            continue
        for qj, qi in Q_PARAMS:
            qc = coefficient("q", (qj, qi), Q_FIXED)
            weight = pi * qj - pj * qi
            if not qc or weight == 0:
                continue
            coordinate = (pj + qj - 1, pi + qi - 1)
            poly = by_coordinate.setdefault(coordinate, {})
            for monomial, value in multiply(pc, qc, weight).items():
                add_term(poly, monomial, value)

    target = by_coordinate.setdefault((0, 2), {})
    add_term(target, (), -1)
    return [(f"bracket_y{j}_x{i}", poly)
            for (j, i), poly in sorted(by_coordinate.items()) if poly]


def build_saturation_equations():
    out = []
    for target in NONZERO_TARGETS:
        sat = f"sat_{target}"
        out.append((f"nonzero_{target}", {(sat, target): 1, (): -1}))
    return out


def build_system():
    bracket_equations = build_bracket_equations()
    saturation_equations = build_saturation_equations()
    return bracket_equations + saturation_equations, len(bracket_equations)


def crosscheck_case1(path: Path):
    """Compare symbolically with the independent 302-equation Q construction."""
    with path.open() as handle:
        source = json.load(handle)
    assert source["content_hash"] == (
        "49d28a2fd7ca72eb4064564d02084b2fab1612222d0c2c86b22ee1fe4702be9a")
    assert source["meta"]["SP_size"] == 61
    assert source["meta"]["SQ_size"] == 125
    assert len(source["equations"]) == 302

    fixed_old = {
        "c_0_0": 0, "c_1_0": 1, "c_1_1": 0,
        "d_0_0": 1, "d_0_1": 0, "d_1_1": 0, "d_2_1": 1,
    }

    def rename(old: str) -> str:
        prefix, i, j = old.split("_")
        return f"{'p' if prefix == 'c' else 'q'}_{j}_{i}"

    reduced = {}
    for equation in source["equations"]:
        x_degree, y_degree = equation["bracket_point"]
        poly: Polynomial = {}
        for factors, rational in equation["terms"]:
            coefficient_value = Fraction(*rational)
            monomial = []
            for old, exponent in factors:
                if old in fixed_old:
                    coefficient_value *= fixed_old[old] ** exponent
                else:
                    monomial.extend([rename(old)] * exponent)
            if coefficient_value:
                assert coefficient_value.denominator == 1
                add_term(poly, tuple(monomial), coefficient_value.numerator)
        if poly:
            reduced[(y_degree, x_degree)] = poly

    ours = {}
    for label, poly in build_bracket_equations():
        y_text, x_text = label.removeprefix("bracket_y").split("_x")
        ours[(int(y_text), int(x_text))] = poly
    assert reduced == ours
    print(f"PASS symbolic cross-check: 302 source equations reduce exactly to "
          f"{len(ours)} p_1_1=0 bracket equations")


def evaluate(poly: Polynomial, point: dict[str, int], prime: int) -> int:
    total = 0
    for monomial, coefficient_value in poly.items():
        term = coefficient_value % prime
        for variable in monomial:
            term = term * point.get(variable, 0) % prime
        total = (total + term) % prime
    return total


def format_polynomial(poly: Polynomial, prime: int) -> str:
    pieces = []
    for monomial, coefficient_value in sorted(poly.items()):
        coefficient_value %= prime
        if coefficient_value == 0:
            continue
        factor = "*".join(monomial) if monomial else "1"
        pieces.append(f"{coefficient_value}*{factor}")
    return "+".join(pieces) if pieces else "0"


def write_msolve(path: Path, prime: int):
    equations, _ = build_system()
    with path.open("w") as handle:
        handle.write(",".join(VARIABLES) + "\n")
        handle.write(str(prime) + "\n")
        handle.write(",\n".join(format_polynomial(poly, prime)
                                  for _, poly in equations) + "\n")


def run_controls(prime: int, case1_json: Path | None = None):
    equations, bracket_count = build_system()
    bracket_equations = equations[:bracket_count]
    saturation_equations = equations[bracket_count:]

    # Exact rational family member P=x+y and its polynomial Q, reduced mod p.
    degenerate = {variable: 0 for variable in VARIABLES}
    degenerate.update({
        "p_1_0": 1,
        "sat_p_1_0": 1,
        "q_2_1": 1,
        "q_3_0": pow(3, prime - 2, prime),
    })
    bracket_bad = [label for label, poly in bracket_equations
                   if evaluate(poly, degenerate, prime)]
    saturation_bad = [label for label, poly in saturation_equations
                      if evaluate(poly, degenerate, prime)]
    assert not bracket_bad, bracket_bad
    assert len(saturation_bad) == 6, saturation_bad
    print("PASS degenerate exact family member satisfies full polynomial bracket")
    print("PASS all-vertex saturation rejects it at six vanished vertices")

    perturbed = dict(degenerate)
    perturbed["q_2_1"] = 2
    negative_bad = [label for label, poly in bracket_equations
                    if evaluate(poly, perturbed, prime)]
    assert negative_bad
    print(f"PASS negative Q perturbation detected ({len(negative_bad)} residues)")

    rng = random.Random(20260822)
    planted_saturation = {variable: rng.randrange(prime)
                          for variable in VARIABLES}
    for target in NONZERO_TARGETS:
        planted_saturation[target] = rng.randrange(1, prime)
        planted_saturation[f"sat_{target}"] = pow(
            planted_saturation[target], prime - 2, prime)
    assert not any(evaluate(poly, planted_saturation, prime)
                   for _, poly in saturation_equations)
    planted_saturation["sat_p_16_8"] += 1
    assert evaluate(dict(saturation_equations)["nonzero_p_16_8"],
                    planted_saturation, prime)
    print("PASS planted saturation assignment and perturbed negative control")

    if case1_json is not None:
        crosscheck_case1(case1_json)

    term_count = sum(len(poly) for _, poly in equations)
    max_degree = max(len(monomial) for _, poly in equations for monomial in poly)
    print(f"PROFILE variables={len(VARIABLES)} equations={len(equations)} "
          f"bracket={bracket_count} saturation={len(saturation_equations)} "
          f"max_degree={max_degree} terms={term_count}")
    print("VERDICT: NO VERDICT")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, default=1000003)
    parser.add_argument("--write", type=Path)
    parser.add_argument(
        "--case1-json", type=Path,
        default=Path(__file__).resolve().parents[1] /
                "campaign/audit_tracks/trackA_system_case1.json")
    args = parser.parse_args()
    run_controls(args.prime, args.case1_json)
    if args.write:
        write_msolve(args.write, args.prime)
        print(f"WROTE {args.write}")


if __name__ == "__main__":
    main()
