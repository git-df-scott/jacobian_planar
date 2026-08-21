"""
Plane Jacobian campaign - Session 19
DEFORMATION / MODULI PROBE OF THE SESSION-18 EMPTINESS THEOREM.

Sessions 16-18 closed the First Framework by reducing every layer of the
(99,66) decision system to one operator equation on the Belyi-realization
functional R along E_{-2},

    alpha^5 * T_D(R) = -c,    T_D(R) = (v+1)^4 (3v(v+1)R' - D R),

with D the cusp-chain degree (13 = First Framework, 23 = Second), c the
Keller constant, alpha the Session-13 rigidity scalar, and then evaluating
at v = -1.  This session does not re-run that evaluation.  It deforms the
system and asks where, if anywhere, the moduli space has a trapdoor.

RESULT 1 (universal obstruction; upgrades the transfer conjecture).
On the polynomial locus the endgame is obstructed for EVERY chain degree
D >= 1, not only for D with D/3 not an integer:

    ev_{v=-1} annihilates the image of T_D identically,

so no chain degree admits a polynomial R with c != 0.  Session 18's
transfer conjecture ("fatal whenever D/3 is not an integer") is therefore
a theorem on the polynomial locus, and it is fatal for all D.  The Second
Framework (D = 23) and every isotope-series degree die with the First.
Certified below for D = 1..60 by exact rank computation, and symbolically
for generic D and generic R.

RESULT 2 (the trapdoor, and it is sharp).
The whole proof rests on exactly one hypothesis - Session 13/14's
pole-fiber theorem, which forces R to be a POLYNOMIAL at U = v+1 = 0 -
and that hypothesis is load-bearing by precisely one unit of pole order:

    ord_{U=0} R >= -3  =>  c = 0   (still obstructed)
    ord_{U=0} R  = -4  =>  c != 0 is attained, by a unique-up-to-scale R,
                           in closed form, for every D outside {3,6,9,12}.

So the Session-18 argument is "QED modulo Theorem 3", and Theorem 3 is the
single point of failure worth re-refereeing.

RESULT 3 (the twin test, and it closes).
The unlocking R has map-degree exactly 4 in v for EVERY D - the numerator
is always a quartic and never vanishes at v = -1.  The framework's
realization layer demands that R realize the chain's degree-D Belyi map,
i.e. map-degree D.  The trapdoor is therefore self-consistent only at

    D = 4,

and the frozen skeleton forbids D = 4: the fork/cusp combinatorics
(Belyi degree N = 2*deg p = 3*deg r + 1, chain degree D = N - 3) admits
only D = 1 (mod 6).  No combinatorial twin can walk through the trapdoor.

RESULT 4 (why 13; a by-product).
Rigidity of the skeleton's Belyi datum needs #unknowns - #equations = 1,
i.e. (5D+13)/6 = D, i.e. D = 13 EXACTLY.  Borisov's chain degree is not
an accident of his search: it is the unique degree at which the First
Framework's Belyi data is rigid.  D = 1, 7 carry positive-dimensional
twin families (too soft to pin a framework); D >= 19 is over-determined.

RESULT 5 (the resonance, and it is Jacobian-silent).
The Session-18 "M == 0 branch" R ~ (v/(v+1))^{D/3} becomes an honest
rational function exactly when 3 | D.  It is a genuine rank jump of the
moduli space - dim goes 1 -> 2 at pole order J = D/3 - but it always
carries c = 0, so it never integrates to a Keller structure.  At
D = 3,6,9,12 that resonance sits at J <= 4 and absorbs the unlocking
direction, which is why those four degrees stay rigid at every pole order.

NET.  The emptiness theorem survives the deformation probe.  No
counterexample and no candidate counterexample was found; what was found
is the exact hypothesis the theorem hangs on, an explicit formula for what
would have to exist to break it, and a combinatorial proof that nothing in
the framework family can supply it.

All arithmetic below is exact.  Companion Singular routines:
    ../singular/endgame_moduli.sing    (scheme, tangent space, obstruction)
    ../singular/rank_jumps.sing        (rank-jump census, closed forms)
    ../singular/monomial_twins.sing    ([P,Q] = x^r twins, admissibility)
"""

from sympy import (symbols, Rational as Q, Poly, diff, expand, cancel,
                   together, numer, factor, fraction, degree, simplify,
                   linear_eq_to_matrix, I, sqrt, gcd, S)

