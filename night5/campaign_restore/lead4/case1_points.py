#!/usr/bin/env python3
"""Reduced 6-variable system -> msolve, at several primes; also count."""
import os, re, subprocess, sys
from case1_ladder import coeffs, sym

SCRATCH = "_scratch_case1"


def reduced_eqs_modp(m, n, p):
    """Eliminate b_1..b_n symbolically over GF(p); return residual eq strings."""
    import sympy as sp
    A = {0: sp.Integer(1), m: sp.Integer(1)}
    for i in range(1, m):
        A[i] = sp.Symbol(f"a{i}")
    W = coeffs(m, n)
    B = {0: sp.Integer(1)}
    for N in range(1, n + 1):
        rest = 0
        for (c, i, j) in W[N]:
            if i == 0 and j == N:
                continue
            rest += c * A[i] * B[j]
        B[N] = sp.expand(-rest / sp.Integer(1 + 2 * N))
    eqs = []
    for N in range(n + 1, m + n + 1):
        e = sp.expand(sum(c * A[i] * B[j] for (c, i, j) in W[N]))
        if e != 0:
            eqs.append(e)
    return eqs, [A[i] for i in range(1, m)]


def to_msolve(eqs, unk, p, fn):
    import sympy as sp
    lines = [",".join(str(v) for v in unk), str(p)]
    body = []
    for e in eqs:
        num, den = sp.fraction(sp.together(e))
        num = sp.expand(num)
        s = str(sp.Poly(num, *unk).as_expr()).replace("**", "^")
        body.append(s)
    open(fn, "w").write("\n".join(lines) + "\n" + ",\n".join(body) + "\n")


if __name__ == "__main__":
    k = int(sys.argv[1]); primes = [int(v) for v in sys.argv[2:]] or [1073741827]
    m, n = 2 * k + 1, 3 * k + 1
    eqs, unk = reduced_eqs_modp(m, n, 0)
    print(f"k={k}: {len(eqs)} residual equations in {len(unk)} unknowns")
    for p in primes:
        fn = f"{SCRATCH}/case1_red_k{k}_p{p}.ms"
        to_msolve(eqs, unk, p, fn)
        out = fn.replace(".ms", ".res")
        subprocess.run(["msolve", "-f", fn, "-o", out], capture_output=True,
                       text=True, timeout=3000)
        t = open(out).read()
        mm = re.search(r"\[1,\s*\n?\[\[(\d+),", t)
        print(f"   p={p}: degree {mm.group(1) if mm else t[:80]}")
