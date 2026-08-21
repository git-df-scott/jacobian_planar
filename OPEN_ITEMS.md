# The open ladder items, re-audited after the 2026-08-21 correction

Status of each item asked about, checked against the repo rather than recalled.
The governing fact: GGV's (1.2) was found misprinted today, so EVERY artefact
built on the printed system is void as a statement about B = 16.  That voids
more of this list than it leaves standing.

## 1. d = 8 chart N "exported but never launched"
WHAT HAPPENED: exported 16:17 today as `wave5/ms/b16_d8_*.ms` -- on the PRINTED
system.  VOID.
NOW: re-exported on the corrected system as `wave5/ms/m16_d8_*.ms`, and smaller:
**30 equations / 23 unknowns** (was 39/30).  Two further simplifications apply:
`a_16` (= a_{2d}) is left FREE in the header, so msolve covers BOTH roots of the
row-0 quadratic in a single run -- no seed split; and F2 (mu0 = a2*mu2/3) proves
chart Z (mu2 = 0) contains no counterexample, so chart N is the only chart and
the mu2 = 1 gauge IS chart N.
STATUS: ready, not yet run.  This is the frontier cell: d <= 7 are now EMPTY in
characteristic zero.

## 2. d = 12 chart N "has TWO rational seeds, -1/12 and 1/20"
VERIFIED CORRECT: at d = 12 the row-0 quadratic 90a^2 + 3a - 3/8 has roots
exactly **-1/12 and 1/20**, and 12d = 144 = 12^2, so d = 12 is a resonant cell.
BUT THE ITEM IS SUPERSEDED: on the corrected export a_{2d} is not seeded at all,
so both roots are covered by one run.  The "two seeds together are the complete
chart N" bookkeeping is no longer needed, and neither is the Z/N chart split.
STATUS: not exported at d = 12 yet; trivial to produce, hard to run (see plan).

## 3. d = 12 unsaturated "genuinely undecided after two kills"
Those kills were on the printed system.  VOID.  Note the better formulation found
today: the UNSATURATED corrected system (mu0 free, mu2 gauged to 1) came back
EMPTY at d = 3,4,5,6 -- i.e. there is no solution with mu2 != 0 at all, which is
strictly stronger than "no solution with mu0 != 0".  d = 12 has not been
attempted in that form.  STATUS: OPEN.

## 4. d = 27 "untouched"
STILL TRUE.  Verified resonant: 12*27 = 324 = 18^2, roots -1/20 and 1/28, both
rational.  Size in the corrected form: 114 equations / 85 unknowns.
STATUS: OPEN, and out of reach of direct Groebner (see plan).  Note that the
rank criterion, which was the campaign's cheap probe for exactly these resonant
cells, was shown TODAY to be a can't-fail certifier -- it cannot decide d = 27
or anything else.

## 5. "The case-(2) over Q route was identified but never executed"
CORRECTION -- case (2) IS DECIDED, and not just identified.
`campaign/audit_tracks/CASE2_VERDICT.md`: "case (2) admits no realization with
its stated Newton polygons.  Complete and certified at three independent
primes -- 65521, 32003, 65537 -- covering every point of the edge variety at
each."  What was never executed is the CHARACTERISTIC-0 confirmation.
WHY THAT MATTERS MORE THAN IT DID: today we proved modular emptiness is unsound
for contradictions.  Three agreeing primes is strong evidence, not a proof, and
case (2) is one of only two shapes of the sole surviving degree pair below 125.
STATUS: decided mod p at three primes; char-0 route OPEN and now higher value.

## 6. Above 125: "429 cases requiring a chain-compiler extension"
STILL OPEN, and its importance went UP today: the dimension-3 refutation
(Alpoge/Gallagher, July 2026) realizes every geometric degree, which kills
degree-bound approaches to JC in general.  If B > 20 the counterexample lives
here.  The blocker is the compiler, not the mathematics.  STATUS: OPEN, large.

## 7. 41 undecided timeout shapes, plus H2 / pentagon machinery
Pentagon case (1) advanced substantially today: the L = 2i-j grading verified,
the top level shown to be exactly 2fg' - 3f'g = w^2, the bottom edge COMPLETELY
classified (ungauged dim 1; chart c2=1 dim 0 with a degree-9 eliminant in char 0
and mod p; chart c2=0 EMPTY), and exactly ONE of the five F_p-rational seeds
admissible.  That seed survives every purely linear consequence.  The 41 timeout
shapes are untouched.  STATUS: pentagon in progress, 41 shapes OPEN.

## THE PLAN, in priority order

P1  RUN d = 8 mod p NOW (30 eq / 23 unk, ready).  It is the frontier cell and the
    cheapest genuinely new result available.  Char 0 after, if mod p is clean.
P2  BUILD THE RATIONAL-FUNCTION CASCADE PROPERLY.  This is the single blocker
    shared by almost everything else.  Direct Groebner scales ~32x per ladder
    level (d=6: 42 s, d=7: 1345 s), so d >= 8 in char 0 and d = 12, 27 are out of
    reach by that route; and the pentagon needs the same machinery to propagate
    past level 3 through its two free parameters.  Both retracted cascades failed
    on exactly this point.  It is the highest-leverage thing to build.
P3  d = 12 on the corrected system (both roots in one run, no chart split), then
    d = 27.  Feasible only after P2.
P4  CHARACTERISTIC-0 CONFIRMATION OF CASE (2).  Converts a three-prime modular
    result into a proof on one of the two shapes of the last surviving pair
    below 125.  Cheap relative to its value.
P5  Above-125 chain-compiler extension: 429 cases.  The long game, and where a
    B > 20 counterexample must live.
P6  The 41 timeout shapes, sorted by size first -- the frontier has never been
    swept smallest-first.
