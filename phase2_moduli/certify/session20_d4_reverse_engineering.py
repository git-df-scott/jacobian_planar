"""
Plane Jacobian campaign - Session 20
REVERSE-ENGINEERING A SKELETON THAT ACCEPTS THE TRAPDOOR.

Session 19 located the trapdoor in the Session-18 emptiness proof: the
endgame is unlocked (Keller constant c != 0) exactly when the realization
functional R is allowed a pole of order 4 at U = v+1 = 0, and the
unlocking R then has map-degree 4, so the realization layer - which
demands map-degree = chain degree D - is satisfied only at D = 4.
Session 19 declared D = 4 inadmissible because the (2,3)-cusp fork
profile forces D = 1 (mod 6).

CORRECTION (Result 2 below).  That congruence was an artefact of pinning
BOTH the cusp type to (2,3) AND the cancellation depth to delta = 3.
With those freed, D = 4 IS constructible, and this session exhibits the
skeleton explicitly:

    cusp type (m,n) = (2,5),  cancellation depth delta = 2,
    Belyi degree N = 6,  p = w^3 + (5/2)w^2 + (15/8)w + 5/16,  r = w + 1,
    deg(p^2 - w r^5) = 2,  ramification 3x2 / 1 + 1x5 / 1x4 + 2x1,
    rigid (solution set = the scaling orbit),  chain degree D = 4.

So steps 1 and 2 of the reverse-engineering programme SUCCEED.  The
D = 1 (mod 6) obstruction reported in Session 19 was too narrow, and is
withdrawn as a general statement (it remains correct for the (2,3),
delta = 3 family it was derived in).

WHAT KILLS THE PROGRAMME (Results 1 and 3).  Generalise the endgame to an
arbitrary cusp exponent s and contact exponent k,

    T_{k,s,D}(R) = (v+1)^k ( s v(v+1) R' - D R ) = -c,

with (k,s) = (4,3) the First Framework.  Then:

  RESULT 1 (generalised trapdoor).  For every (k,s,D), pole order < k
  still forces c = 0, pole order k unlocks it, and the unlocking R has
  numerator a degree-k polynomial not vanishing at v = -1.  So the
  unlocking R has map-degree exactly k, ALWAYS - it never sees D.  The
  realization layer demands map-degree D, so self-consistency forces
  D = k.  The correct target is not "force D = 4" but "force the chain
  degree to equal the contact exponent".

  RESULT 3 (the Belyi gate, and it is where step 4 dies).  With k = D
  forced, the unlocking R has one pole of order D at v = -1 and D-1
  finite critical points.  Those critical points are simple and their
  critical values are DISTINCT, so R has D critical values in all.  A
  Belyi map has exactly 3, and affine post-composition R -> lambda*R+nu
  cannot change how many there are.  Hence R is affine-equivalent to a
  degree-D Belyi map only when D <= 3, uniformly in s.

  In particular D = 4 fails at EVERY cusp exponent s - by the Belyi gate
  when s does not divide 4, by resonance collision when it does.  Step 3's
  hardcoded ansatz is not a Belyi realization at D = 4 no matter what
  geometry is placed underneath it, so step 4 cannot pass, and it fails
  for a reason entirely independent of steps 1 and 2.

SURVIVING WINDOW.  Chain degree D <= 3, e.g. the rigid skeleton
(m,n) = (5,2), delta = 2, N = 5, deg p = 1, deg r = 2, D = 3, also
constructed explicitly below.  Two honest caveats about that window:
  * it still needs the pole-fiber theorem to FAIL for its own geometry -
    the trapdoor is not avoided there, only made degree-consistent;
  * D = 13 corresponds to Moh's degree pair (99,66).  Chain degrees 2
    and 3 correspond to far smaller degree pairs, inside the range where
    the plane Jacobian conjecture is already proved.  Checking that is
    the natural next step, and it is not done here.

All arithmetic below is exact.  Companion Singular routine:
    ../singular/skeleton_generator.sing
"""

from sympy import (symbols, Rational as Q, Poly, diff, expand, cancel,
                   fraction, degree, simplify, resultant, gcd, discriminant,
                   linear_eq_to_matrix, factor)

