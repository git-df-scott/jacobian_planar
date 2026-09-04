# The off-by-one obstruction

## Exact budget equations

Let S have m components.  Write b_i for the number of branches of component
S_i above singular points, nu for total branch excess, n_i for fixed sheets of
a meridian, c_i for its nontrivial cycles, s_p for sheets fixed by the local
link group, and o_p for nontrivial local-group orbits.  The stratified-cover
calculation gives

```
chi(X) = D(1-m+nu) + sum_i n_i(1-b_i) + sum_p s_p,       (E)
chi(R) = sum_i c_i(1-b_i) + sum_p o_p.                   (R)
```

A plane Keller source requires `(E)=1`.  The refined Orevkov test requires each
connected dicritical component, with its singular points restored, to be one
copy of C with one place at infinity.  Thus `(R)` is not an optional diagnostic:
its local orbit data must decompose into line components.

This yields a useful theorem, though not a proof of JC2:

> **Euler--escape budget theorem.**  Fix D, the target component/branch data,
> meridian conjugacy classes, and the allowed local link-group spectra
> `(s_p,o_p)`.  If no joint choice in those spectra satisfies `(E)=1` and the
> componentwise line equations refining `(R)`, then no polynomial curve with
> that peripheral blueprint can be the non-properness curve of a plane Keller
> counterexample.

The statement follows before braid realization or coefficient algebra.  It is
an infinite-class exclusion whenever the peripheral group spectrum has already
been classified.

## Irreducible cusp/node form

For one irreducible S with C cusp points, N nodes, equal meridian fixed count n,
moved count e=D-n, and c nontrivial meridian cycles,

```
b = C+2N,  nu=N,
chi(X) = n(1-C) + N(e-n) + sum_p s_p,
chi(R) = c(1-C-2N) + sum_p o_p.                          (6)
```

Equation (6) isolates the tension: fixed-sheet orbits pay the source Euler
budget, while fusion of moved cycles pays the dicritical-line budget.  They are
two projections of the same local permutation actions and cannot be optimized
independently.

## H3: exactly one escaping orbit short

The independent group-first computation gives the unique six-sheet H3 class:

```
D=6, n=2, e=4, c=2,
C=2, N=1, b=4,
sum s_p = 1,
sum o_p = 2+1+3 = 6.
```

Consequently

```
chi(X) = 6 + 2(1-4) + 1 = 1,
chi(R) = 2(1-4) + 6 = 0.
```

The first budget is exact and the second is one below the minimum coarse line
budget used by the target screen.  The longitude-refined computation is
stronger: it produces two would-be components with Euler characteristics 0
and -1, so neither is a line.  This is a structural group-class exclusion, not
merely a failure of one parametrized curve.

The source bridge adds an independent bounded exclusion: the same cycle data
force discrepancy -1 dicriticals and no compatible coordinate divisor exists
on the archived trees through six blowups.

Adjunction makes the join still tighter.  The H3 escape components contribute
`-12` to the P-fibre Euler sum and `-20` or `-24` to the Q-fibre sum.  Every
non-escape horizontal boundary must contribute exactly +6 to each coordinate,
recovering target fibre Euler values `-6` and `-14/-18`.  Thus a deeper source
tree must solve a fixed weighted partition, not an open-ended degree search.

## A8: the opposite side

The audited four-strand `(5,5,3)+4 nodes` A8 families have the reverse coarse
profile:

```
chi(X)=0,  chi(R)=1.
```

Their escaping cycles can close with the right coarse Euler contribution, but
the source is one Euler unit short.  This is `BLUEPRINT` evidence only; no
general A8 nonrealizability theorem is claimed here.

## What can break the pattern

For a new blueprint to evade the observed obstruction, it must introduce at
least one mechanism that changes the joint local `(s,o)` spectrum, not just
more instances of the same singularity:

1. a higher-contact local group whose moved cycles gain a fusion orbit without
   adding the fixed sheets that spoil `(E)`;
2. non-involution meridians with a different moved-sheet/cycle ratio;
3. multiple target components with peripheral infinity monodromy coupling the
   local orbit decompositions;
4. a longitude pattern that changes componentwise line closure while retaining
   the coarse count; or
5. source boundary data at greater forced depth satisfying the discrepancy and
   coordinate intersection equations simultaneously.

This is the precise additional mechanism sought by the next group-first
search.  Adding arbitrary cusps, nodes, or blowups without changing one of
these quantities cannot address the deficit.

## Scope

The equations are theorems inside the stated stratified-cover and resolved
dicritical setup.  The empirical assertion that every possible S has an
off-by-one defect is **not** a theorem and is not asserted.
