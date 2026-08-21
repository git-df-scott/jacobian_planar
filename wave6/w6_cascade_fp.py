#!/usr/bin/env python3
"""EXACT TRIANGULAR DESCENT over F_p -- decides GGV cells with no Groebner
basis and no memory wall.

Why F_p: over Q the same descent (w5_b16_cascade) dies at d>=4 in nested
radicals -- each quadratic step introduces sqrt's that compound.  Over F_p a
univariate step either has roots in F_p or none, so the recursion is finite,
branch-bounded, and every coefficient stays a machine int.

Structure exploited: after GGV's linear eliminations the rows are mostly
LINEAR in the next unknown (the descent coefficient L_k), so branching is
mild -- essentially the two roots of the row-0 quadratic.

Semantics (stated exactly):
 * a branch that consumes every unknown and leaves all remaining equations
   identically zero is a SOLUTION mod p; if its mu0 != 0 it is a
   COUNTEREXAMPLE CANDIDATE mod p -> verify by exact substitution, repeat at
   more primes, then lift.
 * no surviving branch at a given p = that cell has no mu0 != 0 point over
   F_p.  A rational solution reduces mod almost every p, so agreement across
   several primes is strong evidence of emptiness (never a proof).
 * BRANCH-CAP or step blowup is reported as INCOMPLETE, never as emptiness.

Control: d=3 must report zero survivors at every prime (GGV proved it empty).

Usage: python3 w6_cascade_fp.py DMIN DMAX PRIME [branch_cap]
"""
import sys, os, json, time
sys.path.insert(0, '/home/user/jacobian_planar/wave5')
os.chdir('/home/user/jacobian_planar/wave5')
import sympy as sp
from sympy import symbols, expand, Poly, Rational
from w5_b16_abel import build_system, mu0, mu1, mu2, mu3

def build_modp(d, p):
    eqs, unk, A, q1 = build_system(d)
    a = symbols(f'a0:{2*d+1}'); b = symbols(f'b0:{d}')
    pre = {a[0]: -mu3**2/4, a[1]: mu2, b[0]: mu3, b[1]: 0,
           mu1: -mu3*a[2]/3}
    core = [expand(e.subs(pre)) for e in eqs]
    core = [e for e in core if e != 0]
    unknowns = [a[i] for i in range(2, 2*d+1)] + [b[i] for i in range(2, d)] + [mu2, mu3, mu0]
    out = []
    for e in core:
        P = Poly(e, *unknowns)
        L = 1
        for c in P.coeffs():
            L = sp.lcm(L, sp.denom(c))
        e2 = expand(e * L)
        out.append(Poly(e2, *unknowns, modulus=p))
    return out, unknowns

def roots_modp(P, u, p):
    """All roots in F_p of univariate-in-u polynomial P (Poly over modulus p)."""
    ex = P.as_expr()
    extra = (ex.free_symbols - {u})
    if extra:
        raise RuntimeError('roots_modp called on multivariate: %s' % sorted(map(str, extra))[:3])
    q = Poly(ex, u, modulus=p)
    if q.is_zero:
        return 'ALL'
    if q.degree() == 0:
        return []
    return sorted({int(r) % p for r in q.ground_roots().keys()
                   if r.is_Integer or r.is_Rational})

def descend(d, p, cap=20000):
    polys, unknowns = build_modp(d, p)
    start = [(dict(), [P for P in polys])]
    survivors, dead, incomplete = [], 0, False
    steps = 0
    while start:
        steps += 1
        if steps > cap:
            incomplete = True
            break
        sub, eqs = start.pop()
        eqs = [e for e in eqs if not e.is_zero]
        # inconsistent constant?
        bad = False
        for e in eqs:
            if e.is_ground and not e.is_zero:
                bad = True; break
        if bad:
            dead += 1
            continue
        rem = [u for u in unknowns if u not in sub]
        live = [e for e in eqs if any(u in e.free_symbols for u in rem)]
        if not live:
            survivors.append(dict(sub))     # all remaining eqs vanished
            continue
        if not rem:
            dead += 1
            continue
        # choose equation with fewest remaining unknowns, then lowest degree var
        def nv(e): return sum(1 for u in rem if u in e.free_symbols)
        live.sort(key=nv)
        e0 = live[0]
        vs = [u for u in rem if u in e0.free_symbols]
        u = min(vs, key=lambda v: e0.degree(v))
        # isolate u: treat other unknowns as parameters -> only valid if e0 is
        # univariate in u after substitution; otherwise pick a different eq
        others = [v for v in vs if v != u]
        if others:
            # not univariate: fall back to branching over all F_p values of u
            # only when p is small; otherwise report incomplete for this branch
            if p <= 257:
                for val in range(p):
                    ns = dict(sub); ns[u] = val
                    start.append((ns, [Poly(e.as_expr().subs(u, val), *[w for w in unknowns], modulus=p)
                                       for e in eqs]))
                continue
            incomplete = True
            continue
        rs = roots_modp(e0, u, p)
        if rs == 'ALL':
            rs = list(range(p)) if p <= 257 else None
            if rs is None:
                incomplete = True
                continue
        if not rs:
            dead += 1
            continue
        for val in rs:
            ns = dict(sub); ns[u] = int(val)
            neqs = [Poly(e.as_expr().subs(u, int(val)), *unknowns, modulus=p) for e in eqs]
            start.append((ns, neqs))
    surv_mu0 = [s for s in survivors if int(s.get(mu0, 0)) % p != 0]
    return {'d': d, 'p': p, 'survivors_total': len(survivors),
            'survivors_mu0_nonzero': len(surv_mu0), 'dead_branches': dead,
            'steps': steps, 'INCOMPLETE': incomplete,
            'samples': [{str(k): int(v) for k, v in s.items()} for s in surv_mu0[:2]]}

if __name__ == '__main__':
    dmin, dmax = int(sys.argv[1]), int(sys.argv[2])
    p = int(sys.argv[3]) if len(sys.argv) > 3 else 1000003
    cap = int(sys.argv[4]) if len(sys.argv) > 4 else 20000
    allout = []
    for d in range(dmin, dmax + 1):
        t0 = time.time()
        try:
            r = descend(d, p, cap)
        except Exception as e:
            r = {'d': d, 'p': p, 'ERROR': str(e)[:200]}
        r['secs'] = round(time.time() - t0, 1)
        if r.get('survivors_mu0_nonzero'):
            r['ALERT'] = 'CANDIDATE-MODP'
        print(json.dumps(r), flush=True)
        allout.append(r)
        json.dump(allout, open('/home/user/jacobian_planar/wave6/cascade_fp.json', 'w'), indent=1)
