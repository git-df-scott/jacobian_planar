#!/usr/bin/env python3
"""Decide the lower-edge relation outright.

    2 Ah Qh' - 3 Ah' Qh = r^2
    Ah = r + p_2_2 r^2 + p_4_3 r^3 + ... + p_14_8 r^8     (p_0_1 = 1, gauge)
    Qh = r^2 + q_3_3 r^3 + ... + q_21_12 r^12             (q_1_2 = 1, gauge)

Lowest order is automatic: 2*r*(2r) - 3*1*r^2 = r^2.  So the content is the
vanishing of the r^3..r^19 coefficients: **17 equations in 17 unknowns**, with
the mutable vertices p_14_8 != 0 and q_21_12 != 0.

This is a NECESSARY condition on the pentagon, so EMPTY here => pentagon EMPTY.
"""
import sympy as sp
r = sp.Symbol('r')
pv = [sp.Symbol(f'p_{2*i-2}_{i}') for i in range(2, 9)]
qv = [sp.Symbol(f'q_{2*k-3}_{k}') for k in range(3, 13)]
Ah = r + sum(pv[i-2]*r**i for i in range(2, 9))
Qh = r**2 + sum(qv[k-3]*r**k for k in range(3, 13))
E = sp.expand(2*Ah*sp.diff(Qh, r) - 3*sp.diff(Ah, r)*Qh - r**2)
P = sp.Poly(E, r)
print("CONTROL: the r^2 coefficient must vanish identically (the gauges):",
      sp.expand(P.coeff_monomial(r**2)) == 0)
print("CONTROL: r^0, r^1 coefficients:", P.coeff_monomial(r**0), P.coeff_monomial(r**1))
eqs = [sp.expand(P.coeff_monomial(r**d)) for d in range(3, 20)]
eqs = [e for e in eqs if e != 0]
unk = pv + qv
print(f"\nsystem: {len(eqs)} equations, {len(unk)} unknowns  (square: "
      f"{len(eqs) == len(unk)})")
p_ = 1000003
def ms(e):
    out = []
    for mono, co in sp.Poly(sp.expand(e), *unk).terms():
        t = str(int(co) % p_)
        for v, ex in zip(unk, mono):
            if ex: t += f'*{v}' + (f'^{ex}' if ex > 1 else '')
        out.append(t)
    return '+'.join(out) if out else '0'
names = [str(v) for v in unk] + ['zp', 'zq']
body = [ms(e) for e in eqs] + ['zp*p_14_8-1', 'zq*q_21_12-1']
txt = ','.join(names) + f'\n{p_}\n' + ',\n'.join(body) + '\n'
open('/tmp/red/loweredge.ms','w').write(txt)
print(f"/tmp/red/loweredge.ms: {len(names)} vars, {len(body)} eqs, parens: {'(' in txt}")
print("   saturated: p_14_8 != 0 and q_21_12 != 0 (both mutable Newton vertices)")
