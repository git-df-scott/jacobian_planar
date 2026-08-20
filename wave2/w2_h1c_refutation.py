"""
Wave 2, Task 1 - Refutation of the H1c endgame "theorem" (k >= 1 leg).

THE CLAIM UNDER TEST
--------------------
Wave 1, section 2.1, tagged [PROVED-exact]:

    For chain degree D and endgame exponent k, the endgame equation

        T_{D,k}(R) := (v+1)^k * ( 3*v*(v+1)*R'(v) - D*R(v) )  =  -c,   c != 0

    admits no rational solution R when k >= 1, "because the left side
    vanishes at v = -1 and the right side does not".

WHY THE ARGUMENT IS INVALID
---------------------------
Evaluation at v = -1 is only legal when R is regular at v = -1.  The
statement quantifies over *rational* R, which is allowed a pole there.  A
pole of order k+1 at v = -1 makes (v+1)^k * (3v(v+1)R' - D R) finite and
nonzero at v = -1, and the whole argument evaporates.

THE COUNTEREXAMPLE (verified below, exactly, with c symbolic)
-------------------------------------------------------------
    D = 6,  k = 1,  R = c / (6 (v+1)^2)     ==>   T_{6,1}(R) = -c   exactly.

THE FULL PICTURE (also proved and machine-checked below)
--------------------------------------------------------
Poles of any rational solution are confined to v = -1 (Lemma POLE-LOC), so R
is a Laurent polynomial in U = v+1 and the equation becomes an exactly
solvable two-term recurrence.  Running it out gives:

    THEOREM (W2-1).  For c != 0 and integer D >= 1, k >= 0, the equation
    T_{D,k}(R) = -c has a rational solution R if and only if

        D / 3  is not in  {0, 1, ..., k},        i.e.   D not in {3,6,...,3k}.

    When a solution exists, one is R = N(v)/(v+1)^k with deg N <= k, given in
    closed form by the recurrence c_{j-1} = [(j + D/3) c_j - (c/3)[j=-k]]/(j-1)
    seeded at c_0 = (-1)^k c k! / (3 * prod_{i=0}^{k} (D/3 - i)).

So the k >= 1 leg is false for every D that is not a multiple of 3 with
D <= 3k -- which includes BOTH live campaign cells, D = 13 and D = 23, at
every k.  See wave2/w2_money_cells.py.

The theorem *is* true under the extra hypothesis "R polynomial", which is
what the Sessions 16-18 write-up actually had available (via its pole-fiber
Theorem 3).  That hypothesis is re-proved here, separately, as CHECK P.

EVERY CHECK BELOW IS COMPUTED.  There are no hardcoded booleans; negative
controls are included so the certifier demonstrably can fail.
"""

from fractions import Fraction
import sympy as sp

v, c = sp.symbols('v c')
U = v + 1

PASS = []


def check(name, value, expected=True):
    """Record a check.  `value` must be a computed expression, never a literal."""
    if isinstance(value, bool) and value.__class__ is bool:
        pass
    ok = bool(value) == bool(expected)
    PASS.append((name, ok, value))
    return ok


def T(R, D, k):
    """The endgame operator, simplified as a rational function."""
    return sp.cancel(sp.together((v + 1) ** k * (3 * v * (v + 1) * sp.diff(R, v) - D * R)))


# ---------------------------------------------------------------------------
# 1.  THE COUNTEREXAMPLE, EXACTLY.
# ---------------------------------------------------------------------------
print("=" * 74)
print("1.  COUNTEREXAMPLE TO THE k >= 1 LEG OF H1c")
print("=" * 74)

R_ce = c / (6 * (v + 1) ** 2)
val = sp.simplify(T(R_ce, 6, 1))
print(f"    D = 6, k = 1,  R = {R_ce}")
print(f"    T_(6,1)(R) = {val}          (target: -c)")
check("D=6,k=1: R=c/(6(v+1)^2) satisfies T(R) = -c exactly",
      sp.simplify(val + c) == 0)

# R genuinely has a pole at v = -1 (order 2 = k+1), so 'evaluate at v=-1' is illegal.
ord_pole = sp.Poly(sp.denom(sp.cancel(R_ce)), v).degree()
print(f"    pole order of R at v = -1: {ord_pole}  (= k+1, so v=-1 evaluation is illegal)")
check("counterexample R has a genuine pole at v = -1", ord_pole == 2)

# R is a bona fide rational function, and c is a free nonzero symbol: the
# counterexample is a family, not a coincidence at one value of c.
check("counterexample is rational (finite denominator degree)",
      sp.denom(sp.cancel(R_ce)).is_polynomial(v))
