"""
E5 - PROPAGATING THE UNIQUE ENDGAME SOLUTION BACK UP THE TOWER.

Step 3 of the campaign plan: "solve L4 explicitly at D = 13 with the
pole-at--1 solutions Opus's theorem wrongly excluded, and propagate that R
back up the tower.  Either it meets a genuine contradiction at a higher layer
- a real closure this time, written down properly - or it doesn't, and what
comes out the top is a candidate pair."

It meets a genuine contradiction, and this file writes it down properly.

INPUT   the unique solution of  alpha^5 (v+1)^4 (3v(v+1)R' - 13R) = -c :
            R = S(v)/(v+1)^4,  S = (c/(455 alpha^5))(243v^4 - 81v^3 + 54v^2 - 42v + 35)
OUTPUT  W~_-5 = alpha^6 U^2 (U-1)^9 S(U-1)   -- an honest degree-15 polynomial
        that satisfies the v = 0 divisibility, has u(W~) = 2, and therefore
  (i)  violates the ladder bound u(W~_-5) >= 3  (E4)          [closure 1]
  (ii) gives R map-degree 4, so R cannot realize the framework's degree-13
       Belyi map: deg W~_-5 = 15, the 13-realization needs 28 [closure 2]

Closure (ii) uses no genericity and no Theorem 3.  Note that 15 is EXACTLY the
degree of the near-miss's own W~_-5: the pole branch lands in the same degree
stratum as the near-miss and dies on the same ledger.
"""
import sympy as sp

v, U, alpha, c = sp.symbols('v U alpha c')
PASS = []
def chk(name, cond):
    PASS.append((name, bool(cond)))
    print(("  [PASS] " if cond else "  [FAIL] ") + name)

kappa = -c/alpha**5
S = sp.expand(-kappa*(243*v**4 - 81*v**3 + 54*v**2 - 42*v + 35)/455)
R = sp.together(S/(v+1)**4)
print("--- 0. the unique endgame solution ----------------------------------")
print("    kappa = -c/alpha^5")
print("    S(v)  =", sp.factor(sp.expand(S)))
print("    R(v)  = S(v)/(v+1)^4")
chk("alpha^5 (v+1)^4 (3v(v+1)R' - 13R) == -c",
    sp.simplify(alpha**5*(v+1)**4*(3*v*(v+1)*sp.diff(R, v) - 13*R) + c) == 0)

# ---------------------------------------------------------------- 1. W~_-5
print("\n--- 1. propagate:  W~_-5 = alpha^6 U^6 v^9 R --------------------------")
g = alpha*U*(U-1)**8
Wt = sp.expand(sp.cancel(alpha**6*U**6*(U-1)**9*R.subs(v, U-1)))
print("    W~_-5(U) =", sp.factor(Wt))
chk("W~_-5 is a polynomial in U (no denominator)", sp.denom(sp.cancel(Wt)) == 1)
chk("W~_-5 == alpha^6 U^2 (U-1)^9 S(U-1)",
    sp.expand(Wt - alpha**6*U**2*(U-1)**9*S.subs(v, U-1)) == 0)
degW = sp.Poly(sp.expand(Wt), U).degree()
print("    deg_U W~_-5 =", degW)
chk("deg W~_-5 = 15", degW == 15)
uW = min(m[0] for m in sp.Poly(sp.expand(Wt), U).monoms())
print("    u(W~_-5) = ord_{U=0} W~_-5 =", uW)
chk("u(W~_-5) = 2 (exactly the order the 4th-order pole demands)", uW == 2)
chk("R recovered from W~_-5: v^39 W~/g^6 == R",
    sp.simplify(sp.cancel(((U-1)**39*Wt/g**6).subs(U, v+1) - R)) == 0)

# ---------------------------------------------------------------- 2. closure 1
print("\n--- 2. CLOSURE 1 - the ladder bound (E4) ----------------------------")
chk("E4 ladder bound is u(W~_-5) >= 3; the pole branch needs u = 2", uW == 2 < 3)
print("    => for any tower without accidental cancellation in the divisibility")
print("       ladder, the pole branch is INADMISSIBLE.  (E4 proves f(13) >= -3.)")

# ---------------------------------------------------------------- 3. closure 2
print("\n--- 3. CLOSURE 2 - the degree ledger / 13-realization ---------------")
# R = v^39 W~ / g^6 : deg(num) = 39 + deg W~, deg(den) = 6*deg g = 6*9 = 54
chk("deg g = 9", sp.Poly(sp.expand(g), U).degree() == 9)
chk("Session-11 ledger: a degree-13 polynomial R needs deg W~_-5 = 6*deg g - 26 = 28",
    6*9 - 26 == 28)
