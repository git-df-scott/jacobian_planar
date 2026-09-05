# Astra 12 — exact global differentials and original-plane descent

September 5, 2026. Continued from Astra 11 commit
`5206d825b1e4baf6524b7af0febad58d9f1af4f5`.

**OPEN: no counterexample.** This run attacked the rational one of Astra 11's
17 marked leading solutions. The other 16 were not classified further.
The full coefficient system was not solved. The user then requested a full
report and consolidation into the complete-record branch; this document
records the exact stopping point.

The new result is stronger than eliminating a chosen joint row slice:
for every original polynomial Keller pair with this rational leading
solution and the stated terminal corner,

\[
[x^{11}]P=0,\qquad
[x^{10}]P=\tau y^8(1+y^5)^2(3+5y^2+8y^5). \tag{A}
\]

Here `P` is in the explicitly defined Laurent chart below. All other rows,
including negative powers of `x`, are retained. The scalar `tau` has **not**
been excluded. Its nonzero branch passes the next global differential test.
No claim that (A) is sufficient, or that these are global irreducible
components, is made.

## 1. An exact chart with no assumed reduced upper polygon

Use capital letters for the original plane coordinates and set

\[
X=x^4(y+1),\qquad Y=x^{-1}.
\]

This is a birational change of coordinates with determinant `x^2`. Its
inverse is `x=Y^(-1), y=XY^4-1`. It embeds `C[X,Y]` in
`C[x,x^(-1),y]`. In particular, an original pair with constant Jacobian
`kappa` gives

\[
P_xQ_y-P_yQ_x=\kappa x^2. \tag{B}
\]

We deliberately allow all the resulting negative `x` rows. This chart
does not require the unresolved upper-axis ladder in the old compiler.
The monomial identity

\[
X^iY^j=x^{4i-j}(y+1)^i
\]

gives an exact necessary-and-sufficient original polynomiality test.
For a row `x^k p_k(y)`, original polynomiality is equivalent to

\[
(y+1)^{\max(0,\lceil k/4\rceil)}\mid p_k(y).
\]

Within the original rectangle `0<=i<=24, 0<=j<=84`, it is additionally
equivalent to

\[
\deg_y p_k\le\min\left(24,\left\lfloor\frac{84+k}{4}\right\rfloor\right),
\qquad -84\le k\le12.
\]

For `Q`, replace `(24,84,12)` by `(32,112,16)`. This is a rowwise criterion
because the exponents of `(y+1)` form a basis, and different `(k,i)` map
to different original monomials.

The terminal condition from Astra 11 implies

\[
4k-5j\le3\quad(P),\qquad4k-5j\le4\quad(Q).
\]

To check the change of weight, use the fractional terminal chart
`X=t^4,Y=t^(-1)+z`, of weights `(4,-9)`. Then
`x=t/(1+tz)` and `y=(1+tz)^4-1`. Their leading terms are `t` and `4tz`,
of weights `4` and `-5`; the resulting associated graded coordinate
change is invertible. Thus the terminal weight bound transfers exactly.

For the two rows under examination this gives

| Row | Vanishing at `y=0` | Vanishing at `y=-1` | Maximum degree in `y` |
|---|---:|---:|---:|
| `p11` | 9 | 3 | 23 |
| `p10` | 8 | 3 | 23 |

The rational leading solution becomes

\[
c=y^3h,\quad h=1+y^5,\qquad
P=c^3x^{12}+\sum_{k<12}p_k(y)x^k,
\quad Q=c^4x^{16}+\sum_{k<16}q_k(y)x^k.
\]

The five roots of `h` are simple, and one is `-1`.

## 2. Global exactness forced by a finite mate

Let `w^4=c(y)` and work in the function field `K=C(y,w)` of its smooth
projective curve. Introduce `s=P^(1/12)` with leading term `wx` and invert
at `x=infinity`. If a finite Laurent polynomial `Q` exists, every
coefficient in its expansion in `s` belongs to **this global function
field**. At fixed `P`, equation (B) gives

\[
\left.\partial_yQ\right|_P
=\frac{\kappa x^2}{P_x}
=\frac{\kappa}{3}\partial_P(x^3)
=\frac{\kappa}{36s^{11}}\partial_s(x^3). \tag{C}
\]

Implicit inversion gives

