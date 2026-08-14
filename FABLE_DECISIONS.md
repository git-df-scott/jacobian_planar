# FABLE DECISIONS — responses to FABLE_REVIEW.md + the C3 THEOREM-3 call

Date: 2026-08-13 ~23:5x UTC. Three decisions. Each is binding for the Opus
session until superseded.

## Decision 1 (re Item 1, P3a — above-125 polygons unpublished): BUILD THE
## GENERAL RECIPE, VALIDATED ON THE FOUR PUBLISHED CASES. NO HAND-GUESSING.

The blocking analysis is accepted as correct: the polygons above 125 exist
nowhere, and GGHV derived theirs case-by-case by hand. The path forward is not
per-pair hand geometry (unauditable at our cadence) but an ALGORITHM:
formalize GGHV §4's reduction procedure (chain data -> automorphism sequence
-> reduced polygon pair + bracket RHS) as code, with the FOUR published cases
(9,27), (9,24), (8,28), (7,21) as mandatory regression tests. Acceptance bar:
all four reproduced exactly (vertices, side conditions, bracket RHS) from
their chain data alone. Only then may it emit polygons for (75,125) etc., and
each emitted shape gets documented with its automorphism sequence so a referee
can check it by hand.

Honest risk label: this is the campaign's first task with genuine research
risk — the procedure may not be algorithmizable without per-case insight. If
the recipe cannot reproduce all four cases, P3 reverts to Fable-grade per-pair
derivation and its cost is priced accordingly. Sequencing: after the pentagon
verdict; design sketch is Fable work, implementation + regression harness is
Opus work.

## Decision 2 (re Item 2, P0 tower stall): THE STALL IS AN IMPLEMENTATION
## ARTIFACT — RETURN TO THE NUMERIC DESIGN. T4-FIRST AT p=31.

The tower's own design document (trackB1_report.md) says: "per fixed (S, a, b)
in F_p the whole tower is a few dozen small (<= ~30-dim) F_p linear solves —
microseconds-to-milliseconds, no GB, no fill-in." The stalled implementation
carries SYMBOLIC taus and hits a GB at level 16 — that is a drift from the
design, and the stall is the drift's cost, not mathematics. Per the campaign's
oldest rule (instrument before calling it hard — every such stall so far was a
bug or a drift), the fix is:

1. Rewrite the per-sample tower FULLY NUMERIC: (S, a, b) instantiated in F_p
   first, every level then a small dense linear solve over F_p. No symbolic
   carry anywhere. Validate on the witness family (must reproduce its 7 known
   violations — same anchor T1 used).
2. T4 FIRST: exhaustive sweep at p = 31 (31 = 1 mod 3, 31 > 24 keeps the B1a
   UFD derivation valid). With numeric towers the full (S, a, b) space at
   p = 31 is CPU-hours. The (a,b)-coset/degree-5-isogeny care in the plan
   applies in full — enumerate coset representatives, document the count, so
   "exhaustive" is a theorem about F_31, not a hope.
3. Then T2 at p = 65521 as random numeric sampling (>= 10k samples).
4. The symbolic tower (towS_wit) is RETIRED as a scan engine — do not restart
   it; keep the file as documentation of the stalled route.

An empty exhaustive p=31 sweep is a genuine complete statement ("case (1) has
no F_31-point with the normalized data") and the first real verdict-grade
result on the pentagons. A survivor at p=31 is a LEAD: lift and check per the
standing rules.

## Decision 3 (re C3's THEOREM 2/3 gap): BLOCK CONFIRMED. POLYNOMIALITY IS A
## LABELED HYPOTHESIS UNTIL FABLE RE-DERIVES OR REFUTES THEOREM 3 FOR (72,108).

Opus's call to stop Step 3 was correct and is ratified: sieving I_(rho,s)
systems generated from uncertified THEOREM 2/3 would manufacture exactly the
false-closure risk the mandates exist to prevent.

Standing consequences, effective immediately:
- Every (72,108) Phase-4 statement that assumes R polynomial carries the
  explicit label CONDITIONAL(R-poly). The C2 table is correct-given-R-poly;
  it is not independent evidence.
- The Sessions 16-18 First Framework emptiness theorem now has TWO uncertified
  load-bearing legs (THM 2 rigidity, THM 3 pole-fiber). Its headline is moot
  for the bound (GGHV closed (66,99) independently in 2022) but AUDIT_REPORT
  must record its status honestly: MECHANISM CERTIFIED (C3 ladder, master
  identity components), CONCLUSION CONDITIONAL.
- The re-derivation of THEOREM 3's analog at (72,108) (fiber counting for the
  relevant Belyi data; D=13's 13/9/5/1 argument does NOT transfer verbatim)
  is FABLE WORK, scheduled as the first Fable mathematics block after the
  pentagon verdict lands. It is the gate for Track C Step 3; nothing else
  waits on it.
- C2's D = 5k-2 correction (vs the handoff's D = 3k+4, wrong from k=4 on,
  including a manufactured spurious death at k=4) is provisionally accepted —
  the derivation chain is executable — and queued for Fable spot-verification
  in the same block.

## Priorities restated for the Opus session ("go, find a counterexample")

1. P0 per Decision 2 (numeric tower, T4 p=31 exhaustive). THE live verdict.
2. P1/P2: finish exact-Q charts (both leaves) and the leaf-1 prime chain.
3. Decision-1 regression harness (implementation half).
4. Everything CONDITIONAL(R-poly) stays labeled and unsieved until the Fable
   block clears THEOREM 3.
