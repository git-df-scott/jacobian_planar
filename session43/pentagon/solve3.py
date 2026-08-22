#!/usr/bin/env python3
"""Triangulate the endgame: 59 conditions in 19 parameters (levels 7 .. -1).

WHY THE FIRST TWO ATTEMPTS FAILED, recorded because the fix is the whole point:

  attempt 1  substituted x = -c0/c1 as a rational function and called
             sp.cancel.  Expression swell; minutes per step.
  attempt 2  cleared denominators by hand as sum_k e_k (-c0)^k c1^(d-k).  That
             is correct but forms (-c0)^k EXPLICITLY, and c0 has up to 400
             terms, so c0^4 is on the order of 10^7 terms.  Worse than
             attempt 1.  It only ever completed the ONE step whose pivot
             happened to be linear everywhere.

The right primitive is the PSEUDO-REMAINDER prem(e, c, x): the same
denominator-clearing, but performed incrementally with reduction after each
step, so intermediate results stay small.  And the degree profile says most of
the work is free anyway --

    g1_1, g2_2, g4_4 have MAX DEGREE 1 across all 59 conditions,

so eliminating them cannot blow up at all.  Pivot preference, best first:

  P1  max degree 1 over ALL conditions, rational leading coefficient
        -> unconditional AND no growth possible
  P2  linear in this condition, rational leading coefficient
        -> unconditional
  P3  a pure power of a single variable
        -> unconditional
  P4  linear in this condition, polynomial leading coefficient
        -> BRANCH: the coefficient is assumed nonzero and logged

A condition reducing to a nonzero constant means the component is EMPTY.
Every reduction is capped: a pivot whose result exceeds MAXTERMS is abandoned
and the next candidate tried, so one bad choice cannot hang the run.
"""
import sympy as sp, pickle, sys, time
MAXTERMS = 60000
conds, sub = pickle.load(open('endgame.pkl','rb'))
conds = [sp.expand(c) for c in conds]
def freev(C): return sorted(set().union(*[c.free_symbols for c in C]), key=str) if C else []
def nterms(e): return len(e.args) if e.is_Add else 1

def prim(c):
    vs = sorted(c.free_symbols, key=str)
    if not vs: return c
    P = sp.Poly(c, *vs).primitive()[1]
    return P.as_expr() if P.LC() > 0 else (-P).as_expr()

def reduce_all(C):
    out, seen = [], set()
    for c in C:
        c = sp.expand(c)
        if c == 0: continue
        if c.is_number:
            print(f"\n*** a condition reduced to the nonzero constant {c} ***")
            print("*** THIS COMPONENT IS EMPTY ***", flush=True); sys.exit(0)
        p = prim(c)
        sig = sp.srepr(p)
        if sig in seen: continue
        seen.add(sig); out.append(p)
    return out

# ---- CHECKPOINTING ----------------------------------------------------
# The VM this runs on is SUSPENDED between tool calls: CPU time tracks elapsed
# time exactly, so a backgrounded job makes NO progress while the session is
# idle.  Long runs therefore have to proceed in foreground slices, and each
# slice must resume exactly where the last one stopped.
import os
CKPT = 'solve3.ckpt'
if os.path.exists(CKPT):
    conds, elim, order, assumptions = pickle.load(open(CKPT, 'rb'))
    print(f"RESUMED: {len(conds)} conditions, {len(freev(conds))} parameters, "
          f"{len(elim)} already eliminated", flush=True)
else:
    print(f"start: {len(conds)} conditions, {len(freev(conds))} parameters", flush=True)
    conds = reduce_all(conds)
    assumptions, elim, order = [], {}, []
    pickle.dump((conds, elim, order, assumptions), open(CKPT, 'wb'))
DEADLINE = time.time() + float(os.environ.get('SLICE', '540'))

