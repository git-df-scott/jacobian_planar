#!/usr/bin/env python3
"""Joint level solving: the cascade levels are COUPLED, so they must be solved
together, not one at a time with earlier free directions frozen.

Freezing them is exactly the mistake that produced the retracted spiral.  Level
m's condition depends on P_{10-m} (its newest variable) AND on the free
directions left over from levels < m.  So at each level we solve for BOTH.

Structure found (all measured, trackB1_offbyone_check / trackB1_level4):

  level 3   S | P_7                                     (condition on P_7)
  level 4   (X + (2/3)beta)^2 = 0 in R = F_p[z]/(S),  X = P_6 mod S,
            and -(2/3)beta == M^2/(4a) mod S EXACTLY -- i.e. level 4 says
            "P is a perfect square to order 6", relaxed by H(S) | Y:
                P_6 = M^2/(4a) + H(S)*y + S*z      [ 7 params on comp I,
                                                     6 on comp II ]
  level m>=5  linear in P_{10-m}, polynomial in the earlier free params.

Method here: no symbolic algebra over the whole system.  At each level, fix all
but k of the live unknowns at random, INTERPOLATE the level's condition as a
polynomial of degree <= 3 in the remaining k, solve that small system with a
Groebner basis over GF(p), and extract F_p-rational roots by factoring the
univariate eliminant.  Sound: any solution found is verified against build_N.
"""
import random, sys, itertools
from collections import Counter
import sympy as sp
from trackB1_sqrt import pmul, padd, pscal, ptrim, prange
from trackB1_cascade_general import (prem, component1_S, component2_S,
                                     half_radical)
from trackB1_offbyone_check import build_N
from trackB1_level4 import level4_data

p = 65521

def cond_at(S, Pdict, m, a=1, b=1):
    N = build_N(S, Pdict, m, a, b)
    if N is None:
        return None
    S3 = pmul(pmul(S, S, p), S, p)
    return ptrim(list(prem(N, S3, p)))

def make_P(S, M, wlist, params, layout, a=1):
    """Assemble the P dict from a flat parameter vector."""
    inv4a = pow(4 * a % p, p - 2, p)
    P = {8: pscal(pmul(S, S, p), a, p), 7: pmul(S, M, p)}
    H = half_radical(S, p)
    i = 0
    for w in wlist:
        n = layout[w]
        vec = params[i:i + n]
        i += n
        if w == 6:
            dY = 3 - (len(H) - 1)
            Y = pmul(H, list(vec[:dY + 1]), p) if dY >= 0 else []
            Z = list(vec[dY + 1:])
            P[6] = ptrim(padd(padd(pscal(prem(pmul(M, M, p), S, p), inv4a, p),
                                   Y, p), pmul(S, Z, p), p))
        else:
            lo, hi = prange(w)
            P[w] = ptrim([0] * lo + list(vec))
    for w in range(6, -2, -1):
        P.setdefault(w, [])
    return P

def layout_for(S, wmax=6):
    H = half_radical(S, p)
    lay = {}
    for w in range(wmax, -2, -1):
        if w == 6:
            dY = 3 - (len(H) - 1)
            lay[6] = (dY + 1 if dY >= 0 else 0) + 5
        else:
            lo, hi = prange(w)
            lay[w] = hi - lo + 1
    return lay

def interp_solve(fn, k, nvars, rng, tries=12, maxdeg=3):
    """fn(params)->list of F_p equations.  Fix all but k vars at random,
    interpolate degree<=maxdeg polys in those k, Groebner-solve, return a full
    param vector or None."""
    xs = sp.symbols(f'x0:{k}')
    monos = [m for d in range(maxdeg + 1)
             for m in itertools.combinations_with_replacement(range(k), d)]
    for _ in range(tries):
        idx = rng.sample(range(nvars), k)
        base = [rng.randrange(p) for _ in range(nvars)]

        def ev(vals):
            q = list(base)
            for j, i2 in enumerate(idx):
                q[i2] = vals[j] % p
            return fn(q)

        pts, rows = [], []
        while len(pts) < len(monos) + 6:
            v = [rng.randrange(p) for _ in range(k)]
            pts.append(v)
        vals = [ev(v) for v in pts]
        if any(x is None for x in vals):
            continue
        L = max(len(x) for x in vals) if vals else 0
        if L == 0:
            return base
        A = [[_mval(m, v) for m in monos] for v in pts]
        eqs = []
        for r in range(L):
            rhs = [(x[r] if r < len(x) else 0) for x in vals]
            coef = _solve_lin(A, rhs)
            if coef is None:
                break
            e = 0
            for c, m in zip(coef, monos):
                if c:
                    t = int(c)
                    for i2 in m:
                        t = t * xs[i2]
                    e = e + t
            if e != 0:
                eqs.append(sp.expand(e))
        if not eqs:
            return base
        try:
            G = sp.groebner(eqs, *xs, modulus=p, order='lex')
        except Exception:
            continue
        sol = _extract_root(G, xs, p)
        if sol is None:
            continue
        q = list(base)
        for j, i2 in enumerate(idx):
            q[i2] = int(sol[j]) % p
        if all(x == 0 for x in (fn(q) or [1])):
            return q
    return None

