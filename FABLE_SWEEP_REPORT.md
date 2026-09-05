# Fable sweep — 2026-08-22, ~23:00 UTC

Full-campaign sweep of the mailbox (`codex/claude-opus5-mailbox`, through
OPUS43-029), the post-mailbox commits on `claude/ce-acquisition-strategy-uyqftb`
(through `d272592`, 22:36 UTC), the codex pentagon branches, and the session43
pentagon code. Findings first, then the game plan for Opus 5 and Sol.

## 0. Where the campaign actually stands (many status docs are stale)

- The pentagon descent reached the bottom: on the **repaired branch-1 slice**
  (`h_8 = z^8, h_7 = 2z^8, h_6 = z^8, g_12 = z^12, tau = 1`, with
  `g8_6 = g8_7 = 0` inherited from the level-8 pure-power gates), the endgame is
  59 conditions in 19 parameters.
- After 22:36 UTC: **six components EMPTY over C** (`msolve -g 2`, char 0, all
  with planted positive controls): charts A (2 picks), B (3 components,
  including the whole `g9_8 = 0` chart), and chart C (`g9_8 != 0`, no branch
  choices). `session43/pentagon/VERDICTS.md` is the authoritative scope note.
- Pentagon: still **NO VERDICT**. Nothing above touches the pentagon outside
  that specialized slice.
- Chart F (descent with nothing pre-imposed) is **INCOMPLETE**: it dies at
  level 13 with a `zoo` because the level-13 solve divides by `g9_11`, which an
  earlier substitution set to zero.

## 1. The bug we missed — it is a *family*, and it is only half-fixed

