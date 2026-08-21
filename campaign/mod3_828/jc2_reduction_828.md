# Redoing GGHV22 Section 5 for the open (8,28) shape, bracket $[P,Q]=x^2$

**Task.** GGHV22 (arXiv:2204.14178) closes the sibling shape "(9,27)" of
their Proposition 4.1 using a five-page technique in Section 5 (build an
auxiliary series $C$ with $C^2=P$, write $Q=C^3+\ldots$, derive a
differential equation from $[P,Q]=x$, reduce to a handful of equations, get
a contradiction by degree count). They state in their own words that they
attempted the analogous thing for the open shape "(8,28)" of their
Proposition 4.3 (bracket $[P,Q]=x^2$) and "couldn't solve the corresponding
system of polynomial equations." This document redoes that attempt from
scratch, in exact arithmetic, checking every general mechanism used against
GGHV22's own published numbers for the closed case before trusting it on
the open one.

**Bottom line, stated first.** This reconstruction gets substantially
further than the "naive coefficient system" that `jc2_gghv_system.md`
correctly identifies as hopeless (72 unknowns, 92 equations, direct Groebner
dead). It rebuilds essentially all of GGHV22's Section 5 machinery for the
new bracket — the exponent-forcing step, the auxiliary series, the
normalization, and, novel to this session, an exact closed-form
differential equation with a **unique polynomial solution of degree 14**,
separable and coprime to $y(y+1)$, structurally an exact parallel of
Proposition 5.4. It also derives the Proposition 5.5 and 5.6 analogues
(the $D_k$ recursion and the two valuation bounds) and gets as far as an
explicit, much smaller — but not yet fully collapsed — system: **8 shallow
unknown polynomials, reduced to 5 by three short explicit constraints**,
still short of GGHV22's clean single equation (5.9). Both a pure-Python
(sympy) and a dedicated (Singular) Groebner engine were pointed at the
remaining elimination and neither finished in this session; Singular's own
progress trace shows the same character of degree blow-up documented
elsewhere in this repo for the un-reduced system. **No contradiction and
no solution were found.** The case remains open. Section 6 below states
exactly where the trail stops and why.

All code is in `/home/user/jacobian_planar/jc2_reduction_828.py` (the
consolidated, assertion-checked version — every general formula used below
is verified by an `assert` against GGHV22's own numbers before being
applied to the open case) and in
`/tmp/claude-0/-home-user-jacobian-planar/8579cc16-25cb-5f13-9ff3-9a51c4d87492/scratchpad/work2/`
(the exploratory scripts, `step1`–`step6`, kept for the audit trail).

---

## 1. Source material and method

Fetched and read in full: arXiv:2204.14178v1 Sections 4–6 (`pdftotext -layout`
extraction, cross-checked against the already-fetched copy at
`/tmp/.../scratchpad/pdfs/paper1_2204.14178.txt`, lines 224–997 for
Sections 4–5), and the two lemma sources it cites, arXiv:1401.1784
(`paper2_1401.1784.txt`, Propositions 1.13 and 2.1) at the specific
locations GGHV22 invokes them.

**Method used throughout**: never trust a general mechanism against the
open case until it has been checked, by direct computation, against
GGHV22's own explicit numbers for the closed (9,27) case. This caught two
real errors before they could propagate:

* The `pdftotext -layout` rendering of GGHV22's stated solution
  $f_1=-\frac1{9^{10}}y^9(y+1)^2(\ldots)$ is **ambiguous** — the fraction
  bar and the y-exponent land on the same output line. Plugging the literal
  "$9^{10}$" reading into the stated ODE leaves a residual of
  $(1-\frac{910}{9^{10}})\,y^9(y+1)^2\neq0$: it does **not** solve the
  equation. The correct reading is denominator **910** (nine hundred ten),
  confirmed two ways: (a) it makes the residual exactly zero, (b)
  solving the ODE from scratch by undetermined coefficients (no assumed
  closed form) reproduces $f_1$ with denominator 910 exactly. This is a
  transcription-ambiguity catch, not a claim that the paper is wrong.
* A sign convention in my first hand-transcription of the $C_k$ recursion
  (equation (5.2)) turned out inconsistent with the paper's own later use
  of it (specifically $D_2=\tfrac12P_5$); the version consistent with
  everything downstream was re-derived directly from $C^2=P$ term-by-term,
  not copied from the possibly-mis-OCR'd display.

