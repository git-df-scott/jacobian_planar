#!/usr/bin/env python3
"""Solve the essential-face equation explicitly and emit the leading data.

W(u) = f g + 2u f g' - 3u f' g = 1,  deg f = 7, deg g = 10.
Gauges a0 = 1 (scaling of (f,g)) and a7 = 1 (scaling of u); then W_0 gives
b0 = 1. Triangular elimination expresses b1..b10 in terms of a1..a6,
leaving 6 equations of degree 9 in 6 unknowns. Those are solved here.

Any solution is the exact leading (face) data that a counterexample of
EITHER open (72,108) subcase must have -- both share this face.
"""
import subprocess, sys
import sympy as sp

u = sp.Symbol("u")
m, n = 7, 10
a = sp.symbols(f"a0:{m+1}"); b = sp.symbols(f"b0:{n+1}")
f = sum(a[i]*u**i for i in range(m+1)); g = sum(b[j]*u**j for j in range(n+1))
W = sp.expand(f*g + 2*u*f*sp.diff(g,u) - 3*u*sp.diff(f,u)*g)
base = {a[0]: 1, a[m]: 1, b[0]: 1}
sol = {}
for N in range(1, m+n+1):
    e = sp.expand(W.coeff(u,N).subs(base).subs(sol))
    if e == 0: continue
    nb = [v for v in e.free_symbols if str(v).startswith("b") and v not in sol]
    if len(nb) == 1 and sp.degree(e, nb[0]) == 1:
        v = nb[0]; c1 = sp.expand(sp.Poly(e,v).coeff_monomial(v))
        sol[v] = sp.cancel(-(e - c1*v)/c1)
rem = []
for N in range(1, m+n+1):
    e = sp.expand(W.coeff(u,N).subs(base).subs(sol))
    e = sp.expand(sp.numer(sp.together(e)))
    if e != 0: rem.append(e)
free = sorted({s for r in rem for s in r.free_symbols}, key=str)
print(f"{len(rem)} equations, degrees {[sp.total_degree(r) for r in rem]}")
print(f"unknowns: {[str(v) for v in free]}")

def export(char, fn, sat=None):
    gens = list(rem)
    vs = list(free)
    if sat is not None:
        s = sp.Symbol("s_sat"); gens.append(sp.expand(sat*s-1)); vs = vs+[s]
    out = []
    for gg in gens:
        pe = sp.Poly(gg, *vs, domain="QQ")
        L = 1
        for c in pe.coeffs(): L = sp.ilcm(L, sp.Rational(c).q)
        out.append(str(sp.expand(gg*L)).replace("**","^").replace(" ",""))
    open(fn,"w").write(",".join(str(v) for v in vs)+f"\n{char}\n"
                       + ",\n".join(out)+"\n")
    return fn

for char in (65521, 0):
    fn = export(char, f"facesolve_c{char}.ms")
    try:
        r = subprocess.run(["msolve","-f",fn], capture_output=True,
                           text=True, timeout=1500)
        o = (r.stdout or "").strip()
    except subprocess.TimeoutExpired:
        print(f"char {char}: TIMEOUT"); continue
    tag = ("EMPTY" if o.startswith("[-1]") else
           ("NONEMPTY" if o.startswith("[") else "NO-OUTPUT"))
    print(f"\nchar {char}: {tag}")
    print("  raw:", o[:400].replace("\n"," "))