def _mval(m, v):
    t = 1
    for i in m:
        t = t * v[i] % p
    return t

def _solve_lin(A, rhs):
    n = len(A[0])
    M = [row[:] + [rhs[i]] for i, row in enumerate(A)]
    r = 0
    piv = {}
    for c in range(n):
        pr = next((i for i in range(r, len(M)) if M[i][c] % p), None)
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        iv = pow(M[r][c], p - 2, p)
        M[r] = [x * iv % p for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] % p:
                f = M[i][c]
                M[i] = [(M[i][j] - f * M[r][j]) % p for j in range(n + 1)]
        piv[c] = r
        r += 1
    for i in range(len(M)):
        if all(M[i][c] % p == 0 for c in range(n)) and M[i][n] % p:
            return None
    out = [0] * n
    for c, rr in piv.items():
        out[c] = M[rr][n] % p
    return out

def _extract_root(G, xs, p):
    """Back-substitute a lex Groebner basis to one F_p point, or None."""
    polys = list(G.exprs)
    if 1 in polys or sp.Integer(1) in polys:
        return None
    assign = {}
    for v in reversed(xs):
        cands = [q for q in polys
                 if q.free_symbols and q.free_symbols <= ({v} |
                                                          set(assign.keys()))]
        got = None
        for q in cands:
            qq = sp.expand(q.subs(assign))
            if qq == 0:
                continue
            if not qq.free_symbols:
                return None
            try:
                P1 = sp.Poly(qq, v, modulus=p)
            except Exception:
                continue
            if P1.degree() < 1:
                continue
            for fac, _ in P1.factor_list()[1]:
                if sp.Poly(fac, v, modulus=p).degree() == 1:
                    c = sp.Poly(fac, v, modulus=p).all_coeffs()
                    got = (-int(c[1]) * pow(int(c[0]), p - 2, p)) % p
                    break
            if got is not None:
                break
        assign[v] = sp.Integer(got if got is not None else 0)
    return [assign[v] for v in xs]

def solve_upto(S, M, mmax, rng, a=1, b=1, k=4, verbose=False):
    """Solve levels 4..mmax jointly, returning the parameter vector or None."""
    lay = layout_for(S)
    wl = []
    params = []
    for m in range(4, mmax + 1):
        w = 10 - m
        if w > 6:
            continue
        wl.append(w)
        params += [0] * lay[w]
        nvars = len(params)

        def fn(q, _m=m, _wl=list(wl)):
            P = make_P(S, M, _wl, q, lay, a)
            return cond_at(S, P, _m, a, b)

        sol = interp_solve(fn, min(k, nvars), nvars, rng)
        if sol is None:
            return None, m
        params = sol
        if verbose:
            print(f"    level {m} solved (w={w}, {nvars} live params)")
    return (params, wl, lay), None

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    mmax = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    rng = random.Random(seed)
    print(f"JOINT level solve, levels 4..{mmax}  (p={p}, seed={seed})\n")
    for tag in ("I", "II"):
        tally = Counter()
        for _ in range(n):
            if tag == "I":
                A = [1, rng.randrange(p), rng.randrange(1, p)]
                S = component1_S(A, 1, p)
            else:
                S = None
                for _ in range(400):
                    u, v = rng.randrange(1, p), rng.randrange(1, p)
                    S = component2_S(u, v, 1, p)
                    if S:
                        break
            if S is None:
                continue
            M = [rng.randrange(p) for _ in range(5)]
            res, failed = solve_upto(S, M, mmax, rng, verbose=(n <= 3))
            tally["solved" if res else f"failed at level {failed}"] += 1
        tot = sum(tally.values())
        print(f"  component {tag}: ({tot} samples)")
        for kk, c in sorted(tally.items(), key=lambda t: -t[1]):
            print(f"     {kk:<28} {c}/{tot}")
        print()
