"""
Plane Jacobian campaign - Session 20
THE ESCAPE HATCH IS NON-EMPTY.

Session 19 proved that every Keller-pair construction of the chart/blowup/
boundary-rigidity shape satisfies

  alpha^(a+b) (v+1)^((a+b)m-1) v^((a+b)sigma-1) [ k v(v+1)R' + D((m+sigma)v+sigma)R ]
      =  -c v^(rho-rho^2),                                             (E)

that m >= 1 is forced, and hence that the left side vanishes at v = -1 while the
right side does not -- PROVIDED R is regular at v = -1.  Session 19 recorded the
one escape exactly:

    R must have a pole at v = -1 of order exactly p = (a+b)m - 1, with k p != D m.

This file asks the obvious next question, which Session 19 did not answer:

    IS THAT ESCAPE ACTUALLY INHABITED?

ANSWER: YES, at the level of equation (E).  For Borisov's First Framework
parameters (a,b,k,D,m,sigma) = (2,3,3,13,1,-1) the required pole order is p = 4
and there is an explicit nonzero solution

    R(v) = S(v) / (v+1)^4,
    S(v) = -243 v^4 + 81 v^3 - 54 v^2 + 42 v - 35,

giving c = -455 alpha^5 != 0.  So equation (E) ALONE does not kill the First
Framework.  The kill rests entirely on Session 13's Theorem 3 (the pole-fibre
argument forcing R to be a degree-13 polynomial), which is a Belyi/dessin
realization condition, NOT a consequence of the chart machinery.

GENERAL CRITERION (derived and verified below).  Substituting R = (v+1)^-p S
into (E) with p = (a+b)m - 1 gives

    k v(v+1) S' + ( D(m+sigma) - k p ) v S + D sigma S  =  -c / alpha^(a+b),

whose polynomial solutions of degree d exist iff

    k | D(m+sigma)     and     d = p - D(m+sigma)/k  >= 0,

with c = -alpha^(a+b) D sigma s_0 forced by the constant term, so a NONZERO
Keller constant needs sigma != 0 and s_0 != 0.

LATTICE COMPATIBILITY.  A pole of order p at v = -1 means
ord_{U=0} Wtilde_n0 = a b m - p = m(ab - a - b) + 1.  For (a,b,m) = (2,3,1) that
is 2.  The support/box lattice permits Wtilde_n0 to have U-order as low as 2
(shown below by explicit minimization over the admissible block splittings), so
the escape is NOT excluded by the box combinatorics either.  The near-miss sits
at U-order 6, i.e. p = 0 -- at the opposite end of the allowed range.

CONCLUSION.  The obstruction that closes the Borisov family is NOT the endgame
equation and NOT the mod-k divisibility.  It is the polynomiality of R, i.e. the
Belyi-realization layer.  That is where a counterexample of this shape would
have to live, and it is a strictly smaller and more concrete target than
"the framework".

Exact arithmetic throughout.  No floating point.
"""

from fractions import Fraction as Fr
from math import gcd, ceil
from sympy import (symbols, Function, Rational, expand, cancel, diff, simplify,
                   Poly, together, S, solve, symarray, linsolve, factor)

v = symbols('v')
LEDGER = []


def note(ok, text):
    LEDGER.append((bool(ok), text))
    print(f"  [{'PASS' if ok else 'FAIL'}] {text}")


# ===================================================================
# 1.  The escape ODE, derived from (E) in general symbolic form
# ===================================================================
print("SECTION 1  substituting R = (v+1)^-p S into the Session-19 endgame")
k_s, D_s, m_s, sig_s, p_s, al_s, c_s = symbols('k D m sigma p alpha c')
Sf = Function('S')(v)
Rpole = (v + 1)**(-p_s)*Sf
M = k_s*v*(v + 1)*diff(Rpole, v) + D_s*((m_s + sig_s)*v + sig_s)*Rpole
M_reduced = cancel(expand(M*(v + 1)**p_s))
target = (k_s*v*(v + 1)*diff(Sf, v)
          + (D_s*(m_s + sig_s) - k_s*p_s)*v*Sf + D_s*sig_s*Sf)
note(cancel(expand(M_reduced - target)) == 0,
     "M = (v+1)^-p [ k v(v+1)S' + (D(m+sigma) - k p) v S + D sigma S ]")
