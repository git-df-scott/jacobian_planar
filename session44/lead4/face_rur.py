#!/usr/bin/env python3
"""Recover explicit face solutions from msolve's RUR and VERIFY them.

msolve RUR convention: with linear form T (here T = a6, the last variable),
the eliminant f(T) has the roots, and the remaining variables are
    a_i = +/- num_i(T) / f'(T).
The sign/denominator convention is not assumed here -- all variants are
tried and each candidate is CHECKED against the face equation
W(u) = f g + 2u f g' - 3u f' g = 1. Only verified solutions are kept.
"""
import ast, json, subprocess, sys
import sympy as sp

P = 32003
u = sp.Symbol("u"); m, n = 7, 10

def ev(co, T, mod):
    v = 0
    for c in reversed(co): v = (v*T + c) % mod
    return v

r = subprocess.run(["msolve","-f",f"fp_{P}.ms"], capture_output=True,
                   text=True, timeout=1200)
s = (r.stdout or "").strip().rstrip(":").replace("[","(").replace("]",")")
R = ast.literal_eval(s)
names = list(R[1][3]); blk = R[1][5][1]
ec = list(blk[0][1]); nums = blk[2]
print(f"eliminant degree {blk[0][0]}, {len(nums)} numerators for "
      f"{len(names)} variables -> last variable is the parameter T")
dcs = {"one": [1],
       "fprime": [(i*c) % P for i, c in enumerate(ec)][1:]}
roots = [T for T in range(P) if ev(ec, T, P) == 0]
print(f"rational roots: {roots}")

# face system symbolically (for verification)
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

verified = []
for T in roots:
    combos = [(dn, dcv, sg) for dn, dcv in dcs.items() for sg in (1,-1)]
    hit = False
    for dn, dcv, sign in combos:
        dv = ev(dcv, T, P)
        if dv % P == 0: continue
        inv = pow(dv, P-2, P)
        vals = {names[-1]: T % P}
        for k in range(len(nums)):
            co = list(nums[k][1])
            vals[names[k]] = (sign * ev(co, T, P) * inv) % P
        sub = dict(base)
        for k, v in vals.items(): sub[sp.Symbol(k)] = v
        full = dict(sub)
        ok = True
        for bv, expr in bsol.items():
            try: full[bv] = int(sp.expand(expr.subs(full))) % P
            except Exception: ok = False; break
        if not ok: continue
        Wv = sp.expand(W.subs(full))
        res = [(int(sp.expand(Wv.coeff(u,N))) - (1 if N==0 else 0)) % P
               for N in range(m+n+1)]
        if all(z == 0 for z in res):
            print(f"  root {T} (den {dn}, sign {sign:+d}): VERIFIED vs W(u)=1")
            hit = True
            verified.append({k: int(v) for k, v in full.items()
                             if not isinstance(v, sp.Expr) or v.is_number})
            break
    if not hit:
        print(f"  root {T}: no den/sign combination verified")
print(f"\n{len(verified)} face solutions VERIFIED mod {P}")
if verified:
    json.dump(verified, open("face_solutions.json","w"), indent=1,
              default=int)
    print("wrote face_solutions.json")
    v0 = verified[0]
    print("first solution (a-coefficients):",
          {k: v0[k] for k in sorted(v0) if k.startswith("a")})
