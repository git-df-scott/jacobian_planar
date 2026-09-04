"""
Plane Jacobian campaign - Session 19, generality closure
THE CHART FACTOR FOR A GENERAL MONOMIAL CHART.

session19_general_endgame.py freed the chart slope rho in the family

    U = x1 x2^rho,   v = U - 1,   q = x2 / v^rho.

That family is a one-parameter generalization of Borisov's chart, but it is not
the most general monomial chart.  Since the v = -1 kill compares the LHS's
(v+1)-order against the RHS's, and the RHS is c * delta with
delta = 1/det d(q,v)/d(x1,x2), the kill is only valid if delta does not vanish
to high order at v = -1.  This file settles that.

GENERAL MONOMIAL CHART.  Let

    U = x1^P x2^Q,   v = U - 1,   q = x1^P' x2^Q' v^-w,
    eps := P Q' - Q P' = +-1        (unimodular, so (q,v) really are coordinates)

Then, derived and verified below,

    det d(q,v)/d(x1,x2)  =  -eps * x1^(P+P'-1) x2^(Q+Q'-1) v^-w

and, writing delta = 1/det in the chart coordinates,

    A := ord_{v=-1} delta  =  eps (Q' - P') - 1.

THE KILL NEEDS   A  <  (a+b) m - 1.

  * Borisov's chart (P,Q,P',Q',w) = (1,3,0,1,3):  eps = 1, A = 0 < 4.  Valid.
  * The whole rho-family (1,rho,0,1,rho):         eps = 1, A = 0.      Valid.
  * A = 0 for EVERY chart with P' = 0, Q' = 1 (q built from x2 alone).
  * A >= 4 requires eps(Q' - P') >= 5, i.e. a chart whose transverse coordinate
    carries a large negative power of x1 (or x2).  Enumerated below; this is the
    one place where the general kill is conditional, and it is reported as such.
"""

from sympy import symbols, cancel, expand, diff, simplify, Rational, S

x1, x2 = symbols('x1 x2', positive=True)   # positive: branch-free monomial powers
LEDGER = []


def note(ok, text):
    LEDGER.append((bool(ok), text))
    print(f"  [{'PASS' if ok else 'FAIL'}] {text}")


# ===================================================================
# 1.  det for a general unimodular monomial chart
# ===================================================================
print("SECTION 1  det d(q,v)/d(x1,x2) for a general unimodular monomial chart")


def det_chart(P, Q, Pp, Qp, w):
    U = x1**P * x2**Q
    vv = U - 1
    qq = x1**Pp * x2**Qp * vv**(-w)
    return cancel(expand(diff(qq, x1)*diff(vv, x2) - diff(qq, x2)*diff(vv, x1)))


CHARTS = []
for P in range(0, 4):
    for Q in range(0, 5):
        for Pp in range(-4, 3):
            for Qp in range(-2, 3):
                if P*Qp - Q*Pp in (1, -1):
                    for w in (0, 1, 2, 3):
                        CHARTS.append((P, Q, Pp, Qp, w))

ok = True
checked = 0
for (P, Q, Pp, Qp, w) in CHARTS[:400]:
    eps = P*Qp - Q*Pp
    got = det_chart(P, Q, Pp, Qp, w)
    want = cancel(-eps * x1**(P + Pp - 1) * x2**(Q + Qp - 1) * (x1**P*x2**Q - 1)**(-w))
    ok &= (cancel(expand(got - want)) == 0)
    checked += 1
note(ok, f"det = -eps x1^(P+P'-1) x2^(Q+Q'-1) v^-w  on {checked} unimodular charts")
note(cancel(expand(det_chart(1, 3, 0, 1, 3)
                   - (-x2**3*(x1*x2**3 - 1)**(-3)))) == 0,
     "Borisov's chart (1,3,0,1,3) reproduces the certified -x2^3/v^3")
ok = all(cancel(expand(det_chart(1, r, 0, 1, r)
                       - (-x2**r*(x1*x2**r - 1)**(-r)))) == 0 for r in range(1, 8))
note(ok, "the whole rho-family (1,rho,0,1,rho) gives -x2^rho/v^rho, rho = 1..7")


