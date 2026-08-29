#!/usr/bin/env python3
"""Dependency-free exact verifier for eigenfactor21.json."""

from fractions import Fraction as F
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def poly(d):
    return {tuple(map(int, k.split(","))): F(*v) for k, v in d.items() if v[0]}


def add(a, b, sb=F(1)):
    z = dict(a)
    for m, c in b.items():
        z[m] = z.get(m, F(0)) + sb*c
        if not z[m]:
            del z[m]
    return z


def mul(a, b):
    z = {}
    for (i, j), c in a.items():
        for (k, l), d in b.items():
            z[(i+k, j+l)] = z.get((i+k, j+l), F(0)) + c*d
    return {m: c for m, c in z.items() if c}


def power(a, n):
    z = {(0, 0): F(1)}
    for _ in range(n):
        z = mul(z, a)
    return z


def dx(a):
    return {(i-1, j): c*i for (i, j), c in a.items() if i}


def dy(a):
    return {(i, j-1): c*j for (i, j), c in a.items() if j}


def bracket(P, Q):
    return add(mul(dx(P), dy(Q)), mul(dy(P), dx(Q)), F(-1))


def main():
    with open(os.path.join(HERE, "eigenfactor21.json")) as f:
        data = json.load(f)
    nr = nt = 0
    seen = set()
    for rec in data["records"]:
        P = poly(rec["P"])
        key = tuple(sorted(P.items()))
        assert key not in seen
        seen.add(key)
        if rec["class"] == "reducible_Q":
            z = {(0, 0): F(*rec["constant"])}
            nonunits = 0
            for fac in rec["factors"]:
                f = poly(fac["poly"])
                assert f and max(sum(m) for m in f) > 0 and fac["exp"] > 0
                nonunits += fac["exp"]
                z = mul(z, power(f, fac["exp"]))
            assert nonunits >= 2 and z == P
            nr += 1
        elif rec["class"] == "triangular_coordinate":
            Q = poly(rec["Q"])
            assert bracket(P, Q) == {(0, 0): F(1)}
            nt += 1
        else:
            raise AssertionError(rec["class"])
    assert len(seen) == data["unique_P"]
    assert nr == data["reducible_Q_with_factor_witness"]
    assert nt == data["triangular_coordinates_with_mate"]
    assert nr + nt == len(seen) and data["unclassified"] == 0
    print("PASS: %d exact factor witnesses; %d exact coordinate mates; 0 unclassified" %
          (nr, nt))


if __name__ == "__main__":
    main()
