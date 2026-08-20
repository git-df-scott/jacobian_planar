"""
w3_second_framework_verdict.py  -  ADJUDICATING THE SECOND FRAMEWORK.

The night's sharpest contradiction:

  WAVE2_FINDINGS (errors branch)  : Second Framework D = 23 -- OPEN
  WAVE3_FINDINGS (errors branch)  : superseded, D = 23 -- DEAD for every k != 23
  az3geq STATUS 2.2               : D = deg((-2)-curve Belyi map), 23 for the
                                    Second Framework -- "structural"
  my earlier PR #8 / E6           : D = 15 - 12/beta < 15, so D = 23 is
                                    "unreachable"

The last two cannot both be right, and this file settles which claim is doing
the work.  It also corrects my own.

FINDING 1 -- the two D's are different objects that coincide at (99,66).
  chain degree      D_chain = 2*gamma - sigma      (number of vanishing blocks)
  ODE coefficient   D_ode   = 3(2e + 3beta)/beta,  e = gamma - sigma
  With the cusp-(2,3) relation gamma = 3 beta/2 these are
      D_ode = 18 - 6 sigma/beta      and      D_chain = 3 beta - sigma,
  which are equal IDENTICALLY IN sigma at beta = 6 and at no other beta.
  (99,66) has beta = 6.  So the agreement at 13 is a coincidence of that one
  framework, and neither report may transport its own D to another framework
  without re-deriving it.

FINDING 2 -- my "D < 15, so D = 23 is unreachable" was overstated.
  D_ode = 15 + 6(1-p)/beta needs the Keller chart exponent p, which is
  (99,66)-specific (p = 3).  The bound D <= 15 holds only for p >= 1, which is
  not proved anywhere in the record.  The claim is withdrawn as stated.

FINDING 3 -- what actually kills both frameworks, and it needs no D at all.
  The exponent k on (v+1) is not free: the deviation block carries g^3 and the
  y2 block carries g^2, so with eps := ord_{U=0}(g) the Keller block carries
  U^{5 eps - 1}, i.e.
        k = 5 eps - 1   (eps >= 1),      k = 0   (eps = 0).
  So k is always 0 or == 4 (mod 5).  The realization demands map-degree D_chain,
  the endgame delivers map-degree k, and
        13 mod 5 = 3,   23 mod 5 = 3,
  so k can never equal 13 or 23, for ANY eps.  Both frameworks die, and the
  argument uses neither beta, nor p, nor the Belyi data, nor THEOREM 3.

FINDING 4 -- the one escape neither report closed.
  If 3 | D_ode and D_ode/3 > k, the solution set is a LINE whose generic member
  has map-degree D_ode/3.  That member matches the realization demand exactly
  when D_ode = 3 D_chain.  Nobody checked this.  At (99,66) it is closed
  (D_ode = 13, not 39).  For the Second Framework it is OPEN unless its D_ode
  is computed.  So the honest label there is DEAD-CONDITIONAL, not DEAD.
"""
import sympy as sp

RES = []
def rec(n, ok):
    RES.append((n, bool(ok))); return bool(ok)

beta, sigma, e, p, eps, G, N = sp.symbols('beta sigma e p eps G N', positive=True)
v, U, alpha = sp.symbols('v U alpha')

print("--- 1. D_ode and D_chain are different functions --------------------")
gam = sp.Rational(3, 2)*beta                      # cusp (2,3): gamma = 3 beta / 2
D_ode = sp.simplify(3*(2*(gam - sigma) + 3*beta)/beta)
D_chain = sp.simplify(2*gam - sigma)
print("    D_ode   =", sp.simplify(D_ode))
print("    D_chain =", sp.simplify(D_chain))
diff = sp.simplify(sp.expand(D_ode - D_chain))
print("    D_ode - D_chain =", sp.factor(diff))
rec("D_ode = 18 - 6 sigma/beta", sp.simplify(D_ode - (18 - 6*sigma/beta)) == 0)
rec("D_chain = 3 beta - sigma", sp.simplify(D_chain - (3*beta - sigma)) == 0)
rec("they agree identically in sigma exactly when beta = 6",
    sp.simplify(diff.subs(beta, 6)) == 0
    and all(sp.simplify(diff.subs(beta, b)) != 0 for b in (2, 3, 4, 5, 7, 8, 12)))
rec("(99,66) has beta = 6, gamma = 9, sigma = 5, and both give 13",
    D_ode.subs({beta: 6, sigma: 5}) == 13 and D_chain.subs({beta: 6, sigma: 5}) == 13)
print("    => the coincidence at 13 is a property of beta = 6, not of the cusp.")

print("\n--- 2. my D < 15 claim, re-examined ---------------------------------")
D_p = sp.simplify(3*(2*(beta + 1 - p) + 3*beta)/beta)
rec("D_ode = 15 + 6(1-p)/beta once e = beta + 1 - p is used",
    sp.simplify(D_p - (15 + 6*(1 - p)/beta)) == 0)
rec("D <= 15 requires p >= 1; at p = 3, beta = 6 it gives 13",
    D_p.subs({p: 3, beta: 6}) == 13)
rec("for p = 0 the same formula gives D > 15, so the bound is NOT "
    "cusp-intrinsic", sp.simplify(D_p.subs({p: 0, beta: 6})) > 15)
print("    D(p=0, beta=6) =", sp.simplify(D_p.subs({p: 0, beta: 6})),
      " -> the bound rests on p >= 1, which the record does not prove.")
print("    VERDICT: 'D < 15 hence D = 23 unreachable' is WITHDRAWN as stated.")

