"""
w3_odequation_adjudication.py  -  INDEPENDENT ADJUDICATION OF THE ENDGAME ODE.

Three mutually incompatible claims are on the record about

    T_{D,k}(R) := (v+1)^k * ( 3 v (v+1) R'(v) - D R(v) )  =  -c ,   c != 0,

quantified over RATIONAL R:

  [A]  az3geq STATUS 2.1  "H1c, PROVED-exact"
       a rational solution of degree >= 1 exists  IFF  k = 0 and 3 | D.

  [B]  errors-branch THEOREM W2-1
       a rational solution exists  IFF  D not in {3, 6, ..., 3k}.

  [C]  errors-branch THEOREM W3-1 / my earlier E2
       3 !| D            -> unique solution, map-degree exactly k
       3 | D, D <= 3k    -> none
       3 | D, D >  3k    -> one-parameter family, degrees {k, D/3}

This file decides between them with code written from scratch here: a rank /
consistency analysis of the linear system in the numerator coefficients, over
Q with c carried symbolically.  Nothing is imported from any wave1/wave2/wave3
script and no closed form is assumed - the closed forms are only COMPARED to
the table at the end.

Every check below can evaluate false.  Negative controls are marked NEG.
"""
import sympy as sp

v, c = sp.symbols('v c')
RES = []


def rec(name, ok):
    RES.append((name, bool(ok)))
    return bool(ok)


def T(R, D, k):
    return (v + 1) ** k * (3 * v * (v + 1) * sp.diff(R, v) - D * R)


# ---------------------------------------------------------------------------
# core solver: R = N(v) / ( (v+1)^m * v^l ),  deg N <= n.  Exact over Q(c).
# Returns (nullity, list_of_representative_solutions) or None if inconsistent.
# ---------------------------------------------------------------------------
def solve_box(D, k, m, l, n):
    a = sp.symbols('u0:%d' % (n + 1))
    N = sum(a[i] * v ** i for i in range(n + 1))
    R = N / ((v + 1) ** m * v ** l)
    expr = sp.together(T(R, D, k) + c)
    num, _ = sp.fraction(sp.cancel(expr))
    num = sp.expand(num)
    eqs = sp.Poly(num, v).all_coeffs()
    A, b = sp.linear_eq_to_matrix(eqs, a)
    Aug = A.row_join(b)
    if A.rank() != Aug.rank():
        return None                      # inconsistent: no solution in this box
    sol = sp.linsolve((A, b), a)
    tup = list(sol)[0]
    free = sorted({s for e in tup for s in e.free_symbols} & set(a), key=str)
    reps = []
    for assign in [{f: 0 for f in free}] + [
            {f: (1 if f == g else 0) for f in free} for g in free]:
        Rv = sp.cancel(sum(tup[i].subs(assign) * v ** i for i in range(n + 1))
                       / ((v + 1) ** m * v ** l))
        reps.append(sp.simplify(Rv))
    return (len(free), reps)


def mapdeg(R):
    if R == 0:
        return 0
    nu, de = sp.fraction(sp.cancel(R))
    dn = sp.Poly(sp.expand(nu), v).degree() if sp.expand(nu).has(v) else 0
    dd = sp.Poly(sp.expand(de), v).degree() if sp.expand(de).has(v) else 0
    return max(dn, dd)


def poleorder_at_m1(R):
    nu, de = sp.fraction(sp.cancel(R))
    if not sp.expand(de).has(v):
        return 0
    fl = sp.factor_list(sp.expand(de))[1]
    for base, e in fl:
        if sp.simplify(base.subs(v, -1)) == 0:
            return e
    return 0


# ---------------------------------------------------------------------------
# STEP 0.  Exact substitution check of the quoted D = 13, k = 4 solution.
# ---------------------------------------------------------------------------
print("--- 0. substitution check of the recorded D=13,k=4 solution ----------")
kap = sp.Symbol('kappa')
Rq = -kap * (243 * v**4 - 81 * v**3 + 54 * v**2 - 42 * v + 35) / (455 * (v + 1)**4)
lhs = sp.simplify(sp.cancel(sp.together((v + 1)**4 *
                                        (3 * v * (v + 1) * sp.diff(Rq, v) - 13 * Rq))))
print("    (v+1)^4 (3v(v+1)R' - 13R) simplifies to :", lhs)
rec("quoted R satisfies the operator identically, giving exactly kappa", lhs == kap)
rec("quoted R is not a polynomial", sp.fraction(sp.cancel(Rq))[1] != 1)
rec("quoted R has pole order exactly 4 at v = -1", poleorder_at_m1(Rq) == 4)
rec("quoted R has map-degree exactly 4", mapdeg(Rq) == 4)
rec("NEG: a deliberately corrupted numerator does NOT satisfy the identity",
    sp.simplify(sp.cancel(sp.together((v + 1)**4 * (
        3*v*(v+1)*sp.diff(Rq + v/(v+1)**4, v) - 13*(Rq + v/(v+1)**4))))) != kap)

