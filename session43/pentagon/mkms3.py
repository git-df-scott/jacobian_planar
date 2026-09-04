#!/usr/bin/env python3
"""Emit the g9_8 = 0 chart's endgame (39 conditions, 15 parameters) for msolve.

A16 discipline enforced, not trusted: integer coefficients, fully expanded,
and the emitted text is ASSERTED to contain no parenthesis -- msolve silently
mis-parses parentheses and reports the basis [1], a FALSE EMPTY, in zero
seconds with exit 0 and no warning.
"""
import sympy as sp, pickle, sys
conds, elim, sub, order = pickle.load(open('uncond_g98zero.pkl','rb'))
conds = [sp.expand(c) for c in conds]
V = sorted(set().union(*[c.free_symbols for c in conds]), key=str)
def ms_poly(c):
    P = sp.Poly(c, *V).primitive()[1]
    assert all(co.is_Integer for co in P.coeffs()), "non-integer coefficient"
    out = ""
    for mon, co in sorted(P.terms(), reverse=True):
        parts = [str(abs(co))] if abs(co) != 1 or all(e == 0 for e in mon) else []
        for v, e in zip(V, mon):
            if e == 1: parts.append(str(v))
            elif e > 1: parts.append(f"{v}^{e}")
        out += ("-" if co < 0 else ("+" if out else "")) + "*".join(parts)
    return out
for char, path in ((0, 'g98zero.ms'), (1073741827, 'g98zero_p.ms')):
    txt = ",".join(map(str, V)) + f"\n{char}\n" + ",\n".join(ms_poly(c) for c in conds) + "\n"
    assert "(" not in txt and ")" not in txt, "PARENTHESIS IN MSOLVE INPUT -- A16"
    open(path, 'w').write(txt)
    print(f"{path}: {len(conds)} polys, {len(V)} vars, {len(txt)} bytes")
print("vars:", ", ".join(map(str, V)))
print("max total degree:", max(sp.Poly(c, *V).total_degree() for c in conds))
