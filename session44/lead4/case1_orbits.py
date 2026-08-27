#!/usr/bin/env python3
"""Read msolve's eliminating polynomial mod p, verify it is a polynomial in
T^7 (the mu_7 normalisation orbit), and factor the resulting quintic."""
import re, subprocess, sys, sympy as sp
from case1_points import reduced_eqs_modp, to_msolve

def elim_poly(k, p):
    m, n = 2*k+1, 3*k+1
    eqs, unk = reduced_eqs_modp(m, n, 0)
    fn = f"_scratch_case1/orb_k{k}_p{p}.ms"
    to_msolve(eqs, unk, p, fn)
    out = fn.replace(".ms", ".res")
    subprocess.run(["msolve", "-f", fn, "-o", out], capture_output=True,
                   text=True, timeout=3000)
    t = open(out).read()
    mm = re.search(r"\[1,\s*\n?\[\[(\d+),\s*\n?\[([^\]]*)\]\]", t)
    deg = int(mm.group(1))
    co = [int(v) for v in mm.group(2).split(",")]
    return deg, co

if __name__ == "__main__":
    k = int(sys.argv[1])
    T = sp.Symbol("T"); s = sp.Symbol("s")
    for p in [int(v) for v in sys.argv[2:]]:
        deg, co = elim_poly(k, p)
        # co[i] is the coefficient of T^i
        nz = [i for i, c in enumerate(co) if c]
        step = 2*k+1
        pure = all(i % step == 0 for i in nz)
        print(f"p={p}  deg={deg}  nonzero exponents {nz}")
        print(f"   polynomial in T^{step}? {pure}")
        if pure:
            h = sum((sp.Integer(co[i]) if 2*co[i] <= p else sp.Integer(co[i]-p))
                    * s**(i//step) for i in nz)
            hp = sp.Poly(h, s, modulus=p)
            fac = sp.factor_list(hp.as_expr(), modulus=p)
            degs = sorted(sp.Poly(f, s, modulus=p).degree() for f, e in fac[1]
                          for _ in range(e))
            print(f"   quintic factors mod p with degrees {degs}")
