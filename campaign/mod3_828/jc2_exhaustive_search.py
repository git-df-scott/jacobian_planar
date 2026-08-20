"""
Plane Jacobian campaign - Session 20
DIRECT EXHAUSTIVE SEARCH FOR A JC2 COUNTEREXAMPLE AT SMALL DEGREE.

TARGET (exact, thanks to Jung-van der Kulk):

    find P, Q in Q[x,y] with  J(P,Q) = Px Qy - Py Qx = 1
    and  deg P does not divide deg Q,  deg Q does not divide deg P.

Every automorphism of C^2 is tame (Jung-van der Kulk), and a tame automorphism
has one degree dividing the other.  So ANY Keller pair with non-dividing degrees
IS a counterexample -- no separate automorphism test is needed.

REDUCTIONS USED (each a theorem, not a guess):
 R1  Leading forms.  J(P,Q) = 1 forces J(Pbar,Qbar) = 0, hence
     Pbar^d2 = c Qbar^d1, hence Pbar = alpha h^b, Qbar = beta h^a with
     n = gcd(d1,d2), b = d1/n, a = d2/n, deg h = n.   (verified in
     jc2_cusp_from_degrees.py)
 R2  GL2 normalization of h.  For n = 1 every nonzero linear form is
     GL2-equivalent to y.  For n = 2 the orbits are y^2 and x*y.  For n = 3
     they are y^3, x*y^2 and x*y*(x-y).  (For n >= 4 there are moduli, so the
     exhaustive sweep here stops at n = 3.)
 R3  Scaling.  (P,Q) -> (P/alpha, alpha*Q) preserves J, so alpha = 1 WLOG.
 R4  Constants.  J is unchanged by P -> P + const, Q -> Q + const, so both
     constant terms are 0 WLOG.
 R5  Saturation.  beta != 0 is imposed by Rabinowitsch (beta*w - 1 = 0) so that
     a solution has degrees EXACTLY (d1,d2), not a degeneration.

Method: build the exact polynomial system over Q and decide it with a Groebner
basis.  EMPTY basis <=> no solution.  Everything is exact; no floating point.

A hit here would contradict Moh's degree bound, so the expected outcome is
"no solutions" -- which is exactly what makes it a correctness check on the
whole pipeline, and what makes any non-empty result worth a very hard look.
"""

import sys
import time
from math import gcd
from itertools import combinations_with_replacement
from sympy import (symbols, Poly, expand, groebner, QQ, S, total_degree,
                   simplify, Rational)

x, y, w = symbols('x y w')

RESULTS = []


def jac(P, Q):
    return expand(P.diff(x)*Q.diff(y) - P.diff(y)*Q.diff(x))


def gen_poly(prefix, maxdeg, mindeg=0, skip_const=True):
    """Generic polynomial of degree <= maxdeg with fresh symbols."""
    cs, expr = [], S(0)
    for d in range(mindeg, maxdeg + 1):
        for i in range(d + 1):
            j = d - i
            if skip_const and d == 0:
                continue
            c = symbols(f'{prefix}_{i}_{j}')
            cs.append(c)
            expr += c*x**i*y**j
    return expr, cs


H_ORBITS = {
    1: [('y', y)],
    2: [('y^2', y**2), ('x*y', x*y)],
    3: [('y^3', y**3), ('x*y^2', x*y**2), ('x*y*(x-y)', x*y*(x - y))],
}


def search_pair(d1, d2, hname, h, time_budget=None, verbose=True):
    """Decide: does a Keller pair exist with deg P = d1, deg Q = d2, leading
    forms alpha*h^b and beta*h^a?  Returns (status, detail)."""
    n = gcd(d1, d2)
    b, a = d1//n, d2//n
    assert total_degree(Poly(h, x, y)) == n

    # P = h^b + P1 (deg <= d1-1),  Q = beta*h^a + Q1 (deg <= d2-1)
    beta = symbols('beta')
    P1, cP = gen_poly('p', d1 - 1)
    Q1, cQ = gen_poly('q', d2 - 1)
    P = expand(h**b + P1)
    Q = expand(beta*h**a + Q1)

    Jexpr = expand(jac(P, Q) - 1)
    pj = Poly(Jexpr, x, y)
    eqs = [c for c in pj.coeffs()]
    eqs = [e for e in eqs if e != 0]
    eqs.append(beta*w - 1)                     # R5: beta != 0

    unk = cP + cQ + [beta, w]
    t0 = time.time()
    try:
        G = groebner(eqs, *unk, order='grevlex', domain=QQ)
    except Exception as ex:
        return 'ERROR', f'{type(ex).__name__}: {ex}'
    dt = time.time() - t0
    basis = list(G.exprs)
    if basis == [S(1)] or basis == [1]:
        return 'EMPTY', f'no solution; {len(eqs)} eqs, {len(unk)} unknowns, {dt:.1f}s'
    return 'NONEMPTY', (f'!!! basis has {len(basis)} elements; '
                        f'{len(eqs)} eqs, {len(unk)} unknowns, {dt:.1f}s')


def admissible_pairs(maxsum, maxn=3):
    """Non-dividing degree pairs (d1,d2), d1 > d2, with gcd <= maxn."""
    out = []
    for d1 in range(2, maxsum):
        for d2 in range(2, d1):
            if d1 % d2 == 0 or d2 % d1 == 0:
                continue
            if d1 + d2 > maxsum:
                continue
            if gcd(d1, d2) > maxn:
                continue
            out.append((d1, d2))
    return sorted(out, key=lambda t: (t[0] + t[1], t[0]))


def main(maxsum=13):
    print(f"DIRECT SEARCH: all non-dividing degree pairs with d1+d2 <= {maxsum},")
    print(f"gcd <= 3, leading forms normalized by GL2.  Exact Groebner over QQ.\n")
    pairs = admissible_pairs(maxsum)
    print(f"{len(pairs)} degree pairs to decide: {pairs}\n")
    hits = []
    for (d1, d2) in pairs:
        n = gcd(d1, d2)
        for (hname, h) in H_ORBITS[n]:
            sys.stdout.write(f"  (d1,d2)=({d1},{d2})  n={n}  "
                             f"cusp=(a,b)=({d2//n},{d1//n})  h={hname:12s} ... ")
            sys.stdout.flush()
            status, detail = search_pair(d1, d2, hname, h)
            print(f"{status:9s} {detail}")
            RESULTS.append((d1, d2, hname, status, detail))
            if status == 'NONEMPTY':
                hits.append((d1, d2, hname, detail))
    print("\n" + "=" * 70)
    ne = [r for r in RESULTS if r[3] == 'NONEMPTY']
    er = [r for r in RESULTS if r[3] == 'ERROR']
    em = [r for r in RESULTS if r[3] == 'EMPTY']
    print(f"decided EMPTY (no counterexample): {len(em)}")
    print(f"NONEMPTY (needs hard look):        {len(ne)}")
    print(f"errors/timeouts:                   {len(er)}")
    for r in ne:
        print(f"  !!! HIT: d=({r[0]},{r[1]}) h={r[2]}: {r[4]}")
    for r in er:
        print(f"  err: d=({r[0]},{r[1]}) h={r[2]}: {r[4]}")
    if not ne and not er:
        print("\nNO COUNTEREXAMPLE EXISTS in the swept range. This is a complete,")
        print("exact decision for these degree pairs -- consistent with Moh.")
    return hits


if __name__ == '__main__':
    ms = int(sys.argv[1]) if len(sys.argv) > 1 else 13
    main(ms)
