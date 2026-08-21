#!/usr/bin/env python3
"""Export the CASCADE-REDUCED, TORUS-GAUGED B=16 cells to msolve, over Q.

Three independent reductions are stacked, each verified:

 1. CASCADE (w6_b16_cascade.py).  Row y^{4d} is quadratic in a_{2d} alone; every
    row y^{4d-k} (k = 1..2d) is linear in the single new unknown a_{2d-k} with
    coefficient -((4(2d-k)+8d-12) a_{2d} + 3), a function of a_{2d} ONLY.  So all
    2d+1 of the a's back-substitute away, leaving rows y^{2d-1}..y^0 plus (1.2)
    as pure constraints.  Checked per d by assert_cascade(), and the substitution
    is re-verified by round_trip_check().

 2. NORMALIZATIONS.  b0 = mu3 and b1 = 0 (GGV p.92) are applied as substitutions
    rather than carried as equations.

 3. TORUS GAUGE mu0 = 1 (w6_b16_gauge_export.py).  The corrected system is
    weighted-homogeneous with wt(mu0) = 4d-3 > 0, so on mu0 != 0 the C^* action
    scales mu0 to 1 over an algebraically closed field.  Sound in both
    directions: solutions with mu0 != 0 exist iff solutions with mu0 = 1 do.

The row-0 root lives in Q(sqrt(12d)); we keep the computation over Q by
substituting sqrt(N) -> s and adjoining s^2 - N = 0.  Net size:

    cell d :  4d+6 equations / 3d+5 unknowns   -->   about 2d+3 / d+2

A SOLUTION OF THE EXPORTED SYSTEM IS A COUNTEREXAMPLE TO THE JACOBIAN
CONJECTURE (GGV Theorem 1.2 + their Section 2 construction), so any non-[-1]
output must be lifted, verified exactly, and adjudicated -- never announced.

Usage: python3 wave6/w6_b16_cascade_export.py 7 8 ...
"""
import os, sys, json, time
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'wave5'))
from w5_b16_abel import mu0, mu1, mu2, mu3
from w6_b16_cascade import assert_cascade, row0_roots, reduce_cell, round_trip_check

PRIMES = [1000003, 1000033]

def squarefree_radical(n):
    """12d = m^2 * N with N squarefree; sympy writes the root via sqrt(N)."""
    N, m = n, 1
    i = 2
    while i*i <= N:
        while N % (i*i) == 0:
            N //= i*i; m *= i
        i += 1
    return N, m

def export(d, verbose=True):
    ok, ncheck = assert_cascade(d)
    assert ok, f"cascade structure check FAILED at d={d}"
    N, _ = squarefree_radical(12*d)
    s = sp.Symbol('s')
    b = sp.symbols(f'b0:{d}')
    out = []
    for ri, root in enumerate(row0_roots(d)):
        t0 = time.time()
        cons, free, sol = reduce_cell(d, root, verbose=False)
        assert round_trip_check(d, sol, cons), f"round-trip FAILED d={d} root {ri}"
        sub = {b[0]: mu3, b[1]: 0, mu0: 1}
        cons2 = []
        for c in cons:
            e = sp.expand(c.subs(sub))
            e = sp.expand(e.subs(sp.sqrt(N), s))      # adjoin s, s^2 = N
            if e == 0:
                continue
            if e.free_symbols == set():
                # a nonzero constant generator: this branch is EMPTY, exactly
                return {'d': d, 'root': str(root), 'status': 'EMPTY-BY-CONSTANT',
                        'constant': str(e)}
            cons2.append(e)
        cons2.append(s**2 - N)
        unknowns = sorted({v for c in cons2 for v in c.free_symbols}, key=str)
        # clear denominators
        cleared = []
        for c in cons2:
            p = sp.Poly(c, *unknowns)
            den = 1
            for co in p.coeffs():
                den = sp.lcm(den, co.q if hasattr(co, 'q') else 1)
            cleared.append(sp.expand(c*den))
        head = ",".join(str(u) for u in unknowns) + "\n"
        body = ",\n".join(str(sp.Poly(e, *unknowns).as_expr()).replace('**', '^').replace(' ', '')
                          for e in cleared)
        os.makedirs('wave5/ms', exist_ok=True)
        tag = f"c16_d{d}_r{ri}"
        for p in PRIMES:
            open(f"wave5/ms/{tag}_p{p}.ms", "w").write(head + str(p) + "\n" + body + "\n")
        open(f"wave5/ms/{tag}_q.ms", "w").write(head + "0\n" + body + "\n")
        rec = {'d': d, 'root': str(root), 'file': tag,
               'orig_eqs': 4*d+6, 'orig_unknowns': 3*d+5,
               'reduced_eqs': len(cleared), 'reduced_unknowns': len(unknowns),
               'unknowns': [str(u) for u in unknowns],
               'max_total_degree': int(max(sp.total_degree(e) for e in cleared)),
               'sqrt_adjoined': N, 'secs': round(time.time()-t0, 1)}
        if verbose:
            print(json.dumps(rec), flush=True)
        out.append(rec)
    return out

if __name__ == '__main__':
    allout = []
    for d in [int(v) for v in (sys.argv[1:] or ['5'])]:
        r = export(d)
        allout += (r if isinstance(r, list) else [r])
        json.dump(allout, open('/home/user/jacobian_planar/wave6/b16_cascade_export.json', 'w'),
                  indent=1)
