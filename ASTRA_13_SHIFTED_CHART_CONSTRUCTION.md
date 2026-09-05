# Astra 13 — restored fractional shift and coupled construction attempt

September 5, 2026. Branch `astra/jc2-five-branch-2026-09-05`.

**OPEN. No finite polynomial Keller counterexample was found.** The preceding
review and its exact supporting calculations were pushed first, in commit
`9e764c064b374ba6f7e4e60b2c5e346e33ff20bb`. This report records the subsequent
construction work, including a chart correction, new necessary row families,
a rejected particular family, and retained alternatives.

## 1. Five leading solutions remain, but the row chart needs another parameter

The additional-root argument in
[the review](JC2_RETHINK_AND_COUNTEREXAMPLE_PLAN.md) still excludes twelve of
Astra 11's seventeen marked leading solutions under the documented
standard-pair hypotheses. Its multiplicity checks and terminal arithmetic
replay with `python astra13/verify_review.py`.

The next issue is separate. After marking a triple root, the common corner
is `(7/4,3)` in `L^(4)`. The previous calculations used the direct chart

    X=t^4, Y=t^(-1)+Z.

The regular-corner argument permits a type-III step before the noncommuting
terminal form. The step's normal `(rho,sigma)` has `rho|4` and

    -7/12 < sigma/rho < -1/4.

The only primitive possibility is `(2,-1)`. Its removal introduces a shift
by `eta*X^(-1/2)`. No further distinct type-III normal is in the interval
after this step. The terminal type-I.a option is excluded by the same
integer-endpoint arithmetic as in the review; type-I.b has normal `(16,-9)`.
Consequently the construction must retain

\[
X=t^4,\qquad Y=t^{-1}+\eta t^{-2}+Z. \tag{1}
\]

The determinant is `4t^3` for every eta. The original rectangle bounds
remain unchanged; the terminal conditions must be imposed after (1).

