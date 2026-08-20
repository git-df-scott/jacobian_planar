#!/usr/bin/env python3
"""d=12 degenerate-family existence probe (bifurcation program, step 1).

Builds the slice {mu0=0, a24=-1/12} of the reduced d=12 system (row0 forces
a24 in {-1/12, 1/20}; a degenerate family must sit at the resonant root
-1/12), then asks Singular for dim and minimal associated primes mod 65521.
Run 1: full slice (34 vars).  Run 2: additional mu2=0 slice (33 vars) --
the d=3 family satisfies the analogue, so a structurally similar d=12
family survives run 2.
NO memory cap here: run on a machine where ~10GB is free.

Usage: python3 d12slice_probe.py /path/to/repo
Report RAW Singular output (dim, number of components, the component
ideals if small).  dim >= 1 on either run = FAMILY EXISTS (report
immediately).  'no more memory' or timeout = FAILURE, not a verdict.
"""
import sys, os, subprocess
ROOT = os.path.abspath(sys.argv[1])
sys.path.insert(0, os.path.join(ROOT, 'wave5'))
os.chdir(os.path.join(ROOT, 'wave5'))
import sympy as sp
from sympy import symbols, expand, Rational
from w5_b16_abel import build_system, mu0, mu1, mu2, mu3

d = 12
eqs, unk, A, q1 = build_system(d)
a = symbols(f'a0:{2*d+1}'); b = symbols(f'b0:{d}')

for tag, extra in (('full', {}), ('mu2zero', {mu2: 0})):
    subs = {a[0]: -mu3**2/4, a[1]: 0 if extra else mu2, b[0]: mu3, b[1]: 0,
            mu1: -mu3*(a[2] + 2*b[2])/3, mu0: 0, a[24]: Rational(-1, 12)}
    subs.update(extra)
    vlist = [a[i] for i in range(2, 24)] + [b[i] for i in range(2, 12)]
    vlist += [mu3] if extra else [mu2, mu3]
    core = []
    for e in eqs:
        e2 = expand(e.subs(subs))
        if e2 == 0:
            continue
        p = sp.Poly(e2, *vlist)
        L = 1
        for c in p.coeffs():
            L = sp.lcm(L, sp.denom(c))
        core.append(sp.expand(e2 * L))
    vn = ','.join(str(v) for v in vlist)
    polys = ',\n'.join(sp.sstr(e).replace('**', '^') for e in core)
    sing = f'''ring R = 65521, ({vn}), dp;\nLIB "primdec.lib";\nideal I = {polys};\nint t0 = timer;\nideal G = std(I);\nprint("== {tag} dim:"); print(dim(G));\nprint("== {tag} vdim:"); print(vdim(G));\nprint("== std time:"); print(timer-t0);\nlist L = minAssGTZ(I);\nprint("== {tag} components:"); print(size(L));\nfor (int i=1; i<=size(L); i++) {{ print("-- comp dim:"); print(dim(std(L[i]))); if (size(string(L[i])) < 2000) {{ print(L[i]); }} }}\nquit;\n'''
    path = f'/tmp/d12slice_{tag}.sing'
    open(path, 'w').write(sing)
    print(f'[{tag}] eqs: {len(core)} vars: {len(vlist)} -> {path}', flush=True)
    r = subprocess.run(['Singular', '-q', path], capture_output=True, text=True, timeout=7000)
    print(r.stdout, flush=True)
    if r.returncode != 0:
        print(f'[{tag}] SINGULAR-EXIT {r.returncode} (failure, not verdict)', r.stderr[:300], flush=True)