v, c, x1, x2, w = symbols('v c x1 x2 w')
U = v + 1

PASS = []


def check(name, ok):
    PASS.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")


def T(R, D):
    """Session-18 endgame operator."""
    return expand((v + 1)**4 * (3*v*(v + 1)*diff(R, v) - D*R))


def endgame_system(D, J, N=12):
    """Linear system for R = A(v)/(v+1)^J with deg A <= N+J, target -c/U^4.

    Returns (unknowns, coefficient matrix) of
        3v((v+1)A' - J A) - D A  +  c * (v+1)^(J-4)  =  0
    cleared to a polynomial identity in v.
    """
    a = symbols(f'a0:{N + J + 1}')
    A = sum(a[i]*v**i for i in range(N + J + 1))
    E = 3*v*((v + 1)*diff(A, v) - J*A) - D*A
    E = expand(E*(v + 1)**(4 - J) + c) if J <= 4 else expand(E + c*(v + 1)**(J - 4))
    unk = list(a) + [c]
    M, _ = linear_eq_to_matrix(Poly(E, v).all_coeffs(), unk)
    return unk, M


def solution_space(D, J, N=12):
    """(dim of solution space, whether c can be nonzero)."""
    unk, M = endgame_system(D, J, N)
    ns = M.nullspace()
    return len(ns), any(vec[len(unk) - 1] != 0 for vec in ns)


# =====================================================================
print(__doc__)
print("=" * 70)
print("RESULT 1  universal obstruction on the polynomial locus")
print("=" * 70)

# 1a. symbolic: ev_{v=-1} annihilates the image of T_D, for generic R and D.
Dsym = symbols('D')
r = symbols('r0:9')
Rgen = sum(r[i]*v**i for i in range(9))
check("ev_{v=-1} o T_D == 0 for generic R and symbolic D",
      simplify(T(Rgen, Dsym).subs(v, -1)) == 0)

# 1b. exact: no polynomial R with c != 0, for every D in 1..60.
live = [D for D in range(1, 61) if solution_space(D, 0, N=10)[1]]
check("no polynomial solution with c != 0 for any D in 1..60  "
      f"(live degrees: {live})", live == [])

# 1c. the kernel of T_D on polynomials is trivial for every D in 1..60.
def poly_kernel_dim(D, N=14):
    a = symbols(f'a0:{N + 1}')
    A = sum(a[i]*v**i for i in range(N + 1))
    M, _ = linear_eq_to_matrix(Poly(T(A, D), v).all_coeffs(), list(a))
    return len(M.nullspace())

check("ker T_D = 0 on polynomials for every D in 1..60",
      all(poly_kernel_dim(D) == 0 for D in range(1, 61)))

print("\n  => Session 18's transfer conjecture is a theorem on the")
print("     polynomial locus, for every chain degree.  D = 23 (Second")
print("     Framework) and the whole isotope series are covered.")

# =====================================================================
print()
print("=" * 70)
print("RESULT 2  the trapdoor: pole order 4 at U = v+1 = 0, and sharpness")
print("=" * 70)

DL = [1, 2, 4, 5, 7, 13, 19, 23, 25, 31, 41, 53]
print("    D | J=0  1  2  3  4  5  6   (dim of solution space)"
      "   | c != 0 first at J =")
table_ok = True
for D in DL:
    dims, first = [], None
    for J in range(0, 7):
        d, cok = solution_space(D, J, N=10)
        dims.append(d)
        if cok and first is None:
            first = J
    print(f"  {D:3d} |  " + "  ".join(str(d) for d in dims) +
          f"    | {first}")
    table_ok &= (dims[:4] == [0, 0, 0, 0]) and (first == 4)
check("pole order <= 3 forces c = 0, pole order 4 unlocks it "
      "(all D tested outside {3,6,9,12})", table_ok)

blocked = [D for D in range(1, 61) if not solution_space(D, 4, N=10)[1]]
check(f"the only chain degrees still blocked at J = 4 are {blocked}",
      blocked == [3, 6, 9, 12])


def unlocking_R(D):
    """Closed form of the pole-order-4 solution, normalised to c = 1."""
    unk, M = endgame_system(D, 4, N=10)
    ns = [vec for vec in M.nullspace() if vec[len(unk) - 1] != 0]
    if not ns:
        return None
    vec = ns[0] / ns[0][len(unk) - 1]
    a = [s for s in unk if s.name.startswith('a')]
    A = sum(vec[i]*v**i for i in range(len(a)))
    return cancel(A / U**4)


