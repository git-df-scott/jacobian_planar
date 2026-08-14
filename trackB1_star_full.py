#!/usr/bin/env python3
"""COMPLETE solution of the pentagon bottom criterion (STAR), all strata.

(STAR)   2 S R' + S' R = 2 z^2 S ,   R RATIONAL,
         S of degree 4 with S(0) != 0.

Write S = S1 * S2^2 with S1 SQUAREFREE (the squarefree part) and set
U := R * S2.  Then (STAR) becomes

    (STAR')  2 S1 U' + S1' U = 2 z^2 S1 S2 .

Pole analysis: a pole of U of order m at a root of S1 of multiplicity k=1 needs
k = 2m or k >= m+1, both impossible; and U has no poles off V(S1).  So

    ***  U is a POLYNOMIAL, always.  ***

deg S1 + 2 deg S2 = 4, so deg S1 in {0, 2, 4}:

  d2 = 0  S squarefree            -> handled by trackB1_elliptic_solve.py: the
                                     solvable locus is 5 points, ALL on the
                                     discriminant => NO squarefree S solves.
  d2 = 1  S = A^2 * S1, A linear, S1 squarefree quadratic  -> THIS SCRIPT.
  d2 = 2  S1 = const, S = c*A^2 (perfect square)  -> 2c U' = 2 z^2 c A, so
          U = int z^2 A dz always works: EVERY perfect square solves.

The d2 = 1 stratum is the one the published 0/40 sampling could not see: the
map U |-> 2 S1 U' + S1' U is injective on polynomials of degree <= 4 with
5-dim image inside the 6-dim space of degree <= 5, so solvability is exactly
ONE linear condition on A given S1 -- a positive-dimensional family.
"""
import sympy as sp

z, p, q, a0, a1 = sp.symbols('z p q a0 a1')
u = sp.symbols('u0:5')

S1 = z**2 + p*z + q                 # monic squarefree quadratic
A = a1*z + a0                       # linear
U = sum(u[j]*z**j for j in range(5))

eq = sp.expand(2*S1*sp.diff(U, z) + sp.diff(S1, z)*U - 2*z**2*A*S1)
coeffs = [sp.expand(eq.coeff(z, n)) for n in range(6)]
print("(STAR') coefficient equations, deg U = 4:")
for n, c in enumerate(coeffs):
    print(f"  z^{n}: {c} = 0")

# Solve the five top equations (n = 5..1) for u4..u0; n = 0 is the condition.
sol = sp.solve(coeffs[1:][::-1], u, dict=True)
assert len(sol) == 1, sol
sol = sol[0]
print("\nU coefficients (triangular from the top):")
for j in range(4, -1, -1):
    print(f"  u{j} = {sp.simplify(sol[u[j]])}")

COND = sp.simplify(sp.expand(coeffs[0].subs(sol)))
COND = sp.factor(sp.numer(sp.cancel(COND)))
print(f"\n*** THE SINGLE CONDITION on (p, q, a0, a1):\n    {COND} = 0")

# Solve the condition for a0 in terms of (p, q, a1) -- it is linear in (a0,a1).
sol_a = sp.solve(COND, a0, dict=True)
print(f"\nsolved for a0: {sol_a}")
a0v = sp.simplify(sol_a[0][a0])
print(f"  a0 = {a0v}")

print("\n" + "=" * 72)
print("THE FAMILY:  S = A^2 * S1,  S1 = z^2 + p z + q,  A = a1*(z + a0/a1)")
print("=" * 72)
Aq = sp.simplify((A.subs(a0, a0v))/a1)
print(f"  A / a1 = {sp.factor(sp.simplify(Aq))}")
Sfam = sp.factor(sp.expand(a1**2 * Aq**2 * S1))
print(f"  S / a1^2 = {Sfam}")

# ---- verify a random member really solves (STAR) with a rational R ---------
print("\n--- verification on random members (exact rationals) ---")
import random
random.seed(11)
ok = bad = 0
for _ in range(12):
    pv = sp.Rational(random.randint(-9, 9), random.randint(1, 5))
    qv = sp.Rational(random.randint(1, 9), random.randint(1, 5))
    if sp.simplify(pv**2 - 4*qv) == 0 or qv == 0:
        continue
    sub = {p: pv, q: qv, a1: 1}
    a0n = sp.simplify(a0v.subs(sub))
    An = sp.simplify(A.subs(sub).subs(a0, a0n))
    if sp.simplify(An.subs(z, 0)) == 0:
        continue                       # would violate S(0) != 0
    Sn = sp.expand(An**2 * S1.subs(sub))
    Un = sp.expand(U.subs({k: sp.simplify(v.subs(sub).subs(a0, a0n))
                           for k, v in sol.items()}))
    Rn = sp.cancel(Un / An)
    res = sp.simplify(sp.expand(2*Sn*sp.diff(Rn, z) + sp.diff(Sn, z)*Rn
                                - 2*z**2*Sn))
    sq = sp.simplify(sp.discriminant(sp.Poly(Sn, z)))
    isperfsq = sp.simplify(sp.sqrt(sp.factor(Sn)).is_polynomial(z)) \
        if False else None
    fac = sp.factor(Sn)
    status = "OK " if res == 0 else "FAIL"
    ok += res == 0
    bad += res != 0
    print(f"  {status} S = {fac}")
    print(f"       R = {sp.factor(Rn)}   residual={res}")
print(f"\n  verified {ok} / {ok+bad}")
