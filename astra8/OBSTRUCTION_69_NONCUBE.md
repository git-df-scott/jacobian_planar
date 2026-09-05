# The (6,9) obstruction when the leading factor is not a cube

All coefficient degrees are unrestricted. Work over K=C(c), in characteristic
zero. This is a written proof with exact symbolic certificates, not a proof
assistant formalization or an externally reviewed theorem.

**Theorem.** There are no P,Q in C[c,v] satisfying

    deg_v P=6, deg_v Q=9,
    lc_v P=h^2, lc_v Q=h^3, J_(v,c)(P,Q)=kappa != 0,

when h in C[c] is not a cube in K. Collision membership is not needed.

## Complete normalization

The highest Jacobian coefficient gives the displayed common leading factor,
after constant rescaling. Put q^3=h, L=K(q), and choose W=P^(1/6) with leading
term qv. The descending Jacobian equations give

    Q=[W^9]_+ + sum_(j=0)^8 k_j[W^j]_+,

where the k_j are constants. For completeness, at each descending step the
leading Jacobian equation says that the coefficient divided by the relevant
power of the leading coefficient of W has derivative zero. The constant field
of the finite algebraic function field L is C. Negative Laurent powers cannot
contribute to the Jacobian above degree 4, so this cancellation reaches all
nonnegative powers. A final degree-zero remainder is constant for the same
reason. This is a finite exact polynomial-part identity at v=infinity.

Because h is not a cube, L/K has a nontrivial order-three automorphism. It
takes W to zeta W, with zeta a primitive cube root of unity. Distinct polynomial
parts [W^j]_+ have distinct degrees. Q is fixed, so k_j=0 unless 3 divides j.
Remove k_6 P+k_0 by a target shear. The complete form is

    Q=[P^(3/2)]_+ + k[P^(1/2)]_+.                 (1)

Let R=[P^(1/2)]_+=hv^3+s v^2+t v+r0. Its coefficients need only be rational.
Then S=P-R^2 has v-degree at most two. The auxiliary affine change

    x=q(v+s/(3h))

gives, with five initially rational-over-L coefficient functions,

    R=x^3+a x+b, S=u x^2+w x+z,
    P=R^2+S,
    Q=R^3+(3/2)RS+(3/8)(u^2 x+2uw)+kR.          (2)

The polynomial part commutes with an affine change over L: a strictly
negative Laurent tail stays strictly negative after such a change. Formula
(2) follows from [S^2/R]_+=u^2x+2uw; further terms have negative degree.
The Galois characters of a,b,u,w,z are respectively 2,0,1,2,0 modulo three.
The transformed Jacobian is kappa/q, independent of x.

## Four first integrals, with no discarded zero branch

Put Z=z+2k/3 and define

    G4=-a u^2+2uZ+w^2,
    G3=-2auw-bu^2+2wZ,
    C=u^3+12buw-6Z^2.

With primes denoting differentiation in c at fixed x and J_i the x^i row,
unconstrained expansion gives

    J4=-(9/4)G4',
    J3=-(9/4)G3',
    J2=-(3/4)aG4'+(3/2)a'G4+(3/8)C',
    J1=-(3/4)aG3'+(3/4)a'G3+(3/2)b'G4+(9/8)(u^2w)' .   (3)

All higher rows vanish identically. G4 and G3 have nontrivial characters,
so J4=J3=0 implies G4=G3=0, rather than arbitrary nonzero constants.
Next C is constant. Finally u^2w is constant and has nontrivial character,
so u^2w=0.

If u=0, G4=0 implies w=0. Direct calculation gives

    J_(x,c)=-(3/2)ZZ' R_x,

which cannot be a nonzero constant in x. Hence u is nonzero. It follows
that w=0, then b=0 and Z=au/2. Write W0=au=2Z, an element of K. Thus

    u^3=C+(3/2)W0^2,
    J_(x,c)=-(3/32)(2C+7W0^2)W0'/u.               (4)

Let U=q^2u, also in K. Changing the Jacobian back to v gives

    U^3=h^2(C+(3/2)W0^2),
    kappa=-3h(2C+7W0^2)W0'/(32U).

W0' is nonzero. Cubing and eliminating U gives the exact rational identity

    h=-32768*kappa^3*(C+(3/2)W0^2)
        /(27*(2C+7W0^2)^3*(W0')^3).             (5)

## Global pole obstruction

If C is nonzero, choose the two distinct numbers alpha,-alpha with
alpha^2=-2C/7. At a finite preimage of either under the nonconstant rational
function W0, the numerator in (5) is nonzero and the denominator vanishes.
This would be a pole of h. A nonconstant rational map P^1 -> P^1 is
surjective, and only one value can have all its preimages at infinity.
It cannot avoid both alpha and -alpha on the affine c-line. Therefore C=0.

Now (5) reads

    h=-16384*kappa^3/(3087*W0^4*(W0')^3).        (6)

W0 cannot have a finite zero of order n>=1: the denominator would have
positive order 7n-3. Hence W0=E/f with E nonzero and f a nonconstant
polynomial. Equation (6) makes h a nonzero constant times f^10/(f')^3.
Every root of f' must be a root of f. If f has degree d and r distinct
roots, only d-r of the d-1 roots of f', counted with multiplicities, occur
at these roots. Thus r=1. With t0=c-c0 and m>=1,

    W0=E*t0^(-m), h=H0*t0^(7m+3).

The equation for U shows U has order 4m+2. Define A=q a=hW0/U in K.
It has order 2m+1 and satisfies

    U=(3/2)A^2, W0=(3/2)A^3/h.

In fact U,A are monomials, since their cubes are monomials. For
y=v+eta, eta=s/(3h) rational, the original pair becomes exactly

    P=h^2 y^6+2hA y^4+(5/2)A^2 y^2+(3/4)A^3/h-2k/3,
    Q=h^3 y^9+3h^2A y^7+(21/4)hA^2 y^5
      +(35/8)A^3 y^3+(63/32)A^4 y/h.            (7)

No regularity of eta was assumed. In P's constant coefficient, the last
nonconstant term A^3/h has order -m. If eta has less of a pole than

    ord(eta)=-(5m+2)/2,                          (8)

that term is the unique lowest term. If eta has more of a pole, h^2 eta^6
is the unique lowest term. Thus (8) is necessary. Odd m is already
impossible because eta is rational.

At (8), Y0, the leading value of h eta^2/A, is finite and nonzero. All
four terms of P's constant coefficient have order -m; their cancellation
requires

    F(Y0)=0, F(Y)=Y^3+2Y^2+(5/2)Y+3/4.

All five terms of Q's constant coefficient have order -3m/2; their
cancellation requires

    G(Y0)=0, G(Y)=Y^4+3Y^3+(21/4)Y^2+(35/8)Y+63/32.

But the exact resultant is

    Res_Y(F,G)=567/32768 != 0.

The certificate also supplies explicit Bezout multipliers whose combination
with F,G is 1. This contradiction completes every branch of the theorem.

This result is about coordinate degrees (6,9). The rational-value argument
is degree independent in W0, but deriving equation (5) used the four
specific identities (3) and the nontrivial Galois action. It is not an
arbitrary-coordinate-degree obstruction for the collision algebra.
