"""
Plane Jacobian campaign - Session 30
RIGOR AUDIT OF SESSION 29, AND THE SECOND CASCADE STEP.

Session 29's closure of the sweep mechanism was challenged on two
points, both about the KIND of claim being made rather than the logic.
The challenge was well aimed - this campaign has twice been bitten by
fitting a relation to a few points (Session 25's linear degree law, fit
to three points and wrong off the fitted range; Session 23's nu = mu*n
before the audit).  Both points are answered here, and the answers are
different from those two cases.

=====================================================================
AUDIT 1  is the top-coefficient result general in k, or point-checked?
=====================================================================

It is PROVED for all k, in one line, and the per-k runs corroborate an
expansion identity rather than carrying the argument.

    Phi = sum_{i=0..k} s^i C_i(t)
    dPhi/dt = sum_{i=0..k} s^i C_i'
    dPhi/ds = sum_{j=1..k} j s^(j-1) C_j
    det JPhi = sum_{i=0..k} sum_{j=1..k} j s^(i+j-1) det[C_i', C_j]

by bilinearity of the determinant.  Now maximise i+j-1 subject to
i <= k and j <= k:

    i + j - 1 = 2k - 1  <=>  i + j = 2k  <=>  i = j = k.

The pair is UNIQUE, so no other term reaches that exponent and no
cancellation is possible:

    coeff(s^(2k-1)) = k * det[C_k', C_k] = k * W(C_k),  EXACTLY, for all k.

THE DIFFERENCE FROM THE EARLIER MISTAKES.  Session 25's degree law was a
formula fitted to three data points with no derivation behind it - it
agreed at a = 8 by coincidence and failed elsewhere.  Here the formula
comes first, from bilinearity plus a one-line integer argument, and the
computations only confirm the expansion.  A fit can be wrong off its
range; "i + j = 2k with i, j <= k forces i = j = k" cannot.

=====================================================================
AUDIT 2  is "degenerate => constant direction" intrinsic to n = 2?
=====================================================================

It is PROVED, and the separation at n >= 3 is proved too, by an explicit
witness - not inferred from the check failing every time it was run.

For v : C^(n-1) -> C^n the mechanism's degeneracy is
det[v_{x1}, ..., v_{x(n-1)}, v] = 0.

  n = 2.  TWO ingredients, each specific to dimension 2:
    (a) the determinant involves exactly TWO vectors, [v', v], so
        degeneracy IS pointwise proportionality v' || v;
    (b) the base is ONE-dimensional, so that proportionality is an ODE
        and integrates.  For C = (p,q) with q != 0,
            (p/q)' = W(C)/q^2,
        so W(C) = 0 <=> p/q is constant <=> C = q(t)(lambda,1).  If
        q = 0 then C = p(t)(1,0).  Converse: W(a(t) e) = 0 identically.
    Hence in the plane degeneracy and constant direction are EQUIVALENT.

  n >= 3.  The determinant involves n >= 3 vectors, and "n vectors
    dependent" is rank <= n-1 out of n, strictly weaker than v being
    proportional to a fixed vector.  Non-vacuous by exhibit: the
    twisted-cubic field of Session 1 has det[v_x, v_y, v] = 0 while
    rank[v, v_x] = 2, so it is degenerate and NOT of constant direction.

So the two conditions coincide in the plane and separate from dimension
three on, both directions established.  The writeup language was right,
but Session 29 stated it as though read off the runs; it is derived.

=====================================================================
NEW  the second cascade step, general in k
=====================================================================

Session 29 stopped after one descent.  Pushing further: with
C_k = a(t) e and e = (0,1), the pairs contributing to s^(2k-2) are
i + j = 2k - 1 with i, j <= k, i.e. exactly (k, k-1) and (k-1, k) - a
two-element list, so again nothing else can enter.  Writing
C_(k-1) = (p, q),

    coeff(s^(2k-2)) = (k-1) det[C_k', C_(k-1)] + k det[C_(k-1)', C_k]
                    = k a p' - (k-1) a' p.

Setting it to zero gives the ODE

    k a p' = (k-1) a' p.

DICHOTOMY.  Either p = 0, in which case C_(k-1) also points along e and
    min(deg_s Phi_1, deg_s Phi_2) <= k-2  -- a SECOND descent;
or a p != 0, and then p'/p = ((k-1)/k)(a'/a), so p^k = c a^(k-1).  At a
root of a of multiplicity m this reads k*ord(p) = (k-1)m, and
gcd(k, k-1) = 1 forces k | m.  Hence

    a = alpha h^k,    p = beta h^(k-1)    for a common polynomial h.

So at every order the top two sweep coefficients are forced to be high
powers of ONE polynomial h - a rigid structure that tightens as k grows.

WHAT THIS DOES AND DOES NOT DO.  It does not close k >= 4: the h-family
is a strong constraint, not a contradiction.  What it gives is a genuine
dichotomy - each level either descends one more s-degree or locks into
the h-structure - and a descent chain that reaches min deg_s <= 2, where
the campaign's Sessions 2-5 theorem finishes, whenever the p = 0 branch
is taken often enough.  Stated as a dichotomy because that is what was
proved; the h-branch at k >= 4 remains open.
"""

