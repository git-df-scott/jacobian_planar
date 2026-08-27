#!/usr/bin/env python3
"""Session 44 — generic chart (u != 0) of the (4,6) frontier with u SYMBOLIC.

Walks the sol6 kernel-retaining recurrence at fixed numeric (v, w) mod p with
u a symbolic variable: field F_p(u), elements (num, den) as nmod_poly pairs.
Each rung solves the 3x3 affine system (kernel p3[n], p1[n+1], p2[n+1]) by
linearity probing; divisions live in F_p(u) (the kernel pivot is (n+1)u/4 x
units — its u=0 zero is the separately-decided u=0 chart).  Rungs >= 22 emit
obstruction numerators O_n(u) in F_p[u].

Output per (v,w): degrees of O_22..O_25 and gcd_u(O_22,...) — a nontrivial
gcd flags candidate u-values over that (v,w) slice.  Full-grid or random
slices assemble the char-0 evidence for the generic chart.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
from flint import nmod_poly  # noqa: E402

from uvw_hunt import TERMS  # noqa: E402

P = None


def npoly(c):
    return nmod_poly(c, P)


class R:
    """Rational function num/den in u over F_p."""

    __slots__ = ("n", "d")

    def __init__(self, n, d):
        self.n, self.d = n, d

    @staticmethod
    def const(c):
        return R(npoly([c % P]), npoly([1]))

    @staticmethod
    def u_sym():
        return R(npoly([0, 1]), npoly([1]))

    def is_zero(self):
        return not self.n

    def reduce(self):
        if self.d.degree() > 0 and self.n:
            g = self.n.gcd(self.d)
            if g.degree() > 0:
                self.n //= g
                self.d //= g
        if self.d.degree() >= 0:
            lc = self.d[self.d.degree()]
            if lc != 1:
                iv = pow(int(lc), P - 2, P)
                self.n *= iv
                self.d *= iv
        return self

    def add(self, o):
        if self.is_zero():
            return o
        if o.is_zero():
            return self
        if self.d == o.d:
            return R(self.n + o.n, self.d).reduce()
        return R(self.n * o.d + o.n * self.d, self.d * o.d).reduce()

    def mul(self, o):
        if self.is_zero() or o.is_zero():
            return R_ZERO
        return R(self.n * o.n, self.d * o.d).reduce()

    def neg(self):
        return R(-self.n, self.d)

    def inv(self):
        assert self.n, "division by zero in F_p(u)"
        return R(self.d, self.n).reduce()

    def scal(self, c):
        c %= P
        return R(self.n * c, self.d).reduce() if c else R_ZERO


class GWalk:
    def __init__(self, v, w, horizon, symbolic="u"):
        """symbolic: which of (u,v,w) is the polynomial variable; the other
        two take the numeric arguments (v,w) -> (first, second)."""
        self.N = horizon
        sym = R.u_sym()
        if symbolic == "u":
            leads = (sym, R.const(v), R.const(w))
        elif symbolic == "v":
            leads = (R.const(v), sym, R.const(w))
        else:
            leads = (R.const(v), R.const(w), sym)
        self.s = {1: {0: R_ZERO, 1: leads[0]},
                  2: {0: R_ZERO, 1: leads[1]},
                  3: {0: R_ZERO, 1: leads[2]}}
        self.A = {j: R_ZERO for j in range(6)}
        self.obstructions = {}

    def series_for(self, idx, n):
        z = R_ZERO
        if idx == 0:
            out = [z] * (n + 1)
            if n >= 1:
                out[1] = R.const(P - 1)
            if n >= 84:
                out[84] = R.const(1)
            return out
        if idx < 4:
            src = self.s[idx]
            return [src.get(k, z) for k in range(n + 1)]
        if idx == 4:
            out = [R.const(P - 1)] + [z] * n
            if n >= 83:
                out[83] = R.const(84)
            return out
        if idx < 8:
            src = self.s[idx - 4]
            return [src.get(k + 1, z).scal(k + 1) for k in range(n + 1)]
        if idx < 14:
            out = [z] * (n + 1)
            out[0] = self.A[idx - 8]
            return out
        out = [z] * (n + 1)
        out[0] = R.const(1)
        return out

    def row_coeff(self, row, n):
        cache = {}
        total = R_ZERO
        for num, den, factors in TERMS[row]:
            c0 = num * pow(den, P - 2, P) % P
            acc = [R.const(c0)] + [R_ZERO] * n
            for idx, power in factors:
                if idx not in cache:
                    cache[idx] = self.series_for(idx, n)
                fs = cache[idx]
                for _ in range(power):
                    new = [R_ZERO] * (n + 1)
                    for i, av in enumerate(acc):
                        if av.is_zero():
                            continue
                        for j in range(n + 1 - i):
                            bv = fs[j]
                            if not bv.is_zero():
                                new[i + j] = new[i + j].add(av.mul(bv))
                    acc = new
            total = total.add(acc[n])
        return total

    def solve_rung(self, n):
        """Affine solve of the rung-n system by probing.  Unknowns:
        A-set at rungs 0-1, then (p3[n], p1[n+1], p2[n+1]) within caps."""
        if n == 0:
            unknowns = [("A", 1), ("A", 2), ("A", 3)]
        elif n == 1:
            unknowns = [("A", 5), ("p", 1, 2), ("p", 2, 2)]
        else:
            unknowns = []
            if n <= 21:
                unknowns.append(("p", 3, n))
            if n + 1 <= 63:
                unknowns.append(("p", 1, n + 1))
            if n + 1 <= 42:
                unknowns.append(("p", 2, n + 1))

        def setu(unk, val):
            if unk[0] == "A":
                self.A[unk[1]] = val
            else:
                self.s[unk[1]][unk[2]] = val

        for unk in unknowns:
            setu(unk, R_ZERO)
        rows = []
        for row in range(3):
            const = self.row_coeff(row, n)
            if row == 2 and n == 0:
                pass  # TERMS[2] already includes the -1
            sens = []
            for unk in unknowns:
                setu(unk, R.const(1))
                s = self.row_coeff(row, n).add(const.neg())
                setu(unk, R_ZERO)
                sens.append(s)
            rows.append((const, sens))
        # Gaussian elimination over F_p(u)
        m = [list(sens) + [const.neg()] for const, sens in rows]
        ncols = len(unknowns)
        piv_of_col = {}
        r = 0
        for col in range(ncols):
            piv = next((k for k in range(r, 3) if not m[k][col].is_zero()),
                       None)
            if piv is None:
                continue
            m[r], m[piv] = m[piv], m[r]
            iv = m[r][col].inv()
            m[r] = [x.mul(iv) for x in m[r]]
            for k in range(3):
                if k != r and not m[k][col].is_zero():
                    f = m[k][col]
                    m[k] = [x.add(f.mul(y).neg()) for x, y in zip(m[k], m[r])]
            piv_of_col[col] = r
            r += 1
            if r == 3:
                break
        # leftover inconsistent rows = obstructions
        for k in range(r, 3):
            if not m[k][ncols].is_zero():
                self.obstructions[n] = m[k][ncols]
        # assign
        for col, unk in enumerate(unknowns):
            if col in piv_of_col:
                rr = piv_of_col[col]
                assert all(m[rr][c2].is_zero() for c2 in range(ncols)
                           if c2 != col), f"rung {n}: mixed solve"
                setu(unk, m[rr][ncols])
            else:
                assert False, f"rung {n}: unknown {unk} undetermined"

    def run(self, verbose=False):
        for n in range(self.N + 1):
            self.solve_rung(n)
            if verbose and n in self.obstructions:
                o = self.obstructions[n]
                print(f"rung {n}: obstruction num deg_u = {o.n.degree()}",
                      flush=True)
        return self.obstructions


def main():
    global P, R_ZERO
    ap = argparse.ArgumentParser()
    ap.add_argument("prime", type=int)
    ap.add_argument("v", type=int)
    ap.add_argument("w", type=int)
    ap.add_argument("--horizon", type=int, default=25)
    ap.add_argument("--symbolic", choices=["u", "v", "w"], default="u")
    a = ap.parse_args()
    P = a.prime
    R_ZERO = R(npoly([]), npoly([1]))
    wk = GWalk(a.v, a.w, a.horizon, symbolic=a.symbolic)
    obs = wk.run(verbose=True)
    polys = [o.n for n, o in sorted(obs.items())]
    if len(polys) >= 2:
        g = polys[0].gcd(polys[1])
        for q in polys[2:]:
            g = g.gcd(q)
        print(f"(v,w)=({a.v},{a.w}) mod {P}: obstruction degs "
              f"{[q.degree() for q in polys]}, gcd_u deg {g.degree()}")
        if g.degree() > 0:
            print("NONTRIVIAL u-gcd:", g)


if __name__ == "__main__":
    R_ZERO = None
    main()
