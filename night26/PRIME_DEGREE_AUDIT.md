# Prime-degree audit

## Verdict

The 2024 claim that a planar Keller map cannot have prime function-field
degree is **not proved by its published argument**.  Its `xy not in k(p,q)`
case contains a fatal citation error.  This does not reopen degrees 3 or 5:
older independent theorems exclude all topological degrees at most 5.  For a
generically finite complex polynomial map, that sheet number is the function
field degree.  The first surviving degree is therefore **6**.

## Audit of Moskowicz

Source: Vered Moskowicz, *The two-dimensional Jacobian conjecture and
Galois extensions*, [arXiv:2407.13795v1](https://arxiv.org/html/2407.13795v1),
especially Theorems 3.2 and 3.3.

Theorem 3.2 treats `xy not in k(p,q)`.  It obtains what the paper calls the
"rare property" and then invokes its reference `[24, Answer 2.21]` to conclude
that `[k(x,y):k(p,q)]=2`.  But the cited
[MathOverflow answer](https://mathoverflow.net/questions/472877/a-subfield-r-subseteq-mathbbcx-y-with-many-generators-w-rw-math)
does not prove that implication.  It starts with an already quadratic
extension and constructs generators having the rare property.  This is an
existence example, not a classification of all extensions with that property.
The implication used in Theorem 3.2 is thus absent from the cited source, and
the complementary case of the claimed prime-degree theorem is unsupported.

Theorem 3.3 treats `xy in k(p,q)`.  Its printed Step 2 also appears to reuse a
constant selected against common zeros of `p,q` after replacing `p` by `p-c`.
That presentation gap is repairable: choose a nonzero line `y=mu` outside the
finite exceptional set.  From `xy=H(p,q)`, restriction gives
`mu*x=H(p(x,mu),q(x,mu))`, hence `k[x]=k[p(x,mu),q(x,mu)]`; the restriction is
injective and Gwozdziewicz's line-injectivity theorem applies.  Consequently
this special subcase is sound, but it does not repair Theorem 3.2.

**Applicable conclusion:** the Moskowicz paper does not rigorously kill a
faithful cubic primitive realization unless it also satisfies the special
`xy in k(P,Q)` hypothesis.  No further cubic construction is nevertheless
justified, because stronger older degree-specific results apply without that
hypothesis.

## Independent low-degree gate

The primary theorem used for the operational gate is H. Żołądek,
*An application of Newton–Puiseux charts to the Jacobian problem*, Topology 47
(2008), [DOI 10.1016/j.top.2008.04.001](https://doi.org/10.1016/j.top.2008.04.001):
the two-dimensional Jacobian conjecture holds for maps of topological degree
at most 5.  This includes the earlier degree-3 and degree-4 results:

- S. Yu. Orevkov, *On three-sheeted polynomial mappings of C2*, English
  bibliographic record and abstract at
  [MathDoc](https://geodesic.mathdoc.fr/item/IM2_1987_29_3_a4/).
- A. V. Domrina, *On four-sheeted polynomial mappings C2. II. The general
  case*, [Math-Net](https://www.mathnet.ru/eng/im273).

The current lower bound is also recorded in A. Borisov's survey,
*A geometric approach to the two-dimensional Jacobian Conjecture*,
[arXiv:1901.04073v2](https://arxiv.org/html/1901.04073v2).

Over `C`, a dominant polynomial map is generically finite and the number of
points in a generic fibre (counted away from the branch locus) equals
`[C(x,y):C(P,Q)]`.  Therefore the cited topological-degree theorem excludes
function-field degrees 3, 4, and 5.  NIGHT25 already excluded degree 2 by the
quadratic/Galois Keller theorem.  Degree 6 is the smallest surviving target.

## Dependency ledger

| claim | status | dependency |
|---|---|---|
| every prime field degree is impossible | **not established** | Moskowicz Theorem 3.2 has the citation gap above |
| prime degree with `xy in k(P,Q)` is impossible | established | repaired restriction-to-a-line argument + Gwozdziewicz |
| degree 3 is impossible | established | Orevkov; also Żołądek degree `<=5` |
| degree 4 is impossible | established | Domrina; also Żołądek degree `<=5` |
| degree 5 is impossible | established | Żołądek degree `<=5` |
| degree 6 is excluded by these sources | **no** | outside every theorem above |