# ---------------------------------------------------------------------------
# STEP 1.  Pole localisation, verified rather than assumed: allow a pole at
# v = 0 and check the solver never needs one.
# ---------------------------------------------------------------------------
print("\n--- 1. do solutions ever need a pole at v = 0? -----------------------")
need0 = []
for (D, k) in [(13, 4), (23, 4), (11, 3), (7, 2), (5, 1), (14, 5), (2, 2)]:
    r = solve_box(D, k, k, 3, k + 3 + 3)      # l = 3 allowed
    if r is None:
        need0.append((D, k, 'none'))
        continue
    nf, reps = r
    orders = set()
    for R in reps:
        if R == 0:
            continue
        _, de = sp.fraction(sp.cancel(R))
        orders.add(0 if sp.simplify(sp.expand(de).subs(v, 0)) != 0 else 1)
    need0.append((D, k, orders))
print("    (D,k) -> {1} would mean a v=0 pole occurred:", need0)
rec("no solution anywhere in the grid has a pole at v = 0",
    all(x[2] == {0} for x in need0 if x[2] != 'none'))

# ---------------------------------------------------------------------------
# STEP 2.  The table.  D = 1..30, k = 0..6.  Classification from rank alone.
# ---------------------------------------------------------------------------
print("\n--- 2. independent classification grid (D <= 30, k <= 6) -------------")
MARGIN = 4
def box_m(D, k):
    """denominator exponent large enough to contain the kernel (v/(v+1))^{D/3}"""
    return max(k, D // 3 if D % 3 == 0 else 0, 1)
table = {}
for k in range(0, 7):
    for D in range(1, 31):
        r = solve_box(D, k, box_m(D, k), 0, box_m(D, k) + MARGIN)
        if r is None:
            table[(D, k)] = ('none', None, None)
        else:
            nf, reps = r
            ds = sorted({mapdeg(R) for R in reps if R != 0})
            pos = sorted({poleorder_at_m1(R) for R in reps if R != 0})
            table[(D, k)] = ('unique' if nf == 0 else 'dim%d' % nf, ds, pos)

hdr = "      k |" + "".join(f"{D:>4d}" for D in range(1, 31))
print(hdr)
for k in range(0, 7):
    row = f"      {k} |"
    for D in range(1, 31):
        st, ds, _ = table[(D, k)]
        row += ("   ." if st == 'none'
                else f"{ds[-1]:>4d}" if st == 'unique'
                else f"{'F':>4s}")
    print(row + "    (. = no solution, n = unique of map-degree n, F = family)")

# ---------------------------------------------------------------------------
# STEP 3.  Adjudicate the three claims cell by cell.
# ---------------------------------------------------------------------------
print("\n--- 3. adjudication, cell by cell -----------------------------------")
viol_A, viol_B, viol_C = [], [], []
for (D, k), (st, ds, pos) in table.items():
    exists = (st != 'none')
    # [A] az3geq 2.1 : solution of degree >= 1 iff k == 0 and 3 | D
    predA = (k == 0 and D % 3 == 0)
    gotA = exists and ds is not None and max(ds) >= 1
    if predA != gotA:
        viol_A.append((D, k, predA, gotA))
    # [B] W2-1 : exists iff D not in {3,...,3k}
    predB = not (D % 3 == 0 and 1 <= D // 3 <= k)
    if predB != exists:
        viol_B.append((D, k, predB, exists))
    # [C] W3-1 / E2  -- stated for k >= 1; k = 0 is outside its domain
    if k == 0:
        continue
    if D % 3 != 0:
        predC = ('unique', k)
    elif D // 3 <= k:
        predC = ('none', None)
    else:
        predC = ('dim1', D // 3)
    if predC[0] == 'none':
        okC = (st == 'none')
    elif predC[0] == 'unique':
        okC = (st == 'unique' and ds == [k])
    else:
        okC = (st == 'dim1' and ds is not None and max(ds) == predC[1])
    if not okC:
        viol_C.append((D, k, predC, (st, ds)))

print(f"    [A] az3geq 2.1 : {len(viol_A)} violated cells out of {len(table)}")
if viol_A:
    print("        first witnesses (D,k,predicted,actual):", viol_A[:6])
print(f"    [B] W2-1       : {len(viol_B)} violated cells out of {len(table)}")
if viol_B:
    print("        first witnesses:", viol_B[:6])
print(f"    [C] W3-1 / E2  : {len(viol_C)} violated cells out of {len(table)}")
if viol_C:
    print("        first witnesses:", viol_C[:6])

rec("[A] az3geq 2.1 is REFUTED by the grid (>0 violated cells)", len(viol_A) > 0)
rec("[B] W2-1 matches the grid on every cell", len(viol_B) == 0)
rec("[C] W3-1 / E2 matches the grid on every cell", len(viol_C) == 0)
rec("[B] and [C] agree with each other on existence everywhere",
    all((not (D % 3 == 0 and 1 <= D//3 <= k)) == (table[(D, k)][0] != 'none')
        for (D, k) in table))

# minimised witness against [A]
w = min([x for x in viol_A if x[1] >= 1], key=lambda t: (t[1], t[0]))
Dw, kw = w[0], w[1]
rw = solve_box(Dw, kw, max(kw, 1), 0, max(kw, 1) + MARGIN)
Rw = sp.simplify(rw[1][0])
print(f"\n    minimal witness against [A]: D = {Dw}, k = {kw}")
print("        R =", Rw)
print("        T(R) + c =", sp.simplify(sp.cancel(sp.together(T(Rw, Dw, kw) + c))))
rec("minimal witness verified by direct substitution",
    sp.simplify(sp.cancel(sp.together(T(Rw, Dw, kw) + c))) == 0)
rec("minimal witness has map-degree >= 1 (so it is in [A]'s own scope)",
    mapdeg(Rw) >= 1)

# the two money cells
print("\n--- 4. the money cells ----------------------------------------------")
for (D, k) in [(13, 4), (23, 4), (13, 13), (23, 23)]:
    st, ds, pos = table.get((D, k), (None, None, None))
    if st is None:
        r = solve_box(D, k, box_m(D, k), 0, box_m(D, k) + MARGIN)
        st, ds = ('none', None) if r is None else (
            'unique' if r[0] == 0 else 'dim%d' % r[0],
            sorted({mapdeg(R) for R in r[1] if R != 0}))
        pos = None if r is None else sorted({poleorder_at_m1(R) for R in r[1] if R != 0})
    print(f"    D={D:3d} k={k:3d}: {st:8s} map-degrees {ds}  pole orders at -1 {pos}")
rec("D=13,k=4 : unique, map-degree 4", table[(13, 4)][0] == 'unique' and table[(13, 4)][1] == [4])
rec("D=23,k=4 : unique, map-degree 4", table[(23, 4)][0] == 'unique' and table[(23, 4)][1] == [4])

# W2-1's seed formula, tested
print("\n--- 5. W2-1's explicit seed formula, tested -------------------------")
def seed(D, k):
    num = (-1)**k * c * sp.factorial(k)
    den = 3 * sp.prod([sp.Rational(D, 3) - i for i in range(k + 1)])
    return sp.simplify(num / den)
seed_ok = []
for (D, k) in [(13, 4), (23, 4), (11, 3), (7, 2), (5, 1), (13, 1), (14, 2)]:
    r = solve_box(D, k, k, 0, k + MARGIN)
    if r is None:
        continue
    R = sp.cancel(r[1][0])
    # W2-1 indexes the LAURENT expansion in U = v+1 (its recurrence runs to j = -k),
    # so c_0 is the U^0 coefficient of R, not N(0).
    U = sp.Symbol('U')
    RU = sp.cancel(sp.together(R.subs(v, U - 1)))
    nu, de = sp.fraction(RU)
    nu, de = sp.expand(nu), sp.expand(de)
    dp = sp.Poly(de, U)
    shift = min(m[0] for m in dp.monoms())
    lead = sp.LC(dp, U) if dp.degree() == shift else None
    # de must be lead*U^shift for the extraction to be a plain coefficient read
    okform = sp.simplify(de - sp.LC(dp, U) * U**shift) == 0
    c0 = sp.simplify(sp.Poly(nu, U).coeff_monomial(U**shift) / sp.LC(dp, U)) if okform else None
    seed_ok.append((D, k, okform and sp.simplify(c0 - seed(D, k)) == 0))
print("    (D,k,seed matches):", seed_ok)
rec("W2-1's seed formula reproduces the constant term in every tested cell",
    all(x[2] for x in seed_ok))

print()
bad = [n for n, o in RES if not o]
for n in bad:
    print("FAILED:", n)
print("w3_odequation_adjudication: %d/%d checks pass" % (len(RES) - len(bad), len(RES)))
raise SystemExit(1 if bad else 0)
