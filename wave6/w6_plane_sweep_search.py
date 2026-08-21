#!/usr/bin/env python3
"""SEARCH THE PLANE SIDE CONDITION (see w6_plane_sweep.py for the derivation).

For F = (P/C^i, Q/C^j) built from the tangent sweep, F is Keller iff

    C*2*gamma*detJphi - j*Q*{P,C} + i*P*{Q,C}  =  kappa*C^(i+j+1)      (SC)

identically, plus C^i | P, C^j | Q.  Here we take the plane analogue of Gao's
dimension-3 twist, with one variable fewer:

    phi : (x,y) -> (gamma, w),   gamma = c0 + a*x^al*y^be,   w = gamma*u,
                                 u = 1 + b*x^mu*y^nu,        C = gamma*x^s

and p of degree d with unknown coefficients (q is then forced by q'=(w/2)p').
(SC) becomes a polynomial identity in x,y; its coefficients are the SIDE
CONDITIONS, a polynomial system in (c0, a, b, k1..kd, kappa).  We solve each
with a Groebner basis over Q, saturated by kappa != 0 and a != 0 (a = 0 makes
gamma constant, which the structural fact in w6_plane_sweep.py already excludes).

VERDICT SEMANTICS.  A solution with kappa != 0 and the divisibilities holding is
a PLANE KELLER MAP OF TANGENT-SWEEP TYPE -- to be checked for non-injectivity
before any claim is made.  No solution over the searched shapes is NOT a proof
that none exists; it bounds the shape family only, and the bound is reported.
"""
import sys, json, itertools, time
import sympy as sp

x, y, w = sp.symbols('x y w')

def sweep_q(p_poly):
    return sp.expand(sp.integrate(sp.Rational(1, 2)*w*sp.diff(p_poly, w), (w, 0, w)))

def br(A, B):
    return sp.expand(sp.diff(A, x)*sp.diff(B, y) - sp.diff(A, y)*sp.diff(B, x))

def run_shape(al, be, mu, nu, s, i, j, d, timeout_s=90):
    c0, a, b, kap = sp.symbols('c0 a b kappa')
    ks = sp.symbols(f'k1:{d+1}')
    unk = [c0, a, b, kap] + list(ks)
    gam = c0 + a*x**al*y**be
    u   = 1 + b*x**mu*y**nu
    wx  = sp.expand(gam*u)
    p_poly = sum(ks[t-1]*w**t for t in range(1, d+1))
    q_poly = sweep_q(p_poly)
    P = sp.expand(p_poly.subs(w, wx) + 2*gam)
    Q = sp.expand(q_poly.subs(w, wx) + gam*wx)
    C = sp.expand(gam*x**s)
    detJphi = br(gam, wx)
    lhs = sp.expand(C*2*gam*detJphi - j*Q*br(P, C) + i*P*br(Q, C) - kap*C**(i+j+1))
    if lhs == 0:
        return {'shape': (al, be, mu, nu, s, i, j, d), 'status': 'IDENTICALLY-ZERO'}
    eqs = [sp.expand(c) for c in sp.Poly(lhs, x, y).coeffs()]
    t = sp.Symbol('t_sat')
    eqs = eqs + [sp.expand(t*kap*a - 1)]          # kappa != 0 and a != 0
    try:
        G = sp.groebner(eqs, *(unk + [t]), order='grevlex')
    except Exception as e:
        return {'shape': (al, be, mu, nu, s, i, j, d), 'status': f'ERR {str(e)[:60]}'}
    empty = list(G.exprs) == [sp.Integer(1)]
    return {'shape': (al, be, mu, nu, s, i, j, d), 'neqs': len(eqs),
            'status': 'EMPTY' if empty else 'LIVE',
            'gb_head': [str(e)[:90] for e in list(G.exprs)[:4]]}

if __name__ == '__main__':
    dmax = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    t0 = time.time(); out = []
    shapes = []
    for al, be in itertools.product(range(0, 3), repeat=2):
        if (al, be) == (0, 0): continue
        for mu, nu in itertools.product(range(0, 3), repeat=2):
            for s in range(0, 3):
                for (i, j) in ((1, 2), (1, 1), (0, 1), (2, 3)):
                    for d in range(2, dmax+1):
                        shapes.append((al, be, mu, nu, s, i, j, d))
    print(f"shapes to test: {len(shapes)}", flush=True)
    live = 0
    for k, sh in enumerate(shapes):
        r = run_shape(*sh)
        out.append(r)
        if r['status'] not in ('EMPTY',):
            live += 1
            print(json.dumps(r), flush=True)
        if k % 50 == 0:
            print(f"# {k}/{len(shapes)} live={live} {round(time.time()-t0,1)}s", flush=True)
            json.dump(out, open('/home/user/jacobian_planar/wave6/plane_sweep_search.json', 'w'), indent=1)
    json.dump(out, open('/home/user/jacobian_planar/wave6/plane_sweep_search.json', 'w'), indent=1)
    print(f"\ndone: {len(out)} shapes, {live} not-EMPTY, {round(time.time()-t0,1)}s")
