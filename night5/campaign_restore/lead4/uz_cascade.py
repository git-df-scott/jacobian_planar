#!/usr/bin/env python3
"""Explicit cascade solve of the (u,z) obstruction system over GF(p).

Layer structure (verified by inspecting the obstruction supports):

    (n,4), n=13..18   6 equations  in q2..q8 only
    (n,3), n=13..19   7 equations  LINEAR homogeneous in p1..p8 over Q[q]
    (n,2), n=13..19   7 equations  LINEAR in f1..f8, quadratic in p
    (n,1), n=13..19   7 equations
    (n,0), n= 2..19  18 equations

So: solve the q-layer (0-dimensional after a gauge), then for each q solve
a linear system for p, then a linear system for f, then check the rest.
Everything is explicit -- no Groebner basis on the big system is needed.
"""
import itertools
import random
import sys

from uz_eliminate import run
from uz_system import PVARS, PIDX

MOD = 65521


def obstructions(mod):
    obs, _ = run(mod=mod, fixed={}, verbose=False)
    return dict(obs)


def evalpoly(poly, val, mod):
    """val: dict varname -> int (missing = symbolic not allowed)"""
    tot = 0
    for m, c in poly.items():
        term = c
        for i, e in enumerate(m):
            if e:
                term = term * pow(val[PVARS[i]], e, mod) % mod
        tot = (tot + term) % mod
    return tot


def partial(poly, val, mod, free):
    """evaluate poly at `val` for all variables outside `free`; return a dict
    monomial-in-free-vars -> coefficient."""
    fidx = [PIDX[v] for v in free]
    out = {}
    for m, c in poly.items():
        term = c
        for i, e in enumerate(m):
            if e and i not in fidx:
                term = term * pow(val[PVARS[i]], e, mod) % mod
        if term % mod == 0:
            continue
        key = tuple(m[i] for i in fidx)
        out[key] = (out.get(key, 0) + term) % mod
        if out[key] == 0:
            del out[key]
    return out


# ------------------------------------------------------------ linear algebra
def rref(M, mod):
    M = [row[:] for row in M]
    rows, cols = len(M), len(M[0])
    piv = []
    r = 0
    for c in range(cols):
        pr = None
        for i in range(r, rows):
            if M[i][c] % mod:
                pr = i
                break
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        inv = pow(M[r][c], mod - 2, mod)
        M[r] = [x * inv % mod for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c] % mod:
                f = M[i][c]
                M[i] = [(M[i][j] - f * M[r][j]) % mod for j in range(cols)]
        piv.append(c)
        r += 1
        if r == rows:
            break
    return M, piv


def nullspace(A, mod):
    """A: list of rows, homogeneous. Return a basis of the kernel."""
    if not A:
        n = 0
        return []
    n = len(A[0])
    R, piv = rref(A, mod)
    free = [c for c in range(n) if c not in piv]
    basis = []
    for fc in free:
        v = [0] * n
        v[fc] = 1
        for i, pc in enumerate(piv):
            v[pc] = (-R[i][fc]) % mod
        basis.append(v)
    return basis


def solve_affine(A, b, mod):
    """A x = b.  Return (particular, kernel basis) or None."""
    n = len(A[0])
    aug = [A[i][:] + [b[i] % mod] for i in range(len(A))]
    R, piv = rref(aug, mod)
    if n in piv:
        return None                       # inconsistent
    x = [0] * n
    for i, pc in enumerate(piv):
        x[pc] = R[i][n]
    ker = nullspace([row[:n] for row in A], mod)
    return x, ker
