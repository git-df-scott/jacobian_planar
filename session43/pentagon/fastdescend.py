#!/usr/bin/env python3
"""Fast descent on the diagonal recursion.

Level L (7 <= L <= 19):
    8 c0 sigma^7 D_{L-8}(g_{L-8}) - 12 c1 sigma^11 D_{L-12}(h_{L-12}) = -C_L
with D_k diagonal.  Per sigma-power m:
    (L-8-m) * ( 8 c0 [g_{L-8}]_m - 12 c1 [h_{L-12}]_{m-4} ) = -[C_L/sigma^7]_m
so
  * m != L-8 : determines [g_{L-8}]_m from the free [h_{L-12}]_{m-4}
  * m == L-8 : both sides' unknowns drop out -> OBSTRUCTION [C_L/sigma^7]_{L-8} = 0
  * and sigma^7 | C_L  (m = 0..6 of C_L must vanish)

h_{L-12} is free; g_{L-8} is determined except its sigma^(L-8) coefficient.
Controls: level 19 must give kernel 10 (= 9 coeffs of h_7 + 1), and level 18
must reproduce sigma^2 | h_7.
"""
import sympy as sp
sg, tau, c0, c1 = sp.symbols('sigma tau c0 c1')
s = sg + tau

def hdeg(a): return min(8, a+2)
def gdeg(b): return min(12, b+3)

H, G, FREE = {}, {}, []
def mkh(a):
    lo = max(0, -a)
    cs = [sp.Symbol(f'H{a}_{i}') for i in range(lo, hdeg(a)+1)]
    FREE.extend(cs)
    return sp.expand(sum(cs[i-lo]*s**i for i in range(lo, hdeg(a)+1)))
for a in range(-1, 8): H[a] = mkh(a)
H[-1] = sp.expand(s)                       # gauge p_0_1 = 1
H[8]  = sp.expand(c0*sg**8)
G[12] = sp.expand(c1*sg**12)
G[-1] = sp.expand(s**2)                    # gauge q_1_2 = 1

def coef(e, m): return sp.expand(e).coeff(sg, m)

def CL(L):
    e = 0
    for a in range(-1, 9):
        b = L - a
        if not (-1 <= b <= 12): continue
        if (a, b) in ((8, L-8), (L-12, 12)): continue
        if a in H and b in G:
            e += b*sp.diff(H[a], sg)*G[b] - a*H[a]*sp.diff(G[b], sg)
        else:
            return None
    return sp.expand(e)

print("descent:", flush=True)
conds = []
for L in range(19, 6, -1):
    C = CL(L)
    if C is None: print(f"level {L}: missing pieces, stop"); break
    # divisibility sigma^7 | C_L
    div = [sp.expand(coef(C, m)) for m in range(7)]
    div = [d for d in div if d != 0]
    obs = sp.expand(coef(C, L-1))          # the scalar obstruction: [C_L]_{sigma^(L-1)}
    newc = []
    if -1 <= L-12 <= 7: newc.append(f"h_{L-12}")
    print(f"level {L:3d}: new={newc or ['-']}, "
          f"divisibility conds {len(div)}, scalar obstruction {'0 (auto)' if obs==0 else 'nonzero'}",
          flush=True)
    conds += div + ([obs] if obs != 0 else [])
    # determine g_{L-8}
    b = L-8
    if not (-1 <= b <= 12): break
    Cq = sp.expand(sp.cancel(C/sg**7)) if all(coef(C,m)==0 for m in range(7)) else None
    gcoef = {}
    for m in range(0, gdeg(b)+1):
        if m == b:
            gcoef[m] = sp.Symbol(f'K{b}'); FREE.append(gcoef[m]); continue
        rhs = -(coef(Cq, m) if Cq is not None else sp.Symbol(f'UNDIV{L}_{m}'))
        hm = coef(H[L-12], m-4) if (-1 <= L-12 <= 7 and m >= 4) else 0
        gcoef[m] = sp.expand((rhs/(L-8-m) + 12*c1*hm)/(8*c0))
    G[b] = sp.expand(sum(gcoef[m]*sg**m for m in gcoef))
    if L == 19:
        k = len([v for v in FREE if str(v).startswith('H7_') or str(v)=='K11'])
        print(f"   CONTROL level 19 kernel = {k} (expect 10)", flush=True)
