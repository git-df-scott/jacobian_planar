"""Exact linear algebra over K = F_p[w]/(g), g irreducible mod p.

Elements are sympy expressions in the symbol w, always kept reduced mod g and
mod p.  Everything is exact; no floats, no probabilistic rank tests.

Self-test at the bottom, with negative controls:
  * inversion must invert;
  * a matrix built to have a known 2-dimensional kernel must report nullity 2,
    and a random perturbation of it must NOT (the rank test is not vacuous);
  * an inconsistent system must be reported inconsistent, and the left-kernel
    functionals must actually annihilate the row space.
"""

import sys

import sympy as sp

W = sp.Symbol("w")


class K:
    def __init__(self, p, g):
        self.p = p
        self.g = sp.Poly(g, W, modulus=p)
        self.deg = self.g.degree()

    def red(self, a):
        return sp.rem(sp.Poly(sp.expand(a), W, modulus=p_of(self)), self.g).as_expr()

    def mul(self, a, b):
        return sp.rem(sp.Poly(sp.expand(a * b), W, modulus=self.p), self.g).as_expr()

    def add(self, a, b):
        return sp.rem(sp.Poly(sp.expand(a + b), W, modulus=self.p), self.g).as_expr()

    def sub(self, a, b):
        return sp.rem(sp.Poly(sp.expand(a - b), W, modulus=self.p), self.g).as_expr()

    def inv(self, a):
        pa = sp.Poly(sp.expand(a), W, modulus=self.p)
        if pa.is_zero:
            raise ZeroDivisionError("inverse of 0 in K")
        return sp.invert(pa, self.g).as_expr()

    def is_zero(self, a):
        return sp.Poly(sp.expand(a), W, modulus=self.p).rem(self.g).is_zero


def p_of(k):
    return k.p


def rref(Kf, M, rhs):
    """Row-reduce [M | rhs] over K.  Returns (A, rank, pivots, rowops).

    rowops records the row operations as a matrix U with U*[M|rhs] = A, so the
    LEFT KERNEL functionals can be read off as the rows of U whose M-part is
    zero.  Those are exactly the consistency conditions.
    """
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
                f = A[i][c]
                A[i] = [Kf.sub(A[i][k], Kf.mul(f, A[r][k])) for k in range(nc + 1)]
                U[i] = [Kf.sub(U[i][k], Kf.mul(f, U[r][k])) for k in range(nr)]
        piv.append(c)
        r += 1
        if r == nr:
            break
    return A, r, piv, U


def solve(Kf, M, rhs):
    """(particular, kernel_basis, left_kernel_rows) over K.

    `left_kernel_rows` are the rows U[i] whose M-part vanished: for each, the
    consistency condition is  sum_j U[i][j] * rhs[j] = 0.
    """
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
    lk = []
    for i in range(nr):
        if all(Kf.is_zero(A[i][c]) for c in range(nc)):
            lk.append(U[i])
    return part, basis, lk


if __name__ == "__main__":
    ok = True
    p, gpoly = 1000003, W ** 2 + 1          # x^2+1 is irreducible when p = 3 (4)
    if pow(-1, (p - 1) // 2, p) == 1:
        gpoly = W ** 2 - 2                  # fall back; checked below
    Kf = K(p, gpoly)
    print("=" * 74)
    print(f"SELF-TEST of exact linear algebra over F_{p}[w]/({sp.sstr(gpoly)})")
    print("=" * 74)
    irred = sp.Poly(gpoly, W, modulus=p).is_irreducible
    print(f"    [{'PASS' if irred else 'FAIL'}] the modulus is irreducible")
    ok &= irred
    a = 3 + 5 * W
    good = Kf.is_zero(Kf.sub(Kf.mul(a, Kf.inv(a)), 1))
    print(f"    [{'PASS' if good else 'FAIL'}] inversion inverts")
    ok &= good
    # a 3x4 matrix with a designed 2-dimensional kernel
    M = [[1, 2, W, 2 + 2 * W],
         [0, 1, 1, 1 + W],
         [1, 3, W + 1, 3 + 3 * W]]
    part, basis, lk = solve(Kf, M, [0, 0, 0])
    good = len(basis) == 2
    print(f"    [{'PASS' if good else 'FAIL'}] designed kernel found: nullity "
          f"{len(basis)} (expected 2)")
    ok &= good
    for v in basis:
        for row in M:
            s = sp.Integer(0)
            for cc, vv in zip(row, v):
                s = Kf.add(s, Kf.mul(cc, vv))
            if not Kf.is_zero(s):
                ok = False
    print(f"    [{'PASS' if ok else 'FAIL'}] every kernel vector annihilates every row")
    # NEGATIVE control: perturbing one entry must reduce the nullity
    M2 = [r[:] for r in M]
    M2[2][3] = Kf.add(M2[2][3], 1)
    _, basis2, _ = solve(Kf, M2, [0, 0, 0])
    good = len(basis2) < len(basis)
    print(f"    [{'PASS' if good else 'FAIL'}] NEGATIVE: a one-entry perturbation "
          f"drops the nullity to {len(basis2)}")
    ok &= good
    # NEGATIVE control: an inconsistent system is caught by the left kernel
    rhs = [0, 0, 1]
    part, basis, lk = solve(Kf, M, rhs)
    viol = []
    for row in lk:
        s = sp.Integer(0)
        for cc, rr in zip(row, rhs):
            s = Kf.add(s, Kf.mul(cc, rr))
        if not Kf.is_zero(s):
            viol.append(row)
    good = bool(viol)
    print(f"    [{'PASS' if good else 'FAIL'}] NEGATIVE: an inconsistent right-hand "
          f"side is caught by {len(viol)} left-kernel functional(s)")
    ok &= good
    print("=" * 74)
    sys.exit(0 if ok else 1)
