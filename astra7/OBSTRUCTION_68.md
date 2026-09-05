# Complete obstruction for the (6,8) live system

This proof does not assume even trace of the quadratic approximate root.
It covers both rho=2/3 and rho=4/3, including all of the non-even-trace
component left by Astra 6. Coefficient degrees in c are unrestricted.

## Local form forced by the saved global system

Let K=C(c), let O be the rational functions regular at c=0, and normalize
nu(c)=1. The saved system is

    P=h^3 v^6+sum_(i<6)p_i v^i,
    Q=[P^(4/3)]_+ + k[P^(2/3)]_+ + l[P^(1/3)]_+,
    J_(v,c)(P,Q)=kappa != 0.

It forces nu(h)=1 and top mixed-weight part

    P_3=[h1*v*(cv-rho)]^3, h1=h'(0)!=0, rho in {2/3,4/3}.

As proved in Astra 6, the quadratic root

    R=[P^(1/3)]_+=h v^2+s v+t0

has coefficients in O and s(0)=-rho*h1 != 0. This also follows directly
from s=p5/(3h^2), t0=p4/(3h^2)-p5^2/(9h^5): the top cube cancels the
only possible simple pole in t0. Write

    P=R^3+S, S=S3 v^3+S2 v^2+S1 v+S0.

The coefficients of S are regular at zero. Its maximum mixed weight is
at most 2, because the weight-3 part was cancelled by R^3. Hence S3 is
divisible by c in O.
For rational coefficient functions the weight in this statement is
max_i(i-nu(coefficient of v^i)); it agrees with the polynomial mixed
weight and does not assume absence of poles away from zero.

Pass to L=K(sqrt(h)), whose valuations lie in (1/2)Z, and set

    x=sqrt(h)*(v+s/(2h)), a=t0-s^2/(4h), T=x^2+a.

In these coordinates write

    P=T^3+b x^3+d x^2+e x+f.

The involution of L fixes a,d,f and negates b,e. Coefficient conversion
gives the exact initial bounds

    nu(a)=-1, nu(b)>=-1/2, nu(d)>=-1,
    nu(e)>=-3/2, nu(f)>=-2.                              (1)

For example b=S3/h^(3/2), d=S2/h-3s*S3/(2h^2), and the remaining bounds
follow from the same cubic translation. The equality nu(a)=-1 uses
s(0)!=0 and is valid for both rho values. The Jacobian in these coordinates
is kappa/sqrt(h), independent of x.
The finite polynomial-part formula transports exactly under this affine
change over L, as explained in `OBSTRUCTION_410.md`.

Use the invertible parameter change

    t=d+3k/2, u=e-a b, w=f-a d+3l/4.                    (2)

Now a,t,w are invariant and b,u anti-invariant. The parameter l becomes
an additive constant in P and disappears from the residual identities.
The initial bounds are

    nu(a)=-1, nu(b)>=-1/2, nu(t)>=-1,
    nu(u)>=-3/2, nu(w)>=-2.                              (3)

An anti-invariant nonzero function has half-integral, nonintegral order;
an invariant function has integer order. The order of zero is infinity.
This is the coefficient-field involution of sqrt(h), not the collision
involution of r. It imposes no even-trace assumption on R.

## Four algebraic first integrals and the last row

Define

    F4=b^3-9b w-9t u,

    C=-12a b u+3k b^2-4b^2 t+12t w+6u^2,

    F2=-2a b^3+6b^2 u-9k b t+6b t^2-18u w,

    D=b^4+27k a b^2-36a b^2 t+54a u^2-18b^2 w
      -54k b u+18b t u-27k t^2+12t^3-54w^2.

Let J_i=[x^i]J_(x,c). Direct, unconstrained polynomial expansion gives

    J4 = (8/27) F4',
    J3 = -(2/9) C',
    J2 = (4/27) F2'+(8/27)a F4'-(4/27)a' F4,
    J1 = (2/81) D'-(8/81)b' F4-(2/9)a C',

    J0 = (4/9){ b(a b u)'+u(b u)'-b t w'+u t t' }
         -(2/27)a' F2-(4/27)a a' F4.                   (4)

