# NIGHT23 — BRIANÇON DECISIVE PERIOD STRIKE

## Verdicts first

| target | exact verdict | certificate |
|---|---|---|
| \(g\) | **PERIOD-NONZERO** | on \(g=1\), \(\eta\) extends to a nonzero holomorphic differential on the compact genus-one fibre |
| \(g'\) | **PERIOD-NONZERO** | same exact certificate on \(g'=1\) |

These are `EXACT-ALL-DEGREES` obstructions.  Neither polynomial has a
polynomial Keller mate of any degree.  No mate construction or degree sweep is
therefore triggered, and no counterexample is claimed.

## 1. Exact finite de Rham certificate

Put

\[
s=xy+1,\qquad p=xs+1,\qquad u=s^2+y.
\]

The exact identities

\[
(p-1)u=s(sp-1),\qquad
\frac{\partial(s,p)}{\partial(x,y)}=-(p-1)
\tag{1}
\]

are re-expanded coefficientwise by both checkers.  On the fibre \(P=t\),
clear the denominator in the birational \((s,p)\)-model.  For \(t=1\) the
two integral equations are

\[
\begin{aligned}
H_g&=3s^2p^3-8sp^2+4sp+s-3p+3,\\
H_{g'}&=9s^2p^3-16sp^2+8sp-s-9p+9.
\end{aligned}\tag{2}
\]

In each case \(H=k(p-1)(P-1)\), with \(k=3,9\), respectively.  Equations
(1)--(2) give, in the common function field,

\[
\eta=k\frac{ds}{H_p}=-k\frac{dp}{H_s}.\tag{3}
\]

Thus deciding the class of \(\eta\) reduces to its valuations on the
normalisation of the compactified curve (2).

### The two branches at \(p=\infty\)

Set \(q=1/p\) and multiply (2) by \(q^3\).  If

\[
H=ks^2p^3-Asp^2+Bsp+Cs-kp+k,
\]

the degree-two initial form at \((s,q)=(0,0)\) is

\[
ks^2-Asq-kq^2.\tag{4}
\]

Its discriminants are \(100\) and \(580\), so it has two distinct tangent
branches \(s=\lambda q+O(q^2)\).  The tangent polynomial

\[
k\lambda^2-A\lambda-k
\]

is coprime over \(\mathbb Q\) to both \(\lambda\) and
\(-A\lambda-2k\).  Substitution in (3) therefore gives

\[
\nu(\eta)=0
\]

on each of the two branches.  This is an exact gcd calculation, not a
floating-point Puiseux approximation.

### The branch at \(s=\infty\)

Set \(z=1/s\) and multiply (2) by \(z^2\).  The weighted initial form, for
\(\operatorname{wt}(p)=1,\operatorname{wt}(z)=3\), is

\[
kp^3+Cz.\tag{5}
\]

Since \(kC\ne0\), there is one smooth branch

\[
z=-\frac{k}{C}p^3+O(p^4).
\]

Equation (3) gives \(\nu(\eta)=0\), with leading coefficient \(k/C\).
The two finite inverse-base points \((s,p)=(0,1),(1,1)\) are checked
separately; their expansions give finite \((x,y)=(-1,1),(0,2)\), so no hidden
puncture was omitted.

### Binding conclusion

The cited geometry gives genus one for the compactification of the fibre at
\(t=1\).  The form is regular on the affine curve by gradient unimodularity,
and (4)--(5) show it is regular at all three missing places.  It is not zero:
on the affine fibre it evaluates to one on the Hamiltonian vector field.
Hence

\[
0\ne\eta\in H^0(\bar F_1,\Omega^1_{\bar F_1}).
\]

A nonzero holomorphic differential on a compact genus-one curve cannot be
exact.  Indeed, if \(\eta=dR\), then a pole of \(R\) would create a pole of
\(dR\); hence \(R\) is globally regular, therefore constant.  Equivalently,
at least one period of \(\eta\) is nonzero.  The single exact fibre witness
\(t=1\) disproves the required all-fibre period vanishing for both targets.

The geometric inputs are precisely [Dimca--Sticlaru, Theorem 1.7 and
Propositions 3.3--3.4](https://arxiv.org/pdf/2406.19795): all fibres are smooth
and irreducible, the maps are non-coordinate, and the projective closures of
the two \(t=1\) fibres have genus one.  The paper states, in particular, “All
the fibers ... are irreducible affine plane curves” and
“\(g(C_1)=1\).”

## 2. Why the Briançon family fails

Consider the natural two-parameter family

\[
P_{a,b}=p^2u+a\,ps+b\,s.
\]

Its cleared generic fibre is

\[
H_{a,b}=s^2p^3+(a-1)sp^2+(b-a)sp-bs-tp+t.\tag{6}
\]

On the locus \(b\ne0\), the same two boundary calculations apply: the
\(s=\infty\) initial form is \(p^3-bz\), and the \(p=\infty\) initial form
has two distinct branches over \(\mathbb C(t)\).  Consequently every
submersion in this family retaining the all-irreducible genus-one profile has
the same nonzero holomorphic period obstruction.

The only boundary degeneration inside (6) is \(b=0\).  But there

\[
P_{a,0}=p(pu+as),\tag{7}
\]

so the zero fibre is reducible.  Thus the exact degeneration locus leaves the
all-fibres-irreducible class before it can become a period-zero target.

This is not merely caused by critical points.  At \((a,b)=(-1,0)\), the
checker finds and re-expands an exact degree-seven Bezout identity

\[
U(P_{-1,0})_x+V(P_{-1,0})_y=1,
\]

and the Shpilrain--Yu reduction returns `NON_COORDINATE` in one leaf.  Yet
(7) still supplies the reducible zero fibre.  It is an exact adversarial
control for the family boundary.

There is also an exact local near-hit at \((a,b)=(0,0)\).  In the
\(s=\infty\) chart its initial equation becomes

\[
p^3+t z^2,
\]

which has one cusp branch.  At \(t=1\), over
\(\mathbb Q(\alpha),\alpha^2=-1\), an exact expansion is

\[
p=r^2,\qquad
z=r^3\left(\alpha+\frac12r+\frac{3\alpha}{8}r^2+\cdots\right).
\]

Substitution gives \(\nu(\eta)=-2\), and the coefficient of
\(r^{-1}dr\) cancels exactly, so the residue is zero.  This is precisely the
local second-kind profile required below.  Its fatal global defect is equally
exact: \(P_{0,0}=p^2u\).  Thus the next construction problem is concrete:
retain the cusp model \(p^3+t z^2\) while breaking the common \(p\)-factor and
preserving unimodularity and all-fibre irreducibility.

## 3. General obstruction and next address

The calculation isolates a broader exact obstruction.  If a
gradient-unimodular polynomial has compact generic genus \(g\ge1\) and

\[
\nu_{v_i}(\eta)\ge0
\quad\text{at every infinity place }v_i,\tag{8}
\]

then \(\eta\) is a nonzero global holomorphic differential and its period
class is nonzero.  Therefore any period-zero positive-genus target must have
at least one pole at infinity.  More sharply, an exact nonzero differential
\(dR\) has zero residues and pole order at least two, so a surviving target
must satisfy

\[
\operatorname{Res}_{v_i}(\eta)=0\ \forall i,
\qquad \min_i\nu_{v_i}(\eta)\le-2.\tag{9}
\]

The strongest next address is consequently not another point in (6).  It is
an all-fibres-irreducible, unimodular, non-coordinate \((1,3)\) embedding on a
different boundary Newton stratum satisfying (9).  The remaining global
condition is that the second-kind differential's elliptic de Rham component
also vanish.  That is the next exact obstruction; residues alone are not
sufficient.

## 4. Adversarial audit

1. **All-fibre irreducibility and non-coordinate status:** used only for the
   two published Briançon targets, under Theorem 1.7's exact hypotheses.
2. **Period calculation:** performed on the exact fibre \(t=1\); no numerical
   integration, modular arithmetic, or sampled-zero inference occurs.
3. **All-period implication:** only the necessary direction is used.  One
   nonzero period rules out every polynomial mate.
4. **Descent and polynomialization:** not invoked, because neither target
   reaches the mate gate.
5. **Degree-30 paradox:** disappears.  The new obstruction is all-degrees and
   explains the four bounded EMPTY systems without predicting a first mate
   degree.
6. **Counterexample gate:** no \(Q\) is produced, so bracket and
   noninvertibility claims are not made.

## Final campaign fields

- `CE: NO`
- `CEC: NO`
- strongest surviving target: an all-irreducible unimodular non-coordinate
  \((1,3)\) polynomial retaining the local cusp \(p^3+t z^2\) (hence (9))
  while breaking the common \(p\)-factor of \(P_{0,0}\)
- exact next obstruction: kill the elliptic de Rham component of a
  residue-free second-kind Gelfand--Leray differential
