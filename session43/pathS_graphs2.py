"""Session 43 — non-linear slices Sigma = C^2, on the CORRECTED machinery.

pathS_graphs.py is WITHDRAWN: it ran on the buggy chi (mod-p majority voting for
fibre counts) and reported chi(A_Sigma) = -167, -258 for the derived family.  The
exact values are -3, -4, -5 -- the old numbers were simply wrong.  The verdict
(the family fails) survives, but far more narrowly than reported, so the family
is re-examined here rather than trusted.

Recall the filter, valid for EVERY Sigma = C^2 (only chi(Sigma) = 1 was used):

    chi(S) = 3 - 2 chi(A_Sigma) - #C_Sigma ,     S = C^2  ==>  2 chi + #C = 2

so (#C, chi) must be (0, 1) or (2, 0)  [#C must be even].

BRANCH #C = 0 IS NOW CLOSED for the graph family {w2 = g(w1,w3)}:
  * missing C_sing forces g = 9 w1 w3 + h with the monomials of h on a single
    line j - 2i = m (that is what cancels the pole of w2 = 4/(3t) along C_sing);
  * chi = 1 needs ONE place at infinity; the top form of Delta|_Sigma is
    (9w1w3 + h_d)^3 w3, so for deg h < 3 there are always >= 2 points at
    infinity, and an irreducible curve with s >= 2 places has chi = 2-2g-s <= 0,
    never 1;
  * for deg h = d >= 3 the single-weight-line condition with i+j <= d forces
    i = 0, j = d, i.e. h = c w3^d exactly, and then the top form is c^3 w3^(3d+1)
    -- ONE place at infinity, as required -- but the exact Euler characteristic
    is chi(A_Sigma) = -d <= -3, never 1.
  So no graph in this family has (#C, chi) = (0, 1).

THIS FILE searches the remaining branch, #C_Sigma = 2 with chi(A_Sigma) = 0,
across all three graph families, with the calibrated instruments of chi_exact.py.
"""
import sys
import sympy as sp
from itertools import product

sys.path.insert(0, __file__.rsplit('/', 1)[0])
import chi_exact as CE

w1, w2, w3, t = sp.symbols('w1 w2 w3 t')
DELTA = sp.expand(27*w1**2*w3**2 - 18*w1*w2*w3 + w2**3*w3 + 16*w1 - w2**2)
CS = {w1: sp.Rational(4, 27)/t**2, w2: sp.Rational(4, 3)/t, w3: t}


def n_Csing_graph(solve_for, g):
    """#(Sigma n C_sing) where Sigma = {solve_for = g(other two)}."""
    e = sp.together(sp.expand(g.subs(CS) - CS[solve_for]))
    num = sp.expand(sp.numer(e))
    if num == 0:
        return sp.oo
    p = sp.Poly(num, t)
    if p.degree() < 1:
        return 0
    sq = sp.Poly(sp.quo(p, sp.gcd(p, p.diff(t))), t)
    n = sq.degree()
    if sq.eval(0) == 0:
        n -= 1
    return n


def A_sigma(solve_for, g, params):
    cut = sp.expand(DELTA.subs(solve_for, g))
    cut = sp.expand(sp.numer(sp.together(cut)))
    return sp.expand(cut.subs({params[0]: CE.U, params[1]: CE.V}, simultaneous=True))


def examine(solve_for, g, params, label, quiet=True):
    try:
        nC = n_Csing_graph(solve_for, g)
        if nC is sp.oo or nC % 2 == 1:
            return None
        cut = A_sigma(solve_for, g, params)
        if not sp.sympify(cut).free_symbols:
            return None
        if sp.Poly(cut, CE.U, CE.V).total_degree() > 14:
            return None                                  # keep it exact and fast
        chiA = CE.chi_plane_curve(cut)
        chiS = 3 - 2*chiA - nC
        if chiS != 1:
            return ('miss', nC, chiA, chiS)
        comps = [b for b, _m in sp.factor_list(cut)[1] if b.free_symbols]
        bad = [c for c in comps if CE.is_A1(c)]
        print("   %-34s #C=%s chi(A)=%s chi(S)=1  %s"
              % (label, nC, chiA, "CHAU-FAIL" if bad else "*** SURVIVES chi+Chau ***"))
        return ('hit', nC, chiA, bad)
    except Exception as e:
        return ('err', type(e).__name__, str(e)[:40], None)


if __name__ == '__main__':
    POOL = [0, 1, -1, 2, -2, sp.Rational(1, 2), 3, sp.Rational(1, 3), -3]
    hits, tally = [], {}

    print("family A:  Sigma = { w2 = g(w1,w3) }")
    MONS = [(0, 0), (0, 1), (1, 0), (1, 1), (0, 2), (2, 0), (1, 2), (2, 1)]
    for m1, m2 in [(a, b) for i, a in enumerate(MONS) for b in MONS[i:]]:
        for c1, c2 in product(POOL, repeat=2):
            if c1 == 0 and c2 == 0:
                continue
            g = c1*w1**m1[0]*w3**m1[1] + c2*w1**m2[0]*w3**m2[1]
            r = examine(w2, g, (w1, w3), "w2 = %s" % g)
            if r:
                tally[r[0]] = tally.get(r[0], 0) + 1
                if r[0] == 'hit' and not r[3]:
                    hits.append((w2, g))

    print("\nfamily B:  Sigma = { w1 = g(w2,w3) }")
    for m1, m2 in [(a, b) for i, a in enumerate(MONS) for b in MONS[i:]]:
        for c1, c2 in product(POOL, repeat=2):
            if c1 == 0 and c2 == 0:
                continue
            g = c1*w2**m1[0]*w3**m1[1] + c2*w2**m2[0]*w3**m2[1]
            r = examine(w1, g, (w2, w3), "w1 = %s" % g)
            if r:
                tally[r[0]] = tally.get(r[0], 0) + 1
                if r[0] == 'hit' and not r[3]:
                    hits.append((w1, g))

    print("\nfamily C:  Sigma = { w3 = g(w1,w2) }")
    for m1, m2 in [(a, b) for i, a in enumerate(MONS) for b in MONS[i:]]:
        for c1, c2 in product(POOL, repeat=2):
            if c1 == 0 and c2 == 0:
                continue
            g = c1*w1**m1[0]*w2**m1[1] + c2*w1**m2[0]*w2**m2[1]
            r = examine(w3, g, (w1, w2), "w3 = %s" % g)
            if r:
                tally[r[0]] = tally.get(r[0], 0) + 1
                if r[0] == 'hit' and not r[3]:
                    hits.append((w3, g))

    print("\n" + "=" * 66)
    print("outcome tally:", tally)
    print("Sigma surviving chi(S)=1 AND the Chau filter:", len(hits))
    for s, g in hits:
        print("    %s = %s" % (s, g))
