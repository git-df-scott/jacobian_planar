#!/usr/bin/env python3
"""Add the upper-edge theorem to Codex's degree-2 polynomial-Q target.

  A(t)  = sum_{i=0..8}  p_{i+8,i} t^i  = c0 * G(t)^2
  Qh(t) = sum_{k=0..12} q_{12+k,k} t^k = c1 * G(t)^3      (deg G = 4)

Encoded at DEGREE 2 throughout by naming the intermediate powers:
    w_i - sum_{a+b=i} g_a g_b        = 0      (w = G^2)      9 eqs
    p_{i+8,i} - c0 * w_i             = 0                     9 eqs
    u_k - sum_{a+b=k} w_a g_b        = 0      (u = G^3)     13 eqs
    q_{12+k,k} - c1 * u_k            = 0                    13 eqs

Gauge g4 = 1 (rescales G, absorbed into c0 and c1).  No extra saturation is
needed: p_16_8 = c0 * g4^2 = c0 and p_8_0 = c0 * g0^2 are already saturated in
Codex's file, forcing c0 != 0 and g0 != 0.
"""
import sys
p = 1000003
src = open('full_sat.ms').read().split('\n')
varline, charline = src[0], src[1]
body = [l for l in src[2:] if l.strip()]
V = varline.split(',')
print(f"original: {len(V)} vars, {len(body)} equations, char line {charline.strip()}")

g = [f'g{i}' for i in range(5)]
w = [f'w{i}' for i in range(9)]
u = [f'u{i}' for i in range(13)]
new = g[:4] + ['c0', 'c1'] + w + u          # g4 gauged to 1
def G(i):  return '1' if i == 4 else g[i]

eqs = []
for i in range(9):                                   # w = G^2
    t = [f'{G(a)}*{G(i-a)}' for a in range(5) if 0 <= i-a <= 4]
    eqs.append(f'{w[i]}-({"+".join(t)})')
for i in range(9):                                   # p upper row = c0 * w
    eqs.append(f'p_{i+8}_{i}-c0*{w[i]}')
for k in range(13):                                  # u = G^3 = w * G
    t = [f'{w[a]}*{G(k-a)}' for a in range(9) if 0 <= k-a <= 4]
    eqs.append(f'{u[k]}-({"+".join(t)})')
for k in range(13):                                  # q upper row = c1 * u
    eqs.append(f'q_{12+k}_{k}-c1*{u[k]}')

missing = [v for v in [f'p_{i+8}_{i}' for i in range(9)] + [f'q_{12+k}_{k}' for k in range(13)]
           if v not in V]
assert not missing, f"variables absent from the export: {missing}"

out = ','.join(V + new) + '\n' + charline + '\n' + ',\n'.join(body + eqs) + '\n'
open('reduced.ms', 'w').write(out)
print(f"reduced.ms: {len(V)+len(new)} vars, {len(body)+len(eqs)} equations, "
      f"{len(out)} bytes, all added equations degree <= 2")

# ------------------------------------------------------------------ CONTROL
import random
rnd = random.Random(7)
gv = [rnd.randrange(1, p) for _ in range(4)] + [1]
c0, c1 = rnd.randrange(1, p), rnd.randrange(1, p)
wv = [sum(gv[a]*gv[i-a] for a in range(5) if 0 <= i-a <= 4) % p for i in range(9)]
uv = [sum(wv[a]*gv[k-a] for a in range(9) if 0 <= k-a <= 4) % p for k in range(13)]
env = {f'g{i}': gv[i] for i in range(5)}
env.update({f'w{i}': wv[i] for i in range(9)})
env.update({f'u{i}': uv[i] for i in range(13)})
env['c0'], env['c1'] = c0, c1
for i in range(9):  env[f'p_{i+8}_{i}'] = c0*wv[i] % p
for k in range(13): env[f'q_{12+k}_{k}'] = c1*uv[k] % p
bad = 0
for e in eqs:
    val = eval(e.replace('^', '**'), {}, {k: v for k, v in env.items()}) % p
    if val: bad += 1
print(f"CONTROL (encoding): {len(eqs)-bad}/{len(eqs)} added equations vanish on a "
      f"random (G, c0, c1) point -> {'PASS' if bad == 0 else 'FAIL'}")
# negative control: perturb one g and the p-row equations must break
env2 = dict(env); env2['g0'] = (env2['g0'] + 1) % p
nz = sum(1 for e in eqs if eval(e.replace('^','**'), {}, env2) % p)
print(f"CONTROL (negative, g0 perturbed): {nz}/{len(eqs)} equations now nonzero -> "
      f"{'PASS' if nz > 0 else 'FAIL'}")
