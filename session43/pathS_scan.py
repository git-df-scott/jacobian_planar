"""Session 43, Path S — the combined exact scan over plane slices.

Three INDEPENDENT exact necessary conditions for S = F^{-1}(W) to be C^2:

  (E)  Euler:  chi(S) = 3 - 2 chi(A_W) - #C_W = 1,  i.e.  2 chi(A_W) + #C_W = 2.
       In particular #C_W must be EVEN; a plane meeting Sing(Delta) in 3 distinct
       points -- the GENERIC behaviour -- is excluded outright.
  (C)  Chau / Abhyankar-Moh: no component of the non-properness set A_W of the
       induced planar map may be isomorphic to A^1.
  (H)  H_1: S = (C^2 \ {A=0}) u (a line over each point of {A=B=0}), so
       H_1(S) = Z^r / <meridians of components that are hit>; every irreducible
       component of {A=0} must contain a point of {A=B=0}.

Run: python3 session43/pathS_scan.py
"""
import sympy as sp
from itertools import product

import pathS_chi as CH
from pathS_modification import slice_AB, components, meets

u, v = CH.u, CH.v


def verdict(a, b, c, k):
    nC = CH.n_Csing(a, b, c, k)
    if nC is sp.oo:
        return 'DEGENERATE', {}
    if nC % 2 == 1:
        return 'E-FAIL(odd #C_W)', dict(nC=nC)
    cut = CH.plane_cut(a, b, c, k)
    chiA = CH.chi_curve(cut)
    if chiA is None:
        return 'DEGENERATE', dict(nC=nC)
    chiS = 3 - 2*chiA - nC
    info = dict(nC=nC, chiA=chiA, chiS=chiS, cut=sp.factor(cut))
    if chiS != 1:
        return 'E-FAIL(chi(S)=%s)' % chiS, info
    comps = [b_ for b_, _m in sp.factor_list(cut)[1] if b_.free_symbols]
    if any(CH.is_isomorphic_to_A1(c_, u, v) for c_ in comps):
        return 'C-FAIL(component = A^1)', info
    A, B = slice_AB(a, b, c, k)
    hit = [(f, m, meets(f, B)[0]) for f, m in components(A)]
    info['A'] = sp.factor(A.as_expr())
    info['hit'] = hit
    if not hit:
        return 'A CONSTANT (S = C^2 !!)', info
    if any(h is True and sp.expand(B.as_expr()) == 0 for _f, _m, h in hit):
        return 'REDUCIBLE(1-dim centre)', info
    if not all(h for _f, _m, h in hit):
        return 'H-FAIL(component not hit)', info
    return '*** SURVIVES ALL THREE ***', info


if __name__ == '__main__':
    vals = [0, 1, -1, 2, -2, 3, -3, sp.Rational(1, 2), sp.Rational(1, 3), 4]
    ks = [0, 1, -1, sp.Rational(-1, 4), 2, -2, sp.Rational(1, 3), 3]
    tally, survivors = {}, []
    for a, b, c in product(vals, repeat=3):
        if (a, b, c) == (0, 0, 0):
            continue
        for k in ks:
            try:
                vd, info = verdict(a, b, c, k)
            except Exception as e:
                vd, info = 'ERROR(%s)' % type(e).__name__, {}
            key = vd.split('(')[0]
            tally[key] = tally.get(key, 0) + 1
            if vd.startswith('***') or vd.startswith('A CONSTANT'):
                survivors.append((a, b, c, k, vd, info))
    total = sum(tally.values())
    print("planes scanned:", total)
    for kk in sorted(tally, key=lambda s: -tally[s]):
        print("   %-28s %5d" % (kk, tally[kk]))
    print("\nSURVIVORS:", len(survivors))
    for s in survivors:
        print("   ", s[:5])
