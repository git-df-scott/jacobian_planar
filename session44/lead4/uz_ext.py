#!/usr/bin/env python3
"""Complete the q-layer: run the cascade over GF(p)[a]/(h) for EVERY
irreducible factor h of the eliminating polynomial, so that all 35 solutions
of the q-layer (with the gauge q8 = 1) are covered, not only the GF(p)-rational
ones."""
import ast
import os
import subprocess
import sys

from uz_eliminate import run
from uz_system import PVARS, PIDX

HERE = os.path.dirname(os.path.abspath(__file__))
PV = ["p%d" % a for a in range(1, 9)]
FV = ["f%d" % a for a in range(1, 9)]


# ---------------------------------------------------------------- GF(p)[a]/h
class Fq:
    __slots__ = ("c",)

    def __init__(s, c):
        s.c = tuple(c)

    def __repr__(s):
        return "+".join(f"{v}*a^{i}" for i, v in enumerate(s.c) if v) or "0"


class Field:
    def __init__(self, p, h):
        self.p = p
        self.h = [x % p for x in h]          # monic, low->high
        self.d = len(h) - 1
        assert self.h[-1] == 1

    def red(self, c):
        p, h, d = self.p, self.h, self.d
        c = [x % p for x in c]
        for i in range(len(c) - 1, d - 1, -1):
            v = c[i]
            if v:
                c[i] = 0
                for j in range(d):
                    c[i - d + j] = (c[i - d + j] - v * h[j]) % p
        c = c[:d] + [0] * (d - len(c))
        return Fq(c)

    def zero(self):
        return Fq((0,) * self.d)

    def one(self):
        return self.red([1])

    def const(self, k):
        return self.red([k])

    def gen(self):
        return self.red([0, 1] if self.d > 1 else [0])

    def add(self, x, y):
        p = self.p
        return Fq(tuple((a + b) % p for a, b in zip(x.c, y.c)))

    def sub(self, x, y):
        p = self.p
        return Fq(tuple((a - b) % p for a, b in zip(x.c, y.c)))

    def mul(self, x, y):
        p = self.p
        if not any(x.c) or not any(y.c):
            return self.zero()
        r = [0] * (2 * self.d - 1)
        for i, a in enumerate(x.c):
            if a:
                for j, b in enumerate(y.c):
                    if b:
                        r[i + j] = (r[i + j] + a * b) % p
        return self.red(r)

    def iszero(self, x):
        return not any(x.c)

    def inv(self, x):
        # extended Euclid in GF(p)[a]
        p = self.p
        a = list(x.c) + [0]
        while a and a[-1] == 0:
            a.pop()
        b = self.h[:]
        s0, s1 = [1], [0]

        def pdiv(u, v):
            u = u[:]
            q = [0] * max(1, len(u) - len(v) + 1)
            iv = pow(v[-1], p - 2, p)
            while len(u) >= len(v) and any(u):
                if u[-1] == 0:
                    u.pop()
                    continue
                c = u[-1] * iv % p
                sh = len(u) - len(v)
                q[sh] = c
                for i in range(len(v)):
                    u[sh + i] = (u[sh + i] - c * v[i]) % p
                while u and u[-1] == 0:
                    u.pop()
            return q, u

        def psub(u, v):
            n = max(len(u), len(v))
            u = u + [0] * (n - len(u))
            v = v + [0] * (n - len(v))
            return [(a - b) % p for a, b in zip(u, v)]

        def pmul(u, v):
            r = [0] * (len(u) + len(v) - 1)
            for i, aa in enumerate(u):
                if aa:
                    for j, bb in enumerate(v):
                        if bb:
                            r[i + j] = (r[i + j] + aa * bb) % p
            return r
        A, B = a, b
        SA, SB = s0, s1
        while any(B):
            Qq, R = pdiv(A, B)
            A, B = B, R
            SA, SB = SB, psub(SA, pmul(Qq, SB))
        ic = pow(A[-1], p - 2, p)
        return self.red([v * ic % p for v in SA])


# ------------------------------------------------------- generic linear algebra
def rref_F(K, M):
    M = [row[:] for row in M]
    rows = len(M)
    cols = len(M[0])
    piv = []
    r = 0
    for c in range(cols):
        pr = None
        for i in range(r, rows):
            if not K.iszero(M[i][c]):
                pr = i
                break
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        iv = K.inv(M[r][c])
        M[r] = [K.mul(x, iv) for x in M[r]]
        for i in range(rows):
            if i != r and not K.iszero(M[i][c]):
                f = M[i][c]
                M[i] = [K.sub(M[i][j], K.mul(f, M[r][j])) for j in range(cols)]
        piv.append(c)
        r += 1
        if r == rows:
            break
    return M, piv


def nullspace_F(K, A):
    n = len(A[0])
    R, piv = rref_F(K, A)
    out = []
    for fc in [c for c in range(n) if c not in piv]:
        v = [K.zero()] * n
        v[fc] = K.one()
        for i, pc in enumerate(piv):
            v[pc] = K.sub(K.zero(), R[i][fc])
        out.append(v)
    return out


def solve_affine_F(K, A, b):
    n = len(A[0])
    aug = [A[i][:] + [b[i]] for i in range(len(A))]
    R, piv = rref_F(K, aug)
    if n in piv:
        return None
    x = [K.zero()] * n
    for i, pc in enumerate(piv):
        x[pc] = R[i][n]
    return x


# --------------------------------------------------------------- the cascade
def partial_F(K, poly, val, free):
    fidx = [PIDX[v] for v in free]
    out = {}
    for m, c in poly.items():
        term = K.const(c)
        for i, e in enumerate(m):
            if e and i not in fidx:
                for _ in range(e):
                    term = K.mul(term, val[PVARS[i]])
        if K.iszero(term):
            continue
        key = tuple(m[i] for i in fidx)
        out[key] = K.add(out.get(key, K.zero()), term)
    return {k: v for k, v in out.items() if not K.iszero(v)}


def fstr(x, p):
    return "(" + "+".join(f"{v}*a^{i}" if i else str(v)
                          for i, v in enumerate(x.c) if v) + ")" \
        if any(x.c) else "0"
