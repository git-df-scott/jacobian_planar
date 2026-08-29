# FULL STATE — the complete re-walk (compaction-proof record)

Every thread of the campaign session, re-verified. New misses from this pass
are marked [MISS-n].

## A. B=16 ladder (GGV Thm 1.2 systems; primes 1 mod 3 unless noted)

| cell | status |
|---|---|
| d=2,3,4 | EMPTY, reproduces GGV (char-0 grade) |
| d=5, d=6 | EMPTY, char-0 Groebner PROOF + 3 primes |
| d=7 Z+N (sound split) | EMPTY @p=1000003 only. [MISS-1] confirm primes died in restarts, never re-run |
| d=8 Z | EMPTY, 2 primes. [MISS-2] **d=8 chart N was exported but NEVER LAUNCHED** |
| d=9,10,11 Z | EMPTY @p=1000033 single prime; charts N never run (known queue) |
| d=12 Z (both rational seeds) | EMPTY, 2 primes |
| d=12 N seed -1/12 | TWIN RUNNING @p=1000033 (~55min). Original @p=1000003 OOM-killed, needs solo re-run |
| d=12 N seed 1/20 | [MISS-3, now explicit] REQUIRED for the cell (two seeds = whole chart N, row0 factors rationally); never run; predicted fast (no in-range resonance) |
| d=12 unsaturated (degenerate family?) | UNDECIDED after 2 kills; the biggest anomaly (d=3 analogue is instant); solo slot queued |
| d=27 (next resonant cell, roots 1/28, -1/20) | untouched (queue) |
| GGV conjecture symbolic-d | closed forms + resonance law in hand; proof unattempted |

Resonance law: singular descent only at d=3k^2; d=3 k=6 retrodicts GGV's
family (control exact); d=12 k=36 unique in-range level (root -1/12 only).

## B. (72,108) — the live pair

- (8,28) orientation (campaign's side): pentagons NO VERDICT (>40GB monolithic
  measured; 2-torus found, block-cascade UNBUILT); case (2) EMPTY mod p both
  charts, eliminant deg-1144 irreducible/Q; **case (2) over Q-bar: linear
  residual over K route planned, NEVER EXECUTED** [MISS-4: absent from triage
  T1-T5 -- added to T3 queue].
- (9,27) orientation: killed in the literature ONLY by GGHV Cor 5.7 (Sec 5
  apparatus, never re-derived by anyone).  Our two p108 systems (verified =
  Prop 4.1 polygons, bracket -x, convention checked) are the FIRST independent
  test: shape 1 IN MSOLVE now (1800s), shape 2 queued.  Verdict standards
  pre-registered both directions (Sec 10 of AUDIT_EOD).

## C. Above-125

- Queue-coverage audit: 464 admissible in [125,300]; queue covered 20; virgin
  sweep decided 6 EMPTY (2-prime), 36 TIMEOUT (overnight long-budget queue).
- 429 cases need chain-compiler extension (library stops ~150) -- unbuilt.
- 3 twist-blocked + 1 A'_t-assumed case: unclassified.
- Legacy 180-target trackD queue: [MISS-5] disposition never decided -- it is
  semi-superseded by the coverage audit; DECISION RECORDED HERE: finish its
  remaining targets inside the overnight queue only after the virgin TIMEOUTs,
  since its 20-key coverage is a subset of what the audit mapped.
- Orphan reconciliation: 254/478 vertex-LIVE entries orphaned; F3 x2 EMPTY
  [MISS-6: single prime 65521, bridge to 2nd prime queued]; 5 TIMEOUT; 13 F22
  blocked on j-instance chain-map gap (small build queued).
- Duplicate-system finding: dedup-by-hash across registers pending (morning).

## D. Adjudications (all recorded in ADJUDICATION.md + AUDIT_EOD.md)

W3-1 verified (96 cells); Thm 2/3 recovery verified; Sec 6.7 lemma refuted as
stated; (13,4) sign error pinned; parallel-session claims labelled (OVERSTATED
/ two unsound steps); 45+22 cant-fail checks inventoried; GGV mu0-typo pinned;
chart gauge-fixing error caught+corrected (mine); concurrency kills x2 (mine,
enforcement scheduler unbuilt -- interim one-heavy rule + tripwire swap<8G).

## E. Un-built machines (ordered)

1. Overnight serial queue runner (T3): d8-N [MISS-2], d12-N-1/20 [MISS-3],
   d7 confirms [MISS-1], d9-11 N, d27 cells, 36+5 TIMEOUTs @1800s, (8,28)
   four, F22-j resolver, F3 2nd prime [MISS-6], sliver shape 2, d12-unsat solo,
   case-2 Q-bar ranks [MISS-4].
2. Pentagon block-cascade (grading-based).
3. Chain-compiler extension (429 cases).
4. VR-2025 / 1406.0886 small-cell sweeper (iff-reformulation).
5. Bridge dump-timeout fix (one line, fold into queue runner).

## F. Exposure ledger

- [MISS-7 / RISK] 37+ local commits UNPUSHED (container credential death;
  user-parked).  If this container dies, tonight's results exist only in
  chat logs and the stale API backup branch (early results only).  One
  working `git push` from any session with access, or the Connectors fix,
  clears it.  Flagged to user; their call.
- Twin + sliver share the box: swap tripwire 8G (currently ~22G free).
- Dead-man: task notifications cover both runs; watchdog logs every 3 min.

## G. What is genuinely still capable of producing a CE

1. Twin verdict (d=12 resonance) + the required 1/20-N completion.
2. Cor 5.7 test (both shapes) -- a non-empty here reopens (72,108)'s second
   branch.
3. The 41 undecided TIMEOUT shapes.
4. Pentagon (case 1) via the cascade build.
5. The 429-case frontier after compiler extension.
6. GGV-conjecture refutation at some d (= constructive CE).
7. VR-2025 iff-cells.
Everything else reachable is decided EMPTY.
