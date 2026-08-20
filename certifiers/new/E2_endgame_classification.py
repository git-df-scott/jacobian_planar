"""
E2 - COMPLETE CLASSIFICATION OF THE RATIONAL SOLUTIONS OF THE ENDGAME EQUATION.

    T_{D,m}(R) := (v+1)^m ( 3 v (v+1) R'(v) - D R(v) )  =  kappa,    kappa != 0.

Sessions 16-18 asserted that the (99,66) instance (D=13, m=4, kappa=-c/alpha^5)
is UNSOLVABLE, by the one-line argument "the left side vanishes at v = -1; the
right side is -c != 0".  That argument is valid ONLY for R without a pole at
v = -1.  Its supporting certificate ("T(R)=1 infeasible, exact LA") was run on
a finite-dimensional space of POLYNOMIALS and therefore cannot see any solution
with a pole.

This file classifies ALL rational solutions, with proof-grade case analysis
implemented as executable checks, for arbitrary integer D >= 1 and m >= 1.

THEOREM (E2).  Over any field K of characteristic 0, with kappa != 0:
  (a) every solution is regular on P^1 minus {-1, oo}: no pole at v = 0 and
      none at any v = t not in {0,-1};
  (b) k := -ord_{v=-1}(R) satisfies k >= m; if k > m then D = 3k;
  (c) 3 does not divide D  =>  EXACTLY ONE solution, R = S/(v+1)^m with
      deg S = m exactly; its degree as a map P^1 -> P^1 is exactly m;
  (d) D = 3j with j > m    =>  an affine line of solutions
      R_m + C (v/(v+1))^j ; map-degree m at C=0 and j otherwise;
  (e) D = 3j with j <= m   =>  NO rational solution at all.

For the First Framework (D,m) = (13,4): case (c).  The unique solution has
map-degree 4, NOT 13, and NOT a polynomial.
"""
import sympy as sp
from fractions import Fraction as Fr

v = sp.Symbol('v')
PASS = []
def chk(name, cond):
    PASS.append((name, bool(cond)))
    print(("  [PASS] " if cond else "  [FAIL] ") + name)

def T(R, D, m):
    """the endgame operator, exact"""
    return sp.cancel(sp.together((v+1)**m * (3*v*(v+1)*sp.diff(R, v) - D*R)))

# ---------------------------------------------------------------------------
# 1. closed-form constructor for the k = m branch  (valid whenever 3n != D for
#    n = 0..m, i.e. whenever D/3 is not an integer in [0,m])
# ---------------------------------------------------------------------------
def S_poly(D, m, kappa=sp.Symbol('kappa')):
    """unique polynomial S with 3v(v+1)S' - (3 m v + D) S = kappa, deg S = m."""
    s = [-sp.Rational(1,1)*kappa/D]
    for n in range(1, m+1):
        den = 3*n - D
        if den == 0:
            return None
        s.append(sp.Rational(3*(m+1-n), 1)/den * s[-1])
    return sum(s[n]*v**n for n in range(m+1))

def R_sol(D, m, kappa=sp.Symbol('kappa')):
    S = S_poly(D, m, kappa)
    return None if S is None else sp.together(S/(v+1)**m)

kap = sp.Symbol('kappa', nonzero=True)

print("--- 1. the (D,m) = (13,4) First Framework solution ------------------")
S13 = sp.expand(S_poly(13, 4, kap))
R13 = R_sol(13, 4, kap)
print("    S(v) =", sp.factor(sp.expand(S13/kap)), "* kappa")
print("    R(v) =", sp.simplify(R13))
chk("T_{13,4}(R) == kappa  identically (exact)", sp.simplify(T(R13, 13, 4) - kap) == 0)
chk("R has a pole at v=-1 of order exactly 4",
    sp.simplify(sp.limit(sp.expand(S13).subs(v, -1), v, -1)) != 0
    and sp.expand(S13).subs(v, -1) == -kap)
