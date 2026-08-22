#!/usr/bin/env python3
"""The whole pentagon on the witness as ONE flat system, for msolve.

No descent, no charts, no branch choices, no saturation, no divisions, and no
inherited assumptions such as g8_6 = g8_7 = 0.  Just every coefficient of every
level equation, in every unknown at once:

    261 equations, 144 unknowns, max total degree 2.

Degree 2 because the bracket is BILINEAR: each equation is a sum of h_a * g_b
terms.  A quadratic sparse system is what Groebner engines are good at, and it
sidesteps the expression swell that OOM-killed the sympy back-substitution at
level 10 -- there, 92 unknowns solved on rational pivots had become enormous
polynomials in the remaining free ones.

A16 discipline: integer coefficients, fully expanded, asserted parenthesis-free,
and a planted positive control emitted in the same format and size.
"""
import sympy as sp, sys
z = sp.Symbol('z'); TAU = sp.Integer(1); s = z + TAU
def hsup(a):
    return [i for i in range(9) if 0 <= i+a <= 16 and max(0,(i+a)-8) <= i <= min(8,(i+a)//2+1)]
def gsup(b):
    return [k for k in range(13) if (k+b) >= 0 and ((k+1)//2 if k <= 2 else 2*k-3) <= k+b <= 12+k]
H = {8: z**8, 7: 2*z**8, 6: z**8, -1: sp.expand(s)}
G = {12: z**12, -1: sp.expand(s**2)}
for a in range(0,6): H[a] = sum(sp.Symbol(f'h{a}_{i}')*z**i for i in hsup(a))
for b in range(0,12): G[b] = sum(sp.Symbol(f'g{b}_{k}')*z**k for k in gsup(b))
eqs = []
for L in range(20,-3,-1):
    e = 0
    for a in range(-1,9):
        b = L-a
        if a in H and b in G: e += b*sp.diff(H[a],z)*G[b] - a*H[a]*sp.diff(G[b],z)
    e = sp.expand(e - (s**2 if L==-2 else 0))
    if e == 0: continue
    eqs += [sp.expand(c) for c in sp.Poly(e,z).all_coeffs() if c != 0]
V = sorted(set().union(*[c.free_symbols for c in eqs]), key=str)
print(f"{len(eqs)} equations, {len(V)} unknowns, max degree "
      f"{max(sp.Poly(c,*V).total_degree() for c in eqs)}")
def ms_poly(c):
    P = sp.Poly(c, *V).primitive()[1]
    assert all(co.is_Integer for co in P.coeffs())
    o = ""
    for mon, co in sorted(P.terms(), reverse=True):
        parts = [str(abs(co))] if abs(co) != 1 or all(e==0 for e in mon) else []
        for v, e in zip(V, mon):
            if e == 1: parts.append(str(v))
            elif e > 1: parts.append(f"{v}^{e}")
        o += ("-" if co < 0 else ("+" if o else "")) + "*".join(parts)
    return o
def emit(path, ps, char):
    txt = ",".join(map(str,V)) + f"\n{char}\n" + ",\n".join(ms_poly(p) for p in ps) + "\n"
    assert "(" not in txt and ")" not in txt, "PARENTHESIS -- A16"
    open(path,'w').write(txt); print(f"  {path}: {len(txt)} bytes")
emit('flat_p.ms', eqs, 1073741827)
emit('flat.ms', eqs, 0)
pt = {v: sp.Integer(0) for v in V}
planted = [sp.expand(c - c.subs(pt)) for c in eqs]
assert all(sp.expand(p.subs(pt)) == 0 for p in planted), "planting failed"
emit('flat_planted_p.ms', planted, 1073741827)
