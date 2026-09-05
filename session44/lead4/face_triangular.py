#!/usr/bin/env python3
"""Recover face solutions by ITERATED ELIMINATION -- no RUR convention needed.

Parsing msolve's rational univariate representation proved unreliable (no
denominator/sign combination reproduced a solution). This avoids it: at each
stage msolve is asked only for the ELIMINANT of the last remaining variable,
which is unambiguous. Its roots are found by scanning GF(p); one is fixed,
substituted, and the process repeats on the smaller system.

Every recovered tuple is then CHECKED against the face equation
W(u) = f g + 2u f g' - 3u f' g = 1, so a wrong turn cannot pass silently.
"""
import ast, json, subprocess, sys
import sympy as sp

P = 32003
u = sp.Symbol("u"); m, n = 7, 10
a = sp.symbols(f"a0:{m+1}"); b = sp.symbols(f"b0:{n+1}")
f_ = sum(a[i]*u**i for i in range(m+1)); g_ = sum(b[j]*u**j for j in range(n+1))
W = sp.expand(f_*g_ + 2*u*f_*sp.diff(g_,u) - 3*u*sp.diff(f_,u)*g_)
base = {a[0]:1, a[m]:1, b[0]:1}
bsol = {}
for N in range(1, m+n+1):
    e = sp.expand(W.coeff(u,N).subs(base).subs(bsol))
    if e == 0: continue
    nb = [v for v in e.free_symbols if str(v).startswith("b") and v not in bsol]
    if len(nb)==1 and sp.degree(e,nb[0])==1:
        v = nb[0]; c1 = sp.expand(sp.Poly(e,v).coeff_monomial(v))
        bsol[v] = sp.cancel(-(e-c1*v)/c1)
rem0 = []
for N in range(1, m+n+1):
    e = sp.expand(sp.numer(sp.together(sp.expand(
        W.coeff(u,N).subs(base).subs(bsol)))))
    if e != 0: rem0.append(e)

def eliminant(eqs, vs, tag):
    out = []
    for gg in eqs:
        pe = sp.Poly(gg, *vs, domain="QQ")
        L = 1
        for c in pe.coeffs(): L = sp.ilcm(L, sp.Rational(c).q)
        out.append(str(sp.expand(gg*L)).replace("**","^").replace(" ",""))
    fn = f"tri_{tag}.ms"
    open(fn,"w").write(",".join(str(v) for v in vs)+f"\n{P}\n"+",\n".join(out)+"\n")
    r = subprocess.run(["msolve","-f",fn], capture_output=True, text=True,
                       timeout=900)
    s = (r.stdout or "").strip().rstrip(":").replace("[","(").replace("]",")")
    if s.startswith("(-1"): return None
    R = ast.literal_eval(s)
    try: return list(R[1][5][1][0][1])
    except Exception: return None

def roots(co):
    def ev(T):
        v = 0
        for c in reversed(co): v = (v*T + c) % P
        return v
    return [T for T in range(P) if ev(T) == 0]

eqs = list(rem0)
vs = sorted({s for e in eqs for s in e.free_symbols}, key=str)
assign = {}
print(f"start: {len(eqs)} equations, variables {[str(v) for v in vs]}")
for depth in range(len(vs)):
    cur = [v for v in vs if v not in assign]
    if not cur: break
    ec = eliminant(eqs, cur, f"d{depth}")
    if ec is None:
        print(f"  depth {depth}: system EMPTY over GF({P}) -- no solution"); break
    rr = roots(ec)
    print(f"  depth {depth}: eliminating {cur[-1]}, eliminant degree "
          f"{len(ec)-1}, {len(rr)} rational roots")
    if not rr:
        print(f"    no rational root for {cur[-1]} at this prime; stopping")
        break
    assign[cur[-1]] = rr[0]
    eqs = [sp.expand(e.subs({cur[-1]: rr[0]})) for e in eqs]
    eqs = [e for e in eqs if e != 0]
    if not eqs:
        print("    all equations satisfied"); break
print(f"\nassigned: { {str(k): v for k,v in assign.items()} }")
if len(assign) == len(vs):
    sub = dict(base)
    for k,v in assign.items(): sub[k] = v
    full = dict(sub)
    for bv, expr in bsol.items():
        full[bv] = int(sp.expand(expr.subs(full))) % P
    Wv = sp.expand(W.subs(full))
    res = [(int(sp.expand(Wv.coeff(u,N))) - (1 if N==0 else 0)) % P
           for N in range(m+n+1)]
    ok = all(z == 0 for z in res)
    print(f"VERIFICATION against W(u) = 1: {'PASS' if ok else 'FAIL ' + str(res[:6])}")
    if ok:
        json.dump({str(k): int(v) for k,v in full.items()},
                  open("face_solution_verified.json","w"), indent=1)
        print("wrote face_solution_verified.json -- a TRUE face solution")
