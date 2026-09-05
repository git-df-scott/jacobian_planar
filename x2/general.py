#!/usr/bin/env python3
"""General strip engine for  {P,Q} = x^k.

Configuration (mu, rmax, smax, k, m):

  T = x y^mu ,  P_rho = y^-rho f_rho(T) for rho = 0..rmax ,
                Q_sigma = y^-sigma g_sigma(T) for sigma = 0..smax .

  {P_rho,Q_sigma} = y^(mu-1-rho-sigma) ( rho f g' - sigma f' g )

  x^k = T^k y^(-k*mu) sits at level rho+sigma = (k+1)mu - 1, so we require
  rmax + smax = (k+1)mu - 1, and P must carry the vertex (1,0) which lives in
  slice rho = mu at T-degree 1, so rmax >= mu.

  Slice supports:  f_rho = sum_{n=ceil(rho/mu)}^{m}   c[rho,n] T^n
                   g_sigma = sum_{n=ceil(sigma/mu)}^{M} d[sigma,n] T^n
  with M = smax*m/rmax, forced by the cancellation of the top level's leading
  term (rmax*deg g - smax*deg f = 0).  Then
      deg P = (mu+1)*m ,  deg Q = (mu+1)*M ,  deg Q : deg P = smax : rmax .

  Normalisation c[mu,1] = 1 (the vertex (1,0), the campaign's p10).
  Nondegeneracy: the top coefficients c[0,m] and c[rmax,m] are inverted.

The cascade solves g_smax, g_smax-1, ..., g_0 in turn: at level
Ltop - t the new unknown is g_{smax-t}, entering through the pair
(rmax, smax-t) with diagonal coefficient c[rmax,lo]*(rmax*n - (smax-t)*lo).
That vanishes at n = (smax-t)*lo/rmax -- a resonance, which the generator
reports rather than silently dividing by zero.
"""
import subprocess, sys, os
from math import ceil
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))


def config(mu, rmax, smax, k, m):
    assert rmax + smax == (k + 1) * mu - 1, "level mismatch"
    assert rmax >= mu, "P cannot carry the vertex (1,0)"
    Mf = Fraction(smax * m, rmax)
    if Mf.denominator != 1:
        return None
    return int(Mf)


