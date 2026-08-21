"""
Wave 3 - THEOREM W3-2: the weighted-homogeneous collapse, upgraded to a theorem,
         and THEOREM W3-3: the hypothesis that Session 38's summary dropped.

BACKGROUND
----------
Session 38 tested plane Keller maps that are C*-weighted-homogeneous and reported
a total collapse: "22 branches with nonzero constant Jacobian, every one a
diagonal linear map."  Path B (file `39`) records this as "the shape of a
separator" but correctly labels it BOUNDED-DEGREE EVIDENCE, not a theorem, and
records that the degree-uniform proof was attempted and thrown away.

Two things are established here.

  THEOREM W3-2 (degree-uniform, no bound).
  Let P, Q in C[x,y] be weighted-homogeneous for integer weights (a,b) with
  a*b < 0 -- strictly mixed signs -- and let P_x Q_y - P_y Q_x = c, a nonzero
  constant.  Then (P,Q) is linear:  (P,Q) = (c1 x, c2 y)  or  (c1 y, c2 x).

  THEOREM W3-3 (the dropped hypothesis).
  Mixed signs are essential.  For weights (1,m) with m >= 2 -- SAME sign --
  the map  (x, y + x^m)  is weighted-homogeneous, has Jacobian 1, and is
  NOT linear.  So the unrestricted form of the Session 38 collapse claim is
  false, and the separator must be stated with a*b < 0 written in.

Session 38's own sweep had  a > 0 > b  built into its search grid ("11 weight
pairs (a,b) with a > 0 > b").  The hypothesis was in the experiment and absent
from the summary -- the same quantifier-scope failure as H1c (see
FAILURE_ANALYSIS.md, mechanism M3).

PROOF OF W3-2 (each step machine-checked below)
-----------------------------------------------
Write b = -b' with b' > 0, g = gcd(a,b'), u = b'/g, w = a/g, so u,w >= 1 and
gcd(u,w) = 1.  The monomials x^i y^j with a i + b j = p form a single lattice
line, so

    P = x^alpha y^beta  A(s),   Q = x^gamma y^delta B(s),   s = x^u y^w,

with A,B in C[s] and alpha,beta,gamma,delta >= 0 the minimal exponents.

STEP 1 (the s^2 cancellation).  Direct differentiation gives

    P_x Q_y - P_y Q_x
      = x^(alpha+gamma-1) y^(beta+delta-1) * Phi(s),
    Phi(s) = (alpha*delta - beta*gamma) A B
             + s[ (alpha*w - beta*u) A B' + (u*delta - w*gamma) A' B ].

The A'B' terms cancel identically.  Verified symbolically for many (u,w) and
for generic A,B.

STEP 2 (only one power of s can survive).  s = x^u y^w with u,w >= 1, so
distinct powers of s carry distinct (x,y)-exponents.  A constant Jacobian forces
exactly one t with alpha+gamma-1+u t = 0 and beta+delta-1+w t = 0.  t >= 1 forces
alpha=beta=gamma=delta=0 and u=w=1, whence Phi == 0 and c = 0.  So t = 0 and

    alpha + gamma = 1,   beta + delta = 1.

STEP 3 (four cases).  With alpha,gamma,beta,delta >= 0 there are exactly four:

  (alpha,beta,gamma,delta) = (0,0,1,1):  Phi = (u-w) s A' B      -- no constant term
  (1,1,0,0):                             Phi = (w-u) s A B'      -- no constant term
  (1,0,0,1):  P = x A,  Q = y B,  Phi = sum_{i,j} (1 + u i + w j) a_i b_j s^(i+j)
  (0,1,1,0):  P = y A,  Q = x B,  Phi = -sum_{i,j} (1 + w i + u j) a_i b_j s^(i+j)

The first two have no s^0 term, so c = 0: excluded.

STEP 4 (the top-coefficient induction).  In case (1,0,0,1), the coefficient of
s^(degA+degB) in Phi is  (1 + u*degA + w*degB) * a_top * b_top.  Since u,w >= 1
that factor is strictly positive, so a_top*b_top = 0 -- impossible unless one of
A,B is constant; feeding that back, the other is constant too.  Hence
A = a_0, B = b_0 and (P,Q) = (a_0 x, b_0 y) with a_0 b_0 = c.  Case (0,1,1,0) is
the same computation with u,w swapped and gives (a_0 y, b_0 x).            QED

Every step is checked below, and the theorem is additionally confirmed by an
independent brute-force sweep over seven weight pairs at total degree <= 5.
"""

from math import gcd

import sympy as sp

x, y, s = sp.symbols('x y s', positive=True)
PASS = []