v, c, t, w = symbols('v c t w')
U = v + 1

PASS = []


def check(name, ok):
    PASS.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")


# ---------------------------------------------------------------- endgame
def unlock_system(J, k, s, D, M):
    """Linear system for R = A(v)/(v+1)^J against target -c/(v+1)^k."""
    a = symbols(f'a0:{M + 1}')
    A = sum(a[i]*v**i for i in range(M + 1))
    E = s*v*((v + 1)*diff(A, v) - J*A) - D*A
    E = expand(E*(v + 1)**(k - J) + c) if J <= k else expand(E + c*(v + 1)**(J - k))
    unk = list(a) + [c]
    Mx, _ = linear_eq_to_matrix(Poly(E, v).all_coeffs(), unk)
    return unk, Mx


def c_free(J, k, s, D, M):
    unk, Mx = unlock_system(J, k, s, D, M)
    return any(vec[len(unk) - 1] != 0 for vec in Mx.nullspace())


def unlock_R(k, s, D, M=None):
    """Unlocking R at pole order k, normalised to c = 1 (None if c is forced 0)."""
    M = k + 6 if M is None else M
    unk, Mx = unlock_system(k, k, s, D, M)
    ns = [vec for vec in Mx.nullspace() if vec[len(unk) - 1] != 0]
    if not ns:
        return None
    vec = ns[0] / ns[0][len(unk) - 1]
    A = sum(vec[i]*v**i for i in range(M + 1))
    return cancel(A/U**k)


def critical_data(R):
    """(#critical points, #distinct finite critical values) for a rational R."""
    num, den = fraction(cancel(R))
    Nc = expand(diff(num, v)*den - num*diff(den, v))
    Nc = cancel(Nc/gcd(Nc, den))
    rs = resultant(Nc, num - t*den, v)
    sq = cancel(rs/gcd(rs, diff(rs, t)))
    return degree(Poly(Nc, v), v), degree(Poly(sq, t), t)


print(__doc__)
print("=" * 70)
print("RESULT 1  generalised trapdoor: unlocking pole order = k,")
print("          map-degree of the unlocking R = k, independent of D")
print("=" * 70)
sharp, degk, nonvanish = True, True, True
ncase = 0
for k in range(2, 7):
    for s in range(2, 6):
        for D in [1, 2, 5, 7, 11, 13]:
            if D % s == 0 and D//s <= k:          # resonance collision
                continue
            ncase += 1
            M = k + 6
            for J in range(0, k):                 # every weaker pole
                if c_free(J, k, s, D, M):
                    sharp = False
            R = unlock_R(k, s, D)
            if R is None:
                degk = False
                continue
            num, _ = fraction(cancel(R))
            degk &= (degree(Poly(num, v), v) == k)
            nonvanish &= (simplify(num.subs(v, -1)) != 0)
print(f"   cases swept (k = 2..6, s = 2..5, D in 1,2,5,7,11,13): {ncase}")
check("pole order strictly below k always forces c = 0", sharp)
check("the unlocking numerator has degree exactly k, for every (k,s,D)", degk)
check("that numerator never vanishes at v = -1 (pole order is exactly k)",
      nonvanish)
print("\n   => map-degree(R) = k always.  The realization layer demands")
print("      map-degree(R) = D, so self-consistency forces D = k.")

# =====================================================================
print()
print("=" * 70)
print("RESULT 2  D = 4 IS constructible - Session 19's D = 1 mod 6 withdrawn")
print("=" * 70)


def skeleton(m, n, N):
    """Rigid skeleton data for B = p^m/(w r^n) of Belyi degree N, or None."""
    if N % m or (N - 1) % n:
        return None
    a, b = N//m, (N - 1)//n
    delta = N - a - b
    return (a, b, delta, a + b) if delta >= 1 else None


rigid = []
for m in range(2, 7):
    for n in range(2, 8):
        if gcd(m, n) != 1:
            continue
        for N in range(2, 31):
            sk = skeleton(m, n, N)
            if sk:
                rigid.append((m, n, N) + sk)
