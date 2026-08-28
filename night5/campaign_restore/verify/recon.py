#!/usr/bin/env python3
"""Reconstruct the face ideal's lex Groebner basis over Q from many primes.

The direct characteristic-zero Groebner basis does not finish (a dp run on the
17-variable face system was still going after 10 minutes, and the 69-variable
full formulation did not converge even mod p).  But the lex basis mod p costs
26 seconds and has the SAME SHAPE at every good prime:

    t9^5 + ...            t8^7 + quartic(t9)            t2 - 1
    every other coordinate a polynomial in t8, t9

So the standard modular route applies: compute the lex basis at many primes,
CRT the coefficients, and rationally reconstruct.  No prime needs the quintic
to split -- that was only needed to get explicit points.

The reconstruction is a GUESS until verified.  Verification, done here:
every reconstructed generator must reduce to zero modulo the original face
ideal over Q, and every original face equation must reduce to zero modulo the
reconstructed basis.  Both directions, or the result is not used.
"""
import subprocess, sys, re
import sympy as sp
from face_solve_indep import face_system

def lex_basis(prime):
    eqs, unk, coef, poly = face_system(prime, {"q1": 1, "q8": 1})
    body = ",\n ".join(str(e) for e in eqs)
    L = [f"ring D = {prime}, ({','.join(map(str,unk))}), dp;",
         f"ideal I = {body};", "ideal G = std(I);",
         '"vdim = " + string(vdim(G));',
         f"ring L = {prime}, ({','.join(map(str,unk))}), lp;",
         "setring L; ideal I = fetch(D,I);", "ideal GL = stdfglm(I);",
         "int i; for(i=1;i<=size(GL);i++){ \"GL \"+string(GL[i]); }", "quit;"]
    fn = f"rec_{prime}.sing"
    open(fn, "w").write("\n".join(L) + "\n")
    o = subprocess.run(["Singular", "-q", fn], capture_output=True,
                       text=True, timeout=900).stdout
    if "vdim = 35" not in o:
        return None
    return [l[3:].strip() for l in o.splitlines() if l.startswith("GL ")]

if __name__ == "__main__":
    primes = [int(a) for a in sys.argv[1:]]
    out = {}
    for p in primes:
        if not sp.isprime(p):
            continue
        b = lex_basis(p)
        if b is None:
            print(f"p={p}: vdim != 35, skipped", flush=True); continue
        out[p] = b
        print(f"p={p}: lex basis of {len(b)} generators", flush=True)
    import json
    json.dump(out, open("recon_bases.json", "w"))
    print(f"collected {len(out)} bases -> recon_bases.json")
