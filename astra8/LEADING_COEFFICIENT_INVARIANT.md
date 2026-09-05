# A necessary invariant in arbitrary coordinate degree

This theorem does not close the collision route. It does remove an arbitrary
polynomial coefficient function from the remaining degree-15 system.

**Theorem.** Let P,Q in C[c,v] have J_(v,c)=kappa != 0 and m=deg_v P>1.
If lc_v(P)=f(c)^m for a nonconstant polynomial f, then

    f=gamma*(c-c0)^N, gamma != 0, N>=2.           (1)

No bound on m, deg_v Q, or coefficient degrees is assumed.

## Exactness from the Laurent coefficient

Put W=P^(1/m) with leading term fv, and pass to the rational auxiliary
coordinate x=fv (a further rational translation can depress P without
changing the argument). P is monic of degree m over K=C(c). In the
Laurent expansion of Q in W, write its negative coefficients as mu_i:

    Q=sum_(j>=0) lambda_j W^j+sum_(i>=1) mu_i W^(-i).

The nonnegative coefficients lambda_j are constant, by descending
cancellation in the Jacobian. Because W_x has leading term 1,

    J_(x,c)=m W^(m-1) W_x * sum_(i>=1) mu_i' W^(-i).

Independence of x implies successively

    mu_1'=...=mu_(m-2)'=0,
    mu_(m-1)'=kappa/(m f).                      (2)

All mu_i belong to K: P is monic over K and Q belongs to K[x]. Thus 1/f
has a rational primitive. Only finitely many Laurent coefficients are
needed for (2); this is not an assertion about conductor-adic lifting.

## Rational primitive lemma

**Lemma.** For a nonconstant polynomial f over C, 1/f has a rational
primitive if and only if f has the form (1).

Proof. A simple zero of f produces a nonzero logarithmic residue and is
impossible. Let T'=1/f, with T rational. T cannot have a polynomial part
of positive degree because T' tends to zero at infinity. Subtract T(infinity).
Suppose T has r finite poles of orders m_1,...,m_r>=1, with d=sum m_i.
These poles are exactly the zeros of f, whose orders are m_i+1. Therefore
deg(f)=d+r. At infinity, integration of the leading nonzero term of 1/f
shows T has a zero of order d+r-1. But a nonzero proper rational function
with denominator degree d cannot have a zero at infinity of order greater
than d. Hence r<=1. Since f is nonconstant, r=1. Its multiplicity is at
least two. Conversely, integrate gamma^(-1)(c-c0)^(-N) directly. QED.

Applying the lemma to (2) proves the theorem. Notice that exactness, not
merely a vanishing residue at a selected zero, is what makes the argument
global.

## Precise degree-15 consequence

After the noncube-h theorem, a (6,9) collision candidate must have h=f^3,
so lc_v(P)=f^6. Collision membership forces f(0)=0. Consequently

    f=gamma*c^N, N>=2,
    mu_5=C5+kappa*c^(1-N)/(6*gamma*(1-N)).        (3)

Constant rescaling of P,Q normalizes gamma=1 while changing the nonzero
constant kappa. There is no assumption bounding N.

The other normalized coefficients and the rational translation can all
be taken in C[c,c^(-1)]. Indeed their denominators come only from powers
of f during monic normalization and depression of the original polynomial
P. Formula (3) gives a necessary and sufficient replacement of the last
differential row in the normalized (6,9) system.

This theorem does not show that (3) is incompatible with the other four
first integrals, polynomial reconstruction and collision parity. It also
does not force the leading coefficient to be an m-th power in arbitrary
coordinate degrees. These are separate gaps; the theorem is not an
induction proving full collision-route closure.
