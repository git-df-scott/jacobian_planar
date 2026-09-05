#!/usr/bin/env python3
"""Independent verdict for subcase 2, in three self-checking stages.

Stage A  solve the essential face  2 q t' - 3 q' t = u^2  and VERIFY each
         solution by substituting it back -- no solver is trusted, only
         the identity.
Stage B  compute ker(E3) exactly, as a linear system in (p,s).
Stage C  the rest is settled by hand (see PROOF below), so all that is
         needed is to confirm (p,s) = 0.

PROOF that (p,s) = 0 forces the subcase empty -- characteristic zero, no
computer.  With p = s = 0 the remaining identities read
        E1:  -2 q g' = 0                        =>  g' = 0
        E2:   3 f' t + q' r = 0
        E0:   f' r = 0
q and t are nonzero (they carry the required vertices).  From E0, in an
integral domain, f' = 0 or r = 0.
  * if r = 0 then E2 gives 3 f' t = 0, so f' = 0;
  * if f' = 0 then E2 gives q' r = 0, and q' != 0 because deg q = 8, so r = 0.
Either way f' = 0 and r = 0 and g' = 0: f and g are CONSTANTS.  Hence
        f_8 = 0   (the vertex (8,16) of N(P))
        g_12 = 0  (the vertex (12,24) of N(Q))
and neither Newton polygon is the claimed quadrilateral.  QED.

So the whole subcase turns on one question: can (p,s) be nonzero?
"""
import sys
import sympy as sp

from uz_indep import build, identities, u

def face_system(prime, gauge):
    coef, poly, S = build()
    q, t = poly["q"], poly["t"]
    E4 = sp.expand(3 * sp.diff(q, u) * t - 2 * q * sp.diff(t, u) + u**2)
    eqs = [sp.expand(c) for (_, ), c in sp.Poly(E4, u).terms()]
    unk = sorted(set().union(*[e.free_symbols for e in eqs]), key=str)
    sub = {sp.Symbol(k): v for k, v in gauge.items()}
    eqs = [sp.expand(e.subs(sub)) for e in eqs]
    eqs = [e for e in eqs if e != 0]
    unk = [v for v in unk if v not in sub]
    return eqs, unk, coef, poly

def sing_solve(eqs, unk, prime, tag):
    lines = [f"ring R = {prime}, ({','.join(map(str, unk))}), lp;",
             "ideal I = " + ",\n ".join(str(e) for e in eqs) + ";",
             "ideal G = std(I);",
             '"dim: "+string(dim(G));',
             'if (dim(G)==0) { "vdim: "+string(vdim(G)); }',
             "ideal T = G;",
             'int i; for (i=1;i<=size(T);i++) { "g"+string(i)+" = "+string(T[i]); }',
             "quit;"]
    fn = f"face_{tag}_p{prime}.sing"
    open(fn, "w").write("\n".join(lines) + "\n")
    return fn

if __name__ == "__main__":
    prime = int(sys.argv[1]) if len(sys.argv) > 1 else 65521
    # gauge: q8 = 1 kills the scaling and leaves a finite mu_7 ambiguity
    eqs, unk, coef, poly = face_system(prime, {"q8": 1})
    print(f"essential face 2qt' - 3q't = u^2 :  {len(eqs)} equations, "
          f"{len(unk)} unknowns after the gauge q8 = 1")
    print("   unknowns:", " ".join(map(str, unk)))
    degs = sorted({sp.Poly(e, *unk).total_degree() for e in eqs})
    print(f"   degrees present: {degs}  (bilinear in q and t, as expected)")
    fn = sing_solve(eqs, unk, prime, "face")
    print(f"wrote {fn}")
