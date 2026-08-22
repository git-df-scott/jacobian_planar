#!/usr/bin/env python3
"""Substitute the EIGHTH-POWER theorem into Codex's degree-2 export.

    p_{i+8,i}  = p_16_8 * C(8,i)  * tau^(8-i)      i = 0..7   (i=8 is p_16_8 itself)
    q_{12+k,k} = c1     * C(12,k) * tau^(12-k)     k = 0..12
    p_15_7     = -8 * p_16_8 * tau                 (tau = -p_15_7/(8 p_16_8))

Degree is held down by naming the powers:  T_j = tau^j, T_0 = 1,
    T_j - tau*T_{j-1} = 0    (degree 2)
so each substitution is a single degree-2 product and the substituted degree-2
equations reach degree 4 at worst.

Output is FULLY EXPANDED -- msolve reports a false EMPTY on parenthesised
input (ERRATA A16).
"""
import re, random
from math import comb
p = 1000003
exec(open('expand_subst.py').read().split('src = open')[0])   # pmul/padd/parse/show

src = open('full_sat.ms').read().split('\n')
V = src[0].split(','); ch = src[1].strip()
body = [l.rstrip(',') for l in src[2:] if l.strip()]

def mono(*vs):
    d = {}
    for v in vs: d[v] = d.get(v, 0) + 1
    return {tuple(sorted(d.items())): 1}
T = {0: {(): 1}}
for j in range(1, 13): T[j] = mono(f'T{j}')

sub = {}
for i in range(8):
    sg = 1 if (8-i) % 2 == 0 else -1          # (t-tau)^8 : coeff = C(8,i)*(-tau)^(8-i)
    sub[f'p_{i+8}_{i}'] = {k: (sg*comb(8, i)*v) % p for k, v in pmul(mono('p_16_8'), T[8-i]).items()}
for k in range(13):
    sg = 1 if (12-k) % 2 == 0 else -1
    sub[f'q_{12+k}_{k}'] = {kk: (sg*comb(12, k)*v) % p for kk, v in pmul(mono('c1'), T[12-k]).items()}
assert 'p_15_7' in sub   # i=7 IS p_15_7; the tau<->p_15_7 link is this substitution itself

def apply_sub(A):
    out = {}
    for m, c in A.items():
        acc = {(): c}
        for v, e in m:
            f = sub.get(v, {((v, 1),): 1})
            for _ in range(e): acc = pmul(acc, f)
        out = padd(out, acc)
    return out

parsed = [parse(l) for l in body]
new = [apply_sub(A) for A in parsed]
# defining equations for the tau powers, plus the tau <-> p_15_7 link
extra = []
for j in range(1, 13):
    prev = mono('tau') if j == 1 else pmul(mono('tau'), T[j-1])
    extra.append(padd(T[j], {k: (-v) % p for k, v in prev.items()}))


newV = [v for v in V if v not in sub] + ['tau'] + [f'T{j}' for j in range(1, 13)] + ['c1']
out = ','.join(newV) + '\n' + ch + '\n' + ',\n'.join(show(A) for A in new + extra) + '\n'
open('eighth.ms', 'w').write(out)
deg = max(max(sum(e for _, e in m) for m in A) for A in new + extra if A)
print(f"eighth.ms: {len(newV)} vars (was {len(V)}), {len(new)+len(extra)} eqs, "
      f"{len(out)} bytes, max degree {deg}, parens: {'(' in out}")

# ---------------------------------------------------------------- CONTROLS
rnd = random.Random(3)
env = {v: rnd.randrange(1, p) for v in V}
tau = rnd.randrange(1, p); c1 = rnd.randrange(1, p)
a = env['p_16_8']
for i in range(8):  env[f'p_{i+8}_{i}']  = (1 if (8-i)%2==0 else -1)*a*comb(8, i)*pow(tau, 8-i, p) % p
for k in range(13): env[f'q_{12+k}_{k}'] = (1 if (12-k)%2==0 else -1)*c1*comb(12, k)*pow(tau, 12-k, p) % p

env2 = {k: v for k, v in env.items() if k not in sub}
env2['tau'] = tau; env2['c1'] = c1
for j in range(1, 13): env2[f'T{j}'] = pow(tau, j, p)
def ev(A, e):
    t = 0
    for m, c in A.items():
        v = c
        for var, ex in m: v = v*pow(e[var], ex, p) % p
        t = (t+v) % p
    return t
bad = sum(1 for A, B in zip(parsed, new) if ev(A, env) != ev(B, env2))
print(f"CONTROL (substitution value-preserving): {len(body)-bad}/{len(body)} -> "
      f"{'PASS' if bad == 0 else 'FAIL'}")
ez = sum(1 for A in extra if ev(A, env2) != 0)
print(f"CONTROL (tau-power defining equations vanish): {len(extra)-ez}/{len(extra)} -> "
      f"{'PASS' if ez == 0 else 'FAIL'}")
# negative control: perturb tau AND recompute every T_j (the body equations
# reference T_j, not tau, so moving tau alone would prove nothing)
t2 = (tau+1) % p
e3 = dict(env2); e3['tau'] = t2
for j in range(1, 13): e3[f'T{j}'] = pow(t2, j, p)
d3 = sum(1 for A, B in zip(parsed, new) if ev(A, env) != ev(B, e3))
print(f"CONTROL (negative, tau and all T_j perturbed): {d3}/{len(body)} differ -> "
      f"{'PASS' if d3 > 0 else 'FAIL'}")
# and an inconsistent-T control: T_j left stale while tau moves must break the
# 12 defining equations
e4 = dict(env2); e4['tau'] = t2
ez4 = sum(1 for A in extra if ev(A, e4) != 0)
print(f"CONTROL (negative, stale T_j vs moved tau): {ez4}/{len(extra)} defining "
      f"equations break -> {'PASS' if ez4 > 0 else 'FAIL'}")
