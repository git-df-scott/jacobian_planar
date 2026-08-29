# THE POLE THEOREM AND THE MIXED-ISOBARIC BARRIER

## Verdicts

1. A rational solution of \(D_PQ=1\) does **not** follow from gradient
   unimodularity.  A *regular* primitive on the generic affine fibre is the
   stronger condition detected by localization over \(K[P]\); an arbitrary
   rational primitive may have horizontal poles.
2. If a rational mate does exist, every finite irreducible component of its
   pole divisor is an irreducible component of a fibre of \(P\).
3. Consequently, if every fibre of a gradient-unimodular \(P\) is irreducible,
   every rational mate polynomializes.  On the night20 target locus,
   **rational mate = polynomial mate = a JC2 counterexample** when \(P\) is
   non-coordinate.
4. Every non-coordinate, gradient-unimodular polynomial that is isobaric for a
   mixed weight is mateless in every polynomial degree.  Thus a counterexample
   component cannot become mixed-isobaric after a polynomial symplectic change
   of variables.
5. No counterexample is produced here.

## 1. Pole theorem

Let \(K\) be an algebraically closed field of characteristic zero,
\(A=K[x,y]\), and

\[
 D=D_P=P_x\partial_y-P_y\partial_x,
 \qquad 1\in(P_x,P_y).
\]

### Theorem

Suppose \(Q\in K(x,y)\) and \(D(Q)=1\).  Every irreducible factor of the
denominator of \(Q\), written in lowest terms, defines an irreducible component
of a fibre \(P=c\).

### Proof

Let \(g\) be an irreducible denominator factor and let \(v_g(Q)=-m<0\).
Write locally \(Q=g^{-m}u\), with \(v_g(u)=0\).  If \(g\nmid D(g)\), then

\[
 D(Q)=-m g^{-m-1}uD(g)+g^{-m}D(u)
\]

has valuation \(-m-1\): its displayed first term cannot cancel with the
second.  This contradicts \(D(Q)=1\).  Hence

\[
             g\mid D_P(g)=[P,g]. \tag{1}
\]

Pass to the domain \(R=A/(g)\).  Equation (1) induces a derivation
\(\bar D\) on \(R\).  This derivation is nonzero: if it vanished then both
\(D(x)=-P_y\) and \(D(y)=P_x\) would lie in \((g)\), contradicting
\(1\in(P_x,P_y)\).  In the transcendence-degree-one function field
\(\operatorname{Frac}(R)/K\), the constants of a nonzero derivation are
exactly \(K\): a transcendental constant would make the whole function field
algebraic over a constant subfield, forcing the derivation to vanish in
characteristic zero.  Since \(\bar D(\bar P)=0\), we have \(\bar P=c\in K\).
Thus \(g\mid P-c\).  QED.

This rules out horizontal finite poles.  It does **not** say that rational
mates always exist, nor does it remove the places at infinity from the
generic-fibre exactness problem.

## 2. Irreducible fibres force polynomialization

### Corollary

If every fibre \(P-c\) is irreducible and \(D_P(Q)=1\) has a rational
solution, then it has a polynomial solution.

### Proof

By the theorem, the reduced denominator is a product of whole fibres, hence
\(B=b(P)\) up to a scalar.  Writing \(Q=A/b(P)\) gives

\[
                 D_P(A)=b(P). \tag{2}
\]

Let \(c\) be a root of \(b\).  Modulo the integral domain
\(A/(P-c)\), equation (2) says \(D_P(\bar A)=0\).  The induced derivation is
nonzero and the fraction field has transcendence degree one over the
algebraically closed field \(K\); its constant field is therefore \(K\).
Thus \(\bar A=a_c\in K\), so

\[
 A-a_c=(P-c)A_1,
 \qquad D_P(A)=(P-c)D_P(A_1).
\]

Cancel \(P-c\) from (2), and repeat over every root with multiplicity.  At the
end, \(D_P(A_*)=\lambda\ne0\), and \(A_*/\lambda\) is a polynomial mate. QED.

The night19 pole is now explained in the strongest possible form: its factor
\(\gamma xy+c\) is a *proper component* of the reducible fibre \(P=0\), so it
cannot be canceled as a first-integral denominator.

## 3. Exact second obstruction

Let

\[
 M_P=A/D_P(A),\qquad \kappa(P)=[1]\in M_P.
\]

Then a polynomial mate exists iff \(\kappa(P)=0\).  A regular primitive on the
generic affine fibre exists iff \(\kappa(P)\) dies after localizing the
\(K[P]\)-module at \(K(P)\), equivalently iff there are
\(0\ne b(t)\in K[t]\) and \(A\in K[x,y]\) with

\[
                   D_P(A)=b(P). \tag{3}
\]

