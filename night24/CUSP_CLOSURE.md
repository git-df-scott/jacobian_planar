# NIGHT24 — CUSP-PRESERVING FAMILY: EXACT CLOSURE

## Verdicts first

1. The maximal cusp-preserving family in the natural Briançon chart, linear
   in \(u\) and with cleared bidegree at most \((2,3)\), is

   \[
   P_{\lambda,\alpha,\beta,\gamma}
   =p^2u+\lambda sp^2+\alpha p^2+\beta p+\gamma.\tag{1}
   \]

2. Its genus-one, three-puncture open has
   \(\Delta=\lambda^2-4\alpha\ne0\).  On this open the exact elliptic de
   Rham-zero locus is **EMPTY**: \(\eta\) has exactly one double pole, so a
   primitive would be a nonconstant elliptic function with one simple pole.
3. The generic gradient-unimodular locus is

   \[
   \alpha=\lambda^2/4,\quad
   \beta=-\lambda(\lambda+2)/4,\quad \lambda\ne0,-2.\tag{2}
   \]

   It has \(\Delta=0\).  There are also exactly three isolated submersions;
   two have \(\Delta\ne0\) and realize profile \((1,3)\), but their elliptic
   de Rham class is nonzero.
4. On the curve (2), \(\eta\) does become exact generically and an explicit rational
   mate exists.  But the reducible fibre \(P=\gamma\) has three unequal
   component constants, so its pole mismatch never vanishes.  There is no
   polynomial mate in any degree.
5. **No counterexample is found.  This entire cusp family is closed
   `EXACT-ALL-DEGREES`.**

## 1. Symbolic support derivation

Write a perturbation in the Briançon subalgebra, linear in \(u\):

\[
P=A(p)u+B(s,p).
\]

Using \((p-1)u=s(sp-1)\), put \(H=(p-1)(P-t)\).  Restrict to the smallest
bidegree retaining the Briançon genus calculation, \(\deg_sH\le2\),
\(\deg_pH\le3\).  At \(s=\infty\), put \(z=1/s\).  The cusp weights are

\[
\operatorname{wt}(p)=2,\quad \operatorname{wt}(z)=3.
\]

A monomial \(s^ip^j\) becomes \(z^{2-i}p^j\), of weight
\(3(2-i)+2j\).  Fixing the weight-six terms \(p^3+Tz^2\) and excluding all
lower weights leaves exactly

\[
(i,j)=(2,3),(1,2),(1,3),(0,0),(0,1),(0,2),(0,3).
\]

Polynomial liftability through \((p-1)u=s(sp-1)\) then forces \(A=p^2\),
and forces the \(s\)-dependent perturbation to be \(\lambda sp^2\).  The
remaining terms are a quadratic polynomial in \(p\), giving exactly (1).
`cusp_family24.py` performs this enumeration and all lift identities over
\(\mathbb Q\).

The cleared fibre, with \(T=t-\gamma\), is

\[
\begin{aligned}
H={}&s^2p^3+\lambda sp^3-(1+\lambda)sp^2+\alpha p^3
 +(\beta-\alpha)p^2\\
 &-(T+\beta)p+T.\tag{3}
\end{aligned}
\]

At \(s=\infty\), (3) has initial form \(p^3+Tz^2\), so
\(\nu(\eta)=-2\) and the residue vanishes identically.  At \(p=\infty\),
the boundary polynomial is

\[
s^2+\lambda s+\alpha.
\]

Hence \(\Delta\ne0\) gives two infinity places there; together with the cusp
this is the required three-puncture profile.  The bidegree-\((2,3)\) arithmetic
genus is two and the cusp has delta-invariant one, leaving generic genus one.

## 2. Exact elliptic de Rham reduction

Since (3) is quadratic in \(s\), define

\[
Y=p\{2sp+\lambda p-(1+\lambda)\}.
\]

Completing the square gives the exact genus-one model

\[
Y^2=F(p)=pG(p),\tag{4}
\]

where

\[
\begin{aligned}
G(p)={}&(\lambda^2-4\alpha)p^3\\
&+[-2\lambda(1+\lambda)-4\beta+4\alpha]p^2\\
&+[(1+\lambda)^2+4T+4\beta]p-4T.
\end{aligned}
\]

The Gelfand--Leray form is exactly

\[
\eta=-\frac{dp}{pY}.\tag{5}
\]

For \(T\ne0\), \(p=0\) is one ramified point \(O\).  Formula (5) has a
double pole at \(O\), zero residue, and no other poles on the compact quartic
model.  Therefore

\[
(\eta)_\infty=2O.\tag{6}
\]

If \(\eta=dR\), then \(R\) can have only one simple pole, at \(O\).  But on
a genus-one curve \(\ell(O)=1\) by Riemann--Roch; equivalently, a degree-one
map to \(\mathbb P^1\) would force the curve to be rational.  Thus \(R\) is
constant, contradicting \(\eta\ne0\).  This proves

\[
\boxed{\text{de Rham-zero locus on the genus-one cusp open}=\varnothing.}
\tag{7}
\]

This is the finite exact de Rham decision requested in T3.  No numerical
periods are used.

