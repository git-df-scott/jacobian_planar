# NIGHT22 — REALIZABILITY, CLOSURE, AND COMPONENT-POLE STRIKE

## Verdicts first

1. **The all-fibres-irreducible target class is nonempty.**  Degree-10
   Briançon-type polynomials are explicit gradient-unimodular, non-coordinate
   examples with every fibre smooth and irreducible.
2. The first realized profile is

   \[
   (g,r)_{gen}=(1,3),\qquad
   (g,r)_0=(0,4),\quad (g,r)_{-16/9}=(0,2),
   \]

   with Euler jumps (1+3=4=2g+r-1).  A second example has special profiles
   ((0,3),(0,3)), with jumps (2+2=4).
3. Exact direct solves for both degree-10 polynomials give
   `EMPTY_over_Q` through `deg A,Q = 30`, for both
   (D_P(A)=P) and (D_P(Q)=1), with four independently expanded lambda
   certificates.  This is bounded evidence only.
4. The closure chain is valid with a qualification: **generic algebraic
   exactness** gives a rational mate and descends from an algebraic closure;
   mere pointwise period measurements do not automatically assemble without a
   relative theorem.  In the all-fibres-irreducible plane case, the 2014
   Bustinduy--Giraldo--Muciño theorem supplies exactly that assembly step.
5. On a reducible fibre, polynomiality is governed by a finite componentwise
   principal-part mismatch.  Applied to all 2,755 reducible (D_P(A)=P) hits,
   zero have globally cancellable poles.  The 143 pole-free rows are precisely
   repetitions of the 80 triangular coordinates.
6. Two night15 period survivors have explicit exact rational mates.  Their
   component principal coefficients are respectively `(3/2,0)` and `(1,0)`,
   explaining their failure to polynomialize.
7. **No JC2 counterexample is found.**

## 1. T1 — complete arithmetic profile description

For a smooth irreducible affine fibre with compactification genus (g) and
(r\ge1) punctures,

\[
\chi=2-2g-r.
\]

Put (N=2g+r-1=1-\chi(F_{gen})).  Since there are no affine critical
points, the Suzuki--Gavrilov formula identifies an atypical jump with a
nonnegative Milnor number at infinity.  Hence each atypical value has

\[
 \delta_i=\chi(F_i)-\chi(F_{gen})
 =2(g-g_i)+(r-r_i)>0,qquad \sum_i\delta_i=N. \tag{1}
\]

Equation (1) is an effective enumeration.  Choose a partition
(N=\delta_1+\cdots+\delta_k).  For each part, all arithmetically compatible
special fibres are exactly the nonnegative solutions

\[
                 2g_i+r_i=2g+r-\delta_i,qquad r_i\ge1. \tag{2}
\]

`profiles22.csv` lists these atoms for (0\le g\le4,1\le r\le6); the formulas
are not bounded.

### Pruning

- If (g=0), all fibres irreducible forces (P) to be a coordinate by
  Neumann--Norbury.  Their Theorem 2 states that a rational polynomial with
  irreducible fibres is a coordinate.
- If there is only one atypical value, then its jump is (N), so (2) gives
  ((g_i,r_i)=(0,1)).  That fibre is (mathbb A^1), and
  Abhyankar--Moh--Suzuki makes (P) a coordinate.  In particular the proposed
  generic profile ((0,2)) has (N=1), one (mathbb A^1) special fibre, and
  is killed twice: by this argument and by Neumann--Norbury.
- Therefore a non-coordinate target must have (g\ge1) and at least two
  atypical values.  The cited theorems do **not** make that class empty.

Sources and hypotheses:

