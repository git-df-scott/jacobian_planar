#!/usr/bin/env python3
"""Controls for the g9_8 = 0 msolve run.

PLANTED POSITIVE CONTROL: replace every polynomial f by f - f(0).  The origin
is then a solution of every one, so the ideal is proper and the basis MUST NOT
be [1].  This uses the SAME emitter, the same 39 polynomials, the same 15
variables and the same file size, so if the pipeline had a parse fault (A16:
msolve silently mis-parses parentheses and reports [1] in zero seconds with
exit 0) this control would report [1] too and expose it.

Also emits the true system at a SECOND prime, because EMPTY mod one prime does
not imply EMPTY over Q -- a bad prime can produce a false EMPTY.
"""
import sympy as sp, pickle
conds, elim, sub, order = pickle.load(open('uncond_g98zero.pkl','rb'))
conds = [sp.expand(c) for c in conds]
V = sorted(set().union(*[c.free_symbols for c in conds]), key=str)
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
def emit(path, polys, char):
    txt = ",".join(map(str, V)) + f"\n{char}\n" + ",\n".join(ms_poly(c) for c in polys) + "\n"
    assert "(" not in txt and ")" not in txt, "PARENTHESIS -- A16"
    open(path, 'w').write(txt); print(f"{path}: {len(polys)} polys, {len(txt)} bytes")
zero = {v: 0 for v in V}
planted = [sp.expand(c - c.subs(zero)) for c in conds]
assert all(sp.expand(p.subs(zero)) == 0 for p in planted), "planting failed"
emit('g98zero_planted_p.ms', planted, 1073741827)
emit('g98zero_p2.ms', conds, 2147483587)
