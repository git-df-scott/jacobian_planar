# Session handoff — Jacobian campaign, night of 2026-08-21/22

Branch `claude/jacobian-planar-sweep-iajyma`, PR #13 (draft, base
`claude/opus-5-counterexample-plan-sep6yk`, mergeable).

**No counterexample was found.** Everything below is ground closed, tools built,
or errors corrected. Read §1 and §7 first if you read nothing else.

---

## 1. THE MOST IMPORTANT THING AT HAND

**`wave6/pentseed/reduced_tb1deep_82v.ms` — pentagon case (1), unpinned,
saturated, reduced to 83 variables / 200 equations.**

This is the **only target in the repo where a NONEMPTY verdict would be a
counterexample candidate.** It is trackB1 (the exact char-0 case (1) system)
reduced mod p = 1000003 by the exact forced chain, still carrying the saturation
`zsat·c_1_0·c_8_14·d_12_21·s_4_8 − 1` that enforces all four nondegeneracy
conditions. A solution of this system is an admissible point of case (1).

- **166 → 83 variables** by exact implication only. Symbol-guard verified
  (83 declared, 83 used, 0 undeclared).
- 83 variables is inside the range where Singular `slimgb` has been returning
  verdicts in **seconds** all night (92-var and 89-var systems both did).
- Run it: `Singular -q` on the output of
  `python3 wave6/ms2singular.py wave6/pentseed/reduced_tb1deep_82v.ms OUT.sing`
- Was in flight at handoff. **Get this verdict first.**

If EMPTY → case (1) is empty at that prime by a *stronger* route than the seed
argument (it presupposes no seed decomposition). If NONEMPTY → **stop
everything and lift the point exactly**; that is the counterexample candidate.

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
