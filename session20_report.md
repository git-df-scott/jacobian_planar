# Session 20 — Direct hunt for a JC2 counterexample

**Result: no counterexample found.** Expected. What the session did produce is one
significant correction to the campaign's premise, three new structural results,
and a retargeting.

---

## 0. The correction, first, because it reframes everything

A literature sweep on degree constraints (a question no prior session had asked)
turned up:

> **Guccione–Guccione–Horruitiner–Valqui, arXiv:2204.14178 (2022), Thm 2.1.**
> If `(P,Q)` is a counterexample to JC2 then either `max(deg P, deg Q) ≥ 125`,
> or `(deg P, deg Q) ∈ {(72,108),(108,72)}`.

And their **Theorem 5.1 / Corollary 5.7 excludes (66,99) outright** — a general
argument over all Keller pairs of that shape, not restricted to any construction.

**(66,99) is the degree pair Sessions 7–19 were built around.** It has been closed
in the literature since 2022, by an unrelated and more elementary method.

This does not make the Session 19 mathematics wrong. It does mean:

- The Session 16–18 "First Framework emptiness" theorem is **correct but strictly
  weaker** than a published 2022 result — it kills one construction at a degree
  pair that was already known to admit nothing at all.
- The Session 20 escape hatch found below, at `D = 13`, is **provably empty for
  external reasons**: there is no `(66,99)` Keller pair, escape or no escape.
- The campaign's framing of `(99,66)` as live ("Moh's last troublesome degree
  pair", "the contested case") was accurate as of Borisov's 2019 paper and stale
  thereafter.

Borisov's Remark 3.1 was confirmed verbatim against the primary source, so the
*history* the campaign recorded is right; what was missing is the 2022 resolution.

Current frontier: **(72,108)** is the unique admissible pair below 125. Above 125,
no exhaustive sweep exists.

---

## 1. Cusp type is not a free parameter (`jc2_cusp_from_degrees.py`, 10/10)

`J(P,Q) = 1` forces `J(P̄,Q̄) = 0`, hence `P̄^{d₂} = c·Q̄^{d₁}`, hence by unique
factorization

```
P̄ = α·h^{d₁/n},   Q̄ = β·h^{d₂/n},   n = gcd(d₁,d₂),   deg h = n
```

so the Session 19 cusp type is `(a,b) = (d₂/n, d₁/n)` — **determined by the degree
pair**. `(99,66) → (2,3)`, matching the `(3,2)` valuation proportionality Session
15 recorded as a "discovery". It was never a choice.

This closes **option (a) of the Session 19 question a second, independent time**:
not only does the cusp type fail to move the endgame coefficient, it is not a dial
at all.

**Jung–van der Kulk collapse.** Every automorphism of `C²` is tame, and a tame
automorphism has one degree dividing the other. So the entire search target is

> find `P,Q` with `J(P,Q) = 1` and `deg P ∤ deg Q`, `deg Q ∤ deg P`

with **no automorphism test needed** — only exact degrees.

---

## 2. The Session 19 escape hatch is inhabited (`jc2_escape_hatch.py`, 22/22)

Session 19 proved the endgame kills everything *unless* `R` has a pole at `v = −1`
of order exactly `p = (a+b)m − 1` with `k·p ≠ D·m`, and left that escape
unexamined. **It is non-empty.**

For the First Framework `(a,b,k,D,m,σ) = (2,3,3,13,1,−1)`, `p = 4` and the escape
ODE has the explicit solution

```
R(v) = S(v)/(v+1)^4,   S(v) = −243v⁴ + 81v³ − 54v² + 42v − 35
```

with `(v+1)⁴(3v(v+1)R′ − 13R) = 455` exactly, i.e. `c = −455α⁵ ≠ 0`. Side
condition holds: `3·4 = 12 ≠ 13`.

- **Unique up to scale**: the homogeneous solution `C(v/(v+1))^{13/3}` is
  irrational, so nothing can be added to it.
- **Lattice-compatible**: needs `ord_{U=0} W̃₋₅ = 2`; the support lattice permits
  as low as 2. (The near-miss sits at 6.) Forced block:
  `W̃₋₅ = α⁶·U²·(U−1)⁹·S(U−1)`, degree 15 — same degree as the near-miss, and not
  the 28 the 13-realization demands, exactly as a non-realizing branch should be.
- **Open at 13 of 40 lattice points**, including `D = 13, 23, 28` — because
  `m + σ = 0` makes `k | D(m+σ)` automatic for every `k`. The governing
  divisibility in this branch is `k | D(m+σ)`, **not** `k | D`.

**Consequence.** The endgame equation *alone* kills nothing. The Sessions 16–18
kill rests entirely on Session 13's Theorem 3 (`R` is a degree-13 polynomial),
which is a Belyi/dessin realization condition, not chart machinery. The emptiness
theorem stands; what changes is where its weight is borne.

