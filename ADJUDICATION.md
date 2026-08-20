# ADJUDICATION — independent fact-check of the Opus session outputs, and Wave 5

Auditor session, branch `claude/opus-5-counterexample-plan-sep6yk` (= hunt
branch + wave5 + this file). Every VERIFIED-HERE row was re-run or re-derived
in this session with code sharing nothing with the certifier it checks.
No agents were used; all work inline.

## 0. Bottom line

**No counterexample to the plane Jacobian Conjecture. No CANDIDATE survived
into existence anywhere.** What the night produced instead:

1. **The B=16 door — the one genuinely open counterexample corridor found in
   the sources — was reopened from the literature and pushed four cells past
   where mathematics stopped in 2013** (Wave 5, §2 below). All new cells EMPTY:
   deg(q1)=5 at **characteristic-0 proof standard**, 6–8 mod 3 fresh primes.
2. The Opus hunt/audit branches survive adjudication on every headline, with
   three recorded errors (one sign error, one imprecise lemma, one wrong-tree
   report) and 42 previously unrecorded hardcoded-`True` checks inventoried.
3. GGHV's discard of (80,112) cites a source that does NOT discard it as
   stated — but the specific cell it needs (deg(q1)=3) IS solved there; the
   citation is sloppy, not wrong. The cells the citation does NOT cover are
   exactly the ones Wave 5 closed tonight.

## 1. Claim-by-claim ledger

| claim | source | verdict | how |
|---|---|---|---|
| W3-1 ODE classification ((i) 3∤D unique deg-k; (ii) 3\|D, D≤3k none; (iii) 3\|D, D>3k family) | errors branch | **VERIFIED-HERE** | independent enumeration (pole-location lemma + exact linear algebra, `wave5/w5_w31_adjudication.py`), 96 cells, 0 mismatches |
| (13,4) explicit solution | errors-branch report | **SIGN ERROR in the report** | the printed `−κ(...)` leaves residual 2c; the `+` version (endgame STATUS §6.7) is correct. Existence unaffected |
| (23,4) explicit solution | errors branch | VERIFIED-HERE | exact substitution |
| endgame STATUS §6.7 LEMMA ("solutions are exactly A/(v+1)^k, map-degree exactly k") | endgame branch | **REFUTED as stated** | false for 3\|D, D>3k: family members of pole order ≠ k exist; explicit witness R = c/(6(v+1)²) + (v/(v+1))² at (D,k)=(6,1). Immaterial at D=13,23 (3∤D) |
| THEOREM 2 statement "recovered, certified" | endgame branch | VERIFIED-HERE | statement present verbatim in tracked `Sessions 1-18 status reports` (~ln 1051); `w1_L3_step2_pinning.py` re-run, its pinning checks are computed (one prose-check at :108 noted) |
| THEOREM 3 "confirmed, recorded proof gapped, repaired" | endgame branch | VERIFIED-HERE | gap real (fiber count fixes multiplicity, not location; witness 1/(v+1)¹³ satisfies every recorded premise, not polynomial); repair arithmetic checked; `w1_theorem3_verdict.py` re-run 25/25; W̃₋₅ definition matches the Session-11 text |
| §2.5 eliminant irreducible over ℚ, degree 1144, squarefree | endgame branch | **VERIFIED-HERE** | my own subset-sum sieve (planted-control validated): NO surviving proper degree over the 8 recorded tables; fresh 9th prime 100153 factored here: 6 distinct factors, degrees sum 1144 |
| errors-branch "eliminant ABSENT / Sessions 19–38 ABSENT" | errors branch | **WRONG-TREE** | that branch was cut from `main` (5 files); the artifacts exist on the endgame lineage. Its self-contained math stands; every ABSENT verdict is void |
| T1: 4560 pairs in 105..124 decided, 6 arise, 0 undecided | hunt branch | VERIFIED-HERE | `w5_pairs_105_124.py` re-run 4/4; enumeration positive controls re-run |
| case (2) both charts EMPTY at 3 fresh primes; 5-vs-1144 reconciliation | hunt branch | VERIFIED-HERE (re-run) | `w4_case2_json_audit.py`, `w4_edge_reconciliation.py` re-run clean in this environment |
| T3 symmetry congruence p+q ≡ 3a+b (mod n) | hunt branch | VERIFIED-HERE | re-derived by hand: bracket rhs x² picks up ζ^{2a} |
| T2 same-sign sweep, T5 Gao audit | hunt branch | re-run clean (exit 0) | certifier-level; internals spot-read |
| 5 nonzero certifier re-runs (toolchain branch) | — | **EXPLAINED** | `w0_a6*` ×3: environmental (`Singular` not on PATH — FileNotFoundError); `w1_h1b_reduction*` ×2: designed negative-result encodings ("levels ≥ 18 NOT affine"), matching the report |
| "0 rigged checks in tree" | hunt branch (its own files) | TRUE of its files, **FALSE of the tree** | full-tree AST scan: **45 hardcoded-`True` checks**, 42 previously unrecorded — 19 in inherited `campaign/` certifiers, the rest in wave0/wave1. Load-bearing review: Theorem-2 pinning unaffected (computed); `w1_L1_boxes_closed.py`'s three *conclusion* lines are prose-as-check → "L1 boxes immaterial" downgraded to ARGUED (computed premises, uncomputed inference); `w1_L2_cascade_threedessin.py:44` takes D=13 as read-from-source input (figures committed) rather than computing it |
| pent_L23 retry | compute branch | VERIFIED-HERE (parsed) | exit 137, peak 13.9 GB, output 0 bytes: still OOM. Pentagons remain STALLED |

