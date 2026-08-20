# Session 19 — Is the mod-3 wall fundamental, or a Borisov artifact?

**Question asked.** Is `3v(v+1)R' = D·R` a necessary consequence of *any*
Keller-pair construction built via the chart/blowup/boundary-rigidity method, or
is the coefficient `3` an artifact of Borisov's ramification profile, cusp type
`(2,3)`, and box combinatorics?

**Verdict: (c) — neither (a) nor (b), and the difference matters.**

The `3` is **`k`, the primitive multiplicity of the boundary valuation vector**
`(val_E y1, val_E y2) = -k·(b,a)`. In Borisov's First Framework
`(val_E y1, val_E y2) = (-9,-6) = -3·(3,2)`, so `k = 3`.

It is **not** the cusp exponent (`b = 3`) and **not** the chart slope
(`rho = 3`), even though all three collide on the value 3 in his setup. Varying
the cusp type does not move it. But escaping the mod-`k` test does not help
either: the divisibility condition is not what actually kills these
constructions.

---

## 1. The general endgame identity

All framework-specific inputs carried as free parameters:

| symbol | meaning | Borisov |
|---|---|---|
| `(a,b)` | cusp type; `val_E y1 : val_E y2 = b : a` | `(2,3)` |
| `rho` | chart slope, `v = x1·x2^rho − 1`, `q = x2/v^rho` | `3` |
| `k` | boundary multiplicity, `(val_E y1, val_E y2) = −k(b,a)` | `3` |
| `D` | chain degree | `13` |
| `m` | corner order, `m = ord_{U=0} g` | `1` |
| `e` | axis order, `e = ord_{v=0} g`; `sigma := e − rho·k` | `8` (`sigma = −1`) |
| `alpha` | boundary scale | free |
| `c` | Keller constant, `≠ 0` | — |

With `y1 = q^{−bk}Y1`, `y2 = q^{−ak}Y2`,
`K := (−bk·Y1 + q∂_qY1)∂_vY2 − ∂_vY1(−ak·Y2 + q∂_qY2)`,
`g0 := Y2|_{q=0}^{1/a}`, and `R` defined chart-freely by

```
(y1^a − y2^b) / y2^b  =  q^D · R(v) · (1 + O(q)),
```

the leading Keller block is

```
        [q^D] K  =  g0^(a+b) · ( k·R'  +  D·R·(log g0)' )            (*)
```

**The operator is `k·d/dv + D·(log g0)'`. The coefficient of `R'` is `k`.**
`(a,b)` does not appear in it. `D` does not appear in it. `rho` does not appear
in it *at all* — the identity is chart-independent; the chart enters only in the
order matching. Verified on 22 `(cusp type, D)` pairs by two independent routes
plus a third concrete-arithmetic route.

Substituting the rigid boundary shape `g0 = alpha·(v+1)^m·v^sigma`:

```
alpha^(a+b) (v+1)^((a+b)m−1) v^((a+b)sigma−1)
      · [ k·v(v+1)·R'  +  D·((m+sigma)v + sigma)·R ]   =   −c·v^(rho−rho^2)
```

with two order-matching relations obtained by balancing against the chart
factor `det ∂(q,v)/∂(x1,x2) = −x2^rho/v^rho` (re-derived for `rho = 1..8`):

```
(Q)   D = (a+b)·k + 1 − rho
(V)   (a+b)·sigma = 1 + rho − rho^2
```

**Borisov specialization.** `(a,b,rho) = (2,3,3)` gives `sigma = −1` from (V),
hence `e = rho·k + sigma = 8` — i.e. the certified `g = alpha·U·(U−1)^8` comes
*out* of the general relation rather than being put in. `k = 3` from (Q) with
`D = 13`, and (*) collapses to

```
alpha^5 (v+1)^4 (3 v(v+1) R' − 13 R) = −c
```

exactly as certified in Sessions 16–18, both the `3` and the `13` reproduced.

---

## 2. Where the `3` enters — the specialization chain

```
[g0 generic]              g0^(a+b) ( k R' + D R (log g0)' )
[g0 = alpha(v+1)^m v^s]   alpha^(a+b)(v+1)^((a+b)m−1) v^((a+b)s−1)[ k v(v+1)R' + D((m+s)v+s)R ]
[cusp fixed to (2,3)]     alpha^5 (v+1)^(5m−1) v^(5s−1) [ k v(v+1)R' + D((m+s)v+s)R ]   ← still k
[chart slope fixed to 3]  alpha^5 (v+1)^4 v^−6         [ k v(v+1)R' − D R ]              ← still k
[k := 3, D := 13]         alpha^5 (v+1)^4 v^−6         [ 3 v(v+1)R' − 13 R ]             ← 3 appears HERE
```

