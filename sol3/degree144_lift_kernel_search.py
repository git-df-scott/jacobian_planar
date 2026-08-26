#!/usr/bin/env python3
"""Search the degree-144 support/lift intersection in lift-kernel coordinates.

Unlike penalty continuation, reverse polynomiality is imposed identically:
for each (lambda_2, lambda_3, 1), both reduced polynomials are represented in
the numerical nullspaces of their complete Laurent-pole matrices.  The only
core residuals are the full coefficients of [D,O]-x^2. Two independent torus
gauges are eliminated exactly; the third driver vertex then equals the second
by the exact binomial right-edge identity. A numerical zero is still only a
CANDIDATE-UNVERIFIED and must be reconstructed and checked exactly.
"""
from __future__ import annotations

import argparse
from collections import defaultdict

import numpy as np
from scipy.optimize import least_squares
from scipy.linalg import qr

from degree144_numeric import CASES, Search
from degree144_lift_continuation import FastLift
from lift_x4 import bracket


def nullspace(matrix, expected):
    _, singular, vh = np.linalg.svd(matrix, full_matrices=True)
    tol = max(matrix.shape) * np.finfo(float).eps * singular[0]
    rank = int(np.sum(singular > tol))
    basis = vh[rank:].conj().T
    if basis.shape[1] != expected:
        raise ArithmeticError(f"lift nullity changed: {basis.shape[1]} != {expected}")
    return basis


def pivot_partition(matrix, rank):
    """Choose a fixed full-rank column chart for a matrix family."""
    _, r, order = qr(matrix, mode="economic", pivoting=True)
    tol = max(matrix.shape)*np.finfo(float).eps*abs(r[0, 0])
    if int(np.sum(np.abs(np.diag(r)) > tol)) != rank:
        raise ArithmeticError("reference pivot chart has the wrong rank")
    dependent = list(map(int, order[:rank]))
    free = [c for c in range(matrix.shape[1]) if c not in dependent]
    return dependent, free


def kernel_on_chart(matrix, dependent, free):
    """Smooth nullspace basis with the free-coordinate block equal to I."""
    x, _, rank, _ = np.linalg.lstsq(matrix[:, dependent], -matrix[:, free], rcond=None)
    if rank != len(dependent):
        raise ArithmeticError("lift pivot chart dropped rank")
    n = np.zeros((matrix.shape[1], len(free)), dtype=np.result_type(matrix, complex))
    n[dependent, :] = x
    n[free, :] = np.eye(len(free))
    if np.linalg.norm(matrix @ n) > 1e-7*(1+np.linalg.norm(matrix)):
        raise ArithmeticError("lift-kernel reconstruction failed")
    return n


