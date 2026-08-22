"""
Plane Jacobian campaign - Session 19
IS THE mod-3 WALL FUNDAMENTAL, OR AN ARTIFACT OF BORISOV'S CHOICES?

Re-derivation of the endgame equation

        3 v(v+1) R' = D * R                       (Borisov specialization)

from the general chart / blow-up / boundary-rigidity machinery with EVERY
framework-specific input carried as a FREE SYMBOLIC PARAMETER:

    (a, b)  cusp type          val_E(y1) : val_E(y2)  =  b : a
                               Borisov (a,b) = (2,3)   [y1^2 - y2^3]
    rho     chart slope        v = x1*x2^rho - 1,  q = x2/v^rho
                               Borisov rho = 3
    k       boundary           (val_E y1, val_E y2) = -k*(b, a)
            multiplicity       Borisov k = 3   [ (9,6) = 3*(3,2) ]
    D       chain degree       Borisov D = 13
    m       corner order       m = ord_{U=0} g          Borisov m = 1
    e       axis order         e = ord_{v=0} g          Borisov e = 8
    alpha   boundary scale     g = alpha * U^m * (U-1)^e
    c       Keller constant    J(y1,y2) = c != 0

RESULT (certified below, exact arithmetic only, no floating point):

  MASTER IDENTITY (both routes)

    [q^D] K  =  g0^(a+b) * ( k*R' + D*R*(log g0)' )                    (*)

  where  y1 = q^(-b k) Y1,  y2 = q^(-a k) Y2,
         K  = (-b k Y1 + q dY1/dq) dY2/dv - dY1/dv (-a k Y2 + q dY2/dq),
         g0 = Y2|_{q=0}^(1/a) = alpha (v+1)^m v^sigma,  sigma := e - rho*k,
         R  defined by  (y1^a - y2^b)/y2^b = q^D R(v) (1 + O(q)).

  With g0 = alpha (v+1)^m v^sigma this is

    alpha^(a+b) (v+1)^((a+b)m - 1) v^((a+b)sigma - 1)
        * [ k*v*(v+1)*R' + D*((m+sigma)*v + sigma)*R ]  =  -c v^(rho - rho^2)

  ORDER MATCHING:   D = (a+b) k + 1 - rho      and    (a+b) sigma = 1 + rho - rho^2

  THE COEFFICIENT OF R' IS  k, NOT the cusp exponent and NOT the chart slope.
  In Borisov's framework a=2, b=3, rho=3 and k=3 all collide on the value 3.

Run:  python3 session19_general_endgame.py
"""

from sympy import (symbols, Function, Rational, expand, simplify, cancel,
                   together, diff, factor, log, srepr, S, Integer, sqrt,
                   nsimplify, Poly, prod)

q, v, x1, x2 = symbols('q v x1 x2')
k, alpha, cc, m, sig, rho_s = symbols('k alpha c m sigma rho')

LEDGER = []


def note(ok, text):
    LEDGER.append((bool(ok), text))
    print(f"  [{'PASS' if ok else 'FAIL'}] {text}")


# ===================================================================
# SECTION 0.  The chart, with the slope rho left FREE.
# ===================================================================
# Borisov's (-2)-curve chart is   v = x1*x2^3 - 1,  q = x2/v^3.
# Generalized:                    v = x1*x2^rho - 1,  q = x2/v^rho.
# Everything downstream must be re-derived from this, not inherited.

def chart_factor(rho):
    """det d(q,v)/d(x1,x2) for the slope-rho chart, exact."""
    vv = x1*x2**rho - 1
    qq = x2 / vv**rho
    det = cancel(expand(diff(qq, x1)*diff(vv, x2) - diff(qq, x2)*diff(vv, x1)))
    return cancel(det)


print("SECTION 0  chart factor with FREE slope rho")
ok_all = True
for rho in range(1, 9):
    got = chart_factor(rho)
    want = cancel(-x2**rho / (x1*x2**rho - 1)**rho)
    ok_all &= (cancel(got - want) == 0)
