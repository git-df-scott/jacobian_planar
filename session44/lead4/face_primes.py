#!/usr/bin/env python3
"""Find a prime where the essential-face eliminant has rational roots.

The face system has 35 solutions over the algebraic closure. Over GF(p) the
degree-35 eliminant has rational roots for roughly 1 - 1/e of primes; at
p = 65521 it happened to have none. Scan a few primes to find one whose
roots are rational, so the cascade can be run on TRUE face solutions.
"""
import ast, subprocess, sys
import sympy as sp

u = sp.Symbol("u"); m, n = 7, 10
a = sp.symbols(f"a0:{m+1}"); b = sp.symbols(f"b0:{n+1}")
f = sum(a[i]*u**i for i in range(m+1)); g = sum(b[j]*u**j for j in range(n+1))
W = sp.expand(f*g + 2*u*f*sp.diff(g,u) - 3*u*sp.diff(f,u)*g)
base = {a[0]:1, a[m]:1, b[0]:1}
sol = {}
for N in range(1, m+n+1):
    e = sp.expand(W.coeff(u,N).subs(base).subs(sol))
    if e == 0: continue
    nb = [v for v in e.free_symbols if str(v).startswith("b") and v not in sol]
    if len(nb)==1 and sp.degree(e,nb[0])==1:
        v = nb[0]; c1 = sp.expand(sp.Poly(e,v).coeff_monomial(v))
        sol[v] = sp.cancel(-(e-c1*v)/c1)
rem = []
for N in range(1, m+n+1):
    e = sp.expand(sp.numer(sp.together(sp.expand(
        W.coeff(u,N).subs(base).subs(sol)))))
    if e != 0: rem.append(e)
free = sorted({s for r in rem for s in r.free_symbols}, key=str)

def run(P):
    out = []
    for gg in rem:
        pe = sp.Poly(gg, *free, domain="QQ")
        L = 1
        for c in pe.coeffs(): L = sp.ilcm(L, sp.Rational(c).q)
        out.append(str(sp.expand(gg*L)).replace("**","^").replace(" ",""))
    fn = f"fp_{P}.ms"
    open(fn,"w").write(",".join(str(v) for v in free)+f"\n{P}\n"
                       + ",\n".join(out)+"\n")
    r = subprocess.run(["msolve","-f",fn], capture_output=True, text=True,
                       timeout=900)
    s = (r.stdout or "").strip().rstrip(":").replace("[","(").replace("]",")")
    try: R = ast.literal_eval(s)
    except Exception: return None, "parse fail"
    if not isinstance(R, tuple) or R[0] != 0: return None, str(R)[:40]
    body = R[1]; elim = body[5][1][0]; ec = list(elim[1])
    def ev(T):
        v = 0
        for c in reversed(ec): v = (v*T + c) % P
        return v
    roots = [T for T in range(P) if ev(T)==0]
    return roots, f"eliminant deg {elim[0]}"

for P in (32003, 65537, 101, 1009, 7919, 15013):
    try:
        roots, msg = run(P)
    except Exception as e:
        print(f"  p={P}: error {e}"); continue
    if roots is None:
        print(f"  p={P}: {msg}")
    else:
        print(f"  p={P}: {msg}, {len(roots)} rational roots"
              f"{' -> '+str(roots[:5]) if roots else ''}", flush=True)
        if roots:
            print(f"  *** usable prime found: {P} ***"); break