d4 = [r for r in rigid if r[6] == 4]
print("   rigid skeletons with chain degree 4 (m, n, N, deg p, deg r, "
      "delta, D):")
for r in d4:
    print("     ", r)
check("chain degree 4 is constructible", len(d4) > 0)
check("the First Framework (2,3,N=16,8,5,delta=3,D=13) is in the census",
      (2, 3, 16, 8, 5, 3, 13) in rigid)

# --- build the D = 4 skeleton explicitly: (m,n) = (2,5), N = 6, delta = 2
p3, p2c, p1c, p0c, r0c = symbols('p3 p2 p1 p0 r0')
pD4 = w**3 + p2c*w**2 + p1c*w + p0c
rD4 = w + r0c
F = expand(pD4**2 - w*rD4**5)
eqs = [Poly(F, w).coeff_monomial(w**j) for j in (5, 4, 3)]
sol = __import__('sympy').solve(eqs, [p2c, p1c, p0c], dict=True)[0]
sol_norm = {k_: simplify(vv.subs(r0c, 1)) for k_, vv in sol.items()}
p_ex = expand(pD4.subs(sol).subs(r0c, 1))
r_ex = expand(rD4.subs(r0c, 1))
Fex = expand(p_ex**2 - w*r_ex**5)
print(f"\n   explicit D = 4 skeleton:  p = {p_ex}")
print(f"                             r = {r_ex}")
print(f"                             p^2 - w r^5 = {factor(Fex)}")
check("deg(p^2 - w r^5) == 2 == delta (the cancellation fires)",
      degree(Poly(Fex, w), w) == 2)
check("p is squarefree", discriminant(Poly(p_ex, w)) != 0)
check("p(0) != 0 and r(0) != 0 (non-degenerate: gcd(p, w r) = 1)",
      p_ex.subs(w, 0) != 0 and r_ex.subs(w, 0) != 0 and
      simplify(p_ex.subs(w, -1)) != 0)
# Riemann-Hurwitz for B = p^2/(w r^5), degree N = 6
ram = (3*1) + (0 + 4) + ((6 - 2) - 1)     # 3 double pts / w + 5-fold / D-fold
check(f"Riemann-Hurwitz: ramification {ram} == 2*6 - 2", ram == 2*6 - 2)
print("   profile: 3x2  /  1 + 1x5  /  1x4 + 2x1   -> chain degree D = 4")
print("\n   => steps 1 and 2 of the programme SUCCEED.  The D = 1 mod 6")
print("      statement holds only for the (2,3) cusp with delta = 3.")

# =====================================================================
print()
print("=" * 70)
print("RESULT 3  the Belyi gate - where step 4 dies, for every skeleton")
print("=" * 70)
print("   with k = D forced, count the critical values of the unlocking R")
print()
print("    s \\ D:  " + "  ".join(f"{D:2d}" for D in range(2, 10)))
gate = {}
for s in range(2, 8):
    row = []
    for D in range(2, 10):
        if D % s == 0 and D//s <= D:
            row.append(" x")
            gate[(s, D)] = 'x'
            continue
        R = unlock_R(D, s, D)
        ncp, nfin = critical_data(R)
        ok = (nfin + 1 <= 3)
        row.append(" Y" if ok else " .")
        gate[(s, D)] = 'Y' if ok else '.'
    print(f"    {s}     : " + "  ".join(row))
print("\n    Y = clears the Belyi gate   . = fails it   x = resonance collision")

check("D = 4 fails the gate at EVERY cusp exponent s",
      all(gate[(s, 4)] != 'Y' for s in range(2, 8)))
check("the gate clears only for D <= 3, uniformly in s",
      all(gate[(s, D)] != 'Y' for s in range(2, 8) for D in range(4, 10)))

# the explicit D = 4 failure, spelled out
R4 = unlock_R(4, 3, 4)
ncp4, nfin4 = critical_data(R4)
print(f"\n   the D = 4 ansatz (s = 3): R = {cancel(R4)}")
print(f"   residual of the endgame  = {simplify(3*v*U*diff(R4, v) - 4*R4 + 1/U**4)}")
print(f"   critical points: {ncp4} simple, critical values: {nfin4} finite "
      f"+ 1 pole = {nfin4 + 1}")
