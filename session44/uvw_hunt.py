#!/usr/bin/env python3
"""Session 44, Lead 1 — hunt the (u,v,w) obstruction variety of the (4,6) ribbon.

Object: sol6's kernel-retaining recurrence on the live collision-first (4,6)
frontier (degree-126 weighted triangle), chart

    p0 = x^84 - x   (collision factor; x^84 invisible below rung 45),
    p1 = u x + ..., p2 = v x + ..., p3 = w x + ...   (no constant terms),
    c = 1;  P = p0 + p1 y + p2 y^2 + p3 y^3 + y^4,
    E2 = 0, E1 = 0, E0 = 1   (the three surviving reduced Jacobian rows).

The engine discovers the rung structure generically: at rung x^n the three
coefficient constraints are EXACTLY affine in the frontier unknowns
(p1[n+1], p2[n+1], p3[n+1] within degree caps 63/42/21, plus A1,A2,A3,A5 at
rungs 0-1), because a frontier coefficient p_i[m] first contributes
quadratically at x^(2m-1) > x^n.  Each rung is solved by row reduction; free
kernels are retained; constraints with no remaining unknowns are obstructions.
Past the p3 degree cap (rung >= 22) obstructions accumulate: their vanishing
locus in the surviving free parameters is where a counterexample must live on
this chart.

Modes:
  control          exact-Q replay of sol6's planted seed (calibration gate)
  probe p u v w    structure map at one modular point
  scan p [lo hi]   full F_p^3 grid (or a u-slice range), depth histogram
Nothing this script prints is a counterexample claim; survivors are
candidates for the second-prime / Hensel / exact-replay pipeline.
"""
import argparse
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
import sympy as sp  # noqa: E402

import ribbon46_reduction as r46  # noqa: E402

P_SYMS = list(r46.p)
DP_SYMS = list(r46.dp)
A_SYMS = list(r46.A)
C_SYM = r46.c
ALL_SYMS = P_SYMS + DP_SYMS + A_SYMS + [C_SYM]
DEG_CAP = {0: 84, 1: 63, 2: 42, 3: 21}


def extract_terms(expr):
    poly = sp.Poly(sp.expand(expr), *ALL_SYMS)
    out = []
    for exps, coeff in poly.terms():
        q = sp.Rational(coeff)
        out.append((int(q.p), int(q.q),
                    tuple((i, e) for i, e in enumerate(exps) if e)))
    return out


def build_rows():
    """Return the three surviving rows and their A-sensitivity polynomials."""
    rows = [r46.survivors[2], r46.survivors[1], r46.survivors[0] - 1]
    used_A = sorted({j for row in rows for j in range(6)
                     if sp.Symbol(f"A{j}") in row.free_symbols},
                    )
    terms = [extract_terms(row) for row in rows]
    dA = [[extract_terms(sp.diff(row, A_SYMS[j])) for j in range(6)] for row in rows]
    dP = [[extract_terms(sp.diff(row, P_SYMS[i])) for i in range(4)] for row in rows]
    dDP = [[extract_terms(sp.diff(row, DP_SYMS[i])) for i in range(4)] for row in rows]
    return terms, dA, dP, dDP, used_A


TERMS, D_A, D_P, D_DP, USED_A = build_rows()


