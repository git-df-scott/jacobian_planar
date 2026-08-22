#!/usr/bin/env python3
"""Triangulate the endgame: 59 conditions in 19 parameters (levels 7 .. -1).

Fast and exact.  When a condition is LINEAR in x, write it c = c1*x + c0.
Substituting x = -c0/c1 into another condition e of degree d in x is done
WITHOUT ever forming a rational function:

    e(x) = sum_k e_k x^k   ->   c1^d * e(-c0/c1) = sum_k e_k (-c0)^k c1^(d-k)

which is pure polynomial arithmetic.  Multiplying by c1^d is harmless exactly
when c1 != 0, which is either automatic (c1 a nonzero rational) or a recorded
branch assumption.  sp.cancel on substituted rational functions is what made
the first attempt unusable -- expression swell, minutes per step.

Elimination discipline, strongest first:
  R1  linear in x, coefficient a NONZERO RATIONAL      unconditional
  R2  a pure power of a single variable                unconditional
  R3  linear in x, coefficient a nonzero POLYNOMIAL    branch, assumption logged
A condition reducing to a nonzero constant means this component is EMPTY.
"""
import sympy as sp, pickle, sys
conds, sub = pickle.load(open('endgame.pkl','rb'))
conds = [sp.expand(c) for c in conds]
def freev(C): return sorted(set().union(*[c.free_symbols for c in C]), key=str) if C else []
print(f"start: {len(conds)} conditions, {len(freev(conds))} parameters", flush=True)

def prim(c):
    vs = sorted(c.free_symbols, key=str)
    if not vs: return c
    return sp.Poly(c, *vs).primitive()[1].as_expr()

def reduce_all(C):
    out, seen = [], set()
    for c in C:
        c = sp.expand(c)
        if c == 0: continue
        if c.is_number:
            print(f"\n*** condition reduced to the nonzero constant {c} ***")
            print("*** THIS COMPONENT IS EMPTY ***", flush=True); sys.exit(0)
        p = prim(c)
        sig = sp.srepr(p if sp.Poly(p, *sorted(p.free_symbols, key=str)).LC() > 0 else sp.expand(-p))
        if sig in seen: continue
        seen.add(sig); out.append(p)
    return out

def elim_linear(e, x, c1, c0):
    """return c1^deg * e(x = -c0/c1), expanded; pure polynomial arithmetic"""
    P = sp.Poly(e, x); d = P.degree()
    if d == 0: return sp.expand(e)
    acc = 0
    for k in range(d+1):
        ck = P.coeff_monomial(x**k) if k else P.coeff_monomial(1)
        if ck == 0: continue
        acc += ck * (-c0)**k * c1**(d-k)
    return sp.expand(acc)

conds = reduce_all(conds)
assumptions, elim, order = [], {}, []
for step in range(200):
    if not conds:
        print("\n*** ALL CONDITIONS SATISFIED ***", flush=True); break
    V = freev(conds)
    pick = None
    for rank in ('R1', 'R2', 'R3'):
        cand = []
        for c in conds:
            fs = sorted(c.free_symbols, key=str)
            if rank == 'R2':
                if len(fs) == 1: cand.append((sp.count_ops(c), c, fs[0], None, None))
                continue
            for x in fs:
                P = sp.Poly(c, x)
                if P.degree() != 1: continue
                c1 = P.coeff_monomial(x); c0 = P.coeff_monomial(1)
                if rank == 'R1' and not (c1.is_number and c1 != 0): continue
                if rank == 'R3' and c1 == 0: continue
                cand.append((sp.count_ops(c), c, x, c1, c0))
        if cand:
            cand.sort(key=lambda t: (t[0], str(t[2]))); pick = (rank,) + cand[0][1:]; break
    if not pick:
        print(f"\nNO LINEAR PIVOT LEFT.  IRREDUCIBLE CORE: {len(conds)} condition(s) "
              f"in {len(V)} parameter(s): {[str(v) for v in V]}", flush=True)
        for c in conds: print("   ", str(sp.factor(c))[:220], flush=True)
        break
    rank, c, x, c1, c0 = pick
    if rank == 'R2':
        rts = sp.solve(c, x)
        if not rts:
            print(f"\n*** {c} has no root in {x} -> EMPTY ***", flush=True); sys.exit(0)
        val = rts[0]
        rest = [sp.expand(e.subs(x, val)) for e in conds if e is not c]
        if len(rts) > 1: assumptions.append(f"{x}: chose root {val} of {len(rts)}")
    else:
        val = sp.cancel(-c0/c1)
        rest = [elim_linear(e, x, c1, c0) for e in conds if e is not c]
        if rank == 'R3': assumptions.append(f"NONZERO: {sp.factor(c1)}")
    elim[x] = val; order.append((rank, str(x)))
    conds = reduce_all(rest)
    print(f"step {step:3d} [{rank}] {x} := (expr, {sp.count_ops(val)} ops)  -> "
          f"{len(conds)} conditions, {len(freev(conds))} parameters", flush=True)

print(f"\neliminated {len(elim)}: {order}")
print(f"branch assumptions: {len(assumptions)}")
for a in assumptions: print("   ", a[:180])
pickle.dump((conds, elim, sub, assumptions), open('endgame_solved.pkl','wb'))
print("saved endgame_solved.pkl", flush=True)
