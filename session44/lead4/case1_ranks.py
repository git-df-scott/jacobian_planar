#!/usr/bin/env python3
"""Ranks of the (2,-1)-cascade operator L_W for subcase 1, at an explicit
point of the essential-face variety.

    L_W(p, q) = [face(P), q] + [p, face(Q)]

with p = P_{W-2} (supported on N(P)'s slice 2i-j = W-2) and q = Q_{W-1}
(supported on N(Q)'s slice 2i-j = W-1) -- exactly the unknowns that ENTER
LINEARLY at level W of

    sum_{w1+w2 = W+1} [P_w1, Q_w2] = delta_{W,4} x^2 .

Using face(P) = x f(u), face(Q) = x^2 y g(u) and
[x^a y^b phi, x^c y^d psi] = x^{a+c-1}y^{b+d-1}[(ad-bc)phi psi
                                + (2a-b) u phi psi' - (2c-d) u phi' psi]:

  [face(P), q] = x^{c} y^{d-1} [ d f psi + 2 u f psi' - (W-1) u f' psi ]
  [p, face(Q)] = x^{a+1} y^{b} [ (a-2b) phi g + (W-2) u phi g' - 3 u phi' g ]

coker L_W > 0 means level W imposes conditions that must be absorbed by the
free parameters accumulated at higher levels; coker L_W = 0 means level W is
unobstructed whatever came before.
"""
import sys
from case1_cascade import SP, SQ, base
from case1_point import find

P = 10007


def rank_mod(rows, ncols, p):
    m = [r[:] for r in rows]
    r0 = 0
    for c in range(ncols):
        pr = None
        for r in range(r0, len(m)):
            if m[r][c] % p:
                pr = r
                break
        if pr is None:
            continue
        m[r0], m[pr] = m[pr], m[r0]
        inv = pow(m[r0][c], -1, p)
        m[r0] = [(v * inv) % p for v in m[r0]]
        for r in range(len(m)):
            if r != r0 and m[r][c] % p:
                f = m[r][c]
                m[r] = [(m[r][k] - f * m[r0][k]) % p for k in range(ncols)]
        r0 += 1
    return r0


def level_range(W):
    """index range [lo,hi] of x-exponents of ALL contributions at level W."""
    xs = []
    for w1 in SP:
        w2 = W + 1 - w1
        if w2 not in SQ:
            continue
        a, b, kp = base(SP, w1)
        c, d, kq = base(SQ, w2)
        lo = a + c - 1
        xs.append((lo, lo + (kp - 1) + (kq - 1)))
    if not xs:
        return None
    return min(v[0] for v in xs), max(v[1] for v in xs)


def LW(W, f, g, p):
    """matrix of L_W: rows indexed by x-exponent, cols by (phi_k then psi_k)"""
    rng = level_range(W)
    if rng is None:
        return None
    lo, hi = rng
    nrow = hi - lo + 1
    cols = []
    if (W - 2) in SP and W - 2 <= 1:
        a1, b1, kp = base(SP, W - 2)
        for k in range(kp):
            col = [0] * nrow
            for j, bj in enumerate(g):
                n = k + j
                coef = (a1 - 2 * b1) + (W - 2) * j - 3 * k
                I = (a1 + 1) + n
                if lo <= I <= hi:
                    col[I - lo] = (col[I - lo] + coef * bj) % p
                elif coef * bj % p:
                    raise AssertionError("out of range %d %d" % (W, I))
            cols.append(col)
    if (W - 1) in SQ and W - 1 <= 2:
        c1, d1, kq = base(SQ, W - 1)
        for k in range(kq):
            col = [0] * nrow
            for i, ai in enumerate(f):
                n = i + k
                coef = d1 + 2 * k - (W - 1) * i
                I = c1 + n
                if lo <= I <= hi:
                    col[I - lo] = (col[I - lo] + coef * ai) % p
                elif coef * ai % p:
                    raise AssertionError("out of range %d %d" % (W, I))
            cols.append(col)
    if not cols:
        return (nrow, 0, 0)
    rows = [[cols[c][r] for c in range(len(cols))] for r in range(nrow)]
    return (nrow, len(cols), rank_mod(rows, len(cols), p))


if __name__ == "__main__":
    p = int(sys.argv[1]) if len(sys.argv) > 1 else P
    which = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    r, err = find(p, which)
    if err:
        print("no point:", err)
        sys.exit(1)
    av, f, g, bad, nr = r
    assert not bad
    print("point on the essential-face variety mod %d (cover %d of %d rational)"
          % (p, which, nr))
    print("  f =", f)
    print("  g =", g)
    print("\n W   #eqs  #new-unknowns  rank  dim ker  dim coker")
    tk = tc = 0
    for W in range(3, -22, -1):
        out = LW(W, f, g, p)
        if out is None:
            continue
        nrow, ncol, rk = out
        ker, cok = ncol - rk, nrow - rk
        tk += ker
        tc += cok
        print("%4d  %4d  %8d      %5d %7d %9d" % (W, nrow, ncol, rk, ker, cok))
    print("\n  total kernel dimensions  (free parameters added) :", tk)
    print("  total cokernel dimensions (conditions imposed)   :", tc)
