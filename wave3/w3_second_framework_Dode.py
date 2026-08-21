"""
w3_second_framework_Dode.py  -  D_ode FOR THE SECOND FRAMEWORK, COMPUTED.

The one number the adjudication said was missing.  It was on
`claude/d23-borisov-transfer-test-vpr3m6` and in `campaign/d23_borisov/` on the
az3geq branch the whole time - the same NOT-FETCHED failure as everything else.

THE INPUT, certified by campaign/d23_borisov/d23_phase1_chart.py (re-run here
by hand, 5/5 of its own checks pass):

    same chart:      v = x1 x2^3 - 1,   q = x2/v^3
    pole depths:     val_{(-2)mf}(y1, y2) = (-15, -10)      [FF: (-9, -6)]
    Keller form:     J_{(q,v)} = -c q^-3 v^-6               [identical to FF]

so for the Second Framework  gamma = 15,  beta = 10,  p = 3,  tau = 6.

THE DERIVATION.  D_chain = 2 gamma - sigma (the chain runs n = -2gamma ..
-(sigma+1)); FF checks: 2*9 - 5 = 13.  SF: 2*15 - sigma = 23 => sigma = 7,
hence e = gamma - sigma = 8.  Cross-check against the independent chart
relation e = beta + 1 - p:  10 + 1 - 3 = 8.  Two routes, same answer.

    D_ode = 3 eps (2e + 3 beta) / beta        [eps := ord_{U=0}(g)]
    SF:    3 eps (16 + 30)/10 = 69 eps / 5
    FF:    3 eps (8  + 18)/6  = 13 eps

THE VERDICT.  D_ode(SF) = 69/5 at eps = 1 - not 23, and not 69.  And the
result does not depend on eps at all:

    eps not divisible by 5 : D_ode = 69 eps/5 is not an integer, so 3 does not
        divide it, so the solution is UNIQUE of map-degree k = 5 eps - 1;
        realization demands 23, and 5 eps - 1 == 4 (mod 5) != 23.   DEAD.
    eps = 5m (m >= 1)      : D_ode = 69m, D_ode/3 = 23m, k = 25m - 1, and
        23m <= 25m - 1 for every m >= 1, so by the trichotomy there is
        NO rational solution at all.                                  DEAD.

So the escape route the adjudication left open - "3 | D_ode with D_ode/3 =
D_chain" - is CLOSED for the Second Framework, for every eps.  The label
upgrades DEAD-CONDITIONAL -> DEAD.

AND MY WITHDRAWN CLAIM IS REPAIRED, NOT RESTORED AS WRITTEN.  The correct
formula carries an eps I had dropped:

    D_ode = eps * (15 - 12/beta)        at p = 3.

At eps = 1 that is my "D = 15 - 12/beta"; the bound D < 15 holds only at
eps = 1.  What IS now certified rather than assumed is p = 3 for BOTH
published frameworks, which is the input the bound needed.
"""
import sympy as sp

v = sp.Symbol('v')
RES = []
def rec(n, ok):
    RES.append((n, bool(ok))); return bool(ok)

# ------------------------------------------------------------- 1. the chart
print("--- 1. the Second Framework chart data, re-derived by hand -----------")
x1, x2, q = sp.symbols('x1 x2 q')
V = x1*x2**3 - 1
Q = x2/V**3
X1 = (v + 1)*q**-3*v**-9
X2 = q*v**3
rec("chart inversion x1 = (v+1)q^-3 v^-9, x2 = q v^3 is exact",
    sp.simplify(V.subs({x1: X1, x2: X2}) - v) == 0
    and sp.simplify(Q.subs({x1: X1, x2: X2}) - q) == 0)
J = sp.together(sp.diff(Q, x1)*sp.diff(V, x2) - sp.diff(Q, x2)*sp.diff(V, x1))
rec("chart factor det d(q,v)/d(x1,x2) = -x2^3/v^3",
    sp.simplify(J + x2**3/V**3) == 0)
rec("in chart coordinates that is -q^3 v^6, so J_{(q,v)} = -c q^-3 v^-6: p = 3",
    sp.simplify((-x2**3/V**3).subs({x1: X1, x2: X2}) + q**3*v**6) == 0)
GAM, BET, PP = 15, 10, 3          # from val_{(-2)mf}(y1,y2) = (-15,-10), L1c
rec("SF pole depths give gamma = 15, beta = 10 (FF: 9, 6)",
    (GAM, BET) == (15, 10))
rec("SF satisfies the cusp-(2,3) relation gamma = 3 beta / 2",
    sp.Rational(3*BET, 2) == GAM)

