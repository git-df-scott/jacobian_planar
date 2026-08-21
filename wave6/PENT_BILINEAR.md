# Pentagon case (1) is a BILINEAR system — structure never exploited

## The observation

Monomial census of the exact char-0 system
`campaign/audit_tracks/trackB1_param_system.json`
(283 equations, 165 unknowns: 51 `c`, 110 `d`, 4 `s`):

| shape (c-deg, d-deg, s-deg) | count |
|---|---|
| (1,1,0) | 5376 |
| (0,1,2) | 1069 |
| (1,0,3) | 990 |
| (1,0,2) | 496 |
| (0,1,1) | 431 |
| (1,0,1) | 200 |
| (0,1,0) | 99 |
| (1,0,0) | 95 |
| (0,0,2) | 10 |
| (0,0,1) | 4 |
| (0,0,0) | 2 |

**Max c-degree per monomial = 1. Max d-degree per monomial = 1.**
(s reaches degree 3, but s is only 4 variables.)

So the system is *exactly bilinear* in the c-block and the d-block:

    F(c, d, s) = Ad(c,s) · d + a0(c,s)          (linear in d for fixed c,s)
               = Ac(d,s) · c + b0(d,s)          (linear in c for fixed d,s)

This was recorded qualitatively in session 41 ("every monomial is bilinear, one
c and one d, up to s-powers") for the *bottom edge subsystem*. What is new here
is that it holds for the **entire 283-equation case (1) system**, and that it
has never been used computationally.

## Consequence 1 — the search dimension is 55, not 165

`w6_pentnum.py` runs multi-start Newton over all 165 unknowns. But for any
fixed (c,s) the 110 d-unknowns are the solution of a *linear least-squares
problem* — they never need to be searched at all. This is Golub–Pereyra
variable projection (VARPRO).

    search dimension 165  ->  55   (51 c + 4 s)
    110 unknowns eliminated EXACTLY at every function evaluation

Beyond the 3× dimension drop, VARPRO removes the curved valleys that trap
Gauss–Newton on separable problems: the residual becomes the distance from
`a0(c,s)` to the column space of `Ad(c,s)`, which is the quantity the geometry
actually cares about. Implemented in `w6_pent_varpro.py`, with the campaign's
mandatory P-POS / P-NEG controls.

## Consequence 2 — an exact reformulation of case (1)

Write `C = (c,1) ∈ C^52` and `D = (d,1) ∈ C^111`. Each equation is a bilinear
form `Cᵀ N_k(s) D = 0`. So for each fixed `s ∈ C⁴`, the fiber of case (1) is

  **the intersection of the Segre variety P⁵¹ × P¹¹⁰ ⊂ P⁵⁷⁷¹ (dimension 161)
  with a linear subspace of codimension 283**, restricted to the locus where
  both last coordinates are nonzero.

Expected fiber dimension: 161 − 283 = −122. Adding the 4 s-parameters gives an
expected dimension of **−118** for case (1) overall — which agrees exactly with
the independently measured overdetermination of the linearly reduced system
(241 equations, 123 unknowns → 118). Two different routes to the same 118 is a
consistency check on the whole export chain.

**Read honestly:** expected dimension −118 says a solution would be a
coincidence of codimension 118. It is NOT a proof of emptiness — `N_k(s)` is a
highly structured family, not a generic linear space, and the entire campaign
exists because this system is not generic. But it does say what any positive
result would have to be, and it explains why direct Gröbner runs exhaust memory:
they are computing a wildly overdetermined ideal by a method that cannot see
the bilinear splitting.

## Consequence 3 — what a VARPRO floor would mean

A persistent positive residual floor is **evidence of emptiness, never proof —
a miss is a miss.** But the floor value is itself a datum the campaign has never
had: it measures how close the Keller condition comes to the non-injectivity
locus. The campaign has only ever asked whether the two varieties intersect,
never how near they pass.