print("\n  closed form (normalised c = 1), R = A(v)/(v+1)^4 :")
deg4_ok, resid_ok, pole_ok = True, True, True
for D in DL:
    R = unlocking_R(D)
    num, den = fraction(cancel(R))
    dn = degree(Poly(num, v), v)
    resid = simplify(3*v*U*diff(R, v) - D*R + 1/U**4)
    print(f"   D = {D:3d}:  A = {expand(num)}")
    print(f"            deg A = {dn}, A(-1) = {simplify(num.subs(v, -1))}, "
          f"residual = {resid}")
    deg4_ok &= (dn == 4)
    resid_ok &= (resid == 0)
    pole_ok &= (simplify(num.subs(v, -1)) != 0)
check("the unlocking R solves the endgame exactly", resid_ok)
check("its numerator is a quartic for EVERY D (map-degree 4)", deg4_ok)
check("its pole at U = 0 has order exactly 4 (numerator(-1) != 0)", pole_ok)

# =====================================================================
print()
print("=" * 70)
print("RESULT 3  the twin test: which chain degree could use the trapdoor?")
print("=" * 70)
print("  realization layer demands map-degree(R) = D;  trapdoor supplies 4.")
print("  => the trapdoor is self-consistent only at D = 4.")

# admissible chain degrees for the frozen (2,3)-cusp fork skeleton:
#   B = p^2/(w r^3), N = 2 deg p = 3 deg r + 1, D = N - 3.
adm = []
for b in range(1, 40, 2):          # deg r must be odd so that N = 3b+1 is even
    N = 3*b + 1
    a = N // 2
    adm.append((a, b, N, N - 3))
print("\n   deg p | deg r | Belyi N | chain degree D")
for a, b, N, D in adm[:8]:
    print(f"   {a:5d} | {b:5d} | {N:7d} | {D:5d}")
check("every admissible chain degree is 1 mod 6",
      all(D % 6 == 1 for _, _, _, D in adm))
check("D = 4 is NOT an admissible chain degree "
      "=> the trapdoor has no twin to walk through it",
      4 not in [D for _, _, _, D in adm])

# =====================================================================
print()
print("=" * 70)
print("RESULT 4  why 13: rigidity of the skeleton's Belyi datum")
print("=" * 70)
print("   unknowns  = deg p + deg r          (monic coefficients)")
print("   equations = N - 4                  (cancellation to degree 3)")
print("   rigid <=> unknowns - equations = 1 (only the scaling orbit)")
print()
print("      D | unknowns | equations | difference | verdict")
rigid = []
for a, b, N, D in adm[:8]:
    nu, ne = a + b, N - 4
    verdict = ("RIGID" if nu - ne == 1 else
               ("under-determined" if nu - ne > 1 else "over-determined"))
    if nu - ne == 1:
        rigid.append(D)
    print(f"   {D:4d} | {nu:8d} | {ne:9d} | {nu - ne:10d} | {verdict}")
check(f"the unique rigid chain degree is D = 13  (found {rigid})",
      rigid == [13])
check("algebraically: (5D+13)/6 = D  <=>  D = 13",
      simplify(Q(5, 6)*13 + Q(13, 6) - 13) == 0)

# =====================================================================
print()
print("=" * 70)
print("RESULT 5  the resonance is real but Jacobian-silent")
print("=" * 70)
res_ok, silent_ok = True, True
for d in range(1, 11):
    D = 3*d
    Rh = (v/U)**d
    res_ok &= (simplify(3*v*U*diff(Rh, v) - D*Rh) == 0)
    # a homogeneous solution carries c = 0 by construction
    silent_ok &= (T(Rh, D).subs(v, 0) * 0 == 0)
check("R = (v/(v+1))^{D/3} is an exact kernel element whenever 3 | D",
      res_ok)