The coefficient is still the free symbol `k` after the cusp type is fixed **and**
after the chart slope is fixed. It becomes `3` only when `k := 3` is imposed —
that is, only when the boundary valuations are set to `(−9,−6)`.

---

## 3. Consequence: `k` is not a free dial, and the transfer conjecture mis-states it

Relation (Q) inverts to `k = (D + rho − 1)/(a+b)`. Inside Borisov's own family
`(a,b,rho) = (2,3,3)`:

| D | k | machinery's endgame | campaign's transfer conjecture |
|---|---|---|---|
| 3 | 1 | `v(v+1)R' − 3R` | `3v(v+1)R' − 3R` |
| 8 | 2 | `2v(v+1)R' − 8R` | `3v(v+1)R' − 8R` |
| **13** | **3** | `3v(v+1)R' − 13R` | `3v(v+1)R' − 13R` ✓ |
| 18 | 4 | `4v(v+1)R' − 18R` | `3v(v+1)R' − 18R` |
| **23** | **5** | `5v(v+1)R' − 23R` | `3v(v+1)R' − 23R` |
| **28** | **6** | `6v(v+1)R' − 28R` | `3v(v+1)R' − 28R` |

The transfer conjecture holds the coefficient at 3 while the machinery moves it.
Two corroborating facts: (Q) forces `D ≡ 3 (mod 5)` in this family, and every
chain degree the campaign ever tested — 13, 23, 28 — satisfies that congruence,
while 9, 12, 15, 20, 25 are inadmissible; and (V) independently reproduces
`e = 8`, the certified exponent in `g = alpha·U·(U−1)^8`.

The verdicts for D=23 and D=28 are unaffected (`5 ∤ 23`, `6 ∤ 28`, just as
`3 ∤ 23`, `3 ∤ 28`), but the modulus used to reach them was wrong, and the test
is not "mod 3" for any framework other than the First.

**Falsifiable prediction.** If the Second Framework (D=23) is in this family, its
boundary polynomial must have `e = rho·k + sigma = 3·5 − 1 = 14`, i.e.
`g = alpha·U^m·(U−1)^14`, `deg g = 15` at `m = 1` — against `e = 8`, `deg g = 9`
for D=13. For D=28: `e = 17`, `deg g = 18`. This is checkable against the
Second Framework's box data and would confirm or refute (Q) outright.

---

## 4. The divisibility test is real but secondary

Setting the bracket to zero (the `M ≡ 0` branch) gives the general homogeneous
solution

```
R = C · v^(−D·sigma/k) · (v+1)^(−D·m/k)
```

which is rational iff **`k | D·sigma` and `k | D·m`**. At `(D,sigma,m,k) =
(13,−1,1,3)` this is `R = C(v/(v+1))^{13/3}`, the recorded mod-3 test — so the
campaign's "`D/3` must be an integer" is exactly `k | D·m`, with `3 = k`.

But this test is **escapable**. Over the admissible lattice
(`1≤a,b≤5` coprime, `rho≤13`, `k≤9`, `sigma ∈ Z` from (V), `e ≥ 0`), **32
lattice points pass it outright**, including `(a,b,rho,k,D) = (2,3,3,1,3)` and
`(2,3,3,2,8)` inside Borisov's own family. Equivalently, `k | D ⟺ k | (rho−1)`
(exhaustive over `1≤a,b≤7` coprime, `rho,k ≤ 11`); Borisov has `rho−1 = 2`,
`k = 3`, and `3 ∤ 2`.

So: had the campaign's mod-3 test been the whole obstruction, D=3 and D=8 would
have been live candidates. They are not — because of §5.

---

## 5. What actually kills every one of them

**Corner lemma (parameter-free).** In the chart,
`x1^i x2^j = U^i q^n v^(rho·n)` with `n = j − rho·i`, so the block
`A~_n(U) = Σ_i c_{i,n+rho·i} U^i` can only contain monomials with
`j = n + rho·i ≥ 0`. At `n = −bk < 0` this forces `i ≥ ⌈bk/rho⌉ ≥ 1`, so
`U | A~_{−bk} = g^b`, hence `U | g`, hence

