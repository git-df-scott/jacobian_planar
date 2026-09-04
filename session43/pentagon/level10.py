#!/usr/bin/env python3
"""Level 10, targeted.  Rebuild the descent to 11 with the impositions already
found, then extract level 10's obstruction conditions by NULLSPACE (cheap) and
hand them to msolve rather than sp.solve (which does not finish on 26 symbols).

Known impositions from the full descent (ce_descent.py):
    L=15 : g11_11 = 0                       (lambda = 0)
    L=14 : g9_10 = 3(h5_6 + 16 h5_7^2)/2 , h5_0 = h5_1 = 0
    L=13 : g9_9 = 3 h5_5/2 , h4_0 = h4_1 = 0 , h5_7 = 0
    L=12 : h3_0 = h3_1 = 0 , h4_6 = h5_6
    L=11 : g7_7 = 3(h3_3 + h4_3)/2 , h5_2 = h5_3 = 0
"""
import sympy as sp, sys
z = sp.Symbol('z'); TAU = sp.Integer(1); s = z + TAU
def hsup(a):
    return [i for i in range(9) if 0 <= i+a <= 16 and max(0,(i+a)-8) <= i <= min(8,(i+a)//2+1)]
def gsup(b):
    return [k for k in range(13) if (k+b) >= 0 and ((k+1)//2 if k <= 2 else 2*k-3) <= k+b <= 12+k]
H = {8: z**8, 7: 2*z**8, 6: z**8, -1: sp.expand(s)}
G = {12: z**12, -1: sp.expand(s**2)}
SY = []
for a in range(0, 6):
    cs = [sp.Symbol(f'h{a}_{i}') for i in hsup(a)]; SY += cs
    H[a] = sum(cs[j]*z**i for j, i in enumerate(hsup(a)))
for b in range(0, 12):
    cs = [sp.Symbol(f'g{b}_{k}') for k in gsup(b)]; SY += cs
    G[b] = sum(cs[j]*z**k for j, k in enumerate(gsup(b)))
def lev(L):
    e = 0
    for a in range(-1, 9):
        b = L-a
        if a in H and b in G: e += b*sp.diff(H[a],z)*G[b] - a*H[a]*sp.diff(G[b],z)
    return sp.expand(e - (s**2 if L == -2 else 0))
S = lambda n: sp.Symbol(n)
sub = {S('g11_11'): sp.Integer(0),
       S('h5_0'): sp.Integer(0), S('h5_1'): sp.Integer(0),
       S('h4_0'): sp.Integer(0), S('h4_1'): sp.Integer(0), S('h5_7'): sp.Integer(0),
       S('h3_0'): sp.Integer(0), S('h3_1'): sp.Integer(0),
       S('h5_2'): sp.Integer(0), S('h5_3'): sp.Integer(0)}
def res(e):
    for _ in range(14):
        e2 = sp.expand(e.subs(sub))
        if e2 == e: return e2
        e = e2
    return e
for L in range(19, 10, -1):
    e = res(lev(L))
    eqs = [c for c in (sp.Poly(e, z).all_coeffs() if e != 0 else []) if c != 0]
    if not eqs: print(f"  L={L}: identically satisfied", flush=True); continue
    unk = sorted({v for v in set().union(*[c.free_symbols for c in eqs]) if v in SY}
                 - set(sub), key=str)
    M, v = sp.linear_eq_to_matrix(eqs, unk)
    rM, rA = M.rank(), M.row_join(v).rank()
    if rM != rA: print(f"  L={L}: INCONSISTENT with the recorded impositions", flush=True); sys.exit(1)
    sol = sp.solve(eqs, unk, dict=True)[0]
    sub.update({k: sp.expand(vv) for k, vv in sol.items()})
    for _ in range(4):
        sub = {k: (sp.expand(vv.subs(sub)) if hasattr(vv,'subs') else vv) for k,vv in sub.items()}
    print(f"  L={L}: solved ({len(sol)} of {len(unk)})", flush=True)
print("\nLEVEL 10:", flush=True)
e = res(lev(10))
eqs = [c for c in sp.Poly(e, z).all_coeffs() if c != 0]
carried = sorted({v for v in set().union(*[c.free_symbols for c in eqs]) if v in SY}
                 - set(sub), key=str)
new = [v for v in carried if v.name.startswith('g2_')]
par = [v for v in carried if v not in new]
print(f"   {len(eqs)} equations, {len(new)} new (g_2), {len(par)} carried parameters", flush=True)
M, v = sp.linear_eq_to_matrix(eqs, new) if new else (None, None)
conds = []
if M is not None:
    for n in M.T.nullspace():
        val = sp.cancel(sp.expand((n.T*v)[0,0]))
        if val != 0: conds.append(sp.numer(sp.together(val)))
print(f"   {len(conds)} obstruction condition(s) in the carried parameters", flush=True)
p = 1000003
vs = sorted(set().union(*[c.free_symbols for c in conds]), key=str) if conds else []
print(f"   involving {len(vs)} parameters: {[str(x) for x in vs][:12]}", flush=True)
if conds:
    def ms(e_):
        out = []
        for mono, co in sp.Poly(sp.expand(e_), *vs).terms():
            t = str(int(co) % p)
            for var, ex in zip(vs, mono):
                if ex: t += f'*{var}' + (f'^{ex}' if ex > 1 else '')
            out.append(t)
        return '+'.join(out) if out else '0'
    body = [ms(c) for c in conds]
    txt = ','.join(str(x) for x in vs) + f'\n{p}\n' + ',\n'.join(body) + '\n'
    open('/tmp/red/level10.ms','w').write(txt)
    print(f"   wrote /tmp/red/level10.ms  ({len(vs)} vars, {len(body)} eqs, "
          f"parens: {'(' in txt})", flush=True)
    for c in conds[:2]: print("   COND:", str(sp.factor(c))[:220], flush=True)