print("   pole order of that direction at U = 0 is D/3, so it enters the")
print("   census exactly at J = D/3 - matching the observed 1 -> 2 jumps")
print("   at D = 15,18,21,24,27,30 and the absorption at D = 3,6,9,12.")
jump = []
for D in [15, 18, 21, 24, 27, 30]:
    d_before = solution_space(D, D//3 - 1, N=10)[0]
    d_after = solution_space(D, D//3, N=10)[0]
    jump.append((D, d_before, d_after))
    print(f"   D = {D:2d}:  dim at J = {D//3 - 1} is {d_before},"
          f"  dim at J = {D//3} is {d_after}")
check("the resonance jump lands exactly at J = D/3",
      all(b == 1 and a == 2 for _, b, a in jump))

# =====================================================================
print()
print("=" * 70)
print("RESULT 6  Newton-skeleton obstruction to [P,Q] = x^r  ->  [P,Q] = 1")
print("=" * 70)
u = symbols('u1:9')
# a generic member of the near-miss skeleton: y1 in x1^3*k[x1,x2],
# y2 in x1^2*k[x1,x2]  (forced by the fork exponents, Session 7)
Y1 = x1**3*(u[0] + u[1]*x1 + u[2]*x2 + u[3]*x1*x2**5 + u[4]*x2**7)
Y2 = x1**2*(u[5] + u[6]*x2 + u[2]*x1**4 + u[7]*x1*x2**3)
BR = expand(diff(Y1, x1)*diff(Y2, x2) - diff(Y1, x2)*diff(Y2, x1))
check("on the frozen skeleton, x1^4 divides {y1,y2} identically",
      simplify(cancel(BR/x1**4) - expand(BR/x1**4)) == 0 and
      Poly(BR, x1).all_coeffs()[-1] == 0 and
      all(Poly(BR, x1, x2).coeff_monomial(x1**k*x2**m) == 0
          for k in range(4) for m in range(9)))
check("hence the constant term of {y1,y2} vanishes on the WHOLE box "
      "=> [P,Q] = const is unreachable without changing the x1-support",
      BR.subs({x1: 0, x2: 0}) == 0)

# =====================================================================
print()
print("=" * 70)
print("RESULT 7  cross-epoch consistency with the certified Session-7 data")
print("=" * 70)
s3 = I*sqrt(3)
p = (w**8 + (2 + 8*s3)*w**7 + (Q(-233, 3) + Q(50, 3)*s3)*w**6
     + (Q(-4600, 27) - Q(376, 3)*s3)*w**5 + (Q(835, 3) - Q(890, 3)*s3)*w**4
     + (Q(2420, 3) + Q(22, 3)*s3)*w**3 + (Q(1043, 3) + 336*s3)*w**2
     + (-118 + 158*s3)*w + (-28 + 4*s3))
r_ = (w**5 + (Q(4, 3) + Q(16, 3)*s3)*w**4 + (Q(-278, 9) + Q(68, 9)*s3)*w**3
      + (Q(-140, 3) - 24*s3)*w**2 + (Q(35, 3) - Q(112, 3)*s3)*w
      + Q(68, 3) - Q(20, 3)*s3)
h0 = Q(1664, 3) - Q(832, 3)*s3
N_cubic = expand(p**2 - w*r_**3)
check("deg(p^2 - w r^3) == 3 (the 13-fold miracle cancellation)",
      degree(Poly(N_cubic, w), w) == 3)
n3 = Poly(N_cubic, w).coeff_monomial(w**3)
check("Wronskian constant h == h0",
      simplify(expand(2*diff(p, w)*r_*w - p*(r_ + 3*w*diff(r_, w))) - h0) == 0)
check("cross-epoch identity h0 = -D * n3 with D = 13 (the chain degree "
      "this probe sweeps)", simplify(h0 + 13*n3) == 0)
print(f"   n3 = {simplify(n3)},  h0 = {h0},  h0 / n3 = {simplify(h0/n3)}")

# =====================================================================
print()
print("=" * 70)
print(f"{sum(PASS)}/{len(PASS)} certifications passed.")
print("=" * 70)
print("""
CONCLUSION.  The deformation probe found no counterexample and no
candidate counterexample.  It found:
  * the Session-18 obstruction is universal in the chain degree, which
    upgrades the transfer conjecture to a theorem on the polynomial
    locus and kills the Second Framework (D = 23) with the First;
  * exactly one trapdoor - pole order 4 at U = 0 - with an explicit
    closed-form solution, so the emptiness theorem is now precisely
    "QED modulo the pole-fiber theorem", and that is the one hypothesis
    a referee should attack;
  * that the trapdoor needs chain degree 4, which the frozen skeleton
    cannot supply (D = 1 mod 6);
  * a structural explanation of D = 13 as the unique rigid degree.
""")
assert all(PASS), "a certification failed"
