# night9/interp — audit of the single multi-prime support

Scope note. Measurements only. Every result is labelled with its
characteristic or with the ring it was computed in. No assessment of what any
of these numbers mean is offered.

The cross-prime matrix (`night9/CROSS_PRIME.md` §4) records exactly one
support with non-degenerate NONEMPTY at three or more distinct primes:

    9fad1aac9556,  primes 2, 3, 5
    S_P = (0,10) (1,0) (2,1) (3,0)
    S_Q = (0,1)  (2,1) (3,10) (4,0)

## The audited vector

The matched tuple with coefficient vectors identical at all three primes,

    a = (1, 1, 0, 0)   over the ordered S_P above
    b = (1, 0, 1, 1)   over the ordered S_Q above

is, written out,

    P = y^10 + x
    Q = y + x^3 y^10 + x^4

## Direct exact computation over Z (independent of interp.py)

    P_x = 1                      P_y = 10 y^9
    Q_x = 3 x^2 y^10 + 4 x^3     Q_y = 1 + 10 x^3 y^9

    P_x Q_y - P_y Q_x - 1
      = (1 + 10 x^3 y^9) - 10 y^9 (3 x^2 y^10 + 4 x^3) - 1
      = 10 x^3 y^9 - 30 x^2 y^19 - 40 x^3 y^9

**Integer bracket residual (ring Z):**

    det J - 1  =  -30 x^3 y^9 - 30 x^2 y^19  =  -30 x^2 y^9 (x + y^10)

This matches the coordinator's audit expectation `-30*(x^3*y^9 + x^2*y^19)`
character for character. It was recomputed here symbolically with sympy on
exact integers, and independently by hand above; both agree.

The two collision equalities hold **exactly over Z** (convention `0^0 = 1`):

    P(0,1) - P(1,0) = (1 + 0) - (0 + 1) = 0
    Q(0,1) - Q(1,0) = (1 + 0 + 0) - (0 + 0 + 1) = 0

## Consequence recorded, not interpreted

`30 = 2 * 3 * 5`, so the residual reduces to 0 in `F_2`, `F_3`, `F_5` and is
non-zero in `F_p` for every other prime. The matrix records this same support
as EMPTY at p = 7, 11, 13, 17, 19, 23.

**Exact verification over Q: FAILED** (`det J - 1` is not identically zero).
Recorded as such. The object is filed as CANDIDATE-UNVERIFIED per the brief.

Nothing produced by `interp.py` passed exact verification over Q — see
`INTERP.md` §3 for the full 32-tuple tally.