def check(name, value, expected=True):
    ok = bool(value) == bool(expected)
    PASS.append((name, ok))
    return ok


# ---------------------------------------------------------------------------
# STEP 1 - the s^2 cancellation, symbolically, for generic A and B.
# ---------------------------------------------------------------------------
print("=" * 78)
print("STEP 1  the A'B' terms cancel:  Phi = K*A*B + s[M*A*B' + N*A'*B]")
print("=" * 78)

al, be, ga, de = sp.symbols('alpha beta gamma delta', integer=True, nonnegative=True)
uu, ww = sp.symbols('u w', integer=True, positive=True)
A = sp.Function('A')
B = sp.Function('B')

S = x ** uu * y ** ww
P = x ** al * y ** be * A(S)
Q = x ** ga * y ** de * B(S)
J = sp.expand(sp.diff(P, x) * sp.diff(Q, y) - sp.diff(P, y) * sp.diff(Q, x))

dA = sp.Subs(sp.Derivative(A(s), s), s, S).doit()
dB = sp.Subs(sp.Derivative(B(s), s), s, S).doit()
K = al * de - be * ga
M = al * ww - be * uu
N = uu * de - ww * ga
Phi = K * A(S) * B(S) + S * (M * A(S) * dB + N * dA * B(S))

# compare in the x*y-cleared form so sympy can combine the symbolic exponents
resid = sp.simplify(sp.powsimp(
    sp.expand(J * x * y - x ** (al + ga) * y ** (be + de) * Phi), force=True))
print(f"    residual  x*y*J - x^(a+g) y^(b+d) Phi  =  {resid}")
check("STEP 1: the identity holds symbolically for generic A, B", resid == 0)

# Numeric corroboration with explicit polynomials, several (u,w,alpha,...).
import random
rnd = random.Random(20260820)
bad = []
for trial in range(24):
    U_, W_ = rnd.randint(1, 4), rnd.randint(1, 4)
    a_, b_, g_, d_ = (rnd.randint(0, 3) for _ in range(4))
    na, nb = rnd.randint(0, 3), rnd.randint(0, 3)
    ac = [sp.Integer(rnd.randint(-4, 4)) for _ in range(na + 1)]
    bc = [sp.Integer(rnd.randint(-4, 4)) for _ in range(nb + 1)]
    Sx = x ** U_ * y ** W_
    Ap = sum(ac[i] * Sx ** i for i in range(na + 1))
    Bp = sum(bc[i] * Sx ** i for i in range(nb + 1))
    Pp = x ** a_ * y ** b_ * Ap
    Qp = x ** g_ * y ** d_ * Bp
    Jp = sp.expand(sp.diff(Pp, x) * sp.diff(Qp, y) - sp.diff(Pp, y) * sp.diff(Qp, x))
    K_ = a_ * d_ - b_ * g_
    M_ = a_ * W_ - b_ * U_
    N_ = U_ * d_ - W_ * g_
    As = sum(ac[i] * s ** i for i in range(na + 1))
    Bs = sum(bc[i] * s ** i for i in range(nb + 1))
    Phis = sp.expand(K_ * As * Bs + s * (M_ * As * sp.diff(Bs, s) + N_ * sp.diff(As, s) * Bs))
    tgt = sp.expand(x ** (a_ + g_ - 1) * y ** (b_ + d_ - 1) * Phis.subs(s, Sx))
    if sp.simplify(sp.expand(Jp - tgt)) != 0:
        bad.append((U_, W_, a_, b_, g_, d_))
print(f"    24 randomized explicit-polynomial instances, mismatches: {bad}")
check("STEP 1: identity confirmed on 24 randomized explicit instances", not bad)

# ---------------------------------------------------------------------------
# STEP 2 - only t = 0 is possible.
# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("STEP 2  a constant Jacobian forces alpha+gamma = 1 and beta+delta = 1")
print("=" * 78)
viol = []
for U_ in range(1, 6):
    for W_ in range(1, 6):
        for t in range(0, 6):
            for a_ in range(0, 4):
                for g_ in range(0, 4):
                    if a_ + g_ - 1 + U_ * t != 0:
                        continue
                    for b_ in range(0, 4):
                        for d_ in range(0, 4):
                            if b_ + d_ - 1 + W_ * t != 0:
                                continue
                            if t == 0:
                                continue
                            # t >= 1 must force the degenerate case
                            deg = (a_ == b_ == g_ == d_ == 0 and U_ == 1 and W_ == 1 and t == 1)
                            if not deg:
                                viol.append((U_, W_, t, a_, b_, g_, d_))
