#!/usr/bin/env python3
"""Recheck every [P,A]=P hit for cancellation of A/P's vertical poles."""

from fractions import Fraction as F
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "night21"))
from pole21 import clean, add, scale, mul, D, ONE  # noqa: E402

TERM = re.compile(r"\(([-()0-9/]+)\)\*x\^(\d+)\*y\^(\d+)")


def parse(s):
    z = {}
    for a, i, j in TERM.findall(s):
        a = F(a.replace("(", "").replace(")", ""))
        z[(int(i), int(j))] = a
    return clean(z)


def lead(P):
    return max(P, key=lambda m: (sum(m), m[0], m[1]))


def divide(A, P):
    """Exact one-divisor multivariate division, graded lex order."""
    z, q, rem = dict(A), {}, {}
    mp, cp = lead(P), P[lead(P)]
    while z:
        m, c = lead(z), z[lead(z)]
        if m[0] >= mp[0] and m[1] >= mp[1]:
            d = (m[0]-mp[0], m[1]-mp[1])
            a = c/cp
            q[d] = q.get(d, F(0))+a
            z = add(z, scale(-a, {(i+d[0], j+d[1]): v for (i, j), v in P.items()}))
        else:
            rem[m] = c
            del z[m]
    return clean(q), clean(rem)


def cert_poly(d):
    return {tuple(map(int, k.split(","))): F(*v) for k, v in d.items() if v[0]}


def main():
    raw = json.load(open(os.path.join(ROOT, "night21", "eigensearch21.json")))
    fac = json.load(open(os.path.join(ROOT, "night21", "eigenfactor21.json")))
    certs = {tuple(sorted(cert_poly(r["P"]).items())): r for r in fac["records"]}
    counts = {"rows": 0, "relation_verified": 0, "pole_free_after_C(P)_shift": 0,
              "nonconstant_remainder": 0, "pole_free_coordinate_rows": 0,
              "reducible_rows_with_mismatch": 0,
              "reducible_rows_regular_on_some_component": 0,
              "reducible_rows_polar_on_every_component": 0,
              "absolute_component_distribution_unresolved": 0}
    survivors = []
    for row in raw["rows"]:
        counts["rows"] += 1
        P, A = parse(row["P"]), parse(row["A"])
        assert D(P, A) == P
        counts["relation_verified"] += 1
        Q, rem = divide(A, P)
        if not rem or set(rem) <= {(0, 0)}:
            a = rem.get((0, 0), F(0))
            assert add(A, scale(-1, {(0, 0): a}), scale(-1, mul(P, Q))) == {}
            assert D(P, Q) == ONE
            counts["pole_free_after_C(P)_shift"] += 1
            assert certs[tuple(sorted(P.items()))]["class"] == "triangular_coordinate"
            counts["pole_free_coordinate_rows"] += 1
            survivors.append({"P": row["P"], "A": row["A"], "constant": str(a)})
        else:
            counts["nonconstant_remainder"] += 1
            cert = certs[tuple(sorted(P.items()))]
            assert cert["class"] == "reducible_Q"
            counts["reducible_rows_with_mismatch"] += 1
            alphas = []
            unresolved = False
            for fr in cert["factors"]:
                assert fr["exp"] == 1  # unimodularity makes every fibre reduced
                f = cert_poly(fr["poly"])
                _, ar = divide(A, f)
                if ar and not set(ar) <= {(0, 0)}:
                    # This Q-irreducible factor can split geometrically; A may
                    # take conjugate constants on its absolute components.
                    unresolved = True
                else:
                    alphas.append(ar.get((0, 0), F(0)))
            if unresolved:
                counts["absolute_component_distribution_unresolved"] += 1
            if any(a == 0 for a in alphas):
                counts["reducible_rows_regular_on_some_component"] += 1
            elif not unresolved:
                counts["reducible_rows_polar_on_every_component"] += 1
    out = {"counts": counts, "pole_free_rows": survivors}
    with open(os.path.join(HERE, "eigenpole22.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print(counts)
    print("PASS: every relation re-expanded; every cancellation hit has [P,Q]=1")


if __name__ == "__main__":
    main()
