# The exact remaining (6,9) system

**Status: OPEN.** This file is a complete necessary-and-sufficient reduction
of the degree-15 candidate range, after the noncube obstruction. It is not
an irreducibility certificate, a counterexample, or a reduction of all
coordinate degrees to degree 15.

## Normalizations that retain every candidate

Normalize lc_v(P)=h^2 and lc_v(Q)=h^3 by constant target scalings. The
noncube theorem forces h=f^3. The leading-coefficient invariant then forces
f=gamma*c^N with N>=2: collision parity forces a zero at c=0, and the
invariant permits only one zero. Target scalings normalize gamma=1.

Descending Jacobian cancellation at v=infinity gives

    Q=[P^(3/2)]_+ + sum_(j=0)^8 k_j[P^(j/6)]_+.

Remove k_6 P+k_0 by a target shear. There is now no nontrivial Galois
action on the leading sixth root f=c^N; the other k_j cannot be discarded
by the noncube argument. The target translation P_new=P+delta with
delta=2k_3/3 removes k_3 as well. It changes

    k_1 -> k_1-(7/6)delta*k_7,
    k_2 -> k_2-(4/3)delta*k_8,

and leaves the other surviving k_j unchanged. Polynomial parts of terms
with exponents reduced below zero vanish. The verifier checks this exact
translation before making the renaming. There remain six parameters,

    I={1,2,4,5,7,8},
    Q=[P^(3/2)]_+ + sum_(j in I) k_j[P^(j/6)]_+.      (1)

Depress and make P monic by the auxiliary rational coordinate

    x=c^N(v+eta(c)),
    R=x^3+a x+b,
    p(x,c)=R^2+u x^2+w x+z,
    q(x,c)=[p^(3/2)]_+ + sum_(j in I) k_j[p^(j/6)]_+.  (2)

The original coordinates are P(v,c)=p(c^N(v+eta),c) and similarly Q.
Here a,b,u,w,z,eta belong to C[c,c^(-1)]. This follows from the original
polynomial coefficients and the fact that the only normalization
denominators are powers of c. The source change is auxiliary: collision
membership is always imposed after reconstruction in the original v,c.

## Five algebraic equations replacing the differential system

For i=1,...,5 define the explicit polynomial in the five coefficients and
six constants

    mu_i=-(1/i)[x^(-1)](q_x*p^(i/6)).                (3)

Coefficient extraction here is finite: q_x has degree eight, so one needs
only the terms of p^(i/6) down to x^(-9). Full expanded expressions, all
finite polynomial parts, and their verification are in
`resonant_69_system.json`. Equation (3) defines them without an implicit
infinite solving process.

To prove the reduction, put W=p^(1/6)=x+O(x^(-1)). The coefficient of
W^(-i) in q(x(W)) is mu_i, by change of variable in the formal residue
and integration by parts. The exact Jacobian identity is

    J_(x,c)(p,q)=
      (6x^4+6ax^2+4bx+2a^2/3+u)*mu_1'
      +(6x^3+4ax+2b)*mu_2'
      +(6x^2+2a)*mu_3' +6x*mu_4' +6*mu_5'.       (4)

The script verifies (4) by unconstrained differentiation and expansion.
Thus J_(v,c)=kappa!=0 is equivalent to

    mu_1=C1, mu_2=C2, mu_3=C3, mu_4=C4,
    mu_5=C5+kappa*c^(1-N)/(6*(1-N)), N>=2,        (5)

with constant C1,...,C5. The last integration is exact. In particular it
is not legitimate to set C1,C2,C4 to zero by Galois conjugation here.

## Polynomial reconstruction and collision equations

After (2), require every coefficient of P,Q to lie in C[c]. This is
equivalent to the absence of negative c powers; there are no other
possible finite poles. Write F=sum_(i=0)^n f_i(c)v^i and set

    Phi_n(F)=sum_(i=1)^n f_i(c)*(3c)^(n-i)
                  *sum_(j odd, 1<=j<=i) binom(i,j)*2^(i-j)*(9c)^((j-1)/2).

Then the two exact collision equations are

    Phi_6(P)=0, Phi_9(Q)=0.                        (6)

This is the coefficient of r in the remainder of
(3c)^n F((r+2)/(3c),c) modulo r^2-9c. Hence (6) is equivalent to even
trace on the prescribed collision curve; it is not merely a leading
parity filter. Both Phi polynomials are expanded in `inputs_and_controls.json`.

