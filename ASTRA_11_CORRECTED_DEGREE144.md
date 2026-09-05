# Astra 11 — corrected degree-(108,144) leading system

Status: **OPEN. No counterexample.** Continued from Astra 10 commit
`9fc59779c8d50d8bb36fa54e4ef36a3f3355236f`, on
`astra/jc2-missed-routes-2026-09-05`.

This strike found a concrete loss of support in the archived above-125
compiler, solved the corrected first auxiliary leading equation exactly,
and proved an obstruction to a natural graded extension of every surviving
leading solution. It does **not** exclude the entire degree-(108,144) case,
and does not reduce general JC2 to one irreducible component. The collision
algebra remains excluded by the separate Astra 9 argument.

## What was actually missed

The published chain is

\[
A_0=(8,28),\quad A_1=(7/4,3),\quad(m,n)=(3,4).
\]

See Guccione–Guccione–Horruitiner–Valqui,
[Some algorithms related to the Jacobian Conjecture, Section 6](https://arxiv.org/html/1708.07936v1#S6).
The archived `trackD_chain_map.py` sets the reduced upper height to the
terminal height plus one. Here that produces a base top corner `(4,4)`.
But its stated transformations send

\[
(8,28)\xrightarrow{\text{swap}}(28,8)
\xrightarrow{y\mapsto y+\sum\lambda_kx^{-k}}(28,8)
\xrightarrow{x\mapsto x^{-1},\ y\mapsto x^4y}(4,8).
\]

The translations preserve the coefficient of the highest power of `y`.
Thus the stated map does not justify replacing `(4,8)` by `(4,4)`.
This is a direct contradiction in the compiler's claimed derivation,
not a statement that no other reduction could ever exist. Its upper height
four instead agrees with the different initial corner `(4,12)`.

The old degree-144 calculations are therefore calculations on their
displayed smaller supports, not an exhaustive treatment of the published
case. Their exact slice certificates remain valid on those supports.
We do not change the frozen historical files or retract unrelated
Proposition 4.3 results, whose exponent ratio is different.

The missing original lower corner can be derived: the first normal is
`(4,-1)`. In the integer chart, its lower endpoint `(a',b')` satisfies
`4a'-b'=4`, `0<=b'<28`, and `a'>b'` for this type-II.b edge.
Consequently it is `(1,0)`. The old reduced upper-axis `c'` ladder still
requires a separate proof for this chain; this report does not assume it.

## Exact classification of the first leading equation

In original coordinates put `T=xy^4`. The common leading root is

\[
S=xh(T),\qquad \ell(P)=S^3,\quad \ell(Q)=S^4,
\qquad \deg h=7,\ h(0)\ne0.
\]

Independent target scalings absorb the two leading constants. The marked
root producing `A1` has multiplicity three. Source scaling puts this root
at `1`, and we make `h` monic. Hence

\[
h=(T-1)^3B(T),\quad
B=T^4+a_3T^3+a_2T^2+a_1T+a_0,\quad B(0)B(1)\ne0.
\]

The homogeneous auxiliary identity used in the published chain argument
(the discussion preceding equation (2.12) in the same paper) gives,
after swapping coordinates and scaling the auxiliary polynomial,

\[
\{xyf(T),yh(T)\}=yh(T),\qquad T=x^4y,\quad \deg f\le5.
\]

Indeed the auxiliary weight is three, and its upper endpoint is `(21,6)`.
Expanding the bracket gives the exact univariate identity

\[
4Thf'+(h-3Th')f=h. \tag{1}
\]

This is a necessary leading condition, **not** the global potential
criterion and not a sufficient condition for a Keller pair. Its complete
solution in the displayed degree and marked-root normalization is as follows.

The triple root forces `f=(T-1)g`. Values at zero and one give
`g(0)=-1`, `g(1)=-1/5`. Write

\[
g=-1+c_1T+c_2T^2+c_3T^3+(4/5-c_1-c_2-c_3)T^4.
\]

Then the seven coefficients of

\[
\frac{4T(T-1)Bg'-3T(T-1)B'g-(4T+1)Bg-B}{T(T-1)}=0 \tag{2}
\]

are seven quadratic equations in seven variables. Exact rational Gröbner
elimination makes the ideal triangular: six parameters are polynomials
in `a3`, and the squarefree eliminant, up to a nonzero constant, is

