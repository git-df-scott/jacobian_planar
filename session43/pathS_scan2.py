"""Session 43 — the plane-slice scan, REDONE on the corrected machinery.

The first scan (pathS_scan.py) reported 7992 planes, 0 survivors.  That result
is WITHDRAWN and recomputed here, because the audit found three bugs, one of
which biases in the dangerous direction:

  BUG 5 (fatal)  pairwise-only inclusion-exclusion undercounts chi(A_W) whenever
                 three or more components share a point.  chi(S) = 3 - 2chi(A_W)
                 - #C_W, so an UNDERcount of chi(A_W) makes chi(S) too LARGE and
                 can wrongly REJECT a genuine candidate.  Recomputation is
                 mandatory, not cosmetic.
  BUG 6          points at infinity were counted over Q rather than over C.
  BUG 7          a component dividing B is a 1-DIMENSIONAL centre (S reducible,
                 hence disconnected since S is smooth), not an ordinary hit.

All chi computations now go through chi_exact.py, which is calibrated against 17
curves of independently known Euler characteristic (including three concurrent
lines, the configuration that broke the old code), 4 leading-form cases and 4
A^1 cases.  25/25 calibrations pass.
"""
import sys
import sympy as sp
from itertools import product

sys.path.insert(0, __file__.rsplit('/', 1)[0])
import chi_exact as CE
from pathS_modification import slice_AB, components

w1, w2, w3, t = sp.symbols('w1 w2 w3 t')
x, y = sp.symbols('x y')
DELTA = sp.expand(27*w1**2*w3**2 - 18*w1*w2*w3 + w2**3*w3 + 16*w1 - w2**2)


def plane_cut(a, b, c, k):
    if c != 0:
        sub, par = {w3: (k - a*w1 - b*w2)/c}, (w1, w2)
    elif b != 0:
        sub, par = {w2: (k - a*w1 - c*w3)/b}, (w1, w3)
    else:
        sub, par = {w1: (k - b*w2 - c*w3)/a}, (w2, w3)
    cut = sp.expand(sp.numer(sp.together(sp.expand(DELTA.subs(sub)))))
    return sp.expand(cut.subs({par[0]: CE.U, par[1]: CE.V}, simultaneous=True))


def n_Csing(a, b, c, k):
    """#(W n C_sing): distinct NONZERO roots of 27c t^3 - 27k t^2 + 36b t + 4a.
    (C_sing = (4/27t^2, 4/3t, t); substitute and clear 27t^2.)"""
    p = sp.Poly(27*c*t**3 - 27*k*t**2 + 36*b*t + 4*a, t)
    if p.as_expr() == 0:
        return sp.oo
    if p.degree() < 1:
        return 0
    sq = sp.Poly(sp.quo(p, sp.gcd(p, p.diff(t))), t)
    n = sq.degree()
    if sq.eval(0) == 0:
        n -= 1
    return n


def verdict(a, b, c, k):
    nC = n_Csing(a, b, c, k)
    if nC is sp.oo:
        return 'DEGENERATE', {}
    if nC % 2 == 1:
        return 'E-FAIL(odd #C_W)', dict(nC=nC)
    cut = plane_cut(a, b, c, k)
    if not sp.sympify(cut).free_symbols:
        return 'DEGENERATE(empty cut)', dict(nC=nC)
    chiA = CE.chi_plane_curve(cut)
    chiS = 3 - 2*chiA - nC
    info = dict(nC=nC, chiA=chiA, chiS=chiS, cut=sp.factor(cut))
    if chiS != 1:
        return 'E-FAIL(chi(S)=%s)' % chiS, info
    comps = [b_ for b_, _m in sp.factor_list(cut)[1] if b_.free_symbols]
    if any(CE.is_A1(c_) for c_ in comps):
        return 'C-FAIL(component = A^1)', info
    A, B = slice_AB(a, b, c, k)
    Bx = sp.expand(B.as_expr())
    hit = []
    for f, m in components(A):
        if Bx != 0 and sp.simplify(sp.rem(Bx, sp.expand(f), x)) == 0:
            return 'REDUCIBLE(1-dim centre)', info          # BUG 7
        G = sp.groebner([sp.expand(f), Bx], x, y, order='grevlex')
        hit.append(list(G.exprs) != [sp.Integer(1)])
    info['A'] = sp.factor(A.as_expr())
    info['hit'] = hit
    if not hit:
        return 'A CONSTANT (S = C^2 !!)', info
    if not all(hit):
        return 'H-FAIL(component not hit)', info
    return '*** SURVIVES ALL THREE ***', info


if __name__ == '__main__':
    vals = [0, 1, -1, 2, -2, 3, -3, sp.Rational(1, 2), sp.Rational(1, 3), 4]
    ks = [0, 1, -1, sp.Rational(-1, 4), 2, -2, sp.Rational(1, 3), 3]
    tally, survivors, chiS_hist = {}, [], {}
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
            if 'chiS' in info:
                chiS_hist[int(info['chiS'])] = chiS_hist.get(int(info['chiS']), 0) + 1
            if vd.startswith('***') or vd.startswith('A CONSTANT'):
                survivors.append((a, b, c, k, vd, info))
    print("planes scanned:", sum(tally.values()))
    for kk in sorted(tally, key=lambda s: -tally[s]):
        print("   %-30s %5d" % (kk, tally[kk]))
    print("\nchi(S) histogram (planes reaching the chi computation):",
          dict(sorted(chiS_hist.items())))
    print("\nSURVIVORS:", len(survivors))
    for s in survivors:
        print("   (a,b,c,k)=(%s,%s,%s,%s)  %s" % (s[0], s[1], s[2], s[3], s[4]))
        print("      A_W =", s[5].get('cut'), "  chi(A_W)=", s[5].get('chiA'),
              " #C_W=", s[5].get('nC'))
