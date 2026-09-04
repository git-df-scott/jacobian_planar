# Target/source compatibility

## Result

The target meridian data and source compactification data meet through a local
identity at every dicritical component.  Applying it to the unique H3
six-sheet blueprint and solving the full coordinate complementarity problem on
the archived 11,465 boundary records gives:

> **EXACT-Q, bounded.**  Through six boundary blowups, the H3 bidegrees (3,5)
> and (3,6) admit no compatible P-coordinate divisor and no compatible
> Q-coordinate divisor.  Hence there is no joint target/source survivor in
> that tree list.

This is stronger than the earlier degree-two source sweep for this one target,
but it is not an unbounded exclusion.

## Joint discrete object

| target | source | linking datum |
|---|---|---|
| geometric degree D | intersection matrix M | `D=m dot dQ=n dot dP` |
| target component S_i | boundary component E | `E -> S_i` |
| meridian moved sheets e_i | discrepancy k_E | `r_E=1-k_E` |
| moved cycles c_i | tangential degree d_E | `c_i=sum d_E` |
| parametrization bidegree (alpha_i,beta_i) | horizontal degrees dP_E,dQ_E | `(dP_E,dQ_E)=d_E(alpha_i,beta_i)` |
| local fixed/orbit counts | singular hits on E | Euler and line conditions |
| monodromy at infinity | boundary graph and pole orders | peripheral/intersection equations |

Here `m_E=-ord_E(P)` and `n_E=-ord_E(Q)` on pole components, while
`k_E=-ord_E(dx wedge dy)` is the archived discrepancy convention.

## Keller escape bridge

Take a generic smooth point of S_i and local target coordinates `(u,v)` with
`S_i={u=0}`.  At a source dicritical E, choose resolved local coordinates
`(z,t)` with `E={z=0}`.  In characteristic zero the generic tangential map is
unramified, so locally

```
u = unit * z^r_E,
v = phi(t) + higher z terms,
```

with `phi` of degree d_E and nonzero generic derivative.  Therefore

```
ord_E(F*(du wedge dv)) = r_E - 1.
```

The Keller identity makes this equal to `ord_E(dx wedge dy)=-k_E`, hence

```
r_E = 1-k_E.                                      (1)
```

A generic point of S_i has d_E preimages on E.  Each supplies one meridian
cycle of length r_E.  Summing over the source components above S_i gives

```
c_i = sum_E d_E,
e_i = sum_E d_E r_E = sum_E d_E(1-k_E).           (2)
```

If the normalization parametrization of S_i has coordinate degrees
`(alpha_i,beta_i)`, composition gives

```
dP_E = alpha_i d_E,
dQ_E = beta_i d_E.                                (3)
```

Equations (1)--(3) are generic statements; singular points are handled by the
separate local-orbit and longitude data.

## Source intersection equations

For a resolved boundary with intersection matrix M, coordinate pole vectors
m,n and horizontal degree vectors dP,dQ satisfy

```
M m = dP,
M n = dQ,
m,n,dP,dQ >= 0,
m_E dP_E = n_E dQ_E = 0,                          (4)
D = m dot dQ = n dot dP,
delta_E = m_E+n_E+1-k_E >= 0.                    (5)
```

The complementarity in (4) is essential: a component cannot simultaneously
be a pole of a coordinate and carry a finite nonconstant value of it.

For a fixed set where m vanishes, (4) reduces to the kernel of a principal
submatrix of M.  `astra/joint_blueprint.py` enumerates all such zero sets,
solves them over Q, scales by the target-forced degrees (3), checks integrality,
then applies (5).  No degree bound or support-size bound is imposed.

## Positive control

For the identity map, blow up the two distinct coordinate base points on the
line at infinity.  The exact data are

```
self intersections = (-1,-1,-1)
k                  = (3,2,2)
m                  = (1,0,1),  dP=(0,1,0)
n                  = (1,1,0),  dQ=(0,0,1)
D                  = 1
delta              = (0,0,0).
```

The solver recovers both coordinate solutions.  A mismatched target
moved-sheet count is rejected by the bridge control.

## H3 specialization

The group-first replay fixes

```
D=6, c=2 moved cycles, e=4 moved sheets,
meridian cycles=(2,2), target bidegree=(3,5) or (3,6).
```

Thus every source component over S has `r_E=2` and therefore `k_E=-1`.
The tangential degrees partition c=2 in exactly two ways:

```
one E of degree 2; or two E's of degree 1.
```

Their forced horizontal degrees are respectively `(6,10)/(6,12)` or two
copies of `(3,5)/(3,6)`.  On the 11,465 generated records through six
blowups, 557 records contain a discrepancy -1 component and 654 placements of
these partitions are possible.  Exact principal-kernel enumeration returns
zero P-coordinate solutions and zero Q-coordinate solutions for both target
bidegrees.  No higher-dimensional principal-kernel case was skipped.

The certificate is `astra/artifacts/joint_blueprint_2026-09-04.json`.

## Next forced step

Do not merely run seven or eight blowups.  First derive a lower bound from the
principal-kernel equations: a discrepancy -1 dicritical carrying horizontal
degree 3d must be separated from the positive direction of M by enough pole
components to support a nonnegative isotropic coordinate divisor.  Enumerate
the next depth only after that recurrence fixes the admissible skeletons.
