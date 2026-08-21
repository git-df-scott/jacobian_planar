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

================================================================================
GGHV COROLLARY 5.7 IS UNPROVEN -- THE (9,27) BRANCH OF (72,108) IS NOT CLOSED BY
THE LITERATURE.  (Verified by me, line by line, against the local extractions of
arXiv:2204.14178 (GGHV) and arXiv:1401.1784 (= their reference [1], GGV, J.
Algebra 471 (2017) 13-74).  arXiv has only v1 of 2204.14178, no journal ref, so
there is no corrected version.)
================================================================================

WHY THIS MATTERS.  (72,108) is the last surviving degree pair below max 125.  It
has two orientations.  The (9,27) orientation is killed in the literature by
exactly ONE result: GGHV Corollary 5.7.  Our ledger has flagged it for weeks as
the single load-bearing unverified step.  It is now verified to be BROKEN at a
specific, quotable step.  Everything downstream of it -- and every triage
decision that treated (9,27) as dead -- must be reopened.

THE STATEMENT (gghv.txt:1412-1416, p. 20):
  "Corollary 5.7.  There exist no P, Q in K[x,y] with [P,Q] = x and
     N(P) = {(0,0),(1,1),(6,16),(6,18),(0,18)}
     N(Q) = {(0,0),(1,0),(9,24),(9,27),(0,27)}"
These are exactly the polygons Prop 4.1 (gghv.txt:329) produces from a (9,27)
counterexample, so Cor 5.7 is the whole kill.

THE PROOF'S SKELETON.
  (a) CLAIM: l_{0,1}(P) = lambda_p * y^18 * (x - lambda)^6, lambda in K^x.
  (b) Take phi in Aut(K[x,y]) with phi(y)=y, phi(x)=x+lambda.
  (c) (5.12): Succ_{phi(P)}(1,0) >= (-1,1) and Succ_{phi(Q)}(1,0) >= (-1,1).
  (d) [phi(P),phi(Q)] = x+lambda, so (phi P, phi Q) satisfies Theorem 5.1 -->
      contradiction.
Step (c) is proved by ONE sentence: "By the same argument, for (rho,sigma) =
Succ_{psi(phi(P))}(0,1) we also have that l_{rho,sigma}(psi(phi(P))) is a sixth
power ...", where psi(x) = x^{1/2}, psi(y) = y.

(5.12) IS LOAD-BEARING, NOT DECORATIVE -- I checked this first, because if
Theorem 5.1 applied directly to Prop 4.1's polygons the gap would be harmless.
It does not.  Theorem 5.1 hypothesis (2) demands st_{-1,1}(P) = (6,18).  On
N(P) the form v_{-1,1} = b-a takes the values 0, 0, 10, 12, 18, MAXIMAL AT
(0,18); so st_{-1,1}(P) = (0,18) != (6,18) and hypothesis (2) FAILS.  Same for
Q: values -1, 0, 15, 18, 27, maximal at (0,27), not (9,27).  Theorem 5.1 is
reachable ONLY through (5.12).  (Recomputed; see the arithmetic below.)

THE DEFECT.  "The same argument" is [1, Corollary 7.2] (1401.1784.txt:3382),
whose standing hypothesis, printed on its own line, is

        [P, Q] in K^x

-- and equally [1, Definition 4.3] (1401.1784.txt:1225), which defines an
(m,n)-pair, opens with the same requirement.  Both routes need it.  Now apply
the paper's own chain rule, [1, Proposition 3.10] (1401.1784.txt:1152):
[phi(P),phi(Q)] = phi([P,Q])[phi(x),phi(y)].  With [psi(x),psi(y)] =
(1/2) x^{-1/2}:

  FIRST application, to (psi P, psi Q):
      [psi P, psi Q] = psi(x) * (1/2) x^{-1/2} = 1/2         in K^x.   VALID.
  SECOND application, to (psi phi P, psi phi Q):
      [psi phi P, psi phi Q] = psi(x + lambda) * (1/2) x^{-1/2}
                             = 1/2 + (lambda/2) x^{-1/2}     NOT in K^x.
(Both brackets recomputed symbolically; the second is exactly the first plus a
term of v_{-1,1}-degree +1/2, i.e. nonzero in precisely the directions Cor 7.2
is being invoked for.)

lambda != 0 IS FORCED, so the failure is never vacuous.  The paper itself
writes lambda in K^x in the claim; independently, l_{0,1}(P) = y^18 u(x) with
deg u = 6 and u(0) != 0 because (0,18) is a vertex of N(P), and u =
lambda_p (x-lambda)^6 gives u(0) = lambda_p lambda^6 != 0.

THE OBSTRUCTION IS STRUCTURAL, NOT A TYPO.  The x^{1/2} trick works only because
[P,Q] is the VARIABLE x itself.  A morphism xi with xi(y)=y, xi(x)=h(x) keeps
the bracket constant iff h h' = c, i.e. h = (alpha x + beta)^{1/2}, which lies
in L^(2) only for beta = 0; and the substitution that would fix the translated
pair, x -> x^{1/2} - lambda, composes with phi back to psi -- it undoes the
translation and returns the ORIGINAL polygon.  No repair by the same device.

HOW BIG IS THE HOLE, QUANTITATIVELY.  (5.12) asserts v_{-1,1}(phi P) = 12 and
v_{-1,1}(phi Q) = 18, i.e. the vanishing of every coefficient of x^a y^b with
b - a > 12 (resp. > 18) inside the support rectangles [0,6]x[0,18] and
[0,9]x[0,27]: 21 conditions on P and 45 on Q, 66 in all.  The proven part --
the claim, plus its Q-analogue -- delivers only the TOP ROWS: b=18, a=0..5 (6
conditions) and b=27, a=0..8 (9 conditions).  So 51 of the 66 conditions rest
on the invalid step.  (This corrects the "one condition" figure an assisting
agent reported; the correct count is 15 delivered, 51 unsupported.  The
conclusion is unchanged.)

WHAT IS *NOT* WRONG.  I checked the rest of the chain and it stands: Theorem
5.1's own proof (Props 5.2-5.6, the 9 explicit equations, the unshown CAS
elimination (5.9) = 8T^3 + 18 e1 m1^6 T + 27 e0 m1^9, the y-exponent 507 in
(5.11), and both endgame branches k>=8 and k<=7); Prop 4.1's divisibility
table; and the FIRST half of Cor 5.7 (the claim), which is genuinely valid
because there the bracket really is 1/2 in K^x.  The failure is localised to
one sentence: gghv.txt:1430-1433.

LEDGER CHANGE, EFFECTIVE NOW.
  (9,27) is NOT killed.  Its sole citation has an INVALID STEP, not merely an
  unverified one.  The live region below max 125 is therefore BOTH orientations
  of (72,108), not one.  Any p108 run, any triage table, and any statement of
  the form "only (108,72) survives" must be corrected.  This is failure class
  (i) inherited-assumption: we imported a published kill without checking it,
  and it does not hold.

================================================================================
GGV (1.2) ROW 3 IS MIS-PRINTED IN THE PAPER, AND THE CAMPAIGN COPIED IT.  EVERY
B=16 EMPTINESS VERDICT EVER PRODUCED HERE WAS A VERDICT ABOUT THE WRONG VARIETY.
================================================================================

This is the worst error the campaign has made.  It is not a bug in our code; it
is a typo in the source, transcribed faithfully, that silently shrank the search
space by a codimension-1 condition for two months.

WHAT THE PAPER PRINTS.  GGV, Pro Mathematica 27 (2013) 83-98, Theorem 1.2 (p.85)
and again as (3.6) (p.93):

    A(0) = -mu3^2/4,   A'(0) = mu2,   mu3*A''(0) = -6*mu1 - 2*mu3*q1''(0)

I read this off the page renders myself (ggv_p3-03.png p.85, ggv_p-11.png p.93).
The transcription in wave5/w5_b16_abel.py was CORRECT: the paper really does
print the -2*mu3*q1''(0) term.  The paper is wrong.

WHAT IT SHOULD BE.  GGV justify the last two conditions in one sentence: they
"follow from the requirement that q0'(y) and p0'(y) defined by (3.2) and (3.3)
are polynomials".  I carried out exactly that derivation, from their own setup
(p.91-93), and it gives

    mu3*A''(0) = -6*mu1        -- NO q1''(0) term.

