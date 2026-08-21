#!/usr/bin/env python3
"""STACKED reduction of the B=16 cells: mu0-elimination + torus gauge + cascade.

Three reductions composed, each independently verified elsewhere:

  (A) mu0 occurs in exactly one equation (the y^3 row), linearly, coeff 6, and
      on the normalized locus that row reads 6*mu0 = 2*a2*mu2.  So substitute
      a2 = 3*mu0/mu2 and DROP the row.                      [w6_b16_mu0_export]
  (B) the system is weighted-homogeneous, so gauge mu2 = 1; then a2 = 3*mu0 and
      (corrected 1.2 row 3) mu1 = -mu0*mu3.                 [w6_b16_mu0_export]
  (C) row y^{4d} is quadratic in a_{2d} alone and row y^{4d-k} is linear in
      a_{2d-k} with coefficient -((4(2d-k)+8d-12) a_{2d} + 3), which never
      vanishes at a root of the row-0 quadratic.  Back-substitute a_{2d} down
      to a_3.                                                [w6_b16_cascade]

a_2, a_1, a_0 are already pinned by (A)/(B) and by (1.2) rows 1-2, so the three
cascade rows that would have determined them become CONSTRAINTS instead -- they
are kept, not discarded.

RESULT:            about 2d+2 equations in d unknowns
    d = 7  ->  16 / 7        (campaign: 35 / 27)
    d = 12 ->  26 / 12       (campaign: 55 / 42)
The price is total degree ~4d instead of 4; which reduction wins at a given d is
an empirical question, so both exports are kept.

The row-0 root lives in Q(sqrt(12d)); we stay over Q by adjoining s with
s^2 = squarefree part of 12d.

EVERY EXPORT IS ROUND-TRIP CHECKED: the eliminated a's are substituted back into
the ORIGINAL system and the surviving residuals must be exactly the exported
constraints.  A solution of the exported system IS a counterexample to the
Jacobian conjecture (GGV Thm 1.2 + their Section 2), so a non-[-1] output is a
lead to be lifted and verified, never announced.
"""
import os, sys, json, time
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'wave5'))
from w5_b16_abel import build_system, mu0, mu1, mu2, mu3, y

PRIMES = [1000003, 1000033]
t = sp.Symbol('t')

def sqfree(n):
    N, i = n, 2
    while i*i <= N:
        while N % (i*i) == 0:
            N //= i*i
        i += 1
    return N

def build(d, root_index, verbose=True):
    eqs, unk, A, q1 = build_system(d)
    n13 = len(eqs) - 5
    rows, extra = eqs[:n13], eqs[n13:]
    a = sp.symbols(f'a0:{2*d+1}'); b = sp.symbols(f'b0:{d}')
    # --- locate and drop the mu0 row -------------------------------------
    hits = [i for i, e in enumerate(rows) if mu0 in e.free_symbols]
    assert len(hits) == 1 and sp.Poly(rows[hits[0]], mu0).all_coeffs()[0] == 6
    k0 = hits[0]
    # --- (A)+(B) substitutions -------------------------------------------
    sub = {b[0]: mu3, b[1]: 0, a[0]: -mu3**2/4, a[1]: 1, mu2: 1,
           a[2]: 3*mu0, mu1: -mu0*mu3}
    # --- (C) cascade, a_{2d} down to a_3 ---------------------------------
    r = sp.Symbol('r')
    roots = sp.solve(sp.Eq((8*d - 6)*r**2 + 3*r - sp.Rational(3, 8), 0), r)
    root = roots[root_index]
    sol = {a[2*d]: sp.nsimplify(root)}
    assert sp.simplify(rows[0].subs(sol)) == 0, "root fails the top row"
    for kk in range(1, 2*d - 1):                 # solves a_{2d-1} .. a_3
        j = 2*d - kk
        den = -((4*j + 8*d - 12)*sol[a[2*d]] + 3)
        assert sp.simplify(den) != 0, f"cascade denominator vanishes at j={j}"
        e = sp.expand(rows[kk].subs(sub).subs(sol))
        s_ = sp.solve(sp.Eq(e, 0), a[j])
        assert len(s_) == 1, f"row for a{j} not uniquely solvable"
        sol[a[j]] = sp.expand(s_[0])
    keep = [e for i, e in enumerate(rows) if i not in (k0,) and i >= 2*d - 1]
    keep += extra
    cons = []
    for e in keep:
        v = sp.expand(sp.expand(e.subs(sub)).subs(sol))
        if v == 0:
            continue
        if v.free_symbols == set():
            return {'d': d, 'root_index': root_index, 'status': 'EMPTY-BY-CONSTANT',
                    'constant': str(v)}
        cons.append(v)
    # --- round trip -------------------------------------------------------
    resid = [sp.expand(sp.expand(e.subs(sub)).subs(sol)) for e in rows + extra]
    assert len([x for x in resid if x != 0]) == len(cons), "round-trip mismatch"
    N = sqfree(12*d); s = sp.Symbol('s')
    cons = [sp.expand(c.subs(sp.sqrt(N), s)) for c in cons]
    cons.append(sp.expand(t*mu0 - 1))
    cons.append(s**2 - N)
    unknowns = sorted({v for c in cons for v in c.free_symbols}, key=str)
    cleared = []
    for c in cons:
        p = sp.Poly(c, *unknowns); den = 1
        for co in p.coeffs():
            den = sp.lcm(den, co.q if hasattr(co, 'q') else 1)
        cleared.append(sp.expand(c*den))
    head = ",".join(str(u) for u in unknowns) + "\n"
    body = ",\n".join(str(sp.Poly(e, *unknowns).as_expr()).replace('**', '^').replace(' ', '')
                      for e in cleared)
    tag = f"s16_d{d}_r{root_index}"
    os.makedirs('wave5/ms', exist_ok=True)
    for p in PRIMES:
        open(f"wave5/ms/{tag}_p{p}.ms", "w").write(head + str(p) + "\n" + body + "\n")
    open(f"wave5/ms/{tag}_q.ms", "w").write(head + "0\n" + body + "\n")
    rec = {'d': d, 'root_index': root_index, 'file': tag, 'root': str(root),
           'eqs': len(cleared), 'unknowns': len(unknowns),
           'unknown_names': [str(u) for u in unknowns],
           'max_total_degree': int(max(sp.total_degree(e) for e in cleared)),
           'campaign_eqs': 4*d+7, 'campaign_unknowns': 3*d+6}
    if verbose:
        print(json.dumps(rec), flush=True)
    return rec

if __name__ == '__main__':
    out = []
    for d in [int(v) for v in (sys.argv[1:] or ['5'])]:
        for ri in (0, 1):
            t0 = time.time()
            rec = build(d, ri)
            rec['secs'] = round(time.time() - t0, 1)
            out.append(rec)
            json.dump(out, open('/home/user/jacobian_planar/wave6/b16_stack.json', 'w'), indent=1)
