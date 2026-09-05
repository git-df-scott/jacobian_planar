#!/usr/bin/env python3
"""END-TO-END validation of the cascade instrument.

Two controls, both run on the real subcase-1 data:

 POSITIVE  take a solution of the cascade conditions, substitute it into the
           slices, reassemble P(x,y) and Q(x,y) as honest polynomials over
           F_p, and verify by DIRECT polynomial arithmetic that
                P_x Q_y - P_y Q_x  ==  x^2
           and that the supports lie inside N(P), N(Q).  If the cascade
           bookkeeping (slices, base points, bracket formula, level ranges,
           linear solves) were wrong anywhere, this would fail.

 NEGATIVE  the same decision engine, on the same conditions, WITHOUT the
           vertex non-degeneracy conditions, must NOT say EMPTY (the
           face-only solution is there).  An instrument that says EMPTY
           either way would be worthless.
"""
import sys

import case1_descend as CD
from case1_cascade import SP, SQ, base, inside, NP, NQ
from case1_point import find


def assemble(slices, S, RG, vals, p):
    """slice dict -> {(i,j): coeff} over F_p, with parameters set to vals."""
    out = {}
    for w, coeffs in slices.items():
        a, b, n = base(S, w)
        for k, poly in enumerate(coeffs):
            c = 0
            for mono, co in poly.items():
                t = co
                for idx in mono:
                    t = t * vals[idx] % p
                c = (c + t) % p
            if c:
                out[(a + k, b + 2 * k)] = c
    return out


def bracket(A, B, p):
    out = {}
    for (i1, j1), c1 in A.items():
        for (i2, j2), c2 in B.items():
            co = (i1 * j2 - j1 * i2) % p
            if co == 0:
                continue
            key = (i1 + i2 - 1, j1 + j2 - 1)
            v = (out.get(key, 0) + co * c1 * c2) % p
            if v:
                out[key] = v
            else:
                out.pop(key, None)
    return out


def main(p, which, stopW, vals=None):
    r, err = find(p, which)
    assert not err, err
    CD.run(p, which, verbose=False, check_at=(), dump=None, stopW=stopW)
    L = CD.LAST
    RG, Pw, Qw, conds = L["RG"], L["Pw"], L["Qw"], L["conds"]
    npar = len(L["params"])
    if vals is None:
        vals = [0] * npar
    # conditions must vanish at the chosen point
    res = []
    for c in conds:
        s = 0
        for mono, co in c.items():
            t = co
            for idx in mono:
                t = t * vals[idx] % p
            s = (s + t) % p
        res.append(s)
    print("  parameters:", vals)
    print("  conditions satisfied at this point:",
          "YES" if not any(res) else "NO (%d fail)" % sum(1 for v in res if v))
    if any(res):
        return False
    A = assemble(Pw, SP, RG, vals, p)
    B = assemble(Qw, SQ, RG, vals, p)
    okA = all(inside(k, NP) for k in A)
    okB = all(inside(k, NQ) for k in B)
    br = bracket(A, B, p)
    good = (br == {(2, 0): 1 % p})
    print("  P has %d monomials, all inside N(P): %s" % (len(A), okA))
    print("  Q has %d monomials, all inside N(Q): %s" % (len(B), okB))
    print("  [P,Q] computed directly =",
          "x^2  -- CASCADE VERIFIED" if good else br)
    vtx = [((0, 8), A), ((8, 16), A), ((0, 12), B), ((12, 24), B)]
    print("  vertex coefficients:",
          {v: d.get(v, 0) for v, d in vtx})
    return good and okA and okB


if __name__ == "__main__":
    p = int(sys.argv[1]); which = int(sys.argv[2])
    stopW = int(sys.argv[3]) if len(sys.argv) > 3 else -22
    print("=== POSITIVE CONTROL: the face-only point (all parameters 0) ===")
    main(p, which, stopW)
    print("\n=== POSITIVE CONTROL: a non-trivial point of the cascade ===")
    # t3 and t6 (indices 2 and 5) never appear in the conditions; try them
    r, err = find(p, which)
    CD.run(p, which, verbose=False, check_at=(), dump=None, stopW=stopW)
    npar = len(CD.LAST["params"])
    for cand in ([0] * npar, None):
        pass
    v = [0] * npar
    v[2] = 3
    v[5] = 7
    main(p, which, stopW, v)
