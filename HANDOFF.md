# Session handoff — Jacobian campaign, night of 2026-08-21/22

Branch `claude/jacobian-planar-sweep-iajyma`, PR #13 (draft, base
`claude/opus-5-counterexample-plan-sep6yk`, mergeable).

**No counterexample was found.** Everything below is ground closed, tools built,
or errors corrected. Read §1 and §7 first if you read nothing else.

---

## 1. THE MOST IMPORTANT THING AT HAND

**The target is pentagon case (1), carried by
`wave6/frontier/trackB1_sat_p1000003.ms` — the unreduced root, 166 variables,
284 equations, max degree 5, 170 KB.**

**Attack it through its SUBSYSTEM BLOCKS, not directly** — the root itself has
now failed seven budgeted attempts. See "What to run" below.

This is the **only target in the repo where a NONEMPTY verdict would be a
counterexample candidate.** It is the exact char-0 case (1) system mod
p = 1000003, carrying the saturation
`zsat·c_1_0·c_8_14·d_12_21·s_4_8 − 1` that enforces all four nondegeneracy
conditions. A solution of this system is an admissible point of case (1).

### Read this before running anything: the reductions were de-optimizations

An earlier version of this section named `reduced_tb1deep_82v.ms` (83 vars).
**That was wrong, and so was every other reduced export.** Measuring them:

| export | vars | max degree | total terms | outcome |
|---|---|---|---|---|
| `trackB1_sat_p1000003.ms` (**root**) | 166 | **5** | **8,774** | never given a real budget |
| `reduced_tb1deep_99v.ms` | 100 | 19 | 414,175 | Singular OOM, `halt 14` |
| `reduced_tb1deep_82v.ms` | 83 | — | ~1.5 M | `halt 1`, no verdict |
| `reduced_tb1deep_60v.ms` | 61 | — | ~5.3 M | 240 MB, cannot even load |

The forced chain trades variables for degree, and Gröbner cost is **doubly
exponential in degree**. Dropping 66 variables raised the degree from 5 to 19
and the term count 47-fold. Every "deeper" reduction was strictly harder than
the one before, and the whole trackB1 NO-VERDICT chain is the consequence.

**The root is the easiest form of this question and it is the one that never
got resources.** `w6_branch_solve.py` defaults are `LEAF_MEM=4000000` (4 GB)
and `LEAF_T=120` (2 minutes) — that is all the root ever received, while the
degree-19 blowup got 9 GB and hours. Do not re-derive a reduction.

**But the root has since been given real budgets, seven times, and none
resolved it** — see "What to run" below. The reductions remain the wrong object;
the root is merely the *least* wrong one, and it is still out of reach. The live
route is subsystem blocks.

### Engine choice is not free — the two engines fail on different axes

- **msolve dies on a hard 2²⁵ MONOMIAL ceiling.** It aborts with
  `Enlarging exponent vector for hash table failed, esz = 33554432`.
  ~~Its monomial hash table is dense in nvars, so 2²⁵ × 166 slots ≈ 22 GB.~~
  **That was my diagnosis and it is refuted.** The identical constant appears at
  166, 148 **and 61** variables, and at 6 GB, 9 GB and 13 GB. A quantity that
  does not move when variables drop threefold and memory rises twofold is
  neither. It is a hard internal cap of 2²⁵ hash-table entries. msolve is
  correct on small systems (`[-1]` for empty, a parametrization otherwise); it
  simply cannot take anything whose F4 exceeds that. **Do not spend time on it,
  and do not try to buy past it with RAM.**
- **Singular `slimgb` dies on TIME here**, not memory — every root run was still
  computing when the clock killed it, none crashed. It uses sparse exponent
  vectors, so 166 variables cost it nothing; it ingests the root at ~343 MB.

The earlier claim that "we had the engines pointed backwards, few-terms/many-vars
to msolve and few-vars/many-terms to Singular" was built on the refuted
variable-count story. The true asymmetry is simpler: **msolve has a monomial
ceiling it cannot pass; Singular has no ceiling but needs time.**

### What to run — UPDATED after seven failed root attacks

