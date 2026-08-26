#!/usr/bin/env python3
"""Lane 7: fast exact F_p engine around collision_first/incidence.py.

Adds, on top of the (unmodified) incidence.py engine:
  * a vectorised mod-p RREF so a sweep is feasible,
  * a split of the linear system into  bracket-only  vs  bracket+collision,
  * the collision functional  delta(Q) = Q(1,0) - Q(0,0)  and its invariance,
  * a bottom-row (y=0 restriction) sub-block used as a cheap necessary test,
  * an INDEPENDENT sympy bracket used only to replay claimed solutions.
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

import numpy as np
import sympy as sp

from incidence import (Incidence, bracket, collision_polynomial, value_at,
                       weighted_triangle)

Monomial = Tuple[int, int]
Polynomial = Dict[Monomial, int]

_X, _Y = sp.symbols("x y")


# ----------------------------------------------------------------- mod-p LA

def rref_mod(M: np.ndarray, p: int):
    """In-place RREF of an int64 matrix over F_p.  Returns (M, pivot columns)."""
    M = np.ascontiguousarray(M % p)
    m, n = M.shape
    pivots: List[int] = []
    r = 0
    for c in range(n):
        if r >= m:
            break
        nz = np.nonzero(M[r:, c])[0]
        if nz.size == 0:
            continue
        i = r + int(nz[0])
        if i != r:
            M[[r, i]] = M[[i, r]]
        inv = pow(int(M[r, c]), p - 2, p)
        M[r] = (M[r] * inv) % p
        col = M[:, c].copy()
        col[r] = 0
        rows = np.nonzero(col)[0]
        if rows.size:
            M[rows] = (M[rows] - np.outer(col[rows], M[r])) % p
        pivots.append(c)
        r += 1
    return M, pivots


def solve_mod(A: np.ndarray, b: np.ndarray, p: int, want_kernel: bool = True):
    """Solve A z = b over F_p.

    Returns dict with keys rank, nullity, consistent, particular, kernel.
    The rank reported is rank(A) (not of the augmented matrix).
    """
    m, n = A.shape
    aug = np.concatenate([A % p, (b % p).reshape(m, 1)], axis=1)
    rr, piv_all = rref_mod(aug, p)
    consistent = n not in piv_all
    pivots = [c for c in piv_all if c < n]
    rank = len(pivots)
    out = {"rank": rank, "nullity": n - rank, "consistent": consistent,
           "particular": None, "kernel": None}
    if not consistent:
        return out
    particular = np.zeros(n, dtype=np.int64)
    for row, c in enumerate(pivots):
        particular[c] = rr[row, n]
    out["particular"] = particular
    if want_kernel:
        free = [c for c in range(n) if c not in set(pivots)]
        K = np.zeros((len(free), n), dtype=np.int64)
        for t, fc in enumerate(free):
            K[t, fc] = 1
            for row, c in enumerate(pivots):
                K[t, c] = (-int(rr[row, fc])) % p
        out["kernel"] = K
    return out


# ------------------------------------------------------------- template box

@dataclass
class Template:
    name: str
    px: int
    py: int
    qx: int
    qy: int

    def __post_init__(self):
        self.p_support = weighted_triangle(self.px, self.py)
        self.q_support = weighted_triangle(self.qx, self.qy)
        self.inc = Incidence.create(self.p_support, self.q_support)
        self.ps = self.inc.p_support
        self.qs = self.inc.q_support
        self.targets = self.inc.targets
        self.p_index = {m: i for i, m in enumerate(self.ps)}
        self.q_index = {m: i for i, m in enumerate(self.qs)}
        self.t_index = {m: i for i, m in enumerate(self.targets)}
        self.nt = len(self.targets)
        self.nq = len(self.qs)
        self.npc = len(self.ps)
        rows, pcols, qcols, mults = [], [], [], []
        for (i, j) in self.ps:
            for (k, ell) in self.qs:
                mult = i * ell - j * k
                if mult:
                    rows.append(self.t_index[(i + k - 1, j + ell - 1)])
                    pcols.append(self.p_index[(i, j)])
                    qcols.append(self.q_index[(k, ell)])
                    mults.append(mult)
        self.rows = np.array(rows, dtype=np.int64)
        self.pcols = np.array(pcols, dtype=np.int64)
        self.qcols = np.array(qcols, dtype=np.int64)
        self.mults = np.array(mults, dtype=np.int64)
        self.zero_row = self.t_index[(0, 0)]
        # delta functional on Q coefficients: Q(1,0) - Q(0,0)
        self.delta = np.array([(1 if ell == 0 else 0) - (1 if (k, ell) == (0, 0) else 0)
                               for (k, ell) in self.qs], dtype=np.int64)
        self.q_at_00 = np.array([1 if m == (0, 0) else 0 for m in self.qs], dtype=np.int64)
        self.q_at_10 = np.array([1 if m[1] == 0 else 0 for m in self.qs], dtype=np.int64)
        # bottom sub-block: target rows (*,0), q columns with ell in {0,1}
        self.bot_rows = [self.t_index[m] for m in self.targets if m[1] == 0]
        self.bot_cols = [self.q_index[m] for m in self.qs if m[1] <= 1]
        # P monomials with j <= 1 are the only ones entering that sub-block
        self.p_vertex = self.p_index[(self.px, 0)], self.p_index[(0, self.py)]
        self.q_vertex = self.q_index[(self.qx, 0)], self.q_index[(0, self.qy)]

    def pvec(self, P: Polynomial, p: int) -> np.ndarray:
        v = np.zeros(self.npc, dtype=np.int64)
        for m, c in P.items():
            v[self.p_index[m]] = c % p
        return v

    def poly(self, vec: np.ndarray, which: str = "q", p: int = 0) -> Polynomial:
        support = self.qs if which == "q" else self.ps
        return {m: int(vec[i]) for i, m in enumerate(support) if int(vec[i]) % (p or 1)}

    def matrix(self, pvec: np.ndarray, p: int) -> np.ndarray:
        """Bracket matrix A with A @ qvec = coefficient vector of [P,Q]."""
        A = np.zeros((self.nt, self.nq), dtype=np.int64)
        contrib = (self.mults % p) * pvec[self.pcols] % p
        np.add.at(A, (self.rows, self.qcols), contrib)
        return A % p

    def rhs(self, p: int) -> np.ndarray:
        b = np.zeros(self.nt, dtype=np.int64)
        b[self.zero_row] = 1 % p
        return b

    def full_system(self, pvec: np.ndarray, p: int):
        """Bracket rows PLUS the two Q-collision rows (matches Incidence.system)."""
        A = self.matrix(pvec, p)
        A = np.concatenate([A, self.q_at_00.reshape(1, -1), self.q_at_10.reshape(1, -1)])
        b = np.concatenate([self.rhs(p), np.zeros(2, dtype=np.int64)])
        return A, b


# ------------------------------------------------------- analysis of one P

def analyse(tpl: Template, pvec: np.ndarray, p: int) -> dict:
    """Full rank/consistency profile of one P."""
    A = tpl.matrix(pvec, p)
    b = tpl.rhs(p)
    br = solve_mod(A, b, p, want_kernel=True)
    out = {"bracket_rank": br["rank"], "bracket_nullity": br["nullity"],
           "bracket_consistent": br["consistent"], "delta": None,
           "delta_movable": None, "full_consistent": False,
           "full_rank": None, "full_nullity": None, "Q": None}
    if br["consistent"]:
        d0 = int(tpl.delta @ br["particular"] % p)
        dk = (br["kernel"] @ tpl.delta) % p if br["kernel"] is not None else np.zeros(0, np.int64)
        out["delta"] = d0
        out["delta_movable"] = bool(np.any(dk))
    Afull, bfull = tpl.full_system(pvec, p)
    fu = solve_mod(Afull, bfull, p, want_kernel=True)
    out["full_rank"] = fu["rank"]
    out["full_nullity"] = fu["nullity"]
    out["full_consistent"] = fu["consistent"]
    if fu["consistent"]:
        out["Q"] = fu["particular"]
        out["Qkernel"] = fu["kernel"]
    return out


def bottom_block_consistent(tpl: Template, pvec: np.ndarray, p: int) -> bool:
    """Restriction of [P,Q]=1 to the line y=0 (a necessary sub-block).

    Rows (*,0) of the bracket only involve Q columns with y-exponent <= 1;
    they read  p'(x) s(x) - r(x) q'(x) = 1  with p=P(.,0), r=P_y(.,0).
    The two Q-collision rows also live in that block, so they are included.
    """
    A = tpl.matrix(pvec, p)
    sub = A[np.ix_(tpl.bot_rows, tpl.bot_cols)]
    c00 = tpl.q_at_00[tpl.bot_cols].reshape(1, -1)
    c10 = tpl.q_at_10[tpl.bot_cols].reshape(1, -1)
    sub = np.concatenate([sub, c00, c10])
    b = np.zeros(sub.shape[0], dtype=np.int64)
    b[tpl.bot_rows.index(tpl.zero_row)] = 1 % p
    return solve_mod(sub, b, p, want_kernel=False)["consistent"]


# -------------------------------------------------- independent replay path

def sympy_bracket(P: Polynomial, Q: Polynomial, p: int) -> Polynomial:
    """Independent bracket: symbolic differentiation over ZZ, reduced mod p."""
    Pe = sum(int(c) * _X ** i * _Y ** j for (i, j), c in P.items())
    Qe = sum(int(c) * _X ** i * _Y ** j for (i, j), c in Q.items())
    J = sp.expand(sp.diff(Pe, _X) * sp.diff(Qe, _Y) - sp.diff(Pe, _Y) * sp.diff(Qe, _X))
    if J == 0:
        return {}
    poly = sp.Poly(J, _X, _Y)
    out = {}
    for mon, coeff in zip(poly.monoms(), poly.coeffs()):
        v = int(coeff) % p
        if v:
            out[(int(mon[0]), int(mon[1]))] = v
    return out


def replay(P: Polynomial, Q: Polynomial, p: int) -> dict:
    """Independent verification of a claimed hit."""
    br = sympy_bracket(P, Q, p)
    return {
        "bracket_is_one": br == {(0, 0): 1 % p},
        "bracket": br,
        "P00": value_at(P, (0, 0), p), "P10": value_at(P, (1, 0), p),
        "Q00": value_at(Q, (0, 0), p), "Q10": value_at(Q, (1, 0), p),
    }


# --------------------------------------------------------- P constructions

def random_dense_P(tpl: Template, rng: np.random.Generator, p: int) -> np.ndarray:
    """Random P on the whole triangle with P(0,0)=P(1,0)=0 (via the engine decoder)."""
    free = [m for m in tpl.ps if m not in ((0, 0), (tpl.px, 0))]
    values = rng.integers(0, p, size=len(free)).tolist()
    P = collision_polynomial(tpl.ps, values, p)
    return tpl.pvec(P, p)


def coordinate_P(tpl: Template, fcoeffs: Sequence[int], lam: int, p: int) -> np.ndarray:
    """P = lam * ((y+f(x))^py - f(1)^py * x),  f(0)=0,  deg f <= px/py.

    (w^py + mu x, w) is a polynomial automorphism for w = y+f(x), so P is a
    genuine coordinate; the constant mu = -f(1)^py forces P(0,0)=P(1,0)=0.
    """
    d = tpl.px // tpl.py
    if len(fcoeffs) != d:
        raise ValueError("f must have exactly px/py coefficients (x^1..x^d)")
    w = {(0, 1): 1}
    for k, c in enumerate(fcoeffs, start=1):
        if c % p:
            w[(k, 0)] = c % p
    power = {(0, 0): 1}
    for _ in range(tpl.py):
        nxt = {}
        for m1, c1 in power.items():
            for m2, c2 in w.items():
                m = (m1[0] + m2[0], m1[1] + m2[1])
                nxt[m] = (nxt.get(m, 0) + c1 * c2) % p
        power = {m: c for m, c in nxt.items() if c}
    f1 = sum(int(c) for c in fcoeffs) % p
    mu = (-pow(f1, tpl.py, p)) % p
    P = dict(power)
    P[(1, 0)] = (P.get((1, 0), 0) + mu) % p
    P = {m: (lam * c) % p for m, c in P.items() if (lam * c) % p}
    return tpl.pvec(P, p)


def poly_mul(a: Polynomial, b: Polynomial, p: int) -> Polynomial:
    out: Polynomial = {}
    for m1, c1 in a.items():
        for m2, c2 in b.items():
            m = (m1[0] + m2[0], m1[1] + m2[1])
            out[m] = (out.get(m, 0) + c1 * c2) % p
    return {m: c for m, c in out.items() if c}


def poly_pow(a: Polynomial, n: int, p: int) -> Polynomial:
    out = {(0, 0): 1}
    for _ in range(n):
        out = poly_mul(out, a, p)
    return out


def edge_and_interior(tpl: Template):
    """Split P's triangle into its outer edge (weighted degree px*py) and the rest."""
    edge = [(i, j) for (i, j) in tpl.ps if i * tpl.py + j * tpl.px == tpl.px * tpl.py]
    inner = [(i, j) for (i, j) in tpl.ps if i * tpl.py + j * tpl.px < tpl.px * tpl.py]
    return edge, inner