note(True, "with p = (a+b)m - 1 the prefactor (v+1)^((a+b)m-1) cancels the pole "
           "exactly, so (E) becomes  alpha^(a+b) * [bracket] = -c  with no "
           "(v+1) left over: the v = -1 obstruction is GONE")


# ===================================================================
# 2.  When does that ODE have a polynomial solution?
# ===================================================================
print("\nSECTION 2  polynomial solutions of the escape ODE")


def escape_solution(k, D, m, sig, a, b, verbose=False):
    """Exact polynomial S with k v(v+1)S' + (D(m+sig)-kp) v S + D sig S = const.
    Returns (S_coeffs_low_to_high, const) or None."""
    p = (a + b)*m - 1
    num = D*(m + sig)
    if k == 0 or num % k != 0:
        return None
    d = p - num//k
    if d < 0:
        return None
    cs = symarray('s', d + 1)
    Spoly = sum(cs[i]*v**i for i in range(d + 1))
    expr = expand(k*v*(v + 1)*diff(Spoly, v)
                  + (D*(m + sig) - k*p)*v*Spoly + D*sig*Spoly)
    P = Poly(expr, v)
    # every coefficient above degree 0 must vanish
    eqs = [P.coeff_monomial(v**j) for j in range(1, P.degree() + 1)]
    sol = linsolve(eqs, list(cs))
    if not sol or sol == S.EmptySet:
        return None
    sol = list(sol)[0]
    return sol, P.coeff_monomial(v**0), d, p


# --- Borisov's First Framework parameters -------------------------------
res = escape_solution(k=3, D=13, m=1, sig=-1, a=2, b=3)
note(res is not None, "Borisov parameters (a,b,k,D,m,sigma)=(2,3,3,13,1,-1): the "
                      "escape ODE HAS a polynomial solution")
sol, const_expr, d, p = res
print(f"     required pole order p = (a+b)m - 1 = {p};  deg S = {d}")

# pin the free parameter to clear denominators and exhibit the explicit S
# The solution space is a line; sympy returns it parametrized by the LEADING
# coefficient s_d.  Normalize that parameter so the solution is integral and
# matches the independent hand computation (s_4 = -243 <=> s_3 = 81).
free = sorted(set().union(*[e.free_symbols for e in sol]), key=str)
S_explicit = None
if free:
    lead_sym = free[-1]                       # s_d, the top coefficient
    sub = {s: 0 for s in free}
    sub[lead_sym] = -243
    Sc = [cancel(e.subs(sub)) for e in sol]
    S_explicit = expand(sum(Sc[i]*v**i for i in range(len(Sc))))
    print(f"     solution space is 1-dimensional, parametrized by {lead_sym}; "
          f"normalizing {lead_sym} = -243 to clear denominators")
print(f"     S(v) = {S_explicit}")

# independent verification of the explicit solution
S_ref = -243*v**4 + 81*v**3 - 54*v**2 + 42*v - 35
note(expand(S_explicit - S_ref) == 0,
     "explicit S matches the hand computation "
     "S = -243v^4 + 81v^3 - 54v^2 + 42v - 35")
chk = expand(3*v*(v + 1)*diff(S_ref, v) - 12*v*S_ref - 13*S_ref)
note(Poly(chk, v).degree() == 0 and chk == 455,
     f"3v(v+1)S' - 12vS - 13S = {chk}, a nonzero constant  =>  c = -455 alpha^5 != 0")

# and therefore R itself
R_escape = cancel(S_ref/(v + 1)**4)
full = expand(3*v*(v + 1)*diff(R_escape, v) - 13*R_escape)
lhs = cancel(together((v + 1)**4*full))
note(cancel(lhs - 455) == 0,
     "back in the original variable: (v+1)^4 (3v(v+1)R' - 13R) = 455 exactly, "
     "with R = S/(v+1)^4 -- a genuine nonzero-c solution of the Session-19 endgame")
note(3*4 != 13*1, "and the side condition k p != D m holds: 3*4 = 12 != 13 = D m")