**Do not attack the root directly.** Seven attempts closed, all NO VERDICT:
msolve at 13 GB (hash-table abort), Singular dp at both primes, block order
`(dp51,dp115)`, 3-block `c>d>s`, `stdhilb`, and a degree ladder — the ladder
completing **zero rungs** at 166 variables. Singular never crashed and never ran
out of memory on these; every one was still computing when the clock killed it.
See `wave6/frontier/TB1_RUN_LEDGER.md` for the full table.

**msolve is out entirely, for a reason worth knowing.** It aborts at
`esz = 33554432` = 2²⁵ hash-table entries on *every* hard target here — at 166,
148, and 61 variables alike, and at 6 GB, 9 GB, and 13 GB alike. It is a hard
internal ceiling, not a variable-count or memory problem. (I diagnosed it wrong
twice before checking that the constant never moved.) msolve works fine on small
systems; it simply cannot take anything whose F4 exceeds 2²⁵ monomials.

**Run the SUBSYSTEM BLOCKS instead.** `wave6/w6_tb1_subsystem.py` and
`wave6/w6_tb1_square.py`. Emptiness is monotone, so any subset of the 284
equations that is empty proves trackB1 empty. There is no overdetermined block
(max surplus 0), but there are square ones, and critically **all four saturation
variables `c_1_0, c_8_14, d_12_21, s_4_8` lie inside them**, so each block
carries the full nondegeneracy condition:

| block | size | degree | terms |
|---|---|---|---|
| smallest nontrivial | 60 eq / 60 var (61×61 saturated) | 4 | **533** |
| larger | 96 eq / 96 var (97×97 saturated) | 4 | 1,357 |

against the root's 8,774 terms at degree 5.

  * **block EMPTY ⇒ trackB1 EMPTY. A real verdict.**
  * block NONEMPTY ⇒ inconclusive for trackB1, but yields a small solution set
    to test against the remaining equations — itself a decision procedure.

Note the plain (unsaturated) block is *also* verdict-capable in the EMPTY
direction; saturation is only needed to make a NONEMPTY result meaningful.

**Pair blocks with degree-bounded ladders** (`degBound = d; std(I)`). One-sided:
a unit at any rung proves EMPTY, no unit proves nothing. This is the only method
tonight that produced *incremental* output rather than a binary timeout — the
61-block ladder cleared degrees 4 and 5, the 97-block ladder likewise. Both then
needed more memory at rung 6 (`halt 14`), which is a fixable cap, unlike
msolve's ceiling.

**`wave6/w6_tb1_grow.py`** walks blocks upward automatically, re-saturating at
each step, and stops at the first EMPTY. Built but not yet run to completion.

If EMPTY → case (1) is empty at that prime by a *stronger* route than the seed
argument (it presupposes no seed decomposition). If NONEMPTY → **stop
everything and lift the point exactly**; that is the counterexample candidate.

## 1b. The structural fact that reframes trackB1

`wave6/w6_tb1_rank.py`. **283 of the 284 equations are affine-linear in the
entire 51-variable c-block** — only the saturation row is quadratic in c. So

    A(d,s) · c = b(d,s),    A of shape 283 × 51,

and the c-block eliminates by **Gaussian elimination** (Golub–Pereyra variable
projection) at *zero* degree cost — exactly what the chain failed to do.

Measured at p = 1000003 over 12 random `(d,s)`: `rank A = 51/51` and
`rank[A|b] = 52` every time, i.e. **inconsistent at every probe**. So the
projection of the trackB1 variety to `(d,s)`-space is **not dominant**: a
generic parameter point admits no c, and any solution lies in the proper
determinantal locus `rank[A|b] = rank A` in the **114 d/s variables alone**.

This is **NO VERDICT on emptiness, not evidence for it** — consistency is a
proper closed condition and random points miss a proper closed subvariety by
construction. Do not record it as EMPTY.

Two cautions carried forward, both mine:
- The script first asserted the system was *homogeneous* in c. **That assertion
  fired and was false** (eq 8 has a c-free term). The guard caught a wrong
  claim before it reached a report — keep the guards.
