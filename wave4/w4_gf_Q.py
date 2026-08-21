"""Exact linear algebra over the number field K = Q[w]/(f), f irreducible.

Mirrors wave4/w4_gf.py but over Q instead of F_p, so the case-(2) cascade can be
run in characteristic zero once the parametrisation over Q is in hand.

Self-test with negative controls at the bottom.
"""
import sys

import sympy as sp

W = sp.Symbol("w")


class KQ:
    def __init__(self, f):
        self.f = sp.Poly(f, W)
        self.deg = self.f.degree()

    def red(self, a):
        return sp.rem(sp.Poly(sp.expand(a), W), self.f).as_expr()

    def mul(self, a, b):
        return self.red(sp.expand(a * b))

    def add(self, a, b):
        return self.red(a + b)

    def sub(self, a, b):
        return self.red(a - b)

    def inv(self, a):
        pa = sp.Poly(sp.expand(a), W)
        if pa.is_zero:
            raise ZeroDivisionError("inverse of 0 in K")
        return sp.invert(pa, self.f).as_expr()

    def is_zero(self, a):
        return sp.Poly(sp.expand(a), W).rem(self.f).is_zero


def rref(Kf, M, rhs):
    nr = len(M)
    nc = len(M[0]) if nr else 0
    A = [[Kf.red(M[i][j]) for j in range(nc)] + [Kf.red(rhs[i])] for i in range(nr)]
    U = [[sp.Integer(1) if i == j else sp.Integer(0) for j in range(nr)]
         for i in range(nr)]
    piv, r = [], 0
    for c in range(nc):
        sel = None
        for i in range(r, nr):
            if not Kf.is_zero(A[i][c]):
                sel = i
                break
        if sel is None:
            continue
        A[r], A[sel] = A[sel], A[r]
        U[r], U[sel] = U[sel], U[r]
        iv = Kf.inv(A[r][c])
        A[r] = [Kf.mul(x, iv) for x in A[r]]
        U[r] = [Kf.mul(x, iv) for x in U[r]]
        for i in range(nr):
            if i != r and not Kf.is_zero(A[i][c]):
                fq = A[i][c]
                A[i] = [Kf.sub(A[i][k], Kf.mul(fq, A[r][k])) for k in range(nc + 1)]
                U[i] = [Kf.sub(U[i][k], Kf.mul(fq, U[r][k])) for k in range(nr)]
        piv.append(c)
        r += 1
        if r == nr:
            break
    return A, r, piv, U


def solve(Kf, M, rhs):
    nr = len(M)
    nc = len(M[0]) if nr else 0
    A, r, piv, U = rref(Kf, M, rhs)
    part = [sp.Integer(0)] * nc
    for i, c in enumerate(piv):
        part[c] = A[i][nc]
    free = [c for c in range(nc) if c not in piv]
    basis = []
    for fc in free:
        v = [sp.Integer(0)] * nc
        v[fc] = sp.Integer(1)
        for i, c in enumerate(piv):
            v[c] = Kf.sub(sp.Integer(0), A[i][fc])
        basis.append(v)
    lk = [U[i] for i in range(nr)
          if all(Kf.is_zero(A[i][c]) for c in range(nc))]
    return part, basis, lk


if __name__ == "__main__":
    ok = True
    f = W ** 3 - 2                      # irreducible over Q
    Kf = KQ(f)
    print("=" * 74)
    print("SELF-TEST of exact linear algebra over Q[w]/(w^3 - 2)")
    print("=" * 74)
    irr = sp.Poly(f, W).is_irreducible
    print(f"    [{'PASS' if irr else 'FAIL'}] the modulus is irreducible")
    ok &= irr
    a = 3 + 5 * W - W ** 2
    good = Kf.is_zero(Kf.sub(Kf.mul(a, Kf.inv(a)), 1))
    print(f"    [{'PASS' if good else 'FAIL'}] inversion inverts")
    ok &= good
    M = [[1, 2, W, 2 + 2 * W],
         [0, 1, 1, 1 + W],
         [1, 3, W + 1, 3 + 3 * W]]
    part, basis, lk = solve(Kf, M, [0, 0, 0])
    g2 = len(basis) == 2
    print(f"    [{'PASS' if g2 else 'FAIL'}] designed kernel: nullity {len(basis)} "
          f"(expected 2)")
    ok &= g2
    allz = True
    for v in basis:
        for row in M:
            s = sp.Integer(0)
            for cc, vv in zip(row, v):
                s = Kf.add(s, Kf.mul(cc, vv))
            allz &= Kf.is_zero(s)
    print(f"    [{'PASS' if allz else 'FAIL'}] kernel vectors annihilate every row")
    ok &= allz
    M2 = [r[:] for r in M]
    M2[2][3] = Kf.add(M2[2][3], 1)
    _, b2, _ = solve(Kf, M2, [0, 0, 0])
    dropped = len(b2) < len(basis)
    print(f"    [{'PASS' if dropped else 'FAIL'}] NEGATIVE: a one-entry "
          f"perturbation drops the nullity to {len(b2)}")
    ok &= dropped
    part, basis, lk = solve(Kf, M, [0, 0, 1])
    viol = []
    for row in lk:
        s = sp.Integer(0)
        for cc, rr in zip(row, [0, 0, 1]):
            s = Kf.add(s, Kf.mul(cc, rr))
        if not Kf.is_zero(s):
            viol.append(row)
    print(f"    [{'PASS' if viol else 'FAIL'}] NEGATIVE: an inconsistent "
          f"right-hand side is caught by {len(viol)} left-kernel functional(s)")
    ok &= bool(viol)
    print("=" * 74)
    sys.exit(0 if ok else 1)
