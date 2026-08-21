#!/usr/bin/env python3
"""WAVE 5b -- reduced, gauge-fixed B=16 systems (the RAM-wall workaround).

Reductions applied to build_system(d) from w5_b16_abel.py, each exact:
  1. Linear eliminations from (1.2)+normalizations:
       a0 = -mu3^2/4,  a1 = mu2,  b0 = mu3,  b1 = 0,
       mu1 = -mu3*(a2 + 2*b2)/3          [third (1.2) row, q1''(0) = 2*b2]
     (for d >= 3; d=2 has no b2 -- not needed, d<=6 already decided.)
  2. Quasi-homogeneity (verified below by exponent-matrix nullspace): weights
       b_i -> d-i, a_i -> 2d-i, mu3 -> d, mu2 -> 2d-1, mu1 -> 3d-2, mu0 -> 4d-3
     make every equation homogeneous of weight 4d (coefficient rows) resp. its
     own weight (the (1.2) rows are eliminated already).  The C* action lets us
     gauge-fix one nonzero coordinate per chart.
  3. Chart split, exhaustive for mu0 != 0 (GGV: mu1 = mu2 = 0 forces mu0 = 0;
     and mu1 is proportional to mu3, so mu2 = 0 & mu1 != 0 needs mu3 != 0):
       chart A: mu2 = 1        chart B: mu2 = 0, mu3 = 1
  4. mu0 != 0 saturated by t*mu0 - 1.

Regression demand: reduced d=5 and d=6 must be EMPTY in BOTH charts (matching
the unreduced char-0 verdicts) before any d >= 7 output is trusted.
"""
import os, sys
from sympy import symbols, Symbol, expand, Poly, Rational, linsolve, Matrix
sys.path.insert(0, os.path.dirname(__file__))
from w5_b16_abel import build_system, mu0, mu1, mu2, mu3, y

t = Symbol('t')
PRIMES = [1000003, 1000033, 1000039]

def reduced_charts(d):
    assert d >= 3
    eqs, unk, A, q1 = build_system(d)
    a = symbols(f'a0:{2*d+1}'); b = symbols(f'b0:{d}')
    subs = {a[0]: -mu3**2/4, a[1]: mu2, b[0]: mu3, b[1]: 0,
            mu1: -mu3*(a[2] + 2*b[2])/3}
    core = [expand(e.subs(subs)) for e in eqs]
    core = [e for e in core if e != 0]
    rest = [a[i] for i in range(2, 2*d+1)] + [b[i] for i in range(2, d)]
    charts = {}
    # SOUND split (correction 2026-08-20): the system's only scaling symmetry
    # is the finite group mu_d -- the term 2*mu3*q1''(0) in (1.2) row 3 breaks
    # every continuous torus (both published controls had b2 = 0 and never
    # exercised that term, which is how the unsound gauge passed regression).
    # So NO gauge-fixing: case-split on mu2 with saturation instead.
    # Charts: Z = {mu2 = 0};  N = {mu2 != 0 via u*mu2 = 1}.
    u = Symbol('u')
    for name, fix, extra in (("Z", {mu2: 0}, []), ("N", {}, [u*mu2 - 1])):
        ce = [expand(e.subs(fix)) for e in core] +              [expand((t*mu0 - 1).subs(fix))] + extra
        ce = [e for e in ce if e != 0]
        vars_ = [v for v in rest + [mu0, mu2, mu3] if v not in fix] + [t] +                 ([u] if extra else [])
        charts[name] = (ce, vars_)
    return charts

def weight_check(d):
    """Verify quasi-homogeneity of the eliminated core by exponent nullspace."""
    eqs, unk, A, q1 = build_system(d)
    a = symbols(f'a0:{2*d+1}'); b = symbols(f'b0:{d}')
    w = {a[i]: 2*d - i for i in range(2*d+1)}
    w.update({b[i]: d - i for i in range(d)})
    w.update({mu0: 4*d - 3, mu1: 3*d - 2, mu2: 2*d - 1, mu3: d})
    ok = True
    for e in eqs[:4*d+1]:                       # the (1.3) coefficient rows
        p = Poly(e, *unk)
        wts = {sum(m[i]*w[g] for i, g in enumerate(p.gens)) for m in p.monoms()}
        ok &= (len(wts) <= 1)
    return ok

def to_ms(eqs, unknowns, char):
    def clear(e):
        p = Poly(e, *unknowns)
        den = 1
        from sympy import lcm
        for cco in p.coeffs():
            den = lcm(den, cco.q if hasattr(cco, 'q') else 1)
        return expand(e*den)
    head = ",".join(map(str, unknowns)) + "\n" + str(char) + "\n"
    return head + ",\n".join(str(Poly(clear(e), *unknowns).as_expr())
                             .replace('**', '^').replace(' ', '')
                             for e in eqs) + "\n"

def main():
    os.makedirs("wave5/ms2", exist_ok=True)
    ds = [int(x) for x in (sys.argv[1:] or ["5", "6", "7"])]
    for d in ds:
        print(f"d={d}: quasi-homogeneous core: {weight_check(d)}")
        for name, (ce, vars_) in reduced_charts(d).items():
            for p in PRIMES:
                open(f"wave5/ms2/b16r_d{d}_{name}_p{p}.ms", "w").write(to_ms(ce, vars_, p))
            open(f"wave5/ms2/b16r_d{d}_{name}_q.ms", "w").write(to_ms(ce, vars_, 0))
            print(f"  chart {name}: {len(ce)} eqs, {len(vars_)} vars")

if __name__ == "__main__":
    main()