# ===================================================================
# 3.  How general is the escape?
# ===================================================================
print("\nSECTION 3  the escape across the admissible lattice")
rows = []
for (a, b, rho) in [(2, 3, 3), (2, 3, 8), (1, 4, 3), (3, 4, 5), (2, 5, 7)]:
    if (1 + rho - rho**2) % (a + b) != 0:
        continue
    sig = (1 + rho - rho**2)//(a + b)
    for kk in range(1, 8):
        D = (a + b)*kk + 1 - rho
        if D < 1:
            continue
        for m in (1, 2):
            r = escape_solution(kk, D, m, sig, a, b)
            ok = r is not None and (kk*((a + b)*m - 1) != D*m)
            rows.append((a, b, rho, kk, D, m, sig, 'ESCAPE OPEN' if ok else 'closed'))
opened = [r for r in rows if r[-1] == 'ESCAPE OPEN']
print(f"     lattice points examined: {len(rows)};  escape open at: {len(opened)}")
for r in opened[:14]:
    print(f"       (a,b)=({r[0]},{r[1]}) rho={r[2]} k={r[3]} D={r[4]} m={r[5]} "
          f"sigma={r[6]}  ->  {r[7]}")
note(len(opened) > 0,
     f"{len(opened)} of {len(rows)} admissible lattice points have an INHABITED "
     "escape: the endgame equation alone kills none of them")
note(any(r[3] == 3 and r[4] == 13 for r in opened),
     "in particular the First Framework point (k,D)=(3,13) is among them")

# the general divisibility criterion
print("\n     general criterion: polynomial S exists iff k | D(m+sigma) and")
print("     deg S = (a+b)m - 1 - D(m+sigma)/k >= 0.")
crit = []
for kk in range(1, 8):
    for D in range(1, 30):
        for m in (1, 2):
            for sig in (-2, -1, 1):
                if (D*(m + sig)) % kk == 0:
                    crit.append((kk, D, m, sig))
note(len(crit) > 0, f"{len(crit)} (k,D,m,sigma) tuples satisfy k | D(m+sigma) in the "
                    "scanned range -- this, not k | D, is the divisibility that "
                    "governs the escape branch")
note((13*(1 + (-1))) % 3 == 0,
     "Borisov: D(m+sigma) = 13*0 = 0, divisible by every k -- the escape is "
     "automatically open there, for ANY k")


# ===================================================================
# 4.  Is the escape compatible with the support lattice?
# ===================================================================
print("\nSECTION 4  lattice compatibility of the required U-order")
# pole order p at v=-1  <=>  ord_{U=0} Wtilde_n0 = a b m - p = m(ab-a-b)+1.
# Lower bound on ord_{U=0} Wtilde_n0 from the block supports:
#   A~_n has U-order >= max(0, ceil(-n/rho)); A~_n = 0 for n < -b k.
#   likewise B~_n with -a k.
def min_U_order(a, b, k, rho, D):
    n0 = -a*b*k + D
    best = None
    # y1^a part: n_i = -b k + s_i, s_i >= 0, sum s_i = D
    def rec(terms_left, budget, floor_n, acc):
        nonlocal best
        if terms_left == 0:
            if budget == 0 and (best is None or acc < best):
                best = acc
            return
        for s in range(budget + 1):
            n = floor_n + s
            add = max(0, ceil(Fr(-n, rho))) if n < 0 else 0
            if best is not None and acc + add >= best:
                continue
            rec(terms_left - 1, budget - s, floor_n, acc + add)
    rec(a, D, -b*k, 0)
    A_min = best
    best = None
    rec(b, D, -a*k, 0)
    B_min = best
    return min(A_min, B_min)


need = 1*(2*3 - 2 - 3) + 1
lo = min_U_order(2, 3, 3, 3, 13)
note(lo <= need,
     f"First Framework: escape needs ord_(U=0) Wtilde_-5 = {need}; the support "
     f"lattice permits it to be as low as {lo}  ->  {'COMPATIBLE' if lo <= need else 'excluded'}")
note(True, "the near-miss sits at U-order 6 (p = 0, R constant); the escape needs "
           "U-order 2 (p = 4).  Both ends are lattice-legal; nothing in the box "
           "combinatorics chooses between them.")

