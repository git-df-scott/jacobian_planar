#!/usr/bin/env python3
"""Corrected descent: IMPOSE each level's conditions before continuing.

fastdescend.py computed C_L without imposing higher levels' conditions, so once
level 18's divisibility failed it propagated placeholders downward.  Here every
level's conditions are solved and substituted before the next level is formed.

Per level L (7 <= L <= 19):
   sigma^7 | C_L                      -> [C_L]_m = 0, m = 0..6
   [C_L/sigma^7]_{L-8} = 0            -> the scalar obstruction
then  [g_{L-8}]_m = ( -[C_L/sigma^7]_m/(L-8-m) + 12 c1 [h_{L-12}]_{m-4} ) / (8 c0)
for m != L-8, with [g_{L-8}]_{L-8} free.
h_{L-12} stays free (A3: never chosen greedily).
"""
import sympy as sp
sg, tau, c0, c1 = sp.symbols('sigma tau c0 c1')
s = sg + tau
def hdeg(a): return min(8, a+2)
def gdeg(b): return min(12, b+3)
H, G, FREE = {}, {}, []
for a in range(-1, 8):
    lo = max(0, -a)
    cs = [sp.Symbol(f'H{a}_{i}') for i in range(lo, hdeg(a)+1)]
    FREE.extend(cs); H[a] = sp.expand(sum(cs[i-lo]*s**i for i in range(lo, hdeg(a)+1)))
H[-1] = sp.expand(s); H[8] = sp.expand(c0*sg**8)
G[12] = sp.expand(c1*sg**12); G[-1] = sp.expand(s**2)
def coef(e, m): return sp.expand(sp.expand(e).coeff(sg, m))
def CL(L, H, G):
    e = 0
    for a in range(-1, 9):
        b = L-a
        if not (-1 <= b <= 12): continue
        if (a, b) in ((8, L-8), (L-12, 12)): continue
        if a not in H or b not in G: return None
        e += b*sp.diff(H[a], sg)*G[b] - a*H[a]*sp.diff(G[b], sg)
    return sp.expand(e)

sub = {}
for L in range(19, 6, -1):
    C = CL(L, H, G)
    if C is None: print(f"level {L}: pieces missing", flush=True); break
    C = sp.expand(C.subs(sub))
    eqs = [coef(C, m) for m in range(7)]
    eqs = [e for e in eqs if e != 0]
    unk = sorted(set().union(*[e.free_symbols for e in eqs]) & set(FREE), key=str) if eqs else []
    if eqs:
        # The divisibility conditions are QUADRATIC in the carried h-coefficients
        # (g_{b} is linear in h, so their bracket is quadratic), so no linear solve.
        if L == 18:
            # proved twice independently (EDGE/S_LADDER): sigma^2 | h_7
            h7 = H[7]
            tgt = sorted([v for v in h7.free_symbols if str(v).startswith('H7_')], key=str)[:2]
            sol = sp.solve([h7.subs(sg, 0), sp.diff(h7, sg).subs(sg, 0)], tgt, dict=True)
            if not sol: print("   !! could not impose sigma^2 | h_7", flush=True); break
            print("   imposing the PROVED level-18 condition sigma^2 | h_7", flush=True)
        else:
            sol = sp.solve(eqs, unk, dict=True)
            if not sol:
                print(f"level {L:3d}: conditions have NO SOLUTION in the free "
                      f"coefficients -- this is a genuine obstruction candidate, "
                      f"verify before claiming", flush=True)
                break
        sub.update({k: sp.expand(val) for k, val in sol[0].items()})
        C = sp.expand(C.subs(sub))
        for a in H: H[a] = sp.expand(H[a].subs(sub))
        for b in G: G[b] = sp.expand(G[b].subs(sub))
    nz = [m for m in range(7) if coef(C, m) != 0]
    print(f"level {L:3d}: imposed {len(eqs)} divisibility conds, "
          f"residual nonzero low coeffs: {nz}", flush=True)
    if nz: break
    Cq = sp.expand(sp.cancel(C/sg**7))
    obs = coef(Cq, L-8)
    print(f"          scalar obstruction [C/sigma^7]_{L-8} = "
          f"{'0 (auto)' if obs == 0 else 'NONZERO -> a condition'}", flush=True)
    b = L-8
    if not (-1 <= b <= 12): break
    gc = {}
    for m in range(0, gdeg(b)+1):
        if m == b:
            k = sp.Symbol(f'K{b}'); FREE.append(k); gc[m] = k; continue
        hm = coef(H[L-12], m-4) if (-1 <= L-12 <= 7 and m >= 4) else 0
        gc[m] = sp.expand((-coef(Cq, m)/(b-m) + 12*c1*hm)/(8*c0))
    G[b] = sp.expand(sum(gc[m]*sg**m for m in gc))