Both are documented in `jc2_reduction_828.py`'s Section 1 (`section1_calibration`),
which re-derives, from scratch, and cross-checks against GGHV22's own text:

| Quantity (closed (9,27) case) | GGHV22 states | Re-derived here | Match |
|---|---|---|---|
| $C_3'$ | $(9y+8)y^7$ | same | exact |
| $f_1$ (ODE solution) | $-\tfrac1{910}y^9(y+1)^2(35-42y+54y^2-81y^3+243y^4)$ | same, solved from scratch by undetermined coefficients | exact |
| $\deg(f_1/C_3)$ | 6 | 6 | exact |
| eq (5.9) $\to$ (5.11) substitution | factor $y^{507}$ pulls out | same | exact |
| $v_{-13,-1}(D)$, $v_{17,1}(D)$ | $-39$, $51$ | same, from a general formula (§4 below) | exact |
| resulting degree/divisibility bounds | 26, 39, 52, 34, 51 | same, from the same general formula | exact (all 5) |
| the four $(D_3)_{-k}$ equations, $k=1..4$ | stated explicitly (two trivial, then $+\lambda C_3^{20}$, then $-\lambda D_2C_3^{20}+F_{-4}C_3^{23}$) | re-derived independently from the definition $D_k:=C_kC_3^{5-2k}$ and $Q=C^3+\lambda C^{-1}+F$ | exact, including both exponents 20 and 23 |

Nine independent numeric cross-checks, all exact matches. This is the basis
for trusting the *general formulas* (not the specific numbers) enough to
apply them to the open case.

---

## 2. What changes for (8,28): every place the bracket value enters

Proposition 4.3, sub-case (2) (the smaller of the two Newton-polygon
sub-shapes, the one with 72 unknowns in the naive system — this document
does not separately treat sub-case (1), see §7):

$$N(P)=\{(0,0),(1,0),(8,14),(8,16)\},\quad N(Q)=\{(0,0),(2,1),(12,21),(12,24)\},\quad [P,Q]=x^2.$$

### 2.1 The exponent 2,3 is forced again — but check, don't assume

GGHV22's own derivation for (9,27) ("By [1, Propositions 1.13 and 2.1] there
exists a $(1,0)$-homogeneous $R$ with $\ell_{1,0}(P)=R^2$, $\ell_{1,0}(Q)=R^3$")
uses two general facts from [1] that do **not** mention the bracket value
directly — they only need $[P,Q]$'s $(1,0)$-valuation to be *small* relative
to $v_{1,0}(P)+v_{1,0}(Q)$:

* [1, **Prop 1.13**]: $v_{1,0}([P,Q])\le v_{1,0}(P)+v_{1,0}(Q)-1$, with
  equality iff $[\ell_{1,0}(P),\ell_{1,0}(Q)]\ne0$.
* [1, **Prop 2.1(2)**]: if $[\ell_{1,0}(P),\ell_{1,0}(Q)]=0$ then
  $\ell_{1,0}(P)=\lambda_PR^m$, $\ell_{1,0}(Q)=\lambda_QR^n$ for coprime
  $m,n$ with $n\cdot v_{1,0}(P)=m\cdot v_{1,0}(Q)$.

For (9,27): $v_{1,0}(x)=1 \ll v_{1,0}(P)+v_{1,0}(Q)-1=6+9-1=14$, so
Prop 1.13 forces $[\ell_{1,0}(P),\ell_{1,0}(Q)]=0$, and Prop 2.1(2) with
$6n=9m$ gives $(m,n)=(2,3)$.

For (8,28): $v_{1,0}(P)=8$, $v_{1,0}(Q)=12$ (read directly off Prop 4.3's
polygon), and $v_{1,0}(x^2)=2$. Check: $2 < 8+12-1=19$ — **still far
enough below the threshold**, so the identical argument applies, giving
$8n=12m\Rightarrow2n=3m\Rightarrow(m,n)=(2,3)$ **again** — the same
exponent pair, but now *derived from Prop 4.3's own corner numbers*, not
carried over by analogy (this closes "missing item 1" flagged in
`jc2_gghv_system.md` §6). So:
$$\ell_{1,0}(P)=R^2,\qquad \ell_{1,0}(Q)=R^3,\qquad v_{1,0}(R)=8/2=4.$$
$R$ is $(1,0)$-homogeneous, hence $R=x^4C_4(y)$ for a polynomial $C_4$.
Matching $P$'s edge at $x=8$ (y-range $[14,16]$, width 2 $=m\cdot$width$(C_4)$)
and $Q$'s edge at $x=12$ (y-range $[21,24]$, width 3) both force
width$(C_4)=1$, base power 7:
$$C_4=y^7(a_0+a_1y)\ \xrightarrow{\text{linear change of vars}}\ C_4=y^7(y+1)$$
— by the identical genericity argument GGHV22 uses to fix $C_3=y^8(y+1)$
(a "linear change of vars in $y$" normal-forms any $y^k(a_0+a_1y)$,
$a_0,a_1\ne0$, to $y^k(y+1)$; this step never referenced the bracket value
either).

