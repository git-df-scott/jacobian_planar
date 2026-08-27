#!/usr/bin/env python3
"""Scan primes for a FULLY RATIONAL essential-face solution.

The 35 face solutions are Galois-conjugate; over a given GF(p) the
eliminant may have rational roots whose remaining coordinates still lie in
an extension (observed at p = 32003). This scans primes, doing the full
iterated-elimination descent at each, and stops at the first prime where a
complete rational solution exists -- which is what the cascade needs.
"""
import ast, json, subprocess, sys
import sympy as sp

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
REM = []
for N in range(1, m+n+1):
    e = sp.expand(sp.numer(sp.together(sp.expand(
        W.coeff(u,N).subs(base).subs(bsol)))))
    if e != 0: REM.append(e)

def elim(eqs, vs, P, tag):
    out = []
    for gg in eqs:
        pe = sp.Poly(gg, *vs, domain="QQ")
        L = 1
        for c in pe.coeffs(): L = sp.ilcm(L, sp.Rational(c).q)
        out.append(str(sp.expand(gg*L)).replace("**","^").replace(" ",""))
    fn = f"sc_{P}_{tag}.ms"
    open(fn,"w").write(",".join(str(v) for v in vs)+f"\n{P}\n"+",\n".join(out)+"\n")
    try:
        r = subprocess.run(["msolve","-f",fn], capture_output=True, text=True,
                           timeout=400)
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    s = (r.stdout or "").strip().rstrip(":").replace("[","(").replace("]",")")
    if s.startswith("(-1"): return None
    try: return list(ast.literal_eval(s)[1][5][1][0][1])
    except Exception: return "PARSE"

def descend(P):
    eqs = list(REM)
    vs = sorted({s for e in eqs for s in e.free_symbols}, key=str)
    assign = {}
    for d in range(len(vs)):
        cur = [v for v in vs if v not in assign]
        if not cur: break
        ec = elim(eqs, cur, P, f"d{d}")
        if ec in (None, "TIMEOUT", "PARSE"): return None, assign, str(ec)
        def evp(T):
            v = 0
            for c in reversed(ec): v = (v*T+c) % P
            return v
        rr = [T for T in range(P) if evp(T)==0]
        if not rr: return None, assign, f"no rational root at depth {d}"
        ok = False
        for T in rr:
            e2 = [sp.expand(e.subs({cur[-1]: T})) for e in eqs]
            e2 = [e for e in e2 if e != 0]
            assign[cur[-1]] = T; eqs = e2; ok = True; break
        if not ok: return None, assign, "no usable root"
        if not eqs: break
    return (assign if len(assign)==len(vs) or not eqs else None), assign, "ok"

for P in (32003, 1009, 7919, 15013, 65537, 40009, 50021, 3001):
    got, assign, msg = descend(P)
    tag = "COMPLETE" if got else f"incomplete ({msg})"
    print(f"  p={P:6d}: {tag}, assigned {len(assign)}", flush=True)
    if got:
        print(f"    *** fully rational face solution at p={P}: "
              f"{ {str(k):v for k,v in assign.items()} } ***")
        json.dump({"prime": P, "sol": {str(k): int(v) for k,v in assign.items()}},
                  open("face_rational.json","w"), indent=1)
        break
