#!/usr/bin/env python3
"""VERIFICATION SWEEP: re-check tonight's theorems against CODEX'S export.

The theorems were derived from MY reconstruction of the pentagon's supports.
Codex's p11zero_full_sat_p1000003.ms was built independently from the bracket.
Testing the theorems against HIS equations is therefore a genuine cross-check,
not a restatement.

Method: substitute each claimed family into his equations at random points over
F_p and count how many of his equations vanish.  A theorem that is a consequence
of the bracket must satisfy the corresponding graded block exactly.
"""
import re, random
from math import comb
from collections import defaultdict
p = 1000003
src = open('full_sat.ms').read().split('\n')
V = src[0].split(','); body = [l.rstrip(',') for l in src[2:] if l.strip()]

def wof(v):
    m = re.fullmatch(r'([pq])_(\d+)_(\d+)', v)
    return None if not m else int(m.group(2)) - int(m.group(3))
TERM = re.compile(r'[+-]?\s*\d*\s*\*?\s*((?:[A-Za-z_][A-Za-z0-9_]*(?:\^\d+)?\*?)*)')
def level_of(l):
    ws = set()
    for mon in TERM.findall(l.replace(' ', '')):
        if not mon: continue
        tot = 0; n = 0; ok = True
        for f in filter(None, mon.split('*')):
            v, e = (f.split('^')[0], int(f.split('^')[1])) if '^' in f else (f, 1)
            r = wof(v)
            if r is None: ok = False; break
            tot += r*e; n += e
        if ok: ws.add(tot - (2-n))
    return ws.pop() if len(ws) == 1 else None

blocks = defaultdict(list)
for l in body:
    if 'sat_' in l: continue
    L = level_of(l)
    if L is not None: blocks[L].append(l)

def ev(l, env):
    return eval(l.replace('^', '**'), {}, env) % p

def run(name, mk, target_levels, expect_pass, trials=5):
    tot = ok = 0
    for s in range(trials):
        env = {v: random.Random(s*7+1).randrange(1, p) for v in V}
        mk(env, random.Random(s*13+5))
        for L in target_levels:
            for l in blocks[L]:
                tot += 1
                if ev(l, env) == 0: ok += 1
    verdict = "PASS" if (ok == tot) == expect_pass else "FAIL"
    print(f"  {name:52s} {ok:4d}/{tot:4d} vanish -> {verdict}")
    return verdict == "PASS"

def set_upper(env, rnd, kind):
    a = rnd.randrange(1, p); c1 = rnd.randrange(1, p)
    if kind == 'eighth':
        tau = rnd.randrange(1, p)
        A  = [a*comb(8, i) % p * pow(-tau % p, 8-i, p) % p for i in range(9)]
        Qh = [c1*comb(12, k) % p * pow(-tau % p, 12-k, p) % p for k in range(13)]
    elif kind == 'square':
        g = [rnd.randrange(1, p) for _ in range(5)]
        G2 = [sum(g[i]*g[j] for i in range(5) for j in range(5) if i+j == m) % p for m in range(9)]
        G3 = [sum(G2[i]*g[j] for i in range(9) for j in range(5) if i+j == m) % p for m in range(13)]
        A  = [a*v % p for v in G2]; Qh = [c1*v % p for v in G3]
    else:                                   # generic, should FAIL
        A  = [rnd.randrange(1, p) for _ in range(9)]
        Qh = [rnd.randrange(1, p) for _ in range(13)]
    for i in range(9):
        if f'p_{i+8}_{i}' in env: env[f'p_{i+8}_{i}'] = A[i]
    for k in range(13):
        if f'q_{12+k}_{k}' in env: env[f'q_{12+k}_{k}'] = Qh[k]

print("VERIFICATION SWEEP against Codex's independently-built export")
print(f"  ({len(body)} equations, graded into {len(blocks)} w-levels)\n")
print("LEVEL 20 (the upper-edge block, 19 equations):")
r = []
r.append(run("upper-edge family A=c0G^2, Qh=c1G^3", lambda e, g: set_upper(e, g, 'square'), [20], True))
r.append(run("eighth-power family A=c0(t-tau)^8", lambda e, g: set_upper(e, g, 'eighth'), [20], True))
r.append(run("NEGATIVE: generic A, Qh (must NOT vanish)", lambda e, g: set_upper(e, g, 'generic'), [20], False))
print("\nLEVEL 19 (must NOT be satisfied by the top block alone):")
r.append(run("eighth-power family, level 19 (expect FAIL)", lambda e, g: set_upper(e, g, 'eighth'), [19], False))
print(f"\nSWEEP: {sum(r)}/{len(r)} checks as expected")
