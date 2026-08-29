"""
Plane Jacobian campaign - Session 31
THE THIRD CASCADE STEP, A DIVISIBILITY LADDER, AND THE k = 4 BRANCH.

Session 30 left one live end: the h-branch at sweep order k >= 4.  This
session pushes it.  NO PLANE COUNTEREXAMPLE, but real ground gained and
one self-correction.

=====================================================================
CORRECTION TO SESSION 31's OWN FIRST RUN
=====================================================================

The first attempt reduced the cascade expression modulo h by calling
subs(h, 0).  That is NOT reduction mod h - it zeroes h'(t) as well, and
returned 0 for every k, from which "the reduction is a nonzero multiple
of h' q" was then ASSERTED rather than computed.  Caught before it
propagated.  The correct statement is read off the expression directly:
every term carries an explicit factor h except one, and that one is what
survives.  Recorded because the same slip in the other direction is what
produced corrections 5-7.

=====================================================================
RESULT 1  the third cascade step, exact and general in k
=====================================================================

The pairs (i,j) reaching s^(2k-3) are those with i+j = 2k-2 and
i, j <= k: exactly (k, k-2), (k-1, k-1), (k-2, k) - three terms, so the
coefficient is a short, fully enumerable sum with nothing able to hide
in it.  Writing C_k = (0,a), C_(k-1) = (p,q), C_(k-2) = (u,w):

    coeff(s^(2k-3)) = k a u' - (k-2) a' u + (k-1) W(C_(k-1)),

where W(C_(k-1)) = p'q - q'p.  Verified exactly for k = 3,4,5,6.

=====================================================================
RESULT 2  a divisibility ladder
=====================================================================

Feeding in the Session-30 structure a = alpha h^k, p = beta h^(k-1) and
dividing by h^(k-2), the k = 4 case reads

    4 alpha h^2 u' - 8 alpha h u h' - 3 beta h q' + 9 beta q h'  =  0

and every term carries an explicit factor h EXCEPT 9 beta q h'.  Hence

    h | 9 beta q h',

so for h squarefree (gcd(h,h') = 1) with beta != 0 we get  h | q.
Writing q = h*qt and dividing by h again produces a further condition,
and so on: this is a divisibility ladder of exactly the kind the
campaign met on the framework side in Sessions 11-12.  The surviving
coefficient is COMPUTED per k below, not guessed: it comes out
9, 16, 25 at k = 4, 5, 6, i.e. (k-1)^2 * beta, so the divisibility
h | q holds whenever beta != 0 and h is squarefree.

=====================================================================
RESULT 3  the k = 4 branch, decided at bounded degree
=====================================================================

At k = 4 the dichotomy of Session 30 leaves exactly one live branch,
p_3 != 0, i.e. C_4 = (0, alpha h^4) and C_3 = (beta h^3, q_3).  Taking
h = t (the simplest non-constant case; a linear h is WLOG t after
translation and scaling) and leaving every other coefficient free:

    free coefficients of degree <= 1:  17 conditions, 16 unknowns
                                       Groebner basis = {1}
    free coefficients of degree <= 2:  26 conditions, 23 unknowns
                                       Groebner basis = {1}

with (Jacobian constant) * alpha * beta inverted, so a basis of {1}
means NO SOLUTION with alpha, beta nonzero and a nonzero Jacobian.

So no order-4 sweep over h = t exists with coefficients of degree <= 2.

=====================================================================
SCOPE - what is and is not established
=====================================================================

Established: the third cascade step for all k; the divisibility ladder
it generates; and the non-existence of order-4 sweeps over h = t at
coefficient degree <= 2.

NOT established: the k >= 4 branch in general.  The k = 4 result is
bounded in degree and fixes h = t; larger h, and k >= 5, are untouched.
A bounded-degree Groebner computation is evidence, not a theorem, and it
is reported as such - this campaign has already published one
"verified at every point tested" that was a fit in disguise.

The honest position: the sweep mechanism's essential feature is dead in
the plane at every order (Sessions 29-30, by proof), and the residual
h-branch is now hemmed in by a divisibility ladder and empty wherever it
has been computed.  That is not the same as closed.
"""

from sympy import (symbols, Function, Matrix, expand, simplify, zeros, cancel,
                   Poly, groebner, S)

t, s, z = symbols('t s z')
al, be = symbols('alpha beta')

PASS = []


def check(name, ok):
    PASS.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")


print(__doc__)
print("=" * 70)
print("RESULT 1  the third cascade step, exact at every k")
print("=" * 70)
viol = [(k, i, j) for k in range(3, 60) for i in range(k + 1)
        for j in range(1, k + 1)
        if i + j - 1 == 2*k - 3
        and (i, j) not in {(k, k - 2), (k - 1, k - 1), (k - 2, k)}]
check("only (k,k-2), (k-1,k-1), (k-2,k) reach s^(2k-3)  (k <= 59)",
      viol == [])