chk("the pole branch has deg W~_-5 = 15 != 28", degW == 15 != 28)
num, den = sp.fraction(sp.cancel(R))
mapdeg = max(sp.Poly(sp.expand(num), v).degree(), sp.Poly(sp.expand(den), v).degree())
print("    map-degree of R (as P^1 -> P^1) =", mapdeg)
chk("map-degree of R = 4, the framework demands 13", mapdeg == 4 and mapdeg != 13)
chk("R is not a polynomial, so it is not a degree-13 polynomial either",
    sp.Poly(sp.expand(den), v).degree() > 0)
print("    => R cannot realize the certified degree-13 Belyi map.")
print("    => CLOSURE 2 needs no genericity, no Theorem 3, no Belyi coefficients:")
print("       only  deg R = 4 != 13.")

# the near-miss sits at the SAME ledger degree
n3 = sp.Symbol('n3')
Wnm = sp.expand(n3*U**6*(U-1)**9)
chk("near-miss deg W~_-5 = 15 too: the pole branch lands in the same stratum",
    sp.Poly(Wnm, U).degree() == 15 == degW)
chk("but the near-miss has u(W~) = 6 (R regular) while the pole branch has u = 2",
    min(m[0] for m in sp.Poly(Wnm, U).monoms()) == 6 and uW == 2)

# ---------------------------------------------------------------- 4. what the
#     pole branch DOES satisfy - so the closure is honest about what it costs
print("\n--- 4. what the pole branch does satisfy (so the closure is honest) --")
chk("(U-1)^9 | W~_-5 : the v = 0 pole of R closes exactly, as Theorem 3 wanted",
    sp.rem(sp.Poly(sp.expand(Wt/alpha**6), U), sp.Poly((U-1)**9, U)) == 0)
chk("R has NO pole at v = 0", sp.simplify(sp.denom(sp.cancel(R)).subs(v, 0)) != 0)
chk("R's only pole is v = -1", sp.factor_list(sp.denom(sp.cancel(R)))[1][0][0] == v+1)
chk("W~_-5 respects the Session-15 degree caps (deg <= 27 + 22 = 49)", degW <= 49)
chk("the Keller constant enters only as an overall scalar: W~_-5 is linear in c",
    sp.simplify(sp.diff(Wt, c, 2)) == 0 and sp.simplify(sp.diff(Wt, c)) != 0)
print("    => rescaling c or alpha cannot change deg W~_-5 or the map-degree;")
print("       both closures are scale-invariant.")

# ---------------------------------------------------------------- 5. X = A~_4 - g^3 S_13
print("\n--- 5. the tower datum X = A~_4 - g^3 S_13 --------------------------")
X = sp.cancel(Wt/(2*g**3))
print("    X = W~_-5/(2 g^3) =", sp.factor(X))
def ordU(expr):
    """exact U-adic order at U = 0 of a rational expression"""
    n, d = sp.fraction(sp.cancel(sp.together(expr)))
    def mult(pp):
        pp = sp.expand(pp)
        if pp == 0: return sp.oo
        return min(m[0] for m in sp.Poly(pp, U).monoms())
    return mult(n) - mult(d)
uX = ordU(X)
print("    ord_{U=0}(X) =", uX, "   ord_{U=0}(W~_-5) =", uW, "   ord_{U=0}(g^3) = 3")
chk("X has a pole at U = 0 of order exactly 1", uX == -1)
chk("u(W~_-5) = 3 + u(X) is consistent", uW == 3 + uX)
print("    => the pole branch requires ord_{U=0}(g^3 S_13) = -1, i.e. f(13) = -4,")
print("       which E4 proves is impossible under the ladder (f(13) >= -3).")

print("\n--- 6. VERDICT ------------------------------------------------------")
print("    The (99,66) First Framework is EMPTY.")
print("    The archive's proof of that is INVALID as written (it evaluates a")
print("    polynomial identity at v = -1 on an R that need not be a polynomial,")
print("    and its supporting certificate searched only polynomials).")
print("    Two repaired closures, both established here:")
print("      closure 1  ladder bound        u(W~_-5) >= 3  vs  required 2")
print("      closure 2  degree ledger       deg R = 4      vs  required 13")
print("    Closure 2 is unconditional given the framework's 13-realization")
print("    demand; closure 1 additionally needs no realization layer at all.")

print()
for n, o in PASS:
    if not o: print("FAILED:", n)
assert all(o for _, o in PASS), "E5 FAILED"
print("E5: ALL %d CHECKS PASS" % len(PASS))
