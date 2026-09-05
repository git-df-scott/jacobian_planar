#!/usr/bin/env python3
"""The essential-face equation for the open (72,108) subcase 1.

VERIFIED identity (checked at (deg f, deg g) = (1,1),(2,3),(3,4),(7,10)):

    [ x f(u), x^2 y g(u) ]  =  x^2 ( f g + 2u f g' - 3u f' g ),   u = x y^2.

For subcase 1 with weight w = 2i - j, the P-face is the edge (1,0)-(8,14)
and the Q-face is (2,1)-(12,21), giving deg f = 7, deg g = 10. Crucially
w(bracket top) = 2 + 3 + w(-1,-1) = 4 EQUALS w(x^2) = 4, so this top
component does NOT vanish -- it must equal the target exactly:

    W(u) := f g + 2u f g' - 3u f' g  ==  1.

Coefficientwise  W_N = sum_{i+j=N} (1 + 2j - 3i) a_i b_j = [N = 0].
The top coefficient N = m+n has factor 1 + 2n - 3m = 1 + 20 - 21 = 0, so it
vanishes identically -- a consistency check that this face is admissible.

This is a far smaller object than anything else in the campaign: 19
coefficients, reducible by the two scaling symmetries
    (a,b) -> (t a, t^{-1} b)          [W invariant]
    u -> s u, a_i -> s^i a_i, b_j -> s^j b_j   [W_N -> s^N W_N]
to roughly 16 unknowns against 16 equations.

A NECESSARY condition: if W(u) = 1 has no solution with the required
non-degeneracy (a_0, a_m, b_0, b_n all nonzero -- they are polygon
vertices), then subcase 1 is EMPTY, with no reference to the rest of the
system. Includes a validation ladder at (m,n) = (2k+1, 3k+1).
"""
import argparse, subprocess, sys, tempfile
import sympy as sp


def system(m, n, normalise=True):
    a = sp.symbols(f"a0:{m+1}"); b = sp.symbols(f"b0:{n+1}")
    eqs = []
    for N in range(0, m + n + 1):
        e = 0
        for i in range(max(0, N - n), min(m, N) + 1):
            j = N - i
            e += (1 + 2*j - 3*i) * a[i] * b[j]
        e = sp.expand(e - (1 if N == 0 else 0))
        if e != 0:
            eqs.append(e)
    unk = list(a) + list(b)
    sub = {}
    if normalise:
        sub = {a[0]: 1, a[m]: 1}            # the two scalings
        eqs = [sp.expand(e.subs(sub)) for e in eqs]
        eqs = [e for e in eqs if e != 0]
        unk = [v for v in unk if v not in sub]
    return eqs, unk, a, b


def to_ms(eqs, unk, char, sat):
    s = sp.Symbol("s_sat")
    gens = list(eqs) + ([sp.expand(sat*s - 1)] if sat is not None else [])
    vs = ",".join(str(v) for v in unk) + (",s_sat" if sat is not None else "")
    out = []
    for g in gens:
        pe = sp.Poly(g, *(unk + ([s] if sat is not None else [])), domain="QQ")
        L = 1
        for c in pe.coeffs(): L = sp.ilcm(L, sp.Rational(c).q)
        out.append(str(sp.expand(g*L)).replace("**","^").replace(" ",""))
    return vs + f"\n{char}\n" + ",\n".join(out) + "\n"


def solve(m, n, char, timeout=1200):
    eqs, unk, a, b = system(m, n)
    txt = to_ms(eqs, unk, char, b[n])          # b_n != 0 (a polygon vertex)
    fn = f"faceeq_{m}_{n}_c{char}.ms"
    open(fn, "w").write(txt)
    try:
        r = subprocess.run(["msolve", "-f", fn], capture_output=True,
                           text=True, timeout=timeout)
        out = (r.stdout or "").strip()
    except subprocess.TimeoutExpired:
        return "TIMEOUT", len(eqs), len(unk)
    v = ("EMPTY" if out.startswith("[-1]") else
         ("NONEMPTY " + out[:60].replace("\n"," ") if out.startswith("[") else
          "NO-OUTPUT"))
    return v, len(eqs), len(unk)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ladder", action="store_true")
    ap.add_argument("--char", type=int, default=0)
    ap.add_argument("--m", type=int, default=7)
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--timeout", type=int, default=1200)
    A = ap.parse_args()
    if A.ladder:
        print("validation ladder (m,n) = (2k+1, 3k+1):")
        for k in (0, 1, 2):
            m, n = 2*k+1, 3*k+1
            v, ne, nu = solve(m, n, A.char, 600)
            print(f"  k={k}  (m,n)=({m},{n})  {nu} unknowns, {ne} eqs  ->  {v}",
                  flush=True)
    else:
        v, ne, nu = solve(A.m, A.n, A.char, A.timeout)
        print(f"(m,n)=({A.m},{A.n}) char {A.char}: {nu} unknowns, {ne} eqs")
        print(f"VERDICT: {v}")
        if v == "EMPTY":
            print("*** the essential face admits NO non-degenerate solution")
            print("    -> subcase 1 is EMPTY ***")
