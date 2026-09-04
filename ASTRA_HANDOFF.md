# ASTRA handoff — 2026-09-04

## Result first

No explicit Keller pair, CEC, or CE was found.

The main new result is a joint target/source exclusion of the unique H3
blueprint on every archived boundary-tree record through six blowups.  Unlike
the old source sweep, the new search imposes the target-forced discrepancy,
tangential degrees, and coordinate degrees and solves the complete
nonnegative complementarity problem without a degree-two support cap.  It
finds zero coordinate solutions for both (3,5) and (3,6).

The group-first replay independently proves that the H3 local permutation
class is unique up to simultaneous conjugacy and misses the escaping-line
Euler budget by exactly one.  The Briançon targets remain exactly closed by a
nonzero holomorphic period.  Graded case (2) remains `EMPTY-mod-p` at p=32003
and `UNKNOWN` over characteristic zero.

## Start here

Read, in order:

1. `ASTRA_STATE.md`
2. `TARGET_SOURCE_COMPATIBILITY.md`
3. `OFF_BY_ONE.md`
4. `GROUP_FIRST_SEARCH.md`
5. `BRIANCON_MATE_STRIKE.md`
6. `GRADED_FRONTIER.md`
7. `ASTRA_RECONCILIATION.md`
8. `ASTRA_RUN_LOG.md`

Then run:

```
python3 astra/run_controls.py
```

All JSON artifacts should be regenerated under `astra/artifacts/` and the
runner should finish with `ALL ASTRA CONTROLS: PASS`.

## Exact new artifacts

| file | role |
|---|---|
| `astra/joint_blueprint.py` | target/source bridge, coordinate complementarity, H3 bounded search |
| `astra/group_first_h3.py` | direct H3 enumeration and simultaneous-conjugacy quotient |
| `astra/abstract_target_screen.py` | compact replay of the 5,261-row abstract screen |
| `astra/briancon_control.py` | exact gradients, chart identities, and period-boundary controls |
| `astra/graded_control.py` | Poisson grading and five exact positive witnesses |
| `astra/audit_graded_case2.py` | pinned archive hashes, modular factorization, evidence adjudication |
| `astra/run_controls.py` | deterministic aggregate replay |

## Three next attacks

### 1. Prove the H3 boundary-depth lower bound

Do not blindly run more trees.  Analyze the principal-kernel recurrence for a
discrepancy -1 component with forced degree 3d.  Either prove that no
nonnegative coordinate divisor can occur at any depth in the relevant tree
class, or derive the first possible depth and a finite list of skeletons.  Only
those skeletons should be enumerated.

### 2. Build a residue-free second-kind Briançon target

The next P must enlarge the primitive's pole divisor beyond `2O`, preserve
gradient unimodularity and irreducibility, and kill the elliptic de Rham class.
Start from a degree-two elliptic function R and solve `eta=dR` together with
the embedding equations.  Reject reducible atypical fibres immediately.

### 3. Produce an exact-Q case-(2) descent

Lift the five residual-scaling orbits as algebraic components over Q, establish
which characteristic-zero eliminant is the correct object, and solve the lower
linear levels orbit by orbit.  The output must be a replayable exact-Q `[1]`
certificate or a surviving explicit branch.  Do not rerun the y-adic wall.

## Graded published frontier warning

The degree-144 `(8,28)->(7/4,3)`, `(m,n)=(3,4)` entry is the first published
above-125 target to reconstruct.  The existing compiler assumes an unprinted
A'_t and uses an uncorrected c' ladder.  Repair this provenance before treating
any generated stratum as the published case.

## Evidence boundary

- H3 tree result: `EXACT-Q`, through six blowups only.
- Abstract 5,261 rows: `ADMISSIBLE-SHAPE`, not realizations.
- H3 target group: `BLUEPRINT`, killed by R topology and bounded source data.
- Briançon targets: exact all-degree mate obstruction under explicit published
  fibre-geometry hypotheses.
- Graded case (2): `EMPTY-mod-p` at p=32003; characteristic zero `UNKNOWN`.
- No solver timeout or missing binary is evidence.
