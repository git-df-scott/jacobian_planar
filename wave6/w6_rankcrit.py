#!/usr/bin/env python3
"""EXACT RANK CRITERION at the quasi-homogeneous points, for every d at once.

Two structural facts make this cheap and decisive:

 (1) mu0 occurs in the GGV system in exactly ONE term (-6*mu0*y^3 of (1.3)),
     multiplied by no other unknown.  Hence F(p,mu0) = F0(p) + mu0*G with
     G a CONSTANT vector (-6 in the y^3 row, 0 elsewhere) -- independent of p.

 (2) GGV prove that at mu3=mu2=mu1=mu0=0 the solutions are (rho,sigma)-quasi-
     homogeneous with (rho,sigma)=(d-1,1), i.e. q1 = y^d, A = a_{2d} y^{2d}
     with a_{2d} a root of the row-0 quadratic (8d-6)a^2 + 3a - 3/8.
     So an explicit point of the mu0=0 locus is known for EVERY d.

Therefore the first-order bifurcation test at those points is pure exact
linear algebra over Q:

        does  G  lie in the column span of  J(p) = dF0/d(vars) at p ?

  NO  for all points  ->  no counterexample branches off this stratum (cell
                          closed to first order at the quasi-homogeneous pts)
  YES at some (d, root) -> a counterexample branch sprouts there: solve the
                          higher orders and lift.  IMMEDIATE CANDIDATE.

Controls: d=3 MUST answer NO (GGV proved the cell empty; we showed the
residual is exactly 6*mu0).  The point must also satisfy F0(p)=0 exactly --
verified per d, and a failure there means the quasi-homogeneous ansatz is
wrong for that d and the answer is reported as UNKNOWN, not NO.
"""
import sys, json
import sympy as sp
from sympy import symbols, expand, Rational, Matrix

sys.path.insert(0, '/home/user/jacobian_planar/wave5')
import os
os.chdir('/home/user/jacobian_planar/wave5')
from w5_b16_abel import build_system, mu0, mu1, mu2, mu3

def analyze(d):
    eqs, unk, A, q1 = build_system(d)
    a = symbols(f'a0:{2*d+1}'); b = symbols(f'b0:{d}')
    # split F = F0 + mu0*G  and check G is constant
    F0, G = [], []
    for e in eqs:
        p = sp.Poly(expand(e), mu0)
        if p.degree() > 1:
            return {'d': d, 'error': f'mu0 degree {p.degree()}'}
        g = p.all_coeffs()[0] if p.degree() == 1 else sp.Integer(0)
        F0.append(expand(e.subs(mu0, 0)))
        G.append(sp.simplify(g))
    Gconst = all(gg.free_symbols == set() for gg in G)
    # quasi-homogeneous point: all mu = 0, q1 = y^d, A = a_{2d} y^{2d}
    root_eq = sp.Eq((8*d - 6)*sp.Symbol('r')**2 + 3*sp.Symbol('r') - Rational(3, 8), 0)
    roots = sp.solve(root_eq, sp.Symbol('r'))
    vars_ = [a[i] for i in range(2, 2*d+1)] + [b[i] for i in range(2, d)] + [mu2, mu3]
    Jsym = Matrix(F0).jacobian(Matrix(vars_))
    out = []
    for r in roots:
        pt = {mu1: 0, mu2: 0, mu3: 0}
        for i in range(0, 2*d):
            pt[a[i]] = 0
        pt[a[2*d]] = r
        for i in range(0, d):
            pt[b[i]] = 0
        F0v = [sp.simplify(f.subs(pt)) for f in F0]
        on_locus = all(v == 0 for v in F0v)
        Jv = Jsym.subs(pt)
        Jv = Jv.applyfunc(lambda e: sp.nsimplify(sp.simplify(e)))
        Gv = Matrix([sp.nsimplify(g) for g in G])
        rk_J = Jv.rank()
        rk_aug = Jv.row_join(Gv).rank()
        solvable = (rk_J == rk_aug)
        out.append({'root': str(r), 'on_locus': bool(on_locus),
                    'rank_J': int(rk_J), 'rank_aug': int(rk_aug),
                    'BIFURCATION_POSSIBLE': bool(solvable and on_locus),
                    'verdict': ('BIFURCATION-POINT' if (solvable and on_locus)
                                else ('obstructed' if on_locus else 'UNKNOWN-not-on-locus'))})
    return {'d': d, 'eqs': len(F0), 'vars': len(vars_),
            'G_constant': bool(Gconst), 'results': out}

if __name__ == '__main__':
    ds = [int(x) for x in sys.argv[1:]] or list(range(3, 13))
    allout = []
    for d in ds:
        try:
            r = analyze(d)
        except Exception as e:
            r = {'d': d, 'error': str(e)[:150]}
        print(json.dumps(r), flush=True)
        allout.append(r)
        json.dump(allout, open('/home/user/jacobian_planar/wave6/rankcrit_results.json', 'w'), indent=1)
