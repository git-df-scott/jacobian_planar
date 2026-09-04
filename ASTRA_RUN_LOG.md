# ASTRA run log — 2026-09-04

All verdicts use the repository's binding evidence labels.

## Routing and reconciliation

- Cloned `git-df-scott/jacobian_planar` and read `main/README.md` first.
- Audited PR #25, PR #24, PR #23, PR #22, then the canonical historical branch
  and only the provenance-relevant graded and mate branches.
- Pinned all heads in `ASTRA_RECONCILIATION.md`.
- Compared `STATUS.md`, `STATE_FULL.md`, `LIVE_MAP.md`, `OPEN_ITEMS.md`, and
  `CATCHES.md`.  The later `CATCHES.md` retractions control.
- Classified stale B=16 rows as void and case-(2) characteristic zero as
  `UNKNOWN`.

## Environment

```
Python 3.12.13
SymPy 1.14
NumPy 2.3.5
python-flint 0.9.0
```

GAP, Singular, msolve, and PARI/GP were absent.  An attempted package
provisioning step did not complete under the runtime's network restrictions and
was stopped.  No research verdict depends on it.

## Phase A — controls

1. Ran the graded branch's independent identity verifier and five witness
   producer/checks.  Result: every `{P,Q}=x^2` witness passed exactly over Q.
2. Added and ran `astra/graded_control.py`.  Result: grading identity and all
   five witnesses pass independently.  Label: `EXACT-Q`.
3. Ran the mate branch's `night23` producer and independent verifier.  Result:
   `g` and `gprime` have exact infinity valuations `(0,0,0)` and
   `PERIOD-NONZERO` under the stated genus theorem.
4. Ran the mate branch's `night24` producer and verifier.  Result: the
   cusp-preserving family is closed `EXACT-ALL-DEGREES` under its declared
   support hypotheses.
5. Added `astra/briancon_control.py`.  Exact Groebner bases of both gradient
   ideals are `[1]`; chart, cleared-fibre, and boundary identities pass.
6. Replayed the archived source generator alone: 11,465 records through six
   blowups.  The old all-choice analysis was not used as a new result.
7. Replayed the PR #24 abstract pre-screen: 5,261 rows.  A compact ASTRA replay
   reports 635 basic signatures.  Label: `ADMISSIBLE-SHAPE` only.

## Phase B — target/source compatibility

- Derived the generic bridge `r_E=1-k_E`,
  `c_i=sum d_E`, `e_i=sum d_E(1-k_E)`, and coordinate degree products.
- Derived the adjunction bridge
  `chi(P fibre)=sum(k_E-1)dP_E`.  Escape components give the target subtraction,
  forcing a +D weighted contribution from all other coordinate-horizontal
  components.  H3 therefore has fixed +6 P and Q infinity budgets.
- Added a complete principal-kernel solver for `M m=d`, nonnegativity, and
  coordinate complementarity.
- Positive control: the resolved identity map is recovered with D=1 and zero
  Keller delta.
- Specialized to the H3 meridian data.  Search scope: all 11,465 archived tree
  records through six blowups, both tangential-degree partitions of the two
  moved cycles, no coordinate-degree or support-size cap.
- Results for both target bidegrees (3,5) and (3,6): 557 relevant records, 654
  escape placements, zero P-coordinate solutions, zero Q-coordinate
  solutions, zero joint survivors, zero skipped higher-dimensional kernels.
  Label: `EXACT-Q`, bounded.

## Off-by-one / group-first strike

- Added a direct S6 enumerator.  Its S3/A2 positive control passes.
- H3 result: 45 double transpositions; after fixing one generator, 16 labeled
  transitive triples; one centralizer orbit; generated order 60; local staying
  `(0,1,0)`; moved-orbit counts `(2,1,3)`; Euler 1; coarse chi(R)=0.
- This independently confirms the unique group-level near-miss and makes its
  one-unit escape deficit exact.

## Phase C — Briançon mate strike

- For `P_(a,b)=p^2u+aps+bs`, exact Gate 0 passes for the two published targets.
- The cleared fibre and all infinity valuations were reconstructed over Q.
- With the stated irreducible genus-one theorem, eta is a nonzero holomorphic
  differential and no rational or polynomial mate exists in any degree.
- The family boundary b=0 factors as `p(pu+as)`, leaving the all-irreducible
  class.  No Q was constructed.

## Phase D — graded frontier

- Verified the p=32003 orbit eliminant factorization independently: degrees
  `1+1+3`, two field roots 5934 and 14549, residual cubic irreducible.
- Verified hashes and `[1]` lines for all three lower-stage logs.  Verdict:
  `EMPTY-mod-p` for all five orbits at p=32003.
- p=1000003 supports only a checked rational-orbit kill; later pipeline factors
  have syntax errors.  Characteristic zero remains `UNKNOWN`.
- Checked the primary Section 6 table for the degree-144 `(8,28)->(7/4,3)`
  case.  Stopped before algebra because A'_t and the c' ladder are not yet
  independently reconstructed.  Label: provenance `WALL`.

## Reproduction

From the repository root:

```
python3 astra/run_controls.py
```

Expected final line: `ALL ASTRA CONTROLS: PASS`.

Current counterexample status: no CEC and no CE.
