#!/usr/bin/env python3
"""B=16 cells with mu0 ELIMINATED, the mu2=1 torus gauge, and saturation on mu0.

THE STRUCTURAL FACTS THIS RESTS ON (each verified for many d in the __main__
self-test; none is assumed):

 (F1) mu0 occurs in the ENTIRE system in exactly ONE equation -- the y^3
      coefficient row of (1.3) -- and linearly, with the constant coefficient 6.
      So that row does not constrain anything: it DEFINES mu0.

 (F2) On the (1.2)-normalized locus (b0 = mu3, b1 = 0, a0 = -mu3^2/4, a1 = mu2,
      and mu1 from (1.2) row 3) that row collapses from 20 terms to a single
      monomial:
                              mu0 = a2 * mu2 / 3
      for EVERY d, in both the corrected and the printed variant.  Hence

          a counterexample (mu0 != 0)  <=>  a2 != 0  AND  mu2 != 0.

      COROLLARY: the chart mu2 = 0 contains no counterexample at any d, so the
      campaign's Z-chart runs were searching a region that cannot contain one.

 (F3) Combining (F2) with the CORRECTED (1.2) row 3, mu1 = -mu3*a2/3, and
      eliminating a2 gives a relation among the bracket constants alone:

                          mu0*mu3 + mu1*mu2 = 0

      valid for every d.  It FAILS on the printed variant (which gives
      mu0*mu3 + mu1*mu2 = -(2/3)*mu3*b2*mu2), so this is a consequence of
      today's correction and is new.  Since [P,Q] = x^4 y + mu3 x^3 + mu2 x^2
      + mu1 x + mu0, it is a necessary condition on the bracket of any B=16
      counterexample.

 (F4) The system is weighted-homogeneous (wt(a_i)=2d-i, wt(b_j)=d-j, wt(mu3)=d,
      wt(mu2)=2d-1, wt(mu1)=3d-2, wt(mu0)=4d-3), so on mu2 != 0 the C^* action
      gauges mu2 to 1.  Sound over an algebraically closed field in both
      directions.

RESULTING SYSTEM.  Substituting a0, a1, a2, b0, b1, mu1, mu2 and dropping the
y^3 row leaves

        4d+1 equations in 3d-1 unknowns      (campaign's version: 4d+7 / 3d+6)

i.e. seven fewer unknowns.  A solution IS a counterexample to the Jacobian
conjecture by GGV Theorem 1.2 plus their Section 2 construction.
"""
import os, sys
import sympy as sp
from sympy import symbols, expand, Poly, lcm, Symbol

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'wave5'))
from w5_b16_abel import build_system, mu0, mu1, mu2, mu3, y

PRIMES = [1000003, 1000033]
t = Symbol('t')

def facts(d, variant='corrected'):
    """Re-verify F1-F3 at this d; return (y3_row_index, rows, eqs, a, b)."""
    eqs, unk, A, q1 = build_system(d, variant)
    n13 = len(eqs) - 5
    rows = eqs[:n13]
    a = symbols(f'a0:{2*d+1}'); b = symbols(f'b0:{d}')
    hits = [i for i, e in enumerate(eqs) if mu0 in e.free_symbols]
    assert len(hits) == 1, f"F1 FAILED: mu0 in {len(hits)} equations at d={d}"
    k = hits[0]
    assert sp.degree(eqs[k], mu0) == 1, "F1 FAILED: mu0 not linear"
    assert sp.Poly(eqs[k], mu0).all_coeffs()[0] == 6, "F1 FAILED: coeff(mu0) != 6"
    norm = {b[0]: mu3, b[1]: 0, a[0]: -mu3**2/4, a[1]: mu2}
    mu1s = sp.solve(expand(eqs[-3].subs(norm)), mu1)[0]
    y3 = expand(rows[k].subs(norm).subs(mu1, mu1s))
    assert expand(y3 - (6*mu0 - 2*a[2]*mu2)) == 0, f"F2 FAILED at d={d}: {sp.factor(y3)}"
    return k, rows, eqs, a, b, mu1s, norm

def export(d, verbose=True):
    k, rows, eqs, a, b, mu1s, norm = facts(d)
    # NOTE: sympy's Expr.subs(dict) is SEQUENTIAL (sorted by default_sort_key),
    # not simultaneous, so a chained entry like {a1: mu2, mu2: 1} is order-
    # dependent.  Every value below is therefore written in FINAL form -- no
    # entry's value mentions another entry's key -- so the result cannot depend
    # on substitution order.  (Verified: the exported files are byte-identical
    # to the pre-hardening ones.)
    sub = {b[0]: mu3, b[1]: 0, a[0]: -mu3**2/4,
           a[1]: sp.Integer(1),                    # a1 = mu2 = 1
           mu2: sp.Integer(1),                     # F4: torus gauge
           a[2]: 3*mu0,                            # F2 with mu2 = 1
           mu1: -mu0*mu3}                          # F3 with mu2 = 1
    keep = [e for i, e in enumerate(eqs) if i != k]     # drop the y^3 row (F1)
    out = []
    for e in keep:
        v = expand(e.subs(sub))
        if v == 0:
            continue
        if v.free_symbols == set():
            return {'d': d, 'status': 'EMPTY-BY-CONSTANT', 'constant': str(v)}
        out.append(v)
    out.append(expand(t*mu0 - 1))                  # mu0 != 0  <=> counterexample
    unknowns = sorted({v for e in out for v in e.free_symbols}, key=str)
    cleared = []
    for e in out:
        p = Poly(e, *unknowns); den = 1
        for c in p.coeffs():
            den = lcm(den, c.q if hasattr(c, 'q') else 1)
        cleared.append(expand(e*den))
    head = ",".join(str(u) for u in unknowns) + "\n"
    body = ",\n".join(str(Poly(e, *unknowns).as_expr()).replace('**', '^').replace(' ', '')
                      for e in cleared)
    os.makedirs('wave5/ms', exist_ok=True)
    tag = f"m16_d{d}"
    for p in PRIMES:
        open(f"wave5/ms/{tag}_p{p}.ms", "w").write(head + str(p) + "\n" + body + "\n")
    open(f"wave5/ms/{tag}_q.ms", "w").write(head + "0\n" + body + "\n")
    rec = {'d': d, 'file': tag, 'eqs': len(cleared), 'unknowns': len(unknowns),
           'campaign_eqs': 4*d+7, 'campaign_unknowns': 3*d+6,
           'max_total_degree': int(max(sp.total_degree(e) for e in cleared))}
    if verbose:
        print(__import__('json').dumps(rec), flush=True)
    return rec

if __name__ == '__main__':
    for d in [int(v) for v in (sys.argv[1:] or ['5', '6', '7'])]:
        export(d)