The derivation is committed and self-checking: wave6/w6_ggv12_rederivation.py.
It starts from the Poisson bracket, not from any transcription:
  * P = x^3 y + x^2 p2 + x p1 + p0,  Q = x^2 y + x q1 + q0, and the five
    coefficients of [P,Q] in x are computed directly and checked AGAINST the
    four ODEs printed on p.91 -- all five match, so the setup is theirs;
  * q1 = mu3 + y^2 F', p2 = mu3 + yF + (3/2)y^2 F' (their general solution of
    the first ODE, p.92) is confirmed to satisfy that ODE identically;
  * (3.2)'s numerator vanishing at y=0 gives p1(0) = mu2, i.e. A'(0) = mu2;
  * (3.3)'s numerator vanishing at y=0 gives mu1 = -mu3*(p1'(0) - 2mu3 F'(0))/3;
  * A := y p1 - q1 p2 + (3/4) q1^2 (their p.93) has A(0) = -mu3^2/4 (matches),
    A'(0) = mu2 (matches), and
        mu3*A''(0) = 2*mu3*(p1'(0) - 2*mu3*F'(0)) = -6*mu1  exactly.
  * printed minus truth = -4*F'(0)*mu3 = -2*mu3*q1''(0), the spurious term.

THE DAMAGE, EXACTLY.  q1''(0) = 2*b2 (b2 = the y^2 coefficient of q1).  Combine
the printed row 3 with the y^2 coefficient row of (1.3), after the paper's own
normalizations (b0 = mu3, b1 = 0, a0 = -mu3^2/4, a1 = mu2):

    y^2 row of (1.3)  =  -mu3*(a2*mu3 + 3*mu1)
    printed row 3     =  2*(a2*mu3 + 2*b2*mu3 + 3*mu1)
    mu3*(row 3) + 2*(y^2 row)  =  4*mu3^2*b2

verified identical for d = 3, 4, 5, 6, 7.  So 4*mu3^2*b2 lies in the campaign's
ideal for EVERY d, i.e.

    V_campaign  =  V_true  n  ( {mu3 = 0}  u  {q1''(0) = 0} ).

That is a proper closed subvariety.  EMPTINESS OF IT IMPLIES NOTHING ABOUT B=16.
Under the corrected row 3 the same combination is 0 -- the corrected row is
implied by (1.3) on the chart mu3 != 0, which is what a correctly derived
condition should be.  That is the discriminator, and it can fail: it is printed
by w6_ggv12_rederivation.py for both variants side by side.

