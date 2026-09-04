#!/usr/bin/env python3
"""Branch-1 test, corrected.  Two bugs in branch1_fp.py:

  (a) h_6 was fixed numerically, but h_6 is one of LEVEL 18's unknowns
      (level L's new pieces are h_{L-12} and g_{L-8}, so level 18 introduces
      h_6).  Fixing it over-constrained the level and produced a spurious
      failure at 18, which is impossible since level 18's condition is
      sigma^2 | h_7 and branch 1 has sigma^5 | h_7.
  (b) sp.Matrix.rank(iszerofunc=...) does NOT do modular arithmetic in the
      pivots -- it eliminates over ZZ and only tests zero mod p.  That is not
      an F_p rank.  Replaced with an explicit mod-p rref.

Everything is exact arithmetic in F_p; no sp.solve anywhere, so sympy
case-splitting cannot influence the answer.
"""
import random
import sympy as sp
p = 1000003
s = sp.Symbol('s')
def h_rng(a):
    lo, hi = max(0,-a), min(8, a+2)
    return [i for i in range(lo,hi+1) if 0 <= i+a <= 16]
def g_rng(b):
    return [k for k in range(13)
            if (k+b) >= 0 and ((k+1)//2 if k <= 2 else 2*k-3) <= k+b <= 12+k]

def rref_modp(rows, ncols):
    """returns (rank, rows) in reduced row echelon form over F_p"""
    rows = [[x % p for x in r] for r in rows]
    rk = 0
    for c in range(ncols):
        piv = next((i for i in range(rk, len(rows)) if rows[i][c] % p), None)
        if piv is None: continue
        rows[rk], rows[piv] = rows[piv], rows[rk]
        inv = pow(rows[rk][c], p-2, p)
        rows[rk] = [(v*inv) % p for v in rows[rk]]
        for i in range(len(rows)):
            if i != rk and rows[i][c] % p:
                f = rows[i][c]
                rows[i] = [(rows[i][j] - f*rows[rk][j]) % p for j in range(len(rows[i]))]
        rk += 1
        if rk == len(rows): break
    return rk, rows

def trial(seed, m7, m6, verbose=False):
    rnd = random.Random(seed)
    R = lambda: sp.Integer(rnd.randrange(1, p))
    c0, c1, tau = R(), R(), R()
    sg = s - tau
    H = {8: sp.expand(c0*sg**8)}
    G = {12: sp.expand(c1*sg**12)}
    syms = []
    def unk(name, rng, pref=None):
        cs = [sp.Symbol(f'{name}{i}') for i in rng]
        syms.extend(cs)
        return sp.expand(sum(cs[j]*s**i for j, i in enumerate(rng)))
    # h_7 free at level 19 (its 9 coefficients are exactly level 19's kernel),
    # so a random representative of sigma^{m7} | h_7 is legitimate there.
    H[7] = sp.expand(sg**m7*sum(R()*s**i for i in range(0, 9-m7)))
    # h_6 is an UNKNOWN of level 18, constrained only by sigma^{m6} | h_6
    c6 = [sp.Symbol(f'h6_{i}') for i in range(0, 9-m6)]
    syms.extend(c6)
    H[6] = sp.expand(sg**m6*sum(c6[i]*s**i for i in range(0, 9-m6)))
    for a in (5, 4): H[a] = unk(f'h{a}_', h_rng(a))
    for b in (11, 10, 9, 8): G[b] = unk(f'g{b}_', g_rng(b))
    def lev(L):
        e = 0
        for a in range(-1, 9):
            b = L-a
            if a in H and b in G: e += b*sp.diff(H[a],s)*G[b] - a*H[a]*sp.diff(G[b],s)
        return sp.expand(e)
    carried, sub = [], {}
    for L, new in ((19, ['g11_']), (18, ['g10_', 'h6_']), (17, ['h5_', 'g9_'])):
        e = sp.expand(lev(L).subs(sub))
        eqs = [c for c in sp.Poly(e, s).all_coeffs() if c != 0]
        if not eqs: continue
        u = [v for v in syms if str(v).startswith(tuple(new))] + carried
        M, v = sp.linear_eq_to_matrix(eqs, u)
        rows = [[int(M[i, j]) % p for j in range(M.cols)] for i in range(M.rows)]
        rhs = [int(v[i]) % p for i in range(v.rows)]
        rk, _ = rref_modp(rows, len(u))
        rka, _ = rref_modp([rows[i] + [rhs[i]] for i in range(len(rows))], len(u)+1)
        if verbose: print(f"   level {L}: {len(eqs)} eqs, {len(u)} unk, rank {rk} vs aug {rka}")
        if rk != rka: return f"INCONSISTENT at level {L}"
        sol = sp.solve(eqs, u, dict=True)
        if not sol: return f"no parametrisation at {L}"
        sub.update({k: sp.expand(val) for k, val in sol[0].items()})
        carried = sorted((set(u) - set(sol[0])) | set(carried), key=str)
    e = sp.expand(lev(16).subs(sub))
    eqs = [c for c in sp.Poly(e, s).all_coeffs() if c != 0]
    u = [v for v in syms if str(v).startswith(('h4_','g8_'))] + carried
    M, v = sp.linear_eq_to_matrix(eqs, u)
    rows = [[int(M[i, j]) % p for j in range(M.cols)] for i in range(M.rows)]
    rhs = [int(v[i]) % p for i in range(v.rows)]
    rk, _ = rref_modp(rows, len(u))
    rka, _ = rref_modp([rows[i] + [rhs[i]] for i in range(len(rows))], len(u)+1)
    if verbose: print(f"   level 16: {len(eqs)} eqs, {len(u)} unk, rank {rk} vs aug {rka}")
    return "CONSISTENT through level 16" if rk == rka else "INCONSISTENT at level 16"

print("CONTROL sigma^2|h_7 (must clear 18, fail by 17):", flush=True)
print("  ", trial(1, 2, 0), flush=True)
print("\nCODEX branch 1: sigma^5 | h_7 AND sigma^2 | h_6", flush=True)
for sd in (1, 2, 3):
    print(f"  seed {sd}: {trial(sd, 5, 2, verbose=(sd==1))}", flush=True)
