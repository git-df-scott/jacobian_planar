# Generic residual-edge filter status

## Status

**NO VERDICT** on existence, for every degree pair.  This filter recognizes a
necessary leading-row shape only after a Newton-face certificate has been
supplied.  It has no `EMPTY` output.

## Independent audit

Work over an algebraically closed field of characteristic zero.  Fix one
Newton weight and one affine edge coordinate `t`.  The following are data, not
consequences of the two ordinary degrees:

1. The initial forms of `P` and `Q` lie on the same face and can be written in
   the chosen normalization with nonzero edge polynomials `A(t), B(t)` of
   exact degrees `m,n`.  Both required endpoints of that face are nonzero.
2. The Jacobian has strictly smaller weight than the bracket of those initial
   forms.  Only here may the leading bracket coefficient be set to zero,
   giving

       m A B' = n A' B.                               (1)

   This is a face statement; `deg(P)=m, deg(Q)=n` alone does not imply it.
3. Put `g=gcd(m,n)`, `a=m/g`, and `b=n/g`.  The primitive residual

       R = Q^a - lambda P^b

   cancels that same face, and the newly exposed initial form is nonzero, is
   on the expected next face, and has edge polynomial `H(t)` of exact degree
   `m-1` in the normalization used in (1).
4. On taking `{P,R}`, the right side lies **strictly below that next face**.
   Thus it contributes zero to the next face equation.  The endpoints used to
   identify the coefficient with the displayed differential equation must
   also remain nonzero.

Here is the algebra, with no appeal to a solver.  On the open set where `AB`
is nonzero, (1) gives `m B'/B=n A'/A`; integration in the rational function
field gives `B^m=cA^n`, with `c != 0`.  Polynomial factorization extends this
identity across the roots.  Equivalently, unique factorization gives a
degree-`g` polynomial `G` and nonzero constants `alpha,beta` such that

       A=alpha G^a,  B=beta G^b.                       (2)

Consequently `B^a` and `A^b` are constant multiples of the same polynomial
`G^(ab)`, so a nonzero `lambda` cancels the leading face of `Q^a` against that
of `P^b`.  Notice that `am=bn=mn/g`; this equality checks the residual's face
degree, but does not prove which face cancellation exposes next.

The Poisson calculation is an identity in the complete polynomials:

    {P,R} = a Q^(a-1){P,Q},                            (3)

because `{P,P^b}=0`.  (A normalization such as `{P,Q}=x^2` may be inserted
afterward; it is not part of (3).)  Assumptions 3 and 4 are used exactly once:
they say that the next-face coefficient on the right of (3) is zero, while
the left coefficient is

    (m-1) A'H - m A H' = 0.                           (4)

On `AH != 0`, (4) integrates to

    H^m=d A^(m-1),  d != 0.                           (5)

Again polynomial equality extends across roots.  At every root `rho`, (5)
implies `m ord_rho(H)=(m-1)ord_rho(A)`.  Coprimality of `m` and `m-1`, plus
`deg A=m`, forces exactly one root of multiplicity `m`:

    A=alpha(t-rho)^m,  B=beta(t-rho)^n.                (6)

The conclusion for `B` follows from (2) (or from root multiplicities and its
exact degree).  Equations (1)--(6) prove only a necessary condition.

## Excluded strata and risk ledger

| excluded case | why the generic step fails | disposition | counterexample risk |
| --- | --- | --- | --- |
| `H=0` | (5) cannot be divided/integrated with `d != 0`; the first surviving residual is later | **separate branch**; not ruled out by this theorem | **could still contain one** |
| nonzero `H` of degree `<m-1` | the coefficient and endpoint normalization used in (4) changes | **separate branch** | **could still contain one** |
| cancellation exposes a different Newton face | the expected next-face coefficient is not (4), or the Jacobian right side may meet it | **separate Newton-face branch** | **could still contain one** |
| a required endpoint coefficient vanishes | the advertised face shortens/rotates and “exact degree” or coefficient extraction is invalid | **separate support stratum** | **could still contain one** |
| right side of (3) meets the next face | (4) becomes inhomogeneous rather than zero | **separate Jacobian-visible branch** | **could still contain one** |

None of these cases is ruled out by the generic residual theorem or by the
degree pair.  A campaign-specific theorem may later discharge an individual
row, but that proof must be attached as separate evidence; the filter must
not silently inherit it.

## Practical filter and the 804-pair sweep

`generic_residual_filter.py` accepts a JSON list (or `{ "pairs": [...] }`).
Every record requires positive integers `m,n`; the program always computes
`gcd(m,n)` and primitive exponents `a,b`.  A bare record such as
`{"m":72,"n":108}` returns `NO VERDICT`, because no degree pair automatically
determines its residual face.  `PASS FILTER` is returned only when all nine
named booleans in `edge_certificate` are explicitly true.  Any explicitly
failed boolean is `SEPARATE STRATUM`; an incomplete certificate remains
`NO VERDICT`.

The repository currently documents the count 804 but does not contain the
804-pair dataset.  Therefore no reproducible per-pair table can honestly be
generated here.  When that list is restored, the safe automation path is:

1. Run the script on bare pairs to calculate `gcd,a,b`; all rows initially
   remain `NO VERDICT`.
2. Generate Newton faces for each candidate, retaining endpoint and weight
   metadata rather than only ordinary degrees.
3. Independently certify each of the nine face predicates.  Route every
   failed predicate to a named stratum queue.
4. For `PASS FILTER` rows, impose (6) as a parameter reduction in the next
   solver.  Do **not** remove the row from the search and do not label it empty.
5. Preserve the JSON certificate and solver result so the decision is
   auditable.  Never infer a missing boolean from `gcd`, divisibility, or a
   neighboring pair.

This is the “shaved nozzle” change: the filter is deliberately loosened at
the face boundary.  It sacrifices aggressive rejection so uncertain geometry
cannot seize the sweep by producing a false `EMPTY`.

## Positive controls

For `P=x+y^m`, `Q=y+P^k`, one has `{P,Q}=1` and degree pair `(m,km)`.
The three controls `(1,2)`, `(2,4)`, `(2,6)` have respectively
`(g,a,b)=(1,1,2),(2,1,2),(2,1,3)`.  Their leading rows are already full powers,
so complete face certificates return `PASS FILTER`; the maps remain
**NONEMPTY**.  This confirms that `PASS FILTER` means “satisfies the necessary
shape,” never “excluded.”

