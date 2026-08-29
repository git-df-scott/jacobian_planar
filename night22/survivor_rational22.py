#!/usr/bin/env python3
"""Exact rational mates and pole mismatches for two night15 survivors."""

from fractions import Fraction as F
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "night21"))
from pole21 import clean, add, scale, mul, D, ONE  # noqa: E402


def power(a, n):
    z = ONE
    for _ in range(n):
        z = mul(z, a)
    return z


def dec(d):
    return {tuple(map(int, k.split(","))): F(*v) for k, v in d.items()}


def enc(P):
    return {"%d,%d" % m: [a.numerator, a.denominator] for m, a in sorted(P.items())}


def q(s):
    return F(s)


def main():
    rows = json.load(open(os.path.join(ROOT, "night15", "screen15_records.json")))
    chosen = [r for r in rows if r.get("outcome") == "PERIODS-VANISHING"
              and r["meta"].get("gen") == "G1" and r["meta"].get("n") == 1][:2]
    assert len(chosen) == 2
    out = []
    for r in chosen:
        P = dec(r["P"])
        m, c, h0, a = r["meta"]["m"], q(r["meta"]["c"]), q(r["meta"]["h0"]), q(r["meta"]["a"])
        v = {(0, 1): F(1)}
        for i, z in r["meta"]["t"].items():
            v[(int(i), 0)] = v.get((int(i), 0), F(0))+q(z)/2
        v = clean(v)
        B = power(v, m-1)
        A = {(0, 0): F(1, 1)/(c*(1-m))}
        # D(A/B)=1 iff D(A)B-A D(B)=B^2.
        numer = add(mul(D(P, A), B), scale(-1, mul(A, D(P, B))), scale(-1, mul(B, B)))
        assert not numer
        H = add({(0, 0): h0}, scale(c, mul(add({(1, 0): F(1)}, {(0, 0): -a}), B)))
        assert P == mul(v, H)
        alpha_v = h0**(m-1)/(c*(1-m))
        alpha_H = F(0)
        assert alpha_v != alpha_H
        out.append({
            "hash": r["hash"], "label": r["label"], "P": enc(P),
            "Q_numerator": enc(A), "Q_denominator": enc(B),
            "rational_identity_residual": enc(numer),
            "zero_fibre_factors": [enc(v), enc(H)],
            "pole_order_on_v_component": m-1,
            "principal_coefficients": [str(alpha_v), str(alpha_H)],
            "pole_mismatch": True,
        })
    with open(os.path.join(HERE, "survivor_rational22.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    for r in out:
        print(r["hash"], "PASS rational mate; pole coefficients",
              r["principal_coefficients"], "mismatch=True")


if __name__ == "__main__":
    main()
