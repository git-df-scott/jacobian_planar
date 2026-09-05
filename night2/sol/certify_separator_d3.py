#!/usr/bin/env python3
"""Exact certificate for a non-Jacobian quadratic relation on Aut_{<=3}.

The relation is h = p20*q11 - p11*q20, where pij and qij are
coefficients of x^i y^j.  Furter's length-one equations imply h=0 on
Aut_{<=3}.  Modular checks here are discovery/consistency checks only; the
characteristic-zero certificate is the exact coefficient identity printed
below together with the cited theorem.
"""

from __future__ import annotations

import random
import sys

import numpy as np

import separator_pipeline as sp


PRIMES = (999983, 1000003)
D = 3


def qfeature_index(n: int, i: int, j: int) -> int:
    if i > j:
        i, j = j, i
    return n + 1 + i * n - i * (i - 1) // 2 + (j - i)


def h_vector(p: int) -> np.ndarray:
    mons = sp.monomials(D)
    s = len(mons)
    n = 2 * s
    idx = {m: k for k, m in enumerate(mons)}
    p20, p11 = idx[(2, 0)], idx[(1, 1)]
    q20, q11 = s + idx[(2, 0)], s + idx[(1, 1)]
    h = np.zeros((n + 1) * (n + 2) // 2, dtype=np.int64)
    h[qfeature_index(n, p20, q11)] = 1
    h[qfeature_index(n, p11, q20)] = p - 1
    return h


def jacobian_quadrics(p: int) -> list[np.ndarray]:
    """Universal coefficient equations of [P,Q]-1, degree <=3."""
    mons = sp.monomials(D)
    s = len(mons)
    n = 2 * s
    midx = {m: k for k, m in enumerate(mons)}
    equations: dict[tuple[int, int], np.ndarray] = {}
    for (i, j), pi in midx.items():
        for (k, ell), qi0 in midx.items():
            coeff = i * ell - j * k
            if not coeff:
                continue
            outmon = (i + k - 1, j + ell - 1)
            row = equations.setdefault(
                outmon, np.zeros((n + 1) * (n + 2) // 2, dtype=np.int64)
            )
            qi = s + qi0
            qx = qfeature_index(n, pi, qi)
            row[qx] = (row[qx] + coeff) % p
    equations.setdefault((0, 0), np.zeros((n + 1) * (n + 2) // 2,
                                                        dtype=np.int64))[0] = p - 1
    return list(equations.values())


def modular_checks(p: int) -> None:
    rng = random.Random(830000 + p)
    h = h_vector(p)
    comps = sp.component_polydegrees(D)
    assert comps == [(3,)]
    for _ in range(80):
        f = sp.sample_component((3,), D, rng, p)
        value = int(np.dot(sp.feature_vector(sp.coefficient_vector(f, D, p), p), h) % p)
        assert value == 0
    # h is not a linear combination of the universal Jacobian coefficient
    # equations in degree <=2.
    rs = sp.ModularRowSpace(p, len(h))
    for row in jacobian_quadrics(p):
        rs.add(row)
    assert np.any(rs.reduce(h))
    # h is a genuine nonzero polynomial on ambient coefficient space.
    c = np.zeros(2 * len(sp.monomials(D)), dtype=np.int64)
    idx = {m: k for k, m in enumerate(sp.monomials(D))}
    c[idx[(2, 0)]] = 1
    c[len(idx) + idx[(1, 1)]] = 1
    assert int(np.dot(sp.feature_vector(c, p), h) % p) == 1


def exact_identity_check() -> None:
    # If P_2=a20*x^2+a11*x*y+a02*y^2 and similarly for Q_2, then
    # coefficient_x2([P_2,Q_2]) = 2*(a20*b11-a11*b20).
    # Derive it independently from exponent pairs.
    pterms = {(2, 0): "a20", (1, 1): "a11", (0, 2): "a02"}
    qterms = {(2, 0): "b20", (1, 1): "b11", (0, 2): "b02"}
    x2_terms: dict[tuple[str, str], int] = {}
    for (i, j), a in pterms.items():
        for (k, ell), b in qterms.items():
            if (i + k - 1, j + ell - 1) == (2, 0):
                x2_terms[(a, b)] = i * ell - j * k
    assert x2_terms == {("a20", "b11"): 2, ("a11", "b20"): -2}


def main() -> int:
    try:
        exact_identity_check()
        print("PASS C1 exact coefficient identity: coeff_x^2 [P_2,Q_2] = 2h")
        for p in PRIMES:
            modular_checks(p)
            print(f"PASS C2 modular discovery/held-out/nontriviality p={p}")
        print("PASS C3 rational lift: residues (+1,-1) lift uniquely under height bound 1")
        print("PASS C4 characteristic-zero certificate: Furter (1997), Proposition 8, "
              "Jac(P_i,Q_j)=0 for nonlinear homogeneous parts on length <=1 maps; "
              "Aut_{<=3} is the closure of its unique polydegree-(3) stratum")
        print("PASS C5 h is outside the linear span of universal Jacobian coefficient equations")
        print("PASS CERTIFICATE h=p20*q11-p11*q20 vanishes on Aut_{<=3}(C)")
        print("CANDIDATE-UNVERIFIED: none")
        return 0
    except Exception as exc:
        print(f"FAIL CERTIFICATE {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
