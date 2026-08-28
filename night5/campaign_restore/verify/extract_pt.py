#!/usr/bin/env python3
"""Triangular extraction of an explicit face point, one variable at a time.

At each step the minimal polynomial of the next unpinned variable is computed
on the current quotient ring (via std + reduce only -- no RUR, no msolve
linear form), factored, and a LINEAR factor's root is adjoined.  When vdim
reaches 1 the point is read off and VERIFIED against 2 q t' - 3 q' t = u^2.

If no linear factor exists the extraction stops and says so, rather than
guessing at a convention.  That is deliberate: two earlier attempts in this
campaign went wrong by assuming a solver's output convention.
"""
import sys
import sympy as sp
from minpoly_pt import minpoly, solve_dep
from face_solve_indep import face_system
from uz_indep import u

def run(prime, maxsteps=30):
    eqs, unk, coef, poly = face_system(prime, {"q1": 1, "q8": 1})
    T = sp.Symbol("T")
    pinned = {}
    extra = []
    for step in range(maxsteps):
        todo = [v for v in unk if v not in pinned]
        if not todo:
            break
        progressed = False
        for var in todo:
            vd, rows = minpoly(prime, eqs, unk, str(var), extra)
            if vd is None:
                print("  singular gave no vdim; abort"); return None
            if vd == 1:
                print(f"  vdim = 1 reached after {len(pinned)} pins")
                return finish(prime, eqs, unk, extra, coef, poly, pinned)
            deg, comb = solve_dep(rows, unk, prime)
            if deg is None or deg == 0:
                continue
            co = [int(c) % prime for c in comb[:deg+1]]     # low -> high
            roots = [c for c in range(prime)
                     if sum(a * pow(c, j, prime) for j, a in
                            enumerate(co)) % prime == 0]
            if not roots:
                continue
            root = roots[0]
            pinned[var] = root
            extra.append(sp.Symbol(str(var)) - root)
            print(f"  vdim {vd:3d} -> pinned {var} = {root} "
                  f"(minpoly deg {deg}, {len(roots)} roots in F_p)",
                  flush=True)
            progressed = True
            break
        if not progressed:
            print(f"  no linear factor available at vdim {vd}; "
                  f"the remaining coordinates are irrational at p={prime}")
            return None
    return None

def finish(prime, eqs, unk, extra, coef, poly, pinned):
    # read off every coordinate from the vdim-1 ideal
    from minpoly_pt import singular
    body = ",\n ".join(str(e) for e in eqs + extra)
    txt = [f"ring R = {prime}, ({','.join(map(str,unk))}), lp;",
           f"ideal I = {body};", "ideal G = std(I);",
           "int i; for(i=1;i<=size(G);i++){ \"G \"+string(G[i]); }", "quit;"]
    out = singular("\n".join(txt))
    sol = dict(pinned)
    import re
    for line in out.splitlines():
        m = re.fullmatch(r"G ([a-z]\d+)([+-]\d+)", line.strip().replace(" ", ""))
        if m:
            sol[sp.Symbol(m.group(1))] = (-int(m.group(2))) % prime
    sol[sp.Symbol("q1")] = 1; sol[sp.Symbol("q8")] = 1
    q = poly["q"].subs(sol); t = poly["t"].subs(sol)
    E = sp.expand(2*q*sp.diff(t,u) - 3*sp.diff(q,u)*t - u**2)
    P = sp.Poly(E, u) if E != 0 else None
    ok = (P is None) or all(int(c) % prime == 0 for c in P.coeffs())
    print(f"  recovered {len(sol)} coordinates")
    print(f"  VERIFY 2qt' - 3q't == u^2 mod {prime}: {ok}")
    return sol if ok else None

if __name__ == "__main__":
    prime = int(sys.argv[1])
    print(f"=== extracting a face point at p = {prime} ===")
    sol = run(prime)
    if sol:
        import json
        json.dump({str(k): int(v) for k, v in sol.items()},
                  open(f"facept_p{prime}.json", "w"))
        print(f"  wrote facept_p{prime}.json")
