# Astra handoff — 2026-09-04, second run

Branch: `astra/jc2-exact-descent-2026-09-04`.
Base: `93319412545e84d1093d79c5b59cb87731eec4a9`.

No counterexample or counterexample candidate was found.

GGHV Proposition 4.3(2), the four-vertex reduced polygons with bracket x^2,
is now excluded in characteristic zero. This supersedes the previous
UNKNOWN verdict for that specific case. The proof uses a five-dessin upper
bound, five exact algebraic leading solutions, a complete lower
parametrization, and an independently verified 26-term contradiction identity.
It does not close the neighboring pentagon, the whole degree-(72,108) target,
or JC2.

Read `ASTRA_2_CASE2_EXACT_DESCENT.md` first, then `ASTRA_STATE.md` and
`GRADED_FRONTIER.md`. For prior work read `TARGET_SOURCE_COMPATIBILITY.md`,
`OFF_BY_ONE.md`, `GROUP_FIRST_SEARCH.md`, `BRIANCON_MATE_STRIKE.md`,
`ASTRA_RECONCILIATION.md`, and the chronological `ASTRA_RUN_LOG.md`.

## Replay the new result

With python-flint 0.9.0:

```
python astra/verify_case2_certificate.py
```

Expected: four PASS lines. This rebuilds the relevant equations, verifies the
leading quintic and five dessin representatives, checks matrix rank and lower
parametrization, and multiplies the explicit Nullstellensatz identity.
The universal level-four parametrization and exhaustive dessin reduction are
proved in the accompanying Markdown; they are not machine-formalized proofs.

To regenerate the certificate, with SymPy 1.14 and Singular 4.3.1:

```
python astra/build_case2_descent.py
Singular -q astra/case2_exact_descent_certificate.sing
python astra/verify_case2_certificate.py
```

The five inherited positive witnesses still pass via
`python astra/graded_control.py`. Prior controls remain in
`python astra/run_controls.py`; their archive audit reports historical scope.

## Next explicit target

Reconstruct the neighboring pentagon in Proposition 4.3(1). It adds `(0,8)`
to N(P) and `(0,12)` to N(Q), and permits negative grading levels. Derive the
complete equations and identify which present lemmas survive before running
any elimination. Do not reuse the five-level case-(2) equations unchanged.

Other live lanes remain the H3 boundary-depth theorem, a residue-free
Briancon construction, and repair of the published above-125 translation.
The previous six-blowup H3 exclusion is bounded; the Briancon period
obstructions retain their explicit geometry hypotheses.

## Evidence cautions

- The exact five/35 leading count is proved independently of the historical
  degree-1144 object. That object's full provenance is still unresolved.
- `modStd` was a discovery tool. The raw log's completeness wording is not
  the proof of enumeration completeness; the dessin count is.
- Failed and timed-out exploratory runs are classified in
  `astra/artifacts/case2_run_manifest.json`; they prove no emptiness.
- The final corner condition is A_8 != 0; Singular calls that variable B(8).
- No numerical near-hit or necessary-condition survivor is a CEC.