\[
\begin{aligned}
&(a_3+5)(4a_3^2+8a_3+7)\\
&\quad\cdot(a_3^4+12a_3^3+48a_3^2+80a_3+55)\\
&\quad\cdot(3a_3^4+60a_3^3+394a_3^2+620a_3+475)\\
&\quad\cdot(2a_3^6+76a_3^5+1205a_3^4+10052a_3^3
             +46120a_3^2+109544a_3+104089).
\end{aligned} \tag{3}
\]

All 17 geometric points satisfy `B(0)B(1)!=0` and `deg(g)=4`.
The exact parameter polynomials, original equations and lexicographic basis
are in [astra11/certificate.json](astra11/certificate.json) and
[astra11/leading_lex.txt](astra11/leading_lex.txt).

| Factor degree | Multiplicities of the seven roots of `h` |
|---|---|
| 1 | 3, 1, 1, 1, 1 |
| 2 | 3, 4 |
| 4, first quartic | 3, 2, 2 |
| 4, second quartic | 3, 3, 1 |
| 6 | 3, 2, 1, 1 |

These are 17 **marked normalized leading solutions**, grouped into five
number-field factors, not 17 counterexample candidates or five proven
irreducible components of the global system. Marking a different triple
root can identify some representatives under further equivalences.

The rational solution is particularly transparent:

\[
B=T^4-5T^3+10T^2-10T+5=\frac{1+(T-1)^5}{T},
\qquad f=-\frac{(T-1)B}{5}.
\]

After the marked shear and displayed twist, its common right-edge root is

\[
x^4y^3(1+y^5).
\]

Thus its leading rows are `x^12 y^9(1+y^5)^3` and
`x^16 y^12(1+y^5)^4`. Their `y` degrees are 24 and 32.
This exact solution of the auxiliary identity detects the missing support;
it is not a Keller map.

## Terminal leading equation

For the type-I.b terminal form in `C[x^(1/4),x^(-1/4),y]`, the chain relation
`(m+n)bk-n(bl-a)=k` gives `k=1`. The starting monomials are
`x^(3/4)y` in `P` and `x^(1/4)` in `Q`; the normal is `(16,-9)`.
The opposite assignment gives nonintegral `k=3/4` and is impossible.
The published type-I.a-to-I.b reduction preserves this chart; in fact
type I.a would require `16|4`, so it cannot occur with this terminal data.

Writing `z=x^(9/4)y^4`, and allowing nonzero overall constants, the monic
terminal polynomials take the form

\[
P_* = x^{3/4}y(z^2+az+b),\qquad
Q_* = x^{1/4}(z^3+cz^2+dz+e).
\]

Their exact bracket is constant if and only if

\[
4a-3c=0,\quad ac+8b-6d=0,\quad
-2ad+5bc-9e=0,\quad-5ae+2bd=0.
\]

Nonzero constant bracket additionally requires `be!=0`.
Eliminating `c,d,e` gives
`5a^4-36a^2b+54b^2=0`, so `a!=0`, and

\[
\begin{aligned}
b&=a^2(1/3\pm\sqrt6/18),&c&=4a/3,\\
d&=2a^2(9\pm\sqrt6)/27,&e&=2a^3(4\pm\sqrt6)/81.
\end{aligned}
\]

The signs are linked and the bracket is exactly `-be/4`.
Residual scaling sets `a=1`. These are two conjugate terminal shapes.
They do **not** automatically extend to polynomial maps in the original
coordinates. Substituting `x=t^4` gives ordinary finite polynomials whose
Jacobian with respect to `(t,y)` is `-be*t^3`, not a nonzero constant.

## A structural obstruction to the simplest extension

The following theorem holds with unrestricted coefficient degrees.

**Theorem.** If a polynomial `c(y)` has a simple root, there are no
polynomials `A,B,D,E,F` for which

\[
\begin{aligned}
P&=x^2A+x^7B+x^{12}c^3,\\
Q&=xD+x^6E+x^{11}F+x^{16}c^4
\end{aligned}
\qquad\text{satisfy}\quad J(P,Q)=\kappa x^2,\quad\kappa\ne0.
\]

**Proof.** The coefficients at powers `x^22,x^17,x^12` successively force

\[
F=\frac43cB,\qquad E=\frac43cA+\frac29\frac{B^2}{c^2},\qquad
D=\frac49\frac{AB}{c^2}-\frac4{81}\frac{B^3}{c^5}. \tag{4}
\]

