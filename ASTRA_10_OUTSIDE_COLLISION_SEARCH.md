# Astra 10 — a search outside the closed collision algebra

Date: 2026-09-05. Base: `1e591d8e0691db30958ebf7486db37c3ce2d812b`.
Branch: `astra/jc2-missed-routes-2026-09-05`.

**OPEN: no planar counterexample was obtained.** Astra 9's full obstruction
for the prescribed collision algebra remains in force. This run constructs
and rejects a genuinely exact degree-six elliptic primitive, and proves two
further arbitrary-degree family obstructions. None is a reduction of JC2 to
one remaining component, and no such reduction is claimed.

## What was tried and established

1. **The higher Briançon template cannot work in any degree.** With
   `s=xy+1`, `p=xs+1`, `u=s^2+y`, every
   `P=p^m*u+s*A(p)`, `m>=1`, `A in C[p]`, has no polynomial Keller mate.
   If `A(0)!=0`, the stronger conclusion is no rational mate: its time form
   is a nonzero holomorphic differential on a compact hyperelliptic curve.
   The omitted coefficient cases are covered separately by residues or a
   vanishing gradient. This includes the entire higher-degree template
   displayed in Section 4 of Dimca–Sticlaru, not just its two degree-ten
   examples. It does not classify all Briançon-type polynomials.
2. **A family designed to introduce poles also fails in arbitrary degree.**
   For `a!=0,1`, `k>=1`, and arbitrary polynomials `T,C` with
   `T(1)=-(1-a)^k`, put `z=p-a` and

   ```text
   P=z^(2k)*u+s*z^k*(z^k+T(p))/(p-1)+C(p).
   ```
   The quotient is polynomial. If
   `deg(T(p)^2-4p(p-1)C(p))>=3`, this P has no rational Keller mate.
   Its time form has exactly the intended pair of poles. Exactness would
   make the compact fibres three-point covers of bounded degree and hence
   isotrivial. Their branch cross-ratios demonstrably vary. This is an
   invariant argument for all k and all coefficient degrees, not exhaustion.
3. **An exact primitive really does survive the period test.** On

   ```text
   W^2=t*(z^4-2z^3+3z^2-4z+5)/5,
   Q=(z+1)*W/(3*t*z^3),
   ```
   one has `dQ=-dz/(z^4*W)` on each generic fibre. Q has degree six there.
   The total function field is rational, so this is more than an abstract
   differential on an unrelated curve. However, it satisfies

   ```text
   t*Q^2 = r^6/9+2r^5/15+1/45,  r=1/z.
   ```
   If t and Q were a polynomial Keller pair in a faithful plane chart,
   integral closure would make r polynomial. At r=0, differentiating this
   identity contradicts the nonzero Jacobian. This kills this exact model
   in every birational plane chart, not only the displayed chart.

The last argument extends to a reusable theorem: if P,Q is a polynomial
Keller pair, r is rational and nonconstant, m,n are positive integers, and
`P^m Q^n=f(r)` with f a nonconstant polynomial, then
`f(Z)=c*(Z-b)^d` and `d` divides `gcd(m,n)`. In particular a coprime mixed
power cannot be a nontrivial polynomial in a rational function.

## Evidence and scope

- [Complete proofs](astra10/PROOFS.md), including all excluded special cases.
- [Exact verifier](astra10/verify.py) and
  [its generated certificate](astra10/certificate.json).
- [Search and proof audit](astra10/SEARCH_AND_AUDIT.md).

Run `python astra10/verify.py` from the repository root. The computations
verify algebraic identities, the quartic residual system, and positive and
negative controls. The all-degree conclusions additionally use the written
curve and divisor arguments. They are not proof-assistant formalized and
have not received external peer review.

## What remains unresolved

No new polynomial P passed the exact global mate test. In particular, there
is no verified pair with both nonzero constant Jacobian and a collision.
The open construction problem must escape the three families/identities
above: merely increasing the Briançon exponent, increasing the order of one
pair of poles, or using this mixed-power elliptic primitive cannot do it.
Multiple pole locations or a different primitive identity are not excluded
by these results; neither is asserted to contain a counterexample.

Imposing only one collision is universal, but not itself a solution: after
affine source normalization and target translation, an actual noninjective
pair would have P,Q in `(y,x(x-1))` and `J(P,Q)=1`. Unlike the old conductor
algebra, this condition does not impose identification along an entire
curve. No finite parametrization of all such Keller pairs has been found.

The published above-125 Newton-chain translation problem also remains
unrepaired. This run did not reopen its compiler outputs or perform generic
coefficient sweeps, conductor lifts, modular searches, or numerical shooting.

**Final status: OPEN.** This is a substantive negative search result, not the
requested counterexample and not a solution of the general conjecture.
