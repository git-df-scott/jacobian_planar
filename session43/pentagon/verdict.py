#!/usr/bin/env python3
"""Emit one component for msolve and state its verdict, with controls.

usage: verdict.py <pkl> <tag> [saturate]

<pkl> holds (conds, ...) -- either a raw component from component.py or one
reduced by solve4.py.  If 'saturate' is passed, the chart carries g9_8 != 0, so
the honest object is the SATURATION I : g9_8^inf, obtained by dividing the
explicit g9_8 factors out and adjoining the Rabinowitsch equation g9_8*t - 1.
Testing I itself would be wrong: I has points with g9_8 = 0 and those are not
in this chart.

Always emits a PLANTED positive control in the same format and size: shift each
polynomial by its value at a chosen point so that point becomes a solution, so
the basis must NOT be [1].  That is what distinguishes a real emptiness from
erratum A16 (msolve silently mis-parses parentheses and reports [1]).
"""
import sympy as sp, pickle, sys
src, tag = sys.argv[1], sys.argv[2]
sat = len(sys.argv) > 3 and sys.argv[3] == 'saturate'
data = pickle.load(open(src, 'rb'))
conds = [sp.expand(c) for c in data[0]]
g98, t = sp.Symbol('g9_8'), sp.Symbol('t')
if sat:
    out, nd = [], 0
    for c in conds:
        k = 0
        while True:
            q, r = sp.div(c, g98, g98)
            if sp.expand(r) != 0: break
            c = sp.expand(q); k += 1
        nd += 1 if k else 0
        out.append(c)
    conds = out + [sp.expand(g98*t - 1)]
    print(f"saturated: divided g9_8 out of {nd} conditions, adjoined g9_8*t-1")
V = sorted(set().union(*[c.free_symbols for c in conds]), key=str)
print(f"{tag}: {len(conds)} polys, {len(V)} vars")
def ms_poly(c):
    P = sp.Poly(c, *V).primitive()[1]
    assert all(co.is_Integer for co in P.coeffs())
    o = ""
    for mon, co in sorted(P.terms(), reverse=True):
        parts = [str(abs(co))] if abs(co) != 1 or all(e == 0 for e in mon) else []
        for v, e in zip(V, mon):
            if e == 1: parts.append(str(v))
            elif e > 1: parts.append(f"{v}^{e}")
        o += ("-" if co < 0 else ("+" if o else "")) + "*".join(parts)
    return o
def emit(path, ps, char):
    txt = ",".join(map(str, V)) + f"\n{char}\n" + ",\n".join(ms_poly(p) for p in ps) + "\n"
    assert "(" not in txt and ")" not in txt, "PARENTHESIS -- A16"
    open(path, 'w').write(txt); print(f"  {path}: {len(txt)} bytes")
emit(f'{tag}.ms', conds, 0)
emit(f'{tag}_p.ms', conds, 1073741827)
pt = {v: sp.Integer(0) for v in V}
if sat: pt[g98] = sp.Integer(1); pt[t] = sp.Integer(1)
planted = [sp.expand(c - c.subs(pt)) for c in conds]
assert all(sp.expand(p.subs(pt)) == 0 for p in planted), "planting failed"
emit(f'{tag}_planted_p.ms', planted, 1073741827)
