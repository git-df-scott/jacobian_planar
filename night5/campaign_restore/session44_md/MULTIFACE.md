# Every qualifying face, not just one

The face parameterisation was being applied to ONE face. Both open
subcases carry more, and each independently determines coefficients.

## Subcase 2 (quadrilaterals) -- 2 qualifying faces

    dir (-2,1): P-face (0,0)-(8,16) len 8, Q-face (0,0)-(12,24) len 12
                -> R^2/R^3, deg R = 4, eliminates 17
    dir ( 1,0): P-face (8,14)-(8,16) len 2, Q-face (12,21)-(12,24) len 3
                -> R^2/R^3, deg R = 1, eliminates 5
    naive total eliminable: 22

## Subcase 1 (pentagons) -- 3 qualifying faces

    dir (-1,0): P-face (0,0)-(0,8)  len 8, Q-face (0,0)-(0,12)  len 12
                -> R^2/R^3, deg R = 4, eliminates 17
    dir (-1,1): P-face (0,8)-(8,16) len 8, Q-face (0,12)-(12,24) len 12
                -> R^2/R^3, deg R = 4, eliminates 17
    dir ( 1,0): P-face (8,14)-(8,16) len 2, Q-face (12,21)-(12,24) len 3
                -> R^2/R^3, deg R = 1, eliminates 5
    naive total eliminable: 39

Subcase 1 is therefore MORE constrained than subcase 2, not less -- its
extra vertices buy it an extra face. That inverts the natural assumption
that the pentagon case (more coefficients) is the harder one.

## The deg R = 1 face is an explicit closed-form condition

Both subcases share the (1,0) face with deg R = 1, i.e. R linear. Then
face(P) = R^2 on the three points (8,14),(8,15),(8,16) forces the classic
square condition

    a_(8,15)^2 = 4 a_(8,14) a_(8,16),

and face(Q) = R^3 on (12,21),(12,22),(12,23),(12,24) forces those four
coefficients to be the cube of the same linear form -- two more
independent conditions. These are explicit, checkable, and were never
imposed by any instrument in this campaign.

## Caveat

The totals are naive sums: faces share endpoint coefficients, so the true
reduction is smaller than 22 and 39 respectively. The correct way to use
this is to parameterise by the face roots jointly and let the shared
endpoints impose consistency (e.g. the (1,0) and (-2,1) faces of subcase 2
share the vertex (8,16), so the two R's must agree there). That
consistency is itself an extra equation and could be a source of
contradiction -- worth checking directly.
