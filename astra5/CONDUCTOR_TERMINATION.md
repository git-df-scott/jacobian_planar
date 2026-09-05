# Conductor strike: formal completion and global obstructions

September 5, 2026. Continues local Astra 4 commit `8921a59`.
The target is a polynomial pair in the exact collision subalgebra B with
Jacobian 1. No such pair was obtained. The full subalgebra is not excluded.

This strike resolves the formal correction problem, proves that a concrete
all-order solution cannot terminate polynomially, closes additional
unbounded families, and supplies stronger global construction gates.

## 1. Coordinates and scope

Use `A=C[v,c]`,

\[
r=3cv-2,\qquad t=\Delta=r^2-9c,\qquad
b=-3cv^2+4v+2.
\]

The result of Astra 4 is

\[
B=\{f\in A:f|_{\Delta=0}\text{ is even in }r\}
 =\mathbb C[b,c]+\Delta A.
\]

On the conductor,

\[
c=r^2/9,\qquad v=3(r+2)/r^2,\qquad r\in\mathbb C^*.
\]

Every pair in B identifies `(-1/3,4)` and `(2/3,4)`. There is no
ambiguity about the collision; polynomiality and the exact original
Jacobian are the unresolved requirements.

## 2. A global period condition missed by the first jet

If `{P,Q}_{v,c}=1`, then

\[
d(P\,dQ-v\,dc)=0.
\]

A closed polynomial one-form on A2 has a polynomial primitive. Restricting
to the conductor and taking its residue at r=0 therefore gives