print("\n--- 3. k = 5 eps - 1, and 13, 23 are both unreachable ---------------")
# re-derive the U-power of the Keller block with eps free
R = sp.Function('R')(v)
a_, b_ = sp.symbols('a b')
Uu = v + 1
ok = True
for ev in range(0, 8):
    eta = alpha**2*Uu**(2*ev)*v**a_
    delta = sp.Rational(1, 2)*alpha**3*Uu**(3*ev)*R*v**b_
    blk = e*delta*sp.diff(eta, v) + beta*sp.diff(delta, v)*eta
    cl = (alpha**5/2)*Uu**(5*ev - 1)*v**(a_+b_-1)*(
        beta*Uu*v*sp.diff(R, v) + ev*(2*e + 3*beta)*v*R + (e*a_ + beta*b_)*Uu*R)
    if sp.simplify(sp.expand(sp.powsimp(blk - cl, force=True))) != 0:
        ok = False
rec("block == (alpha^5/2) U^{5 eps - 1} v^{a+b-1} [ ... ] for eps = 0..7", ok)
# the bracket's U-order: it contains a term with no U factor iff eps != 0
# computed, not asserted: the bracket at U = 0 (v = -1) must be nonzero for eps>=1
brk = beta*Uu*v*sp.diff(R, v) + eps*(2*e + 3*beta)*v*R + (e*a_ + beta*b_)*Uu*R
brk_at = sp.simplify(brk.subs(v, -1).doit())
rec("bracket|_{v=-1} = -eps(2e+3beta) R(-1): nonzero iff eps != 0, so the "
    "block's (v+1)-order is exactly 5 eps - 1 for eps >= 1",
    sp.simplify(brk_at + eps*(2*e + 3*beta)*R.subs(v, -1)) == 0
    and sp.simplify(brk_at.subs(eps, 0)) == 0)
ks = sorted({5*ev - 1 for ev in range(1, 12)} | {0})
print("    admissible k =", ks)
rec("every admissible k is 0 or == 4 (mod 5)",
    all(kk == 0 or kk % 5 == 4 for kk in ks))
rec("13 is not admissible (13 mod 5 = 3)", 13 % 5 == 3 and 13 not in ks)
rec("23 is not admissible (23 mod 5 = 3)", 23 % 5 == 3 and 23 not in ks)
print("    => realization needs map-degree D_chain = k; 13 and 23 are")
print("       unreachable for EVERY eps.  Both frameworks die on this alone.")

print("\n--- 4. the escape nobody closed: the 3|D family branch --------------")
# from the adjudication grid: 3|D and D/3 > k gives a line whose generic member
# has map-degree D/3.  That matches the realization iff D_ode = 3 D_chain.
def escape(D_ode_val, k_val, D_chain_val):
    if D_ode_val % 3 != 0:
        return ('unique', k_val, k_val == D_chain_val)
    j = D_ode_val // 3
    if j <= k_val:
        return ('none', None, False)
    return ('line', j, (j == D_chain_val) or (k_val == D_chain_val))
rows = [("First (99,66)", 13, 4, 13), ("First, hypothetical D=39", 39, 4, 13),
        ("Second, D_ode = 23", 23, 4, 23), ("Second, hypothetical D=69", 69, 4, 23)]
for nm, Do, kk, Dc in rows:
    st, dg, surv = escape(Do, kk, Dc)
    print(f"    {nm:28s} D_ode={Do:3d} k={kk} D_chain={Dc:3d} -> {st:6s} "
          f"degree {dg}  survives realization: {surv}")
rec("(99,66) at its actual D_ode = 13: dead (unique, degree 4 != 13)",
    escape(13, 4, 13) == ('unique', 4, False))
rec("but at the hypothetical D_ode = 3*13 = 39 the framework would SURVIVE "
    "the endgame", escape(39, 4, 13)[2] is True)
rec("so the verdict genuinely depends on D_ode, not only on k",
    escape(13, 4, 13)[2] != escape(39, 4, 13)[2])
rec("Second Framework at D_ode = 23: dead", escape(23, 4, 23)[2] is False)
rec("Second Framework at the hypothetical D_ode = 69: would survive",
    escape(69, 4, 23)[2] is True)

print("\n--- 5. VERDICT -------------------------------------------------------")
print("""    WAVE2 'OPEN'  vs  WAVE3 'DEAD': wave 3 is right in direction and its
    supersession is legitimate - but its label is stronger than its evidence.

    Second Framework status, stated exactly:
      DEAD, provided (i) its realization layer demands map-degree equal to its
      chain degree 23, and (ii) its ODE coefficient D_ode is not 69 = 3 x 23.
      (i) is the framework's own demand and is safe; (ii) is unchecked by every
      report on the record.  D_ode for that framework has never been computed.

    az3geq's 'D = deg((-2)-curve Belyi map), structural' is UNVERIFIED: it is
    true of D_chain by definition and false of D_ode away from beta = 6.

    my 'D < 15, so 23 is unreachable' is WITHDRAWN: correct at p = 3, but p = 3
    is chart-specific and the record does not prove p >= 1 in general.

    What survives with no conditions at all: k = 5 eps - 1, so k in {0,4,9,...},
    and 13, 23 are both == 3 (mod 5).  The unique-solution branch can never meet
    the realization demand for either framework.  Only the 3|D family branch
    could, and closing it needs one number - D_ode for the Second Framework.""")

print()
bad = [n for n, o in RES if not o]
for n in bad:
    print("FAILED:", n)
print("w3_second_framework_verdict: %d/%d checks pass" % (len(RES) - len(bad), len(RES)))
raise SystemExit(1 if bad else 0)