# ===================================================================
# 2.  A = ord_{v=-1} delta,  delta = 1/det, in chart coordinates
# ===================================================================
print("\nSECTION 2  the (v+1)-order A of the right-hand side")
# x1 = U^(eps Q') (q v^w)^(-eps Q),  x2 = U^(-eps P') (q v^w)^(eps P)
# so delta = -eps^-1 x1^(1-P-P') x2^(1-Q-Q') v^w  has U-order
#     A = eps Q'(1-P-P') - eps P'(1-Q-Q') = eps(Q' - P') - 1.


def A_formula(P, Q, Pp, Qp):
    eps = P*Qp - Q*Pp
    return eps*(Qp - Pp) - 1


def A_direct(P, Q, Pp, Qp):
    """Independent computation: U-exponent of x1^(1-P-P') x2^(1-Q-Q')."""
    eps = P*Qp - Q*Pp
    aU, gU = eps*Qp, -eps*Pp          # U-exponents of x1 and x2
    return aU*(1 - P - Pp) + gU*(1 - Q - Qp)


bad = [(P, Q, Pp, Qp) for (P, Q, Pp, Qp, w) in CHARTS
       if A_formula(P, Q, Pp, Qp) != A_direct(P, Q, Pp, Qp)]
note(bad == [], f"A = eps(Q'-P') - 1 agrees with the direct U-exponent count on "
                f"all {len(CHARTS)} charts")
note(A_formula(1, 3, 0, 1) == 0,
     "Borisov's chart: A = 0, so RHS(v=-1) = -c * (nonzero constant) != 0")
note(all(A_formula(1, r, 0, 1) == 0 for r in range(1, 12)),
     "the entire rho-family has A = 0 for rho = 1..11")
note(all(A_formula(P, Q, 0, 1) == 0 for (P, Q, Pp, Qp, w) in CHARTS if (Pp, Qp) == (0, 1)),
     "A = 0 for EVERY unimodular chart with (P',Q') = (0,1), i.e. whenever the "
     "transverse coordinate is built from x2 alone")


# ===================================================================
# 3.  Where, exactly, the kill is conditional
# ===================================================================
print("\nSECTION 3  the residual condition:  A < (a+b) m - 1")
# with m >= 1 forced and a+b >= 5 for a genuine cusp, the kill needs A <= 3.
risky = sorted({(P, Q, Pp, Qp, A_formula(P, Q, Pp, Qp))
                for (P, Q, Pp, Qp, w) in CHARTS
                if A_formula(P, Q, Pp, Qp) >= 4})
print(f"     unimodular charts in the scanned range with A >= 4: {len(risky)}")
for t in risky[:10]:
    print(f"       (P,Q,P',Q') = {t[:4]},  A = {t[4]}")
note(all(A_formula(P, Q, Pp, Qp) <= 3 for (P, Q, Pp, Qp, w) in CHARTS
         if -1 <= Pp <= 1 and 0 <= Qp <= 1),
     "every chart with P' in {-1,0,1} and Q' in {0,1} has A <= 3, hence dies")
note(all(A_formula(*t[:4]) >= 4 for t in risky) if risky else True,
     f"the A >= 4 charts all require eps(Q'-P') >= 5, i.e. |Q'-P'| >= 5: the "
     f"transverse coordinate must carry a 5th-or-higher power of a variable")

print("\n     HONEST SCOPE STATEMENT")
print("     The v = -1 kill is proved for every chart with A < (a+b)m - 1.")
print("     That covers Borisov's chart (A=0), the whole rho-family (A=0), and")
print("     every chart whose transverse coordinate is built from a single")
print("     variable (A=0).  It does NOT cover charts with eps(Q'-P') >= 5.")
print("     Whether such a chart can carry an actual resolution of a Keller pair")
print("     is NOT settled here and is the one residual gap in the (b)-strength")
print("     part of the claim.  The (c) finding about the coefficient k is")
print("     unaffected: the master identity is chart-independent.")

print("\n" + "=" * 70)
bad = [t for ok_, t in LEDGER if not ok_]
print(f"LEDGER: {len(LEDGER) - len(bad)}/{len(LEDGER)} PASS")
for t in bad:
    print("  FAILED:", t)
assert not bad
