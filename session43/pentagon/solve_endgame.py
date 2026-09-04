#!/usr/bin/env python3
"""Solve the endgame: 59 conditions in 19 parameters (levels 7 .. -1).

Elimination discipline, strongest first -- only ever take a weaker step when no
stronger one is available:

  RANK 1 (free)   a condition that is linear in X with a NONZERO RATIONAL
                  constant coefficient.  Solving for X is unconditional: it
                  costs no generality and opens no branch.
  RANK 2 (free)   a condition that is a pure power of a single variable X.
                  X = 0 is forced, again unconditional.
  RANK 3 (costly) a condition linear in X whose coefficient is a nonzero
                  POLYNOMIAL.  Solving assumes that polynomial is nonzero, so
                  it opens a branch and the complementary branch is recorded,
                  not explored.
  RANK 4 (costly) a reducible condition: a union of components, take one and
                  record the rest.

Every elimination is followed by re-reducing all conditions and dropping the
ones that become identically zero.  If a condition ever reduces to a NONZERO
CONSTANT, this component is EMPTY and the script says so.
"""
import sympy as sp, pickle, sys
conds, sub = pickle.load(open('endgame.pkl','rb'))
conds = [sp.expand(c) for c in conds]
free = lambda C: sorted(set().union(*[c.free_symbols for c in C]), key=str) if C else []
print(f"start: {len(conds)} conditions, {len(free(conds))} parameters", flush=True)

assumptions, branches, elim = [], [], {}

def prim(c):
    """primitive part, monic in the sorted-variable order -- a cheap canonical
    signature for 'equal up to a nonzero scalar'.  Uses Poly content, NOT
    factor_list, which is catastrophically slow on big multivariate input."""
    vs = sorted(c.free_symbols, key=str)
    P = sp.Poly(c, *vs)
    P = P.primitive()[1]
    lc = P.LC()
    if lc != 0: P = P.quo_ground(lc) if lc.is_Integer else P
    return P.as_expr()

def reduce_all(C):
    out, seen = [], set()
    for c in C:
        c = sp.cancel(c)
        n, _d = sp.fraction(c)
        n = sp.expand(n)
        if n == 0: continue
        if n.is_number:
            print(f"\n*** condition reduced to the nonzero constant {n} ***")
            print("*** THIS COMPONENT IS EMPTY ***", flush=True); sys.exit(0)
        sig = sp.srepr(prim(n))
        if sig in seen: continue
        seen.add(sig); out.append(n)
    return out

conds = reduce_all(conds)
for step in range(200):
    if not conds:
        print("\nALL CONDITIONS SATISFIED", flush=True); break
    V = free(conds)
    pick = None
    # RANK 1
    for c in sorted(conds, key=lambda e: len(e.args)):
        for x in sorted(c.free_symbols, key=str):
            p = sp.Poly(c, x)
            if p.degree() == 1 and p.coeff_monomial(x).is_number and p.coeff_monomial(x) != 0:
                pick = ('R1', c, x); break
        if pick: break
    # RANK 2
    if not pick:
        for c in conds:
            fs = list(c.free_symbols)
            if len(fs) == 1:
                pick = ('R2', c, fs[0]); break
    # RANK 3
    if not pick:
        for c in sorted(conds, key=lambda e: len(e.args)):
            for x in sorted(c.free_symbols, key=str):
                p = sp.Poly(c, x)
                if p.degree() == 1 and p.coeff_monomial(x) != 0:
                    pick = ('R3', c, x); break
            if pick: break
    if not pick:
        print(f"\nNo linear pivot left. IRREDUCIBLE CORE: {len(conds)} condition(s) "
              f"in {len(V)} parameter(s) {[str(v) for v in V]}", flush=True)
        for c in conds: print("   ", str(sp.factor(c))[:200], flush=True)
        break
    rank, c, x = pick
    if rank == 'R2':
        val = sp.Integer(0)
        if sp.factor_list(c)[1][0][0] != x:
            roots = sp.solve(c, x)
            if not roots:
                print(f"\n*** {c} has no root in {x} -> EMPTY ***"); sys.exit(0)
            if len(roots) > 1: branches.append((str(c), f"{len(roots)} roots for {x}"))
            val = roots[0]
    else:
        val = sp.cancel(sp.solve(c, x)[0])
        coeff = sp.Poly(c, x).coeff_monomial(x)
        if rank == 'R3': assumptions.append(sp.factor(coeff))
    elim[x] = val
    conds = reduce_all([sp.expand(e.subs(x, val)) for e in conds if e is not c])
    print(f"step {step:3d} [{rank}] {x} = {str(sp.factor(val))[:90]}   "
          f"-> {len(conds)} conditions, {len(free(conds))} parameters", flush=True)

print(f"\neliminated {len(elim)} parameters")
print(f"branch assumptions (each must be NONZERO): {len(assumptions)}")
for a in assumptions: print("   ", str(a)[:140])
if branches:
    print("unexplored components:")
    for b in branches: print("   ", b)
pickle.dump((conds, elim, sub, assumptions), open('endgame_solved.pkl','wb'))
