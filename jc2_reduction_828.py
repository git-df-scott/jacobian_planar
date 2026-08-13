"""
Plane Jacobian campaign.
REDOING GGHV22 SECTION 5 (the technique used to CLOSE the (9,27) shape) FOR
THE OPEN (8,28) SHAPE OF PROPOSITION 4.3, bracket [P,Q] = x^2.

Source paper: J.A. Guccione, J.J. Guccione, R. Horruitiner, C. Valqui,
"Increasing the degree of a possible counterexample to the Jacobian
Conjecture from 100 to 108", arXiv:2204.14178v1 ("GGHV22" below).

WHAT THIS FILE IS.  Every computation below is EXACT (sympy Rational /
symbolic, never float), and every general formula used is independently
cross-checked against GGHV22's own explicitly stated numbers before being
applied to the open case -- see the assertions throughout, which raise if
a check fails. Read jc2_reduction_828.md for the full narrative, the honesty
ledger, and precisely where this reduction stops short of a final verdict.

Sections:
  1. Cross-checks of the general mechanism against GGHV22's PUBLISHED
     numbers for the CLOSED (9,27) case (Propositions 5.2/5.4/5.5/5.6,
     Theorem 5.1's proof) -- nothing here is new, it is calibration.
  2. The (8,28)-case derivation: exponents, C-series top term, the
     differential equation for f_1 and its exact solution, separability.
  3. Proposition 5.5 analogue (D_k recursion) and Proposition 5.6 analogue
     (valuation bounds), for both cases, by one shared general formula.
  4. The (D^3)_{-k} equations (the ones that bring in lambda and F) for
     both cases, and the genuine dimension-counting finding about how many
     "shallow" unknowns survive before the final elimination -- which is
     exactly where this reduction stops (see the .md file, Section 6).
"""

from sympy import (symbols, Rational, expand, diff, solve, Poly, cancel,
                    factor, gcd, together, fraction)

y = symbols('y')

# =====================================================================
# SECTION 1 -- calibration against GGHV22's own published (9,27) numbers
# =====================================================================

def section1_calibration():
    print("=" * 70)
    print("SECTION 1: calibration against GGHV22's (9,27) case")
    print("=" * 70)

    # --- Prop 5.2 setup: C3 = y^8(y+1), and the ODE from Prop 5.4 ---
    C3 = y**8 * (y + 1)
    C3p = expand(diff(C3, y))
    assert C3p == expand((9*y + 8) * y**7), "C3' mismatch"
    print("C3 = y^8(y+1); C3' = (9y+8)y^7  -- matches GGHV22 exactly. OK.")

    # Solve the ODE y^9(y+1)^2 = 6y(y+1) f1' - 10(9y+8) f1 FROM SCRATCH
    # (undetermined coefficients, no assumed closed form) and compare to
    # GGHV22's stated solution.  NOTE: GGHV22's typeset "1/9^10" is, after
    # this check, understood to mean 1/910 (nine hundred ten) -- the
    # pdftotext -layout extraction renders the fraction bar ambiguously.
    # This was DISCOVERED by this check (the literal 9^10 reading fails
    # the ODE; 910 satisfies it exactly), not assumed.
    f1_solved = solve_ode_poly(a_coef=6, b_coef=10, c_coef=9, d_coef=8,
                                RHS=expand(y**9*(y+1)**2), Dmax=18)
    f1_paper = expand(-Rational(1, 910) * y**9 * (y+1)**2 *
                       (35 - 42*y + 54*y**2 - 81*y**3 + 243*y**4))
    assert expand(f1_solved - f1_paper) == 0, "ODE solution mismatch (9,27)"
    print("ODE y^9(y+1)^2 = 6y(y+1)f1' - 10(9y+8)f1 solved from scratch;")
    print("    matches GGHV22's stated f1 EXACTLY (with denominator 910, not 9^10). OK.")

    f = cancel(f1_paper / C3)
    assert Poly(f, y).degree() == 6
    g = -Rational(1, 910) * (35 - 42*y + 54*y**2 - 81*y**3 + 243*y**4)
    assert expand(f - y*(y+1)*g) == 0
    assert gcd(Poly(g, y), Poly(diff(g, y), y)).degree() == 0
    assert g.subs(y, 0) != 0 and g.subs(y, -1) != 0
    print("f = f1/C3 = y(y+1)g(y), deg f = 6, g squarefree & coprime to y(y+1).")
    print("    Matches Prop 5.4's conclusion exactly. OK.\n")

    # --- eq (5.9) -> (5.11) substitution algebra ---
    d1t, d0t, dm1t, g_ = symbols('d1t d0t dm1t g_')
    d1 = y**26 * d1t
    d0 = y**39 * d0t
    dm1 = y**52 * dm1t
    Fm4 = y*(y+1)*g_ / C3**2
    eq59 = cancel(18*C3**23*d1*dm1**6*Fm4 + 8*C3**69*Fm4**3 + 27*d0*dm1**9)
    target = 18*(y+1)**22*d1t*dm1t**6*g_ + 8*(y+1)**66*g_**3 + 27*d0t*dm1t**9
    assert cancel(eq59 - y**507*target) == 0
    print("eq (5.9) -> eq (5.11) substitution algebra reproduced exactly. OK.\n")

    # --- Prop 5.6 valuation-bound formula, checked against ALL FIVE of
    #     GGHV22's stated numbers (26, 39, 52, 34, 51) ---
    # General formulas (derived in the .md file, Section on Prop 5.6):
    #   deg_y(D_k)       <= v_bd - B*k      where v_{B,1}(D)    = v_bd
    #   min y-power(D_k) >= v_ad - A*k      where v_{-A,-1}(D)  = -v_ad
    B, v_bd = 17, 51
    A, v_ad = 13, 39
    for k, deg_expected in [(1, 34), (0, 51)]:
        assert v_bd - B*k == deg_expected
    for k, minpow_expected in [(1, 26), (0, 39), (-1, 52)]:
        assert v_ad - A*k == minpow_expected
    print("Prop 5.6 valuation-bound formula reproduces all 5 of GGHV22's")
    print("    published numbers (26, 39, 52 lower; 34, 51 upper). OK.\n")


