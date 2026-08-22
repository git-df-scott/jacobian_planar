# The GGHV (72,108) system: what arXiv:2204.14178 actually hands us for the open case

**Source.** J.A. Guccione, J.J. Guccione, R. Horruitiner, C. Valqui, *Increasing the
degree of a possible counterexample to the Jacobian Conjecture from 100 to 108*,
arXiv:2204.14178v1 (29 Apr 2022). Referred to below as **GGHV22**. Section/theorem/line
numbers refer to the `pdftotext -layout` extraction of this PDF, cross-checked against
page images for the passages that matter most.

Companion papers consulted (all by the same authors, referenced as [1]–[6] inside
GGHV22, arXiv ids added):

| GGHV22 ref | Title | arXiv id |
|---|---|---|
| [1] | *On the shape of possible counterexamples to the Jacobian Conjecture* | 1401.1784 |
| [2] | *The Two-Dimensional Jacobian Conjecture and the Lower Side of the Newton Polygon* | 1605.09430 (not fetched — not needed below) |
| [3] | *A system of polynomial equations related to the Jacobian Conjecture* | 1406.0886 |
| [5] | *Some algorithms related to the Jacobian Conjecture* | 1708.07936 |
| [6] | *The Jacobian Conjecture: Approximate roots and intersection numbers* | 1708.09367 |

All PDFs and their `pdftotext -layout` extractions are saved under the scratchpad
(`.../scratchpad/pdfs/`), not in this repo, per instructions.

---

## 0. Bottom line

**The open system is NOT explicitly given in the paper, and it cannot be
reconstructed from the paper with the precision needed for a Groebner engine
without redoing original mathematical derivation the authors themselves did not
publish.**

What GGHV22 *does* give for the open case is a single proposition (**Proposition
4.3**, "Case (8,28)") pinning down the *shape* (Newton polygon) of a hypothetical
reduced pair and the value of its bracket ($[P,Q]=x^2$). That is one page of
combinatorial/valuation-theoretic reduction. For the sibling case that GGHV22
*does* close — "Case (9,27)" — the analogous shape-only proposition (**Proposition
4.1**) is followed by five more pages (Section 5: Proposition 5.2 → Proposition
5.4 → Proposition 5.5 → Proposition 5.6 → proof of Theorem 5.1) of a bespoke
"convert to a power series in an auxiliary variable, extract the fully-reduced
polynomial system, invoke a CAS on it, get a handful of equations that force a
contradiction" argument. **That five-page reduction has no analogue anywhere in
the paper for Case (8,28).** The paper's own words:

> "In section 5 we use the systems of polynomial equations associated to a
> possible counterexample as in [3] in order to discard the case $(\deg(P),
> \deg(Q)) = (66, 99)$ and one of the cases with $(\deg(P), \deg(Q)) = (72,
> 108)$. For the other case with $(\deg(P), \deg(Q)) = (72, 108)$ we couldn't
> solve the corresponding system of polynomial equations, thus it is left
> open." (Introduction, p.1–2)

I searched the full text of GGHV22 for every occurrence of "(8, 28)" (the label
of the open case — see §2 below); there are exactly two occurrences outside the
one-page Proposition 4.3 itself, both about an unrelated intermediate point
`A1 = (8,28)` used while discarding the *different* case max{deg P, deg Q}=120
in Section 3. **Nothing else in the paper touches the open case.** Section 5's
title is literally "Systems of polynomial equations for (9,24) and (9,27)" —
(8,28) is not in it.

So: I can, and below do, build one *unambiguous* thing directly from
Proposition 4.3's data — the "naive" coefficient-matching system implied
mechanically by "$P,Q$ have exactly this Newton polygon and $[P,Q]=x^2$". That
system is real, precisely specified, and Groebner-engine-ready (see §5, and
`jc2_gghv_system.py`). But it is **not** the small, tractable system the
authors mean when they say "the corresponding system of polynomial equations"
— by analogy with the closed sibling, their intended system would have on the
order of 10 unknowns after the same kind of series-substitution reduction used
in Section 5, not 72–186. Reproducing *that* reduction for the (8,28) shape is
new mathematics, not extraction, and I have not attempted it (see §6 for
exactly what is missing and why it is hard).

---

## 1. Theorem 2.1 and where the open case sits

> **Theorem 2.1.** If $(P,Q)$ is a counterexample to the Jacobian Conjecture,
> then we have either $\max\{\deg(P),\deg(Q)\} \ge 125$, or $(\deg(P),\deg(Q))
> \in \{(72,108),(108,72)\}$.

The proof works from a table of 10 "corner" cases (GGHV22 §2, reproduced from
[5]=1708.07936 §5–6), each labeled by a point $A_0$ (a Newton-polygon corner)
and a coprime pair $(m,n)$:

