#!/usr/bin/env python3
"""MY OWN end-to-end verdict on subcase 2, at an explicit verified face point.

Uses only things built in this directory: the (x,y)-derived (u,z) identities
(cross-checked against a direct bracket), and the five face covers extracted
by FGLM and verified against 2qt' - 3q't = u^2.

For each cover, substitute the explicit (q,t) into

    E0:  f'r - p g'                        = 0
    E1:  2f's + p'r - p r' - 2q g'         = 0
    E2:  3f't + 2p's + q'r - p s' - 2q r'  = 0
    E3:  3p't + 2q's - p t' - 2q s'        = 0

and ask whether the two REMAINING polygon vertices can both be present:

    f_8  = a_16_8  (the vertex (8,16) of N(P))
    g_12 = b_12_24 (the vertex (12,24) of N(Q))

imposed by a Rabinowitsch inverse of their product.  Unit ideal => that cover
admits no subcase-2 pair.  All five covers empty => subcase 2 empty at p.

CONTROL: the same system WITHOUT the vertex condition must be non-empty --
the face-only solution (f,p,r,s,g all zero but for constants) always exists.
A run reporting EMPTY there would mean the engine is unsound.
"""
import json, subprocess, sys
import sympy as sp
from uz_indep import build, u

def systems(pt, prime):
    coef, poly, S = build()
    sub = {sp.Symbol(k): sp.Integer(v) for k, v in pt.items()}
    q = poly["q"].subs(sub); t = poly["t"].subs(sub)
    f, p_, g, r, s = (poly[k] for k in ("f", "p", "g", "r", "s"))
    d = lambda e: sp.diff(e, u)
    E = [d(f)*r - p_*d(g),
         2*d(f)*s + d(p_)*r - p_*d(r) - 2*q*d(g),
         3*d(f)*t + 2*d(p_)*s + d(q)*r - p_*d(s) - 2*q*d(r),
         3*d(p_)*t + 2*d(q)*s - p_*d(t) - 2*q*d(s)]
    eqs = []
    for e in E:
        P = sp.Poly(sp.expand(e), u)
        eqs += [sp.expand(c) for c in P.coeffs()]
    eqs = [e for e in eqs if e != 0]
    unks = sorted(set().union(*[e.free_symbols for e in eqs]), key=str)
    return eqs, unks

def run(eqs, unks, prime, nondeg, tag, timeout=1500):
    vs = ",".join(map(str, unks)) + (",WW" if nondeg else "")
    L = [f"ring R = {prime}, ({vs}), dp;",
         "ideal I = " + ",\n ".join(str(e) for e in eqs) + ";"]
    if nondeg:
        L.append("I = I + ideal(WW*(" + ")*(".join(nondeg) + ") - 1);")
    L += ["int t0=timer; ideal G = std(I);",
          '"secs " + string(timer-t0);',
          'if (size(G)==1 && G[1]==1) { "RESULT EMPTY"; } else '
          '{ "RESULT LIVE dim " + string(dim(G)); }', "quit;"]
    fn = f"own_{tag}.sing"
    open(fn, "w").write("\n".join(L) + "\n")
    o = subprocess.run(["Singular", "-q", fn], capture_output=True,
                       text=True, timeout=timeout).stdout
    for line in o.splitlines():
        if line.startswith("RESULT") or line.startswith("secs"):
            print("     " + line.strip(), flush=True)
    return "EMPTY" in o

if __name__ == "__main__":
    prime = int(sys.argv[1])
    pts = json.load(open(f"facepts_verified_p{prime}.json"))
    print(f"=== own end-to-end verdict, p = {prime}, {len(pts)} covers ===")
    print("CONTROL first (no vertex condition; must be LIVE):")
    eqs, unks = systems(pts[0], prime)
    print(f"   cover 0: {len(eqs)} equations, {len(unks)} unknowns")
    ctrl_empty = run(eqs, unks, prime, [], f"ctrl_{prime}")
    print(f"   control sound: {not ctrl_empty}")
    if ctrl_empty:
        print("   CONTROL FAILED -- engine unsound, verdicts below mean nothing")
        sys.exit(1)
    print("MAIN (vertices (8,16) and (12,24) both required nonzero):")
    verdicts = []
    for i, pt in enumerate(pts):
        eqs, unks = systems(pt, prime)
        e = run(eqs, unks, prime, ["f8", "g12"], f"main_{prime}_{i}")
        print(f"   cover {i}: {'EMPTY' if e else 'LIVE'}", flush=True)
        verdicts.append(e)
    print(f"\n{sum(verdicts)}/{len(verdicts)} covers EMPTY")
