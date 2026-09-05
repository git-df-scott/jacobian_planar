# First remaining component: partial degrees (6,8)

This is an exact global reduction, not a formal conductor lifting problem.
There is no claim that the remaining equations have a solution.

## Two leading branches, not one

Normalize the top coefficients to

    P=h(c)^3 v^6+sum_(i=0)^5 p_i(c)v^i,
    [v^8]Q=h(c)^4,
    J(P,Q)=kappa != 0.

Use weight wt(v)=1, wt(c)=-1. Newton homothety makes the two maximum
weights proportional to 3:4. The leading-coefficient lemma makes the
first maximum less than 6. A nonpositive maximum puts P in C[c,cv],
excluded in `astra5/CONDUCTOR_TERMINATION.md`. Thus the maxima are 3,4.
The top bracket equation then forces

    P_3=alpha [v(cv-rho)]^3,
    Q_4=beta  [v(cv-rho)]^4,

with nonzero alpha,beta. In particular h has a simple zero at c=0.
The alternative constant polynomial in cv fails trace parity. The first
odd trace coefficients in the displayed forms are proportional to

    (2-3rho)^2(4-3rho),   (2-3rho)^3(4-3rho).

Consequently **both rho=2/3 and rho=4/3 remain**. Dividing by 2-3rho would
lose the first branch. For rho=4/3 the common root is -(b-2)/3. For
rho=2/3 it is vr/3, whose leading trace vanishes to higher order. Lower
weighted terms can enter its next trace conditions. This branch has not
been excluded by the leading residue.

For the associated Jacobian-1 potential, its top mixed-weight part is
H_7=(4/7)P_3 Q_4, and deg_v H=14. Thus this is also a concrete leading
potential classification, not just a degree label for the coordinates.

## Complete remaining system

For a Laurent series in v at infinity, [ ]_+ denotes its finite polynomial
part. Since h has a simple zero it is not a square. Galois conjugation in
the leading root of P^(1/6) removes all odd powers from the descending
coefficient expansion. After a target shear and translation, every pair
in this component has exactly

    Q=[P^(4/3)]_+ + k4 [P^(2/3)]_+ + k2 [P^(1/3)]_+,       (9)

where k4,k2 are constants and P^(1/3) has leading term h v^2.
The omitted terms are k6 P+k0 and are harmless target equivalences.
All coefficients in (9) are explicit rational functions of the p_i and h.
There is no infinite unknown series in (9).

Let q_j be those coefficients, with p_6=h^3. Define

    E_k=sum_(i+j=k+1) (i p_i q_j' - j p_i' q_j).           (10)

The equations E_13=...=E_5=0 hold identically. The unresolved equations are

    E_4=E_3=E_2=E_1=0,       E_0=kappa in C*,             (11)

subject to h,p_i,q_j polynomial and both exact collision-parity equations.
For a polynomial Z=sum_(i=0)^m z_i(c)v^i the latter equation is the single
polynomial identity

    Phi_m(Z)=sum_(i=1)^m z_i(c)(3c)^(m-i)
              sum_(1<=j<=i, j odd) binom(i,j)2^(i-j)(9c)^((j-1)/2)=0.

Thus the extra equations are Phi_6(P)=Phi_8(Q)=0. Polynomiality of q_j is
essential: clearing their denominators must retain the requirement that
the original rational coefficients are regular. Equations (9)--(11),
these regularity conditions, and the two parity equations are necessary
and sufficient for this normalized component. A solution with kappa
nonzero would give the requested Jacobian 1 after dividing Q by kappa.

The script `derive_exceptional_system.py` emits all nine q_j and the five
remaining differential equations with exact rational coefficients. It
checks each of the nine eliminated upper equations independently.

There is also a smaller useful representation. Set

    R=[P^(1/3)]_+=h v^2+s v+t,  S=P-R^3,  deg_v S<=3,
    L=[S/R]_+, N=S-LR, Z=L^2+2[L N/R]_+.

Then (9) becomes the finite rational expression

    Q=R^4+(4/3)RS+(2/9)Z+k4(R^2+(2/3)L)+k2 R.           (12)

Here R and S can have rational coefficients even though P is polynomial.
This distinction is exactly where an unwarranted recursive-collapse
argument could enter.

## The polynomial root inside B does collapse

Suppose R is polynomial and belongs to B. Every such quadratic R and
every cubic S in B have representations

    R=F(c)b+T(c),              F(0)!=0,
    S=A(c)a+B(c)b+W(c),        a=-cv^3+v^2+v,

with all coefficient functions polynomial. These representations follow
directly by solving Phi_2 and Phi_3; no localization is hidden in them.
In (12), Q in B requires either A=0 or

    A=3cM,  B=-M-(3/2)k4 F.

Indeed L=A v/(3F)+A/(9Fc)+B/F, and its quadratic correction in (12)
has even trace precisely under this condition. If A=0, P and Q both
belong to C(c)[R], so their Jacobian in C(c)[v] is divisible by the
nonconstant polynomial R_v, impossible.

For A!=0 put

    S=M(3ca-b)-(3/2)k4 F b+W.

Let J_j denote the coefficient of v^j in the exact expanded Jacobian
from (12). The certificate `polynomial_root_certificate.json` contains
all five rows and their exact combination

    D=J_3+8 J_4/(3c).

If M=c^m(mu+O(c)), F=F0+O(c), with F0 mu nonzero, its leading term is

    D=(64/3)F0 mu^2 (2m-1)c^(2m)+higher powers of c.       (13)

The exact expression has no W dependence, and all remaining terms have
higher valuation. Equations J_4=J_3=0 force m=1/2, impossible for a
nonzero polynomial (or a rational function regular enough for the stated
coefficient hypotheses). This proves that the whole polynomial-R-in-B
branch is empty, with arbitrary polynomial degrees of F,T,M,W.

## Extension: denominators do not rescue an even root

The same obstruction applies when R has rational coefficients and even
trace. Its coefficients are automatically regular at c=0. Indeed

    s=p5/(3h^2), t=p4/(3h^2)-p5^2/(9h^5).

The maximum-weight bound gives ord_0(p5)>=2, ord_0(p4)>=1, while
ord_0(h)=1. Thus s is regular, and t has at most a simple pole. The
specified top form P_3=alpha[v(cv-rho)]^3 cancels that pole exactly.

If R has even rational trace, solve Phi_2(R)=0 to obtain R=Fb+T with
F,T rational and regular at zero and F(0)!=0. Then S=P-R^3 has the same
regularity and even trace. Solving Phi_3 represents it as Aa+Bb+W with
A,B,W regular at zero: the apparent divisions by c are removed by the
constant and next coefficient of Phi_3. Parity of Q gives the same
A=3cM, B=-M-(3/2)k4F, with M regular at zero.

The certificate and (13) use only rational identities and orders at zero;
they do not need absence of poles elsewhere. They therefore give the same
impossible m=1/2. **Every remaining (6,8) candidate must have a quadratic
root R with non-even rational trace**, whether or not R is polynomial.

## Precise gap

The first remaining (6,8) component must have **R with non-even rational
trace**. The rho=2/3 leading branch has this defect already at leading
order. In the rho=4/3 branch R must have lower odd trace terms. Neither
polynomiality of P=R^3+S nor membership P in B by itself proves even trace
of its quadratic root.

The unresolved task is to solve or contradict (11) with this defect,
while retaining the exact regularity and parity conditions. The valuation
argument (13) is not valid until even trace of R is proved. No theorem
here propagates that property recursively. This is
why the full collision subalgebra remains open, despite the all-degree
obstructions for the preceding strata.