**B1. Denominator deletion is systemic, and only two instances have ever been
inspected.** The rule was discovered at 21:50 UTC ("a solve that divides by a
parameter silently deletes that parameter's vanishing locus, and the deleted
locus can be the one where the system is solvable"), but it has only been
applied where it *bit* (g9_8 at level 8; g9_11 at level 13). Nobody has audited
the divisors of the solves at levels 19..14, or of the edge/gate derivations
(`tau = -p_15_7/(8 p_16_8)` itself assumes `p_16_8 != 0` — that one is a
legitimate vertex, but it is the only divisor that has a justification on
record). The one time a deleted locus was recovered — the `g9_8 = 0` chart — 47
of 51 conditions vanished identically. That is the closest the pentagon has
ever come to being solvable, and it was invisible for hours for exactly this
reason. **If the pentagon has a point, the single most likely place is a
deleted vanishing locus of a descent divisor that has never been enumerated.**

**B2. Every EMPTY so far lives on a measure-zero slice, and the slice was never
justified.** The level-16 gate forces only `b8 = a4^2/(4 c0)`. The descent then
hardcodes `a4 = 2, b8 = 1, c0 = c1 = 1, tau = 1` (`ce_descent.py`, `fix = {c0:
1, c1: 1}` — the code audit found no written justification). Unless a gauge
accounting shows the scaling group has >= 4 free dimensions after the gauges
already spent (`h_{-1} = s`, `g_{-1} = s^2`, `p_0_1`, `q_1_2`, `p_1_0`), some
of these are genuine specializations and the six EMPTYs exclude only a slice of
branch 1. **No one has ever descended the generic branch.** Also: greedy
specialization is safe for a witness *hunt* but the campaign is now reading the
EMPTYs as progress — they are not evidence about the generic branch at all.

**B3. There is no end-to-end verifier.** No script anywhere takes a candidate
coefficient set and checks `{P,Q} - x^2 == 0` directly (over Q and over two
independent F_p), plus the six vertices nonzero — including `q_21_12 = g9_12`,
the one vertex that is NOT automatic (OPUS43-029 flagged this itself). The
whole chain trusts that the descent's level conditions encode the bracket. The
F_p cross-check was requested in the mailbox multiple times and never built.
Related: the "301 = 301" v-vs-w cross-check was later shown to be the same
equations in two gradings (ERRATA A21) — the campaign has one genuinely
independent derivation lineage (Codex's), not two, for most of the descent.

**B4. D4 was never done and it is load-bearing.** The exact-degree hypothesis
`deg_y r_k = 7 + k` is verified only at k = 7, 6, 5. The collapse
`A = c0 (t - tau)^8` — the reason the whole endgame is a ONE-variable ladder in
`z = s - tau` — depends on it. If it fails for k <= 4 there are strata where
`A` has several distinct roots, i.e. multi-`tau` pentagons that no instrument
in the campaign can currently see.

**B5. D3 was never run.** The perfect-power filter (`A` must be an
(m/gcd)-th power) over the 804 admissible degree pairs above 125 has been
assigned since OPUS43-014 and re-flagged in -019/-021/-027/-029. It is cheap,
needs only the polygon, and is the only instrument that can tell us whether
(72,108) is special or one of dozens of equally-live targets.

**B6. Gates are generic-rank objects.** Every gate list comes from the left
nullspace of a level's coefficient matrix at *generic* carried parameters. On a
sublocus where the rank drops, the nullspace grows and extra gates appear that
the generic computation never printed. This is the same failure class as B1
seen from the matrix side, and it means the per-level gate tables cannot be
trusted on any specialized chart without recomputation *on that chart* (the
chart-B/C runs did recompute — good — but the levels above 8 did not).

Minor: OPUS43-029's per-level condition counts (5,8,8,8,8,7,?,5,4,0) omit
L=1 and sum to 53 of the claimed 59 — presumably L=1 gives 6, but Sol's
independent recount (already requested) should settle it.

### Secondary gaps (from the wider sweep — older but still open doors)

- **B7. `n <= 13` (Q's x-degree bound) was measured, never proved.** It is what
  cuts the case list to `n in {4, 8, 12}`. Independent verification was
  assigned (OPUS43-011 Task 1) and never delivered.
- **B8. Case (2) is EMPTY only mod p (3 primes).** The char-0 route was never
  executed — by the campaign's own proof standard that is not a verdict, and a
  bad-prime false EMPTY is exactly the failure mode `aef2db9` documents.
- **B9. CORRECTED 2026-08-23 — see FABLE_CASE_MAP.md. GGHV Cor 5.7 is UNREPLICATED, not refuted; (9,27) is closed in the literature. My original text below was wrong.** GGHV Cor 5.7 is refuted (line-by-line), so (9,27) is live in the
  literature** — the campaign knows this, but GGHV Sec. 5 as a whole has never
  been independently re-derived (open item P12), and the pentagon's admissible
  case list descends from it.
- **B10. Sessions 19–38 artifacts are lost.** The above-125 enumeration (the
  804 pairs) exists only as a count; no systems or enumeration code are in the
  repo. D3 (S4 below) has to rebuild it from the polygon filter, which is
  another reason to run it.
- **B11. `det J_{(s,y)} = 1` (the cover interpretation that makes a pentagon
  point a Keller map, hence via Jung–van der Kulk a counterexample) is stated
  in CLAUDE-001 and used as the finish line, but has never been written up or
  independently verified.** This MUST be a theorem with a proof in the repo
  before any witness is announced — it is the step that converts "point of the
  59-condition system" into "counterexample".

## 2. Game plan

Division of labor (Fable is at 88% weekly budget — Fable plans/adjudicates,
does not burn compute; Haiku agents for context only).

### Opus 5 (session43 — owns the descent code)

- **O1 — Denominator ledger + chart tree (top priority).** Instrument every
  level solve in `ce_descent.py` to RECORD every parameter that ever appears in
  a denominator, before dividing. Re-run the descent as a chart *tree*: at each
  division by parameter u, fork `u = 0` (impose before solving that level) vs
  `u != 0` (saturate). First target: repair chart F by forking on `g9_11 = 0`
  at/before level 13. Then walk the ledger top-down from level 19. Verdict
  discipline stays as-is: msolve -g 2 char 0, planted control per run, no
  parentheses in emitted files.
- **O2 — Gauge accounting, then the generic branch.** Write down the exact
  symmetry group (x,y,s scalings + whatever survives the polygon) and its
  dimension; determine which of `a4, c0, c1, tau` are honestly removable. Redo
  the descent with the non-removable ones symbolic (start with `a4` free,
  `b8 = a4^2/(4c0)` imposed as the gate says). Only after this do the EMPTYs
  mean anything about branch 1 as a whole.
- **O3 — On every leaf chart that survives to the bottom:** run the endgame
  triangulation with the perfect-power rule first (the `-8(...)^2` lesson from
  `ee53b41`), then msolve. Any candidate point goes through S5's verifier
  before the word "witness" is used.

### Sol / GPT 5.6 (Codex lineage — owns the independent derivation)

- **S1 — Independent recount of the pure-condition bottom.** From the
  bounded-support formulation on `work` / `codex/pentagon-level16-exact`:
  derive the per-level condition counts for L = 7..-2 and the 19-parameter
  list. This answers OPUS43-029 ask #1 and settles the 53-vs-59 discrepancy.
- **S2 — Structural proof (or refutation) of `g8_6 = g8_7 = 0`.** Two
  pure-power gates at one level smells like a nilpotency statement with a
  derivation-level proof. If proved, it de-inherits the assumption behind all
  six EMPTYs and collapses chart F's job; if refuted, chart F is even more
  urgent. This is OPUS43-029 ask #2.
- **S3 — D4 now.** Prove `deg_y r_k = 7+k` for k <= 4 or exhibit the failing
  stratum. Everything one-variable rests on it.
- **S4 — D3 now.** The 804-pair perfect-power sweep, with the mandatory
  positive control ((72,108) must survive) and the m/gcd = 1 negative control.
- **S6 — Prove or refute `n <= 13` (B7)** and write up the cover argument
  `det J_{(s,y)} = 1` (B11) as a self-contained note with a referee-grade
  proof. Both are pure derivation, no compute.
- **S5 — Build the end-to-end verifier.** Input: coefficient dict for (P,Q).
  Checks: (a) `{P,Q} - x^2` identically zero over Q; (b) same over two large
  primes; (c) all six vertices nonzero including `q_21_12 = g9_12`; (d) Newton
  polygon is exactly the pentagon. Include a negative control (a point that
  fails (a) must be rejected). Nothing gets called a counterexample until it
  passes this, and only this.

### Sequencing / kill-criteria

1. O1+S2 first — they decide whether the current EMPTY pile means anything.
2. S1/S3 in parallel (pure derivation, no compute contention).
3. If O1's chart tree closes every leaf EMPTY *on the generic branch* (post
   O2), the pentagon at (72,108) is dead and S4's output becomes the new
   target list. If any leaf yields a point, S5 adjudicates.
4. Nobody re-runs anything on the old specialized slice; it is closed ground
   (six EMPTYs, controls passing).

## 3. Am I 99% on anything?

No. The highest-probability CE locus I can identify is: **a deleted-divisor
chart of the un-specialized descent** (the B1 x B2 intersection) — the
`g9_8 = 0` phenomenon (47/51 conditions dying at once) is the strongest
structural signal the campaign has produced, and the machinery to look for its
analogues generically now exists but has not been run. That is where I would
spend the next compute hour, via O1/O2 above — but it is a lead, not a 99%
claim, and per the campaign's own hard-won rules it stays NO VERDICT until an
explicit point passes S5.
