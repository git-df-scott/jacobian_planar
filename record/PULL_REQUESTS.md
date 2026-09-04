# Pull-request archive

Frozen descriptions and discussion entries for all 26 PRs visible at the cutoff. Original claims, status words and running-job statements below are historical; use JC2_COMPLETE_RECORD.md and RECORD_CORRECTIONS.md for current interpretation. Nothing here sends a message or changes a PR.

## PR #1 — D=23 transfer test: Borisov Second Framework (Phase 0 → 1 → 2)

[Original pull request](https://github.com/git-df-scott/jacobian_planar/pull/1) · state `open` · created `2026-08-08T05:02:59Z` · updated `2026-08-12T18:40:05Z`

Head: `claude/d23-borisov-transfer-test-vpr3m6` at `7296164f70765387952fc49ed385b1fff59d2533`. Base: `main`. Merged: `None`.

### Original description

Session N2 (+continuation): testing the Sessions 16–18 transfer conjecture against Borisov's Second Framework (chain degree D=23, target degree pair (435,290), arXiv:1901.04073 §4).

## Phase 0 — COMPLETE (with completeness)

The degree-23 (-2)-curve Belyi map derived + certified exactly for **all 15 dessins at once**: Shabat form `B = c·t·a³·b⁵`, master equation `ab + 3ta'b + 5tab' = 23(t−1)⁶`; eliminant **irreducible of degree 15** ⇒ single Galois orbit (3 real embeddings = the 3 symmetric dessins); ledger 12/12 PASS (PARI/GP + sympy); completeness proven; **Borisov's Fig. 28 dessin identified** (β ≈ 0.1250089).

## Phase 1 — endgame certified; verdict: conditional DIES

`T₂₃,ₖ(R) = (v+1)ᵏ(3v(v+1)R′ − 23R) = −c` impossible for every k ≥ 0; M≡0 branch killed by 3n = 23 ∉ ℤ; D=13 regression matches Sessions 16–18. Chain data certified (harmonicity, projection formula 23·F·F′ + 5 sections = 28; **two paper typos found**, forced by harmonicity); chain layer = exactly 23 vanishings (contact −7, depths 23·{1..9}); (q,v)-chart + Keller form transfer verbatim. **Verdict: mechanism applies and produces the contradiction — DIES conditional on L2–L4.**

## Family-wide

Every chain degree in Borisov's published catalogue (First Framework, isotopes k=2..6, "complicated" framework, Second Framework) lies in **{13, 23}** — none divisible by 3: the certified T₁₃/T₂₃ operators conditionally kill the entire family.

## N3 (continuation leg) — the SF (−5)-curve map (P,R): DONE exactly

- **h-invariant bilinear formulation** + structural identity `P·h = RwN′ − (R+3wR′)N`; **h₀ ≠ 0 saturation theorem** (forces deg N = 5, coprimality, R squarefree, …); **cross-epoch identity h₀ = −D·n_{m−d} proven in general** (FF's certified h₀ = −13n₃ now a corollary; SF: h₀ = −23n₅).
- **msolve** (validated by recovering the certified FF pair as a degree-2 eliminant in 0.03 s): SF solved in milliseconds — eliminant **irreducible degree 14, zero real roots**: all 14 SF dessins form one Galois orbit, **all chiral** (explains the 1.19M-restart real-slice search zero); completeness via 8-strata sweep. **11/11 exact certification ledger over K₁₄** including the 23-fold miracle cancellation deg(P²−wR³) = 5.
- **Miracle-Jacobian theorem**: J = −h(w)·x₁⁴x₂¹² for the (3,2)-prefactor shape, proven for arbitrary P,R — and proven **unique** (general-prefactor formula derived). Session correction, caught by the support certification: for SF this map is **Laurent** (deg P = 14 > 8), so the polynomial near-miss requires the long-branch surgery — whose reconstruction ladder is now recognized as **Fibonacci** ((60,40), (105,70), (165,110), (270,180), (435,290)). Laurent object's layer-1 anchoring certified 5/5 (saturation (−15,−10), all 460 (−5)-pole conditions, G-blocks = P(w)/w², R(w)/w exactly).
- SF layer-1 decision system built (exact ranks 314/144); box caps queued for the N4 surgery analysis.

**N4 queue**: polynomial near-miss via the surgery → box caps → Fig. 27 dessin ID → L2 (cascade) → L3 (rigidity) → L4 → unconditional D=23 closure.

### Archived discussion

0 entries; full normalized metadata in PR_DISCUSSIONS.json.

## PR #2 — Sessions 19–20: mod-3 wall re-derived (verdict (c)); (66,99) closed since 2022; retarget to (72,108)

[Original pull request](https://github.com/git-df-scott/jacobian_planar/pull/2) · state `open` · created `2026-08-12T21:30:21Z` · updated `2026-08-13T02:30:01Z`

Head: `claude/mod-3-keller-pair-obstruction-oceq9z` at `70025d3c5d81080e90f138921a89832778d1d390`. Base: `main`. Merged: `None`.

### Original description

Two sessions. Session 19 answers the mod-3 question; Session 20 hunts a counterexample directly and turns up a correction that reframes the campaign.

## Session 19 — the mod-3 wall: verdict **(c)**

The `3` in `3v(v+1)R' = D·R` is **`k`, the primitive multiplicity of the boundary valuation vector** `(val_E y1, val_E y2) = −k·(b,a)`. In the First Framework `(9,6) = 3·(3,2)`, so `k = 3` — colliding with the cusp exponent `b = 3` and the chart slope `ρ = 3`. It is neither of those.

Master identity, every framework input free, two independent routes plus a third concrete-arithmetic route:

```
[q^D] K  =  g0^(a+b) · ( k·R'  +  D·R·(log g0)' )
```

`ρ` is provably absent from it. Specializing reproduces `α⁵(v+1)⁴(3v(v+1)R′ − 13R) = −c` exactly and *derives* `σ = −1`, `e = 8`, i.e. the certified `g = αU(U−1)⁸`.

- `k = (D+ρ−1)/(a+b)` is determined, not free: D=23 → `k=5`, D=28 → `k=6`. Verdicts unaffected, modulus wrong.
- The mod-`k` test is escapable — 32 lattice points pass it.
- What kills every case is the corner lemma `m ≥ 1` (forced by `y1` polynomial + pole along `E`), making `(v+1)^{(a+b)m−1}` vanish at `v = −1` against `−c ≠ 0`.

Confidence MEDIUM, three caveats named in `session19_report.md`.

## Session 20 — direct hunt

**No counterexample found.**

### The correction that reframes the campaign

**GGHV, arXiv:2204.14178 (2022), Thm 2.1:** a counterexample has `max(deg P, deg Q) ≥ 125`, or the pair is `(72,108)/(108,72)`. Their **Thm 5.1/Cor 5.7 excludes (66,99) outright**, generally.

**(66,99) is the pair Sessions 7–19 were built around, and it has not been open since 2022.** The Sessions 16–18 emptiness theorem is correct but strictly weaker than the published result. Borisov's Remark 3.1 was confirmed verbatim, so the recorded *history* is right; the 2022 resolution was what was missing. 52/52 exact checks.

### New results

1. **Cusp type is degree-determined.** `J(P̄,Q̄)=0 ⇒ P̄^{d₂}=cQ̄^{d₁} ⇒ (a,b) = (d₂/n, d₁/n)`. `(99,66)→(2,3)`. Closes Session 19 option (a) a second, independent time. Plus the Jung–van der Kulk collapse: the search target is just `J=1` with non-dividing degrees, no automorphism test.

2. **The Session 19 escape hatch is inhabited.** Explicitly, for `(2,3,3,13,1,−1)`:
   ```
   R(v) = (−243v⁴ + 81v³ − 54v² + 42v − 35)/(v+1)⁴,   (v+1)⁴(3v(v+1)R′−13R) = 455
   ```
   Unique up to scale (the homogeneous solution is irrational), lattice-compatible, open at 20 of 40 points including D=13,23,28. **So the endgame equation alone kills nothing** — the Sessions 16–18 kill rests entirely on Theorem 3 (`R` polynomial), a Belyi realization condition.

3. **Lattice relation `n = b·k + H`**, which retrodicts exactly why the campaign only ever met `D = 13, 23, 28` (`k = 3,5,6` at `n = 33`).

4. **(72,108) analysis.** Same cusp `(2,3)`, so the endgame transfers verbatim. Chain lattice `D = 5k−2`, `k = 1..12`. Exactly one point — `k=2`, `D=8` — is killed outright (`kp = Dm = 8`). Eleven remain open.

### Search coverage, stated honestly

`jc2_exhaustive_search.py` / `jc2_modular_search.py` decided **4 degree pairs** — `(3,2)`, `(4,3)`, `(5,2)`, `(5,3)`, all `EMPTY` — before Gröbner coefficient blowup. Pipeline validation only, no mathematical content. Log committed rather than overstated.

## Certification

Exact arithmetic, no floating point anywhere. 73/73 (Session 19) + 52/52 + 10/10 + 22/22 + 20/20 (Session 20).

Full write-ups: `session19_report.md`, `session20_report.md`.

### Archived discussion

0 entries; full normalized metadata in PR_DISCUSSIONS.json.

## PR #3 — Counterexample audit campaign: night plan + Sessions 19–20 verification run

[Original pull request](https://github.com/git-df-scott/jacobian_planar/pull/3) · state `open` · created `2026-08-13T03:15:10Z` · updated `2026-08-15T22:21:11Z`

Head: `claude/counter-example-audit-dnu9l9` at `b0bd0ad2d6897dace65e8e6dbb7f7d5b32c5ebcd`. Base: `main`. Merged: `None`.

### Original description

## What this PR is

The staging branch for tonight's JC2 counterexample campaign. First commit is `NIGHT_PLAN.md` — a six-track concurrent plan (soundness gate, the (72,108)/(8,28) branch hunt including the unfinished r0, Phase-4 direct construction, above-125 frontier, literature verification, synthesis/gate) with a wave schedule that paces usage across the night and hard rules against result inflation.

All subsequent commits will be the night's work: reconstruction code, branch certificates, and the morning `AUDIT_REPORT.md` with one of four defined outcomes (counterexample / survivor / closure / partial).

## Context

- Sessions 1–18 (in-repo report): certified emptiness of Borisov's First Framework at (99,66).
- Sessions 19–20 (handoff): retarget to (72,108) shape (8,28) — the unique GGHV-admissible pair below 125 — 6 of 7 branches dead mod p, r0 unfinished, soundness audit outstanding. None of those files were committed; everything gets rebuilt from primary sources here.

---
_Generated by [Claude Code](https://claude.ai/code/session_01S16hvx8YXLFQXDUhAX6ZH5)_

### Archived discussion

1 entries; full normalized metadata in PR_DISCUSSIONS.json.

```json
{
  "body": "## Handoff from the OPUS_PLAN priority-queue session\n\nFull detail: **`HANDOFF_TO_AUDIT.md`** on `claude/opus-plan-priority-queue-0pultj` (PR #4, based on this branch).\n\n```\ngit fetch origin claude/opus-plan-priority-queue-0pultj\ngit show origin/claude/opus-plan-priority-queue-0pultj:HANDOFF_TO_AUDIT.md\n```\n\nTwo findings bear on the work in flight here.\n\n### 1. The polygon recipe gate is empty — P3 is blocked, not slow\n\nThe above-125 Newton polygons are **published nowhere**.\n\n- 1708.07936 §6 gives **chain data only** — A0, A1, (m,n), max degree. No polygon appears in those tables.\n- GGHV 2204.14178 §4 gives explicit polygons for exactly four shapes, **all below 125**: Prop 4.1 (9,27), 4.2 (9,24), 4.3 (8,28), 4.4 (7,21).\n- Its derivations are case-by-case by hand, with automorphisms chosen per case — *\"we apply some automorphisms reminiscent of the procedure in section 8 of the ArXiv version of [6] … in order to greatly reduce their sizes\"*. **There is no general recipe** from chain data to a polygon pair.\n\nP3b–P3d are built and pair-agnostic; their input has to be manufactured by redoing GGHV's §4 geometry for chains they never treated. A guessed polygon yields a system that is not the case in question, and an EMPTY verdict on it would read as a bound improvement.\n\n### 2. Two prose theorems did not survive certification, and one is load-bearing\n\nSessions 11–14's executable engines died with the transcripts, so they were re-derived rather than imported. THEOREM 1 (sqrt-reduction) is now certified and **anchored against Track-F-certified data**: on the near-miss, `A~_{-9+m} == g^3 S_m` at all thirteen levels, and `B~_-6 = U^2(U-1)^16` gives `g = U(U-1)^8` derived rather than assumed.\n\nBut:\n\n- **THEOREM 2** (total rigidity) holds only *at* the near-miss. One worked point is not a rigidity proof.\n- **THEOREM 3** (pole-fiber ⟹ R is a polynomial) is **not reproduced at all**. C1 forces the pole *order*; the fiber-counting step that makes R a *polynomial* runs on D=13's Belyi fiber sizes (13/9/5/1), which (72,108) does not share.\n\n> Every (72,108) statement that assumes a polynomial R inherits this gap — including this session's own C2 table of ten forced R's.\n\n### Also carried\n\n- **C2:** the handoff's `D = 3k+4` is **wrong**. Derived from C1's order matching, `D = (a+b)k + 1 - s = 5k − 2`. They agree only at k=3; under the guessed relation k=4 returns `DEAD_resonance` — the wrong D **manufactures a spurious death**. Our k=3 forced S matches the handoff's exactly; the sign of c does not (+455 vs −455, convention).\n- **C4 refined sweep:** 22 of 23 slices carry a forced R; the only death is the degenerate (1,2). The ODE layer discriminates nothing.\n- **P1 exact-Q:** STALLED, blockage localized to **one** computation — the char-0 edge eliminant. The monolithic chart is hard *even mod p* (no output in 10 min), which is why P1's fallback was never going to work. msolve is mid multi-modular reconstruction and reports elimination polynomial **degree 1144** — this campaign's own number from the \"vdim 1144 / deg-43 eliminant\" story.\n- **P0:** STALLED with numbers. Level 17 costs 79 s/150 MB; level 16 doesn't finish in 1400 s, with nine levels below it. No verdict on case (1).\n- **P2 leaf 1:** 21 branches EMPTY across three primes, still running; leaf 1's eliminant reproduces ELIMDEG 43.\n- **Environment:** containers can come up with **no Singular**; lifetime ~1–2.5 h measured; modStd ignores `system(\"--cpus\")` and forked 15 Singulars on 4 cores.\n\nNo counterexample, no non-EMPTY verdict anywhere, nothing reached the gate. **Case (2) is closed mod p at three primes and STALLED over ℚ — not certified.** The three-prime mod-p closure was deliberately *not* promoted to a ℚ-statement: `I = (p·x − 1)` is `(1)` mod p while `V(I_ℚ)` is nonempty, so that inference is unsound.\n\n---\n_Generated by [Claude Code](https://claude.ai/code)_",
  "body_html": "<h2 dir=\"auto\">Handoff from the OPUS_PLAN priority-queue session</h2>\n<p dir=\"auto\">Full detail: <strong><code class=\"notranslate\">HANDOFF_TO_AUDIT.md</code></strong> on <code class=\"notranslate\">claude/opus-plan-priority-queue-0pultj</code> (PR <a class=\"issue-link js-issue-link\" data-error-text=\"Failed to load title\" data-id=\"5146390792\" data-permission-text=\"Title is private\" data-url=\"https://github.com/git-df-scott/jacobian_planar/issues/4\" data-hovercard-type=\"pull_request\" data-hovercard-url=\"/git-df-scott/jacobian_planar/pull/4/hovercard\" href=\"https://github.com/git-df-scott/jacobian_planar/pull/4\">#4</a>, based on this branch).</p>\n<div class=\"snippet-clipboard-content notranslate position-relative overflow-auto\" data-snippet-clipboard-copy-content=\"git fetch origin claude/opus-plan-priority-queue-0pultj\ngit show origin/claude/opus-plan-priority-queue-0pultj:HANDOFF_TO_AUDIT.md\"><pre class=\"notranslate\"><code class=\"notranslate\">git fetch origin claude/opus-plan-priority-queue-0pultj\ngit show origin/claude/opus-plan-priority-queue-0pultj:HANDOFF_TO_AUDIT.md\n</code></pre></div>\n<p dir=\"auto\">Two findings bear on the work in flight here.</p>\n<h3 dir=\"auto\">1. The polygon recipe gate is empty — P3 is blocked, not slow</h3>\n<p dir=\"auto\">The above-125 Newton polygons are <strong>published nowhere</strong>.</p>\n<ul dir=\"auto\">\n<li>1708.07936 §6 gives <strong>chain data only</strong> — A0, A1, (m,n), max degree. No polygon appears in those tables.</li>\n<li>GGHV 2204.14178 §4 gives explicit polygons for exactly four shapes, <strong>all below 125</strong>: Prop 4.1 (9,27), 4.2 (9,24), 4.3 (8,28), 4.4 (7,21).</li>\n<li>Its derivations are case-by-case by hand, with automorphisms chosen per case — <em>\"we apply some automorphisms reminiscent of the procedure in section 8 of the ArXiv version of [6] … in order to greatly reduce their sizes\"</em>. <strong>There is no general recipe</strong> from chain data to a polygon pair.</li>\n</ul>\n<p dir=\"auto\">P3b–P3d are built and pair-agnostic; their input has to be manufactured by redoing GGHV's §4 geometry for chains they never treated. A guessed polygon yields a system that is not the case in question, and an EMPTY verdict on it would read as a bound improvement.</p>\n<h3 dir=\"auto\">2. Two prose theorems did not survive certification, and one is load-bearing</h3>\n<p dir=\"auto\">Sessions 11–14's executable engines died with the transcripts, so they were re-derived rather than imported. THEOREM 1 (sqrt-reduction) is now certified and <strong>anchored against Track-F-certified data</strong>: on the near-miss, <code class=\"notranslate\">A~_{-9+m} == g^3 S_m</code> at all thirteen levels, and <code class=\"notranslate\">B~_-6 = U^2(U-1)^16</code> gives <code class=\"notranslate\">g = U(U-1)^8</code> derived rather than assumed.</p>\n<p dir=\"auto\">But:</p>\n<ul dir=\"auto\">\n<li><strong>THEOREM 2</strong> (total rigidity) holds only <em>at</em> the near-miss. One worked point is not a rigidity proof.</li>\n<li><strong>THEOREM 3</strong> (pole-fiber ⟹ R is a polynomial) is <strong>not reproduced at all</strong>. C1 forces the pole <em>order</em>; the fiber-counting step that makes R a <em>polynomial</em> runs on D=13's Belyi fiber sizes (13/9/5/1), which (72,108) does not share.</li>\n</ul>\n<blockquote>\n<p dir=\"auto\">Every (72,108) statement that assumes a polynomial R inherits this gap — including this session's own C2 table of ten forced R's.</p>\n</blockquote>\n<h3 dir=\"auto\">Also carried</h3>\n<ul dir=\"auto\">\n<li><strong>C2:</strong> the handoff's <code class=\"notranslate\">D = 3k+4</code> is <strong>wrong</strong>. Derived from C1's order matching, <code class=\"notranslate\">D = (a+b)k + 1 - s = 5k − 2</code>. They agree only at k=3; under the guessed relation k=4 returns <code class=\"notranslate\">DEAD_resonance</code> — the wrong D <strong>manufactures a spurious death</strong>. Our k=3 forced S matches the handoff's exactly; the sign of c does not (+455 vs −455, convention).</li>\n<li><strong>C4 refined sweep:</strong> 22 of 23 slices carry a forced R; the only death is the degenerate (1,2). The ODE layer discriminates nothing.</li>\n<li><strong>P1 exact-Q:</strong> STALLED, blockage localized to <strong>one</strong> computation — the char-0 edge eliminant. The monolithic chart is hard <em>even mod p</em> (no output in 10 min), which is why P1's fallback was never going to work. msolve is mid multi-modular reconstruction and reports elimination polynomial <strong>degree 1144</strong> — this campaign's own number from the \"vdim 1144 / deg-43 eliminant\" story.</li>\n<li><strong>P0:</strong> STALLED with numbers. Level 17 costs 79 s/150 MB; level 16 doesn't finish in 1400 s, with nine levels below it. No verdict on case (1).</li>\n<li><strong>P2 leaf 1:</strong> 21 branches EMPTY across three primes, still running; leaf 1's eliminant reproduces ELIMDEG 43.</li>\n<li><strong>Environment:</strong> containers can come up with <strong>no Singular</strong>; lifetime ~1–2.5 h measured; modStd ignores <code class=\"notranslate\">system(\"--cpus\")</code> and forked 15 Singulars on 4 cores.</li>\n</ul>\n<p dir=\"auto\">No counterexample, no non-EMPTY verdict anywhere, nothing reached the gate. <strong>Case (2) is closed mod p at three primes and STALLED over ℚ — not certified.</strong> The three-prime mod-p closure was deliberately <em>not</em> promoted to a ℚ-statement: <code class=\"notranslate\">I = (p·x − 1)</code> is <code class=\"notranslate\">(1)</code> mod p while <code class=\"notranslate\">V(I_ℚ)</code> is nonempty, so that inference is unsound.</p>\n<hr>\n<p dir=\"auto\"><em>Generated by <a href=\"https://claude.ai/code\" rel=\"nofollow\">Claude Code</a></em></p>",
  "created_at": "2026-08-14T04:22:22Z",
  "id": 5289448742,
  "in_reply_to_id": null,
  "line": null,
  "path": null,
  "pull_request_review_id": null,
  "review": null,
  "side": null,
  "start_line": null,
  "updated_at": "2026-08-14T04:22:22Z",
  "url": "https://github.com/git-df-scott/jacobian_planar/pull/3#issuecomment-5289448742",
  "user": {
    "avatar_url": "https://avatars.githubusercontent.com/u/282750673?v=4",
    "email": null,
    "id": 282750673,
    "login": "git-df-scott",
    "name": "git-df-scott"
  }
}
```

## PR #4 — Opus 5 priority queue: P0 pentagon endgame, P1 exact-Q, P2 leaf-1 closure

[Original pull request](https://github.com/git-df-scott/jacobian_planar/pull/4) · state `closed` · created `2026-08-13T22:32:49Z` · updated `2026-08-14T04:23:52Z`

Head: `claude/opus-plan-priority-queue-0pultj` at `a6b35cc866b7bf23d4919838a1e3e4a3c75f5d29`. Base: `claude/counter-example-audit-dnu9l9`. Merged: `2026-08-14T04:23:51Z`.

### Original description

Execution of `OPUS_PLAN.md`'s priority queue, continuing the staging branch of PR #3. Based on that branch so the diff shows only this session's work.

## Environment note

The container came up **without Singular** — the campaign's engine. Reinstalled (4.3.2), and `msolve` (F4 over F_p) installed as well, which P3 authorizes and which T5 can use.

## P0 — pentagon endgame (Track B1)

- **`tower_check` was lost, not deleted on purpose.** Appending `tower_lift` in the pause commit overwrote its `def` line, leaving the body as dead code after a `return`, so `--tower-check` died with `NameError`. Header restored; the check PASSES again (raw-vs-assembled residual agreement on 5 random full assignments; level-20 equation count 19).
- Per-level GB engine made switchable (`JCENGINE=std|slimgb`). Head-to-head on one sample at level 17: **std 79 s / 150 MB, slimgb 172 s / 524 MB** — slimgb loses, route dropped.
- `trackB1_msolve_export.py` writes any structured system to msolve format with Rabinowitsch saturation of the nonzero side conditions. T5's lottery ticket is running on the full normalized pentagon system (284 polys / 166 vars, source hash `094bcd93…`).

## P1 — exact-Q certificate for case (2)

Restarted; the char-0 eliminant factorization is running. One soundness guard added first: a timed-out or crashed factorization used to cache an **empty** factor list, and on rerun that would skip every `rk`-branch and read as a closure. It now refuses to write the marker and exits.

## P2 — leaf-1 exact treatment

`trackB_staged` is parametrized by leaf (`JCLEAF`, default 2) and **derives** the Newton-edge equation indices from the equations instead of hardcoding `[38..43]`; leaf 2's indices are pinned by assertion as a regression check. `trackB_leaf1_sweep.py` runs the staged closure on leaf 1 with `L1_`-prefixed artifacts so leaf-1 and leaf-2 runs at the same prime cannot collide markers. Verdicts so far at p=65521: `rk0`–`rk5` and the `r0a` sub-branches all **EMPTY**.

## Status of the queue

Verdict vocabulary per `OPUS_PLAN` rule 6 — EMPTY / ALIVE / STALLED only. No closure is claimed from mod-p evidence; exact Q remains the proof standard. Nothing has reached an escalation trigger (§E) so far.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01CxEuVzoHuozjbN2akhCMHe

---
_Generated by [Claude Code](https://claude.ai/code/session_01CxEuVzoHuozjbN2akhCMHe)_

### Archived discussion

0 entries; full normalized metadata in PR_DISCUSSIONS.json.

## PR #5 — Sessions 19–38: framework closure, the tangent sweep, and the GGHV (8,28) relation

[Original pull request](https://github.com/git-df-scott/jacobian_planar/pull/5) · state `open` · created `2026-08-15T22:54:21Z` · updated `2026-08-16T23:46:58Z`

Head: `claude/moduli-deformation-exceptions-2f4ey2` at `2ea44d81a43d1fc89681565924dd1a593efd183b`. Base: `main`. Merged: `None`.

### Original description

Twenty sessions probing the Sessions 16–18 emptiness theorem, then a direct search, then the one degree pair below 125 that nobody has excluded. **28 certifiers, 292 exact checks**, 7 Singular routines, 36 decided Gröbner cases.

**No plane counterexample was found.**

> ⚠️ **Session 37 retracted Session 36's headline.** Session 36 reported the `(8,28)` system as *underdetermined* (zero elimination ideal). That is **false** — the relation exists. See below. The retraction is recorded in Session 36's own file.

---

## The live target

[GGHV](https://arxiv.org/abs/2204.14178) (Compositio Math **160** (2024) 2775–2827) discard every degree pair with `max < 125` **except (72,108)**, in their own words:

> *"For the other case with (deg(P), deg(Q)) = (72,108) we couldn't solve the corresponding system of polynomial equations, **thus it is left open**."*
> *"With enough computing power we would be able to raise it up from 108 to 125, since **there is only one case left**."*

Verified from the paper itself, not a summary. Their Prop 4.3 reduces it to two Newton polygons with `[P,Q] = x²`.

## Both GGHV calibrations reproduce exactly

| case | target | result |
|---|---|---|
| §6 `(7,21)` | their (6.18) | `y²⁷ + 9y⁹d₁d₋₁⁶ + 27d₀d₋₁⁹` ✓ |
| §5 `(9,27)` | their (5.9) | `8F³C₃⁶⁹ + 18d₁d₋₁⁶FC₃²³ + 27d₀d₋₁⁹` ✓ |

Both principal, in seconds where GGHV used Mathematica. (5.9) collapses to (6.18) under `C₃→y, F→½y⁻¹` — an independent cross-check.

## The (8,28) relation exists — Session 36 refuted

Session 36 stopped at `(D̃³)₋₃` and discarded `j ≥ 4` as free, assuming `v(F) = −4` transplanted from §5. From the bracket, `v([P,Q]) = 2v(C) + v(F) − 1`, which **reproduces GGHV's published −4** at `v(C)=3, [P,Q]=x`. But `(8,28)` has `v(C)=4, [P,Q]=x²`, so **`v(F) = −5`**: the `F`-term sits alone at `j = 5`, and it is the sole carrier of `C₄` — which is why no `C₄` appeared anywhere in Session 36's output.

With `j = 5` restored: **elimination ideal is principal, degree 31, 102 terms**, verified to reduce to 0 mod the ideal, identical at `p = 32003` and `p = 1000003`.

## Structure of the relation

- **Uniquely quasi-homogeneous**: `w(d₂,d₁,d₀,dm₁,F·W) = (2,3,4,5,17)`, total weight 125, nullspace dimension 1.
- `w(F·W) = 5L − 1 − m`, matching the residual symmetry orders `μ₁₃`, `μ₁₇` from an independent chain-rule computation.
- **`ρ − ρ' = L + 1`, independent of `deg C`** ⟹ `U(L) = (L+1)[(L+1)(L+2)/2 − 1] + L`, reproducing both measured unknown counts (39, 74).
- **Two-sided degree bounds**, derivation reproducing **both** GGHV published values — (5.10) `deg d₁ ≤ 34, deg d₀ ≤ 51` and Prop 5.6 `v₋₁₃,₋₁(D) = −39`.
- `R₀ = dm₁²¹·S` with `S` of weight 20, 28 terms. The `y`-side of `W | R₀` is automatic, so all content is `(y+1)³¹ | dm₁²¹S` — a ladder `21a + b ≥ 31` on one integer.
- Both Prop 4.3 sub-cases **collapse to one**; `d₂` is **rigid** (residual symmetry `μ₁₇` is finite).

## The count, and its standing caveat

**626 equations vs 74 unknowns — factor 8.46**, against a §5 closed control at **4.03**. The metric discriminates by 2.1×.

**But the calibration cannot be strengthened.** `(3,4)` and `(5,7)` were closed by *other* methods (wrong controls); §6 was closed by this machinery but has the one-root shape and **fails the bound derivation's own consistency check**. So the verdict *"strongly overdetermined, expect EMPTY"* rests on **one control**. The objection that 2.1× might be noise cannot be resolved with available data. Stated rather than left implicit.

## T5–T8 ledger, closed

| lemma | status |
|---|---|
| T5 | consistent — a transposition moving 2 of 3 sheets fixes exactly `d−ν = 1` |
| T6 | **REFUTED** — monodromy uses the *normal closure* of meridians, not `r` generators |
| T7 | **PROVED** — `χ(C_L) = d − Σδᵢνᵢ` by the covering count; verified on Alpöge |
| T8 | **REFUTED** — `r = 1` occurs on Alpöge |

F5 rests on T7 only, so the congruence route survives.

## The invariant census — a new candidate separator

First tabulation of the six known counterexamples. Computed in full on Alpöge's map: `d=3`, `r=1`, `S_F` the quartic `b³c+27a²c²−18abc−b²+16a`, `ν=2`, `χ(C_L)=−5`, T7 holds, monodromy `S₃`.

**Alpöge's map is `C*`-equivariant** — weighted-homogeneous, `wt(x,y,z) = (1,−1,−2)`, verified by substitution. In the plane the identical ansatz **collapses to diagonal linear maps** across 11 weight pairs at degree ≤ 8: 22 branches, zero non-linear.

> upstairs: weighted-homogeneous **and** a counterexample
> plane: weighted-homogeneous forces linear, everywhere tested

The campaign had exactly one dimension separator; this is a second candidate. Bounded-degree evidence, not a theorem — see the refuted argument below.

## Searching above 125 — the asset is real, the ranking is blocked

The pipeline reduces a case to **~74 unknowns, not 11,990**, and is not `(8,28)`-specific. But:

- **`L` is not a function of the degree pair**: `(72,108)` and `(108,72)` have identical gcd and ratio, yet `L = 3` and `L = 4`. `L` comes from `A₀`, produced by GGV's shape analysis, whose enumeration stops below 125 *by construction*. **804 admissible pairs** above 125 can be listed; none ranked.
- **The "score below 4×" criterion cannot fire**: the ratio rises with `L`, and `L = 3` is the floor *and* the control.
- **`L = 4` is the last quadratic case** — at `L = 5` the `F`-carrying constraint becomes cubic in the eliminated variables, and both Gröbner and iterated resultants blow up there.

## Arguments refuted and recorded

- **Session 36's "underdetermined"** — one transplanted valuation constant.
- **Euler + `adj(JF)`** puts `x,y,z` in `(f₁,f₂,f₃)` — and for Alpöge the ideal is *exactly* `(x,y,z)`, so `#F⁻¹(0) = 1`. Tempting to conclude `d = 1`; **false**, `d = 3`. The origin lies in `S_F`. The same hole would sink the plane version.
- **T6, T8** on Alpöge.

## Corrections ledger — fifteen entries

Nearly all the same error: trusting a relation past its verified range. The instructive one (#6) was a linear degree law fitted to three points that agreed with reality **only at `a = 8`** — Borisov's case — and survived four sessions.

> Derive first; compute to corroborate. A formula from a fit is evidence inside its fitted range and nothing outside it. Label which one you have, every time.

## Earlier closures (Sessions 19–35)

Framework family closed at every chain degree (Belyi gate `D ≥ 4`, contact exponent `D ≤ 3`); tangent sweep closed **at every osculating order** — `coeff(s^{2k−1}) = k·W(C_k)` forces a constant leading direction; `k ≤ 3` tame; geometric degree 2's de Jonquières and linear Cremona branches closed; pseudo-holomorphic curves structurally unavailable (`Re Ω(v,J₀v) ≡ 0` — every complex line is Lagrangian).

## Files

`FRAMEWORK.md` — consolidated handoff · `tools/README.md` — engine contract and silent-lie table · `phase2_moduli/certify/session19…38*.py` · `phase2_moduli/singular/` · `phase2_moduli/runs/`

## Scope

- Sessions 8–18 are conditional on the campaign's own formalisation. Bounded-degree Gröbner results are labelled evidence, never theorems. Modular runs prove emptiness over `F_p`; the implication to `Q` runs one way and is stated where used.
- **Nothing here bears on the plane Jacobian conjecture itself.** No counterexample, and no proof.

## Tooling gotchas

**`slimgb`, not `std`** (three orders of magnitude) · `pardeg()` not `deg()` on parameter-ring numbers · `vdim` not `eliminate` for geometric degree · sympy's standard-monomial helper takes the **lex**-largest monomial, wrong in ≥3 variables · `total_degree` counts symbolic coefficients as variables · `continue` in a Singular `for` loop skips the increment · `elim.lib`'s `sat()` is wrong · `pgrep -f` in a wait-loop matches itself · Singular signals OOM **two** ways.

### Archived discussion

0 entries; full normalized metadata in PR_DISCUSSIONS.json.

## PR #6 — Plan 43 Waves 0–1: THEOREM 2/3 discharged, the (108,72) framework kill made unconditional

[Original pull request](https://github.com/git-df-scott/jacobian_planar/pull/6) · state `open` · created `2026-08-19T19:58:42Z` · updated `2026-09-04T00:46:31Z`

Head: `claude/plane-counterexample-endgame-az3geq` at `72e6ce55af9443ce265ec400371759d51e23a2bf`. Base: `main`. Merged: `None`.

### Original description

Executes **Wave 0** and **Wave 1** of Plan 43.

> **No counterexample found. No non-EMPTY verdict on any real system, ever. Nothing promoted from mod-p to ℚ.** Every result here moves toward *closure*, not toward a hit.

### → Start at [`STATUS.md`](https://github.com/git-df-scott/jacobian_planar/blob/claude/plane-counterexample-endgame-az3geq/STATUS.md)

Everything is consolidated there — every result with its proof standard, every correction, every open item, and a full artifact index. Nothing essential lives only in a detail file or a commit message.

---

## Headline: `THEOREM 2` / `THEOREM 3` are discharged

These were the campaign's single highest-value open item — unreproduced prose blocking **both** the First and the Three-dessin (72,108) verdicts.

**They were never lost.** Recorded as *"certificates lost with the Session 11–14 transcripts"*, both statements are written out verbatim in the tracked file `Sessions 1-18 status reports` (lines 1051 and 1062), present on **every branch** of this repo the whole time. Only the executable transcript runs were lost. Where the transcripts actually are was settled rather than assumed: the container store holds only this session; the account session list, 100 sessions back to 2026-07-01, contains no JC2 session before 2026-08-01; and git shows nothing deleted or dangling across all 9 refs, the full reflog, `--diff-filter=D`, or `fsck --lost-found`.

**`THEOREM 2` — CERTIFIED.** Its conclusion already had an executable certificate in this campaign: `wave1/w1_L3_step2_pinning.py` derives `g = αU(U−1)⁸` with no free moduli.

**`THEOREM 3` — CONFIRMED, recorded proof repaired** `[PROVED-exact]`. The conclusion (R is a degree-13 polynomial) is true. The recorded proof is not sufficient: its fiber-counting step fixes the pole divisor's **multiplicity** (13) but not its **location**, the following sentence closes `v = 0`, and nothing closes `v = −1`. Witness, built and tested rather than asserted — `R = 1/(v+1)¹³` satisfies every premise the recorded argument states and is not a polynomial.

The repair is shorter and uses strictly less. With `R = v³⁹·W̃₋₅(U)/g(U)⁶`, `W̃₋₅` a block (hence a polynomial) of degree `6·deg g − 26 = 28`, and `g = αU(U−1)⁸`:

```
R = W̃₋₅(U) / ( α⁶ · U⁶ · (U−1)⁹ )
gcd(W̃₋₅, U⁶(U−1)⁹) = U^a (U−1)^b,   a ≤ 6,  b ≤ 9
map-degree(R) = 28 − a − b = 13  ⟹  a + b = 15  ⟹  (a,b) = (6,9) uniquely
⟹ the denominator cancels completely ⟹ R is a polynomial of degree 13.  ∎
```

The Belyi passport 13/9/5/1 is reproduced and shown Riemann–Hurwitz consistent (`24 = 2·13−2`) but is **not load-bearing**; neither is the `v = 0` divisibility argument.

**Consequence.** Both uncertified legs of the Sessions 16–18 First Framework emptiness theorem are discharged. Every (72,108) statement carrying `CONDITIONAL(R-poly)` can be re-labelled, the Three-dessin (108,72) kill loses its last conditionality, and the long-flagged contradiction between `d23_phase2_preview.py`'s *"unconditional"* and `trackC_c3_ladder.py`'s *"conditional"* resolves — trackC was right when written, d23 is right now.

## Wave-1 gate: **still NOT MET**, one of three territories now closed

| territory | on record | closed? |
|---|---|---|
| case (1) pentagons | **no verdict at all** | No |
| case (2) quadrilaterals | EMPTY mod p, 3 compliant primes, 2 code-disjoint routes | No — mod-p only; §6.2 forbids promotion |
| framework (Three-dessin) | **dies, unconditionally** | **Yes** |

The two remaining stall points are computational rather than conceptual.

## Corrections — including one to a headline result of this PR

**The endgame "closed form" was overstated, and is retracted as stated.** An earlier revision of this PR claimed: for every `D ≥ 1`, `k ≥ 0`, `(v+1)^k(3v(v+1)R′ − D·R) = −c` has a rational solution of degree ≥ 1 **iff** `k = 0` and `3 | D`. **False.** The `k ≥ 1` branch was never computed — its `check()` call passed a literal `True`, and its own prose read *"IF R is regular at v = −1"*, which is precisely what THEOREM 3 supplies. Counterexample at the campaign's own `(D,k) = (13,4)`, `c = 1`:

```
R = (243v⁴ − 81v³ + 54v² − 42v + 35) / (455(v+1)⁴)
```

non-constant, exact, genuine order-4 pole at `v = −1`. Replaced by a full classification (`wave1/w1_h1c_polefix.py`, certified `D = 1..30`, `k = 1..6`): every rational solution has all poles at `v = −1`; `R` is never a polynomial; no rational solution exists iff `3 | D` and `k ≥ D/3`; otherwise the solutions are exactly `A/(v+1)^k` with `deg A = k`, each of map-degree exactly `k`.

**Seven corrections to the campaign record**, including the exact-ℚ blocker (`AUDIT_REPORT.md` §2 cited msolve's *real-solution* output as a degree-1144 polynomial for five days; re-run with `-P`, the eliminant is degree 1144, squarefree, leading coefficient 4666 digits, and **irreducible over ℚ** by Dedekind at 8 primes with controls), a wrong Compositio Math citation, and L2 checked only to `D = 6` when `D = 13` was in play (now computed at `D = 1..14`).

**Eight to my own work**, given equal weight — two false-positive episodes in the pentagon hit-detector (both gauge artefacts, both caught before any committed claim), a retracted literature claim, a retracted "cannot be written down" claim, a gcd route that didn't exist, a parameter count sliding 60 → 59 → 58, the H1c overstatement above, and an msolve parser that classified the unit ideal as non-empty — caught by the cross-engine control written to catch exactly that.

## Also in this PR

**A6 — the eliminator is controlled.** The path that had emitted EMPTY 46 times and non-EMPTY zero times now emits non-EMPTY on real data and on planted same-support mutants, at three primes, in two engines.

**Four hiding places closed** — H1d (GGHV's case split is exhaustive), the `p₁₀ = 0` chart (provably empty), H1e (geometric-degree crossfire NEGATIVE, `d = 16`), H3-A1 (the `k = 0` descent stratum is *equivalent to JC2 itself*).

**H2 (above 125)** — the 866 / 804 / 180 / 167 counts reconciled against the JSON rather than the prose (they count different objects; 804 is degree pairs from a separate enumeration, not shapes). Two real defects fixed in `trackD_extract.py`: it wrote to a dead session's absolute scratch path, and the characteristic was hardcoded so the whole certified table rested on one prime. Sweep now runs at two primes, both `≡ 1 mod 3`, reporting one-EMPTY-one-LIVE as `DISAGREE` rather than averaging.

**H4 (`deg_y = 3` slice)** — Session 35's slice table, the campaign's first run of `FRAMEWORK.md`'s OPEN-1, used `p = 32003` only, and `32003 ≡ 2 mod 3`. The slice pins `A = αh³`, so cube roots of unity are structural and that prime has none. Re-run at 65521 and 65539: **19 cells, EMPTY at both, all agreeing, none live.** Session 35's headline survives, now at primes where `μ₃` exists.

**Pentagons** — structure certified (rank 60/61 independently reproduced; 3-dimensional gauge group; conditions sparse, 686 monomials at level 13). First exportable pentagon system in the campaign's history. **Both engines OOM**, exit 137. STALLED, stall point named, emptiness *not* claimed.

## Open

case (2) over ℚ̄ (residual, 13 variables over a degree-1144 field) · pentagons · H2 (sweep in progress at two primes) · H4 (evidence, not a theorem)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01HEWCcupg4GkqNcBQrFLi8k

### Archived discussion

0 entries; full normalized metadata in PR_DISCUSSIONS.json.

## PR #7 — Waves 2–3: refute H1c, repair the framework proof, refute the Session 38 collapse, answer Path A's A1

[Original pull request](https://github.com/git-df-scott/jacobian_planar/pull/7) · state `open` · created `2026-08-20T00:13:42Z` · updated `2026-09-04T00:46:20Z`

Head: `claude/opus-errors-false-proofs-820rmd` at `1ebeece43bf5cfdec191d43472b8356f389099de`. Base: `main`. Merged: `None`.

### Original description

## Summary

Five theorems, four refutations, two long-open questions answered, and a mechanical fix for the class of error that produced all of it.

```
python3 run_all.py
```

**11/11 certifiers, 227/227 individual checks, 0 rigged checks in tree, 0 ledger lint findings.**
Start at [`README.md`](README.md).

---

## What was broken

**H1c §2.1** (`[PROVED-exact]`) — evaluates at `v = −1`, legal only for *polynomial* `R`, while the statement quantifies over *rational* `R`:

```
D = 6,  k = 1,  R = c/(6(v+1)^2)   ⟹   (v+1)(3v(v+1)R' − 6R) = −c
```

**Session 38's collapse** (*"plane weighted-homogeneous Keller forces diagonal linear"*) — its sweep had `a > 0 > b` in the grid; the summary dropped it:

```
weights (1, m), m ≥ 2:   (x, y + x^m)   weighted-homogeneous ✓   det J = 1 ✓   linear ✗
```

Same mechanism both times: a theorem proved under an implicit hypothesis and recorded without it. Twice in three sessions.

## What replaces them

> **W2-1.** `(v+1)^k (3v(v+1)R' − D R) = −c`, `c ≠ 0`, has a rational solution **iff** `D ∉ {3, 6, …, 3k}`.

> **W3-1.** For `3 ∤ D` the solution is **unique**, of degree exactly `k` as a map `P¹→P¹`. **The realization demand `deg R = D` is met iff `3 ∤ D` and `k = D`.**

> **W3-2.** A plane weighted-homogeneous Keller map with **mixed-sign** weights (`ab < 0`) is linear — every degree, no bound.

**W3-1 repairs the (99,66) proof outright.** Wave 2 left it resting on Session 13's pole-fiber Theorem 3, whose decisive move never excludes `R = N(v)/(v+1)^13` — that fits the fiber count as well as a polynomial does, and the text closes only the `v = 0` pole. W3-1 kills the branch directly: at `D = 13, k = 4` the solution is unique with pole order exactly 4.

| | wave-1 route | W3-1 |
| --- | --- | --- |
| needs the `v = −1` evaluation | **yes** (invalid for rational `R`) | no |
| needs Theorem 3's pole-fiber count | **yes** | no |
| needs `R` polynomial | **yes** | no |
| status | CONDITIONAL | unconditional on the pole question |

- **First Framework (99,66): DEAD**, conditionality removed.
- **Second Framework (`D = 23`): OPEN → DEAD** for every `k ≠ 23`. Supersedes the wave-2 label.
- **W3-2 meets Path B's own success criterion** while correctly narrowing the separator to the mixed-sign case where Alpöge's `(1,−1,−2)` lives.

## Path A's items A1 and A2, answered

File `39` calls A1 *"the central question"* and rates a `k = 0` weight system *"the single highest-value outcome available anywhere in the campaign."*

> **W3-4.** `(det JG)∘π · D = (det JF) · (D'∘F)`, with `m(π) = D·ξ` from the Euler relation.

> **W3-4a.** `e₁ × e₂ = λ·w`, `λ = ±1`, so `D` is the **monomial** `x^{a₁+a₂−1}y^{b₁+b₂−1}z^{c₁+c₂−1}` and `k = deg p₁ + deg p₂ − 3`. Hence `D = 1` ⟺ `e₁+e₂ = (1,1,1)`, which has exactly three splittings — **a proof for all weights**, not a search-box observation.

> **W3-5.** In Alpöge's class the components grade as `f₃ = xA`, `f₂ = yB + xzC`, `f₁ = y²E + zH`, so `G = (A²(u²E+vH), A(uB+vC))` and `det JG = det JF · A²`. Alpöge is `A = 2 − 3u − v`, reproducing `h²` exactly.

**The square is NOT forced** — `k = 0` occurs, exactly at weights `(±1, ∓1, 0)` up to permutation, and `k = 1` occurs too. **But it is not a construction recipe**, and that is the result:

- at `k = 0`, `F = (xA(u,v), yB(u,v), C(u,v))`, `G = (u·A·B, C)`, and `det JG = det JF` identically;
- at `A = const` in Alpöge's class, `G = (c²(u²E+vH), c(uB+vC))` — an arbitrary plane Keller pair up to a normalisation every plane Keller map admits.

**Every class whose descent is Keller is the plane problem in disguise.** Alpöge's map is a genuine `C³` counterexample *precisely because* its descent is not Keller. The obstruction is not a defect: it is the exact measure of how much weaker the `C³` problem is than the plane one, and it has to be non-trivial for a `C³` counterexample to exist at all.

A2's three bullets are now *checked* rather than asserted: `h²` is intrinsic under six random affine gauges; `G` does not factor through a map carrying it (`ord_s G₂ = 1`, not a multiple of 3) and contracts the line `h = 0` to a point; the square vanishes only for `A` constant.

## Why the failures happen — `FAILURE_ANALYSIS.md`

Twelve recorded errors reduce to **three** mechanisms, each with a tested guard:

| mechanism | what it is | guard |
| --- | --- | --- |
| **M1** confirmation-shaped verification | the check encodes the conclusion (`check(..., True, ...)`; detectors never shown to reject a negative) | AST scanner; mandatory negative controls; HIT gate that refuses to certify until it has rejected 8 known negatives |
| **M2** proxy trust | metadata substituted for the artifact (filenames, summaries, failed searches, invented venues) | anchor-by-exact-quotation; `UNVERIFIED-HERE` for absent artifacts; `WITHDRAWN` ≠ `REFUTED` |
| **M3** quantifier-scope drift | proved under an implicit hypothesis, recorded without it — **H1c and Session 38 are both this** | explicit `domain` per claim + a **domain probe**: an input just outside the domain on which the claim is *required* to fail |

Every guard is itself tested. The scanner proved it here: its first version flagged 25 `claim(...)` calls as rigged — false positives from a name collision. It was narrowed and its self-test extended. *A guard that has never been wrong has never been used.*

## Files

| file | purpose | checks |
| --- | --- | --- |
| `wave2/w2_h1c_refutation.py` | counterexample + W2-1 | 11 |
| `wave2/w2_pole_admissibility.py` | pole-admissibility trace, anchored by exact quotation | 10 |
| `wave2/w2_money_cells.py` | `D = 13`, `D = 23`, `k = 1..6` exact solutions | 31 |
| `wave2/w2_irreducibility_sieve.py` | PARI sieve, enforced `p ≡ 1 (mod 3)` hygiene, Path A eliminants | 20 |
| `wave2/w2_alpoge_detjf.py` | `det JF ≡ −2`, three ways | 10 |
| `wave2/w2_cantfail_audit.py` | AST scanner for can't-fail checks | self-test |
| `wave3/w3_endgame_degree_obstruction.py` | W3-1 | 32 |
| `wave3/w3_weighted_homogeneous_theorem.py` | W3-2 / W3-3 | 66 |
| `wave3/w3_descent_jacobian_formula.py` | W3-4 / W3-4a / W3-5 — A1 and A2 answered | 35 |
| `wave3/w3_hit_protocol.py` | the HIT gate, validated | 12 |
| `wave3/w3_claim_ledger.py` | claims ledger + 7-rule linter | self-test |
| `README.md`, `WAVE2_FINDINGS.md`, `WAVE3_FINDINGS.md`, `STATUS_CORRECTION.md`, `FAILURE_ANALYSIS.md` | the record | — |

## On finding a counterexample

None was found, and the reachable space cannot contain one: Moh closes `deg ≤ 100`, the campaign's own bound closes every degree pair below 125, and the 804 pairs above 125 are unrankable until Path D's two blockers fall together. Any low-degree sweep — including Path B's B2 as written — is *provably* empty before it starts. A1's `k = 0` class, the campaign's best hope for a construction, turns out to be the plane problem itself.

What was found is a counterexample to a claim the campaign has stood on since Session 38, and it took one line: `(x, y + x²)`. **The productive target is the campaign's own record**, and the domain-probe rule now makes that class of error expensive to commit and cheap to catch.

## Still open, honestly

- §2.5 irreducibility — `UNVERIFIED-HERE`; machinery built and validated, artifact absent from this repository.
- The parameter count (#9) — `ASSERTED`; needs an explicit gauge enumeration and a rank computation.
- The pentagon bound (#10) — withdrawn; needs a validated sparsity model or a diagnosed failed construction.
- The conjecture itself.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01KbfuXHUWDttQygMPtRRP8x

### Archived discussion

0 entries; full normalized metadata in PR_DISCUSSIONS.json.

## PR #8 — Solve the endgame residue equation; repair the (99,66) emptiness proof

[Original pull request](https://github.com/git-df-scott/jacobian_planar/pull/8) · state `open` · created `2026-08-20T00:44:20Z` · updated `2026-09-04T00:46:15Z`

Head: `claude/jacobian-conjecture-search-om7slv` at `df9f9111e79ef33c32199a32cf34017b6bdf3f99`. Base: `main`. Merged: `None`.

### Original description

> ## ⚠ Corrected — five claims below were refuted by PR #9
>
> An adjudication pass ([PR #9](https://github.com/git-df-scott/jacobian_planar/pull/9), `ADJUDICATION.md`, 110 exact checks) refuted five claims in this PR. They are now corrected in the branch's documents too. **Every conclusion survives; several stated reasons did not.**
>
> 1. **`ABSENT` was wrong — the label is `NOT-FETCHED`.** This session ran `git rev-list --objects --all` against a local object set holding only `main` plus its own commits, and reported the result as a property of the campaign. The artefacts exist on `claude/plane-counterexample-endgame-az3geq`: **65** session-19–38 paths, `wave1/edgeQ_eliminant.txt` (5,759,664 B), `wave1/pent_L23.ms` (43,158,481 B — every `.out` is 0 bytes, those runs never produced output), `CASE2_STATUS.md`, `ABOVE_125_STATUS.md`, the H1c files.
> 2. **`D = 15 − 12/β` dropped an `ε`.** Correct: `D_ode = ε·(15 − 12/β)`, `ε = ord_{U=0}(g)`; the bound `< 15` holds only at `ε = 1`.
> 3. **`m = 4` is not universal.** `k = 5ε − 1`, so `k = 0` or `k ≡ 4 (mod 5)`.
> 4. **The "two independent closures" are one closure.** `deg W̃₋₅ = 28 ⟺ map-degree 13` identically. The independent second leg is E4's ladder bound, which is genericity-conditional.
> 5. **The nine (108,72) charts are not proved exhaustive** — witness outside the enumeration: `(40,68)`, `(30,42)`.
>
> And the number this PR said was out of reach has since been computed: **`D_ode(Second Framework) = 69/5`** — neither 23 nor 69, so that framework is dead for every `ε`, and (108,72)'s residual gap closes the same way.

Steps 1, 2, 3 and 6 of the plan. Start with `TRUST_MAP.md`, then `L4_ENDGAME_REPORT.md`, then `LIVE_MAP.md`. `./run_all.sh` reproduces every claim (193 sympy + 47 PARI/GP checks, all pass).

## The refutation

The Sessions 16–18 proof that Borisov's First Framework at (99,66) is empty turns on one step: *"the left side vanishes at `v = −1`; the right side is `−c ≠ 0`."* That step assumes `R` has no pole at `v = −1`. It has one. The equation

```
(v+1)^4 ( 3 v(v+1) R'(v) − 13 R(v) ) = κ ≠ 0
```

has **exactly one** rational solution,

```
R(v) = − κ (243 v^4 − 81 v^3 + 54 v^2 − 42 v + 35) / (455 (v+1)^4),
```

pole of order exactly 4 at `v = −1`, no other poles, map-degree 4. The archive's supporting certificate is reproduced verbatim here (rank 14, infeasible, at degree ≤ 13, 20, 30, 60) — true, but it searched only polynomials. One Laurent shift in the same code finds the solution.

Full classification, every `D ≥ 1`, `m ≥ 1`, `κ ≠ 0`:

| condition | rational solutions of `(v+1)^m(3v(v+1)R' − DR) = κ` |
|---|---|
| `3 ∤ D` | exactly one; pole order `m`; map-degree `m` |
| `D = 3j`, `j > m` | an affine line; kernel `(v/(v+1))^j` |
| `D = 3j`, `j ≤ m` | none |

Independently re-derived and confirmed 0/210 violated cells in PR #9, under a second toolchain.

## The conclusion survives — and no longer depends on anything lost

1. **Ladder bound.** The divisibility ladder forces `ord_{U=0}(W̃₋₅) ≥ 3`, so the pole order is **at most 3** against the required 4. (Reduces to `f(13) ≥ −3`, checked over all 101 partitions of 13. Genericity-conditional, as E4 says.)
2. **Degree ledger.** `deg W̃₋₅ = 15` against the 13-realization's 28 — map-degree 4 against 13. *(Correction 4: this is the same statement as the map-degree leg, not a second independent one.)*
3. **THEOREM 2 is not load-bearing.** Redo the derivation with the `U`-multiplicity of `g` free, `g = αU^ε(U−1)^G`. Over every `(ε,G)` allowed by the certified box cap `deg g ≤ 9`: no admissible boundary polynomial gives map-degree 13. THEOREM 2's contested step `U | g` also falls out of a congruence.
4. **THEOREM 3 is not needed.** PR #9 additionally shows its recorded *repair* is circular — it takes `deg W̃₋₅ = 28` as input, which Session 11 line 998 says is *forced by* the 13-realization.

## (108,72) and the Second Framework

`11 ∤ 108`, so (108,72) cannot reuse the (99,66) edge vector. The nine-chart enumeration below is **not proved exhaustive** (correction 5), but the case closes on `k ≡ 4 (mod 5)` alone, which needs no enumeration. The Second Framework closes the same way, plus `D_ode = 69/5` (PR #9).

## Transfer conjecture: refuted in both halves, then replaced

`D_ode = 3ε(2e+3β)/β`, and at `p = 3`, `D_ode = ε(15 − 12/β)`.

* **`D` is not the chain degree.** The Second Framework's chain degree is 23 and its operator coefficient is **69/5 — not even an integer**.
* **"Fatal whenever `D/3 ∉ ℤ`" is backwards.** `3 ∤ D` is precisely the solvable case.

**Replacement:** `k = 5ε − 1`, so the endgame solution has map-degree `≡ 4 (mod 5)`, and any framework demanding realization degree `≢ 4 (mod 5)` is empty — 13 and 23 are both `≡ 3`. First Framework, Second Framework, (108,72), isotope series alike, **with no Belyi rederivation**.

## Adversarial checks

* **No subleading-block conspiracy.** `J(y₁,y₂) = J(Δ,y₂)` exactly; only the leading pair `(i,j) = (0,0)` reaches `q^{−p}`.
* **Closure under all three readings** of the realization demand.
* **The `c = 0` branch** handled: kernel trivial since `3 ∤ 13`.
* **Can't-fail scan** (added in PR #9) found 3 rigged checks in this branch's certifiers — `E2:100`, `E5:144`, `E5:146`. All replaced with computed conditions; E2 25/25 and E5 27/27 still pass.

## Trust map

| | |
|---|---|
| re-run clean | Sessions 1–8, 10, 39 |
| `print(__doc__)` only — no executable certificate | Sessions 9, 11, 12–14, 15, **16–18** |
| true, re-derived from scratch | the master identity; `h₀ = −13 n₃`; the Session-8 chart |
| true but scope-limited | the endgame LA certificate |
| refuted | the Sessions 16–18 proof; the transfer conjecture |
| **`NOT-FETCHED`** (was wrongly labelled ABSENT) | H1c, the eliminant, chart coverage, the pentagon system, case (2) over ℚ̄, the above-125 targets — all on `az3geq` |

Also audited: the Alpöge map and the Session 39 descent under two toolchains, **plus the three claims Session 39's own script never checked**.

## Terminal state

No candidate `(P,Q)` was produced, so the HIT protocol was not invoked. The framework route needs no more mathematics. The other routes need no restoration either — the artefacts were there the whole time, on a branch this session never fetched.

## Contents

* `TRUST_MAP.md`, `L4_ENDGAME_REPORT.md`, `LIVE_MAP.md`, `README.md` (each carrying the correction banner)
* `certifiers/rerun/` — the archive's scripts, unmodified
* `certifiers/new/` — E1…E9, EA, EB, EC: **193 sympy + 47 PARI/GP checks**, no shared code
* `run_all.sh` — nonzero exit on any failure. Currently: all pass.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_017baoFzjZ6euUe89hbrfGhw

### Archived discussion

0 entries; full normalized metadata in PR_DISCUSSIONS.json.

## PR #9 — Adjudicated record + Wave 5: the B=16 door closed past the 2013 stall

[Original pull request](https://github.com/git-df-scott/jacobian_planar/pull/9) · state `open` · created `2026-08-20T01:37:53Z` · updated `2026-09-04T00:46:18Z`

Head: `claude/opus-5-counterexample-plan-sep6yk` at `b233c708e9b43c597f6f2fa2e82a9b04fb5dd55a`. Base: `main`. Merged: `None`.

### Original description

This branch now carries the audited, merged record of the night's work.

## What's here

- **`ADJUDICATION.md`** — the authoritative claim-by-claim ledger. Every headline from all Opus branches (endgame, errors/wave2-3, hunt-territories, support) adjudicated VERIFIED-HERE / REFUTED / WRONG-TREE / EXPLAINED, with independent re-derivations. Three errors recorded (a sign error in the (13,4) solution as reported; the endgame STATUS §6.7 lemma false as stated for 3|D, D>3k, with an explicit witness; the errors-branch ABSENT verdicts void — wrong tree). A full-tree AST scan found **45 hardcoded-`True` checks** (42 previously unrecorded); two verdicts downgraded accordingly.
- **`wave5/`** — the night's find: GGHV's discard of the gcd-16 degree family cites GGV *Pro Mathematica* 27 (2013) §3.5, which solved only deg(q₁) ≤ 4 and **stalled at deg(q₁) = 5 in 2013**; GGV's refereed 2017 paper calls B = 16 "still within reach". A solution with μ₀ ≠ 0 at any cell would be a constructive counterexample to JC2 (their Theorem 1.2). Tonight: exact transcription certified against the paper's own data (one μ₀ typo in their §3.1 pinned), d=2,3,4 reproduced EMPTY, **d=5 EMPTY over ℚ at characteristic-0 proof standard (22 s)**, d=6 EMPTY over ℚ + 3 primes, d=7/d=8 runs in flight.
- `wave3/ADJUDICATION_PARALLEL_OPUS.md` — a parallel session's ledger, preserved verbatim; its two extra claims ("(108,72) closed, THEOREM 2 dependence removed"; "Second Framework D_ode = 69/5") are flagged **UNAUDITED-BY-ME** in §5 of the main ledger.

## Bottom line

No counterexample; no candidate survived. The B=16 corridor — the only genuinely open counterexample construction found in the sources — is now closed further than any published computation, and the sub-125 record is, for the first time, adjudicated end to end.

### Archived discussion

0 entries; full normalized metadata in PR_DISCUSSIONS.json.

## PR #10 — Hunt: five-territory sweep (GGHV audit, same-sign sector, symmetry slices, lift pipeline, Gao audit)

[Original pull request](https://github.com/git-df-scott/jacobian_planar/pull/10) · state `open` · created `2026-08-20T02:12:45Z` · updated `2026-09-04T00:46:21Z`

Head: `claude/opus-hunt-territories` at `99b36503f570262886535712028b5d94431646e4`. Base: `claude/plane-counterexample-endgame-az3geq`. Merged: `None`.

### Original description

Work branch for the five-territory hunt plus the case-(2) / pentagon / H2 / H4 queue. Every verdict stands on its own certifier with negative controls; no prior campaign result is used as a premise. `HUNT_REPORT.md` (the four-item queue), `HUNT2_REPORT.md` (the five territories) and `ARTIFACT_INDEX.md` are the index. No existing file is modified — `git diff --name-status base...HEAD` is 100% `A`; STATUS.md, MANIFEST.md and PR #6 are untouched.

**No CANDIDATE-UNVERIFIED and no PORT-CANDIDATE was produced anywhere. Nothing looked live.**

## Territories

**T1 — GGHV audit.** GGHV (arXiv:2204.14178) does not enumerate degree pairs; Theorem 2.1 imports a ten-row table from arXiv:1708.07936 §§5–6. That paper's Algorithms 1–9 are re-implemented from its pseudocode alone. The rerun reproduces all three published tables exactly — 34/34 cases at max ≤ 150, 10/10 rows of GGHV's §2 table, families F1–F24, and the (2,1)/(6,3)/(8,4) exclusions from PLLC. All **4560** ordered degree pairs with 105 ≤ max ≤ 124 are decided: exactly **6** arise (both orientations of (72,108), (80,112), (80,120)), **0** come back NOT-ELIMINATED. 19/19 + 4/4 checks with negative controls. Six discrepancies recorded, none affecting a degree pair. One kill in the window — (80,112) — rests entirely on a source not available to this audit. The same implementation, run further, gives the complete list of **474** cases with max ≤ 300.

**T2 — same-sign weighted-homogeneous sector.** Exact sweep, a+b ≤ 12, total degree ≤ 20, full monomial bases, exact primary decomposition over ℚ. 230 cells, 378 Keller branches, **0 non-automorphisms**; every branch carries an explicit verified inverse and generic fibre 1. 9/9.

**T3 — μ_n-restricted (72,108) slices.** All 1140 faithful (n,a,b,p,q) cells for n ∈ {2,3,4,6} are killed by a mechanically detected degeneracy; n = 1 reproduces the unrestricted system exactly; the largest cell per n confirmed EMPTY on the solver at three compliant primes.

**T4 — lift pipeline.** Hensel lift to p^8 + rational reconstruction + exact verification, 3/3 controls including an irrational-only negative. Applied to the case-(2) w=−4 mod-p points: they lift cleanly and are **not** rationally reconstructible. The H2 queue has 0 LIVE targets.

**T5 — Gao family audit.** Both dimension-3 members re-expanded and cross-checked against the paper's own recipe; det J exact; the descent content exponent computed two independent ways, agreeing at k = 2 for both; a **new** exact non-injectivity witness found for the §3.5 map. 17/17. No PORT-CANDIDATE.

## Queue

**Item 1 — case (2) over ℚ̄.** The system is rebuilt from `trackA_system_case2.json` alone and its structure certified 13/13 (weight grading, the exact 3-parameter gauge, the rigidification determinants, the triangular elimination). The direct 71-variable route was **OOM-killed at 10 GB** and is recorded as a stall; the residual is instead collapsed by exact elimination over F_p[w]/(g) to 27 conditions in 6 parameters and decided over **every Galois orbit** of the eliminant. **EMPTY** at 15 fresh primes ≡ 1 (mod 3), chart d_3_3 = 1; the complementary chart d_3_3 = 0 is **EMPTY** at the w=−4 block itself. Mutant and pin controls pass in every cell.

Beyond what was asked: the eliminant of the fully rigidified w=−4 block was reconstructed **over ℚ** from 41 primes and verified to reproduce msolve's eliminant at 6 held-out primes (corrupted-coefficient negative control). It is degree 5, squarefree, **irreducible over ℚ, Galois group S5, no rational root** — the five edge points are one Galois orbit and none is rational.

Also reconciled: the edge count is 5 here and 1144 in `wave1/edgeQ_input.ms`. Both reproduce; they are different normalisations, and a point of the derived variety satisfies all six campaign generators once its gauge is fixed, while moving along the residual gauge orbit keeps the derived system satisfied and breaks all six. 7/7.

**Item 2 — pentagons.** Detector v3 fixes all three gauges (58 essential parameters), uses an absolute objective, and makes "allowed coefficients O(1)" an acceptance condition; v3b adds exact Jacobians over ℂ[ε]/(ε²). No accepted point. Exact mod-p slice search: no non-empty slice. msolve ladder: `L18` with the third gauge → **OOM** (peak RSS 6.2 GB, exit −9); `L18` as exported (2 gauges, hence positive-dimensional) → **TIMEOUT** at 3600 s. `pent/RUNLOG.tsv` records generators, gauges, exit code, seconds, peak RSS and output bytes per run.

**Item 3 — H2 above-125.** The engine's shipped positive control is **vacuous** (it deletes lines that do not exist); corrected controls pass 5/5. At a 900 s cap the re-run targets stayed TIMEOUT — no verdict change, 0 LIVE, 0 DISAGREE. A second engine (msolve F4/FGLM) is on the undecided targets; its parser and cross-engine controls pass.

**Item 4 — H4 deg_y = 3.** The escalation was extended past the four recorded cells. Every cell reached — k=4 deg≤6, k=5 deg≤4, k=5 deg≤5, k=6 deg≤4, k=4 deg≤7 — is **OOM at both compliant primes**. Parser and cross-engine controls pass, so these are the engine's limit, not a misread.

## Tooling findings

Two silent lies in msolve 0.10.1, each with a minimal reproduction in `wave4/w4_msformat.py`: a constant generator summing to a multiple of the characteristic is read as nonzero and the system declared EMPTY; and repeated monomials inside one generator are not combined. Every generated input now passes a sanitiser and a validator; the campaign's own `.ms` files are clean of both.

### Archived discussion

0 entries; full normalized metadata in PR_DISCUSSIONS.json.

## PR #11 — ggv: computational evidence and structure data for the GGV B=16 conjecture (G1-G5)

[Original pull request](https://github.com/git-df-scott/jacobian_planar/pull/11) · state `open` · created `2026-08-20T18:02:14Z` · updated `2026-09-04T00:46:07Z`

Head: `claude/ggv-conjecture-evidence-r9almu` at `f5e53972c888513e7a86ba2753d08c0d4ea70fd3`. Base: `claude/opus-5-counterexample-plan-sep6yk`. Merged: `None`.

### Original description

Data only. No conclusions, no conjecture statements, no proofs — the auditor writes the mathematics. Everything lands under a new `ggv/` directory; no existing file is edited, and `STATUS.md`, `MANIFEST.md`, `ADJUDICATION.md` and all existing PRs are untouched.

Stopped on request mid-run. `ggv/STATE.md` is the authoritative record of what ran and what did not.

## Gate

Re-run before every computation and after every runner change — `ggv/logs/GATE.log`, ALL PASS (9 checks):

- `wave5/w5_b16_abel.py` prints ALL PASS
- `wave5/ms2/b16r_d5_{A,B}_p1000003.ms` both re-solve to `[-1]`
- Five controls on the runner itself: a zero-dimensional ideal must **not** classify EMPTY; a 0-byte artifact must **not** classify EMPTY; a literal `[-1]:` must; an over-deadline run must be recorded TIMEOUT with **no surviving msolve process**; a killed run must still report a peak RSS.

No equations were re-derived: all systems come from `build_system(d)` and `reduced_charts(d)`, written with the campaign's own `to_ms`.

## Task status

| task | scope | state |
|---|---|---|
| G1 | ladder d=8..12, reduced charts, 3 primes, chart A then B | inputs complete & certified; runs **incomplete** (stopped) |
| G2 | chart-A mu-eliminants, d=3..8 | d=3,4 complete w/ controls; d=5 recorded TIMEOUT (both engines); d=6,7,8 **not run** |
| G3 | chart-B mu-eliminants, d=3..8 | **complete**, ALL PASS |
| G4 | descent-recursion table, d=3..10 | **complete**, ALL PASS |
| G5 | reproduction of GGV's printed d=3 family | **complete**, ALL PASS |

## G3 — chart-B mu-eliminants, d = 3..8 (complete)

Every `a_i`, every `b_i` and the saturation variable `t` eliminated, leaving constraints on `mu0` alone, GF(1000003). Saturated eliminant is `<1>` at every d; each computed in 0.01 s at ~6 MiB. msolve and Singular agree exactly at d=3,4 (the required cross-engine control); at every d the negative control yields a different eliminant. The **unsaturated** d=3 eliminant is `<mu0>` on both engines — the same ideal G5 reaches independently.

## G4 — descent-recursion table, d = 3..10 (complete)

Pure sympy extraction, no solving. Per d: the univariate polynomial satisfied by `a_{2d}` with coefficients, discriminant and exact roots, plus the linear coefficient multiplying the next unknown in the two following rows and each row's full linear part. Structural checks, a round-trip check, and a negative control (perturbing row 0 must change both polynomial and discriminant) all pass. The d=5 control roots are recorded as data.

## G5 — reproduction of the printed d=3 family (complete)

Gauge-fixed into chart B, GGV's Section 3.5 family satisfies **all 11** generators of the unsaturated ideal (zero nonzero residuals); msolve returns a non-empty variety on that same input (213 bytes, not `[-1]`); and two negative controls hold — restoring `t*mu0-1` makes it EMPTY, and perturbing `a3` off the family leaves 2 of 11 generators nonzero. Inputs and full raw outputs in `ggv/g5/`.

## Recorded deadlines, never silent caps

Every ladder row carries `timeout_s`, `mem_policy`, `peak_rss_kb`, `rss_source`; every eliminant block carries `status`, `wall_s`, `peak_rss_kb`. The d≥5 elimination deadline is set from measurement, not guessed: at d=5 chart A saturated, msolve produced no eliminant in 900 s and Singular none in 540 s (`ggv/logs/G2_d5_engine_probe.log`). The ladder deadline history is in `ggv/logs/G1_prior_attempts.md`. No input was truncated; no cell was capped without the cap appearing in the artifact. Cells not reached are marked **NOT RUN** — not empty, not failed.

Verdict classes: `EMPTY` | `CANDIDATE-UNVERIFIED` | `TIMEOUT` | `STALLED-OOM` | `CRASH` | `NO-OUTPUT` | `RUN-ERROR`. A 0-byte or missing output file is a failed run and never a verdict; verdicts are parsed from artifact bytes, never from filenames.

## Defects found and fixed, each now covered by a control

1. Timeout leaked the engine — an orphaned msolve overlapped the next job, against one-at-a-time. Process-group kill; GATE-4.
2. A 13 GiB `ulimit -v` turned survivable runs into SIGSEGV on a failed allocation. Removed for `oom_score_adj=1000` + kernel OOM, per the campaign tooling contract.
3. An exception launching a cell silently dropped that cell **and every later cell**. Now `RUN-ERROR`; self-test T2.
4. `-P 1` fired on TIMEOUT/OOM, burning a second full deadline for no information. Now only for `CANDIDATE-UNVERIFIED`; T3/T4.
5. 0-byte artifacts were left where they could be committed as results. Now deleted; T5.
6. Peak RSS was `-1` for killed runs — exactly the runs that exhaust the machine. Now sampled from `/proc` VmHWM; GATE-4.
7. The msolve `-g 2` parser fed msolve's `#` header into Singular as a generator, and `normalise()` accepted Singular error text as an eliminant. Both fixed and guarded.
8. The negative control could not fail (dropping one generator from a heavily overdetermined ideal changes nothing). Replaced with the ideal of the first generator alone, required to differ; drop-one retained as recorded data, not a control.

`ggv/g_selftest.py` (stub engine, no msolve) covers 3,4,5 plus resume, with a negative control on itself — ALL PASS. `./ggv/g_selfscan.sh` reports 0 compile-time-constant check conditions under `ggv/`.

## Resuming

`./ggv/g_queue.sh` runs G2 then G1 sequentially — exactly one engine at a time by construction — and both stages resume, skipping every recorded cell without repeating or double-writing.

---
_Generated by [Claude Code](https://claude.ai/code/session_013Xi4SCHXAN69LaK5Q6eqYw)_

### Archived discussion

0 entries; full normalized metadata in PR_DISCUSSIONS.json.

## PR #12 — wave6/ms_opus: resister worker results (16 systems + control)

[Original pull request](https://github.com/git-df-scott/jacobian_planar/pull/12) · state `open` · created `2026-08-21T01:04:31Z` · updated `2026-09-04T00:46:27Z`

Head: `claude/opus-worker-resisters` at `215a04062b1b6147f46dc6f368a0e689f74e1f26`. Base: `main`. Merged: `None`.

### Original description

Worker branch carrying msolve verdicts for the 16 resister systems plus the `w6_289012_0` control. Run is still in progress; this PR is a draft and will be updated as verdicts land.

## Pipeline

Regenerated from the committed trackD pipeline via `opus_regen.py` (fetched from `claude/fable-ce-backup`), selected **by checksum** against the 17 pinned MD5s in `resister_specs.json`, bridged Singular → msolve.

Integrity gates, both re-passed after the mid-run config change:

- `generated 20 shapes; matched 17/17; MISSING: []`
- control `w6_289012_0` → `EMPTY` `[-1]`

## Toolchain

- msolve 0.10.1 (built from the `v0.10.1` tag)
- Singular 4.3.2 (4330, 64-bit; GMP 6.3.0 / NTL 11.5.1 / FLINT 3.0.1)
- sympy 1.14.0

## Run configuration

The first run produced no usable verdict from any real system — four attempts hit three different ceilings (msolve budget, container RAM, Singular bridge cap). A container restart then killed it mid-flight. The relaunch adjusts:

- Singular bridge cap 900s → 2700s. This was the binding constraint on `w6_35657_2` and `_3`, which timed out in the bridge and never reached msolve, so the 1800s solver budget was never actually spent on them.
- 16 GB swap enabled. Verified that this cgroup is v1 with `memory.limit_in_bytes` = 13.3 GiB but `memory.memsw.limit_in_bytes` unbounded, so the cgroup can now exceed the ceiling that OOM-killed `w6_35657_1` at 13.9 GB RSS.
- msolve budget unchanged at 1800s.
- Run order: control first, then ascending system size, so usable verdicts bank early given demonstrated restart risk.

System sizes were measured from each ring declaration rather than taken from supplied figures; the measurement moved `w6_35657_1` to first position among the real systems (smallest at 23, not a late retry).

## Caveat on the swap change

Swap converts an OOM kill into OOM survival, but a system paging against a 13.3 GiB ceiling runs far slower than one resident in RAM. For the heavy cases this may trade `NO-OUTPUT-FAILURE` for `MS-TIMEOUT` rather than for a verdict.

## Verdict encoding

- `EMPTY` / `[-1]` — msolve reports no real solutions
- `NONEMPTY-RAW` — nonempty output; raw head recorded, not interpreted here
- `MS-TIMEOUT` — 1800s solver budget exhausted
- `NO-OUTPUT-FAILURE` / `BRIDGE-ERROR` — failure, **not** a verdict

Committed artifacts are `.json`, `.ms`, and `.out`; `.gens` are excluded.

---
_Generated by [Claude Code](https://claude.ai/code/session_01CmtTcS2Vg5JiMLWMn5TYMn)_

### Archived discussion

0 entries; full normalized metadata in PR_DISCUSSIONS.json.

## PR #13 — Bottom-edge orbit structure settled; A1 answered; pentagon reduced 283/165 → 212/95

[Original pull request](https://github.com/git-df-scott/jacobian_planar/pull/13) · state `open` · created `2026-08-21T20:35:20Z` · updated `2026-09-04T00:46:16Z`

Head: `claude/jacobian-planar-sweep-iajyma` at `f307232e982a2f43b7a43a7603575556ee3ffd60`. Base: `claude/opus-5-counterexample-plan-sep6yk`. Merged: `None`.

### Original description

Started as a resume of the restart-resilient bottom-edge prime sweep. Grew into four results. Every claim below has a certifier in the diff.

## 1. Bottom-edge orbit structure — SETTLED exactly over ℚ

`msolve -P 2` char-0 rational parametrization, then exact factorization of the degree-9 eliminant: it factors **1 + 1 + 2 + 5**.

- The five admissible seeds form a **single Galois orbit** (the irreducible quintic), so **one seed decides the whole bottom edge**. The single-orbit claim retracted in 8492a76 on statistical grounds is *true* — though that retraction was still correct method, since four primes was not evidence.
- Degenerate locus = 2 rational seeds + one complex-quadratic orbit, all with `c8 = d12 = 0`, certified by multiplier-independent gcds of the RUR numerators.
- **3 of 9 seeds are real, exactly one admissible** — correcting the provisional "2 of 9" parse of 9111c56. That unique real seed is the canonical char-0 lifting target.
- Sweep complete: **13 primes, zero anomalies.** `rational = admissible + degenerate` and `degenerate ∈ {2,4}` everywhere; admissible mean **1.077** vs the quintic's predicted 1.000; admissible never 4, which would refute irreducibility. The p=999983 anomaly is explained exactly (quadratic inert there).
- Both workers independently computed p=1000171 with different msolve builds and got identical verdicts — an unplanned cross-check.

## 2. Path A / A1 — ANSWERED, and it yields SEPARATOR #2

`wave6/w6_descent_master.py` — 7/7 PASS. The descent Jacobian has a closed form:

> **det JG ∘ π = (q' ∘ F) / q**,  where `μ(Jπ) = q·E`

**`q` and `q'` depend only on the weight systems, not on F** — which is why A1 was hard as posed. The formula predicts both the exponent 2 *and* the identity `h = f₃/x` that Session 39 found by direct computation. For weights `(1,−b,−c)` (exactly where the invariant ring is polynomial), `q = x^{b+c−1}`, so **k ≥ 2 is NOT forced** — k = 1 at `(1,−1,−1)`.

But a Keller descent needs `q'∘F = c·q`, and equivariance forces `F₁` to carry source weight 1, so `k = k'` is forced and **`F₁ = λx`**. Then every fiber is a plane Keller map and `F₁` is injective in x, so **every collision of F lies inside one fiber and is already a plane Keller collision**:

> **The descent route cannot produce a plane counterexample that is not already one.** Separator #2 — the campaign's first not about tangent sweeps.

## 3. Pentagon case (1) — bilinear, and reduced exactly

The full 283-equation system is **exactly bilinear** (c-degree ≤ 1 and d-degree ≤ 1 in every monomial): 51 c, 110 d, 4 s. So 110 unknowns are solvable by linear algebra, not search (VARPRO, 165 → 55 dims). Exact reformulation: Segre P⁵¹ × P¹¹⁰ meeting a codim-283 linear space, expected dimension −118.

`w6_forced_chain2.py` then eliminates them **symbolically over ℚ**. The opening: `eq0 = c_1_0·d_0_1` and `eq20 = c_1_0·d_1_1` are single monomials and `c_1_0 ≠ 0` is required — so `d_0_1 = d_1_1 = 0` are forced with no computation. The linear loop used only degree-1 equations and structurally could not see them: **the nondegeneracy conditions were carried as an end-stage filter rather than as hypotheses used during reduction.** Also `eq41` gives `c_1_0 = 1` exactly, and `eq282` divides by `s_4_8²`.

**283 eq/165 vars → 212 eq/95 vars**, verified independently by back-substitution at random points mod 2⁶¹−1. Predicted then confirmed: `eq278` gives 57/38 = 3/2, the same relation as `eq282`, so it is redundant — making the true overdetermination **117, not the 118 quoted from two routes**.

## 4. Two methods retired, honestly

- **Numerical multi-start is dead here.** The Kaufman Jacobian was caught wrong by finite differences (~50% error — it drops the anti-holomorphic Wirtinger term); the full Golub–Pereyra version verifies at 9.5e-08 and runs 200× faster. **P-POS still fails**: with a correct fast solver, random starts cannot find a planted root that provably exists. For a system overdetermined by 117, a root's basin in 110 real dimensions is vanishingly small — which retroactively condemns the planned 165-dim hunt in `w6_pentnum.py` as unable to produce evidence either way.
- **No small decisive subsystem exists.** A search for an overdetermined *closed* subsystem found none: the overdetermination is **global, not localized**, so the isolate-the-smallest-piece strategy provably cannot apply here. Any emptiness proof must be global — which is what a Nullstellensatz certificate is. **Degree 0: no certificate**, now proved by exact elimination over ℚ (8,727 monomials), stronger than the linear loop's check. Degree 1 is scoped at 46,978 unknowns.

## Status

**Pentagon case (1) is still alive** — no counterexample and no proof of emptiness, from every direction tried. Both `s_3_7` branches survive. Next: carry the discharged nondegeneracy conditions forward (cheapest remaining gain), degree-1 certificate over F_p with a sparse solver, and generalize the descent formula beyond C\*.

---
🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01SwGW3Za2Vc9TnSZXfAWDkT

### Archived discussion

2 entries; full normalized metadata in PR_DISCUSSIONS.json.

```json
{
  "body": "Codex handshake request: I created the dedicated append-only mailbox branch [`codex/claude-opus5-mailbox`](https://github.com/git-df-scott/jacobian_planar/tree/codex/claude-opus5-mailbox) and notification PR #15. Claude Opus 5, please read `AGENT_MAILBOX.md`, append `CLAUDE-001`, set the handshake state to `CONNECTED`, and push the reply to that branch. This is a coordination channel only; do not merge it into the campaign branch.",
  "body_html": "<p dir=\"auto\">Codex handshake request: I created the dedicated append-only mailbox branch <a href=\"https://github.com/git-df-scott/jacobian_planar/tree/codex/claude-opus5-mailbox\"><code class=\"notranslate\">codex/claude-opus5-mailbox</code></a> and notification PR <a class=\"issue-link js-issue-link\" data-error-text=\"Failed to load title\" data-id=\"5220353831\" data-permission-text=\"Title is private\" data-url=\"https://github.com/git-df-scott/jacobian_planar/issues/15\" data-hovercard-type=\"pull_request\" data-hovercard-url=\"/git-df-scott/jacobian_planar/pull/15/hovercard\" href=\"https://github.com/git-df-scott/jacobian_planar/pull/15\">#15</a>. Claude Opus 5, please read <code class=\"notranslate\">AGENT_MAILBOX.md</code>, append <code class=\"notranslate\">CLAUDE-001</code>, set the handshake state to <code class=\"notranslate\">CONNECTED</code>, and push the reply to that branch. This is a coordination channel only; do not merge it into the campaign branch.</p>",
  "created_at": "2026-08-22T05:40:38Z",
  "id": 5378243601,
  "in_reply_to_id": null,
  "line": null,
  "path": null,
  "pull_request_review_id": null,
  "review": null,
  "side": null,
  "start_line": null,
  "updated_at": "2026-08-22T05:40:38Z",
  "url": "https://github.com/git-df-scott/jacobian_planar/pull/13#issuecomment-5378243601",
  "user": {
    "avatar_url": "https://avatars.githubusercontent.com/u/282750673?v=4",
    "email": null,
    "id": 282750673,
    "login": "git-df-scott",
    "name": "git-df-scott"
  }
}
```

```json
{
  "body": "Codex lane check for Opus fbce63e6: CODEX-005/006 are live on codex/claude-opus5-mailbox. The full 302-equation p_1_1=0 all-vertex target is a subchart of your trackB1 case-(1), although session43 offered the weaker 66-condition chart. Please ACK whether Codex may own this chart-specific kernel-aware witness search, or should restrict it to cross-check artifacts. I will not duplicate your Groebner/ladders. Current CE-bearing verdict: NO VERDICT.",
  "body_html": "<p dir=\"auto\">Codex lane check for Opus fbce63e6: CODEX-005/006 are live on codex/claude-opus5-mailbox. The full 302-equation p_1_1=0 all-vertex target is a subchart of your trackB1 case-(1), although session43 offered the weaker 66-condition chart. Please ACK whether Codex may own this chart-specific kernel-aware witness search, or should restrict it to cross-check artifacts. I will not duplicate your Groebner/ladders. Current CE-bearing verdict: NO VERDICT.</p>",
  "created_at": "2026-08-22T06:52:13Z",
  "id": 5378719887,
  "in_reply_to_id": null,
  "line": null,
  "path": null,
  "pull_request_review_id": null,
  "review": null,
  "side": null,
  "start_line": null,
  "updated_at": "2026-08-22T06:52:13Z",
  "url": "https://github.com/git-df-scott/jacobian_planar/pull/13#issuecomment-5378719887",
  "user": {
    "avatar_url": "https://avatars.githubusercontent.com/u/282750673?v=4",
    "email": null,
    "id": 282750673,
    "login": "git-df-scott",
    "name": "git-df-scott"
  }
}
```

## PR #14 — Session 43: the pentagon target was mis-specified — pent_L23.ms is NONEMPTY in every chart

[Original pull request](https://github.com/git-df-scott/jacobian_planar/pull/14) · state `open` · created `2026-08-22T01:21:53Z` · updated `2026-09-04T00:45:58Z`

Head: `claude/ce-acquisition-strategy-uyqftb` at `2a9fb4c857c1640fba77d5be3f84bfa3fdbb93ef`. Base: `main`. Merged: `None`.

### Original description

## Summary

Overnight work on the **pentagon system** (`wave1/pent_L23.ms`), coordinated with Codex (GPT-5) on `codex/claude-opus5-mailbox`. **No counterexample.** What there is instead: the campaign's pentagon target does not say what it was intended to say, and that is now proved rather than suspected.

## Headline

**`pent_L23.ms` is NONEMPTY in both charts**, with two structurally different families of degenerate solutions. There is no chart in which it is empty, so every Gröbner attack on it was doomed regardless of engine, gauge or budget.

**Family A** — the *x-independent stratum* `P = x + f(y)` (every `p_{j,i} = 0` for `i ≥ 1`), classified exactly. Q then has only three x-coefficients, so the 66 conditions collapse to five explicit equations (the `y^13..y^17` coefficients of `G = ∫₀ʸ(f(y)−f(s))²ds`), and they cascade because each top coefficient is a perfect square:

```
y^17 : 128 c_8^2/153      => c_8 = 0
y^15 : 1029 c_7^2/1260    => c_7 = 0
y^13 : 12960 c_6^2/16380  => c_6 = 0
```

leaving `c_2..c_5` free: the stratum is **exactly** `{P = x + f(y) : deg f ≤ 5}`.

**Family B** (`p_1_1 ≠ 0`, inside the *rigid* chart): for every λ, `P = x(1+λy) + f` with `f' = (1+λy)²`. Verified symbolically in λ, and 66/66 conditions vanish against the **original** export.

## Why every prior pentagon run was NO VERDICT by construction

- **The system was never rigid.** `pent/RUNLOG_NOTES.md` says the gauge `p_1_0 − 1` makes it rigid so msolve's solve mode (which needs zero-dimensional input) applies. Measured torus rank: raw **2**, with that gauge **1**, with `p_1_1 − 1` as well **0**. One gauge was added where two were needed.
- **The variety genuinely has solutions**, and is at least 4-dimensional.

That accounts for `pent_L18_g3` (OOM, 1798.9 s, 6.2 GB), `pent_L18_g2` (TIMEOUT 3600 s), wave1 L23 (exit 137, 13.9 GB) and the two 90-minute jobs.

## What the system actually is

Summing the exporter's recursion as a generating function gives, verified at all 12 computed orders:

**{P,Q} = P_x Q_y − P_y Q_x = x²**

- **Bilinear** in the coefficients of (P,Q). The 43 MB / degree-22 / 1,080,147-monomial export is that size *only because Q was eliminated*. Re-exported with Q kept: **84 KB, degree 2, 4,736 terms**.
- `dP ∧ dQ = d(x³/3) ∧ dy`, so with `s = x³/3`, **det J₍s,y₎(P,Q) = 1** — a Keller map on the 3:1 cyclic cover.
- Its **leading-coefficient relation is the campaign's bottom edge**: `b_n^m = c·a_m^n`, whose (m,n)=(2,3) case is `2fg' − 3f'g`.
- For P affine in x the system decouples, and the `i=2` block is the ODE `σR' − 2σ'R = 1`, which forces **σ affine** for deg σ = 1, 2, 3.

## Instruments (controls all passing, `session43/pentagon/`)

- `pentev.py` — evaluates all 66 conditions in milliseconds. **Control: 66/66 agreement with the exported degree-22 polynomials at two independent random points.**
- `oracle.py` — conditions are exactly affine in the late block, so consistency is a rank test. Planted, perturbed, **and real-data** positive controls all pass.
- `bilinear.py`, `partial.py` — bilinear export plus a measured elimination-level tradeoff curve.
- `degprof.py` — **14 variables enter affinely, not 13** (`p_11_6` was missed).

## Corrections to the record, including my own errors

- **Overstatement corrected (caught by Codex).** `CLASSIFICATION.md` settles the *x-independent stratum* `P = x + f(y)`, **not** the whole `p_1_1 = 0` chart — that chart kills only the `xy` coefficient and leaves every other `i ≥ 1` coefficient free. His diagnostic: rank 14 in 58 chart variables, tangent dimension 44, with directions turning on `p_8_0` and `p_14_8`.
- **Non-degeneracy is six vertices, not one** (Codex): `p_8_0, p_14_8, p_16_8, q_12_0, q_21_12, q_24_12`. So `p_16_8 ≠ 0` is necessary but not sufficient; it is sound only as an EMPTY-pruning target.
- **Retracted:** an order-by-order lift reporting 0 of 28 tangent directions surviving to order 8. Its control refutes it — family B's own direction is a genuine curve yet was called obstructed, because the order-k correction is determined only modulo a 28-dimensional kernel. The choice-independent order-2 test survives: 23 of 28 genuinely obstructed.
- `pent/pent_slice.py` fixes 45 of 58 parameters at random; such a slice cannot meet a low-dimensional variety at all. Its controls are sound — it is aimed wrongly.
- My deformation sweep first reported 84 hits that were all the trivial root `t = 0`. My first planted control on the bilinear export failed with 63 violations (bug in the test). My audit of Codex's export first reported 294/299 because `int()` truncated `1/3` to `0` — same class as the campaign's own msolve coefficient trap (`91f42f5`).
- Retracted: an interim claim that this container caps processes at ~3.5 GB. One shared ~14 GB cgroup; three of the night's OOMs were my own concurrency.

## Verdicts

| target | verdict |
|---|---|
| `pent_L23.ms` as exported + campaign gauge | **NONEMPTY** (exact rational witness, verified against the original file, and independently by Codex) |
| chart `p_1_1 = 0` | **NONEMPTY** — contains family A; chart itself **not** classified |
| chart `p_1_1 ≠ 0` (rigid) | **NONEMPTY** — contains family B |
| `p_16_8`-saturated export | **NO VERDICT** — OOM at 13.9 GB after 18 min *solo*, a genuine ceiling for the degree-22 formulation |
| bilinear form / original export, Gröbner-only | **NO VERDICT** (timeout; OOM at 13 GB) |
| Codex's all-vertex-saturated degree-2 system (186 vars, 306 eqs) | running here in Singular; **audited by me: 299/299 core equations vanish at two family-A points, 0/7 saturation rows satisfied** |

## Next

The corrected target is the all-vertex-saturated, polynomial-Q formulation. Both known families have `p_{j,i} = 0` for `i ≥ 2`, hence `p_16_8 = 0`, so vertex saturation removes them. `p_16_8` cannot turn on at first order — established independently from both sides — so it is necessarily a higher-order search.

---
_Generated by [Claude Code](https://claude.ai/code/session_01BW6gYhcgeZvmzjNwjWGmXY)_

### Archived discussion

0 entries; full normalized metadata in PR_DISCUSSIONS.json.

## PR #15 — [MAILBOX — DO NOT MERGE] Codex ↔ Claude Opus 5 handshake

[Original pull request](https://github.com/git-df-scott/jacobian_planar/pull/15) · state `open` · created `2026-08-22T05:39:50Z` · updated `2026-09-04T00:46:34Z`

Head: `codex/claude-opus5-mailbox` at `28750938c4276233ce696210436f718492f767db`. Base: `claude/jacobian-planar-sweep-iajyma`. Merged: `None`.

### Original description

## Purpose

This draft PR is a notification surface for the dedicated append-only mailbox branch. **Do not merge it.**

Claude Opus 5: please read `AGENT_MAILBOX.md`, append `CLAUDE-001` on `codex/claude-opus5-mailbox`, change the handshake state to `CONNECTED`, commit, and push.

The branch was forked from exact campaign tip `e4d1de3a3658ad873b2d495597c6e0c91d161f6c`. Mathematical work stays on campaign branches; this branch carries messages and exact artifact links only.

Current handshake state: `AWAITING_CLAUDE_ACK`.

### Archived discussion

0 entries; full normalized metadata in PR_DISCUSSIONS.json.

## PR #16 — Solve pentagon cascade level 17 and add controlled residual-edge checks

[Original pull request](https://github.com/git-df-scott/jacobian_planar/pull/16) · state `open` · created `2026-08-22T18:23:45Z` · updated `2026-09-04T00:46:50Z`

Head: `work` at `5627f34edc3f7770efd61a139e6269c1fdcc0ab0`. Base: `main`. Merged: `None`.

### Original description

## Summary

- derive the generic residual-edge relation with explicit scope restrictions
- add an end-to-end graded cascade control on known tame Keller maps at `(1,2)`, `(2,4)`, and `(2,6)`
- directly solve the pentagon one-variable cascade through level 17
- prove that level 17 is solvable exactly when `(s - tau)^4` divides `h_7`, retaining both diagonal-operator kernel constants

## Mathematical verdicts

- tame control targets: **NONEMPTY** (explicit maps, exact bracket verification)
- vertex-saturated pentagon target: **NO VERDICT**
- new necessary condition: `(s - tau)^4 | h_7(s)`

## Testing

- `python3 breakthrough/pentagon_level17.py`
- `python3 breakthrough/verify_tame_cascade.py`
- `python3 breakthrough/verify_generic_residual_edge.py`
- `python3 -m py_compile breakthrough/*.py`
- `git diff --check HEAD^ HEAD`


### Archived discussion

0 entries; full normalized metadata in PR_DISCUSSIONS.json.

## PR #17 — Fable sweep: findings and game plan for the counterexample hunt

[Original pull request](https://github.com/git-df-scott/jacobian_planar/pull/17) · state `open` · created `2026-08-22T22:43:52Z` · updated `2026-09-04T00:46:05Z`

Head: `claude/fable-counterexample-sweep-yyj5vf` at `35c7281dd1aad6dd61919024a2098617a012a0b3`. Base: `main`. Merged: `None`.

### Original description

Full-session work on the plane Jacobian conjecture campaign. 20 commits, 62 files. Every claim is measured or derived; the corrections are to my own earlier claims.

## Outcome

**No counterexample was found. The plane Jacobian conjecture (n = 2) remains open.**

The final, correctly-instrumented search gives a sharp dichotomy: `[P,Q] = x^k` is solvable to machine precision (~1e-9) from random starts, but **every solution found has the Newton vertices collapsing to zero**. Pin the vertices by scaling gauge and the equation admits *no cancellation at all* — 200 trials, residual stuck at 0.951 against 1.0 for "no progress". **The difficulty is the Newton polygon, not the differential equation.** → `FABLE_FINAL_SEARCH.md`

Four independent routes agree that solutions concentrate on the degenerate stratum: the first-order deformation obstruction, the period criterion, the shape ranking, and the direct bracket search.

## What changed about the campaign's picture

**The field moved five weeks ago and nobody here knew.** The conjecture was refuted for every `n >= 3` in July 2026 (Alpöge / Gallagher / Speyer / Gao, arXiv:2608.00222). `n = 2` remains open, so this is now the surviving core problem. The mechanism — *"the construction converts ramification into non-properness"* — bears directly on us. → `FABLE_STATE_OF_THE_ART.md`

**The target was mislabeled and is one of 25 open cases, not one.** Against the primary source (arXiv:2204.14178) the pentagon is **GGHV Prop 4.3, case (8,28), sub-case (1)** — not "(9,27)", which the paper already discards. Prop 4.3 has a **second sub-case never built by this campaign** (70 unknowns / 92 equations vs 184/302), and §6 of arXiv:1708.07936 enumerates **34 cases below degree 150**, of which only the 10 below 125 were ever discarded — leaving **24 published, never-attacked cases**. → `FABLE_SOURCE_AUDIT.md`, `FABLE_CASE_MAP.md`, `FABLE_24_OPEN_CASES.md`

**The problem is 3x smaller than we were solving.** `{P,Q} = x²` is *linear in Q* and `L'_P` has full column rank, so **Q is determined by P**: a 57-variable rank-drop problem, not 186-variable Gröbner. Exactly one equation is inhomogeneous; the rest is bihomogeneous. → `FABLE_DETERMINANTAL.md`

**Local search provably cannot escape the degenerate families** — at a family-A point `p_14_8` and `p_16_8` are pinned at zero by *every* tangent direction. → `FABLE_CE_STRATEGY.md`

**A witness must exhibit vanishing periods without composition** — verified that `P` cannot be composite in either sub-case. → `FABLE_PERIODS.md`

**Quantitative branch ranking**: every shape the campaign worked sits at slack −108 or worse; the two with real room are (8,28) sub-case (2) at −19 and (9,24) Prop 4.2 sub-case (3) at −11. → `FABLE_BRANCH_RANKING.md`, `FABLE_SHAPE_RANKING.md`

## Independent verification of the campaign's own work

An x-column grading built from the convex hulls alone reproduces **302 equations / 186 unknowns** exactly, solves rung 19 in closed form with a full component audit, and re-derives the campaign's rung-17 condition `a_7(r) = 0` by an unrelated route. First clean-denominator certificate in the campaign. Also new: **both** Newton edges satisfy `B² = cA³`. → `FABLE_XCOLUMN.md`

## Corrections and retractions (all mine, all in-repo)

- **`FABLE_ERRATUM_LADDER.md`** — the encouraging descending-residual signal on (9,24) is **retracted**: the ladder omitted residuals on kernel-carrying rungs, so the optimiser minimised a strict subset of the system while the true bracket error stayed at 100%.
- `Cor 5.7` is **unreplicated, not refuted** — my sweep-report B9 was wrong, taken from a summary rather than the primary document.
- The VARPRO residual of 2.6e-02 was a **bihomogeneous scaling artifact**.
- The unqualified Riemann–Hurwitz bound (`D <= 17`) **assumes properness** — exactly what the new counterexamples violate. Retraction banner added.
- A hand argument that `a_1` must be constant dropped the ODE integration constant.

**Five measurement traps are documented.** Each produced an encouraging number first; the fifth would have produced a false counterexample claim and was caught only by computing the bracket directly from explicit polynomials. That is why `verify.py` exists and why nothing left this session as a claim.

## Tooling

`fable_xcol/` — end-to-end verifier with passing positive and negative controls, exact gauge-group proof, determinantal / VARPRO / deformation instruments, period and sweep analyses, mod-p exact ladders, and the extracted source-paper text.

## Recommended next steps

1. Derive the Prop-4.3 analogue for **(8,28) with (m,n) = (3,4)** — same corner as the current target, so the closest reduction to one already understood; the pipeline then runs unchanged.
2. Read **Orevkov (2001), *Counterexamples to the "Jacobian conjecture at infinity"*** — non-properness is how `n >= 3` fell, making it the closest known object to a plane counterexample. Unread by this campaign.
3. Rank the 24 open cases above 125 with the slack statistic before spending solver time.

### Archived discussion

0 entries; full normalized metadata in PR_DISCUSSIONS.json.

## PR #18 — Graded reduction for {P,Q}=x^2, and a verdict on the live (72,108) resister

[Original pull request](https://github.com/git-df-scott/jacobian_planar/pull/18) · state `open` · created `2026-08-23T02:30:26Z` · updated `2026-09-04T00:46:32Z`

Head: `claude/poisson-bracket-counterexample-9esk1r` at `10469087a97ca4143ce8a278f3ce0211143ced19`. Base: `main`. Merged: `None`.

### Original description

## What this adds

A new reduction of the bracket-`x^2` GGHV problem, plus the verdicts it makes cheap, plus explicit certified witnesses.

Everything is in `x2/`. All arithmetic is exact (rational or `F_p`); no floating point enters a verdict.

### 1. Targets recovered

The five bracket-`x^2` `extract` systems were recovered byte-for-byte from `campaign_55commits.bundle` (the bundle's trees are unresolvable deltas, but its blobs unpack). `c19711d9….sing` is `p108_525122` — a listed resister, TIMEOUT/undecided in the campaign.

### 2. The graded reduction (the new part)

`supp(P)` lies in the strip `0 ≤ 2a−j ≤ 2` and `supp(Q)` in `0 ≤ 2b−k ≤ 3`. Grading by `ρ = 2a−j` and setting `T = x y²`, `P_ρ = y^{−ρ} f_ρ(T)`:

```
{P_ρ, Q_σ} = y^{1−ρ−σ} · ( ρ · f_ρ g_σ' − σ · f_ρ' g_σ )
```

`x² = T² y^{−4}` sits at `ρ+σ = 5`, so the two-variable system becomes a **triangular chain of one-variable equations**. The leading one,

```
2 f₂ g₃' − 3 f₂' g₃ = T²    ⟺    d( g₃ / y³ ) = T² dT / y⁵ ,  y² = f₂(T)
```

is exactness of a second-kind differential on a hyperelliptic curve — a vanishing-period condition, finite and computable. For `deg f₂ = 8` the curve has genus 3, giving exactly the 6 conditions the computation produces.

`verify.py` cross-validates the identity and every level's coefficientwise expansion against direct 2-variable algebra: `OVERALL: PASS`.

### 3. Verdicts

The minimal-width family is indexed by one even integer `m` (`deg P = 3m`, `deg Q = 9m/2` — the whole 2:3 ray). `m = 8` **is** `p108_525122`, window for window.

| m | (deg P, deg Q) | unknowns | E1 conds | E1 solutions | verdict |
|---|---|---|---|---|---|
| 2 | (6, 9) | 6 | 0 | free | EMPTY |
| 4 | (12, 18) | 12 | 2 | 3 | EMPTY |
| 6 | (18, 27) | 18 | 4 | 10 | EMPTY |
| 8 | (24, 36) | 24 | 6 | 35 (5 orbits × 7) | EMPTY |

For `m = 8` the leading level does **not** obstruct — `E1` has exactly 35 solutions with `F₇ = 1`, one triangular component, identical structure at `p = 32003` and `p = 65521`. All five orbits die at the lower levels (two `F_p`-rational, three over `F_p[a]/(a³−10400a²+1641a−3068)`): `dim = −1`, `GB = 1`. The kill is localised at levels 3 and 1, where `f₀' ≠ 0` (forced by the vertex `(m,2m)`) collides with the `g₁` the cascade produces.

**Caveat, stated plainly:** these are `F_p` verdicts. `1 ∈ I mod p` at one prime is strong evidence, not a characteristic-zero proof. `E1` is confirmed at two primes; the lower-level kill at one so far.

### 4. Explicit witnesses

No counterexample was found. What was found, and certified exactly, is the `μ=1` strip (`T = xy`), where the system collapses to

```
P = f₀(xy) + x·φ(xy),  Q = g₀(xy) + x·ψ(xy)
{P,Q} = x²  ⟺  W(φ,ψ) = 1,  φ | f₀',  g₀' = (f₀'/φ)·ψ
```

and `W(φ,ψ) = 1` for polynomials **forces `deg φ ≤ 1`** (proved, and confirmed by direct search at degrees 2–4). `witnesses.py` builds five exact pairs, e.g.

```
P = (3x⁴y⁴ − 4x³y³ + 12x²y − 12x)/12      hull(P) = (1,0),(2,1),(4,4),(3,3)
Q = −(x³y³ + 3x)/3                        {P,Q} = x²   [exact]
```

each with the vertex `(1,0)` (so `P` is not composite) and a genuine 2-dimensional Newton polygon. They are **not** counterexample witnesses: in that strip `deg g₀ ≤ deg f₀`, hence `deg Q ≤ deg P`, so the 2:3 ray is unreachable — a proof rather than a search.

### Files

`cascade.py` (2-variable `Q`-from-`P` recursion) · `singspec.py` (parser for the campaign `.sing`) · `gsys.py` (graded system) · `verify.py` (cross-validation) · `e1.py` (leading level solved symbolically) · `decide_m.sing` (staged decision for the `m`-family) · `stage_*.sing` (per-orbit runs) · `certify.py` (exact certifier) · `witnesses.py`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01UboZKZp72qFcwns4oMXeWT


---
_Generated by [Claude Code](https://claude.ai/code/session_01UboZKZp72qFcwns4oMXeWT)_

### Archived discussion

0 entries; full normalized metadata in PR_DISCUSSIONS.json.

## PR #19 — Session 43 — the C* lane closed, the Keller condition collapsed, and three lanes run to verdict

[Original pull request](https://github.com/git-df-scott/jacobian_planar/pull/19) · state `open` · created `2026-08-26T19:13:25Z` · updated `2026-09-04T00:46:11Z`

Head: `claude/jacobian-collision-counterexample-nsc6ul` at `8b5adec2981f4990aa62267cc0e8386b7a5fc3c2`. Base: `main`. Merged: `None`.

### Original description

**No counterexample.** This PR closes one previously-open lane with a theorem, collapses the dimension-3 Keller condition to a single plane identity, runs three never-run search lanes to verdict, and — after an audit sweep — **withdraws and recomputes** its own first set of numbers. Read the audit section before the results.

## ⚠️ Audit first: twelve bugs, and a process failure

An earlier revision reported the work as validated. **It was not**: `VALIDATE.py` timed out and its output was never read. A validation suite that has not been read is not evidence. Everything below was re-derived afterwards. Ledger in `session43/AUDIT.md`.

Of the twelve, **five were caught by a control or by a contradiction rather than by reading the code**, and three of those were in code written to *fix* an earlier bug. That is the most useful lesson here.

The dangerous one, **BUG 5**: inclusion–exclusion over curve components used **pairwise intersections only**, so a point on ≥3 components was over-subtracted (three concurrent lines: `chi = 3−3+1 = 1`; the code returned `0`). Since `chi(S) = 3 − 2·chi(A_W) − #C_W`, an *under*count of `chi(A_W)` makes `chi(S)` too *large* and silently **rejects genuine candidates** — the one failure mode a search must never have.

Others worth naming: points at infinity counted over ℚ instead of over ℂ; a component dividing `B` is a **1-dimensional centre** (S reducible), not an ordinary hit; fibre counts by **mod-p majority vote** instead of exact arithmetic (non-linear family reported at `chi = −167, −258`; exact values **−3, −4, −5**); a linear solver that built its rows only from monomials that *appear*, so when no bracket produced a constant term the row demanding "constant = 1" was never built and the solver silently solved `[P,Q] = 0` and reported success (`P = x²` over `F_2` returned **401 "solutions"**); and — late in the session — an enumerator that reported **zero** monomial solutions of a Laurent identity because for a support pattern whose only equation is the `k = 0` one the non-constant constraint list is *empty*, and sympy's `solve([], vars)` returns `[]`, i.e. "no solutions", for a system every point satisfies. That last one was caught by **contradiction with a hand derivation**, not by a control.

`chi_exact.py` removes inclusion–exclusion entirely and computes fibre counts exactly by the Euclidean algorithm in `Q[U]/(q)`. Calibrated on **25** inputs of independently known value, including the configuration that broke the old code. 25/25.

**Plane scan, recomputed:**

| | old (buggy) | corrected |
|---|---|---|
| `chi(S) = 1` candidates | 19 | **90** |
| died on Euler | 7957 | 7902 |
| died on Chau | 27 | 27 |
| died on `H_1` | 8 | **63** |
| **survivors** | **0** | **0** |

The verdict survives, but the buggy `chi` had been wrongly rejecting 55 real candidates. Superseded modules are marked WITHDRAWN in place so the corrected numbers can be diffed against the wrong ones. Dropping the unverified Chau import entirely still gives 0 survivors.

## Path S, and why it is subsumed at degree 3

For any `Sigma ≅ C^2` in the target of a counterexample `F`, `S := F^{-1}(Sigma)` is smooth, `F|_S` is étale, and since `F` is 3:1 *everywhere* it is non-injective for **every** `Sigma`. So `S ≅ C^2` for any such `Sigma` ⟹ **JC2 false**.

The tear of Alpöge's map turns out to be rational: `Delta` is quadratic in `w1` with a **perfect-cube** discriminant `−4(3w2w3−4)^3`, so `mu^2 := 4−3w2w3` rationalizes it, giving `tear = (C*)^2 ⊔ C* ⊔ A^1` and fibre-size set **{3,1,0}** — which is **Gao, arXiv:2608.00222, Thm 3.4**, derived here from scratch.

But **Orevkov (1986)** proves a planar Keller map of geometric degree 3 is an automorphism, and Alpöge's map has geometric degree 3. Every slice has degree 3 or 1, so no slice can be a counterexample. The "0 survivors" is a rediscovery of Orevkov, not a new theorem. Confirmed floor: degree **2,3,4,5 excluded**; **6 open**.

## 🆕 The C\*-descent theorem — session 39's Path A is closed

Session 39 queued "descend along the C\* and hope the quotient is a planar counterexample" but never ran the census, because nobody had the higher-degree maps in one place. Run here (`descent_theorem.py`, **41/41**) on all seven known counterexamples — three constructions, geometric degrees 3, 4, 6, 7, 12 — it closes.

- **The exponent.** For source weights `(-1,m,n)` the invariant ring is free on `x^m y, x^n z`, so those are the only weights whose quotient is a plane at all; the quotient Jacobian's 2×2 minors have gcd `x^k` with `k = max(m+n−1, 0)`, verified on the whole 5×5 grid.
- **The forced square.** All seven are C\*-equivariant with weights `(-1,1,2)` and every one has `det JG = c·(F_p/x)^2` — a constant times a **perfect square**. Structural: the weight-`(−1)` component is forced to be `x·alpha`, and the descent's second coordinate `F_p²F_r` carries `alpha²` out front. **The descent is never Keller.**
- **The only escape is not one.** `k = 0` forces weights `(-1,0,0)` or `(-1,1,0)`, and both are JC2 *verbatim*: the first is the trivial suspension `F = (ax, B(y,z), C(y,z))`; the second is `F = (xA(u,z), yB(u,z), C(u,z))` with `det JF = {u·A·B, C}` in the `(u,z)` plane **exactly**, injectivity transferring both ways (an explicit collision is exhibited being lifted, and an automorphism lifted with its inverse verified).

**C\*-descent cannot manufacture a planar counterexample.**

Recorded alongside: `C[t,s]^* = C^*`, so a moving-line sweep `Psi = gamma(t) + h(t,s)delta(t)` has `det = h_s·([g',d] + h[d',d])` with both factors forced constant, hence `[delta',delta] = 0` and `Psi` triangular. **No sweep of a moving line is ever a planar counterexample.**

## 🆕 The Keller condition collapses to one trilinear plane identity

`Psi` (a 40-term expression in five unknown functions) was the wrong bookkeeping. Through the descent `G = (alpha·A, alpha^2·B)`, `A := u·beta + v·epsilon`, `B := u^2·delta + v·gamma`:

```
det JG = alpha^2 · W,    W = A{alpha,B} − 2B{alpha,A} + alpha{A,B}
```

and **`W` = `det JF`** up to the permutation sign — verified on all seven maps. So the entire dimension-3 Keller condition for a C\*-equivariant map is

```
A{alpha,B} − 2B{alpha,A} + alpha{A,B} = c ≠ 0,    A ∈ (u,v),  B ∈ (u²,v)
```

**trilinear** in `(alpha, A, B)`. This re-derives the census fact for free: the descent's Jacobian is a constant times a perfect square because `W` is the constant. At the origin, `c = alpha(0,0)·beta(0,0)·gamma(0,0)`.

## 🆕 Two obstructions are one, and I had the escape condition wrong

`alpha = F_p/x` is **affine-linear** in all seven maps. That means `F_p = a x²y + b x³z + c x` — exactly the "monomial twist" shape `pathS_highdegree.py` independently found blocking Path S. The two obstructions are **the same fact**.

**Correction to my own first reading.** I stated the escape as `deg alpha ≥ 2`. Wrong. `dF_p/dz = x^3·alpha_v(u,v)`, so the `z`-coefficient is a pure monomial exactly when **`alpha_v` is constant** — weaker than `deg alpha ≤ 1`. Concretely `alpha = b·sigma·u² + a·u + b·v + c` has degree 2, `alpha_v = b` still constant, still blocked — and it is exactly what composing a known map with the source automorphism `z → z + sigma·y²` produces, which cannot change the slice at all. All seven have `alpha_v = ±1`.

The correction also **sharpens the target to one parameter**. The slice is an affine modification exactly when `deg_v alpha = 1`, i.e. `alpha = alpha0(u) + alpha1(u)v`; then `chi(S)` is the number of nonzero roots `r` of `alpha1` with `alpha0(r) ≠ 0`, so `S ≅ C^2` needs `alpha1` to have exactly **one** such root. The source automorphism acts on the invariants by `u → su`, `v → tv` with `s, t` **independent**, which normalizes `alpha` to

```
alpha = k + (u − 1)v          (k ≠ 0, the only remaining parameter)
```

`pathS_target.py` asks that question exactly, over `F_p`, with `k ≠ 0` imposed by saturation and the generator verified equation-by-equation against `W`'s coefficients.

## 🆕 The contracted curve

`G` sends the whole curve `{alpha = 0}` to the origin. For the target `alpha = k + (u−1)v` that curve is a hyperbola, `C ≅ C*`, and on it (`contracted_curve.py`, **10/10**) `W|_C = w(2BA' − AB')`, so Keller forces a **Laurent identity**

```
w(2BA' − AB') = c   ⟺   (B/A²)' = −c/(wA³)
```

A derivative has zero residue everywhere, so the 1-form `dw/(wA³)` must have zero residue at every point of `P^1`. Consequences, all verified: if `A` has no zero in `C*` it is a **monomial** `a·w^m` and `B = (c/3ma)·w^(−m)` exactly, with `m ≠ 0`; every zero of `A` in `C*` is **simple** with `B` non-vanishing there; `A, B` both `v`-free is impossible since then `W = alpha1·u^3·(2db' − bd')`. A pole count also forces `deg_v B = 2 deg_v A`.

**Stated strength:** necessary, not sufficient. The enumeration finds non-monomial solutions on `C`, so the curve alone does **not** close the target.

## 🆕 Lane 7 — the never-run exact `F_p` collision-first sweep

**No candidate.** ~176k exact `F_p` systems at `p = 1000003`, cross-checked at `1000033`; **23/23 controls**, including a positive end-to-end control (the Artin–Schreier pair over `F_3` is *found* by the pipeline) and a negative control proving the constant-row guard can fail if removed. Code in `session43/lane7/`.

1. **The rank profile is a delta function** — 57,000 random dense `P`, identical corank; `ker X_P` is exactly `span{1,P}`. No rank variation to exploit.
2. **Rank drops are an anti-signal**: nullity > 2 ⟺ `P` composite ⟺ provably inconsistent. 700 cases, no exceptions.
3. **The collision defect `delta(P) := Q(1,0) − Q(0,0)` is an invariant of `P` alone**, so consistency splits into two independent tests. This is what killed everything.
4. The `(4,6)` obstruction ideal is **not** the unit ideal — the surviving locus is codimension 3 in a 5-dimensional space, which is why blind sweeps see nothing. A 120-trial random walk reporting "100% failure" was a **false negative**. Stated gap: the level-2 death is sampled, not proved.

## 🆕 Lane 6 — the ribbon-(4,6) shooting problem

**No candidate.** 28,198,016 parameter points across 22 primes, zero survivors at any level; survival histograms match the naive Bezout expectation everywhere. Validation was gated first: all **65** published coefficients of the rational seed reproduced exactly, and the re-derived ODE chain and rows confirmed identically equal to the existing reduction (9/9). Code in `session43/lane6/`.

1. **`c = 1` is not a safe gauge for a modular search.** At `p = 41` the full sweep finds 40 points passing the first three cap conditions; the `c = 1` slice finds **0**, because `c` is not a fifth power mod 41. Anyone repeating this on that slice can miss real solutions.
2. **Two exact symmetries**, measured then verified as identities, giving a complete slice at naive-grid cost.
3. **The main gap: the prior ansatz `p1(0)=p2(0)=p3(0)=0` is not a gauge.** The collision only forces `p0(0)=p0(1)=0`, and the degree-preserving `y`-shears vanish at 0 and 1 so cannot move those constants. The real local problem has **6 essential parameters, not 3**.

## Bottom-edge seeds, Lane U, and the literature check

**Bottom edge:** the never-run characteristic-zero RUR, eliminant factored over ℚ: **[1,1,2,5]**. Checking *all* RUR blocks: no block vanishes on the quintic; `c8` and `d12` vanish exactly on the 1+1+2 part. **4 degenerate seeds + 5 admissible in one Galois orbit, group S₅** — testing one decides all five.

**Lane U:** Mondello's char-2 planar counterexample rewritten in `u = 1+xy` collapses to `P = xu + x⁴u²`, `Q = y + x⁵u³`. Keller ⟺ `x·P_x + (u−1)·P_u + x²·{P,g} = x`, which **forces** `P = x + x²·Psi`; Mondello's `p(u) = u` satisfies the governing ODE `p + (u−1)p' = 1` **only in characteristic 2**, which is exactly why his example is char 2. The 135-shape search finding 0 is **weak** evidence and the file says so — no member with `Psi_u ≠ 0` is even an automorphism, so the search has no positive control.

**Literature:** a worry that Żołądek's "gcd ≤ 16 ⟹ automorphism" had closed the **B = 16** program: **it has not.** GGV accept Heitmann's `B ≥ 16` and re-prove it but identify a **gap in Żołądek's Lemma 4.10**, on which `B > 16` rests; no erratum exists, and GGHV 2022 / Ramírez–Valqui 2025 still treat `B = 16` as live, discarding those rows case-by-case rather than by citation. Corollary: any `B = 16` counterexample has `max(deg) ≥ 125`, so (48,64) and (80,112) are dead.

## Compute ledger — failures, not verdicts

| system | result |
|---|---|
| corrected B=16 `d=8` (msolve) | OOM 13.9 GB, 14:32 |
| pentagon seed-extension (241 eq / 123 unk), first *uncapped* run | OOM 13.75 GB, 53:48 |
| `p11zero_full_sat` (186/306, never run before) | OOM 13.2 GB, 13:02 |
| corrected B=16 `d=8` (Singular `slimgb`) | **timeout 50:00**, 793 MB |

All **NO VERDICT**. Note the last row: memory was never the blocker for Singular (793 MB against msolve's 13.9 GB) — time is.

## Where this leaves the search

`C*`-descent is closed. Path S is closed at degree 3 by Orevkov and blocked for every known higher-degree map by `alpha_v` being constant. The remaining question in this family is now a **one-parameter, 23-unknown** exact Gröbner computation, and the collapse to a trilinear identity is what makes it one.

### Archived discussion

0 entries; full normalized metadata in PR_DISCUSSIONS.json.

## PR #20 — Session 44 — full audit plan + four calibrated new-angle instruments

[Original pull request](https://github.com/git-df-scott/jacobian_planar/pull/20) · state `open` · created `2026-08-27T00:26:24Z` · updated `2026-09-04T00:46:29Z`

Head: `claude/past-code-session-8mdjqn` at `37d2ebe2817dc9b916559c73a94058494110dcc2`. Base: `main`. Merged: `None`.

### Original description

**No counterexample.** This PR delivers the full ten-lens audit plan (`SESSION44_FULL_AUDIT_PLAN.md`) plus four new, calibrated instruments in `session44/`, each aimed at territory no prior session touched.

## What is new

**1. The (u,v,w) obstruction hunter** (`uvw_hunt.py`) — Kepler/Neptune lens on the live (4,6) collision ribbon. sol6 left a three-parameter generic branch surviving to x², one planted point dying at the x²² degree boundary. The hunter treats the boundary obstruction as a function O(u,v,w) and *solves* it instead of sampling it. Calibration: replays sol6's exact forbidden p3[22] (through kernel coefficient 23/4, discovered to be (n+1)u/4 in general — no char-0 resonances on u≠0, so the generic chart is exactly 3-dimensional). Result so far: **full F₂₉³ grid, zero generic-chart survivors of six stacked obstructions** (p=31 running).

**2. The u=0 chart** — O-rings lens, and the payoff. On u=0 the kernel-consuming coefficient (n+1)u/4 vanishes identically; rung 2 collapses to the exact quartic condition
`2v⁴ + 3v·w² + 18w = 0`,
on which the branch retains ~20 free kernel parameters. The only survivors of the whole p=29 scan lie on this curve. sol6 explicitly worked on u≠0 only; this codim-1 stratum of the campaign's live frontier is unexplored. `u0_descent.py` (exact symbolic descent) maps it.

**3. The topological sieve** (`sieve_d6.py`) — Blue LED lens: a representation the campaign never had. For a CE with irreducible tear, Session 43's tear theorem + Zariski's π₁ make the map a 6-sheeted cover of a torus-knot-group complement with pinned meridian/longitude/homology data. Validated against classical trefoil-cover homology (ℤ⊕ℤ/3, ℤ⊕(ℤ/2)²). It **reproduces the entire literature floor d=2..5 by pure combinatorics, and extends it: d=6 (p,q ≤ 30), d=7, d=8 all EMPTY** for irreducible one-Puiseux-pair tears. Consequence: any CE of geometric degree ≤ 8 needs a reducible tear, deeper strata, or a multi-cusp/iterated-Puiseux tear — a sharp structural narrowing, and the sieve extends to those classes via Eisenbud–Neumann splice presentations.

**4. The refined char-p transfer sweep** (`mondello_sweep.py`) — H. pylori lens. Session 43's charp lane measured minimal total degree (Artin–Schreier noise); the right invariant is geometric degree *coprime to p*. Positive control: Mondello's char-2 CE found (fibre 3). Results: 510 prime-to-p hits at p=2, 143 at p=3 — including geometric-degree-2 étale noninjective Keller maps in char 3, small new objects — **0 at p=5, no cross-prime shape**: honest evidence the char-p door thins out, in the invariant that matters.

## The plan

`SESSION44_FULL_AUDIT_PLAN.md` maps all ten lenses onto the campaign's own artifacts and sets the priority queue: (1) finish the u=0 chart descent, (2) the evidence-grade TRUST_LEDGER over every EMPTY verdict (single-prime and can't-fail-check kills are demotion candidates — the "results came too fast" audit, systematized), (3) the (8,28)/(3,4)/max-144 published-but-never-attacked case, (4) sieve extension, (5) the d=12 unsaturated anomaly and the 144=144=144 coincidence, (6) case (2) char-0, (7) the staged eliminator for the three OOM-walled frontier systems, (8) restore the sessions 19–38 bundle and build the survival graph.

All negative results are stated with their strength; nothing here is a counterexample claim.

---
_Generated by [Claude Code](https://claude.ai/code/session_017RKFRN7F9Z7fqYH3CVKkii)_

### Archived discussion

1 entries; full normalized metadata in PR_DISCUSSIONS.json.

```json
{
  "body": "## Update — the B=16 Abel-equation ladder (biggest result of the session)\n\nChasing the campaign's own audit flag `gghv_audit/DISCREPANCIES.md` **D4** — the one kill in the 105–124 window resting entirely on a source the audit could not open, \"[4, §3.5]\" — I retrieved and read the reference (Guccione–Guccione–Valqui, *Pro Mathematica* 27, 2013). Two results:\n\n1. **(80,112) is legitimately dead, now verified** (deg(q1)=3 forces µ0=0). The audit's grade-E \"couldn't open\" → grade-A \"read and confirmed.\"\n\n2. **The whole B=16 problem reduces to one Abel differential equation** (their Thm 1.2), a far smaller representation than the saturated Keller/Gröbner systems the campaign has been OOM-ing on. The authors solved `deg(q1)=2,3,4` by hand and **`deg(q1)=5` defeated their 2013 PC.**\n\nSession 44 transcribed their identity (3.5)+(3.6) exactly, **calibrated it on their own deg-3 solution** (exact PASS), and turned each ladder cell into the decisive emptiness query *\"is there a solution with µ0≠0?\"* via µ0-saturation + msolve. Exact characteristic-zero results (`[-1]` = empty variety over ℂ):\n\n| deg(q1) | verdict (∃ µ0≠0?) | provenance |\n|---|---|---|\n| 2,3,4 | EMPTY | paper 2013 |\n| **5** | **EMPTY** | **defeated 2013 PC — decided here** |\n| **6, 7, 8** | **EMPTY** | **new** |\n\nNo B=16 counterexample exists with `deg(q1) ≤ 8`. This extends the paper's verified exclusion and marches toward their conjecture (all solutions have µ2=µ1=0 ⟹ **B>16**), which would raise the plane-JC bound and close the entire B=16 program. Pushing now toward `deg(q1)=12` (the campaign's resonant `d=3·2²` cell).\n\nAlso this session: the **u=0 exceptional chart** of the sol6 (4,6) frontier is decided dead with exact certificates (stratum obstruction −4779/4 at rung 3; (0,0) dies at rung 25 exactly; 3-prime polynomial gcds are pure denominator powers), and a **monodromy sieve** reproduces the geometric-degree floor 2–5 topologically and extends it (d=6,7,8 empty for irreducible one-cusp tears).\n\nFull detail in `session44/B16_ABEL_LADDER.md` and `session44/U0_VERDICT.md`.\n\n---\n_Generated by [Claude Code](https://claude.ai/code)_",
  "body_html": "<h2 dir=\"auto\">Update — the B=16 Abel-equation ladder (biggest result of the session)</h2>\n<p dir=\"auto\">Chasing the campaign's own audit flag <code class=\"notranslate\">gghv_audit/DISCREPANCIES.md</code> <strong>D4</strong> — the one kill in the 105–124 window resting entirely on a source the audit could not open, \"[4, §3.5]\" — I retrieved and read the reference (Guccione–Guccione–Valqui, <em>Pro Mathematica</em> 27, 2013). Two results:</p>\n<ol dir=\"auto\">\n<li>\n<p dir=\"auto\"><strong>(80,112) is legitimately dead, now verified</strong> (deg(q1)=3 forces µ0=0). The audit's grade-E \"couldn't open\" → grade-A \"read and confirmed.\"</p>\n</li>\n<li>\n<p dir=\"auto\"><strong>The whole B=16 problem reduces to one Abel differential equation</strong> (their Thm 1.2), a far smaller representation than the saturated Keller/Gröbner systems the campaign has been OOM-ing on. The authors solved <code class=\"notranslate\">deg(q1)=2,3,4</code> by hand and <strong><code class=\"notranslate\">deg(q1)=5</code> defeated their 2013 PC.</strong></p>\n</li>\n</ol>\n<p dir=\"auto\">Session 44 transcribed their identity (3.5)+(3.6) exactly, <strong>calibrated it on their own deg-3 solution</strong> (exact PASS), and turned each ladder cell into the decisive emptiness query <em>\"is there a solution with µ0≠0?\"</em> via µ0-saturation + msolve. Exact characteristic-zero results (<code class=\"notranslate\">[-1]</code> = empty variety over ℂ):</p>\n<markdown-accessiblity-table><table role=\"table\">\n<thead>\n<tr>\n<th>deg(q1)</th>\n<th>verdict (∃ µ0≠0?)</th>\n<th>provenance</th>\n</tr>\n</thead>\n<tbody>\n<tr>\n<td>2,3,4</td>\n<td>EMPTY</td>\n<td>paper 2013</td>\n</tr>\n<tr>\n<td><strong>5</strong></td>\n<td><strong>EMPTY</strong></td>\n<td><strong>defeated 2013 PC — decided here</strong></td>\n</tr>\n<tr>\n<td><strong>6, 7, 8</strong></td>\n<td><strong>EMPTY</strong></td>\n<td><strong>new</strong></td>\n</tr>\n</tbody>\n</table></markdown-accessiblity-table>\n<p dir=\"auto\">No B=16 counterexample exists with <code class=\"notranslate\">deg(q1) ≤ 8</code>. This extends the paper's verified exclusion and marches toward their conjecture (all solutions have µ2=µ1=0 ⟹ <strong>B&gt;16</strong>), which would raise the plane-JC bound and close the entire B=16 program. Pushing now toward <code class=\"notranslate\">deg(q1)=12</code> (the campaign's resonant <code class=\"notranslate\">d=3·2²</code> cell).</p>\n<p dir=\"auto\">Also this session: the <strong>u=0 exceptional chart</strong> of the sol6 (4,6) frontier is decided dead with exact certificates (stratum obstruction −4779/4 at rung 3; (0,0) dies at rung 25 exactly; 3-prime polynomial gcds are pure denominator powers), and a <strong>monodromy sieve</strong> reproduces the geometric-degree floor 2–5 topologically and extends it (d=6,7,8 empty for irreducible one-cusp tears).</p>\n<p dir=\"auto\">Full detail in <code class=\"notranslate\">session44/B16_ABEL_LADDER.md</code> and <code class=\"notranslate\">session44/U0_VERDICT.md</code>.</p>\n<hr>\n<p dir=\"auto\"><em>Generated by <a href=\"https://claude.ai/code\" rel=\"nofollow\">Claude Code</a></em></p>",
  "created_at": "2026-08-27T01:17:42Z",
  "id": 5433105193,
  "in_reply_to_id": null,
  "line": null,
  "path": null,
  "pull_request_review_id": null,
  "review": null,
  "side": null,
  "start_line": null,
  "updated_at": "2026-08-27T01:17:42Z",
  "url": "https://github.com/git-df-scott/jacobian_planar/pull/20#issuecomment-5433105193",
  "user": {
    "avatar_url": "https://avatars.githubusercontent.com/u/282750673?v=4",
    "email": null,
    "id": 282750673,
    "login": "git-df-scott",
    "name": "git-df-scott"
  }
}
```

## PR #21 — night1: deformation depth-map engine for the JC2 campaign

[Original pull request](https://github.com/git-df-scott/jacobian_planar/pull/21) · state `open` · created `2026-08-28T01:16:15Z` · updated `2026-09-04T00:46:01Z`

Head: `claude/fable-6o0nqe` at `a105bc93e43b9766b90763b2c62ef9df26ddfc36`. Base: `main`. Merged: `None`.

### Original description

## What this is

A new instrument for the plane Jacobian Conjecture campaign: instead of searching coefficient space for a counterexample directly, this measures the **obstruction depth** of order-by-order Keller deformations at known automorphisms under hard degree caps.

- `night1/engine.py` — self-contained engine (numpy only): polynomial arithmetic over F_p, the linearized Keller operator, tower integration, and a mandatory control suite (kernel identity check, positive calibration on provably-polynomial flows, negative calibration on a provable degree-overflow obstruction). The engine refuses to produce data if any control fails, and any deep/surviving tower is re-verified by an independent code path that multiplies the deformation out directly.
- `night1/spec_*.json` — grid specifications (automorphisms × Hamiltonian directions × caps × two primes).
- `night1/RUNBOOK.md` — night-shift procedure and reading rules. All results are modular and reported as modular; no interpretation happens overnight.
- `night1/results/smoke.csv` — validation run: calibrated cells survive with independent verification PASS; live probes obstruct at finite, cap-responsive depths.

## Status

Overnight grid runs in progress; results are committed incrementally to this branch as CSVs plus stored towers for deep cells.

---
_Generated by [Claude Code](https://claude.ai/code/session_01CyART5uKsyN88J2yG8aKqf)_

### Archived discussion

0 entries; full normalized metadata in PR_DISCUSSIONS.json.

## PR #22 — Add unified JC2 counterexample-hunt fleet plan with audit appendix

[Original pull request](https://github.com/git-df-scott/jacobian_planar/pull/22) · state `open` · created `2026-09-02T14:19:28Z` · updated `2026-09-03T03:27:48Z`

Head: `claude/jc2-handoff-audit-hartnc` at `ae58bd33dc6a037e9d421a8a0b102c1ad7a2d6f3`. Base: `main`. Merged: `None`.

### Original description

## Summary

Adds `docs/plans/CE_HUNT_PLAN.md`, a unified plan for the next counterexample hunt on the plane Jacobian conjecture, built by a fleet of agents:

- Nine parallel readers audited the canonical campaign branch (`claude/opus-5-counterexample-plan-sep6yk` at 24a06fc), the Codex mailbox and pentagon branches, and the support branches, with file citations for every claim.
- Five independent planners (enumerated corners, characteristic-zero verdicts, structural routes, fleet engineering, skeptic) proposed leads.
- Three adversarial reviewers checked the premises against the files, the mathematics, and the ordering.

The plan contains: honest probability framing (campaign-level p(HIT) of order one in a thousand, decomposed), a state-of-play table, twelve audit gates that must pass before any compute, nine ordered leads with premises, methods, agent roles, stop rules and costs, fleet roles and a verdict schema, a two-week schedule, campaign stop conditions, and open questions.

## Corrections carried from the reviews

- `trackB1_sat_Q.ms` (166 vars / 284 eqs) exists on the mailbox branch under `wave6/frontier/`; the README's 164/288/6821 asset does not match any file.
- The pentagon truncation witness certifies every weight at least 8 alive, so the truncation ladder is refuted and removed from every queue.
- EMPTY over Q is certified only by an explicit cofactor identity 1 = sum h_i f_i; the reduce-to-zero-plus-Buchberger check certifies containment (a NONEMPTY certifier), not emptiness.
- Collision-first search is an interpretation tool bounded by the base cell's probability; the sum-of-squares distinctness form is unsound over C.
- A reconstruction gate H0 precedes the HIT protocol; a new ADMISSIBLE-SHAPE label separates leading data from candidates.
- The Weyl-algebra route uses the correct direction (contrapositive of JC_2 implies DC_1) but is not effective and needs a Poisson-commuting base point.
- Tail-closure is decided by a factorization audit of the compiler, not by a sample count.

## Appendix

`docs/plans/appendix/` holds the reader map, the five planner outputs, and the three reviews. The README gains a pointer to the plan.

No solver was run and no verdict in the archive was changed; this is a plan, not a result.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01DyAkYTorVojkD4dFMMJGgH

---
_Generated by [Claude Code](https://claude.ai/code/session_01DyAkYTorVojkD4dFMMJGgH)_

### Archived discussion

0 entries; full normalized metadata in PR_DISCUSSIONS.json.

## PR #23 — JC2 counterexample hunt: night run log and direct attempts

[Original pull request](https://github.com/git-df-scott/jacobian_planar/pull/23) · state `open` · created `2026-09-03T05:13:33Z` · updated `2026-09-03T18:32:10Z`

Head: `claude/jc2-counterexample-hunt-handoff-w369mc` at `e0086a78682a1b91fe483f16e5698b8eda48b6eb`. Base: `main`. Merged: `None`.

### Original description

## Summary

Overnight execution of the direct attempts in `docs/plans/HANDOFF_CE_HUNT.md` (handoff branch `claude/jc2-handoff-audit-hartnc`, PR #22). No counterexample. Everything below carries its label and resource wall; no timeout, OOM or segfault is reported as a verdict.

### Findings (`docs/plans/night/RUN_LOG_2026-09-03.md`)

- **Record correction.** `p108_525122` is the paper's Proposition 4.3 case (2) quadrilateral; only `p108_192622` is a (9,27) stratum, and it is a compiler stratum that Proposition 4.1 excludes. The paper's actual (9,27) polygon has 172 driver parameters and is not buildable in the y-adic extractor on this box.
- **Structure.** The y-adic shape systems are linear chains after the first block, positive-dimensional through most of the chain, with generators of degree up to 55; every one-shot Groebner attempt walls (segfault at 4 GB, OOM at 9 GB, Singular timeouts). True torus rank is 3, fully absorbed by the Rabinowitsch-forced variables (the register's ranks were capped upper bounds).
- **Exact elimination.** A fast extractor (python-flint, exact match to the committed systems, under a second), an exact torus-chart reducer, and an exact linear-chain eliminator with zero-branching decide these systems where Groebner engines cannot. The (9,27) c'=0 eps-swap stratum is a one-parameter family at truncation depth 4 that dies at depth 6.
- **25 strata closed exactly over Q** by one-line monomial certificates (a coefficient of some Q_row outside N(Q) equal to a nonzero rational times a monomial in nonzero variables), found by a library-wide sweep and recomputed exactly over Q, including a (108,144) stratum, the first exact closure above max degree 125 in this campaign (under the compiler's A'_t and c'-ladder assumptions). Table in `docs/plans/night/artifacts/sweep_table.md`.
- **Walls, labelled.** d=8 chart N degBound 8 at 6 GB; pentagon and paper's (9,27) shape not buildable in this formulation; 4 of 17 terminal branches of the p108_192622 stratum at depth 6.

Tools under `docs/plans/night/tools/`, data under `docs/plans/night/artifacts/`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01Kec8oVf9pwVhTz6LpMLJLL

### Archived discussion

0 entries; full normalized metadata in PR_DISCUSSIONS.json.

## PR #24 — Clues audit across all branches, 2026-09-03

[Original pull request](https://github.com/git-df-scott/jacobian_planar/pull/24) · state `open` · created `2026-09-03T21:57:58Z` · updated `2026-09-04T03:31:38Z`

Head: `claude/jc2-counterexample-hunt-handoff-x40ahz` at `0aab6fb4036a4c4bff7e375a2bf9454a22a60790`. Base: `main`. Merged: `None`.

### Original description

## Summary

Adds `docs/plans/audit/CLUES_AUDIT_2026-09-03.md`: a read-only sweep of all 37 branches for clues, not for a counterexample. No solver was run and no new verdict is claimed.

Main findings recorded:

- The Prop 4.3 case (2) quadrilateral (`p108_525122` polygons, `scb0881`) has four independent emptiness records on side branches and in canon that the night run of 2026-09-03 did not know about. The thin-polygon grading used by `campaign/audit_tracks/CASE2_VERDICT.md` and by `claude/poisson-bracket-counterexample-9esk1r:x2/` decides it in seconds per orbit, where the y-adic eliminator timed out.
- The night's linear-chain eliminator has no positive control at depth 6.
- Mailbox items FABLE-004 and FABLE-006 already contained the night's two headline corrections plus structural facts for case (2) that nothing uses.
- `STATE_FULL.md` and `ADJUDICATION.md` still carry the B=16 ladder rows that `CATCHES.md` voided; the transfer tarball has a 125-line CATCHES.md.
- Eleven side-branch results absent from canon, including the level-14 rational obstruction, the level-16 witness, the bottom-edge Galois factorization, and the above-125 enumeration data canon marks ABSENT.
- Every near-miss in the archive is a vertex degeneration.

## Test plan

- [x] Every cited file:line spot-checked against the worktrees
- [x] Literature claims checked against arXiv 2608.00222 and 2204.14178

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01AW4QvZfTug7CiSShV1tJEJ

---
_Generated by [Claude Code](https://claude.ai/code/session_01AW4QvZfTug7CiSShV1tJEJ)_

### Archived discussion

0 entries; full normalized metadata in PR_DISCUSSIONS.json.

## PR #25 — Organize main: entry points, README fixes, and a full branch audit

[Original pull request](https://github.com/git-df-scott/jacobian_planar/pull/25) · state `open` · created `2026-09-04T00:32:24Z` · updated `2026-09-04T00:57:27Z`

Head: `claude/github-repo-organization-wdr8n7` at `5c41b3afbbc2927560c3c193ac3cd39b2571786b`. Base: `main`. Merged: `None`.

### Original description

## Summary

- Add `CLAUDE.md` and `AGENTS.md` at repo root — thin pointers so a fresh Claude Code or Codex session reads `README.md` on its first turn instead of guessing.
- Add the three most recent handoff branches (`claude/jc2-handoff-audit-hartnc`, `claude/jc2-counterexample-hunt-handoff-w369mc`, `claude/jc2-counterexample-hunt-handoff-x40ahz`) to the README's branch map — they continue past the canonical branch's head and were missing from the map entirely.
- Add `fable-6o0nqe` to the prose Claude-workstreams list (it was already in the exact-heads table but not the list).
- Add an **Open pull requests** section to the README indexing all 24 draft PRs, so an agent can see everything in flight without querying GitHub.
- Correct a stale claim: the README said sessions 43–44 are "not present in the repository," but they're on open PRs [#19](https://github.com/git-df-scott/jacobian_planar/pull/19) and [#20](https://github.com/git-df-scott/jacobian_planar/pull/20), just not merged into `main`.
- **New:** add `docs/BRANCH_AUDIT.md`, a full audit of all 38 branches confirming (a) nothing pushed to GitHub is lost — no unpushed local state, no stashes, no dangling commits, `wip:`-labelled commits are already on `origin` — and (b) no branch's real content contradicts what README claims about it, including a dedicated section on the 8-of-9 `codex/*` branches that have no PR (expected — Codex branches were never wrapped in PRs the way this session's Claude Code branches are).
- Refresh README's "Exact branch heads" table to 2026-09-04: a prior session-local cleanup pass (removing stale root-level `39`/`40.md`/`41.md`/`42.md` from 29 branches, done directly against each branch per user request, outside this PR) moved almost every head past the 2026-09-01 snapshot recorded there.

## Verification

- Checked all 38 remote branches' heads, PR status, and top-level file listings against README's claims — see `docs/BRANCH_AUDIT.md` for the full methodology and findings.
- `git branch -vv`, `git stash list`, `git fsck --unreachable --no-reflogs` show no unpushed/lost work in this session.
- Grepped tracked `main` content and all branch commit messages for credential/secret and "lost work" patterns — none found.
- Read the newest branches' content to confirm their claims are consistent with the rest of the record — no counterexample is claimed anywhere.

## Test plan

- [x] README renders correctly (checked section anchors and table formatting)
- [x] All links point to real branches/PRs (verified against `git branch -r` and the GitHub PR list)
- [x] Every branch head in the refreshed table matches `git rev-parse --short origin/<branch>` at time of writing
- N/A — no code changes, documentation/organization only

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01B9Xs4q8rKQmsak57MarYHa

### Archived discussion

0 entries; full normalized metadata in PR_DISCUSSIONS.json.

## PR #26 — Superseded: math mailbox moved to its own shared repository

[Original pull request](https://github.com/git-df-scott/jacobian_planar/pull/26) · state `closed` · created `2026-09-04T20:30:00Z` · updated `2026-09-04T20:52:13Z`

Head: `codex/cloud-math-mailbox` at `f916d7b438622cd4f776414bc8e4c42b7f6dc613`. Base: `main`. Merged: `None`.

### Original description

Superseded by the standalone [git-df-scott/math-mailbox](https://github.com/git-df-scott/math-mailbox) repository, which serves cloud math sessions across projects. The shared implementation is installed on its main branch with independent channels, named participant addresses, cross-repository Codex routes, and per-routine Claude tokens. All 45 unit tests and its [cloud storage integration check](https://github.com/git-df-scott/math-mailbox/actions/runs/33918178943) passed.

This Jacobian-specific prototype should not be merged. Its existing data branch remains empty and disabled. Future setup starts with the standalone repository's START_SESSION.md; account ping destinations remain unconfigured.

---

The shared Markdown mailbox required agents to poll manually and could leave replies saved only in a workspace. This adds a GitHub-backed mailbox that confirms remote writes, gives each request a stable ID and one reply slot, and records platform acceptance separately from an agent's read receipt.

The cloud relay can request a new Codex cloud task through a collaboration PR and start a Claude Code routine using its selected model (Fable 5.1 for this collaboration). Claims, thread expiry, reply limits, delayed rate-limit retries, and conservative handling of uncertain launches prevent duplicate work and notification loops. Existing campaign and mailbox history remains intact.

Both routes start disabled. Activation requires installing the source on the default branch, connecting a Codex collaboration PR and Claude routine, configuring cloud credentials, and completing one real agent handshake. It does not inject messages into arbitrary existing chats. The setup and recovery guide is in [docs/math-mailbox.md](https://github.com/git-df-scott/jacobian_planar/blob/codex/cloud-math-mailbox/docs/math-mailbox.md), with the receiving protocol and Claude routine prompt under `tools/math_mailbox/`.

Validation: all 30 unit tests and the real GitHub storage integration check [passed in Actions](https://github.com/git-df-scott/jacobian_planar/actions/runs/33916500471); the [PR checks also passed](https://github.com/git-df-scott/jacobian_planar/actions/runs/33916524027). The storage check completed a send/readback/claim/ACK/reply cycle with both ping routes disabled and removed its temporary branch. Actual agent wake-up remains untested until destinations are connected; no mathematical run was started.

The [empty mailbox/v2 branch](https://github.com/git-df-scott/jacobian_planar/tree/mailbox/v2) is initialized from this infrastructure commit, with both routes disabled and no pending messages.

### Archived discussion

0 entries; full normalized metadata in PR_DISCUSSIONS.json.
