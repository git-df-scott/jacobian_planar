#!/usr/bin/env python3
"""General strip engine, per-slice top degrees.

  T = x y^mu,  P_rho = y^-rho f_rho(T),  Q_sigma = y^-sigma g_sigma(T)
  {P_rho,Q_sigma} = y^(mu-1-rho-sigma) ( rho f g' - sigma f' g )
  x^k sits at level rho+sigma = (k+1)mu - 1 = rmax + smax,  rmax >= mu.

  f_rho = sum_{n=ceil(rho/mu)}^{tops[rho]} c T^n
  g_sigma = sum_{n=ceil(sigma/mu)}^{M}     d T^n ,  M = smax*tops[rmax]/rmax
  (M is forced: the top level's leading term cancels iff rmax*M = smax*deg f_rmax.)

  deg P = max_rho ((mu+1)*tops[rho] - rho),  deg Q = (mu+1)*M.

Coefficients of g that the cascade cannot solve for (diagonal
rmax*n - sigma*lo_top = 0) are added as FREE unknowns, never dropped.
Nondegeneracy: the two top-slice coefficients c[0,tops[0]] and
c[rmax,tops[rmax]] are inverted (these are the polygon's two upper vertices).
"""
import subprocess, os, sys
from math import ceil
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))


def build(mu, rmax, smax, k, tops, N=None, p=32003):
    assert rmax + smax == (k + 1) * mu - 1 and rmax >= mu
    lo_f = {r: ceil(Fraction(r, mu)) for r in range(rmax + 1)}
    lo_g = {s: ceil(Fraction(s, mu)) for s in range(smax + 1)}
    for r in range(rmax + 1):
        if tops[r] < lo_f[r]:
            return None
    # N: a GENEROUS common bound on deg_T of every g_sigma.  Prescribing one
    # degree per slice (as the campaign's windows do) is a restriction; here we
    # search over all Q of strip type with deg_T g_sigma <= N.  Raising N adds
    # unknowns but NOT conditions (the residual count per level is
    # deg f_rmax - lo_top + 1 regardless), so the search only widens.
    if N is None:
        N = 2 * max(tops) + 2
    M = int(N)
    if M < 1:
        return None
    lo_top = lo_f[rmax]
    if (mu, 1) not in [(r, n) for r in range(rmax + 1) for n in range(lo_f[r], tops[r] + 1)]:
        return None  # the vertex (1,0) is not in the support

    fv, idx = {}, 0
    for r in range(rmax + 1):
        for n in range(lo_f[r], tops[r] + 1):
            idx += 1
            fv[(r, n)] = f'c({idx})'
    resv, res = {}, []
    for t in range(smax + 1):
        s_new = smax - t
        for n in range(lo_g[s_new], M + 1):
            if rmax * n - s_new * lo_top == 0:
                idx += 1
                resv[(s_new, n)] = f'c({idx})'
                res.append((s_new, n))
    nvars = idx

    L = [f'ring R0 = {p}, (c(1..{nvars}), T), dp;']
    for r in range(rmax + 1):
        L.append(f'poly f{r} = ' + ' + '.join(
            ('1' if (r, n) == (mu, 1) else fv[(r, n)]) + f'*T^{n}'
            for n in range(lo_f[r], tops[r] + 1)) + ';')
    L += ['proc cf(poly q, int e) { matrix Mx = coeffs(q, T); if (e+1 > nrows(Mx)) { return(poly(0)); } return(Mx[e+1,1]); }',
          'proc addall(poly q) { matrix Mx = coeffs(q,T); int e; ideal J; for (e=1; e<=nrows(Mx); e++) { J = J + ideal(Mx[e,1]); } return(J); }',
          'poly dd; ideal RES;']
    Ltop = rmax + smax
    for t in range(smax + 1):
        s_new, lev = smax - t, Ltop - t
        src = [f'({rho})*f{rho}*diff(g{sig},T) - ({sig})*diff(f{rho},T)*g{sig}'
               for rho in range(rmax + 1)
               for sig in [lev - rho] if 0 <= sig <= smax and sig > s_new]
        rhs = f' - T^{k}' if lev == Ltop else ''
        L.append(f'poly src{s_new} = ' + (' + '.join(src) if src else '0') + rhs + ';')
        L.append(f'poly g{s_new} = 0; poly op{s_new};')
        for n in range(lo_g[s_new], M + 1):
            diag = rmax * n - s_new * lo_top
            if diag == 0:
                L.append(f'g{s_new} = g{s_new} + {resv[(s_new, n)]}*T^{n};')
                continue
            L.append(f'op{s_new} = ({rmax})*f{rmax}*diff(g{s_new},T) - ({s_new})*diff(f{rmax},T)*g{s_new} + src{s_new};')
            L.append(f'dd = -cf(op{s_new}, {n + lo_top - 1})/({diag});')
            L.append(f'g{s_new} = g{s_new} + dd*T^{n};')
        L.append(f'op{s_new} = ({rmax})*f{rmax}*diff(g{s_new},T) - ({s_new})*diff(f{rmax},T)*g{s_new} + src{s_new};')
        L.append(f'RES = RES + addall(op{s_new});')
    for lev in range(Ltop - smax - 1, -1, -1):
        src = [f'({rho})*f{rho}*diff(g{sig},T) - ({sig})*diff(f{rho},T)*g{sig}'
               for rho in range(rmax + 1)
               for sig in [lev - rho] if 0 <= sig <= smax]
        if src:
            L.append('RES = RES + addall(' + ' + '.join(src) + ');')
    degP = max((mu + 1) * tops[r] - r for r in range(rmax + 1))
    degQ = (mu + 1) * M
    L += ['RES = simplify(RES,2);',
          f'"CFG mu={mu} r={rmax} s={smax} k={k} tops={tuple(tops)} M={M} degP={degP} degQ={degQ} vars={nvars} conds=" + string(size(RES));',
          f'ring RF = {p}, (c(1..{nvars}), U), dp;',
          'ideal I = imap(R0,RES) + ideal(U*' + fv[(0, tops[0])] + '*' + fv[(rmax, tops[rmax])] + ' - 1);',
          'ideal G = std(I);',
          '"VERDICT dim " + string(dim(G)) + " GB1 " + string(G[1]);',
          'quit;']
    return '\n'.join(L), nvars, M, res, degP, degQ


def run(mu, rmax, smax, k, tops, N=None, p=32003, budget=420, tag=None):
    b = build(mu, rmax, smax, k, tops, N, p)
    if b is None:
        return None
    script, nvars, M, res, degP, degQ = b
    tag = tag or f'g2_{mu}_{rmax}_{smax}_{k}_' + '_'.join(map(str, tops)) + f'_N{M}'
    path = os.path.join(HERE, f'_{tag}.sing')
    open(path, 'w').write(script)
    try:
        r = subprocess.run(['Singular', '-q', path], capture_output=True, text=True, timeout=budget)
    except subprocess.TimeoutExpired:
        print(f"mu={mu} ({rmax},{smax}) tops={tuple(tops)}: TIMEOUT {budget}s", flush=True)
        return 'TIMEOUT'
    out = [l for l in r.stdout.splitlines() if l.startswith(('CFG', 'VERDICT'))]
    line = ' | '.join(out)
    print(line + (f'   resonant-free: {res}' if res else ''), flush=True)
    os.remove(path)
    return line


if __name__ == '__main__':
    mu, rmax, smax, k, N = (int(v) for v in sys.argv[1:6])
    tops = [int(v) for v in sys.argv[6:]]
    run(mu, rmax, smax, k, tops, None if N == 0 else N)