Reference for the exact theorem used here: [Stacks Project, Riemann--Roch for
curves](https://stacks.math.columbia.edu/tag/0B5B), applied to a smooth
projective genus-one curve and the degree-one divisor \(O\).

## 3. Exact geometric conflict

Let \(h=p-1\) and \(d=4\alpha-\lambda^2\).  Away from the two inverse-base
charts, criticality reduces exactly to

\[
2dh^3+(d+2\lambda+4\alpha+4\beta)h^2+1=0.\tag{8}
\]

Normally, a nonconstant (8) has a root away from the exceptional values
\(h=-1\) (the \(p=0\) chart) and \(h=1/\lambda\) (the non-liftable
\(s=0\) value), producing a critical point.  Enumerating the cases where all
roots lie in that two-point set gives exactly three additional submersions:

\[
(\lambda,\alpha,\beta)=
(1,1/4,-1),\quad(1/2,3/32,-9/16),\quad(2,3/4,-9/4).\tag{9}
\]

A quadratic gives the first; a cubic with exceptional-root multiplicities
\((1,2)\) or \((2,1)\) gives the other two.  Exact Bezout certificates
independently confirm all three.  Outside (9), avoiding critical points forces
(2).  Conversely, on (2) the remaining charts are exact: at \(p=0\),
\(dP=\beta\,dp\), so \(\beta\ne0\) is equivalent to
\(\lambda\ne0,-2\); the two \(p=1\) charts have no simultaneous derivative
zero.

The curve (2) makes \(\Delta=0\).  In fact (4) collapses further to

\[
Y^2=p\bigl((1+4T)p-4T\bigr),
\]

which is rational.  The first point in (9) also has \(\Delta=0\).  The other
two have \(\Delta=-1/8\) and \(1\), respectively, so the geometric
profile-\((1,3)\) submersion locus is not empty.  Nevertheless (6)--(7) apply
unchanged: each has one double pole on its elliptic compactification, hence a
nonzero de Rham class and no rational generic mate.

## 4. Rational mate and exact pole mismatch on (2)

Although the genus-one target has died, the unimodular degeneration is an
important adversarial control.  Put

\[
L=2sp+\lambda p-(1+\lambda),\qquad A=-L/2.
\]

The formal coefficient checker proves on (2), in
\(\mathbb Q[\lambda,x,y]\),

\[
D_P(A)=P-\gamma.\tag{10}
\]

Thus

\[
Q_{\rm rat}=\frac{A}{P-\gamma}
\]

is an exact rational mate.  The exceptional fibre factors more strongly than
the initial visible \(p\)-factor:

\[
P-\gamma=\frac14pR_+R_-,\tag{11}
\]

with

\[
R_+=2+2xs+\lambda x,\quad
R_-=2y+2s^2+\lambda s.
\]

The identities

\[
L+1=sR_+,\quad L-1=xR_-
\]

give the principal coefficients of \(A/(P-\gamma)\) on these three
components:

\[
\left(\frac{1+\lambda}{2},\frac12,-\frac12\right).\tag{12}
\]

The last two are unequal in characteristic zero for every \(\lambda\).
Consequently the component-pole mismatch is always nonzero, no addition of
\(h(P)\) can cancel the poles, and no polynomial mate exists.  This closes
the reducible case `EXACT-ALL-DEGREES`.

The exact sample \((\lambda,\alpha,\beta,\gamma)=(2,1,-2,0)\) carries an
independently expanded degree-eight gradient Bezout certificate, a
Shpilrain--Yu `NON_COORDINATE` verdict, the rational identity (10), the
factorization (11), and all three constants (12).  A second sample,
\((\lambda,\alpha,\beta)=(1/2,3/32,-9/16)\), independently certifies an
isolated profile-\((1,3)\) submersion with \(\Delta=-1/8\).

## 5. Minimal next obstruction

The conflict is now precise:

- the original Briançon open makes \(\eta\) holomorphic;
- the cusp makes \((\eta)_\infty=2O\), which is still too small for an exact
  differential on an elliptic curve;
- the generic unimodular locus collapses the elliptic curve and creates three
  incompatible fibre-component constants, while its isolated elliptic
  exceptions retain the one-double-pole obstruction.

By Riemann--Roch, the next positive-genus family must enlarge the prospective
primitive's pole divisor to degree at least two.  Equivalently, the next
Gelfand--Leray pole profile must contain either

\[
(\eta)_\infty\ge3O
\quad\text{or}\quad
(\eta)_\infty\ge2O_1+2O_2,
\tag{13}
\]

with all residues zero.  This is the minimal next construction target.  A
single double pole on a genus-one compactification is now forbidden, not just
for (1), but universally.

The constructive enlargement should therefore be parameterized in reverse:
choose a genus-one model and a degree-two elliptic function \(R\), prescribe
\(\eta=dR\) (whose pole divisor starts at \(3O\)), and solve the polynomial
embedding equations that make this differential the Gelfand--Leray form of
some \(P:\mathbb A^2\to\mathbb A^1\).  This “triple-pole reverse-exactness”
family is the minimal theoretical enlargement; merely adding more coefficients
to (1) while retaining \((\eta)_\infty=2O\) cannot help.

## Final fields

- `CE: NO`
- `CEC: NO`
- cusp-preserving family: equation (1)
- de Rham-zero locus: `EMPTY` on its genus-one open
- strongest surviving \(P\): `NONE`
- mate status: rational-with-poles on the unimodular degeneration; otherwise
  obstructed by the elliptic period class
- next exact obstruction: realize a residue-free pole divisor of type (13)
  while retaining a smooth non-coordinate positive-genus submersion
