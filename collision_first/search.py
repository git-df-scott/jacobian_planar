#!/usr/bin/env python3
"""Complex collision-first search in original polynomial coordinates.

Both P and Q vanish at (0,0) and (1,0) identically in the parameterization.
The only residual is every coefficient of [P,Q]-1.  One P coefficient is fixed
to remove the P -> cP, Q -> c^-1Q symmetry.  Numerical zeros remain
CANDIDATE-UNVERIFIED until exact algebraic reconstruction.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass

import numpy as np
from scipy.optimize import least_squares

from incidence import Incidence, weighted_triangle


@dataclass
class CollisionCoordinates:
    support: list
    pivot: tuple
    free: list
    basis: np.ndarray
    fixed: np.ndarray

    @classmethod
    def create(cls, support, gauge=None):
        support = sorted(set(support))
        if (0, 0) not in support:
            raise ValueError("collision support needs (0,0)")
        bottom = sorted((i, j) for i, j in support if j == 0 and i > 0)
        if not bottom:
            raise ValueError("collision support needs a positive bottom row")
        pivot = bottom[-1]
        excluded = {(0, 0), pivot}
        fixed = np.zeros(len(support), dtype=complex)
        if gauge is not None:
            if gauge in excluded or gauge not in support:
                raise ValueError("invalid gauge monomial")
            excluded.add(gauge)
            fixed[support.index(gauge)] = 1
        free = [monomial for monomial in support if monomial not in excluded]
        basis = np.zeros((len(support), len(free)), dtype=complex)
        for column, monomial in enumerate(free):
            basis[support.index(monomial), column] = 1
            if monomial[1] == 0:
                basis[support.index(pivot), column] = -1
        # A y-positive gauge vanishes at both normalized collision points and
        # therefore does not alter the bottom-row pivot relation.
        return cls(support, pivot, free, basis, fixed)

    def decode(self, values):
        return self.fixed+self.basis@values


class Search:
    def __init__(self, p_support, q_support, p_gauge):
        self.incidence = Incidence.create(p_support, q_support)
        self.pc = CollisionCoordinates.create(self.incidence.p_support, p_gauge)
        self.qc = CollisionCoordinates.create(self.incidence.q_support)
        self.np = len(self.pc.free)
        self.nq = len(self.qc.free)
        self.nt = len(self.incidence.targets)
        self.target_index = {target: row for row, target in enumerate(self.incidence.targets)}
        self.x0 = self.target_index[(0, 0)]
        self.tensor = []
        p_index = {m: i for i, m in enumerate(self.incidence.p_support)}
        q_index = {m: i for i, m in enumerate(self.incidence.q_support)}
        for pm in self.incidence.p_support:
            i, j = pm
            for qm in self.incidence.q_support:
                k, ell = qm
                multiplier = i*ell-j*k
                if multiplier:
                    target = (i+k-1, j+ell-1)
                    self.tensor.append((self.target_index[target], p_index[pm],
                                        q_index[qm], multiplier))
        self.row_scale = np.ones(self.nt)
        for row, _, _, multiplier in self.tensor:
            self.row_scale[row] += abs(multiplier)

    def decode(self, z):
        return self.pc.decode(z[:self.np]), self.qc.decode(z[self.np:])

    def core(self, z):
        p, q = self.decode(z)
        residual = np.zeros(self.nt, dtype=complex)
        residual[self.x0] = -1
        for row, i, j, multiplier in self.tensor:
            residual[row] += multiplier*p[i]*q[j]
        return residual

    def jacobian_complex(self, z):
        p, q = self.decode(z)
        jacobian = np.zeros((self.nt, self.np+self.nq), dtype=complex)
        for row, i, j, multiplier in self.tensor:
            jacobian[row, :self.np] += multiplier*q[j]*self.pc.basis[i]
            jacobian[row, self.np:] += multiplier*p[i]*self.qc.basis[j]
        return jacobian

    def residual_real(self, x):
        n = self.np+self.nq
        z = x[:n]+1j*x[n:]
        residual = self.core(z)/self.row_scale
        return np.r_[residual.real, residual.imag]

    def jacobian_real(self, x):
        n = self.np+self.nq
        jacobian = self.jacobian_complex(x[:n]+1j*x[n:])/self.row_scale[:, None]
        return np.block([[jacobian.real, -jacobian.imag],
                         [jacobian.imag, jacobian.real]])

    def control(self):
        rng = np.random.default_rng(144)
        n = self.np+self.nq
        z = rng.normal(size=n)+1j*rng.normal(size=n)
        direction = rng.normal(size=n)+1j*rng.normal(size=n)
        eps = 1e-7
        finite = (self.core(z+eps*direction)-self.core(z-eps*direction))/(2*eps)
        analytic = self.jacobian_complex(z)@direction
        error = np.linalg.norm(finite-analytic)/(1+np.linalg.norm(analytic))
        if error > 1e-7:
            raise AssertionError(f"analytic Jacobian control failed: {error}")
        p, q = self.decode(z)
        for coefficients, coordinates in ((p, self.pc), (q, self.qc)):
            polynomial = dict(zip(coordinates.support, coefficients))
            assert abs(sum(value for (i, j), value in polynomial.items() if j == 0)) < 1e-10
            assert abs(polynomial.get((0, 0), 0)) < 1e-10


TEMPLATES = {
    "ribbon12": (12, 2, 18, 3),
    "ribbon24": (24, 2, 36, 3),
    "ribbon42": (42, 2, 63, 3),
    "frontier126": (84, 2, 126, 3),
    "frontier126_46": (84, 4, 126, 6),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", choices=TEMPLATES, default="ribbon12")
    parser.add_argument("--trials", type=int, default=8)
    parser.add_argument("--nfev", type=int, default=1500)
    parser.add_argument("--seed", type=int, default=25144)
    parser.add_argument("--output", default="collision_first/best.npz")
    parser.add_argument("--initial", help="continue from a saved npz search point")
    parser.add_argument("--method", choices=("trf", "lm"), default="trf")
    parser.add_argument("--lsmr", action="store_true",
                        help="use the iterative trust-region linear solver")
    ns = parser.parse_args()
    px, py, qx, qy = TEMPLATES[ns.template]
    p_support = weighted_triangle(px, py)
    q_support = weighted_triangle(qx, qy)
    search = Search(p_support, q_support, (0, py))
    search.control()
    print("CONTROLS: collision coordinates and analytic Jacobian PASS", flush=True)
    print(f"template={ns.template} P={len(p_support)} coeff/{search.np} free "
          f"Q={len(q_support)} coeff/{search.nq} free bracket={search.nt} rows",
          flush=True)
    rng = np.random.default_rng(ns.seed)
    n = search.np+search.nq
    best = (np.inf, None)
    initial = None
    if ns.initial:
        saved = np.load(ns.initial)
        if str(saved["template"]) != ns.template:
            raise ValueError("initial point uses a different template")
        initial = saved["z"]
        print(f"INITIAL REPLAY: raw={np.linalg.norm(search.core(initial)):.12e}", flush=True)
    for trial in range(ns.trials):
        if initial is None:
            z0 = .1*(rng.normal(size=n)+1j*rng.normal(size=n))
        else:
            scale = 10**(-4-trial/2)
            z0 = initial+scale*(rng.normal(size=n)+1j*rng.normal(size=n))
        x0 = np.r_[z0.real, z0.imag]
        options = {"tr_solver": "lsmr"} if ns.lsmr and ns.method == "trf" else {}
        answer = least_squares(search.residual_real, x0, jac=search.jacobian_real,
                               method=ns.method, x_scale="jac", max_nfev=ns.nfev,
                               ftol=1e-13, xtol=1e-13, gtol=1e-13, **options)
        z = answer.x[:n]+1j*answer.x[n:]
        raw = search.core(z)
        norm = float(np.linalg.norm(raw))
        p, q = search.decode(z)
        if norm < best[0]:
            best = (norm, z.copy())
            np.savez(ns.output, z=z, p=p, q=q, raw=raw,
                     p_support=np.asarray(p_support), q_support=np.asarray(q_support),
                     template=ns.template)
        vertices = [abs(q[search.qc.support.index(m)])
                    for m in ((0, qy), (qx, 0)) if m in search.qc.support]
        print(f"trial={trial:3d} raw={norm:.12e} max={np.max(np.abs(raw)):.12e} "
              f"q_vertices={vertices} status={answer.status} nfev={answer.nfev}",
              flush=True)
    if not ns.trials:
        print("NO SEARCH REQUESTED")
    elif best[0] < 1e-9:
        print("CANDIDATE-UNVERIFIED: exact reconstruction required")
    else:
        print(f"NO NUMERICAL HIT: best raw residual {best[0]:.12e}")


if __name__ == "__main__":
    main()