The corresponding homogeneous solutions over `C(y)` would be constant
multiples of `c^(11/4),c^(6/4),c^(1/4)`. Each has a fractional order at a
simple root of `c`, so none is a nonzero rational function. This proves
uniqueness of (4), not just that these expressions are particular solutions.

Polynomiality of `E` forces `B=cB1`. At a simple root `alpha` of `c`,
polynomiality of `D` then forces `B1(alpha)=0`: otherwise its second term
has a pole of order two that the first term cannot cancel. Locally write
`B=c^2 b`. The coefficient of `x^7` in the bracket at this root is

\[
\frac83 c'(\alpha)A(\alpha)^2.
\]

It must vanish. Since the root is simple, `A(alpha)=0`. Formula (4) now
shows that `D(alpha)=0`, and every coefficient of both `P` and `Q` is
divisible by `y-alpha`. Their Jacobian is divisible by `y-alpha`, which
contradicts `J=kappa*x^2`. This proves the theorem.

For every one of the 17 leading solutions the corrected common right-edge
coefficient is

\[
c(y)=y^3(y+1)B(y+1).
\]

It has a simple root at `y=-1`, since `B(0)!=0`. Thus the theorem excludes
this entire graded extension of all 17 solutions. The missing coefficient
rows cannot be set to zero without justification: **the theorem does not
exclude extensions using those rows**.

## Exact remaining problem and limits

One conservative finite formulation avoids assuming an unproved reduced
upper polygon. For each leading root `h` from (2), set `S=xh(xy^4)` and

\[
\begin{aligned}
P&=S^3+\sum_{\substack{0\le i\le24,\ 0\le j\le84\\4i-j<12}}p_{ij}x^iy^j,\\
Q&=S^4+\sum_{\substack{0\le i\le32,\ 0\le j\le112\\4i-j<16}}q_{ij}x^iy^j.
\end{aligned}
\]

Set the two free constant coefficients to zero by target translations.
These rectangles come from the standard-pair definition, not from the
faulty compiler. The unresolved equations are the exact coefficients of

\[
P_xQ_y-P_yQ_x-\kappa=0,\qquad \kappa u-1=0. \tag{5}
\]

The full terminal conditions can further be imposed after the finite
substitution `x=t^4, y=y+t^(-1)`: all terms of weight `4 deg_t-9 deg_y`
above 3 in `P` and above 4 in `Q` must vanish; terms at these weights are
the terminal forms above, with constants consistent with `B(1)`.
These are finite polynomial identities, not successive formal lifts.

No solution or characteristic-zero unit certificate for this full
compatibility problem was obtained. Equation (5) is not asserted to be
minimal or irreducible; the two endpoint classifications are not a
classification of its components. In particular, a fresh proof of the
reduced upper boundary and treatment of the nongraded coefficients remain
necessary before claiming a small exhaustive reduced system.

The useful change of direction is concrete: retain the missing upper
support, use the 17 exact leading solutions, and require a survivor to
escape the simple-root graded obstruction. Returning to the old smaller
degree-144 system would not address the published case.

## Reproduction and evidence scope

Run `python astra11/verify.py`. It recomputes the rational Gröbner basis,
FGLM elimination, five number-field parameterizations, nonvanishing tests,
root multiplicities, corner transport, terminal bracket identities and
graded obstruction identities, then compares the committed certificate.
Use `--write` only to regenerate the outputs.

The calculations use exact characteristic-zero arithmetic. There is no
numerical search, modular extrapolation or generic degree sweep. Ordinary
Keller and transformed-Jacobian positive controls are included. The
global collision-potential criterion was not modified, so no new conductor
jets or replay of its already-verified nontermination control was needed.
The proofs are human-readable mathematical arguments supported by exact
calculation, not externally reviewed or proof-assistant formalized proofs.

The old compiler is preserved by Git blob
`dd2e48198dd9368c2669d064dbbf58167661f184`; its narrative is
`3a4717d7ab6ef21c5301fb6390e889b5ea4377e6`.
The separate old lift report is blob
`fec452308130eb22de9fdd1ca702cc86f64e9c51`.
All can be read with `git cat-file -p <blob>` in the complete-record clone.

Final status: **OPEN — no finite polynomial Keller counterexample found.**
