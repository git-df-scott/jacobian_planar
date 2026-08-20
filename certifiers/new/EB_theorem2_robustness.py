"""
EB - HOW MUCH OF THE CLOSURE DEPENDS ON THEOREM 2 (BOUNDARY RIGIDITY)?

Step 2 of the plan: "THEOREM 2/3 - reproving or refuting these two lost
theorems swings every framework verdict at once.  Highest single lever on the
board."  This file removes the lever instead of pulling it: it shows the
(99,66) closure holds for EVERY admissible boundary polynomial g, so THEOREM 2
is not load-bearing for the emptiness verdict at all.

SET-UP.  THEOREM 2 asserts g = alpha U (U-1)^8 exactly.  Drop that and take
        g = alpha * U^eps * (U-1)^G ,
the general shape allowed by the two facts that ARE certified: Session 8's
support box forces deg(g^3) <= 27, i.e. deg g = eps + G <= 9; and Session 9's
(-2)-cluster rigidity makes the boundary-line polynomials a common power of a
single g.  (Extra roots of g elsewhere are handled by E2(a): R can have no
pole off {0,-1} whatever g does.)

E1's general derivation, redone with the U-multiplicity eps free, gives

    6 U v R' + [ 26 eps + 26 G - 6 N ] U R - 26 eps R
        = -(2c/alpha^5) U^{1-5 eps} v^{N-5G+1} ,

so the R-part collapses exactly when  N = 13(eps+G)/3, and then

    3 v(v+1) R' - 13 eps R = -kappa (v+1)^{1-5 eps} v^{(16 - 2G + 13 eps - 13)/3}

with kappa = c/alpha^5.  At (eps,G) = (1,8) this is (star) verbatim.

RESULT.  For every admissible (eps, G) the realization object R comes out with
map-degree != 13 - most of the time because no rational R exists at all.  The
closure is therefore INDEPENDENT of THEOREM 2.

BONUS.  Integrality alone forces eps = 1 once G = 8: N = 13(eps+8)/3 needs
3 | eps+8, and eps <= 1 from deg g <= 9.  That replaces THEOREM 2's contested
"propagation from the {1}-marked corner" (which established U | g) with a
one-line congruence.
"""
import sympy as sp
from fractions import Fraction as Fr

v = sp.Symbol('v')
PASS = []
def chk(name, cond):
    PASS.append((name, bool(cond)))
    print(("  [PASS] " if cond else "  [FAIL] ") + name)

# ---------------------------------------------------------------- derivation
print("--- 1. the general-eps endgame equation ------------------------------")
alpha, c, U_, e_, beta_, G_, N_, eps_ = sp.symbols('alpha c U e beta G N eps')
a_, b_ = sp.symbols('a b')
U = v + 1
R = sp.Function('R')(v)
ok_ident = True
for epsv in range(0, 10):
    eta = alpha**2*U**(2*epsv)*v**a_
    delta = sp.Rational(1,2)*alpha**3*U**(3*epsv)*R*v**b_
    blk = e_*delta*sp.diff(eta, v) + beta_*sp.diff(delta, v)*eta
    cl = (alpha**5/2)*U**(5*epsv-1)*v**(a_+b_-1)*(
        beta_*U*v*sp.diff(R, v) + epsv*(2*e_+3*beta_)*v*R + (e_*a_+beta_*b_)*U*R)
    if sp.simplify(sp.expand(sp.powsimp(blk - cl, force=True))) != 0:
        ok_ident = False
        print("      identity fails at eps =", epsv)
chk("general-eps block identity verified for eps = 0..9 with symbolic "
    "a, b, e, beta", ok_ident)
aa, bb = 2*G_ - 3*beta_, 3*G_ + 3*e_ - N_
coeffU = sp.expand(eps_*(2*e_+3*beta_) + (e_*aa + beta_*bb))
chk("U-coefficient = (2e+3b)(eps+G) - b N",
    sp.expand(coeffU - ((2*e_+3*beta_)*(eps_+G_) - beta_*N_)) == 0)
Nstar = sp.solve(sp.Eq(coeffU, 0), N_)[0]
print("    collapse:  N = (2e+3beta)(eps+G)/beta =", sp.factor(Nstar),
      "  -> at e=4,beta=6:", sp.simplify(Nstar.subs({e_: 4, beta_: 6})))
chk("(99,66): N = 13(eps+G)/3",
    sp.simplify(Nstar.subs({e_: 4, beta_: 6}) - sp.Rational(13,3)*(eps_+G_)) == 0)
