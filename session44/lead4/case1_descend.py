#!/usr/bin/env python3
"""Full (2,-1)-weight descent for subcase 1 from a pinned essential face.

Level W of  sum_{w1+w2=W+1} [P_w1, Q_w2] = delta_{W,4} x^2  has exactly two
NEW unknown slices, P_{W-2} and Q_{W-1}, and they enter LINEARLY through
L_W(p,q) = [face P, q] + [p, face Q].  So the whole problem is a linear
cascade over F_p with a growing set of free parameters:

   at each W: solve L_W z = RHS_known(t)   (RHS quadratic in earlier slices)
              pivot unknowns  -> polynomials in the accumulated parameters t
              free unknowns   -> new parameters t
              cokernel rows   -> POLYNOMIAL CONDITIONS on t

Ranks (case1_ranks.py) give 9 free parameters in total against 150 cokernel
rows, so the conditions are heavily overdetermined.  This module accumulates
them and hands the ideal to Singular after every level, stopping as soon as
it contains 1 (that cover is then EMPTY over F_p).
"""
import subprocess
import sys

from case1_cascade import SP, SQ, base
from case1_point import find
from case1_ranks import level_range

# ---------- sparse multivariate polynomials over F_p ----------
class Ring:
    def __init__(self, p):
        self.p = p
        self.nv = 0

    def var(self):
        i = self.nv
        self.nv += 1
        return {(i,): 1}

    def const(self, c):
        c %= self.p
        return {} if c == 0 else {(): c}

    def add(self, A, B):
        C = dict(A)
        for m, c in B.items():
            v = (C.get(m, 0) + c) % self.p
            if v:
                C[m] = v
            else:
                C.pop(m, None)
        return C

    def scal(self, A, c):
        c %= self.p
        if c == 0:
            return {}
        return {m: (v * c) % self.p for m, v in A.items()}

    def mul(self, A, B):
        C = {}
        for m1, c1 in A.items():
            for m2, c2 in B.items():
                m = tuple(sorted(m1 + m2))
                v = (C.get(m, 0) + c1 * c2) % self.p
                if v:
                    C[m] = v
                else:
                    C.pop(m, None)
        return C

    def deg(self, A):
        return max((len(m) for m in A), default=0)

    def s(self, A, names):
        if not A:
            return "0"
        out = []
        for m, c in sorted(A.items()):
            t = str(c)
            for i in set(m):
                e = m.count(i)
                t += "*" + names[i] + ("^%d" % e if e > 1 else "")
            out.append(t)
        return "+".join(out)


def rref(mat, ncol, p):
    """returns (R, T, pivots) with T*mat = R in reduced row echelon form."""
    nrow = len(mat)
    A = [list(mat[r]) + [1 if k == r else 0 for k in range(nrow)]
         for r in range(nrow)]
    piv = []
    r0 = 0
    for c in range(ncol):
        pr = None
        for r in range(r0, nrow):
            if A[r][c] % p:
                pr = r
                break
        if pr is None:
            continue
        A[r0], A[pr] = A[pr], A[r0]
        inv = pow(A[r0][c], -1, p)
        A[r0] = [(v * inv) % p for v in A[r0]]
        for r in range(nrow):
            if r != r0 and A[r][c] % p:
                f = A[r][c]
                A[r] = [(A[r][k] - f * A[r0][k]) % p
                        for k in range(ncol + nrow)]
        piv.append(c)
        r0 += 1
    R = [row[:ncol] for row in A]
    T = [row[ncol:] for row in A]
    return R, T, piv


