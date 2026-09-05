#!/usr/bin/env python3
"""Test degree-uniform strengthenings toward the paper's B>16 conjecture.

Paper proves (unconditional, all deg): mu1=mu2=0  =>  mu0=0.
Conjecture: ALL solutions have mu2=mu1=0  =>  B>16.

We probe, per degree, which of these saturated systems are EMPTY:
  Q_a: {(3.5),(3.6), mu2 != 0}         -- is mu2=0 forced?
  Q_b: {(3.5),(3.6), mu1 != 0}         -- is mu1=0 forced?
  Q_c: {(3.5),(3.6), mu0 != 0}         -- the counterexample query (done)
A degree-uniform EMPTY pattern for Q_a or Q_b, with a visible mechanism in
the Groebner staircase, is the route to a uniform proof.
"""
import subprocess, sys, tempfile, sympy as sp
import abel_b16 as ab, abel_msolve as am

def query(k, killvar):
    eqs, unk, q1, A = ab.build_identity(k)
    s = sp.Symbol("s_sat"); sub={ab.mu3:1}
    vars2=[v for v in unk if v!=ab.mu3]
    gens=[]
    for e in eqs:
        pe=sp.Poly(sp.expand(e.subs(sub)),*vars2,domain="QQ"); L=1
        for c in pe.coeffs(): L=sp.ilcm(L,sp.Rational(c).q)
        gens.append(sp.expand(e.subs(sub)*L))
    gens.append(killvar*s-1); vars2=vars2+[s]
    txt=am.to_msolve(gens,vars2)
    f=tempfile.NamedTemporaryFile("w",suffix=".ms",delete=False); f.write(txt); f.close()
    try:
        r=subprocess.run(["msolve","-f",f.name],capture_output=True,text=True,timeout=2400)
    except subprocess.TimeoutExpired: return "TIMEOUT"
    o=(r.stdout or "").strip()
    return "EMPTY" if o.startswith("[-1]") else "NONEMPTY"

if __name__=="__main__":
    k=int(sys.argv[1])
    for name,var in (("mu2!=0",ab.mu2),("mu1!=0",ab.mu1)):
        print(f"deg(q1)={k} {name}: {query(k,var)}",flush=True)
