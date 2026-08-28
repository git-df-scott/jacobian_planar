# Manifest — JC2 certified-separator pivot

All computed nullspaces and counts are labeled modular.  No counterexample
candidate was produced.

## `FULL_NIGHT_REPORT.md`

Claim: complete adversarial response to Tasks 1–7, including the exact
certificate protocol, the refusal to infer quadratic counts from dimension,
corrected two-prime results, scaling analysis, published equations, and tomorrow's
recommended order.

Verify:

```bash
python3 verify_deliverables.py
```

## `ROUND2_THEORY.md`

Claim: standalone theory note for Tasks 1, 2, 3/6, 4, and 5/7 with primary-source
links and the frozen generic-plane benchmark.

Verify:

```bash
python3 verify_deliverables.py
```

## `separator_pipeline.py`

Claim: stdlib+NumPy modular tame sampler and degree-at-most-two interpolator with
controls `S0`, `S1`, `S2`, `I1`, `I2`, and `I3`.  It never promotes modular
relations to characteristic-zero certificates.

Fast smoke verification:

```bash
python3 separator_pipeline.py --d 3 --prime 999983 --batch 96 --patience 3 --max-samples 1000 --holdout 12 --csv /tmp/jc2_smoke.csv
```

Full grid reproduction (computationally expensive; run each prime independently
or in parallel):

```bash
for d in 3 4 5 6 7 8 9 10; do for p in 999983 1000003; do python3 separator_pipeline.py --d "$d" --prime "$p" --batch 640 --patience 3 --max-samples 15000 --holdout 20 --csv "/tmp/jc2_${d}_${p}.csv" || exit; done; done
```

## `separator_counts.csv`

Claim: corrected `MODULAR-CORRECTED` results for `d=3..10` and both requested
primes, including samples, rank, nullity, component labels, all controls, and the
explicitly non-predictive generic-plane benchmark comparison.  Earlier results
from a nondominant narrow sampler were withdrawn and are not present.

Verify:

```bash
python3 verify_deliverables.py
```

## `certify_separator_d3.py`

Claim: exact characteristic-zero certification of
`h=p20*q11-p11*q20` on `Aut_{<=3}`, with two-prime consistency checks,
ambient nontriviality, and proof that `h` is outside the linear span of the
universal Keller coefficient quadrics.

Verify:

```bash
python3 certify_separator_d3.py
```

Expected terminal line: `CANDIDATE-UNVERIFIED: none`.

## `verify_deliverables.py`

Claim: fast syntax, CSV integrity, rank-nullity, cross-prime, certificate, and
report-structure checker.  It does not recompute the expensive grid.

Verify:

```bash
python3 verify_deliverables.py
```
