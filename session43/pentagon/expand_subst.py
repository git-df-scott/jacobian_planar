#!/usr/bin/env python3
"""Rebuild subst.ms FULLY EXPANDED -- msolve's .ms reader cannot handle
parentheses and silently reports [1] (ERRATA A16).

Representation: a polynomial is a dict {monomial: coeff} where a monomial is a
sorted tuple of (var, exponent).  Substitution and expansion are done directly,
so no sympy and no parentheses ever appear in the output.
"""
import re, random
p = 1000003

def pmul(A, B):
    out = {}
    for ma, ca in A.items():
        for mb, cb in B.items():
            d = dict(ma)
            for v, e in mb: d[v] = d.get(v, 0) + e
            k = tuple(sorted(d.items()))
            out[k] = (out.get(k, 0) + ca*cb) % p
    return {k: v for k, v in out.items() if v}

def padd(A, B):
    out = dict(A)
    for m, c in B.items():
        out[m] = (out.get(m, 0) + c) % p
        if not out[m]: del out[m]
    return out

TERM = re.compile(r'([+-]?)\s*([0-9]*)\s*\*?\s*((?:[A-Za-z_][A-Za-z0-9_]*(?:\^[0-9]+)?\*?)*)')
def parse(line):
    """parse an expanded polynomial line into {monomial: coeff}"""
    out = {}
    for sign, num, mon in TERM.findall(line.replace(' ', '')):
        if not num and not mon: continue
        c = int(num) if num else 1
        if sign == '-': c = -c
        m = []
        for f in filter(None, mon.split('*')):
            if '^' in f:
                v, e = f.split('^'); m.append((v, int(e)))
            else:
                m.append((f, 1))
        d = {}
        for v, e in m: d[v] = d.get(v, 0) + e
        k = tuple(sorted(d.items()))
        out[k] = (out.get(k, 0) + c) % p
    return {k: v for k, v in out.items() if v}

def show(A):
    if not A: return '0'
    parts = []
    for m, c in sorted(A.items()):
        s = str(c % p)
        for v, e in m: s += f'*{v}' + (f'^{e}' if e > 1 else '')
        parts.append(s)
    return '+'.join(parts)

src = open('full_sat.ms').read().split('\n')
V = src[0].split(','); ch = src[1].strip()
body = [l.rstrip(',') for l in src[2:] if l.strip()]

# G = g0 + g1 t + g2 t^2 + g3 t^3 + t^4  (g4 = 1 gauge)
gpoly = [{(('g0',1),):1}, {(('g1',1),):1}, {(('g2',1),):1}, {(('g3',1),):1}, {():1}]
def convolve(A, B):
    out = [dict() for _ in range(len(A)+len(B)-1)]
    for i, a in enumerate(A):
        for j, b in enumerate(B):
            out[i+j] = padd(out[i+j], pmul(a, b))
    return out
G2 = convolve(gpoly, gpoly)
G3 = convolve(G2, gpoly)
c0 = {(('c0',1),):1}; c1 = {(('c1',1),):1}
sub = {}
for i in range(9):  sub[f'p_{i+8}_{i}']  = pmul(c0, G2[i])
for k in range(13): sub[f'q_{12+k}_{k}'] = pmul(c1, G3[k])

def apply_sub(A):
    out = {}
    for m, c in A.items():
        acc = {(): c}
        for v, e in m:
            f = sub.get(v, {((v,1),):1})
            for _ in range(e): acc = pmul(acc, f)
        out = padd(out, acc)
    return out

parsed = [parse(l) for l in body]
newbody = [apply_sub(A) for A in parsed]
newV = [v for v in V if v not in sub] + ['g0','g1','g2','g3','c0','c1']
out = ','.join(newV) + '\n' + ch + '\n' + ',\n'.join(show(A) for A in newbody) + '\n'
open('subst_exp.ms','w').write(out)
print(f"subst_exp.ms: {len(newV)} vars, {len(newbody)} eqs, {len(out)} bytes, "
      f"parens present: {'(' in out}")
print(f"max terms in an equation: {max(len(A) for A in newbody)}, "
      f"total terms: {sum(len(A) for A in newbody)}")

# ---------------------------------------------------------------- CONTROLS
rnd = random.Random(5)
env = {v: rnd.randrange(1, p) for v in V}
g = [rnd.randrange(1, p) for _ in range(4)] + [1]
C0, C1 = rnd.randrange(1, p), rnd.randrange(1, p)
w = [sum(g[a]*g[i-a] for a in range(5) if 0 <= i-a <= 4) % p for i in range(9)]
u = [sum(w[a]*g[k-a] for a in range(9) if 0 <= k-a <= 4) % p for k in range(13)]
for i in range(9):  env[f'p_{i+8}_{i}']  = C0*w[i] % p
for k in range(13): env[f'q_{12+k}_{k}'] = C1*u[k] % p
env2 = {k: v for k, v in env.items() if k not in sub}
env2.update(dict(zip(['g0','g1','g2','g3'], g[:4]))); env2['c0'], env2['c1'] = C0, C1
def ev(A, e):
    t = 0
    for m, c in A.items():
        v = c
        for var, ex in m: v = v*pow(e[var], ex, p) % p
        t = (t+v) % p
    return t
bad = sum(1 for A, B in zip(parsed, newbody) if ev(A, env) != ev(B, env2))
print(f"CONTROL (expansion value-preserving): {len(body)-bad}/{len(body)} -> "
      f"{'PASS' if bad == 0 else 'FAIL'}")
e3 = dict(env2); e3['g0'] = (e3['g0']+1) % p
diff = sum(1 for A, B in zip(parsed, newbody) if ev(A, env) != ev(B, e3))
print(f"CONTROL (negative, g0 perturbed): {diff}/{len(body)} differ -> "
      f"{'PASS' if diff > 0 else 'FAIL'}")