class State:
    """Recurrence state over a field (mod p ints, or Fraction for p=None)."""

    def __init__(self, p, u, v, w, horizon):
        self.p = p
        self.N = horizon
        z, o = self.conv(0), self.conv(1)
        self.series = {i: [z] * (horizon + 2) for i in range(4)}
        self.series[0][1] = self.neg(o)          # p0 = -x (+ x^84, invisible)
        self.series[1][1] = self.conv(u)
        self.series[2][1] = self.conv(v)
        self.series[3][1] = self.conv(w)
        self.A = {j: z for j in range(6)}
        self.free = []       # list of ("p", i, m) or ("A", j) still undetermined
        self.fixed_log = []  # (rung, name, value)
        self.obstructions = []  # (rung, value, n_free_at_rung)

    # field helpers -------------------------------------------------------
    def conv(self, x):
        if self.p is None:
            return Fraction(x)
        return x % self.p

    def neg(self, x):
        return -x if self.p is None else (-x) % self.p

    def add(self, x, y):
        return x + y if self.p is None else (x + y) % self.p

    def mul(self, x, y):
        return x * y if self.p is None else (x * y) % self.p

    def inv(self, x):
        return Fraction(1) / x if self.p is None else pow(x, self.p - 2, self.p)

    # series helpers ------------------------------------------------------
    def sym_series(self, idx, n):
        """Series (length n+1) for symbol index in ALL_SYMS at current state."""
        z = self.conv(0)
        if idx < 4:
            return self.series[idx][: n + 1]
        if idx < 8:
            i = idx - 4
            s = self.series[i]
            return [self.mul(self.conv(k + 1), s[k + 1]) for k in range(n + 1)]
        if idx < 14:
            out = [z] * (n + 1)
            out[0] = self.A[idx - 8]
            return out
        out = [z] * (n + 1)
        out[0] = self.conv(1)  # c = 1
        return out

    def ratio(self, num, den):
        if self.p is None:
            return Fraction(num, den)
        return (num % self.p) * self.inv(den % self.p) % self.p

    def eval_coeff(self, term_list, n):
        """Coefficient of x^n of a monomial-list expression at current state."""
        z = self.conv(0)
        total = z
        for num, den, factors in term_list:
            acc = [z] * (n + 1)
            acc[0] = self.ratio(num, den)
            for idx, power in factors:
                fs = self.sym_series(idx, n)
                for _ in range(power):
                    new = [z] * (n + 1)
                    for a_i, a_val in enumerate(acc):
                        if a_val == z:
                            continue
                        for b_i in range(n + 1 - a_i):
                            b_val = fs[b_i]
                            if b_val != z:
                                new[a_i + b_i] = self.add(new[a_i + b_i],
                                                          self.mul(a_val, b_val))
                    acc = new
            total = self.add(total, acc[n])
        return total

    def low_eval(self, term_list, order=1):
        """First (order+1) coefficients of an expression (cheap)."""
        return [self.eval_coeff(term_list, k) for k in range(order + 1)]

    # sensitivities -------------------------------------------------------
    def sensitivity(self, row, unk, n):
        kind = unk[0]
        if kind == "A":
            return self.eval_coeff(D_A[row][unk[1]], n)
        _, i, m = unk
        s = self.conv(0)
        if n - m >= 0:
            s = self.add(s, self.eval_coeff(D_P[row][i], n - m))
        if n - m + 1 >= 0:
            ddp = self.eval_coeff(D_DP[row][i], n - m + 1)
            s = self.add(s, self.mul(self.conv(m), ddp))
        return s

    # rung solve ----------------------------------------------------------
    def run(self, verbose=False):
        z = self.conv(0)
        for j in USED_A:
            self.free.append(("A", j))
        for n in range(self.N + 1):
            for i in (1, 2, 3):
                m = n + 1
                if 2 <= m <= DEG_CAP[i]:
                    self.free.append(("p", i, m))
            rows_dat = []
            for row in range(3):
                const = self.eval_coeff(TERMS[row], n)
                sens = [self.sensitivity(row, unk, n) for unk in self.free]
                rows_dat.append((const, sens))
            # row reduce the 3 x |free| affine system
            mat = [list(sens) + [self.neg(const)] for const, sens in rows_dat]
            ncols = len(self.free)
            pivots = []
            r = 0
            for col in range(ncols):
                piv = next((k for k in range(r, 3) if mat[k][col] != z), None)
                if piv is None:
                    continue
                mat[r], mat[piv] = mat[piv], mat[r]
                iv = self.inv(mat[r][col])
                mat[r] = [self.mul(iv, x) for x in mat[r]]
                for k in range(3):
                    if k != r and mat[k][col] != z:
                        f = mat[k][col]
                        mat[k] = [self.add(x, self.neg(self.mul(f, y)))
                                  for x, y in zip(mat[k], mat[r])]
                pivots.append((r, col))
                r += 1
                if r == 3:
                    break
            # inconsistent rows -> obstructions
            for k in range(r, 3):
                if mat[k][ncols] != z:
                    self.obstructions.append((n, self.neg(mat[k][ncols]),
                                              len(self.free)))
                    if verbose:
                        print(f"  rung {n}: OBSTRUCTION {self.neg(mat[k][ncols])} "
                              f"({len(self.free)} free)")
                    return False
            # back-substitute determined unknowns (cols with pivot, others zero
            # in every row => truly determined only if col appears in exactly
            # one pivot row and no free col mixes; handle general case by
            # solving pivot cols in terms of non-pivot cols only when the
            # non-pivot sens are all zero in that row)
            piv_cols = [c_ for _, c_ in pivots]
            det_vals = {}
            for rr, col in pivots:
                mixed = any(mat[rr][c2] != z for c2 in range(ncols)
                            if c2 != col and c2 not in piv_cols)
                if not mixed:
                    det_vals[col] = mat[rr][ncols]
            # NOTE: if pivot rows mix undetermined frees, the relation couples
            # future kernels; we then leave those unknowns free and DO NOT fix
            # them (correctness first).  Record for inspection.
            for col in sorted(det_vals, reverse=True):
                unk = self.free[col]
                val = det_vals[col]
                if unk[0] == "A":
                    self.A[unk[1]] = val
                else:
                    _, i, m = unk
                    self.series[i][m] = val
                self.fixed_log.append((n, unk, val))
                self.free.pop(col)
            if verbose:
                fixed_here = [(u_, v_) for (rn, u_, v_) in self.fixed_log
                              if rn == n]
                print(f"  rung {n}: fixed {len(fixed_here)}, "
                      f"free now {self.free}")
        return True


