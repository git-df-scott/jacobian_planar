# The candidate map — where a CE has room to live (Session 44)

All 134 eps-passing charts of the 34 published chains, probed with the
campaign's calibrated rank instrument + vertex probe (mod 65521, 3 trials):

- 62 charts structurally dead (required vertex identically zero),
- 49 charts tight (dim<=1 -> sweepable/solvable; queue territory),
- **23 charts LOOSE with all required vertices alive — the candidate set.**

Top candidates by residual freedom (dim = params - rank):
| dim | shape | max |
|---|---|---|
| 69 | (9,27)/(9,24)/(11/3,8) (2,3) — the Cor-5.7 shape | 108 |
| 69 | (12,33), (9,36)-chain, (12,36)-chains (2,3) | 135–144 |
| 65/54 | (8,32)- and (8,40)-chains /(8,28)/(11/4,7) (3,2) | 120/144 |
| 56 & 13 | **(8,28)/(7/4,3) (3,4)** — the never-attacked max-144 case | 144 |
| 46/33 | (7,35)/(19/7,5) (2,3) | 126 |
| 45 | (9,36)/(17/9,4), both orientations | 135 |

These dims are *linear tangent bounds at random points* of the reduced
residual — not proofs of positive-dimensional solution sets, but exactly
where elimination is needed and where nothing has ever been closed.
Retired en route: a modular Gauss–Newton point hunter (its positive control
failed — Newton mod p cannot reliably land on these varieties, so its
outputs are uninformative; per standing rules it is not used).

Next instruments for this set, in order: (1) Gröbner on the dim-3 charts
(nearly tight — cheap decisive), (2) sol's bigger boxes for dim 13 (T3 in
SOL_TASKS.md), (3) a y-graded walk solver (the ribbon technique) for the
dim>=45 charts, where Gröbner is hopeless but the recurrence is triangular.