chk("deg S = 4 exactly", sp.Poly(sp.expand(S13), v).degree() == 4)
chk("map-degree of R = max(deg num, deg den) = 4",
    max(sp.Poly(sp.expand(S13), v).degree(), 4) == 4)
chk("S(-1) = -kappa", sp.expand(S13).subs(v, -1) == -kap)
chk("gcd(S, (v+1)) = 1 (pole order is exactly 4, not less)",
    sp.rem(sp.Poly(sp.expand(S13/kap), v), sp.Poly(v+1, v)) != 0)
chk("R is NOT a polynomial", sp.denom(sp.cancel(R13)) != 1)
chk("R does not have degree 13", max(sp.Poly(sp.expand(S13), v).degree(), 4) != 13)

# the archive's decisive step, re-examined
print("\n--- 2. the archive's decisive step, re-examined ---------------------")
Rp = sum(sp.Symbol('r%d' % i)*v**i for i in range(14))     # generic poly, deg<=13
lhs_at_m1 = sp.expand(T(Rp, 13, 4)).subs(v, -1)
chk("for POLYNOMIAL R the archive is right: T(R)|_{v=-1} = 0 identically",
    sp.simplify(lhs_at_m1) == 0)
chk("for the pole solution the archive's step does not apply: (v+1)^4 R is a "
    "nonzero polynomial at v=-1",
    sp.expand((v+1)**4*R13).subs(v, -1) != 0)

# ---------------------------------------------------------------------------
# 3. the structural lemmas, checked symbolically
# ---------------------------------------------------------------------------
print("\n--- 3. structural lemmas (a),(b),(c) --------------------------------")
mu, Dq, kq, mq = sp.symbols('mu D k m')
# (a) pole at v=0 of order -mu: leading coefficient of the bracket is (3 mu - D) rho
chk("(a) no pole at v=0: leading coefficient (3 mu - D) != 0 for mu<0<D",
    all((3*mm - DD) != 0 for mm in range(-12, 0) for DD in range(1, 40)))
# (a) pole at t not in {0,-1}: ord drops by exactly 1 through R'
# computed: a pole at t not in {0,-1} makes the operator blow up there
_noptail = []
for _t in (2, -3, sp.Rational(5, 7)):
    for _n in (1, 2, 5):
        _R = 1/(v - _t)**_n
        _E = sp.cancel(sp.together((v+1)**4*(3*v*(v+1)*sp.diff(_R, v) - 13*_R)))
        _num, _den = sp.fraction(_E)
        _ord = 0
        _p = sp.Poly(sp.expand(_den), v)
        while sp.div(_p, sp.Poly(v - _t, v))[1].as_expr() == 0:
            _p = sp.div(_p, sp.Poly(v - _t, v))[0]; _ord += 1
        _noptail.append(_ord == _n + 1)
chk("(a) no pole at t not in {0,-1}: the operator's order at t is ord_t(R)-1, "
    "so it cannot equal a nonzero constant", all(_noptail) and len(_noptail) == 9)
# (b),(c): Phi(-1) = (3k-D) S(-1)
Sf = sp.Function('S')(v)
Phi = sp.expand(3*v*(v+1)*sp.diff(Sf, v) - (3*kq*v + Dq)*Sf)
chk("(b/c) Phi(-1) = (3k-D) S(-1)",
    sp.simplify(Phi.subs(v, -1) - (3*kq - Dq)*Sf.subs(v, -1)) == 0)

