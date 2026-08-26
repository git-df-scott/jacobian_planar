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

## Restoring linear jets opens an exact algebraic branch

The preceding contradiction depends on omitting the linear lower jets of
`p1,p2,p3`. Restore them in the minimal chart

```text
p0=x^84-x, p1=b*x^63+u*x, p2=d*x^42+v*x, p3=e*x^21.
```

The constant coefficients of `E2=E1=0,E0=1` solve

```text
A1=-1, A2=-u/2, A3=-(v+u^2)/3.
```

The three linear coefficients then give an exact compatible branch with

```text
A5=-(3*u^2*v+u^4+v^2)/5,
u^15+96*u^10-2052*u^5-216=0,
3258*v=7*u^12+663*u^7-16380*u^2.
```

The degree-15 equation has nonzero constant term, so every root has `u != 0`.
`ribbon46_linear_jet_branch.py` independently substitutes this branch into
the three reduced original-Jacobian rows and verifies all six coefficients
through `x^1` vanish exactly modulo the degree-15 polynomial.

This is the first exact surviving collision-first seed in the `(4,6)` lane.
It is **not a counterexample or full modular point**: coefficients from `x^2`
upward and the endpoint condition `Q(1)=0` remain to be solved. It specifically
justifies extension-field searches, because the seed is naturally algebraic
rather than rational.

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
- `collision_first/ribbon46_linear_jet_branch.py`: exact algebraic first-jet
  seed after restoring the missing linear lower jets.
- `collision_first/ribbon46_export.py`: exact small-scale saturated exporter
  and guard against the known scale-21 dense-expansion failure.
