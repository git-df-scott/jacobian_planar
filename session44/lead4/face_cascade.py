#!/usr/bin/env python3
"""THE DECISIVE TEST: do genuine face solutions extend to a full (P,Q)?

At p = 32003 the essential-face eliminant has rational roots, so true face
solutions are available in GF(p). For each:
  1. recover a1..a6 from the RUR, then b1..b10 by triangular elimination;
  2. VERIFY it satisfies W(u) = f g + 2u f g' - 3u f' g = 1 exactly;
  3. place f,g as the deepest weight levels of P and Q;
  4. run the linear cascade w = -3, -2, -1 and the w = 0 consistency check.

Outcome:
  every face solution fails  -> mod-p evidence the subcase does not extend
  one succeeds               -> explicit candidate (P,Q) mod p, to be
                                lifted to characteristic zero and verified
                                exactly before ANY claim of a counterexample
"""
import ast, json, subprocess, sys
import sympy as sp
from face_param import lattice_points

P = 32003
u = sp.Symbol("u"); x, y = sp.symbols("x y")
m, n = 7, 10


def rur(fn):
    r = subprocess.run(["msolve","-f",fn], capture_output=True, text=True,
                       timeout=1200)
    s = (r.stdout or "").strip().rstrip(":").replace("[","(").replace("]",")")
    return ast.literal_eval(s)


def ev(co, T, mod):
    v = 0
    for c in reversed(co): v = (v*T + c) % mod
    return v


# --- rebuild the face system symbolically (same as face_primes) ---
a = sp.symbols(f"a0:{m+1}"); b = sp.symbols(f"b0:{n+1}")
f = sum(a[i]*u**i for i in range(m+1)); g = sum(b[j]*u**j for j in range(n+1))
W = sp.expand(f*g + 2*u*f*sp.diff(g,u) - 3*u*sp.diff(f,u)*g)
base = {a[0]:1, a[m]:1, b[0]:1}
bsol = {}
for N in range(1, m+n+1):
    e = sp.expand(W.coeff(u,N).subs(base).subs(bsol))
    if e == 0: continue
    nb = [v for v in e.free_symbols if str(v).startswith("b") and v not in bsol]
    if len(nb)==1 and sp.degree(e,nb[0])==1:
        v = nb[0]; c1 = sp.expand(sp.Poly(e,v).coeff_monomial(v))
        bsol[v] = sp.cancel(-(e-c1*v)/c1)

R = rur(f"fp_{P}.ms")
body = R[1]; names = list(body[3]); blk = body[5][1]
elim, den, nums = blk[0], blk[1], blk[2]
ec = list(elim[1])
roots = [T for T in range(P) if ev(ec, T, P) == 0]
print(f"prime {P}: {len(roots)} rational face solutions, roots {roots}")
# den is (deg, coeffs) with coeffs possibly a bare int
_d = den[1] if isinstance(den, tuple) else den
dc = list(_d) if isinstance(_d, (tuple, list)) else [_d]

sols = []
for T in roots:
    dv = ev(dc, T, P) if dc else 1
    if dv % P == 0: continue
    inv = pow(dv, P-2, P)
    vals = {}
    for k, nm in enumerate(names):
        nk = nums[k]
        # each numerator is ((deg, (coeffs)),) or (deg, (coeffs))
        ent = nk[0] if (isinstance(nk, tuple) and isinstance(nk[0], tuple)) else nk
        co = list(ent[1])
        vals[nm] = (ev(co, T, P) * inv) % P
    valsneg = {k: (-v) % P for k, v in vals.items()}
    sols.append((T, vals)); sols.append((T, valsneg))
    print(f"  root {T}: " + ", ".join(f"{k}={v}" for k,v in vals.items()))

print("\nverifying each against W(u) = 1 ...")
good = []
for T, vals in sols:
    sub = {a[0]:1, a[m]:1, b[0]:1}
    for k, v in vals.items(): sub[sp.Symbol(k)] = v
    bfull = dict(sub)
    for bv, expr in bsol.items():
        bfull[bv] = int(sp.expand(expr.subs(bfull))) % P
    Wv = sp.expand(W.subs(bfull))
    res = [int(sp.expand(Wv.coeff(u,N))) % P - (1 if N==0 else 0)
           for N in range(m+n+1)]
    okv = all(rr % P == 0 for rr in res)
    print(f"  root {T}: W(u) == 1 mod {P}?  {'YES' if okv else 'NO ' + str(res[:5])}")
    if okv: good.append((T, bfull))
json.dump({"prime": P, "roots": roots, "verified": len(good)},
          open("face_cascade_status.json","w"))
print(f"\n{len(good)} verified face solutions ready for the cascade.")
