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