### 2.2 The crux: $v_{1,0}(F)$ shifts from $-4$ to $-5$

This is the one place the bracket value $x$ vs. $x^2$ genuinely changes a
number, not just relabels one. GGHV22's argument that $v_{1,0}(F)=-4$
(where $Q=C^3+\alpha_2C^2+\alpha_1C+\alpha_0+\alpha_{-1}C^{-1}+F$) goes:
write $\Phi:=Q-C^3$; since $C^3$ is a function of $C$ alone, $[C^3,P]=0$
(any two functions of one common series bracket to zero — verified directly:
$[f(C),g(C)]=f'(C)g'(C)(C_xC_y-C_yC_x)=0$), so $[\Phi,P]=-[P,Q]$. Prop 1.13
at $(\rho,\sigma)=(1,0)$ gives
$$v_{1,0}(\Phi)\ \ge\ v_{1,0}([P,Q])-v_{1,0}(P)+1,$$
with the bound *tight* (not just an inequality) because if $v_{1,0}(\Phi)$
were strictly larger, $[\ell_{1,0}(P),\ell_{1,0}(\Phi)]=0$ would be forced
(Prop 1.13's iff clause), making $\ell_{1,0}(\Phi)$ a pure power of $R$
(Prop 2.1(2) again) — precisely the "resonant" $\alpha_kC^k$ pieces that get
subtracted off one at a time until the bound is reached exactly (and it
*is* reached exactly, not overshot, by the same argument run in reverse:
going below the bound would force $v_{1,0}([\Phi,P])<v_{1,0}([P,Q])$,
contradicting that this valuation is fixed throughout since only
zero-bracket terms were ever subtracted).

$$v_{1,0}(F)=v_{1,0}([P,Q])-v_{1,0}(P)+1.$$

* Closed case: $1-6+1=-4$. Matches GGHV22 exactly.
* **(8,28) case: $2-8+1=-5$.**

The resonant exponent set to normalize away is $\{k:\ N<k\cdot v_{1,0}(R)<3v_{1,0}(R)\}$;
plugging in gives $\{-1,0,1,2\}$ for **both** cases (closed: $N=-4$,
$v_{1,0}(R)=3$; open: $N=-5$, $v_{1,0}(R)=4$ — different numbers, same
resulting integer set), so Remark 5.3's normalization
($Q=C^3+\lambda C^{-1}+F$, $\alpha_2=\alpha_1=\alpha_0=0$ by an algebraic
"depressing the cubic" substitution that never touches $[P,Q]$ — checked:
$[\tilde P,\tilde Q]=[P,Q]$ exactly, since $\tilde P-P$ and $\tilde Q-Q$
are a constant and a multiple of $P$ respectively) carries over to (8,28)
**verbatim**, just with the new threshold: $v_{1,0}(F)=-5$.

### 2.3 The differential equation for $f_1$ — rebuilt from bracket algebra, not copied

GGHV22 derive the ODE (their eq. before (5.4)–(5.5)) via a chain: expand
$Q^2-P^3-2\lambda P$, show its $(1,0)$-leading form is $2x^5C_3^3F_{-4}$
(using $v_{1,0}(F)=-4$ and $[\ell_{1,0}(P),\ell_{1,0}(F)]\ne0$ — itself
automatic from the same tight-bound argument in §2.2), equate this to
$\ell_{1,0}([P,Q^2])=\ell_{1,0}(2xQ)$ (chain rule: $[P,Q^2]=2Q[P,Q]=2Qx$),
apply the identity $[A^2,B]=2A[A,B]$ and the two-line identity
$[x^pf(y),x^qg(y)]=x^{p+q-1}(pfg'-qf'g)$ (both re-derived and checked
against GGHV22's own intermediate coefficients "6" and "10" — see
`jc2_reduction_828.py`, and independently against the paper's stated
$C_3'=(9y+8)y^7$).

Redone for us with $[P,Q]=x^2$ (so $[P,Q^2]=2Qx^2$), $v_{1,0}(R)=4$,
$v_{1,0}(F)=-5$:

$$\ell_{1,0}(Q^2-P^3-2\lambda P)=2x^7C_4^3F_{-5},\qquad
\ell_{1,0}([P,Q^2])=2x^{14}C_4^3,$$
$$2x^{14}C_4^3=[x^8C_4^2,\ 2x^7C_4^3F_{-5}]
\ \xrightarrow{\text{same algebra}}\
C_4^2=8C_4f_1'-14C_4'f_1,\quad f_1:=C_4^3F_{-5}.$$

Plugging in $C_4=y^7(y+1)$, $C_4'=y^6(8y+7)$:

$$\boxed{y^8(y+1)^2\ =\ 8y(y+1)\,f_1'\ -\ 14(8y+7)\,f_1.}$$

(Compare the closed case's $y^9(y+1)^2=6y(y+1)f_1'-10(9y+8)f_1$ — same
shape, coefficients $6\to8$, $9\to8$, $8\to7$, $10\to14$, top power
$9\to8$, all forced by $a=v_{1,0}(R)$ going $3\to4$ and the bracket's
valuation going $1\to2$.)

### 2.4 Solving it — exact, unique, and checked to be well-posed

Solved from scratch by undetermined coefficients (a degree-$D$ generic
polynomial ansatz, coefficients matched order by order; **no closed form
assumed**), exactly as the closed case was re-solved in §1 for calibration:

$$f_1\ =\ -\frac{y^8(y+1)^2\bigl(2048y^4-512y^3+320y^2-240y+195\bigr)}{6630},
\qquad \deg f_1=14.$$

The solution is **unique**: the homogeneous ODE $8y(y+1)f'=14(8y+7)f$ has
solution $f^{\text{hom}}=y^{49/4}(y+1)^{7/4}$ (fractional exponents — not a
polynomial), so no polynomial multiple of a homogeneous solution can be
added; any polynomial solution of the inhomogeneous equation is forced to
be unique. (Same check run on the closed case: homogeneous exponents
$40/3,\,5/3$, also fractional — consistent with GGHV22 calling their
solution "the" unique one.)

Dividing by $C_4=y^7(y+1)$:
$$f:=f_1/C_4=-\frac{y^6\cdot(\ldots)}{\ldots}\quad(\text{exact division, no remainder}),\qquad \deg f=6.$$
$$f=y(y+1)\,Q(y),\qquad Q(y)=-\tfrac1{6630}\bigl(2048y^4-512y^3+320y^2-240y+195\bigr).$$

**Checked, not assumed** (Proposition 5.4's exact structural conclusion,
re-verified for this case): $Q(0)=195\ne0$, $Q(-1)=3315\ne0$ (so $y,y+1\nmid Q$),
$\gcd(Q,Q')=1$ (squarefree — confirmed both symbolically and by locating
its four roots numerically: two complex-conjugate pairs, all four
distinct), and $\gcd(f,f')=1$ (the full degree-6 $f$ is squarefree too,
since $y$, $y+1$, and $Q$'s four roots are pairwise distinct). **This is an
exact structural match to Proposition 5.4's conclusion for the closed
case** — separability is exactly what the endgame (comparing $(y+1)$-adic
multiplicities, §2.6 below) will need.

### 2.5 Proposition 5.5 analogue: $D_k:=C_kC_4^{7-2k}\in K[y]$

Re-derived (not copied) from $C^2=P$ term-by-term, giving the recursion
$$C_k=\frac1{2C_4}\Bigl(P_{4+k}-\sum_{i=1}^{3-k}C_{4-i}C_{k+i}\Bigr),\qquad k\le3,$$
and, mirroring GGHV22's induction exactly (verified computationally in
`Dk_recursion_general` — using `cancel()`, not `together()`, so
polynomiality is actually checked, not merely displayed):
$$D_k=\tfrac12P_{4+k}C_4^{6-2k}-\tfrac12\sum_{i=1}^{3-k}D_{4-i}D_{k+i}\in K[y],\qquad k\le3.$$
(This same general recursion, run with $a=3$ instead of $4$, reproduces
GGHV22's own $D_2=\tfrac12P_5\in K[y]$ exactly — the calibration in §1.)

### 2.6 Proposition 5.6 analogue: the two valuation bounds

GGHV22's bounds $v_{-13,-1}(D)=-39$, $v_{17,1}(D)=51$ come from a
$k$-independence trick: bound each $D_kx^k$ in a chosen direction
$(-A,-1)$ or $(B,1)$, using $v_{2,-1}(C)\le1$ (their $v_{3,-1}(C)\le1$) and
$v_{-1,1}(C)\le4$ (their $v_{-1,1}(C)\le6$) — read directly off $R$'s two
"reduced" corners $(4,7)$ and $(4,8)$ of Prop 4.3's polygon (in place of
$(3,8),(3,9)$) — then choosing $A,B$ so the $k$-dependence in the resulting
bound cancels exactly. Re-derived from scratch (general formula, then
solved for the cancelling $A,B$ symbolically):
$$v_{-12,-1}(D)=-48,\qquad v_{15,1}(D)=60.$$
(directions $(-12,-1)$ and $(15,1)$ replace $(-13,-1)$ and $(17,1)$.)
Consequence, same general formula that reproduced all five of GGHV22's
own numbers (26, 39, 52, 34, 51) in §1:

| $k$ | $\deg_y(D_k)\le$ | $y^{(\cdot)}\mid D_k$ | width (monomials) |
|---:|---:|---:|---:|
| 4 | 0 | $y^0$ | 0 (constant; $D_4=1$) |
| 3 | 15 | $y^{12}$ | 3 (4) |
| 2 | 30 | $y^{24}$ | 6 (7) |
| 1 | 45 | $y^{36}$ | 9 (10) |
| 0 | 60 | $y^{48}$ | 12 (13) |
| $-1$ | 75 | $y^{60}$ | 15 (16) |

---

## 3. The $(D^3)_{-k}$ equations — verified mechanism, then applied

GGHV22 states, without re-derivation, four explicit equations
$(D_3)_{-1}=0,\ (D_3)_{-2}=0,\ (D_3)_{-3}+\lambda C_3^{20}=0,\
(D_3)_{-4}-\lambda D_2C_3^{20}+F_{-4}C_3^{23}=0$. These were **re-derived
independently** here from $Q=C^3+\lambda C^{-1}+F$, $(D^3)_{-k}=(C^3)_{-k}C_3^{15+2k}$,
and case analysis on when $(C^{-1})_{-k}$ and $F_{-k}$ first become nonzero
— and matched the paper's equations **exactly, including both exponents 20
and 23** (`step3_full_elim_original.py`; see also §1's table). The general
formula, applicable to any top exponent $a$ (checked at $a=3$, then run at
$a=4$):

$$(D^3)_{-k}=0\ \ (k=1,\ldots,a-1),\qquad
(D^3)_{-a}+\lambda C_a^{8a-4}=0,\qquad
(D^3)_{-(a+1)}-\lambda D_{a-1}C_a^{8a-4}+F\,C_a^{8a-1}=0.$$

For $a=3$: exponents $20,23$ — matches. For **$a=4$ (our case)**:
exponents $\mathbf{28,31}$, and there is one *extra* trivial equation
($(D^3)_{-3}=0$, since now $k=1,2,3$ are all $<a=4$) compared to the closed
case's two.

---

## 4. Where the mechanical reconstruction stops

This is the genuinely new (and genuinely inconclusive) finding of this
session, and it is exactly the kind of thing the task asked to be reported
precisely rather than glossed over.

**What works cleanly**: using $(D^2)_{-k}=0$ ($k=1,2,\ldots$) alone, each
equation is *linear* in exactly one new "deepest" unknown $D_{-(k+a)}$ and
can be solved for it symbolically in terms of shallower $D$'s — verified
computationally to depth 7+ for both $a=3$ and $a=4$, no obstruction. This
leaves **$2a$ shallow $D$'s genuinely free** before anything else is
imposed: $D_{a-1},\ldots,D_{-a}$, i.e. **6** for the closed case
($D_2,D_1,D_0,D_{-1},D_{-2},D_{-3}$), **8** for (8,28)
($D_3,D_2,D_1,D_0,D_{-1},D_{-2},D_{-3},D_{-4}$).

**The trap this session fell into and climbed back out of**: it is tempting
to assume $(D^3)_{-k}=0$ for $k<a$ is *automatically* satisfied once the
deep $D$'s are substituted in (after all, GGHV22's own derivation shows
it's a consequence of $Q$ being a genuine polynomial). **It is not
automatic under this parametrization.** The $(D^2)$-only substitution
knows nothing about $Q$; imposing $(D^3)_{-k}=0$ for $k=1,\ldots,a-1$ is
exactly the *new, genuine* information that ties the $P$-side data to the
$Q$-side data. Computed explicitly (both cases, exact rational
coefficients):

**Closed case ($a=3$), two constraints:**
$$\tfrac32D_1D_{-1}^2+3D_2D_{-1}D_{-2}+3D_{-1}D_{-3}+\tfrac32D_{-2}^2=0,$$
$$-\tfrac32D_0D_{-1}^2+\tfrac32D_2D_{-2}^2+3D_{-2}D_{-3}=0.$$

**(8,28) case ($a=4$), three constraints:**
$$\tfrac32D_1D_{-1}^2+3D_2D_{-1}D_{-2}+3D_3D_{-1}D_{-3}+\tfrac32D_3D_{-2}^2+3D_{-1}D_{-4}+3D_{-2}D_{-3}=0,$$
$$-\tfrac32D_0D_{-1}^2+\tfrac32D_2D_{-2}^2+3D_3D_{-2}D_{-3}+3D_{-2}D_{-4}+\tfrac32D_{-3}^2=0,$$
$$-3D_0D_{-1}D_{-2}-\tfrac32D_1D_{-2}^2+\tfrac32D_3D_{-3}^2-\tfrac12D_{-1}^3+3D_{-3}D_{-4}=0.$$

This drops the free count from $2a$ to $a+1$: **4** for the closed case —
matching, exactly, GGHV22's eq. (5.9), which has exactly four surviving
unknowns $d_1,d_0,d_{-1},F_{-4}$ (with $\lambda$ eliminated via the
$(D^3)_{-a}$ equation, which is linear in $\lambda$) — a strong consistency
check on this whole line of attack. For (8,28): **5** ($D$'s worth $a+1=5$,
paralleling $d_1,d_0,d_{-1},F_{-4}$ plus one more).

**What did not complete**: collapsing this further to GGHV22's clean
single equation requires either

1. correctly implementing the coordinate shift $\varphi(x)=x-D_{a-1}$ that
   GGHV22 use to kill one more variable for free — attempted here by naive
   substitution ($D\mapsto D(x+D_{a-1})$ and $D\mapsto D(x-D_{a-1})$ into
   $D$'s own series), **neither reproduced the required cancellation of
   the next coefficient**, so this was not pursued further rather than
   risk publishing a wrong shift formula (the shift is very likely applied
   to $P,Q$ directly, not to $D$'s formal series in place — GGHV22's own
   phrasing, "the automorphism $\varphi$ of $K[y]((x^{-1}))$ given by
   $\varphi(x)=x-D_2$", is a ring automorphism argument this session did
   not have time to reconstruct correctly), or
2. a direct multivariate Groebner elimination of the remaining system.

**(2) was attempted computationally, twice, and neither attempt
finished.** A pure-Python (sympy) `groebner()` call on the $a=3$ system
(12 equations, 10 variables to eliminate — the *already-solved* case, used
purely as a test of method) was killed by a 5-minute wall-clock timeout
with no output. A dedicated Groebner engine (Singular, `std()` with a
genuine elimination block ordering) was then tried on the same system, at
successively *smaller* scale (down to just 6 equations, 5 variables to
eliminate) — even this "tiny" version did not finish in the timeouts
tried (30–100s), and a longer background run's own `option(prot)`
S-polynomial-degree trace showed degree markers climbing past **3700**
within a few minutes with no sign of termination — the same qualitative
failure mode `jc2_gghv_system.md` §5.5 already documents for the
un-reduced 72-variable naive system ("Singular slimgb ran out of memory
at 6GB, std did not finish"). This is not a claim that the elimination is
impossible — GGHV22's own authors got through the analogous computation
for the closed case using a CAS (they name Mathematica) — only that it
resisted both a from-scratch symbolic elimination and a dedicated Groebner
engine within this session's resources, at a stage of the problem that is
already **far smaller** (single-digit-to-teens polynomial unknowns in $y$
of bounded, computed degree, not 72 monomial coefficients).

**No contradiction was reached, and no candidate $(P,Q)$ was found.** The
(8,28) case remains open after this session. What has changed is that the
gap identified in `jc2_gghv_system.md` §6 ("Missing: items 1–4, none of
which are guessed") is now closed for items 1–3 (the exponent, the series
construction including its exact convergence bounds, and the differential
equation with its exact unique solution) and substantially narrowed for
item 4 (the final degree-count contradiction) — the two valuation bounds
that would feed it are in hand, and the size of the *remaining* elimination
problem is now known precisely (an explicit 5-unknown-polynomial system,
handed off below), rather than "an unreconstructed black box."

---

## 5. Honesty ledger

**Stated by the paper, quoted/cited above:** Proposition 4.3's Newton
polygons and bracket value; Theorem 5.1's hypotheses and the outline of its
proof (Propositions 5.2, 5.4, 5.5, 5.6); the four numeric values 26, 39,
52 and 34, 51 (Prop 5.6 consequences); the four $(D_3)_{-k}$ equations;
[1, Propositions 1.13 and 2.1] (fetched and read directly from
arXiv:1401.1784, not taken on GGHV22's word).

**Derived here, clearly new work, and independently checked before use on
the open case:**
* The exponent pair $(2,3)$ for (8,28), from Prop 4.3's own corner data
  via [1, Props 1.13, 2.1] (§2.1) — GGHV22 never states this for (8,28).
* $v_{1,0}(F)=-5$ (vs. $-4$) — the one place the bracket value $x^2$ (vs.
  $x$) directly changes a number in this derivation (§2.2).
* The ODE $y^8(y+1)^2=8y(y+1)f_1'-14(8y+7)f_1$ and its **unique** exact
  polynomial solution of degree 14, checked separable and coprime to
  $y(y+1)$ (§2.3–2.4) — this is the furthest point reached; it is a
  genuinely new closed-form result, not previously published anywhere I
  could find (checked: it does not appear in GGHV22 or in any of the six
  companion papers fetched for `jc2_gghv_system.md`).
* The Prop 5.5 and 5.6 analogues (§2.5–2.6), and the $(D^3)_{-k}$ general
  formula with exponents $8a-4,8a-1$ (§3).
* The dimension-counting finding (§4): $2a$ shallow free $D$'s, cut to
  $a+1$ by $(a-1)$ short explicit constraints from $(D^3)_{-k}=0$,
  $k<a$ — including the discovery that these are **not** automatically
  zero under the $(D^2)$-only parametrization (a trap avoided by checking
  computationally rather than assuming, mirroring GGHV22's closed-case
  count exactly: $a+1=4$ matches eq (5.9)'s four unknowns).

**Every division by a quantity assumed nonzero, listed explicitly** (per
the task's instruction, since none of the above amounts to a closure —
this list is for the specific inequalities/nonvanishing facts leaned on):
* $2C_4\ne0$ throughout the $C_k$ recursion (true: $C_4=y^7(y+1)\ne0$ as a
  polynomial).
* $[\ell_{1,0}(P),\ell_{1,0}(F)]\ne0$, used to get the equality case of
  Prop 1.13 in the ODE derivation — this is *forced*, not assumed (§2.2's
  tight-bound argument), given $F\ne0$ (which holds, else $[P,Q]=0$,
  contradicting $[P,Q]=x^2\ne0$).
* $y,y+1\nmid Q(y)$ and $Q$ squarefree, in §2.4 — **checked directly**
  ($Q(0)=195$, $Q(-1)=3315$, $\gcd(Q,Q')=1$, all exact rational
  computations), not assumed.
* Division by $D_{-1}$ implicitly in the (unused) attempt to solve the
  first $(D^3)$-constraint for $D_{-3}$ in §4 — this path was **not**
  carried through to any conclusion, so no result here depends on it.

**No contradiction was reached in this session**, so the task's requirement
of an independent second derivation of a contradiction does not apply.
**No solution was found either** — nothing here should be read as
suggesting one exists; the honest state is "reduced further than before,
still open."

**Not checked / explicitly out of scope:** Proposition 4.3's **sub-case
(1)** (the shape with the extra $(0,8)/(0,12)$ vertex). By analogy with how
GGHV22's Theorem 5.1 hypothesis only pins the corners *shared* by both of
Proposition 4.2's sub-cases (letting one theorem dispatch several shapes at
once via Corollary 5.7), the $(1,0)$-leading-edge data used throughout §2–4
above (the edge from $(1,0)$ to $(8,14)$ to $(8,16)$) is **identical**
between Prop 4.3's sub-cases (1) and (2) — only the far side of the polygon
differs. It is plausible the same ODE and $D_k$/$D^3$ machinery covers
sub-case (1) too (after a shear automorphism analogous to the one used in
GGHV22's Corollary 5.7, since sub-case (1)'s $(-1,1)$-direction leading
form is a genuine edge, not a single vertex — checked: $v_{-1,1}$ ties at
value 8 between $(8,16)$ and $(0,8)$, exactly mirroring why Corollary 5.7
needed its shear for the closed case's own y-axis-edge shape). This was
**not** attempted here; it is flagged, not derived, per the honesty
requirement.

---

## 6. Handoff: the reduced system, Singular-ready

Per the task's step 4, here is the concrete size of what remains, handed
off as an explicit, checked system rather than a vague pointer. This is
**not solved** — it is the smallest well-defined target this session
reached.

**Unknowns** (8 total, all polynomials in $K[y]$, degree-bounded as in the
table in §2.6): $D_3,D_2,D_1,D_0,D_{-1},D_{-2},D_{-3},D_{-4}$, plus the two
scalars $\lambda,F$ (a shorthand for the single coefficient $F_{-5}$), all
over the base field $\mathbb Q$ with $C_4=y^7(y+1)$ substituted in
explicitly (a fixed, known polynomial, not a further unknown).

**Equations** (concrete, generated by
`gen_singular2.build_system(a=4, Nmax=…, F_index=5)` in
`/tmp/claude-0/-home-user-jacobian-planar/8579cc16-25cb-5f13-9ff3-9a51c4d87492/scratchpad/work2/`,
reused without modification from the code that reproduced GGHV22's own
four equations exactly for $a=3$):

* $(D^2)_{-k}=0$ for $k=1,\ldots,N-4$ (as many as needed to reach whatever
  depth $N$ the eventual elimination requires — these were verified to
  triangularly define $D_{-5},D_{-6},\ldots$ in terms of the 8 shallow
  unknowns, to any depth tested).
* The three constraints of §4 ($(D^3)_{-1}=(D^3)_{-2}=(D^3)_{-3}=0$).
* $(D^3)_{-4}+\lambda C_4^{28}=0$.
* $(D^3)_{-5}-\lambda D_3C_4^{28}+F\cdot C_4^{31}=0$.

**Target**: eliminate $D_3$ and the deep $D_{-k}$'s ($k\ge2$), leaving a
relation among $D_1,D_0,D_{-1},\lambda,F$ (or, if the shift substitution of
§4(1) can be gotten right, among four shifted polynomials analogous to
GGHV22's $d_1,d_0,d_{-1}$ plus $F$) — expected, by the $a+1=5$
dimension count of §4, to be **one polynomial equation in five unknowns**,
the direct analogue of GGHV22's eq. (5.9). Reaching it is exactly the
"redo GGHV22 §5 for (8,28)" task that the paper's own authors say they
attempted and did not complete; this document gets to the equation *before*
it, with every ingredient needed to state it (the two exponents 28, 31;
the two valuation bounds $-48,60$; the ODE's exact solution) now in hand
and checked, but does not complete the final elimination.

The generator scripts (`gen_singular2.py`, `gen_singular3.py`, and the raw
`.sing` files `orig_a3.sing`, `small2_a3.sing`, `tiny_a3.sing` for the
$a=3$ test runs) are in the scratchpad directory above, available to resume
from, together with the triangular-substitution driver
(`step6_triangular_original.py` and its inline $a=4$ counterpart) that
produced the three explicit constraint polynomials quoted in §4.

---

## File manifest

* `/home/user/jacobian_planar/jc2_reduction_828.md` — this file.
* `/home/user/jacobian_planar/jc2_reduction_828.py` — consolidated,
  assertion-checked derivation. Every general formula is verified against
  GGHV22's own published numbers for the closed (9,27) case (Section 1 of
  the script) before being applied to (8,28) (Sections 2–4 of the script).
  Running it (`python3 jc2_reduction_828.py`) re-executes every check in
  this document from scratch and prints "ALL ASSERTIONS PASSED" if nothing
  has silently drifted.
* Exploratory scripts and raw Singular attempts (not needed to reproduce
  the above, kept for the audit trail):
  `/tmp/claude-0/-home-user-jacobian-planar/8579cc16-25cb-5f13-9ff3-9a51c4d87492/scratchpad/work2/step1_verify_original.py`
  through `step6_triangular_original.py`, `gen_singular2.py`,
  `gen_singular3.py`, and the `.sing` files.
