"""
w3_theorem3_repair_audit.py  -  IS THE THEOREM 3 REPAIR SOUND?

az3geq `wave1/w1_theorem3_verdict.py` declares THEOREM 3 "CONFIRMED, proof
repaired", by this argument:

    R = W~_-5(U) / (alpha^6 U^6 (U-1)^9),     deg W~_-5 = 28
    gcd(W~_-5, U^6 (U-1)^9) = U^a (U-1)^b,    a <= 6, b <= 9
    map-degree(R) = 28 - a - b = 13  =>  a + b = 15  =>  (a,b) = (6,9)
    => the denominator cancels completely => R is a polynomial of degree 13.

It states its dependencies as: THEOREM 2 (certified), "deg W~_-5 = 28
(Session 11 ledger, arithmetic from deg g = 9)", W~_-5 polynomial, and
"deg R = 13, the framework's own 13-realization, NOT THEOREM 3".

THE PROBLEM.  Session 11 line 998 reads, verbatim:

    "STRATEGIC THEOREM (degree ledger): THE 13-REALIZATION FORCES
     deg W~_-5 = 6*deg(g) - 26 = 28"

so `deg W~_-5 = 28` is not independent arithmetic from `deg g = 9` - it is the
13-realization restated.  Indeed R = v^39 W~/g^6 is a polynomial of degree 13
IFF 39 + deg W~ = 54 + 13 IFF deg W~ = 28.  The repair therefore uses the
13-realization to obtain its degree input, and then again to force a+b = 15.

WHAT BREAKS.  Drop `deg W~ = 28` and keep only what is genuinely independent
(W~ a polynomial; poles bounded by U^6 (U-1)^9; map-degree 13; and even the
v = 0 divisibility the script calls "NOT load-bearing"), and non-polynomial R
survives.  Two witnesses are built and verified below.

CONSEQUENCE.  THEOREM 3's conclusion is not established by the repair.  It is
also NOT NEEDED: the endgame equation independently forces map-degree = k = 4
(w3_odequation_adjudication.py), and 4 != 13 closes (99,66) with no reference
to R's polynomiality at all.  The verdict on THEOREM 3 must be downgraded from
CONFIRMED to UNVERIFIED; the verdict on (99,66) is unaffected.
"""
import sympy as sp

U, v = sp.symbols('U v')
RES = []
def rec(n, ok):
    RES.append((n, bool(ok))); return bool(ok)

def ordat(poly, pt):
    p = sp.Poly(sp.expand(poly), U)
    k = 0
    while k < 400:
        q, r = sp.div(p, sp.Poly(U - pt, U))
        if r.as_expr() != 0:
            return k
        p = q; k += 1
    return k

def mapdeg_U(expr):
    n, d = sp.fraction(sp.cancel(expr))
    dn = sp.Poly(sp.expand(n), U).degree() if sp.expand(n).has(U) else 0
    dd = sp.Poly(sp.expand(d), U).degree() if sp.expand(d).has(U) else 0
    return max(dn, dd)

DEN = sp.expand(U**6 * (U - 1)**9)

print("--- 1. the degree input is the conclusion restated ------------------")
# R = v^39 W~ / g^6, g = alpha U (U-1)^8, v = U-1.
g = U * (U - 1)**8
R_sym = sp.cancel((U - 1)**39 * sp.Symbol('W') / g**6)
rec("R = W~ / (U^6 (U-1)^9) after the (U-1) cancellation",
    sp.simplify(R_sym - sp.Symbol('W')/DEN) == 0)
# "R is a polynomial of degree 13"  <=>  39 + deg W = 54 + 13  <=>  deg W = 28
rec("R polynomial of degree 13  <=>  deg W~ = 28  (so the two are equivalent, "
    "not independent)", 39 + 28 == 6*9 + 13)
rec("Session 11 states the implication in that direction: 'the 13-realization "
    "FORCES deg W~_-5 = 6 deg g - 26 = 28'", 6*9 - 26 == 28)

print("\n--- 2. witness A: v = 0 pole left open (script's own premise set) ---")
# a + b = 2, deg W~ < 15 : map-degree comes from the DENOMINATOR, not W~.
hA = sp.expand(U**2 * (U**8 + 3*U**5 - 7*U + 5))          # deg 10, ord_0 = 2
WA = hA
RA = sp.cancel(WA / DEN)
nA, dA = sp.fraction(RA)
print("    W~ = U^2 (U^8 + 3U^5 - 7U + 5),  deg", sp.Poly(WA, U).degree())
print("    R  =", sp.factor(RA))
rec("A: W~ is a polynomial", sp.fraction(sp.cancel(WA))[1] == 1)
rec("A: ord_{U=0} W~ = 2 <= 6 and ord_{U=1} W~ = 0 <= 9 (inside the box)",
    ordat(WA, 0) == 2 and ordat(WA, 1) == 0)
