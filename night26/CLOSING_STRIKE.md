# NIGHT26 closing strike

## Outcome

No counterexample was obtained.  The run does produce a new minimal surviving
primitive-first mechanism at field degree 6 and reduces it to one exact
rational Darboux/affine-modification problem.  This is classified **GO**, not
CE: no polynomial pair is being claimed.

The prime-degree audit is separate in `PRIME_DEGREE_AUDIT.md`.  It kills the
Moskowicz all-primes proof but confirms by independent older work that degrees
3, 4, and 5 must not be searched.  Degree 6 is minimal.

## Exact degree-six primitive model

On the total rational surface `A2_(u,r)`, put

```
t = r^2 + 2*u^2*r,                 R = r^3.
```

On the generic `t`-fibre, set `w=2ru`.  Then

```
C_t:  w^2 = 2*t*r - 2*r^3.
```

Its cubic has discriminant `64*t^3`, so over `Q(t)` it is a smooth genus-one
curve.  The point at infinity is `O`; write `B0=(0,0)` and let `B+`, `B-` be
the two geometric points with `r^2=t,w=0`.  Standard Weierstrass valuations
give

```
(r)       = 2*B0 - 2*O,
(dr)      = B0 + B+ + B- - 3*O,
(R)_inf   = 6*O,
(dR)      = 5*B0 + B+ + B- - 7*O.
```

Thus `dR=3r^2 dr` is exact by construction and has the minimal pole order
associated with this degree-six primitive.

The intended extension really has degree 6.  Over `Q(t,R)`, `r` satisfies
`z^3-R`, irreducible by Eisenstein at `R`.  After adjoining `r`,

```
u^2 = (t-r^2)/(2r).
```

The right side is not a square in `Q(t,r)`, because it has valuation one at
the prime `t-r^2`.  Hence the tower has degree `3*2=6`.

The tower has the visible involution `u -> -u`, but the full extension is not
Galois.  After extending constants to contain a cube root of unity `zeta`, a
cubic rotation `r -> zeta*r` would have to send `u` to a square root with
radicand `(t-zeta^2*r^2)/(2*zeta*r)`.  Its ratio to the original radicand has
odd valuations at the distinct divisors `t-zeta^2*r^2` and `t-r^2`, hence is
not a square in `C(t,r)`.  The rotation therefore does not extend.  The
quadratic/Galois Keller theorem used in NIGHT25 does not apply to the full
degree-six extension.  No claim is made that the residual involution is
harmless; it is an explicit condition that any future boundary construction
must survive.

Finally,

```
dt wedge dR = 12*u*r^3 du wedge dr.
```

This zero divisor is the design datum for the missing plane chart, not a
Keller identity in `(u,r)`.

## Why this is not another triangular control

The two finite critical divisors are geometrically informative:

- `u=0` maps as `(t,R)=(r^2,r^3)`, the cusp `R^2=t^3`;
- `r=0` is contracted to `(0,0)`.

Any faithful Keller plane chart must move both divisors into its boundary.
The cusp is compatible with the known one-place-at-infinity condition for a
nonproper value curve; see Nguyen Van Chau,
[*Non-proper value set and Jacobian condition*](https://arxiv.org/abs/math/0305088).
No cited nonproperness theorem here rules it out.

There cannot be a **regular polynomial birational intermediate map**
`G:A2_(u,r)->A2_(x,y)`.  For a birational morphism between smooth normal
surfaces, a divisor in the Jacobian zero locus is exceptional (a
nonexceptional divisor is generically an isomorphism at its codimension-one
point).  Thus `u=0` would be contracted by `G`.  But both pullbacks `t=r^2`
and `R=r^3` vary there, contradicting `t=P(G), R=Q(G)`.  A solution must be a
genuinely rational affine modification with `u=0` in its indeterminacy or
boundary.

Toric rational charts are also exactly impossible.  If

```
x=c1*u^a*r^b,   y=c2*u^c*r^d
```

generate the function field and have the required volume form, exponent
matching gives `a+c=2`, `b+d=4`.  Their lattice determinant is then

```
a*d-b*c = 4*a-2*b,
```

which is even and cannot be `+1` or `-1`.  The checker audits a large range,
but the displayed parity identity is the proof for all integer exponents.

## A killed affine-modification control

The nearby split-quartic surface does polynomialize its genus-one fibres.
With

```
P=2*y+x^4*y^2,       Y=1+x^4*y,
```

one has `Y^2=1+P*x^4`.  However `P_y=2Y`, so its Gelfand–Leray differential
is `-dx/(2Y)` up to orientation.  On the smooth projective quartic model this
is a nonzero holomorphic differential.  It is therefore not exact.  This
control shows that an affine modification can solve polynomiality and genus
while still failing the primitive requirement; it is not a CE candidate.

## Precise remaining construction equation

Find `x,y in Q(u,r)` satisfying all four conditions:

1. `Q(x,y)=Q(u,r)` (faithfulness);
2. `t=r^2+2u^2r` and `R=r^3` lie in `Q[x,y]`;
3. `dx wedge dy = 12*u*r^3 du wedge dr`;
4. the rational chart boundary contains both `u=0` and `r=0`.

Then the resulting polynomials `P(x,y)=t` and `Q(x,y)=R` would obey
`[P,Q]=1`, have field degree 6, and—because an automorphism has field degree
1—would be a genuine JC2 counterexample.  The remaining equation is narrow
and exact: construct or obstruct a non-toric affine modification realizing a
specified log-volume form while polynomializing two fixed functions.

No explicit `P,Q in Q[x,y]` were found, so the binding CE gate is not passed.

## Adversarial verdict

- Hidden genus drop: absent; cubic discriminant is `64*t^3 != 0` generically.
- Wrong intended degree: absent; independent cubic and quadratic witnesses
  give degree 6.
- Exactness confusion: absent; `R=r^3` is explicit.
- Triangular/coordinate collapse: no realization exists yet; regular and
  monomial birational realizations are separately obstructed.
- Hidden finite ramification: present in `(u,r)` and explicitly required to
  move to the boundary; this is the remaining risk, not a solved condition.
- Polynomiality/reverse lift: unsolved and therefore no CE claim is made.
- Theorem collision: degree `<=5` results do not apply; the nonproper cusp is
  not excluded by the audited necessary condition; the visible involution
  does not make the entire degree-six extension Galois.

**Strategic classification: GO.**
