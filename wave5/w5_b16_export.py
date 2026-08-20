#!/usr/bin/env python3
"""WAVE 5 -- export GGV (1.2)+(1.3) coefficient systems to msolve format.

For each d = deg(q1), the system from w5_b16_abel.build_system plus the
saturation t*mu0 - 1 = 0 (so every solution has mu0 != 0: the counterexample
condition of GGV Theorem 1.2).  Files:
  wave5/ms/b16_d{d}_p{p}.ms   (char p, p = 1 mod 3)
  wave5/ms/b16_d{d}_q.ms      (char 0)
Sanity per msolve silent-lie findings (wave4/w4_msformat.py): all polynomials
are sympy-expanded (repeated monomials combined) and integer-cleared; no
constant generators.
"""
import os, sys
from sympy import Symbol, symbols, expand, Poly, nsimplify, together, fraction, lcm, Integer
sys.path.insert(0, os.path.dirname(__file__))
from w5_b16_abel import build_system, mu0, mu1, mu2, mu3, y

PRIMES = [1000003, 1000033, 1000039]
t = Symbol('t')

def int_clear(e, gens):
    p = Poly(e, *gens)
    den = 1
    for c in p.coeffs():
        den = lcm(den, c.q if hasattr(c, 'q') else 1)
    return expand(e * den)

def to_ms(eqs, unknowns, char):
    head = ",".join(str(u) for u in unknowns) + "\n" + str(char) + "\n"
    body = ",\n".join(str(Poly(e, *unknowns).as_expr()).replace('**', '^').replace(' ', '')
                      for e in eqs)
    return head + body + "\n"

def main():
    os.makedirs("wave5/ms", exist_ok=True)
    ds = [int(x) for x in (sys.argv[1:] or ["4", "5"])]
    for d in ds:
        eqs, unk, A, q1 = build_system(d)
        eqs = [int_clear(e, unk) for e in eqs]
        eqs.append(expand(t*mu0 - 1))
        unknowns = unk + [t]
        # drop identically-zero coefficient rows (leading rows can vanish)
        eqs = [e for e in eqs if e != 0]
        for p in PRIMES:
            open(f"wave5/ms/b16_d{d}_p{p}.ms", "w").write(to_ms(eqs, unknowns, p))
        open(f"wave5/ms/b16_d{d}_q.ms", "w").write(to_ms(eqs, unknowns, 0))
        print(f"d={d}: {len(eqs)} equations, {len(unknowns)} unknowns "
              f"-> wave5/ms/b16_d{d}_[p*|q].ms")

if __name__ == "__main__":
    main()