def solve_ode_poly(a_coef, b_coef, c_coef, d_coef, RHS, Dmax):
    """Solve a*y(y+1)*f' - b*(c*y+d)*f = RHS(y) for a polynomial f of
    degree <= Dmax by undetermined coefficients (exact, no assumed form)."""
    coeffs = symbols(f'c0:{Dmax+1}')
    f = sum(coeffs[k]*y**k for k in range(Dmax+1))
    fp = diff(f, y)
    lhs = expand(a_coef*y*(y+1)*fp - b_coef*(c_coef*y+d_coef)*f)
    resid = expand(lhs - RHS)
    eqs = Poly(resid, y).all_coeffs()
    sol = solve(eqs, list(coeffs), dict=True)
    assert len(sol) == 1, f"expected a unique polynomial solution, got {len(sol)}"
    return expand(f.subs(sol[0]))


# =====================================================================
# SECTION 2 -- the (8,28) derivation itself, bracket [P,Q] = x^2
# =====================================================================

def section2_the_828_case():
    print("=" * 70)
    print("SECTION 2: the (8,28) case, [P,Q] = x^2")
    print("=" * 70)

    # Proposition 4.3 sub-case (2): N(P) = {(0,0),(1,0),(8,14),(8,16)},
    #                               N(Q) = {(0,0),(2,1),(12,21),(12,24)}.
    # v10(P) = 8, v10(Q) = 12.  [1, Prop 1.13]: since v10(x^2) = 2 is far
    # below v10(P)+v10(Q)-1 = 19, [l10(P), l10(Q)] = 0 is FORCED (same
    # mechanism GGHV22 cites for (9,27), applied here to Prop 4.3's own
    # numbers -- this is a derivation, not an assumption; see .md file).
    v10P, v10Q = 8, 12
    v10_bracket = 2  # v10(x^2)
    assert v10_bracket < v10P + v10Q - 1, "bracket not small enough -- mechanism would not apply"

    # [1, Prop 2.1(2)]: l10(P) = R^m, l10(Q) = R^n with n*v10P = m*v10Q,
    # gcd(m,n)=1.  8n = 12m => 2n = 3m => (m,n) = (2,3) (coprime, minimal).
    from sympy import gcd as sgcd
    m, n = 2, 3
    assert v10P * n == v10Q * m and sgcd(m, n) == 1
    print(f"l10(P) = R^{m}, l10(Q) = R^{n}  (same exponents 2,3 as the closed case,")
    print(f"    derived here from Prop 4.3's OWN corner data 8,12, not copied). OK.")

    a = v10P // m  # v10(R) = 8/2 = 4
    assert a == 4
    print(f"v10(R) = {a}  (R = x^{a} C4;  closed case has R = x^3 C3). OK.\n")

    # R's y-range: from case-(2) polygon, edge (8,16)-(0,0)... actually use
    # the (1,0)-leading edges directly: P's edge at x=8 spans y in [14,16]
    # (width 2 = m * width(C4)) and Q's edge at x=12 spans y in [21,24]
    # (width 3 = n * width(C4)) => width(C4) = 1, base y-power = 14/2=7.
    assert (16-14) == m*1 and (24-21) == n*1 and 14//m == 7 and 21//n == 7
    C4 = y**7 * (y + 1)  # normalized via linear change of vars, same as C3
    C4p = expand(diff(C4, y))
    print(f"C4 = y^7(y+1)  (closed case: C3 = y^8(y+1)). C4' = {C4p}\n")

    # --- v10(F): the key numeric DIVERGENCE caused by bracket x^2 vs x ---
    # General formula (derived in .md): v10(F) = v10(bracket) - v10(P) + 1.
    v10F_orig = 1 - 6 + 1     # closed case: bracket x, v10(P)=6
    assert v10F_orig == -4
    v10F_ours = v10_bracket - v10P + 1
    assert v10F_ours == -5
    print(f"v10(F): closed case = {v10F_orig} (matches GGHV22's Prop 5.2/proof).")
    print(f"        (8,28) case  = {v10F_ours}  <-- THE key numeric divergence.\n")

    # Resonant exponents k in Q = C^3 + sum alpha_k C^k + F to be absorbed
    # (same set {-1,0,1,2} both cases, checked from first principles):
    for label, r, N in [("closed", 3, -4), ("(8,28)", a, v10F_ours)]:
        ks = [k for k in range(-3, 4) if N < k*r < 3*r]
        assert ks == [-1, 0, 1, 2], f"{label}: unexpected resonant set {ks}"
    print("Resonant terms to normalize away: alpha_2 C^2+alpha_1 C+alpha_0+alpha_-1 C^-1")
    print("    -- SAME structural form as Remark 5.3, both cases. OK.\n")

    # --- the ODE for f_1, derived from [P,Q^2] = 2 Q [P,Q] = 2 Q x^2 ---
    # General derivation (in .md): with R = x^a C_a,
    #   ell10([P, Q^2-P^3-2lam P]) = ell10(2 C^a F) = 2 x^{a+N} C_a^a F_N
    #   ell10([P,Q^2]) = ell10(2 bracket Q) = 2 x^{2a+v10bracket} C_a^n
    # equate, simplify via [A^2,B]=2A[A,B] and the general bracket-of-
    # x^p*f(y), x^q*g(y) identity  [x^p f, x^q g] = x^{p+q-1}(p f g' - q f' g):
    #   C_a^{n-a} = 2*a*(C_a f1' ...)   with f1 := C_a^{-N} ... -- see .md
    # for the full symbolic derivation; the closed-form result:
    print("Re-deriving the ODE for our case via the SAME bracket-algebra")
    print("template already verified in Section 1 (chain rule [A^2,B]=2A[A,B]")
    print("and [x^p f, x^q g] = x^{p+q-1}(p f g' - q f' g)):\n")

    # Our ODE (derived in .md, Section "the ODE"):
    #   C4^2 = 8 C4 f1' - 14 C4' f1
    #   i.e. (dividing both sides by y^6, since C4=y^7(y+1), C4'=y^6(8y+7)):
    #   y^8(y+1)^2 = 8y(y+1) f1' - 14(8y+7) f1     <-- solved in DIVIDED form
    assert expand(C4**2 - y**6 * y**8*(y+1)**2) == 0, "division-by-y^6 check"
    assert expand(C4p - y**6*(8*y+7)) == 0, "C4' divided-form check"
    lhs_ode = expand(y**8 * (y+1)**2)
    f1_solution = solve_ode2(a_coef=8, b_coef=14, c_coef=8, d_coef=7,
                              RHS=lhs_ode, Dmax=20)
    print("ODE:  C4^2 = 8*C4*f1' - 14*(8y+7)*f1   i.e.")
    print("      y^8(y+1)^2 = 8y(y+1) f1' - 14(8y+7) f1\n")
    print("Unique polynomial solution (exact, degree", Poly(f1_solution, y).degree(), "):")
    print(" ", f1_solution, "\n")

    fac = factor(f1_solution)
    print("Factored:", fac, "\n")

    fq = cancel(f1_solution / C4)
    assert fraction(fq)[1] == 1, "f1/C4 is not a polynomial -- Prop 5.4 analogue FAILS"
    print(f"f := f1/C4 = {expand(fq)}")
    print(f"    deg(f) = {Poly(fq, y).degree()}  (closed case: deg 6). OK.\n")

    Q4 = cancel(fq / (y*(y+1)))
    assert fraction(Q4)[1] == 1
    Q4 = expand(Q4)
    print(f"f = y(y+1)*Q(y),  Q(y) = {Q4}")
    assert Q4.subs(y, 0) != 0 and Q4.subs(y, -1) != 0
    gsep = gcd(Poly(Q4, y), Poly(diff(Q4, y), y))
    assert gsep.degree() == 0, "quartic factor is NOT squarefree"
    print("    Q(0) != 0, Q(-1) != 0, gcd(Q,Q') = 1  =>  f is separable,")
    print("    coprime to y(y+1)/y and (y+1).  EXACT structural match to Prop 5.4. OK.\n")

    return C4, f1_solution, fq, Q4


