# Morning summary — overnight session (2026-08-21)

## Bottom line

No counterexample. Two of my own results were RETRACTED after controls caught
them. The night's real product is (a) a set of exact structural results that
make a coherent case the B=16 ladder is closed, and (b) two methodological
catches that protect every future verdict.

## What is now DECIDED (exact, control-backed)

* Rank criterion at the quasi-homogeneous points, **d = 3..15, 18, 20 and 27**,
  both roots of the row-0 quadratic, every case: the augmented rank exceeds
  the plain rank by EXACTLY ONE -> ALWAYS OBSTRUCTED. No counterexample
  bifurcates off that stratum at any d tested. **d = 27 is the decisive one**:
  it is the next resonant level (12d = 324 = 18^2, both roots rational), the
  place the resonance law says degeneration is most likely -- and it is
  obstructed at both roots (ranks 53 -> 54, 107 eqs, 80 unknowns).
  d = 18 (35 -> 36) and d = 20 (39 -> 40) likewise. d = 48, the next
  resonant level, needs hardware that stays up (198 eqs, 143 unknowns).
  (Rank VALUES were corrected to 2d-1 -> 2d once the (1.2) constraints are
  eliminated before differentiating; the verdicts are unchanged.)
* The factored form of GGV (1.3):  6 D (D+2C) = y (4AA' - mu2 q1^2 + 3mu1 y q1
  - 6 mu0 y^2) with D = A - q1^2/4, reducing to 6DE = (same RHS). Three exact
  checks pass, including: the leading-coefficient balance REPRODUCES the row-0
  quadratic (8d-6)a^2+3a-3/8 = 0, so the whole resonance law falls out of it.
* At the d=3 family the entire system collapses to exactly R = 6*mu0 -- a
  nonzero constant, independent of every family parameter. That is the precise
  mechanism of GGV's d=3 emptiness.
* Rigidity: a counterexample needs a degree-(4d-1) polynomial to collapse to
  the single monomial -6 mu0 y^2 -- 4d-1 conditions on 3d-1 unknowns, an
  excess of ~d that GROWS with d. Bigger cells are HARDER, not roomier.

## What is UNDECIDED (and why)

* d = 8, 9, 10, 11, 12 chart N. d=8 was attacked in four formulations
  (chart-split, GB-only via msolve -g 2, unsplit, 16-bit prime) -- all TIMEOUT
  with clean stderr. Exact elimination cannot decide these on this hardware
  inside the container's uptime, and no numerical substitute is admissible.
* (72,108): the resister systems still resist (worker's p108_525122 timed out
  at 1800s).  GGHV Cor 5.7, the only thing killing the (9,27) branch anywhere,
  has now been verified BY HAND -- and it is BROKEN (see below).  BOTH
  orientations of (72,108) are live.
* Pentagon case (1): still no verdict by any method.

## The two RETRACTIONS (both caught by controls I ran on my own work)

1. **Numerical "empty floors" are VOID.** Planted-root controls (a root
   inserted by construction, residual exactly 0.0) were NOT found by random
   multi-start at 25 unknowns (d=8) or 165 (pentagon). So the 1e-10 floors at
   d=8/9/12 measured the SOLVER, not emptiness. Multi-start is demoted to an
   opportunistic finder: a hit would be real, a miss says nothing.
2. **A fast "d=8 EMPTY" was an artefact.** msolve refuses to parse a constant
   generator that is a nonzero multiple of the characteristic -- and then
   EXITS 0 after writing "[-1]" to the output file. A parse failure wearing an
   EMPTY verdict's clothes. Caught because the hardened rerun took minutes
   where the artefact took seconds. Audit: all 131 campaign .ms files scanned,
   ZERO affected -- no prior verdict touched. New standing rule: capture
   stderr; "[-1]" plus a parse error is a FAILURE.

## Strategic synthesis (the thing worth acting on)

GGV prove **B = 16 or B > 20**. Every independent exact line above points to
B = 16 being empty. If that holds, a counterexample's degrees are multiples of
some B >= 21 -- necessarily ABOVE 125, where GGHV's elimination does not reach
and no reduction machinery exists at all. The above-125 frontier stops being a
side-quest and becomes the only remaining home for a counterexample; the
tail-closure predictor (last-2-segments + shape index -> system hash, zero
violations across every system this campaign ever generated) is what could
make that frontier finite.

## Two structural wins worth keeping

* Seeding the row-0 root covers the WHOLE cell (the relation is mu-free), so
  the Z/N chart split is unnecessary work -- it just adds a saturation
  variable. Roots are irrational (sqrt(12d)), so mod-p work needs primes where
  12d is a square.
* Prime size is irrelevant to the cost here (16-bit bought nothing): the
  bottleneck is Groebner structure, not coefficient arithmetic.

## Infrastructure reality

The container restarted FIVE times overnight, twice rolling the git tree back
to an older commit. Recovery: `git fetch origin <branch>` then
`git merge --ff-only`, after moving conflicting logs aside. Everything of
value is pushed. Generated .ms files are regenerable (wave6/w6_seed_d8.py).
Long computations (>~20 min) cannot survive and should not be scheduled here.

## Recommended next moves

1. Run the undecided ladder cells (d=8..12 chart N, seeded, unsplit) on
   hardware that stays up for hours -- they are small systems that simply need
   uninterrupted time.
2. DONE, and it failed: GGHV Cor 5.7 is UNPROVEN.  Its proof of (5.12)
   applies [1, Cor 7.2] -- standing hypothesis [P,Q] in K^x -- to the pair
   (psi phi P, psi phi Q), whose bracket is 1/2 + (lambda/2)x^{-1/2}, not in
   K^x, with lambda != 0 forced.  (5.12) is load-bearing: Thm 5.1's hypothesis
   (2) fails outright on Prop 4.1's polygons (st_{-1,1}(P) = (0,18), not
   (6,18)).  Of the 66 coefficient conditions (5.12) asserts, the proven claim
   delivers 15.  The rest of the chain -- Thm 5.1 itself, the unshown CAS
   elimination (5.9), Prop 4.1's table -- I re-checked and it stands; the
   failure is one sentence, gghv.txt:1430-1433.  Full write-up in CATCHES.md.
   CONSEQUENCE: the (9,27) branch is NOT closed by the literature, so the live
   region below max 125 is both orientations of (72,108), and the (9,27)
   systems (p108_*) go back on the compute queue as first-class targets.
3. Build the tail-closure test on the frontier (does the tail set saturate?),
   since that is what makes the above-125 territory finite.