\[
\boxed{\operatorname{Res}_{r=0}(p(r)q'(r)\,dr)=4/3,}
\qquad p=P|_\Delta,\quad q=Q|_\Delta.
\]

Indeed `v dc=(2/3+4/(3r))dr` on the conductor. This is a necessary global
condition; it does not follow from the bracket being correct modulo Delta.

The old trace pair `p=r^2/9`, `q=-1+12/r^2` has residue -8/3. Therefore
**no corrections divisible by Delta, of any polynomial degree, can make
that trace pair a polynomial Keller pair**. This closes the old first-jet
trace choice even if both coordinates are varied away from the conductor.

A corrected trace choice is

\[
p=r^2/9,\qquad q=-6/r^2,
\]

lifted by `P0=c`, `Q0=-(b+1)/2`. Its residue is 4/3.

For general even Laurent traces, the residue is the coefficient identity

\[
\sum_{n\in\mathbb Z}2n\,p_{-n}q_n=4/3,
\quad p=\sum p_n r^{2n},\quad q=\sum q_n r^{2n}.
\]

In particular, traces that are both polynomials in r^2, or both polynomials
in r^-2, are excluded. Both ends of the conductor must be visible at
infinity in the trace image. The residue condition is necessary, not sufficient.

## 3. The full formal correction problem is soluble exactly when the trace is immersed

The Delta-adic completion of A is

\[
\widehat A\simeq\mathbb C[r,r^{-1}][[t]],
\quad c=(r^2-t)/9,\quad v=3(r+2)/(r^2-t).
\]

To justify this, r and c are units modulo Delta, hence units in the
completion, and the displayed mutually inverse coordinate formulas apply.
The volume form and Keller equation become

\[
dv\wedge dc=-\frac{dr\wedge dt}{3(r^2-t)},\qquad
P_rQ_t-P_tQ_r=-\frac1{3(r^2-t)}.
\]

Write `P=sum p_i(r)t^i` and `Q=sum q_i(r)t^i`. At order n the complete
equation is

\[
(n+1)(p_0'q_{n+1}-q_0'p_{n+1})
=-\frac1{3r^{2n+2}}-K_n,
\]

\[
K_n=\sum_{i=1}^{n}\big((n+1-i)p_i'q_{n+1-i}
-i p_iq_{n+1-i}'\big).
\]

Only the lower coefficients enter K_n. No kernel is discarded: a particular
solution can be changed by
`(p_(n+1),q_(n+1)) += h(r)(p0',q0')` for arbitrary Laurent h.

**Formal theorem.** A prescribed trace pair p0,q0 has a formal Keller
extension if and only if `(p0',q0')` is the unit ideal in C[r,r^-1].

Necessity follows from the order-zero equation, whose right side is a unit.
For sufficiency, a Laurent Bezout identity for p0',q0' solves every displayed
linear equation recursively. This condition says precisely that the trace
parametrization has no critical point on C*.

If p0,q0 are even, all finite truncations lift to polynomials in B: A
surjects onto each A/(Delta^N), and the only membership constraint in B is
the even constant trace. Consequently **every immersed even trace has
polynomial approximations satisfying the bracket to every finite conductor
order**, including trace pairs forbidden by the global residue condition.

If the residue condition also holds, `P dQ-v dc` has a formal primitive:
closedness makes its r-residue independent of t; it is zero at t=0, so
termwise Laurent integration followed by formal t-integration constructs
the primitive. Thus even formal exactness adds no further obstruction after
the trace residue is imposed. This is not polynomial or rational exactness.

## 4. Explicit all-order control with a proof of nontermination

Define the polynomials

\[
s=\frac{rv-3}{6},\qquad
z=\frac{\Delta(cv^2-1)}4.
\]

They satisfy

\[
rs=1+\Delta v/6,\qquad 9cs^2=1+z,\qquad s|_\Delta=r^{-1}.
\]

For every integer N>=1, put

\[
Q_N=-v+3s\sum_{j=0}^{N}\binom{-1/2}{j}z^j,\qquad P_N=c.
\]

These are polynomials in B with the corrected traces from section 2.
An exact identity, valid for every N, is

\[
\boxed{\{c,Q_N\}-1
=-(r+1)(2N+1)\binom{-1/2}{N}z^N.}
\]

Proof: for `S_N(z)=sum_(j=0)^N binom(-1/2,j)z^j`, coefficient cancellation
gives
`S_N+2(1+z)S_N'=(2N+1)binom(-1/2,N)z^N`.
Now use `z=9cs^2-1` and `3s_v=r+1`.

The residual is divisible by Delta^N and is nonzero for every N. Degrees
are `deg Q_N=7N+3`, with no upper bound. At the origin the residual is

\[
(2N+1)\binom{2N}{N}/4^N>0.
\]

The formal limit is

\[
\widehat Q=-v+3s(1+z)^{-1/2},\qquad
c(\widehat Q+v)^2=1.
\]

It has exact formal Jacobian 1, preserves the collision, and satisfies the
global conductor residue condition. It cannot be polynomial: the last
identity would make the nonunit c invertible in C[v,c]. In fact it is not
rational in the original function field, because c has odd valuation at
the divisor c=0 and cannot have a rational square root.

Allowing both displayed coordinates to vary does not fix this example.
The polynomial pair `(c+Q_N^2,Q_N)` has the same residual and collision;
its formal limit has the same algebraic obstruction. The verifier checks
both coordinates and the original Jacobian for N=1,2,3,4. The written
identity proves the result for every N; no high-order numerical inference
is used.

## 5. Infinity splits a period that the conductor alone cannot distinguish

For a generic fibre Delta=t=a^2, with a!=0,+2,-2, the rational parametrization
has three punctures: r=a, r=-a, and infinity. A global polynomial Keller
pair must satisfy the separate residue identities

\[
\operatorname{Res}_{r=a}(P\,dQ)=\frac{a+2}{3},\qquad
\operatorname{Res}_{r=-a}(P\,dQ)=\frac{-a+2}{3}.
\]

The source form is
`v dc=2r(r+2)/(3(r^2-a^2)) dr`; its residue at infinity is -4/3.
Each identity follows from the same global polynomial primitive in section 2.
The two finite punctures coalesce at t=0. Their individual residues carry
information lost by the single conductor period.

For the base lift `(c,-(b+1)/2)`, the residue at r=a is `(4-a^2)/6`.
For the corrected polynomial controls of section 4, the errors in that
individual residue are

\[
\begin{aligned}
N=1:&\quad a(a^2-4)/16,\\
N=2:&\quad 5a(a^2-4)(a^2+12)/1024.
\end{aligned}
\]

They are nonzero, although their sums with the r=-a errors vanish.
Thus these controls can pass even the total period over a generic Delta
fibre while failing the separate infinity conditions. The verifier computes
these residues directly on the rational fibres, independently of the
Jacobian-error formula.

## 6. An unbounded family excluded at infinity

**Theorem.** If a polynomial Keller pair has a component
`P in C[c,cv]=C[c,r]`, it is a polynomial automorphism.

Write P=F(r,c), and C(r)=F(r,0).

If C is nonconstant, take a generic fibre P=p and a simple root a of
C(a)=p. In the rational (r,c) chart, c is a local parameter at (a,0),
and F_r(a,0)=C'(a)!=0. For a rational mate Q, the Keller equation on
that fibre gives

\[
\frac{dQ}{dc}=\frac1{3cF_r(r(c),c)}.
\]

Its residue is `1/(3C'(a))`, nonzero. The differential of a rational
function cannot have a nonzero residue. Hence no rational mate exists.

If C is constant, P is constant along the source line c=0. Restricting
the original Jacobian identity there gives
`-P_c(v,0)Q_v(v,0)=1`, so Q restricts to an affine linear function with
nonzero slope. The map is injective on that line, and therefore is an
automorphism by [Gwozdziewicz, Injectivity on one line](https://arxiv.org/abs/alg-geom/9305008).

In particular, a pair in B cannot have either component in C[c,r]. This
closes all attempts that keep one component polynomial solely in r and
Delta, with arbitrary degree. It includes
`P=c+Delta U(r)` for every polynomial U, and much larger correction families.
The symmetric statement holds for C[v,cv].

## 7. Stronger mixed-weight bounds

Give v,c weights 1,-1. Write d_+(P) for the greatest weight appearing in P.
The preceding theorem handles d_+(P)<=0.

**Corollary.** A polynomial Keller map with d_+(P)<=1 is an automorphism.

For d_+(P)=1 and d_+(Q)=q>0, write the leading terms as
`v f(u)` and `v^q g(u)`, u=cv. Their weight-(q+1) bracket must vanish.
The exact homogeneous bracket formula is

\[
\{v^if(u),v^jg(u)\}
=v^{i+j}(i f g'-j f'g).
\]

Thus `f g'-q f'g=0`, and `g=lambda f^q` for a nonzero constant lambda.
The polynomial target shear `Q-=lambda P^q` reduces d_+(Q). Repeat until
d_+(Q)<=0; section 6 applies to that component. The shears preserve the
Keller condition and invertibility. This proves the corollary.

By interchanging v,c, a component whose least weight is at least -1 also
forces invertibility. Moreover, if both greatest weights are at most 2,
the only remaining case is (2,2); its leading terms are proportional, and
a linear target subtraction reduces one to greatest weight at most 1.
The symmetric lower-weight statement follows as well.

Therefore a counterexample in this subalgebra must have both positive and
negative weights of magnitude at least 2 in each component, and at least
one component must reach weight >=3 and at least one weight <=-3. These
are all-degree necessary bounds, not a theorem excluding all wider strips.
Target shears can move a pair into an excluded class; merely displaying
both signs in both coordinates is not sufficient.

## 8. A necessary factorization for the minimal corrected traces

Suppose the trace pair is `p=r^2/9`, `q=-6/r^2`. Then

\[
PQ+2/3=\Delta H
\]

for a polynomial H. Taking the bracket with P and restricting to Delta gives

\[
P=\{P,PQ+2/3\}|_\Delta
=H|_\Delta\,(-3r^2p'),
\]

so `H|_Delta=-1/(6r)`. The exact full form is therefore

\[
H=-s/6+\Delta W(v,c),\qquad
\boxed{PQ=\Delta(-s/6+\Delta W)-2/3.}
\]

The trace of H is a unit, so H=0 is disjoint from the conductor. This is a
global polynomial factorization gate with both coordinates free. A
factorization alone does not imply Jacobian 1. For the degree-2m hyperbola
traces with product `-2/(3m)`, the same argument gives `H|_Delta=-1/(6mr)`.

No polynomial W and factors P,Q satisfying all the gates were obtained.
No bounded search over arbitrary W was undertaken: low-degree boxes are
already excluded, and generic failures would not establish all-degree closure.

## 9. An exact global construction gate using one polynomial potential

For a genuine polynomial solution, write

\[
dH=P\,dQ-v\,dc.
\]

Since the traces of P,Q are even, comparison under r -> -r gives
`H(r)-H(-r)=-4r/3` on the conductor. Thus the complete allowed potential
class is

\[
H=K-2r/3,\qquad K\in B.
\]

For a supplied polynomial H, calculate

\[
A=H_v,\quad C=H_c+v,\quad g=\gcd(A,C),\quad
\alpha=A/g,\quad\beta=C/g.
\]

If `alpha_c=beta_v`, the polynomial one-form
`alpha dv+beta dc` has a polynomial primitive Q. Differentiating
`g dQ=dH+v dc` then gives `{g,Q}=1` exactly. Check g,Q belong to B;
if they do, their known collision completes the counterexample gate.

Conversely, every polynomial Keller pair in B produces such a potential.
Since `(Q_v,Q_c)` is the unit ideal, the common factor g is P up to a
nonzero constant. Thus the construction loses no pairs in B, although it
does not provide a finite bound on K or guarantee that a suitable K exists.

`potential_gate` in the verifier implements this calculation for a supplied
H. Positive controls reconstruct actual polynomial automorphisms and then
reject them from B. Negative controls include an admissible potential with
gcd 1 and one with nonconstant gcd c; neither has a closed quotient form.
This is an exact global gate, not an exhaustive search or a claimed example.

## 10. Reproduction and verdict

Run `python astra5/verify_conductor_strike.py`. Seven groups pass: conductor
period, the full formal recurrence at four symbolic orders with its kernel,
all-order controls at four finite orders, separate infinity residues,
the hyperbola factor constraint, mixed-weight algebra, and the global
potential gate. Output and script hash are in `verification.json`.

The formal equivalence, the all-N nontermination identity, and the unbounded
family exclusions are written proofs. The line-injectivity theorem is an
explicit external input. No novelty priority, external review, or formal
proof-assistant verification is claimed.

The proposed local correction search has now been fully characterized and
shown insufficient as a discriminator. The original trace choice and the
stated unbounded families are closed. The full arbitrary-degree subalgebra
remains open. The remaining work is to satisfy the global polynomial gates,
not to collect more successful conductor jets. No polynomial counterexample
was found in this strike.
