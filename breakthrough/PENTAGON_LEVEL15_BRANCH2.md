# Pentagon level 15 on level-16 branch 2

## Result

**NO VERDICT.**  On the level-16 branch `lambda=0` with

    b0=a0^2/(4c0),   b1=a0*a1/(2c0),

level 15 is solvable exactly when four explicitly generated carried
coefficients `C3,C4,C5,C6` vanish.  There is no additional `D_7` resonance.
The first two equations factor as

    C3 = 33 a0 c1 F2^2/(32 c0^4),
    C4 = 15 c1 F2(4a0^2 a3+6a0 a1 a2-8a0 c0 b3
                         +a1^3-4a1 c0 b2)/(16c0^4),
    F2 = 2a0 a2+a1^2-4c0 b2.

Thus level 15 branches again; it does not kill branch 2.

## Generic open chart

Put `F3=a0*a3+a1*a2-2c0*b3`.  On the open chart `a0*F3 != 0`, the exact
conditions are triangular:

1. `C3=0` forces `F2=0`, matching one more coefficient of
   `h6=(h7/z^4)^2/(4c0)`.
2. After `F2=0`, `C5` is linear in the retained level-18 kernel `kappa`, with
   nonzero coefficient `-45a0^3/(16c0^2)`, so it determines `kappa` uniquely.
3. After that substitution, `C6` is linear in the free coefficient `d0` of
   `h5`, with coefficient `24c1F3/c0^2`, so it determines `d0` uniquely.

Coefficientwise inversion then reconstructs the complete `D_7` solution with
its new kernel constant.  Therefore the generic part of branch 2 survives
level 15.  The divisors `a0=0` and `F3=0` are genuine exceptional subbranches,
not failures; they must be decomposed separately using the exact four
polynomials emitted by the verifier.

## Bookkeeping control

The calculation retains `kappa`, the `D_9` kernel, the `D_8` kernel, arbitrary
`h5` and `h4`, and uses the coupled variables

    W9=g9-(3c1/2c0)z^4h5,
    W8=g8-(3c1/2c0)z^4h4.

This prevents the same generic-specialization error that corrupted the earlier
rank scans.  `pentagon_level15_branch2.py` verifies the complete descent from
level 18, proves the factorization, reconstructs the generic solution, and
checks the missing `D_7` resonance.