```
   A0       (m,n)   max{deg(P),deg(Q)}   Discarded?
 (4, 12)    (3,4)          64            [4 §3.5],[10],[7]        <- red/solved
 (4, 12)    (5,7)         112            [4 §3.5]                  <- red/solved
 (5, 20)    (2,3)          75            [3 §5], no detail in [10] <- red/solved
 (5, 20)    (3,2)          75            [3 §5], no detail in [10] <- red/solved
 (7, 21)    (2,3)          84            no detail in [10]
 (8, 24)    (2,3)          96            [5, Proposition 6.1]      <- red/solved
 (8, 28)   *(3,2)         108            -
 (8, 32)    (3,2)         120            -
 (9, 24)    (2,3)          99            no detail in [10]
 (9, 27)    (2,3)         108            -
```

(Table transcribed from GGHV22 p.3; "red" rows — confirmed against the page
image — are the ones the authors consider already solved by earlier
literature *before this paper*.) GGHV22 itself then closes, within this
paper: `max=84` and `max=120` in §3 (using [6] and a direct argument
respectively); `max=99` (row `(9,24)`) and one of the two `max=108` rows in
§5; and gives an independent second proof of `max=84` in §6.

Two different table rows both give `max{deg P, deg Q}=108`: `A0=(9,27)` and
`A0=(8,28)`. Both correspond to the *same* unordered degree pair
$\{72,108\}$ (GGHV22 explicitly: "there are two cases with $(\deg(P),\deg(Q))
= (72,108)$", Introduction). The intro sentence quoted in §0 tells us the
`(9,27)` row is the one solved in §5, and `(8,28)` is the one left open. This
is corroborated inside §4:

* **Proposition 4.1** is captioned **"Case (9,27)"**.
* **Proposition 4.3** is captioned **"Case (8,28)"**.
* Section 5's title is **"Systems of polynomial equations for (9,24) and
  (9,27)"** — `(8,28)` is absent from that title and from the section's
  content (verified by full-text search).

**This matches the task's description exactly**: the shape "around (9,27)" is
the *closed* one; the shape "around (8,28)" is the *open* one. Do not mix
these up — swapping them is the single easiest way to misreport this paper.

A secondary open notational point, not load-bearing for anything below: the
table lists the open row's pair as `*(3,2)` with an unexplained asterisk
(no footnote is present in the PDF). The companion algorithm paper
[5]=1708.07936 (§6, "chain of length 1" table) lists the same case as
`A0=(8,28)`, `A1=(11/4,7)`, `(m,n)=(3,2)`, `max=108`, without a star. I did
not find an explanation of the star's meaning in either paper; it does not
affect anything reconstructed below, which is derived from Proposition 4.3's
explicit Newton polygons, not from the table row.

---

## 2. Notation (self-contained, quoted from [1] = arXiv:1401.1784)

GGHV22 is not self-contained; it explicitly inherits notation from [1], [2],
[3], [5] ("Since this article continues the work in [1], [2], [3] and [5], we
will use the notations and conventions established in these articles",
Introduction). The definitions actually needed to state Proposition 4.3
precisely are all in [1]:

**Directions and valuations** ([1] Def. 1.1, §1, p.3–4):

> "We define the set of directions by $V := \{(\rho,\sigma)\in\mathbb Z^2 :
> \gcd(\rho,\sigma)=1\}$ ... For all $(\rho,\sigma)\in V$ and $(i/l,j)\in
> \frac1l\mathbb Z\times\mathbb Z$ we write $v_{\rho,\sigma}(i/l,j) :=
> \rho i/l+\sigma j$."

**Leading form, support, Newton polygon** ([1] Def. 1.2 and the paragraph
after, p.4):

> "Let $(\rho,\sigma)\in V$. For $P=\sum a_{i/l,j}x^{i/l}y^j \in L^{(l)}
> \setminus\{0\}$, we define: the support of $P$ as $\mathrm{Supp}(P):=\{(i/l,j)
> : a_{i/l,j}\neq0\}$; the $(\rho,\sigma)$-degree of $P$ as $v_{\rho,\sigma}(P)
> := \max\{v_{\rho,\sigma}(i/l,j) : a_{i/l,j}\neq 0\}$; the $(\rho,\sigma)$-leading
> term of $P$ as $\ell_{\rho,\sigma}(P) := \sum_{\{\rho i/l+\sigma j =
> v_{\rho,\sigma}(P)\}} a_{i/l,j}x^{i/l}y^j$."
>
> "For each $P\in L^{(l)}\setminus\{0\}$, we let $H(P)$ denote the convex hull
> of the support of $P$. As it is well known, $H(P)$ is a polygon, called the
> Newton polygon of $P$..." (Notation 1.6, p.4).

