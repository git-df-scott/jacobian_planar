# Session 43 — audit sweep

Prompted by "these results are fast, we've gotten our hands burned from that
before". The sweep was justified: **eight bugs**, one of them biasing in the
dangerous direction, and one process failure that matters more than any of them.

## The process failure, first

I committed and wrote a PR saying the work was validated, but `VALIDATE.py`
**never finished** — it timed out and I never read its output. A validation
suite that has not been read is not evidence. Every claim below was re-derived
after that was noticed.

## Bugs found

| # | Where | What | Which way it biased |
|---|---|---|---|
| 1 | `_n_intersection` | `res(c, g) = c^deg g` reports a **phantom intersection** for a vertical component. `{w2=0}` gave `chi(A)=0` instead of `1`. | suppressed real hits |
| 2 | `meets` | resultant picks up **spurious roots** wherever `lc_y` vanishes: `res_y(1+xy, B) = k·x^(deg_y B)` vanishes at `x=0`, but `{1+xy=0}` has no point with `x=0` and `B ≡ k ≠ 0` there. | manufactured false hits |
| 3 | `keller_residual` (Lane U) | sign error. Caught by the generic-`P,g` identity test before any result was produced. | none (caught) |
| 4 | `pathS_tear_parametrized` | ideal membership used where **radical** membership was meant. Fixed with Rabinowitsch. | none (failed loudly) |
| 5 | `chi_curve` | inclusion–exclusion used **pairwise intersections only**, so a point on ≥3 components is over-subtracted. Three concurrent lines: `chi = 3−3+1 = 1`, code gave `0`. | **wrongly REJECTED candidates** |
| 6 | `leading_form_places` | counted irreducible factors **over Q**, not points over **C**. A binary form splits over C, so `u²+v²` is 2 points at infinity, reported as 1. | inflated `chi`, i.e. false candidates |
| 7 | hit test | a component `f` with `f | B` is a **1-dimensional centre** (S reducible, hence disconnected since S is smooth), reported as an ordinary hit. | manufactured false hits |
| 8 | `_fibre_count_on_orbit` | fibre counts at special values by **mod-p majority vote** rather than exact arithmetic. Produced badly wrong numbers: the non-linear family was reported as `chi = −167, −258`; the exact values are **−3, −4, −5**. | numbers simply wrong |

Bug 5 is the serious one. `chi(S) = 3 − 2·chi(A_W) − #C_W`, so an **under**count
of `chi(A_W)` makes `chi(S)` too **large** and silently discards genuine
candidates — the one failure mode a search must never have.

## What changed after the fixes

`chi` now goes through `chi_exact.py`: no inclusion–exclusion at all (a generic
shear removes vertical components, then one projection plus motivic additivity
handles any number of components), and fibre counts at special values are exact,
via the Euclidean algorithm in the field `Q[U]/(q)` for each irreducible factor
`q` of the special locus. Calibrated against **25** inputs of independently known
value — 17 curves (including the three-concurrent-lines configuration that broke
the old code), 4 leading-form cases, 4 `A^1` cases. 25/25 pass.

The plane scan, recomputed:

| | old (buggy) | corrected |
|---|---|---|
| planes with `chi(S) = 1` | 19 | **90** |
| died on Euler parity/value | 7957 | 7902 |
| died on Chau | 27 | 27 |
| died on `H_1` | 8 | **63** |
| **survivors** | **0** | **0** |

So the verdict survives, but the buggy `chi` had been wrongly rejecting 55 real
candidates; they died only because the `H_1` filter caught them independently.
The old internal numbers must not be quoted.

The non-linear graph family: exact `chi(A_Sigma) = −d` for `Sigma = {w2 = 9w1w3 +
c w3^d}`, not the reported `−167, −258`. Conclusion unchanged (never 1), but far
narrower than claimed.

## The larger correction: this lane was subsumed by a 1986 theorem

Independently of any bug: **Orevkov (1986)** proves a planar Keller map of
geometric degree 3 is an automorphism, and Alpöge's map has geometric degree 3
with fibre-size set exactly `{3,1,0}` (Gao, arXiv:2608.00222, Thm 3.4 — which is
precisely the stratification derived from scratch here). Any slice `S = F^{-1}(W)`
has `F|_S` of geometric degree 3 or 1, so **no slice of Alpöge's map can be a
planar counterexample**, whatever the Euler characteristic says. The scan's
"0 survivors" is a rediscovery of Orevkov, not a new theorem.

The confirmed floor is: geometric degree **2,3,4,5 all excluded** (Campbell 1973;
Orevkov 1986; Domrina–Orevkov 1998 + Domrina 2000; Żołądek, Topology 47 (2008)
431–469), and **6 is open**. So the lane is only alive for source maps of
geometric degree ≥ 6, which do exist (Gallagher; Gao: arbitrarily large
geometric degree in every dimension > 2).

## What survives the audit

- The reduction itself (`S = C^2` for any `Sigma = C^2` ⟹ JC2 false): unaffected.
- The tear parametrization and stratification (8/8 checks): unaffected, and it
  independently reproduces a published theorem on the fibre sizes.
- The `(C*)^2` lemma: a mathematical argument, not a computation.
- Lane U: unaffected — its only bug was caught by a calibration test before it
  produced any number.

## Standing rule added

Do not report a validation suite as evidence unless its output has been read.
Calibrate every instrument on inputs of independently known value **before**
pointing it at the problem, and include at least one input the instrument is
expected to get wrong if the suspected bug is present.

## Fibre structure: what was verified, and what was not

The load-bearing claim under the whole Euler filter is the fibre-size
stratification. Two routes were attempted:

* **The strongest route did NOT finish.** `verify_fibres.py` attempts a lex
  Gröbner over the function fields `Q(w1,w2,w3)` and `Q(mu,r)` — the generic
  point of each stratum. It was **killed at 2400 s without completing**. That is
  a NO RESULT and is recorded as one; it is not a confirmation.
* **The routes that terminate all pass** (`verify_fibres_light.py`, 6/6): the
  parametrization is proved **onto** the tear (exact identity modulo `Delta`),
  and dense sampling at exact rational points gives fibre **3** off the tear (12
  points), **1** on the tear with `mu != 0` (27 points), **0** on `C_sing` (6
  points), and **3** on the `E=0` locus — confirming `E=0` is not part of the
  tear.

The measured fibre-size set is **{3, 1, 0}**, which is exactly Gao
(arXiv:2608.00222) Theorem 3.4 — an independent published statement, derived
here from scratch.
