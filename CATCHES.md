# CATCHES — consolidated ledger of every error found, and the fix plan

Method note: the recurring failure classes are (i) runs believed launched but
never launched, (ii) runs killed silently, (iii) coverage believed complete
but incomplete, (iv) verdicts double-counted, (v) certifiers that cannot
fail, (vi) single-prime verdicts quoted as decided, (vii) convention and
orientation errors, (viii) literature steps assumed unverified, (ix) policy
without an enforcer.  Section 3 walks each class contrapositively ("if not
x, then y") against the current state.

## 1. Catch inventory (full session)

### Mine
| catch | class | status |
|---|---|---|
| Unsound gauge charts (claimed scaling symmetry killed by 2*mu3*q1''(0)) | iii/vii | FIXED: sound Z/N saturation split; d=7 re-decided on it |
| Concurrency OOM kills x2 (incl. original chart-N at 83min) | ix | ENFORCED tonight: tripwire_enforcer.sh live (was policy-only) |
| Vacuous-else bug in quick sieve | v | FIXED with planted control |
| Bridge dump timeout 120s (6x BRIDGE-ERROR) | — | queued one-liner (fold into queue runner) |
| p108_821326/843700 md5-identical, EMPTY double-counted | iv | FIXED: global dedup run tonight (Sec 2) |
| Enforcer v1 grabbed bash wrapper PID not msolve (3MB vs 7.4GB) | v | FIXED: /proc cmdline check; verified live on real PID |

### Opus's (adjudicated)
(13,4) sign error; Sec 6.7 lemma false as stated; (108,72) closure
OVERSTATED (underived beta=6); Second-Framework two unsound steps; 45+22
compile-time-constant "can't-fail" checks; msolve silent-lie modes
(constant generator, repeated monomials).  All recorded in ADJUDICATION.md;
none currently load-bearing for a live verdict.

### Literature
GGV mu0-typo (Sec 3.1 example needs mu0=2); GGHV Cor 5.7 never re-derived by
anyone (now under direct computational test); [5] assumes A'_t=(1,0)
unprinted.

### Write-out finds (prior rounds)
MISS-1 d7 confirm primes lost; MISS-2 d8-N never launched; MISS-3 d12-N-1/20
required and never run; MISS-4 case-2 Q-bar route never executed; MISS-5
legacy queue disposition; MISS-6 F3 single-prime; MISS-7 unpushed-commit
exposure; sliver = GGHV Prop 4.1 (9,27) polygons; d12 row0 rational
factorization; 444/464 coverage hole; pentagon 2-torus.

## 2. Tonight's lateral pass — new finds

1. **Tripwire had no enforcer** (class ix — the exact class that killed the
   original chart-N run).  Built and launched wave5/tripwire_enforcer.sh:
   swap-free < 8G -> SIGSTOP every non-twin msolve; > 12G -> SIGCONT; exits
   with the twin.  First version had a class-(v) bug (matched the bash
   wrapper, would have "protected" a 3MB process); fixed and verified
   against the real 7.4GB PID.
2. **msolve extension-field soundness test** (new negative-control class).
   Risk: if msolve mod p returned [-1] for 0-dim systems whose points live
   only in F_p^2, every irrational-solution EMPTY would be false.  Tested
   x^2 - 17 mod 65521 (17 a non-residue): msolve returns the full
   parametrization, NOT [-1]; genuinely inconsistent system returns [-1].
   **All mod-p EMPTY verdicts stand**; ext_nr.ms joins the control suite as
   the extension-field positive control the suite lacked.
3. **Global dedup-by-hash (49 TIMEOUT records = 16 unique systems).**
   The reduced system depends only on the chain TAIL: all four virgin cases
   sharing tail .../11/3,8 produce byte-identical 8-shape families;
   verdict transfer by hash identity is rigorous.  Consequences:
   - overnight TIMEOUT queue shrinks 49 -> 16 runs (~8h at 1800s);
   - running sliver shape 1 (p108_192622 = w6_35657_0 = orph_98503 ...)
     decides SIX records across three registers at once — the Cor 5.7 test
     now also covers virgin cases (9,36), (12,33), (12,36)x2;
   - w6_289012_0 == w6_384804_0 both decided EMPTY independently: a free
     replication control, passed;
   - the paused pair108 sweep was re-running its own 4-minutes-earlier
     TIMEOUT under a different tag (621292 == 671059) — pause loses nothing;
   - STRATEGY: hash the frontier/uncovered cases by tail-system BEFORE any
     compute; the 429-case compiler extension likely collapses similarly.
4. **Seed dichotomy is chart-independent and forced.**  Verified row0 is
   mu-free (the d=3..14 scale-comparison against a constant-coefficient
   quadratic would fail otherwise), and a_{2d}=0 gives row0=-3/8 != 0, so
   every solution in EITHER chart has a_{2d} in {-1/12, 1/20} at d=12.
   The two seeds partition each chart with no escape component.  Seeded-Z
   verdicts confirmed sound retroactively.
5. **Seed substitution validated transitively**: a24 fully eliminated from
   the seeded exports (absent from vars line); the d=3 seeded controls that
   exactly retrodict GGV's family went through the same code path.
6. **Sliver shape 1 resisted 1800s** (peak 6.0GB; earlier bridge msolve
   CRASHED at 43s = failure-not-verdict).  Next tier, in order: (a) run the
   pentagon grading-finder on the 16 unique systems — a torus slice may
   collapse them the way it explained the pentagon OOM; (b) 2x-4x budget
   overnight; (c) msolve -g 2 (GB-only, no parametrization) for pure
   emptiness detection.
7. **1/20-N export already on disk** (b16seed2_d12_N_p1000003.ms, never
   run) — MISS-3 is one command, first in queue after the twin verdict.

## 3. Contrapositive sweep of the failure classes (state: 22:00Z)

- (i) believed-launched: ps-verified twin, sliver-2, enforcer; pair108
  paused deliberately (SIGSTOP, self-expires ~22:20).  Nothing else claimed
  running.
- (ii) killed-silently: enforcer logs every 60s; task notifications armed on
  twin + sliver wrappers; dead-man check-in 22:46Z.
- (iii) coverage: chart split proved (Z union N exhaustive by construction);
  seed pair proved forced (Sec 2.4).  Remaining known holes are LISTED
  (STATE_FULL Sec A/C), not believed closed.
- (iv) double-count: global hash dedup done; registers now carry the
  16-unique map (this file + wave6/unique_timeout_map note).
- (v) can't-fail certifiers: new extension-field control added; enforcer
  PID bug caught by reading its own first log line — rule: every new
  watchdog must log a value that would differ if it watched the wrong thing.
- (vi) single-prime: d9-11 Z, F3 pair — queued confirms, still labelled.
- (vii) conventions: bracket sign on sliver verified (-x, gauge); twin char
  line replacement verified structurally (line 2, count=1).
- (viii) literature: GGHV Cor 5.7 under live test; GGHV Sec 5 re-derivation
  and GGV p.92 WLOG re-read remain OPEN (only cheap-read items left).
- (ix) policy-without-enforcer: tripwire now enforced; one-heavy rule still
  manual — the queue RUNNER (serial by construction) is the fix and is the
  first overnight build.

## 4. Fix plan (ordered)

1. Twin verdict (protected; enforcer live) -> per protocol; then 1/20-N
   (one command) and the twin's p=1000003 solo confirm.
2. Sliver shape 2 verdict (running) -> record across its 2 records.
3. Overnight serial queue on the 16 UNIQUE systems (not 49), plus d8-N,
   d9-11-N, d27 cells, d7 confirms, d12-unsat solo, F3 second prime,
   case-2 Q-bar ranks; runner enforces one-heavy by construction.
4. Grading-finder pass over the 16 unique systems (cheap linear algebra)
   before burning 1800s budgets — torus slices first.
5. Tail-hash the 429-case frontier before building the compiler extension.
6. Cheap reads: GGV p.92 WLOG argument; GGHV Sec 5 skeleton.
7. Morning: bridge timeout one-liner; register annotation with unique-map.

## RETRACTION (05:45Z) — the numerical "empty floor" evidence is VOID

Two planted-root controls, run tonight, kill it:

 * PENTAGON (165 unknowns): a root planted BY CONSTRUCTION (residual exactly
   0.0) was NOT found by random multi-start; best of 3 starts was 1.9e5.
 * LADDER d=8 (25 unknowns): same test, planted root at residual 0.0, 25
   starts, best 1.7e3, never found.  wave6/w6_plantctl.py, reproducible.

Therefore multi-start Newton cannot be relied on to locate an isolated root
at d >= 8, and the readings quoted earlier tonight --
   d=8  best 1.2e-10,  d=9  best 1.4e-10,  d=12 best 1.6e-10
-- measure the SOLVER, not emptiness.  They are hereby RETRACTED as evidence
of emptiness and must not be cited that way.  (The d=3 controls C1/C2 passed
honestly at 8 unknowns; the mistake was extrapolating that power to 25-40.)

Same reasoning voids the bifurcation-system residual (1.6e-3 at d=12) as
evidence: it is a numerical miss at 136 real unknowns, i.e. no information.

STATUS CHANGE: the numerical lanes are demoted from "evidence producers" to
"opportunistic finders" -- a HIT would still be real (and gets the full
verification protocol), a MISS says nothing at all.

WHAT SURVIVES intact (all exact, none numerical):
 * the exact rank criterion at quasi-homogeneous points, d=3..13, both roots
 * the factored form 6DE = 4AA' - mu2 q1^2 + 3mu1 y q1 - 6mu0 y^2 and its
   three exact checks (row-0 quadratic recovered, d=3 obstruction 6*mu0
   re-derived, D==0 branch killed by degree)
 * the excess count (4d+6 equations vs 3d-1 unknowns) and the rigidity argument
 * every exact msolve EMPTY verdict from the mod-p runs
The structural case that B=16 is closed rests entirely on these, and is
unaffected by the retraction.

## NEW msolve SILENT-LIE MODE (06:00Z) — parse error written as EMPTY

Discovered while hardening the seeded d=8 export.  If an input contains a
CONSTANT generator whose integer value is a nonzero multiple of the
characteristic, msolve refuses it:

    Error when parsing term 1000003 (coefficient cannot be 0 modulo 1000003).
    Error when reading file (exit but things need to be free-ed)

and then **exits 0 having written "[-1]:" to the -o file** -- i.e. a PARSE
FAILURE is indistinguishable from a genuine EMPTY verdict unless stderr is
read.  Minimal reproduction: /tmp/ctl_zero.ms (generators "x-1" and the
integer p).

Consequence caught in the act: my first seeded d=8 chart-N run "returned
EMPTY at both roots in 20 seconds" on a cell that had defeated 90 minutes
unseeded.  That was this artifact -- the seeded row-0 row becomes exactly
such a constant (the quadratic evaluated at its own root, an integer = 0
mod p).  RETRACTED; the export now reduces every coefficient mod p, drops
rows that vanish, and raises on a genuinely nonzero constant.  The honest
hardened run is grinding (minutes, not seconds), as a real computation
should.

CONTAMINATION AUDIT: all 131 .ms files ever produced by this campaign were
scanned for constant generators -- ZERO found.  Only tonight's two files
(since regenerated) were ever affected, so no previously recorded verdict is
touched.

STANDING RULE ADDED: every msolve invocation must capture stderr, and any
"[-1]" accompanied by a parse/read error is a FAILURE, never a verdict.

## d=8 chart N — resistance measured, not a verdict (08:00Z)

The smallest undecided ladder cell was attacked in every cheap formulation
available tonight.  ALL timed out with CLEAN stderr (genuine timeouts, not
the parse artefact):

  formulation                                   vars  budget  result
  seeded chart-N split (u*mu2-1), p=1000003      25    200s   TIMEOUT
  seeded chart-N split, GB-only (msolve -g 2)    25    420s   TIMEOUT
  seeded, NO chart split (mu0-saturation only)   24    200s   TIMEOUT
  seeded chart-N split, 16-bit prime p=65521     25    220s   TIMEOUT

Two structural improvements were found along the way and are kept:
 * seeding the row-0 root covers the WHOLE cell (the relation is mu-free), so
   the Z/N chart split is unnecessary work -- dropping it removes the u
   saturation variable (25 -> 24 unknowns);
 * a 16-bit prime buys nothing here, so the cost is Groebner structure, not
   coefficient arithmetic.

CONCLUSION (honest): exact elimination cannot decide d >= 8 chart N on this
hardware inside the container's uptime windows.  d=8..12 chart N therefore
remain UNDECIDED, and no numerical substitute is admissible (multi-start is
blind at these sizes -- see the retraction above).  The ladder's closure case
rests on the EXACT STRUCTURAL results (rank criterion d=3..13, the factored
form, the excess count), not on cell-by-cell elimination.

INFRASTRUCTURE NOTE: the container restarted 4x tonight, twice rolling the
working tree back to an older commit.  Recovery = git fetch + merge --ff-only
from origin (stale logs moved aside first).  Every result must be pushed
immediately; generated .ms files are regenerable from wave6/w6_seed_d8.py.
## PENTAGON TRUNCATION — the real mistake, found Saturday

The truncation ladder (trackB1_trunc10..19.json) is a CLOSED subsystem: every
full solution restricts to a truncation solution, so an EMPTY truncation kills
pentagon case (1) of (72,108) outright.  It was built, run once at W=19, died
"no more memory", and was abandoned.  Today's diagnosis of why that was never
going to work:

    W    eqs  vars  excess
    10   184  157   +27
    11   169  151   +18
    12   153  143   +10
    13   136  133    +3
    14   118  120    -2
    ...
    19    20   26    -6      <== the level everyone kept running

**W=19 is UNDERDETERMINED by 6.**  Its variety is positive-dimensional, so it
is almost certainly NON-empty, and every attempt to prove it empty -- the
original Singular run, and three of mine today -- was aimed at a level that
cannot deliver the result by construction.  Worse, msolve's default mode
computes a rational parametrisation, which needs dimension 0; that is why it
OOM'd rather than merely running long.

CORRECT TARGET: W <= 13, where the system is overdetermined and CAN be empty.
An overdetermined ideal that is empty collapses to {1} at low degree, so GB-only
(msolve -g 2) is the right mode and the size is not the binding constraint.

Two sound reductions established today:
 * TORUS GAUGE.  The truncated system carries a torus of rank 2 (exact
   nullspace of the exponent-difference matrix).  s_4_8 carries weight -1 and
   is FORCED NONZERO by the system's own Rabinowitsch equation w1*s_4_8 = 1,
   so every orbit meets {s_4_8 = 1}: gauge-fixing it loses NO branch, and it
   collapses w1 as well.  (This is the gauge done right -- contrast the unsound
   scaling gauge caught earlier in the campaign.)
 * SUB-IDEAL PRINCIPLE.  Any sub-ideal that is empty proves the whole ideal
   empty.  Searched for a small overdetermined closed block (a variable set
   whose fully-contained equations outnumber it): NONE exists below the whole
   system -- the coupling is global.  Worth knowing; it closes off that shortcut.

STATUS: W=13 gauged (137 eqs, 132 vars, +5) and W=12 gauged (154 eqs, 142
vars, +12) built and clean (no constant generators).  Neither finishes GB-only
inside this container's ~8 min usable window.  This is now a well-posed,
sound, correctly-levelled target that needs uninterrupted compute -- not a
research question.

## THE DEGREE-BOUNDED TEST — the method that finally fits the hardware

Every previous attempt asked the solver for a whole Groebner basis: unbounded
work, which is why the pentagon systems OOM'd or timed out for two weeks.  But
emptiness only needs ONE question: is the constant 1 in the ideal?  Fixing a
degree bound D makes that a BOUNDED computation whose cost I choose.

  SOUND one way (the way we want): 1 found at degree <= D  =>  ideal is the
  whole ring  =>  truncation EMPTY  =>  pentagon case (1) DEAD.
  Not found  =>  inconclusive, raise D.  Never a false kill.

Implemented with Singular's `degBound` (/tmp/degbound.sh).  THREE controls:
 * an inconsistent system reports ONE-IN-IDEAL;
 * a consistent one does not;
 * the bound must actually BITE -- the 132-variable W=13 system, which eats
   8 minutes unbounded, returns in 0.23 s at D=2.
The first version silently failed this third control: `option(degBound,D)` is
not Singular syntax and errored, so the runs were unbounded and only "passed"
because the first two controls are trivial.  Correct form is the reserved
variable `degBound = D;`.

MEASURED COST LADDER (gauged truncations, p=65521):

  level   excess   D=4              D=5
  W=10    +29      36 s / 306 MB    > 260 s / 868 MB
  W=11    +20      12 s / 148 MB    > 260 s
  W=12    +12      -                running
  W=13     +5      1.7 s / 44 MB    231 s / 648 MB  (COMPLETED, no constant)

No constant through D=5 at W=13, or D=4 at W=10/11.

THE IMPORTANT SHIFT: peak memory is UNDER 1 GB everywhere.  The pentagon
computation is no longer memory-bound -- it is time-bound.  That means it no
longer OOMs, it parallelises (4 cores, ~1 GB each), and it survives inside this
container's limits.  A two-week memory wall became a schedulable time cost.

## FOUND IN PLAIN SIGHT — the eliminator was aimed at the wrong levels too

campaign/audit_tracks/trackA_eliminator.py is a branch-and-reduce engine with
a documented soundness contract ("R1 or-branching over every variable of the
monomial; R2 pivots only unit*nonzero-monomial with divisibility checked at
selection; every closed branch certified") and SEVEN selftests, all of which
pass today.  It shrinks these systems hard and fast:

    W=17: 60 eqs / 69 vars  ->  44 / 54   (15 pivots, seconds)
    W=18: 40 / 48           ->  27 / 36   (12 pivots)
    W=19: 20 / 26           ->  11 / 18   ( 8 pivots)

It had been run on W=17, 18, 19 ONLY -- exactly the underdetermined levels
that cannot be empty.  The same targeting error as the truncation itself, one
layer down: a working tool pointed where its output could never decide
anything.  Its reduced leaves are all still underdetermined, which is why they
sat unused with "contra: 0, open_leaves: 1" and were never followed up.

FIRST RUN ON THE OVERDETERMINED LEVELS (W=10..13) is now under way.  Over Q it
swells badly (27 MB and 60 MB of partial output before the budget cut it), so
it is running with --mod 65521, which is what that flag exists for.

Also measured today: peak memory for the degree-bounded Singular runs is under
1 GB at every level, so this whole branch is time-bound rather than memory-
bound and can be parallelised -- four cores, roughly 1 GB each.  Job mix is
managed by hand for now (eliminators preferred over degBound runs when memory
tightens), and wave6/pentagon_watch.log records contradictions and completions.

WHY IT MATTERS: a CONTRADICTION at any W <= 13 means that truncation is empty,
and by the closed-subsystem property that KILLS pentagon case (1) of (72,108)
-- the branch no method has ever decided.

## THE ELIMINATOR'S REDUCTION IS A TRAP (measured, Saturday)

Running trackA_eliminator.py on the overdetermined truncations DOES shrink
them, and all three that completed stayed overdetermined:

    W=13: 136 eq /133 var  ->  95 / 92   (excess +3)
    W=12: 153 /143         -> 111 /101   (excess +10)
    W=11: 169 /151         -> 126 /108   (excess +18)
    W=10: crashed mid-write when the disk allowance ran out

No contradiction was found (0 closed branches).  But the reduction is NOT a
win for emptiness testing, because it trades variables for DEGREE:

    W=13 gauged, pre-elimination : 137 eqs, 132 vars, MAX DEGREE  4
    W=13 after elimination       :  97 eqs,  94 vars, MAX DEGREE 23

Its pivots substitute variables, and the substituted expressions compound.
Degree is the dominant cost for Groebner and for the degree-bounded test, so
a 30% cut in variables at the price of degree 4 -> 23 is a large net loss.  It
also explains the 90-150 MB output trees (degree-23 polynomials in 94
variables) and hence the exhausted disk allowance.

CONSEQUENCE, and a near-miss worth recording: the degree-bounded runs on the
reduced systems reported "no constant at degBound 4/5" -- which is VACUOUS,
because the bound sat far below the inputs' own degrees, so no reduction ever
happened.  The tell was gbsize being exactly equal to the number of input
equations (97 in, 97 out; 113 in, 113 out).  Read carelessly, that line looks
like evidence of non-emptiness.  It is evidence of nothing.

STANDING RULE ADDED: a degree-bounded result is only meaningful when D exceeds
the maximum degree of the input generators; always report both, and treat
gbsize == number-of-inputs as a no-op sentinel.

CORRECT TARGET remains the GAUGED, PRE-ELIMINATION truncations at W <= 13
(degree 4, ~130 vars), where the measured ladder is D=4 cheap (1.7-36 s),
D=5 a few minutes, D=6 the frontier -- all under 1 GB.

## P0 IS FUTILE — the repo already contained the disproof (verified Saturday)

trackB1_pentagon.py:432 `witness()` constructs an exact rational point
(P = S~^2, Q = S~^3 with S~ = y^4(1+(xy)^4) + x^4y^7).  I evaluated it myself,
from the raw JSON, against every truncation on disk:

    file                    eqs   failures   side conditions hold?
    trunc10                 184      0       NO  (c_1_0 = 0 required nonzero)
    trunc11                 169      0       NO  (same)
    trunc12 ... trunc19  153..20     0       YES
    full param system       283      7       NO

**Every truncation from W=12 to W=19 is CERTIFIABLY NON-EMPTY.**  They each
have an explicit solution over Q satisfying all their equations and all their
declared side conditions.  No emptiness search at W >= 12 can ever succeed,
because those systems are not empty.  W=10/11 fail only the side condition
c_1_0 != 0, so they are not certified alive -- but nor are they killed.

CONSEQUENCE: the entire P0 plan (run the truncation ladder to find an empty
level and thereby kill pentagon case (1)) is FUTILE and is hereby WITHDRAWN.
Today's work -- the gauge, the degree-bounded test, the eliminator runs, the
excess table -- was all aimed at proving empty something that has a solution.

WHY IT SURVIVED SO LONG: the docstring of witness() states this outright, and
the truncation's own meta says "converse false (truncation only necessary)".
Nobody read either -- including me, four hours after calling P0 "the decisive
shot".  The failure class is (viii) literature/artifact assumed unread, and it
is the third instance today of the same pattern: a correct, tested artifact
sitting unexamined while effort went to the thing it had already settled.

WHAT IT LEAVES STANDING (this is the real content):
Any death of case (1) MUST engage the equations of weight <= 7 -- the
bottom-vertex datum c_1_0 * d_2_1 = 1 -- which every truncation discards.  The
witness satisfies the whole top of the tower and fails exactly there.  So the
target is not "find an empty truncation" but "show the bottom-vertex datum is
incompatible with the top structure".  That is a sharply posed question and it
is where case (1) effort belongs.

ONE OVERSTATEMENT CORRECTED: witness()'s docstring claims every normalized
truncation W >= 8 is alive "side conditions incl."  At W = 10, 11 the
truncation still declares c_1_0 != 0 while the witness has c_1_0 = 0, so
certified aliveness begins at W >= 12, not W >= 8.  The same wording is
inherited by trackB1_witness.json's "consequence" field.

SOUNDNESS NOTE (audited separately, and it holds): empty truncation => case (1)
empty is valid, and for a more basic reason than the weight argument -- the
declared variable list is defined as the union of variables occurring in the
kept equations, so a full solution's restriction satisfies them for ANY subset
of equations.  The weight bookkeeping (beta-alpha additive; c-lines >= w-12,
d-lines >= w-8, s-weight 4) was verified exactly against the data with zero
violations, and dropping side conditions errs in the safe direction.

## MODULAR ELIMINATION IS UNSOUND FOR CONTRADICTIONS (verified Saturday)

trackA_eliminator.py --mod p can CLOSE a branch that has a genuine rational
solution.  Minimal counterexample, constructed and run today:

    nonzero = [y, z]
    x - 3y = 0 ,  x + 4y - z = 0        solution over Q: x=3, y=1, z=7

    exact Q : 1 open leaf                      (correct -- a solution exists)
    --mod 7 : "1 closed, 0 open leaves"        FALSE CONTRADICTION
    --verify: "1/1 closed-branch certificates replayed OK", exit 0

Mechanism: z = 7y is nonzero over Q but vanishes mod 7, so a declared-nonzero
coordinate dies under reduction and a satisfiable branch is closed.  Generally
a mod-p contradiction only excludes solutions that are p-integral AND whose
declared-nonzero coordinates survive reduction -- neither is implied by the
rational problem.  (p*x - 1 = 0 is the minimal illustration.)

The generating run does print "(SCOUTING ONLY)", so the author knew.  But that
warning is NOT in the output JSON, NOT in --verify, and NOT in the exit code,
so it does not survive into the artifact anyone would later read.

DIRECT RELEVANCE: I ran all four W=10..13 eliminators with --mod 65521 this
afternoon.  They returned contra = 0, so no false result entered the record --
but the guardrail would not have caught one.  Any contradiction claim from this
tool must come from an EXACT run (meta.mod == null) and be cross-checked with
an independent engine.

Related weaknesses in the same tool, worth knowing before relying on it:
 * A CAPPED run (max_nodes / max_seconds hit) reports "0 open leaves" and exits
   0, indistinguishable from a completed proof except for the `capped` counter;
   the checkpoint file writes done: True unconditionally.
 * --verify skips branched/merged/capped nodes entirely, does not check that a
   branch's children cover all cases, and reads the nonzero hypotheses from the
   TREE's own meta rather than the system file -- so the artifact asserts its
   own hypotheses.  It is a replay sharing the engine's arithmetic, not an
   independent check.
 * load_system stores zero coefficients and silently overwrites repeated
   monomials; either can manufacture a false contradiction.  Current inputs are
   clean (checked: 0 zero-coeff terms, 0 duplicate monomials), so this is
   latent rather than live.
 * The 7 selftests never test a negative control (a system WITH a solution must
   stay open), never touch --mod, the caps, --normalize, or the loader.

The exact-Q reduction logic itself was reviewed closure-site by closure-site
and fuzzed on ~1900 systems with planted solutions: ZERO false closures.  The
engine is sound over Q; it is the reporting and verification layer that is not.

## FIRST DIRECT ATTACK ON THE BOTTOM-VERTEX PROBLEM (Saturday, exact over Q)

Method (deliberately NOT elimination -- elimination clogs; this is pure rank):
we possess one EXACT point, the witness, which satisfies the whole top of the
tower and fails only the 7 low-weight equations with c_1_0 = 0.  So instead of
solving the system, ask a LINEAR question at that point: can the witness be
deformed to kill those 7 residuals and switch c_1_0 on?

Computation, exactly over Q, no Groebner basis anywhere:
    system            283 equations, 165 variables
    residual F(w)     7 nonzero, at weights -2, 5, 6, 7
    rank J(w)         163  (of 165)
    J v = -F(w)       INFEASIBLE -- 2 inconsistent rows

RESULT: **the witness admits NO first-order correction at all.**  It is not an
infinitesimal limit of solutions.

Two obstruction certificates extracted and INDEPENDENTLY VERIFIED (each is a
vector lambda with lambda^T J(w) = 0 but <lambda, F(w)> != 0):

  1. lambda supported on the SINGLE equation at bracket point (1,8), weight 7:
       value at witness    F = -16   (nonzero)
       gradient at witness ALL 165 partials ZERO
     i.e. the witness is a CRITICAL POINT of that equation with nonzero value.
     A rank-one, fully explicit obstruction: no perturbation moves F toward 0
     at first order because the differential is identically zero there.

  2. lambda supported on 4 equations, bracket points (1,9), (1,10), (5,12),
     (9,16), with <lambda, F(w)> = 24.

WHAT THIS DOES AND DOES NOT ESTABLISH.  It does NOT prove case (1) is empty: a
solution could exist far from the witness, and this is a local statement at one
point.  What it does establish is that the obvious bridge -- deform the known
top-of-tower solution until the bottom vertex switches on -- is CLOSED, and
closed for a concrete reason that can be written down and checked by hand.
It also gives the first quantitative handle on the bottom-vertex problem, and
the (1,8) equation is now a named, specific object to attack.

NEXT (each cheap and grounded by this): second-order / Lyapunov-Schmidt at the
witness restricted to ker J(w) (dim 2 in the domain, cokernel 120); ask whether
the (1,8) critical point is isolated or sits in a positive-dimensional critical
locus; and run the same rank test at OTHER exact points of the top variety if
more can be constructed (the witness has a parameter t).
