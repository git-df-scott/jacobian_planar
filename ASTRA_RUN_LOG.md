# ASTRA run log — 2026-09-04

All verdicts use the repository's binding evidence labels.
Entries through Phase D describe the first Astra run; Phase E supersedes its
case-(2) UNKNOWN verdict and Singular availability statement. Phase F closes
the pentagon that Phase E left open.

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

## Phase E — Astra 2, exact case-(2) descent

- Started from `93319412545e84d1093d79c5b59cb87731eec4a9` on a separate
  branch, `astra/jc2-exact-descent-2026-09-04`.
- Reconstructed the complete one-variable grading directly from GGHV
  Proposition 4.3(2), including the absent T term in F.
- Provisioned SymPy 1.14, python-flint 0.9.0 and Singular 4.3.1 locally.
  System apt setup failed; locally unpacked official Debian binaries worked.
- Replayed all five positive Poisson witnesses successfully.
- Leading modular reconstruction over Q produced an irreducible quintic in
  the `C_1=C_2=1` chart. A separate exact checker verifies all five solutions.
- Proved completeness using the degree-21 Belyi passport
  `(3^7; 2^10,1; 17,1^4)`, whose dessins reduce to the five rooted plane full
  binary trees with three internal vertices. Checked permutations,
  connectedness, genus, passports and inequivalence independently.
- Derived the complete two-parameter solution of level (4). Solved (3) with
  exact matrix rank six and verified its full parametrization independently.
- Regenerated the 25 remaining lower equations and produced 26 multipliers
  certifying 1 after imposing `z*A_8-1`. FLINT exact replay and altered-
  certificate controls pass. Label: `EXACT-Q` with the written completeness
  proof in `ASTRA_2_CASE2_EXACT_DESCENT.md`.
- Direct leading GB attempts and an auxiliary chart certificate lift timed
  out; an initial coefficient-parser run failed. Their logs are retained and
  not used as evidence. The successful modStd log's completeness wording is
  superseded by the explicit dessin proof, not accepted on its own.
- The historical 1144 object is not asserted to coincide with this scheme.
  The neighboring pentagon and above-125 translation wall remain open.
- Final result: no CE or CEC; exact exclusion of this one reduced polygon.

## Phase F — pentagon geometry and the projective boundary

- Started from `e479477263c1f4176b287309dda2dcb4213fcb84` on
  `astra/jc2-pentagon-geometry-2026-09-04`. Read the historical pentagon
  retractions and the p_1_1=0 slice status before constructing the new system.
- Reconstructed every nonconstant lattice monomial of Proposition 4.3(1):
  60 for P and 124 for Q. Independently checked the convex hulls and the
  original x,y monomial determinant identity. Replayed the inherited exact
  leading-completeness data and case-(2) certificate successfully.
- Derived the right-edge square/cube relation and exhibited the one residual
  torus action that normalizes its parameter. Retained every linear kernel;
  seven unnormalized parameters become five, with weights (1,2,3,3,4).
- Computed exact coefficient-operator ranks through r=-13. Proved directly
  that the homogeneous lower operators are injective from r=-3 onward.
- The initial seven-parameter modular elimination timed out. Right-edge
  normalization gave an affine modular contradiction, but this alone was
  kept as finite-field reconnaissance.
- Three direct characteristic-zero eliminations timed out. PARI/GP suggested
  a smaller quintic field and an integral scale; FLINT verified the field
  isomorphism, scale and leading equation exactly. Nine raw exact
  compatibility equations were independently reconstructed with
  `verify_pentagon_descent.py --constraints-only`; no direct exact unit
  certificate was obtained or claimed.
- Restored the right-edge parameter t and reconstructed the single weighted
  homogeneous system through weight 8. Generated explicit certificates at
  p=32003: nine affine equations generate 1; fourteen boundary equations
  contain u1^9, u2^5, u3^3, u4^2 and u5^3.
- `verify_pentagon_projective.py` multiplies all six identities with separate
  sparse arithmetic, matches both charts to the same homogeneous system,
  checks support windows, weights and modular matrix ranks, and verifies
  entry by entry the good reduction of all exact field operators. All four
  reported verification groups pass, including altered-certificate controls.
- The written valuation argument turns emptiness of the projective special
  fibre into characteristic-zero emptiness. Together with Astra 2's five-orbit
  completeness proof this excludes every Proposition 4.3(1) leading branch.
- Large generated scripts from failed exact eliminations are losslessly
  compressed. Inputs, partial outputs, parser failures, successful certificates
  and classifications are preserved in `astra/artifacts/pentagon_run_manifest.json`.
- Result: no CE or CEC. Computer-assisted characteristic-zero exclusion of
  Proposition 4.3(1); together with Astra 2, both proposition polygons and the
  original case called (8,28) there are closed. No claim about JC2 as a whole,
  the different above-125 (3,4) chain, literature priority or external review.

## Closing record — Claude, earlier Codex/Sol and Astra

- Fetched and pinned all 44 remote branches and all 26 PRs at the cutoff.
  Retrieved their four discussion entries. Built a complete index of 1,287
  reachable commits and 35,078 branch/file occurrences, deduplicated to
  10,062 path/blob records; 581 distinct report versions are linked directly.
- Compared the earlier local checkouts with remote history. Recovered two
  unpublished Codex commits, 5a0592b and b07d9e9, containing twelve night25/26
  files. Preserved the original bytes, commit patches and Git bundle. The
  total commit catalog therefore contains 1,289 records. Another older
  checkout's 89 existing changed-file contents were already in remote history.
- Found a direct obstruction to night26's proposed GO model: faithfulness and
  polynomiality of Q=r^3 imply r is polynomial by integral closure, so its
  Jacobian has the nonconstant factor r^2. Recorded the complete written proof
  in RECORD_CORRECTIONS.md without altering the recovered historical files.
- Wrote JC2_COMPLETE_RECORD.md, the full PR archive, report index, commit
  chronology, frozen metadata and reproducible inventory builder. Git commit
  objects were checked against their SHA-1 IDs, every branch tree was fully
  enumerated, and original recovered file bytes were checked by SHA-256.
- This was a closeout and reconciliation, not a new full solver campaign or
  a claim that every historical computation was independently replayed.
