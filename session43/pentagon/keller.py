#!/usr/bin/env python3
"""Generic Keller search at a degree pair (m,n) -- no Newton polygon ansatz.

By Jung-van der Kulk every polynomial automorphism of C^2 has one of deg P,
deg Q dividing the other.  So for any pair with m does not divide n and n does
not divide m, a Keller map with EXACTLY those degrees cannot be an automorphism,
and therefore IS a counterexample to JC2.

That makes this the whole conjecture at (m,n), with no ansatz at all:

    P = sum_{i+j<=m} p_ij x^i y^j ,  Q = sum_{i+j<=n} q_ij x^i y^j
    P_x Q_y - P_y Q_x = 1                       (Keller, normalised)
    deg P = m exactly, deg Q = n exactly        (else the pair is not (m,n))

The exact-degree conditions are the interesting part.  "Some degree-m
coefficient of P is nonzero" is a UNION of charts, so it is handled by
Rabinowitsch one chart at a time: adjoin t and the equation c*t - 1 for the
chosen leading coefficient c.  The pair is empty iff every chart is empty.

Constant terms are gauge: P and Q may each be shifted by a constant without
changing the bracket, so p_00 = q_00 = 0.
"""
import sympy as sp, sys, itertools, subprocess, os
# Characteristic 0 times out at 23 unknowns within a 120s per-chart budget.
# Mod p the same charts finish.  For a SEARCH that is the right trade: a
# NONEMPTY mod p hands back a liftable candidate, which is what a counterexample
# hunt needs, while an EMPTY mod p is evidence rather than proof (a bad prime can
# manufacture a false EMPTY).  The (2,3) negative control was already settled in
# characteristic 0, so nothing rests on mod p alone.
CHAR = int(os.environ.get('CHAR', '1073741827'))
x, y, t1, t2 = sp.symbols('x y t1 t2')
def run(m, n, verbose=True):
    P = sum(sp.Symbol(f'p{i}_{j}')*x**i*y**j
            for i in range(m+1) for j in range(m+1-i) if (i or j))
    Q = sum(sp.Symbol(f'q{i}_{j}')*x**i*y**j
            for i in range(n+1) for j in range(n+1-i) if (i or j))
    br = sp.expand(sp.diff(P,x)*sp.diff(Q,y) - sp.diff(P,y)*sp.diff(Q,x) - 1)
    base = [c for c in sp.Poly(br, x, y).coeffs() if c != 0]
    ptop = [sp.Symbol(f'p{i}_{m-i}') for i in range(m+1)]
    qtop = [sp.Symbol(f'q{i}_{n-i}') for i in range(n+1)]
    charts, results = list(itertools.product(ptop, qtop)), []
    import json as _j, os as _o, time as _t
    CC = f'kelchart_{m}_{n}.json'
    cache = _j.load(open(CC)) if _o.path.exists(CC) else {}
    DL = _t.time() + float(_o.environ.get('SLICE','430'))
    if verbose:
        print(f"({m},{n}): {len(base)} bracket equations, "
              f"{len(br.free_symbols - {x,y})} unknowns, {len(charts)} charts")
    for ci, (pc, qc) in enumerate(charts):
        if str(ci) in cache:
            results.append((pc, qc, cache[str(ci)])); continue
        if _t.time() > DL:
            print(f"  slice deadline after {len(cache)} of {len(charts)} charts; rerun",
                  flush=True)
            _j.dump(cache, open(CC,'w')); sys.exit(3)
        polys = base + [pc*t1 - 1, qc*t2 - 1]
        V = sorted(set().union(*[p.free_symbols for p in polys]), key=str)
        nm = {v: str(v).replace('-','m') for v in V}
        def ms(c):
            Pp = sp.Poly(c, *V).primitive()[1]
            o = ""
            for mon, co in sorted(Pp.terms(), reverse=True):
                parts = [str(abs(co))] if abs(co) != 1 or all(e==0 for e in mon) else []
                for v, e in zip(V, mon):
                    if e == 1: parts.append(nm[v])
                    elif e > 1: parts.append(f"{nm[v]}^{e}")
                o += ("-" if co < 0 else ("+" if o else "")) + "*".join(parts)
            return o
        txt = ",".join(nm[v] for v in V) + f"\n{CHAR}\n" + ",\n".join(ms(p) for p in polys) + "\n"
        assert "(" not in txt and ")" not in txt, "PARENTHESIS -- A16"
        f = f'kel_{m}_{n}_{ci}.ms'
        open(f,'w').write(txt)
        r = subprocess.run(['timeout','100','msolve','-g','2','-f',f,'-o',f+'.gb'],
                           capture_output=True)
        gb = open(f+'.gb').read() if os.path.exists(f+'.gb') else ''
        if 'length of basis' not in gb:
            results.append((pc, qc, 'TIMEOUT')); cache[str(ci)] = 'TIMEOUT'
            _j.dump(cache, open(CC,'w')); continue
        ln = [l for l in gb.splitlines() if 'length of basis' in l][0]
        v = 'EMPTY' if '1 element' in ln else 'NONEMPTY'
        results.append((pc, qc, v)); cache[str(ci)] = v
        _j.dump(cache, open(CC,'w'))
        for junk in (f, f+'.gb'):
            if _o.path.exists(junk): _o.remove(junk)
    _j.dump(cache, open(CC,'w'))
    return results
import json, os
DONE = json.load(open('keller_results.json')) if os.path.exists('keller_results.json') else {}
PAIRS = [(2,3),(3,4),(2,5),(3,5),(4,5),(4,6),(2,7),(3,7),(5,6),(4,7)]
for (m, n) in PAIRS:
    if f'{m},{n}' in DONE:
        print(f'({m},{n}): cached -> {DONE[f"{m},{n}"]}'); continue
    assert n % m and m % n, "one degree divides the other -- automorphisms exist, not a CE test"
    res = run(m, n)
    ne = [r for r in res if r[2] == 'NONEMPTY']
    to = [r for r in res if r[2] == 'TIMEOUT']
    print(f"  -> {len(res)} charts: {sum(1 for r in res if r[2]=='EMPTY')} EMPTY, "
          f"{len(ne)} NONEMPTY, {len(to)} TIMEOUT")
    for r in ne: print(f"     *** NONEMPTY chart: {r[0]} != 0, {r[1]} != 0 ***")
    DONE[f'{m},{n}'] = {'empty': sum(1 for r in res if r[2]=='EMPTY'),
                        'nonempty': len(ne), 'timeout': len(to),
                        'nonempty_charts': [[str(r[0]), str(r[1])] for r in ne]}
    json.dump(DONE, open('keller_results.json','w'), indent=1)
    print()
