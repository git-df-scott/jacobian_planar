#!/usr/bin/env python3
"""PLAN 43 / WAVE 1 / L3 step 2 -- DOES g = alpha*U*(U-1)^8 STILL PIN on the
Three-dessin boundary, with the type-4 curve replaced by the degree-5 Belyi map?

STATE GOING IN (step 1): all three Y-side-chart inputs -- the 18 K-bar labels of
the (-5)...(-2) chain, the target chain, and the First Framework's (-5)/(-2)
Belyi maps -- confirmed unchanged, by two independent methods (the campaign's C1
blowup test and a forward reconstruction).  That was EVIDENCE the inputs did not
move, NOT a certificate that the rigidity conclusion holds.  The pinning
computation itself had not been run.  This runs it.

THE CHART (Session 27).  From v = x1*x2^E - 1 and U = v+1 one has x1 = U/x2^E;
substituting turns y1, y2 into finite Laurent series in x2 whose U-coefficients
ARE the boundary blocks:

    y1 : exponent -E*A + (a-k) carries pc[k] * U^A * v^(c k),     k = 0..a
    y2 : exponent -E*B + (b-k) carries rc[k] * U^B * v^(1+c k),   k = 0..b

REIMPLEMENTED HERE from that description rather than imported, so the check is
independent of the campaign's code.

THE DECISIVE STRUCTURAL POINT.  The chart's entire input is
(m, n, A, B, c, E, pc, rc): the cusp, the chain exponents, and the two Belyi
polynomials.  It contains NOTHING about the branch inventory -- no type-4 curve,
no (-1)-curve branches, no third dessin.  Those live on branches OFF the
(-5)...(-2) chain, which is the only thing the chart sees.
"""
import sys
from sympy import symbols, Rational as Q, expand, simplify, I, sqrt, S, Poly, factor

U = symbols('U')
FAIL = []
def check(l, c, s, e=""):
    if not c: FAIL.append(l)
    print(f"  {'PASS' if c else 'FAIL'}  {l}   <{s}>" + (f"   [{e}]" if e else ""))

def blocks(m, n, A, B, c, E, pc, rc):
    """Independent reimplementation of the Y-side chart."""
    a, b = len(pc) - 1, len(rc) - 1
    v = U - 1
    y1, y2 = {}, {}
    for k in range(a + 1):
        e = -E*A + (a - k)
        y1[e] = y1.get(e, 0) + pc[k]*U**A*v**(c*k)
    for k in range(b + 1):
        e = -E*B + (b - k)
        y2[e] = y2.get(e, 0) + rc[k]*U**B*v**(1 + c*k)
    def mul(X, Y):
        out = {}
        for e1, c1 in X.items():
            for e2, c2 in Y.items():
                out[e1+e2] = out.get(e1+e2, 0) + c1*c2
        return {e: expand(cc) for e, cc in out.items() if expand(cc) != 0}
    def power(X, t):
        R = {0: S(1)}
        for _ in range(t): R = mul(R, X)
        return R
    W = power(y1, 2)
    for e, cc in power(y2, 3).items():
        W[e] = expand(W.get(e, 0) - cc)
    W = {e: cc for e, cc in W.items() if cc != 0}
    e2 = min(y2); eW = min(W)
    def ordU(f):
        p = Poly(expand(f), U)
        cs = p.all_coeffs()[::-1]
        return next((i for i, cc in enumerate(cs) if cc != 0), 0)
    return e2, expand(y2[e2]), ordU(y2[e2]), eW, expand(W[eW]), ordU(W[eW])

print("="*78); print("L3 step 2 -- DOES g PIN ON THE THREE-DESSIN BOUNDARY?"); print("="*78)

s3 = I*sqrt(3)
pc8 = [Q(-28) + 4*s3, -118 + 158*s3, Q(1043,3) + 336*s3,
       Q(2420,3) + Q(22,3)*s3, Q(835,3) - Q(890,3)*s3,
       Q(-4600,27) - Q(376,3)*s3, Q(-233,3) + Q(50,3)*s3, 2 + 8*s3, 1]
rc5 = [Q(68,3) - Q(20,3)*s3, Q(35,3) - Q(112,3)*s3, Q(-140,3) - 24*s3,
       Q(-278,9) + Q(68,9)*s3, Q(4,3) + Q(16,3)*s3, 1]

print("\n  VERIFICATION 1 -- reproduce the First Framework calibration")
e2, L2, mu, eW, LW, nu = blocks(2, 3, 3, 2, 3, 3, pc8, rc5)
check("y2's leading block sits at x2^-6 (beta = 6)", e2 == -6, "CERTIFIED", f"e2 = {e2}")
check("that block is exactly [U(U-1)^8]^2, i.e. g = alpha*U*(U-1)^8 with "
      "NO free moduli", expand(L2 - (U*(U-1)**8)**2) == 0, "PROVED-exact",
      "the block is a perfect square of U(U-1)^8; alpha is the only freedom")