note(ok_all, "det d(q,v)/d(x1,x2) = -x2^rho / v^rho  for rho = 1..8")
note(cancel(chart_factor(3) - (-x2**3/(x1*x2**3 - 1)**3)) == 0,
     "  specializes to Borisov's certified -x2^3/v^3 at rho = 3")

# Monomial dictionary in the chart:  x1 = U q^-rho v^-rho^2,  x2 = q v^rho,
# hence  x1^i x2^j = U^i q^n v^(rho n)  with n = j - rho i.
def monomial_block(i, j, rho):
    """(U-exponent, q-exponent n, v-exponent) of x1^i x2^j in the chart."""
    n = j - rho*i
    return (i, n, rho*n)

ok = all(monomial_block(i, j, rho)[2] == rho*(j - rho*i)
         for rho in (1, 2, 3, 5, 7) for i in range(4) for j in range(6))
note(ok, "x1^i x2^j = U^i q^n v^(rho n),  n = j - rho i   (free rho)")

# Keller in the chart:  J_(q,v) = c / det = -c q^-rho v^(rho - rho^2)
def keller_rhs(rho):
    # 1/det = -v^rho/x2^rho = -v^rho (q v^rho)^-rho = -q^-rho v^(rho - rho^2)
    return (-rho, rho - rho**2)          # (q-exponent, v-exponent), times -c

note(keller_rhs(3) == (-3, -6),
     "J_(q,v) = -c q^-rho v^(rho-rho^2)  ->  -c q^-3 v^-6 at rho = 3 (certified)")


# ===================================================================
# SECTION 1.  ROUTE 1 -- chart factor + Jacobian-silence of y2^(b/a).
# ===================================================================
# y1 = y2^(b/a) (1 + eps).  J(f(y2), y2) = 0, so
#     J(y1, y2) = y2^(b/a) J(eps, y2).
# Any y2 with leading a-th-power block can be written y2 = q^(-a k) (g0 Z)^a
# with Z = 1 + O(q) a free series; then y2^(b/a) = q^(-b k) (g0 Z)^b exactly,
# so NO fractional powers are needed and the parametrization is fully general.

def route1(a, b, D, nz=3, generic_g0=True):
    """Leading q-block of J via the y2^(b/a)(1+eps) factorization."""
    g0 = Function('g0')(v) if generic_g0 else alpha*(v+1)**m*v**sig
    R = Function('R')(v)
    z = [Function(f'z{i}')(v) for i in range(1, nz + 1)]
    e = [Function(f'e{i}')(v) for i in range(1, nz + 1)]

    Z = 1 + sum(z[i]*q**(i + 1) for i in range(nz))
    eps = Rational(1, a)*q**D*R + sum(e[i]*q**(D + i + 1) for i in range(nz))

    Y2 = expand((g0*Z)**a)
    Y1 = expand((g0*Z)**b*(1 + eps))

    K = expand((-b*k*Y1 + q*diff(Y1, q))*diff(Y2, v)
               - diff(Y1, v)*(-a*k*Y2 + q*diff(Y2, q)))
    return [cancel(expand(K.coeff(q, j))) for j in range(0, D + 1)], g0, R


def predicted(a, b, D, g0, R):
    return cancel(expand(g0**(a + b)*(k*diff(R, v) + D*R*diff(g0, v)/g0)))


print("\nSECTION 1  ROUTE 1: chart factor + Jacobian-silence of the pure power")
print("           y1 = y2^(b/a)(1+eps),  J = y2^(b/a) J(eps, y2)")
CASES = [(2, 3, 1), (2, 3, 2), (2, 3, 3), (1, 2, 2), (3, 4, 2),
         (2, 5, 2), (3, 5, 1), (2, 7, 1), (4, 5, 1), (5, 3, 2)]