def gen(mu, rmax, smax, k, m, p=32003):
    M = config(mu, rmax, smax, k, m)
    if M is None:
        return None
    if m < ceil(Fraction(rmax, mu)):
        return None
    Mf = M
    lo_f = {r: ceil(Fraction(r, mu)) for r in range(rmax + 1)}
    lo_g = {s: ceil(Fraction(s, mu)) for s in range(smax + 1)}
    fvars = {}
    idx = 0
    for r in range(rmax + 1):
        for n in range(lo_f[r], m + 1):
            idx += 1
            fvars[(r, n)] = f'c({idx})'
    # resonances: coefficients of g that the cascade cannot solve for.  They are
    # FREE unknowns, not zero -- allocate a ring variable for each.
    lo_top0 = lo_f[rmax]
    resvars = {}
    for t in range(0, smax + 1):
        s_new = smax - t
        for n in range(lo_g[s_new], int(Mf) + 1):
            if rmax * n - s_new * lo_top0 == 0:
                idx += 1
                resvars[(s_new, n)] = f'c({idx})'
    nvars = idx
    lines = [f'ring R0 = {p}, (c(1..{nvars}), T), dp;']
    for r in range(rmax + 1):
        terms = []
        for n in range(lo_f[r], m + 1):
            coef = '1' if (r, n) == (mu, 1) else fvars[(r, n)]
            terms.append(f'{coef}*T^{n}')
        lines.append(f'poly f{r} = ' + ' + '.join(terms) + ';')
    lines += [
        'proc cf(poly q, int e) { matrix Mx = coeffs(q, T); if (e+1 > nrows(Mx)) { return(poly(0)); } return(Mx[e+1,1]); }',
        'proc addall(poly q) { matrix Mx = coeffs(q,T); int e; ideal J; for (e=1; e<=nrows(Mx); e++) { J = J + ideal(Mx[e,1]); } return(J); }',
        'poly cur; poly dd; int n; ideal RES;',
    ]
    Ltop = rmax + smax
    lo_top = lo_f[rmax]
    resonances = []
    for t in range(0, smax + 1):
        s_new = smax - t
        L = Ltop - t
        # source = all pairs (rho,sigma) with rho+sigma = L, sigma > s_new
        src = []
        for rho in range(rmax + 1):
            sig = L - rho
            if sig < 0 or sig > smax or sig <= s_new:
                continue
            src.append(f'({rho})*f{rho}*diff(g{sig},T) - ({sig})*diff(f{rho},T)*g{sig}')
        rhs = ' - T^%d' % k if L == Ltop else ''
        lines.append(f'poly src{s_new} = ' + (' + '.join(src) if src else '0') + rhs + ';')
        lines.append(f'poly g{s_new} = 0;')
        lines.append(f'poly op{s_new};')
        for n in range(lo_g[s_new], M + 1):
            diag = rmax * n - s_new * lo_top
            if diag == 0:
                resonances.append((s_new, n))
                lines.append(f'g{s_new} = g{s_new} + {resvars[(s_new, n)]}*T^{n};')
                continue
            lines.append(
                f'op{s_new} = ({rmax})*f{rmax}*diff(g{s_new},T) - ({s_new})*diff(f{rmax},T)*g{s_new} + src{s_new};')
            lines.append(f'dd = -cf(op{s_new}, {n + lo_top - 1})/({diag});')
            lines.append(f'g{s_new} = g{s_new} + dd*T^{n};')
        lines.append(
            f'op{s_new} = ({rmax})*f{rmax}*diff(g{s_new},T) - ({s_new})*diff(f{rmax},T)*g{s_new} + src{s_new};')
        lines.append(f'RES = RES + addall(op{s_new});')
    # levels below smax..0 that no g introduces: L = Ltop - t for t > smax
    for L in range(Ltop - smax - 1, -1, -1):
        src = []
        for rho in range(rmax + 1):
            sig = L - rho
            if sig < 0 or sig > smax:
                continue
            src.append(f'({rho})*f{rho}*diff(g{sig},T) - ({sig})*diff(f{rho},T)*g{sig}')
        if src:
            lines.append('RES = RES + addall(' + ' + '.join(src) + ');')
    lines += [
        'RES = simplify(RES,2);',
        f'"CFG mu={mu} rmax={rmax} smax={smax} k={k} m={m} M={M} degP={(mu+1)*m} degQ={(mu+1)*M} vars={nvars} conds=" + string(size(RES));',
        f'ring RF = {p}, (c(1..{nvars}), U), dp;',
        'ideal I = imap(R0,RES) + ideal(U*' + fvars[(0, m)] + '*' + fvars[(rmax, m)] + ' - 1);',
        'ideal G = std(I);',
        '"VERDICT dim " + string(dim(G)) + " GB1 " + string(G[1]);',
        'quit;',
    ]
    return '\n'.join(lines), nvars, M, resonances


def run(mu, rmax, smax, k, m, p=32003, budget=900):
    out = gen(mu, rmax, smax, k, m, p)
    if out is None:
        print(f"mu={mu} ({rmax},{smax}) k={k} m={m}: skipped (M not integral)")
        return
    script, nvars, M, res = out
    tag = f'gen_{mu}_{rmax}_{smax}_{k}_{m}_{p}'
    path = os.path.join(HERE, f'_{tag}.sing')
    open(path, 'w').write(script)
    if res:
        print(f"  resonances (free unknowns added): {res}", flush=True)
    try:
        r = subprocess.run(['Singular', '-q', path], capture_output=True, text=True, timeout=budget)
        lines = [l for l in r.stdout.splitlines() if l.startswith(('CFG', 'VERDICT'))]
        print(' | '.join(lines) if lines else f'mu={mu} ({rmax},{smax}) m={m}: no output\n{r.stdout[:300]}', flush=True)
    except subprocess.TimeoutExpired:
        print(f"mu={mu} ({rmax},{smax}) k={k} m={m}: TIMEOUT {budget}s", flush=True)


if __name__ == '__main__':
    a = [int(v) for v in sys.argv[1:]]
    run(*a)
