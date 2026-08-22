#!/usr/bin/env python3
"""Decide v-cascade levels 4 AND 3 together.

Level 4 : 2 F_2 G_3' - 3 F_2' G_3 = r^2                (the lower edge; NONEMPTY alone)
Level 3 : 2 F_2 G_2' - 2 F_2' G_2 + F_1 G_3' - 3 F_1' G_3 = 0

Both are NECESSARY, so EMPTY on the pair => pentagon EMPTY.
Saturate every mutable Newton vertex that appears.
"""
import sympy as sp
r = sp.Symbol('r')
def P_ok(j, i): return 0 <= i <= 8 and 0 <= j <= 16 and max(0, j-8) <= i <= min(8, j//2+1)
def Q_ok(j, k):
    if not (0 <= k <= 12): return False
    lo = (k+1)//2 if k <= 2 else 2*k-3
    return lo <= j <= 12+k
def Fd(d):
    t = 0
    for i in range(9):
        j = 2*i-d
        if j >= 0 and P_ok(j,i):
            t += (sp.Integer(0) if (j,i)==(0,0) else sp.Integer(1) if (j,i)==(0,1)
                  else sp.Symbol(f'p_{j}_{i}'))*r**i
    return sp.expand(t)
def Ge(e):
    t = 0
    for k in range(13):
        j = 2*k-e
        if j >= 0 and Q_ok(j,k):
            t += (sp.Integer(0) if (j,k)==(0,0) else sp.Integer(1) if (j,k)==(1,2)
                  else sp.Symbol(f'q_{j}_{k}'))*r**k
    return sp.expand(t)
F2, F1, G3, G2 = Fd(2), Fd(1), Ge(3), Ge(2)
L4 = sp.expand(2*F2*sp.diff(G3,r) - 3*sp.diff(F2,r)*G3 - r**2)
L3 = sp.expand(2*F2*sp.diff(G2,r) - 2*sp.diff(F2,r)*G2 + 1*F1*sp.diff(G3,r) - 3*sp.diff(F1,r)*G3)
eqs = [c for c in sp.Poly(L4,r).all_coeffs() if c != 0] + \
      [c for c in sp.Poly(L3,r).all_coeffs() if c != 0]
unk = sorted(set().union(*[e.free_symbols for e in eqs]) - {r}, key=str)
print(f"levels 4+3: {len(eqs)} equations, {len(unk)} unknowns")
print("  F_1 =", F1); print("  G_2 =", G2)
verts = [v for v in ('p_14_8','q_21_12','p_8_0','p_16_8','q_12_0','q_24_12')
         if sp.Symbol(v) in unk]
print("  mutable vertices present:", verts)
p_ = 1000003
def ms(e):
    out = []
    for mono, co in sp.Poly(sp.expand(e), *unk).terms():
        t = str(int(co) % p_)
        for v, ex in zip(unk, mono):
            if ex: t += f'*{v}' + (f'^{ex}' if ex > 1 else '')
        out.append(t)
    return '+'.join(out) if out else '0'
names = [str(v) for v in unk] + [f'z{i}' for i in range(len(verts))]
body = [ms(e) for e in eqs] + [f'z{i}*{v}-1' for i, v in enumerate(verts)]
txt = ','.join(names) + f'\n{p_}\n' + ',\n'.join(body) + '\n'
open('/tmp/red/v43.ms','w').write(txt)
print(f"/tmp/red/v43.ms: {len(names)} vars, {len(body)} eqs, parens: {'(' in txt}")
