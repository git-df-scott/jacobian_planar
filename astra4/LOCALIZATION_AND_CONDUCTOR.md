# Rational mates and the exact x=1 subalgebra

September 5, 2026; base record `efff2dc5c31a71030ccf931d22b9cd2047c0e172`.
All displayed polynomial/rational identities are independently checked in
`verify_missed_routes.py`. The general arguments are written proofs.

## 1. A false localization distinction in night21

The historical `night21/POLE_THEOREM.md`, blob
`eaef3802cbe22cf1365fdd8f56a971b8693ee3ef`, simultaneously proves that rational
mates have only vertical finite poles and says a rational mate need not
give a regular primitive on the generic affine fibre. The latter statement
is false. Section 3 explicitly denies the existence of A,b with
`D_P(A)=b(P)` for its night19 example; the example itself supplies them.

Put `A0=C[x,y]` and `D_P={P,-}`. For gradient-unimodular P, the correct
equivalence is

\[
\exists Q\in\mathbb C(x,y):D_PQ=1
\iff \exists Q\in A_0\otimes_{\mathbb C[P]}\mathbb C(P):D_PQ=1
\iff \exists A\in A_0,\ 0\ne b\in\mathbb C[t]:D_PA=b(P).
\]

Proof of the nontrivial implication: the valid pole theorem in that same
report says each irreducible denominator factor g divides some fibre P-c.
For every pole-bearing fibre, choose an exponent high enough that the
product `b(P)=product_c(P-c)^(N_c)` clears all denominators. This works
whether the fibres are irreducible or reducible. Now A=b(P)Q is polynomial
and D_PA=b(P). The converse follows by division.

An exact control is

\[
P=xy^2+y,\qquad Q=-\frac{x}{xy+1},\qquad A=-xy.
\]

Here `D_PQ=1`, `A/P=Q`, and `D_PA=P`. The gradient is unimodular since
`(1-2xy)P_y+4x^2P_x=1`. Also `-1/y` is a rational mate, and
`Q-(-1/y)=1/P`. Poles on a proper fibre component do not prevent clearing
by a whole fibre.

This control has no polynomial mate, as the valid mixed-weight argument
in night21 proves. Consequently the distinction that survives is between
a torsion class and the zero class of `[1]` in `A0/D_P(A0)`. Rational
solvability means torsion; polynomial solvability means zero. It is **not**
a distinction between a rational primitive and a generic regular primitive.

The all-irreducible-fibre cancellation proof remains valid. More precisely,
it suffices that the fibres over roots of the clearing polynomial b are
irreducible: modulo P-c, the numerator is constant; subtract that constant
and divide by P-c, then repeat. Nothing here reopens the two Briançon
targets whose generic differential is nonzero and holomorphic. A rational
function with nonzero exact differential cannot have that differential
holomorphic on a compact positive-genus curve.

## 2. Exact normalization and conductor of the collision subalgebra

In the inherited x=1 restriction, make the affine source-coordinate change
`v=y+1`, `c=2-3y-z`. The three target generators become

\[
a=-cv^3+v^2+v,\quad b=-3cv^2+4v+2,\quad c=c.
\]

Let `B=C[a,b,c]` inside `A=C[v,c]`. Direct calculation gives

\[
v^2-(b+1)v+3a=0,
\]

\[
\Delta=(3cv-2)^2-9c=4-3c(b+1),\qquad
\Delta v=b-2-9ca.
\]

Thus A=B+Bv is finite over B, their fraction fields are equal, and A is
the normalization of B. The identities also give `Delta*A subset B`.

The curve Delta=0 is a copy of C* with parameter r:

\[
r=3cv-2,\quad c=r^2/9,\quad v=3(r+2)/r^2,\quad
r^{-1}=(rv-3)/6.
\]

The last identity holds on the curve and proves the parametrization has
a regular inverse. Restrictions of the three generators are

\[
a=12r^{-4}-3r^{-2},\quad b=-1+12r^{-2},\quad c=r^2/9.
\]

