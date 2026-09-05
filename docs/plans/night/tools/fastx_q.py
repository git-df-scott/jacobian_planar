"""Exact rational version of fastx.build (fmpq_mpoly): returns generators over Q; used to certify monomial kills exactly."""
import sys, time
sys.path.insert(0, '/tmp/wt/canon/campaign/audit_tracks')
from trackB1_polygon import hull_rows
import flint
from fractions import Fraction
def build_q(NP, NQ, r, jextra=2):
    RP, RQ = hull_rows(NP), hull_rows(NQ)
    if RP.get(0) == (0, 1) and RQ.get(0) == (0, 0): DV, OV, sign = NP, NQ, 1
    elif RQ.get(0) == (0, 1) and RP.get(0) == (0, 0): DV, OV, sign = NQ, NP, -1
    else: raise ValueError('out of scope')
    DR, OR_ = hull_rows(DV), hull_rows(OV); jmax = max(max(DR), max(OR_)) + jextra
    params = [(j, i) for j in sorted(DR) for i in range(DR[j][0], DR[j][1] + 1)]; n = len(params)
    names = [f'c_{k+1}' for k in range(n)] + ['w', 'u', 'x']
    ctx = flint.fmpq_mpoly_ctx.get(tuple(names), ordering='degrevlex'); gens = ctx.gens(); X = gens[-1]; W = gens[-3]
    pv = {(j, i): gens[k] for k, (j, i) in enumerate(params)}
    zero = ctx.from_dict({})
    Pd = {j: (sum((pv[(j, i)] * X**i for i in range(DR[j][0], DR[j][1] + 1)), zero) if j in DR else zero) for j in range(0, jmax + 2)}
    Rr = {j: zero for j in range(0, jmax + 2)}; Rr[0] = ctx.from_dict({tuple([0]*(n+2) + [r]): sign})
    dx = lambda f: f.derivative('x')
    Q = {0: zero, 1: Rr[0] * W}
    for k in range(1, jmax + 1):
        acc = Rr[k]
        for a in range(0, k + 1):
            b = k - a
            if a + 1 <= jmax + 1 and b <= jmax + 1: acc = acc + (a + 1) * Pd[a + 1] * dx(Q[b])
            if a >= 1 and b + 1 <= jmax + 1: acc = acc - (b + 1) * dx(Pd[a]) * Q[b + 1]
        Q[k + 1] = acc * W * flint.fmpq(1, k + 1)
    conds = []; xi = len(names) - 1
    for j in range(1, jmax + 1):
        lo, hi = OR_.get(j, (None, None)); byx = {}
        for mon, cf in zip(Q[j].monoms(), Q[j].coeffs()):
            e = mon[xi]; m2 = list(mon); m2[xi] = 0; byx.setdefault(e, {})[tuple(m2)] = cf
        for e, d in byx.items():
            if lo is None or e < lo or e > hi: conds.append((j, e, ctx.from_dict(d)))
    nd = [pv[(0, 1)]] + [pv[(j, i)] for (j, i) in params if (i, j) in [tuple(v) for v in DV] and (i, j) != (0, 0) and pv[(j, i)] != pv[(0, 1)]]
    return ctx, names, conds, dict(nparams=n, jmax=jmax, ndegen=[str(f) for f in nd])
if __name__ == '__main__':
    import hashlib, json
    sys.path.insert(0,'/tmp/wt/canon/campaign/audit_tracks'); import trackD_chain_map as T
    sid, J = sys.argv[1], int(sys.argv[2])
    for ch in T.all_chains():
        for c in T.reduced_candidates(ch)[0]:
            tag=f"{ch.name} | a={c['a']} b={c['b']} c'={c['cprime']} r={c['r']} eps={c['epsP']},{c['epsQ']}"
            if 's'+hashlib.sha1(tag.encode()).hexdigest()[:6]==sid:
                t=time.time(); ctx,names,conds,info=build_q(c['NP'],c['NQ'],c['r'],jextra=J)
                nz=set(info['ndegen'])|{'w'}
                for (j,e,g) in conds:
                    if len(g.monoms())==1:
                        vs={names[i] for i,ee in enumerate(g.monoms()[0]) if ee}
                        if vs and vs<=nz: print(f'EXACT-Q KILL {sid} {tag}: row j={j}, x^{e}: {g}  ({round(time.time()-t,1)}s)')
                print('done', sid, 'conds', len(conds), round(time.time()-t,1), 's')
