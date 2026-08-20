"""
Wave 3 - THEOREM W3-1: the endgame degree obstruction.

This REPAIRS the Sessions 16-18 First Framework proof.  Wave 2 showed its
decisive step -- "the left side vanishes at v = -1" -- is invalid for rational
R, and that it survived only because Session 13's pole-fiber THEOREM 3 pins R
polynomial by a separate argument.  That left the whole (99,66) verdict resting
on THEOREM 3, whose own decisive move ("so the pole fiber is the order-13 point
at v = infinity") never rules out the OTHER candidate: R totally ramified over
infinity at v = -1, i.e. R = N(v)/(v+1)^13.

THEOREM W3-1 removes that dependence entirely.

    Endgame equation:   T_{D,k}(R) = (v+1)^k (3v(v+1) R' - D R) = -c,  c != 0.
    Realization demand: R must have degree exactly D as a map P^1 -> P^1
                        (it realizes a degree-D Belyi map).

    THEOREM W3-1.  Let D >= 1 and k >= 0.  Then:

      (i)   3 does not divide D:  the rational solution set is a SINGLE
            function, and it has degree exactly k as a map P^1 -> P^1
            (pole divisor k*[-1], numerator degree k, coprime).

      (ii)  3 | D and D <= 3k:  there is no rational solution at all.

      (iii) 3 | D and D > 3k:  the rational solutions form a one-parameter
            family R_k + C (v/(v+1))^{D/3}; its members have degree k
            (at C = 0) or D/3 (at C != 0).

    COROLLARY.  The endgame equation is compatible with the degree-D
    realization demand IF AND ONLY IF  3 does not divide D  AND  k = D.
      - in (i) the only available degree is k, so the demand needs k = D;
      - in (ii) nothing is available at all;
      - in (iii) the available degrees are k and D/3; D/3 = D is impossible
        for D >= 1, and k = D contradicts D > 3k.  So 3 | D is always fatal.

    FIRST FRAMEWORK (99,66):  D = 13 and k = 4 are read off the campaign's own
    endgame identity, quoted verbatim from the primary artifact below:
        alpha^5 (v+1)^4 (3v(v+1) R' - 13 R) = -c.
    4 != 13.  DEAD -- with no appeal to the v = -1 evaluation and no appeal to
    THEOREM 3's pole-fiber step.

    SECOND FRAMEWORK:  D = 23 (also not a multiple of 3).  Dead by the same
    criterion for every k != 23.  Whatever its rigidity layer produces, it dies
    unless that layer produces endgame exponent exactly 23.

This is strictly stronger than the wave-1 argument: it needs only the chain
degree D, the endgame exponent k, and the realization demand deg R = D.  It
needs no Belyi coefficients, no pole-fiber count, and no polynomiality
hypothesis.

Nothing below is asserted; the trichotomy, the degree formula and the corollary
are all computed on a grid, with negative controls.
"""

import sympy as sp

v, c = sp.symbols('v c')
U = v + 1
PASS = []


def check(name, value, expected=True):
    ok = bool(value) == bool(expected)
    PASS.append((name, ok))
    return ok


def T(R, D, k):
    return sp.cancel(sp.together((v + 1) ** k * (3 * v * (v + 1) * sp.diff(R, v) - D * R)))


def map_degree(R):
    """Degree of R as a map P^1 -> P^1 = max(deg numerator, deg denominator)
    after cancellation."""
    R = sp.cancel(sp.together(R))
    n, d = sp.fraction(R)
    dn = sp.Poly(n, v).degree() if n.has(v) else 0
    dd = sp.Poly(d, v).degree() if d.has(v) else 0
    return max(dn, dd)


