# The whole-conjecture sweep — frameworks applied (Session 44)

Question asked: what did we miss, where haven't we looked, where do we go.
Each framework below names its finding and its action. Items marked DONE
were closed this session; items marked GO are the forward moves.

## O-rings — flaws we normalized because nothing broke yet

1. **Gauge µ3=1** (FOUND, closing now). Every trusted B=16 verdict covered
   only µ3 ≠ 0. The µ3=0 stratum batch is running; sol has T1b. DONE-ish.
2. **The superset tier bookkeeping** (FOUND). "Out of scope" chains fell
   between categories; 732 charts never swept. Now ranked: 77 loose charts
   total (vs the 23 previously known), Wave A Gröbner queue launched. GO.
3. **Two-prime EMPTY ≡ dead.** A char-0 point survives to F̄_p for all but
   finitely many primes, so double-prime GB=⟨1⟩ kills — *unless both our
   primes land in the finite bad set*. No reason they should; but every
   "closed" claim in the ledger is a mod-2-primes claim and the final
   writeup must say so. Standing residual risk, accepted, stated.
4. **rmax=8 and v11(A0) ≤ 35 caps.** The superset enumeration stops at
   r=8 (our choice); the paper's ≤150 catalog was generated with
   v11 ≤ 35 (their choice). If the paper's cap is a computational cutoff
   rather than a proven bound, the "complete ≤150" claim has a hole and
   fatter-polygon shapes ≤150 could exist unexamined. CHECK the paper
   (arXiv:1708.07936 Sec. 6) — GO, cheap and decisive.
5. **F18–F21 exclusion.** The paper says "we claim that F18–F21 can not
   be obtained from a standard (m,n)-pair" — the word is *claim*. Four
   families at max ≤ 150 excluded on a sentence. Our generator already
   builds them (`include_excluded=True`). Verify the paper's argument; if
   thin, sweep them with our own instruments. GO — this is also the top
   Blue-LED candidate (the abandoned material nobody else will touch).

## Blue LED / Penicillin — the discard pile

- **F24 is the field's own anomaly**: flagged OPEN by the paper at
  max=128, and our fresh ranking shows it carries the LARGEST residual
  freedom in the entire catalog (charts at dim 88, 85, 79 — nothing else
  is above 73). The one shape the paper could not close is the one with
  the most room. Wave A starts with its params-50 dim-2 chart; the
  dim-88 charts go to the walker. GO — this is the primary hunting
  ground now.
- **F18–F21** (above).
- **The Abel-equation view** of B=16 was abandoned with the transcription
  bug — but only the transcription was wrong, not the view. The paper's
  eq. (3.5) is an Abel ODE with polynomial-solution constraints; there is
  an entire literature (moment problems, composition conditions,
  Briskin–Françoise–Yomdin school) on exactly this question that the
  campaign has never consulted. µ-rigidity might BE a known theorem, or
  a known open problem with partial results that settle our j ladder.
  GO — literature check (AlphaFold move: someone else's field may have
  already solved our subproblem).

## Kepler — drop the aesthetic assumption

The campaign hunts at MINIMAL degree/B because floors give structure —
but minimal = maximally constrained = where everything dies. The places
with actual freedom in the data: F24's dim-88 charts, the dim-69 class,
the (11,33)/(12,36) superset families. Hunt where it is loose, kill where
it is tight. Also: the family growth law means above-150 instances of
each F-family may reuse the SAME local systems (F17's charts share
(a,b,c',r) with five other chains already); if the reduced system is
j-stable along a family, one verdict closes an infinite ladder. CHECK
j-stability on F1 instances (j=3 vs 5 vs 7). GO — could collapse
"above 150" from infinite to finite.

## PageRank — structure of the link graph, not the pages

Fingerprinting all 866 charts: only 638 distinct (NP, NQ, r) systems, and
the interesting classes are SHARED: the dim-3 obstruction system serves
SIX published shapes (F17, (12,33), (9,27)-, (9,36)-, both (12,36)-
chains); its c'=9 sibling at dim 69 serves five. One Gröbner kill or one
walker witness propagates across every shape in the class. All queue
files are now deduplicated by fingerprint priority. DONE (instrument),
ongoing (verdicts).

## Einstein's elevator — change the frame

Two reframes not yet exploited:
- **Jelonek non-properness**: a plane Keller CE has a non-properness
  curve A(F) with strong known constraints; combining those with the
  B ≥ 16 degree data is a structural pincer nobody here has run. PARKED
  (heavy; needs literature first).
- **µ-rigidity as the theorem**: we treat µ1=µ2=0 rigidity as the enemy
  (it kills B=16 levels). Flip: if rigidity is provable uniformly in j,
  B=16 closes FOREVER and the technique likely climbs to B=17+. The
  F-system derivation is exactly the setup such a proof needs. The crack
  test (sol T1/T1b) decides which frame is true at deg 8: a NONEMPTY is
  a CE door; an EMPTY is evidence for the rigidity theorem. Either
  outcome is progress — this is why T1 is the most valuable computation
  in flight.

## Where we go, in order

1. Wave A Gröbner (39 tractable loose charts, F24 first) — RUNNING.
2. Walker on F24's dim-88/85/79 charts + the dim-69 class — NEXT SLOT.
3. Paper checks: v11 ≤ 35 provenance; F18–F21 exclusion argument.
4. Abel/moment literature on µ-rigidity.
5. j-stability of family local systems (above-150 collapse).
6. µ3=0 batch + sol T1/T1b verdicts as they land.
