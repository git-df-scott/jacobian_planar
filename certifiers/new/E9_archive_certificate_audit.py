"""
E9 - AUDIT OF THE ARCHIVE'S OWN ENDGAME CERTIFICATE, AND THE CROSS-EPOCH CHECK.

The Sessions 16-18 ledger records:

  [PASS] endgame operator T(R) = (v+1)^4 (3v(v+1)R'-13R):
         kernel trivial (rank 14), T(R) = 1 infeasible    (exact LA)
  [PASS] cross-epoch identity h0 = -13 n3, linking the Session-7 Wronskian
         constant to the Session-10 cubic

  AUDIT NOTE: the first endgame certificate tested the WRONG operator
  (M without the (v+1)^4 factor) and came back solvable, contradicting the
  hand proof; the audit located the slip in the test, not the theorem.

This file reproduces BOTH certificates exactly, and then shows precisely
what the endgame certificate does and does not cover.  Verdict:

  * the cross-epoch identity h0 = -13 n3 is TRUE  (re-derived here);
  * the endgame LA certificate is TRUE but SCOPE-LIMITED: it searches a
    space of POLYNOMIALS, and the solution E2/E3 exhibit is not one.  The
    2026 audit "located the slip in the test, not the theorem" - it located
    a real slip, but stopped one step short: the corrected test is still
    restricted to polynomials, so it could not have found the pole solution
    either.  Widening the same certificate by a single Laurent shift finds
    it immediately.
"""
import sympy as sp

v = sp.Symbol('v')
PASS = []
def chk(name, cond):
    PASS.append((name, bool(cond)))
    print(("  [PASS] " if cond else "  [FAIL] ") + name)

def T(R):
    return sp.expand((v+1)**4*(3*v*(v+1)*sp.diff(R, v) - 13*R))

# ------------------------------------------------------ 1. reproduce the LA
print("--- 1. the archive's endgame certificate, reproduced ------------------")
for dg in (13, 20, 30, 60):
    cs = sp.symbols('r0:%d' % (dg+1))
    Rp = sum(cs[i]*v**i for i in range(dg+1))
    eqs = sp.Poly(sp.expand(T(Rp) - 1), v).all_coeffs()
    sol = sp.linsolve(eqs, cs)
    ker = sp.linsolve(sp.Poly(sp.expand(T(Rp)), v).all_coeffs(), cs)
    kerdim = 0 if not ker else len({s for e in list(ker)[0] for s in e.free_symbols} & set(cs))
    chk(f"deg <= {dg} polynomials: T(R) = 1 INFEASIBLE (archive's claim)", not sol)
    chk(f"deg <= {dg} polynomials: kernel of T is trivial", kerdim == 0)
    if dg == 13:
        M = sp.Matrix([[sp.diff(e, c) for c in cs] for e in
                       sp.Poly(sp.expand(T(Rp)), v).all_coeffs()])
        print("    coefficient matrix is", M.shape, " rank =", M.rank())
        chk("archive's 'rank 14' reproduced at deg <= 13", M.rank() == 14)

# ------------------------------------------------------ 2. one Laurent shift
print("\n--- 2. the same certificate, widened by ONE Laurent shift ------------")
for k in (1, 2, 3, 4, 5, 6):
    dg = 12
    cs = sp.symbols('a0:%d' % (dg+1))
    Rk = sum(cs[i]*v**i for i in range(dg+1))/(v+1)**k
    num = sp.expand(sp.cancel(sp.together((T(Rk) - 1)*(v+1)**k)))
    eqs = sp.Poly(num, v).all_coeffs()
    sol = sp.linsolve(eqs, cs)
    found = bool(sol)
    chk(f"box P(v)/(v+1)^{k}: solution {'FOUND' if found else 'none'} "
        f"(E2 predicts {'FOUND' if k >= 4 else 'none'})", found == (k >= 4))
    if found:
        Rv = sp.cancel(sum(list(sol)[0][i]*v**i for i in range(dg+1))/(v+1)**k)
        nn, dd = sp.fraction(sp.cancel(Rv))
        ordm1 = sp.Poly(sp.expand(dd), v).degree() if dd.has(v) else 0
        print("    box k = %d gives" % k, sp.factor(sp.simplify(Rv)),
              "  reduced pole order at v=-1 :", ordm1)
        chk(f"box (v+1)^{k}: the solution is UNIQUE and reduces to pole order 4",
            not ({s2 for e in list(sol)[0] for s2 in e.free_symbols} & set(cs))
            and ordm1 == 4)
        chk(f"box (v+1)^{k}: the solution satisfies T(R) = 1 exactly",
            sp.simplify(sp.cancel(sp.together((v+1)**4*(3*v*(v+1)*sp.diff(Rv, v)
                                                        - 13*Rv))) - 1) == 0)

# ------------------------------------------------------ 3. cross-epoch check
print("\n--- 3. the cross-epoch identity h0 = -13 n3 --------------------------")
s = sp.I*sp.sqrt(3)                                  # sqrt(-3)
Rq = sp.Rational
p = (v**8 + (2 + 8*s)*v**7 + (Rq(-233,3) + Rq(50,3)*s)*v**6
     + (Rq(-4600,27) - Rq(376,3)*s)*v**5 + (Rq(835,3) - Rq(890,3)*s)*v**4
     + (Rq(2420,3) + Rq(22,3)*s)*v**3 + (Rq(1043,3) + 336*s)*v**2
     + (-118 + 158*s)*v + (-28 + 4*s))
r = (v**5 + (Rq(4,3) + Rq(16,3)*s)*v**4 + (Rq(-278,9) + Rq(68,9)*s)*v**3
     + (Rq(-140,3) - 24*s)*v**2 + (Rq(35,3) - Rq(112,3)*s)*v
     + Rq(68,3) - Rq(20,3)*s)
h0 = Rq(1664,3) - Rq(832,3)*s
N = sp.expand(p**2 - v*r**3)
chk("deg(p^2 - w r^3) = 3 (the 16 -> 3 miracle cancellation)",
    sp.Poly(sp.expand(sp.radsimp(N)), v).degree() == 3)
n3 = sp.simplify(sp.expand(N).coeff(v, 3))
print("    n3 =", sp.simplify(sp.expand(n3)))
print("    h0 =", h0)
chk("h0 == -13 * n3  (Session-7 Wronskian constant vs Session-10 cubic)",
    sp.simplify(sp.expand(h0 + 13*n3)) == 0)
chk("h := 2 p' r w - p(r + 3 w r') is the constant h0",
    sp.simplify(sp.expand(2*sp.diff(p, v)*r*v - p*(r + 3*v*sp.diff(r, v))) - h0) == 0)

print("\n--- 4. VERDICT ------------------------------------------------------")
print("    cross-epoch identity h0 = -13 n3 : TRUE, re-derived independently.")
print("    endgame LA certificate           : TRUE on polynomials, but the")
print("      solution space it searched CANNOT contain the actual solution.")
print("      One Laurent shift - (v+1)^-4 - finds it in the same code.")

print()
for n, o in PASS:
    if not o: print("FAILED:", n)
assert all(o for _, o in PASS), "E9 FAILED"
print("E9: ALL %d CHECKS PASS" % len(PASS))
