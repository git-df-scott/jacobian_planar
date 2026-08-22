# Codex independent `p_1_1 = 0`, `p_1_0 != 0` hunt

## Target

This branch attacks the pentagon chart

```text
p_1_1 = 0
p_1_0 != 0
```

over finite fields, starting independently from the raw 66-condition export in
`wave1/pent_L23.ms`.  A modular witness would be a counterexample lead only;
it would still require characteristic-zero lifting and verification in the
original equations.

## Independent construction and controls

`pentagon_core.py` reconstructs `Q` directly from

```text
{P,Q} = P_x Q_y - P_y Q_x = x^2
```

and implements the stated Newton-polygon supports without parsing the raw
million-term formulas.

The following controls pass:

- all 66 independently reconstructed equations agree exactly with the raw
  export at a generic point over `F_43`;
- all 66 agree at an independent point in the `p_1_1 = 0` chart;
- perturbing that chart point is detected by all 66 negative controls;
- the full 14-variable late block is checked to be jointly affine;
- a planted consistent affine system is recovered and verified;
- an inconsistent perturbation is rejected;
- the degenerate solution `P=x+y` is accepted by the bracket/support equations
  and by all 66 untouched raw polynomials, but rejected by the required
  Newton-vertex checks.

The unsaturated exported system in this chart is therefore `NONEMPTY`.  That
result is degenerate and is not a counterexample candidate.  The CE-bearing
target in this branch always includes the Newton-vertex nonzero conditions.

## Non-degeneracy audit

The convex hulls reconstructed from the row supports have vertices

```text
N(P): (0,0), (1,0), (8,14), (8,16), (0,8)
N(Q): (0,0), (2,1), (12,21), (12,24), (0,12)
```

After the additive/fixed normalizations, a candidate must check the mutable
nonzeros

```text
p_8_0, p_14_8, p_16_8
q_12_0, q_21_12, q_24_12.
```

Thus `p_16_8 != 0` is a sound necessary saturation for an EMPTY-pruning run,
but it is not a complete non-degeneracy test for a returned point.  Every
candidate must pass all six mutable vertex checks above.

## Completed searches

### Coordinate-sparse search over `F_43`

- 1,764 exhaustive choices with `p_1_0,p_8_0 != 0` and every other early
  coordinate zero;
- 42 additional one-coordinate perturbations;
- every affine completion test had ranks `rank(A)=14`,
  `rank([A|b])=15`.

This excludes only those explicit sparse slices.

### Square-top-edge search over `F_29`

The necessary top-edge structure was imposed as `P_top=S^2` for a quartic
`S`.  In the normalized slice

```text
p_1_0 = s_0 = s_4 = 1
```

all 29^3 = 24,389 choices of `s_1,s_2,s_3` were tested, with the remaining
nine late variables solved exactly.  Every test had ranks `9` and `10`, so no
point exists in this explicit slice.

This does not imply that the full chart is empty.

## Tangent reconnaissance

At the degenerate bracket solution over `F_43`, both the raw 66-condition
system and the independently derived full support system have linearization
rank 14 and tangent dimension 44.  The tangent space can turn on the lower and
middle required `P` vertices, but not `p_16_8`; the top vertex therefore appears
only at higher order.  This is consistent with the square-top-edge geometry
and explains why coordinate-sparse probes miss the live directions.

## Full sparse bilinear target

`bilinear_full.py` keeps every supported Q coefficient and imposes the complete
polynomial identity `{P,Q}=x^2`, rather than only the 66 truncated L23
conditions.  It substitutes `p_1_1=0` and uses separate Rabinowitsch variables
for the chart condition and all six mutable Newton vertices, preserving maximum
degree two.

The independent generator was symbolically compared with the hash-pinned
302-equation exact-Q source `trackA_system_case1.json`.  After the stated
gauges and `p_1_1=0`, all source equations reduce exactly to the generator's
299 bracket equations.  With seven saturation rows the exported target has:

```text
186 variables
306 equations
degree <= 2
6,924 terms
125,784 bytes
```

The generated modular file is `p11zero_full_sat_p1000003.ms`.  No compatible
solver is installed in this environment, so generation and validation do not
constitute a solve.

## Reproduction

Run with Python 3:

```text
python3 codex_p11zero/audit_p11zero.py
python3 codex_p11zero/raw_export_control.py
python3 codex_p11zero/vertex_audit.py
python3 codex_p11zero/bilinear_full.py
python3 codex_p11zero/search_sparse.py
python3 codex_p11zero/tangent_probe.py
python3 codex_p11zero/search_top_edge.py
```

No candidate witness has been found, and no proof of emptiness has been
obtained.

VERDICT: NO VERDICT
