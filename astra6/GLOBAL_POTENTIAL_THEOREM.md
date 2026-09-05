# Exact global polynomial-potential criterion

Work over C, in A=C[v,c]. Put r=3cv-2, D=r^2-9c and
B=C[b,c]+DA, where b=-3cv^2+4v+2. The conductor/parity theorem in
`astra4/LOCALIZATION_AND_CONDUCTOR.md` is used throughout:

    f in B <=> f(3(r+2)/r^2,r^2/9) is even in r.

All assertions below concern finite polynomials, not completions.

## Necessary and sufficient test

For H in A set

    A_H=H_v, C_H=H_c+v,
    g=gcd(A_H,C_H), X_H=C_H partial_v-A_H partial_c.

Choose any nonzero constant normalization of the gcd. It always exists:
A_H and C_H cannot both vanish identically. There is a polynomial Keller
pair in B giving this potential, up to reciprocal constant rescaling of
the two coordinates, **if and only if**

    H+2r/3 in B,                 (1)
    g in B,                     (2)
    X_H(g)=g.                   (3)

This is also an existence equivalence: B contains a Keller pair if and
only if a polynomial H satisfies (1)--(3). In particular the conditions
do not merely filter necessary leading terms.

Proof. Write alpha=A_H/g, beta=C_H/g. Direct differentiation gives

    alpha_c-beta_v=(-g-A_H g_c+C_H g_v)/g^2.

Thus (3) is precisely closedness of the polynomial form
alpha dv+beta dc. Every closed polynomial one-form on affine two-space
has a polynomial primitive Q: integrate alpha in v, then integrate the
remaining polynomial in c. Moreover

    J(g,Q)=(C_H g_v-A_H g_c)/g=1.

It remains to prove Q in B, which is redundant as a separate test. On
D=0 write p=g|D, q=Q|D and k=(H+2r/3)|D. Then

    p q'=k'+4/(3r).             (4)

The right side is odd, and p is even. The case p=0 is impossible:
the derivative of a Laurent polynomial has zero residue, whereas
4/(3r) has nonzero residue. Hence q' is odd, so the Laurent polynomial
q is even. This proves sufficiency, including collision membership.

Conversely, J(P,Q)=1 makes P dQ-v dc closed, with a polynomial primitive
H. Since Q_v and Q_c generate the unit ideal (use the Jacobian identity),
gcd(PQ_v,PQ_c) is a constant multiple of P. Conditions (2),(3) follow.
On D the functions p,q are even. Also

    v dc = (2/3+4/(3r)) dr.

The even part of H' is therefore -2/3, so H+2r/3 has even trace.
This proves (1) and necessity. QED.

In the single variable z=r^2, (4) is

    p(z) q_z(z)=k_z(z)+2/(3z).

The residue condition is included in the exact test; it is not a
replacement for (3). The vector field X_H has divergence 1, and (3)
says that its actual polynomial gcd is an eigenfunction with eigenvalue
1. An arbitrary Darboux factor is not sufficient.

## Consequences and equivalences

For a passing potential, g is squarefree, its gradient generates the
unit ideal, and distinct irreducible factors of g have disjoint zero
sets. Each assertion follows directly from J(g,Q)=1; a repeated factor,
a critical point, or an intersection of two factors would contradict it.

Adding a constant to H is immaterial. The replacement Q -> Q+f(P)
changes H by a polynomial R(P) with R'(P)=P f'(P). Thus R has no linear
term. Conversely every such R comes from a polynomial target shear.
Reciprocal constant rescaling (P,Q)->(lambda P,lambda^-1 Q) preserves H.
General polynomial target automorphisms of determinant 1 preserve B and
the collision. These are valid equivalences, but no assertion that they
classify all passing potentials is made. Source changes require the
collision algebra to be transported; they cannot silently redefine B.

If m=deg_v P,n=deg_v Q are positive, then

    deg_v H=m+n,
    [v^(m+n)]H = n/(m+n) [v^m]P [v^n]Q.

This follows from H_v=P Q_v and is exact, without a genericity condition.
For total degree p+q>2 the same formula holds for the highest homogeneous
parts. For c-degree it holds when both component c-degrees are positive
and their sum exceeds 2, because H_c=P Q_c-v. The degree filtration used
in this strike is v-degree, with completely unbounded c-degree.

## Controls and the lowest degrees

For a quadratic potential

    H=a v^2/2+b0 vc+d c^2/2+e v+f c+h0,

the two affine polynomials H_v,H_c+v have a nonconstant common factor
exactly when the matrix

    [[a,b0,e],[b0+1,d,f]]

has rank one. Its three minors are
ad-b0(b0+1), af-e(b0+1), b0 f-ed. Rank zero is impossible.
When rank one holds, (3) holds and the reconstructed pair is affine.
Otherwise g=1 and (3) fails. Since B in total degree at most two is
span{1,c,c^2}, admissibility forces H=F(c)-2cv+constant here; the first
minor is -2. There are no passing admissible quadratic potentials.

The infinite family H=F(c)+lambda b-2cv, for arbitrary polynomial F,
also has gcd 1. For lambda=0 this is immediate. Otherwise
H_v=-2(lambda r+c) is irreducible. On its zero set
v=(2lambda-c)/(3lambda c), divisibility of H_c+v would require

    F'(c)=4lambda/(3c^2)-2/(3c),

which is not polynomial. This includes all admissible cubic potentials.

The exact gate accepts ordinary polynomial Keller maps in A, for example
(c,-v), (c+v^2,-v), and a composition of two triangular automorphisms.
It correctly excludes them from B. These are positive controls for
closedness and reconstruction, not purported collision examples.

The Astra 5 deceptive family is rejected globally. Its putative limit
satisfies c(Q+v)^2=1. At the prime c, the left valuation is odd for every
rational Q+v, so no rational, hence no polynomial, limit exists. Equivalently,
a polynomial mate of P=c must be Q=-v+f(c), which fails even trace. No
additional D-adic orders are calculated in this strike.

The supplied verifier checks these identities and reconstructs the
positive controls. It does not enumerate all polynomials H.
