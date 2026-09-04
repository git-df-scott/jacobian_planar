# Astra 3 — pentagon descent and the projective boundary

Date: 2026-09-04. Base: `e479477263c1f4176b287309dda2dcb4213fcb84`.
Branch: `astra/jc2-pentagon-geometry-2026-09-04`.

**Result: a computer-assisted characteristic-zero exclusion of GGHV
Proposition 4.3(1).** The proof combines an exact five-parameter reduction,
explicit finite-field certificates on both projective charts, and a valuation
argument. No counterexample or counterexample candidate was found.

Together with Astra 2, this excludes both polygons in Proposition 4.3,
and hence the original case called **(8,28)** in that proposition. It is not
a proof of JC2 or a claim about every other degree configuration. No priority
claim relative to the literature is made. The written argument and software
have not received external peer review or proof-assistant formalization.

## 1. The complete target

The primary source is GGHV,
[arXiv:2204.14178, Proposition 4.3](https://arxiv.org/pdf/2204.14178).
The pentagon requires

```
N(P) = conv{(0,0),(1,0),(8,14),(8,16),(0,8)},
N(Q) = conv{(0,0),(2,1),(12,21),(12,24),(0,12)},
{P,Q} = x^2.
```

With `T=xy^2`, write

```
P = sum(y^-r f_r(T), r=-8,...,2),
Q = sum(y^-s g_s(T), s=-12,...,3).
```

For r>=0, `deg f_r<=8`; for r<0, `deg f_r<=8+r`.
For s>=0, `deg g_s<=12`; for s<0, `deg g_s<=12+s`.
The positive levels f_1,f_2,g_1 are divisible by T, and g_2,g_3 by T^2.
The additive constants in f_0,g_0 can be removed. The independent convex-hull
check finds exactly 60 P and 124 Q nonconstant monomials in these windows.
It checks the bracket identity on every pair of basis monomials.

Let `C=f_2`, `G=g_3`. The leading equation is still

```
2 C G' - 3 C' G = T^2.
```

Normalize `C_1=G_2=C_2=1` as in
[Astra 2](ASTRA_2_CASE2_EXACT_DESCENT.md). Its five-dessin argument proves
that the saved irreducible quintic field accounts for all five leading
scaling orbits, including the exclusion of a missing C_2=0 chart. The prior
independent verifier was rerun successfully in this session.

## 2. The right edge supplies a necessary relation and one normalization

The coefficients at the highest x powers have the form

```
[x^8] P  = y^14 (c8+b8*y+a8*y^2),
[x^12] Q = y^21 (g12+d2*y+d1*y^2+d0*y^3).
```

The x^19 coefficient of the bracket vanishes. Consequently the square of
the cubic factor divided by the cube of the quadratic factor is constant.
Unique factorization, together with nonzero endpoint coefficients, gives

```
c8+b8*y+a8*y^2 = c8*(1+t*y)^2,
g12+d2*y+d1*y^2+d0*y^3 = g12*(1+t*y)^3,
t != 0.
```

There is exactly the needed residual source/output scaling:

```
P_b(x,y)=b^2 P(b^-2*x,b*y),
Q_b(x,y)=b^3 Q(b^-2*x,b*y).
```

It preserves `{P,Q}=x^2`, all supports, and the whole leading pair C,G.
It sends t to b*t. Setting b=1/t is therefore legitimate and imposes only

```
[T^8] f_1 = 2*c8,   [T^8] f_0 = c8.
```

The remaining right-edge Q coefficients then follow from the bracket.
This does not independently fix all six vertices or discard the residual
torus: it explicitly uses that torus once. Both P right-edge corners remain
nonzero. The other endpoint nonzero conditions are unnecessary for the
obstruction below, so omitting them only enlarges the tested system.

## 3. Five parameters, with every kernel retained

At each successive level r=1,0,-1,..., solve for `f=f_r`, `g=g_(r+1)`:

```
L_r(f,g) = 2 C g' -(r+1) C' g + r f G' -3 f' G = -H_r.
```

Here H_r uses only the levels already constructed. The coefficient matrix
depends on C,G, not on any unknown deformation parameter. Gaussian
elimination therefore divides only by fixed nonzero field elements.
Every free kernel coordinate is retained; every compatibility row becomes
an equation. No variable-dependent pivot, greedy particular lift, or
unjustified specialization is used.

After the right-edge normalization, the exact ranks are:

| r | Coefficients being solved | Rank | New free parameters | Weight |
|---|---:|---:|---:|---:|
| 1 | 18 | 17 | 1 | 1 |
| 0 | 19 | 18 | 1 | 2 |
| -1 | 20 | 18 | 2 | 3 |
| -2 | 19 | 18 | 1 | 4 |
| -3 | 17 | 17 | 0 | 5 |
| -4 | 15 | 15 | 0 | 6 |
| -5 | 13 | 13 | 0 | 7 |
| -6 | 11 | 11 | 0 | 8 |

Thus the necessary prefix through r=-6 depends on just five parameters,
with weights `(1,2,3,3,4)`. The unnormalized descent has seven free parameters.
Exact ranks were also computed for all remaining levels through r=-13.

There is a structural reason that further kernels disappear. For a homogeneous
solution let `S=2Cg-3fG` and `a=(r+3)/2`. Then

```
C S' - a C' S = -a f T^2.
```

For r<=-4, a nonzero S of degree j would force f to have degree j+5, with
nonzero leading factor `4*(r+3)-j`. This exceeds its bound 8+r, because
j>=0 and r+3<0. Thus S=f=g=0. For r=-3, S is constant; divisibility by T
forces S=0. Then `(C/T)` divides f, impossible for `deg f<=5` since
`deg(C/T)=7`. This explains the injectivity from r=-3 onward.

## 4. Homogenize before drawing a characteristic-zero conclusion

Restore a variable t in the two fixed right-edge coefficients:

```
[T^8] f_1 = 2*c8*t,   [T^8] f_0 = c8*t^2.
```

Give `(u1,u2,u3,u4,u5,t)` weights `(1,2,3,3,4,1)`.
Inductively every coefficient of f_r and g_(r+1), and every compatibility
equation at level r, is homogeneous of weight 2-r. This follows because
all coefficient operators are constant and the source products have that
same weight. The exact recurrence defines a homogeneous system over the
quintic field; its t=1 chart contains every normalized pentagon solution.

The verifier reconstructs this single homogeneous system through weight 8.
It specializes that same system to t=1 and t=0 and compares the generated
equations with the saved certificate inputs. Thus the boundary is checked
as part of the actual compactification, not as a separately guessed system.

## 5. Explicit certificates on both charts

Use p=32003 and the residue `C_8=26088` of the original quintic field.
On the chart t=1, nine compatibility equations through weight 7 have
explicit multipliers satisfying

```
sum(q_i*p_i, i=1,...,9) = 1  over F_32003[u1,...,u5].
```

At t=0, fourteen nonzero equations through weight 8 have explicit
certificates placing all the following powers in their ideal:

```
u1^9, u2^5, u3^3, u4^2, u5^3.
```

Therefore the affine chart is empty over the algebraic closure of F_32003,
and the only boundary zero is the zero vector. That vector is not a point of
weighted projective space. The whole projective special fiber is empty.
The exploratory boundary quotient has dimension zero and length 42, but the
proof relies on the five multiplied-out power identities, not that dimension
or length report.

The independent checker uses its own sparse polynomial arithmetic to
multiply all six certificates. It also checks altered-certificate controls,
the support and bracket reconstruction, all homogeneous weights, the rank of
every modular row-transformation matrix, and the exact coefficient reduction.
It does not invoke Singular.

## 6. Why this excludes characteristic zero

This is the essential step that an affine modular EMPTY result alone lacks.

Let K be the original irreducible quintic field. Its monic defining
polynomial has coefficients integral at p=32003 and has the specified
residue root. Every coefficient of C,G and every entry of every exact
row-reduction matrix through r=-6 is verified to be integral at this prime.
Their reductions agree entry by entry with the matrices used to generate
the modular system. All modular row transformations are invertible, hence
the corresponding exact transformations are invertible as well. The
recurrence uses only these constants, addition and multiplication, so all
homogeneous equations have good reduction at the chosen place of K.

Suppose a characteristic-zero solution existed. A nonempty finite-type
algebraic set over K has a point over a finite extension L of K, so it is
enough to consider algebraic parameter values. Extend the chosen valuation
to L and write the projective coordinates as `(u1,...,u5,1)`.

Let m be the minimum of `v(coordinate)/weight` among the nonzero
coordinates. After a finite ramified extension, choose lambda with
`v(lambda)=-m`. Weighted rescaling makes every coordinate integral and at
least one a unit. Homogeneity preserves all equations. Reducing gives a
nonzero projective solution over an algebraic extension of the residue field.

If the reduced t is nonzero, rescale it to 1; the affine unit certificate
gives a contradiction. If reduced t is zero, the five boundary power
certificates force every remaining coordinate to be zero, also a
contradiction. Thus no characteristic-zero solution exists.

The same argument applies to the abstract quintic-field model and hence to
all its conjugates. Astra 2 proves these are all leading scaling orbits.
This establishes the stated pentagon exclusion. It neither assumes that
an affine point survives reduction nor treats a modular failure as a
characteristic-zero result without controlling the boundary.

## 7. Replay

From the repository root, with Python and python-flint 0.9.0:

```
python astra/verify_case2_certificate.py
python astra/verify_pentagon_projective.py
```

The second command finishes with:

```
HOMOGENEOUS_SYSTEM_AND_BOTH_CHARTS: PASS
AFFINE_UNIT_CERTIFICATE: PASS
ALL_FIVE_BOUNDARY_POWER_CERTIFICATES: PASS
EXACT_FIELD_AND_ALL_OPERATOR_REDUCTIONS: PASS
```

The JSON report `astra/artifacts/pentagon_projective_verification.json`
records the certificate hashes, weights, support sizes and reduction checks.
To regenerate the modular certificates using Singular 4.3.1:

```
python astra/pentagon_descent.py --right-edge --stop-r -5 --defer-gb
Singular -q astra/pentagon_descent_modular_right_raw.sing
python astra/pentagon_descent.py --right-edge --stop-r -6 --defer-gb --boundary
Singular -q astra/pentagon_descent_modular_right_raw_boundary.sing
python astra/verify_pentagon_projective.py
```

## 8. Exploration, failures and remaining scope

The initial seven-parameter modular run timed out in an intermediate
positive-dimensional elimination. Right-edge normalization made the modular
obstruction fast. Three direct characteristic-zero elimination attempts
timed out; none is used as emptiness evidence.

PARI suggested the smaller field polynomial `a^5-a^4+3*a^3+3*a^2+26`.
FLINT independently verified its isomorphism and a T scaling that reduced
the largest stored leading coefficient from hundreds of characters to 26.
That improvement and the nine explicit exact compatibility polynomials are
preserved, but the successful proof uses the projective good-reduction route.
It does not depend on a completed characteristic-zero Groebner basis.

The earlier pentagon p_1_1=0 experiments and their retractions were read for
provenance; no sparse census, greedy lift, or six-vertex normalization was
reused. The old degree-1144 object is still not identified with this model.

All run classifications are in `astra/artifacts/pentagon_run_manifest.json`.
Large generated exact scripts are stored losslessly as `.sing.gz`; their
builder and the raw equations remain available. No runtime dependency or
credential is included in the research artifacts.

The next explicit-polynomial task is to reconstruct the published
above-125 chain `(8,28)->(7/4,3)`, `(m,n)=(3,4)`, from its primary definitions,
including the unprinted lower-corner issue. Its exponent ratio differs from
this completed (2,3) descent, so the present exclusion is not transferred to it.
