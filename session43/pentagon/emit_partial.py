#!/usr/bin/env python3
"""Use a PARTIAL descent as a preconditioner for msolve.

The descent's only job is variable reduction, and a partial reduction is still
a reduction.  nodivide4 stalls mid level 12, but by then it has already solved
81 unknowns on rational pivots -- unconditionally, no divisions by symbolic
quantities, no branch choices.  So instead of handing msolve the raw system
(261 equations, 142 unknowns, which OOM-ed both engines at 13.96 GB), hand it

    the conditions already carried out
  + every remaining level equation with the substitutions applied

which is the same variety in far fewer variables.  Waiting for the descent to
finish was never necessary.
"""
import sympy as sp, pickle, sys, os
CK = sys.argv[1] if len(sys.argv) > 1 else 'nodivide4.ckpt'
TAG = sys.argv[2] if len(sys.argv) > 2 else 'partial4'
z = sp.Symbol('z'); TAU = sp.Integer(1); s = z + TAU
def hsup(a):
    return [i for i in range(9) if 0 <= i+a <= 16 and max(0,(i+a)-8) <= i <= min(8,(i+a)//2+1)]
def gsup(b):
    return [k for k in range(13) if (k+b) >= 0 and ((k+1)//2 if k <= 2 else 2*k-3) <= k+b <= 12+k]
H = {8: z**8, -1: sp.expand(s)}
G = {12: z**12, -1: sp.expand(s**2)}
for a in range(0, 8): H[a] = sum(sp.Symbol(f'h{a}_{i}')*z**i for i in hsup(a))
for b in range(0, 12): G[b] = sum(sp.Symbol(f'g{b}_{k}')*z**k for k in gsup(b))
def lev(L):
    e = 0
    for a in range(-1, 9):
        b = L-a
        if a in H and b in G: e += b*sp.diff(H[a],z)*G[b] - a*H[a]*sp.diff(G[b],z)
    return sp.expand(e - (s**2 if L == -2 else 0))
if os.path.exists(CK + '.mid'):
    L0, sub, USES, conds, eqs_left, new, solved = pickle.load(open(CK + '.mid','rb'))
    print(f"loaded MID checkpoint at level {L0}: {solved} solved, {len(conds)} conditions")
    conds = list(conds) + list(eqs_left)
else:
    L0, sub, USES, conds = pickle.load(open(CK,'rb'))
    print(f"loaded checkpoint after level {L0}: {len(conds)} conditions")
    L0 -= 1
polys = [sp.expand(c) for c in conds]
for L in range(L0, -3, -1):
    e = sp.expand(lev(L).subs(sub))
    if e == 0: continue
    polys += [sp.expand(c) for c in sp.Poly(e, z).all_coeffs() if c != 0]
polys = [p for p in polys if sp.expand(p) != 0]
seen, uniq = set(), []
for p in polys:
    vs = sorted(p.free_symbols, key=str)
    if not vs: 
        print(f"*** a condition is the nonzero constant {p} -> EMPTY ***"); sys.exit(0)
    q = sp.Poly(p, *vs).primitive()[1]
    q = q if q.LC() > 0 else -q
    k = sp.srepr(q.as_expr())
    if k not in seen: seen.add(k); uniq.append(q.as_expr())
polys = uniq
V = sorted(set().union(*[p.free_symbols for p in polys]), key=str)
print(f"{TAG}: {len(polys)} polys, {len(V)} vars, "
      f"max degree {max(sp.Poly(p,*V).total_degree() for p in polys)}")
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
emit(f'{TAG}.ms', polys, 0)
emit(f'{TAG}_p.ms', polys, 1073741827)
pt = {v: sp.Integer(0) for v in V}
planted = [sp.expand(p - p.subs(pt)) for p in polys]
assert all(sp.expand(p.subs(pt)) == 0 for p in planted), "planting failed"
emit(f'{TAG}_planted_p.ms', planted, 1073741827)