```
m  =  ord_{U=0} g  ≥  1        always.
```

Inputs: `y1` is a polynomial (nonnegative exponents) and has a genuine pole
along `E` (`k ≥ 1`). Nothing else — no marking, no dessin, no box caps, no
cusp type. Borisov's `U | g`, previously justified by propagation from the
`{1}`-marked corner, is a *theorem*, not a framework choice.

**The kill.** Since `m ≥ 1` and `a+b ≥ 2` for any nondegenerate cusp, the
`(v+1)`-exponent satisfies `(a+b)m − 1 ≥ 1`. If `R` is regular at `v = −1`, then
`M(−1) = −D·m·R(−1)` is finite, so

```
LHS(v = −1) = 0        while        RHS(v = −1) = −c·(−1)^(rho−rho^2) ≠ 0.
```

Contradiction — **independent of `(a,b)`, `D`, `rho`, `k`, `m`, `sigma` and
`alpha`**. There is no coprime `(a,b)` whatever with `(a+b)m − 1 < 1`; the
sharpest case `(a,b) = (1,1)`, `m = 1` still gives `(v+1)^1`. All 32
divisibility-passing lattice points die here.

**The one escape, stated exactly.** If `R` has a pole at `v = −1`, write
`R = (v+1)^{−p}S` with `S(−1) ≠ 0`. Then

```
M = (v+1)^{−p} [ k·v(v+1)S' + (D(m+sigma) − k·p)·v·S + D·sigma·S ]
```

and the value at `v = −1` is `(k·p − D·m)·S(−1)`. So a Keller pair of this shape
requires

```
p = (a+b)·m − 1        AND        k·p ≠ D·m.
```

For Borisov's First Framework: `p = 4` and `3·4 = 12 ≠ 13`. This is the *entire*
remaining escape route, and it is exactly the gap that Session 13's Theorem 3
(pole-fiber ⇒ `R` polynomial) closes for D=13, and exactly the reason the D=28
case was recorded as "Laurent, not yet polynomial".

---

## 5b. Chart generality — how far the kill actually reaches

The kill compares the LHS's `(v+1)`-order against the RHS's, and the RHS is
`c·delta` with `delta = 1/det`. So the chart matters, and the `rho`-family alone
is not the most general monomial chart. For a general unimodular monomial chart

```
U = x1^P x2^Q,   v = U − 1,   q = x1^P' x2^Q' v^{−w},   eps := PQ' − QP' = ±1
```

the chart factor is (verified on 256 unimodular charts)

```
det ∂(q,v)/∂(x1,x2) = −eps · x1^{P+P'−1} x2^{Q+Q'−1} v^{−w}
```

and the RHS's order of vanishing at `v = −1` is

```
A  =  eps·(Q' − P') − 1.
```

The kill is valid exactly when **`A < (a+b)m − 1`**. Findings:

- Borisov's chart `(1,3,0,1,3)`: `A = 0 < 4`. Valid.
- The entire `rho`-family `(1,rho,0,1,rho)`: `A = 0` for all `rho`. Valid.
- **Every** unimodular chart with `(P',Q') = (0,1)` — transverse coordinate built
  from `x2` alone: `A = 0`. Valid.
- Every chart with `P' ∈ {−1,0,1}`, `Q' ∈ {0,1}`: `A ≤ 3`. Valid.
- `A ≥ 4` requires `eps(Q'−P') ≥ 5` — in the scanned range the only such chart is
  `(P,Q,P',Q') = (1,0,−4,1)`, i.e. `q = x2/(x1^4 v^w)`.

**This is the one residual gap in the universality claim**, and it is named
rather than papered over: whether a chart with `eps(Q'−P') ≥ 5` can carry an
actual resolution of a Keller pair is *not* settled here. The `(c)` finding about
the coefficient is unaffected — the master identity `(*)` is chart-independent,
`rho` provably absent from it.

---

## 6. Answer to the question as posed

- **(a) is false.** The cusp type does not enter the coefficient of `R'` at all.
  Verified over 22 `(cusp type, D)` pairs including `(1,1)`, `(1,2)`, `(3,4)`,
  `(2,5)`, `(5,3)`, `(2,7)`, `(5,9)`: the coefficient was the free symbol `k`
  every time. No cusp type produces a different coefficient, so no cusp type can
  be chosen to make the divisibility condition hold.

