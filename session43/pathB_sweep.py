#!/usr/bin/env python
"""Path B item B2: mu_n-equivariant plane Keller map sweep.

Cell = (n, b, p, q) with q = (1+b-p) mod n (Keller-compatibility congruence).
F1 = sum a_ij x^i y^j over monomials with i + b*j = p (mod n), 1<=i+j<=D
F2 = sum b_ij x^i y^j over monomials with i + b*j = q (mod n), 1<=i+j<=D
Impose det JF = const: all nonconstant coeffs of det = 0. Solve for coeffs.
Classify each solution branch via Jung-van der Kulk elementary reduction.
"""
import sys, json, random, time
import sympy as sp
from sympy import symbols, Poly, Rational, simplify, expand

x, y = symbols('x y')
random.seed(7)

def monos(n, b, r, D):
    return [(i,j) for d in range(1, D+1) for i in range(d+1) for j in [d-i] if (i + b*j - r) % n == 0]

def build_cell(n, b, p, q, D):
    m1 = monos(n,b,p,D); m2 = monos(n,b,q,D)
    a = {ij: sp.Symbol('a_%d_%d'%ij) for ij in m1}
    bb = {ij: sp.Symbol('b_%d_%d'%ij) for ij in m2}
    F1 = sum(a[ij]*x**ij[0]*y**ij[1] for ij in m1)
    F2 = sum(bb[ij]*x**ij[0]*y**ij[1] for ij in m2)
    det = sp.expand(sp.diff(F1,x)*sp.diff(F2,y) - sp.diff(F1,y)*sp.diff(F2,x))
    pdet = sp.Poly(det, x, y)
    eqs = []
    const = sp.Integer(0)
    for mono, c in zip(pdet.monoms(), pdet.coeffs()):
        if mono == (0,0):
            const = c
        else:
            eqs.append(sp.expand(c))
    return F1, F2, list(a.values())+list(bb.values()), eqs, const

def top_form(f):
    pf = sp.Poly(sp.expand(f), x, y)
    d = max((sum(m) for m in pf.monoms()), default=-1)
    if d <= 0: return d, sp.Integer(0)
    tf = sum(c*x**m[0]*y**m[1] for m,c in zip(pf.monoms(), pf.coeffs()) if sum(m)==d)
    return d, sp.expand(tf)

def try_reduce(F1, F2, maxsteps=30):
    """Jung-van der Kulk elementary reduction on a concrete (numeric-coeff) map.
    Returns 'automorphism' if reduces to invertible linear, else 'CANDIDATE'."""
    G1, G2 = sp.expand(F1), sp.expand(F2)
    for _ in range(maxsteps):
        d1, h1 = top_form(G1); d2, h2 = top_form(G2)
        if d1 <= 1 and d2 <= 1:
            J = sp.Matrix([[sp.diff(G1,x), sp.diff(G1,y)],[sp.diff(G2,x), sp.diff(G2,y)]]).det()
            return 'automorphism' if sp.simplify(J) != 0 else 'degenerate'
        # order so d1 >= d2
        if d1 < d2:
            G1, G2, d1, d2, h1, h2 = G2, G1, d2, d1, h2, h1
        if d2 < 1 or (d2 >= 1 and d1 % d2 == 0):
            if d2 >= 1:
                k = d1 // d2
                # h1 == c*h2^k ?
                q = sp.simplify(sp.cancel(h1 / h2**k))
                if q.free_symbols - {x,y} == q.free_symbols and not q.has(x) and not q.has(y):
                    G1 = sp.expand(G1 - q*G2**k)
                    continue
            return 'CANDIDATE'
        return 'CANDIDATE'
    return 'CANDIDATE'

def classify_branch(F1, F2, sol, allvars):
    s1 = sp.expand(F1.subs(sol)); s2 = sp.expand(F2.subs(sol))
    free = (s1.free_symbols | s2.free_symbols) - {x,y}
    # substitute random values for free params; retry to keep det nonzero
    for trial in range(12):
        vals = {f: sp.Integer(random.randint(1,9)) for f in free}
        t1 = sp.expand(s1.subs(vals)); t2 = sp.expand(s2.subs(vals))
        J = sp.expand(sp.diff(t1,x)*sp.diff(t2,y) - sp.diff(t1,y)*sp.diff(t2,x))
        if J.has(x) or J.has(y) or J == 0:
            continue
        d1,_ = top_form(t1); d2,_ = top_form(t2)
        if d1 <= 1 and d2 <= 1:
            return 'linear/affine', max(d1,d2), (t1,t2)
        res = try_reduce(t1, t2)
        if res == 'automorphism':
            return 'nonlinear-tame-automorphism', max(d1,d2), (t1,t2)
        return 'CANDIDATE', max(d1,d2), (t1,t2)
    return 'no-keller-specialization', 0, (s1,s2)

def run_cell(n, b, p, D, timeout_hint=None):
    q = (1 + b - p) % n
    F1, F2, avars, eqs, const = build_cell(n,b,p%n,q,D)
    if not avars:
        return dict(n=n,b=b,p=p%n,q=q,D=D,status='empty')
    try:
        if eqs:
            g = sp.groebner(eqs, *avars, order='grevlex')
            sols = sp.solve(list(g.exprs), avars, dict=True)
        else:
            sols = [dict()]
    except Exception as e:
        return dict(n=n,b=b,p=p%n,q=q,D=D,status='solve-failed:'+str(e)[:80])
    out = dict(n=n,b=b,p=p%n,q=q,D=D,status='solved', nvars=len(avars), neqs=len(eqs),
               nbranches=len(sols), branches=[])
    for sol in sols:
        cls, deg, (t1,t2) = classify_branch(F1,F2,sol,avars)
        entry = dict(cls=cls, maxdeg=int(deg))
        if cls == 'no-keller-specialization':
            cs = sp.simplify(const.subs(sol))
            if cs == 0 and all(sp.simplify(e.subs(sol))==0 for e in eqs[:3]):
                entry['cls'] = 'degenerate(det=0)'
        if entry['cls'] not in ('linear/affine','degenerate(det=0)'):
            entry['F1'] = str(t1); entry['F2'] = str(t2)
        if entry['cls'] == 'CANDIDATE':
            entry['sol'] = {str(k):str(v) for k,v in sol.items()}
        out['branches'].append(entry)
    return out

if __name__ == '__main__':
    n, b, p, D = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    t0 = time.time()
    r = run_cell(n,b,p,D)
    r['secs'] = round(time.time()-t0,1)
    print(json.dumps(r))