Their image is exactly `C[r^2,r^-2]`. Since Delta*A is already contained
in B, this proves the complete, all-degree membership criterion

\[
\boxed{B=\{f\in\mathbb C[v,c]:f|_{\Delta=0}(r)=f|_{\Delta=0}(-r)\}.}
\]

It also proves that the conductor is **exactly** Delta*A. If f is in the
conductor, its restriction is even (multiply by 1), and its product with r
is even (multiply by the polynomial 3cv-2). In characteristic zero these
two conditions force the restriction of f to vanish. The reverse inclusion
was proved above.

An equivalent construction form, without an ambient target-degree cutoff, is

\[
P=F(b,c)+\Delta U(v,c),\qquad Q=G(b,c)+\Delta V(v,c),
\]

where F,G,U,V are arbitrary polynomials. This is complete for B, since b,c
already generate the even Laurent restrictions.

Every such pair identifies the two distinct source points

\[
(v,c)=(-1/3,4),\quad(2/3,4),
\]

whose common `(a,b,c)` image is `(-2/27,-2/3,4)`. Therefore an exact
solution of `{P,Q}_{v,c}=1` in this subalgebra would immediately be a
planar counterexample. This is a concrete restricted construction problem,
not an assertion that all possible counterexamples belong to B.

## 3. Why the old cubic projection frontier was already closed

The total degrees of a,b,c are 4,3,1. An ambient target polynomial of total
degree at most d restricts to a plane polynomial of degree at most 4d.
The proposed cubic projection therefore has plane degrees at most 12;
it was already excluded by known degree bounds.

More generally, the published lower bound 108 excludes all target-degree
cutoffs d<=26, because 4d<=104. This uses the reported theorem of
[Guccione–Guccione–Horruitiner–Valqui](https://arxiv.org/abs/2204.14178).
Using only Moh's older bound still excludes d<=25. Thus degree 27 is merely
the first target degree not eliminated by this coarse published bound;
it is not a viable example or a sufficient degree. Existing campaign Newton
exclusions still apply wherever their hypotheses hold.

## 4. Exact local progress that does not solve polynomial termination

There is a simple first-order solution along the conductor. With r=3cv-2,
put

\[
P_1=c+\Delta\,r(2r-1)/72,\qquad Q_1=b.
\]

These polynomials belong to B, preserve the collision, and satisfy
`{P1,Q1}-1 in (Delta)`. The verifier also checks this residual is nonzero.
Thus they are **not** a Keller pair. This establishes that the first normal
jet is not an obstruction. It does not establish higher-jet compatibility,
convergence, finite polynomial termination, or an all-degree mate for b.
There is also a direct all-degree no-mate proof for this fixed b. Give v,c
weights 1,-1. Since b-2 has weight 1, only the weight -1 part of P could
contribute to a constant bracket. It is c*S(z), z=cv, and

\[
\{cS(z),b\}=-(4-6z)S(z)-z(4-3z)S'(z).
\]

For nonzero S of degree n, this has leading coefficient
`3(n+2)lc(S)` at degree n+1, so cannot be constant. The fixed-Q=b
construction is a local control, not a live global search lane.

The remaining direct question here is whether two sufficiently high-degree
members of B can have bracket 1. The parity presentation removes redundant
ambient expressions and gives an exact membership gate for that question.

## 5. An integral-closure filter for primitive constructions

The closeout's pure-power obstruction extends as follows. Suppose a faithful
plane realization makes t=P and H(t,r)=Q polynomial, where r is rational
in the plane function field and H is monic in r of degree m>1 with
coefficients in C[t]. Then r is integral over C[x,y], hence polynomial.
If `{P,Q}` were nonzero constant, P,r would be algebraically independent,
but

\[
\{P,Q\}=H_r(P,r)\{P,r\}
\]

has the nonconstant polynomial factor H_r(P,r), a contradiction.
This is a useful early rejection test before searching plane charts.
It does not cover arbitrary nonunit leading coefficients or rational
t-dependent coefficients in H; those require their actual denominator and
integrality analysis.
