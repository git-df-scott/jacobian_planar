# The complete monic height-(4,6) family is impossible

September 5, 2026. Independent audit of the lane inherited from
`session43/lane7/SOL5_COLLISION_FIRST.md`,
`session43/lane6/SOL6_COLLISION_FIRST.md`, and
`session43/lane6/lane6_report.md`. Base record: `efff2dc5c31a71030ccf931d22b9cd2047c0e172`.

**Theorem.** Over an algebraically closed field of characteristic zero, no
polynomials of the forms

\[
P=p_0(x)+p_1(x)y+p_2(x)y^2+p_3(x)y^3+p_4y^4,\qquad
Q=\sum_{j=0}^5q_j(x)y^j+q_6y^6,
\]

with constant nonzero `p4,q6`, have nonzero constant Jacobian.
The x-degrees are unrestricted. No collision normalization, fixed p0,
zero initial coefficients, or recurrence-chart condition is imposed.

This is an all-degree exclusion of this family, not of general JC2 pairs
or families with nonconstant leading y coefficients. The algebra is checked
by `verify_missed_routes.py`; the degree argument below is a written proof.
No literature-priority or external-review claim is made.

## 1. Complete reduction and three integrals

Scale P and Q to make their leading y coefficients one. The target bracket
becomes some constant `kappa != 0`. The polynomial symplectic substitution
`y=Y-p3(x)/4` depresses P. Write

\[
P=Y^4+aY^2+bY+c=(Y^2+a/2)^2+bY+d,\qquad d=c-a^2/4.
\]

Solving the coefficients of the original bracket at powers `Y^8` down
through `Y^3` determines all six lower Q coefficients with six arbitrary
constants `k0,...,k5`. Each step divides only by 4 and integrates a closed
polynomial one-form. It is complete because the difference of two solutions
at that step has derivative zero. Constants k0 and k4 do not enter the
remaining bracket. Put `h=k5, k=k3, ell=k2, m=k1`.

For a direct check without running code, the complete upper-row solution is

\[
\begin{aligned}
Q={}&Y^6+hY^5+\tfrac32aY^4+
 (\tfrac54ha+\tfrac32b+k)Y^3\\
&+(\tfrac38a^2+\tfrac54hb+\tfrac32c+\ell)Y^2\\
&+(\tfrac5{32}ha^2+\tfrac34ab+\tfrac34ka+\tfrac54hc+m)Y\\
&-\tfrac1{16}a^3+\tfrac5{16}hab+\tfrac34ac+
 \tfrac12\ell a+\tfrac38b^2+\tfrac34kb+k_4P+k_0.
\end{aligned}
\]

Here c=d+a^2/4 as above; all six constants are arbitrary.

The remaining three rows satisfy the exact identity

\[
\{P,Q\}=H_2'(Y^2+a/4)+H_1'Y+H_0',
\]

where primes differentiate after substitution of a(x),b(x),d(x), and

\[
32H_2=5ha^3+12ka^2+40had+32ma+20hb^2+96bd+64\ell b+96kd,
\]

\[
32H_1=-5ha^2b-24ab^2-24kab+40hbd+32mb+48d^2+64\ell d,
\]

\[
\begin{aligned}
512H_0={}&15ha^4+32ka^3+80ha^2d+64ma^2-160hab^2\\
&-384abd-256\ell ab-128b^3-192kb^2+320hd^2+512md.
\end{aligned}
\]

Therefore a Keller solution is equivalent to

\[
H_2=C_2,\qquad H_1=C_1,\qquad H_0=\kappa x+C_0. \tag{1}
\]

The old rows E2 and E1 were individually exact differentials. The third
becomes exact after subtracting `a E2/4`. This is why the coefficient-level
shooting problem hid a much smaller algebraic problem.

## 2. Degree proof: a constant

If a and b are constant, H1 constant forces d constant, by its nonzero
quadratic term in d. All H are then constant, impossible.