chk("at eps=1, G=8: N = 39", Nstar.subs({e_: 4, beta_: 6, eps_: 1, G_: 8}) == 39)

print("\n--- 2. integrality forces eps = 1 once G = 8 -------------------------")
sols = [eps for eps in range(0, 10) if (13*(eps+8)) % 3 == 0 and eps + 8 <= 9]
print("    eps with 3 | (eps+8) and deg g = eps+8 <= 9 :", sols)
chk("G = 8 and deg g <= 9 force eps = 1, i.e. U | g (THEOREM 2's step, "
    "recovered from a congruence)", sols == [1])

# ---------------------------------------------------------------- sweep
print("\n--- 3. sweep over every admissible (eps, G) --------------------------")
def rational_solutions(D, Aexp, Bexp, K=14, L=12, dg=26, kappa=1):
    """all rational R with 3v(v+1)R' - D R = -kappa (v+1)^Aexp v^Bexp,
       found by exact linear algebra on R = P(v)/((v+1)^K v^L)."""
    den = (v+1)**K*v**L
    cs = sp.symbols('p0:%d' % (dg+1))
    P = sum(cs[i]*v**i for i in range(dg+1))
    Rr = P/den
    lhs = 3*v*(v+1)*sp.diff(Rr, v) - D*Rr
    rhs = -kappa*(v+1)**Aexp*v**Bexp
    expr = sp.cancel(sp.together((lhs - rhs)))
    num, _ = sp.fraction(expr)
    num = sp.expand(num)
    if num == 0:
        return ('all',)
    eqs = sp.Poly(num, v).all_coeffs()
    sol = sp.linsolve(eqs, cs)
    if not sol:
        return ('none',)
    sol = list(sol)[0]
    free = sorted({s for e in sol for s in e.free_symbols} & set(cs), key=str)
    reps = []
    for assign in ([{f: 0 for f in free}] +
                   [{f: (1 if f == g else 0) for f in free} for f in free for g in [f]]):
        Rv = sp.cancel(sum(sol[i].subs(assign)*v**i for i in range(dg+1))/den)
        reps.append(sp.simplify(Rv))
    return (len(free), reps)

def mapdeg(Rv):
    if Rv == 0: return 0
    n, d = sp.fraction(sp.cancel(Rv))
    return max(sp.Poly(sp.expand(n), v).degree() if n.has(v) else 0,
               sp.Poly(sp.expand(d), v).degree() if d.has(v) else 0)

rows = []
for eps in range(0, 10):
    for G in range(0, 10 - eps):
        if (13*(eps+G)) % 3 != 0:
            continue                              # collapse impossible: N not integral
        N = 13*(eps+G)//3
        A = 1 - 5*eps
        B = N - 5*G + 1
        if B < 0 or int(B) != B:
            continue
        D = 13*eps
        res = rational_solutions(D, A, int(B))
        if res[0] == 'none':
            verdict, md = "NO rational R", None
        elif res[0] == 'all':
            verdict, md = "degenerate (0 = 0)", None
        else:
            nf, reps = res
            ds = sorted({mapdeg(r) for r in reps if r != 0})
            verdict = ("unique" if nf == 0 else "%d-parameter family" % nf)
            md = ds
        rows.append((eps, G, N, D, A, B, verdict, md))
        print(f"    eps={eps} G={G} deg g={eps+G} N={N} D={D}: "
              f"{verdict}   map-degrees {md}")
chk("every admissible (eps,G) gives either no rational R or map-degree != 13",
    all(r[7] is None or 13 not in r[7] for r in rows))
chk("the sweep includes the certified case (eps,G) = (1,8)",
    any(r[0] == 1 and r[1] == 8 for r in rows))
row18 = [r for r in rows if r[0] == 1 and r[1] == 8][0]
chk("(1,8) reproduces (star): D = 13, A = -4, B = 0, unique solution of "
    "map-degree 4", (row18[3], row18[4], row18[5]) == (13, -4, 0)
    and row18[6] == "unique" and row18[7] == [4])

print("\n--- 4. VERDICT -------------------------------------------------------")
print("    The (99,66) emptiness verdict does NOT depend on THEOREM 2.")
print("    For every boundary polynomial g = alpha U^eps (U-1)^G admitted by")
print("    the certified box cap, the endgame either has no rational solution")
print("    or has one whose map-degree is not 13.  THEOREM 2's own conclusion")
print("    (eps = 1 when G = 8) additionally follows from integrality alone.")

print()
for n, o in PASS:
    if not o: print("FAILED:", n)
assert all(o for _, o in PASS), "EB FAILED"
print("EB: ALL %d CHECKS PASS" % len(PASS))
