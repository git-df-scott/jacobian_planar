"""
ITEM 1 -- the residual cascade above a w=-4 solution, as exact linear algebra.

Given a solution of the w = -4 block (the (C,G) piece), the rest of the case-(2)
system is a chain of LINEAR problems, which is what makes the residual tractable:

    w = -3 : 18 equations, HOMOGENEOUS linear in (B, F)      19 unknowns
    w = -2 : 19 equations, affine linear in (A, E)           21 unknowns
             (its inhomogeneous part is quadratic in (B,F))
    w = -1 : 19 equations, affine linear in D                13 unknowns, of
             which d_0_0 does not occur -> the "residual 13-variable system"
    w =  0 : 19 equations, bilinear in (A,B,D,E), no new unknowns -> a check

That block structure is not assumed: build_block() reads each equation from the
JSON and REFUSES to proceed unless the equation really is affine of degree <= 1
in the block's unknowns, so a wrong structural belief cannot pass silently.

All arithmetic is over F_p with p = 1 (mod 3).  Every routine here is exact.
"""

import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w4_case2_system as S

VARS, NONZERO, EQS, META, CHASH = S.load()
BYW = S.split_by_weight(EQS)

PIECE = {}
for v in VARS:
    w = S.var_weight(v)
    PIECE[v] = ({0: "A", -1: "B", -2: "C"} if v.startswith("c_")
                else {0: "D", -1: "E", -2: "F", -3: "G"})[w]
OF = {L: [v for v in VARS if PIECE[v] == L] for L in "ABCDEFG"}


def cf(fr, p):
    return (fr.numerator % p) * pow(fr.denominator % p, p - 2, p) % p


def build_block(w, unknown_letters, known, p):
    """(M, rhs, cols): the block's equations as M * unknowns = rhs over F_p.

    `known` maps every variable NOT in unknown_letters to its value in F_p.
    Raises if any equation is not affine-linear in the unknowns.
    """
    cols = [v for L in unknown_letters for v in OF[L]]
    colidx = {v: k for k, v in enumerate(cols)}
    M, rhs = [], []
    for idx in BYW[w]:
        row = [0] * len(cols)
        const = 0
        for c, m in S.eq_terms(EQS[idx]):
            coef = cf(c, p)
            unk = [v for v in m if v in colidx]
            deg = sum(m[v] for v in unk)
            if deg > 1:
                raise SystemExit(f"w={w} equation {idx} is degree {deg} in "
                                 f"{unknown_letters}: {m}")
            for v in m:
                if v in colidx:
                    continue
                if v not in known:
                    raise SystemExit(f"w={w} equation {idx} uses unknown {v}")
                coef = coef * pow(known[v], m[v], p) % p
            if deg == 0:
                const = (const + coef) % p
            else:
                row[colidx[unk[0]]] = (row[colidx[unk[0]]] + coef) % p
        M.append(row)
        rhs.append((-const) % p)
    return M, rhs, cols


def rref(M, rhs, p):
    """Exact row reduction over F_p.  Returns (R, r, pivots, consistent)."""
    A = [row[:] + [rhs[i]] for i, row in enumerate(M)]
    nr, nc = len(A), len(M[0]) if M else 0
    piv, r = [], 0
    for c in range(nc):
        sel = None
        for i in range(r, nr):
            if A[i][c] % p:
                sel = i
                break
        if sel is None:
            continue
        A[r], A[sel] = A[sel], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [v * inv % p for v in A[r]]
        for i in range(nr):
            if i != r and A[i][c] % p:
                f = A[i][c]
                A[i] = [(A[i][k] - f * A[r][k]) % p for k in range(nc + 1)]
        piv.append(c)
        r += 1
        if r == nr:
            break
    consistent = all(any(A[i][c] % p for c in range(nc)) or A[i][nc] % p == 0
                     for i in range(nr))
    return A, r, piv, consistent


def solve_block(M, rhs, p):
    """(consistent, rank, nullity, particular, basis) over F_p."""
    if not M:
        return True, 0, 0, [], []
    A, r, piv, cons = rref(M, rhs, p)
    n = len(M[0])
    if not cons:
        return False, r, None, None, None
    part = [0] * n
    for i, c in enumerate(piv):
        part[c] = A[i][n] % p
    free = [c for c in range(n) if c not in piv]
    basis = []
    for fcol in free:
        vec = [0] * n
        vec[fcol] = 1
        for i, c in enumerate(piv):
            vec[c] = (-A[i][fcol]) % p
        basis.append(vec)
    return True, r, len(free), part, basis
