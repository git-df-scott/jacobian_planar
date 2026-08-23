
## A22 — OPEN VERIFICATION GAP: does the pentagon system really sit at (72,108)?

**Status: a question I could not settle from the repository, raised rather than
answered. Not a claim that anything is wrong.**

The pentagon's Newton polygons, as recorded in `EDGE_LADDER.md` and audited in
`WITNESS.md`, are

    N(P): (0,0), (1,0), (8,14), (8,16), (0,8)
    N(Q): (0,0), (2,1), (12,21), (12,24), (0,12)

Taking total degree as `max(i+j)` over the vertices gives

    deg P = 8 + 16 = 24 ,   deg Q = 12 + 24 = 36 ,

not `72` and `108`. The ratio is right — `24 : 36 = 72 : 108 = 2 : 3` — and
indeed `(72,108) = 3 * (24,36)`, so the two differ by an exact factor of three.

The top vertices do factor consistently with the GGV framework `en(P) = 2B`,
`en(Q) = 3B`:

    en(P) = (8,16) = 2 * (4,8) ,  en(Q) = (12,24) = 3 * (4,8) ,  so B = (4,8) .

But `41.md` records `L = 3` for `(72,108)` and `L = 4` for `(108,72)`, where `L`
is the first coordinate of `B`. Here that coordinate is `4`.

### Why this matters, and why it does NOT invalidate the computations

It does not affect whether the EMPTY verdicts are correct. Those are statements
about an explicitly constructed polynomial system, they were computed in
characteristic 0, and the pipeline that produced them now passes an end-to-end
positive control (an automorphism at `(2,4)` -> NONEMPTY) and a negative control
(`(2,3)` -> EMPTY in all 12 charts). What is in question is not whether the
system is empty but **which degree pair the system is about**.

That distinction is sharp here. If the pentagon is literally `(24,36)` in
ordinary coordinates, then its max degree is `36`, comfortably inside the range
where JC2 is already known (Moh: max degree at most 100), and emptiness would be
expected rather than informative. If instead the pentagon is a reduced or
blown-up representation whose ordinary degrees are `(72,108)`, the verdicts bear
on genuinely open territory.

### What would settle it

One of:

* the explicit map from a pentagon solution `(h_a, g_b)` back to a pair
  `(P,Q)` in ordinary `x, y` coordinates, from which `deg P` can be read off
  directly; or
* the derivation that produced these vertices from `(72,108)` — attributed in
  `EDGE_LADDER.md` to Codex's reconstruction — including whichever coordinates
  the polygon is expressed in; or
* a statement of `B` and `L` for `(72,108)` that reconciles `L = 3` with
  `B = (4,8)`.

Flagged for Codex, who reconstructed the polygons. Until it is resolved, the
correct phrasing of every verdict in this campaign is "the pentagon system is
empty", not "there is no counterexample at (72,108)".
