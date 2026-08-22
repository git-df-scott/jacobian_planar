#!/usr/bin/env python3
"""Emit the endgame for msolve after the two UNCONDITIONAL eliminations.

g1_1 and g2_2 have max degree 1 across all 59 conditions and occur with a
nonzero RATIONAL coefficient, so eliminating them
  * costs no generality (no branch, no nonzero assumption), and
  * cannot grow the system (degree 1 everywhere means no c0^k is ever formed).
Nothing else is touched -- in particular none of the polynomial-coefficient
pivots, which would each impose a nonzero assumption and change the variety.
A16 discipline as in mkms.py: integer coefficients, no parentheses, asserted.
"""
import sympy as sp, pickle
conds, sub = pickle.load(open('endgame.pkl','rb'))
conds = [sp.expand(c) for c in conds]
def freev(C): return sorted(set().union(*[c.free_symbols for c in C]), key=str)
def prim(c):
    vs = freev([c])
    P = sp.Poly(c, *vs).primitive()[1]
    return P.as_expr() if P.LC() > 0 else (-P).as_expr()
for name in ('g1_1', 'g2_2'):
    x = sp.Symbol(name)
    V = freev(conds)
    md = max((sp.Poly(c, x).degree() for c in conds if x in c.free_symbols), default=0)
    piv = None
    for c in conds:
        if x not in c.free_symbols: continue
        P = sp.Poly(c, x)
        if P.degree() == 1 and P.coeff_monomial(x).is_number and P.coeff_monomial(x) != 0:
            piv = c; break
    assert md == 1, f"{name} has max degree {md}, elimination is NOT growth-free"
    assert piv is not None, f"no rational-coefficient linear pivot for {name}"
    out = []
    for e in conds:
        if e is piv: continue
        r = sp.expand(sp.prem(e, piv, x)) if x in e.free_symbols else e
        if r != 0: out.append(prim(r))
    seen, uniq = set(), []
    for c in out:
        s = sp.srepr(c)
        if s not in seen: seen.add(s); uniq.append(c)
    conds = uniq
    print(f"eliminated {name} (unconditional): {len(conds)} conditions, "
          f"{len(freev(conds))} parameters")
V = freev(conds)
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
for char, path in ((0, 'endgame2.ms'), (1073741827, 'endgame2_p.ms')):
    txt = ",".join(map(str, V)) + f"\n{char}\n" + ",\n".join(ms_poly(c) for c in conds) + "\n"
    assert "(" not in txt and ")" not in txt, "PARENTHESIS -- A16"
    open(path, 'w').write(txt)
    print(f"{path}: {len(conds)} polys, {len(V)} vars, {len(txt)} bytes")
