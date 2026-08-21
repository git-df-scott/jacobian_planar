#!/usr/bin/env python3
"""FAST exact rank criterion at the quasi-homogeneous point, via mod p.

Soundness of the mod-p shortcut (one direction only, which is the one we
need): if G lies in the column span of J over Q, then reducing that linear
combination mod p puts G in the span mod p (for p not dividing the
denominators).  Contrapositive: **G not in the span mod p  =>  G not in the
span over Q**, i.e. OBSTRUCTED mod p implies OBSTRUCTED over Q.
(The converse is not claimed; a mod-p coincidence would be reported as
INCONCLUSIVE-modp and would need an exact recheck.)

Speed: at the quasi-homogeneous point every unknown is 0 except a_{2d}=r, so
    J[i][j] = sum over monomials of F_i of the form a_{2d}^k * x_j
              of  coeff * r^k
-- a single pass over monomials, no symbolic differentiation, no substitution.
G = dF/dmu0 is the constant vector (-6 in the y^3 row).

Usage: python3 w6_rankcrit_modp.py PRIME D [D ...]
"""
import sys, os, json, time
sys.path.insert(0, '/home/user/jacobian_planar/wave5')
os.chdir('/home/user/jacobian_planar/wave5')
import sympy as sp
from sympy import symbols, expand, Poly, Rational
from w5_b16_abel import build_system, mu0, mu1, mu2, mu3

def rank_modp(rows, ncols, p):
    mat = [r[:] for r in rows]; rank = 0; col = 0; nr = len(mat)
    while rank < nr and col < ncols:
        piv = None
        for i in range(rank, nr):
            if mat[i][col] % p: piv = i; break
        if piv is None: col += 1; continue
        mat[rank], mat[piv] = mat[piv], mat[rank]
        inv = pow(mat[rank][col] % p, p-2, p)
        mat[rank] = [(v*inv) % p for v in mat[rank]]
        for i in range(nr):
            if i != rank and mat[i][col] % p:
                f = mat[i][col] % p
                mat[i] = [(a - f*b) % p for a, b in zip(mat[i], mat[rank])]
        rank += 1; col += 1
    return rank

def analyze(d, p):
    t0 = time.time()
    eqs, unk, A, q1 = build_system(d)
    a = symbols(f'a0:{2*d+1}'); b = symbols(f'b0:{d}')
    pre = {a[0]: -mu3**2/4, a[1]: mu2, b[0]: mu3, b[1]: 0,
           mu1: -mu3*a[2]/3}
    core = [expand(e.subs(pre)) for e in eqs]
    core = [e for e in core if e != 0]
    vars_ = [a[i] for i in range(2, 2*d+1)] + [b[i] for i in range(2, d)] + [mu2, mu3]
    allv = vars_ + [mu0]
    top = a[2*d]; itop = vars_.index(top)
    # rational roots of (8d-6)x^2+3x-3/8 exist iff 12d is a perfect square
    # roots of (8d-6)x^2+3x-3/8 = 0 taken MOD P: they exist in F_p iff 12d is
    # a square mod p (disc = 12d).  This covers every d, not just the resonant
    # d = 3k^2 where the roots happen to be rational over Q.
    disc = (12*d) % p
    roots = []
    if pow(disc, (p-1)//2, p) == 1:
        q_ = p-1; s_ = 0
        while q_ % 2 == 0: q_ //= 2; s_ += 1
        z_ = 2
        while pow(z_, (p-1)//2, p) != p-1: z_ += 1
        M_, c_, t_, R_ = s_, pow(z_, q_, p), pow(disc, q_, p), pow(disc, (q_+1)//2, p)
        while t_ != 1:
            i_, t2_ = 0, t_
            while t2_ != 1: t2_ = t2_*t2_ % p; i_ += 1
            b__ = pow(c_, 1 << (M_-i_-1), p); M_ = i_; c_ = b__*b__ % p
            t_ = t_*c_ % p; R_ = R_*b__ % p
        inv2 = pow(2*(8*d-6) % p, p-2, p)
        roots = [(-3 + R_)*inv2 % p, (-3 - R_)*inv2 % p]
    out = []
    polys = [Poly(e, *allv) for e in core]
    n = len(vars_); m = len(polys)
    if not roots:
        return {'d': d, 'p': p, 'results': [{'skipped': '12d is not a square mod p -- choose another prime'}]}
    for rp in roots:
        rr = f'root mod p = {rp}'
        J = [[0]*n for _ in range(m)]
        G = [0]*m
        Fval = [0]*m
        for i, P in enumerate(polys):
            for mono, cf in zip(P.monoms(), P.coeffs()):
                cfr = sp.Rational(cf)
                c = int(cfr.p) * pow(int(cfr.q), p-2, p) % p
                deg_top = mono[itop]
                rest = [(j, e) for j, e in enumerate(mono) if e and j != itop]
                # value at the point (all vars 0 except a_2d=r, mu0=0)
                if not rest:
                    Fval[i] = (Fval[i] + c*pow(rp, deg_top, p)) % p
                elif len(rest) == 1 and rest[0][1] == 1:
                    j = rest[0][0]
                    contrib = c*pow(rp, deg_top, p) % p
                    if j == len(vars_):          # the mu0 column
                        G[i] = (G[i] + contrib) % p
                    else:
                        J[i][j] = (J[i][j] + contrib) % p
        on_locus = all(v % p == 0 for v in Fval)
        rkJ = rank_modp(J, n, p)
        rkA = rank_modp([row + [g] for row, g in zip(J, G)], n+1, p)
        out.append({'root': str(rr), 'on_locus_modp': on_locus,
                    'rank_J': rkJ, 'rank_aug': rkA,
                    'BIFURCATION_POSSIBLE': bool(rkJ == rkA and on_locus),
                    'verdict': ('BIFURCATION-POINT' if (rkJ == rkA and on_locus)
                                else ('obstructed' if on_locus else 'not-on-locus'))})
    return {'d': d, 'p': p, 'eqs': m, 'vars': n, 'secs': round(time.time()-t0, 1),
            'results': out}

if __name__ == '__main__':
    p = int(sys.argv[1])
    for d in [int(x) for x in sys.argv[2:]]:
        try:
            r = analyze(d, p)
        except Exception as e:
            r = {'d': d, 'ERROR': str(e)[:150]}
        print(json.dumps(r), flush=True)
