# Global degree collapse and its boundary

All degrees here are degrees in v; coefficients range over all of C[c].
J denotes J_(v,c). Constants multiplying a Jacobian may be any nonzero
complex number when classifying normalized pairs.

## External input and collision-specific input

We use the Newton-polygon homothety theorem quoted as Theorem 2.1 in
[Gwozdziewicz, Injectivity on one line](https://arxiv.org/pdf/alg-geom/9305008),
and that paper's Theorem 1.1: a polynomial Keller map injective on a source
line is an automorphism. Polygons include the origin. The homothety ratio
is also the ratio of the v-degrees, since the maximum v coordinate is a
support functional. These are the only external theorems used below.

**Leading-coefficient lemma.** If P in B has positive v-degree m, then
c divides its leading coefficient. Indeed on D its leading coefficient
at c=0 would contribute a nonzero term r^(-2m+1) to the odd trace.
Every other contribution has exponent at least -2m+2. Even trace therefore
forces that coefficient to vanish.

**Coprime-degree obstruction.** If P,Q in B have coprime positive
v-degrees m,n, they cannot be Keller. Let i,j be the degrees of their
restrictions to c=0, with constants assigned degree zero. Homothety gives
i/m=j/n. By the lemma i<m,j<n. Coprimality forces i=j=0, so both functions
are constant on the line and the Jacobian vanishes there. If either total
degree is at most one, the affine-component case is already an automorphism
and cannot preserve the prescribed collision. This handles that exception
to the homothety theorem's hypotheses.

**Divisibility reduction.** If n=km, the highest coefficient equation is
m A E'-n A'E=0. Thus E=lambda A^k, with constant lambda. Replacing
Q by Q-lambda P^k strictly lowers its v-degree, preserves B, and preserves
the Jacobian. This is a finite polynomial target shear.

**Components of v-degree at most two.** These force automorphisms. For
a quadratic or linear component with nonconstant leading coefficient,
specialize at a zero of that coefficient: its restriction is linear or
constant. In the latter case the Jacobian makes the other restriction
affine with nonzero slope. The line theorem applies. With constant
quadratic leading coefficient, a polynomial translation in v gives
A v^2+D(c); absence of critical points forces D' to be a nonzero constant,
so the component is a coordinate. The linear and v-independent cases are
immediate. Such maps cannot belong to B in both components.

## The noncoprime (4,6) case

The top coefficient equation permits normalization

    P=h^2 v^4+B3 v^3+C2 v^2+D1 v+E0,
    [v^6]Q=h^3,
    J(P,Q)=kappa != 0.                         (5)

Here h is a polynomial. We first prove that (5) is impossible whenever
h is not a square in C(c), without assuming collision membership.

Put W=P^(1/4) in the Laurent field at v=infinity, choosing its leading
coefficient sqrt(h). Cancelling descending coefficients of the Jacobian
shows that

    Q=[W^6]_+ + sum_(j=0)^5 k_j [W^j]_+,

with constant k_j. This is an exact polynomial-part identity; a negative
Laurent tail contributes to the Jacobian only in v-degree at most two.
Galois conjugation sqrt(h)->-sqrt(h) forces k_5=k_3=k_1=0. Remove k_4 P
and k_0, and write k=k_2.

The v^4 and v^3 coefficients of Q include respectively

    3 B3^2/(8h)+3 C2 h/2,
    -B3^3/(16h^3)+3 B3 C2/(4h)+3 D1 h/2.

At a zero of h of order q, the first forces ord(B3)>=ceil(q/2).
If ord(B3)<q, the first term in the second expression is a unique pole.
Thus h divides B3. Write

    s=B3/(2h), t=(C2-s^2)/(2h),
    T=h v^2+s v+t, P=T^2+u v+w.

Here s is polynomial, whereas t,u,w are initially only rational in c.
Set x=sqrt(h)(v+s/(2h)), and write

    P=x^4+a x^2+b1 x+d,
    z=d-a^2/4+2k/3.

The top two remaining Jacobian equations are the derivatives of

    -3 b1 z,                3 a b1^2/4-3 z^2/2.

Both must be constant. The first is Galois anti-invariant, hence zero.
If b1=0 the remaining equations give Jacobian zero. Otherwise z=0 and
a b1^2=beta is constant. The final Jacobian coefficient is

    J_(x,c)(P,Q)=3 b1^2 b1'/4.

With b1=u/sqrt(h), define e=3u^2/(8h). Then

    u e'=kappa,     h=3 kappa^2/(8 e e'^2).       (6)

