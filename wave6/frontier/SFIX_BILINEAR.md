# The s-specialised slice of trackB1

`scratchpad/tb1_sfix.sing`, generated from
`campaign/audit_tracks/trackB1_case1_full_p65521.ms` at p = 65521 with
`s_1_5=34562, s_2_6=7018, s_3_7=8383, s_4_8=37424` (s_4_8 nonzero as the
saturation row requires).

## Why fix s

The root is degree 1 in the 51-variable c-block, degree 1 in the 110-variable
d-block, and degree ≤3 in the **4-variable s-block**. All the nonlinearity is
in those four variables. Fixing them numerically should collapse the system.

## What it actually produced — measured, not assumed

I claimed the slice would be "purely bilinear, every equation bidegree (1,1),
total degree 2". **That claim is false and the check caught it.**

| total degree | # equations |
|---|---|
| 1 | **21** |
| 2 | 262 |
| 4 | **1** |

| (deg_c, deg_d) | # equations |
|---|---|
| (1,0) | 1 |
| (1,1) | 282 |
| (2,1) | 1 |

162 variables, 284 equations, **7,032 terms**, against the root's 166 variables
and 8,774 terms at degree 5.

The degree-4 row is the saturation, `w_sat·c_1_0·c_8_14·d_12_21·37424 − 1`:
substituting `s_4_8` still leaves four variables multiplied together. So the
correct statement is **283 of 284 equations at total degree ≤ 2, plus one
quartic saturation row** — not "all bilinear".

## The unplanned find: 21 linear equations

Fixing s makes **21 equations purely linear**. They do not exist in the root —
they appear only once the s-monomials are numeric. Twenty-one linear equations
permit **21 exact variable eliminations at zero degree cost**.

That is the free reduction the forced chain never had. The chain eliminated by
substituting high-degree expressions, which is why it drove degree 5 → 19 and
terms 8,774 → 414,175. Eliminating with a genuinely linear equation cannot
raise the degree of anything.

**Untried and cheap: use the 21 linear rows to reduce 162 → 141 variables, then
solve.** This is the next thing to run on this slice.

## How to read the outcome

- **NONEMPTY** → a genuine point of case (1) at this s. That is the hit, and it
  must then be verified against the original equations and lifted.
- **EMPTY** → only that *this one s* admits no solution. It does **not** close
  trackB1. What it would establish is that the generic s-slice is empty, so any
  solution lies over a proper closed subset of the 4-dimensional s-space — and
  4 dimensions is small enough to then attack exhaustively.

An EMPTY here is a result about one point of s-space, and must never be
recorded as a verdict on trackB1.

---

## LIMITATION — why an EMPTY slice is weak evidence, stated before the results

Recording this **before** any slice verdict lands, so it cannot be written as a
rationalisation afterwards.

Fixing `s` makes the computation tractable, but it **strictly reduces the chance
that a solution exists in the object being computed**. The slice is empty
whenever the chosen `s` is not in the image of the projection

    V(trackB1)  --->  s-space  (4-dimensional)

and we already have direct evidence that trackB1's projections are **not
dominant**: at both primes, every random `(d,s)` admits no `c`, and every random
`(c,s)` admits no `d`. A variety whose projection to the `(d,s)`-block misses a
generic point has no reason to hit a generic point of the smaller `s`-block
either.

So the inference to be careful about is:

> generic s-slice EMPTY  ⟹  trackB1 EMPTY      **✗ INVALID**

If V(trackB1) is nonempty but its projection to `s`-space is not dominant — which
is exactly what the probes suggest — then **every** generic `s`-slice is empty
while trackB1 itself is nonempty. Emptiness of the slices would be precisely
what we should expect in that case, and would carry almost no information about
the question we care about.

What the slices CAN do, honestly:

- **NONEMPTY at any seed → a genuine point.** This direction is sound and is the
  whole reason to run them. A hit is a hit.
- **EMPTY at several seeds →** only that those `s` are outside the image. It
  confines any solution over a proper closed subset of the 4-dimensional
  `s`-space. That is worth having *only* because 4 dimensions is small enough to
  then attack directly — not because it is evidence of emptiness.

This is the same trap as the random `(d,s)` probes, one level up: a search that
provably cannot reach the solution locus tells you little when it fails. The
slices are being run for their **positive** direction and as a route to
characterising the exceptional `s`-locus, not as an emptiness argument.