*A retraction made during the work:* I briefly thought the cascade
`W̃₋₅ = 2g³(Ã₄ − g³S₁₃)` forced `g³ | W̃₋₅` and killed the escape. It does not —
`S₁₃` is not polynomial (`S₁₃ = −n₃v⁻³⁹/2`), and the near-miss itself fails that
divisibility.

---

## 3. New lattice relation, and (72,108) (`jc2_target_72_108.py`, 20/20)

Recovered from the campaign's own box data: with `x1`-extents `(bG, aG)` and
`x2`-extents `(bH, aH)`,

```
G = deg g = b·k,        n = G + H = b·k + H,        D = (a+b)k + 1 − ρ
```

**Retrodiction:** at `n = 33` this gives `k = 3,5,6 → D = 13,23,28` — precisely
and only the three chain degrees the campaign ever encountered, which was
previously unexplained.

Applied to **(108,72)**: `n = 36`, cusp `(2,3)` — *identical* to `(99,66)`, so the
Session 19 endgame transfers verbatim. Chain-degree lattice `D = 5k − 2`,
`k = 1..12`, i.e. `D ∈ {3,8,13,18,23,28,33,38,43,48,53,58}`.

| | |
|---|---|
| all 12 points | die immediately unless `R` has a pole of order exactly 4 at `v = −1` |
| **`k = 2`, `D = 8`** | **killed outright** — `k·p = D·m = 8`, so the `v = −1` residue `(kp − Dm)S(−1)` vanishes and the escape degenerates |
| other 10 | open at the endgame level |

Closed form: `p = 4`, `D = 5k − 2`, so `kp = Dm ⟺ 4k = 5k − 2 ⟺ k = 2`. Exactly
one chain degree in the whole family is self-killing, and `(72,108)` contains it.

---

## 4. Direct exhaustive search (`jc2_exhaustive_search.py`, `jc2_modular_search.py`)

Exact Gröbner decision per degree pair — leading forms normalized by GL₂, `β ≠ 0`
saturated by Rabinowitsch so degrees are exact, multi-prime modular variant with a
Frobenius guard (`p > max degree`, since JC is false in char `p`).

**Honest coverage: 4 degree pairs decided** — `(3,2)`, `(4,3)`, `(5,2)`, `(5,3)` —
all `EMPTY`. `(5,4)` and beyond blow up in coefficient growth and did not finish.

This is **pipeline validation only, with no mathematical content**: everything in
range is far below Moh's bound, and the 2022 literature result (`max ≥ 125` except
`(72,108)`) makes brute force at these sizes moot. Reported because the coverage
is what it is, not because it establishes anything.

### 4b. Tractability of the raw Keller system — a useful negative result

Singular 4.x was installed and benchmarked against the same wall. Sanity-checked
first (returns `_[1] = 1` on an inconsistent ideal, correct basis sizes on toy
systems), so the engine is sound.

On the `(5,4)` Keller system — 25 equations, 23 unknowns after normalizing both
leading coefficients to 1 (WLOG over `C`: `(P,Q)→(sP,Q/s)` and `(x,y)→(ux,vy)`
with `uv = 1` normalize both, and triviality of the ideal over `Q` still decides
emptiness over `Q̄` by the Nullstellensatz) — **Singular does not finish in 100
seconds either.** Same wall as sympy, one degree pair past `(5,3)`.

**Conclusion: the bottleneck is the formulation, not the engine.** The raw
Keller-coefficient ideal is intractable by general-purpose Gröbner methods at
degrees an order of magnitude below the frontier. This is precisely why the
literature attacks JC2 through Newton-polygon combinatorics rather than direct
elimination, and it means **Path A's feasibility rests entirely on GGHV's
*reduced* system being small** — not on throwing more compute at the problem.
Any plan of the form "install a better solver and grind" is dead on arrival.

---

## 5. Scorecard

**Found:** no counterexample.

**New this session:** cusp type is degree-determined; the search target reduces to
a pure degree condition; the escape hatch is inhabited with a unique explicit `R`;
the lattice relation `n = bk + H` and its retrodiction of `D = 13,23,28`; a
12-point analysis of `(72,108)` closing exactly one point.

**Corrected:** `(66,99)` is not open and has not been since 2022; the campaign's
flagship target was already settled.

**Where a counterexample would have to be:** `(72,108)` with `max ≥ 125` the only
other territory. Within the chart/blowup geometry, it must have `R` with a pole of
order exactly `(a+b)m − 1` at `v = −1` and must fail the realization layer. Ten
of the twelve `(72,108)` chain degrees survive everything this session could throw
at them.

**Prior, stated plainly:** low. The 2022 authors set up the polynomial system for
`(72,108)` and could not solve it; there is no reason to think the chart route is
easier, and this session's machinery reaches only one of its twelve points.