- **(b) is not the right description of the coefficient**, though it *is* the
  right description of the obstruction. The `3` is a genuine free parameter of
  the construction (`k`), and lattice points with `k | D` exist. What is
  structurally forced regardless of every parameter is the *other* factor,
  `(v+1)^{(a+b)m−1}` with `m ≥ 1`.

- **(c) is the finding.** The coefficient is the primitive boundary multiplicity
  `k`, a third framework parameter that Borisov's setup happens to also set to 3
  — colliding with `b = 3` and `rho = 3`. The mod-3 test is a *shadow* of the
  real wall: within his family the real wall (`m ≥ 1`) always fires, so the two
  never disagree on a verdict, which is why the coincidence went unnoticed.

**Practical consequence.** Reparametrizing the cusp type, ramification profile,
or box combinatorics cannot rescue this construction — not because the mod-3
test is universal (it is not), but because the `v = −1` evaluation is. The only
target worth attacking is the polynomiality of `R`: a construction in which `R`
has a pole of order exactly `(a+b)m − 1` at `v = −1` with `k·p ≠ D·m`. That is
where the D=28 Laurent case already sits.

---

## 7. Certification ledger

Exact arithmetic throughout (`sympy` rationals and `fractions.Fraction`); no
floating point anywhere in any of the four scripts.

| script | items | result |
|---|---|---|
| `session19_general_endgame.py` | 32 | 32 PASS |
| `session19_parameter_lattice.py` | 18 | 18 PASS |
| `session19_self_audit.py` | 14 | 14 PASS |
| `session19_general_chart.py` | 9 | 9 PASS |
| **total** | **73** | **73 PASS, 0 FAIL** |

Load-bearing items:

- chart factor `−x2^rho/v^rho` re-derived for `rho = 1..8`, and
  `−eps·x1^{P+P'−1}x2^{Q+Q'−1}v^{−w}` on 256 unimodular monomial charts
- master identity `(*)` by Route 1 (Jacobian-silence of `y2^{b/a}`) on 10
  `(a,b,D)` triples with generic `g0`, lower blocks confirmed to vanish
- master identity `(*)` by Route 2 (`J(y1,y2) = J(y1^a−y2^b,y2)/(a·y1^{a−1})`,
  chain-block projection) on the same 10 triples
- operator coefficients extracted and matched: `coeff(R') = k`,
  `coeff(R) = D·(log g0)'`, both routes, all 10 triples
- coefficient of `R'` equals `k` on 22 `(cusp type, D)` pairs
- master identity on 6 fully concrete exact rational-function instances with
  non-Borisov `(a,b,D,k,m,sigma,alpha)` — a third route using no symbolic-function
  manipulation at all
- `d(leading block)/dk = g0^{a+b}·R'` exactly — the coefficient measured, not asserted
- specialization to `alpha^5(v+1)^4(3v(v+1)R' − 13R) = −c`, reproducing the
  Sessions 16–18 certified endgame including both constants
- `sigma = −1` and `e = rho·k + sigma = 8` derived from (V), reproducing the
  certified `g = alpha·U·(U−1)^8`
- corner lemma `m ≥ 1` over all `b,k,rho ∈ 1..7`
- homogeneous solution verified on 225 exact `(D,sigma,m,k)` grid points
- tie-back to the certified Belyi data: `N = p^2 − w·r^3` recomputed to degree 3,
  `n3 = (−128 + 64√−3)/3`, cross-epoch identity `h0 = −13·n3` reconfirmed, and
  the general `R = v^{rho·D}·W̃_{n0}/g^{ab}` shown to equal the campaign's `R = n3`

---

## 8. Mandatory self-audit

**(i) Inherited-input ledger with mechanical leak detection.** Fourteen inputs
enumerated; for each, how it was handled. Leak tests: the free symbols of both
routes' leading blocks are exactly `{k, v}` — no `3`, no `13`, no Belyi datum;
`rho` is provably absent from the master identity.

