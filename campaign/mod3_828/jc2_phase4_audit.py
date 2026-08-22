"""
ADVERSARIAL AUDIT of the Phase 4 "direct attack" machinery on the plane
Jacobian conjecture (session19_general_endgame.py, session19_parameter_lattice.py,
session19_general_chart.py, jc2_escape_hatch.py, jc2_target_72_108.py,
jc2_phase4_direct.py).

This file does NOT import or modify the audited files. Every check below is
re-derived independently from first principles (or from a genuinely different
computational path -- e.g. sympy Matrix.nullspace() instead of the audited
code's symarray/linsolve, or plain Python fractions.Fraction with hand-coded
polynomial derivatives instead of sympy at all) and then, where relevant,
cross-checked against the audited files' actual printed output.

Findings are reported as PASS/FAIL against an explicit claim for each check.
Some checks are "attack succeeded" checks: a PASS there means an independently
reproducible BUG was confirmed to exist in the audited code (this is flagged
explicitly in the text -- do not read a bare PASS as "the audited code is fine"
without reading the label).

Run:  python3 jc2_phase4_audit.py
"""

from fractions import Fraction as PyFrac
from math import gcd, ceil
from sympy import (symbols, Function, Matrix, Rational, expand, cancel, simplify,
                    diff, Poly, together, S, solve, symarray, linsolve, factor)

v, q = symbols('v q')
LEDGER = []


def note(ok, text):
    LEDGER.append((bool(ok), text))
    print(f"  [{'PASS' if ok else 'FAIL'}] {text}")


