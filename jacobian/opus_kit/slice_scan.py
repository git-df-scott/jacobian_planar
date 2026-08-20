#!/usr/bin/env python3
"""HORIZONTAL SLICE SCAN -- the mu3=0 slice of the saturated (mu0 != 0)
GGV cell, swept across d = 13..N: virgin territory no one has evaluated.

Soundness: any solution found IS a full solution (a counterexample seed);
an empty slice closes nothing (it is a hunt, not a closure).
Controls (MUST run first): the d=5 and d=7 slices must return [-1] --
those cells are proven EMPTY, so their slices must be too.  If either
control fails to return [-1], STOP and report CONTROL-FAILURE.

Usage: python3 slice_scan.py /path/to/repo [dmax=22] [budget=300]
Per d: builds the system (sympy; build time grows with d -- report it),
applies mu3=0 (which forces a0=b0=b1=mu1=0, a1=mu2), appends saturation
t*mu0-1, exports msolve input mod 1000003, runs msolve -t 2 at budget.
Verdicts: [-1] = SLICE-EMPTY; other output = CANDIDATE-RAW (report head
immediately, prominently); no output = FAILURE not verdict; timeout =
TIMEOUT.  Results stream to wave6/slice_scan_results.json.
"""
import sys, os, json, subprocess, time
ROOT = os.path.abspath(sys.argv[1])
DMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 22
BUDGET = int(sys.argv[3]) if len(sys.argv) > 3 else 300
sys.path.insert(0, os.path.join(ROOT, 'wave5'))
os.chdir(os.path.join(ROOT, 'wave5'))
import sympy as sp
from sympy import symbols, expand, Symbol, Poly
from w5_b16_abel import build_system, mu0, mu1, mu2, mu3

t = Symbol('t')
OUTD = os.path.join(ROOT, 'wave6')
os.makedirs(OUTD, exist_ok=True)
results = []

def run_d(d):
    t0 = time.time()
    eqs, unk, A, q1 = build_system(d)
    a = symbols(f'a0:{2*d+1}'); b = symbols(f'b0:{d}')
    subs = {mu3: 0, a[0]: 0, b[0]: 0, b[1]: 0, mu1: 0, a[1]: mu2}
    core = []
    vlist = [a[i] for i in range(2, 2*d+1)] + [b[i] for i in range(2, d)] + [mu0, mu2, t]
    for e in eqs:
        e2 = expand(e.subs(subs))
        if e2 == 0:
            continue
        p = Poly(e2, *vlist)
        L = 1
        for c in p.coeffs():
            L = sp.lcm(L, sp.denom(c))
        core.append(expand(e2 * L))
    core.append(expand(t*mu0 - 1))
    build_secs = round(time.time() - t0, 1)
    head = ','.join(str(v) for v in vlist) + '\n1000003\n'
    body = ',\n'.join(str(Poly(e, *vlist).as_expr()).replace('**', '^').replace(' ', '') for e in core)
    ms = os.path.join(OUTD, f'slice_mu3z_d{d}.ms')
    open(ms, 'w').write(head + body + '\n')
    out = os.path.join(OUTD, f'slice_mu3z_d{d}.out')
    t1 = time.time()
    try:
        subprocess.run(['msolve', '-t', '2', '-f', ms, '-o', out], timeout=BUDGET)
    except subprocess.TimeoutExpired:
        return {'d': d, 'verdict': 'TIMEOUT', 'build_secs': build_secs, 'eqs': len(core), 'vars': len(vlist)}
    data = open(out).read(80) if os.path.exists(out) else ''
    if data.startswith('[-1]'):
        v = 'SLICE-EMPTY'
    elif not data:
        v = 'NO-OUTPUT-FAILURE'
    else:
        v = 'CANDIDATE-RAW'
    return {'d': d, 'verdict': v, 'head': data[:60], 'build_secs': build_secs,
            'solve_secs': round(time.time() - t1, 1), 'eqs': len(core), 'vars': len(vlist)}

for d in [5, 7] + list(range(13, DMAX + 1)):
    r = run_d(d)
    r['control'] = d in (5, 7)
    print(json.dumps(r), flush=True)
    results.append(r)
    json.dump(results, open(os.path.join(OUTD, 'slice_scan_results.json'), 'w'), indent=1)
    if d in (5, 7) and r['verdict'] != 'SLICE-EMPTY':
        print('CONTROL-FAILURE at d=%d: expected [-1]. STOP and report.' % d, flush=True)
        sys.exit(1)
print('SLICE-SCAN-DONE', flush=True)
