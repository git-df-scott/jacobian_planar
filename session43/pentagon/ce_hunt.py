#!/usr/bin/env python3
"""FAST COUNTEREXAMPLE HUNT: specialise freely, descend to the bottom.

The A3 hazard is ASYMMETRIC.  Choosing kernel constants greedily can manufacture
a false OBSTRUCTION, so it is fatal when claiming emptiness.  It can never
manufacture a false WITNESS: if a fully specialised descent closes, substituting
the output into {P,Q} verifies it outright.  So for a CE hunt, specialise.

Strategy: descend 19 -> -2 with every coefficient numeric.  At each level solve
the linear system for the new unknowns; whatever stays free is set by `pick`.
Several `pick` policies are tried.  Any run reaching level -2 is a candidate and
is then CHECKED by direct substitution into the bracket.
"""
import sys, random
import sympy as sp
z, tau = sp.symbols('z tau')
def hsup(a):
    return [i for i in range(9) if 0 <= i+a <= 16 and max(0,(i+a)-8) <= i <= min(8,(i+a)//2+1)]
def gsup(b):
    return [k for k in range(13) if (k+b) >= 0 and ((k+1)//2 if k <= 2 else 2*k-3) <= k+b <= 12+k]

def run(TAU, pick, label):
    s = z + TAU
    H = {8: z**8, 7: 2*z**8, 6: z**8, -1: sp.expand(s)}
    G = {12: z**12, -1: sp.expand(s**2)}
    SY = []
    for a in range(0, 6):
        cs = [sp.Symbol(f'h{a}_{i}') for i in hsup(a)]; SY += cs
        H[a] = sum(cs[j]*z**i for j, i in enumerate(hsup(a)))
    for b in range(0, 12):
        cs = [sp.Symbol(f'g{b}_{k}') for k in gsup(b)]; SY += cs
        G[b] = sum(cs[j]*z**k for j, k in enumerate(gsup(b)))
    def lev(L):
        e = 0
        for a in range(-1, 9):
            b = L-a
            if a in H and b in G: e += b*sp.diff(H[a],z)*G[b] - a*H[a]*sp.diff(G[b],z)
        return sp.expand(e - (s**2 if L == -2 else 0))
    sub = {}
    def res(e):
        for _ in range(14):
            e2 = sp.expand(e.subs(sub))
            if e2 == e: return e2
            e = e2
        return e
    for L in range(19, -3, -1):
        e = res(lev(L))
        eqs = [c for c in (sp.Poly(e, z).all_coeffs() if e != 0 else []) if c != 0]
        if not eqs: continue
        unk = sorted({v for v in set().union(*[c.free_symbols for c in eqs]) if v in SY}, key=str)
        if not unk:
            return f"{label}: DEAD at level {L} (pure obstruction, no unknowns)"
        try:
            M, v = sp.linear_eq_to_matrix(eqs, unk)
        except Exception:
            return f"{label}: nonlinear at level {L}"
        if M.rank() != M.row_join(v).rank():
            return f"{label}: DEAD at level {L} (inconsistent)"
        sol = sp.solve(eqs, unk, dict=True)
        if not sol: return f"{label}: DEAD at level {L} (no solution)"
        sd = dict(sol[0])
        free = [u for u in unk if u not in sd]
        for u in free: sd[u] = pick(u)
        for k in list(sd): sd[k] = sp.expand(sp.simplify(sd[k].subs({u: sd[u] for u in free})
                                                        if hasattr(sd[k],'subs') else sd[k]))
        sub.update(sd)
        for _ in range(4):
            sub = {k: sp.expand(vv.subs(sub)) if hasattr(vv,'subs') else vv for k, vv in sub.items()}
    return f"{label}: **REACHED LEVEL -2**", H, G, sub, s

rnd = random.Random(7)
policies = [(sp.Integer(0), "all free -> 0"),
            (None, "all free -> random small ints")]
for val, label in policies:
    pick = (lambda u: sp.Integer(0)) if val is not None else (lambda u: sp.Integer(rnd.randrange(1,7)))
    out = run(sp.Integer(1), pick, label)
    print(out if isinstance(out, str) else out[0], flush=True)
    if not isinstance(out, str):
        _, H, G, sub, s = out
        print("   candidate found -- verifying by direct substitution", flush=True)
        break
