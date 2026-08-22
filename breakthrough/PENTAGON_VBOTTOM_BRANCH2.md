# The 45 v-bottom equations on level-15 branch 2

## Exact verdict

**A rational obstruction occurs at the next level.**
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

Branch 2 reconstructed the complete w-equations through level 15, so the
first 39 reduce to zero on the generic chart and on both exceptional divisors.
Carrying the six remaining equations into level 14 kills the rational generic
point

    c0=c1=a0=a3=1,
    a1=a2=a4=b3=...=b7=d1=...=d7=eta=theta=0,

where the omitted `b0,b1,b2,b8,kappa,d0` are fixed by the generic branch
formulas.  This point has `a0*F3=1` and solves every complete level 20 through
15.  Even with all six coefficients of the new `h3` row and the `D7` kernel
`iota` retained, level 14 gives

    [z] w14 = -63/32.

This is exactly the pending `V=-13,r^1` v-bottom equation.  It is independent
of all seven carried freedoms, so the point has no level-14 extension.  This
kills a genuine part of the surviving generic geometry, but not yet the whole
generic stratum or either exceptional stratum.

In particular, the deepest relation

    2 p_8,0 q_13,1 = 3 p_9,1 q_12,0

is the constant coefficient of w-level 20.  Its agreement with eighth-power
scaling is exact but supplies no independent existence evidence.

## Reproducer

`pentagon_vbottom_branch2.py` generates all 45 sparse bilinear equations,
checks the coefficient identity term by term, asserts the distribution above,
and prints the six genuinely pending equations.  It uses no random point,
finite-field specialization, division by `a0`, or division by `F3`.
`pentagon_level14_rational_obstruction.py` independently reconstructs the
rational point, checks levels 20 through 15 as polynomial identities, retains
the seven new freedoms, and evaluates the sparse v-equation separately.

## Exceptional strata status

The regrading argument is branch-independent, so it also settles the requested
v-bottom substitution on `a0=0` and `F3=0`: the same 39 equations vanish and
the same six await lower descent.  It does **not** complete their level-15
decomposition.  The exact level-15 equations still give:

* on `a0=0`, `C3=0` and
  `C4=15*a1*c1*(a1^2-4*c0*b2)^2/(16*c0^4)`, producing the shifted subcases
  `a1=0` and `a1^2=4*c0*b2`;
* on `F3=0`, `C3` and `C4` retain an `F2^2` factor, so the loci `F2=0` and
  `a0=a1=0` must remain separate before solving `C5,C6`.

Pentagon status remains **NO VERDICT**.  This is an exact rational obstruction
to one generic point, not an emptiness certificate for a full stratum and not
a planar Jacobian counterexample.
