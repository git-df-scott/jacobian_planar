"""Sound torus-chart reduction of an msolve .ms system over F_p-bar.

1. Weight lattice: integer nullspace of the exponent-difference matrix (every generator quasi-homogeneous).
2. Variables forced nonzero by Rabinowitsch rows (v * stuff - 1) are gauged to 1 when they carry an
   independent torus weight (always possible over the algebraic closure): no chart split needed.
3. Remaining torus directions: pick a variable with nonzero residual weight; split into chart v=0 and chart v=1.
Output: list of chart .ms files whose union of solution sets (over F_p-bar) equals that of the input.
"""
import sys, re, json, itertools
from fractions import Fraction
import sympy as sp

def parse_ms(path):
    lines = open(path).read().split('\n'); names = lines[0].split(','); p = int(lines[1])
    body = '\n'.join(lines[2:]); gens = [g.strip().rstrip(',') for g in re.split(r',\s*\n', body) if g.strip()]
    return names, p, gens

def terms(g, names):
    out = []
    for term in re.findall(r'[+-]?[^+-]+', g.replace(' ', '')):
        cf = 1; mon = [0]*len(names)
        for fac in term.split('*'):
            if re.fullmatch(r'[+-]?\d+', fac): cf = int(fac)
            else:
                m = re.fullmatch(r'([+-]?)([A-Za-z_]\w*)(?:\^(\d+))?', fac)
                if m.group(1) == '-': cf = -cf
                mon[names.index(m.group(2))] += int(m.group(3) or 1)
        out.append((tuple(mon), cf))
    return out

def weight_lattice(names, gens):
    rows = []
    for g in gens:
        T = terms(g, names); m0 = T[0][0]
        for m, _ in T[1:]:
            rows.append([a - b for a, b in zip(m, m0)])
    M = sp.Matrix(rows) if rows else sp.zeros(0, len(names))
    ns = M.nullspace()
    basis = []
    for v in ns:
        den = sp.ilcm(*[sp.fraction(x)[1] for x in v]) if len(v) else 1
        w = [int(x*den) for x in v]
        from math import gcd
        from functools import reduce
        gg = reduce(gcd, [abs(x) for x in w if x] or [1]); basis.append([x//gg for x in w])
    return basis

def forced_nonzero(names, p, gens):
    nz = set()
    for g in gens:
        T = terms(g, names)
        if len(T) == 2:
            (m1, c1), (m2, c2) = T
            const = [m for m, c in T if sum(m) == 0]
            if const:
                other = [m for m in (m1, m2) if sum(m) > 0][0]
                for i, e in enumerate(other):
                    if e > 0: nz.add(names[i])
    return nz

def substitute(gens, names, var, val, p):
    """substitute var := val (0 or 1) into generator strings; return new names, gens (zeros and dups dropped)."""
    i = names.index(var); out = []; seen = set()
    for g in gens:
        T = terms(g, names); acc = {}
        for m, c in T:
            if m[i] > 0 and val == 0: continue
            m2 = list(m); m2[i] = 0; m2 = tuple(m2)
            acc[m2] = (acc.get(m2, 0) + c) % p
        acc = {m: c for m, c in acc.items() if c}
        if not acc: continue
        if all(sum(m) == 0 for m in acc): return names, ['1']  # nonzero constant: chart empty
        s = '+'.join(f"{c}" + ''.join(f"*{names[j]}^{e}" if e > 1 else f"*{names[j]}" for j, e in enumerate(m) if e) for m, c in sorted(acc.items()))
        if s in seen: continue
        seen.add(s); out.append(s)
    new_names = [n for n in names if n != var]
    return new_names, out

def reduce_system(path, outdir, tag):
    names, p, gens = parse_ms(path)
    charts = [(names, gens, [])]
    final = []
    log = []
    while charts:
        names, gens, hist = charts.pop()
        if gens == ['1']: final.append((names, gens, hist + ['EMPTY-by-substitution'])); continue
        W = weight_lattice(names, gens)
        # drop weights supported only on unused variables
        used = set(); [used.update(names[j] for j, e in enumerate(m) if e) for g in gens for m, _ in terms(g, names)]
        names_u = [n for n in names if n in used]
        if names_u != names:
            names, gens = names_u, gens  # strings unaffected
            W = weight_lattice(names, gens)
        if not W: final.append((names, gens, hist)); continue
        nz = forced_nonzero(names, p, gens)
        # pick gauge variable: prefer forced-nonzero with nonzero weight in span
        Wm = sp.Matrix(W)
        cand = None
        for v in names:
            j = names.index(v)
            if v in nz and any(w[j] for w in W): cand = (v, True); break
        if cand is None:
            # variable appearing in most weights, not constant-only
            best = max(names, key=lambda v: sum(1 for w in W if w[names.index(v)]))
            if not any(w[names.index(best)] for w in W): final.append((names, gens, hist)); continue
            cand = (best, False)
        v, free = cand
        n1, g1 = substitute(gens, names, v, 1, p)
        charts.append((n1, g1, hist + [f'{v}=1']))
        if not free:
            n0, g0 = substitute(gens, names, v, 0, p)
            charts.append((n0, g0, hist + [f'{v}=0']))
    import os; os.makedirs(outdir, exist_ok=True)
    idx = []
    for k, (names, gens, hist) in enumerate(final):
        if gens == ['1']: idx.append(dict(chart=k, hist=hist, empty=True)); continue
        used = set(); [used.update(names[j] for j, e in enumerate(m) if e) for g in gens for m, _ in terms(g, names)]
        names = [n for n in names if n in used]
        fn = f'{outdir}/{tag}_chart{k}.ms'
        open(fn, 'w').write(','.join(names) + '\n' + str(p) + '\n' + ',\n'.join(gens) + '\n')
        idx.append(dict(chart=k, hist=hist, file=fn, nvars=len(names), ngens=len(gens), torus_rank=len(weight_lattice(names, gens))))
    json.dump(idx, open(f'{outdir}/{tag}_charts.json', 'w'), indent=1)
    return idx

if __name__ == '__main__':
    path, outdir, tag = sys.argv[1:4]
    for r in reduce_system(path, outdir, tag): print(r)