\[
x^3=\frac{s^3}{w^3}
-\frac{p_{11}}{4w^{14}}s^2
 +\left(\frac{13p_{11}^2}{96w^{25}}-\frac{p_{10}}{4w^{13}}\right)s
 +O(s^0).
\]

Consequently the coefficient of `s^(-10)` in `Q` must be a rational
primitive of `-kappa*p11*dy/(72*w^14)`. After `p11=0`, the coefficient
of `s^(-11)` must be a rational primitive of
`-kappa*p10*dy/(144*w^13)`.

These are global meromorphic-differential exactness conditions, not
solvability to a specified local order. The expansion extracts necessary
global conditions; it does not imply polynomial termination. The finite
conductor-lifting route remains closed.

## 3. Proof that the entire `p11` row vanishes

The high bracket equations give

\[
\begin{aligned}
q_{15}&=\tfrac43cp_{11},\\
q_{14}&=\tfrac43cp_{10}+\tfrac29p_{11}^2/c^2,\\
q_{13}&=\tfrac43cp_9+\tfrac49p_{11}p_{10}/c^2
                      -\tfrac4{81}p_{11}^3/c^5.
\end{aligned}
\]

There are no additional homogeneous rational solutions in these rows:
they would be constant multiples of `c^(15/4)`, `c^(14/4)`, and
`c^(13/4)`, respectively, and have fractional orders at a simple root.

Polynomiality of `q14` first forces `h|p11`. If `p11` had order exactly
one at a root of `h`, the last term of `q13` would have a pole of order
two, while the other terms could not cancel it. Thus `h^2|p11`.
The row bounds at zero and infinity then give

\[
p_{11}=y^9h^2a(y),\qquad \deg a\le4.
\]

Put `z=w^2/y`, so `z^2=y+y^6`. The first differential from (C) is a
nonzero constant multiple of `a(y)dy/z^3`. Exactness in `K` implies
exactness in `C(y,z)` by normalized field trace. Taking the odd part of
a primitive under `z->-z` preserves its derivative.

At the six simple branch points this differential has poles of order at
most two, so its primitive has poles of order at most one. It is regular
at both points at infinity. It follows that its odd primitive must be
`B(y)/z`, where `B` is a polynomial of degree at most three. This proves
necessity, as well as sufficiency, of the finite polynomial identity

\[
2(y+y^6)B'-(1+6y^5)B=2a. \tag{D}
\]

Coefficient comparison gives exactly
`B=b3*y^3`, `a=(5*b3/2)*y^3`. Hence
`p11=lambda*y^12*h^2`. But its order at `y=-1` is two when
`lambda!=0`, whereas original polynomiality requires order at least
three. Equivalently, its second derivative there is `50*lambda`.
Therefore **`p11=0`**. No assumption was made about the other rows.

## 4. Complete reduction of the next row

With `p11=0`, the relevant high equations, up to an arbitrary polynomial
target shear `Q->Q+alpha*P`, are

\[
\begin{aligned}
q_{12}&=\tfrac43cp_8+\tfrac29p_{10}^2/c^2+\alpha c^3,\\
q_{11}&=\tfrac43cp_7+\tfrac49p_{10}p_9/c^2,\\
q_{10}&=\tfrac43cp_6+\tfrac49p_{10}p_8/c^2+\tfrac29p_9^2/c^2
          -\tfrac4{81}p_{10}^3/c^5+\alpha p_{10}.
\end{aligned}
\]

At a simple root of `h`, first `q12` gives `p10=c*v` locally.
Let `v0` and `b0` be the values of `v` and `p9` at the root.
The leading poles of `q11,q10` give

\[
v_0b_0=0,\qquad9b_0^2-2v_0^3=0.
\]

These imply `v0=b0=0`; explicit polynomial identities certifying
`v0^4=0` and `b0^3=0` are checked by the script. Thus `h^2|p10` and
`h|p9`. In particular,

\[
p_{10}=y^8h^2a(y),\qquad\deg a\le5.
\]

Now set `u=1/y`, `V=w/y^2`. The quartic curve becomes

\[
V^4=1+u^5.
\]

The next differential from (C), apart from a nonzero constant, becomes
`u^6*a(1/u)du/V^5`. It has poles of order at most two at the five finite
branch points, and order at most four at the unique point at infinity.
Projecting a primitive to its character under `V->iV`, it must be
`B(u)/V`, with `B` a polynomial of degree at most two. There are no other
allowed poles. Exactness is therefore equivalent to