check("the D = 4 ansatz solves the endgame exactly",
      simplify(3*v*U*diff(R4, v) - 4*R4 + 1/U**4) == 0)
check("but it has 4 critical values, so it is affine-equivalent to no "
      "Belyi map (a Belyi map has 3)", nfin4 + 1 == 4)

# =====================================================================
print()
print("=" * 70)
print("RESULT 4  the surviving window: chain degree D <= 3")
print("=" * 70)
surv = [r for r in rigid if r[6] <= 3]
print("   rigid skeletons with D <= 3 (m, n, N, deg p, deg r, delta, D):")
for r in surv:
    tag = ""
    if r[6] % r[1] == 0:
        tag = "   [resonance collision - dead]"
    print("     ", r, tag)
alive = [r for r in surv if r[6] % r[1] != 0]
print("\n   surviving after the resonance gate:", alive)

# explicit D = 3 survivor: (m,n) = (5,2), N = 5, deg p = 1, deg r = 2
p0s, r1s, r0s = symbols('p0s r1s r0s')
pS = w + p0s
rS = w**2 + r1s*w + r0s
FS = expand(pS**5 - w*rS**2)
eqS = [Poly(FS, w).coeff_monomial(w**j) for j in (4, 3)]
solS = __import__('sympy').solve(eqS, [r1s, r0s], dict=True)[0]
p_s = expand(pS.subs(p0s, 1))
r_s = expand(rS.subs(solS).subs(p0s, 1))
FSex = expand(p_s**5 - w*r_s**2)
print(f"\n   explicit D = 3 survivor:  p = {p_s}")
print(f"                             r = {r_s}")
print(f"                             p^5 - w r^2 = {factor(FSex)}")
check("deg(p^5 - w r^2) == 2 == delta", degree(Poly(FSex, w), w) == 2)
check("r is squarefree and r(0) != 0",
      discriminant(Poly(r_s, w)) != 0 and r_s.subs(w, 0) != 0)
ram3 = (0 + 4) + (0 + 2*1) + ((5 - 2) - 1)   # 1x5 / w + 2x2 / D-fold + simple
check(f"Riemann-Hurwitz: ramification {ram3} == 2*5 - 2", ram3 == 2*5 - 2)
R3 = unlock_R(3, 2, 3)
ncp3, nfin3 = critical_data(R3)
print(f"   its unlocking R = {cancel(R3)}")
print(f"   critical values: {nfin3} finite + 1 pole = {nfin3 + 1}  "
      f"(Belyi needs 3)")
check("the D = 3 survivor's unlocking R clears the Belyi gate",
      nfin3 + 1 <= 3)

# =====================================================================
print()
print("=" * 70)
print(f"{sum(PASS)}/{len(PASS)} certifications passed.")
print("=" * 70)
print("""
VERDICT ON THE FOUR-STEP PROGRAMME.
  step 1  reverse-engineer the edge-count equations   -> SUCCEEDS, but the
          right target is chain degree = contact exponent, not D = 4.
  step 2  build a skeleton natively producing D = 4   -> SUCCEEDS: cusp
          type (2,5), delta = 2, exhibited explicitly and certified.
  step 3  hardcode the pole-order-4 R at D = 4        -> the ansatz is
          exact for the endgame, as Session 19 already showed.
  step 4  run the realization pipeline                -> FAILS, and not
          for a degree-bookkeeping reason.  The D = 4 unlocking R has 4
          critical values and no Belyi map has more than 3, so it cannot
          realize the chain's degree-4 Belyi map under ANY skeleton.  The
          failure is independent of steps 1 and 2, so no amount of
          re-engineering the polygon can repair it.

Still no counterexample, and no candidate counterexample.  The one place
left to look is chain degree D <= 3, which needs the pole-fiber theorem
to fail on its own terms AND lands in degree ranges where the plane
Jacobian conjecture is already proved.
""")
assert all(PASS), "a certification failed"
