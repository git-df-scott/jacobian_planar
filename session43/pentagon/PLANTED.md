# An explicit solution of {P,Q} = x^2, from a real counterexample

The pentagon's defining equation is `{P,Q} = P_x Q_y - P_y Q_x = x^2`
(see BRACKET.md).  Path A (`session43/pathA_results.md`) descends Alpoge's
degree-7 counterexample in C^3 through its C*-quotient to a plane map

    G1 = (u+1)(3u+v-2)^2 (3u^3 + u^2 v + 4u^2 + 2uv + v)
    G2 = -(3u+v-2)(9u^3 + 3u^2 v + 12u^2 + 6uv + u + 3v)
    det JG = -2 (3u+v-2)^2                          [verified]

a nonzero constant times the **square of a line** -- the same shape the pentagon
demands.  Setting `x = 3u+v-2`, `y = u` (so `u = y`, `v = x-3y+2`, a linear
change with Jacobian -1) and halving the first component gives

    P(x,y) = G1(y, x-3y+2)/2 ,   Q(x,y) = G2(y, x-3y+2)

with, verified symbolically in exact rational arithmetic,

    **P_x Q_y - P_y Q_x = x^2   exactly.**

deg P = 6, deg Q = 4.

## What this does and does not mean

It does **not** produce a counterexample.  `{P,Q} = x^2` is not the Keller
condition -- the Jacobian here is `x^2`, not a nonzero constant -- and this
(P,Q) does not satisfy the pentagon's Newton-polygon support conditions
(its support starts at `(2,0)`, while the pentagon export normalises
`P_0(x) = x`).

What it does establish:

1. **The bracket equation is satisfiable over Q, explicitly.**  So whatever
   makes the pentagon system hard is carried by the *support and vanishing
   conditions*, not by `{P,Q} = x^2` itself.  That localises the obstruction.

2. **It is the first planted witness available to pentagon machinery.**  Every
   pentagon computation on record has returned EMPTY, TIMEOUT or OOM; by the
   campaign's own planted-witness rule an instrument that has only ever said NO
   is untrusted.  This solution gives an instance where the answer is known to
   be NONEMPTY, so the export -> solve -> verify chain can be required to
   recover it.

3. **Path A and the pentagon are the same geometry.**  Path A proved that a
   C*-equivariant Keller map on C^3 descends with `det JG = c h^k`, `k >= 1`,
   and `k = n` for Keller maps (`k = 2` for Alpoge).  The pentagon asks for a
   plane map with `det J = x^2` -- the `k = 2` case.  The campaign's two live
   threads are looking at one object from two sides, and the descent exponent
   `k` is the quantity linking them.

## Status

Verified: the identity `{P,Q} = x^2` for the explicit (P,Q) above.
No witness for the pentagon system itself.  `NO VERDICT` there is unchanged.