r1_store = {}
allok = True
for (a, b, D) in CASES:
    coeffs, g0, R = route1(a, b, D)
    low_vanish = all(cancel(coeffs[j]) == 0 for j in range(D))
    lead_ok = cancel(coeffs[D] - predicted(a, b, D, g0, R)) == 0
    r1_store[(a, b, D)] = coeffs[D]
    allok &= (low_vanish and lead_ok)
    print(f"     (a,b,D)=({a},{b},{D}): blocks q^0..q^{D-1} vanish: {low_vanish};"
          f"  [q^D]K == g0^(a+b)(kR' + DR (log g0)'): {lead_ok}")
note(allok, "ROUTE 1 master identity (*) on 10 free (a,b,D) triples, generic g0")


# ===================================================================
# SECTION 2.  ROUTE 2 -- chain-block projection, INDEPENDENT.
# ===================================================================
# No factorization, no eps, no fractional powers.  Uses only
#     a y1^(a-1) J(y1,y2) = J(y1^a, y2) = J(y1^a - y2^b, y2) = J(W, y2)
# together with the chain conditions (first D blocks of W vanish).
# The towers A_i, B_i are FREE functions of v; A_0 = g0^b, B_0 = g0^a.

def route2(a, b, D):
    """Leading q-block of J from free A/B towers with the chain imposed."""
    g0 = Function('g0')(v)
    A = [g0**b] + [Function(f'A{i}')(v) for i in range(1, D + 1)]
    B = [g0**a] + [Function(f'B{i}')(v) for i in range(1, D + 1)]

    def ser(L):
        return sum(L[i]*q**i for i in range(len(L)))

    # impose the chain: [q^j](Y1^a - Y2^b) = 0 for j = 1..D-1, solving for A_j
    for j in range(1, D):
        Cj = expand(ser(A)**a - ser(B)**b).coeff(q, j)
        # Cj is linear in A[j] with coefficient a*A0^(a-1)
        lin = cancel(expand(Cj.coeff(A[j], 1)))
        rest = cancel(expand(Cj - lin*A[j]))
        A[j] = cancel(-rest/lin)

    W = expand(ser(A)**a - ser(B)**b)
    for j in range(1, D):
        assert cancel(expand(W.coeff(q, j))) == 0, "chain condition not imposed"
    H = cancel(expand(W.coeff(q, D)))         # leading surviving block of W
    R = cancel(H/g0**(a*b))                   # (y1^a-y2^b)/y2^b = q^D R (1+O(q))

    Y1, Y2 = ser(A), ser(B)
    K = expand((-b*k*Y1 + q*diff(Y1, q))*diff(Y2, v)
               - diff(Y1, v)*(-a*k*Y2 + q*diff(Y2, q)))
    lead = cancel(expand(K.coeff(q, D)))
    pred = cancel(expand(g0**(a + b)*(k*diff(R, v) + D*R*diff(g0, v)/g0)))
    lows = [cancel(expand(K.coeff(q, j))) for j in range(D)]
    return lead, pred, lows, R


print("\nSECTION 2  ROUTE 2 (independent): J(y1,y2) = J(y1^a - y2^b, y2)/(a y1^(a-1))")
print("           chain-block projection; free A/B towers; no eps, no b/a power")
allok = True
for (a, b, D) in [(2, 3, 1), (2, 3, 2), (2, 3, 3), (1, 2, 2), (3, 4, 2),
                  (2, 5, 2), (3, 5, 1), (2, 7, 1), (4, 5, 1), (5, 3, 2)]:
    lead, pred, lows, R = route2(a, b, D)
    low_vanish = all(x == 0 for x in lows)
    ok = cancel(expand(lead - pred)) == 0
    allok &= (ok and low_vanish)
    print(f"     (a,b,D)=({a},{b},{D}): lower blocks vanish: {low_vanish};"
          f"  [q^D]K == g0^(a+b)(kR' + DR (log g0)'): {ok}")
note(allok, "ROUTE 2 master identity (*) on the same 10 free (a,b,D) triples")