An arbitrary rational mate lies only in \(\operatorname{Frac}(A)\), so it need
not imply (3): night19 is the concrete counterexample, with a pole on a proper
fibre component.  Fibrewise period vanishing says the specialized de Rham
class is zero; upgrading all such specializations to (3) is precisely the
relative-module/base-change step that must be certified.  Polynomiality then
asks whether the torsion class itself is zero.  On the
all-fibres-irreducible locus, the cancellation proof shows that this
distinguished torsion class cannot be nonzero:

\[
 \boxed{\quad \kappa(P)\text{ torsion}\Longrightarrow\kappa(P)=0
        \quad\text{if all fibres are irreducible}.\quad}
\]

Moreover, on that locus the pole theorem converts any rational mate into (3),
so rational, generic-regular, and polynomial mates are equivalent.  This is a
structural, degree-free mate test once generic exactness can be decided.

## 4. Complete mixed-isobaric classification

Take coprime \(p,q>0\) and the mixed weight

\[
                  w(x)=-p,\qquad w(y)=q.
\]

Suppose \(P\) is nonconstant, isobaric, and gradient-unimodular.  Since its
gradient is nonzero at the origin, \(P\) has a linear term.  The terms \(x\)
and \(y\) have different weights, so exactly one can occur.

If the linear term is \(y\), every exponent satisfies

\[
 -pi+qj=q,
\]

and coprimality gives

\[
 P=yH(z),\qquad z=x^q y^p,qquad H(0)\ne0. \tag{4}
\]

The other case is \(P=xH(z)\).  In (4), direct differentiation shows

\[
 1\in(P_x,P_y)\quad\Longleftrightarrow\quad H\text{ is squarefree}.
\]

Indeed, the axes are harmless because \(H(0)\ne0\); in the torus a critical
point is exactly a common nonzero root of \(H,H'\).

### Arbitrary-degree no-mate theorem

The bracket raises mixed weight by \(p\).  Only the weight \(-p\) part of a
prospective \(Q\) can hit the weight-zero target.  Its polynomial monomials
are precisely those of

\[
                    Q_{-p}=xS(z).
\]

An exact calculation gives

\[
 D_P(xS(z))=-\{HS+qzHS'+pzH'S\}. \tag{5}
\]

If \(n=\deg H\ge1\) and \(s=\deg S\), the highest coefficient inside braces
is

\[
 \operatorname{lc}(H)\operatorname{lc}(S)(1+qs+pn),
\]

which is nonzero in characteristic zero.  Equation (5) cannot equal 1.  If
\(H\) is constant, \(P\) is a coordinate and a linear mate exists.  The case
with linear term \(x\) is symmetric.

Therefore every admissible non-coordinate mixed-isobaric \(P\) has no
polynomial mate in any degree.  Night19 is \(p=q=1\) and linear \(H\); the
earlier pure-power families are special cases with \(q=1\).

## 5. Corrections to the live-search rationale

- An interior lattice point is **necessary**, not sufficient, for positive
  generic genus: Baker's inequality is an upper bound on genus.  Every actual
  candidate still needs an exact genus computation.
- Irreducibility removes proper vertical pole components, but not places at
  infinity.  Generic exactness remains a real condition.
- A bounded rational-denominator search returning EMPTY is carrier-relative.
  The pole theorem becomes unconditional only after either a rational mate is
  exhibited or generic exactness/torsion is certified structurally.
- Minkowski indecomposability is a sound sufficient test for fibre
  irreducibility, but it may discard valid irreducible fibres and therefore
  cannot define the whole CE locus.

## 6. Direct strike on the pole-free locus

The identity

\[
                         D_P(A)=P \tag{6}
\]

is a particularly sharp construction equation.  It gives the rational mate
\(A/P\).  If the zero fibre is irreducible, the proof above says that
\(A-a=PQ\) and (6) reduces exactly to \(D_P(Q)=1\).  Thus a
gradient-unimodular, non-coordinate solution of (6) with irreducible zero
fibre passes directly to the binding CE gate; no degree-bounded mate solve is
involved.

For fixed \(A\), equation (6) is linear in the coefficients of \(P\).
`eigensearch21.py` exhaustively tests all normalized two-term \(A\) of degree
at most 5 with the stated six-coefficient alphabet, plus 5,000 deterministic
sparse three/four-term cases, solving for \(P\) through degree 8 and checking
gradient unimodularity exactly.  The sweep found 2,898 hits, representing
2,835 distinct \(P\).  The independent certificate audit classifies every
one:

- 2,755 have an explicit nontrivial factorization over \(\mathbb Q\);
- 80 are triangular coordinates and carry an explicit polynomial mate;
- 0 remain unclassified.

Therefore this finite construction locus contains no counterexample.  This is
an exhaustive verdict only for the enumerated carriers and coefficient set,
not a theorem about all solutions of (6).

## Binding gate

No explicit polynomial pair \((P,Q)\) was found.  There is no CE claim.
