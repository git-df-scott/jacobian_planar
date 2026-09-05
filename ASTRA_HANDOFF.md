# Astra handoff — 2026-09-04, third run

**Current Astra 10 update:** [Search outside the collision algebra](ASTRA_10_OUTSIDE_COLLISION_SEARCH.md) found no counterexample. Read
`astra10/PROOFS.md` before attempting higher Briançon exponents, a single
pair of higher-order poles, or the newly constructed exact degree-six
elliptic twist. The first two stated families are excluded in arbitrary
degree, and the twist is excluded in every faithful polynomial chart by
mixed-power rigidity. Nine exact checks pass. Other embeddings and the
general two-point collision problem remain unresolved.

**Current September 5 update:** [Astra 9](ASTRA_9_FULL_COLLISION_ROUTE_CLOSURE.md)
proves FULL COLLISION-ROUTE CLOSURE for C[b,c]+Delta*C[v,c] in arbitrary
degree. The degree-15 resonance and every higher-degree potential in this
algebra are excluded by parity, the slope-one Newton-edge residue obstruction,
and a final factor c in the Jacobian. Use ASTRA_STATE.md for current routing;
the older run-specific handoff below is historical.

**Closeout update:** the complete historical record and recovered nights 25–26
are on `astra/jc2-complete-record-2026-09-04`. Start with
`JC2_COMPLETE_RECORD.md` and `RECORD_CORRECTIONS.md`; the latter excludes the
recovered night26 `R=r^3` model by integral closure and the Jacobian product
rule. The branch/base below identify the completed third research run.

Branch: `astra/jc2-pentagon-geometry-2026-09-04`.
Base: `e479477263c1f4176b287309dda2dcb4213fcb84`.

No counterexample or counterexample candidate was found.

Both polygons of GGHV Proposition 4.3 are now excluded in characteristic
zero by computer-assisted arguments. Astra 2 closed the quadrilateral;
Astra 3 closes the pentagon with a complete five-parameter reduction and
explicit certificates on both charts of a weighted projective model.
Verified good reduction and a written valuation argument supply the bridge
from the finite-field identities to characteristic zero. This excludes the
original case called (8,28) in that proposition. It does not resolve JC2 or
the different above-125 chain with exponent ratio (3,4).

Read `ASTRA_3_PROGRESS_REPORT.md`, then `ASTRA_3_PENTAGON_PROJECTIVE.md`.
The leading-orbit completeness proof is in `ASTRA_2_CASE2_EXACT_DESCENT.md`.
`ASTRA_STATE.md` and `GRADED_FRONTIER.md` describe the live targets;
`ASTRA_RUN_LOG.md` preserves the chronological record. Earlier reports remain
historical snapshots, including statements that the pentagon was then open.

## Replay the results

From the repository root, with Python and python-flint 0.9.0:

```
python astra/verify_case2_certificate.py
python astra/verify_pentagon_projective.py
```

Each command prints four PASS lines. Neither invokes Singular. The pentagon
checker reconstructs the homogeneous system, specializes both charts,
multiplies one unit identity and five pure-power identities, checks the
matrices and verifies good reduction at p=32003. The geometric normalization,
dessin completeness and valuation arguments are written proofs, not
proof-assistant formalizations. No external peer review is claimed.

To regenerate the pentagon certificates with Singular 4.3.1:

```
python astra/pentagon_descent.py --right-edge --stop-r -5 --defer-gb
Singular -q astra/pentagon_descent_modular_right_raw.sing
python astra/pentagon_descent.py --right-edge --stop-r -6 --defer-gb --boundary
Singular -q astra/pentagon_descent_modular_right_raw_boundary.sing
python astra/verify_pentagon_projective.py
```

An additional exact-field reconstruction is available as
`python astra/verify_pentagon_descent.py --constraints-only`. It verifies nine
raw characteristic-zero equations from a separate small-field model. Its
default certificate mode expects a direct exact certificate that was not
obtained; it is not the verifier for the successful projective proof.

The five inherited positive witnesses pass via
`python astra/graded_control.py`. Prior controls remain in
`python astra/run_controls.py`; their archive audit retains historical scope.

## Next explicit target

Repair the translation of the published above-125 chain
`(8,28)->(7/4,3)`, `(m,n)=(3,4)`, corresponding to the (108,144) campaign
target. The primary table does not print the compiler's assumed last lower
corner, and its c' range predates a correction. Derive those data from the
primary definitions before generating supports or running elimination.
The matching label (8,28) does not transfer the completed (2,3) proof to this
different exponent ratio.

Other live lanes are the H3 boundary-depth theorem and a residue-free
Briançon construction. The six-blowup H3 exclusion is bounded, and the
Briançon period obstructions retain their explicit geometry hypotheses.
Do not restart either completed Proposition 4.3 polygon without identifying
a concrete flaw in its proof or verification.

## Evidence cautions

- Affine modular emptiness alone does not prove characteristic-zero emptiness.
  Astra 3 depends on the verified boundary certificates and good reduction as
  well as its valuation argument.
- The exact five/35 leading count is proved independently of the historical
  degree-1144 object; that object's full provenance remains unresolved.
- Three direct exact pentagon eliminations timed out. No direct
  characteristic-zero Groebner unit certificate is claimed for the pentagon.
  The failed generated scripts are preserved losslessly as `.sing.gz`.
- Successful and failed runs are classified in
  `astra/artifacts/pentagon_run_manifest.json`. Parser errors and timeouts
  are not evidence of emptiness.
- No numerical near-hit or necessary-condition survivor is a CEC.
