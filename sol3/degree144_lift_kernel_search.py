#!/usr/bin/env python3
"""Search the degree-144 support/lift intersection in lift-kernel coordinates.

Unlike penalty continuation, reverse polynomiality is imposed identically:
for each (lambda_2, lambda_3, 1), both reduced polynomials are represented in
the numerical nullspaces of their complete Laurent-pole matrices.  The only
core residuals are the full coefficients of [D,O]-x^2 and three legitimate
torus gauges on the nonzero driver vertices.  A numerical zero is still only a
CANDIDATE-UNVERIFIED and must be reconstructed and checked exactly.
"""
from __future__ import annotations

import argparse
from collections import defaultdict

import numpy as np
from scipy.optimize import least_squares

from degree144_numeric import CASES, Search
from degree144_lift_continuation import FastLift
from lift_x4 import bracket


def nullspace(matrix, expected):
    _, singular, vh = np.linalg.svd(matrix, full_matrices=True)
    tol = max(matrix.shape) * np.finfo(float).eps * singular[0]
    rank = int(np.sum(singular > tol))
    basis = vh[rank:].T
    if basis.shape[1] != expected:
        raise ArithmeticError(f"lift nullity changed: {basis.shape[1]} != {expected}")
    return basis


class KernelSearch:
    def __init__(self):
        data = next(c for c in CASES if c[0] == "Q-drives")
        self.shape = Search(*data, pin_other=False, lift_chart=None)
        self.sd, self.so = self.shape.Dsupp, self.shape.Osupp
        self.fd, self.fo = FastLift(self.sd), FastLift(self.so)
        self.nd, self.no = 11, 7
        self.nd_free = self.nd-3
        targets = {(2, 0)}
        self.products = []
        for a, (i, j) in enumerate(self.sd):
            for b, (k, ell) in enumerate(self.so):
                multiplier = i*ell-j*k
                if multiplier:
                    target = (i+k-1, j+ell-1)
                    targets.add(target)
                    self.products.append((target, a, b, multiplier))
        self.targets = sorted(targets)
        self.target_index = {m: n for n, m in enumerate(self.targets)}
        self.products = [(self.target_index[t], a, b, m)
                         for t, a, b, m in self.products]
        self.x2row = self.target_index[(2, 0)]
        self.driver_gauges = [self.sd.index(v) for v in ((1, 0), (16, 12), (16, 16))]
        self.other_vertices = [self.so.index(v) for v in ((2, 1), (12, 9), (12, 12))]

    def bracket_rows(self, d, o):
        r = np.zeros(len(self.targets))
        r[self.x2row] = -1
        for row, a, b, multiplier in self.products:
            r[row] += multiplier*d[a]*o[b]
        return r

    def control(self):
        l2, l3 = .2, -.1
        md, mo = self.fd.matrix(l2, l3).real, self.fo.matrix(l2, l3).real
        nd, no = nullspace(md, self.nd), nullspace(mo, self.no)
        assert np.linalg.norm(md @ nd) < 1e-9
        assert np.linalg.norm(mo @ no) < 1e-9
        rng = np.random.default_rng(144)
        d, o = rng.normal(size=len(self.sd)), rng.normal(size=len(self.so))
        direct = bracket(dict(zip(self.sd, d)), dict(zip(self.so, o)))
        direct[(2, 0)] = direct.get((2, 0), 0)-1
        tensor = self.bracket_rows(d, o)
        assert np.allclose(tensor, [direct.get(t, 0) for t in self.targets])

    def decode(self, q):
        l2, l3 = q[-2:]
        nd = nullspace(self.fd.matrix(l2, l3).real, self.nd)
        no = nullspace(self.fo.matrix(l2, l3).real, self.no)
        gauge_matrix = nd[self.driver_gauges, :]
        particular, _, rank, _ = np.linalg.lstsq(gauge_matrix, np.ones(3), rcond=None)
        if rank != 3:
            raise ArithmeticError("driver gauge rank dropped")
        gauge_kernel = nullspace(gauge_matrix, self.nd_free)
        du = particular + gauge_kernel @ q[:self.nd_free]
        offset = self.nd_free
        return nd @ du, no @ q[offset:offset+self.no], l2, l3

    def core(self, q):
        d, o, _, _ = self.decode(q)
        r = self.bracket_rows(d, o)
        return r

    def residual(self, q):
        try:
            d, o, _, _ = self.decode(q)
            core = self.core(q)
        except (ArithmeticError, np.linalg.LinAlgError):
            return np.ones(len(self.targets)+3)*1e3
        # Barrier is reconnaissance-only; it prevents attraction to a boundary
        # that deletes a required vertex.  It is excluded from the raw verdict.
        v = o[self.other_vertices]
        barrier = 0.01/np.sqrt(v*v+1e-8)
        return np.r_[core, barrier]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=20)
    ap.add_argument("--nfev", type=int, default=1200)
    ap.add_argument("--seed", type=int, default=5144)
    ap.add_argument("--output", default="sol3/degree144_lift_kernel_best.npz")
    ns = ap.parse_args()
    rng = np.random.default_rng(ns.seed)
    search = KernelSearch()
    search.control()
    print("CONTROLS: lift nullspaces and independent bracket builder PASS", flush=True)
    print(f"lift-kernel dimensions: driver={search.nd} (free after gauges={search.nd_free}), "
          f"other={search.no}; "
          f"full bracket rows={len(search.targets)}", flush=True)
    best = (np.inf, None)
    for trial in range(ns.trials):
        q0 = rng.normal(scale=.25, size=search.nd_free+search.no+2)
        q0[-2:] = rng.normal(scale=.1, size=2)
        ans = least_squares(search.residual, q0, method="trf", x_scale="jac",
                            max_nfev=ns.nfev, ftol=1e-13, xtol=1e-13, gtol=1e-13)
        raw = search.core(ans.x)
        val = float(np.linalg.norm(raw))
        d, o, l2, l3 = search.decode(ans.x)
        verts = np.abs(o[search.other_vertices])
        if val < best[0]:
            best = (val, ans.x.copy())
            np.savez(ns.output, q=ans.x, driver=d, other=o, raw=raw,
                     lambda2=l2, lambda3=l3, vertices=verts)
        print(f"trial={trial:3d} raw={val:.12e} raw_max={np.max(np.abs(raw)):.12e} "
              f"lift=(exact-kernel) lambdas=({l2:.7g},{l3:.7g},1) "
              f"other_vertices={verts.tolist()}", flush=True)
    if best[0] < 1e-9:
        print("CANDIDATE-UNVERIFIED: support/lift intersection; exact replay required")
    else:
        print(f"NO NUMERICAL HIT: best raw residual {best[0]:.12e}")


if __name__ == "__main__":
    main()