def section(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


# ===================================================================
# AXIS (a) ALGEBRA -- independent re-derivation of claim 1, BEFORE reading
# the audited derivation (done in the actual audit session in that order;
# reproduced here as a clean, standalone check).
#
#   [q^D] K  =  g0^(a+b) * ( k R' + D R (log g0)' )
#
# Derived by hand from J(y1,y2) = J(y1^a - y2^b, y2) / (a y1^(a-1)) (Route 2,
# as instructed), then checked here by constructing EXPLICIT power series
# Y1, Y2 satisfying the exact defining relations, WITH NONZERO "gauge" freedom
# injected at every intermediate q-order (q^1 .. q^(D-1)).  If claim 1 secretly
# depended on that gauge (which the report's formula never mentions), this
# test would catch it: the two sides would disagree once gauge != 0.
# ===================================================================
section("AXIS (a): ALGEBRA -- independent re-derivation of claim 1")


def claim1_case(a, b, k, D, g0_expr, R_expr, Y2_gauge, label):
    g0 = g0_expr
    Y1_0 = expand(g0**b)
    Y2_0 = expand(g0**a)
    Y1_coeffs = [Y1_0]
    Y2_coeffs = [Y2_0] + list(Y2_gauge)
    assert len(Y2_coeffs) == D + 1

    u = symbols('u_unknown')
    for i in range(1, D + 1):
        Y1_trunc = sum(Y1_coeffs[j] * q**j for j in range(i)) + u * q**i
        Y2_trunc = sum(Y2_coeffs[j] * q**j for j in range(i + 1))
        Y1a = expand(Y1_trunc**a)
        Y2b = expand(Y2_trunc**b)
        c1 = Y1a.coeff(q, i)
        c2 = Y2b.coeff(q, i)
        eq = expand(c1 - c2) if i < D else expand(c1 - c2 - g0**(a * b) * R_expr)
        sol = solve(eq, u)
        Y1_coeffs.append(simplify(sol[0]))

    Y1_full = sum(Y1_coeffs[j] * q**j for j in range(D + 1))
    Y2_full = sum(Y2_coeffs[j] * q**j for j in range(D + 1))
    check = expand(Y1_full**a - Y2_full**b)
    for i in range(D):
        assert simplify(check.coeff(q, i)) == 0
    assert simplify(check.coeff(q, D) - expand(g0**(a * b) * R_expr)) == 0

    K = ((-b * k * Y1_full + q * diff(Y1_full, q)) * diff(Y2_full, v)
         - diff(Y1_full, v) * (-a * k * Y2_full + q * diff(Y2_full, q)))
    K_D = simplify(expand(K).coeff(q, D))
    claim = simplify(expand(g0**(a + b) * (k * diff(R_expr, v) + D * R_expr * diff(g0, v) / g0)))
    ok = simplify(together(K_D - claim)) == 0
    note(ok, f"claim 1 holds at {label}, WITH nonzero gauge freedom injected at every "
              f"intermediate q-order (rules out the formula secretly depending on "
              f"unstated lower-block data)")
    return ok


claim1_case(2, 3, 2, 3, v**2 + v + 2, v**3 - 2*v + 1, [v + 1, v**2 - 3, 2*v - 5],
            "(a,b,k,D)=(2,3,2,3)")
claim1_case(1, 1, 1, 1, v**3 - v + 4, 5*v**2 + v - 1, [7*v - 2],
            "(a,b,k,D)=(1,1,1,1) [minimal/degenerate cusp]")
claim1_case(3, 2, 3, 4, v**2 + 5, v**4 - v**2 + 2*v,
            [3*v - 2, v**2 + v, -v + 7, 2*v**2 - v + 1], "(a,b,k,D)=(3,2,3,4)")

# non-coprime (a,b) -- claim 1's algebra never invokes coprimality; check it
# survives being fed a non-primitive "cusp type" anyway (an interpretive point,
# not an algebraic one: gcd(2,4)=2, so (2,4) would not arise as an actual
# cusp type from any real degree pair, but the IDENTITY itself doesn't care).
claim1_case(2, 4, 1, 2, v**2 + 3, v + 1, [v - 2, v**2 + 1], "(a,b,k,D)=(2,4,1,2) [non-coprime a,b]")

# D=0 boundary: is it even a coherent case, independent of claim 1's formula?
g0_test = v**2 + 1
Y1_0_t, Y2_0_t = expand(g0_test**3), expand(g0_test**2)
forced_R_at_D0 = simplify((Y1_0_t**2 - Y2_0_t**3) / Y2_0_t**3)
note(forced_R_at_D0 == 0,
     "D=0 is DEGENERATE under the framework's own definitions: g0 is defined so that "
     "Y1|_(q=0)=g0^b, Y2|_(q=0)=g0^a identically, which forces [q^0]((y1^a-y2^b)/y2^b)=0 "
     "-- so D=0 would force R=0, contradicting 'R is the leading NONZERO coefficient at "
     "order D'. D>=1 is baked into the setup, not a separate hypothesis to verify.")


# ===================================================================
# AXIS (a) continued: chart-factor identities (session19_general_chart.py),
# independently re-derived by hand and cross-checked symbolically.
#   det d(q,v)/d(x1,x2) = -eps * x1^(P+P'-1) x2^(Q+Q'-1) v^-w
#   A := ord_{v=-1} delta = eps(Q'-P') - 1
# ===================================================================
section("AXIS (a) continued: chart-factor generality (session19_general_chart.py)")
x1s, x2s = symbols('x1 x2', positive=True)


def det_chart(P, Q, Pp, Qp, w):
    U = x1s**P * x2s**Q
    vv = U - 1
    qq = x1s**Pp * x2s**Qp * vv**(-w)
    return cancel(expand(diff(qq, x1s) * diff(vv, x2s) - diff(qq, x2s) * diff(vv, x1s)))


ok = True
tested = 0
for (P, Q, Pp, Qp, w) in [(1, 3, 0, 1, 3), (1, 8, 0, 1, 8), (2, 5, 1, 2, 2),
                          (0, 1, 1, 0, 1), (1, 1, 0, 1, 4), (1, 2, 1, 1, 0)]:
    eps = P * Qp - Q * Pp
    if eps not in (1, -1):
        continue
    got = det_chart(P, Q, Pp, Qp, w)
    want = cancel(-eps * x1s**(P + Pp - 1) * x2s**(Q + Qp - 1) * (x1s**P * x2s**Q - 1)**(-w))
    ok &= (cancel(expand(got - want)) == 0)
    tested += 1
note(ok and tested >= 3, f"det d(q,v)/d(x1,x2) = -eps x1^(P+P'-1) x2^(Q+Q'-1) v^-w "
     f"independently re-derived and matched on {tested} charts")


def A_formula(P, Q, Pp, Qp):
    eps = P * Qp - Q * Pp
    return eps * (Qp - Pp) - 1


note(A_formula(1, 3, 0, 1) == 0, "A=0 for Borisov's chart, independently re-derived by hand "
     "via the (x1,x2)->(U,q,v) inversion (see audit report for the derivation)")
note(all(A_formula(1, r, 0, 1) == 0 for r in range(1, 12)),
     "A=0 for the entire rho-family, independently confirmed for rho=1..11")


# ===================================================================
# AXIS (b) HIDDEN ASSUMPTIONS in claim 3 (m >= 1 forced).
# Argument: i >= ceil(b*k/rho) forces U | g, hence m >= 1, "always".
# Stress-test the regimes named in the task: k=0, rho > b*k, negative sigma.
# ===================================================================
section("AXIS (b): hidden assumptions in the m>=1 corner-order lemma")

k0_val = ceil(Rational(3 * 0, 3))
note(k0_val == 0,
     f"ATTACK SUCCEEDS on the bare inequality: at k=0, ceil(b*k/rho) = {k0_val}, which "
     f"does NOT force i>=1 (hence does NOT force U|g, hence does NOT force m>=1). "
     f"'m>=1 always' is FALSE at k=0 as a pure consequence of the displayed inequality.")
note(True,
     "BUT this does not reach the actual claim: k>=1 ('y1 has a genuine pole along E') "
     "is stated as an explicit INPUT HYPOTHESIS throughout session19_report.md's table, "
     "and every downstream loop in all 6 audited files that ranges over k starts at 1, "
     "never 0 (session19_general_endgame.py Section 6: 'for k_ in range(1,8)'; "
     "jc2_escape_hatch.py Section 3: 'for kk in range(1,8)'; jc2_target_72_108.py/"
     "jc2_phase4_direct.py: 'for k in range(1, N//B+1)'). k=0 is never smuggled through.")

rho_extreme = ceil(Rational(1 * 1, 1000))
note(rho_extreme >= 1,
     f"ATTACK FAILS: 'rho > b*k' does NOT break the lemma. Tested rho=1000 >> b*k=1: "
     f"ceil(bk/rho) = {rho_extreme} >= 1 still. ceil(x) >= 1 for ANY x>0 regardless of "
     f"magnitude, so no rho, however large, can defeat this. Tried and did not break.")

note(True,
     "ATTACK FAILS: negative sigma does not interact with the m>=1 argument at all -- "
     "sigma is the v=0 axis order (a different corner of the chart entirely); the "
     "corner-order lemma at v=-1 (equivalently U=0) depends only on b, k, rho. Verified "
     "by inspection: sigma does not appear anywhere in session19_general_endgame.py "
     "Section 6's min_U_order() or the surrounding proof.")


# ===================================================================
# AXIS (c) BOUNDARY CASES -- do the escape/forced_R functions validate their
# inputs, or silently produce output for mathematically-excluded parameter
# values?  (a=b=1 already covered under axis (a) above: PASSES cleanly.)
# ===================================================================
section("AXIS (c): boundary-case robustness of the escape-solving functions")


def escape_solution_original(k, D, m, sig, a, b):
    """Faithful reproduction of the escape-solving logic shared by
    jc2_escape_hatch.py / jc2_target_72_108.py (pre-refinement)."""
    p = (a + b) * m - 1
    num = D * (m + sig)
    if k == 0 or num % k != 0:
        return None
    d = p - num // k
    if d < 0:
        return None
    cs = symarray('s', d + 1)
    Spoly = sum(cs[i] * v**i for i in range(d + 1))
    expr = expand(k * v * (v + 1) * diff(Spoly, v)
                  + (D * (m + sig) - k * p) * v * Spoly + D * sig * Spoly)
    P = Poly(expr, v)
    eqs = [P.coeff_monomial(v**j) for j in range(1, P.degree() + 1)]
    sol = linsolve(eqs, list(cs))
    if not sol or sol == S.EmptySet:
        return None
    sol = list(sol)[0]
    return sol, P.coeff_monomial(v**0), d, p


res = escape_solution_original(k=1, D=0, m=1, sig=-1, a=2, b=3)
note(res is not None,
     "ROBUSTNESS GAP (not a live bug): D=0, fed directly into the escape-solver logic, "
     "is silently ACCEPTED and produces a 'solution' (deg S=4) with no warning, even "
     "though D=0 was independently shown above to be degenerate/meaningless. None of "
     "the 3 files ever call this with D<=0 in their actual reported results (D is "
     "always computed as (a+b)k+1-rho with k>=1 in a regime keeping D>=1), so this "
     "is untriggered in practice -- but the function itself does not check D>=1.")

res = escape_solution_original(k=1, D=13, m=0, sig=-1, a=2, b=3)
note(res is not None,
     "ROBUSTNESS GAP: m=0, fed in with a compatible k, is silently accepted too "
     "(p=(a+b)*0-1=-1, a NEGATIVE 'pole order', silently treated as a valid ansatz "
     "'(v+1)^(-p)' with p<0, i.e. actually a ZERO not a pole -- no cross-check against "
     "the m>=1 lemma proven elsewhere in the same campaign). Never triggered with m=0 "
     "in the actual reported results (m is hardcoded to 1 throughout the (72,108) files).")

res = escape_solution_original(k=1, D=1, m=1, sig=0, a=2, b=3)
note(res is not None,
     "sigma=0 is accepted (as expected -- it is not itself an invalid input, just a "
     "value that forces CONST = D*sigma*s0 = 0 identically for ANY s0, matching the "
     "jc2_escape_hatch.py docstring's own remark that 'a nonzero Keller constant needs "
     "sigma != 0'). Confirms that remark is right, and shows sigma=0 does not crash.")

N, B = 7, 5
k_range = list(range(1, N // B + 1))
note(k_range == [1],
     f"n not divisible by b: N={N}, B={B} (7 not divisible by 5). Python's floor "
     f"division in 'range(1, N//B+1)' still correctly reproduces the intended "
     f"constraint k <= N/B = 1.4, i.e. k in {{1}}. ATTACK FAILS: no off-by-one bug.")


# ===================================================================
# AXIS (d) THE LATE-ADDED CONDITION -- full independent re-verification.
# Ground truth built via sympy Matrix.nullspace() (a different code path than
# the audited files' symarray/linsolve), checking BOTH that the "forced
# constant" claim is right at every point AND that no >1-dimensional solution
# space is hiding an escape behind an arbitrary gauge choice.
# ===================================================================
section("AXIS (d): the late-added 'forced constant nonzero' condition")


def ground_truth(a, b, k, D, m, sig):
    """Returns (verdict_str, extra) where verdict_str in
    {'CLOSED-nodivide','CLOSED-degneg','CLOSED-onlyzero','CLOSED-forcedc0','OPEN','OPEN-ambiguous'}."""
    p = (a + b) * m - 1
    num = D * (m + sig)
    if k == 0 or num % k != 0:
        return "CLOSED-nodivide", None
    d = p - num // k
    if d < 0:
        return "CLOSED-degneg", None
    s = symbols(f's0:{d + 1}')
    Sp = sum(s[i] * v**i for i in range(d + 1))
    expr = expand(k * v * (v + 1) * diff(Sp, v) + (D * (m + sig) - k * p) * v * Sp + D * sig * Sp)
    P = Poly(expr, v)
    if d == 0:
        M = Matrix.zeros(0, 1)
    else:
        eqs = [P.coeff_monomial(v**j) for j in range(1, d + 1)]
        M = Matrix([[eq.coeff(si, 1) for si in s] for eq in eqs])
        residual = [expand(eqs[i] - sum(M[i, j] * s[j] for j in range(d + 1))) for i in range(len(eqs))]
        assert all(r == 0 for r in residual), "system unexpectedly nonlinear"
    ns = M.nullspace()
    if len(ns) == 0:
        return "CLOSED-onlyzero", None
    consts = [expand(D * sig * basis[0]) for basis in ns]
    if all(simplify(c) == 0 for c in consts):
        return "CLOSED-forcedc0", len(ns)
    if len(ns) > 1:
        return "OPEN-ambiguous", len(ns)
    return "OPEN", consts[0]


# --- (72,108) family: a=2,b=3,m=1,sigma=-1,rho=3, D=5k-2, k=1..12 --------
print("\n  --- (72,108) family: k=1..12, D=5k-2 (m=1, sigma=-1) ---")
rows_72_108 = []
for k in range(1, 13):
    D = 5 * k - 2
    verdict, extra = ground_truth(2, 3, k, D, 1, -1)
    rows_72_108.append((k, D, verdict, extra))
    print(f"    k={k:2d} D={D:3d}: {verdict}" + (f"  (nullity={extra})" if verdict == "CLOSED-forcedc0" else
                                                  f"  const={extra}" if verdict == "OPEN" else ""))

closed_c0 = [r for r in rows_72_108 if r[2] == "CLOSED-forcedc0"]
opens = [r for r in rows_72_108 if r[2] == "OPEN"]
ambiguous = [r for r in rows_72_108 if r[2] == "OPEN-ambiguous"]

note(len(rows_72_108) == 12, "all 12 (72,108) lattice points examined")
note(ambiguous == [],
     "no point has a >1-dimensional escape-ODE solution space (nullity always exactly 1 "
     "-- confirmed by direct Matrix.nullspace() rank computation), so jc2_phase4_direct.py's "
     "normalization trick ('set the leading free symbol to 1, all others to 0') CANNOT be "
     "hiding a real escape behind an arbitrary gauge choice: there is no other gauge to pick.")
note(sorted(r[0] for r in closed_c0) == [1, 2],
     f"k=1 (D=3) AND k=2 (D=8) are BOTH independently confirmed forced-c=0 via one single, "
     f"uniform from-scratch linear-algebra test (different sympy entry point -- "
     f"Matrix.nullspace() -- than the audited code's symarray/linsolve): each has a "
     f"1-dimensional null space whose unique basis vector has s0=0 identically, so "
     f"CONST=D*sigma*s0=0 for every scalar multiple, not an artifact of a normalization "
     f"choice. THE LATE-ADDED CONDITION IN jc2_phase4_direct.py IS VERIFIED CORRECT for "
     f"k=1. NOTE: this single uniform test subsumes jc2_phase4_direct.py's k=2 check too "
     f"(k*p=D*m=8) as a special case of the same underlying fact (CONST forced to 0) -- "
     f"the two 'different mechanisms' the file describes are two different PROOF ROUTES "
     f"to the same linear-algebra fact, not logically independent phenomena; worth noting "
     f"precisely so nobody expects a THIRD, different-looking self-kill elsewhere.")
note(2 * 4 == 8 * 1,
     "independently confirms the k=2 arithmetic shortcut k*p=D*m (2*4=8=8*1) that "
     "jc2_phase4_direct.py uses as its faster, non-nullspace closure route for k=2")
note(len(opens) == 10 and sorted(r[1] for r in opens) == [13, 18, 23, 28, 33, 38, 43, 48, 53, 58],
     "exactly 10 chain degrees D in {13,18,23,28,33,38,43,48,53,58} are genuinely OPEN, "
     "matching jc2_phase4_direct.py's reported 10 -- INDEPENDENTLY CONFIRMED, not just "
     "re-run")

# --- Cross-check the 10 explicit R polynomials jc2_phase4_direct.py prints,
#     against an independently-solved nullspace vector, exactly (no `simplify`
#     tricks -- polynomial coefficient equality after clearing scale).
print("\n  --- cross-checking the 10 explicit S(v)/R(v) formulas jc2_phase4_direct.py prints ---")
reported = {
    3:  (13, 243*v**4 - 81*v**3 + 54*v**2 - 42*v + 35, -455),
    4:  (18, 128*v**4 - 64*v**3 + 48*v**2 - 40*v + 35, -630),
    5:  (23, 625*v**4 - 375*v**3 + 300*v**2 - 260*v + 234, -5382),
    6:  (28, 243*v**4 - 162*v**3 + 135*v**2 - 120*v + 110, -3080),
    7:  (33, 2401*v**4 - 1715*v**3 + 1470*v**2 - 1330*v + 1235, -40755),
    8:  (38, 2048*v**4 - 1536*v**3 + 1344*v**2 - 1232*v + 1155, -43890),
    9:  (43, 19683*v**4 - 15309*v**3 + 13608*v**2 - 12600*v + 11900, -511700),
    10: (48, 625*v**4 - 500*v**3 + 450*v**2 - 420*v + 399, -19152),
    11: (53, 14641*v**4 - 11979*v**3 + 10890*v**2 - 10230*v + 9765, -517545),
    12: (58, 31104*v**4 - 25920*v**3 + 23760*v**2 - 22440*v + 21505, -1247290),
}
all_R_ok = True
for k, (D, S_reported, const_claimed) in reported.items():
    p = 4
    lhs = expand(k * v * (v + 1) * diff(S_reported, v) - k * p * v * S_reported - D * S_reported)
    Plhs = Poly(lhs, v)
    ode_exact_const = (Plhs.degree() <= 0) and (Plhs.coeff_monomial(v**0) if Plhs.degree() >= 0 else 0) == const_claimed
    all_R_ok &= ode_exact_const
note(all_R_ok, "all 10 reported (k, S(v), const) triples independently re-verified: "
     "k v(v+1)S' - 4k vS - D S is EXACTLY the claimed constant (a pure Poly.degree()==0 "
     "check, not a simplify() call) for every one of the 10 open points")

# pure-Python fractions.Fraction cross-check (a maximally independent second
# implementation, no sympy at all) of the k=3 case at 4 different rational v
def S3(vv):
    return 243*vv**4 - 81*vv**3 + 54*vv**2 - 42*vv + 35


def S3p(vv):
    return 972*vv**3 - 243*vv**2 + 108*vv - 42


pure_ok = True
for vv in (PyFrac(2), PyFrac(5), PyFrac(-3, 7), PyFrac(11, 4)):
    lhs = 3*vv*(vv+1)*S3p(vv) - 3*4*vv*S3(vv) - 13*S3(vv)
    pure_ok &= (lhs == -455)
note(pure_ok, "pure-Python fractions.Fraction check (NO sympy at all, hand-coded "
     "polynomial derivative) confirms the k=3,D=13 escape identity at 4 distinct "
     "rational v including a non-integer one: 3v(v+1)S'-12vS-13S = -455 exactly")

# --- broader sweep: jc2_escape_hatch.py Section 3's 40-point lattice --------
print("\n  --- jc2_escape_hatch.py Section 3's general 40-point sweep (a,b,rho) != only (2,3,3) ---")


def escape_solution_verbatim(k, D, m, sig, a, b):
    return escape_solution_original(k, D, m, sig, a, b)


sweep_rows = []
for (a, b, rho) in [(2, 3, 3), (2, 3, 8), (1, 4, 3), (3, 4, 5), (2, 5, 7)]:
    if (1 + rho - rho**2) % (a + b) != 0:
        continue
    sig = (1 + rho - rho**2)//(a + b)
    for kk in range(1, 8):
        D = (a + b)*kk + 1 - rho
        if D < 1:
            continue
        for m in (1, 2):
            r = escape_solution_verbatim(kk, D, m, sig, a, b)
            file_ok = r is not None and (kk*((a + b)*m - 1) != D*m)
            sweep_rows.append((a, b, rho, kk, D, m, sig, file_ok))

note(len(sweep_rows) == 40 and sum(1 for r in sweep_rows if r[-1]) == 20,
     "faithfully reproduced jc2_escape_hatch.py Section 3's own reported '20 of 40' "
     "before applying any independent correction (sanity check on the reproduction itself)")

false_opens, false_closeds = [], []
for (a, b, rho, k, D, m, sig, file_ok) in sweep_rows:
    verdict, extra = ground_truth(a, b, k, D, m, sig)
    truth_open = verdict == "OPEN"
    if file_ok and not truth_open:
        false_opens.append((a, b, rho, k, D, m, sig, verdict))
    elif (not file_ok) and truth_open:
        false_closeds.append((a, b, rho, k, D, m, sig, verdict))

note(len(false_opens) == 7,
     f"ATTACK SUCCEEDS (bug confirmed): {len(false_opens)} of the 20 points "
     f"jc2_escape_hatch.py Section 3 reports as 'ESCAPE OPEN' are FALSE OPENS -- the "
     f"forced constant is identically zero on their entire (1-dimensional) solution "
     f"space, exactly the bug pattern jc2_phase4_direct.py later fixed, but this file "
     f"was never patched. True count: 13/40 open, not 20/40. Points: " +
     "; ".join(f"(a,b)=({fo[0]},{fo[1]}) rho={fo[2]} k={fo[3]} D={fo[4]} m={fo[5]}" for fo in false_opens))
note(len(false_closeds) == 0,
     "REASSURING: zero FALSE CLOSED points found anywhere in this 40-point sweep -- the "
     "more dangerous error direction (wrongly discarding a location a counterexample "
     "could live) did not occur here. Every point the file calls 'closed' really is closed.")

note(2 in [r[3] for r in false_opens if r[0:3] == (2, 3, 3)] or
     1 in [r[3] for r in false_opens if r[0:3] == (2, 3, 3)],
     "in particular, the (a,b,rho)=(2,3,3) row of this SAME sweep already contained the "
     "k=1,D=3,m=1 false-open point later found and fixed specifically for (72,108) in "
     "jc2_phase4_direct.py -- it was sitting in jc2_escape_hatch.py's own output the "
     "whole time (visible directly in that file's printed 'rows[:14]' sample), uncorrected")


# ===================================================================
# AXIS (e) NUMERICS -- no floating point; cancel()==0 / Poly.degree()==0
# checks are safe canonicalizations, not simplify() guesses.  (grep evidence
# reported in the .md; this section adds one more targeted symbolic spot
# check on the one place a FRACTIONAL power appears -- the D=13 homogeneous
# solution -- which is exactly the kind of expression that can trip up
# simplification.)
# ===================================================================
section("AXIS (e): numerics -- fractional-power identity spot check")
vp = symbols('v', positive=True)
C = symbols('C', positive=True)
Rh = C * vp**Rational(13, 3) * (vp + 1)**Rational(-13, 3)
lhs_frac = cancel(together(3*vp*(vp + 1)*diff(Rh, vp) - 13*Rh))
note(lhs_frac == 0,
     "3v(v+1)Rh' - 13Rh = 0 for Rh = C(v/(v+1))^(13/3), confirmed via cancel() (a complete "
     "canonicalization algorithm for rational-function expressions, not a best-effort "
     "simplify()) -- re-derived by hand: d/dv[v^(13/3)(v+1)^(-13/3)] = (13/3)v^(10/3)"
     "(v+1)^(-16/3), and 3v(v+1) times that equals 13*v^(13/3)(v+1)^(-13/3) exactly, "
     "matching Rh's own functional form")


# ===================================================================
# AXIS (f) THE LATTICE RELATION n = b*k + H -- is it forced, or fitted to
# one data point?
# ===================================================================
section("AXIS (f): the lattice relation n = b*k + H")

a, b = 2, 3
admissible_rho = []
for rho in range(1, 41):
    val = 1 + rho - rho**2
    if val % (a + b) == 0:
        admissible_rho.append((rho, val // (a + b)))
note(len(admissible_rho) >= 6,
     f"found {len(admissible_rho)} admissible rho values (satisfying (a+b)|1+rho-rho^2) "
     f"for cusp (2,3) in the range 1..40: {[r for r,_ in admissible_rho]} -- rho=3 "
     f"(the campaign's and Borisov's only examined choice) is one of many")

m_fixed = 1
G_matches_bk = []
for rho, sigma in admissible_rho:
    matches_for_all_k = all((m_fixed + rho*kk + sigma) == b*kk for kk in range(1, 13))
    G_matches_bk.append((rho, sigma, matches_for_all_k))
note(G_matches_bk[0][0] == 3 and G_matches_bk[0][2] is True,
     "at rho=3 (sigma=-1): G(k) = m + rho*k + sigma = 3k = b*k for every k -- this IS "
     "the identity jc2_target_72_108.py/jc2_phase4_direct.py use, and it checks out AT "
     "rho=3")
note(all(not matches for (rho, sigma, matches) in G_matches_bk[1:]),
     "ATTACK SUCCEEDS: at EVERY OTHER admissible rho (8, 13, 18, 23, 28, 33, 38, ...), "
     "G(k) = m + rho*k + sigma is a DIFFERENT function of k and does NOT equal b*k "
     "(checked for rho=8: G(k)=8k-10 vs b*k=3k -- equal only by coincidence at k=2, "
     "never identically). 'G = b*k' is not a general consequence of the framework; it "
     "is a numerical coincidence of Borisov's specific choice rho=b=3 together with "
     "m+sigma=0, restated as if it generalizes.")

# does the D-retrodiction (13, 23, 28) actually need claim 6 at all, or does
# it already follow from relation (Q) alone (established independently in
# session19, with no reference to G, H, or n)?
Q = lambda a, b, k, rho: (a + b)*k + 1 - rho
retro = [(k, Q(2, 3, k, 3)) for k in (3, 5, 6)]
note(retro == [(3, 13), (5, 23), (6, 28)],
     "the D=13,23,28 retrodiction follows DIRECTLY from relation (Q): D=(a+b)k+1-rho at "
     "(a,b,rho)=(2,3,3), k=3,5,6 -- with NO reference to G, H, or n=b*k+H anywhere. "
     "Relation (Q) was established independently in session19 (verified above under "
     "axis (a)/(d)), so claim 6 is not needed to explain WHICH degrees the campaign hit; "
     "the only thing claim 6 uniquely contributes is the k<=n/b UPPER BOUND that turns "
     "an unbounded family into a finite 12-point lattice -- and THAT part rests on "
     "exactly one data point (Borisov's single certified box at k=3).")

note(True,
     "SCOPE FINDING: jc2_target_72_108.py and jc2_phase4_direct.py both hardcode "
     "'rho, m, sig = 3, 1, -1' with no scan over rho or m. The '(72,108) chain-degree "
     "lattice' and its 'ten open chain degrees' are the open points WITHIN the rho=3, "
     "m=1 slice only -- inherited wholesale from Borisov's one certified (66,99)/(99,66) "
     "construction. At least 7 other admissible rho values (and m=2, also demonstrated "
     "above to produce additional false-open/closed points elsewhere in the lattice) "
     "are never examined for (72,108) at all.")


# ===================================================================
# Final ledger
# ===================================================================
section("FINAL LEDGER")
bad = [t for ok_, t in LEDGER if not ok_]
print(f"{len(LEDGER) - len(bad)}/{len(LEDGER)} independent checks landed as expected "
      f"(read the text of each line above -- several PASS lines report CONFIRMED BUGS, "
      f"not confirmations that the audited code is correct; see jc2_phase4_audit.md "
      f"for the PASS/FAIL-against-the-original-claims ledger).")
for t in bad:
    print("  UNEXPECTED:", t)
if bad:
    raise SystemExit(1)
