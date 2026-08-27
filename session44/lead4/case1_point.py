#!/usr/bin/env python3
"""Explicit F_p point of subcase 1's essential-face variety.

Uses the exact characteristic-zero eliminating polynomial produced by msolve
over Q for the reduced 6-variable system.  It is a polynomial in T^7 (T = a6):

    w(T) = h(T^7),  h irreducible quintic over Q  (verified with sympy)

so: pick a prime p with 7 not dividing p-1 (then 7th roots are unique) and
with h having a root s0 in F_p; set a6 = s0^(1/7); substitute and finish the
remaining 5 unknowns with a lex Groebner basis.  The point is then checked
by evaluating W(u) = f g + 2u f g' - 3u f' g and requiring it to be 1.
"""
import subprocess, sys, sympy as sp
from case1_ladder import coeffs

HCO = [-1888043347611739526396142670327809715470336,
       586529490054134032292876680565455306752,
       591414847960503971284831143987840,
       265472843532245531128968765,
       62410476400737833472,
       9374377445732]           # h(s) = sum HCO[i] s^i,  s = a6^7

M, N = 7, 10


def residual_eqs():
    from case1_points import reduced_eqs_modp
    return reduced_eqs_modp(M, N, 0)


def find_point(p):
    if (p - 1) % 7 == 0:
        return None, "p = 1 mod 7 (7th root not unique) -- skipped"
    h = sp.Poly(sum(sp.Integer(c) * sp.Symbol('s')**i
                    for i, c in enumerate(HCO)), sp.Symbol('s'), modulus=p)
    rts = sp.ground_roots(h)
    if not rts:
        return None, "h has no root mod p"
    s0 = int(list(rts)[0]) % p
    e = pow(7, -1, p - 1)
    a6 = pow(s0, e, p)
    assert pow(a6, 7, p) == s0 % p
    eqs, unk = residual_eqs()
    es = []
    for e_ in eqs:
        num, den = sp.fraction(sp.together(e_.subs(sp.Symbol('a6'), a6)))
        es.append(str(sp.expand(num)).replace("**", "^"))
    L = [f"ring R = {p}, (a1,a2,a3,a4,a5), lp;",
         "ideal I = " + ",\n".join(es) + ";",
         "ideal G = std(I);",
         '"vdim " + string(vdim(G));', "G;", "quit;"]
    fn = f"_scratch_case1/pt_p{p}.sing"
    open(fn, "w").write("\n".join(L))
    pr = subprocess.run(["Singular", "-q", fn], capture_output=True,
                        text=True, timeout=1200)
    return (a6, pr.stdout), None


def build_fg(avals, p):
    """avals = [a1..a6]; returns (f coeffs a_0..a_7, g coeffs b_0..b_10)."""
    a = [1] + [v % p for v in avals] + [1]
    W = coeffs(M, N)
    b = [1]
    for n in range(1, N + 1):
        rest = 0
        for (c, i, j) in W[n]:
            if i == 0 and j == n:
                continue
            rest = (rest + c * a[i] * b[j]) % p
        b.append((-rest * pow(1 + 2 * n, -1, p)) % p)
    return a, b


def check(a, b, p):
    """W_n == delta_{n,0} for all n?"""
    W = coeffs(M, N)
    bad = []
    for n in range(0, M + N + 1):
        v = sum(c * a[i] * b[j] for (c, i, j) in W[n]) % p
        if v != (1 if n == 0 else 0):
            bad.append((n, v))
    return bad


if __name__ == "__main__":
    for p in [int(v) for v in sys.argv[1:]]:
        res, err = find_point(p)
        print(f"=== p={p} (p mod 7 = {p%7}) ===")
        if err:
            print("   ", err); continue
        a6, out = res
        print("    a6 =", a6)
        print(out)