class KernelSearch:
    def __init__(self):
        data = next(c for c in CASES if c[0] == "Q-drives")
        self.shape = Search(*data, pin_other=False, lift_chart=None)
        self.sd, self.so = self.shape.Dsupp, self.shape.Osupp
        self.fd, self.fo = FastLift(self.sd), FastLift(self.so)
        self.nd, self.no = 11, 7
        self.nd_free = self.nd-2
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
        self.row_scale = np.ones(len(self.targets))
        for row, _, _, multiplier in self.products:
            self.row_scale[row] += abs(multiplier)
        self.driver_gauges = [self.sd.index(v) for v in ((1, 0), (16, 12))]
        self.driver_vertices = [self.sd.index(v) for v in ((1, 0), (16, 12), (16, 16))]
        self.other_vertices = [self.so.index(v) for v in ((2, 1), (12, 9), (12, 12))]
        md0, mo0 = self.fd.matrix(.17, -.11), self.fo.matrix(.17, -.11)
        self.dd, self.df = pivot_partition(md0, 40)
        self.od, self.of = pivot_partition(mo0, 24)
        nd0 = kernel_on_chart(md0, self.dd, self.df)
        self.gd, self.gf = pivot_partition(nd0[self.driver_gauges, :], 2)

    def bracket_rows(self, d, o):
        r = np.zeros(len(self.targets), dtype=np.result_type(d, o))
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
        nd = kernel_on_chart(self.fd.matrix(l2, l3), self.dd, self.df)
        no = kernel_on_chart(self.fo.matrix(l2, l3), self.od, self.of)
        gauge_matrix = nd[self.driver_gauges, :]
        du = np.zeros(self.nd, dtype=np.result_type(q, complex))
        du[self.gf] = q[:self.nd_free]
        rhs = np.ones(2)-gauge_matrix[:, self.gf] @ du[self.gf]
        try:
            du[self.gd] = np.linalg.solve(gauge_matrix[:, self.gd], rhs)
        except np.linalg.LinAlgError:
            raise ArithmeticError("driver gauge chart dropped rank")
        offset = self.nd_free
        return nd @ du, no @ q[offset:offset+self.no], l2, l3

    def encode(self, d, o, l2, l3):
        """Put an existing lifted pair into the fixed smooth kernel chart."""
        nd = kernel_on_chart(self.fd.matrix(l2, l3), self.dd, self.df)
        no = kernel_on_chart(self.fo.matrix(l2, l3), self.od, self.of)
        # Centre the fixed gauge chart at the continuation seed; a chart chosen
        # at unrelated shears can be full-rank but catastrophically conditioned.
        self.gd, self.gf = pivot_partition(nd[self.driver_gauges, :], 2)
        du, _, rd, _ = np.linalg.lstsq(nd, d, rcond=None)
        ou, _, ro, _ = np.linalg.lstsq(no, o, rcond=None)
        if rd != self.nd or ro != self.no:
            raise ArithmeticError("could not encode lifted pair")
        q = np.r_[du[self.gf], ou, l2, l3]
        dd, oo, _, _ = self.decode(q)
        if np.linalg.norm(dd-d)+np.linalg.norm(oo-o) > 1e-7:
            raise ArithmeticError("encoded pair does not replay")
        return q

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
        barrier = 0.01/np.sqrt(np.abs(v)**2+1e-8)
        return np.r_[core.real/self.row_scale, barrier]

    def residual_complex(self, x):
        n = self.nd_free+self.no+2
        q = x[:n]+1j*x[n:]
        try:
            _, o, _, _ = self.decode(q)
            core = self.core(q)
        except (ArithmeticError, np.linalg.LinAlgError):
            return np.ones(2*len(self.targets)+3)*1e3
        v = o[self.other_vertices]
        barrier = 0.01/np.sqrt(np.abs(v)**2+1e-8)
        return np.r_[core.real/self.row_scale, core.imag/self.row_scale, barrier]

    def residual_complex_unscaled(self, x):
        n = self.nd_free+self.no+2
        q = x[:n]+1j*x[n:]
        try:
            _, o, _, _ = self.decode(q)
            core = self.core(q)
        except (ArithmeticError, np.linalg.LinAlgError):
            return np.ones(2*len(self.targets)+3)*1e3
        v = o[self.other_vertices]
        barrier = 0.01/np.sqrt(np.abs(v)**2+1e-8)
        return np.r_[core.real, core.imag, barrier]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=20)
    ap.add_argument("--nfev", type=int, default=1200)
    ap.add_argument("--seed", type=int, default=5144)
    ap.add_argument("--output", default="sol3/degree144_lift_kernel_best_corrected.npz")
    ap.add_argument("--complex", action="store_true",
                    help="search all complex coefficients and complex shears")
    ap.add_argument("--initial", help="npz lifted pair used as a continuation seed")
    ap.add_argument("--unscaled", action="store_true",
                    help="optimize raw bracket rows instead of conditioned rows")
    ns = ap.parse_args()
    rng = np.random.default_rng(ns.seed)
    search = KernelSearch()
    search.control()
    print("CONTROLS: lift nullspaces and independent bracket builder PASS", flush=True)
    print(f"lift-kernel dimensions: driver={search.nd} (free after gauges={search.nd_free}), "
          f"other={search.no}; "
          f"full bracket rows={len(search.targets)}", flush=True)
    best = (np.inf, None)
    initial = None
    if ns.initial:
        saved = np.load(ns.initial)
        initial = search.encode(saved["driver"], saved["other"],
                                saved["lambda2"].item(), saved["lambda3"].item())
        print(f"INITIAL REPLAY: raw={np.linalg.norm(search.core(initial)):.12e}", flush=True)
    for trial in range(ns.trials):
        n = search.nd_free+search.no+2
        if ns.complex:
            if initial is None:
                q0 = rng.normal(scale=.25, size=n)+1j*rng.normal(scale=.25, size=n)
                q0[-2:] = rng.normal(scale=.1, size=2)+1j*rng.normal(scale=.1, size=2)
            else:
                scale = 10**(-2-trial/4)
                q0 = initial + scale*(rng.normal(size=n)+1j*rng.normal(size=n))
            x0 = np.r_[q0.real, q0.imag]
            fun = search.residual_complex_unscaled if ns.unscaled else search.residual_complex
        else:
            q0 = rng.normal(scale=.25, size=n)
            q0[-2:] = rng.normal(scale=.1, size=2)
            x0 = q0
            fun = search.residual
        ans = least_squares(fun, x0, method="trf", x_scale="jac",
                            max_nfev=ns.nfev, ftol=1e-13, xtol=1e-13, gtol=1e-13)
        q = ans.x[:n]+1j*ans.x[n:] if ns.complex else ans.x
        raw = search.core(q)
        val = float(np.linalg.norm(raw))
        d, o, l2, l3 = search.decode(q)
        verts = np.abs(o[search.other_vertices])
        if val < best[0]:
            best = (val, q.copy())
            np.savez(ns.output, q=q, driver=d, other=o, raw=raw,
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