This rational identity is the global termination obstruction. Since h is
polynomial, e has no finite zero. Thus e=E/f for a nonconstant polynomial f,
and f'^2 divides f^5. Every zero of f' is a zero of f. Counting the zeros
of f' not accounted for by the distinct roots of f shows f has only one
distinct root. With z0=c-c0, therefore

    e=E z0^-m,
    u=U z0^(m+1),       U=-kappa/(m E),
    h=H0 z0^(3m+2),     H0=3 kappa^2/(8m^2 E^3),
    m>=1.                                                (7)

The earlier constant beta gives

    tau=beta h/(2u^2),  t=s^2/(4h)+tau,
    P=T^2+u(v+s/(2h))-2k/3,
    Q=T^3+(3/2)u T(v+s/(2h))+e.                   (8)

Tau is polynomial and vanishes to order m. If t is regular at z0=0,
regularity of the constant coefficient of P forces u s/(2h) regular.
Then the constant coefficient of Q has the uncancelled pole e.

If t has a pole, let l=ord(s). Cancellation in P's constant coefficient
requires

    l=(4m+3)/3,    ord(t)=-m/3.

If this is not an integer, it is already impossible. Otherwise, denoting
leading constants by s0,t0,w0, polynomiality of P gives

    s0^3=-8H0 U,  w0=-t0^2,  t0^3=U^2/H0=8E/3.

The pole coefficient in Q is t0^3+(3/2)t0 w0+E=-E/3, nonzero.
This proves the nonsquare case in all coefficient degrees. Notice that
allowing rational t was essential; assuming t polynomial would leave a gap.

If h=f^2 is a square, use W with leading coefficient f. All k_j are now
allowed. Polynomiality of the v^3 coefficient of Q still forces
f^2 divides B3: for ord(f)=q and ord(B3)<2q the term
-B3^3/(16f^6) is a unique pole, including in comparison with
k_5(5B3^2/(32f^3)+5C2 f/4). The collision lemma gives f(0)=0.
Even trace of P is exactly

    27c^3 D1+36c^2 C2+(36c+27c^2)B3+(32+72c)h^2=0.

Since ord_0(h^2)>=4 and ord_0(B3)>=2, this forces C2(0)=0.
Thus P restricts to degree at most one on c=0, and the line theorem
excludes a pair in B. This completes the (4,6) obstruction.

## Degree theorem and the first remaining range

**Theorem.** No polynomial potential satisfying the exact criterion has
v-degree at most 13. This is an arbitrary-c-degree theorem, not a bounded
coefficient search.

Proof. Its reconstructed pair has m+n=deg_v H. Apply the degree-at-most-two
case, the coprime obstruction, and divisibility reduction. Among positive
pairs with sum at most 13, the only noncoprime pair, neither dividing the
other, that remains is (4,6) or its transpose. It was proved impossible
above. Every reduction decreases the sum. QED.

The next sum is 14. Its two new pairs are (4,10) and (6,8), up to exchange.
This is the first degree range not excluded by these arguments; existence
of a solution is **not** asserted. The component attacked further in this
strike is (6,8); the (4,10) equations are separately retained in
`EXCEPTIONAL_410.md`. The proof is specific to the v filtration.
No analogous c-degree bound is claimed here without a separate argument
for the asymmetric collision algebra.

The low-degree collapse does not prove that every degree collapses. In
particular the pole calculation for (4,6) cannot be reused unchanged for
(6,8): there are five remaining coefficient equations, not three, and
the rational approximate root need not lie in B.
