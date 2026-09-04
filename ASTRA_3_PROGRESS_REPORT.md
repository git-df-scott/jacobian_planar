# Astra 3 progress report — 2026-09-04

**No counterexample found. This run excludes the neighboring pentagon in
GGHV Proposition 4.3(1), by a computer-assisted characteristic-zero argument.**
Together with Astra 2, both polygons of that proposition are excluded, and
therefore so is its original case called (8,28). JC2 remains open here.

Branch: `astra/jc2-pentagon-geometry-2026-09-04`.
Parent: `e479477263c1f4176b287309dda2dcb4213fcb84`.

1. **Reconstructed the full target.** The support check covers all 60 P and
   124 Q nonconstant monomials. Negative grading levels are included. The
   leading quintic and five-orbit completeness result from Astra 2 still apply.
2. **Reduced the problem to five parameters.** The highest-x edge forces a
   square/cube relation. One explicitly exhibited scaling normalizes its
   nonzero parameter. Constant field matrices solve each level while retaining
   every free kernel coordinate; their ranks are checked exactly.
3. **Closed the gap left by a finite-field contradiction.** Restoring the
   scaling parameter gives a weighted homogeneous system. At p=32003, an
   explicit unit certificate excludes its affine chart, and five explicit
   power certificates exclude every nonzero point on its boundary. Every
   exact coefficient operator has verified good reduction. A written
   valuation argument then excludes characteristic-zero solutions.
4. **Verified and preserved the evidence.** The independent replay passes
   all four check groups: homogeneous reconstruction and both charts, affine
   identity, five boundary identities, and exact good reduction. The code,
   certificates, logs and run manifest are included. Three direct exact
   eliminations timed out; their inputs and outputs are retained and are not
   used as emptiness evidence.

The full argument, its hypotheses and reproduction commands are in
[ASTRA_3_PENTAGON_PROJECTIVE.md](ASTRA_3_PENTAGON_PROJECTIVE.md). This is a
scoped computer-assisted proof with written geometric steps; no external
peer review, proof-assistant formalization or literature-priority claim is
made. The source reduction is
[GGHV Proposition 4.3](https://arxiv.org/pdf/2204.14178).

The next explicit target is the separate above-125 chain
`(8,28)->(7/4,3)` with exponent ratio `(3,4)`. Its missing lower-corner and
c' data must be reconstructed from the primary definitions before searching.
The present `(2,3)` exclusion does not settle it.
