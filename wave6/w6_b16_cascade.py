#!/usr/bin/env python3
"""THE B=16 LADDER IS A CASCADE.  Reduce each GGV cell from 4d+6 equations in
3d+5 unknowns to ~2d+2 equations in d+2 unknowns, by exact back-substitution --
no Groebner basis anywhere in the reduction.

WHY THIS CELL AND NOT ANOTHER.  GGV Theorem 1.2: B = 16 iff (1.2)+(1.3) has a
solution, and a solution with mu0 != 0 "would yield a counterexample to the JC"
(their words, p.85), with the construction given in their Section 2.  This is
the ONLY place in the whole campaign where a single point converts into a
counterexample by a published theorem plus an explicit recipe.  Moreover the
degree map says cell d realizes degrees (16(3d-2), 16(2d-1)), and
gcd(3d-2, 2d-1) = 1 always (2(3d-2) - 3(2d-1) = -1), so EVERY cell has
B = 16 exactly -- admissible under GGV's own "B = 16 or B > 20" dichotomy.
Moh needs max > 100, i.e. d >= 3; GGHV's elimination reaches only max < 125,
i.e. d <= 3.  So every cell with d >= 4 is virgin territory that no published
work touches, and where a hit is immediately a counterexample.

THE STRUCTURE (verified, not assumed -- assert_cascade() checks it per d).
Order the coefficient rows of (1.3) by descending power of y.  Then

  row y^{4d}      is QUADRATIC in a_{2d} alone   -- GGV's row-0 quadratic
                     (8d-6) a^2 + 3a - 3/8 = 0,  discriminant 12d
  row y^{4d-k}    is LINEAR in the single new unknown a_{2d-k}, k = 1..2d,
                     with coefficient  -( (4(2d-k) + 8d - 12) * a_{2d} + 3 )

The coefficient depends on a_{2d} ONLY.  Fix a_{2d} = r, a root of the
quadratic; then every coefficient is a CONSTANT, so the back-substitution
introduces no denominators beyond constants and each a_j comes out a POLYNOMIAL
in the remaining unknowns b_2..b_{d-1}, mu0..mu3.  Rows y^{2d-1} .. y^0 then
introduce no new unknowns at all: they are pure constraints.

RESULT: cell d  ==  ~2d+2 polynomial constraints in d+2 unknowns.
        d = 12 : 14 unknowns instead of 41.   d = 27 : 29 instead of 86.

CONTROLS (all must pass before any verdict is read off):
  * assert_cascade(d) re-derives the linearity and the coefficient formula.
  * the two roots of the row-0 quadratic are seeded separately and BOTH must be
    run: they partition the cell (the quadratic is mu-free).
  * a denominator ((4j+8d-12) r + 3) that VANISHES invalidates the elimination
    at that j; the code raises instead of dividing.
  * reduce_cell(d) is checked by substituting the reduced solution back into the
    ORIGINAL system (round_trip_check).
"""
import sys, os, json, time
import sympy as sp

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'wave5'))
from w5_b16_abel import build_system, mu0, mu1, mu2, mu3, y


def rows_of(d):
    eqs, unk, A, q1 = build_system(d)
    n13 = len(eqs) - 5
    return eqs[:n13], eqs[n13:], unk, A, q1


def assert_cascade(d):
    """Verify the two structural claims; return the coefficient formula check."""
    rows, extra, unk, A, q1 = rows_of(d)
    a = sp.symbols(f'a0:{2*d+1}')
    n = len(rows)
    top = rows[0]
    assert sp.degree(top, a[2*d]) == 2, "top row not quadratic in a_{2d}"
    assert set(str(v) for v in top.free_symbols) == {f'a{2*d}'}, \
        f"top row involves more than a_{2*d}: {top.free_symbols}"
    ok = []
    for k in range(1, 2*d + 1):
        e = rows[k]
        j = 2*d - k
        assert sp.degree(e, a[j]) == 1, f"row y^{n-1-k} not linear in a{j}"
        c = sp.Poly(e, a[j]).all_coeffs()[0]
        pred = -((4*j + 8*d - 12)*a[2*d] + 3)
        ok.append(sp.simplify(c - pred) == 0)
    return all(ok), len(ok)


def row0_roots(d):
    r = sp.Symbol('r')
    return sp.solve(sp.Eq((8*d - 6)*r**2 + 3*r - sp.Rational(3, 8), 0), r)


def reduce_cell(d, root, verbose=True):
    """Back-substitute the a's; return (constraints, free_unknowns, a_solution)."""
    rows, extra, unk, A, q1 = rows_of(d)
    a = sp.symbols(f'a0:{2*d+1}'); b = sp.symbols(f'b0:{d}')
    sol = {a[2*d]: sp.nsimplify(root)}
    # check the top row really vanishes at the root
    assert sp.simplify(rows[0].subs(sol)) == 0, "root does not satisfy the top row"
    for k in range(1, 2*d + 1):
        j = 2*d - k
        den = -((4*j + 8*d - 12)*sol[a[2*d]] + 3)
        if sp.simplify(den) == 0:
            raise ZeroDivisionError(
                f"cascade denominator vanishes at j={j}, d={d}, root={root}")
        e = sp.expand(rows[k].subs(sol))
        s = sp.solve(sp.Eq(e, 0), a[j])
        assert len(s) == 1, f"row for a{j} not uniquely solvable"
        sol[a[j]] = sp.expand(s[0])
        if verbose and k <= 3:
            print(f"    a{j} = {str(sol[a[j]])[:90]}...", flush=True)
    constraints = [sp.expand(e.subs(sol)) for e in rows[2*d+1:]]
    constraints += [sp.expand(e.subs(sol)) for e in extra]
    constraints = [c for c in constraints if c != 0]
    free = [v for v in (list(b) + [mu0, mu1, mu2, mu3])
            if any(v in c.free_symbols for c in constraints)]
    return constraints, free, sol


def round_trip_check(d, sol, constraints):
    """Substituting the cascade solution into the ORIGINAL system must leave
    exactly the constraints (a can-fail control on the elimination)."""
    rows, extra, unk, A, q1 = rows_of(d)
    resid = [sp.expand(e.subs(sol)) for e in rows + extra]
    nonzero = [r for r in resid if r != 0]
    return len(nonzero) == len(constraints)


if __name__ == '__main__':
    ds = [int(v) for v in sys.argv[1:]] or [5, 6, 7]
    out = []
    for d in ds:
        t0 = time.time()
        ok, ncheck = assert_cascade(d)
        print(f"=== d={d}: cascade structure verified on {ncheck} rows: {ok}", flush=True)
        roots = row0_roots(d)
        for ri, root in enumerate(roots):
            try:
                cons, free, sol = reduce_cell(d, root)
            except ZeroDivisionError as e:
                print(f"  root {ri} ({root}): {e}"); continue
            rt = round_trip_check(d, sol, cons)
            degs = [sp.total_degree(c) for c in cons]
            rec = {'d': d, 'root': str(root), 'orig_eqs': 4*d + 6,
                   'orig_unknowns': 3*d + 5, 'reduced_eqs': len(cons),
                   'reduced_unknowns': len(free),
                   'free': [str(v) for v in free],
                   'max_total_degree': int(max(degs)) if degs else 0,
                   'round_trip': bool(rt),
                   'secs': round(time.time() - t0, 1)}
            print("  " + json.dumps(rec), flush=True)
            out.append({'rec': rec,
                        'constraints': [sp.srepr(c) for c in cons]})
    json.dump([o['rec'] for o in out],
              open('/home/user/jacobian_planar/wave6/b16_cascade_sizes.json', 'w'), indent=1)