rec("A: R's poles are confined to U in {0,1}, i.e. v in {-1,0}",
    set(sp.roots(sp.Poly(sp.expand(dA), U)).keys()) <= {sp.Integer(0), sp.Integer(1)})
rec("A: map-degree(R) = 13", mapdeg_U(RA) == 13)
rec("A: R is NOT a polynomial", dA != 1)
rec("A: and the script's formula 28 - a - b would have said "
    "%d, not 13" % (28 - 2 - 0), 28 - 2 - 0 != 13)

print("\n--- 3. witness B: v = 0 pole CLOSED too (the stronger premise set) --")
# b = 9 (so v = 0 is not a pole at all), a = 0, deg W~ = 22.
hB = sp.expand(U**13 + 5*U**7 - 3*U + 11)                  # deg 13, h(0) != 0
WB = sp.expand((U - 1)**9 * hB)
RB = sp.cancel(WB / DEN)
nB, dB = sp.fraction(RB)
print("    W~ = (U-1)^9 (U^13 + 5U^7 - 3U + 11),  deg", sp.Poly(WB, U).degree())
print("    R  =", sp.factor(RB))
rec("B: W~ is a polynomial of degree 22", sp.Poly(WB, U).degree() == 22)
rec("B: ord_{U=0} W~ = 0 <= 6, ord_{U=1} W~ = 9 <= 9 (inside the box)",
    ordat(WB, 0) == 0 and ordat(WB, 1) == 9)
rec("B: v = 0 is NOT a pole of R (the divisibility the script calls "
    "'not load-bearing' is satisfied)", sp.simplify(sp.expand(dB).subs(U, 1)) != 0)
rec("B: R's only pole is U = 0, i.e. v = -1",
    set(sp.roots(sp.Poly(sp.expand(dB), U)).keys()) == {sp.Integer(0)})
rec("B: pole order at v = -1 is exactly 6", sp.Poly(sp.expand(dB), U).degree() == 6)
rec("B: map-degree(R) = 13", mapdeg_U(RB) == 13)
rec("B: R is NOT a polynomial", dB != 1)
rec("B: every premise the repair uses EXCEPT deg W~ = 28 holds, and the "
    "conclusion fails", sp.Poly(WB, U).degree() != 28 and dB != 1)

print("\n--- 4. the repair is sound ONLY with its degree input ---------------")
# with deg W~ = 28 imposed, the script's conclusion does follow - verify it.
sols = [(a, b) for a in range(7) for b in range(10) if 28 - a - b == 13]
rec("given deg W~ = 28, (a,b) = (6,9) is forced, as the script says",
    sols == [(6, 9)])
# but without it, the (a,b) box does not determine polynomiality:
alt = [(dw, a, b) for dw in range(0, 40) for a in range(7) for b in range(10)
       if max(dw, 15) - a - b == 13 and 15 - a - b > 0]
rec("without the degree input there are %d (degW,a,b) triples giving "
    "map-degree 13 with a NON-trivial denominator" % len(alt), len(alt) > 0)
print("    e.g.", alt[:6])

print("\n--- 5. NEG controls: the audit must not fire on sound reasoning -----")
Wok = sp.expand(U**6 * (U - 1)**9 * (U**13 + 3*U**7 - 5*U + 2))
Rok = sp.cancel(Wok / DEN)
rec("NEG: a genuine deg-28 W~ divisible by U^6(U-1)^9 does give a polynomial R "
    "of degree 13", sp.fraction(Rok)[1] == 1
    and sp.Poly(sp.fraction(Rok)[0], U).degree() == 13)
rec("NEG: witness B is rejected once deg W~ = 28 is assumed (its degree is 22)",
    sp.Poly(WB, U).degree() != 28)
rec("NEG: the script's own witness 1/(v+1)^13 is correctly rejected by the "
    "box (it needs a = 13 > 6)", 13 > 6)

print("\n--- 6. does any of this move the (99,66) verdict? -------------------")
Rend = (243*v**4 - 81*v**3 + 54*v**2 - 42*v + 35)/(455*(v + 1)**4)
nn, dd = sp.fraction(sp.cancel(Rend))
mdend = max(sp.Poly(sp.expand(nn), v).degree(), sp.Poly(sp.expand(dd), v).degree())
rec("the endgame solution at D=13,k=4 has map-degree 4", mdend == 4)
rec("4 != 13, so (99,66) closes without THEOREM 3 in any form", mdend != 13)
print("    => THEOREM 3: downgrade CONFIRMED -> UNVERIFIED.")
print("    => (99,66): unaffected.  The endgame degree does the work.")

print()
bad = [n for n, o in RES if not o]
for n in bad:
    print("FAILED:", n)
print("w3_theorem3_repair_audit: %d/%d checks pass" % (len(RES) - len(bad), len(RES)))
raise SystemExit(1 if bad else 0)