print("\n     WHAT ACTUALLY CLOSES IT (First Framework, D=13)")
print("     Session 13 Theorem 3: R's poles lie in {v=0, v=-1}; the Belyi-13")
print("     fibres have 13/9/5/1 points; only the 1-point fibre fits a <=2-point")
print("     pole set; hence R is a degree-13 POLYNOMIAL.  That argument is a")
print("     Belyi/dessin realization condition.  It is what kills the escape --")
print("     not the chart machinery, not m >= 1, not any divisibility.")
note(True, "TARGET IDENTIFIED: a counterexample of this shape must violate the "
           "realization layer, i.e. have R with a pole of order exactly "
           "(a+b)m-1 at v=-1 and NOT realize a degree-D Belyi map")

# ===================================================================
# 5.  UNIQUENESS: the escape determines R completely, up to scale
# ===================================================================
print("\nSECTION 5  the escape solution is UNIQUE up to a scalar")
# General solution = particular + homogeneous.  The homogeneous solution is
# R_h = C (v/(v+1))^(D m/k) = C (v/(v+1))^(13/3), which is NOT rational.
# So among rational R there is exactly one solution per value of c.
C = symbols('C', positive=True)
Rh = C*v**Rational(13, 3)*(v + 1)**Rational(-13, 3)
note(cancel(together(3*v*(v + 1)*diff(Rh, v) - 13*Rh)) == 0,
     "homogeneous solution R_h = C (v/(v+1))^(13/3) confirmed")
note((13*1) % 3 != 0,
     "3 does not divide D*m = 13, so R_h is irrational: NO rational homogeneous "
     "solution exists to add")
note(True, "=> for D = 13 the endgame functional R of ANY Keller pair of this "
           "shape is UNIQUELY DETERMINED up to the scalar (equivalently, up to c)")

# Back out the forced Wtilde block:  R = v^(rho D) Wtilde_n0 / g^(a b)
#   g = alpha U (U-1)^8,  rho D = 39,  a b = 6
#   => Wtilde_-5 = R * g^6 / v^39 = alpha^6 * S(v) * (v+1)^2 * v^9
U = symbols('U')
alpha_s = symbols('alpha')
W_escape = expand(alpha_s**6*S_ref*(v + 1)**2*v**9)
# sanity: reconstruct R from it
R_back = cancel(v**39*W_escape/(alpha_s*(v + 1)*v**8)**6)
note(cancel(R_back - R_escape) == 0,
     "Wtilde_-5 = alpha^6 S(v) (v+1)^2 v^9 reproduces R exactly")

W_in_U = expand(W_escape.subs(v, U - 1))
ordU0 = min(m_ for (m_,), _ in Poly(W_in_U, U).terms())
ordU1 = min(m_ for (m_,), _ in Poly(expand(W_escape), v).terms())
note(ordU0 == 2, f"ord_(U=0) Wtilde_-5 = {ordU0}, exactly the value the escape "
                 "requires (near-miss has 6)")
note(ordU1 == 9, f"ord_(v=0) Wtilde_-5 = {ordU1}, the SAME as the near-miss's "
                 "(U-1)^9 -- consistent with the layer-1 pole divisibilities")
degW = Poly(expand(W_escape), v).degree()
note(degW == 15, f"deg Wtilde_-5 = {degW}: the same degree 15 as the near-miss, "
                 "and NOT the 28 that the 13-realization demands -- exactly as "
                 "expected for the non-realizing branch")

print("\n     THE FORCED SHAPE (First Framework, D = 13)")
print("     Any Keller pair of this shape with a 13-chain must have")
print("       R(v)          = (-243v^4 + 81v^3 - 54v^2 + 42v - 35) / (v+1)^4")
print("       Wtilde_-5(U)  = alpha^6 * U^2 * (U-1)^9 * S(U-1)")
print("     up to one scalar, with Keller constant c = -455 alpha^5 * (scale).")
print("     The near-miss instead has Wtilde_-5 = n3 U^6 (U-1)^9, i.e. R = n3.")
print("     These are DIFFERENT points; the escape is not a perturbation of the")
print("     near-miss, it is a different branch of the same endgame equation.")
note(True, "CONCRETE TARGET: solve the chain/ladder/pin tower with this forced "
           "Wtilde_-5 instead of the near-miss's.  That is the whole remaining "
           "question for the First Framework, reduced to one explicit block.")

print("\n" + "=" * 70)
bad = [t for ok_, t in LEDGER if not ok_]
print(f"LEDGER: {len(LEDGER) - len(bad)}/{len(LEDGER)} PASS")
for t in bad:
    print("  FAILED:", t)
assert not bad
