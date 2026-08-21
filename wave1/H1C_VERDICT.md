# H1c — the Three-dessin Framework at (108,72): VERDICT

**Status: CONDITIONALLY DEAD.** The endgame obstruction applies, and it is now
proved uniformly rather than extrapolated. What remains conditional is named
exactly, and it is narrower than Plan 43 assumed in one place and wider in
another.

No counterexample. Nothing promoted from mod-p to ℚ. Nothing here closes
(72,108) — only its **framework side**.

---

## 1. What Plan 43 asked

> *"Reconcile with PR#1's claim that the 'complicated framework' at (108,72)
> reuses the FF D=13 Belyi map — if its chain degree is 13, the endgame
> obstruction conditionally kills it, but the condition (rigidity-layer
> transfer, Theorem 2/3) was never established for this framework;
> establishing OR refuting that condition is decisive either way."*

## 2. The degree ledger, read from the source

All four degrees below are quoted from arXiv:1901.04073v2 directly, not from
any campaign file. `pdftotext -layout`, verbatim.

| framework | (−5)-curve Belyi map | (−2)-curve Belyi map | chain degree `D` | Keller degrees |
|---|---|---|---|---|
| First | 16 | **13** | 13 | (99,66) |
| Second | 28 | **23** | 23 | (435,290) |
| **Three-dessin** | = First's (16) | **= First's (13)** | **13** | **(108,72)** |

Borisov, §5, verbatim: *"This framework has three rational Belyi maps… Two of
them, for the (-5)-curves and the (-2)-curves are the same as those in the First
Framework. The third one, for the (-1)-curves, has degree 5…"* and *"it is not
hard to figure out the pair of degrees of the possible Keller map: (108, 72)."*

**The identification `D = deg((−2)-curve Belyi map)` is not a coincidence of two
examples.** Borisov arranges coordinates in *both* frameworks so that the
(−2)-curve map *"is given by a polynomial"*, and the campaign's realization layer
demands precisely that `R` realize **a degree-`D` polynomial Belyi map**
(`phase2_moduli/README.md`; `d23_phase2_preview.py`). The (−2)-curve map is that
object. It matches on both published data points, 13 and 23.

**The third dessin does not move `D`.** It sits above the **(−1)**-curves, a
different curve class from the (−2)-curves that carry the chain degree. Its
degree is 5, and it is certified exactly in `wave0/w0_h1c_borisov_belyi.py`
(degree 5, ramification (5)/(3,2)/(2,1,1,1) over ∞/0/1, critical values exactly
{0,1}, defined over ℚ).

Hence **`D = 13` for the Three-dessin Framework**, and `3 ∤ 13`.

## 3. The endgame obstruction, upgraded from ledger to theorem

The campaign certified the endgame per-degree by linear algebra: at `D = 13`
"kernel trivial, rank 14", at `D = 23` "kernel trivial, rank 24", plus a
leading-exponent argument (`3n = D` insoluble) for the `M ≡ 0` branch. Two data
points and a bound; the family-wide claim was an **extrapolation** from them
(`d23_phase2_preview.py` says so in its own docstring).

It is now a theorem. `wave1/w1_h1c_endgame_closed_form.py`:

> **THEOREM.** For every integer `D ≥ 1` and every `k ≥ 0`,
> `(v+1)^k ( 3v(v+1)R′ − D·R ) = −c` with `c ≠ 0`
> has a rational solution `R` of degree `≥ 1` **iff `k = 0` and `3 | D`.**

*Proof.* The homogeneous equation integrates: `R′/R = (D/3)(1/v − 1/(v+1))`, so
`R = C·(v/(v+1))^{D/3}` — rational iff `D/3 ∈ ℤ`. `R = c/D` is a particular
solution, so the general rational solution is `R = c/D + C(v/(v+1))^{D/3}`. For
`k ≥ 1`, evaluate at `v = −1`: the left side vanishes, forcing `c = 0`. ∎

Verified by direct substitution for **symbolic** `D`, and it reproduces both
campaign ledgers exactly as corollaries (rank 14 at `D=13`, rank 24 at `D=23`,
kernels trivial — recomputed here from an independently built matrix). The
operator is injective on polynomials *precisely* when `3 ∤ D`, and the closed
form explains why: its only homogeneous solution is then non-rational.

**Consequences.**
* The obstruction is **uniform in `D`, with no ceiling and no per-degree
  computation**. Plan 43's "certified general-D lemma" is now earned.