print(f"    exponent solutions with t >= 1 that are NOT the degenerate case: {viol}")
check("STEP 2: every t >= 1 solution is the degenerate u=w=1, all exponents 0", not viol)
# and in that degenerate case Phi vanishes identically
K0, M0, N0 = 0 * 0 - 0 * 0, 0 * 1 - 0 * 1, 1 * 0 - 1 * 0
check("STEP 2: the degenerate case has K = M = N = 0, so Phi == 0 and c = 0",
      K0 == 0 and M0 == 0 and N0 == 0)

# ---------------------------------------------------------------------------
# STEP 3 + 4 - the four cases and the top-coefficient induction.
# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("STEP 3/4  the four cases, and the top-coefficient kill")
print("=" * 78)

cases = [(0, 0, 1, 1), (1, 1, 0, 0), (1, 0, 0, 1), (0, 1, 1, 0)]
check("STEP 3: exactly four exponent cases with alpha+gamma=1, beta+delta=1",
      sorted(cases) == sorted([(a_, b_, g_, d_) for a_ in (0, 1) for g_ in (0, 1)
                               for b_ in (0, 1) for d_ in (0, 1)
                               if a_ + g_ == 1 and b_ + d_ == 1]))

na, nb = 5, 5
ac = sp.symbols(f'a0:{na + 1}')
bc = sp.symbols(f'b0:{nb + 1}')
As = sum(ac[i] * s ** i for i in range(na + 1))
Bs = sum(bc[i] * s ** i for i in range(nb + 1))

for (a_, b_, g_, d_) in cases:
    for (U_, W_) in [(1, 1), (1, 2), (2, 1), (3, 2), (2, 3), (1, 4)]:
        K_ = a_ * d_ - b_ * g_
        M_ = a_ * W_ - b_ * U_
        N_ = U_ * d_ - W_ * g_
        Phis = sp.expand(K_ * As * Bs + s * (M_ * As * sp.diff(Bs, s) + N_ * sp.diff(As, s) * Bs))
        const_term = sp.Poly(Phis, s).coeff_monomial(1)
        if (a_, b_, g_, d_) in [(0, 0, 1, 1), (1, 1, 0, 0)]:
            check(f"case {(a_, b_, g_, d_)} u,w={U_},{W_}: Phi has NO constant term "
                  f"(so c = 0, excluded)", sp.simplify(const_term) == 0)
        else:
            # Phi = sum_{i,j} (1 + U i + W j) a_i b_j s^{i+j}  up to the overall sign
            sign = 1 if (a_, b_, g_, d_) == (1, 0, 0, 1) else -1
            uu_, ww_ = (U_, W_) if (a_, b_, g_, d_) == (1, 0, 0, 1) else (W_, U_)
            model = sign * sp.expand(sum((1 + uu_ * i + ww_ * j) * ac[i] * bc[j] * s ** (i + j)
                                         for i in range(na + 1) for j in range(nb + 1)))
            check(f"case {(a_, b_, g_, d_)} u,w={U_},{W_}: Phi matches the "
                  f"(1 + u i + w j) coefficient model",
                  sp.simplify(sp.expand(Phis - model)) == 0)
            # top coefficient factor is strictly positive
            top = 1 + uu_ * na + ww_ * nb
            check(f"case {(a_, b_, g_, d_)} u,w={U_},{W_}: top factor "
                  f"1+u*degA+w*degB = {top} > 0", top > 0)

print("    all four cases behave as the proof requires")

# ---------------------------------------------------------------------------
# STEP 5 - independent brute force over mixed-sign weights.
# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("STEP 5  independent brute force: mixed-sign weights, total degree <= 5")
print("=" * 78)


def sweep(a, b, dmax):
    out = []
    mons = [(i, j) for i in range(dmax + 1) for j in range(dmax + 1) if i + j <= dmax]
    wts = sorted({a * i + b * j for i, j in mons})
    for p in wts:
        q = a + b - p
        Pm = [(i, j) for i, j in mons if a * i + b * j == p]
        Qm = [(i, j) for i, j in mons if a * i + b * j == q]
        if not Pm or not Qm:
            continue
        Av = sp.symbols(f'A0:{len(Pm)}')
        Bv = sp.symbols(f'B0:{len(Qm)}')
        Pp = sum(Av[k] * x ** i * y ** j for k, (i, j) in enumerate(Pm))
        Qp = sum(Bv[k] * x ** i * y ** j for k, (i, j) in enumerate(Qm))
        Jp = sp.expand(sp.diff(Pp, x) * sp.diff(Qp, y) - sp.diff(Pp, y) * sp.diff(Qp, x))
        pj = sp.Poly(Jp, x, y)
        eqs = [co for mo, co in zip(pj.monoms(), pj.coeffs()) if mo != (0, 0)]
        c0 = pj.coeff_monomial((0, 0))
        for so in sp.solve(eqs + [c0 - 1], list(Av) + list(Bv), dict=True):
            Ps, Qs = sp.simplify(Pp.subs(so)), sp.simplify(Qp.subs(so))
            if Ps == 0 or Qs == 0:
                continue
            if sp.simplify(sp.diff(Ps, x) * sp.diff(Qs, y) - sp.diff(Ps, y) * sp.diff(Qs, x) - 1) != 0:
                continue
            out.append((p, q, Ps, Qs))
    return out