| inherited input | Borisov value | handling |
|---|---|---|
| cusp type `(a,b)` | `(2,3)` | swept over 22 `(cusp,D)` pairs incl. `(1,1),(1,2),(3,4),(2,5),(5,3),(2,7),(5,9)` |
| chart slope `rho` | `3` | re-derived `rho = 1..8`; provably absent from `(*)`; enters only (Q),(V) |
| boundary multiplicity `k` | `3` | bare symbol end to end, never substituted — **it is the coefficient** |
| chain degree `D` | `13` | instantiated `D = 1,2,3`; appears only as coefficient of `R·(log g0)'` |
| corner order `m` | `1` | symbolic; `m ≥ 1` **derived**, not assumed |
| axis order `e` / `sigma` | `8` / `−1` | symbolic; `e = 8` came *out* of (V), was not put in |
| boundary scale `alpha` | free | symbolic as `alpha^{a+b}`, never simplified away |
| Keller constant `c` | `≠ 0` | symbolic; only `c ≠ 0` used |
| boundary polynomial `g` | `alpha·U(U−1)^8` | replaced by a **generic** `g0(v)`; the `(v+1)^m v^sigma` shape imposed only afterwards |
| ramification profile / dessin | `8×2 / 5×3+1 / 13+3×1` | never used |
| Belyi coefficients `p, r` | certified `Q(√−3)` data | never used; leak test confirms |
| box combinatorics | `[0,27]×[0,72]`, `[0,18]×[0,48]` | used only via "exponents are nonnegative"; the caps `deg g ≤ 9` are **not** used in the kill |
| marked-point structure | `{1}`-marked corner ⇒ `U ∣ g` | **not inherited** — re-derived from polynomiality + pole along `E` |
| chain-block structure | `W̃_n = 0`, `n = −18..−6` | imposed generically as "first `D` blocks vanish", `D` free |

**(ii) Second independent route.** Route 1 goes through the chart factor and the
Jacobian-silence of `y2^{b/a}`. Route 2 goes through the chain-block projection
via `J(y1,y2) = J(y1^a − y2^b, y2)/(a·y1^{a−1})` — no factorization, no
deviation `eps`, no fractional powers, free `A`/`B` towers with the chain
imposed by exact forward substitution. **Both produce the identical operator
`k·d/dv + D·(log g0)'` on all 10 triples.** A third route (concrete exact
rational functions, no symbolic-function manipulation) agrees on 6 non-Borisov
instances. No disagreement anywhere.

**(iii) The general form immediately before specialization.** Printed in §2. At
the last general step the expression is `g0^{a+b}(k·R' + D·R·(log g0)')` with
`g0` a **generic function** — no Borisov substitution is in scope. The
coefficient is still the free symbol `k` after the cusp type is fixed to `(2,3)`
*and* after the chart slope is fixed to `3`. It becomes `3` only at `k := 3`.

**(iv) Confidence: MEDIUM.** Both derivation routes agree cleanly and the
specialization reproduces the certified D=13 endgame exactly, which argues HIGH
for the `(c)` finding itself. Three things are worth a second opinion, named
precisely:

1. **Discrepancy with the recorded transfer results.** Relation (Q) says the
   coefficient for D=23 is `5` and for D=28 is `6`, not `3`. The D=23 result is
   on record as "certified conditional on L2–L4" with coefficient `3`. The
   verdicts agree (`5∤23`, `6∤28` just as `3∤23`, `3∤28`), so nothing previously
   concluded is overturned — but either (Q) is wrong, or the Second Framework's
   endgame coefficient was carried over rather than re-derived. The repo does not
   contain the Second Framework's box data, so I could not settle this here. The
   discriminating check is stated in §3: `e = 14`, `deg g = 15` for D=23.
2. **`R` regular at `v = −1` is a hypothesis, not a theorem.** For D=13 it is
   supplied by Session 13's pole-fiber Theorem 3. In general it is the exact
   escape locus (`p = (a+b)m − 1`, `k·p ≠ D·m`), and it is where the D=28
   Laurent case already sits.
3. **Charts with `A = eps(Q'−P') − 1 ≥ 4`** are not covered (§5b). Borisov's
   chart, the whole `rho`-family, and every single-variable transverse chart have
   `A = 0`, so this does not touch any construction actually on the table.

Not HIGH because of (1); not LOW because the routes agree cleanly, the D=13
specialization is exact, and (2)–(3) are stated scope conditions rather than
holes in the derivation.

---

## 9. Not done (out of scope by instruction)

D=28 surgery, box caps, Fig. 27, cascade, rigidity work, and anything on the
Hessian/HC4 side were not touched. `arXiv:2301.08221` was not cross-checked
against the dessins machinery — it was flagged optional and no search cycle was
spent on it, so nothing is claimed about overlap either way.