If a is constant and `B=deg b>0`, H1 constant forces `deg d<=B`:
otherwise its d-squared term has uniquely largest degree. In H0 the
term `-b^3/4` then has uniquely largest degree `3B`. This contradicts (1).
This covers every choice of h,k,ell,m when a is constant, including a=0.

Hence assume `A=deg a>0`. Constants or zero polynomials below are treated
separately; degree comparisons involving a positive degree are unaffected
by their omission.

## 3. Case h nonzero

If b is constant or `deg b<=A`, H1 forces `deg d<=3A/2`:
for a larger d-degree the d-squared term would be uniquely largest, including
against the bd term. Then `5ha^3` is uniquely largest in H2, impossible.

Thus `B=deg b>A`. In H1, cancellation of the largest terms forces

\[
D=\deg d=B+A/2.
\]

Indeed below this value the term `-24ab^2` is uniquely largest; above it,
`48d^2` is uniquely largest. In H2, bd now dominates ad, b-squared,
and the lower terms. Its only possible competitor is `5ha^3`, giving

\[
B=5A/4,\qquad D=7A/4,\qquad
b_Bd_D=-5h a_A^3/96.
\]

Here subscripted letters are nonzero leading coefficients. In H0 the only
terms of degree 4A are `15ha^4` and `-384abd`. Their combined leading
coefficient, after dividing by 512, is

\[
35h a_A^4/512\ne0.
\]

Thus `deg H0=4A>1`. In fact A must be a positive multiple of four, so the
degree is at least 16. Contradiction.

## 4. Case h=0 and k nonzero

If b is constant, H1 forces `deg d<=A/2`, and the term `12ka^2` in H2
is uniquely largest. This includes the cases b=0 and b=-k, where the
coefficient of a in H1 cancels and d must be constant. Hence B>0.

H1 forces `D=B+A/2`. In H2, the only possible leading cancellation is
between `12ka^2` and `96bd`. Therefore

\[
B=3A/4,\qquad D=5A/4,\qquad b_Bd_D=-k a_A^2/8.
\]

The degree-3A terms in H0 combine to `5k a_A^3/32 != 0`.
Thus `deg H0=3A`, at least 12 because A is a positive multiple of four.
Contradiction.

## 5. Case h=k=0 and m nonzero

For b constant, H1 again gives `deg d<=A/2`, while the term `32ma`
is uniquely largest in H2. Thus B>0. H1 forces `D=B+A/2`, and H2
then forces

\[
B=A/4,\qquad D=3A/4,\qquad b_Bd_D=-m a_A/3.
\]

The degree-2A terms in H0 combine to `3m a_A^2/8 != 0`.
Hence `deg H0=2A>=8`, again impossible.

## 6. Case h=k=m=0

Here there is a direct factorization:

\[
H_2=b(3d+2\ell)=C_2,\qquad
H_0=-aC_2/4-b^3/4.
\]

If C2 is nonzero, b and d must be constants because their product is a
unit of the polynomial ring; b is nonzero. H1 constant then forces a
constant. If C2=0, H0 is `-b^3/4`, of degree zero or a positive multiple
of three. Neither case gives degree one. This exhausts all constants.

## 7. Verification and implications

Run `python astra4/verify_missed_routes.py`. The first verification group:

- derives Q directly from the original bracket without importing campaign code;
- checks closedness, integration, and every upper row;
- checks the three displayed integrals and their identity;
- recomposes actual polynomial pairs with nonconstant cubic shears;
- checks deliberately perturbed pairs fail that identity;
- verifies all three noncancellation coefficients used above;
- preserves the genuine Keller control `(x+y^4,y)`, which is outside the sextic gate.

This supersedes the recommendation to shoot more points in the monic
height-(4,6) family. In particular, restoring its omitted initial values,
freeing p0, using extension fields, or increasing x-degree cannot rescue it.
The result does not impose the fixed collision points at any stage, so moving
those points under the depression shear causes no loss of generality.
