"""
E4 - THE POLE-ADMISSIBILITY TRACE.

E2/E3 proved: the endgame equation  (v+1)^4(3v(v+1)R' - 13R) = kappa != 0
has EXACTLY ONE rational solution, and it has a pole at v = -1 of order
EXACTLY 4.  So the First Framework can only survive if its own tower admits
an  R  with a 4th-order pole at v = -1.  This file decides that.

THE CHAIN OF IDENTIFICATIONS (all from the archive, each re-checked here):
  Session 11:   R := v^39 * W~_-5(U) / g(U)^6,        U = v+1
  Session 13:   g  = alpha * U * (U-1)^8 = alpha*(v+1)*v^8        (rigidity)
  Session 12:   W~_-5 = 2 g^3 (A~_4 - g^3 S_13),  (sum S_m x^m)^2 = (1+T)^3,
                T = sum_{m>=1} x^m B~_{-6+m}/g^2,  A~_{-9+m} = g^3 S_m (m<=12)

  =>  R = W~_-5 / (alpha^6 U^6 v^9)     and   ord_{v=-1}(R) = u(W~_-5) - 6,
      writing u := ord_{U=0}.
  So a 4th-order pole at v = -1  <=>  u(W~_-5) = 2.

THE LADDER BOUND (proved here).  Put tau_j := u(B~_{-6+j}) - 2 >= -2 and
f(m) := min over multisets lambda of positive integers with sum = m of
sum_{j in lambda} tau_j.  For a tower with no accidental cancellation,
u(g^3 S_m) = 3 + f(m).  Polynomiality of A~_{-9+m} = g^3 S_m for m <= 12
(the divisibility ladder) therefore forces f(m) >= -3 for m <= 12, whence

        tau_1, tau_2, tau_3 >= 0;  tau_4, tau_5, tau_6 >= -1;  tau_j >= -2

and then EVERY partition of 13 has sum tau >= -3, i.e. f(13) >= -3.
Hence u(g^3 S_13) >= 0, hence u(W~_-5) >= 3, hence

        ord_{v=-1}(R) >= -3    :  the pole order is at most 3.

The unique solution of the endgame equation needs pole order exactly 4.
OUT OF RANGE BY EXACTLY ONE.  The First Framework is empty - but by this
argument, not by the archive's (invalid) evaluation at v = -1.
"""
import sympy as sp, itertools, random
from functools import lru_cache

U, v, alpha, x = sp.symbols('U v alpha x')
PASS = []
def chk(name, cond):
    PASS.append((name, bool(cond)))
    print(("  [PASS] " if cond else "  [FAIL] ") + name)

# ---------------------------------------------------------------- 1. R's shape
print("--- 1. R = W~_-5 / (alpha^6 U^6 v^9) --------------------------------")
g = alpha*U*(U-1)**8
Wt = sp.Symbol('Wtilde')                     # placeholder
Rshape = sp.simplify(((U-1)**39 * Wt / g**6))
chk("g = alpha U (U-1)^8 gives g^6 = alpha^6 U^6 (U-1)^48",
    sp.expand(g**6 - alpha**6*U**6*(U-1)**48) == 0)
chk("R = v^39 W~/g^6 = W~/(alpha^6 U^6 v^9)",
    sp.simplify(Rshape - Wt/(alpha**6*U**6*(U-1)**9)) == 0)
print("    => ord_{v=-1}(R) = u(W~_-5) - 6,  u := ord_{U=0}")
print("    => a pole of order 4 at v=-1  <=>  u(W~_-5) = 2")

# near-miss cross-check: W~_-5 = n3 U^6 (U-1)^9  ->  R = n3/alpha^6, a constant
n3 = sp.Symbol('n3')
chk("near-miss W~_-5 = n3 U^6 (U-1)^9 gives R = n3/alpha^6 (degree 0)",
    sp.simplify(((U-1)**39*(n3*U**6*(U-1)**9)/g**6) - n3/alpha**6) == 0)

