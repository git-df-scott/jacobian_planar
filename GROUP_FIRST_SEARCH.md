# Group-first target search

## Current result

`astra/group_first_h3.py` independently reproduces the decisive six-sheet H3
near-miss without GAP or a curve equation.

Fix one double transposition `a` in S6.  Enumerate double transpositions `b,c`
with

```
(ab)^3=(bc)^5=(ac)^2=1
```

and require `<a,b,c>` to be transitive.  The exact result is:

| invariant | value |
|---|---:|
| double transpositions in S6 | 45 |
| labeled triples after fixing a | 16 |
| centralizer of a | 16 |
| simultaneous-conjugacy orbits | 1 |
| generated group order | 60 |
| local staying counts: ordinary cusp, (2,5)-cusp, node | `(0,1,0)` |
| local moved-orbit counts | `(2,1,3)` |
| source Euler | 1 |
| coarse chi(R) | 0 |

All generators are even; the archived GAP computation identifies the order-60
image as A5 in its degree-six action.  The ASTRA computation needs only the
permutation action and does not rely on that name for its verdict.

The script first runs an S3/A2 closure and transitivity positive control.

## Abstract pre-screen replay

`astra/abstract_target_screen.py` reproduces the PR #24 integer-orbit screen:

```
5,261 feasible rows
635 basic (D,e,n,cusp multiset,node count) signatures
```

These rows are labeled `ADMISSIBLE-SHAPE`.  They do not construct a transitive
group, peripheral representation, braid factorization, or polynomial curve.
The concentration by degree is saved in
`astra/artifacts/abstract_target_screen_2026-09-04.json`.

## Search record schema

The next database should store one canonical record per simultaneous-conjugacy
and Hurwitz class:

```
D
transitive group identifier and generators
meridian conjugacy classes and cycle partitions
local relation template at every singularity
(s_p,o_p) local fixed/orbit counts
peripheral longitudes and monodromy at infinity
Euler source budget and componentwise R-line budget
target parametrization degrees
source discrepancy/tangential-degree partitions
source coordinate complementarity status
generic-fibre weighted boundary budgets
```

The cheap rejection order is:

1. nontrivial fixed and moved sheets for every component;
2. transitivity and generation by meridian classes;
3. source Euler budget;
4. coarse escaping budget;
5. componentwise longitude/R-line test;
6. target/source discrepancy and intersection compatibility;
7. the +D non-escape horizontal budget for each coordinate;
8. generic-line and connected-fibre conditions;
9. only then braid and polynomial-curve realization.

## Duplication control

- Fix one representative of the first meridian conjugacy class.
- Quotient remaining tuples by its centralizer, as in the H3 replay.
- Quotient ordered local factors by Hurwitz moves.
- Quotient all generators by simultaneous conjugacy.
- Hash the full peripheral tuple, not just group name and cycle types.

## Runtime wall and next run

The current runtime has no GAP installation, so the archived `gscreen.g`
degree-4 through degree-10 database sweep was not independently rerun.  This is
a `WALL`, not a negative result.  The next run should export machine-readable
records from GAP and feed them directly to `astra/joint_blueprint.py`; printing
thousands of unconstrained rows is no longer useful.

Priority should go to local spectra not isomorphic to the already-excluded H3
class and capable of changing the `(sum s_p,sum o_p)` budget by the one missing
unit identified in `OFF_BY_ONE.md`.
