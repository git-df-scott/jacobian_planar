#!/usr/bin/env python3
"""Pentagon case (1) of (72,108): solve level by level along L = 2*alpha - beta,
starting from a verified bottom-edge seed.  Pure linear algebra mod p, no
Groebner basis.

Structure (verified in CATCHES.md): every monomial is bilinear (one c, one d)
up to s-powers; max L is 2 on P's support and 3 on Q's.  So the equations at
level Lambda pair L(c) + L(d) = Lambda + 1, and the fresh unknowns at level
Lambda are exactly c at L = Lambda-2 and d at L = Lambda-1, each appearing
LINEARLY multiplied by an already-determined top-level coefficient.  The
s-variables appear to powers and are handled by treating any monomial that is
not linear in the fresh unknowns as a nonlinear carry.

Method: process levels in decreasing Lambda.  At each level, substitute
everything already known, then split the equations into
   * those affine-linear in the remaining fresh unknowns -> solve by Gaussian
     elimination mod p, recording rank, free parameters and INCONSISTENCY;
   * the rest -> carry forward as residual constraints.
An inconsistent level kills the seed.  Free parameters are carried symbolically
only if few; otherwise they are reported and the level is where the work stops.

This is memory-light by construction: coefficients are ints mod p, polynomials
are dicts from sorted monomial tuples to ints.
"""
import json, sys, collections

P = 1000003

def load(path='campaign/audit_tracks/trackB1_param_system.json'):
    d = json.load(open(path))
    eqs = []
    for e in d['equations']:
        terms = {}
        for mon, co in e['terms']:
            key = tuple(sorted((nm, ex) for nm, ex in mon))
            num, den = co
            c = (num * pow(den, P-2, P)) % P
            terms[key] = (terms.get(key, 0) + c) % P
        terms = {k: v for k, v in terms.items() if v}
        eqs.append({'bp': tuple(e['bracket_point']), 'terms': terms})
    return d, eqs

def L(name):
    p = name.split('_'); return 2*int(p[1]) - int(p[2])

def subst(terms, known):
    """Substitute known values; return a new term dict."""
    out = {}
    for mon, c in terms.items():
        rest = []
        for nm, ex in mon:
            if nm in known:
                c = (c * pow(known[nm], ex, P)) % P
            else:
                rest.append((nm, ex))
        if c == 0: continue
        k = tuple(sorted(rest))
        out[k] = (out.get(k, 0) + c) % P
    return {k: v for k, v in out.items() if v}

def solve_level(eqs_at_level, known, fresh):
    """Gaussian elimination mod P on the equations that are affine-linear in `fresh`."""
    lin, nonlin = [], []
    for t in eqs_at_level:
        t = subst(t, known)
        if not t: continue
        ok = True
        for mon in t:
            deg = sum(ex for nm, ex in mon if nm in fresh)
            other = [nm for nm, ex in mon if nm not in fresh]
            if deg > 1 or (deg == 1 and other):
                # linear in a fresh var but multiplied by an unknown non-fresh var
                if deg == 1 and other: ok = False; break
                if deg > 1: ok = False; break
        (lin if ok else nonlin).append(t)
    cols = sorted({nm for t in lin for mon in t for nm, ex in mon if nm in fresh})
    idx = {c: i for i, c in enumerate(cols)}
    rows = []
    for t in lin:
        r = [0]*(len(cols)+1)
        for mon, c in t.items():
            f = [nm for nm, ex in mon if nm in fresh]
            if not mon: r[-1] = (r[-1] + c) % P
            elif len(f) == 1 and len(mon) == 1: r[idx[f[0]]] = (r[idx[f[0]]] + c) % P
            else: r[-1] = (r[-1] + c) % P   # constant after substitution
        rows.append(r)
    # elimination
    piv = {}; rank = 0; inconsistent = 0
    for j in range(len(cols)):
        pr = None
        for i in range(rank, len(rows)):
            if rows[i][j]: pr = i; break
        if pr is None: continue
        rows[rank], rows[pr] = rows[pr], rows[rank]
        inv = pow(rows[rank][j], P-2, P)
        rows[rank] = [(v*inv) % P for v in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][j]:
                f = rows[i][j]
                rows[i] = [(a - f*b) % P for a, b in zip(rows[i], rows[rank])]
        piv[j] = rank; rank += 1
    for i in range(rank, len(rows)):
        if all(v == 0 for v in rows[i][:-1]) and rows[i][-1] % P != 0:
            inconsistent += 1
    return cols, rows, piv, rank, inconsistent, len(lin), nonlin

if __name__ == '__main__':
    d, eqs = load()
    seed = json.load(open('wave6/bottomedge/seeds_admissible.json'))[0]
    known = {}
    for i in range(1, 9): known[f'c_{i}_{2*i-2}'] = seed[f'c{i}'] % P
    for j in range(3, 13): known[f'd_{j}_{2*j-3}'] = seed[f'd{j}'] % P
    allvars = set(d['variables'])
    bylvl = collections.defaultdict(list)
    for e in eqs: bylvl[2*e['bp'][0]-e['bp'][1]].append(e['terms'])
    print(f"seed pins {len(known)} variables; {len(allvars)-len(known)} unknown")
    print(f"{'Lam':>4} {'eqs':>4} {'lin':>4} {'fresh':>5} {'rank':>4} {'free':>4} {'INCONSIST':>9} {'carry':>5}")
    carry = []
    for lam in sorted(bylvl, reverse=True):
        fresh = {v for v in allvars if v not in known and
                 (L(v) == lam-2 and v.startswith('c') or L(v) == lam-1 and v.startswith('d')
                  or v.startswith('s') and L(v) == lam-1)}
        cols, rows, piv, rank, inc, nlin, nonlin = solve_level(bylvl[lam], known, fresh)
        free = len(cols) - rank
        print(f"{lam:>4} {len(bylvl[lam]):>4} {nlin:>4} {len(fresh):>5} {rank:>4} {free:>4} {inc:>9} {len(nonlin):>5}")
        if inc:
            print(f"\n*** LEVEL {lam} IS INCONSISTENT ({inc} contradictory rows) -> THIS SEED DIES ***")
            break
        if free == 0 and rank == len(cols) and cols:
            for c, j in [(c, i) for i, c in enumerate(cols)]:
                if j in piv: known[c] = rows[piv[j]][-1] % P
        carry += nonlin
    print(f"\ncarried nonlinear constraints: {len(carry)}; variables still unknown: "
          f"{len(allvars)-len(known)}")