\[
4(1+u^5)B'-5u^4B=4u^6a(1/u). \tag{E}
\]

Writing `B=b0+b1*u+b2*u^2`, all solutions are

\[
b_1=0,\qquad a(y)=\tfrac34b_2-\tfrac54b_0y^2+2b_2y^5.
\]

Original polynomiality requires `a(-1)=0`, hence `b0=-b2`.
Putting `b2=4*tau` gives precisely (A), with the exact primitive

\[
\frac{4\tau(u^2-1)}{V}.
\]

This proves the classification for this row. The entire nonzero parameter
range can be normalized to `tau=1` by the original diagonal change
`(X,Y)->(r^4X,r^(-1)Y)` and independent target scalings, choosing
`r^2=tau`. This preserves `XY^4` and the marked leading solution.
The cases `tau=0` and `tau!=0` must both be retained.

## 5. Direct attack on the nonzero survivor

The next source-forcing differential contains, up to a nonzero scalar,

\[
\frac{24c^3p_8-11p_{10}^2}{w^{23}}\,dy. \tag{F}
\]

This test does **not** eliminate `tau!=0`. With `E=3+5y^2+8y^5`, the
explicit finite polynomial

\[
p_8=\frac{11}{24}\tau^2y^7hE^2
\]

makes its numerator identically zero and satisfies the original row bounds
and descent divisibility. This is an exact control against falsely closing
the surviving parameter. It is not a pair `P,Q`, not a complete solution
of the coefficient equations, and not evidence that a formal construction
terminates. The full next meromorphic linear problem was also solved in
scratch and had 11 free parameters; that redundant exploratory calculation
is preserved in `astra12/exploration/next_exact.py`.

The remaining equation is still (B), with all finite rows satisfying the
exact original-plane descent conditions, the two endpoint leading forms,
and (A). In particular `p9` and the other lower rows have not been solved.
No rational or complex finite Keller pair was reconstructed, so there is
no collision or noninvertibility witness to report.

## 6. Other work examined and limits

- Rechecked the published chain and transformation arguments in
  [arXiv:1708.07936](https://arxiv.org/html/1708.07936v1) and
  [arXiv:2204.14178](https://arxiv.org/html/2204.14178v1).
  The old reduced upper-axis ladder was not promoted to a proved input.
- Considered eliminating other marked leading solutions by choosing their
  additional multiple roots. The root-selection hypotheses of the regular
  corner theorem were not fully verified, so **no such elimination is claimed**.
  The relevant primary source is
  [On the shape of possible counterexamples, arXiv:1401.1784v3](https://arxiv.org/pdf/1401.1784).
- Checked a polynomial-part ansatz
  `P=R^3+A*R+B`, `Q=R^4+(4/3)A*R^2+(4/3)B*R+(2/9)A^2`.
  For `A=u*x^3*y^2`, `B=v*x^2*y`, its bracket is divisible by `x^3*y`
  for every polynomial `R`; that ansatz cannot give `kappa*x^2`.
  This observation does not exclude general `A,B` or general Keller pairs.
- A cyclic character projection strengthens Astra 11's joint graded-slice
  exclusion: if `P` has only rows `2,7,12` and `deg_x Q<=16`, averaging any
  mate onto rows `1,6,11,16` preserves (B). Therefore adding other `Q` rows
  alone cannot rescue that `P` slice. This does not justify projecting a
  general `P`, because the bracket is bilinear.
- No degree sweep, numerical point search, modular exclusion, new conductor
  lift, or claimed global component enumeration was performed.

## 7. Reproduction and proof status

Run `python astra12/verify.py`. Seven groups pass, including the saved-output
comparison. The script recomputes the high coefficients, local radical
identities, two exact linear differential classifications, inverse descent,
an ordinary Keller control, and the nonzero surviving-parameter control.
Use `--write` to regenerate `astra12/certificate.json`.

The written pole-order arguments establish completeness of the two global
primitive tests within their specified spaces. They have not received
external review or proof-assistant formalization. The script is supporting
exact algebra, not an independent verification of every written geometric
hypothesis. The full JC2 objective remains unachieved.
