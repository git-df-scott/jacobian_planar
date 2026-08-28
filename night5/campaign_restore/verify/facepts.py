#!/usr/bin/env python3
"""Find F_p-rational points of the essential-face variety and VERIFY each
one by substituting it back into  2 q t' - 3 q' t = u^2.

No solver output is trusted: a point counts only if the identity holds
exactly, coefficient by coefficient, mod p.
"""
import subprocess, sys, re
import sympy as sp
from face_solve_indep import face_system
from uz_indep import u

def gen(prime):
    eqs, unk, coef, poly = face_system(prime, {"q1": 1, "q8": 1})
    lines = [f"ring R = {prime}, ({','.join(map(str, unk))}), dp;",
             "ideal I = " + ",\n ".join(str(e) for e in eqs) + ";",
             "option(redSB);",
             "list L = facstd(I);",
             '"components: "+string(size(L));',
             "int i; int j; int d; int v; ideal G;",
             "for (i=1;i<=size(L);i++) {",
             "  G = std(L[i]);",
             "  d = dim(G);",
             "  v = -1;",
             "  if (d == 0) { v = vdim(G); }",
             '  "### comp "+string(i)+" dim "+string(d)+" vdim "+string(v);',
             "  if (d == 0 && v == 1) {",
             "    for (j=1;j<=size(G);j++) { \"PT \"+string(G[j]); }",
             "  }",
             "}",
             "quit;"]
    fn = f"facepts_p{prime}.sing"
    open(fn, "w").write("\n".join(lines) + "\n")
    return fn, unk, poly

def verify(sol, poly, prime):
    """sol: dict name->value.  Check 2 q t' - 3 q' t == u^2 mod prime."""
    q = poly["q"].subs({sp.Symbol("q1"): 1, sp.Symbol("q8"): 1}).subs(sol)
    t = poly["t"].subs(sol)
    E = sp.expand(2 * q * sp.diff(t, u) - 3 * sp.diff(q, u) * t - u**2)
    P = sp.Poly(E, u)
    return all(int(c) % prime == 0 for c in P.coeffs()) if P.coeffs() else True

if __name__ == "__main__":
    primes = [int(a) for a in sys.argv[1:]] or [10007]
    for prime in primes:
        if (prime - 1) % 7 == 0:
            print(f"p={prime}: skipped (7 | p-1, mu_7 would be rational)")
            continue
        fn, unk, poly = gen(prime)
        out = subprocess.run(["Singular", "-q", fn], capture_output=True,
                             text=True, timeout=900).stdout
        pts, cur = [], {}
        for line in out.splitlines():
            if line.startswith("### comp"):
                if cur: pts.append(cur); cur = {}
            if line.startswith("PT "):
                g = line[3:].strip()
                m = re.fullmatch(r"([a-z]\d+)([+-]\d+)?", g.replace(" ", ""))
                if m:
                    cur[sp.Symbol(m.group(1))] = (-int(m.group(2) or 0)) % prime
        if cur: pts.append(cur)
        good = []
        for pt in pts:
            if len(pt) == len(unk) and verify(pt, poly, prime):
                good.append(pt)
        ncomp = out.count("### comp")
        print(f"p={prime}: {ncomp} components, {len(pts)} candidate rational "
              f"points, {len(good)} VERIFIED against 2qt'-3q't = u^2")
        if good:
            import json
            json.dump([{str(k): int(v) for k, v in pt.items()} for pt in good],
                      open(f"facepts_p{prime}.json", "w"))
            print(f"   wrote facepts_p{prime}.json")
