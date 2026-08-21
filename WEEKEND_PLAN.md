# Weekend plan (Sat–Sun) — for Monday's audit

## Framing (read first)

The deliverable is NOT "counterexample or bust". A counterexample may not
exist; the exact evidence gathered so far points to B=16 being rigid, and most
of the field expects JC2 to be true. The deliverable is a body of VERIFIED
work with one decisive test at its centre. Success on Monday = every claim
below is either (a) computed and control-backed, or (b) explicitly labelled
undecided. Nothing else counts, and nothing else is claimed.

## P0 — THE decisive test: the pentagon truncation ladder

Why it is first: `truncate(W)` in campaign/audit_tracks/trackB1_pentagon.py
builds a CLOSED subsystem — every full solution restricts to a truncation
solution — so **an EMPTY truncation kills pentagon case (1) of (72,108)
outright**. That branch has never had a verdict by any method, anywhere.
The systems already exist on disk (trackB1_trunc10..19.json), W=19 being
21 equations in 27 unknowns: the smallest live object in the whole campaign.

Status: W=19 was run ONCE, died "no more memory" in Singular, and the route
was then dropped. Converted to msolve today and it was OOM-killed at this
container's 13.3GiB cap. Every failure so far has been MEMORY, never maths.

Actions, smallest first:
 1. W=19 (21 eqs / 27 vars) via msolve on a machine with >= 32GB.
 2. If it finishes: W=18 (40 eqs), then W=17 (60 eqs) as independent
    confirmations at the same prime, then a second prime for each.
 3. Guards: capture stderr (a parse error makes msolve print "[-1]" and exit
    0 — see CATCHES.md); reject any input carrying a constant generator;
    an EMPTY needs two agreeing primes before it is quoted.
 4. If EMPTY at two primes -> pentagon case (1) is DEAD; write it up as the
    first independent verdict on that branch.
 5. If NON-EMPTY -> extract the point, substitute exactly, then the
    finite-field one-to-one check (wave6/w6_bijcheck.py). That is a
    counterexample candidate on (72,108).

## P1 — The undecided B=16 cells (d = 8..12, chart N)

These are small systems (24–35 unknowns) that need only uninterrupted time.
Use the seeded, unsplit export (wave6/w6_seed_d8.py): seeding a root of the
mu-free row-0 relation covers the WHOLE cell, so the Z/N chart split is
unnecessary work. Roots are irrational (sqrt(12d)), so pick primes where 12d
is a square. Order: d=8, 9, 10, 11, 12. Two primes each before quoting.

## P2 — Extend the exact rank criterion

wave6/w6_rankcrit_modp.py now reaches every cell (discriminant square root
taken mod p). Unbroken so far: d = 3..15, 18, 20, 27 — including the resonant
d=27. Next: **d = 48**, the following resonant level (198 eqs, 143 unknowns;
exceeded a 520s budget here). Then d = 75. Any BIFURCATION_POSSIBLE=true is a
candidate point: re-run at a second prime, verify exactly, and stop everything
else.

## P3 — RESOLVED, AND IT BROKE: GGHV Cor 5.7 is UNPROVEN

DONE (Aug 21). Cor 5.7 was the ONLY thing killing the (9,27) branch of
(72,108) anywhere in the literature. Re-derived by hand against the local
extractions: the proof of (5.12) applies [1, Cor 7.2], whose standing
hypothesis is [P,Q] in K^x (as is [1, Def 4.3]'s), to the pair
(psi phi P, psi phi Q) — whose bracket, by the paper's own chain rule
[1, Prop 3.10], is 1/2 + (lambda/2)x^{-1/2}, NOT in K^x, with lambda != 0
forced by (0,18) in N(P). The first half of the proof is valid precisely
because [psi P, psi Q] = 1/2. (5.12) is load-bearing: Thm 5.1's hypothesis (2)
demands st_{-1,1}(P) = (6,18), but on Prop 4.1's polygon v_{-1,1} = b-a is
maximal at (0,18). Of the 66 coefficient conditions (5.12) asserts, the proven
claim delivers 15. Everything else in the chain re-checked and stands. Full
write-up in CATCHES.md.

CONSEQUENCE — this changes the plan: the live region below max 125 is now
BOTH orientations of (72,108). The p108_* systems (the (9,27) branch, the
smallest of which is p108_525122: 25 params, 140 conditions) are promoted to
first-class compute targets alongside P1's ladder cells. Two lanes are open on
them: (a) decide them exactly with the time-boxed elimination machinery, or
(b) attempt to REPAIR Cor 5.7 — and if no repair exists, hunt for a solution
of the (9,27) polygon system directly, since nothing in print excludes it.

## P4 — The frontier (where a CE must live if B=16 closes)

GGV prove B = 16 **or B > 20**. If the ladder is rigid, a counterexample has
degrees that are multiples of some B >= 21, hence above 125 — territory
GGHV's elimination does not reach. Test whether the tail set SATURATES
(the (last-2-segments, shape-index) -> system-hash predictor has zero
violations across every system this campaign ever generated). If tails
saturate, the 429-case frontier collapses to finitely many systems and
becomes attackable. This is the long game and the best home for new results.

## Infrastructure (must fix first, or P0/P1 cannot run)

This container: ~13.3GiB cgroup cap and restarts every ~30 minutes; it rolled
the git tree back twice overnight. Nothing needing >20 minutes or >12GB can
finish here. Options: a cloud worker with more RAM, a persistent machine, or
splitting jobs below the memory ceiling. **P0 and P1 are blocked on this.**

## Standing rules (earned the hard way, all in CATCHES.md)

1. Numerical multi-start is BLIND at >= 25 unknowns (planted-root controls
   failed). A hit would be real; a miss is NOT evidence of emptiness.
2. msolve writes "[-1]" and exits 0 on a parse error. ALWAYS read stderr.
3. Timeout / OOM / no-output are FAILURES, never verdicts.
4. Every method needs a positive AND a negative control before its output
   counts. Mod-p emptiness needs two agreeing primes.
5. Push after every commit — the tree rolls back.

## What Monday's audit should check

* Are the P0 verdicts (if any) backed by two primes AND clean stderr?
* Is every undecided cell still labelled undecided, with no drift toward
  "probably empty" in the prose?
* Do the two retractions (numerical floors; the fast "d=8 EMPTY") remain
  prominently recorded rather than quietly dropped?
* Does any claimed rank result reproduce from wave6/w6_rankcrit_modp.py with
  its d=3 and d=12 controls passing?