- [Suzuki--Gavrilov formula](https://emis.de/ft/47878), for polynomials with
  isolated critical points; here the affine Milnor number is zero.  The paper's
  criterion says an atypical value has strictly larger Euler characteristic.
- [Neumann--Norbury, Theorem 2](https://arxiv.org/pdf/math/9805093): “a
  rational (f) with irreducible fibres is a coordinate.”
- [Artal--Cassou-Noguès--Luengo](https://doi.org/10.1007/BF01459795), whose
  exact subject is polynomials with irreducible fibres and no critical points.

Short source quotations (kept here to make the invoked hypotheses auditable):

- Dimca--Sticlaru, Theorem 1.7: “All the fibers of the polynomials \(g\) and
  \(g'\) are irreducible affine plane curves.”
- Neumann--Norbury, Theorem 2: “a rational \(f\) with irreducible fibres is a
  coordinate.”
- Bustinduy--Giraldo--Muciño, Theorem 1 assumes periods vanish “for every
  \([\gamma]\in H_1(A_c,\mathbb Z)\)” and concludes “there is a polynomial
  \(F_1\).”

## 2. T2 — the realized address and direct strike

Let

\[
s=xy+1,\qquad p=xs+1,\qquad u=s^2+y,
\]

and

\[
g=p^2u-\frac53ps-\frac13s,
\qquad
g'=p^2u-\frac79ps+\frac19s. \tag{3}
\]

[Dimca--Sticlaru, Theorem 1.7](https://arxiv.org/html/2406.19795v4)
records that both have no critical points, all fibres are irreducible, exactly
two atypical values, and generic first Betti number (4).  Its Propositions
3.3--3.4 and branch data give:

| polynomial | generic | atypical profiles | jumps |
|---|---:|---:|---:|
| (g) | ((1,3)) | (0:(0,4),-16/9:(0,2)) | (1,3) |
| (g') | ((1,3)) | (0:(0,3),-64/81:(0,3)) | (2,2) |

Both are non-coordinate because (b_1(F_{gen})=4), rather than zero.

`briancon22.py` builds (3) over (mathbb Q) and independently solves the two
linear systems through degree 30.  All four are empty with exact dual
certificates.  This neither proves arbitrary-degree matelessness nor computes
the periods; it says the correct target exists but the first explicit members
do not yield a low-degree CE.

## 3. T3 — closure chain, precisely

Let (k=\mathbb C(t)) and

\[
C/k:\ P(x,y)=t,qquad \eta=dy/P_x=-dx/P_y.
\]

The local formulas glue because (1\in(P_x,P_y)).

### (i) Generic exactness equals a rational mate

(D_P) kills (P), hence is (k)-linear on (k(C)=\mathbb C(x,y)).
Thus (D_P(Q)=1) is exactly (dQ=\eta) in the function field of (C).
Moreover, since (eta) is regular on the smooth generic affine curve, a
primitive cannot have an affine pole: in characteristic zero a pole of order
(m) gives a pole of order (m+1) after differentiation.  Therefore the
primitive is regular on the generic affine curve, i.e. lies in
(\mathbb C[x,y]\otimes_{\mathbb C[P]}k).

### (ii) Descent from \(\bar k\)

Suppose (dQ=\eta) after a finite algebraic extension (L/k).  For every
(\sigma\in\operatorname{Gal}(L/k)),

\[
d(\sigma Q-Q)=0,
\]

so geometric connectedness gives (\sigma Q-Q\in L).  This is an additive
Galois cocycle.  Additive Hilbert 90 gives (a\in L) with
(\sigma Q-Q=\sigma a-a); hence (Q-a\in k(C)).  Exactness descends.  The
same conclusion follows by solving the finite coefficient system over (k).

### (iii) From fibrewise periods to a polynomial mate

There are two logically distinct routes.

1. If generic algebraic exactness has already been certified, it gives a
   rational mate; the night21 pole theorem polynomializes it when every fibre
   is irreducible.
2. If one only knows that **every period on every complex fibre** vanishes,
   assembly is not formal base change.  However
   [Bustinduy--Giraldo--Muciño, Theorem 1](https://www.journalofsing.org/volume9/bustiunduy-giraldo-mucino-raymundo.pdf)
   applies: in dimension two, its codimension-two reducible-fibre hypothesis
   means no reducible fibres; its exact-period hypothesis is precisely the
   stated one; and its finite set at infinity is automatic for a plane
   polynomial (also stated there for submersions).  It produces a polynomial
   Jacobian mate.

Consequently the conditional implication is exact:

\[
\boxed{\text{unimodular + non-coordinate + all fibres irreducible + all
fibre periods zero}\Longrightarrow\text{JC2 counterexample}.}
\]

The named gap is **certifying all fibre periods**, not Galois descent.  Sampled
periods, only typical fibres, or only residues do not meet the theorem.

## 4. T4 — exact component-pole formula

Fix a reducible fibre

\[
P-c=C_1\cup\cdots\cup C_s.
\]

Unimodularity makes it reduced and its components disjoint in the affine
plane.  Let (t=P-c).  In the completed local field at the generic point of
(C_i), write a rational mate as

\[
Q=\sum_{j=-m_i}^{\infty}a_{i,j}t^j.
\]

Since (D_P(t)=0), comparison of negative powers in (D_P(Q)=1) gives

\[
D_{C_i}(\bar a_{i,j})=0\quad(j<0).
\]

The induced derivation on the component function field is nonzero, whose
constant field is (mathbb C).  Hence every negative coefficient is a scalar
(alpha_{i,j}\in\mathbb C).  Define

\[
O_{c,j}(Q)=
(\alpha_{1,j}-\alpha_{s,j},\ldots,
 \alpha_{s-1,j}-\alpha_{s,j}). \tag{4}
\]

Two rational mates differ by an element of (mathbb C(P)), which shifts all
component coefficients at a fixed order by the same scalar.  Therefore (4) is
mate-invariant, and

\[
\boxed{\text{all vertical poles are cancellable by }h(P)
\iff O_{c,j}(Q)=0\text{ for every }c,j.} \tag{5}
\]

After cancellation the rational function has no affine codimension-one poles;
normality of (mathbb C[x,y]) makes it a polynomial.  Thus, once one rational
mate has been exhibited, (5) is a finite exact polynomiality test.  It does
not by itself decide whether a rational mate exists.

For (Q=A/P), only (j=-1) occurs and

\[
\alpha_i=A|_{C_i};qquad O=0\iff A-a\in(P)\text{ for some }a\in\mathbb C.
\]

`eigenpole22.py` verifies all 2,898 construction rows exactly:

- 2,755 reducible rows have nonconstant normal remainder and nonzero mismatch;
- 143 pole-free rows are exactly repetitions of triangular coordinates;
- no reducible hit polynomializes.

The exact global mismatch is decided over (mathbb Q).  Resolving the
individual constants on every absolute component remains unavailable for
2,086 rows because the stored certificate factors only over (mathbb Q), but
this does not weaken the global no-cancellation verdict.

## 5. T5 — two explicit night15 rational mates

For the G1 family with (n=1),

\[
P=h_0v+c(x-a)v^m=v\{h_0+c(x-a)v^{m-1}\},
\qquad v=y+t(x)/2,
\]

one has the exact rational mate

\[
Q=\frac{v^{1-m}}{c(1-m)},\qquad D_P(Q)=1. \tag{6}
\]

At pole order (m-1), its two zero-fibre component coefficients are

\[
\left(\frac{h_0^{m-1}}{c(1-m)},0\right),
\]

so (4) is nonzero.  `survivor_rational22.py` verifies (6) independently for
night15 hashes `c5e02d711fe5` and `a3b909a78c74`; their coefficient pairs are
`(3/2,0)` and `(1,0)`.  Thus period-zero and rational solvability coexist, but
component-pole mismatch blocks polynomiality exactly as predicted.

## Adversarial corrections and remaining holes

- The night20 sentence “(P-c) is irreducible over \(\bar{\mathbb Q}(c)\), so
  the generic fibre is geometrically irreducible” needs correction.  Degree
  one in the parameter proves irreducibility over that rational function
  field, not geometric irreducibility after algebraic closure (compare
  (x^2-c)).  Gradient unimodularity rules out nontrivial composition and can
  restore primitivity, but that is a separate argument.
- “All periods vanish over \(\bar k\)” must mean vanishing of the algebraic de
  Rham class.  There is no single analytic period lattice attached directly
  to the abstract \(\bar{\mathbb C(t)}\)-curve.
- The degree-30 Briançon verdicts are carrier-bounded.  No effective minimal
  mate-degree theorem has been proved.
- No exact nonzero Briançon period is supplied here.  Finding one would close
  these two explicit targets unconditionally by the period obstruction; a
  zero result would instead trigger the binding CE gate via the closure chain.
