#!/usr/bin/env python3
"""DIRECT COUNTEREXAMPLE ATTEMPT: descend the repaired branch-1 point to the bottom.

Top-down clears 20..15.  Bottom-up clears -2..8.  Only levels 9..14 remain.
If the descent closes, the output IS an explicit (P,Q) with {P,Q} = x^2 on the
pentagon's Newton polygon -- and by Jung-van der Kulk a Keller map with degree
ratio 3:2 cannot be an automorphism, so it would be a counterexample.

Ladder (s-form):  sum_{a+b=L} [ b h_a' g_b - a h_a g_b' ] = delta_{L,-2} s^2 .
Everything in z = s - tau; the gauge pieces h_{-1} = s = z + tau and
g_{-1} = s^2 bring tau in at the bottom, which is where an obstruction would bite.

Kernels are retained symbolically at every level (A3).  Consistency by rank.
"""
import sympy as sp
z, tau = sp.symbols('z tau')
c0, c1 = sp.symbols('c0 c1', nonzero=True)
s = z + tau
def hsup(a):
    return [i for i in range(9) if 0 <= i+a <= 16 and max(0,(i+a)-8) <= i <= min(8,(i+a)//2+1)]
def gsup(b):
    return [k for k in range(13) if (k+b) >= 0 and ((k+1)//2 if k <= 2 else 2*k-3) <= k+b <= 12+k]

H, G, SYM = {}, {}, []
def mk(name, deg):
    cs = [sp.Symbol(f'{name}{i}') for i in range(deg+1)]
    SYM.extend(cs)
    return sum(cs[i]*z**i for i in range(deg+1))
H[8]  = c0*z**8
H[7]  = 2*z**8                     # a4 = 2  (repaired witness)
H[6]  = z**8                       # b8 = 1  -> a4^2 = 4 c0 b8 with c0 = 1
G[12] = c1*z**12
H[-1] = sp.expand(s)               # gauge p_0_1 = 1
G[-1] = sp.expand(s**2)            # gauge q_1_2 = 1
for a in range(0, 6): H[a] = mk(f'h{a}_', max(hsup(a)))
for b in range(0, 12): G[b] = mk(f'g{b}_', max(gsup(b)))

def resolve(e, sub):
    """sympy .subs is a single simultaneous pass; earlier entries of `sub` can map
    to expressions still containing later-fixed symbols.  Iterate to a fixed point."""
    for _ in range(12):
        e2 = sp.expand(e.subs(sub))
        if e2 == e: return e2
        e = e2
    return e

def lev(L):
    e = 0
    for a in range(-1, 9):
        b = L-a
        if a in H and b in G: e += b*sp.diff(H[a],z)*G[b] - a*H[a]*sp.diff(G[b],z)
    return sp.expand(e - (s**2 if L == -2 else 0))

sub, carried = {}, []
print("descending with c0 = c1 = 1:", flush=True)
fix = {c0: 1, c1: 1}
for L in range(19, -3, -1):
    e = sp.expand(resolve(lev(L), sub).subs(fix))
    eqs = [c for c in (sp.Poly(e, z).all_coeffs() if e != 0 else []) if c != 0]
    if not eqs:
        print(f"  level {L:3d}: identically satisfied", flush=True); continue
    new = sorted({v for v in set().union(*[c.free_symbols for c in eqs]) if v in SYM}
                 - set(carried), key=str)
    unk = new + carried
    if not unk:
        bad = [c for c in eqs if sp.simplify(c) != 0]
        print(f"  level {L:3d}: {len(eqs)} eqs, NO unknowns -> "
              f"{'SATISFIED' if not bad else f'{len(bad)} PURE OBSTRUCTIONS'}", flush=True)
        if bad:
            print("        first:", sp.factor(bad[0]), flush=True); break
        continue
    # linear in the NEW unknowns only; carried kernel parameters ride in the
    # coefficients (they multiply new unknowns, so including them is nonlinear)
    M, v = sp.linear_eq_to_matrix(eqs, new)
    rM, rA = M.rank(), M.row_join(v).rank()
    ok = rM == rA
    print(f"  level {L:3d}: {len(eqs):2d} eqs, {len(new):2d} new + {len(carried):2d} carried, "
          f"rank {rM}, kernel {len(new)-rM} -> {'OK' if ok else 'INCONSISTENT'}", flush=True)
    if not ok:
        # Obstructions may involve CARRIED parameters, which are still free: then
        # they are conditions to impose, not inconsistencies.  Iterate until the
        # level is consistent or no free parameter remains to absorb them.
        for _round in range(12):
            conds = []
            for n in M.T.nullspace():
                val = sp.simplify(sp.expand((n.T*v)[0,0]))
                if val != 0: conds.append(val)
            if not conds: ok = True; break
            cfree = sorted({x for c in conds for x in c.free_symbols} & set(carried), key=str)
            if not cfree:
                print(f"        GENUINE OBSTRUCTION at level {L}, no free parameter:",
                      sp.factor(conds[0]), flush=True); break
            csol = sp.solve(conds, cfree, dict=True)
            if not csol:
                print(f"        conditions unsatisfiable in {[str(x) for x in cfree]}",
                      flush=True); break
            print(f"        round {_round}: imposing {csol[0]}", flush=True)
            sub.update({k: sp.expand(vv) for k, vv in csol[0].items()})
            carried = [x for x in carried if x not in csol[0]]
            new = [x for x in new if x not in csol[0]]
            e = sp.expand(resolve(lev(L), sub).subs(fix))
            eqs = [c for c in (sp.Poly(e, z).all_coeffs() if e != 0 else []) if c != 0]
            if not eqs or not new: ok = True; break
            M, v = sp.linear_eq_to_matrix(eqs, new)
            if M.rank() == M.row_join(v).rank(): ok = True; break
        if not ok: break
        print(f"  level {L:3d}: OK after imposing", flush=True)
    sol = sp.solve(eqs, new, dict=True)
    if not sol: print("        !! solve empty", flush=True); break
    sub.update({k: sp.expand(val) for k, val in sol[0].items()})
    carried = sorted((set(new) - set(sol[0])) | set(carried), key=str)