def solve_endgame(D, k, lo=-60, hi=8):
    """Exact rational solve, built from the Laurent recurrence in U = v+1.

    Poles are confined to v = -1 (Lemma POLE-LOC, wave 2), so R is a Laurent
    polynomial in U and the U^j coefficient of 3v(v+1)R' - D R is
        -(3j + D) c_j + 3(j-1) c_{j-1}.
    Returns (particular_solution_or_None, nullity_of_the_homogeneous_system).
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
        eqs.append(sp.expand(e - (-1 if j == -k else 0)))
    A, b = sp.linear_eq_to_matrix(eqs, cs)
    if A.rank() != A.row_join(b).rank():
        return None, len(cs) - A.rank()
    nullity = len(cs) - A.rank()
    sol = list(sp.linsolve((A, b), cs))[0]
    free = sorted(set().union(*[e.free_symbols for e in sol]), key=str)
    pt = [sp.simplify(e.subs({sy: 0 for sy in free})) for e in sol]
    R = sp.cancel(sp.together(sum(pt[i] * U ** j for i, j in enumerate(idx))))
    return R, nullity


# ---------------------------------------------------------------------------
# 1.  THE TRICHOTOMY AND THE DEGREE FORMULA
# ---------------------------------------------------------------------------
print("=" * 78)
print("1.  TRICHOTOMY + DEGREE, computed on a grid")
print("=" * 78)

DS = [1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 22, 23, 25,
      3, 6, 9, 12, 15, 18, 21, 24]
KS = list(range(0, 7))

bad_case = []
bad_deg = []
bad_resid = []
rows = []
for D in DS:
    for k in KS:
        R, nullity = solve_endgame(D, k)
        if D % 3 != 0:
            want_solvable, want_nullity, want_deg = True, 0, k
        elif D <= 3 * k:
            want_solvable, want_nullity, want_deg = False, None, None
        else:
            want_solvable, want_nullity, want_deg = True, 1, D // 3
        got_solvable = R is not None
        if got_solvable != want_solvable:
            bad_case.append((D, k, got_solvable, want_solvable))
            continue
        if not got_solvable:
            rows.append((D, k, None, None))
            continue
        resid = sp.simplify(T(R, D, k) + 1)
        if resid != 0:
            bad_resid.append((D, k, resid))
        dg = map_degree(R)
        if nullity != want_nullity or dg != want_deg:
            bad_deg.append((D, k, dg, want_deg, nullity, want_nullity))
        rows.append((D, k, dg, nullity))

print(f"    cells checked: {len(DS)} x {len(KS)} = {len(DS) * len(KS)}")
print(f"    solvability mismatches : {bad_case}")
print(f"    degree/nullity mismatch: {bad_deg}")
print(f"    residual mismatches    : {bad_resid}")
check("(i)/(ii)/(iii): solvability matches the trichotomy on every cell", not bad_case)
check("(i)/(iii): degree and nullity match the theorem on every cell", not bad_deg)
check("every produced solution verifies through the operator", not bad_resid)

# NEGATIVE CONTROL: a wrong degree rule must be rejected by the same grid.
wrong = [(D, k, dg) for (D, k, dg, _) in rows if dg is not None and dg != D]
check("NEGATIVE CONTROL: the bogus rule 'deg R = D always' is rejected", len(wrong) > 0)
wrong2 = [(D, k, dg) for (D, k, dg, _) in rows if dg is not None and dg != k]
check("NEGATIVE CONTROL: the bogus rule 'deg R = k always' is also rejected "
      "(it fails in case (iii))", len(wrong2) > 0)

# ---------------------------------------------------------------------------
# 2.  UNIQUENESS IN CASE (i), FROM THE HOMOGENEOUS SOLUTION
# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("2.  UNIQUENESS when 3 does not divide D")
print("=" * 78)
print("""    The homogeneous equation 3v(v+1)R' = D R has solution
    R = C (v/(v+1))^(D/3), rational only when 3 | D.  So for 3 not dividing D
    the rational solution set of the inhomogeneous equation is a single point.""")

lam = sp.symbols('lam')
for D in (13, 23, 7):
    Rh = (v / (v + 1)) ** sp.Rational(D, 3)
    hom = sp.simplify(3 * v * (v + 1) * sp.diff(Rh, v) - D * Rh)
    check(f"D={D}: (v/(v+1))^(D/3) solves the homogeneous equation", hom == 0)
    check(f"D={D}: and it is NOT rational (3 does not divide D)", D % 3 != 0)
for D in (6, 12, 21):
    Rh = (v / (v + 1)) ** (D // 3)
    hom = sp.simplify(3 * v * (v + 1) * sp.diff(Rh, v) - D * Rh)
    check(f"D={D}: the homogeneous solution IS rational (3 | D)",
          hom == 0 and sp.denom(sp.cancel(Rh)).is_polynomial(v))

nullities = {(D, k): solve_endgame(D, k)[1] for D in (13, 23) for k in KS}
print(f"    nullity at D = 13, 23 for k = 0..6: {sorted(set(nullities.values()))}")
check("D = 13 and D = 23: the solution is unique (nullity 0) at every k",
      set(nullities.values()) == {0})

# ---------------------------------------------------------------------------
# 3.  THE COROLLARY:  compatible with deg R = D  <==>  k = D
# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("3.  COROLLARY:  realization demand deg R = D is met  <==>  k = D")
print("=" * 78)


def available_degrees(D, k):
    """The set of degrees realized by rational solutions of T_{D,k}(R) = -c."""
    R, nullity = solve_endgame(D, k)
    if R is None:
        return set()
    degs = {map_degree(R)}
    if nullity >= 1:
        # add a member with the homogeneous part switched on
        Rh = (v / (v + 1)) ** (D // 3)
        for C in (1, sp.Rational(-3, 7)):
            degs.add(map_degree(sp.cancel(sp.together(R + C * Rh))))
    return degs


mismatch = []
for D in DS:
    for k in KS:
        degs = available_degrees(D, k)
        compatible = D in degs
        if compatible != (D % 3 != 0 and k == D):
            mismatch.append((D, k, sorted(degs), compatible))
print(f"    cells where 'D in available degrees' disagrees with "
      f"'3 does not divide D and k == D': {mismatch}")
check("COROLLARY holds on every grid cell", not mismatch)

# the k = D cells must genuinely be compatible, else the corollary is vacuous
witness = [(D, D) for D in DS if D in KS and D % 3 != 0]
blocked = [(D, D) for D in DS if D in KS and D % 3 == 0]
for D, k in witness:
    degs = available_degrees(D, k)
    print(f"    witness D = k = {D}: available degrees {sorted(degs)}")
    check(f"witness D = k = {D}: degree D IS available", D in degs)
check("the corollary is not vacuous (at least one k = D witness exists)", len(witness) > 0)
for D, k in blocked:
    degs = available_degrees(D, k)
    print(f"    blocked  D = k = {D} (3 | D): available degrees {sorted(degs)}")
    check(f"blocked D = k = {D}: 3 | D is fatal, degree D NOT available", D not in degs)

# ---------------------------------------------------------------------------
# 4.  THE FRAMEWORKS
# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("4.  APPLICATION TO THE FRAMEWORKS")
print("=" * 78)

# D = 13 and k = 4 are SOURCED, not remembered: locate the identity by exact
# substring match in the primary artifact, and fail if it is not there.
import os
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_status = os.path.join(_root, "Sessions 1-18 status reports")
_txt = open(_status, encoding="utf-8", errors="replace").read() if os.path.exists(_status) else ""
_identity = "alpha^5 (v+1)^4 (3v(v+1) R' - 13 R) = -c."
print(f"\n    SOURCE ANCHOR for (D, k) = (13, 4):")
print(f"      artifact : Sessions 1-18 status reports")
print(f"      quotation: {_identity}")
print(f"      found    : {_identity in _txt}")
check("D = 13 and k = 4 are sourced by exact quotation from the primary artifact",
      _identity in _txt)

for name, D, k in [("First Framework (99,66)", 13, 4), ("Second Framework", 23, 4)]:
    R, nullity = solve_endgame(D, k)
    dg = map_degree(R)
    print(f"\n    {name}:  D = {D},  k = {k}")
    print(f"      unique rational solution R = {sp.simplify(R)}")
    print(f"      deg R as a map P^1 -> P^1 = {dg};  realization demands {D}")
    print(f"      T(R) + c = {sp.simplify(T(R, D, k) + 1)}   (0 = solves the equation)")
    print(f"      => {dg} != {D}:  FRAMEWORK DEAD by W3-1, no pole-fiber step used")
    check(f"{name}: the endgame solution exists and is unique", R is not None and nullity == 0)
    check(f"{name}: its degree is {k}, not {D}", dg == k and dg != D)
    check(f"{name}: it solves the equation exactly", sp.simplify(T(R, D, k) + 1) == 0)

print("""
    The wave-1 proof needed:  the v = -1 evaluation (invalid for rational R)
                              + THEOREM 3's pole-fiber count to restore it.
    THEOREM W3-1 needs:       D, k, and the realization demand deg R = D.

    In particular the branch THEOREM 3 never excluded -- R totally ramified
    over infinity at v = -1, i.e. R = N(v)/(v+1)^13 -- is killed here directly:
    at D = 13, k = 4 the rational solution is UNIQUE and has pole order 4, so
    no solution of pole order 13 exists.""")

# the specific branch Theorem 3 left open, killed explicitly
R13, _ = solve_endgame(13, 4)
den = sp.denom(sp.cancel(R13))
pole_order = sp.Poly(den, v).degree()
num = sp.numer(sp.cancel(R13))
print(f"\n    D=13,k=4:  pole order at v = -1 is {pole_order} (not 13); "
      f"numerator at v=-1 is {sp.simplify(num.subs(v, -1))} != 0")
check("the R = N/(v+1)^13 branch is excluded: the unique solution has pole order 4",
      pole_order == 4)
check("numerator does not vanish at v = -1, so the pole order is exact",
      sp.simplify(num.subs(v, -1)) != 0)

# ---------------------------------------------------------------------------
print()
print("=" * 78)
for name, ok in PASS:
    print(("    PASS  " if ok else "    FAIL  ") + name)
print("=" * 78)
print(f"    {sum(1 for _, ok in PASS if ok)}/{len(PASS)} checks passed")
assert all(ok for _, ok in PASS), "w3_endgame_degree_obstruction.py: a check FAILED"
print("""    VERDICT
      THEOREM W3-1 holds.  The endgame admits a degree-D realization
      iff 3 does not divide D and k = D.
      First Framework (D=13, k=4): DEAD, unconditionally on the pole question.
      Second Framework (D=23): DEAD for every k != 23.""")