WHY NO CONTROL CAUGHT IT.  w5_b16_abel.py has 6 controls and all 6 pass on the
WRONG system -- because both of GGV's own worked examples (Sec 3.1 and Sec 3.5)
have q1''(0) = 0.  The file even says so in a comment ("both published controls
had b2 = 0 and never exercised that term") and the campaign read that as a note
rather than as an alarm.  This is failure class (v), can't-fail certifier: a
control suite that is structurally incapable of detecting the error it is
supposed to guard, plus failure class (i), inherited assumption.

SECOND-ORDER DAMAGE.  The campaign killed its own torus gauge charts on the
grounds that "the term 2*mu3*q1''(0) in (1.2) row 3 breaks every continuous
torus" (ADJUDICATION section 6, w5_b16_reduce.py:40-44).  That reason is void.
Any gauge decision resting on it must be redone.

WHAT IS VOID.  Every B=16 EMPTY row in STATE_FULL.md section A and the
ADJUDICATION section 2 headline ("the B=16 corridor is now closed further than
any published source") -- all d, both charts, both seeds, all primes.  Not
"unconfirmed": VOID, as statements about B=16.  They remain true statements
about V_campaign, which is not an object anyone cares about.

WHAT I RE-RAN TODAY ON THE CORRECTED SYSTEM (msolve, mu0 saturated, stderr read
and empty, zero constant generators audited, positive control passing):

    d = 2   EMPTY   char 0   0.00 s      d = 4   EMPTY   char 0   0.10 s
    d = 3   EMPTY   char 0   0.01 s      d = 5   EMPTY   char 0   4.42 s
    (mod p = 1000003 agrees at every d; d = 6,7,8 launched.)

POSITIVE CONTROL (mandatory, because these are all [-1] verdicts): the SAME
corrected system with the mu0 saturation REMOVED returns [1, 14, -1, []] at
d = 3 (positive-dimensional -- GGV's published mu0 = 0 family) and an explicit
solution list at d = 4.  So the pipeline can say "non-empty"; the [-1]s are real.

NET EFFECT ON THE CAMPAIGN.  d = 2..5 are re-decided EMPTY in characteristic 0
on the correct system, so GGV's published d = 2,3,4 conclusions survive the typo
and d = 5 -- which GGV explicitly could not solve ("after an hour the PC hadn't
solved it") -- is decided here for the first time, correctly, in 4.4 seconds.
Everything above d = 5 reverts to UNDECIDED and must be re-run from scratch.

CODE FIXED: wave5/w5_b16_abel.py (build_system now takes variant='corrected'
(default) or 'printed' to reproduce the old wrong system); the substitution
mu1 = -mu3*(a2 + 2*b2)/3, which is the erroneous row solved for mu1, corrected
to mu1 = -mu3*a2/3 in w6_seed_d8.py, w6_rankcrit_modp.py, w6_numhunt.py,
w6_plantctl.py, w6_bifsystem.py, w6_mu0walk.py, w6_cascade_fp.py.

STANDING RULE ADDED.  A transcribed equation is not verified by reproducing the
source's own examples.  It is verified by re-deriving it from the source's own
prior equations, or by an example that exercises every term.  Before trusting
any transcription, list its terms and name, for each one, the control that would
die if that term were deleted.  If a term has no such control, it is unverified
no matter how many controls pass.

================================================================================
THE (9,27) SYSTEM IS A CASCADE, NOT A GROEBNER PROBLEM.  A branch-and-factor
walk descends five blocks in two minutes on a system exact elimination could not
touch in 1800 seconds.
================================================================================

Motivated by the Cor 5.7 finding above -- the (9,27) orientation of (72,108) is
live again -- I looked at the smallest system on that branch,
wave6/p108_525122_q.gens (140 conditions, c2..c25 plus w = 1/c2 and u), which
had timed out repeatedly.  It is not a generic system.  Its conditions partition
by variable support into blocks

  {c3,c4}:22   {c3..c7}:20   {c3..c10}:18   {c3..c13}:16   {c3..c16}:14
  {c3..c19}:12  {c3..c22}:10  {c3..c25}:22  + 2 sparse rows + 2 saturations

and the block structure is severe.  VERIFIED, not assumed: every one of the 22
generators of the first block is divisible by c4*L with
L = 6439534922*c3^2*w + 131043*c4, and gen[0] = 52417*c4*w^3*L exactly.  Since
V(f) = V(G) u V(f/G) and one generator IS the gcd,

    V(block 1)  =  V(c4)  u  V(L)

exactly -- 22 equations collapse to ONE binary branch.  The same happens at
every block: the gcd is attained by some generator, and the block reduces to a
single equation whose irreducible factors are the branches.  On the branch
c4 = 0, block 2's 20 generators all become const*c3^k*w^m*(3434414257*c3*c6*w -
124490*c7); on the branch L = 0 they all become const*c3^k*w^m*(a quadratic in
c5,c6,c7).  Each block is one equation wearing twenty disguises.

That is why msolve and Singular choke: the coefficients are 20-40 digits and
there are 26 variables, but the solution set is a shallow tree, and a Groebner
engine has no way to see that before it has already blown up.

wave6/w6_p108_cascade.py walks the tree exactly over Q.  It is falsifiable at
every node: it CHECKS that some generator equals the gcd, and when that fails it
records the residual piece V(h_1..h_n) as an explicit OPEN leaf rather than
dropping it.  Forced-nonzero variables (c2, c23, c25 from the two saturation
rows, and w) are never used as branches.

FIRST RUN: 8 leaves in 122 s, reaching block 5 of 8 with explicit rational
substitutions for c4, c7, c9, c8 in terms of c3, c5, c6, c10.... One leaf is
already a clean nonlinear condition in two unknowns,

    1516347*c10^2 - 16559562258*c10*c6^2*w + 6509724012810760*c6^4*w^2 = 0
    (on the branch c4 = c3 = c7 = 0),

which is a quadratic in c10 -- solvable in closed form.  NO VERDICT YET: the
walk has not reached the last three blocks, and the residual pieces are open.
Recorded now because the structural fact -- these systems are cascades, and the
campaign spent weeks handing them to the wrong kind of solver -- applies to
every p108 system and probably to the frontier shapes that share this shape.

================================================================================
A NEW DOOR: THE PLANE TANGENT SWEEP.  The July 2026 refutation of JC in
dimension 3 hands us a mechanism for non-injective etale maps, and nobody has
asked why it fails in the plane -- including the papers that announce it.
================================================================================

THE NEWS (verified from papers/2608.00222.pdf, which was in this repo unread).
JC was refuted in dimension 3 by Alpoge on 2026-07-19; Gallagher gave an
infinite family (07-20) of every geometric degree d >= 3; Speyer named the
mechanism the TANGENT SWEEP (07-23); Gao generalized it to every n > 2
(arXiv:2608.00222, 07-31).  A polynomial map C^n -> C^n, etale everywhere,
non-injective, det J constant.  The plane case n = 2 explicitly REMAINS OPEN and
is stated to be untouched by these constructions.  Two corollaries for us:
  * "JC2 might just be true" is now a weaker prior than it was in June;
  * degree-bound approaches to JC are dead in n >= 3 (Gallagher's family
    realizes every degree), which is worth knowing before we invest more in the
    max-125 frontier as a route to a THEOREM.

THE MECHANISM, AND WHY IT IS OUR BUSINESS.  The tangent sweep is a PLANE map:

    S(gamma, w) = ( p(w) + 2*gamma ,  q(w) + gamma*w ),    q'(w) = (w/2) p'(w)
    det J(S) = 2*gamma                                     (Gao, section 3.1)

It is generically (deg p + 1)-to-one -- the count is the class of the swept
curve, by projective duality -- and unramified away from gamma = 0.  Its ONLY
defect as a counterexample is that its Jacobian is the COORDINATE 2*gamma rather
than a constant.  Everything dimension 3 buys is spent cancelling that gamma:
pad with a variable x, set C = gamma*x, divide the components by C and C^2, and
arrange the divisibilities by "side conditions".  Reproduced here: our
implementation returns q = -w^3 + w^2 from p = -3w^2 + 4w, which is exactly
Alpoge's counterexample as printed in Gao section 3.4, and det J(S) = 2*gamma for
every p tested.

GAO GIVES NO REASON THE PLANE FAILS.  The only justification offered anywhere
for "dimension >= 3" is Wang's degree-2 theorem plus "the known constructions
produce degree >= 3" (2608.00222, p.2, lines 125-127).  The architecture of his
section 4.1 does degenerate at n = 2 -- the swept hypersurface would have
dimension n-2 = 0 -- but that is a statement about ONE construction, not about
the plane.

WHAT I PROVED TODAY (short, and it sharpens the question).  No POLYNOMIAL
conjugation can repair the plane sweep.  If phi, psi : C^2 -> C^2 are polynomial
and F = psi . S . phi, then

    det J(F) = detJpsi(S(phi)) * 2*gamma(phi) * det J(phi),

a product of three polynomials.  In the domain C[x,y] a product is a nonzero
constant only if every factor is; so gamma . phi is constant, phi maps into a
line, F is not dominant, and Keller maps are dominant.  Hence ANY plane
counterexample of tangent-sweep type must use a DIVISION twist with divisibility
side conditions -- precisely the dimension-3 device, one variable short.

THE PLANE SIDE CONDITION (the object nobody has written down).  For
F = (P/C^i, Q/C^j) direct differentiation gives the exact identity

    det J(F) = C^{-i-j-1} * [ C*{P,Q} - j*Q*{P,C} + i*P*{Q,C} ]

({A,B} = A_x B_y - A_y B_x), verified against random data as a can-fail control
(w6_plane_sweep.verify_identity).  With (P,Q) = S . phi the chain rule gives
{P,Q} = 2*gamma(phi)*det J(phi), so F is Keller with det J(F) = kappa exactly when

    C*2*gamma*detJphi  -  j*Q*{P,C}  +  i*P*{Q,C}  =  kappa*C^(i+j+1)

holds identically, together with C^i | P and C^j | Q.  That is the two-variable
analogue of Gao section 3.3 / Speyer's side conditions.  Its coefficients in
(x,y) are a polynomial system in the shape parameters, solvable exactly.

STATUS: wave6/w6_plane_sweep.py (derivation + controls) and
wave6/w6_plane_sweep_search.py (exact Groebner sweep over shapes
gamma = c0 + a x^al y^be, w = gamma(1 + b x^mu y^nu), C = gamma x^s, twists
(i,j) in {(1,2),(1,1),(0,1),(2,3)}, deg p <= 3, saturated by kappa != 0 and
a != 0) are committed and running.  NO VERDICT YET.  Standing semantics: a
solution with kappa != 0 and the divisibilities holding is a plane Keller map of
sweep type and must then be checked for NON-INJECTIVITY before any claim; no
solution bounds the shape family only and is not a proof that none exists.

================================================================================
TWO CATCHES ON MY OWN PLANE-SWEEP SEARCH, BOTH FOUND BEFORE IT FINISHED, AND THE
CORRECTED FORMULATION THAT ACTUALLY HAS CONTENT.
================================================================================

CATCH 1 -- THE SEARCH WAS VACUOUS BY MOH'S THEOREM.  The shape family I launched
(gamma = c0 + a x^al y^be with al,be <= 2; u = 1 + b x^mu y^nu with mu,nu <= 2;
w = gamma*u; deg p <= 3) produces maps of total degree at most about 32.  Moh
proved JC2 for all maps of degree <= 100.  So every shape in that family is a
theorem of Moh's, and the search was GUARANTEED to return nothing.  A negative
result from it would have carried exactly zero information, and I would have had
a 1728-shape "EMPTY" table to be misled by.  Killed mid-run.
  STANDING RULE ADDED: before launching any counterexample search, compute the
  MAXIMUM TOTAL DEGREE the ansatz can produce.  If it is <= 100, the search is a
  restatement of Moh and must not be run.  Degree > 100 is a necessary condition
  for a plane counterexample and is therefore a free pre-flight gate.
  (Second free gate, from GGV: gcd(deg P, deg Q) must be 16 or > 20.  Third,
  from GGHV as amended today: below max 125 the only surviving pair is
  (72,108), now in BOTH orientations.)

CATCH 2 -- THE TWIST ANSATZ WAS CIRCULAR IN TWO VARIABLES.  I had derived
    det J(P/C^i, Q/C^j) = C^{-i-j-1} [ C{P,Q} - j Q{P,C} + i P{Q,C} ]
and called the numerator "the plane side condition".  It is an identity, and the
identity control passed -- but it has no content.  Once the divisibilities hold,
write P = C^i A and Q = C^j B; then
    C{P,Q} - j Q{P,C} + i P{Q,C}  ==  C^{i+j+1} {A,B}
identically (verified symbolically for (i,j) = (1,2),(2,1),(1,1),(2,3),(3,1)).
So the "side condition" says {A,B} = kappa, i.e. "F = (A,B) is a Keller map" --
which is what we were trying to solve.  The twist is bookkeeping, not a
constraint.  In dimension 3 the content is NOT in this algebra either; it is in
the fact that C = gamma*x is a COMPONENT OF THE TARGET, so dividing by it is a
genuine map on the target and the sweep's non-injectivity is inherited.  The
plane has no spare component, which is the real content of "dimension >= 3".

THE CORRECTED FORMULATION (this one is not circular).  Take gamma, u in C[x,y],
set w = gamma*u, and keep Alpoge's normalization p(0) = 0.  Then q = int (s/2)p'
starts at w^2, so
    P = p(w) + 2*gamma       is divisible by gamma
    Q = q(w) + gamma*w       is divisible by gamma^2
AUTOMATICALLY (verified by exact polynomial division, remainder 0).  Put
P~ = P/gamma, Q~ = Q/gamma^2.  Then the exact identity

    gamma * {P~, Q~}  =  2{gamma,u} - P~{gamma,Q~} + 2 Q~{gamma,P~}

holds (verified symbolically), so F = (P~, Q~) is a Keller map with
det J(F) = kappa precisely when

    kappa * gamma  =  2{gamma,u}  -  P~{gamma,Q~}  +  2 Q~{gamma,P~}      (*)

This IS a constraint: two unknown polynomials gamma(x,y), u(x,y) and the
coefficients k_1..k_d of p, with (*) an identity in x,y.  It is the plane
analogue of Gao section 3.3 with the padding variable removed and the
divisibility supplied by w = gamma*u instead of by C = gamma*x.

WHAT (*) DOES NOT GIVE, AND MUST BE CHECKED SEPARATELY.  In dimension 3 the
non-injectivity of the sweep is inherited automatically because the twist is a
map on the target.  Here it is not: gamma is not in general recoverable from
(P~, Q~), so F is not literally (map) o S o phi.  ANY SOLUTION OF (*) MUST HAVE
ITS NON-INJECTIVITY CHECKED DIRECTLY before the word counterexample is used --
a solution of (*) with F injective is just an automorphism and proves nothing.

================================================================================
THE B=16 LADDER, RE-READ.  Four structural facts that were invisible until
today's correction, and that shrink every cell by seven unknowns.  ALL VERIFIED
FOR MANY d, none assumed.  This is where a hit is a counterexample.
================================================================================

WHY THIS CELL AND NOT ANOTHER.  Of everything the campaign has open, the B=16
ladder is the only place where a single point converts into a counterexample by
a PUBLISHED THEOREM plus an explicit recipe: GGV Theorem 1.2 says B = 16 iff
(1.2)+(1.3) has a solution, and a solution with mu0 != 0 "would yield a
counterexample to the JC" (their p.85), constructed in their Section 2.  Two
supporting checks: cell d realizes degrees (16(3d-2), 16(2d-1)), and
gcd(3d-2, 2d-1) = 1 always (since 2(3d-2) - 3(2d-1) = -1), so every cell has
B = 16 EXACTLY -- admissible under GGV's own "B = 16 or B > 20".  Moh needs
max > 100, i.e. d >= 3; GGHV's elimination reaches only max < 125, i.e. d <= 3.
So every cell with d >= 4 is virgin territory no published work touches.

(F1) mu0 OCCURS IN EXACTLY ONE EQUATION OF THE WHOLE SYSTEM.  It appears in
(1.3) only through the term -6*mu0*y^3, hence only in the y^3 coefficient row,
linearly, with the constant coefficient 6 (checked d = 3..12).  That row
therefore constrains nothing -- it DEFINES mu0.  The campaign knew mu0 entered
linearly in one term (BIFURCATION.md, "G is a constant vector") but used it only
for a first-order rank test at a single point; it never used it to remove mu0
and its row from the system.

(F2) ON THE NORMALIZED LOCUS THAT ROW COLLAPSES TO ONE MONOMIAL.  Substituting
GGV's own b0 = mu3, b1 = 0 and (1.2)'s a0 = -mu3^2/4, a1 = mu2, and mu1 from
(1.2) row 3, the y^3 row goes from 20 terms to

                        6*mu0  -  2*a2*mu2  =  0,     i.e.   mu0 = a2*mu2/3

for EVERY d (checked 3,4,5,6,7,8,10,12), in BOTH the corrected and the printed
variant -- so this one is robust to the typo.  Therefore

        a counterexample (mu0 != 0)   <=>   a2 != 0   AND   mu2 != 0.

COROLLARY, and it retires a whole lane: the chart mu2 = 0 CANNOT CONTAIN A
COUNTEREXAMPLE at any d.  The campaign's Z/N chart split ran mu2 = 0 as a
first-class case at every level; half that compute was spent on a region proved
here to be empty of counterexamples in one line.

(F3) A NEW NECESSARY CONDITION ON THE BRACKET CONSTANTS.  Combining (F2) with
the CORRECTED (1.2) row 3, mu1 = -mu3*a2/3, and eliminating a2:

                        mu0*mu3 + mu1*mu2 = 0

for every d (checked 3..12).  Since [P,Q] = x^4 y + mu3 x^3 + mu2 x^2 + mu1 x
+ mu0, this is a condition on the bracket of ANY B=16 counterexample.  It FAILS
on the printed variant, which gives mu0*mu3 + mu1*mu2 = -(2/3)*mu3*b2*mu2 -- so
it is a consequence of today's correction and could not have been seen before.

(F4) THE SYSTEM IS WEIGHTED-HOMOGENEOUS, so the torus gauge is exact.  Under

    wt(a_i) = 2d-i,  wt(b_j) = d-j,  wt(mu3) = d,  wt(mu2) = 2d-1,
    wt(mu1) = 3d-2,  wt(mu0) = 4d-3

EVERY equation carries a single weight (verified row by row for d = 3..8).  All
weights are positive except wt(a_{2d}) = 0.  So on mu2 != 0 the C^* action
scales mu2 to 1, over an algebraically closed field, and

    solutions with mu2 != 0 exist  <=>  solutions with mu2 = 1 exist.

This is the torus the campaign DISCARDED, on the explicit grounds that "the term
2*mu3*q1''(0) in (1.2) row 3 breaks every continuous torus" (ADJUDICATION
section 6).  That term is the misprint.  The gauge is exact and is now restored.

THE RESULTING SYSTEM (wave6/w6_b16_mu0_export.py, which re-verifies F1-F2 at
every d before exporting).  Substituting a0, a1, a2, b0, b1, mu1, mu2 and
dropping the y^3 row:

    d    this export        campaign's version     max total degree
    5    18 eqs / 14 unk    27 / 21                4   (unchanged)
    6    22 / 17            31 / 24                4
    7    26 / 20            35 / 27                4
    8    30 / 23            39 / 30                4

Seven fewer unknowns at every level, with NO degree blow-up -- unlike the
cascade reduction below, which trades unknowns for degree ~4d.

CONTROLS RUN AND PASSED: d = 5 EMPTY in char 0 in 0.99 s (direct system: 4.42 s)
and d = 6 EMPTY in 39.7 s (direct: 64.66 s), both agreeing with the direct
corrected runs.  d = 7 launched.

ALSO RECORDED -- THE LADDER IS A CASCADE (wave6/w6_b16_cascade.py).  Ordering
the (1.3) rows by descending power of y: row y^{4d} is quadratic in a_{2d}
alone (GGV's row-0 quadratic), and row y^{4d-k} is LINEAR in the single new
unknown a_{2d-k} for k = 1..2d, with coefficient

        -( (4(2d-k) + 8d - 12) * a_{2d} + 3 )

depending on a_{2d} ONLY (verified per d).  That coefficient never vanishes at a
root of the row-0 quadratic (substituting a_{2d} = -3/(4j+8d-12) into it gives
-144 - 3(8d-4)^2 != 0), so all 2d+1 of the a's back-substitute away with no
Groebner basis at all, leaving rows y^{2d-1}..y^0 as pure constraints:

    d = 5:  26 eqs / 20 unk  ->  14 / 7      d = 6:  30 / 23  ->  17 / 10

round-trip verified by resubstitution into the original system.  The cost is
max total degree ~4d+1 instead of 4.  The two reductions are complementary and
can be stacked; which wins is an empirical question per d, not a theory question.
This cascade structure IS the weight filtration of (F4): row y^j carries weight
4d-j, and the variable of weight w is exactly the one that row introduces.

================================================================================
THE RANK / BIFURCATION CRITERION IS A CAN'T-FAIL CERTIFIER.  Its uniform
"obstructed at every d" answer is forced by the shape of the system and carries
NO information about whether counterexamples exist.
================================================================================

WHAT IT CLAIMED.  BIFURCATION.md and MORNING_SUMMARY.md report, as a headline
"DECIDED" result, that the rank test rank[J|G] = rank J + 1 holds at the
quasi-homogeneous point for d = 3..15, 18, 20 and the resonant d = 27, and gloss
it as "no counterexample bifurcates off that stratum at any d tested".  The test
asks whether G = dF/dmu0 lies in the image of J, i.e. whether there is a
first-order deformation in which mu0 moves.

WHY IT CANNOT ANSWER ANYTHING ELSE.  By (F2) above, the system contains the
equation  6*mu0 - 2*a2*mu2 = 0.  Differentiate it at any point where a2 = 0 and
mu2 = 0:

    d(6*mu0 - 2*a2*mu2) = 6*dmu0 - 2*(a2*dmu2 + mu2*da2) = 6*dmu0.

So the LINEARIZED system contains the row 6*dmu0 = 0, forcing dmu0 = 0 in every
first-order deformation.  The quasi-homogeneous point has all variables zero
except a_{2d}, so a2 = mu2 = 0 there for every d >= 2.  Verified directly: at
that point the gradient of the mu0-row has exactly ONE nonzero entry, the
coefficient 6 of mu0 itself (checked d = 3, 5, 8, 12).

Hence G is never in the image of J at that point, FOR EVERY d, whether or not
counterexamples exist anywhere in the cell.  The criterion is incapable of
returning any other verdict there.

THE UNDERLYING REASON, stated positively.  mu0 = a2*mu2/3 is a PRODUCT of two
quantities that both vanish at the quasi-homogeneous point.  Along any curve of
solutions through it, mu0 = O(s^2).  A first-order test looks for O(s) and will
never see an O(s^2) quantity.  Turning mu0 on is intrinsically a SECOND-order,
codimension-two move: BOTH a2 and mu2 must be deformed away from zero.  The
unbroken "obstructed" pattern across d = 3..27 was measuring that fact, not
rigidity of the cell.

STATUS CHANGE.  Every rank-criterion row is downgraded from evidence to
bookkeeping.  It does not support "the B=16 corridor is closed", it does not
support the resonant-cell conclusions at d = 12 and d = 27, and it must not be
cited as evidence that a counterexample does not bifurcate.  What survives is
the exact arithmetic (the ranks are correctly computed) and the observation that
the obstruction at d=3 equals exactly 6*mu0 -- which is now explained: it IS the
mu0-row.

FAILURE CLASS: (v) can't-fail certifier.  This is the third instance today
(after the watcher regex and the numerical floors), and the most expensive,
because it was the load-bearing evidence for a headline claim.  The general
lesson, now a standing rule: BEFORE running any first-order test, ask what the
test would report if the quantity being tested for were a product of two
functions vanishing at the base point.  If the answer is the same as the answer
you expect to get, the test is vacuous.

WHAT TO DO INSTEAD.  The right local question at that point is second-order, or
better, the global one this file already sets up: solve the cell with mu0
eliminated, mu2 gauged to 1, and a2 saturated.  That is exactly the export in
wave6/w6_b16_mu0_export.py.

================================================================================
TWO BLINDSPOTS IN TODAY'S OWN RESULTS, BOTH RAISED AS CHALLENGES AND BOTH REAL.
One is a correction to how I presented the evidence; the other is now closed by
an independent test.
================================================================================

BLINDSPOT 1 -- "VERIFIED FOR MANY d" WAS RE-CHECKING ONE OBJECT.
I reported (F2) mu0 = a2*mu2/3 and (F3) mu0*mu3 + mu1*mu2 = 0 as "verified for
d = 3,4,5,6,7,8,10,12".  That reads as eight independent confirmations.  It is
not.  Printing the RAW y^3 row before any collapse:

    d :  len(rows)   len(a)=2d+1   mu0-row index   #terms(H)
    3        13           7           9 (y^3)          20
    5        21          11          17 (y^3)          20
    7        29          15          25 (y^3)          20
    9        37          19          33 (y^3)          20

and then comparing them AS POLYNOMIALS:

    H(d=5) == H(d=7) == H(d=9)   -- identical expressions, not merely equivalent
    H(d=3) - H(d=5) = 3*(b3 - 1)*(8*a0*b0 - 4*a0*mu3 - 2*b0^3 + 3*b0^2*mu3)/4

The reason is structural and should have been stated up front: the y^3
coefficient of (1.3) can only involve a_0..a_3, b_0..b_3 and the mu's -- every
index is capped at 3 -- so for d >= 4 the row is literally d-INDEPENDENT.  The
d = 3 case differs only because b3 does not exist there (q1 = y^3 + ... has
leading coefficient 1 in the y^3 slot), and the difference is exactly the
substitution b3 -> 1.

CONSEQUENCE.  (F2) and (F3) are each ONE identity, not a pattern across d.  That
does not weaken them -- a single identity valid for all d >= 4 by construction is
cleaner than a coincidence repeated -- but it does mean the multi-d runs carried
no extra evidential weight, and I should not have presented them as if they did.
The ledger is corrected accordingly.  The same caution applies to (F1), which is
likewise structural (mu0 enters (1.3) only through -6*mu0*y^3).
GENERAL RULE ADDED: before reporting "verified for d = ...", check whether the
object being verified actually depends on d.  If it does not, say so and report
it as one check.

BLINDSPOT 2 -- THE WHOLE SESSION RESTED ON ONE UNCORROBORATED TEXTUAL
CORRECTION.  Fair, and it is now closed.

THE MISPRINT IN ONE LINE: GGV print  mu3*A''(0) = -6*mu1 - 2*mu3*q1''(0);
the truth is  mu3*A''(0) = -6*mu1.  The spurious term is -2*mu3*q1''(0).

It now rests on four independent legs, not one:

 (i)   THE SOURCE, TWICE, IN TWO DIFFERENT DOCUMENTS.  I read the misprint off
       the 150dpi page renders of the printed offprint myself (p.85 Theorem 1.2
       and p.93 equation (3.6)).  Separately, the final arXiv version
       1310.8249v3 -- whose own journal-ref line identifies it as the published
       version -- prints the same thing as its equation (3.9).  No erratum or
       corrigendum exists anywhere.  So the misprint is in the literature, in
       both versions, and is not an artifact of our transcription.
 (ii)  A RE-DERIVATION FROM THEIR OWN PRIOR EQUATIONS.  wave6/w6_ggv12_
       rederivation.py starts from the Poisson bracket, checks all five bracket
       coefficients against the four ODEs printed on p.91, and obtains
       mu3*A''(0) = -6*mu1 from the polynomiality of their (3.2) and (3.3).
 (iii) AN EXPLICIT NUMERICAL INSTANCE, INDEPENDENT OF (ii).  Using ONLY the
       definitions P = x^3 y + x^2 p2 + x p1 + p0, Q = x^2 y + x q1 + q0 and
       A := y p1 - q1 p2 + (3/4) q1^2 -- all read off the page renders -- and a
       DIRECT Poisson bracket, with q0', p0' obtained by solving the bracket's
       own x^2 and x^1 coefficient equations and demanding polynomiality:

           q1 = 3y^2 + 5          p2 = 15y^2/2 + 5      p1 = y^2 + 6y + 7
           q0 = -5y^3 + y^2/2 + 7y
           p0 = -225y^4/8 + 5y^3/2 - 27y^2/4 + 21y

       gives  [P,Q] = x^4*y + 5x^3 + 7x^2 + 40x + (non-constant),  so
       mu3 = 5, mu2 = 7, mu1 = 40 are genuine constants and this is a real
       instance of the Theorem 1.1 setup.  Crucially q1''(0) = 6 != 0 and
       mu3 = 5 != 0 -- the case BOTH of GGV's own worked examples fail to
       exercise.  Then A = -63y^4/4 + y^3 - 24y^2 + 7y - 25/4, so
           A(0)  = -25/4 = -mu3^2/4          (their row 1 holds)
           A'(0) = 7     = mu2               (their row 2 holds)
           mu3*A''(0) = -240 = -6*mu1        (CORRECTED FORM HOLDS)
           printed form demands -300         (FAILS, by exactly 2*mu3*q1''(0)=60)
       This uses none of (ii)'s algebra: it is arithmetic on explicit
       polynomials.
 (iv)  INTERNAL CONSISTENCY (the weakest leg, listed last): the corrected row is
       implied by (1.3) on mu3 != 0, whereas the printed row additionally forces
       4*mu3^2*b2 into the ideal.

Legs (i) and (iii) together are decisive and are independent of everything else
found today.  The single-point-of-failure is closed.

================================================================================
THE B=16 OBSTRUCTION IS NOT ABOUT mu0 AT ALL.  IT IS THAT mu2 != 0 IS
IMPOSSIBLE -- and that is a much better target for a uniform theorem.
================================================================================

THE OBSERVATION.  Take the gauged export (mu2 = 1, a2 = 3*mu0, mu1 = -mu0*mu3,
y^3 row dropped) and REMOVE the mu0 saturation, so mu0 = 0 is allowed.  Then:

    d = 3   EMPTY   char 0   0.00 s        d = 5   EMPTY   char 0   0.74 s
    d = 4   EMPTY   char 0   0.02 s        d = 6   EMPTY   char 0  36.25 s

Empty even with mu0 free.  So the cells contain NO SOLUTION WITH mu2 != 0 at
all, at d = 3,4,5,6 -- nothing to do with mu0.

This is consistent with GGV's published d = 3 family, which has
mu0 = mu1 = mu2 = 0 and is therefore excluded by the mu2 = 1 gauge, not by the
saturation.  Soundness of the reading: any solution with mu2 != 0 can be scaled
to mu2 = 1 by the C^* action (F4), and then satisfies (F2) a2 = 3*mu0 and (F3)
mu1 = -mu0*mu3, so it is a point of the exported variety.  Empty ==> no such
solution.

WHY THIS IS THE BETTER TARGET.  By (F2), a counterexample requires mu2 != 0.  So

        "mu2 = 0 on every solution of (1.2)+(1.3), for every d"
                        ==>  B = 16 IS CLOSED, for all d at once.

That is one clean statement to prove or refute, replacing an infinite ladder of
emptiness computations.  It is also strictly stronger than what GGV proved for
d <= 4 (they showed every solution has mu0 = 0; this says every solution has
mu2 = 0), and it is verified here for d = 3..6 in characteristic zero.

A ROUTE THAT IS NOW CLOSED, WITH THE REASON.  The natural attempt is to prove it
from the LOW rows alone, because those are d-INDEPENDENT: the y^k coefficient of
(1.3) involves only a_0..a_k and b_0..b_k, so for k < d the row does not depend
on d (verified: rows y^0..y^8 are identical at d = 14 and d = 11).  A
contradiction among them would hold for all large d simultaneously.  It cannot
happen.  Counting new unknowns per row, after the normalizations:

    y^2 : +1 eq, new {a2, mu1, mu3}      deficit +2
    y^3 : +1 eq, new {mu0, mu2}          deficit +3
    y^4 : +1 eq, new {a3, a4, b2}        deficit +5
    y^5 : +1 eq, new {a5, b3}            deficit +6
    y^6 : +1 eq, new {a6, b4}            deficit +7      ... and so on

From y^4 onward every row brings TWO new unknowns (a_k and b_{k-2}) for ONE
equation, so the deficit grows monotonically and the low system is
underdetermined at every truncation.  It can never be inconsistent.  No uniform
theorem comes from the bottom end alone.

WHAT THE SYSTEM ACTUALLY IS: A TWO-ENDED RECURSION (a shooting problem).
  * From the TOP, the cascade (row y^{4d} quadratic in a_{2d}; row y^{4d-k}
    linear in a_{2d-k}) determines a_{2d}, a_{2d-1}, ... downward in terms of
    the b's.
  * From the BOTTOM, row y^k has a_k with the nonzero coefficient -a_k*mu3^2
    (on mu3 != 0), so it determines a_k upward in terms of a_2..a_{k-1} and
    b_2..b_{k-2}.
  * BOTH ends determine the same a's.  The entire content of the cell is the
    MATCHING CONDITION in the middle.
That is exactly the structure of a two-point boundary value problem for the
Abel equation GGV say (1.3) is, and it is the right frame for the remaining
work: solving from both ends and matching halves the length of each
back-substitution chain, so it should also halve the degree growth that makes
the one-ended cascade expensive at large d.

================================================================================
WE AUDITED (1.2) AND NEVER AUDITED (1.3).  Now done: (1.3) IS CORRECT, and the
verification hands us a much more concrete form of the whole problem.
================================================================================

THE GAP.  This morning we found that GGV's (1.2) is misprinted, re-derived it,
and rebuilt the campaign on the corrected form.  But every one of today's
results also rests on (1.3), which IS the system -- and (1.3) had only ever been
checked against GGV's own two worked examples, i.e. against exactly the examples
that provably cannot detect the (1.2) error either (both have q1''(0) = 0).
That is the same blindspot, one equation over.

THE AUDIT.  GGV obtain (1.3) by inserting their parametrization into the FOURTH
bracket ODE, mu0 = p1*q0' - p0'*q1.  So (1.3) should be equivalent to that ODE.
Starting from the p.91 ODEs and the p.92 general solution (q1 = mu3 + y^2 F',
p2 = mu3 + yF + (3/2)y^2 F', F in y K[y]), solving ODE2 for q0' and ODE3 for p0'
with the polynomiality conditions, and writing Omega := p1*q0' - p0'*q1, the
residual of (1.3) divides EXACTLY:

        E(1.3)  =  -6*y^3 * ( Omega - mu0 ),     remainder 0

(symbolic, with F of degree 4 and p1 of degree 5, all coefficients free).  So

        (1.3)   <==>   p1*q0' - p0'*q1 = mu0.

(1.3) IS CORRECT.  The factor -6*y^3 is exactly the coefficient of the -6*mu0*y^3
term, as it must be.  The foundation now rests on four independently checked
legs: the Theorem 1.1 normal form (read off the page renders), the four bracket
ODEs (re-derived from the Poisson bracket and matched to p.91 term by term),
(1.2) (re-derived, misprint found, confirmed by an explicit numerical instance),
and (1.3) (this check).

A STRUCTURAL COROLLARY THAT EXPLAINS AN EARLIER OBSERVATION.  Because the
residual is divisible by y^3, the y^0 and y^1 coefficient rows of (1.3) VANISH
IDENTICALLY and the y^2 row is not an independent condition at all -- it is
exactly (1.2) row 3, up to the factor -mu3/2:

        y^2 row  =  -mu3*(a2*mu3 + 3*mu1)  =  -(mu3/2) * [corrected (1.2) row 3]

which is why the corrected row 3 turned out to be redundant on mu3 != 0 while the
misprinted one added the spurious 4*mu3^2*b2 to the ideal.  The redundancy was
observed this morning; it is now explained.

THE PROBLEM, RESTATED CONCRETELY.  (1.3) is not really a differential equation to
be matched coefficient by coefficient.  It says:

    choose F in y K[y] and p1 in K[y] with p1(0) = mu2;
    q1 := mu3 + y^2 F',  p2 := mu3 + yF + (3/2) y^2 F';
    let q0' and p0' be the (forced, polynomial) solutions of ODE2 and ODE3;
    then  B = 16  <==>  p1*q0' - p0'*q1  is a NONZERO CONSTANT.

That is a Wronskian-type condition, det [[p1, q1], [p0', q0']] = mu0 != 0, on two
freely chosen polynomials.  Degree count: deg q0' = 2d-2, deg p0' = 3d-3, so
Omega has degree up to 4d-3 and requiring it constant is 4d-3 cancellations
against roughly 3d free coefficients -- the same excess d-3 seen from the
coefficient side, now visible as massive cancellation in a single determinant
rather than as an opaque overdetermined system.

================================================================================
A COMPLETELY DIFFERENT HUNT: CLASSIFY BY THE DECK GROUP, NOT BY THE DEGREE PAIR.
Result: a plane Keller counterexample CANNOT have geometric degree 2, and more
generally cannot be a Galois covering.  So hunt at mu >= 3 -- which is exactly
where the dimension-3 counterexamples live.
================================================================================

THE SHIFT.  Every hunt in this campaign has had the same shape: pick a cell of
the GGV/GGHV Newton-polygon framework, write down its coefficient system, and
try to solve it.  That is elimination.  The dimension-3 refutation was NOT found
that way -- Alpoge/Gallagher/Speyer found it by asking what KIND of map can be
etale and non-injective, and then constructing one.  So: classify the possible
maps, not the possible degree pairs.

THE HANDLE.  A counterexample F = (P,Q) : C^2 -> C^2 has generic fibre size
mu >= 2, so C(x,y) / C(P,Q) is a field extension of degree mu.  Let
G := Aut(C(x,y)/C(P,Q)) -- the deck group.  Every element of G is a BIRATIONAL
SELF-MAP of C^2 fixing P and Q.  Finite-order birational self-maps of the plane
are CLASSIFIED (Bayle-Beauville for involutions; Dolgachev-Iskovskikh, Blanc for
higher order).  That is a finite classification to search, in place of an
infinite ladder of degree pairs.

THE LEMMA (short, and it is the whole engine).
    Let sigma in G, let p in C^2 with sigma regular at p and sigma(p) = p.
    F is etale at p, hence a local biholomorphism, hence INJECTIVE near p.
    From F o sigma = F and injectivity, sigma = id near p, so sigma = id.
So EVERY non-identity element of G is FIXED-POINT-FREE on the open set of C^2
where it is regular.

APPLYING IT AT mu = 2.  Degree 2 is automatically Galois, so G = Z/2 and its
generator sigma is a nontrivial birational involution of C^2 that must be
fixed-point-free.  By Bayle-Beauville every nontrivial birational involution of
P^2 is conjugate to one of:

  * de JONQUIERES -- preserves a pencil of lines.  Computed here explicitly:
        sigma(x,y) = ( x , (a(x) y + b(x)) / (c(x) y - a(x)) )
    verified to be an involution, with fixed locus the conic
        c(x) y^2 - 2 a(x) y - b(x) = 0,
    a nonempty affine curve.  Its resultant with the pole locus c(x)y - a(x) is
    (a^2 + b c)*c, which is NONZERO exactly when sigma is a genuine involution --
    so sigma is REGULAR along its own fixed curve, and the lemma applies.
    (Sub-case c = 0: sigma(y) = -y - b/a, fixed locus y = -b/(2a), same
    conclusion.)  CONTRADICTION.
  * GEISER (fixed curve a smooth quartic, genus 3) and BERTINI (genus 4).  A
    curve of genus >= 1 is not rational, and every boundary component of a smooth
    compactification of C^2 is rational, so the fixed curve cannot lie in the
    boundary and must meet C^2.  CONTRADICTION.
  * LINEAR (fixed locus = a line plus an isolated point).  If the fixed line is
    taken to be the line at infinity, the isolated fixed point lies in C^2.
    CONTRADICTION.

    ==>  A PLANE KELLER COUNTEREXAMPLE CANNOT HAVE GEOMETRIC DEGREE 2:  mu >= 3.

INPUTS I AM RELYING ON, STATED HONESTLY: Bayle-Beauville's classification of
birational involutions of P^2, and the fact (Ramanujam / Morrow) that every
boundary component of a smooth compactification of C^2 is rational.  Neither is
re-derived here.  The de Jonquieres computation IS done here and is the case
that carries the most weight, since it is the flexible family.

GENERALISATION, AND WHERE IT STOPS.  The lemma applies to any nontrivial deck
transformation, so the same argument attacks every case where G != 1, i.e. every
GALOIS covering.  It says nothing when G = 1: for mu = 3 with Galois closure S_3
the deck group is trivial (the point stabiliser S_2 is not normal), and the
argument gives no information.  So the honest statement is:

    a plane Keller counterexample is a NON-GALOIS covering of degree mu >= 3.

WHERE TO HUNT NOW.  mu >= 3, non-Galois.  This is a real convergence: Alpoge's
dimension-3 counterexample has geometric degree exactly 3, Gallagher's family
realizes every degree >= 3, and the tangent sweep of a degree-d curve has
mu = d+1 >= 3.  Every known counterexample-producing mechanism sits at mu >= 3,
and we now know the plane must too.  Degree 2 -- the first thing anyone would
try -- is provably empty, which is worth knowing before spending compute on it.

================================================================================
THE SWEEP MECHANISM IS DEAD IN THE PLANE -- COMPLETELY, WITH A SHARP REASON.
And the torus rank confirms the (1.2) correction a fourth time.
================================================================================

TORUS RANK (computed, not argued).  Taking every pair of monomials in every
equation and computing the nullspace of their exponent differences -- the exact
space of gradings under which the whole system is weighted-homogeneous:

    d      corrected system      printed system
    4      TORUS RANK 1          TORUS RANK 0
    5      TORUS RANK 1          TORUS RANK 0
    6      TORUS RANK 1          TORUS RANK 0

and the rank-1 grading recovered is exactly the one derived by hand:
wt(a_i) = 2d-i, wt(b_j) = d-j, wt(mu3) = d, wt(mu2) = 2d-1, wt(mu1) = 3d-2,
wt(mu0) = 4d-3.  So the misprint DESTROYS the symmetry outright.  ADJUDICATION
section 6 observed exactly this and drew the wrong conclusion -- that no
continuous torus exists -- when the right conclusion was that the equation was
wrong.  This is a fourth independent confirmation of the correction.

It also CORRECTS a claim passed to me earlier today, that the corrected system
carries a TWO-parameter torus.  It does not: the rank is 1, and the gauge
freedom is therefore already fully spent by mu2 = 1.  No further reduction is
available from symmetry.  (The raw system before GGV's normalizations b0 = mu3,
b1 = 0 and q1 monic may well have rank 2; those normalizations consume the
second parameter, which is presumably what that claim was seeing.)

THE SWEEP DICHOTOMY.  For a general plane sweep S(gamma,w) = X(w) + gamma*Delta(w)
with X, Delta in C[w]^2, direct differentiation gives (verified symbolically)

        det J(S)  =  det(Delta, X')  +  gamma * det(Delta, Delta').

Two cases, and BOTH are closed:

 (a) det(Delta, Delta') != 0.  Then det J(S) has positive degree in gamma, so it
     vanishes on a curve and S is not Keller.  The divisional twist cannot
     repair this in the plane: with w = gamma*u the twisted Jacobian is
     u^2 * Psi(gamma,u) * {gamma,u}, and a product of polynomials equal to a
     nonzero constant forces u to be constant, whence {gamma,u} = 0.

 (b) det(Delta, Delta') = 0.  Then Delta is parallel to a CONSTANT vector,
     Delta(w) = h(w)*v.  Normalising v = (0,1),
         S(gamma,w) = ( X1(w), X2(w) + gamma*h(w) ),   det J(S) = -h * X1'.
     Constant and nonzero forces X1' constant, so X1 is LINEAR and h is
     constant -- and then S is a TRIANGULAR automorphism, hence INJECTIVE.

    ==>  NO PLANE SWEEP IS A COUNTEREXAMPLE.

THE REASON, IN ONE SENTENCE: non-injectivity of a sweep requires the direction
field to TURN, and turning is precisely what puts the factor gamma into the
Jacobian.  Dimension 3 has a spare coordinate to absorb that factor (C = gamma*x,
divide by C and C^2); the plane does not.  That is the actual content of
"dimension >= 3", which arXiv:2608.00222 asserts but never explains.

WHAT THIS COSTS US, STATED PLAINLY.  Combined with today's deck-group result
(no Galois covering; mu >= 3), the position is:
  * the only mechanism that has ever produced a counterexample to the Jacobian
    conjecture in ANY dimension -- the tangent sweep -- provably cannot work in
    the plane;
  * a plane counterexample must be a NON-GALOIS covering of degree mu >= 3;
  * so it must use a mechanism that is not known in dimension 3 either.
That is a sobering finding rather than an encouraging one, and it should be
recorded as such.  It also means effort is better spent on the systems where the
Newton polygons are already pinned down -- (72,108) in both orientations -- than
on constructing sweeps.

================================================================================
B=16 LADDER: d = 7 IS EMPTY IN CHARACTERISTIC ZERO.  And the (72,108) pentagon
bottom edge is NON-EMPTY, zero-dimensional, and explicit.
================================================================================

d = 7 CLOSED.  msolve on the mu0-eliminated, mu2-gauged export: 26 equations /
20 unknowns, zero constant generators, stderr clean, characteristic 0 (so this
is a proof, not a modular signal).  1345.48 s, 6.67 GB.  Verdict [-1] = EMPTY.
Mod p = 1000003 agrees (21 min).  The corrected ladder now reads, all in char 0:

    d      verdict     degrees (16(3d-2), 16(2d-1))     status
    3      EMPTY       (112,  80)     reproduces GGV
    4      EMPTY       (160, 112)     reproduces GGV
    5      EMPTY       (208, 144)     NEW  (GGV stalled here)
    6      EMPTY       (256, 176)     NEW
    7      EMPTY       (304, 208)     NEW

GGV solved deg(q1) = 2,3,4 and stalled at 5 ("after an hour the PC hadn't
solved it").  d = 5,6,7 are decided here for the first time, on the CORRECTED
system, and all three lie above GGHV's max < 125 reach, so no published work
touches them.  Reminder of the standing caveat: these close cells of the
ladder, not the conjecture -- d >= 8 remains open and the ladder is infinite.

THE (72,108) PENTAGON BOTTOM EDGE, VERIFIED AND SOLVED.

Verification first.  Grouping the 283 equations of trackB1_param_system.json by
the linear functional L = 2*alpha - beta on the bracket point gives 17 equations
at the extreme level L = 4, involving exactly the 18 bottom-edge variables
c_{i,2i-2} (i = 1..8) and d_{j,2j-3} (j = 2..12) -- a closed subsystem.  With

    w = x y^2,   f = sum_{i=1..8} c_{i,2i-2} w^i,   g = w^2 + sum_{j=3..12} d_{j,2j-3} w^j

(d_2_1 is already gauged to 1 in the JSON), I generated the coefficients of

                        2 f g' - 3 f' g  =  w^2

and matched them against the JSON: ALL 17 MATCH, SCALE FACTOR EXACTLY 1, no
unmatched rows.  The equation at bracket point (2,0) is literally c_1_0 - 1 = 0.
So 17 of the 283 equations collapse to a single identity in ONE variable, and
the bottom-vertex datum c_1_0 * d_2_1 = 1 is precisely its w^2 coefficient --
the inhomogeneity of that one equation.
  (Method note: my first pass matched only 9/17.  The misses were exactly the
  low bracket points, because I had left d_2_1 symbolic while the JSON has it
  gauged to 1.  With the gauge applied the match is exact.  Recorded because the
  9/17 near-miss is precisely the kind of partial agreement that invites a
  wrong conclusion in either direction.)

Solving it.  17 equations, 18 unknowns, with a residual 1-parameter torus
c_i -> t^{i-1} c_i, d_j -> t^{j-2} d_j (derived by requiring 2fg'-3f'g = w^2 and
the gauge d_2_1 = 1 to be preserved; note c_1_0 has weight 0, so the torus does
NOT act on it and c_1_0 = 1 does not fix the gauge).  In the chart c_2 = 1,
msolve returns

        dim = 0,  eliminating polynomial of degree 9,  155.72 s, 189 MB
        (p = 1000003; characteristic 0 running)

so the bottom-edge system is NON-EMPTY with finitely many solutions.

WHAT THIS IS AND IS NOT.  A bottom edge is 17 of 283 equations.  It is NOT a
counterexample and must not be reported as one.  What it is: the first
explicit, finite starting point this campaign has had on (72,108) -- a short
list of candidate bottom edges, from which the remaining levels of the same
L-grading are far more constrained than the raw system.  The next step is to
extend each seed upward level by level and see which, if any, survive; a seed
that survives every level IS a counterexample and would then need exact
verification of [P,Q] = const and a bijectivity check.

================================================================================
THE (72,108) PENTAGON BOTTOM EDGE IS COMPLETELY CLASSIFIED, AND IT ADMITS
EXACTLY ONE ADMISSIBLE SEED MOD p.  The pentagon case now has a single, fully
explicit entry point instead of a 283-equation wall.
================================================================================

THE GRADING (verified against the data, not assumed).  Grade every variable and
every bracket point by L = 2*alpha - beta.  Then:
  * every monomial of the 283 equations is BILINEAR -- exactly one c and one d --
    up to powers of the four s-variables (counts: 5376 (c,d), 1069 (d,s,s),
    990 (c,s,s,s), 496 (c,s,s), 431 (d,s), 200 (c,s), 99 (d), 95 (c), 2 constants);
  * max L on P's support is 2, max L on Q's support is 3;
  * so the equations at level Lambda pair L(c) + L(d) = Lambda + 1, and the
    FRESH unknowns at level Lambda are exactly c at L = Lambda-2 (paired with the
    top d) and d at L = Lambda-1 (paired with the top c) -- each appearing
    LINEARLY, multiplied by an already-determined top-level coefficient.
The equation/fresh-variable census, running cumulative deficit:

   Lambda   4    3    2    1    0   -1   -2   -3  ...  -19
   eqs     17   18   19   19   20   19   18   17  ...    1
   fresh   18   19   20   19   18   16   13   11  ...    0
   defic   +1   +2   +3   +3   +1   -2   -7  -13  ... -118

So levels 4..0 are (barely) underdetermined and the system first becomes
OVERDETERMINED AT LEVEL -1.  That is where any obstruction must first appear.

THE TOP LEVEL IS ONE EQUATION IN ONE VARIABLE.  With w = x*y^2,
f = sum_{i=1..8} c_{i,2i-2} w^i, g = w^2 + sum_{j=3..12} d_{j,2j-3} w^j (d_2_1 is
gauged to 1), the 17 equations at L = 4 are EXACTLY the coefficients of

                        2 f g' - 3 f' g  =  w^2

-- all 17 matching at scale 1, verified term by term against the JSON.  The
bottom-vertex datum c_1_0 * d_2_1 = 1 is its w^2 coefficient, and in the gauge
the equation at bracket point (2,0) is literally c_1_0 - 1 = 0.

COMPLETE CHART ANALYSIS of that subsystem (17 equations, 18 unknowns, residual
torus c_i -> t^{i-1} c_i, d_j -> t^{j-2} d_j, on which c_1_0 has weight 0):

    ungauged           dim 1                    = exactly the torus orbits
    chart c_2 = 1      dim 0, eliminant deg 9   char 0 AND mod p (316 s / 156 s)
    chart c_2 = 0      EMPTY                    (1.67 s)

The c_2 = 0 chart being empty makes the c_2 = 1 chart EXHAUSTIVE up to the
torus, so this is a complete classification, not a sample.

THE SEEDS.  The degree-9 eliminant has 5 roots in F_p (p = 1000003); the other
4 solutions live in extensions and are not seen at this prime.  Extracting each
from the rational parametrization and substituting back:

    all 5 satisfy all 17 bottom-edge equations exactly (residuals 0/17),
    and d_3_3 = 2/3 on every one of them (it is a constant of the parametrization).

But the pentagon system carries nonzero = [c_1_0, c_8_14, d_12_21, s_4_8], and

    seed 0:  c_8_14 = 183720,  d_12_21 = 720777    ADMISSIBLE
    seeds 1-4: c_8_14 = 0 and d_12_21 = 0          KILLED by the side conditions

so exactly ONE of the five F_p-rational bottom edges is admissible.

SUBSTITUTING IT INTO THE FULL SYSTEM.  Pinning those 18 variables in the
283-equation system:
  * exactly 17 equations are satisfied (2 identically, 15 evaluating to 0 mod p)
    -- precisely the L = 4 level, which is the correct self-check;
  * NO nonzero constant row appears, so the seed does not die immediately;
  * 22 of the remaining equations are now LINEAR;
  * what is left is 266 equations in 147 unknowns (267/148 with the s_4_8
    saturation), degree profile {1:22, 2:72, 3:57, 4:115}.
That system is now running.  Standing caveat: this is mod p and one seed; a
non-empty answer is a candidate to be lifted and verified exactly, never a
counterexample by itself, and the 4 non-F_p-rational seeds still need a prime
where they are visible.

================================================================================
TWO BUGS IN MY OWN PENTAGON CASCADE, BOTH FOUND BY ME, BOTH RETRACTED.  The
files are committed WITH their defects documented, because a cascade that can
only ever answer "consistent" is the can't-fail certifier pattern again.
================================================================================

BUG 1 (wave6/w6_pent_levelcascade.py) -- MANUFACTURED A CONTRADICTION.
It reported "LEVEL 2 IS INCONSISTENT (1 contradictory row) -> THIS SEED DIES".
That is an ARTIFACT.  Level 3 solves to rank 17 with TWO FREE PARAMETERS, so the
level-3 variables are NOT determined.  The row-builder classifies a monomial as
"linear" whenever it has degree <= 1 in the FRESH unknowns -- but a monomial with
degree 0 in the fresh unknowns and containing an UNDETERMINED non-fresh variable
also passes that test, and is then added to the constant column, i.e. the
undetermined variable is silently set to 1.  The contradiction was produced by
that substitution, not found in the data.

  The general lesson, which was flagged in advance and which I did not heed:
  when a level leaves free parameters, consistency at lower levels is a
  POLYNOMIAL CONDITION ON THOSE PARAMETERS, not a plain rank test.  A rank test
  run after specialising the parameters (even implicitly, even to 1) answers a
  different question.

BUG 2 (wave6/w6_pent_cascade2.py) -- VACUOUS.  Written to fix Bug 1 by carrying
the parameters symbolically with fraction-free elimination over F_p.  It does
carry them correctly, but it NEVER WRITES THE SOLVED VALUES BACK into `known`.
So nothing propagates: from level 2 downward every monomial contains two still-
undetermined variables, every equation is classified nonlinear, and the run
reports "0 conditions, 0 contradictions" at every level.  It cannot fail.  That
is the third can't-fail certifier of the day and the second I wrote myself.

  Tell for this class of bug, worth adding to the pre-flight list: if a cascade
  reports NO constraints at EVERY level while the equation count exceeds the
  unknown count by 118, it is not finding a big solution set -- it is not
  computing anything.  Check that the "solved" values are actually used
  downstream before reading any verdict.

WHAT SURVIVES, AND WHAT DOES NOT.
  VOID: "the admissible seed dies at level 2"; and "no conditions arise at any
  level".  Neither statement has any content.
  INTACT (independently verified earlier, and untouched by these bugs):
    * the L = 2*alpha - beta grading and the bilinearity of every monomial;
    * the level census (deficits +1,+2,+3,+3,+1 then negative from Lambda = -1);
    * the identity 2 f g' - 3 f' g = w^2 for the 17 top-level equations, 17/17
      at scale 1, with c_1_0 - 1 = 0 as the bracket-point-(2,0) row;
    * the complete chart analysis of the bottom edge (ungauged dim 1; c_2 = 1
      dim 0 with a degree-9 eliminant in char 0 and mod p; c_2 = 0 EMPTY);
    * the five F_p-rational seeds, all satisfying the 17 equations exactly, of
      which exactly ONE is admissible under nonzero = [c_1_0, c_8_14, d_12_21];
    * pinning that seed into the 283-equation system satisfies exactly the 17
      L = 4 equations, produces NO nonzero constant row, and leaves 266
      equations in 147 unknowns with 22 of them linear.

THE REAL BLOCKER.  Propagating past level 3 requires dividing by pivots that are
polynomials in the two free parameters, i.e. rational-function arithmetic over
F_p.  That has to be implemented properly.  Until it is, the pentagon verdict
rests entirely on the direct msolve run on the pinned system, which is untouched
by these bugs.