The published ingredients are the corner transformations and restrictions
in [On the shape of possible counterexamples](https://arxiv.org/html/1401.1784v3),
especially Propositions 5.17–5.19 and Theorem 7.6. The direction enumeration,
Jacobian identity, and an ordinary Keller positive control are checked in
`verify_shifted_rows.py`. This is a written application of the published
geometry with algebraic checks, not a proof-assistant formalization.

**Scope correction:** Astra 12's proof that p11 vanishes remains valid for
its stated direct terminal chart. The record had not proved that eta must
vanish in the entire degree-(108,144) case. The expanded necessary equations
below allow nonzero eta. They do not establish that a full pair with
nonzero eta exists.

For the rational leading root, use the same birational integer chart

    X=x^4(y+1), Y=x^(-1), c=y^3(1+y^5), J(P,Q)=kappa*x^2.

Before removing the possible extra shift, the weaker bounds are

    k-j<=3 for P, k-j<=4 for Q.

In particular p11 can start at y^8 rather than y^9. Original polynomiality
still requires order three at y=-1 and degree at most 23 for this row.
This single additional possibility materially changes the first-row test.

## 2. Complete widened first row on the rational branch

Put `h=1+y^5`. The high Q rows still force `h^2|p11`. The expanded row is

    p11=y^8*h^2*a(y), deg(a)<=5.

On `z^2=y+y^6`, the forced differential is proportional to
`a(y)dy/(y*z^3)`. Its odd rational primitive must be `B(y)/z`, with

    B=b_(-1)/y+b0+b1*y+b2*y^2+b3*y^3.

The extra pole at y=0 explains the new Laurent term. There are no other
allowed poles, and the infinity bound gives the displayed upper degree.
Exactness is equivalent to

    y*(2(y+y^6)B'-(1+6y^5)B)=2a.

Solving the entire linear identity and imposing original descent at y=-1
gives

\[
\boxed{p_{11}=\mu y^8h^2(3+5y^4+8y^5).} \tag{2}
\]

A primitive is `2mu*(y^3-1/y)/z`. The first shifted terminal cancellation
identifies

\[
\eta=-\mu/12. \tag{3}
\]

Thus mu=0 recovers the previously studied chart. A nonzero mu can be
normalized by the original diagonal scaling, but cannot simply be omitted.
The nonzero polynomial row in (2) descends to the original rectangle
exactly; the script checks this by substitution.

## 3. The next rational row survives with one additional scalar

Define

\[
\begin{aligned}
E_1&=3+5y^4+8y^5,\\
E_2&=3+5y^2+8y^5,\\
R&=12+5y^3+60y^4+79y^5+30y^8+110y^9+92y^{10}.
\end{aligned}
\]

The next global forcing coefficient is proportional to

    (13*p11^2-24*c^3*p10)dy/w^25, w^4=c.

Set `u=1/y`, `V=w/y^2`, `D=1+u^5`. Its primitive has the form
`B(u)/V^9`, with `deg B<=13`. All finite and infinite pole bounds are
included. The complete linear equation is

    4D B'-45u^4 B = 4N,
    N=24u^24*p10(1/u)-13mu^2*u^12*D*E1(1/u)^2.

Polynomiality of the high Q rows first requires `h|p10`. At a simple root
of h, write `p11=c^2*u0+...`, `p10=c*v0+...`, `p9=w0+...`. The local
leading cubic and quartic must commute. Their coprime exponents force

    v0=u0^2/3, w0=u0^3/27.

Equivalently the next-row conditions include

    p10 = p11^2/(3c^3) modulo h^2,
    p9  = p11^3/(27c^6) modulo h.

For clarity, the perfect-cube conclusion is obtained from the actual
local leading polynomials: if they are `x^9 A(cx)` and `x^12 B(cx)`, with
monic degrees three and four in the argument, commutation yields
`3AB'-4A'B=0`, hence `B^3=A^4` and `A` is a cube of a linear polynomial.
This does not assume a global common cube root for P.

Adding the plane-descent constraints and the second shifted terminal
coefficient to the global linear identity gives

\[
\boxed{p_{10}=\frac{\mu^2}{3}y^7hR+
\tau y^8h^2E_2.} \tag{4}
\]

Both mu and tau survive. In particular `[y^7]p10=4mu^2`. Setting mu=0
recovers Astra 12's displayed p10 family. The exploratory calculation first
had nine free parameters; the local cube congruence reduces it to the one
additional tau in (4). These are complete necessary classifications of
the stated first two rows, not full polynomial pairs.

## 4. The four algebraic leading solutions were also attacked

Let A satisfy

    3A^4+60A^3+394A^2+620A+475=0.

Write `h(T)=(T-1)^3(T-r)^3(T-s)` using the exact r,s from the review, and
put

    beta=r-1, gamma=s-1,
    F=y(y-beta), G=(y+1)(y-gamma), D=FG, c=F^3G.

Both marked triple roots must satisfy the widened chart constraints.
The first row therefore has the form

    p11=mu*F^8*G^2*a(y), deg a<=3, a(-1)=0.

On the quadratic subfield `z^2=D`, its primitive is `C/(Fz)`, `deg C<=4`.
The full identity is

    2FG C'-(3F'G+FG')C=2a.

Over the exact quartic number field, its solution space with the descent
constraint is one-dimensional. Its generator is recorded in
`two_roots_output.txt` and recomputed by `explore_two_roots.py`.

For mu=1, retain

    p10=F^7 G*(a^2/3+G*b(y)), deg b<=5.

The next exactness condition has primitive `B/(D w)`, `deg B<=6`, and is

    4FG B'-(7F'G+5FG')B=4(5a^2-24G b).

The original-plane and two terminal constraints impose

    b(-1)=0,
    b(0)=a(0)^2/(9G(0)),
    b(beta)=a(beta)^2/(9G(beta)).

This exact affine problem also survives with one free parameter. The script
checks a particular primitive by substituting it into the full identity.
It works over the quartic field, so the result carries to its embeddings.
This does not solve the lower equations or demonstrate a Keller extension.

## 5. Coupling p9 and p8 on the shifted rational branch

Normalize mu=1 and keep tau arbitrary. Put `a=E1`, `d=R/3+tau*y*h*E2`,
and write

    p9=y^6*f, f=a^3/27+h*e, deg e<=12,
    p8=y^5*k, deg k<=18.

Descent and the next shifted terminal coefficients require

    e(-1)=e'(-1)=k(-1)=k'(-1)=0,
    e(0)=19/9, k(0)=14/9.

The inverse expansion at drop four gives the forcing numerator

    N= -h*k/4 +11*a*f/48 +11*d^2/96
       -253*a^2*d/1152 +8855*a^4/165888.

The differential is `N dy/(y*h^3*w)`. A complete allowed primitive has
the form `B/(h^2*w)`, `deg B<=18`, so the exact linear identity is

    4y*h*B'-(3h+9y*h')B=4N.

This system has a 21-dimensional affine solution for every tau. The script
`coupled_rational.py` retains the entire affine parameterization and verifies
all its equations symbolically; its certificate records the parameterization
and a particular section. This is global rational exactness on the complete
auxiliary curve, not a local conductor jet. It remains a necessary condition
on an unfinished finite pair.

## 6. A genuine rejection, followed by retained alternatives

The easiest particular section of that 21-parameter space fails the next
polynomiality gate for every complex tau. The rejection is exact and has
a saved Bezout identity; it is not a numerical residual or a timeout.

Here is the next gate. Write

    b=(d-a^2/3)/h.

At a simple zero of h the relevant Q row is q9. Expanding the fractional
power around the local common cube gives the necessary condition

\[
\boxed{(e-2ab/3)(k-ae/3+a^2b/9)=0\pmod h.} \tag{5}
\]

One direct derivation uses a temporary formal variable z. The local P series
has the form

    (1+a*z/3)^3+h*(b*z^2+e*z^3+k*z^4)+O(h^2).

The coefficient at z^7 in its 4/3 power, at order h^2, is
`4/9*(e-2ab/3)*(k-ae/3+a^2b/9)`. The still-unknown next P row contributes
at order h^2 but cannot reach z^7 in its linear contribution. Higher rows
contribute only at regular orders. Thus they cannot cancel this q9 pole.
This is a constraint on the retained p9,p8 data, independent of setting
lower rows to zero.

Substituting the convenient particular section gives coefficient polynomials
in tau whose gcd is one. The saved multipliers combine them to one, and
`check_next_local_gate.py` verifies that identity. This excludes only that
particular section, not the 21-parameter family.

Keeping the parameters instead gives the following exact surviving slices:

| Imposed local condition | Free dimension at fixed tau | Result |
|---|---:|---|
| First factor in (5) vanishes modulo h | 17 | Survives for all tau |
| Second factor in (5) vanishes modulo h | 17 | Survives for all tau |
| Both factors vanish modulo h | 13 | Survives for all tau |

`retain_local_branches.py` saves the affine parameterizations and checks a
particular from each against both the global primitive identity and (5).
These uniform choices do not exhaust assignments that choose different
factors at different roots of h. Those mixed cases remain unclassified.

## 7. Exact stopping point and the counterexample requirement

The work has produced no finite P,Q, no original constant-Jacobian identity,
and no collision witness. The retained objects are row families and exact
necessary compatibility conditions. They must not be called candidate
counterexamples, full irreducible components, or a five-component reduction
of general JC2.

The full construction still requires all original rectangle coefficients,
the shifted terminal conditions, every coefficient of `J(P,Q)=kappa*x^2`,
original polynomial descent, and kappa nonzero. Negative Laurent rows are
essential. Indeed, if all Laurent rows are nonnegative, original descent
forces both original polynomials to be constant on X=0, contradicting a
nonzero constant Jacobian there.

In original coordinates, writing

    P=sum X^i A_i(Y), Q=sum X^i B_i(Y),

the bottom boundary already requires

    A1 B0' - A0' B1 = kappa.

Neither this boundary system nor the remaining lower bracket rows has been
solved here. The next construction must connect them to the retained upper
families and keep all mixed local choices in (5). The present calculations
do not justify discarding any of the five remaining leading solutions.

This run therefore found another consequential omitted case and advanced
its exact constraints. It did not achieve the user's counterexample target.

## 8. Reproduction

Run, from the repository root:

    python astra13/verify_review.py
    python astra13/verify_shifted_rows.py
    python astra13/explore_shifted_rational.py
    python astra13/explore_two_roots.py
    python astra13/coupled_rational.py
    python astra13/check_next_local_gate.py
    python astra13/retain_local_branches.py

The last three regenerate their JSON certificates. The exploratory scripts'
full printed outputs are saved separately. SymPy exact rational and number-
field arithmetic was used; no numerical search or modular promotion supplies
any conclusion in this report. The inherited Astra 12 verifier had also
passed in the preceding review; its scoped identities remain intact.

The scripts verify exact algebra, including full affine substitutions where
claimed. Pole-space completeness, chart coverage and use of published corner
results are written arguments, not independently formalized geometry.
