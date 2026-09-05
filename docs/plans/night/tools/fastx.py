"""Independent re-implementation of trackD_extract.build_singular's ideal, in python-flint nmod_mpoly.
Same recursion, same variable order (c(1..n), w, u, x), same support conditions and saturations."""
import sys, re, time
sys.path.insert(0, '/tmp/wt/canon/campaign/audit_tracks')
from trackB1_polygon import hull_rows
import flint

def build(NP, NQ, r, p, jextra=2):
    RP, RQ = hull_rows(NP), hull_rows(NQ)
    if RP.get(0) == (0, 1) and RQ.get(0) == (0, 0): DV, OV, sign = NP, NQ, 1
    elif RQ.get(0) == (0, 1) and RP.get(0) == (0, 0): DV, OV, sign = NQ, NP, -1
    else: raise ValueError('out of scope')
    DR, OR_ = hull_rows(DV), hull_rows(OV)
    jmax = max(max(DR), max(OR_)) + jextra
    params = [(j, i) for j in sorted(DR) for i in range(DR[j][0], DR[j][1] + 1)]
    n = len(params)
    names = [f'c_{k+1}' for k in range(n)] + ['w', 'u', 'x']
    ctx = flint.nmod_mpoly_ctx.get(tuple(names), ordering='degrevlex', modulus=p)
    gens = ctx.gens(); X = gens[-1]; W = gens[-3]; U = gens[-2]
    pv = {(j, i): gens[k] for k, (j, i) in enumerate(params)}
    Pd = {}
    for j in range(0, jmax + 2):
        if j in DR:
            Pd[j] = sum((pv[(j, i)] * X**i for i in range(DR[j][0], DR[j][1] + 1)), ctx.from_dict({}))
        else:
            Pd[j] = ctx.from_dict({})
    zero = ctx.from_dict({})
    Rr = {j: zero for j in range(0, jmax + 2)}
    Rr[0] = ctx.from_dict({tuple([0]*(n+2) + [r]): (1 if sign == 1 else p - 1)})
    dx = lambda f: f.derivative('x')
    Q = {0: zero, 1: Rr[0] * W}
    for k in range(1, jmax + 1):
        acc = Rr[k]
        for a in range(0, k + 1):
            b = k - a
            if a + 1 <= jmax + 1 and b <= jmax + 1:
                acc = acc + (a + 1) * Pd[a + 1] * dx(Q[b])
            if a >= 1 and b + 1 <= jmax + 1:
                acc = acc - (b + 1) * dx(Pd[a]) * Q[b + 1]
        Q[k + 1] = acc * W * pow(k + 1, p - 2, p)
    conds = []
    xi = len(names) - 1
    for j in range(1, jmax + 1):
        lo, hi = OR_.get(j, (None, None))
        # coefficients of x^e
        byx = {}
        for mon, cf in zip(Q[j].monoms(), Q[j].coeffs()):
            e = mon[xi]
            m2 = list(mon); m2[xi] = 0
            byx.setdefault(e, {})[tuple(m2)] = int(cf)
        for e, d in byx.items():
            if lo is None or e < lo or e > hi:
                conds.append(ctx.from_dict(d))
    p10 = pv[(0, 1)]
    nd = [p10]
    for (j, i) in params:
        if (i, j) in [tuple(v) for v in DV] and (i, j) != (0, 0) and pv[(j, i)] not in nd:
            nd.append(pv[(j, i)])
    prod = ctx.from_dict({tuple([0]*len(names)): 1})
    for f in nd: prod = prod * f
    conds.append(W * p10 - 1); conds.append(U * prod - 1)
    # simplify: drop zeros and duplicates (Singular simplify(I,2) drops zeros only; msolve export dedups?)
    out = []; seen = set()
    for f in conds:
        if f == zero: continue
        s = str(f)
        if s in seen: continue
        seen.add(s); out.append(f)
    return ctx, names, out, dict(nparams=n, jmax=jmax, driver_is_P=(sign == 1), ndegen=[str(f) for f in nd])

def write_ms(path, names, gens, p, drop_unused=True):
    strs = [str(g) for g in gens]
    used = set(re.findall(r'[A-Za-z_]\w*', ' '.join(strs)))
    keep = [v for v in names if (v in used or not drop_unused)]
    with open(path, 'w') as f:
        f.write(','.join(keep) + '\n' + str(p) + '\n' + ',\n'.join(strs) + '\n')
    return keep

if __name__ == '__main__':
    NP = [(0, 0), (1, 0), (8, 14), (8, 16)]; NQ = [(0, 0), (2, 1), (12, 21), (12, 24)]
    t = time.time(); ctx, names, gens, info = build(NP, NQ, 2, 65521)
    print('built', len(gens), 'gens in', round(time.time() - t, 1), 's', info)
    # compare with committed p108_525122.ms
    lines = open('/tmp/wt/p11/wave6/ms/p108_525122.ms').read().split('\n')
    cvars = lines[0].split(','); assert int(lines[1]) == 65521
    body = '\n'.join(lines[2:]); cg = [g.strip().rstrip(',') for g in re.split(r',\s*\n', body) if g.strip()]
    assert cvars == names, (cvars, names)
    def parse(s):
        f = ctx.from_dict({})
        for term in re.findall(r'[+-]?[^+-]+', s.replace(' ', '')):
            cf = 1; mon = [0]*len(names)
            for fac in term.split('*'):
                if re.fullmatch(r'[+-]?\d+', fac): cf = int(fac)
                elif fac == '-' : cf = -1
                else:
                    m = re.fullmatch(r'([+-]?)([A-Za-z_]\w*)(?:\^(\d+))?', fac)
                    if m.group(1) == '-': cf = -cf
                    mon[names.index(m.group(2))] += int(m.group(3) or 1)
            f += ctx.from_dict({tuple(mon): cf % 65521})
        return f
    committed = set(str(parse(g)) for g in cg)
    mine = set(str(g) for g in gens)
    print('committed', len(committed), 'mine', len(mine), 'equal sets:', committed == mine,
          'only committed', len(committed - mine), 'only mine', len(mine - committed))
    if committed != mine:
        for g in list(committed - mine)[:2]: print(' C:', g[:150])
        for g in list(mine - committed)[:2]: print(' M:', g[:150])