def leading_form_P(tpl: Template, fcoeffs, lam: int, lower: dict, p: int):
    """P = lam*(y+f(x))^py + (arbitrary lower-weighted-degree terms), collision-fixed.

    The leading (edge) form of any Keller partner pair with these Newton
    triangles must be lam*h^py with h = y+c x^d weighted-homogeneous; this
    family is exactly the stratum satisfying that necessary condition.
    """
    d = tpl.px // tpl.py
    h = {(0, 1): 1}
    for k, c in enumerate(fcoeffs, start=1):
        if c % p:
            h[(k, 0)] = int(c) % p
    P = {m: (lam * c) % p for m, c in poly_pow(h, tpl.py, p).items()}
    for m, c in lower.items():
        if m == (0, 0):
            continue
        P[m] = (P.get(m, 0) + int(c)) % p
    P.pop((0, 0), None)
    # enforce P(1,0)=0 by adjusting the largest bottom-row monomial below the vertex
    bottom = sorted(i for (i, j) in tpl.ps if j == 0 and i > 0)
    fix = (bottom[-2], 0)
    P[fix] = (P.get(fix, 0) - sum(c for (i, j), c in P.items() if j == 0)) % p
    P = {m: c % p for m, c in P.items() if c % p and m in tpl.p_index}
    return tpl.pvec(P, p)


def is_nondegenerate(tpl: Template, pvec: np.ndarray, qvec: np.ndarray, p: int):
    return (bool(pvec[tpl.p_vertex[0]] % p), bool(pvec[tpl.p_vertex[1]] % p),
            bool(qvec[tpl.q_vertex[0]] % p) if qvec is not None else None,
            bool(qvec[tpl.q_vertex[1]] % p) if qvec is not None else None)


TEMPLATES = {
    "ribbon12": Template("ribbon12", 12, 2, 18, 3),
    "ribbon4": Template("ribbon4", 4, 2, 6, 3),
    "t44": Template("t44", 4, 4, 6, 6),
    "t84": Template("t84", 8, 4, 12, 6),
    "t164": Template("t164", 16, 4, 24, 6),
}