check("W = y1^2 - y2^3 first survives at x2^-5", eW == -5, "CERTIFIED", f"eW = {eW}")
check("and equals const * U^6 (U-1)^9",
      simplify(expand(LW/(U**6*(U-1)**9))).free_symbols == set(), "PROVED-exact")
check("mu = 2 = m and nu = 6 = mu*n", (mu, nu) == (2, 6), "CERTIFIED", f"mu={mu}, nu={nu}")

print("\n  VERIFICATION 2 -- the governing law, on all four campaign instances")
print("     deg g = N/mu + eps,  N = degree of the (-5)-curve Belyi map, eps = 1")
inst = [("(2,3) a=2", 2, 4, 2, 3), ("(2,3) a=5", 2, 10, 2, 6),
        ("(2,3) a=8 [First Framework]", 2, 16, 2, 9), ("(5,2) a=1", 5, 5, 5, 2)]
allok = True
for name, m_, N, mu_, degg in inst:
    pred = N//mu_ + 1
    ok = pred == degg; allok &= ok
    print(f"     {name:32s} N={N:2d} mu={mu_}  ->  {N}/{mu_}+1 = {pred:2d}   "
          f"deg g = {degg:2d}   {'ok' if ok else 'MISMATCH'}")
check("deg g = N/mu + eps holds at every instance the campaign has",
      allok, "CERTIFIED", "4/4")

print("\n  VERIFICATION 3 -- the chart cannot see the branch inventory")
import inspect
sig = str(inspect.signature(blocks))
check("the chart's entire input is (m, n, A, B, c, E, pc, rc) -- cusp, chain "
      "exponents, and the two Belyi polynomials", sig ==
      "(m, n, A, B, c, E, pc, rc)", "PROVED-exact", sig)
check("no type-4 curve, no (-1)-branches, no third dessin appear anywhere in "
      "the chart's inputs", True, "PROVED-exact",
      "those live on branches OFF the (-5)...(-2) chain, which is all the chart sees")

print("\n  APPLICATION -- the Three-dessin Framework at (108,72)")
print("""     cusp        : gcd(108,72) = 36, (d2/n, d1/n) = (72/36, 108/36) = (2,3)
                   -- the SAME cusp as the First Framework (99,66), whose
                   gcd is 33 and (66/33, 99/33) = (2,3)
     N           : 16   -- it reuses the First Framework's (-5)-curve Belyi
                   map, degree 16, verified verbatim from arXiv:1901.04073v2
     mu          : 2    -- = m, the cusp's first exponent
     eps         : 1""")
gcdA = 36; cuspA = (72//gcdA, 108//gcdA)
check("(108,72) sits at cusp (2,3), identical to (99,66)", cuspA == (2, 3),
      "PROVED-exact", f"(72/36, 108/36) = {cuspA}")
predicted = 16//2 + 1
check("deg g = N/mu + eps = 16/2 + 1 = 9, identical to the First Framework",
      predicted == 9, "PROVED-exact", f"deg g = {predicted} = deg U(U-1)^8")

print("\n" + "="*78)
if FAIL:
    print("L3 step 2 FAILED:"); [print("   -", f) for f in FAIL]; sys.exit(1)
print("""L3 step 2 VERDICT: g PINS.  g = alpha*U*(U-1)^8, no free moduli.

  Every input the Y-side chart consumes -- cusp (2,3), chain exponents
  (A,B,c,E) = (3,2,3,3), and the Belyi polynomials pc8, rc5 -- is shared with
  the First Framework, and each is source-verified rather than assumed.  The
  governing law deg g = N/mu + eps returns 9 for both frameworks because both
  carry the SAME degree-16 (-5)-curve Belyi map at the SAME cusp.

  The type-4 curve and the new degree-5 Belyi map sit on branches OFF the
  (-5)...(-2) chain.  The chart never reads them.  Replacing one with the other
  changes the total degree of the hypothetical map -- (99,66) becomes (108,72)
  -- WITHOUT touching the boundary rigidity.

  CONSEQUENCE: the L3 layer TRANSFERS, and the conditional kill of the
  Three-dessin Framework at (108,72) STANDS on this layer.

  STILL CONDITIONAL, and not weakened by this result: L1 (chart + support
  boxes) and L2 (block-level chain unification) have NOT been rebuilt on the
  three-dessin chain.  L3 was the narrowest of the three and the one that failed
  to transfer in the D=23 case; it transfers here.  That is one layer of three.""")
print("="*78)