- `rank[A|b] = rank A + 1` is **structurally forced** (one extra column raises
  rank by at most one). It carries no information. I nearly wrote it up as
  "minimal obstruction"; that would have been error #5 again.

Note the untried lever: only **4 variables (the s-block) carry any
nonlinearity**. Fixing s makes the whole system bilinear in (c,d).

---

## 2. RESULTS ESTABLISHED

### Bottom-edge orbit structure — SETTLED exactly over ℚ
`wave6/bottomedge/ORBIT_VERDICT.md`, `AUDIT_SWEEP.md`

Degree-9 eliminant factors **1 + 1 + 2 + 5**, all four factors irreducible over
ℚ and squarefree. The five admissible seeds form a **single Galois orbit**, so
one seed decides all five. Degenerate locus = 2 rational + one quadratic orbit,
all with `c8 = d12 = 0`, by multiplier-independent gcds. **3 of 9 seeds real,
exactly one admissible.** Corroborated by a **13-prime census, zero anomalies**,
admissible mean 1.077 against the quintic's predicted 1.000.

### The admissible seed does NOT extend — two primes, two engines
`wave6/SEED_VERDICT.md`, `wave6/TWO_PRIMES.md`, `wave6/certificates/`

| | p = 1000003 | p = 1000039 |
|---|---|---|
| msolve | `[-1]` | `[-1]` |
| Singular `slimgb` | UNIT IDEAL | UNIT IDEAL |
| Nullstellensatz certificate | 9 multipliers, 53 terms, deg 5 | same |
| independent re-verification | **PASS** | **PASS** |

p = 1000039 is **like-for-like**: I reconstructed the seed-pinning myself
(mapping `c_i ↔ c_i_{2i−2}`, `d_j ↔ d_j_{2j−3}`), validated by rebuilding the
campaign's own p = 1000003 export **equation for equation, all 266 identical**.

### Separator #2 — the descent route cannot produce a plane counterexample
`wave6/DESCENT_MASTER.md`, certifier `wave6/w6_descent_master.py` (7/7)

Closed form: **det JG ∘ π = (q′ ∘ F)/q**, where `q, q′` depend only on the
weight systems, not on F — which is why A1 was hard as posed. It predicts both
the exponent 2 *and* the identity `h = f₃/x` that Session 39 found by direct
computation. For weights `(1,−b,−c)`, `q = x^{b+c−1}`, so **k ≥ 2 is NOT
forced** (k = 1 at `(1,−1,−1)`). But a Keller descent forces `k = k′` and
`F₁ = λx`, hence F is fibered with plane-Keller fibers, hence every collision is
already a plane Keller collision.

### Plane tangent-sweep family — 501/501 closed
`wave6/LIVE_SHAPES_RESOLVED.md`

The sweep's 2 LIVE shapes are resolved: every branch forces all `k_t = 0`, so
`p ≡ 0` and the map is **affine and injective**. Not counterexamples.

### OPEN-1 h-branch frontier — both unresolved cases decided
`wave6/frontier/RESOLVED_k5.md`

| case | campaign | here |
|---|---|---|
| k=5, h=t, D=4 | OOM at 2m46s | **EMPTY** — 15 leaves |
| k=6, h=t, D=4 | "no more memory", 3m40s | **EMPTY** — 22 leaves |

msolve — the fix `FRAMEWORK.md` explicitly named and never ran — **also failed**
(SIGSEGV at 6 GB, no verdict at 10 GB). What worked was branching.

### (9,27) branch of (72,108) — 2 of 4 decided
`wave6/frontier/P108_RESULTS.md`

`p108_843700` **EMPTY**, `p108_821326` **EMPTY**, `p108_525122` 3-of-5 leaves
empty (root NO VERDICT), `p108_192622` NO VERDICT.

### SF target — resolved, never previously run
`campaign/d23_borisov/SF_TARGET_RESOLVED.md`

`d23_n3_msolve.py` prints run commands for two systems; the validation output
exists, **the target's does not**. Ran it: SF (14,9,23) is **NONEMPTY, dim 0,
vdim 14** (FF is vdim 2). Does **not** contradict Phase 1 — that death is an
integrality obstruction at the chain layer, not a realizability one. The count
is new.