PAIRS = [(1, -1), (2, -1), (1, -2), (3, -2), (2, -3), (3, -1), (1, -3)]
total_branches = 0
for (a, b) in PAIRS:
    res = sweep(a, b, 5)
    total_branches += len(res)
    nonlin = [r for r in res
              if sp.Poly(r[2], x, y).total_degree() > 1 or sp.Poly(r[3], x, y).total_degree() > 1]
    print(f"    weights ({a:2d},{b:2d}):  {len(res)} Keller branches, nonlinear: {len(nonlin)}")
    check(f"brute force ({a},{b}): no nonlinear mixed-sign branch", not nonlin)
check("brute force found Keller branches at all (the sweep is not vacuous)",
      total_branches >= len(PAIRS))

# ---------------------------------------------------------------------------
# THEOREM W3-3 - the dropped hypothesis, with an explicit counterexample.
# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("THEOREM W3-3  same-sign weights: the collapse FAILS")
print("=" * 78)
for m in (2, 3, 4, 7):
    Pc, Qc = x, y + x ** m
    Jc = sp.expand(sp.diff(Pc, x) * sp.diff(Qc, y) - sp.diff(Pc, y) * sp.diff(Qc, x))
    # weighted-homogeneity for weights (1, m): P has weight 1, Q has weight m
    lam = sp.symbols('lam')
    wh_P = sp.simplify(sp.expand(Pc.subs({x: lam * x, y: lam ** m * y}) - lam ** 1 * Pc))
    wh_Q = sp.simplify(sp.expand(Qc.subs({x: lam * x, y: lam ** m * y}) - lam ** m * Qc))
    nonlinear = sp.Poly(Qc, x, y).total_degree() > 1
    print(f"    m = {m}:  (x, y + x^{m}),  weights (1,{m}),  det J = {Jc},  "
          f"wh: {wh_P == 0 and wh_Q == 0},  nonlinear: {nonlinear}")
    check(f"m={m}: det J = 1", sp.simplify(Jc - 1) == 0)
    check(f"m={m}: both components weighted-homogeneous for weights (1,{m})",
          wh_P == 0 and wh_Q == 0)
    check(f"m={m}: the map is NOT linear", nonlinear)
    check(f"m={m}: the weights have the SAME sign (a*b = {1 * m} > 0)", 1 * m > 0)

# and the ab = 0 boundary, computed rather than assumed
print()
print("    boundary case a > 0, b = 0 (y has weight zero):")
res0 = sweep(1, 0, 4)
nonlin0 = [r for r in res0 if sp.Poly(r[2], x, y).total_degree() > 1
           or sp.Poly(r[3], x, y).total_degree() > 1]
print(f"      weights (1,0): {len(res0)} branches, nonlinear: {len(nonlin0)}")
for r in res0[:6]:
    print(f"        p={r[0]} q={r[1]}   P = {r[2]}   Q = {r[3]}")
check("boundary a*b = 0 collapses to affine-linear as well (computed, not assumed)",
      not nonlin0)

# ---------------------------------------------------------------------------
print()
print("=" * 78)
for name, ok in PASS:
    print(("    PASS  " if ok else "    FAIL  ") + name)
print("=" * 78)
print(f"    {sum(1 for _, ok in PASS if ok)}/{len(PASS)} checks passed")
assert all(ok for _, ok in PASS), "w3_weighted_homogeneous_theorem.py: a check FAILED"
print("""    VERDICT
      THEOREM W3-2 (a*b < 0): plane weighted-homogeneous Keller => linear,
        at EVERY degree.  Session 38's bounded-degree evidence is now a
        theorem, and Path B's stated success criterion is met.
      THEOREM W3-3 (a*b > 0): the collapse fails; (x, y + x^m) is an explicit
        nonlinear weighted-homogeneous Keller map.  The separator must carry
        the mixed-sign hypothesis explicitly.""")
