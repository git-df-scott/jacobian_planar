#!/usr/bin/env python3
"""Graded (Newton-weighted) descent on the collision-first incidence variety.

Weights are (wt x, wt y) = (1, d) with d = px/py, so P's Newton edge has
weighted degree px and Q's has qx = 3px/2.  Any solution of [P,Q]=1 must have

    P_top = lam * h^py ,   Q_top = mu * h^qy ,   h = y + c x^d + ...

(a common weighted-homogeneous factor), because the top graded piece of the
bracket has to vanish.  Writing P = sum_a P_a, Q = sum_b Q_b by weighted degree,

    [P,Q]_g = sum_{a+b = g+1+d} [P_a, Q_b] = delta_{g,0}

and at level k (g = px+qx-1-d-k) the ONLY unknown blocks are P_{px-k} and
Q_{qx-k}; everything else was fixed at earlier levels.  So the whole upper part
of the Keller system is a triangular chain of small LINEAR systems.  This script
runs that chain exactly over F_p, level by level, and reports where it dies.
"""
from __future__ import annotations

import json
import sys
from collections import Counter

import numpy as np

from lane7_lib import (TEMPLATES, Template, poly_mul, poly_pow, replay,
                       solve_mod, sympy_bracket)

P_MAIN = 1000003


def wdeg(m, d):
    return m[0] + d * m[1]


class Descent:
    def __init__(self, tpl: Template, p: int):
        self.tpl = tpl
        self.p = p
        self.d = tpl.px // tpl.py
        d = self.d
        self.pblocks = {}
        for m in tpl.ps:
            self.pblocks.setdefault(wdeg(m, d), []).append(m)
        self.qblocks = {}
        for m in tpl.qs:
            self.qblocks.setdefault(wdeg(m, d), []).append(m)
        self.levels = tpl.qx + 1          # k = 0 .. qx  (Q's constant block last)

    def bracket_block(self, A, B):
        """[A,B] as a dict, A and B dicts of monomial -> coeff."""
        p = self.p
        out = {}
        for (i, j), a in A.items():
            for (k, ell), b in B.items():
                mult = i * ell - j * k
                if mult % p:
                    t = (i + k - 1, j + ell - 1)
                    out[t] = (out.get(t, 0) + mult * a * b) % p
        return {m: c for m, c in out.items() if c}

    def run(self, lam, mu, hcoeffs, rng, record=None):
        """One random walk down the descent.  Returns (P, Q, level_failed)."""
        p, d, tpl = self.p, self.d, self.tpl
        h = {(0, 1): 1}
        if hcoeffs[-1] % p:
            h[(d, 0)] = int(hcoeffs[-1]) % p
        Ptop = {m: (lam * c) % p for m, c in poly_pow(h, tpl.py, p).items()}
        Qtop = {m: (mu * c) % p for m, c in poly_pow(h, tpl.qy, p).items()}
        P = {a: {} for a in self.pblocks}
        Q = {b: {} for b in self.qblocks}
        P[tpl.px] = Ptop
        Q[tpl.qx] = Qtop
        dims = []
        for k in range(0, self.levels):
            g = tpl.px + tpl.qx - 1 - d - k
            unknown_p = self.pblocks.get(tpl.px - k, []) if k > 0 else []
            unknown_q = self.qblocks.get(tpl.qx - k, []) if k > 0 else []
            # known part: pairs (px-i, qx-k+i) for 0 < i < k
            known = {}
            for i in range(1, k):
                a, b = tpl.px - i, tpl.qx - (k - i)
                if a in P and b in Q and P[a] and Q[b]:
                    for m, c in self.bracket_block(P[a], Q[b]).items():
                        known[m] = (known.get(m, 0) + c) % p
            if k == 0:
                chk = self.bracket_block(Ptop, Qtop)
                if chk:
                    return None, None, ("TOP FORM DOES NOT COMMUTE", k), dims
                dims.append((k, g, 0, 0))
                continue
            rows = sorted({m for m in known} |
                          {(i + kk - 1, j + ll - 1)
                           for (i, j) in list(Ptop) + unknown_p
                           for (kk, ll) in list(Qtop) + unknown_q}
                          )
            rows = [m for m in rows if wdeg(m, d) == g and m[0] >= 0 and m[1] >= 0]
            ridx = {m: r for r, m in enumerate(rows)}
            ncol = len(unknown_p) + len(unknown_q)
            A = np.zeros((len(rows), ncol), dtype=np.int64)
            b = np.zeros(len(rows), dtype=np.int64)
            for m, c in known.items():
                if m in ridx:
                    b[ridx[m]] = (-c) % p
                elif c % p:
                    return None, None, ("KNOWN TERM OUTSIDE ROW SET", k, m), dims
            if g == 0:
                if (0, 0) not in ridx:
                    # the constant row must exist even with no basis contribution
                    rows.append((0, 0))
                    ridx[(0, 0)] = len(rows) - 1
                    A = np.concatenate([A, np.zeros((1, ncol), dtype=np.int64)])
                    b = np.concatenate([b, np.zeros(1, dtype=np.int64)])
                b[ridx[(0, 0)]] = (b[ridx[(0, 0)]] + 1) % p
            for col, m in enumerate(unknown_p):
                i, j = m
                for (kk, ll), cq in Qtop.items():
                    mult = i * ll - j * kk
                    if mult % p:
                        t = (i + kk - 1, j + ll - 1)
                        if t in ridx:
                            A[ridx[t], col] = (A[ridx[t], col] + mult * cq) % p
            for col0, m in enumerate(unknown_q):
                col = len(unknown_p) + col0
                kk, ll = m
                for (i, j), cp in Ptop.items():
                    mult = i * ll - j * kk
                    if mult % p:
                        t = (i + kk - 1, j + ll - 1)
                        if t in ridx:
                            A[ridx[t], col] = (A[ridx[t], col] + mult * cp) % p
            sol = solve_mod(A, b, p)
            if not sol["consistent"]:
                if record is not None:
                    record.append((k, g, "inconsistent"))
                return None, None, ("INCONSISTENT", k, g), dims
            z = sol["particular"].copy()
            K = sol["kernel"]
            if K is not None and len(K):
                coef = rng.integers(0, p, size=len(K))
                z = (z + coef @ K) % p
            dims.append((k, g, len(rows), int(sol["nullity"])))
            for col, m in enumerate(unknown_p):
                if z[col] % p:
                    P[tpl.px - k][m] = int(z[col] % p)
            for col0, m in enumerate(unknown_q):
                if z[len(unknown_p) + col0] % p:
                    Q[tpl.qx - k][m] = int(z[len(unknown_p) + col0] % p)
        Pfull, Qfull = {}, {}
        for blk in P.values():
            for m, c in blk.items():
                Pfull[m] = (Pfull.get(m, 0) + c) % p
        for blk in Q.values():
            for m, c in blk.items():
                Qfull[m] = (Qfull.get(m, 0) + c) % p
        Pfull = {m: c for m, c in Pfull.items() if c}
        Qfull = {m: c for m, c in Qfull.items() if c}
        return Pfull, Qfull, None, dims


