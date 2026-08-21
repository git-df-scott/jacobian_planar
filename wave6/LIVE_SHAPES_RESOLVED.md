# The plane tangent-sweep search is now 501/501 closed

`w6_plane_sweep_search.py` tested 501 shapes and reported **499 EMPTY, 2 LIVE**.
Its own docstring defers two checks on a LIVE shape — the divisibilities
`C^i | P`, `C^j | Q`, and non-injectivity — and neither was ever run. So the two
survivors sat unresolved: the only surviving candidates in the entire plane
sweep.

## Both are resolved, and both are trivial

`w6_resolve_live.py` solves the side-condition systems exactly over ℚ with
`kappa != 0, a != 0`, then finishes the deferred checks.

| shape | branches | outcome |
|---|---|---|
| `(1,0,0,1,1,0,1,2)` — 35 eq | 1 | k1 = k2 = 0 |
| `(1,0,0,1,1,0,1,3)` — 63 eq | 3 | k1 = k2 = k3 = 0 on every branch |

**Every branch forces all `k_t = 0`, i.e. the sweep polynomial `p ≡ 0`.** With
`c0 = 0` the resulting map is

    F1 = 2a·x ,   F2 = (b·y)/a + 1/a       (affine, after clearing)

with `det JF = kappa`, a nonzero constant — so these *are* Keller, which is why
the Gröbner basis was not the unit ideal and the sweep flagged them LIVE. But
the collision system `F(x,y) = F(X,Y)` has the single solution `X = x, Y = y`:
**they are affine and injective.** Not counterexamples.

## Why this is worth recording

The sweep's LIVE verdict was correct but incomplete: it detected "the side
conditions are satisfiable" without noticing the only satisfying point is the
degenerate `p ≡ 0` one, where the tangent sweep is not a sweep at all. That is
exactly the gap the docstring warned about and left open.

**Result: the plane tangent-sweep shape family is now closed at 501/501** — 499
by emptiness, 2 by degeneracy — consistent with the campaign's headline that the
plane tangent sweep is impossible, and removing the last two open cases in that
family.
