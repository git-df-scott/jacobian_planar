#!/usr/bin/env python3
"""Iterated elimination, with msolve's LINEAR FORM checked at every step.

Bug found in face_scan.py: msolve returns the eliminant with respect to a
linear form of its own choosing, reported in the output. I had assumed it
was always the last variable, so after the first substitution I was
substituting roots of the wrong polynomial -- which is why the system
looked EMPTY at every prime.

Here the linear form is read and used. If it is a single variable the root
is substituted for that variable; if it is a genuine combination, that is
reported rather than guessed at.
"""
import ast, subprocess, sys
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

def solve_msolve(eqs, vs, P, tag):
    out = []
    for gg in eqs:
        pe = sp.Poly(gg, *vs, domain="QQ"); L = 1
        for c in pe.coeffs(): L = sp.ilcm(L, sp.Rational(c).q)
        out.append(str(sp.expand(gg*L)).replace("**","^").replace(" ",""))
    fn = f"fx_{P}_{tag}.ms"
    open(fn,"w").write(",".join(str(v) for v in vs)+f"\n{P}\n"+",\n".join(out)+"\n")
    try:
        r = subprocess.run(["msolve","-f",fn], capture_output=True, text=True,
                           timeout=400)
    except subprocess.TimeoutExpired:
        return None, None, "TIMEOUT"
    s = (r.stdout or "").strip().rstrip(":").replace("[","(").replace("]",")")
    if s.startswith("(-1"): return None, None, "EMPTY"
    try:
        R = ast.literal_eval(s); body = R[1]
        names = list(body[3]); lin = list(body[4]); ec = list(body[5][1][0][1])
        return (names, lin, ec), None, "ok"
    except Exception as ex:
        return None, None, f"parse {type(ex).__name__}"

P = int(sys.argv[1]) if len(sys.argv) > 1 else 32003
eqs = list(REM)
vs = sorted({s for e in eqs for s in e.free_symbols}, key=str)
assign = {}
print(f"prime {P}: iterated elimination with the linear form CHECKED\n")
for d in range(len(vs)):
    cur = [v for v in vs if v not in assign]
    if not cur:
        print("  all variables assigned"); break
    got, _, msg = solve_msolve(eqs, cur, P, f"d{d}")
    if got is None:
        print(f"  depth {d}: {msg}"); break
    names, lin, ec = got
    nz = [i for i, c in enumerate(lin) if c != 0]
    form = " + ".join(f"{lin[i]}*{names[i]}" for i in nz)
    print(f"  depth {d}: vars {names}, linear form = {form}, "
          f"eliminant degree {len(ec)-1}")
    if len(nz) != 1:
        print("    linear form is a genuine combination -- substituting a")
        print("    root for a single variable would be WRONG. Stopping here")
        print("    rather than guessing; this is the bug that made the")
        print("    earlier scan report EMPTY.")
        break
    var = sp.Symbol(names[nz[0]])
    def ev(T):
        v = 0
        for c in reversed(ec): v = (v*T + c) % P
        return v
    rr = [T for T in range(P) if ev(T) == 0]
    print(f"    variable {var}, {len(rr)} rational roots")
    if not rr: print("    no rational root; stopping"); break
    assign[var] = rr[0]
    eqs = [sp.expand(e.subs({var: rr[0]})) for e in eqs]
    eqs = [e for e in eqs if e != 0]
    print(f"    fixed {var} = {rr[0]}, {len(eqs)} equations remain")
    if not eqs: print("    ALL EQUATIONS SATISFIED"); break
print(f"\nassigned: { {str(k): v for k,v in assign.items()} }")