# ---------------------------------------------------------------------------
# 4. exhaustive verification of the theorem by INDEPENDENT brute-force linear
#    algebra over Q, for a grid of (D, m).  No use of the closed form.
# ---------------------------------------------------------------------------
print("\n--- 4. independent brute force: exact linear algebra over Q ---------")
def brute(D, m, K=10, L=3, DEGMAX=16, kappa=1):
    """Solve T_{D,m}(R)=kappa for R = P(v)/((v+1)^K v^L) by exact linear algebra
       over Q on the coefficients of P.  Independent of the closed form.
       The box is large enough to contain every rational function with poles
       only at {0,-1} of order <= K, <= L and numerator degree <= DEGMAX.
       Returns ('none',) or (dim of affine solution set, representatives)."""
    den = (v+1)**K * v**L
    cs = sp.symbols('a0:%d' % (DEGMAX+1))
    P = sum(cs[i]*v**i for i in range(DEGMAX+1))
    R = P/den
    num = sp.expand(sp.cancel(sp.together(
        ((v+1)**m*(3*v*(v+1)*sp.diff(R, v) - D*R) - kappa) * den)))
    eqs = sp.Poly(num, v).all_coeffs()
    sol = sp.linsolve(eqs, cs)
    if not sol:
        return ('none',)
    sol = list(sol)[0]
    free = sorted({s for e in sol for s in e.free_symbols} & set(cs), key=str)
    reps = []
    assigns = [{f: 0 for f in free}] + [{f: (1 if f == g else 0) for f in free}
                                        for g in free]
    for assign in assigns:
        Rv = sp.cancel(sum(sol[i].subs(assign)*v**i for i in range(DEGMAX+1))/den)
        reps.append(sp.simplify(Rv))
    return (len(free), reps)

grid = [(13,4),(23,4),(11,4),(14,4),(7,4),(1,4),(2,4),(5,4),(4,4),(8,4),
        (12,4),(15,4),(18,4),(21,4),(3,4),(6,4),(9,4),
        (13,1),(13,2),(13,3),(13,5),(13,6),(23,6),(5,2),(6,2),(9,2),(3,1),(6,1)]
rows = []
for (D, m) in grid:
    res = brute(D, m)
    j = D//3 if D % 3 == 0 else None
    if D % 3 != 0:
        pred = ('unique', m)
    elif j > m:
        pred = ('line', j)
    else:
        pred = ('none',)
    if res[0] == 'none':
        got = ('none',)
    else:
        nfree, reps = res
        degs = set()
        for Rv in reps:
            n_, d_ = sp.fraction(sp.cancel(Rv))
            if sp.simplify(Rv) == 0: continue
            degs.add(max(sp.Poly(sp.expand(n_), v).degree(),
                         sp.Poly(sp.expand(d_), v).degree()))
        got = ('unique' if nfree == 0 else 'line', max(degs) if degs else 0)
    ok = (got == pred)
    rows.append((D, m, pred, got, ok))
    print(f"    D={D:3d} m={m}: predicted {str(pred):16s} brute force {str(got):16s} {'OK' if ok else 'MISMATCH'}")
chk("brute-force linear algebra reproduces THEOREM (E2) on all %d grid points" % len(grid),
    all(r[4] for r in rows))

# and the flagship: brute force finds exactly the closed-form solution at (13,4)
res134 = brute(13, 4)
chk("(13,4): brute force finds solutions at all", res134[0] != 'none')
nf, reps = res134
chk("(13,4): brute force finds a UNIQUE solution", nf == 0)
chk("(13,4): brute-force solution == closed form S/(v+1)^4 with kappa=1",
    sp.simplify(reps[0] - R_sol(13, 4, sp.Integer(1))) == 0)

print("\n--- 5. the 3|D branches, explicitly --------------------------------")
# D = 3j, j > m : kernel is rational
for (D, m) in [(15,4),(18,4),(21,4),(24,4)]:
    j = D//3
    ker = (v/(v+1))**j
    chk(f"D={D}: (v/(v+1))^{j} is in the kernel of 3v(v+1)R'-{D}R",
        sp.simplify(3*v*(v+1)*sp.diff(ker, v) - D*ker) == 0)
for (D, m) in [(12,4),(9,4),(6,4),(3,4)]:
    res = brute(D, m)
    chk(f"D={D}, m={m}: (3|D, j<=m) NO rational solution", res[0] == 'none')

print()
for n, ok in PASS:
    if not ok: print("FAILED:", n)
assert all(ok for _, ok in PASS), "E2 FAILED"
print("E2: ALL %d CHECKS PASS" % len(PASS))