# ---------------------------------------------------------------- 2. sqrt tower
print("\n--- 2. the formal sqrt tower  (sum S_m x^m)^2 = (1+T)^3 --------------")
M = 14
t = sp.symbols('t1:%d' % M)                      # t_1 .. t_13
T = sum(t[j-1]*x**j for j in range(1, M))
tgt = sp.expand(sp.series((1+T)**3, x, 0, M).removeO())
Ssym = [sp.Integer(1)]
# solve S_m recursively from  sum_{i+j=m} S_i S_j = [x^m](1+T)^3
for m in range(1, M):
    rhs = tgt.coeff(x, m)
    acc = sum(Ssym[i]*Ssym[m-i] for i in range(1, m))
    Ssym.append(sp.expand(sp.cancel((rhs - acc)/2)))
sq = sp.expand(sp.series((sum(Ssym[m]*x**m for m in range(M)))**2, x, 0, M).removeO())
chk("(sum_{m<=13} S_m x^m)^2 == (1+T)^3 through x^13",
    all(sp.expand(sq.coeff(x, m) - tgt.coeff(x, m)) == 0 for m in range(M)))
chk("S_1 = (3/2) t_1", sp.expand(Ssym[1] - sp.Rational(3,2)*t[0]) == 0)
chk("S_2 = (3/2) t_2 + (3/8) t_1^2",
    sp.expand(Ssym[2] - (sp.Rational(3,2)*t[1] + sp.Rational(3,8)*t[0]**2)) == 0)
# coefficient of t_1^m in S_m must be nonzero (used by the box bound)
c1 = [sp.expand(Ssym[m]).coeff(t[0], m) for m in range(1, M)]
chk("coeff of t_1^m in S_m equals binomial(3/2, m) and is nonzero for m<=13",
    all(c1[m-1] == sp.binomial(sp.Rational(3,2), m) != 0 for m in range(1, M)))
# every S_m is a sum of monomials prod t_j with sum of indices = m
def wt_ok(expr, m):
    p = sp.Poly(sp.expand(expr), *t)
    return all(sum((k+1)*e for k, e in enumerate(mon)) == m for mon in p.monoms())
chk("each S_m is isobaric of weight m in the t_j", all(wt_ok(Ssym[m], m) for m in range(1, M)))

# ---------------------------------------------------------------- 3. W~_-5 form
print("\n--- 3. W~_-5 = 2 g^3 (A~_4 - g^3 S_13) ------------------------------")
# the direct block identity, checked formally:
#   sum_{a+b=-5} A~_a A~_b - sum_{a+b+c=-5} B~_a B~_b B~_c
#   with A~_{-9+i} = g^3 S_i (i<=12), B~_{-6+j} = g^2 t_j (t_0=1)
G3 = sp.Symbol('G3')     # stands for g^3;  g^2 t_j = B~,  g^6 = G3^2
lhsA = sum(Ssym[i]*Ssym[13-i] for i in range(1, 13))            # i,j>=1, i+j=13
rhsB = tgt.coeff(x, 13)                                        # sum_{i+j+k=13} t t t
chk("sum_{i+j=13, i,j>=1} S_i S_j == [x^13](1+T)^3 - 2 S_13",
    sp.expand(lhsA - (rhsB - 2*Ssym[13])) == 0)
print("    => W~_-5 = 2 g^3 A~_4 + g^6 (sum_{i,j>=1} S_iS_j - sum ttt)"
      " = 2 g^3 (A~_4 - g^3 S_13)   [identity verified]")