All coefficients of x^i for i>=5 vanish identically. Since J4=J3=0,
F4 is constant and C is constant. The constant field of L is C (the
minimal-polynomial argument is given in `OBSTRUCTION_410.md`). F4 is
anti-invariant, so F4=0. Then J2=0 gives F2 constant, and anti-invariance
gives F2=0. Finally J1=0 gives D constant. Thus the five differential
equations reduce to

    F4=F2=0, C,D in C,
    kappa=(4/9)sqrt(h){b(a b u)'+u(b u)'-b t w'+u t t'}.  (5)

No division by b,u,t,w or by a parameter was used. In particular every
identically-zero or singular component is retained. The script verifies
all five identities (4) before imposing any equation.

## Valuation obstruction theorem

**Theorem.** The exact bounds (3) and algebraic equations in (5) force

    nu(b)>=1/2, nu(u)>=1/2, nu(t)>=0, nu(w)>=0.           (6)

With these bounds the last equation of (5) cannot have kappa nonzero.

Proof, first improvement. If nu(u)=-3/2, the equation F2=0 forces
nu(w)>=-1: otherwise -18uw is the unique term of order -7/2, whereas
all other terms have order at least -5/2. But then in D the term
54a u^2 has order -4, and every other term has order at least -3.
That contradicts constancy of D. Therefore nu(u)>=-1/2. If nu(w)=-2,
the term -54w^2 is now the unique order -4 term of D, again impossible.
Thus nu(w)>=-1.

Leading-coefficient elimination. Put

    A=h a, B=sqrt(h)b, U=sqrt(h)u, T1=h t, W=h w.

All five functions are regular at zero, and A(0)!=0. Multiply F2=0
by h^(5/2), and D=constant by h^3, then evaluate at zero. Writing the
residue values with subscripts 0, one obtains

    2B0(3T1_0^2-A0 B0^2)=0,
    12T1_0(T1_0^2-3A0 B0^2)=0.                         (7)

The exact resultant in T1_0 of these two polynomials is

    -73728 A0^3 B0^9.

As A0 is nonzero, B0=0; the second equation then gives T1_0=0.
Equivalently, if B0 were nonzero the equations would require both
T1_0^2=A0 B0^2/3 and T1_0^2=3A0 B0^2. Consequently
nu(b)>=1/2 and nu(t)>=0.

Second improvement. If still nu(u)=-1/2, all terms of F2 except -18uw
have order at least 1/2, so nu(w)>=1. In D the term 54a u^2 then has
order -2 while every other term has nonnegative order, impossible.
Thus nu(u)>=1/2. If nu(w)=-1, -54w^2 is now the unique negative-order
term of D. It follows that nu(w)>=0, establishing (6).

Jacobian contradiction. The functions

    B=sqrt(h)b, U=sqrt(h)u

are rational and vanish at zero. The functions abu, bu, t, w are rational
and regular there: for abu, its order is at least -1+1/2+1/2=0.
Therefore the final equation of (5) reads

    kappa=(4/9){B(abu)'+U(bu)'-B t w'+U t t'},          (8)

whose right side vanishes at zero. This contradicts kappa != 0. QED.
Equation (8) is an identity in K with regular right side, so its evaluation
is legitimate even though the auxiliary coordinate change is singular
at c=0.

The theorem eliminates the **entire (6,8) system**, including both leading
alternatives and every non-even-trace root left by Astra 6. It is not an
assertion about arbitrary coordinate degrees. Its crucial inputs are the
four specific first integrals and their exact pole-order bounds.

`verify_68_obstruction.py` emits the finite normalized P,Q, all five row
identities, both scaled residue equations, their resultant, and the last
Jacobian factorization in `certificate_68.json`. The local valuation proof
above is the arbitrary-coefficient argument behind that certificate.