def main():
    p = P_MAIN
    names = sys.argv[1:] or ["t44", "t84", "ribbon12", "t164"]
    out = {}
    for name in names:
        tpl = TEMPLATES[name]
        des = Descent(tpl, p)
        rng = np.random.default_rng(2024)
        fails = Counter()
        completed = 0
        collisions = Counter()
        dims_seen = None
        sample = None
        for trial in range(120):
            lam = int(rng.integers(1, p))
            mu = int(rng.integers(1, p))
            hc = [int(rng.integers(0, p)) for _ in range(des.d - 1)] + [int(rng.integers(1, p))]
            hc = hc[::-1] if False else hc
            P, Q, err, dims = des.run(lam, mu, hc, rng)
            if dims_seen is None:
                dims_seen = dims
            if err is not None:
                fails[str(err[:3])] += 1
                continue
            completed += 1
            rp = replay(P, Q, p)
            if not rp["bracket_is_one"]:
                fails["REPLAY FAILED"] += 1
                continue
            # now impose the four collision values
            c = (rp["P00"], rp["P10"], rp["Q00"], rp["Q10"])
            collisions[("P00=0" if c[0] == 0 else "P00!=0") + "," +
                       ("P10=P00" if c[1] == c[0] else "P10!=P00") + "," +
                       ("Q10=Q00" if c[3] == c[2] else "Q10!=Q00")] += 1
            if sample is None:
                sample = {"P": {str(k): v for k, v in P.items()},
                          "Q": {str(k): v for k, v in Q.items()},
                          "values": c}
        out[name] = {"levels": des.levels, "d": des.d,
                     "completed_descents": completed, "trials": 120,
                     "failures": dict(fails),
                     "collision_pattern_of_completed": dict(collisions),
                     "level_dims(k,g,rows,nullity)": dims_seen,
                     "sample": sample}
        print(f"--- {name} ---")
        print(json.dumps(out[name], indent=1, default=str)[:3000], flush=True)
    with open("lane7_descent.json", "w") as fh:
        json.dump(out, fh, indent=1, default=str)


if __name__ == "__main__":
    main()