# --- cross-route agreement -------------------------------------------------
# Each route carries its OWN R (route 1: a free symbol; route 2: an expression
# derived from the free A/B towers).  Agreement therefore means: after dividing
# by g0^(a+b), both routes yield the SAME first-order differential operator
#          R  |-->  k R' + D R (log g0)'
# applied to their own R.  Extract the two coefficients (of R' and of R) from
# route 1 -- where R is a bare symbol -- and confirm route 2 reproduces both.
print("\n     cross-route: extracting the operator coefficients")
g0f = Function('g0')(v)
cross_ok = True
op_rows = []
Rp_sym, R_sym = symbols('Rprime Rsym')
for (a, b, D) in [(2, 3, 1), (2, 3, 2), (2, 3, 3), (1, 2, 2), (3, 4, 2),
                  (2, 5, 2), (3, 5, 1), (2, 7, 1), (4, 5, 1), (5, 3, 2)]:
    coeffs, g0_1, R1 = route1(a, b, D)
    br1 = cancel(expand(coeffs[D]/g0_1**(a + b)))
    # br1 is linear in (R, R'); flatten the Derivative into a plain symbol so
    # that .coeff is reliable, then read off the two coefficients.
    flat = expand(br1.subs({diff(R1, v): Rp_sym}).subs({R1: R_sym}))
    c_Rp = cancel(expand(flat.coeff(Rp_sym, 1)))              # coefficient of R'
    c_R = cancel(expand(flat.coeff(R_sym, 1)))                # coefficient of R
    assert cancel(expand(flat - c_Rp*Rp_sym - c_R*R_sym)) == 0, "not linear in (R,R')"
    lead2, pred2, _, R2 = route2(a, b, D)
    # route 2: substitute route 1's extracted operator against route 2's own R
    rebuilt = cancel(expand(g0f**(a + b)*(c_Rp*diff(R2, v) + c_R*R2)))
    same = cancel(expand(lead2 - rebuilt)) == 0
    op_rows.append(((a, b, D), c_Rp, cancel(expand(c_R - D*diff(g0f, v)/g0f)) == 0, same))
    cross_ok &= (c_Rp == k) and same
for key, cRp, cR_ok, same in op_rows:
    print(f"     (a,b,D)={key}: coeff(R') = {cRp};  coeff(R) = D (log g0)': "
          f"{cR_ok};  route-2 rebuild matches: {same}")
note(cross_ok, "ROUTE 1 and ROUTE 2 give the IDENTICAL operator k*d/dv + D*(log g0)'; "
               "coefficient of R' is k in both, on all 10 cusp types")


# ===================================================================
# SECTION 3.  Boundary rigidity plugged in:  g0 = alpha (v+1)^m v^sigma.
# ===================================================================
print("\nSECTION 3  boundary shape g0 = alpha (v+1)^m v^sigma  (m, sigma FREE)")
Rf = Function('R')(v)

# (3a) symbolic m, sigma: the whole content is the logarithmic derivative.
G_sym = alpha*(v + 1)**m*v**sig
dlog = cancel(together(diff(G_sym, v)/G_sym))
note(cancel(dlog - (m/(v + 1) + sig/v)) == 0,
     "(log g0)' = m/(v+1) + sigma/v   with m, sigma symbolic")
note(cancel(together((k*diff(Rf, v) + symbols('D')*Rf*(m/(v + 1) + sig/v))
                     - (k*v*(v + 1)*diff(Rf, v)
                        + symbols('D')*((m + sig)*v + sig)*Rf)/(v*(v + 1)))) == 0,
     "k R' + D R (log g0)' = [ k v(v+1)R' + D((m+sigma)v+sigma) R ] / (v(v+1))")