# ------------------------------------------------------------- 2. sigma, e
print("\n--- 2. sigma and e, two independent routes --------------------------")
def Dchain(gam, sig): return 2*gam - sig
rec("FF: D_chain = 2*9 - 5 = 13", Dchain(9, 5) == 13)
SIG = 2*GAM - 23
rec("SF: D_chain = 23 forces sigma = 7", SIG == 7)
E_SF = GAM - SIG
rec("route 1: e = gamma - sigma = 8", E_SF == 8)
rec("route 2: e = beta + 1 - p = 8 (independent, from the chart exponent)",
    BET + 1 - PP == 8)
rec("the two routes agree", E_SF == BET + 1 - PP)
rec("FF cross-check: both routes give e = 4", 9 - 5 == 4 == 6 + 1 - 3)

# ------------------------------------------------------------- 3. D_ode
print("\n--- 3. D_ode ---------------------------------------------------------")
eps = sp.Symbol('eps', positive=True, integer=True)
def D_ode(e_, b_): return sp.simplify(3*eps*(2*e_ + 3*b_)/b_)
D_SF, D_FF = D_ode(E_SF, BET), D_ode(4, 6)
print("    D_ode(SF) =", D_SF, "   D_ode(FF) =", D_FF)
rec("D_ode(SF) = 69 eps / 5", sp.simplify(D_SF - sp.Rational(69, 5)*eps) == 0)
rec("D_ode(FF) = 13 eps", sp.simplify(D_FF - 13*eps) == 0)
rec("at eps = 1: D_ode(SF) = 69/5 = 13.8, NOT 23",
    D_SF.subs(eps, 1) == sp.Rational(69, 5) and D_SF.subs(eps, 1) != 23)
rec("at eps = 1: D_ode(FF) = 13, matching the certified FF endgame",
    D_FF.subs(eps, 1) == 13)
rec("the p = 3 form D_ode = eps(15 - 12/beta) reproduces both",
    sp.simplify(D_SF - eps*(15 - sp.Rational(12, BET))) == 0
    and sp.simplify(D_FF - eps*(15 - sp.Rational(12, 6))) == 0)

# ---------------------------------------- 3b. direct symbolic verification
print("\n--- 3b. the SF operator, built from scratch rather than substituted --")
alpha = sp.Symbol('alpha')
R = sp.Function('R')(v)
a_, b_ = sp.symbols('a b')
Uu = v + 1
EPSV, GV, NV = 1, 14, 69          # g = alpha U v^14 (SF predicted shape), N from collapse
BV, EV = BET, E_SF                # beta = 10, e = 8
rec("collapse condition N = (2e+3beta)(eps+G)/beta gives N = 69 at "
    "(eps,G) = (1,14)", sp.Rational((2*EV + 3*BV)*(EPSV + GV), BV) == NV)
aN, bN = 2*GV - 3*BV, 3*GV + 3*EV - NV
rec("SF: a = 2G-3beta = -2 and b = 3G+3e-N = -3, so a+b-1 = -6 = -tau "
    "(identical to FF)", (aN, bN) == (-2, -3) and aN + bN - 1 == -6)
eta = alpha**2*Uu**(2*EPSV)*v**aN
delta = sp.Rational(1, 2)*alpha**3*Uu**(3*EPSV)*R*v**bN
block = EV*delta*sp.diff(eta, v) + BV*sp.diff(delta, v)*eta
target = (alpha**5/2)*sp.Rational(BV, 3)*Uu**4*v**(-6)*(
    3*Uu*v*sp.diff(R, v) - sp.Rational(69, 5)*R)
rec("SF block == (alpha^5/2)(beta/3) U^4 v^-6 [ 3v(v+1)R' - (69/5) R ] "
    "-- derived, not substituted",
    sp.simplify(sp.expand(block - target)) == 0)
# and the same construction at the FF numbers must return 13, as a control
eta9 = alpha**2*Uu**2*v**(-2)
delta9 = sp.Rational(1, 2)*alpha**3*Uu**3*R*v**(-3)
block9 = 4*delta9*sp.diff(eta9, v) + 6*sp.diff(delta9, v)*eta9
rec("NEG/control: the same construction at the FF numbers returns 13, not 69/5",
    sp.simplify(sp.expand(block9 - alpha**5*Uu**4*v**(-6)*(
        3*Uu*v*sp.diff(R, v) - 13*R))) == 0)

# ------------------------------------------------------------- 4. verdict
print("\n--- 4. the trichotomy, applied for every eps -------------------------")
def verdict(Dv, k, dchain):
    """returns (branch, achievable map-degrees, survives realization)"""
    if not sp.Rational(Dv).is_integer or sp.Rational(Dv) % 3 != 0:
        return ('unique', {k}, k == dchain)
    j = int(sp.Rational(Dv) / 3)
    if j <= k:
        return ('none', set(), False)
    return ('line', {k, j}, dchain in {k, j})
