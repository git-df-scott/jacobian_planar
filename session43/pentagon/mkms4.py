#!/usr/bin/env python3
"""The complementary chart g9_8 != 0, done EXACTLY by saturation.

"g9_8 != 0" is an open condition, so the variety in question is
V(I) \\ V(g9_8), whose Zariski closure is cut out by the saturation
I : g9_8^infinity.  Testing I itself would be wrong -- I certainly has points
with g9_8 = 0 and they are not in this chart.

Rabinowitsch: adjoin a variable t and the equation g9_8*t - 1.  Then the
extended ideal is the unit ideal exactly when the saturation is, so a basis of
[1] means there is NO point with g9_8 != 0.  Dividing the explicit g9_8 factors
out of the 47 conditions that carry them first is legitimate for the same
reason and keeps the degrees down.

A16 discipline as before: integer coefficients, no parentheses, asserted; and a
planted positive control emitted in the same format.
"""
import sympy as sp, pickle
conds, elim, sub, order = pickle.load(open('endgame_uncond.pkl','rb'))
g98 = sp.Symbol('g9_8'); t = sp.Symbol('t')
cof, ndiv = [], 0
for c in conds:
    c = sp.expand(c)
    k = 0
    while True:
        q, r = sp.div(c, g98, g98)
        if sp.expand(r) != 0: break
        c = sp.expand(q); k += 1
    if k: ndiv += 1
    cof.append(c)
print(f"divided g9_8 out of {ndiv} of {len(conds)} conditions")
polys = cof + [sp.expand(g98*t - 1)]
V = sorted(set().union(*[p.free_symbols for p in polys]), key=str)
print(f"{len(polys)} polys in {len(V)} vars: {[str(v) for v in V]}")
def ms_poly(c):
    P = sp.Poly(c, *V).primitive()[1]
    assert all(co.is_Integer for co in P.coeffs())
    out = ""
    for mon, co in sorted(P.terms(), reverse=True):
        parts = [str(abs(co))] if abs(co) != 1 or all(e == 0 for e in mon) else []
        for v, e in zip(V, mon):
            if e == 1: parts.append(str(v))
            elif e > 1: parts.append(f"{v}^{e}")
        out += ("-" if co < 0 else ("+" if out else "")) + "*".join(parts)
    return out
def emit(path, ps, char):
    txt = ",".join(map(str, V)) + f"\n{char}\n" + ",\n".join(ms_poly(p) for p in ps) + "\n"
    assert "(" not in txt and ")" not in txt, "PARENTHESIS -- A16"
    open(path, 'w').write(txt); print(f"{path}: {len(ps)} polys, {len(txt)} bytes")
emit('sat_p.ms', polys, 1073741827)
emit('sat.ms', polys, 0)
# planted control: shift so that (0,...,0,g9_8=1,t=1) is a solution
pt = {v: sp.Integer(0) for v in V}; pt[g98] = sp.Integer(1); pt[t] = sp.Integer(1)
planted = [sp.expand(p - p.subs(pt)) for p in polys]
assert all(sp.expand(p.subs(pt)) == 0 for p in planted), "planting failed"
emit('sat_planted_p.ms', planted, 1073741827)
