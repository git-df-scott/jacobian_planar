# Full collision-subalgebra obstruction

Work over C. Let A=C[v,c],

    b=-3cv^2+4v+2,
    Delta=(3cv-2)^2-9c,
    B=C[b,c]+Delta*A.

**Theorem.** For all finite polynomials P,Q in B,

    J_(v,c)(P,Q) in C  ==>  J_(v,c)(P,Q)=0.

In particular no pair in the entire collision subalgebra can be a Keller
pair. There are no bounds on either coordinate degree or coefficient degree.
The result also holds for the possibly larger set of all polynomials whose
trace under the substitution below is even; the converse membership theorem
from earlier strikes is not needed.

## 1. Collision parity forces a nonmonomial leading form

Define the integer mixed weight

    w(v^i c^j)=i-j,  w(F)=max{i-j : [v^i c^j]F != 0}.

On the collision curve use the exact parametrization

    c=r^2/9, v=3(r+2)/r^2.

It gives Delta=0 and b=-1+12/r^2. Therefore every F in B has an even
Laurent-polynomial trace in r.

Suppose w(F)=d>0. If the top weighted form were the single monomial
A0*v^i*c^j, with i-j=d and A0!=0, its trace would be

    A0*3^(i-2j)*(r+2)^i*r^(-2d).

The coefficient at the odd power r^(-2d+1) is

    A0*3^(i-2j)*i*2^(i-1),                     (1)

which is nonzero since i=d+j>0. Every lower-weight monomial has trace
starting at a power at least -2d+2, so none can cancel (1). This contradicts
even trace. Hence the top weighted form has at least two monomials.

As d>0, write that form uniquely as

    F_d=v^d L(vc), L in C[z].                    (2)

The polynomial L is not a monomial. Factor out its largest power of z.
What remains has nonzero constant coefficient and positive degree, and so
has a nonzero complex root lambda. Thus L(lambda)=0, lambda!=0.

Equivalently, the Newton polygon of F has an exposed edge with slope 1.
Adding the origin to the polygon makes no difference here, because d>0.

## 2. The residue obstruction for a Keller component

**Lemma.** A polynomial F whose positive mixed-weight leading form is
v^d L(vc), with L having a nonzero root, has no polynomial Jacobian mate.

Proof. Suppose J_(v,c)(F,G)=kappa!=0. The polynomial one-form

    F dG-kappa*v dc

is closed, so it equals dH for a polynomial H. This uses only polynomial
integration in characteristic zero.

Set t=1/v and c=t z. The polynomial

    E(t,z)=t^d F(t^(-1),t z)

has E(0,z)=L(z). Newton-Puiseux at a nonzero root lambda gives an integer
e>=1 and z(s) in C[[s]] with z(0)=lambda such that

    t=s^e, v=s^(-e), c=s^e z(s), F(v,c)=0.

Repeated roots are allowed; e is not assumed to be one. Restriction gives

    d(H(v(s),c(s)))=-kappa*v(s)*dc(s).

The left side is a derivative in C((s)) and has residue zero. But

    v(s)*dc(s)=(e*z(s)/s+z'(s))ds

has residue e*lambda. Thus 0=-kappa*e*lambda, a contradiction. QED.

Newton-Puiseux is used to assert an exact algebraic branch, not a finite
approximation to one. F(v(s),c(s)) vanishes identically. H restricts to a
Laurent series with only finitely many negative powers because H is a finite
polynomial. The coefficient of s^(-1) in its derivative is exactly zero.

This is the slope-one Newton-edge obstruction. An independent published
statement, in greater generality and with the same characteristic-zero
polynomial hypotheses, is Corollary 1.6 of
[Guccione, Guccione and Valqui, *The two-dimensional Jacobian conjecture and
the lower side of the Newton polygon*, arXiv:1605.09430v2](https://arxiv.org/html/1605.09430v2#S1).
The argument above spells out the specialization needed here. It does not
use that paper's later minimal-pair or standard-pair assumptions.

## 3. Both remaining components force a zero Jacobian

Assume now P,Q in B and J(P,Q)=kappa!=0. By section 1 and the lemma,
w(P)>0 is impossible. Applying the same argument with Q as first component
and Jacobian -kappa shows w(Q)>0 is impossible as well.

Thus every monomial of either component satisfies i<=j. Equivalently,

    P=F(c,cv), Q=G(c,cv), F,G in C[c,t].

The exact chain rule gives

    J_(v,c)(P,Q)=c*(F_t*G_c-F_c*G_t)|_(t=cv).    (3)

This vanishes on c=0, contradicting kappa!=0. Constants and zero components
cause no exception: they already have zero Jacobian. This proves the theorem.

## 4. Consequences for the requested construction

The full global potential criterion reconstructs a finite pair in B with
Jacobian 1. The theorem rules out that pair. Consequently there is no
polynomial potential H satisfying all three exact conditions

    H+2(3cv-2)/3 in B,
    g=gcd(H_v,H_c+v) in B,
    (H_c+v)g_v-H_v*g_c=g.

This consequence uses the saved necessary-and-sufficient criterion, but the
pair obstruction itself is independent of its derivation and all preceding
degree exclusions.

In particular every degree-15 (6,9) resonance is excluded. Its two top forms

    P_top=[A*v*(cv-rho)]^2, rho=2/3 or 4/3,

already have the forbidden edge; lambda=rho is nonzero in both cases. The
six retained fractional-power constants and every N>=2 are covered without
elimination or division by a parameter. All larger coordinate degrees are
covered by exactly the same proof. There is no next degree frontier in B.

The theorem closes this collision-subalgebra construction only. It does not
assert that every noninjective Keller map would lie in this subalgebra, and
does not settle the planar Jacobian conjecture in general.