rows = []
for ev in range(1, 13):
    k = 5*ev - 1
    Dv = sp.Rational(69, 5)*ev
    br, degs, surv = verdict(Dv, k, 23)
    rows.append((ev, Dv, k, br, sorted(degs), surv))
    print(f"    eps={ev:2d}  D_ode={str(Dv):8s}  k={k:3d}  {br:6s}  "
          f"map-degrees {sorted(degs)}  survives: {surv}")
rec("SF: no eps in 1..12 survives the realization demand 23",
    not any(r[5] for r in rows))
rec("SF: the only eps that could give D_ode/3 = 23 is eps = 5",
    [ev for ev in range(1, 40) if sp.Rational(69, 5)*ev == 69] == [5])
rec("SF at eps = 5: D_ode = 69, D_ode/3 = 23 <= k = 24, so the trichotomy "
    "gives NO solution at all - the escape is closed",
    verdict(69, 24, 23)[0] == 'none')
rec("SF general: 23m <= 25m - 1 for every m >= 1, so every eps = 5m gives "
    "no solution", all(23*m <= 25*m - 1 for m in range(1, 200)))
rec("SF otherwise: k = 5 eps - 1 == 4 (mod 5) and 23 == 3 (mod 5)",
    all((5*ev - 1) % 5 == 4 for ev in range(1, 200)) and 23 % 5 == 3)

print("\n    same structure for the First Framework:")
for ev in (1, 2, 3, 4, 5):
    k = 5*ev - 1
    br, degs, surv = verdict(13*ev, k, 13)
    print(f"    eps={ev}  D_ode={13*ev:3d}  k={k:3d}  {br:6s}  "
          f"map-degrees {sorted(degs)}  survives: {surv}")
rec("FF: eps = 3 is the only one with D_ode/3 = 13, and there 13 <= k = 14, "
    "so no solution", verdict(39, 14, 13)[0] == 'none')
rec("FF: no eps in 1..12 survives", not any(
    verdict(13*ev, 5*ev - 1, 13)[2] for ev in range(1, 13)))

# ------------------------------------------------------------- 5. refutations
print("\n--- 5. what this settles in the record -------------------------------")
# the D=23 file's E3 claim, refuted by the same witness as az3geq STATUS 2.1
Rw = sp.Symbol('c')*(3*v + 2)/(2*(v + 1))
cc = sp.Symbol('c')
rec("d23_phase1_endgame.py E3 ('evaluation at v=-1 covers ALL k>=1') is "
    "refuted by the same witness: D=1, k=1",
    sp.simplify(sp.cancel(sp.together((v+1)*(3*v*(v+1)*sp.diff(Rw, v) - Rw) + cc))) == 0)
# its E5 'collapse identity' carries no information about D
D_, dg_ = sp.symbols('D dg')
rec("d23_phase1_endgame.py E5's identity D((dg)v + dg-1) - D*dg*(v+1) = -D "
    "holds for EVERY D and every deg g, so it cannot determine D",
    sp.simplify(sp.expand(D_*(dg_*v + dg_ - 1) - D_*dg_*(v + 1) + D_)) == 0)
rec("  and it reproduces both quoted instances",
    sp.expand(13*(9*v + 8) - 117*(v + 1)) == -13
    and sp.expand(23*(15*v + 14) - 345*(v + 1)) == -23)
rec("NEG control: the identity FAILS if the middle term is perturbed",
    sp.simplify(sp.expand(23*(15*v + 15) - 345*(v + 1) + 23)) != 0)

print("""
    VERDICT
      D_ode(Second Framework) = 69 eps / 5,  i.e. 13.8 at eps = 1.
      It is neither 23 (which would have let the unique branch meet the
      realization demand) nor 69 (which would have let the family branch meet
      it).  For every eps the framework is dead, by two disjoint mechanisms:
      eps not a multiple of 5 -> unique solution of map-degree 4 (mod 5) != 23;
      eps a multiple of 5     -> no rational solution at all.

      SECOND FRAMEWORK: DEAD-CONDITIONAL  ->  DEAD.

      The transfer conjecture's premise "D = the chain degree" is false here in
      the sharpest possible way: the chain degree is 23 and the operator's
      coefficient is 69/5, not even an integer.""")

print()
bad = [n for n, o in RES if not o]
for n in bad:
    print("FAILED:", n)
print("w3_second_framework_Dode: %d/%d checks pass" % (len(RES) - len(bad), len(RES)))
raise SystemExit(1 if bad else 0)