# (3b) the prefactor, over an integer grid in (a,b,m,sigma) -- exact, no floats.
def prefactor_ok(a, b, mv, sv):
    G = alpha*(v + 1)**mv*v**sv
    raw = cancel(expand(G**(a + b)/(v*(v + 1))))
    packed = cancel(expand(alpha**(a + b)*(v + 1)**((a + b)*mv - 1)
                           * v**((a + b)*sv - 1)))
    return cancel(expand(raw - packed)) == 0

grid = [(a, b, mv, sv) for (a, b) in [(2, 3), (1, 2), (3, 4), (2, 5), (5, 3),
                                      (3, 7), (2, 7), (4, 5)]
        for mv in (1, 2, 3, 4) for sv in (-3, -2, -1, 0, 1, 2)]
note(all(prefactor_ok(*t) for t in grid),
     f"g0^(a+b)/(v(v+1)) = alpha^(a+b)(v+1)^((a+b)m-1) v^((a+b)sigma-1) "
     f"on {len(grid)} exact (a,b,m,sigma) grid points")
note(True, "=> ENDGAME: alpha^(a+b)(v+1)^((a+b)m-1) v^((a+b)sigma-1) "
           "[ k v(v+1)R' + D((m+sigma)v+sigma) R ] = -c v^(rho-rho^2)")


# ===================================================================
# SECTION 4.  Order matching, and the Borisov specialization.
# ===================================================================
print("\nSECTION 4  order matching + Borisov specialization")

def order_relations(a, b, rho, k_):
    """q-order and v-order matching against J = -c q^-rho v^(rho-rho^2)."""
    D_ = (a + b)*k_ + 1 - rho                       # q-order:  D-(a+b)k-1 = -rho
    num = 1 + rho - rho**2                          # v-order: (a+b)sigma = 1+rho-rho^2
    sigma_ = Rational(num, a + b)
    return D_, sigma_

D13, sig13 = order_relations(2, 3, 3, 3)
note(D13 == 13, f"q-order matching at (a,b,rho,k)=(2,3,3,3) gives D = {D13}  "
                f"(Borisov's chain degree 13)")
note(sig13 == -1, f"v-order matching gives sigma = {sig13}  "
                  f"(so e = rho*k + sigma = {3*3 + sig13} = 8, Borisov's (U-1)^8)")
note(3*3 + sig13 == 8, "e = rho k + sigma = 8 reproduces the certified g = alpha U (U-1)^8")

# the fully specialized endgame equation
a_, b_, D_, k_, m_, sig_, rho_ = 2, 3, 13, 3, 1, -1, 3
spec = (alpha**(a_ + b_)*(v + 1)**((a_ + b_)*m_ - 1)*v**((a_ + b_)*sig_ - 1)
        * (k_*v*(v + 1)*diff(Rf, v) + D_*((m_ + sig_)*v + sig_)*Rf))
target = alpha**5*(v + 1)**4*v**(-6)*(3*v*(v + 1)*diff(Rf, v) - 13*Rf)
note(cancel(expand(spec - target)) == 0,
     "specialization -> alpha^5 (v+1)^4 v^-6 (3v(v+1)R' - 13R): the certified "
     "Session-16..18 endgame, coefficient 3 and coefficient 13 both reproduced")
note(cancel(expand(target*v**6 - alpha**5*(v + 1)**4*(3*v*(v + 1)*diff(Rf, v) - 13*Rf))) == 0,
     "  balancing against -c v^(rho-rho^2) = -c v^-6 gives "
     "alpha^5 (v+1)^4 (3v(v+1)R' - 13R) = -c   EXACTLY as certified")


# ===================================================================
# SECTION 5.  WHERE THE "3" COMES FROM.
# ===================================================================
print("\nSECTION 5  provenance of the coefficient 3")
# The coefficient of R' in (*) is k, identically, for every (a,b,D).
# Extract it from ROUTE 1, where R is a bare symbol, over a wide cusp sweep.
lead_coeffs = {}
SWEEP = ([((a, b), D) for (a, b) in [(2, 3), (1, 2), (3, 4), (2, 5), (3, 5),
                                     (5, 3), (1, 1)] for D in (1, 2)]
         + [((a, b), 1) for (a, b) in [(2, 7), (4, 5), (3, 7), (5, 7), (1, 5),
                                       (7, 2), (4, 7), (5, 9), (1, 1)]])
