# Frozen schema: `jc2.face-triage.v1`

One `cases[]` entry represents one row of the GGHV enumeration. Distinct rows
with the same degree pair remain distinct. A chart is one reduced Newton-polygon
pair, including its orientation and `cprime` value. A face is one primitive
weight for which the target monomial has top weight.

Verdict semantics:

- `KILLED`: every emitted admissible chart has a verified mandatory-vertex kill;
- `SURVIVES`: at least one chart has an explicit solution of every essential-face
  coefficient equation and no essential face kills it;
- `UNCLEAR`: reduction data, chart coverage, or face solving is incomplete.

`coverage.level` is independent of the verdict and is one of
`published_exact`, `derived_from_published_lemmas`, `verified_extrapolation`, or
`conjectural_pattern`.

Every coefficient equation is a sparse integer polynomial. A term means
`integer * product(variable)`; variables may repeat to encode powers. The
`rhs` is an integer. A killing coefficient carries its reductions at both
required primes.
