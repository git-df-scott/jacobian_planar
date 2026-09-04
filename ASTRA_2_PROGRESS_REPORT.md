# Astra 2 — JC2 progress report

Date: 2026-09-04.
Repository: `git-df-scott/jacobian_planar`.
Branch: `astra/jc2-exact-descent-2026-09-04`.
Research package: [commit 1e05b08](https://github.com/git-df-scott/jacobian_planar/commit/1e05b08a6a9ade28949d7c0be74548c36e569b45).

## Bottom line

No genuine JC2 counterexample or counterexample candidate was found.

The session produced a computer-assisted exclusion of the four-vertex
reduced polygon case in GGHV Proposition 4.3(2). All five leading scaling
orbits are accounted for, and none extends to the required polynomial pair.
This advances that specific case from the inherited audited UNKNOWN status
to an exact proof package. It does not settle JC2 or the full original
degree-(72,108) target. No literature-priority claim is made.

The proof combines written mathematics with independently checked exact
algebra. It has not been formalized in a proof assistant or externally
peer-reviewed.

## What was completed

| Component | Result | Evidence |
|---|---|---|
| Published target | Reconstructed the complete supports and five graded bracket equations | Explicit derivation in the proof note |
| Leading solutions | Five distinct solutions in one irreducible quintic field | Exact FLINT substitution and irreducibility check |
| Leading completeness | At most five scaling orbits; all five are realized | Written Belyi/dessin argument; finite permutation enumeration checked |
| Normalizations | Five orbits in the C_1=C_2=1 chart; 35 points in C_1=C_8=1 | Seven scale choices per orbit; no C_2=0 orbit |
| Level-four descent | Complete two-parameter formula for B,F | Written proof and exact identity check |
| Level-three descent | Complete parametrization with A_7,A_8 free | Rank six and substitution verified independently |
| Final lower system | 25 equations, plus z*A_8-1 imposing the required corner | Independently regenerated equations |
| Contradiction | 26 explicit multipliers satisfy sum(q_i*p_i)=1 | Singular production; independent FLINT multiplication |
| Controls | All five inherited positive Poisson witnesses pass | Exact bracket checks |
| Reproduction | Certificate regenerated from the saved producer and rechecked | Successful replay log; verifier passes again for this report |

The central improvement is completeness: the modular solver was used to
discover exact algebraic candidates, not to justify that every branch was
found. The written counting argument reduces all admissible leading dessins
to the five rooted plane full binary trees with three internal vertices.
Five independently verified polynomial solutions meet that upper bound.

The reduced target has bracket `x^2`. It is a necessary-condition search
derived from JC2, not itself a constant-Jacobian counterexample. The final
contradiction excludes its required nonzero coefficient A_8.

## Checks repeated for this report

The GitHub branch was read directly and confirmed at `1e05b08` before adding
this report. Its working tree was clean. The independent verifier was rerun
and returned:

```
IRREDUCIBLE_QUINTIC_AND_FIVE_DESSINS: PASS
LEADING_IDENTITY_FLINT: PASS
LOWER_GENERATION_AND_RANK_FLINT: PASS
BOTTOM_NULLSTELLENSATZ_FLINT: PASS
```

This reporting turn did not launch a new counterexample search or rerun the
expensive leading elimination.

## Failed attempts and unresolved issues

- Four direct leading-basis attempts timed out. These are not emptiness
  evidence.
- An auxiliary C_2=0 chart returned a unit ideal, but its certificate lift
  timed out. The final proof does not require that auxiliary computation.
- One early generated script failed because of algebraic-coefficient parsing.
  The generator was corrected; the successful certificate was regenerated.
- The historical degree-1144 eliminant has not been identified with this
  saturated leading scheme. The present proof reconstructs its own inputs
  from the published polygon and does not use that eliminant.
- Raw exploratory log wording is not promoted into a proof: the old modular
  completeness label is superseded by the written counting argument, and
  timer values are not presented as wall-clock benchmarks.

Failed logs and their classifications remain in the repository for audit.

## What remains live

The next chosen target is the neighboring pentagon, GGHV Proposition 4.3(1).
It adds vertices `(0,8)` and `(0,12)` to the two polygons, allowing negative
grading levels. Its full bracket system must be reconstructed before using
any of the present descent formulas. No search of that larger system was
performed in this session.

The separate above-125 translation/provenance problem, H3 boundary-depth
question, and residue-free Briancon construction also remain open. Their
earlier results retain their original scopes.

## Repository entry points

- [Full proof](ASTRA_2_CASE2_EXACT_DESCENT.md)
- [Current state](ASTRA_STATE.md)
- [Next-session handoff](ASTRA_HANDOFF.md)
- [Chronological run log](ASTRA_RUN_LOG.md)
- [Graded frontier](GRADED_FRONTIER.md)
- [Independent verifier](astra/verify_case2_certificate.py)
- [Dessin enumeration](astra/case2_dessin_count.py)
- [Certificate generator](astra/build_case2_descent.py)
- [Verification output and hashes](astra/artifacts/case2_independent_verification.json)
- [Run classifications](astra/artifacts/case2_run_manifest.json)
- [Explicit contradiction multipliers](astra/artifacts/case2_exact_bottom_certificate.txt)

Quick replay from the repository root, with python-flint installed:

```
python astra/verify_case2_certificate.py
```

The original research commit already contains the proof, scripts, exact
artifacts, successful and failed logs, and updated campaign state. This report
is an additional checkpoint on the same research branch, not a merge to main.
