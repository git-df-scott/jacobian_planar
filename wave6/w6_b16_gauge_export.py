#!/usr/bin/env python3
"""B=16 cells exported with the TORUS GAUGE mu0 = 1 instead of the Rabinowitsch
saturation t*mu0 - 1.

The corrected GGV system (see CATCHES.md, "GGV (1.2) ROW 3 IS MIS-PRINTED") is
WEIGHTED-HOMOGENEOUS for every d under

    wt(a_i) = 2d - i,  wt(b_j) = d - j,
    wt(mu3) = d,  wt(mu2) = 2d - 1,  wt(mu1) = 3d - 2,  wt(mu0) = 4d - 3

-- verified equation by equation for d = 3..8 (every row carries a single
weight).  All weights are positive except wt(a_{2d}) = 0, so there is an exact
C^* action, and on the locus mu0 != 0 it can be used to scale mu0 to 1:
if (a,b,mu) solves the system with mu0 != 0, pick lambda with
lambda^{4d-3} = 1/mu0 (possible over an algebraically closed field) and rescale.
Hence

    { solutions with mu0 != 0 }  is empty  <=>  { solutions with mu0 = 1 } is empty

and a solution of the gauged system IS a solution with mu0 != 0, i.e. a
counterexample to the Jacobian conjecture by GGV Theorem 1.2.

WHY IT MATTERS COMPUTATIONALLY.  The saturation costs an extra unknown t and an
extra equation, and Rabinowitsch variables are notoriously bad for Groebner
bases.  The gauge removes BOTH and additionally pins mu0, so the cell drops from
(4d+7 equations, 3d+6 unknowns) to (4d+6, 3d+4).

The campaign previously discarded its torus gauges on the grounds that "the term
2*mu3*q1''(0) in (1.2) row 3 breaks every continuous torus".  That term is the
misprint; with it removed the torus is exact.  This file is the gauge restored.
"""
import os, sys
import sympy as sp
from sympy import Symbol, symbols, expand, Poly, lcm

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'wave5'))
from w5_b16_abel import build_system, mu0, mu1, mu2, mu3, y

PRIMES = [1000003, 1000033, 1000039]

def check_grading(d):
    a = symbols(f'a0:{2*d+1}'); b = symbols(f'b0:{d}')
    W = {a[i]: 2*d - i for i in range(2*d+1)}
    W.update({b[j]: d - j for j in range(d)})
    W.update({mu3: d, mu2: 2*d - 1, mu1: 3*d - 2, mu0: 4*d - 3})
    eqs, unk, A, q1 = build_system(d)
    gens = sorted(W, key=str)
    for e in eqs:
        if e == 0:
            continue
        p = Poly(expand(e), *gens)
        degs = {sum(k*W[g] for k, g in zip(m, p.gens)) for m in p.monoms()}
        if len(degs) != 1:
            return False
    return True

def int_clear(e, gens):
    p = Poly(e, *gens); den = 1
    for c in p.coeffs():
        den = lcm(den, c.q if hasattr(c, 'q') else 1)
    return expand(e*den)

def to_ms(eqs, unknowns, char):
    head = ",".join(str(u) for u in unknowns) + "\n" + str(char) + "\n"
    body = ",\n".join(str(Poly(e, *unknowns).as_expr()).replace('**', '^').replace(' ', '')
                      for e in eqs)
    return head + body + "\n"

def export(d):
    assert check_grading(d), f"grading FAILED at d={d} -- gauge would be unsound"
    eqs, unk, A, q1 = build_system(d)
    eqs = [expand(e.subs(mu0, 1)) for e in eqs]          # THE GAUGE
    consts = [e for e in eqs if e != 0 and e.free_symbols == set()]
    assert not consts, f"nonzero constant generator after gauge: {consts}"
    eqs = [e for e in eqs if e != 0]
    unknowns = [u for u in unk if u != mu0]
    eqs = [int_clear(e, unknowns) for e in eqs]
    os.makedirs('wave5/ms', exist_ok=True)
    for p in PRIMES:
        open(f"wave5/ms/g16_d{d}_p{p}.ms", "w").write(to_ms(eqs, unknowns, p))
    open(f"wave5/ms/g16_d{d}_q.ms", "w").write(to_ms(eqs, unknowns, 0))
    return len(eqs), len(unknowns)

if __name__ == '__main__':
    for d in [int(v) for v in (sys.argv[1:] or ['5', '6', '7'])]:
        n, m = export(d)
        print(f"d={d}: grading verified; gauged system {n} equations / {m} unknowns "
              f"(saturated version was {n+1} / {m+2})  -> wave5/ms/g16_d{d}_*.ms", flush=True)
