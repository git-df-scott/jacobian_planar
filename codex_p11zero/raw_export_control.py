#!/usr/bin/env python3
"""Independently compare the recurrence with the 43 MB exported system."""

import random
import sys

from pentagon_core import VARS, exported_conditions, recur_q


def eval_term(term, points, prime):
    vals = [1] * len(points)
    for factor in term.split("*"):
        factor = factor.strip()
        if not factor:
            continue
        if factor.isdigit():
            base, exponent = int(factor), 1
            for k in range(len(vals)):
                vals[k] = vals[k] * base % prime
            continue
        if "^" in factor:
            name, power = factor.split("^", 1)
            exponent = int(power)
        else:
            name, exponent = factor, 1
        for k, point in enumerate(points):
            vals[k] = vals[k] * pow(point[name], exponent, prime) % prime
    return vals


def eval_poly(poly, points, prime):
    totals = [0] * len(points)
    for signed in poly.replace("-", "+-").split("+"):
        signed = signed.strip()
        if not signed:
            continue
        negative = signed.startswith("-")
        term = signed[1:] if negative else signed
        values = eval_term(term, points, prime)
        for k, value in enumerate(values):
            totals[k] = (totals[k] - value if negative else totals[k] + value) % prime
    return totals


def main(path):
    with open(path) as handle:
        names = [x.strip() for x in handle.readline().split(",")]
        prime = int(handle.readline().strip())
        if names != VARS:
            raise AssertionError(f"variable mismatch: export={len(names)}, core={len(VARS)}")

        rng = random.Random(20260822)
        generic = {name: rng.randrange(prime) for name in VARS}
        chart = {name: rng.randrange(prime) for name in VARS}
        chart["p_1_1"] = 0
        chart["p_1_0"] = 1
        degenerate = {name: 0 for name in VARS}
        degenerate["p_1_0"] = 1
        points = [generic, chart, degenerate]
        raw = [[] for _ in points]
        for line in handle:
            poly = line.strip().rstrip(",")
            if not poly:
                continue
            values = eval_poly(poly, points, prime)
            for k, value in enumerate(values):
                raw[k].append(value)

    core = []
    for point in points:
        _, q = recur_q(point, prime)
        core.append(exported_conditions(q, prime))

    if any(len(row) != 66 for row in raw):
        raise AssertionError(f"expected 66 exported polynomials, got {[len(x) for x in raw]}")
    matches = [sum(a == b for a, b in zip(raw[k], core[k]))
               for k in range(len(points))]
    print(f"POS generic point: {matches[0]}/66 exact matches")
    print(f"POS p_1_1=0 chart point: {matches[1]}/66 exact matches")
    print(f"POS degenerate rational witness: {matches[2]}/66 exact matches, "
          f"raw_zero={not any(raw[2])}")
    if matches != [66, 66, 66] or any(raw[2]):
        return 1

    # Negative control: compare the raw generic evaluation to a deliberately
    # perturbed mathematical point.  The comparison must notice the mismatch.
    perturbed = dict(generic)
    perturbed["p_2_0"] = (perturbed["p_2_0"] + 1) % prime
    _, qbad = recur_q(perturbed, prime)
    bad = exported_conditions(qbad, prime)
    mismatch = sum(a != b for a, b in zip(raw[0], bad))
    print(f"NEG perturbed point: {mismatch}/66 mismatches detected")
    if mismatch == 0:
        return 1
    print("CONTROL: PASS")
    print("VERDICT: NO VERDICT")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "wave1/pent_L23.ms"))