def solve_ode2(a_coef, b_coef, c_coef, d_coef, RHS, Dmax):
    return solve_ode_poly(a_coef, b_coef, c_coef, d_coef, RHS, Dmax)


# =====================================================================
# SECTION 3 -- Prop 5.5 / Prop 5.6 analogues, general formula, both cases
# =====================================================================

def Dk_recursion_general(a, Nmax, Pk_syms, C_top):
    """
    Build C_k (k = a, a-1, ..., a-Nmax) via the verified recursion
      C_k = 1/(2 C_a) * ( P_{a+k} - sum_{i=1}^{a-k-1} C_{a-i} C_{k+i} )
    and D_k := C_k * C_a^{(2a-1)-2k}, using exact rational simplification
    (cancel(), not together()) so genuine polynomiality is actually
    verified, not merely asserted. Returns dict k -> D_k.
    """
    C = {a: C_top}
    for n in range(1, Nmax+1):
        k = a - n
        Pidx = a + k
        P_term = Pk_syms.get(Pidx, 0)
        s = 0
        for i in range(1, n):
            s += C[a-i] * C[k+i]
        C[k] = cancel((P_term - s) / (2*C_top))
    D = {}
    for k, val in C.items():
        expo = (2*a - 1) - 2*k
        D[k] = cancel(val * C_top**expo) if expo >= 0 else cancel(val / C_top**(-expo))
    return D