from sympy import (symbols, Function, Matrix, expand, simplify, diff,
                   zeros, Poly)

t, s = symbols('t s')

PASS = []


def check(name, ok):
    PASS.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")


print(__doc__)
print("=" * 70)
print("AUDIT 1  the top coefficient is proved, not fitted")
print("=" * 70)
# the integer step, as a general statement over a wide range
viol = [(k, i, j) for k in range(1, 60) for i in range(k + 1)
        for j in range(1, k + 1) if i + j - 1 == 2*k - 1 and (i, j) != (k, k)]
check("i+j = 2k with i,j <= k forces i = j = k  (no violating pair, k<=59)",
      viol == [])
# the expansion identity itself, corroborated per k
allok = True
for K in range(1, 7):
    Cs = [Matrix([Function(f'p{i}')(t), Function(f'q{i}')(t)])
          for i in range(K + 1)]
    Ph = sum((s**i*Cs[i] for i in range(K + 1)), zeros(2, 1))
    lhs = expand(Matrix.hstack(Ph.diff(t), Ph.diff(s)).det())
    rhs = expand(sum(j*s**(i + j - 1)
                     * (Cs[i][0].diff(t)*Cs[j][1] - Cs[i][1].diff(t)*Cs[j][0])
                     for i in range(K + 1) for j in range(1, K + 1)))
    ok = simplify(lhs - rhs) == 0
    allok &= ok
print("   det JPhi = sum_{i,j} j s^(i+j-1) det[C_i',C_j] : corroborated "
      f"for k = 1..6 -> {allok}")
check("the expansion identity holds (bilinearity, checked per k)", allok)
print("   => the result is carried by the PROOF; the runs confirm the")
print("      expansion, they do not establish the general-k claim.")

# =====================================================================
print()
print("=" * 70)
print("AUDIT 2  the dimension claim is derived, both directions")
print("=" * 70)
p, q = symbols('p q', cls=Function)
W = p(t).diff(t)*q(t) - p(t)*q(t).diff(t)
check("(p/q)' = W/q^2 identically, so W = 0 <=> p/q constant",
      simplify(diff(p(t)/q(t), t) - W/q(t)**2) == 0)
a = Function('a')(t)
e1, e2 = symbols('e1 e2')
check("converse: W(a(t)*e) = 0 for any constant direction e",
      simplify((a*e1).diff(t)*(a*e2) - (a*e1)*(a*e2).diff(t)) == 0)
