# Sol 6: collision-first `(4,6)` continuation

Date: 2026-08-25. Parent tip: `2fe8ab2` on
`codex/sol5-collision-first`.

## Binding verdict gate

There is **no counterexample yet**. A numerical or modular point remains
`CANDIDATE-UNVERIFIED` until exact characteristic-zero reconstruction and a
direct original-coordinate replay of `[P,Q]=1` and the normalized collision.

## Reproduction audit

Both Sol 5 exact certificates replay under SymPy 1.14:

```text
COLLISION RIBBON (2,3) EXACT CERTIFICATE: PASS
COLLISION RIBBON (4,6) UPPER REDUCTION: PASS
```

The `(4,6)` reduction has 52, 57, and 43 formal terms in `E2,E1,E0` and the
degree-126 frontier has 147, 168, and 189 coefficient equations respectively.

## Exact closure: first sparse outer-edge chart

Keep the four outer weighted-edge monomials, the collision factor in `p0`,
and all constant lower jets:

```text
p0 = a(x^84-x)
p1 = b x^63 + r1
p2 = d x^42 + r2
p3 = e x^21 + r3.
```

Direct substitution into the independently verified reduced original
Jacobian gives the one-coefficient certificate

```text
[x^1] E1 = 3 a^2 c.
```

The required bottom vertex of `P` gives `a != 0`, and the required top vertex
`c*y^6` of `Q` gives `c != 0`. Therefore this entire chart is empty over
characteristic zero. `r1,r2,r3` were retained, and the proof makes no division
or nonresonance assumption. The script includes negative controls for the
collision tail and the top-Q vertex.

This closes only this sparse chart, not the full 212-variable frontier.

## Export audit and representation correction

`collision_first/ribbon46_export.py` constructs exact dense coefficient
systems at small scale and passes the scale-1 control:

```text
20 variables, 24 equations
Jacobian rows 4+7+10, two Q-collision rows, one vertex-saturation row.
```

The live scale-21 dense expansion was attempted and stopped without a file or
verdict: expanding the formally compact 504 rows into the 212 coefficient
variables is substantially larger than the row count suggests. The exporter
is now capped at scale 4 so this failure cannot be mistaken for a completed
modular search.

The exact scalable representation is evaluation based. Over a prime larger
than the degree bounds, `E2,E1,E0` vanish coefficientwise exactly when they
vanish at 147, 168, and 189 distinct field points. At an evaluation point,
each `p_i` and `p_i'` is a linear form in its coefficients, while each residual
retains only the original 52, 57, or 43 formal terms. The next implementation
should use this straight-line evaluator for modular tangent/rank searches and
reserve coefficient expansion for a final small lifted candidate.

## Files

- `collision_first/ribbon46_sparse_edge_certificate.py`: exact sparse-chart
  closure and negative controls.
- `collision_first/ribbon46_export.py`: exact small-scale saturated exporter
  and guard against the known scale-21 dense-expansion failure.

