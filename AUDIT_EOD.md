# End-of-day clean audit — every t crossed, every i dotted

State as of this audit; branch holds 26 unpushed commits (push = dead
container credentials, parked by user; content safe locally).

## 1. PROVED / decided at strongest standard

| item | standard |
|---|---|
| B=16 d=2,3,4 | reproduces GGV (char-0 basis) |
| B=16 d=5, d=6 (both = full cells) | **char-0 Groebner proof** + 3 primes |
| B=16 d=7 sound Z/N split | mod p=1000003 (chart Z instant, N 15.7min) |
| B=16 d=8..12 chart Z (mu2=0 side) | mod p, 2 primes at d=8/12, 1 prime d=9,10,11 |
| d=12 resonant seed -1/12, chart Z (mu0!=0) | EMPTY, 2 primes |
| d=12 seed 1/20 chart Z; d=3 seed 1/12 both charts | EMPTY, 2 primes |
| Virgin cases (126),(140): 6 shapes | EMPTY w/ nondegeneracy, **2 primes** |
| Orphan family F3(3,2): 2 shapes | EMPTY (p=65521, single prime) |
| mu2=0 ladder d=2..12 | closed end to end |
| Resonance law (only d=3k^2 can degenerate; d=12 level 36 unique) | verified d=3..14 + control retrodicts GGV family |

## 2. RUNNING now

| job | state |
|---|---|
| **TWIN: d=12 resonant chart N (seed -1/12, mu2!=0) @p=1000033** | 34min, 4.3GB, deg-6 round; THE verdict of the night; protected |
| bridge w6_35657_1 (max=135 shape) @600s | 5.5min in |
| orphan-family sweep (F17/F1/F22-j...) | grinding |
| main virgin sweep (144-group, w6_6587_5) | grinding |
| (72,108)-sliver run (p108 shapes) | first shape extracting |

## 3. UNDECIDED (no verdict exists, must not be quoted as EMPTY)

| item | why | plan |
|---|---|---|
| d=12 resonant chart N | twin running; original OOM-killed at 83min | twin verdict, then solo re-run @p1 |
| d=12 unsaturated (degenerate family?) | OOM-killed at 65min; d=3 analogue answers instantly -- strongest anomaly | solo re-run tonight |
| d=7 chart A confirm primes (p33/p39) | runs killed in restarts | solo re-runs (80min each) |
| 33 virgin TIMEOUT shapes | facstd+msolve both stall at short budgets | overnight long-budget queue |
| pentagon L18 (case (1)) | needs >40GB monolithic; 2-torus found | block-cascade build |
| d>=9 charts N (incl. d=27 next resonant cell) | never run | overnight queue after twin |
| F22 13 live shapes | j-instance resolution needed (matcher found 0 cands) | small build |
| (8,28) 4 shapes at max=144 | TIMEOUT both engines | overnight queue |

## 4. OPEN MATH (no computation exists)

1. 429 frontier cases (150,300]: need chain-compiler extension (library stops ~150).
2. 3 twist-blocked cases (c_t non-integer): territory or closure theorem, unclassified.
3. (10,40) case: [5] assumed A'_t=(1,0) unprinted -- re-derive.
4. (72,108) case-split completeness vs the orphaned max=108 shapes (sliver run will
   partially answer; the classification proof remains).
5. GGV conjecture symbolic (uniform-d): closed forms in hand, proof unattempted.
6. B>=17: no reduction machinery exists anywhere.
7. VR-2025 / 1406.0886 small cells: iff-reformulation, unswept.
8. Nguyen 104: trusted refereed, never re-derived here.

## 5. PROCESS risks (twice-paid, now enforced)

- One-heavy-at-a-time is policy but not yet mechanism; scheduler unbuilt.
  Interim rule in force: nothing >2GB launches beside the twin.
- Push credentials dead on this container (user-parked; 26 commits local).
- p=65521 verdicts from the campaign extractor are single-prime unless
  bridged (virgin 6 done; orphan F3 pair not yet).

## 6. Triage recommendation (tonight)

T1. Twin finishes (protected) -> record; if EMPTY, launch solo re-run @p1.
T2. Solo re-run d12-unsaturated (the anomaly question).
T3. Overnight serial queue: d=7A confirms, d>=9 charts N, d=27-Z+seeds,
    33 TIMEOUT shapes at 1800s, (8,28) four, F22-j build+run.
T4. Morning: sliver-run classification writeup + compiler extension start.

## 7. Self-audit catches (post-audit)

- p108_821326 / p108_843700 are md5-identical systems: the (8,28)/11/4,7 and
  (8,32)/8,28/11/4,7 orphans reduce to ONE system; their EMPTYs are one
  verdict, not two.  ACTION: dedup-by-system-hash across all sweep registers
  (morning consolidation).
- The (9,27) sliver TIMEOUTs are re-labelled IDENTITY-UNRESOLVED: possibly a
  different reduction of the already-known case-(1)/(2) territory of (72,108)
  (37/25 params vs the campaign's 58/72) rather than new ground.  Verdicts
  still required either way; polygon-level comparison queued (T5).
