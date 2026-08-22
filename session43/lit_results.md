# Literature check results (2026-08-22)

## TASK 1: arXiv:2608.00222 (Path E abort-check E1)

**Paper EXISTS and is fetchable.**
Title: "Counterexamples to the Jacobian conjecture in dimensions greater than two"
Author: Shuhong Gao. arXiv:2608.00222.

Abstract (as returned by fetch, verbatim): "The Jacobian conjecture, open since 1939, asks whether every polynomial map of C^n whose Jacobian determinant is a nonzero constant must have a polynomial inverse. It was refuted in dimension three by Alpöge on July 19, 2026, with an infinite family by Gallagher (July 20) and a geometric explanation by Speyer (July 23): the counterexample sweeps the tangent lines of a plane curve --- a map that classical duality forces to hit most points several times. We give a self-contained account of this tangent-sweep mechanism and generalize it from plane curves to direction fields on hypersurfaces. The resulting construction produces counterexamples in every dimension greater than two and, in each dimension, of arbitrarily large geometric degree (the number of preimages of a typical point). We work it out in five new explicit maps: one three-dimensional of degree four, two four-dimensional of degrees five and ten, and two five-dimensional of degrees six and twelve. The counterexamples provide explicit examples of etale coverings C^n -> C^n that are not proper: they are everywhere unramified, and fail to be injective only through points escaping to infinity. All identities were verified in exact rational arithmetic; an appendix determines exact fiber structures through Gröbner bases."

### (a) Mechanism
VERDICT: YES — it is explicitly the tangent-sweep mechanism, generalized. The paper self-describes as "a self-contained account of this tangent-sweep mechanism," generalized "from plane curves to direction fields on hypersurfaces." Core form (per HTML fetch of v1): a "padded sweep"
  F0(x, gamma, w) = (gamma*x, X(w) + gamma*Delta(w))
with tangency criterion det(Delta, J(X)) = 0, then det J(F0) = gamma * det(Delta, J(X) + gamma J(Delta)) = sum_k L_k gamma^{k+1}; after monomial conjugation + twisting by divisibility, constant Jacobian is achieved. So: same family as "Phi = sum s^i C_i(t)" tangent-sweep generalization — NOT a different mechanism.

### (b) Arbitrary geometric degree; d=2?
Geometric degree = number of roots of a "tangency polynomial" W_{X,Y}(w) = q(w) + (w/2)(X - p(w)) - Y; sweeping a plane curve of degree d gives tangency polynomial of degree d+1, hence generic fiber d+1. Degree grows by taking higher-degree base curves / direction fields. d=2 does NOT occur: the fetch reports the paper notes degree-2 (geometric degree 2) is impossible — consistent with the classical fact that a Keller map of geometric degree 2 would be invertible (and Wang's deg<=2 theorem is cited in this connection). [CAVEAT: the "no d=2" reasoning was paraphrased by the fetch model; the cited reason (Wang) concerns algebraic degree <=2 of the map, not geometric degree — treat the precise exclusion argument as UNVERIFIED wording, but the paper's explicit examples start at geometric degree 3 (Alpöge) / 4 (this paper's 3D example).]

### (c) C*-equivariance
The paper's construction carries an explicit weighted/graded discrete-data structure (weights d_j on parameters w_j, twist exponents e_i on outputs, monomial degrees m_j on source variables, with sum_j m_j = sum_i e_i and sum_j d_j + (k+1) = sum_i e_i). Fetch reports "explicit weighted structure, though not global homogeneity." I could NOT verify a verbatim claim of C*-equivariance of the final maps; treat as LIKELY graded/quasi-equivariant by construction but UNVERIFIED as a stated theorem.

### Explicit small member (3D, geometric degree 4, Theorem 3.5 per fetch)
G = (gamma*x, (p(w) + 2*gamma)/(gamma*x)? ...) — as reported by the fetch:
  G = ( gamma*x,  (p(w)+2gamma)/(gamma x),  (q(w)+gamma w)/(gamma x)^2 )^T
with
  p(w) = w^3 - 6w^2 + 6w
  q(w) = (3/8)w^4 - 2w^3 + (3/2)w^2
  gamma = 2 - 4xy - x^2 z
  w = gamma*(1 + xy)
and det J(G) = 2 identically, geometric degree 4.
**VERIFIED SYMBOLICALLY (sympy, this session): G2 and G3 are genuinely polynomial in (x,y,z) after cancellation, and det J(G) = 2 identically.** This member is safe to feed to the quotient-descent computation. (Expand G2 = cancel((p(w)+2*gamma)/(gamma*x)), G3 = cancel((q(w)+gamma*w)/(gamma*x)^2) with the substitutions above.)

### Alpöge's original map (recounted in Sec. 3.4 of 2608.00222; Theorem 3.3)
  f1 = (1+xy)^3 z + y^2 (1+xy)(4+3xy)
  f2 = y + 3x(1+xy)^2 z + 3x y^2 (4+3xy)
  f3 = 2x - 3x^2 y - x^3 z
det J = -2 identically. **VERIFIED SYMBOLICALLY (sympy, this session): det J(f) = -2.**
(Announced informally July 19 2026, not as a traditional arXiv paper; Alpöge credited Akhil Mathew with suggesting the problem and Claude with assisting. Gallagher gave an infinite family July 20; Speyer's geometric explanation July 23: "one sweeps the tangent lines of a plane curve — a map that is unavoidably many-to-one, by projective duality." Terry Tao's digestion post exists at terrytao.wordpress.com 2026/07/21 but returned HTTP 403 to this agent's proxy.)

Paper also states (per fetch): "In dimension two, Moh verified the conjecture for maps of degree at most 100; the two-dimensional case remains open."

### Dimension-two remark
The paper (per fetch) does not give a 2D obstruction theorem; the mechanism needs the extra "padding" dimension (sweep of a curve family lives naturally in >=3 variables); no analogous construction is claimed in the plane.

