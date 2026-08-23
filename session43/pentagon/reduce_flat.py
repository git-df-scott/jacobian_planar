#!/usr/bin/env python3
"""Shrink the flat pentagon UNCONDITIONALLY, without raising its degree.

Both engines OOM at the same 13.96 GB on the full 261 x 142 degree-2 system --
msolve and Singular independently -- so the system has to get smaller before
either can finish, and it has to get smaller without assuming anything.

The safe move: a variable x that never appears in a QUADRATIC monomial occurs
in every equation with a rational coefficient only.  Any equation containing it
is c*x + R with c a nonzero rational, so x = -R/c, and substituting that into
another equation replaces a rational multiple of x by R.  Degree is preserved
exactly (nothing multiplies x, so nothing lifts R's degree), the division is by
a rational and therefore unconditional, and no vanishing locus is deleted.

Iterated to a fixed point, because eliminating one such variable can make
others quadratic-free.
"""
import sympy as sp, pickle, sys
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
V = lambda E: sorted(set().union(*[c.free_symbols for c in E]), key=str) if E else []
print(f"start: {len(eqs)} equations, {len(V(eqs))} unknowns", flush=True)
elim = {}
for rnd in range(300):
    vs = V(eqs)
    P = {c: sp.Poly(c, *vs) for c in eqs}
    quad = set()
    for c, p in P.items():
        for mon in p.monoms():
            nz = [j for j, e in enumerate(mon) if e]
            if sum(mon) >= 2:
                for j in nz: quad.add(vs[j])
    free_lin = [x for x in vs if x not in quad]
    if not free_lin:
        print(f"round {rnd}: no quadratic-free variable left", flush=True); break
    x = free_lin[0]
    piv = None
    for c in eqs:
        if x not in c.free_symbols: continue
        p = sp.Poly(c, x); c1 = p.coeff_monomial(x)
        if c1.is_number and c1 != 0: piv = (c, sp.expand(-p.coeff_monomial(1)/c1)); break
    if piv is None:
        print(f"round {rnd}: {x} quadratic-free but no rational pivot (should not happen)")
        break
    c, val = piv
    elim[x] = val
    eqs = [sp.expand(e.subs(x, val)) for e in eqs if e is not c]
    eqs = [e for e in eqs if e != 0]
    if rnd % 10 == 0 or len(free_lin) < 4:
        print(f"round {rnd:3d}: eliminated {x} -> {len(eqs)} equations, {len(V(eqs))} unknowns, "
              f"maxdeg {max(sp.Poly(e,*V(eqs)).total_degree() for e in eqs)}", flush=True)
vs = V(eqs)
print(f"\nREDUCED: {len(eqs)} equations, {len(vs)} unknowns, "
      f"maxdeg {max(sp.Poly(e,*vs).total_degree() for e in eqs)}, "
      f"{len(elim)} eliminated unconditionally")
pickle.dump((eqs, elim), open('reduced_flat.pkl','wb'))
print("saved reduced_flat.pkl", flush=True)
