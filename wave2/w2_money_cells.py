"""
Wave 2, Task 3 - The money cells: D = 13 and D = 23 with k >= 1.

QUESTION
--------
The two live frameworks sit at chain degree D = 13 (First Framework,
degrees (99,66)) and D = 23 (Second Framework).  The endgame equation is

    T_{D,k}(R) := (v+1)^k * ( 3 v (v+1) R'(v) - D R(v) )  =  -c,     c != 0.

Does a RATIONAL solution exist at those D, for k >= 1?

METHOD
------
Exact linear algebra over Q on the ansatz

    R = N(v) / (v+1)^m ,      deg N <= n,

for a rectangle of (m, n).  Nothing is assumed about which (m, n) works: the
whole rectangle is solved and the minimal working cell is reported.  Every
solution found is then substituted back through the operator symbolically and
must return exactly -c.

Independent cross-check: the closed form of THEOREM W2-1
(w2_h1c_refutation.py) predicts solvability iff D is not in {3,6,...,3k}.
Both D = 13 and D = 23 are prime, hence never a multiple of 3, so the closed
form predicts a solution at EVERY k.  The linear algebra below must agree.

NEGATIVE CONTROLS
-----------------
D = 3, 6, 9, 12 with k large enough are unsolvable by the same theorem.  They
are run through the identical code path; if the solver reports a solution
there, the solver is broken and the script fails.
"""

import sympy as sp

v, c = sp.symbols('v c')
PASS = []


def check(name, value, expected=True):
    ok = bool(value) == bool(expected)
    PASS.append((name, ok))
    return ok


def T(R, D, k):
    return sp.cancel(sp.together((v + 1) ** k * (3 * v * (v + 1) * sp.diff(R, v) - D * R)))


def solve_cell(D, k, m, n):
    """Exact solve for R = N(v)/(v+1)^m, deg N <= n.  Returns R or None."""
    a = sp.symbols(f'n0:{n + 1}')
    N = sum(a[i] * v ** i for i in range(n + 1))
    R = N / (v + 1) ** m
    # multiply the equation through by (v+1)^(m+1-k) worth of denominator:
    expr = sp.expand(sp.numer(sp.cancel(sp.together(T(R, D, k) + c))))
    eqs = sp.Poly(expr, v).all_coeffs()
    A, b = sp.linear_eq_to_matrix(eqs, a)
    if A.rank() != A.row_join(b).rank():
        return None
    sol = list(sp.linsolve((A, b), a))[0]
    free = sorted(set().union(*[e.free_symbols for e in sol]) - {c}, key=str)
    sol = [sp.simplify(e.subs({s: 0 for s in free})) for e in sol]
    Rs = sp.cancel(sp.together(sum(sol[i] * v ** i for i in range(n + 1)) / (v + 1) ** m))
    return sp.simplify(Rs)


def minimal_solution(D, k, mmax=8, nmax=8):
    """Smallest (m, n) in the rectangle admitting a solution, and that solution."""
    for tot in range(0, mmax + nmax + 1):
        for m in range(0, min(tot, mmax) + 1):
            n = tot - m
            if n > nmax:
                continue
            R = solve_cell(D, k, m, n)
            if R is not None and sp.simplify(R) != 0:
                return m, n, R
    return None, None, None


print("=" * 78)
print("MONEY CELLS:  D = 13 and D = 23,  k = 1..6")
print("=" * 78)

results = {}
for D in (13, 23):
    print()
    print(f"  --- D = {D} " + "-" * 60)
    for k in range(1, 7):
        m, n, R = minimal_solution(D, k)
        pred = not (D % 3 == 0 and D <= 3 * k)
        got = R is not None
        results[(D, k)] = (m, n, R)
        check(f"D={D}, k={k}: linear algebra agrees with THEOREM W2-1", got == pred)
        if got:
            resid = sp.simplify(T(R, D, k) + c)
            check(f"D={D}, k={k}: solution verified through the operator", resid == 0)
            pole = sp.Poly(sp.denom(sp.cancel(R)), v).degree() if sp.denom(sp.cancel(R)) != 1 else 0
            print(f"    k={k}:  SOLVABLE.  minimal (m,n) = ({m},{n}); pole order at v=-1 = {pole}")
            print(f"           R = {sp.simplify(R)}")
            print(f"           T(R) + c = {resid}")
        else:
            print(f"    k={k}:  no rational solution in the rectangle")

# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("NEGATIVE CONTROLS  (same code path, must come back UNSOLVABLE)")
print("=" * 78)
neg = [(3, 1), (3, 4), (6, 2), (6, 4), (9, 3), (12, 4)]
for D, k in neg:
    m, n, R = minimal_solution(D, k, mmax=6, nmax=6)
    print(f"    D={D:2d} k={k}: solvable = {R is not None}   (expected False)")
    check(f"NEGATIVE CONTROL D={D}, k={k} is unsolvable", R is None)

# positive control that the rectangle is big enough to find things at all
m, n, R = minimal_solution(6, 1, mmax=6, nmax=6)
print(f"    D= 6 k=1: solvable = {R is not None}   (expected True - Wave 2 counterexample)")
check("POSITIVE CONTROL D=6, k=1 is solvable (the section-1 counterexample)", R is not None)
if R is not None:
    print(f"           R = {sp.simplify(R)}")

# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("CONSEQUENCE")
print("=" * 78)
R13 = results[(13, 4)][2]
R23 = results[(23, 4)][2]
print(f"""
    At the First Framework's own exponent k = 4:

      D = 13:  R = {sp.simplify(R13)}
      D = 23:  R = {sp.simplify(R23)}

    Both are rational, both have a pole at v = -1, both satisfy the endgame
    equation exactly.  So:

    * The endgame step CANNOT close D = 13 or D = 23 on its own.  It closes
      them only after polynomiality of R is established independently.
    * At D = 13 that independent step exists inside the First Framework:
      Session 13's THEOREM 3 (pole-fiber) + the degree-13 Belyi realization.
      The (99,66) verdict therefore survives -- conditionally, on THEOREM 3.
    * At D = 23 no analogue of THEOREM 3 is on record in this repository.
      The TRANSFER CONJECTURE's stated mechanism ("fatal whenever D/3 is not
      an integer") is therefore EXACTLY BACKWARDS for rational R: D/3 not an
      integer is precisely the condition under which a rational solution
      EXISTS (THEOREM W2-1).  L4 is not immaterial at D = 23; it is open.
""")

print("=" * 78)
for name, ok in PASS:
    print(("    PASS  " if ok else "    FAIL  ") + name)
print("=" * 78)
print(f"    {sum(1 for _, ok in PASS if ok)}/{len(PASS)} checks passed")
assert all(ok for _, ok in PASS), "w2_money_cells.py: a check FAILED"
