# Exact obstructions outside the conductor algebra

Work over C, in characteristic zero. A Keller mate means
`J(P,Q)=P_x Q_y-P_y Q_x=1`; any nonzero constant is reduced to this case by
scaling Q. All rational functions are in the indicated full function field.

## 1. The birational chart and the time form

Set

```text
s=xy+1, p=xs+1, u=s^2+y.
(p-1)u=s(sp-1),  J(s,p)=-(p-1).
x=(p-1)/s, y=s(s-1)/(p-1).
```

Thus C(x,y)=C(s,p). For arbitrary R,A,C in C[p], consider

```text
P=R(p)u+sA(p)+C(p),
B=(p-1)A-R,
H=pR s^2+B s+(p-1)(C-t)=(p-1)(P-t),
w=2pR s+B,
w^2=D=B^2+4pR(p-1)(t-C).
```

The last equation holds on the generic fibre P=t, and gives a birational
quadratic model when R is nonzero and D is nonsquare. From
`dx wedge dy=-ds wedge dp/(p-1)` one obtains the exact time form

```text
eta=-dp/H_s=-dp/w.
```

If a rational mate exists, its restriction to the generic fibre has
derivative eta over C(t). A nonzero holomorphic differential on a smooth
compact curve is not the derivative of a rational function: any pole of
that function would give a pole of its derivative, and a globally regular
function on a compact curve is constant. This argument needs neither a
numerical period calculation nor irreducibility of every special fibre.

## 2. All exponents in the higher Briançon template

**Theorem 1.** For every integer m>=1 and A in C[p], the polynomial

```text
P=p^m*u+s*A(p)
```

has no polynomial Keller mate. If A(0)!=0, or if m=1, or if A has a simple
zero at 0, it has no rational Keller mate either.

**Proof.** Here

```text
B=(p-1)A-p^m,
D=B^2+4t*p^(m+1)*(p-1),
eta=-dp/w.
```

First assume A(0)!=0. Put g=4p^(m+1)(p-1). Then
`B(0)=-A(0)!=0`, `B(1)=-1`, so gcd(B,g)=1. D is squarefree over C(t): a
common root of D and D_p would be a root of the constant-coefficient
polynomial `g*(B^2)' - g'*B^2`. This polynomial is not identically zero,
since otherwise B^2/g would be constant, contrary to its odd pole/zero
order at p=1. Such a root must therefore be constant in C. The identity
`B(alpha)^2+t*g(alpha)=0` would then force B(alpha)=g(alpha)=0, impossible.

Also `deg_p D=max(2 deg B,m+2)>=3`; equality of the two degrees cannot
cancel their leading coefficients over C(t). The smooth compact model of
`w^2=D` has positive genus. The differential dp/w is holomorphic:
at a simple root of D use p-alpha=r^2; at infinity its order is g-1
at each of two points when deg D=2g+2, and 2g-2 at the single point
when deg D=2g+1. It is nonzero. Section 1 excludes a rational mate.

Now assume A(0)=0, and write A=p*A1 and B=p*B1. Then D=p^2*E and
`eta=-dp/(p*sqrt(E))`. If m=1, `E(0)=(A1(0)+1)^2-4t`, nonzero in C(t).
If m>=2 and A1(0)!=0, `E(0)=A1(0)^2`, also nonzero. On normalization the
two points over p=0 have nonzero residues `-1/sqrt(E(0))` and its negative.
A rational derivative has zero residue at every point, so no rational
mate exists. This local reasoning remains valid even if E has repeated
roots elsewhere.

The only case left is m>=2 and p^2 divides A. Then p^2 divides P in
C[x,y]. Its gradient vanishes along p=0, a nonempty curve (for example
(-1,0) lies on it). No polynomial mate is possible. This last step does
not claim that a rational mate is impossible for a polynomial with a
vanishing gradient. QED.