x, y = symbols('x y')
v = Matrix([(1 + x*y)**3, 3*x*(1 + x*y)**2, -x**3])
check("n=3 witness: the twisted-cubic field is degenerate "
      "(det[v_x,v_y,v] = 0)",
      simplify(Matrix.hstack(v.diff(x), v.diff(y), v).det()) == 0)
check("and it is NOT of constant direction (rank[v, v_x] = 2)",
      Matrix.hstack(v, v.diff(x)).rank() == 2)
print("   => coincide in the plane (proved), separate at n >= 3 (witness).")

# =====================================================================
print()
print("=" * 70)
print("NEW  the second cascade step, exact at every order")
print("=" * 70)
viol2 = [(k, i, j) for k in range(2, 60) for i in range(k + 1)
         for j in range(1, k + 1)
         if i + j - 1 == 2*k - 2 and (i, j) not in {(k, k - 1), (k - 1, k)}]
check("only (k,k-1) and (k-1,k) reach s^(2k-2)  (no other pair, k<=59)",
      viol2 == [])
allok2 = True
for K in range(2, 7):
    Cs = [Matrix([Function(f'p{i}')(t), Function(f'q{i}')(t)])
          for i in range(K - 1)]
    Cs.append(Matrix([Function('P')(t), Function('Q')(t)]))
    Cs.append(Matrix([0, Function('A')(t)]))
    Ph = sum((s**i*Cs[i] for i in range(K + 1)), zeros(2, 1))
    JJ = expand(Matrix.hstack(Ph.diff(t), Ph.diff(s)).det())
    got = expand(Poly(JJ, s).coeff_monomial(s**(2*K - 2)))
    want = expand(K*Function('A')(t)*Function('P')(t).diff(t)
                  - (K - 1)*Function('A')(t).diff(t)*Function('P')(t))
    m = simplify(got - want) == 0
    allok2 &= m
    print(f"   k = {K}: coeff(s^(2k-2)) = k a p' - (k-1) a' p  -> {m}")
check("the second-step coefficient is k a p' - (k-1) a' p at every k",
      allok2)

print()
print("   solving  k a p' = (k-1) a' p  over polynomials:")
h = Function('h')(t)
al, be = symbols('alpha beta')
famok = True
for K in range(2, 8):
    resid = simplify(K*(al*h**K)*(be*h**(K - 1)).diff(t)
                     - (K - 1)*(al*h**K).diff(t)*(be*h**(K - 1)))
    famok &= (resid == 0)
check("a = alpha h^k, p = beta h^(k-1) solves the ODE for k = 2..7", famok)
print("   and k | m at every root forces exactly that family, since")
print("   gcd(k, k-1) = 1.")
print()
print("   DICHOTOMY at each level:")
print("     p = 0     -> C_(k-1) also points along e, min deg_s <= k-2")
print("                  (a second descent)")
print("     p != 0    -> a = alpha h^k and p = beta h^(k-1): the top two")
print("                  coefficients are powers of a common h")
check("this is a dichotomy, not a closure: the h-branch at k >= 4 is "
      "NOT ruled out here", True)

print()
print("=" * 70)
print(f"{sum(PASS)}/{len(PASS)} certifications passed.")
print("=" * 70)
print("""
VERDICT ON THE CHALLENGE.

  Both flagged claims are PROVED, not pattern-matched, and the
  distinction from the campaign's two earlier mistakes is concrete: the
  degree law was a fit with no derivation and failed off its range,
  whereas the top-coefficient result follows from bilinearity plus
  "i+j = 2k with i,j <= k forces i = j = k".  Session 29 presented it as
  five checks; that was a presentation error, and the writeup should
  carry the proof, not the table.

  NEW GROUND: the second cascade step, exact at every k, giving the ODE
  k a p' = (k-1) a' p and the dichotomy - descend one more s-degree, or
  lock into a = alpha h^k, p = beta h^(k-1).

  STILL OPEN: the h-branch at k >= 4.  This session does not close it,
  and says so.  No plane counterexample.
""")
assert all(PASS), "a certification failed"
