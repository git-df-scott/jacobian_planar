#!/usr/bin/env python3
"""Pentagon case (1) of (72,108): CORRECT level cascade along L = 2*alpha-beta.

Supersedes w6_pent_levelcascade.py, which had a fatal bug: when a level left
FREE PARAMETERS, the undetermined higher-level variables were dumped into the
constant column (i.e. silently set to 1), manufacturing a spurious
inconsistency.  Free parameters must be carried SYMBOLICALLY; a level that
looks inconsistent then yields a POLYNOMIAL CONDITION on the parameters, which
is a constraint to be solved, not a death certificate.

Implementation: polynomials in the free parameters over F_p as dicts
{exponent tuple: coefficient}.  Elimination is FRACTION-FREE (rows are scaled by
pivots, never divided), so everything stays polynomial and exact.

Per level the report gives: #equations, how many were genuinely affine-linear in
the fresh unknowns, the rank, the number of new free parameters introduced, and
-- crucially -- the polynomial CONDITIONS on the parameters produced by rows that
reduce to 0 = (nonzero polynomial).  Those conditions are the real content.
"""
import json, sys, collections
P = 1000003

# ---- polynomials in the parameters over F_p -------------------------------
def pzero(): return {}
def pconst(c, n):
    c %= P
    return {(0,)*n: c} if c else {}
def padd(a, b):
    o = dict(a)
    for k, v in b.items():
        w = (o.get(k, 0) + v) % P
        if w: o[k] = w
        elif k in o: del o[k]
    return o
def pscal(a, c):
    c %= P
    if c == 0: return {}
    return {k: (v*c) % P for k, v in a.items()}
def pmul(a, b):
    o = {}
    for k1, v1 in a.items():
        for k2, v2 in b.items():
            k = tuple(x+y for x, y in zip(k1, k2))
            w = (o.get(k, 0) + v1*v2) % P
            if w: o[k] = w
            elif k in o: del o[k]
    return o
def pdeg(a): return max((sum(k) for k in a), default=-1)

def load():
    d = json.load(open('campaign/audit_tracks/trackB1_param_system.json'))
    eqs = []
    for e in d['equations']:
        t = {}
        for mon, co in e['terms']:
            key = tuple(sorted((nm, ex) for nm, ex in mon))
            c = (co[0]*pow(co[1], P-2, P)) % P
            t[key] = (t.get(key, 0) + c) % P
        eqs.append({'bp': tuple(e['bracket_point']), 'terms': {k: v for k, v in t.items() if v}})
    return d, eqs

def L(name):
    p = name.split('_'); return 2*int(p[1]) - int(p[2])

if __name__ == '__main__':
    d, eqs = load()
    seed = json.load(open('wave6/bottomedge/seeds_admissible.json'))[0]
    NPAR = 24                              # room for free parameters
    known = {}
    for i in range(1, 9): known[f'c_{i}_{2*i-2}'] = pconst(seed[f'c{i}'], NPAR)
    for j in range(3, 13): known[f'd_{j}_{2*j-3}'] = pconst(seed[f'd{j}'], NPAR)
    allvars = set(d['variables'])
    bylvl = collections.defaultdict(list)
    for e in eqs: bylvl[2*e['bp'][0]-e['bp'][1]].append(e['terms'])
    npar = 0
    conditions = []
    print(f"seed pins {len(known)} variables, {len(allvars)-len(known)} unknown\n")
    print(f"{'Lam':>4} {'eqs':>4} {'lin':>4} {'nonlin':>6} {'fresh':>5} {'rank':>4} {'newpar':>6} {'CONDS':>5} {'maxdeg':>6}")
    for lam in sorted(bylvl, reverse=True):
        fresh = sorted(v for v in allvars if v not in known and
                       ((v.startswith('c') and L(v) == lam-2) or
                        (v.startswith('d') and L(v) == lam-1) or
                        (v.startswith('s') and L(v) == lam-1)))
        lin, nonlin = [], []
        for terms in bylvl[lam]:
            row = {}; ok = True
            for mon, c in terms.items():
                coef = pconst(c, NPAR); fv = None; bad = False
                for nm, ex in mon:
                    if nm in known:
                        for _ in range(ex): coef = pmul(coef, known[nm])
                    elif nm in fresh and ex == 1 and fv is None:
                        fv = nm
                    else:
                        bad = True; break
                if bad: ok = False; break
                row[fv] = padd(row.get(fv, {}), coef)
            (lin if ok else nonlin).append(row if ok else terms)
        cols = sorted({k for r in lin for k in r if k is not None})
        M = [[r.get(c, {}) for c in cols] + [r.get(None, {})] for r in lin]
        rank = 0; newconds = 0; maxdeg = 0
        for j in range(len(cols)):
            pr = next((i for i in range(rank, len(M)) if M[i][j]), None)
            if pr is None: continue
            M[rank], M[pr] = M[pr], M[rank]
            piv = M[rank][j]
            for i in range(len(M)):
                if i != rank and M[i][j]:
                    f = M[i][j]
                    M[i] = [padd(pmul(piv, a), pscal(pmul(f, b), P-1)) for a, b in zip(M[i], M[rank])]
                    maxdeg = max(maxdeg, max((pdeg(x) for x in M[i]), default=0))
            rank += 1
        for i in range(rank, len(M)):
            if all(not x for x in M[i][:-1]) and M[i][-1]:
                conditions.append(M[i][-1]); newconds += 1
        newpar = len(cols) - rank
        npar += newpar
        print(f"{lam:>4} {len(bylvl[lam]):>4} {len(lin):>4} {len(nonlin):>6} {len(fresh):>5} "
              f"{rank:>4} {newpar:>6} {newconds:>5} {maxdeg:>6}")
        if lam <= -2 and npar == 0: break
    print(f"\ntotal free parameters introduced: {npar}")
    print(f"total polynomial CONDITIONS on the parameters: {len(conditions)}")
    print(f"  of which nonzero CONSTANTS (unconditional contradictions): "
          f"{sum(1 for c in conditions if pdeg(c)==0)}")
