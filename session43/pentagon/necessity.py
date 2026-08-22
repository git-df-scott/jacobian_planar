#!/usr/bin/env python3
"""Are the descent's conditions NECESSARY, or artifacts of solve ordering?

Two separate questions, answered separately.

1. Does solving a level ever SPECIALISE a surviving parameter?
   No -- and this is checkable.  sp.solve on a consistent underdetermined
   linear system returns the general solution, leaving the kernel directions as
   free symbols.  The check that certifies it: after substituting the solution
   back, the level residual must be identically zero AS A POLYNOMIAL, i.e. zero
   for EVERY value of every remaining free symbol.  That is asserted at every
   level.  If solving had quietly specialised something, the residual would
   vanish only on a subvariety and would not be the zero polynomial.

2. Is each imposed gate necessary?
   The gates are n . v for n in the LEFT NULLSPACE of the level's coefficient
   matrix M.  That space, and hence the ideal the gates generate, does not
   depend on how the level is solved -- only the printed generators do.  So the
   IDEAL is canonical.  What is not canonical is which COMPONENT of it we
   follow.  This script classifies each gate:

       linear in one variable      -> that value is NECESSARY
       pure power of one variable  -> that variable = 0 is NECESSARY
       a product / reducible       -> BRANCH CHOICE, with its component count

   Only the third kind costs generality, and those are the ones to report.
"""
import sympy as sp, sys
exec(open('endgame.py').read().split("for L in range(19, 7, -1)")[0])

report = []
for L in range(19, 7, -1):
    st, eqs, cs, info = analyse(L)
    rnd = 0
    while st == 'gate':
        rnd += 1
        for c_ in cs:
            f = sp.factor(c_)
            fs = sorted(c_.free_symbols, key=str)
            lin = [x for x in fs if sp.degree(sp.Poly(c_, x), x) == 1]
            if len(fs) == 1:
                kind = f"PURE POWER of {fs[0]} -> {fs[0]} = 0 NECESSARY"
            elif lin:
                kind = f"linear in {lin[0]} -> value NECESSARY"
            else:
                kind = "no variable occurs linearly"
            fac = sp.factor_list(c_)[1]
            nontriv = [b for b, e in fac if b.free_symbols]
            if len(nontriv) > 1:
                kind = (f"REDUCIBLE, {len(nontriv)} factors -> BRANCH CHOICE: "
                        + " | ".join(f"({b} = 0)" for b in nontriv))
            report.append((L, rnd, str(f)[:110], kind))
        cv = sorted(set().union(*[c_.free_symbols for c_ in cs]), key=str)
        linv = [x for x in cv if all(sp.degree(sp.Poly(c_, x), x) <= 1 for c_ in cs)]
        sol = sp.solve(cs, linv or cv, dict=True)
        assert sol
        sub.update({k: sp.cancel(sp.expand(v)) for k, v in sol[0].items()}); norm()
        st, eqs, cs, info = analyse(L)
    assert st == 'ok', (L, st)
    new = [u for u in newsyms(L) if u not in sub]
    sol = sp.solve(eqs, new, dict=True)[0]
    # question 1: did the solve specialise anything that was already free?
    assigned = set(sol)
    assert assigned <= set(new), f"L={L} solve assigned a NON-new symbol: {assigned - set(new)}"
    assert len(assigned) == info[2], (f"L={L} assigned {len(assigned)} symbols but rank is "
                                      f"{info[2]} -- a free direction was specialised")
    sub.update({k: sp.cancel(sp.expand(vv)) for k, vv in sol.items()}); norm()
    r = res(lev(L))
    assert r == 0, f"L={L} residual not the ZERO POLYNOMIAL"
    print(f"L={L:3d}: solve assigned exactly rank={info[2]} of the {info[1]} new symbols, "
          f"{info[1]-info[2]} left free; residual is the zero polynomial", flush=True)

print("\n=== GATE CLASSIFICATION ===")
nb = 0
for L, rnd, f, kind in report:
    print(f"L={L:3d} r{rnd}: {f}\n        {kind}")
    if kind.startswith("REDUCIBLE"): nb += 1
print(f"\n{len(report)} gates total, {nb} of them REDUCIBLE (branch choices); "
      f"the other {len(report)-nb} are necessary.")