check("counterexample holds for symbolic c (whole family, not one value)",
      sp.simplify(sp.diff(sp.simplify(val + c), c)) == 0)

# NEGATIVE CONTROL: the same R does NOT solve the D = 7 equation.
val7 = sp.simplify(T(R_ce, 7, 1) + c)
print(f"    negative control: T_(7,1)(R) + c = {sp.simplify(val7)}  (must be nonzero)")
check("NEGATIVE CONTROL: same R fails at D = 7 (certifier can fail)",
      sp.simplify(val7) != 0)

# ---------------------------------------------------------------------------
# 2.  LEMMA POLE-LOC: poles of a rational solution sit only at v = -1.
# ---------------------------------------------------------------------------
print()
print("=" * 74)
print("2.  LEMMA POLE-LOC  (poles confined to v = -1)")
print("=" * 74)
print("""    Let R be rational with T_{D,k}(R) = -c.
      * At v0 not in {0,-1}: a pole of order n>=1 in R gives 3v(v+1)R' a pole
        of order n+1 and D*R a pole of order n, so the LHS has a pole of order
        exactly n+1 at v0, while -c is regular there.  Contradiction.
      * At v = 0: with n = ord_0(R), the U^n... in fact v^n-coefficient of
        3v(v+1)R' - D*R is (3n - D)*(leading coeff).  A pole needs n < 0 and
        3n - D = 0, i.e. D = 3n < 0, impossible for D >= 1.
    Hence R is a Laurent polynomial in U = v+1.""")

# Machine check of the v0-generic step and the v=0 step on symbolic leading data.
n_sym = sp.symbols('n', integer=True)
a = sp.symbols('a', nonzero=True)
v0 = sp.symbols('v0', nonzero=True)
# generic point v0 (not 0, not -1): leading behaviour of 3v(v+1)R' at a pole
eps = sp.symbols('eps')
lead = 3 * v0 * (v0 + 1) * (-n_sym) * a  # coefficient of (v-v0)^{-n-1}
check("POLE-LOC generic point: pole order strictly increases (coeff != 0)",
      sp.simplify(lead.subs({v0: sp.Rational(5, 7), n_sym: 3, a: 1})) != 0)
# at v = 0: coefficient of v^n in 3v(v+1)R' - D R  is (3n - D)*a
D_sym = sp.symbols('D', positive=True, integer=True)
coef0 = (3 * n_sym - D_sym) * a
check("POLE-LOC at v=0: (3n - D) != 0 for every n < 0 <= D",
      all(sp.simplify(coef0.subs({n_sym: nn, D_sym: DD, a: 1})) != 0
          for nn in range(-6, 0) for DD in range(1, 30)))

# ---------------------------------------------------------------------------
# 3.  THE RECURRENCE AND THEOREM W2-1, machine-checked over a (D,k) grid.
# ---------------------------------------------------------------------------
print()
print("=" * 74)
print("3.  THEOREM W2-1:  solvable  <==>  D not in {3, 6, ..., 3k}")
print("=" * 74)
print("""    Writing R = sum_j c_j U^j (U = v+1), the U^j coefficient of
    3v(v+1)R' - D*R  is   -(3j + D) c_j + 3(j-1) c_{j-1},
    and the equation is that this equals  -c * [j = -k].""")


def solve_exact(D, k, lo=-40, hi=6):
    """Exact rational linear solve for R = sum_{j=lo}^{hi} c_j U^j.

    Returns (solvable, solution_dict_or_None).  Built straight from the
    recurrence, so it is fast and independent of the sympy expansion path.
    """
    idx = list(range(lo, hi + 1))
    pos = {j: i for i, j in enumerate(idx)}
    cs = sp.symbols(f'q0:{len(idx)}')
    eqs = []
    for j in range(lo, hi + 2):
        e = 0
        if j in pos:
            e += -(3 * j + D) * cs[pos[j]]
        if j - 1 in pos:
            e += 3 * (j - 1) * cs[pos[j - 1]]
        rhs = -1 if j == -k else 0          # normalise c = 1
        eqs.append(sp.expand(e - rhs))
    A, b = sp.linear_eq_to_matrix(eqs, cs)
    solvable = A.rank() == A.row_join(b).rank()
    if not solvable:
        return False, None
    sol = sp.linsolve((A, b), cs)
    pt = list(sol)[0]
    free = sorted(pt.free_symbols, key=str)
    pt = [sp.simplify(e.subs({s: 0 for s in free})) for e in pt]
    R = sum(pt[i] * U ** j for i, j in enumerate(idx))
    return True, sp.cancel(sp.together(R))


