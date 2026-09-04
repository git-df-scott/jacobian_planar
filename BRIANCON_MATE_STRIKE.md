# Briançon mate strike

## Verdict

No Q is produced.  The two published degree-ten Briançon submersions are
closed by an exact all-degree period obstruction, and their natural
two-parameter boundary shows exactly why the obstruction cannot be removed
without leaving the all-fibres-irreducible class.

## Family and targets

Use

```
s=xy+1,  p=xs+1,  u=s^2+y,
P_(a,b)=p^2 u + a p s + b s.
```

The two targets are

```
g:       (a,b)=(-5/3,-1/3),
g-prime: (a,b)=(-7/9, 1/9).
```

### Gate 0 — no affine critical points

`astra/briancon_control.py` expands each degree-ten polynomial over Q and
computes the lexicographic Groebner basis of `(P_x,P_y)`.  Both bases are
exactly `[1]`.  Thus both gradient ideals are `(1)`.

### Gate 1 — non-coordinate

The cited exact geometry gives a compact genus-one completion of the t=1
fibre.  A coordinate polynomial has every fibre isomorphic to A1, whose smooth
completion has genus zero.  Therefore each target is non-coordinate.  This
criterion uses the published fibre theorem; it is not inferred from a failed
coordinate search.

### Gate 2 — fibre topology

Dimca--Sticlaru, arXiv:2406.19795, Theorem 1.7 and Propositions 3.3--3.4 are the
inputs used in the archived proof: the relevant fibres are irreducible, and
the t=1 completions have genus one.  ASTRA keeps these theorem inputs explicit
in the JSON certificate.

### Gate 3 — exact period obstruction

The identities

```
(p-1)u=s(sp-1),
Jac(s,p)=-(p-1)
```

give the cleared fibre

```
H_(a,b)=s^2p^3+(a-1)sp^2+(b-a)sp-bs-tp+t
```

and the Gelfand--Leray form

```
eta=ds/H_p=-dp/H_s.
```

At p=infinity the t=1 tangent equation is

```
lambda^2+(a-1)lambda-1=0.
```

For both rational targets it has two distinct nonzero roots and is coprime to
the leading denominator.  Eta has valuation zero on both branches.  At
s=infinity the weighted initial form is `p^3-bz`; since b is nonzero, there is
one branch and eta again has valuation zero.

Thus eta extends to a nonzero holomorphic differential on the compact
genus-one fibre.  It cannot equal dR: any pole of R would give a pole of dR,
while a pole-free rational function on a compact curve is constant.  Hence eta
has a nonzero period and neither polynomial has a rational or polynomial mate
in any degree.

### Natural family boundary

For rational a and nonzero b, the same t=1 boundary profile persists (the
tangent discriminant `(a-1)^2+4` is nonzero).  Every submersion member that
retains the cited irreducible genus-one fibre hypotheses therefore has the same
period obstruction.

The only simple boundary degeneration is b=0, where the exact factorization is

```
P_(a,0)=p(pu+as).
```

The zero fibre is reducible before the period obstruction can disappear.  This
is the recurring pole/reducible-fibre mechanism in exact form.

### Gates 4--6

They are not reached for `g` or `g-prime`: periods do not vanish, so no rational
primitive exists and there is no polar-part cancellation problem to test.

## Independent cusp-family control

The `codex/sol-session3-pole` `night24` producer and independent verifier were
both replayed.  For

```
P=p^2u+lambda sp^2+alpha p^2+beta p+gamma
```

the generic genus-one locus has eta with one double pole `2O`; Riemann--Roch
forces a primitive with at most one simple pole to be constant.  The
unimodular degeneration has an exact rational mate, but its exceptional fibre
factors and the primitive takes three unequal component constants, so the mate
has a noncancellable pole.  The family is closed `EXACT-ALL-DEGREES` under its
stated support hypotheses.

## Next construction address

The next family must change the divisor, not just coefficients:

1. retain gradient unimodularity and an irreducible positive-genus atypical
   fibre;
2. make eta second-kind with zero residues;
3. give its prospective primitive a pole divisor of degree at least three
   (for example `3O` or `2O1+2O2`);
4. kill the elliptic de Rham component exactly; and
5. only then solve global pole cancellation.

A concrete reverse-exactness ansatz is to choose a degree-two elliptic function
R, prescribe `eta=dR`, and solve the embedding/unimodularity equations.  Any
solution still must pass irreducibility and polynomialization independently.

Evidence: `astra/artifacts/briancon_control_2026-09-04.json`.  Current status:
no mate, no CEC, no CE.