The published higher-degree family
`p^(2n)u+s*(sum_{j=0}^n a_j p^j+sum_{j=n+1}^{2n-1}p^j)` is a subfamily.
Its formula is from [Dimca–Sticlaru, Section 4, equation (4.1)](https://arxiv.org/html/2406.19795v1#S4). The theorem above supplies the
mate obstruction and is not a claim made in that source.

## 3. Introducing a pair of high-order poles does not repair this pencil

**Theorem 2 (varying hyperelliptic pencil).** Let a in C\{0,1}, k>=1,
and D0 in C[p] with L=deg D0>=3. On the smooth compact model over C(t) of

```text
w^2=D0(p)+4t*p*(p-1),
```

the differential `dp/((p-a)^k*w)` has no rational primitive. This holds
for every k and every D0 of the stated degree.

**Squarefreeness.** Let g=4p(p-1). If D and D_p have a common root, that
root satisfies `g D0'-g' D0=0`. This is a nonzero polynomial in C[p], with
leading coefficient `4(L-2)*lc(D0)`, so the root is constant. Comparing
coefficients of t in D=D_p=0 would give g=g'=0 there. But g is squarefree.
Thus the generic curve is smooth after normalization and has genus
`floor((L-1)/2)>=1`. Moreover D(a) is nonzero in C(t).

**Poles and ramification.** Write eta=dp/((p-a)^k*w). If k=1, its two
residues over p=a are nonzero, and the assertion follows. For k>=2,
eta has exactly two poles, each of order k. Any rational primitive Q
would consequently have exactly two poles, each of order k-1, and
degree n=2k-2 as a map of compact curves to P^1.

If L=2g+1 is odd, the unique infinity point has
`ord(eta)=2k+2g-2`. Thus Q would have local mapping degree
`2k+2g-1 > 2k-2=n` there. This is impossible.

Suppose L=2g+2 is even. There are two infinity points, each with
`ord(eta)=k+g-1`. At every other non-pole point eta is nonzero, including
finite branch points of p. Therefore the only possible finite critical
values of Q are its two values at infinity. The involution w->-w sends
eta to -eta; subtracting a constant makes Q odd. Its infinity values are
then b and -b. They cannot both be zero: Q would have zeros of total
order at least `2(k+g)>2k-2`, exceeding its degree. Consequently b!=0.
After division by b, Q is unramified away from {-1,1,infinity}.

For a fixed degree n there are only finitely many isomorphism classes
of connected compact covers with these three branch values. Indeed their
restrictions to the thrice-punctured sphere are determined by two
permutations in S_n up to conjugacy, and a topological cover carries a
unique pulled-back complex structure and unique compactification. There
are finitely many such permutation pairs. Hence existence of Q over
C(t) would force this family of compact source curves to be isotrivial.
One may specialize away from the finitely many bad parameters and
normalize the two critical values separately on each fibre; a rational
choice of b over C(t) is not required.

**The family is not isotrivial.** As t tends to infinity, two distinct
roots alpha_0,alpha_1 of D approach 0 and 1. This follows exactly from
the implicit function theorem for `g(p)+(1/t)D0(p)=0` at the two simple
roots of g. The other L-2 roots escape to infinity: any bounded limiting
root must be 0 or 1, and each already has its unique local branch.
Choose two escaping roots beta_1,beta_2, possible since even L>=4.
Their cross-ratio with the two finite roots satisfies

```text
lambda=((alpha_0-beta_1)*(alpha_1-beta_2))
       /((alpha_0-beta_2)*(alpha_1-beta_1)) -> 1.
```

On a local algebraic branch for large finite t it never equals 1,
because all four points are distinct. It is therefore nonconstant.
An isotrivial family of hyperelliptic curves cannot have this property:
for genus >=2 its degree-two map is unique up to PGL_2, so the finite
set of unordered branch cross-ratios is fixed. For genus 1 the same
conclusion follows from
`j=256*(1-lambda+lambda^2)^3/(lambda^2*(1-lambda)^2)` for its four branch
points: fixed j gives finitely many lambda. Thus isotriviality gives a
contradiction. This proves the even-degree case and the theorem. QED.

This use of limiting roots is a proof about exact algebraic curves, not
a formal approximation to a Keller pair. No truncation or numerical
period is used. The fixed-degree three-point-cover fact is also described
by the monodromy correspondence in [Sijsling–Voight, *On computing Belyi
maps*](https://www.numdam.org/item/10.5802/pmb.5.pdf).

**Polynomial corollary.** With s,p,u as in Section 1, let a!=0,1, k>=1,
T,C in C[p], and `T(1)=-(1-a)^k`. Write z=p-a and set

```text
P=z^(2k)*u+s*z^k*(z^k+T(p))/(p-1)+C(p).
```

The division is exact in C[p]. In Section 1, `R=z^(2k)` and `B=z^k*T`.
After dividing w by z^k the generic fibre is

```text
W^2=T^2+4p(p-1)(t-C), eta=-dp/(z^k*W).
```

If `deg(T^2-4p(p-1)C)>=3`, Theorem 2 excludes every rational mate and
therefore every polynomial mate. There is no restriction on deg T,
deg C, or k. Degree <=2, the exceptional positions a=0,1, and multiple
distinct pole locations are outside this corollary, not silently closed.

## 4. The first degree-six residual equations, independently

The elliptic case L=4, k=4 admits a small purely algebraic check, separate
from the all-degree proof. Put z=p-a and
`D=d0+d1*z+d2*z^2+d3*z^3+d4*z^4`, where d4!=0. An odd primitive with
only the permitted poles must be

```text
Q=((u*z+v)/z^3)*W.
```

The numerator is at most linear because Q is regular at both infinities;
at finite branch points odd regularity excludes additional poles. The
identity `dQ=-dz/(z^4*W)` is equivalent to exactly five equations:

```text
3*v*d0=1,
4*u*d0+5*v*d1=0,
3*u*d1+4*v*d2=0,
2*u*d2+3*v*d3=0,
u*d3+2*v*d4=0.
```

They force v,u,d3 nonzero and

```text
d2=3*d3^2/(4*d4),
d1=d3^3/(2*d4^2),
d0=5*d3^4/(16*d4^3).
```

For the pencil of Theorem 2, d3 and d4 are constant in t. These identities
would force d0,d1,d2 constant, contradicting the nonzero t coefficient
`4p(p-1)`. This eliminates the entire quartic k=4 residual system over
C(t), with no bounded coefficient search. The verifier checks both the
coefficient extraction and the displayed elimination parametrization.

## 5. A genuine exact degree-six primitive, and its failed reconstruction

The five equations do have solutions outside that varying pencil. Let

```text
D*(z)=(z^4-2z^3+3z^2-4z+5)/5,
W^2=t*D*(z),
Q=(z+1)*W/(3*t*z^3).
```

D* is squarefree. Its compact curve is elliptic. Direct differentiation
on t=constant gives `dQ=-dz/(z^4*W)` exactly. At the two points over z=0,
Q has pole order three and no other poles, so its generic degree is six.
The total field is rational because `t=W^2/D*(z)` and z,W are independent.
Thus this test retains an exact higher-genus primitive with a rational
total space, rather than rejecting all nontrivial period controls.

However, with r=1/z the following exact identity holds:

```text
t*Q^2=F(r),
F(r)=r^6/9+2r^5/15+1/45,
F'(r)=2r^4*(r+1)/3,
F(0)=1/45, F(-1)=0.
```

In any faithful birational plane chart where P=t and Q are polynomials,
r is rational and satisfies a monic polynomial over C[x,y] (multiply
`F(r)-P Q^2=0` by 9). Integral closure therefore makes r polynomial.
It is nonconstant, so the fibre r=0 is nonempty. At any point of that
fibre, P Q^2=1/45, hence Q!=0. Differentiating the identity there gives
`Q^2 dP+2P Q dQ=0`. A nonzero constant Jacobian makes dP,dQ linearly
independent at every point, a contradiction. This excludes all faithful
polynomial Keller realizations of this particular primitive.

The displayed rational chart itself has
`J_(z,W)(t,Q)=2/(z^4*D*(z))`, not a constant. No claim of a counterexample
is based on its rational two-form.

## 6. Mixed-power rigidity in every degree

**Theorem 3.** Let P,Q in C[x,y] have nonzero constant Jacobian. Suppose
r in C(x,y) is nonconstant, m,n>=1, and

```text
P^m Q^n=f(r), f in C[Z], deg f=d>=1.
```

Then r is polynomial, `f(Z)=c*(Z-b)^d` for c!=0, and d divides gcd(m,n).

**Proof.** Integral closure first makes r polynomial. If f'(b)=0 and
f(b)!=0, choose any point of r=b; such a point exists for every b since
a nonconstant polynomial minus a constant is not a unit in C[x,y].
At that point P,Q are nonzero. Differentiation gives

```text
0=m*P^(m-1)*Q^n*dP+n*P^m*Q^(n-1)*dQ,
```

contradicting independence of dP,dQ. All critical values of f therefore
equal zero. If f has s distinct roots of multiplicities e_1,...,e_s,
its derivative has exactly multiplicity e_i-1 at each such root. All
d-1 roots of f' must occur among these, so
`d-1=sum(e_i-1)=d-s` and s=1. This includes the linear case directly.
Hence f has the stated form.

P and Q are squarefree: a repeated irreducible factor would make the
respective gradient vanish along a curve. They are relatively prime:
a common irreducible factor would divide their Jacobian. Unique
factorization in `P^m Q^n=c*(r-b)^d` now implies d divides m and d divides n.
QED. No assertion of polynomial invertibility was used.

The hypotheses are sharp for the degree condition: the Keller pair
P=x,Q=y with m=n=2, r=xy, f(Z)=Z^2 is a valid control. For coprime m,n
the only possible d is one. Section 5 has (m,n,d)=(1,2,6), so it is also
excluded directly by this arbitrary-degree theorem.

## 7. What one collision does, and does not, reduce

For completeness, any actual noninjective Keller pair can be normalized
by an invertible affine source change to have a collision at (0,0),(1,0).
Translate the common target value to zero and scale one coordinate to
make the Jacobian one. The ideal of those two points is exactly
`(y,x(x-1))`: reducing modulo y gives the one-variable vanishing condition.
Conversely, a Keller pair in that ideal has the stated collision.

Thus this is a necessary-and-sufficient normalization of the general
counterexample problem. It supplies no global existence argument or finite
classification. In particular Theorems 1–3 do not close that ideal or JC2.