### Case (2) audit — a verdict whose control never completed
`wave4/CASE2_CONTROL_AUDIT.md`

The p = 1000003 EMPTY (`full_one_pin`, 6 bytes) was accepted while its own
planted-point control (`full_one_mutant`) returned **0 bytes** at 3.9 GB. I
verified without any solver that the plant is genuine — supplying the missing
`sat = 666673` gives **96/96** — so that system is nonempty by construction and
its run was a **failed control**, not a result.

### Other cells closed
`wave5/ms/m16_d6_p1000003.ms` EMPTY; `wave5/ms2/b16r_d5_A_q.ms` **EMPTY in
characteristic 0**. Sweep of 160 unsolved exports: 31 EMPTY, 48 NO VERDICT.

---

## 3. TOOLS BUILT (all in `wave6/`)

| file | what it does |
|---|---|
| `w6_branch_solve.py` | **branch → forced chain → slimgb → msolve.** Splits on monomial equations `uv=0`. P-POS/P-NEG controlled. |
| `w6_chain_export.py` | `chain_core` — the exact forced chain, mod p, with checkpoint exports. Verified identical to the shipped `main()`. |
| `w6_forced_chain.py` / `2.py` | the chain over ℚ (exact `Fraction`) |
| `w6_verify_cert.py` | **independent** certificate checker — own parser, own arithmetic, no Singular |
| `w6_descent_master.py` | the A1 certifier, 7/7 |
| `w6_prime2.py` | trackB1 mod p with 4 built-in bug checks |
| `w6_seed_prime.py` | rebuilds the seed-pinning at any prime; self-controls against the campaign's own export |
| `w6_unpinned_q.py` | the unpinned ℚ-system builder |
| `w6_sweep_cells.py` | sweeps every unsolved `.ms` with Singular |
| `ms2singular.py` | `.ms` → Singular, with the symbol guard |
| `w6_cert_lift.py` | CRT certificate reconstruction (aimed at the wrong system — see §5) |
| `frontier/gen_hbranch.py` | regenerates the campaign's *own* h-branch systems |

**Installed this session and not present before: `msolve` and `Singular 4.3.2`.**
Singular `slimgb` is the strongest engine here by a wide margin.

---

## 4. THE METHOD THAT WORKED, AND ITS BOUNDARY

Branching beat a memory wall that more RAM and a different engine could not.
**But it is structure-dependent:**

- h-branch: **6 monomial equations sharing variables** (`c_46` in 4 of 6) →
  collapsed to 15 and 22 easy leaves. **Worked.**
- trackB1: **2 monomial equations, both on `c_1_0`** → one split, leaf still
  163 of 166 variables. **Bought nothing.**
- (9,27): shallow trees, leaves nearly as hard as roots. **Half-worked.**

> **Branching converts a wall into progress in proportion to the number of
> *independent* monomial equations. One shared pivot variable gives one split,
> and one split gives nothing.**

When branching fails, the lever is **the reduction** (the forced chain), not the
solver. That is what got trackB1 from 166 to 83.

---

## 5. MY OWN ERRORS — all caught, all corrected

Read these before trusting any tooling here.

1. **Elimination bug** (`RETRACTION_msolve.md`) — `subs_linear` skipped
   monomials of degree ≥ 2 in the pivot, so variables were counted eliminated
   while still present; exports declared 100 variables and used 109; msolve
   returned a **false `[-1]`**. Fixed, and `write_ms` now *asserts* against
   undeclared symbols.
2. **117 vs 118** — corrected. 118 stands un-localized (rank is exactly 283,
   zero dependent equations); 117 appears only after localizing.
3. **Two overclaims stated as fact** — "no small overdetermined subsystem
   exists" (a greedy heuristic, 283 paths vs 2¹⁶⁵ subsets) and "w₀ = 1 is
   exactly where the invariant ring is polynomial" (only one case checked).
   Both softened.