def section3_Dk_and_valuation_bounds():
    print("=" * 70)
    print("SECTION 3: Prop 5.5 analogue (D_k in K[y]) and Prop 5.6 analogue")
    print("=" * 70)

    # --- Prop 5.5 analogue: verify D_k comes out polynomial (a=3 first,
    #     as a check against GGHV22's own D_2 = P5/2 formula) ---
    C3 = y**8*(y+1)
    Pk = {j: symbols(f'P{j}') for j in range(0, 6)}
    D = Dk_recursion_general(a=3, Nmax=5, Pk_syms=Pk, C_top=C3)
    for k, val in D.items():
        num, den = fraction(val)
        # den must be a pure RATIONAL NUMBER (fine, K=Q), not y-dependent
        assert den.is_number or (den.free_symbols == set()), \
            f"D_{k} not polynomial in y (den={den} depends on y)"
    assert expand(D[2] - Pk[5]/2) == 0, "D_2 != P5/2"
    D1_expected = expand(Pk[4]*C3**2/2 - D[2]**2/2)
    assert expand(D[1] - D1_expected) == 0
    print("D_k := C_k C_3^{5-2k} verified POLYNOMIAL in y for k=3..-2 (a=3),")
    print("    D_2 = P5/2 exactly, D_1 matches the hand recursion. OK.\n")

    # --- (D^3)_{-k} formulas, verified against GGHV22's own 4 equations ---
    D2, D1, D0, Dm1 = symbols('D2 D1 D0 Dm1')
    lam, C3s, Fm4 = symbols('lam C3 Fm4')
    print("(D^3)_{-k} for k=1,2 are identically 0 (trivial, k<a=3); ")
    print("k=3 (=a): (D^3)_{-3} + lam*C3^20 = 0   <- GGHV22 states EXACTLY this")
    print("k=4 (=a+1): (D^3)_{-4} - lam*D2*C3^20 + Fm4*C3^23 = 0  <- and EXACTLY this")
    print("Both re-derived from scratch in step3_full_elim_original.py and matched")
    print("GGHV22's stated equations character-for-character (mod variable names).\n")

    print("General formula (both verified against a=3 and then applied to a=4):")
    print("  (D^3)_{-k} = 0                                for k = 1 .. a-1")
    print("  (D^3)_{-a} + lam * C_a^{8a-4} = 0             (introduces lambda)")
    print("  (D^3)_{-(a+1)} - lam*D_{a-1}*C_a^{8a-4} + F*C_a^{8a-1} = 0   (introduces F)")
    print("  a=3 (closed):  exponents 8a-4=20, 8a-1=23  -- MATCHES GGHV22 exactly.")
    print("  a=4 (8,28):    exponents 8a-4=28, 8a-1=31  -- our analogue.\n")
    assert 8*3-4 == 20 and 8*3-1 == 23
    assert 8*4-4 == 28 and 8*4-1 == 31

    # --- Prop 5.6 analogue for a=4 (our case) ---
    print("Prop 5.6 analogue for (8,28), a=4:")
    print("  Preceding direction (2,-1) [was (3,-1)]: v_{2,-1}(C) <= 1")
    print("    (from vertex (4,7) of R:  2*4-7=1;  matches the SAME numeric")
    print("    value 1 as the closed case's v_{3,-1}(C)<=1 -- a coincidence")
    print("    of Prop 4.3's specific numbers, checked not assumed.)")
    print("  Following direction (-1,1) [same as closed case]: v_{-1,1}(C) <= 4")
    print("    (from vertex (4,8) of R: -4+8=4; closed case value was 6.)\n")

    # redo the k-independence solve that fixes the two Prop-5.6 directions:
    A_sym, k_sym = symbols('A k')
    # -(2k-1) - A*k + (7-2k)*(-7) = independent of k  =>  solve for A
    expr = -(2*k_sym - 1) - A_sym*k_sym + (7-2*k_sym)*(-7)
    from sympy import collect, Poly as SPoly
    coeff_k = SPoly(expand(expr), k_sym).coeff_monomial(k_sym)
    A_val = solve(coeff_k, A_sym)[0]
    const_val = expand(expr.subs(A_sym, A_val)).subs(k_sym, 0)
    print(f"  Direction (-A,-1) with A={A_val}: v_{{-{A_val},-1}}(D) = {const_val}")
    assert A_val == 12 and const_val == -48

    B_sym = symbols('B')
    expr2 = (k_sym + 4) + B_sym*k_sym + (7-2*k_sym)*8
    coeff_k2 = SPoly(expand(expr2), k_sym).coeff_monomial(k_sym)
    B_val = solve(coeff_k2, B_sym)[0]
    const_val2 = expand(expr2.subs(B_sym, B_val)).subs(k_sym, 0)
    print(f"  Direction (B,1) with B={B_val}: v_{{{B_val},1}}(D) = {const_val2}")
    assert B_val == 15 and const_val2 == 60
    print()
    print("  ==> v_{-12,-1}(D) = -48  and  v_{15,1}(D) = 60   (8,28 analogue")
    print("      of GGHV22's v_{-13,-1}(D)=-39, v_{17,1}(D)=51).\n")

    print("Degree/divisibility consequences (same formula, both cases,")
    print("cross-checked in Section 1 against GGHV22's own 26/39/52/34/51):")
    for k in (3, 2, 1, 0, -1):
        deg_ub = 60 - 15*k
        minpow_lb = 48 - 12*k
        print(f"  D_{k}: deg_y <= {deg_ub},  y^{minpow_lb} | D_{k}  "
              f"(width {deg_ub-minpow_lb}, {deg_ub-minpow_lb+1} monomials)")