`N(P)` in GGHV22 is this Newton polygon $H(P)$, given as its (finite) set of
**vertices** — i.e. `N(P) = {A_1,...,A_k}` means $H(P) = \mathrm{conv}\{A_1,
\dots,A_k\}$, *not* that $\mathrm{Supp}(P)=\{A_1,\dots,A_k\}$. (Lattice points
strictly inside or on the interior of an edge of the hull may or may not carry
nonzero coefficients; GGHV22's propositions constrain only the extreme
points/vertices.) I flag this reading explicitly because it is the crux of
how large "the naive system" turns out to be in §5 below, and because in one
place (Theorem 6.1, a case not otherwise relevant here — see the Appendix) the
literal vertex list as printed is *not* convex, which is only consistent with
this reading if that particular instance is a typo.

**$\mathrm{st}_{\rho,\sigma}$, $\mathrm{en}_{\rho,\sigma}$** ([1] Notation 1.6):

> "We let $\mathrm{st}_{\rho,\sigma}(P)$ and $\mathrm{en}_{\rho,\sigma}(P)$
> denote the first and the last point that we find on $H(\ell_{\rho,\sigma}(P))$
> when we run counterclockwise along the boundary of $H(P)$."

**Jacobian bracket and Jacobian pair** ([1] Notation 1.10, Def. 1.11):

> "For $P,Q\in L^{(l)}$ we write $[P,Q]:=\det J(P,Q)$... We say that $(P,Q)$
> is a Jacobian pair if $[P,Q]\in K^\times$."

**The ambient ring $L^{(l)}$** ([1] p.3, just before Def. 1.1): $L^{(l)} :=
K[x^{1/l},x^{-1/l},y]$, i.e. Laurent polynomials in a formal $l$-th root of
$x$, times ordinary polynomials in $y$. $L^{(1)}=K[x,x^{-1},y]$; note this
already allows negative powers of $x$ (it is *not* $K[x,y]$), which is why
GGHV22's Propositions 4.1–4.4 conclude "there exist $P,Q\in L^{(1)}$..." —
these are reduced/transformed pairs living one automorphism (of $L^{(1)}$, not
of $K[x,y]$) away from the actual counterexample.

**$(m,n)$-pair** ([1] Def. 4.3, p.10, quoted because the table in §1 above is
indexed by it):

> "Let $m,n\in\mathbb N$ be coprime with $n,m>1$. A pair $(P,Q)$ of elements
> $P,Q\in L^{(l)}$ ... is called an $(m,n)$-pair in $L^{(l)}$ ... if $[P,Q]\in
> K^\times$, $\dfrac{v_{1,1}(P)}{v_{1,1}(Q)} = \dfrac{v_{1,0}(P)}{v_{1,0}(Q)} =
> \dfrac{m}{n}$ and $v_{1,-1}(\mathrm{en}_{1,0}(P)) < 0$."

---

## 3. Proposition 4.3 — the entirety of what the paper gives for the open case

