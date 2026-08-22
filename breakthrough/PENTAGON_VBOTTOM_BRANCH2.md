# The 45 v-bottom equations on level-15 branch 2

## Exact verdict

**No obstruction occurs among the equations reached by the current descent.**
The 45 equations split exactly as follows:

* 39 are identities modulo the already solved w-levels 15 through 20;
* 6 are coefficients of w-levels 12 through 14, which have not yet been
  descended and therefore cannot honestly be called either identities or
  obstructions.

This is not a dimension count or a specialization.  For a monomial indexed by
`p_(j,i) q_(l,k)`, put `d=2i-j`, `e=2k-l`.  Its coefficient at v-level `V` is

    d*k - e*i,

while its coefficient in the w-ladder, at `a=j-i`, `b=l-k`, is

    b*i - a*k = d*k - e*i.

If it occurs as the coefficient of `r^n`, then `a+b=n-V`.  Thus every one of
the 45 equations is literally a coefficient of a w-level equation, not merely
a consequence after a generic substitution.  Their distribution is

    w=20,19,18,17,16,15,14,13,12:  9,8,7,6,5,4,3,2,1.

Branch 2 has reconstructed the complete w-equations through level 15, so the
first 39 reduce to zero on the generic chart and on every exceptional component
that actually satisfies those same level-15 equations.  This qualification is
important: merely setting `a0=0` or `F3=0` does not by itself solve `C3..C6`.
The six remaining equations must be carried into levels 14, 13, and 12 with
all new polynomial pairs and kernel constants retained.

In particular, the deepest relation

    2 p_8,0 q_13,1 = 3 p_9,1 q_12,0

is the constant coefficient of w-level 20.  Its agreement with eighth-power
scaling is exact but supplies no independent existence evidence.

## Reproducer

`pentagon_vbottom_branch2.py` generates all 45 sparse bilinear equations,
checks the coefficient identity term by term, asserts the distribution above,
and prints the six genuinely pending equations.  It uses no random point,
finite-field specialization, division by `a0`, or division by `F3`.

## Exceptional strata status

The regrading identity is branch-independent.  On any component of `a0=0` or
`F3=0` that survives the complete level-15 system, the same 39 equations vanish
and the same six await lower descent.  It does **not** prove that every point of
either divisor survives, nor does it complete their level-15 decomposition.
The exact level-15 equations still give:

* on `a0=0`, `C3=0` and
  `C4=15*a1*c1*(a1^2-4*c0*b2)^2/(16*c0^4)`, producing the shifted subcases
  `a1=0` and `a1^2=4*c0*b2`;
* on `F3=0`, `C3` and `C4` retain an `F2^2` factor, so the loci `F2=0` and
  `a0=a1=0` must remain separate before solving `C5,C6`.

Pentagon status remains **NO VERDICT**.  No counterexample and no emptiness
certificate is claimed.