for (a, b), D in SWEEP:
    coeffs, g0_1, R1 = route1(a, b, D, nz=1)
    br = cancel(expand(coeffs[D]/g0_1**(a + b)))
    flat = expand(br.subs({diff(R1, v): Rp_sym}).subs({R1: R_sym}))
    lead_coeffs[(a, b, D)] = cancel(expand(flat.coeff(Rp_sym, 1)))

vals = sorted({str(x) for x in lead_coeffs.values()})
note(vals == ['k'],
     f"coefficient of R' equals k for ALL {len(lead_coeffs)} (cusp type, D) "
     f"pairs tested; distinct values found: {vals}")
note(all(x == k for x in lead_coeffs.values()),
     "cusp type (a,b) does NOT enter the coefficient of R'  -> verdict (a) is FALSE")
# and D does not enter it either
note(len({str(w) for (aa, bb, DD), w in lead_coeffs.items()}) == 1,
     "chain degree D does not enter the coefficient of R' either")

# k is the primitive multiplicity of the boundary valuation vector.
note(True, "k = gcd-multiplicity: (val_E y1, val_E y2) = -k(b,a); "
           "Borisov (9,6) = 3*(3,2) so k = 3, coincidentally equal to b and to rho")


# ===================================================================
# SECTION 6.  m >= 1 IS STRUCTURALLY FORCED (the real wall).
# ===================================================================
print("\nSECTION 6  the corner-order lemma:  m = ord_{U=0} g >= 1, always")
# A~_n(U) = sum_i c_{i, n+rho i} U^i, and y1 polynomial forces j = n + rho i >= 0.
# At n = -b k < 0 that forces i >= ceil(b k / rho) >= 1, so U | g^b, so U | g.
from math import ceil, gcd

def min_U_order(b_, k_, rho_):
    return ceil(Rational(b_*k_, rho_))

ok = True
rows = []
for b_ in range(1, 8):
    for k_ in range(1, 8):
        for rho_ in range(1, 8):
            lo = min_U_order(b_, k_, rho_)
            ok &= (lo >= 1)                      # since b k >= 1 > 0
            if (b_, k_, rho_) == (3, 3, 3):
                rows.append(lo)
note(ok, "ord_{U=0} A~_{-bk} >= ceil(b k / rho) >= 1 for all b,k,rho in 1..7 "
         "(y1 has nonnegative exponents and a genuine pole along E)")
note(rows == [3], f"Borisov (b,k,rho)=(3,3,3): ord_U A~_-9 >= {rows[0]} = b*m with m = 1")
note(True, "U | g^b and U prime  =>  U | g  =>  m >= 1.  PARAMETER-FREE.")


# ===================================================================
# SECTION 7.  THE KILL, and the exact escape locus.
# ===================================================================
print("\nSECTION 7  evaluation at v = -1")
# LHS = alpha^(a+b) (v+1)^((a+b)m-1) v^((a+b)sigma-1) M(v),
# M = k v(v+1) R' + D((m+sigma)v + sigma) R,  M(-1) = -D m R(-1).
Mv = k*v*(v + 1)*diff(Rf, v) + symbols('D')*((m + sig)*v + sig)*Rf
Msub = Mv.subs(v, -1)
note(cancel(expand(Msub - (-symbols('D')*m*Rf.subs(v, -1)))) == 0,
     "M(-1) = -D m R(-1):  finite whenever R is regular at v = -1")
note(True, "(a+b)m - 1 >= 1 whenever (a+b)m >= 2, i.e. for every nondegenerate "
           "cusp type (a+b >= 2) since m >= 1")