def fmt(unk):
    return f"A{unk[1]}" if unk[0] == "A" else f"p{unk[1]}[{unk[2]}]"


def control():
    """Exact replay of the sol6 planted seed as an instrument calibration."""
    st = State(None, 1, 0, 0, 22)
    ok = st.run(verbose=True)
    expect = {(1, 2): Fraction(7, 4), (1, 3): Fraction(1, 4),
              (2, 2): Fraction(-39, 8), (2, 3): Fraction(-49, 8),
              (3, 2): Fraction(33, 8)}
    print("A:", {j: st.A[j] for j in USED_A})
    for (i, m), val in expect.items():
        got = st.series[i][m]
        print(f"p{i}[{m}] = {got}  expected {val}  "
              f"{'OK' if got == val else 'MISMATCH'}")
    print("p3[3] =", st.series[3][3])
    print("survived:", ok, " obstructions:", st.obstructions)
    print("free at end:", [fmt(u_) for u_ in st.free])


def probe(p, u, v, w, horizon):
    st = State(p, u, v, w, horizon)
    ok = st.run(verbose=True)
    print("survived:", ok)
    print("obstructions:", st.obstructions)
    print("free at end:", [fmt(u_) for u_ in st.free])
    return st


def scan(p, horizon, ulo, uhi):
    """Depth map over F_p^3 (u in [ulo,uhi), v,w full).  Depth = first
    obstruction rung; survivors past the horizon are printed immediately."""
    from collections import Counter
    hist = Counter()
    survivors = []
    for u in range(ulo, uhi):
        for v in range(p):
            for w in range(p):
                st = State(p, u, v, w, horizon)
                ok = st.run()
                if ok:
                    survivors.append((u, v, w, [fmt(x) for x in st.free]))
                    print(f"SURVIVOR to rung {horizon}: (u,v,w)=({u},{v},{w}) "
                          f"free={[fmt(x) for x in st.free]}", flush=True)
                else:
                    hist[st.obstructions[0][0]] += 1
        print(f"u={u} done; depth histogram so far: {dict(sorted(hist.items()))}",
              flush=True)
    print("FINAL histogram:", dict(sorted(hist.items())))
    print("survivors:", survivors)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["control", "probe", "scan"])
    ap.add_argument("args", nargs="*", type=int)
    ap.add_argument("--horizon", type=int, default=27)
    a = ap.parse_args()
    if a.mode == "control":
        control()
    elif a.mode == "probe":
        p, u, v, w = a.args
        probe(p, u, v, w, a.horizon)
    else:
        p = a.args[0]
        ulo = a.args[1] if len(a.args) > 1 else 0
        uhi = a.args[2] if len(a.args) > 2 else p
        scan(p, a.horizon, ulo, uhi)
