#!/usr/bin/env python3
"""Solve the (STAR) solvability locus exactly, in every stratum.

(STAR)  2 S R' + S' R = 2 z^2 S,  R rational, S = sum_{k<=4} s_k z^k,
        s4 != 0 (deg S = 4), s0 != 0 (vertex c_0_8 != 0).

For S SQUAREFREE, R is forced polynomial of degree 3 (pole analysis: a pole of
order m at a root of S of multiplicity k needs k = 2m or k >= m+1, both
impossible for k = 1; and R has no poles off V(S)).  The four top coefficient
equations solve triangularly for R; the remaining three are conditions on S.

Symmetries: S -> u S (R fixed), and S(z) -> S(tz) with R -> t^-3 R(tz).
Normalize s4 = 1 and then s3 in {1, 0}.
"""
import sympy as sp

s0, s1, s2, s3, s4 = sp.symbols('s0 s1 s2 s3 s4')

C2 = -768*s0*s4**3 + 552*s1*s3*s4**2 + 256*s2**2*s4**2 - 460*s2*s3**2*s4 + 105*s3**4
C1 = 48*s0*s3*s4**2 + 240*s1*s2*s4**2 - 42*s1*s3**2*s4 - 116*s2**2*s3*s4 + 35*s2*s3**3
C0 = 128*s0*s2*s4**2 - 56*s0*s3**2*s4 + 144*s1**2*s4**2 - 116*s1*s2*s3*s4 + 35*s1*s3**3

def report(sols, label, subs_extra):
    print(f"\n===== stratum {label} =====")
    if not sols:
        print("  NO SOLUTIONS")
        return []
    keep = []
    for sol in sols:
        d = dict(subs_extra)
        d.update(sol)
        S = sum(d.get(v, v) * z**k for k, v in enumerate([s0, s1, s2, s3, s4]))
        S = sp.expand(S)
        Sp = sp.Poly(S, z)
        disc = sp.simplify(sp.discriminant(Sp))
        s0v = d.get(s0, s0)
        print(f"\n  S = {S}")
        print(f"    s0 = {sp.nsimplify(s0v)}   (need != 0: {sp.simplify(s0v) != 0})")
        print(f"    disc = {disc}   squarefree: {sp.simplify(disc) != 0}")
        fac = sp.factor(S)
        print(f"    factored: {fac}")
        if sp.simplify(s0v) != 0 and sp.simplify(disc) != 0:
            print("    *** SQUAREFREE with S(0) != 0 -> COUNTEREXAMPLE TO THE THEOREM ***")
            keep.append(S)
    return keep

z = sp.symbols('z')

# ---------------- stratum s4 = 1, s3 = 1 -----------------------------------
sub = {s4: 1, s3: 1}
eqs = [sp.expand(c.subs(sub)) for c in (C2, C1, C0)]
print("stratum s4=1,s3=1 equations:")
for e in eqs:
    print("   ", e)
sols = sp.solve(eqs, [s0, s1, s2], dict=True)
print(f"\n  raw solutions: {len(sols)}")
for x in sols:
    print("   ", x)
keep1 = report(sols, "s4=1, s3=1", sub)

# ---------------- stratum s4 = 1, s3 = 0 -----------------------------------
sub = {s4: 1, s3: 0}
eqs = [sp.expand(c.subs(sub)) for c in (C2, C1, C0)]
print("\nstratum s4=1,s3=0 equations:")
for e in eqs:
    print("   ", e)
sols = sp.solve(eqs, [s0, s1, s2], dict=True)
print(f"\n  raw solutions: {len(sols)}")
for x in sols:
    print("   ", x)
keep0 = report(sols, "s4=1, s3=0", sub)

# ---------------- dimension of the full cone --------------------------------
print("\n===== Groebner / dimension of the full locus (s4 = 1) =====")
G = sp.groebner([sp.expand(c.subs({s4: 1})) for c in (C2, C1, C0)],
                s0, s1, s2, s3, order='lex')
for g in G.exprs:
    print("   ", sp.factor(g))
