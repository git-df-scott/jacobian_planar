#!/usr/bin/env python3
"""DIRECT STRIKE: push the s-ladder to the bottom.

Level L:  sum_{a+b=L} [ b h_a' g_b - a h_a g_b' ] = delta_{L,-2} s^2
New unknowns at level L: h_{L-12} (while L >= 11) and g_{L-8} (while L >= 7).
Levels 6..-1 introduce NOTHING -> pure conditions.

Known so far: h_8 = c0 sigma^8, g_12 = c1 sigma^12 (eighth-power theorem),
and level 18 forces sigma^2 | h_7.  Impose that and keep descending.

Carried freedom stays SYMBOLIC (A3).  Consistency by RANK (A14/A16).
"""
import sympy as sp
s, tau, c0, c1 = sp.symbols('s tau c0 c1')
sg = s - tau

def h_rng(a):
    lo, hi = max(0,-a), min(8, a+2)
    return [i for i in range(lo,hi+1) if 0 <= i+a <= 16]
def g_rng(b):
    return [k for k in range(13)
            if (k+b) >= 0 and ((k+1)//2 if k <= 2 else 2*k-3) <= k+b <= 12+k]

H, G = {}, {}
for a in range(-1,9):
    H[a] = sp.expand(sum((sp.Integer(0) if (i+a,i)==(0,0) else sp.Integer(1) if (i+a,i)==(0,1)
                          else sp.Symbol(f'p_{i+a}_{i}'))*s**i for i in h_rng(a)))
for b in range(-1,13):
    G[b] = sp.expand(sum((sp.Integer(0) if (k+b,k)==(0,0) else sp.Integer(1) if (k+b,k)==(1,2)
                          else sp.Symbol(f'q_{k+b}_{k}'))*s**k for k in g_rng(b)))
def lev(L):
    e = 0
    for a in range(-1,9):
        b = L-a
        if -1 <= b <= 12: e += b*sp.diff(H[a],s)*G[b] - a*H[a]*sp.diff(G[b],s)
    return sp.expand(e - (s**2 if L == -2 else 0))

H[8]  = sp.expand(c0*sg**8)
G[12] = sp.expand(c1*sg**12)
assert sp.simplify(lev(20)) == 0
print("level 20 control: PASS", flush=True)

# level 18 forces sigma^2 | h_7 : impose h_7(tau) = h_7'(tau) = 0
h7 = H[7]
sol = sp.solve([h7.subs(s,tau), sp.diff(h7,s).subs(s,tau)],
               [sp.Symbol('p_7_0'), sp.Symbol('p_8_1')], dict=True)[0]
H[7] = sp.expand(H[7].subs(sol))
print("imposed sigma^2 | h_7 :",
      sp.simplify(H[7].subs(s,tau)) == 0 and sp.simplify(sp.diff(H[7],s).subs(s,tau)) == 0,
      flush=True)

free = []
for L in range(19, -3, -1):
    new = []
    a, b = L-12, L-8
    if -1 <= a <= 8: new += [v for v in H[a].free_symbols if str(v)[0]=='p']
    if -1 <= b <= 12: new += [v for v in G[b].free_symbols if str(v)[0]=='q']
    new = sorted(set(new)-set(free), key=str)
    e = lev(L)
    eqs = [c for c in (sp.Poly(e,s).all_coeffs() if e != 0 else []) if c != 0]
    if not eqs:
        print(f"level {L:3d}: identically satisfied", flush=True); continue
    if not new:
        print(f"level {L:3d}: {len(eqs)} eqs, NO new unknowns -> PURE CONDITIONS "
              f"({len(free)} carried)", flush=True)
        break
    M, v = sp.linear_eq_to_matrix(eqs, new)
    rM, rA = M.rank(), M.row_join(v).rank()
    print(f"level {L:3d}: {len(eqs):2d} eqs, {len(new):2d} new, {len(free):2d} carried, "
          f"rank {rM}, kernel {len(new)-rM} -> {'CONSISTENT' if rM==rA else 'CONDITIONS'}",
          flush=True)
    if rM != rA:
        n_ = M.T.nullspace()
        print(f"       {len(n_)} left-null vectors; conditions:", flush=True)
        for nn in n_[:2]:
            val = sp.simplify(sp.expand((nn.T*v)[0,0]))
            if val != 0: print("       COND:", sp.factor(val), flush=True)
        break
    sol = sp.solve(eqs, new, dict=True)
    if not sol: print("       !! rank consistent, solve empty", flush=True); break
    sub = {k: sp.expand(val) for k, val in sol[0].items()}
    for k_ in H: H[k_] = sp.expand(H[k_].subs(sub))
    for k_ in G: G[k_] = sp.expand(G[k_].subs(sub))
    free = sorted((set(new)-set(sub)) | set(free), key=str)
    assert sp.simplify(lev(L)) == 0, f"level {L} re-check FAILED"