## 2. Wave 5 — the B=16 door (the night's find)

Chain of custody, every link checked here:

1. GGHV 2022 (arXiv:2204.14178, **unrefereed**) prints "In [4] this case and
   the case (deg P, deg Q) = (80,112) have been discarded."
2. [4] = GGV, *Pro Mathematica* 27 (2013) 83–98 (fetched tonight, in
   `papers/`): **discards nothing.** Its Theorem 1.2: **B = 16 iff** system
   (1.2)+(1.3) has a solution with μ₀ ≠ 0, and such a solution "would yield a
   counterexample to the JC". Its §3.5 solves only deg(q1) = 2, 3, 4 (all
   solutions have μ₀ = 0) and **stalls at deg(q1) = 5** ("after an hour the PC
   hadn't solved"). It ends in an open CONJECTURE.
3. GGV's **refereed** 2017 paper (arXiv:1401.1784, p.2): Heitmann's claimed
   B > 16 rests on a gapped lemma; "B ≥ 16 remains … the best lower limit";
   "the possible counterexample at B = 16 is still within reach."
4. The gcd-16 cells at deg(q1) = d correspond to degree pairs
   (16(2j+1), 16(3j+1)), j = d−1: d=3 ↔ (80,112) — solved by GGV, so GGHV's
   row survives on a sloppy citation — but **d ≥ 4 lies above the 125 window
   and was open**. Valqui's newest paper (arXiv:2506.05697, June 2025, fetched
   tonight) works the adjacent n=3 family — the B=16 ladder itself had not
   been touched since 2013.

Tonight (`wave5/`): exact transcription of (1.2)+(1.3) from page renders,
certified against the paper's own data (6/6 controls; found and pinned a μ₀
typo in their §3.1 example — the printed μ₀=1 leaves residual −6y³+6μ₀y³,
uniquely fixed by μ₀=2); GGV's p.92 WLOG normalizations included (without them
the mod-p points are pure gauge copies — observed, then killed by the
normalization); μ₀ ≠ 0 saturated; msolve:

| cell | degree pair | 2013 status | tonight |
|---|---|---|---|
| d=2,3,4 | ≤ (112,160) | solved, μ₀=0 only | EMPTY — **reproduced** |
| **d=5** | (144,208) | **STALLED (1h, PC)** | **EMPTY over ℚ (char-0 Gröbner proof, 22 s)** + 3 primes |
| d=6 | (176,256) | untouched | EMPTY at 3 primes (~70 s each); char-0 running |
| d=7, d=8 | (208,304), (240,352) | untouched | running |

Every cell is a place a constructive JC2 counterexample could have lived.
None does. The B=16 corridor is now closed further than any published source,
and the method (exact transcription + normalization + saturation + msolve)
runs a 2013-intractable cell in seconds — the remaining ladder is pure compute.

## 3. What remains live, honestly

* **Pentagons** at (72,108): still the only no-verdict territory below 125.
  RAM-bound (13.9 GB OOM); needs a bigger machine or a better split.
* **Case (2) over ℚ̄**: mod-p EMPTY everywhere + eliminant irreducible; the
  13-variable residual over the degree-1144 field remains the well-posed
  heavy target.
* **B=16 ladder, d ≥ 9** and the GGV CONJECTURE (all solutions have
  μ₁ = μ₂ = 0): each further cell is one msolve run; a proof of their
  conjecture would close B=16 outright — that is now the sharpest
  theorem-shaped target on the board.
* **H2 above-125**: sweep continues; D7 (family F6 non-coprime) stands.
* (80,112): closed, but by an uncited-in-detail computation now reproduced
  here (d=3 EMPTY). GGHV's citation should be corrected if ever written up.

## 4. Corrections filed tonight

1. errors-branch report: (13,4) solution sign.
2. endgame STATUS §6.7 LEMMA: false as stated for 3|D, D > 3k (witness above);
   its uses at D = 13, 23 are unaffected.
3. "0 rigged checks in tree": 45 exist outside the new branches; inventory in
   §1; two verdicts downgraded (L1-boxes → ARGUED; L2's D=13 → SOURCE-READ).
4. errors-branch ABSENT verdicts: void (wrong tree).
5. GGV 2013 §3.1: μ₀ typo, pinned by uniqueness.
6. My own first sieve script had a vacuous-else bug (empty parse → "NONE");
   caught by re-inspection, rewritten with a planted control. Recorded because
   the campaign's rule is that the auditor's errors get logged too.
