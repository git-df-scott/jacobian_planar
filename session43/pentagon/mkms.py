#!/usr/bin/env python3
"""Emit the 59-condition endgame as an msolve input file.

ERRATUM A16 DISCIPLINE, enforced here rather than trusted: msolve silently
MIS-PARSES parentheses and reports the basis [1] -- a FALSE EMPTY, in zero
seconds, exit 0, no warning.  Demonstrated previously with x*y-1, x+y giving a
2-element basis while (x)*(y)-1, x+y gives [1].  So:
  * every polynomial is fully expanded and cleared to INTEGER coefficients,
  * the emitted text is asserted to contain NO parenthesis at all,
  * and controls are run alongside the real system every time.
"""
import sympy as sp, pickle, sys
conds, sub = pickle.load(open('endgame.pkl','rb'))
conds = [sp.expand(c) for c in conds]
V = sorted(set().union(*[c.free_symbols for c in conds]), key=str)
def intpoly(c):
    P = sp.Poly(c, *V)
    P = P.primitive()[1]                      # clear rational denominators
    assert all(co.is_Integer for co in P.coeffs()), "non-integer coefficient"
    return P
def ms_term(mon, co):
    parts = [str(abs(co))] if abs(co) != 1 or all(e == 0 for e in mon) else []
    for v, e in zip(V, mon):
        if e == 1: parts.append(str(v))
        elif e > 1: parts.append(f"{v}^{e}")
    return "*".join(parts)
def ms_poly(c):
    P = intpoly(c)
    out = ""
    for mon, co in sorted(P.terms(), reverse=True):
        t = ms_term(mon, co)
        out += ("-" if co < 0 else ("+" if out else "")) + t
    return out
def emit(path, polys, varlist, char=0):
    body = ",\n".join(polys)
    txt = ",".join(str(v) for v in varlist) + f"\n{char}\n" + body + "\n"
    assert "(" not in txt and ")" not in txt, "PARENTHESIS IN MSOLVE INPUT -- A16"
    open(path, "w").write(txt)
    return txt
txt = emit("endgame.ms", [ms_poly(c) for c in conds], V)
print(f"endgame.ms: {len(conds)} polys, {len(V)} vars, {len(txt)} bytes, no parentheses")
# --- controls, emitted in the SAME way so a parser fault would show up ---
x, y = sp.symbols('x y')
emit("ctrl_empty.ms", ["x-1", "x-2"], [x, y])          # must give [1]
emit("ctrl_nonempty.ms", ["x*y-1", "x+y"], [x, y])     # must NOT give [1]
print("controls written: ctrl_empty.ms (expect [1]), ctrl_nonempty.ms (expect NOT [1])")
