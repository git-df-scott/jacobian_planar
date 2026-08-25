#!/usr/bin/env python3
"""Continue a genuine reduced degree-144 point toward the inverse-lift locus.

This is a numerical reconnaissance tool, never a verdict machine.  It starts
from a saved Q-drives point satisfying all 209 support equations, frees the two
generic shear parameters (lambda_2, lambda_3), fixes lambda_4=1, and increases
the weight of all 64 reverse-Laurent pole equations.  Fixed row scaling is used
only for conditioning.  Every stage prints the unscaled support and lift norms.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from math import comb

import numpy as np
from scipy.optimize import least_squares

from degree144_numeric import CASES, Search


class FastLift:
    """Precomputed generic-chart negative rows of the reverse Laurent map."""

    def __init__(self, supp):
        self.supp = list(supp)
        by_target = defaultdict(list)
        for col, (i, j) in enumerate(self.supp):
            # After phi4, expand
            # (y-l2*x^-2-l3*x^-3-x^-4)^j, then perform the final swap.
            for r in range(j + 1):
                left = j-r
                for a in range(left + 1):
                    for b in range(left-a + 1):
                        c = left-a-b
                        xp = 4*j-i-2*a-3*b-4*c
                        if xp >= 0:
                            continue
                        multinomial = comb(j, r)*comb(left, a)*comb(left-a, b)
                        coeff = multinomial * (-1 if left % 2 else 1)
                        by_target[(r, xp)].append((col, a, b, coeff))
        self.targets = sorted(by_target)
        self.rows = [by_target[t] for t in self.targets]

    def evaluate(self, coeffs, l2, l3):
        return self.matrix(l2, l3) @ coeffs

    def matrix(self, l2, l3):
        """Dense pole-coefficient matrix, rows=negative monomials."""
        p2 = [1]
        p3 = [1]
        max2 = max((a for row in self.rows for _, a, _, _ in row), default=0)
        max3 = max((b for row in self.rows for _, _, b, _ in row), default=0)
        for _ in range(max2): p2.append(p2[-1]*l2)
        for _ in range(max3): p3.append(p3[-1]*l3)
        out = np.zeros((len(self.rows), len(self.supp)), dtype=complex)
        for ri, row in enumerate(self.rows):
            for col, a, b, cc in row:
                out[ri, col] += cc*p2[a]*p3[b]
        return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", default="sol3/degree144_reduced_seed.npz")
    ap.add_argument("--nfev", type=int, default=3000)
    ap.add_argument("--weights", default="1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,1e-2,1e-1,1")
    ap.add_argument("--output", default="sol3/degree144_lift_continuation_best.npz")
    ns = ap.parse_args()

    data = next(c for c in CASES if c[0] == "Q-drives")
    support = Search(*data, pin_other=False, lift_chart=None)
    z0 = np.load(ns.seed)["z"].astype(complex)
    nsupp = len(support.evaluate(z0))
    fast = [FastLift(support.Dsupp), FastLift(support.Osupp)]

    # Independent implementation check against lift_x4.reverse through Search.
    slow = Search(*data, pin_other=False, lift_chart=(2, 3, 1))
    slow_all = slow.evaluate(z0)
    D0, O0 = support.solve_other(z0)
    def coeff_vector(rows, supp):
        return np.asarray([rows.get(j, np.zeros(0, complex))[i]
                           if i < len(rows.get(j, ())) else 0 for i, j in supp])
    fast_check = np.r_[fast[0].evaluate(coeff_vector(D0, support.Dsupp), 2, 3),
                       fast[1].evaluate(coeff_vector(O0, support.Osupp), 2, 3)]
    if not np.allclose(fast_check, slow_all[nsupp:], rtol=1e-12, atol=1e-10):
        raise RuntimeError("fast lift matrix disagrees with independent reverse()")
    print("FAST-LIFT CONTROL: PASS", flush=True)

    def split(q):
        z = q[:len(z0)].astype(complex)
        sr = support.evaluate(z).real
        D, O = support.solve_other(z)
        lr = np.r_[fast[0].evaluate(coeff_vector(D, support.Dsupp), q[-2], q[-1]),
                   fast[1].evaluate(coeff_vector(O, support.Osupp), q[-2], q[-1])]
        return sr, lr.real

    q = np.r_[z0.real, 0.0, 0.0]
    s0, l0 = split(q)
    # These scales are frozen at the seed.  They improve conditioning without
    # changing during optimization and cannot manufacture a small raw defect.
    lscale = np.maximum(1.0, np.abs(l0))
    print(f"seed support: n={len(s0)} norm={np.linalg.norm(s0):.12e} max={np.max(np.abs(s0)):.12e}", flush=True)
    print(f"seed lift:    n={len(l0)} norm={np.linalg.norm(l0):.12e} max={np.max(np.abs(l0)):.12e}", flush=True)

    for weight in map(float, ns.weights.split(',')):
        def fun(v):
            sr, lr = split(v)
            return np.r_[sr, weight * lr/lscale]

        ans = least_squares(fun, q, method="trf", x_scale="jac",
                            max_nfev=ns.nfev, ftol=1e-13, xtol=1e-13,
                            gtol=1e-13, verbose=0)
        q = ans.x
        sr, lr = split(q)
        z = q[:len(z0)].astype(complex)
        vertices = support.other_vertices(z)
        print(
            f"weight={weight:.1e} status={ans.status:2d} nfev={ans.nfev:5d} "
            f"support={np.linalg.norm(sr):.12e} support_max={np.max(np.abs(sr)):.12e} "
            f"lift={np.linalg.norm(lr):.12e} lift_max={np.max(np.abs(lr)):.12e} "
            f"lambdas=({q[-2]:.12g},{q[-1]:.12g},1) "
            f"vertices=({abs(vertices[0]):.6g},{abs(vertices[1]):.6g})",
            flush=True,
        )
        np.savez(ns.output, z=z, lambda2=q[-2], lambda3=q[-1],
                 support=sr, lift=lr, weight=weight)

    sr, lr = split(q)
    if np.linalg.norm(sr) < 1e-9 and np.linalg.norm(lr) < 1e-9:
        print("CANDIDATE-UNVERIFIED: simultaneous support/lift numerical hit")
    else:
        print("NO NUMERICAL INTERSECTION: no counterexample claim")


if __name__ == "__main__":
    main()
