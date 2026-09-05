# Complete obstruction for the (4,10) live system

Work in K=C(c), with derivative denoted by a prime. Let O be its local
ring at c=0 and let nu(c)=1. All orders used below are exact discrete
valuations, not truncated equations or numerical approximations.

## Inputs from the already reduced system

Astra 6 reduces every collision Keller pair in this range, up to constant
rescalings and target shears, to

    P=h^2 v^4+p3 v^3+p2 v^2+p1 v+p0,
    Q=[P^(5/2)]_+ + k[P^(3/2)]_+ + l[P^(1/2)]_+,
    J_(v,c)(P,Q)=kappa != 0.

Here h has a simple zero at c=0, and the top mixed-weight part of P is
the square of h1*v*(cv-rho), with h1=h'(0)!=0 and
rho in {2/3,4/3}. No other leading branch is omitted.

The quadratic polynomial part of the square root is

    R=[P^(1/2)]_+=h v^2+s v+t,
    s=p3/(2h), t=p2/(2h)-p3^2/(8h^3).

Its coefficients are in O. The weight bound makes s regular and gives t
at most a simple pole. The displayed top square cancels the coefficient
of that pole. Also s(0)=-rho*h1 is nonzero. Thus

    P=R^2+u v+w,                         u,w in O.          (1)

No claim that R is polynomial globally, or has even collision trace,
is required.

## Exact elimination of the three rows

In the quadratic extension L=K(sqrt(h)), introduce

    x=sqrt(h)*(v+s/(2h)),
    a=t-s^2/(4h), beta=u/sqrt(h), z=w-u*s/(2h).

This is a rational change used only to compute identities. Its Jacobian
is sqrt(h); it is not asserted to be a global polynomial automorphism.
Set T=x^2+a, L0=beta*x+z. Then

    P=T^2+L0,
    Q=T^5+(5/2)T^3 L0+(15/8)T L0^2
      +(5/16)(beta^3*x+3beta^2*z)
      +k(T^3+(3/2)T L0+3beta^2/8)+lT.                    (2)

Equation (2) is exactly the finite polynomial-part expression above.
Polynomial parts commute with this affine change over L: a negative
power of v has only negative powers of x after substitution, so no tail
term can change the displayed polynomial. The chain rule gives
J_(v,c)=sqrt(h)*J_(x,c), including the c-dependent translation.
The remaining x^2 and x coefficients of the Jacobian are I2' and I1',
where

    I2=beta*(5a beta^2-12kz-8l-15z^2)/4,

    I1=(48a beta^2 k+120a beta^2 z+5beta^4
        -48kz^2-64lz-40z^3)/32.

Consequently I2,I1 are constants. The constant field of L is C: if an
algebraic function has zero derivative, differentiate its monic minimal
polynomial over C(c); minimality forces all its coefficients to be
constant, and C is algebraically closed. The involution sqrt(h)->-sqrt(h)
fixes a,z and changes the sign of beta. Thus I2 is an anti-invariant
constant and must be zero.

If beta is identically zero, the constant Jacobian row is already zero.
Otherwise

    5a beta^2=15z^2+12kz+8l.                              (3)

Put

    y=beta^2=u^2/h, Z=z+2k/5,
    A=128l/5-192k^2/25.

Substituting (3) into I1 gives, for some constant B,

    y^2+64Z^3+A Z=B.                                     (4)

The constant Jacobian row, using (3), is

    J_(x,c)=beta^2*(5beta*z'+(6k+15z)*beta')/8.

Multiplying by sqrt(h), the original nonzero constant must therefore obey

    kappa = u*(10y Z'+15Z y')/16.                        (5)

Equations (4),(5) eliminate a and the redundant shifts of k,l from the
obstruction. They cover every value of A,B, including all singular cubic
degeneracies; no discriminant or unknown function has been divided out
apart from the separately handled beta=0 case.

## Local valuation theorem

**Theorem.** Suppose h has a simple zero, u,w,s are regular at that zero,
z=w-us/(2h), and y=u^2/h. Then (4),(5) cannot hold with kappa nonzero.

Proof. Both y and Z have poles of order at most one. If Z had a pole,
64Z^3 would have order -3, whereas y^2 has order at least -2 and AZ,B
have orders at least -1,0. That unique pole cannot cancel in (4).
Thus Z is regular. Equation (4) then makes y regular. Since
nu(y)=2nu(u)-1 and u is regular, u must vanish at c=0. Derivatives of
regular rational functions are regular, so the right side of (5)
vanishes at c=0. This contradicts kappa != 0. QED.
The evaluation is of an identity of regular rational functions in K;
it does not evaluate the singular auxiliary coordinate x at c=0.

This proves impossibility of the **entire (4,10) system**, with arbitrary
coefficient degrees and either collision leading branch. The proof is
local at one forced zero of h, so possible poles of the auxiliary root
elsewhere cannot evade it.

The exact identities, the original polynomial-part formula, the cubic
elimination, and the Jacobian factor are independently expanded by
`verify_410_obstruction.py`; its output is `certificate_410.json`.
