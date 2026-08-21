#!/usr/bin/env python3
"""Seeded chart-N export for cell d, mod p.

Soundness: the row-0 relation (8d-6)a_{2d}^2 + 3a_{2d} - 3/8 = 0 is mu-free
(verified d=3..14), so EVERY solution of the cell has a_{2d} equal to one of
its two roots.  Seeding each root in turn therefore covers the whole cell --
this is exactly the split that made d=12 tractable, and it removes one
unknown plus the quadratic, which is what strangles the unseeded run.

Chart N is the mu2 != 0 side (saturated by u*mu2 - 1); chart Z (mu2 = 0) is
already decided for these cells.  mu0 is saturated by t*mu0 - 1, so every
solution found has mu0 != 0 -- i.e. IS a counterexample seed.

Usage: python3 w6_seed_d8.py D PRIME
Writes wave5/ms2/b16seedN_d{D}_r{k}_p{PRIME}.ms for k = 0,1.
"""
import sys, os
sys.path.insert(0, '/home/user/jacobian_planar/wave5')
os.chdir('/home/user/jacobian_planar/wave5')
import sympy as sp
from sympy import symbols, expand, Symbol, Poly
from w5_b16_abel import build_system, mu0, mu1, mu2, mu3

d = int(sys.argv[1]); p = int(sys.argv[2])

# roots of the row-0 quadratic mod p
A = (8*d - 6) % p
disc = (12*d) % p
assert pow(disc, (p-1)//2, p) == 1, "12d is not a square mod p -- pick another prime"
q = p - 1; s0 = 0
while q % 2 == 0: q //= 2; s0 += 1
z = 2
while pow(z, (p-1)//2, p) != p-1: z += 1
M, c, t, R = s0, pow(z, q, p), pow(disc, q, p), pow(disc, (q+1)//2, p)
while t != 1:
    i, t2 = 0, t
    while t2 != 1: t2 = t2*t2 % p; i += 1
    b_ = pow(c, 1 << (M-i-1), p); M = i; c = b_*b_ % p; t = t*c % p; R = R*b_ % p
sq = R
assert sq*sq % p == disc
inv = pow(2*A % p, p-2, p)
roots = [(-3 + sq) * inv % p, (-3 - sq) * inv % p]
print('roots mod p:', roots)

eqs, unk, Apoly, q1 = build_system(d)
a = symbols(f'a0:{2*d+1}'); b = symbols(f'b0:{d}')
t_ = Symbol('t'); u_ = Symbol('u')

for k, r in enumerate(roots):
    pre = {a[0]: -mu3**2/4, a[1]: mu2, b[0]: mu3, b[1]: 0,
           mu1: -mu3*a[2]/3, a[2*d]: sp.Integer(r)}
    core = [expand(e.subs(pre)) for e in eqs]
    core = [e for e in core if e != 0]
    core.append(expand(t_*mu0 - 1))
    core.append(expand(u_*mu2 - 1))
    vars_ = [a[i] for i in range(2, 2*d)] + [b[i] for i in range(2, d)] \
            + [mu0, mu2, mu3, t_, u_]
    rows = []
    for e in core:
        P = Poly(e, *vars_)
        L = 1
        for cc in P.coeffs():
            L = sp.lcm(L, sp.denom(cc))
        e2 = expand(e * L)
        P2 = Poly(e2, *vars_)
        # reduce coefficients mod p and DROP generators that vanish mod p
        # (the seeded row-0 row does; leaving it as a big integer constant is
        #  exactly the msolve silent-lie shape we screen for)
        d2 = {m: int(c) % p for m, c in zip(P2.monoms(), P2.coeffs()) if int(c) % p != 0}
        if not d2:
            continue
        expr = sum(cc * sp.prod([v**e_ for v, e_ in zip(vars_, m)]) for m, cc in d2.items())
        if not expr.free_symbols:
            raise RuntimeError('NONZERO CONSTANT GENERATOR mod p -- system is trivially the whole ring')
        rows.append(str(Poly(expr, *vars_).as_expr()).replace('**', '^').replace(' ', ''))
    out = ','.join(str(v) for v in vars_) + '\n' + str(p) + '\n' + ',\n'.join(rows) + '\n'
    path = f'/home/user/jacobian_planar/wave5/ms2/b16seedN_d{d}_r{k}_p{p}.ms'
    open(path, 'w').write(out)
    # verify the seed really satisfies row0 mod p
    chk = ((8*d-6)*r*r + 3*r) % p
    chk = (chk*8 - 3) % p
    print(f'root {k}={r}: eqs={len(core)} vars={len(vars_)} row0_ok={chk==0} -> {os.path.basename(path)}')