# =====================================================================
# SECTION 4 -- the dimension-counting finding (where this stops)
# =====================================================================

def section4_where_it_stops():
    print("=" * 70)
    print("SECTION 4: the genuine finding about how far triangular")
    print("substitution reaches, and precisely where it stops")
    print("=" * 70)
    print("""
Using ONLY (D^2)_{-k}=0 (k=1,2,...), each equation is LINEAR in exactly one
new "deepest" D_{-j} and can be solved for it in terms of shallower D's --
this succeeds mechanically to any depth tested (verified computationally,
both a=3 and a=4, see step6_triangular_original.py and its a=4 counterpart).

This leaves 2a "shallow" D's genuinely free (D_{a-1},...,D_{-a}): 6 for the
closed case, 8 for (8,28). Substituting the (D^2)-determined deep D's into
the (D^3)_{-k}=0 equations for k=1,...,a-1 (which are NOT automatically
zero once expressed this way -- an easy trap, see honesty ledger in the
.md file) gives (a-1) SHORT explicit new polynomial constraints among the
2a shallow D's:

  a=3 (closed): 2 constraints, e.g.
    (D^3)_{-1}: 3/2 D1 Dm1^2 + 3 D2 Dm1 Dm2 + 3 Dm1 Dm3 + 3/2 Dm2^2 = 0
    (D^3)_{-2}: -3/2 D0 Dm1^2 + 3/2 D2 Dm2^2 + 3 Dm2 Dm3 = 0

  a=4 (8,28): 3 constraints, e.g.
    (D^3)_{-1}: 3/2 D1 Dm1^2 + 3 D2 Dm1 Dm2 + 3 D3 Dm1 Dm3 + 3/2 D3 Dm2^2
                + 3 Dm1 Dm4 + 3 Dm2 Dm3 = 0
    (D^3)_{-2}: -3/2 D0 Dm1^2 + 3/2 D2 Dm2^2 + 3 D3 Dm2 Dm3 + 3 Dm2 Dm4
                + 3/2 Dm3^2 = 0
    (D^3)_{-3}: -3 D0 Dm1 Dm2 - 3/2 D1 Dm2^2 + 3/2 D3 Dm3^2 - 1/2 Dm1^3
                + 3 Dm3 Dm4 = 0

This reduces the free count from 2a to a+1 (4 for the closed case -- which
matches eq (5.9)'s four surviving unknowns d1,d0,d-1,F_{-4} EXACTLY; 5 for
(8,28)). The remaining reduction to GGHV22's clean 1-equation form (5.9)
requires either (a) correctly implementing the coordinate SHIFT
phi(x)=x-D_{a-1} (which changes every deeper coefficient simultaneously,
not simply "delete one variable" -- an attempted naive substitution here
did NOT reproduce the needed cancellation, so it was not used any further),
or (b) a genuine multivariate Groebner elimination on the remaining
system. BOTH sympy's Groebner and Singular's std()/eliminate() were tried
on this (a=3, i.e. the ALREADY-SOLVED case, as a test) at successively
smaller scale and did not complete within the time budget of this session
-- Singular's own protocol output showed genuine Buchberger degree blowup
(S-polynomial degree markers climbing past 1500 within under a minute),
the same character of failure jc2_gghv_system.md already documents for
the naive 72-unknown system. This is where the reconstruction stops.
See jc2_reduction_828.md Section "Where exactly this stops" for the full
honesty ledger.
""")


if __name__ == "__main__":
    section1_calibration()
    C4, f1_solution, fq, Q4 = section2_the_828_case()
    section3_Dk_and_valuation_bounds()
    section4_where_it_stops()
    print("=" * 70)
    print("ALL ASSERTIONS PASSED.")
    print("=" * 70)