4. **A void desaturation test** — I stripped my `zz9` but left the campaign's
   own `zz0`, so both sides were saturated. Withdrawn.
5. **A tautology cited four times** — "overdetermined by 118, so emptiness is
   expected." My own planted control has the identical shape *and has a
   solution*. Retracted as evidence.
6. **NOTUNIT / NO-VERDICT conflated** in `w6_cert_lift` — hid a 1200 s timeout
   behind wording that read like a result. Separated.
7. **`parse_ms` crashed on characteristic 0** (`% 0`), silently killing four
   char-0 cells into a log. Fixed.
8. **Two saturation-variable slips** (`−p0·r0·t−1`, and `sat` in the case-(2)
   plant). **Pattern: when a saturated system looks one equation short of
   satisfied, the missing equation is the saturation row and the fault is
   mine.**

**Every one was caught by checking the artifact, not the algorithm.** The
back-substitution check *passed* while a variable was not really eliminated; the
desaturation test *passed* while the system was still saturated. What caught
them was counting symbols in the file and reading line 269 by hand.

---

## 6. STANDING RULES (the campaign's, reconfirmed the hard way)

- **0-byte output is NO VERDICT.** Not EMPTY, not a hit. msolve exits 0 on
  timeout, crash, and parse error alike.
- **exit 139 = SIGSEGV = NO VERDICT** (memory), **124 = timeout = NO VERDICT.**
- **A malformed `.ms` returns a false `[-1]`.** Check
  `header ⊇ symbols(body)` before trusting any verdict.
- **Sequence, do not race.** Two heavy jobs both wanting the ceiling is how the
  prime-2 SIGSEGV happened; `modStd` also spawned 4 workers holding 8 GB after
  I thought I had killed it.
- **Modular emptiness is unsound for contradictions.** Two primes minimum, and
  char 0 is still owed.

---

## 7. PLAN FOR THE NEXT SESSION

**P1 — Get the trackB1 83-variable verdict.** §1. This is the whole ballgame.
Nothing else in the repo can produce a counterexample candidate.

**P2 — If P1 is EMPTY, get it at a second prime**, then decide char 0. The
correct char-0 target is the **unpinned** system: the seed-pinned one lives over
a degree-5 number field (the seed is a root of the irreducible quintic) and its
certificate can **never** be CRT-reconstructed over ℚ. `w6_cert_lift.py` was
aimed at the wrong object for exactly this reason.

**P3 — Finish the case-(2) control.** `wave4/CASE2_CONTROL_AUDIT.md`. Singular
on `c2_full_one_mutant_p1000003.ms` (nonempty by construction). If it recovers
the plant, the p = 1000003 EMPTY is supported; if not, that leg should be
labelled unvalidated rather than counted among three certified primes.

**P4 — The residual named leaves.** `p108_525122` has exactly 2 unresolved
leaves (one is 29 eq / 23 vars, resistant to both engines + the chain) and
`p108_192622` has 1 (139 eq / 38 vars). These are *named*, small, and closest to
the main line.

**P5 — The 48 sweep NO-VERDICT cells**, ranked in
`wave6/frontier/TARGET_QUEUE.md`. **Exclude the 14 `bottomedge/be_*` entries** —
they are NO VERDICT only because they are *nonempty and slow*, and counting them
as leads would be counting known results as discoveries.

**P6 — Generalize the descent formula beyond C\*.** Pure derivation, no compute.
Nothing in it used more than "the kernel of Jπ is spanned by the infinitesimal
action" and `det JF = 1`, so a finite group or higher-rank torus should give the
same rigidity — which would widen separator #2 from one mechanism to every
quotient-type construction. **Highest value per unit of compute in the repo.**

### Where a counterexample could still live

Everything below degree 125 that this campaign has touched is closed or
expected-empty. If one exists with B > 20 it is **above degree 125** — the 429
`NO-CHAIN` cases and the 3 live entries at degrees 250, 252, 294
(`wave6/frontier_151_300_map.json`), plus 254 orphaned live shapes. Those are
blocked on a chain-compiler, not on mathematics. **That is the honest place to
look, and nothing tonight touched it.**