for step in range(300):
    if not conds:
        print("\n*** ALL CONDITIONS SATISFIED ***", flush=True); break
    V = freev(conds)
    # One Poly per condition over ALL variables, not one per (condition,
    # variable) pair.  The naive version cost 77 SECONDS per step -- 19 steps
    # of pure overhead -- because sp.Poly(c, v) reparses the whole expression
    # for each v.  Built this way the per-variable degrees are free.
    P_of = {}
    for c in conds:
        vs = sorted(c.free_symbols, key=str)
        P_of[c] = (sp.Poly(c, *vs), vs)
    maxdeg = {v: 0 for v in V}
    for c, (P, vs) in P_of.items():
        for j, v in enumerate(vs):
            d = max(m[j] for m in P.monoms())
            if d > maxdeg[v]: maxdeg[v] = d
    cands = []
    for c in conds:
        P, vs = P_of[c]
        fs = vs
        if len(fs) == 1:
            cands.append((3, nterms(c), str(fs[0]), c, fs[0], None))
            continue
        for j, x in enumerate(fs):
            if max(m[j] for m in P.monoms()) != 1: continue
            c1 = sp.Poly(c, x).coeff_monomial(x)
            if c1 == 0: continue
            if c1.is_number and maxdeg[x] == 1: tier = 1
            elif c1.is_number:                  tier = 2
            else:                               tier = 4
            cands.append((tier, nterms(c), str(x), c, x, c1))
    if not cands:
        print(f"\nNO LINEAR PIVOT LEFT.  IRREDUCIBLE CORE: {len(conds)} condition(s) "
              f"in {len(V)} parameter(s): {[str(v) for v in V]}", flush=True)
        for c in conds: print("   ", str(sp.factor(c))[:240], flush=True)
        break
    cands.sort(key=lambda t: (t[0], t[1], t[2]))
    done = False
    for tier, _n, _sx, c, x, c1 in cands:
        t0 = time.time()
        try:
            if c1 is None:
                rts = sp.solve(c, x)
                if not rts:
                    print(f"\n*** {c} has no root in {x} -> EMPTY ***", flush=True); sys.exit(0)
                val = rts[0]
                if len(rts) > 1: assumptions.append(f"{x}: chose root {val} of {len(rts)} (BRANCH)")
                rest = [sp.expand(e.subs(x, val)) for e in conds if e is not c]
            else:
                val = sp.cancel(-sp.Poly(c, x).coeff_monomial(1)/c1)
                rest = []
                for e in conds:
                    if e is c: continue
                    r = sp.expand(sp.prem(e, c, x)) if x in e.free_symbols else e
                    if nterms(r) > MAXTERMS: raise OverflowError(str(x))
                    rest.append(r)
                if tier == 4: assumptions.append(f"NONZERO: {sp.factor(c1)}")
        except OverflowError as ex:
            print(f"      pivot {ex} abandoned (> {MAXTERMS} terms)", flush=True); continue
        elim[x] = val; order.append((f"P{tier}", str(x)))
        conds = reduce_all(rest)
        print(f"step {step:3d} [P{tier}] {x}  ({time.time()-t0:.1f}s) -> {len(conds)} conditions, "
              f"{len(freev(conds))} parameters, biggest {max([nterms(e) for e in conds] or [0])} terms",
              flush=True)
        pickle.dump((conds, elim, order, assumptions), open(CKPT, 'wb'))
        done = True
        if time.time() > DEADLINE:
            print(f"\n--- slice deadline reached, checkpointed after {len(elim)} "
                  f"eliminations; rerun to continue ---", flush=True)
            sys.exit(3)
        break
    if not done:
        print("\nevery pivot blew the term cap; stopping", flush=True); break

print(f"\neliminated {len(elim)}: {order}")
print(f"branch assumptions: {len(assumptions)}")
for a in assumptions: print("   ", a[:200])
pickle.dump((conds, elim, sub, assumptions), open('endgame_solved.pkl','wb'))
print("saved endgame_solved.pkl", flush=True)