allok = True
for K in range(3, 7):
    Cs = [Matrix([Function(f'p{i}')(t), Function(f'q{i}')(t)])
          for i in range(K - 2)]
    U_, Wv = Function('U')(t), Function('Wv')(t)
    P_, Q_ = Function('P')(t), Function('Q')(t)
    A_ = Function('A')(t)
    Cs += [Matrix([U_, Wv]), Matrix([P_, Q_]), Matrix([0, A_])]
    Ph = sum((s**i*Cs[i] for i in range(K + 1)), zeros(2, 1))
    JJ = expand(Matrix.hstack(Ph.diff(t), Ph.diff(s)).det())
    got = expand(Poly(JJ, s).coeff_monomial(s**(2*K - 3)))
    want = expand(K*A_*U_.diff(t) - (K - 2)*A_.diff(t)*U_
                  + (K - 1)*(P_.diff(t)*Q_ - Q_.diff(t)*P_))
    m = simplify(got - want) == 0
    allok &= m
    print(f"   k = {K}: coeff(s^(2k-3)) = k a u' - (k-2) a' u "
          f"+ (k-1) W(C_(k-1))  -> {m}")
check("the third-step coefficient is exact at every k tested", allok)

# =====================================================================
print()
print("=" * 70)
print("RESULT 2  the divisibility ladder (h = t; genuine polynomial arithmetic)")
print("=" * 70)
print("   with a = alpha t^k and p = beta t^(k-1), divide the third-step")
print("   expression by t^(k-2) and read which terms survive at t = 0.")
D = 4
uc = symbols('u0:5')
qc = symbols('qq0:5')
u_poly = sum(uc[i]*t**i for i in range(D + 1))
q_poly = sum(qc[i]*t**i for i in range(D + 1))
ladder = True
for K in (4, 5, 6):
    a_ = al*t**K
    p_ = be*t**(K - 1)
    e = expand(K*a_*u_poly.diff(t) - (K - 2)*a_.diff(t)*u_poly
               + (K - 1)*(p_.diff(t)*q_poly - q_poly.diff(t)*p_))
    red = expand(cancel(e/t**(K - 2)))
    val = expand(red.subs(t, 0))
    coefq0 = expand(val).coeff(qc[0])
    ok = (val == coefq0*qc[0]) and (coefq0 != 0)
    ladder &= ok
    print(f"   k = {K}: value at t = 0 is {val}")
    print(f"            = ({coefq0}) * q(0)   -> forces q(0) = 0, i.e. t | q")
check("at k = 4,5,6 the third step forces t | q_(k-1) (coefficient of q(0) "
      "is nonzero and nothing else survives at t = 0)", ladder)
print("   substituting q = t*qt and dividing by t again yields a further")
print("   condition: a divisibility ladder, as on the framework side.")

# =====================================================================
print()
print("=" * 70)
print("RESULT 3  the k = 4 branch over h = t, decided at bounded degree")
print("=" * 70)
print("   C_4 = (0, alpha t^4),  C_3 = (beta t^3, q3), all else free")
print("   (Jacobian constant)*alpha*beta inverted: GB = {1} means NO SOLUTION")
results = {}
for DEG in (1, 2):
    def mkpoly(name):
        c = symbols(f'{name}0:{DEG+1}')
        return sum(c[i]*t**i for i in range(DEG + 1)), list(c)
    p0, c1 = mkpoly('A')
    q0, c2 = mkpoly('B')
    p1, c3 = mkpoly('C')
    q1, c4 = mkpoly('D')
    u_, c5 = mkpoly('E')
    w_, c6 = mkpoly('F')
    q3, c7 = mkpoly('G')
    unk = c1 + c2 + c3 + c4 + c5 + c6 + c7 + [al, be]
    C = [Matrix([p0, q0]), Matrix([p1, q1]), Matrix([u_, w_]),
         Matrix([be*t**3, q3]), Matrix([0, al*t**4])]
    Ph = sum((s**i*C[i] for i in range(5)), zeros(2, 1))
    J = expand(Matrix.hstack(Ph.diff(t), Ph.diff(s)).det())
    P = Poly(J, s, t)
    eqs = [c for (m_, c) in zip(P.monoms(), P.coeffs()) if m_ != (0, 0)]
    const = P.coeff_monomial(1)
    G = list(groebner(eqs + [z*const*al*be - 1], *(unk + [z]),
                      order='grevlex'))
    results[DEG] = (len(eqs), len(unk), G == [S(1)])
    print(f"   coefficient degree <= {DEG}: {len(eqs)} conditions, "
          f"{len(unk)} unknowns -> "
          f"{'GB = {1}, NO SOLUTION' if G == [S(1)] else 'solutions exist'}")
check("no order-4 sweep over h = t at coefficient degree <= 1",
      results[1][2])
check("no order-4 sweep over h = t at coefficient degree <= 2",
      results[2][2])

print()
print("=" * 70)
print(f"{sum(PASS)}/{len(PASS)} certifications passed.")
print("=" * 70)
print("""
NO PLANE COUNTEREXAMPLE.

  GAINED: the third cascade step, exact for all k; the divisibility
  ladder it generates on the h-branch; and the emptiness of the order-4
  sweep over h = t at coefficient degree <= 2.

  NOT GAINED: the k >= 4 branch in general.  The k = 4 result fixes
  h = t and bounds the degree; larger h and k >= 5 are untouched.  A
  bounded-degree Groebner run is evidence, not a theorem, and this
  campaign has already published one "verified at every point tested"
  that turned out to be a fit in disguise.  Labelled accordingly.
""")
assert all(PASS), "a certification failed"