Quoted verbatim from GGHV22, Section 4 ("Reducing the size of the Newton
polygon"), p.10–11 (this is *the whole statement*; nothing about the open case
appears after this proposition's proof ends):

> **Proposition 4.3 (Case (8,28)).** *If there is a counterexample to the
> Jacobian Conjecture in the case (8, 28), then there exist $P, Q \in L^{(1)}$
> with $[P, Q] = x^2$ and one of the following cases holds:*
> 1. $N(P) = \{(0,0),(1,0),(8,14),(8,16),(0,8)\}$, $N(Q) =
>    \{(0,0),(2,1),(12,21),(12,24),(0,12)\}$.
> 2. $N(P) = \{(0,0),(1,0),(8,14),(8,16)\}$, $N(Q) =
>    \{(0,0),(2,1),(12,21),(12,24)\}$.

Note the **bracket value is $x^2$**, not $x$ (as in the (7,21) and (9,24)
cases) and not $x+g(y)$ (as in the general hypothesis of Theorem 5.1). This
alone means Section 5's machinery cannot be applied to Case (8,28) by mere
substitution of different numbers — the whole derivation in §5 (Propositions
5.2–5.6, building a series $C$ with $C^2=P$, writing $Q=C^3+\dots$, and using
$[P,Q]=x$ or $x+g(y)$ at a specific step, e.g. equation (5.3)–(5.5)) is tuned
to that bracket value.

The proof of Proposition 4.3 (which I read and verified reduces to an
argument of the same *kind* as the proof of Proposition 4.1 for the (9,27)
case — repeated use of `[1, Corollary 7.4]`, `[2, Proposition 3.12]`, and case
splits on the number of linear factors of a $(\rho,\sigma)$-homogeneous
element $R$) establishes the Newton polygon shape and stops. It does **not**
go on to construct an analogue of Propositions 5.2–5.6. This is the entirety
of the paper's engagement with the open case; I confirmed this with an
exhaustive grep of the extracted text for every occurrence of "(8, 28)" and
"(8,28)".

---

## 4. What "solving the system" for the sibling case actually looked like

To make concrete exactly what is *missing* for (8,28), here is what GGHV22
does for the *closed* sibling (9,27) — this is the derivation that has no
counterpart for (8,28):

> **Proposition 4.1 (Case (9,27)).** *...there exist $P,Q\in L^{(1)}$ with
> $[P,Q]=x$ and $N(P)=\{(0,0),(1,1),(6,16),(6,18),(0,18)\}$,
> $N(Q)=\{(0,0),(1,0),(9,24),(9,27),(0,27)\}$.*

Section 5 then proves:

> **Theorem 5.1.** *There exist no pair of polynomials $P,Q\in K[x,y]$ such
> that (1) $[P,Q]=x+g(y)$ for some $g(y)\in K[y]$, (2)
> $\mathrm{en}_{3,-1}(P)=\mathrm{st}_{1,0}(P)=2(3,8)=(6,16)$ and
> $\mathrm{st}_{-1,1}(P)=\mathrm{en}_{1,0}(P)=2(3,9)=(6,18)$, (3)
> $\mathrm{en}_{3,-1}(Q)=\mathrm{st}_{1,0}(Q)=3(3,8)=(9,24)$ and
> $\mathrm{st}_{-1,1}(Q)=\mathrm{en}_{1,0}(Q)=3(3,9)=(9,27)$.*

(this hypothesis is weaker than fixing all of $N(P),N(Q)$ — it fixes only two
corners of each polygon — which is why the same theorem, via **Corollary
5.7**, also finishes off Proposition 4.1's case *and*, via Proposition 4.2's
three sub-cases, the sibling degree-99 row `A0=(9,24)` too.)

The proof of Theorem 5.1 (pp.14–19) runs, in outline:

1. `[1, Propositions 1.13, 2.1]` force $\ell_{1,0}(P)=R^2$, $\ell_{1,0}(Q)=R^3$
   for a $(1,0)$-homogeneous $R$; a linear change of variables pins $R=x^3
   y^8(y+1)$.
2. **Proposition 5.2** constructs, by an explicit recursive formula (eq.
   (5.2)), a Laurent series $C\in K[y,C_3^{-1}]((x^{-1}))$ with $C^2=P$ and
   $Q=C^3+\alpha_2C^2+\alpha_1C+\alpha_0+\alpha_{-1}C^{-1}+F$ for a tail $F$
   with $v_{1,0}(F)=-4$.
3. **Remark 5.3** normalizes $\alpha_2=\alpha_1=\alpha_0=0$ by a further
   change of $P,Q$.
4. **Proposition 5.4** derives, from $[P,Q]=x$, a first-order linear ODE for
   an auxiliary polynomial $f_1(y)$, solves it explicitly ("This equation
   has a unique solution that can be found using a CAS"), and gets
   $f_1 = -\tfrac1{9^{10}}y^9(y+1)^2(35-42y+54y^2-81y^3+243y^4)$.
5. The equalities $C^2=P$, $Q=C^3+\lambda C^{-1}+F$ are converted (eq.
   (5.6)–(5.8)) into **9 polynomial equations** $(D_2)_{-k}=0\ (k=1,\dots,8)$,
   $(D_3)_{-1}=0$, $(D_3)_{-2}=0$, $(D_3)_{-3}+\lambda C_3^{20}=0$,
   $(D_3)_{-4}-\lambda D_2C_3^{20}+F_{-4}C_3^{23}=0$, where $D_k :=
   C_kC_3^{5-2k}$ are now genuine polynomials in $y$ (Proposition 5.5).
6. After a further shift of variable ($\varphi(x)=x-D_2$) these become **9
   explicit polynomial equations in the 8 unknown polynomials $d_1,d_0,
   d_{-1},\dots,d_{-8}\in K[y]$** (eq. after (5.8), reproduced in the extraction
   at lines 895–907 of the text).
7. "using a CAS (for example Mathematica) we eliminate the variables
   $d_{-10},d_{-8},d_{-7},d_{-6},d_{-5},d_{-4},d_{-3},d_{-2}$" down to **one**
   equation (5.9): $18C_3^{23}d_1(d_{-1})^6F_{-4}+8C_3^{69}F_{-4}^3+27d_0(d_{-1})^9=0$.
8. Degree bounds from **Proposition 5.6** ($v_{-13,-1}(D)=-39$,
   $v_{17,1}(D)=51$) plus the separability of $f_1/C_3$ established in
   Proposition 5.4 turn (5.9) into a clean contradiction by comparing degrees
   in $y$ on both sides.

The point of laying this out is: **the actual "system of polynomial
equations" GGHV22 means is not a static list handed to a Groebner engine —
it is this whole derivation**, ending in one scalar-coefficient elimination
(step 7) that used a CAS's `solve`/`eliminate`, not a Groebner-basis emptiness
proof over 70+ variables. Reconstructing the analogous thing for (8,28) means
redoing steps 1–8 with: bracket $x^2$ instead of $x$; leading form
$\ell_{1,0}(P)=R^a$ for whatever power $a$ is forced by Proposition 4.3's
shape (plausibly $a=2$ again, since $8=2\cdot4$ vs. $12=3\cdot4$, but this is
*not stated* in the paper and must be independently re-derived from `[1,
Propositions 1.13, 2.1]` the way step 1 was for (9,27)); a fresh differential
equation in step 4 (the ODE's right-hand side comes from $[P,Q]=x^2$, not
$x$, so it is not the same ODE with different coefficients — the whole
right-hand side structure changes); and fresh degree bookkeeping throughout.
This is original derivation, not extraction.

---

## 5. What *is* unambiguous: the naive Newton-polygon coefficient system

Although the *reduced* system is not recoverable from the text, Proposition
4.3's data — a specific Newton polygon for $P$, a specific Newton polygon for
$Q$, and the exact bracket value $[P,Q]=x^2$ — mechanically specifies a
perfectly well-defined polynomial system: treat $P$ (resp. $Q$) as a generic
polynomial supported on the (all, not just boundary) lattice points of
$N(P)$ (resp. $N(Q)$) as given in case (1) or case (2) of Proposition 4.3,
with one unknown coefficient per lattice point, and impose $P_xQ_y-P_yQ_x-x^2
=0$ **as an identity of polynomials**, i.e. one linear-in-nothing,
quadratic-in-the-unknowns equation per monomial that can appear on either
side.

This is exactly the system `jc2_gghv_system.py` builds (see file for the
runnable code; summary below). I call it the **naive system** to keep it
sharply distinguished from the unreconstructed *reduced* system of §4.
**Emptiness of the naive system for both sub-cases of Proposition 4.3 (with
the corner coefficients forced nonzero, see side conditions below) is
logically sufficient to close the open case** — any actual counterexample
matching Proposition 4.3's shape gives a solution of the naive system, by
definition of "matching that Newton polygon." So this is a legitimate,
if oversized, target.

### 5.1 Unknowns

One symbol per lattice point of the Newton polygon (vertices + edge points +
interior points), computed by Pick's theorem / direct enumeration and
cross-checked against each other in the constructor:

| sub-case | $P$ polygon (vertices) | #$P$-unknowns | $Q$ polygon (vertices) | #$Q$-unknowns | **total** |
|---|---|---:|---|---:|---:|
| (1) (with $(0,8)$/$(0,12)$ edge) | $\{(0,0),(1,0),(8,14),(8,16),(0,8)\}$ | 61 | $\{(0,0),(2,1),(12,21),(12,24),(0,12)\}$ | 125 | **186** |
| (2) (no $y$-axis edge) | $\{(0,0),(1,0),(8,14),(8,16)\}$ | 25 | $\{(0,0),(2,1),(12,21),(12,24)\}$ | 47 | **72** |

(These counts come from Pick's theorem, $I=\text{Area}-B/2+1$, total $=I+B$,
applied to each polygon, and independently cross-checked in the script by
direct lattice-point enumeration inside the convex hull — the two methods
agree exactly for all four polygons, which is also a check that Proposition
4.3's vertex lists are honestly convex, i.e. not corrupted by a transcription
error the way one instance in Section 6 is — see Appendix.)

### 5.2 Equations

One equation per lattice point $(i,j)$ that appears with nonzero coefficient
in the formal expansion of $P_xQ_y - P_yQ_x - x^2$ (each coefficient, a
quadratic form in the $P$- and $Q$-unknowns, set to $0$; the $x^2$ term
contributes $-1$ to the equation at $(i,j)=(2,0)$ only). Counted by the
script:

| sub-case | #equations | monomial support actually occurring (computed by the script, not just an upper bound) |
|---|---:|---|
| (1) | 302 | $x$-degree $0$–$19$, $y$-degree $0$–$38$ |
| (2) | 92 | $x$-degree $1$–$19$, $y$-degree $0$–$38$ |

(The naive Minkowski-sum upper bound would be $x$-degree up to $8+12-1=19$
— attained — and $y$-degree up to $16+24-1=39$; the actual top monomial
$(19,39)$ cancels identically, because its two contributions $i\ell\,c_{i,j}d_{k,l}$
and $-jk\,c_{i,j}d_{k,l}$ at $(i,j)=(8,16)$, $(k,l)=(12,24)$ satisfy $i\ell=jk=192$
— i.e. $(8,16)$ and $(12,24)$ are aligned/proportional corners of $N(P)$ and
$N(Q)$. This is not a bug: it is the same phenomenon (aligned leading corners)
that these papers' whole apparatus of "leading forms" is built to exploit —
see `ℓ_{ρ,σ}` in §2 — and it is exactly why $N(P)=8/12$-slope corners like
these are viable Newton-polygon shapes for a hypothetical Jacobian pair in
the first place.)

Every equation is **quadratic** (bilinear) in the unknowns — a product of one
$P$-coefficient and one $Q$-coefficient per term, several such products
summed per equation.

### 5.3 Side conditions (non-vanishing)

`N(P)` being *exactly* the stated polygon (not a smaller one) requires the
coefficients at its **vertices** to be nonzero — that is what makes them
vertices of the convex hull of the support. So, for sub-case (2):
$c_{0,0},c_{1,0},c_{8,14},c_{8,16}\neq0$ for $P$, and
$d_{0,0},d_{2,1},d_{12,21},d_{12,24}\neq0$ for $Q$ (8 non-vanishing side
conditions; sub-case (1) has 10, one more vertex on each side). Interior and
edge-interior lattice points carry **no** constraint from Proposition 4.3
beyond being an unknown that may or may not vanish. These non-vanishing
conditions are not polynomial equalities; a Groebner engine needs them
saturated in (e.g. Rabinowitsch trick: for each such coefficient $c$, add a
new variable $t_c$ and the equation $c\,t_c-1=0$) — `jc2_gghv_system.py`
documents this but does not add the saturation variables by default (they
would add 8 or 10 more variables and equations).

### 5.4 Field

Characteristic $0$ throughout (GGHV22 works over a general characteristic-0
field $K$; take $K=\mathbb Q$ or $\mathbb C$ for a Groebner computation — the
paper's own reduction steps use "algebraically closed" implicitly when
factoring leading forms into linear factors, e.g. in the proof of
Proposition 4.3 itself, so $K=\overline{\mathbb Q}$ or working over
$\mathbb Q$ and adjoining roots as needed is the safe choice if factorization
over $K$ is needed at any point).

### 5.5 Is this within reach of a Groebner engine?

Sub-case (2) — 72 unknowns, 92 quadratic equations — is at the ragged edge:
not obviously hopeless to *attempt*, but 72 dense-ish unknowns with no further
structure exploited is well past what generic `groebner`/`std` calls in
Singular, Macaulay2, or Magma finish in practical time; sparse-quadratic
systems this size occasionally go through with the right monomial order and
a lot of RAM, but there is no reason to expect it, and the paper's own
authors — who are the world experts on exactly this reduction — evidently
did not run the naive system either; the entire point of Section 5's
technique (§4 above) is to avoid ever building a system this large, by first
passing to the $C,D_k$ substitution and eliminating 8 of 9 unknowns
symbolically via a CAS `eliminate` call, not a general Groebner basis on the
full unknown set. Sub-case (1) — 186 unknowns, 302 equations — is
substantially larger still and I would not expect a direct run to complete.

**Recommendation if someone wants to actually attack the open case
computationally:** the tractable route is not "run Groebner on the naive
system" but "redo GGHV22 §5's reduction (§4 above, steps 1–8) for
Proposition 4.3's shape and bracket $x^2$," which is exactly what the paper
says the authors attempted and could not finish. That reduction, if
successfully redone, would very plausibly land on a system with $O(10)$
unknowns like the closed sibling's eq. (5.9)–(5.11) — genuinely
Groebner/CAS-tractable — but producing it requires new derivation (a fresh
Proposition-5.2-style recursive series construction, a fresh
Proposition-5.4-style ODE derived from $[P,Q]=x^2$, fresh degree bookkeeping
analogous to Proposition 5.6) that this document does not attempt, per the
honesty requirement: I did not derive it, I am not going to guess at it, and
no citation in this paper or its cited companions writes it down.

---

## 6. What exactly is missing, and where it would have to come from

To be maximally explicit about the gap (per the task's "say so plainly"
requirement):

1. **Missing: the exponent(s) analogous to $\ell_{1,0}(P)=R^2$, $\ell_{1,0}(Q)=R^3$.**
   For (9,27) this came from `[1, Propositions 1.13, 2.1]` applied to
   $[P,Q]=x$ and the specific corner data. For (8,28), with $[P,Q]=x^2$ and
   Proposition 4.3's different corners, the analogous factorization is not
   stated in GGHV22 and would need to be independently derived from the same
   lemmas in [1] — a short but nontrivial step (the exponents plausibly
   relate to the $(m,n)=(3,2)$ from the table, by analogy with $(m,n)=(2,3)$
   giving exponents $2,3$ in the closed case, but the paper does not confirm
   this for (8,28) and the bracket being $x^2$ rather than $x$ changes the
   degree bookkeeping that pins the exponent, so I have not assumed it).
2. **Missing: the auxiliary series construction (Proposition-5.2 analogue).**
   Needs $C$ with $C^a=P$ for whatever $a$ is found in step 1, and a formula
   for $Q$ in terms of $C$ plus a bounded tail $F$. The recursive coefficient
   formula (paper's eq. (5.2)) is specific to the bracket value $x$ (or
   $x+g(y)$ in Theorem 5.1's more general hypothesis); with bracket $x^2$ the
   analogous recursion has not been derived here.
3. **Missing: the differential equation (Proposition-5.4 analogue).** In the
   closed case this came from equating $\ell_{1,0}$ of $[P,Q^2-P^3-2\lambda
   P]$ on both sides of an identity that used $[P,Q]=x$ specifically (paper
   eq. (5.4)–(5.5), producing the ODE $y^9(y+1)^2=6y(y+1)f_1'-10(9y+8)f_1$).
   The (8,28) analogue would produce a *different* ODE (bracket $x^2$ enters
   the corresponding identity differently) that is not written down anywhere
   in the source material I retrieved.
4. **Missing: the final degree-counting contradiction (Proposition-5.6 /
   end-of-proof analogue).** This is case-specific arithmetic on the
   $v_{-13,-1}, v_{17,1}$-style valuations of the Newton polygon in question;
   for (8,28) it is neither stated nor immediate from what's given.

None of (1)–(4) are "missing because I failed to find them in the PDF" — I
read Sections 4–6 of GGHV22 in full, grepped the extracted text exhaustively
for every mention of the case label, and checked the two most relevant
companion papers ([1]=1401.1784 for the shape/valuation machinery, and
[3]=1406.0886 for the general "system of polynomial equations related to the
JC" framework, see §7). They are missing because **the paper's authors say,
in their own words, that they attempted this and did not succeed**, and did
not publish partial progress on it beyond Proposition 4.3.

---

## 7. The general framework in [3] = arXiv:1406.0886, and why it doesn't
   close the gap either

[3]'s abstract: "We prove that the Jacobian conjecture is false if and only
if there exists a solution to a certain system of polynomial equations. We
analyse the solution set of this system. In particular we prove that it is
zero dimensional." Its introduction defines a general system $\mathrm{St}(n,m,
(\lambda_i),F_{1-n})$ of $m+n-2$ equations in $m+n-2$ unknowns over a
commutative $K$-algebra $D$ (Theorem 1.9/Corollary 1.17: $\mathrm{St}(n,m,
(\lambda_i),y)$ has a solution in $K[y]^{m+n-2}$ for some $\lambda_i$ iff a
counterexample of degree $(n,m)$ exists), and states plainly:

> "Our system provides a significative reduction of the number of equations
> and variables needed in order to verify the existence of a counterexample
> to JC at $(n,m)$... **However the number of equations is still too big to
> have a realistic chance to verify the existence of a counterexample to JC**
> for the pairs $(m,n)=(48,64),(50,75),(56,84),(66,99)$" (Introduction).

For $(n,m)=(72,108)$ this general system would have $m+n-2=178$ equations and
unknowns — comparable in size to (actually a bit smaller than, but the same
order of magnitude as) my naive system for Proposition 4.3's sub-case (1)
above (186 unknowns), and the same order as sub-case (2) (72). [3]'s own last
section illustrates, for the much smaller case $(n,m)=(50,75)$, that even
their reduced-from-naive $\mathrm{St}$ system needs a further ad hoc
"reduction of degree technique" (citing Section 8 of [1]) before it becomes
tractable — precisely the kind of case-by-case reduction that GGHV22 §5
carries out for (9,27)/(9,24) and that is missing for (8,28). So [3] confirms
the general shape of the problem but does not, by itself, hand us a smaller
explicit system for (8,28) either; it is the *method*, not a lookup table.

---

## 8. Honesty ledger

**Stated by the paper, quoted verbatim above:** Theorem 2.1; the corner
table (§2); the sentence that (9,27) is solved and (8,28) is left open
(Introduction); Proposition 4.1 (Case 9,27); Proposition 4.2 (Case 9,24, 3
sub-cases); **Proposition 4.3 (Case 8,28)** — the sole content the paper
gives for the open case; Theorem 5.1 and its full proof (closed case);
Corollary 5.7 (closed case); [3]'s abstract and introductory remarks about
system size.

**Derived by me, clearly marked as such:** the "naive" coefficient system of
§5 (unknowns = lattice points of Proposition 4.3's Newton polygons, equations
= coefficient-matching of $P_xQ_y-P_yQ_x=x^2$), its unknown/equation counts
(verified two independent ways — Pick's theorem and direct enumeration — in
`jc2_gghv_system.py`), and the sizing/feasibility discussion in §5.5.

**Assumed:** nothing about the actual reduced system was assumed or guessed;
§6 lists exactly the four derivation steps that would need to be redone and
explicitly declines to guess their content (e.g., I do *not* assume the
exponent $a$ in $\ell_{1,0}(P)=R^a$, even though $a=2$ is a plausible guess by
analogy — it is not stated in the paper and the bracket value differs from
the case it would be copied from).

**Not checked:** I did not read [2]=1605.09430 in full (only referenced for
`[2, Remark 3.31]`, `[2, Proposition 3.12]`, `[2, Proposition 3.29]` used
inside Section 3/4's arguments, which are about *different* cases than the
open one); I did not read [6]=1708.09367 beyond confirming it is the source
of the intersection-number machinery used in Section 3 (irrelevant to the
open case, which GGHV22 resolves — or fails to — without intersection
numbers). Neither omission affects the conclusion above, since neither paper
is cited anywhere near Proposition 4.3 or in connection with the open case.

---

## 9. What solving it (either version) would prove

* **The reduced system (§4/§6, not reconstructed here):** if someone
  completes the missing derivation and shows the resulting small system has
  no solution (matching how eq. (5.9)–(5.11) was shown inconsistent for the
  closed case), that discards Case (8,28), hence discards `max{deg P,deg
  Q}=108` entirely (since (9,27) is already discarded by GGHV22), hence
  raises the Moh/GGHV22 lower bound on a JC2 counterexample's degree from
  108 to **125** — exactly the improvement GGHV22's introduction says is the
  one remaining step ("With enough computing power we would be able to raise
  it up from 108 to 125, since there is only one case left").
* **The naive system (§5, reconstructed and provided in
  `jc2_gghv_system.py`):** emptiness of this system for *both* sub-cases (1)
  and (2) of Proposition 4.3 is logically equivalent in strength to the above
  (it's implied by, and implies — given Proposition 4.3's "one of the
  following cases holds" being exhaustive — the same conclusion), but as a
  Groebner target it is much larger than necessary, per §5.5.
* **A solution found to either system** would not by itself produce a JC2
  counterexample — Proposition 4.3's pairs $(P,Q)\in L^{(1)}$ are related to
  an actual counterexample in $K[x,y]$ by a chain of automorphisms of
  $L^{(1)}$ (not automorphisms of $K[x,y]$; see the proof of Proposition 4.1
  for the analogous chain in the closed case) that would need to be inverted;
  finding a nonzero solution would be enormous news (it would falsify JC2 at
  degree $(72,108)$, modulo checking that the automorphism-chain really does
  invert to a genuine pair in $K[x,y]$ with $[P,Q]=1$) but is not the same
  statement as "found a counterexample" without that additional check.

---

## Appendix: an apparent typo noticed in passing (Section 6, unrelated to the
open case)

While cross-checking every Newton-polygon vertex list in the paper for
internal convexity (as a sanity check on my own extraction — see §5.1), one
instance failed: **Theorem 6.1** states

> $N(P) = \{(0,0),(4,0),(2,6),(0,14)\}$, $N(Q) = \{(0,0),(6,0),(3,9),(0,21)\}$

but the point $(2,6)$ lies strictly *inside* the triangle
$\mathrm{conv}\{(0,0),(4,0),(0,14)\}$ (and $(3,9)$ strictly inside
$\mathrm{conv}\{(0,0),(6,0),(0,21)\}$), so as printed these are not valid
Newton-polygon vertex lists. The immediately preceding **Proposition 4.4**
(Case (7,21)), which Theorem 6.1 is supposed to restate after a normalizing
change of variables, gives $N(P)=2\{(2,0),(3,1),(0,7)\}\cup\{(0,0)\} =
\{(0,0),(4,0),(6,2),(0,14)\}$ and $N(Q) = \{(0,0),(6,0),(9,3),(0,21)\}$ — i.e.
the third vertex transposed ($(6,2)$ not $(2,6)$; $(9,3)$ not $(3,9)$) — and
the immediately following **Proposition 6.2** asserts $\ell_{1,0}(P)=x^6y^2$,
$\ell_{1,0}(Q)=x^9y^3$, which is only consistent with the $(6,2)/(9,3)$
reading (the $(1,0)$-leading term sits at the vertex with the largest
$x$-coordinate, which is $6$ resp. $9$ under that reading, not $4$ resp. $6$
under the literal Theorem 6.1 text). I read this as a transposition typo in
the published PDF, verified against the page image (not a
`pdftotext`/OCR artifact — the glyphs in the image do read "(2, 6)" and
"(3, 9)"). **This does not affect anything above**: it concerns Section 6
(an independent second proof of the already-elsewhere-closed max=84 case),
not Section 4/5's treatment of the open (8,28) case, and I checked
independently that every Newton polygon vertex list attached to Propositions
4.1–4.3 (the ones this document relies on) *is* internally convex as printed
— confirmed by convex-hull recomputation in `jc2_gghv_system.py`.

---

## File manifest

* `/home/user/jacobian_planar/jc2_gghv_system.md` — this file.
* `/home/user/jacobian_planar/jc2_gghv_system.py` — sympy constructor for the
  naive Newton-polygon coefficient system of §5, for both sub-cases of
  Proposition 4.3 (the open case) and, as a validation/sizing comparator, the
  same construction applied to Proposition 4.1's (9,27) shape and a
  hand-verifiable linear ($\deg=1$) sanity check. Emits Singular `ring`/`ideal`
  syntax. Does not attempt to solve anything (no Groebner call).
* Fetched PDFs and `pdftotext` extractions live under the scratchpad
  (`/tmp/claude-0/-home-user-jacobian-planar/8579cc16-25cb-5f13-9ff3-9a51c4d87492/scratchpad/pdfs/`),
  not in this repo, per instructions.
