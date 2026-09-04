# Astra 2: exact descent for GGHV case (2)

Date: 2026-09-04. Base: `93319412545e84d1093d79c5b59cb87731eec4a9`.

**Result: case (2) of GGHV Proposition 4.3 is excluded in characteristic
zero**, by a mathematical completeness argument and independently replayed
exact algebra. No counterexample or counterexample candidate was found.
This does not exclude the other polygon in that proposition, the entire
original degree-(72,108) target, or the planar Jacobian conjecture.
No claim of priority relative to the mathematical literature is made.

## 1. Exact target and equations

The source is Guccione, Guccione, Horruitiner and Valqui,
[arXiv:2204.14178, Proposition 4.3(2)](https://arxiv.org/pdf/2204.14178).
Its required Newton polygons are

```
N(P) = conv{(0,0),(1,0),(8,14),(8,16)},
N(Q) = conv{(0,0),(2,1),(12,21),(12,24)},
{P,Q} = x^2.
```

Put `T=xy^2`. The complete lattice supports give

```
P = A(T) + B(T)/y + C(T)/y^2,
Q = D(T) + E(T)/y + F(T)/y^2 + G(T)/y^3.
```

Here `deg(A,B,C)<=8`, `deg(D,E,F,G)<=12`; `B,C,E` are divisible
by T, and `F,G` by T^2. Additive constants in A,D have no effect.
In particular, a T term in F is forbidden: it would be the monomial x
outside the polygon of Q. The corners require `C_1 C_8 A_8 G_12 D_12 != 0`.
Only the necessary conditions `C_1 C_8 G_12 A_8 != 0` are used below.

With primes denoting T derivatives, the bracket is equivalent to

```
(5)  2 C G' - 3 C' G = T^2,
(4)  2 C F' - 2 C' F + B G' - 3 B' G = 0,
(3)  2 C E' - C' E + B F' - 2 B' F - 3 A' G = 0,
(2)  2 C D' + B E' - B' E - 2 A' F = 0,
(1)  B D' - A' E = 0.
```

The general identity is
`{y^-r f(T), y^-s g(T)} = y^(1-r-s)(r f g' - s f' g)`.
Multiplying P,Q by inverse constants normalizes `C_1=G_2=1`.
The transformation
`P_lambda(x,y)=P(lambda*x,y)/lambda`,
`Q_lambda(x,y)=Q(lambda*x,y)/lambda^2`
preserves the bracket and all supports. It sends
`C(T)` to `C(lambda*T)/lambda`, hence `C_2` to `lambda*C_2`.

## 2. Completeness of the leading equation: exactly five scaling orbits

This proof supplies the completeness missing from a mere substitution into a
modularly reconstructed basis. Work over C first.

Let C,G satisfy (5), with degrees 8,12 and `C_1=G_2=1`.
Their only common root is zero; every other root of either polynomial is
simple. This follows by evaluating (5) at a nonzero root.
Write `C=T U`, `G=T^2 V`, where U,V have degrees 7,10 and constant term 1.
Set `kappa=G_12^2/C_8^3` and `W=G^2-kappa*C^3`.

The top terms of W cancel, and

```
C W' - 3 C' W = T^2 G.
```

If `deg W=d<24`, the left side has degree `d+7`, with nonzero
leading coefficient `(d-24) C_8 W_d`. Thus `deg W=7`.
Also `W=T^3 H`, where `deg H=4` and `H(0)=-kappa`.
The rational function

```
R = G^2/(kappa*C^3) = T*V^2/(kappa*U^3)
```

has degree 21 and derivative `R'=V/(kappa*U^4)`. Its ramification partitions
are therefore

| value of R | partition | distinguished point |
|---|---|---|
| 0 | `2^10,1` | the unique simple zero is T=0 |
| infinity | `3^7` | seven distinct poles |
| 1 | `17,1^4` | the unique point of index 17 is T=infinity |

For the last row, `R-1=H/(kappa*U^3)` has order 17 at infinity.
Its finite zeros are simple because R' cannot vanish there.
Thus R is a Belyi map. Apply the dessin correspondence to `1/(1-R)`:
black vertices have degrees `3^7`, white vertices `2^10,1`, and faces
degrees `17,1^4`. The needed correspondence and uniqueness are the
Riemann existence theorem; see Pakovich and Zvonkin,
[Theorem 2.3](https://arxiv.org/html/1509.07973v2#S2.SS2).

Here is an exhaustive count of these dessins. Suppress the ten white vertices
of degree two. This leaves seven trivalent black vertices joined by ten edges,
plus one stem ending at the unique white leaf. Each degree-one face comes
from a loop at a black vertex: in permutation terms, a fixed point of the
face permutation pairs two darts at the same trivalent vertex. A white fixed
point cannot produce such a face. The four loops occupy distinct vertices,
since a trivalent vertex cannot carry two loops.

Removing those four loops leaves a connected graph on seven black vertices
with six edges, hence a tree, together with the root stem. Its four former
loop vertices are leaves. Its other three vertices are internal vertices of
a full binary tree rooted at the stem. The orientation of the sphere orders
the two children at each internal vertex. Conversely, adding one loop at
each leaf recovers the original dessin, uniquely up to oriented isomorphism.
There are exactly `Catalan(3)=5` such rooted plane binary trees.

Consequently there are at most five leading solutions modulo T scaling.
An isomorphism of the rational maps must preserve the distinguished points
0 and infinity, so its coordinate change is exactly `T -> lambda*T`.
The rational map determines C,G under `C_1=G_2=1`: recover their nonzero
roots from its poles and double zeros, respectively, then use the constant
terms of U,V. No additional polynomial solutions are hidden by this map.

The saved file `astra/artifacts/case2_exact_modular_lex.txt` explicitly
constructs five solutions with `C_2=1`: `a=C_8` satisfies the first polynomial
h of degree five, and each `C_3,...,C_7` is a rational polynomial in a.
The independent checker proves that h is irreducible, verifies the complete
identity (5), and verifies `C_8 G_12 != 0` in `Q[a]/(h)`.
The five embeddings give distinct `C_8`, so distinct normalized solutions.
Two cannot be related by scaling, because both have `C_2=1`.

Five constructed orbits meet the upper bound of five. This proves
completeness, including the absence of a `C_2=0` orbit, without trusting
the enumeration completeness of `modStd`. The other chart `C_1=C_8=1`
therefore has exactly 35 geometric solutions: seven choices of scale for
each of the five orbits.

`astra/case2_dessin_count.py` enumerates the five trees, constructs their
permutations, and checks the passports, connectedness, genus zero and pairwise
inequivalence. The reduction of all admissible dessins to those trees is the
written argument above, not a claim made by that finite computation.

## 3. A complete two-parameter solution of level (4)

For every leading solution, all B,F in the specified degree and divisibility
windows are

```
B = b0*(C' - C/T) + b1*(T*C' - 3*C/2),
F = b0*(G' - 3*G/(2*T) - C/2) + b1*(T*G' - 9*G/4).
```

To prove completeness, put `S=2CF-3BG`. Equations (4),(5) give
`C S'-2C'S=-2T^2 B`. Divisibility gives `S=T^2 v` for a polynomial
v with `v(0)=0`, and hence

```
B = v C' - (v/T + v'/2) C.
```

For `deg v=k>1`, the leading term of B has degree `k+7` and coefficient
proportional to `7-k/2`. The only possible exception is k=14.
The polynomial `(C/T)^2` lies in the kernel of this operator and has degree
14. Subtract its appropriate scalar multiple to cancel a resonant term.
The remaining polynomial must have degree at most one. Thus
`v=b0+b1*T+lambda*(C/T)^2`; the condition `v(0)=0` gives `lambda=-b0`.
Substitution into S and use of (5) yield exactly the displayed B,F.
Their required divisibility holds, including cancellation of the T term of F.

## 4. Exact lower contradiction and independent verification

Work in the field `K=Q[a]/(h)`. In (3), coefficients `E_j`, j=1,...,12,
are solved successively with nonzero pivots `2j-1`. The residual coefficients
form seven equations, linear in `A_1,...,A_8`, with terms quadratic in b0,b1.
The saved six-element basis expresses `A_1,...,A_6` in terms of
`A_7,A_8,b0,b1`. The independent checker verifies the substitution in every
coefficient of (3), and computes matrix rank six over K. Hence this
parametrization covers every solution of (3), for every b0,b1.

Equation (2) similarly determines `D_j` with pivots `2j`.
Its remaining coefficients, together with (1), give 25 polynomials
`p_1,...,p_25` in `K[A_7,A_8,b0,b1]`. A necessary corner is `A_8 != 0`.
Adjoin z and `p_26=z*A_8-1`.

The 26 explicit multipliers in
`astra/artifacts/case2_exact_bottom_certificate.txt` satisfy

```
sum(q_i * p_i, i=1,...,26) = 1  in K[A_7,A_8,b0,b1,z].
```

The producer uses Singular. The verifier uses FLINT through a separate
restricted arithmetic parser; it does not invoke Singular. It independently
rebuilds all levels, checks the rank and parametrization, matches the bottom
generators up to invertible coefficient factors, and multiplies out the
certificate exactly. Altered-certificate controls are also checked.
In the stored Singular files `B(7),B(8)` mean `A_7,A_8`, not coefficients
of the polynomial B.

The identity survives each of the five embeddings of K into C. Therefore
none of the five leading orbits extends to a pair with `A_8 != 0`.
The completeness argument proves the claimed case exclusion over C.
The same exclusion holds in characteristic zero: a hypothetical finite tuple
of coefficients generates a finitely generated field over Q that embeds
into C.

## 5. Replay and evidence boundaries

From the repository root, with Python 3 and python-flint 0.9.0:

```
python astra/verify_case2_certificate.py
```

Expected four PASS lines: irreducible quintic and dessins; leading identity;
lower generation and rank; final Nullstellensatz identity. The JSON report
contains artifact SHA-256 hashes and the five dessin representatives.
The five inherited positive Poisson witnesses also pass independently:

```
python astra/graded_control.py
```

For a complete regeneration of the lower certificate (SymPy 1.14 and
Singular 4.3.1 were used):

```
python astra/build_case2_descent.py
Singular -q astra/case2_exact_descent_certificate.sing
python astra/verify_case2_certificate.py
```

`case2_exact_modular.sing` is the leading-solution discovery script, not a
required step in independent certificate verification. Its saved log predates
the final evidence review: `LEADING_EXACT_Q_COMPLETE` in that raw log is not
used as a proof of completeness. The dessin proof supplies that step.
Likewise historical `SECONDS` labels in exploratory logs denote Singular's
timer output; no wall-clock claim is based on them.

Direct leading standard-basis attempts in both normalizations timed out.
A direct `C_2=0,C_8=1` computation returned `[1]`, but lifting a certificate
for that auxiliary chart timed out. Neither that auxiliary result nor any
timeout is needed for the proof. One initial descent script had a Singular
algebraic-coefficient parser error; its failed log is retained and explicitly
excluded from evidence. See `case2_run_manifest.json` for run classifications.

The historical degree-1144 object is not asserted to be this saturated leading
scheme. Its full provenance remains unaudited. The present equations were
reconstructed directly from the published polygon; the five/35 count has its
own completeness proof and does not depend on identifying that old eliminant.

## 6. Next explicit target

The other polygon in Proposition 4.3 adds vertices `(0,8)` and `(0,12)`.
It permits negative grading levels, so the five-level descent above does not
cover it. Reconstruct its full support and bracket equations before deciding
whether any of the present leading or lower lemmas still apply.
The separate above-125 translation/provenance wall also remains open.