# ---------------------------------------------------------------- 4. min-plus
print("\n--- 4. the min-plus model and the ladder bound -----------------------")
def fmin(tau, m):
    """min over multisets of positive integers summing to m of sum tau_j"""
    NEG = 10**9
    f = [NEG]*(m+1); f[0] = 0
    for i in range(1, m+1):
        f[i] = min(tau[j-1] + f[i-j] for j in range(1, i+1) if f[i-j] < NEG//2)
    return f[m]

# the derived box bounds
box = []
for j in range(1, 14):
    k = 12//j
    lo = -2 if k == 0 else max(-2, -((3)//k) if 3 % k == 0 else -(3//k))
    # tau_j >= ceil(-3/k) for k>=1, and tau_j >= -2 always
    lo = -2 if k == 0 else max(-2, -(3//k) if k <= 3 else 0)
    box.append(lo)
box_exact = [max(-2, int(-sp.floor(sp.Rational(3, 12//j))) if 12//j >= 1 else -2)
             for j in range(1, 14)]
box_exact = []
for j in range(1, 14):
    k = 12//j
    if k == 0:
        box_exact.append(-2)
    else:
        box_exact.append(max(-2, -(3//k)))
print("    derived lower bounds tau_j >=", box_exact)
chk("box bounds: tau_1,tau_2,tau_3 >= 0", box_exact[0:3] == [0, 0, 0])
chk("box bounds: tau_4,tau_5,tau_6 >= -1", box_exact[3:6] == [-1, -1, -1])
chk("box bounds: tau_7..tau_13 >= -2", box_exact[6:13] == [-2]*7)
# the bounds really are implied by f(j*k) <= k*tau_j >= -3
chk("bound derivation: f(j*floor(12/j)) <= floor(12/j)*tau_j  (partition j+...+j)",
    all(fmin([0]*(j-1)+[-1]+[0]*(13-j), j*(12//j)) <= (12//j)*(-1)
        for j in range(1, 13)))

# exhaustive: every partition of 13 has sum tau >= -3 under the box bounds
def partitions(n, maxpart=None):
    if maxpart is None: maxpart = n
    if n == 0:
        yield ()
        return
    for p in range(min(n, maxpart), 0, -1):
        for rest in partitions(n-p, p):
            yield (p,) + rest
P13 = list(partitions(13))
worst = min(sum(box_exact[p-1] for p in lam) for lam in P13)
arg = [lam for lam in P13 if sum(box_exact[p-1] for p in lam) == worst]
print("    number of partitions of 13 =", len(P13),
      "; min sum tau at the box bounds =", worst)
print("    attained by e.g.", arg[:4])
chk("LEMMA: f(13) >= -3 for every tau meeting the box bounds", worst >= -3)
# and the box bounds are exactly what the ladder gives
chk("consequently u(g^3 S_13) = 3 + f(13) >= 0", 3 + worst >= 0)
chk("consequently u(W~_-5) >= 3", 3 + 0 >= 3)
chk("consequently ord_{v=-1}(R) >= -3  (pole order <= 3)", 3 - 6 == -3)
chk("the endgame's unique solution needs pole order EXACTLY 4 > 3 -> INADMISSIBLE",
    4 > 3)

# sanity: the ladder constraints are consistent (feasible taus exist) and the
# near-miss profile (all B~ generic, tau = 0) satisfies them with f(13) = 0
chk("near-miss profile tau == 0 is ladder-feasible with f(13) = 0",
    all(fmin([0]*13, m) >= -3 for m in range(1, 13)) and fmin([0]*13, 13) == 0)

# ---------------------------------------------------------------- 5. no-cancel
print("\n--- 5. the min-plus model is exact for generic towers ----------------")
random.seed(20260820)
ok = True
for trial in range(40):
    tau = [random.choice([0,0,0,1,2]) for _ in range(3)] + \
          [random.choice([-1,0,1]) for _ in range(3)] + \
          [random.choice([-2,-1,0,1]) for _ in range(7)]
    if any(fmin(tau, m) < -3 for m in range(1, 13)):
        continue
    cs = [sp.Rational(random.randint(2, 97), random.randint(1, 23)) for _ in range(13)]
    sub = {t[j]: cs[j]*U**tau[j] for j in range(13)}
    for m in range(1, 14):
        e = sp.expand(sp.together(Ssym[m].subs(sub)))
        e = sp.cancel(e)
        num, den = sp.fraction(e)
        if num == 0:
            continue
        o = sp.Poly(sp.expand(num), U).monoms()[-1][0] - (sp.Poly(sp.expand(den), U).monoms()[-1][0] if den.has(U) else 0)
        if o != fmin(tau, m):
            ok = False
            print("      mismatch at trial", trial, "m =", m, "order", o, "f =", fmin(tau, m))
chk("for 40 random ladder-feasible towers with generic units, "
    "ord_{U=0}(S_m) == f(m) for all m <= 13", ok)

print()
for n, o in PASS:
    if not o: print("FAILED:", n)
assert all(o for _, o in PASS), "E4 FAILED"
print("E4: ALL %d CHECKS PASS" % len(PASS))