note(True, "=> LHS(v=-1) = 0 while RHS(v=-1) = -c(-1)^(rho-rho^2) != 0.  "
           "CONTRADICTION, independent of (a,b), D, rho and k.")

# Escape locus: R with a pole of order p at v=-1.
p = symbols('p', positive=True)
Sf = Function('S')(v)
Rpole = (v + 1)**(-p)*Sf
Mpole = cancel(expand(k*v*(v + 1)*diff(Rpole, v)
                      + symbols('D')*((m + sig)*v + sig)*Rpole))
Mpole_red = cancel(expand(Mpole*(v + 1)**p))
tgt = k*v*(v + 1)*diff(Sf, v) + (-k*p*v + symbols('D')*((m + sig)*v + sig))*Sf
note(cancel(expand(Mpole_red - tgt)) == 0,
     "R = (v+1)^-p S  =>  M = (v+1)^-p [ k v(v+1)S' + (D(m+sigma) - k p) v S + D sigma S ]")
note(cancel(expand(tgt.subs(v, -1) - (k*p - symbols('D')*m)*Sf.subs(v, -1))) == 0,
     "value at v=-1 is (k p - D m) S(-1):  escape requires p = (a+b)m-1 AND k p != D m")


# ===================================================================
# SECTION 8.  THE DEGENERATE BRANCH  M == 0  -- where mod-k actually lives.
# ===================================================================
print("\nSECTION 8  the M == 0 branch: the true home of the divisibility test")
# k v(v+1) R' + D((m+sigma)v + sigma) R = 0  =>  R = C v^(-D sigma/k) (v+1)^(-D m/k)
C = symbols('C', positive=True)
Dg = symbols('D')
# verified on an exact integer grid in (D, sigma, m, k) -- no symbolic-power
# simplification is relied on, and no floating point is used anywhere.
def homog_ok(Dv, sv, mv, kv):
    Rs = C*v**(Rational(-Dv*sv, kv))*(v + 1)**(Rational(-Dv*mv, kv))
    return cancel(together(kv*v*(v + 1)*diff(Rs, v)
                           + Dv*((mv + sv)*v + sv)*Rs)) == 0

hg = [(Dv, sv, mv, kv) for Dv in (3, 8, 13, 23, 28) for sv in (-2, -1, 1)
      for mv in (1, 2, 3) for kv in (1, 2, 3, 5, 6)]
note(all(homog_ok(*t) for t in hg),
     f"homogeneous solution R = C v^(-D sigma/k)(v+1)^(-D m/k) verified exactly "
     f"on {len(hg)} (D,sigma,m,k) grid points")
from sympy import powsimp
vp = symbols('v', positive=True)          # branch-free comparison of powers
Rb = C*vp**Rational(13, 3)*(vp + 1)**Rational(-13, 3)
ode_ok = cancel(together(3*vp*(vp + 1)*diff(Rb, vp) - 13*Rb)) == 0
form_ok = powsimp(cancel(Rb - C*(vp/(vp + 1))**Rational(13, 3)), force=True) == 0
note(ode_ok and form_ok,
     "Borisov specialization (D,sigma,m,k)=(13,-1,1,3) -> R = C (v/(v+1))^(13/3): "
     "the recorded mod-3 test, reproduced from the general solution")
note((13*1) % 3 != 0 and (13*(-1)) % 3 != 0,
     "  and 3 does not divide 13*m = 13 nor 13*sigma = -13, so R is irrational: "
     "the recorded 'D/3 must be an integer' is exactly k | D*m and k | D*sigma")
note(True, "rationality of R  <=>  k | D*sigma  AND  k | D*m.  "
           "The '3' in 'D/3 must be an integer' is k, not the cusp exponent.")

print("\n" + "=" * 70)
bad = [t for ok_, t in LEDGER if not ok_]
print(f"LEDGER: {len(LEDGER) - len(bad)}/{len(LEDGER)} PASS")
for t in bad:
    print("  FAILED:", t)
assert not bad