def run(p, which, verbose=True, stop_on_empty=True):
    r, err = find(p, which)
    if err:
        return None, err
    av, f, g, bad, nr = r
    assert not bad
    RG = Ring(p)
    Pw = {2: [RG.const(c) for c in f]}
    Qw = {3: [RG.const(c) for c in g]}
    params = []
    conds = []
    log = []

    for W in range(3, -22, -1):
        rng = level_range(W)
        if rng is None:
            continue
        lo, hi = rng
        n = hi - lo + 1
        rhs = [dict() for _ in range(n)]
        # known contributions
        for w1 in sorted(Pw):
            w2 = W + 1 - w1
            if w2 not in Qw:
                continue
            if w1 == 2 and w2 == W - 1:
                continue
            if w1 == W - 2 and w2 == 3:
                continue
            a, b, _ = base(SP, w1)
            c, d, _ = base(SQ, w2)
            ph, ps = Pw[w1], Qw[w2]
            for i, ci in enumerate(ph):
                if not ci:
                    continue
                for j, cj in enumerate(ps):
                    if not cj:
                        continue
                    co = ((a * d - b * c) + w1 * j - w2 * i) % p
                    if co == 0:
                        continue
                    I = a + c - 1 + i + j
                    rhs[I - lo] = RG.add(rhs[I - lo],
                                         RG.scal(RG.mul(ci, cj), co))
        if W == 4:
            pass
        # linear operator columns
        cols, tag = [], []
        if (W - 2) in SP and W - 2 <= 1:
            a1, b1, kp = base(SP, W - 2)
            for k in range(kp):
                col = [0] * n
                for j, bj in enumerate(g):
                    co = ((a1 - 2 * b1) + (W - 2) * j - 3 * k) % p
                    I = a1 + 1 + k + j
                    col[I - lo] = (col[I - lo] + co * bj) % p
                cols.append(col)
                tag.append(("P", W - 2, k))
        if (W - 1) in SQ and W - 1 <= 2:
            c1, d1, kq = base(SQ, W - 1)
            for k in range(kq):
                col = [0] * n
                for i, ai in enumerate(f):
                    co = (d1 + 2 * k - (W - 1) * i) % p
                    I = c1 + i + k
                    col[I - lo] = (col[I - lo] + co * ai) % p
                cols.append(col)
                tag.append(("Q", W - 1, k))
        ncol = len(cols)
        mat = [[cols[c][r] for c in range(ncol)] for r in range(n)]
        R, T, piv = rref(mat, ncol, p) if ncol else ([[] for _ in range(n)],
                                                     [[1 if k == r else 0
                                                       for k in range(n)]
                                                      for r in range(n)], [])
        # transformed RHS:  L z = -rhs
        trhs = []
        for r in range(n):
            acc = {}
            for k in range(n):
                if T[r][k] % p:
                    acc = RG.add(acc, RG.scal(rhs[k], -T[r][k]))
            trhs.append(acc)
        newc = [trhs[r] for r in range(len(piv), n) if trhs[r]]
        conds.extend(newc)
        # solve: free columns become new parameters
        z = [None] * ncol
        free = [c for c in range(ncol) if c not in piv]
        for c in free:
            v = RG.var()
            params.append(v)
            z[c] = v
        for idx, c in enumerate(piv):
            acc = dict(trhs[idx])
            for c2 in free:
                if R[idx][c2] % p:
                    acc = RG.add(acc, RG.scal(z[c2], -R[idx][c2]))
            z[c] = acc
        # install
        for c in range(ncol):
            kind, w, k = tag[c]
            tgt = Pw if kind == "P" else Qw
            if w not in tgt:
                sz = len(SP[w]) if kind == "P" else len(SQ[w])
                tgt[w] = [dict() for _ in range(sz)]
            tgt[w][k] = z[c]
        maxdeg = max([RG.deg(c) for c in newc], default=0)
        log.append((W, n, ncol, len(piv), len(free), len(newc), maxdeg,
                    len(params), len(conds)))
        if verbose:
            print("W=%4d eqs %3d unk %3d rank %3d newparams %d "
                  "newconds %2d (deg<=%d)  params %d conds %d"
                  % (W, n, ncol, len(piv), len(free), len(newc), maxdeg,
                     len(params), len(conds)), flush=True)
        if newc and stop_on_empty:
            v = decide(conds, len(params), p, RG)
            if verbose:
                print("      ideal after this level: %s" % v, flush=True)
            if v == "CONTAINS 1":
                return ("EMPTY", W, len(conds), len(params)), None
    return ("SURVIVES", None, len(conds), len(params)), None


def decide(conds, nv, p, RG):
    if not conds:
        return "trivial"
    names = ["t%d" % (i + 1) for i in range(max(nv, 1))]
    src = ["ring R = %d, (%s), dp;" % (p, ",".join(names)),
           "ideal I = " + ",\n".join(RG.s(c, names) for c in conds) + ";",
           "ideal G = std(I);",
           'if (size(G)==1 && G[1]==1) { "CONTAINS 1"; } else '
           '{ "dim " + string(dim(G)); }', "quit;"]
    open("_scratch_case1/dec.sing", "w").write("\n".join(src))
    pr = subprocess.run(["Singular", "-q", "_scratch_case1/dec.sing"],
                        capture_output=True, text=True, timeout=1800)
    return pr.stdout.strip().splitlines()[-1] if pr.stdout.strip() else "?"


if __name__ == "__main__":
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 10007
    which = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    res, err = run(p, which)
    print("\nRESULT:", res if res else err)