Conditions (5),(6), Laurent coefficient membership and polynomial
reconstruction are necessary and sufficient for the normalized (6,9)
component. A solution would give an actual finite polynomial Keller pair
in B. Conversely every such (6,9) pair reaches this system under the
listed constant target transformations. The inherited potential criterion
then recovers its polynomial potential by integrating P dQ-kappa*v dc.

## Forced singular leading face: what changes at degree 15

Use the inherited Newton-polygon homothety and mixed-weight obstruction
with weight(v)=1, weight(c)=-1. The maximum weights are positive and in
ratio 2:3. For P they can only be 2 or 4. The top forms are T^2,T^3.

If P has weight 4, then T=v^2 L(cv), deg L<=1. Constant L is excluded by
the highest odd trace term; linear L makes P's v^6 coefficient have c-order
2, impossible for c^(6N). If P has weight 2, then T=v L(cv), deg L<=2.
Constant L is again excluded. Quadratic L makes the v^6 coefficient have
c-order 4, also impossible. Thus

    P_top=[A*v*(cv-rho)]^2,
    Q_top=[A*v*(cv-rho)]^3,
    A!=0, rho in {2/3,4/3}.                       (7)

For example on the collision curve T=A(r+2)(r+2-3rho)/r^2. The highest
odd term of T^2 is 2A^2(4-3rho)(4-6rho)r^(-3), giving both alternatives.
Lower weights cannot cancel this term.

Write P=c^(6N)v^6+sum_(i<6)p_i(c)v^i. Equation (7) gives

    ord_0(p4)=2, ord_0(p3)>=1, ord_0(p2)>=0.

In fact the next coefficients of Q force

    ord_0(p5)=3N+1,
    leading(p5^2/(c^(6N)*p4))=4.                (8)

Proof. The exact v^6 coefficient of Q contains

    (3/2)c^(3N)p3+(3/4)p5*p4/c^(3N)-p5^3/(16c^(9N))
      +k8*((4/3)c^(2N)p4+(2/9)p5^2/c^(4N))
      +(7/6)k7*c^N*p5.

If ord(p5)<3N, its cubic term is the unique pole; hence ord(p5)>=3N.
If ord(p5)=3N, the v^5 coefficient's p5^4/c^(15N) term is the unique
pole. Thus ord(p5)>=3N+1. If it were greater, that row's p4^2/c^(3N)
term would be the unique pole, of order 4-3N<0. At equality, the terms
of that lowest order are proportional to

    (p4^2/c^(3N))*(Y^2-8Y+16), Y=p5^2/(c^(6N)*p4).

All retained k_j terms have strictly higher order. Therefore Y has leading
value 4. This proof is valid for every N>=2 and both rho values. No bound
on the remaining c degrees was used.

Depression then gives

    ord_0(eta)=1-3N,
    ord_0(a)=2-4N, ord_0(b)=3-6N,
    leading(4a^3+27b^2)=0.                      (9)

Indeed, for alpha=p5/c^(5N), beta=p4/c^(4N), gamma=p3/c^(3N),

    a=(beta-5alpha^2/12)/2,
    b=(gamma-2alpha*beta/3+5alpha^3/27)/2.

The leading ratio alpha^2/beta=4 yields a double root in the leading
cubic R. In particular b has a forced pole with nonzero leading value;
the noncube proof's equation b=0 cannot be reused.

The quadratic part of the first-integral equations has a nonzero tangent
direction at that double-root cubic. Put a=-3B^2, b=2B^3 and
(u,w,z)=epsilon*(1,B,-2B^2). With all k_j zero, G4=G3=0 exactly, while
C=epsilon^3 and u^2w=B*epsilon^3. Thus checking only quadratic leading
terms cannot eliminate this direction. The cubic and higher equations,
the six surviving k_j, and global polynomiality still have to coexist.
This tangent is not a Keller pair or a solution of (5).

## Exact unresolved assertion

There is no proof here that the system (5),(6) has a solution or is empty
for every N>=2, with (7)--(9). Its algebraic fibers have not been proved
irreducible. More fundamentally, no argument reduces arbitrary larger
coordinate degrees in B to this system. Therefore this is **not** the
user's requested SINGLE IRREDUCIBLE GAP for the entire collision route.
Neither a counterexample nor full collision-route closure has been obtained.
