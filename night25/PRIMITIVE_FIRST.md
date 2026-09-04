# NIGHT25 — PRIMITIVE-FIRST JC2 STRIKE

## Verdict first

The two requested minimal genus-one primitive models are both
`IMPOSSIBLE` as faithful polynomial Keller realizations.  The obstruction is
not ansatz-specific.

If a polynomial Keller pair \((P,Q)\) faithfully realizes \((C_t,R)\), then

\[
[\mathbb C(x,y):\mathbb C(P,Q)]=\deg(R:C_t\to\mathbb P^1). \tag{1}
\]

Both \((R)_\infty=2O\) and \((R)_\infty=O_1+O_2\) have degree two.  Thus
either realization would give a quadratic function-field extension.  In
characteristic zero it is Galois.  The classical Galois case of the Jacobian
Conjecture says that a Keller map with Galois function-field extension is a
polynomial automorphism.  This is Bass--Connell--Wright, Theorem 2.1,
implication (g) => (a), independently due to Razar and Wright:
[DOI 10.1090/S0273-0979-1982-15032-7](https://doi.org/10.1090/S0273-0979-1982-15032-7).
An automorphism has coordinate first component and rational generic fibre,
contradicting the genus-one hypothesis.

Consequently the primitive-first search cannot possibly start at primitive
degree two.  Its minimal live degree is three, where non-Galois monodromy is
possible.

No counterexample or counterexample candidate was found.

## 1. Why degree of the primitive is the generic map degree

Put

\[
L=\mathbb C(x,y),\qquad K=\mathbb C(P,Q).
\]

Over the generic value \(t\) of \(P\), the function field of the generic
fibre is \(\mathbb C(t)(C_t)=\mathbb C(P)(x,y)\).  Restriction of \(Q\) is
the function \(R\).  Therefore

\[
\deg R=[\mathbb C(P)(x,y):\mathbb C(P)(Q)]=[L:K]. \tag{2}
\]

This also identifies a hidden failure mode in inverse constructions: a
symplectic quotient may make \(t,R\) polynomial while discarding a finite
cover of the intended curve.  Such a quotient does not faithfully realize
\(C_t\).

## 2. Model A: one double pole

Work over \(K_0=\mathbb Q(t)\) with

\[
C_t:\quad v^2=u^3+u+t,\qquad R=u. \tag{3}
\]

The cubic discriminant is

\[
-4-27t^2\ne0,
\]

so the generic curve is smooth of genus one.  It has one point \(O\) at
infinity and

\[
(R)_\infty=2O. \tag{4}
\]

The exact differential is \(dR=du\).  The curve relation gives the exact
identity

\[
2v\,dv=(3u^2+1)\,du. \tag{5}
\]

If \(B_1,B_2,B_3\) are the three points \(v=0\), then

\[
(du)=B_1+B_2+B_3-3O. \tag{6}
\]

Thus the required differential pole pattern is exactly \(3O\).  For any
Keller affine open, the three zeros of \(du\) must also be punctures: on a
smooth affine Keller fibre, \(dQ\) evaluated on the Hamiltonian tangent field
is the nonzero constant \([P,Q]\), so it cannot vanish.

The total surface is the \((u,v)\)-plane with

\[
t=v^2-u^3-u.
\]

There is an exact symplectic quotient

\[
X=u,\qquad Y=-v^2,
\]

for which

\[
dt\wedge dR=dX\wedge dY,
\qquad
P=-Y-X^3-X,\quad Q=X,\quad [P,Q]=1. \tag{7}
\]

This is an adversarial control, not a realization: it forgets the quadratic
extension \(v^2=-Y\).  The quotient pair is triangular and its fibres are
rational.  Any faithful realization retains the quadratic extension and is
impossible by (2) and the Galois-case theorem.

Verdict: `IMPOSSIBLE`.

## 3. Model B: two simple poles

Take

\[
C_t:\quad v^2=u^4+u+t,\qquad R=u. \tag{8}
\]

The quartic discriminant is

\[
256t^3-27\ne0,
\]

so the generic compactification is smooth of genus one.  It has two points
\(O_+,O_-\) over \(u=\infty\), and

\[
(R)_\infty=O_++O_-. \tag{9}
\]

Again \(dR=du\) exactly, with

\[
2v\,dv=(4u^3+1)\,du. \tag{10}
\]

Writing \(B_1,\ldots,B_4\) for the four points \(v=0\),

\[
(du)=B_1+B_2+B_3+B_4-2O_+-2O_-. \tag{11}
\]

The same quotient

\[
X=u,\qquad Y=-v^2
\]

gives

\[
P=-Y-X^4-X,quad Q=X,quad [P,Q]=1, \tag{12}
\]

but again destroys the quadratic cover and leaves a triangular coordinate
pair.  Every faithful realization has field degree two and is impossible by
the Galois-case theorem.

Verdict: `IMPOSSIBLE`.

## 4. Minimal live successor: degree-three primitive

Return to the cubic curve (3), but choose the primitive first as

\[
R=v. \tag{13}
\]

Then

\[
(R)_\infty=3O,
\qquad
(dR)=Z_1+Z_2+Z_3+Z_4-4O, \tag{14}
\]

where the four \(Z_i\) satisfy \(3u^2+1=0\) and the curve equation.  This is
exact by construction and has degree three.  Put

\[
X=-u^3-u,\qquad Y=v.
\]

Then

\[
dt\wedge dR=dX\wedge dY,
\qquad
P=X+Y^2,quad Q=Y,quad [P,Q]=1. \tag{15}
\]

Again the displayed pair is only the quotient and is triangular.  This time,
however, the discarded extension is the cubic

\[
u^3+u+X=0. \tag{16}
\]

It is irreducible over \(\mathbb Q(X,Y)\), and its discriminant

\[
-4-27X^2
\]

is not a square.  Hence its Galois closure has group \(S_3\).  The extension
is non-Galois, exactly as a live Keller counterexample extension must be.

The current normalization \(\mathbb A^2_{u,v}\to\mathbb A^2_{X,Y}\) is
ramified on \(3u^2+1=0\), reflected by

\[
[t,R]_{u,v}=-(3u^2+1), \tag{17}
\]

so it is not itself Keller.  The inverse realization problem is now precise:
find a polynomial-plane model \(\mathbb Q[x,y]\subset\mathbb Q(u,v)\)
containing \(t,R\), with full fraction field \(\mathbb Q(u,v)\), such that
the cubic ramification is moved entirely to infinity and
\(dt\wedge dR=dx\wedge dy\).

This is `UNKNOWN`, and is the strongest explicit \((C_t,R)\) produced here.

## 5. First inverse-realization ansatz is exactly dead

On the total \((u,v)\)-plane, consider the smallest fibre-adapted birational
chart

\[
x=f(u),\qquad y=a(u)v+b(u). \tag{18}
\]

For \(\mathbb Q(x,y)=\mathbb Q(u,v)\), generic degree forces
\(\deg f=1\).  Then \(u\) is polynomial in \(x\).  Requiring the primitive
\(R=v=(y-b(u))/a(u)\) to be polynomial in \(x,y\) forces \(a(u)\) to be a
nonzero constant.  But then

\[
\frac{\partial(x,y)}{\partial(u,v)}=f'(u)a(u)
\]

is constant and cannot equal the required \(-(3u^2+1)\).  The transposed
linear-in-\(v\) chart dies identically.  This is only a small ansatz closure;
it is not promoted into a closure of the cubic model.

## 6. Adversarial audit

- **Hidden genus drop:** excluded for (3), (8) by their nonzero generic
  discriminants.  The quotient pairs do drop genus and are explicitly marked
  nonfaithful.
- **Hidden coordinate form:** both quotient pairs are explicitly triangular;
  none is called a candidate.
- **Missing infinity branches:** Model A has one infinity point; Model B has
  two; Model C has one.  All zeros and poles of the displayed differentials
  are accounted for by degree-zero divisors.
- **Zero residue versus exactness:** exactness is literal: \(dR=du\) or
  \(dv\).
- **Polynomiality:** all displayed quotient \(P,Q\) are honest integer
  polynomials, but are controls only.
- **Extension-field descent:** all models and identities are over
  \(\mathbb Q(t)\); no descent claim is needed.
- **Truncation/modular artifacts:** none; both checkers use exact rational
  arithmetic.
- **Theorem hypotheses:** a hypothetical realization is extended from
  \(\mathbb Q\) to \(\mathbb C\); constant nonzero Jacobian gives a Keller
  map; degree two gives a separable normal extension; the Galois-case theorem
  applies.

## Final fields

- `CE: NO`
- `CEC: NO`
- `primitive-first Model A: IMPOSSIBLE`
- `primitive-first Model B: IMPOSSIBLE`
- `strongest explicit (C_t,R): v^2=u^3+u+t, R=v, (R)_infty=3O, (dR)_infty=4O`
- `strongest explicit P: NONE (faithful); P=X+Y^2 is a triangular quotient control`
- `mate status: exact on the curve; faithful polynomial-plane realization UNKNOWN for the cubic successor`
- `exact obstruction: primitive degree 2 => quadratic Galois Keller extension => automorphism => genus 0 contradiction`
- `next minimal construction: non-Galois degree-3 plane model moving the S3 cubic ramification entirely to infinity`
- `artifacts: night25/PRIMITIVE_FIRST.md, primitive_first25.py, primitive_first25.json, verify_primitive_first25.py`
- `verification commands: python3 night25/primitive_first25.py && python3 night25/verify_primitive_first25.py`