* `L4`'s role — pinning the specific `k` — is **immaterial**, as the D=23 report
  already suspected: *every* `k ≥ 0` dies, for *every* `D` with `3 ∤ D`.
* Plan 43's **H7 `3|D` loophole is exact**, not heuristic: the obstruction
  vanishes **if and only if** `3 | D`. Every published framework has
  `D ∈ {13, 23}` — now source-verified — and neither is divisible by 3. The
  loophole is real and **unpopulated by anything Borisov published**.

## 4. What is still conditional, exactly

From `D23_phase1_report.md`, the layers separating "mechanism applies and kills"
from an unconditional theorem, with FF's session that built each:

| layer | content | Three-dessin status |
|---|---|---|
| L1 chart | (q,v)-chart, chart factor, Keller form | **needs rebuild** — chart follows the chain, and the target graph differs |
| L1 boxes | total-degree support boxes | **needs rebuild** |
| L2 | block-level chain unification, valuation → block cascade, sqrt-reduction | **needs rebuild** |
| L3 | boundary rigidity, Taylor pins forcing `g = αU v^m` | **needs rebuild** |
| L4 | pole-fiber/realization theorem, Keller pairing fixing `k` | **IMMATERIAL** — §3 kills every `k ≥ 0` |

**Why they do not transfer for free, unlike the isotopes.** PR#1 could transfer
L1–L3 to the isotope series because those share the **same target graph** as the
First Framework (Borisov: the isotopes *"will have the same target graph"*), so
same Y-side chain, same contact, same chart, same rigidity data — leaving only
the box-cap census open. The Three-dessin Framework does **not** share it: it has
a **third forked vertex** and, in Borisov's words, *"Interestingly, it has no
curves of type 4."* A different curve inventory is a different chain, so L1–L3
must be rebuilt on its own data.

This is precisely Plan 43's L8 *"FF-specific transfer never performed"*, now
located to three named layers instead of a general worry.

## 5. A2.8 reconciled

Plan 43 flags FRAMEWORK.md's uniform closure and the D=23 conditional DIES as
unreconciled, and warns one of them over- or under-claims. **Neither does.** They
are two arguments at two strengths over two different scopes:

1. **Belyi-gate + contact-exponent closure** — unconditional, but scoped to the
   cusp-chain family the campaign parametrised, template `(3+12a, 6+12b)` with
   `2a−3b=1` = `(27,18), (63,42), (99,66), (135,90), …`. **`(108,72)` is not in
   this template** (checked: `12a = 105` has no integer solution), and Session 23
   says so in its own words: *"(72,108) … is not reachable by this campaign's
   template … The campaign says nothing about it."*
2. **The `3 ∤ D` endgame obstruction** — reaches any framework whose chain degree
   is known, hence the Three-dessin Framework at `D = 13`, but **conditional on
   L1–L3**.

The apparent conflict was a scope ambiguity, not an error. Recorded as resolved.

## 6. Verdict

> **The Three-dessin Framework at (108,72) DIES, conditional on L1 (chart +
> boxes), L2 (block cascade) and L3 (rigidity pins) being rebuilt on its own
> three-dessin, type-4-free chain.** The endgame obstruction itself is
> unconditional and now proved uniformly in `D`; `L4` is immaterial.

**What this does and does not settle.** It does not close `(72,108)`. Borisov's
frameworks are *sufficient* combinatorial data for a hypothetical Keller map, not
*necessary* — a counterexample at (72,108) need not come from any framework, and
Orevkov (Steklov 235, 2001) is the standing warning that at-infinity data can
pass every combinatorial test and still not extend to a polynomial map. The
pentagon system (H1b) is the non-framework route and remains undecided.

**Next, in order of decisiveness:**
1. Rebuild **L3** first, not L1. Rigidity pins are the narrowest layer and the
   one that failed to transfer in the D=23 case; if `g = αU v^m` cannot be pinned
   on a type-4-free chain, the conditional kill is *refuted* and the framework is
   **alive and constructive** — the strongest possible outcome for the hunt.
2. Then L2, then L1's boxes.
3. Independently: verify `D = deg((−2)-curve map)` is a *theorem* of the chain
   construction, not a two-point pattern. If the Three-dessin chain degree is not
   13, everything in §3–4 re-opens; if it were divisible by 3, the obstruction
   vanishes outright.