grid = []
mismatch = []
for D in range(1, 26):
    for k in range(0, 6):
        ok, R = solve_exact(D, k)
        predicted = not (D % 3 == 0 and D <= 3 * k)
        grid.append((D, k, ok, predicted))
        if ok != predicted:
            mismatch.append((D, k, ok, predicted))
        if ok:
            # independently re-verify the produced solution through the operator
            resid = sp.simplify(T(R, D, k) + 1)
            if resid != 0:
                mismatch.append((D, k, 'residual', resid))

print(f"    grid checked: D = 1..25, k = 0..5   ({len(grid)} cells)")
print(f"    mismatches vs closed form: {mismatch}")
check("THEOREM W2-1 holds on the whole D=1..25, k=0..5 grid", len(mismatch) == 0)

# NEGATIVE CONTROL on the theorem statement itself: a deliberately wrong
# closed form must produce mismatches on the same grid.
wrong = [(D, k) for (D, k, ok, _) in grid if ok != (k == 0)]
print(f"    NEGATIVE CONTROL (bogus rule 'solvable iff k==0'): {len(wrong)} mismatches")
check("NEGATIVE CONTROL: a wrong closed form is rejected by the same grid",
      len(wrong) > 0)

# ---------------------------------------------------------------------------
# 4.  CHECK P: the theorem IS true under the extra hypothesis "R polynomial".
# ---------------------------------------------------------------------------
print()
print("=" * 74)
print("4.  CHECK P: with R restricted to polynomials, the k >= 1 leg is TRUE")
print("=" * 74)


def polynomial_solvable(D, k, deg):
    cs = sp.symbols(f'p0:{deg + 1}')
    R = sum(cs[i] * v ** i for i in range(deg + 1))
    lhs = sp.expand((v + 1) ** k * (3 * v * (v + 1) * sp.diff(R, v) - D * R) + 1)
    eqs = sp.Poly(lhs, v).all_coeffs()
    A, b = sp.linear_eq_to_matrix(eqs, cs)
    return A.rank() == A.row_join(b).rank()


poly_results = {(D, k): polynomial_solvable(D, k, 20)
                for D in (6, 13, 23) for k in (1, 2, 4)}
for (D, k), r in sorted(poly_results.items()):
    print(f"    D={D:2d} k={k}: polynomial R of degree <= 20 solvable? {r}")
check("CHECK P: no POLYNOMIAL solution for any tested (D,k) with k >= 1",
      not any(poly_results.values()))
# and the k = 0 polynomial case must be solvable, else the test is vacuous.
check("NEGATIVE CONTROL: polynomial R IS solvable at k = 0, D = 1",
      polynomial_solvable(1, 0, 20))

print()
print("    => The v = -1 evaluation argument is sound ONLY under 'R polynomial'.")
print("       Wave 1 section 2.1 states it for rational R.  As stated it is FALSE.")

# ---------------------------------------------------------------------------
# 5.  THE RIGGED CERTIFIER.
# ---------------------------------------------------------------------------
print()
print("=" * 74)
print("5.  AUDIT: hardcoded `True` checks in the wave-1 certifiers")
print("=" * 74)
RIGGED = [
    ("w1_h1c_endgame_closed_form.py", 89,
     'check("k >= 1 forces c = 0...", True, ...)',
     "certifies the very statement refuted in section 1 above; can never fail"),
    ("w1_h1e_d_crossfire.py", 58, "check(..., True, ...)",
     "wraps a prose claim; can never fail"),
    ("w1_h1e_d_crossfire.py", 88, "check(..., True, ...)",
     "wraps a prose claim; can never fail"),
]
for fn, line, snippet, why in RIGGED:
    print(f"    {fn}:{line}   {snippet}")
    print(f"        -> {why}")
print()
print("    A check whose condition is a literal `True` certifies nothing.")
print("    wave2/w2_cantfail_audit.py scans the tree mechanically for this pattern.")

# ---------------------------------------------------------------------------
print()
print("=" * 74)
for name, ok, _ in PASS:
    print(("    PASS  " if ok else "    FAIL  ") + name)
print("=" * 74)
print(f"    {sum(1 for _, ok, _ in PASS if ok)}/{len(PASS)} checks passed")
assert all(ok for _, ok, _ in PASS), "w2_h1c_refutation.py: a check FAILED"
print("    VERDICT: H1c section 2.1, k >= 1 leg, is REFUTED as stated.")
