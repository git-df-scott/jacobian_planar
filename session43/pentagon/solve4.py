#!/usr/bin/env python3
"""Triangulate the endgame, PERFECT POWERS FIRST.

The rule the earlier attempts missed.  Factor every condition.  If its
factorisation has exactly ONE distinct non-constant irreducible factor, i.e.

        c = const * u^k ,

then u = 0 is FORCED -- unconditionally, one component, no branch choice --
because the variety of c is exactly the variety of u.  This is the same
argument that killed g8_6 and g8_7 at level 8, applied to the endgame.

It matters here because the very first endgame condition is

        -8 (3 g5_4 - 2 g8_8 g9_8 + 3 g9_8^2)^2

a perfect square in three variables, and the next three conditions are that
same factor times something else -- so ONE forced substitution clears four
conditions at once.  Ranking pivots by term count, as the earlier attempts did,
walks straight past this.

Order of work, and nothing weaker is used while something stronger exists:
  1. iterate the perfect-power rule to a fixed point   (unconditional)
  2. rational-coefficient linear pivots, growth-free   (unconditional)
  3. rational-coefficient linear pivots                (unconditional)
  4. report what is left, WITHOUT branching
Reducible-but-not-a-power conditions are NOT resolved here: each is a union of
components and choosing one costs generality.  They are listed instead.
"""
import sympy as sp, pickle, sys, time, os
conds, sub = pickle.load(open('endgame.pkl','rb'))
conds = [sp.expand(c) for c in conds]
def freev(C): return sorted(set().union(*[c.free_symbols for c in C]), key=str) if C else []
def nterms(e): return len(e.args) if e.is_Add else 1
def prim(c):
    vs = freev([c])
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
        p = prim(c); s = sp.srepr(p)
        if s in seen: continue
        seen.add(s); out.append(p)
    return out

elim, order, notes = {}, [], []
conds = reduce_all(conds)
print(f"start: {len(conds)} conditions, {len(freev(conds))} parameters", flush=True)

def apply_sub(x, val, tag):
    global conds
    elim[x] = val; order.append((tag, str(x)))
    conds = reduce_all([sp.expand(e.subs(x, val)) if x in e.free_symbols else e
                        for e in conds])
    print(f"  [{tag}] {x} = {sp.factor(val)}  -> {len(conds)} conditions, "
          f"{len(freev(conds))} parameters", flush=True)

for rnd in range(60):
    # ---- 1. perfect powers, unconditional ----
    hit = False
    for c in list(conds):
        fl = [(b, e) for b, e in sp.factor_list(c)[1] if b.free_symbols]
        if len(fl) != 1: continue
        u = fl[0][0]
        # solve u = 0 for a variable occurring linearly with rational coefficient
        for x in sorted(u.free_symbols, key=str):
            P = sp.Poly(u, x)
            if P.degree() == 1 and P.coeff_monomial(x).is_number and P.coeff_monomial(x) != 0:
                val = sp.cancel(-P.coeff_monomial(1)/P.coeff_monomial(x))
                print(f"round {rnd}: PERFECT POWER {sp.factor(c)}", flush=True)
                apply_sub(x, val, "POWER"); hit = True; break
        if hit: break
        if not hit and u not in [e for e in conds]:
            notes.append(f"power factor with no rational-linear variable: {u}")
    if hit: continue
    if not conds:
        print("\n*** ALL CONDITIONS SATISFIED ***", flush=True); break
    # ---- 2/3. rational-coefficient linear pivots, unconditional ----
    V = freev(conds)
    P_of = {}
    for c in conds:
        vs = freev([c]); P_of[c] = (sp.Poly(c, *vs), vs)
    maxdeg = {v: 0 for v in V}
    for c, (P, vs) in P_of.items():
        for j, v in enumerate(vs):
            d = max(m[j] for m in P.monoms())
            if d > maxdeg[v]: maxdeg[v] = d
    cands = []
    for c in conds:
        P, vs = P_of[c]
        for j, x in enumerate(vs):
            if max(m[j] for m in P.monoms()) != 1: continue
            c1 = sp.Poly(c, x).coeff_monomial(x)
            if not (c1.is_number and c1 != 0): continue
            cands.append(((1 if maxdeg[x] == 1 else 2), nterms(c), str(x), c, x, c1))
    if not cands: break
    cands.sort(key=lambda t: (t[0], t[1], t[2]))
    tier, _n, _s, c, x, c1 = cands[0]
    val = sp.cancel(-sp.Poly(c, x).coeff_monomial(1)/c1)
    apply_sub(x, val, f"LIN{tier}")

print(f"\n=== after {len(elim)} UNCONDITIONAL eliminations: {order}")
print(f"remaining: {len(conds)} conditions in {len(freev(conds))} parameters "
      f"{[str(v) for v in freev(conds)]}")
red = 0
for c in sorted(conds, key=nterms):
    fl = [b for b, e in sp.factor_list(c)[1] if b.free_symbols]
    mark = f"  <-- REDUCIBLE, {len(fl)} components" if len(fl) > 1 else ""
    if len(fl) > 1: red += 1
    print(f"  [{nterms(c):4d} terms] {str(sp.factor(c))[:170]}{mark}")
print(f"\n{red} of {len(conds)} remaining conditions are reducible (each a branch).")
pickle.dump((conds, elim, sub, order), open('endgame_uncond.pkl','wb'))
